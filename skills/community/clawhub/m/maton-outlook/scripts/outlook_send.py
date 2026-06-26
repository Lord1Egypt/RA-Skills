#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

BASE = "https://gateway.maton.ai/outlook/v1.0"


def api_post(path: str, payload: dict):
    key = os.environ.get("MATON_API_KEY")
    if not key:
        raise SystemExit("MATON_API_KEY is required")
    url = f"{BASE}{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode("utf-8", "ignore")
        if body:
            print(body)
        else:
            print(f"HTTP {r.status}")


def parse_recipients(items):
    out = []
    for item in items:
        out.append({"emailAddress": {"address": item}})
    return out


def build_message(args):
    msg = {
        "subject": args.subject,
        "body": {
            "contentType": "Text",
            "content": args.body,
        },
        "toRecipients": parse_recipients(args.to),
    }
    if args.cc:
        msg["ccRecipients"] = parse_recipients(args.cc)
    if args.bcc:
        msg["bccRecipients"] = parse_recipients(args.bcc)
    return msg


def cmd_draft(args):
    payload = build_message(args)
    api_post("/me/messages", payload)


def cmd_send(args):
    payload = {
        "message": build_message(args),
        "saveToSentItems": True,
    }
    api_post("/me/sendMail", payload)


def build_parser():
    p = argparse.ArgumentParser(description="Outlook / Maton helper for drafting and sending mail")
    sub = p.add_subparsers(dest="command")

    def add_common(sp):
        sp.add_argument("--to", nargs="+", required=True, help="One or more recipient addresses")
        sp.add_argument("--cc", nargs="*", default=[], help="Optional CC addresses")
        sp.add_argument("--bcc", nargs="*", default=[], help="Optional BCC addresses")
        sp.add_argument("--subject", required=True, help="Mail subject")
        sp.add_argument("--body", required=True, help="Plain text body")

    s = sub.add_parser("draft", help="Create a draft message")
    add_common(s)
    s.set_defaults(func=cmd_draft)

    s = sub.add_parser("send", help="Send a message immediately")
    add_common(s)
    s.set_defaults(func=cmd_send)

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
