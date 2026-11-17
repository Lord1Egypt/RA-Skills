"""LightPage communication commands, with private persistent retry receipts."""

import hashlib
import json
import sys
import uuid
from pathlib import Path

from echo_cli.compat import subparsers
from echo_cli.credentials import atomic_json
from echo_cli.user_ids import user_reference


def commands(root):
    author = root.add_parser(
        "author", help="Find the current author of a work URL; no login required"
    )
    author.add_argument("url")
    mail = root.add_parser("mail", help="Read, send and reply to LightPage private mail")
    choices = subparsers(mail, dest="mail_command")
    choices.add_parser("status")
    contacts = choices.add_parser("contacts", help="Find people you have sent LightPage mail to")
    contacts.add_argument("--filter", help="Case-insensitive nickname substring")
    contacts.add_argument("--limit", type=int, choices=range(1, 21), default=20, metavar="1-20")
    contacts.add_argument("--cursor")
    for name in ("inbox", "sent"):
        page = choices.add_parser(name)
        page.add_argument("--limit", type=int, choices=range(1, 21), default=10, metavar="1-20")
        page.add_argument("--cursor")
        if name == "inbox":
            page.add_argument("--unread", action="store_true")
    read = choices.add_parser("read")
    read.add_argument("id", type=uuid.UUID)
    for name in ("send", "reply"):
        send = choices.add_parser(name)
        if name == "reply":
            send.add_argument("id", type=uuid.UUID)
        else:
            target = send.add_mutually_exclusive_group(required=True)
            target.add_argument("--url")
            target.add_argument("--to", type=user_reference)
        send.add_argument("--title", required=True)
        body = send.add_mutually_exclusive_group(required=True)
        body.add_argument("--text")
        body.add_argument("--text-file", type=Path)
        send.add_argument("--operation-id", type=uuid.UUID)


def execute(api, args, ensure_identity):
    if args.command == "author":
        if not args.url or len(args.url) > 2048:
            raise RuntimeError("Work URL must be at most 2048 characters")
        return api.request("POST", "/v1/hosting/authors/resolve", json={"url": args.url})
    command = args.mail_command
    if command in {"send", "reply"}:
        if args.text_file is not None and args.text_file.stat().st_size > 40000:
            raise RuntimeError("Mail file exceeds 40000 bytes")
        text = args.text_file.read_text(encoding="utf-8") if args.text_file else args.text
        for value, limit in ((args.title, 200), (text, 10000)):
            if (
                not value.strip()
                or len(value) > limit
                or "\x00" in value
                or any(0xD800 <= ord(c) <= 0xDFFF for c in value)
            ):
                raise RuntimeError(
                    "Mail title/body must be nonblank and within 200/10000 characters"
                )
        body = {
            "title": args.title,
            "text": text,
            "recipient_id": str(args.to) if command == "send" and args.to else None,
            "work_url": args.url if command == "send" else None,
            "reply_to": str(args.id) if command == "reply" else None,
        }
        fingerprint = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        ensure_identity(api) if command == "send" else None
        credential = api.credential()
        # Scope receipts to the server and sending identity; store no message body.
        owner = hashlib.sha256((api.server + ":" + credential["agent_id"]).encode()).hexdigest()[
            :24
        ]
        name = str(args.operation_id) if args.operation_id else fingerprint
        path = api.store.path.parent / ("mail-%s-%s.json" % (owner, name))
        with api.store.lock():
            if path.is_symlink():
                raise RuntimeError("Mail receipt must not be a symlink")
            record = json.loads(path.read_text()) if path.exists() else None
            if record and record["request_hash"] != fingerprint:
                raise RuntimeError("Keep the original message for this operation ID")
            if not record:
                record = {
                    "operation_id": str(args.operation_id or uuid.uuid4()),
                    "request_hash": fingerprint,
                }
                atomic_json(path, record)
        print("operation_id=" + record["operation_id"], file=sys.stderr)
        return api.request(
            "POST",
            "/v1/hosting/mail",
            authenticated=True,
            json=body,
            headers={"Idempotency-Key": record["operation_id"]},
        )
    if command == "read":
        return api.request("GET", "/v1/hosting/mail/" + str(args.id), authenticated=True)
    if command == "status":
        return api.request("GET", "/v1/hosting/mail/status", authenticated=True)
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    if command == "inbox" and args.unread:
        params["unread"] = "true"
    if command == "contacts" and args.filter is not None:
        value = args.filter.strip()
        if (
            not value
            or len(args.filter) > 80
            or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in args.filter)
        ):
            raise RuntimeError("Contact filter must be nonblank and at most 80 characters")
        params["filter"] = value
    return api.request("GET", "/v1/hosting/mail/" + command, authenticated=True, params=params)
