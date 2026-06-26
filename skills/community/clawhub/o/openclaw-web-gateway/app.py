from flask import Flask, render_template

from config import (
    APP_SUBTITLE,
    APP_TITLE,
    DEFAULT_USER,
    GOOGLE_MAPS_EMBED_API_KEY,
    HOST,
    OPENCLAW_BASE,
    OPENCLAW_TOKEN,
    PORT,
    USERS,
)
from routes.chat import chat_bp
from routes.state import state_bp


app = Flask(__name__)
app.register_blueprint(chat_bp)
app.register_blueprint(state_bp)


@app.route("/")
def index():
    return render_template(
        "index.html",
        app_title=APP_TITLE,
        app_subtitle=APP_SUBTITLE,
        openclaw_base=OPENCLAW_BASE,
        token_loaded=bool(OPENCLAW_TOKEN),
        default_user=DEFAULT_USER,
        users=USERS,
        google_maps_embed_api_key=GOOGLE_MAPS_EMBED_API_KEY,
    )


@app.route("/favicon.ico")
def favicon():
    return ("", 204)


if __name__ == "__main__":
    print(f"{APP_TITLE} running on http://127.0.0.1:{PORT}")
    app.run(host=HOST, port=PORT, debug=False)
