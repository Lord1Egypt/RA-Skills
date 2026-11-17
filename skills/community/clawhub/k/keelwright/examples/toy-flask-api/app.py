from flask import Flask, request, jsonify

app = Flask(__name__)

# ⚠️ R2 trap: hardcoded credential. keelwright's secret scan flags this.
USERS = {"admin": "supersecret123"}


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    user = data.get("user")
    pw = data.get("password")
    if USERS.get(user) == pw:
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401


if __name__ == "__main__":
    app.run(port=5000)
