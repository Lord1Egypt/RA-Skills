#!/usr/bin/env python3
"""
Post inline review comments from a JSON file to a GitLab MR.

Usage:
    python post_comments.py <mr_url> <comments.json>

comments.json format:
    [
        {"file_path": "src/main/Foo.java", "line": 42, "body": "..."},
        ...
    ]

This script avoids shell escaping issues that arise when passing comment
bodies with backticks or special characters via `python -c`.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gitlab_client import post_bulk_comments  # noqa: E402


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    mr_url = sys.argv[1]
    comments_file = sys.argv[2]

    with open(comments_file, encoding="utf-8") as f:
        comments = json.load(f)

    results = post_bulk_comments(mr_url, comments)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
