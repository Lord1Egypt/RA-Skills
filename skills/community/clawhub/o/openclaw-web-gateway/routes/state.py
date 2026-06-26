from flask import Blueprint, jsonify, request

from state_manager import load_state, save_state


state_bp = Blueprint("state", __name__)


@state_bp.route("/api/state", methods=["GET"])
def api_get_state():
    return jsonify(load_state())


@state_bp.route("/api/state", methods=["POST"])
def api_post_state():
    save_state(request.get_json(silent=True) or {})
    return jsonify({"ok": True})
