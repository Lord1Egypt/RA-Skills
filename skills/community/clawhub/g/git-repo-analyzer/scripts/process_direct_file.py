#!/usr/bin/env python3
"""Queue a direct file link for async processing instead of immediate download."""
import sys, json, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queue_utils import append_to_queue


def queue_link(url: str, subtype: str = "unknown"):
    entry = f"- [直链文件]({url}) - {subtype}"
    result = append_to_queue(entry)
    return {
        "action": "queue",
        "url": url,
        "type": subtype,
        "pendingPath": result["pendingPath"],
    }


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    subtype = sys.argv[2] if len(sys.argv) > 2 else "unknown"

    if not url:
        print(json.dumps({"error": "URL required"}), file=sys.stderr)
        sys.exit(1)

    try:
        result = queue_link(url, subtype)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
