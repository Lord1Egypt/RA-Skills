"""Flask REST API for intent classification."""
import os
from flask import Flask, request, jsonify, send_from_directory

from .engine import IntentEngine
from .storage import IntentStore

# Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    static_url_path="",
)

store = IntentStore()
engine = IntentEngine(store)


# --- Static UI ---
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# --- Classification ---
@app.route("/api/classify", methods=["POST"])
def classify():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    multi = data.get("multi", False)
    threshold = data.get("threshold", 0.3)
    top_k = data.get("top_k", 5)

    if not text:
        return jsonify({"error": "text is required"}), 400

    if multi:
        results = engine.classify_multi(text, threshold, top_k)
        return jsonify({
            "input": text,
            "results": [r.to_dict() for r in results],
            "count": len(results),
        })

    result = engine.classify(text, top_k)
    if result is None:
        return jsonify({"input": text, "result": None, "message": "No intent matched"})

    return jsonify({"input": text, "result": result.to_dict()})


@app.route("/api/classify/batch", methods=["POST"])
def classify_batch():
    data = request.get_json(silent=True) or {}
    texts = data.get("texts", [])
    if not texts:
        return jsonify({"error": "texts array required"}), 400
    results = engine.classify_batch(texts)
    return jsonify({"results": results})


@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(silent=True) or {}
    cases = data.get("cases", [])
    if not cases:
        return jsonify({"error": "cases array required"}), 400
    return jsonify(engine.evaluate(cases))


# --- Intent CRUD ---
@app.route("/api/intents", methods=["GET"])
def list_intents():
    only = request.args.get("enabled_only", "false").lower() == "true"
    intents = [i.to_dict() for i in store.get_all(enabled_only=only)]
    return jsonify({"intents": intents, "count": len(intents)})


@app.route("/api/intents", methods=["POST"])
def create_intent():
    data = request.get_json(silent=True) or {}
    required = ["name", "category", "sub_category"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    intent = store.create(data)
    return jsonify({"intent": intent.to_dict()}), 201


@app.route("/api/intents/<intent_id>", methods=["GET"])
def get_intent(intent_id):
    intent = store.get(intent_id)
    if not intent:
        return jsonify({"error": "Intent not found"}), 404
    return jsonify({"intent": intent.to_dict()})


@app.route("/api/intents/<intent_id>", methods=["PUT"])
def update_intent(intent_id):
    data = request.get_json(silent=True) or {}
    intent = store.update(intent_id, data)
    if not intent:
        return jsonify({"error": "Intent not found"}), 404
    return jsonify({"intent": intent.to_dict()})


@app.route("/api/intents/<intent_id>", methods=["DELETE"])
def delete_intent(intent_id):
    if store.delete(intent_id):
        return jsonify({"ok": True})
    return jsonify({"error": "Intent not found"}), 404


# --- Stats & Meta ---
@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(store.stats())


@app.route("/api/categories", methods=["GET"])
def categories():
    return jsonify({
        "categories": [
            {"key": "CODE", "label": "代码类", "icon": "\U0001f4bb", "color": "#3b82f6"},
            {"key": "KNOW", "label": "知识类", "icon": "\U0001f4da", "color": "#8b5cf6"},
            {"key": "TASK", "label": "任务类", "icon": "\u2699\ufe0f", "color": "#f59e0b"},
            {"key": "CHAT", "label": "闲聊类", "icon": "\U0001f4ac", "color": "#10b981"},
        ]
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "2.0.0", "name": "intent-engine"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5700, debug=True)
