#!/usr/bin/env python3
"""
JSON encoding helper for Coral Bricks persistent-agent-memory skill.
Encodes stdin as JSON string, validates metadata, or formats API responses.
Used by coral_store, coral_retrieve, coral_delete_matching.
"""
import json
import sys


def encode_string() -> None:
    """Read stdin, output JSON-encoded string."""
    print(json.dumps(sys.stdin.read()))


def validate_metadata() -> None:
    """Read stdin as JSON, output dict as JSON or {} if invalid."""
    try:
        val = json.load(sys.stdin)
        if isinstance(val, dict):
            print(json.dumps(val))
        else:
            print("{}")
    except (json.JSONDecodeError, TypeError):
        print("{}")


def format_store_response() -> None:
    """Parse Memory API store response, output status JSON."""
    raw = sys.stdin.read()
    try:
        d = json.loads(raw)
        if "error" in d or "detail" in d:
            print(json.dumps(d))
        else:
            print(json.dumps({"status": d.get("status", "success")}))
    except (json.JSONDecodeError, TypeError):
        print(raw)


def format_retrieve_response() -> None:
    """Parse Memory API search response, output results JSON."""
    raw = sys.stdin.read()
    try:
        d = json.loads(raw)
        results = d.get("results", [])
        out = [
            {"text": r.get("text", ""), "score": r.get("score", 0)}
            for r in results
        ]
        print(json.dumps({"results": out}))
    except (json.JSONDecodeError, TypeError):
        print(raw)


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--metadata":
        validate_metadata()
    elif mode == "--store-response":
        format_store_response()
    elif mode == "--retrieve-response":
        format_retrieve_response()
    else:
        encode_string()


if __name__ == "__main__":
    main()
