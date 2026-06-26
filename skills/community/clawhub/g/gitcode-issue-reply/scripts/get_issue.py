#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch a single GitCode issue (title + body). No comments, no DeepWiki.
Usage: python get_issue.py --issue-url "https://gitcode.com/owner/repo/issues/123"
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from _common import get_token, parse_issue_url, api_get, init_windows_encoding, print_json


def main():
    parser = argparse.ArgumentParser(description="Fetch one GitCode issue (title + body)")
    parser.add_argument("--issue-url", required=True, help="Full issue URL")
    parser.add_argument("--token", help="GitCode API token (optional, will use GITCODE_TOKEN env var if not provided)")
    args = parser.parse_args()
    init_windows_encoding()
    token = get_token(args.token)
    if not token:
        print_json({"error": "GITCODE_TOKEN not set"})
        sys.exit(1)
    try:
        owner, repo, number = parse_issue_url(args.issue_url)
    except ValueError as e:
        print_json({"error": str(e)})
        sys.exit(1)
    try:
        issue = api_get(token, f"repos/{owner}/{repo}/issues/{number}")
    except Exception as e:
        print_json({"error": str(e)})
        sys.exit(1)
    # Output only fields needed for CVE/description
    out = {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "body": issue.get("body"),
        "state": issue.get("state"),
        "html_url": issue.get("html_url"),
        "created_at": issue.get("created_at"),
        "user": issue.get("user"),
        "labels": issue.get("labels"),
    }
    print_json(out)


if __name__ == "__main__":
    main()
