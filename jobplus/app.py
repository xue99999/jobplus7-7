from flask import Flask
from jobplus.config import configs
from jobplus.models import db, User
from flask_login import LoginManager
from flask_migrate import Migrate


def register_blueprints(app):
    from .handlers import front, user, company, job
    app.register_blueprint(front)
    app.register_blueprint(job)
    app.register_blueprint(user)
    app.register_blueprint(company)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    return app

