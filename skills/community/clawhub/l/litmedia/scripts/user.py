#!/usr/bin/env python3
"""Query LitMedia account credit balance and usage history.

Usage:
    python user.py credit [--json]
    python user.py logs [--type TYPE] [--start TIME] [--end TIME] [--page N] [--size N] [--json]
"""

import argparse
import json as json_mod
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))

from typing import Any, Optional
from shared.client import LitMediaClient, TaskStatus

CREDIT_PATH = "/user/credit/detail"

TASK_TYPES = [
    "image",
    "video",
]

HISTORY_ENDPOINTS = {
    "image": "/lit-video/get-image-history",
    "video": "/lit-video/get-video-history",
}

def cmd_credit(client: LitMediaClient, args):
    result = client.get(CREDIT_PATH)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        credit = result.get("credit", result)
        print(f"Credit balance: {credit}")


def cmd_logs(client: LitMediaClient, args):
    payload = {
        "page": str(args.page),
        "page_size": str(args.size),
        **({"start_time": args.start} if args.start else {}),
        **({"end_time": args.end} if args.end else {}),
    }
    LOGS_PATH = HISTORY_ENDPOINTS[args.type]
    result = client.post(LOGS_PATH, json=payload)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
        return

    page_no = args.page
    page_size = args.size

    if not args.quiet:
        print(
            f"Page {page_no} | {len(result)} items",
            file=sys.stderr,
        )

    if not result:
        print("No records found.")
        return

    if args.type == "image":
        print_image_history(result)
    elif args.type == "video":
        print_video_history(result)


def print_image_history(result: Optional[dict] = None):
    header = f"{'Date':<16} {'TaskID':<8} {'St':<10} {'ImageURL'}"
    print(header)
    print("-" * len(header))

    for entry in result:
        create_id = entry.get("create_id")
        ts = entry.get("create_at")
        status = TaskStatus(entry.get("status"))
        error = entry.get("error", "")
        image_urls = entry.get("image_urls", [])

        # 时间格式化
        date = datetime.datetime.fromtimestamp(ts).strftime("%y-%m-%d %H:%M") if ts else ""

        # 截断 error
        error_short = (error[:22] + "...") if len(error) > 25 else error

        # 只取第一张图
        image_url = image_urls[0] if image_urls else error_short

        print(f"{date:<16} {create_id:<8} {status.label:<10} {image_url}")

def print_video_history(result: Optional[dict] = None):
    header = f"{'Date':<16} {'TaskID':<8} {'St':<10} {'VideoURL'}"
    print(header)
    print("-" * len(header))

    for entry in result:
        create_id = entry.get("create_id")
        ts = entry.get("create_at")
        status = TaskStatus(entry.get("status"))
        error = entry.get("error", "")
        video_url = entry.get("video_url", [])

        # 时间格式化
        date = datetime.datetime.fromtimestamp(ts).strftime("%y-%m-%d %H:%M") if ts else ""

        # 截断 error
        error_short = (error[:22] + "...") if len(error) > 25 else error

        # 只取第一张图
        video_url = video_url if video_url else error_short

        print(f"{date:<16} {create_id:<8} {status.label:<10} {video_url}")


def main():
    parser = argparse.ArgumentParser(
        description="LitMedia account credit management."
    )
    parser.add_argument("--json", action="store_true",
                        help="Output full JSON response")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress status messages on stderr")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("credit", help="Query credit balance")

    logs_p = sub.add_parser("logs", help="Query credit usage history")
    logs_p.add_argument("--type", default=None, choices=TASK_TYPES,
                        help="Filter by task type")
    logs_p.add_argument("--start", default=None,
                        help="UTC start time (yyyy-MM-dd)")
    logs_p.add_argument("--end", default=None,
                        help="UTC end time (yyyy-MM-dd)")
    logs_p.add_argument("--page", type=int, default=1,
                        help="Page number (default: 1)")
    logs_p.add_argument("--size", type=int, default=20,
                        help="Items per page (default: 20)")

    args = parser.parse_args()
    client = LitMediaClient()

    if args.command == "credit":
        cmd_credit(client, args)
    elif args.command == "logs":
        cmd_logs(client, args)


if __name__ == "__main__":
    main()
