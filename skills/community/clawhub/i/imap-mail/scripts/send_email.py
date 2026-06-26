#!/usr/bin/env python3
"""
Send email via IMAP Mail API.

Usage:
    python send_email.py --to user@example.com --subject "Hello" --text "Body"
    python send_email.py --to a@b.com --to c@d.com --subject "Hi" --text "Hello"
    python send_email.py --to user@example.com --subject "Re: Topic" --text "Reply" --reply-to "<msg-id>"

Environment:
    IMAP_MAIL_API    (default: http://127.0.0.1:8025)
    IMAP_MAIL_INBOX  default inbox address
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API   = os.getenv("IMAP_MAIL_API",   "http://127.0.0.1:8025")
INBOX = os.getenv("IMAP_MAIL_INBOX", "")


def api_post(path, payload):
    url  = API.rstrip("/") + path
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to IMAP Mail API at {API}: {e}", file=sys.stderr)
        print("Is the API server running? Start with: python3 mail-api.py", file=sys.stderr)
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Send email via IMAP Mail API")
    p.add_argument("--to",         required=True, action="append", help="Recipient (repeatable)")
    p.add_argument("--subject",    required=True)
    p.add_argument("--text",       default="", help="Plain text body")
    p.add_argument("--html",       default="", help="HTML body")
    p.add_argument("--reply-to",   dest="reply_to", default="", help="In-Reply-To message ID")
    p.add_argument("--references", default="", help="References header")
    p.add_argument("--inbox",      default=INBOX, help="Sending inbox (overrides IMAP_MAIL_INBOX)")
    args = p.parse_args()

    if not args.inbox:
        print("Error: specify --inbox or set IMAP_MAIL_INBOX", file=sys.stderr)
        sys.exit(1)

    enc    = urllib.parse.quote(args.inbox, safe="@.")
    result = api_post(f"/inboxes/{enc}/messages", {
        "to":          args.to,
        "subject":     args.subject,
        "text":        args.text,
        "html":        args.html,
        "in_reply_to": args.reply_to,
        "references":  args.references,
    })
    print(f"✅ Sent!  Message-ID: {result.get('message_id', '?')}")


if __name__ == "__main__":
    main()
