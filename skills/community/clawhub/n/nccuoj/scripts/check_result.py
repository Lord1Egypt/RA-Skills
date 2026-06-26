#!/usr/bin/env python3
"""
Check submission result on NCCUOJ.

Usage:
  python check_result.py <submission_id> --username <user> --password <pass>
  python check_result.py <submission_id> --username <user> --password <pass> --poll

Output: JSON submission data to stdout.
"""

import argparse
import json
import sys
import time
import os

sys.path.insert(0, os.path.dirname(__file__))
from session import get_session, api_get, api_post, API_URL

RESULT_MAP = {
    -2: "Compile Error",
    -1: "Wrong Answer",
    0: "Accepted",
    1: "Time Limit Exceeded",
    2: "Memory Limit Exceeded",
    3: "Runtime Error",
    4: "System Error",
    6: "Pending",
    7: "Judging",
    8: "Partial Accepted",
}

PENDING_RESULTS = {6, 7}


def login(opener, cookie_jar, username, password):
    api_post(opener, cookie_jar, f"{API_URL}/login", {
        "username": username,
        "password": password,
    })


def fetch_result(opener, submission_id):
    data = api_get(opener, f"{API_URL}/submission?id={submission_id}")
    result_code = data.get("result")
    data["result_text"] = RESULT_MAP.get(result_code, f"Unknown ({result_code})")
    return data


def main():
    parser = argparse.ArgumentParser(description="Check NCCUOJ submission result")
    parser.add_argument("submission_id", help="Submission ID")
    parser.add_argument("--username", required=True, help="NCCUOJ username")
    parser.add_argument("--password", required=True, help="NCCUOJ password")
    parser.add_argument("--poll", action="store_true", help="Poll until judging completes (max 60s)")
    args = parser.parse_args()

    opener, cookie_jar, csrf = get_session()
    login(opener, cookie_jar, args.username, args.password)

    if args.poll:
        deadline = time.time() + 60
        while time.time() < deadline:
            data = fetch_result(opener, args.submission_id)
            if data.get("result") not in PENDING_RESULTS:
                break
            print(f"Status: {data['result_text']}... waiting", file=sys.stderr)
            time.sleep(2)
    else:
        data = fetch_result(opener, args.submission_id)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
