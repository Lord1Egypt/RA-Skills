"""Entry point for intent-engine server."""
from intent_classifier.api import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5700, debug=True)
