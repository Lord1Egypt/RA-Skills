#!/usr/bin/env python3
"""Handle paper/docs Git repos: queue the link for async processing."""
import sys, json, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queue_utils import append_to_queue


def queue_link(url: str, repo_name: str, item_type: str = "paper"):
    entry = f"- [{repo_name}]({url}) - {item_type}"
    result = append_to_queue(entry)
    return {
        "action": "queue",
        "repoName": repo_name,
        "url": url,
        "type": item_type,
        "pendingPath": result["pendingPath"],
    }


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    repo_name = sys.argv[2] if len(sys.argv) > 2 else "repo"

    if not url or not repo_name:
        print(json.dumps({"error": "URL and repo_name required"}), file=sys.stderr)
        sys.exit(1)

    try:
        result = queue_link(url, repo_name, item_type="paper")
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
