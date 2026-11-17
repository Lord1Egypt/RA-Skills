#!/usr/bin/env python3
"""Small, dependency-free client for PlainlyKit's receive-only email API."""
import argparse
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, build_opener, HTTPRedirectHandler

BASE = "https://plainlykit.com/tools/temporary-email/api"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward a mailbox token to a redirected destination.


def request(method, path, token=None):
    headers = {"Accept": "application/json", "User-Agent": "PlainlyKit-Temporary-Email/1.0 (+https://plainlykit.com/developers/temporary-email)"}
    if token:
        headers["Authorization"] = "Bearer " + token
    data = b"{}" if method == "POST" else None
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = Request(BASE + path, data=data, headers=headers, method=method)
    with build_opener(NoRedirect).open(req, timeout=20) as response:
        return json.load(response)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path,
                        help="Private per-inbox credential file (created with mode 0600)")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "list", "delete"):
        sub.add_parser(name)
    sub.add_parser("read").add_argument("message_id")
    args = parser.parse_args(argv)
    if args.command == "create":
        # Reserve first: never create an inaccessible inbox by overwriting credentials.
        with os.fdopen(os.open(args.state, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as state:
            try:
                inbox = request("POST", "/mailboxes")
                if not all(isinstance(inbox.get(k), str) and inbox[k] for k in ("id", "token", "address")):
                    raise ValueError("Invalid inbox response")
                json.dump(inbox, state)
            except Exception:
                args.state.unlink()
                raise
        result = {k: inbox.get(k) for k in ("address", "expiresAt")}
    else:
        if args.state.is_symlink() or args.state.stat().st_mode & 0o077:
            raise ValueError("State must be a private file: chmod 600 it before use")
        inbox = json.loads(args.state.read_text())
        if not all(isinstance(inbox.get(k), str) and inbox[k] for k in ("id", "token")):
            raise ValueError("Invalid inbox state")
        path = "/mailboxes/" + quote(inbox["id"], safe="")
        if args.command in ("list", "read"):
            path += "/messages"
        if args.command == "read":
            path += "/" + quote(args.message_id, safe="")
        result = request("DELETE" if args.command == "delete" else "GET", path, inbox["token"])
        if args.command == "delete":
            args.state.unlink()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except HTTPError as error:
        print(f"API request failed (HTTP {error.code}). See SKILL.md for recovery.", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError, KeyError, URLError):
        print("Request failed. Check network, private state file and API availability.", file=sys.stderr)
        sys.exit(1)
