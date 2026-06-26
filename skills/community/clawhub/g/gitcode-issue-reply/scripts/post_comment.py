#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post a single comment to a GitCode issue.

Usage:
  python post_comment.py --issue-url "https://gitcode.com/owner/repo/issues/123" --body "text"
  python post_comment.py --issue-url "..." --body-file "/tmp/body.txt"
"""

import sys
import argparse
from pathlib import Path
from urllib.error import HTTPError

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from _common import get_token, print_json, parse_issue_url, api_post, init_windows_encoding


def main():
    parser = argparse.ArgumentParser(description="Post a comment to a GitCode issue")
    parser.add_argument("--issue-url", required=True, help="Full issue URL")
    parser.add_argument("--token", help="GitCode API token (optional, will use GITCODE_TOKEN env var if not provided)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="Comment body text")
    group.add_argument("--body-file",
                       help="Path to a UTF-8 text file containing the comment body")
    args = parser.parse_args()

    init_windows_encoding()

    body = args.body
    if args.body_file:
        bf = Path(args.body_file)
        if not bf.is_file():
            print_json({"status": "error", "message": "body-file not found: " + args.body_file})
            sys.exit(1)
        body = bf.read_text(encoding="utf-8").strip()
    if not body:
        print_json({"status": "error", "message": "Comment body is empty"})
        sys.exit(1)

    token = get_token(args.token)
    if not token:
        print_json({"status": "error", "message": "GITCODE_TOKEN not configured"})
        sys.exit(1)

    try:
        owner, repo, number = parse_issue_url(args.issue_url)
    except ValueError as e:
        print_json({"status": "error", "message": str(e)})
        sys.exit(1)

    path = f"repos/{owner}/{repo}/issues/{number}/comments"
    try:
        api_post(token, path, {"body": body})
        print_json({"status": "posted", "owner": owner, "repo": repo, "issue_number": number})
    except HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print_json({"status": "error", "message": f"API {e.code}: {body_err}"})
        sys.exit(1)


if __name__ == "__main__":
    main()
