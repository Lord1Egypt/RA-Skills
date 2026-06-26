from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .client import GmailNoSend
from .auth import authenticate


def _read_body(body: str | None, body_file: str | None) -> str:
    if body_file:
        return Path(body_file).read_text()
    if body is None:
        raise SystemExit("--body or --body-file is required")
    return body


def main():
    parser = argparse.ArgumentParser(prog="gmail-no-send")
    sub = parser.add_subparsers(dest="cmd", required=True)

    auth = sub.add_parser("auth", help="Authenticate with Gmail")
    auth.add_argument("--client-secret", required=True)
    auth.add_argument("--account", required=True)
    auth.add_argument("--force", action="store_true")

    search = sub.add_parser("search", help="Search messages")
    search.add_argument("--account", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--max", type=int, default=20)

    read = sub.add_parser("read", help="Read message")
    read.add_argument("--account", required=True)
    read.add_argument("--message-id", required=True)

    dcreate = sub.add_parser("draft-create", help="Create draft")
    dcreate.add_argument("--account", required=True)
    dcreate.add_argument("--to", required=True)
    dcreate.add_argument("--subject", required=True)
    dcreate.add_argument("--body", required=False)
    dcreate.add_argument("--body-file", required=False)

    dupdate = sub.add_parser("draft-update", help="Update draft")
    dupdate.add_argument("--account", required=True)
    dupdate.add_argument("--draft-id", required=True)
    dupdate.add_argument("--to", required=True)
    dupdate.add_argument("--subject", required=True)
    dupdate.add_argument("--body", required=False)
    dupdate.add_argument("--body-file", required=False)

    archive = sub.add_parser("archive", help="Archive message")
    archive.add_argument("--account", required=True)
    archive.add_argument("--message-id", required=True)

    args = parser.parse_args()

    if args.cmd == "auth":
        authenticate(args.client_secret, args.account, force=args.force)
        print("ok")
        return

    client = GmailNoSend(account=args.account)

    if args.cmd == "search":
        print(json.dumps(client.search(args.query, args.max), indent=2))
    elif args.cmd == "read":
        print(json.dumps(client.read(args.message_id), indent=2))
    elif args.cmd == "draft-create":
        body = _read_body(args.body, args.body_file)
        print(json.dumps(client.create_draft(args.to, args.subject, body), indent=2))
    elif args.cmd == "draft-update":
        body = _read_body(args.body, args.body_file)
        print(json.dumps(client.update_draft(args.draft_id, args.to, args.subject, body), indent=2))
    elif args.cmd == "archive":
        print(json.dumps(client.archive(args.message_id), indent=2))
    else:
        raise SystemExit("unknown command")


if __name__ == "__main__":
    main()
