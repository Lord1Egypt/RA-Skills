#!/usr/bin/env python3
"""
Submit code to NCCUOJ.

Usage:
  python submit.py <problem_internal_id> <language> <code_file> --username <user> --password <pass>
  python submit.py <problem_internal_id> <language> <code_file> --username <user> --password <pass> --contest <contest_id>

Examples:
  python submit.py 42 "C++" solution.cpp --username alice --password secret
  python submit.py 42 "Python3" solution.py --username alice --password secret --contest 5
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from session import get_session, api_post, API_URL


def login(opener, cookie_jar, username, password):
    api_post(opener, cookie_jar, f"{API_URL}/login", {
        "username": username,
        "password": password,
    })


def main():
    parser = argparse.ArgumentParser(description="Submit code to NCCUOJ")
    parser.add_argument("problem_id", type=int, help="Problem internal ID (numeric)")
    parser.add_argument("language", help='Language name (e.g. "C++", "Python3")')
    parser.add_argument("code_file", help="Path to source code file")
    parser.add_argument("--username", required=True, help="NCCUOJ username")
    parser.add_argument("--password", required=True, help="NCCUOJ password")
    parser.add_argument("--contest", type=int, help="Contest ID (for contest submissions)")
    args = parser.parse_args()

    with open(args.code_file, "r") as f:
        code = f.read()

    opener, cookie_jar, csrf = get_session()
    login(opener, cookie_jar, args.username, args.password)

    payload = {
        "problem_id": args.problem_id,
        "language": args.language,
        "code": code,
    }
    if args.contest:
        payload["contest_id"] = args.contest

    data = api_post(opener, cookie_jar, f"{API_URL}/submission", payload)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
