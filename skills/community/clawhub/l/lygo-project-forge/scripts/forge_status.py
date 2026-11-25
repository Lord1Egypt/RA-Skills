"""Read a local LYGO Project Forge desk. Prints public status only."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8796/api/status"
KEEP = ("ok", "brand", "version", "hermes", "store", "account")


def main() -> int:
    try:
        with urllib.request.urlopen(URL, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print("Forge desk is not answering on http://127.0.0.1:8796")
        print(type(exc).__name__)
        return 1
    if not isinstance(payload, dict):
        print("Forge status was not an object")
        return 1
    out = {key: payload.get(key) for key in KEEP}
    brain = payload.get("brain") if isinstance(payload.get("brain"), dict) else {}
    out["brain_label"] = brain.get("label")
    out["brain_model"] = brain.get("model")
    out["brain_tier"] = brain.get("tier")
    out["brain_ready"] = brain.get("ready")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
