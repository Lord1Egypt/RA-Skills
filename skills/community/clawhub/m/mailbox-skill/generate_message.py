#!/usr/bin/env python3
"""Generate mailbox messages in the skill's frontmatter Markdown format."""

from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a mailbox message in Markdown frontmatter format."
    )
    parser.add_argument(
        "--message-type",
        required=True,
        choices=("NEW", "REPLY"),
        help="Mailbox message type.",
    )
    parser.add_argument(
        "--request-id",
        help="Request identifier. Defaults to a generated UUID without dashes.",
    )
    parser.add_argument(
        "--receiver-inbox-path",
        required=True,
        help="Absolute receiver inbox path for this message.",
    )
    parser.add_argument(
        "--reply-inbox-path",
        required=True,
        help="Absolute reply inbox path for follow-up or delivery.",
    )
    parser.add_argument(
        "--channel-id",
        help="Optional channel or thread identifier.",
    )
    body_group = parser.add_mutually_exclusive_group()
    body_group.add_argument(
        "--body",
        help="Message body content.",
    )
    body_group.add_argument(
        "--body-file",
        help="Read message body content from a file.",
    )
    parser.add_argument(
        "--output",
        help="Write the generated message to a file. Defaults to stdout.",
    )
    return parser.parse_args()


def read_body(args: argparse.Namespace) -> str:
    if args.body is not None:
        return args.body
    if args.body_file is not None:
        return Path(args.body_file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def build_message(
    *,
    request_id: str,
    message_type: str,
    receiver_inbox_path: str,
    reply_inbox_path: str,
    channel_id: str | None,
    body: str,
) -> str:
    lines = [
        "---",
        f"REQUEST_ID: {request_id}",
        f"MESSAGE_TYPE: {message_type}",
    ]
    if channel_id:
        lines.append(f"CHANNEL_ID: {channel_id}")
    lines.extend(
        [
            f"RECEIVER_INBOX_PATH: {receiver_inbox_path}",
            f"REPLY_INBOX_PATH: {reply_inbox_path}",
            "---",
            "",
            body.rstrip("\n"),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    request_id = args.request_id or uuid.uuid4().hex
    body = read_body(args)
    message = build_message(
        request_id=request_id,
        message_type=args.message_type,
        receiver_inbox_path=args.receiver_inbox_path,
        reply_inbox_path=args.reply_inbox_path,
        channel_id=args.channel_id,
        body=body,
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(message, encoding="utf-8")
    else:
        sys.stdout.write(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
