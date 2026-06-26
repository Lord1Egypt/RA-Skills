#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

BASE = "https://gateway.maton.ai/outlook/v1.0"


def api_get(path: str):
    key = os.environ.get("MATON_API_KEY")
    if not key:
        raise SystemExit("MATON_API_KEY is required")
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def cmd_profile(_args):
    data = api_get("/me")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_recent(args):
    top = args.top
    path = f"/me/messages?$top={top}&$select=subject,receivedDateTime,from,isRead,webLink"
    data = api_get(path)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_unread(args):
    top = args.top
    path = f"/me/messages?$top={top}&$filter=isRead eq false&$select=subject,receivedDateTime,from,isRead,webLink"
    data = api_get(path)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_inbox(args):
    top = args.top
    path = f"/me/mailFolders/Inbox/messages?$top={top}&$select=subject,receivedDateTime,from,isRead,webLink"
    data = api_get(path)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_get(args):
    msg_id = urllib.parse.quote(args.message_id, safe='')
    select = "subject,from,toRecipients,ccRecipients,receivedDateTime,bodyPreview,isRead,webLink"
    if args.full:
        select = "subject,from,toRecipients,ccRecipients,receivedDateTime,body,bodyPreview,isRead,webLink"
    path = f"/me/messages/{msg_id}?$select={select}"
    data = api_get(path)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_search(args):
    query = urllib.parse.quote(f'"{args.query}"')
    top = args.top
    path = f"/me/messages?$top={top}&$search={query}"
    data = api_get(path)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description="Outlook / Maton helper for common read-only tasks")
    sub = p.add_subparsers(dest="command")

    s = sub.add_parser("profile", help="Show mailbox profile")
    s.set_defaults(func=cmd_profile)

    s = sub.add_parser("recent", help="List recent messages")
    s.add_argument("--top", type=int, default=5)
    s.set_defaults(func=cmd_recent)

    s = sub.add_parser("unread", help="List unread messages")
    s.add_argument("--top", type=int, default=10)
    s.set_defaults(func=cmd_unread)

    s = sub.add_parser("inbox", help="List inbox messages")
    s.add_argument("--top", type=int, default=10)
    s.set_defaults(func=cmd_inbox)

    s = sub.add_parser("get", help="Read one message")
    s.add_argument("message_id")
    s.add_argument("--full", action="store_true", help="Fetch full body")
    s.set_defaults(func=cmd_get)

    s = sub.add_parser("search", help="Search messages")
    s.add_argument("query")
    s.add_argument("--top", type=int, default=10)
    s.set_defaults(func=cmd_search)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        raise SystemExit(2)
    try:
        args.func(args)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        print(body, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
