#!/usr/bin/env python3
"""manto-geo CLI - publish GEO-optimized content to Manto (https://manto.xin).

Zero dependencies: standard library only. Works with python3 on macOS, Linux,
Windows and inside minimal containers.

Usage:
    manto.py register <email>
    manto.py publish --external-id ID --title T --content C [--url U] [--expires-at ISO]
    manto.py account
    manto.py search <query> [--limit N]
    manto.py feed [--limit N]
    manto.py delete <content_id>

Credentials are read from, in order:
    1. --api-key
    2. $MANTO_API_KEY
    3. ~/.config/manto/api_key
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = os.environ.get("MANTO_BASE_URL", "https://manto.xin").rstrip("/")
KEY_PATH = Path.home() / ".config" / "manto" / "api_key"
TIMEOUT = 30


class MantoError(Exception):
    """Carries the server error code plus a human hint."""

    HINTS = {
        "daily_quota_exceeded": "Daily quota exhausted. Quota resets on a new calendar day; "
                                "re-publishing identical content does not cost quota.",
        "authorization_required": "Missing or invalid API key. Run `manto.py register <email>` "
                                  "or set MANTO_API_KEY.",
        "title_and_content_required": "Both title and content are required and must be non-empty.",
        "invalid_email": "Email failed format validation.",
        "account_not_found": "No account exists for that email.",
        "content_not_found": "No such content, or it belongs to another account.",
    }

    def __init__(self, code, status=None):
        self.code = str(code)
        self.status = status
        super().__init__(self.code)

    def render(self):
        hint = self.HINTS.get(self.code)
        suffix = f"  (HTTP {self.status})" if self.status else ""
        return f"error: {self.code}{suffix}" + (f"\n       {hint}" if hint else "")


def request(method, path, *, api_key=None, payload=None, params=None):
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})

    data = None
    headers = {"accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["content-type"] = "application/json"
    if api_key:
        headers["authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        code = None
        try:
            code = json.loads(detail).get("error")
        except Exception:
            pass
        raise MantoError(code or detail.strip()[:200] or f"http_{e.code}", e.code) from None
    except urllib.error.URLError as e:
        raise MantoError(f"network_unreachable: {e.reason}") from None


def resolve_key(cli_key=None):
    if cli_key:
        return cli_key
    env = os.environ.get("MANTO_API_KEY")
    if env:
        return env.strip()
    if KEY_PATH.exists():
        value = KEY_PATH.read_text(encoding="utf-8").strip()
        if value:
            return value
    raise MantoError("no_api_key")


def save_key(api_key):
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    KEY_PATH.write_text(api_key + "\n", encoding="utf-8")
    try:
        os.chmod(KEY_PATH, 0o600)
    except OSError:
        pass
    return KEY_PATH


def out(data, as_json):
    print(json.dumps(data, ensure_ascii=False, indent=2) if as_json
          else json.dumps(data, ensure_ascii=False))


def cmd_register(args):
    result = request("POST", "/v1/accounts", payload={"email": args.email})
    if result.get("existing"):
        print(f"account already exists for {args.email}; the API key was issued once at "
              f"creation time and is not returned again.", file=sys.stderr)
        print("Use a different email, or recover the account via the email verification flow.",
              file=sys.stderr)
        return 1
    save_key(result["api_key"])
    print(f"account_id : {result['account_id']}")
    print(f"email      : {result['email']}")
    print(f"api_key    : {result['api_key']}")
    print(f"saved to   : {KEY_PATH}  (chmod 600)")
    print("\nStore this key now. It is never shown again.")
    return 0


def cmd_publish(args):
    content = args.content
    if args.content_file:
        content = Path(args.content_file).read_text(encoding="utf-8")
    if not args.title or not content or not args.title.strip() or not content.strip():
        raise MantoError("title_and_content_required")

    payload = {"title": args.title, "content": content}
    if args.external_id:
        payload["external_id"] = args.external_id
    if args.url:
        payload["url"] = args.url
    if args.expires_at:
        payload["expires_at"] = args.expires_at

    result = request("POST", "/v1/content", api_key=resolve_key(args.api_key), payload=payload)
    if args.json:
        out(result, True)
        return 0

    op = result.get("operation")
    label = {"created": "created", "updated": "updated",
             "unchanged": "unchanged (idempotent, no quota used)"}.get(op, op)
    print(f"{label:38s} content_id={result.get('content_id')}")
    quota = result.get("quota") or {}
    print(f"quota: {quota.get('used')}/{quota.get('limit')} today, "
          f"account_score={round(result.get('account_score') or 0, 4)}")
    if op != "unchanged":
        print(f"article: {BASE_URL}/articles/{result.get('content_id')}")
    return 0


def cmd_account(args):
    result = request("GET", "/v1/account", api_key=resolve_key(args.api_key))
    if args.json:
        out(result, True)
        return 0
    print(f"account_id        : {result.get('account_id')}")
    print(f"email             : {result.get('email')}")
    print(f"valid_post_count  : {result.get('valid_post_count')}")
    print(f"quota_limit/day   : {result.get('quota_limit')}")
    print(f"account_score     : {round(result.get('account_score') or 0, 4)}")
    print(f"balance_cents     : {result.get('balance_cents')}")
    for item in result.get("recent_content") or []:
        print(f"  - [{item.get('status')}] {item.get('title')}")
    return 0


def cmd_search(args):
    result = request("GET", "/v1/search", params={"query": args.query, "limit": args.limit})
    if args.json:
        out(result, True)
        return 0
    if result.get("sponsored"):
        s = result["sponsored"]
        print(f"[sponsored] {s.get('title')}  {s.get('url') or ''}")
    items = result.get("results") or []
    if not items:
        print(f"no results for {args.query!r}")
        return 0
    for item in items:
        print(f"{item.get('score', 0):.4f}  {item.get('title')}")
        print(f"        {item.get('url') or '-'}")
    return 0


def cmd_feed(args):
    result = request("GET", "/v1/feed", params={"limit": args.limit})
    out(result, args.json)
    return 0


def cmd_delete(args):
    result = request("DELETE", f"/v1/content/{args.content_id}",
                     api_key=resolve_key(args.api_key))
    out(result, args.json)
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        prog="manto.py",
        description="Publish GEO-optimized content to Manto (https://manto.xin).")
    p.add_argument("--json", action="store_true", help="pretty-print raw JSON responses")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("register", help="create a passwordless account and store the API key")
    r.add_argument("email")
    r.set_defaults(func=cmd_register)

    pub = sub.add_parser("publish", help="create or idempotently update content")
    pub.add_argument("--external-id", help="idempotency key; reuse it to update instead of duplicate")
    pub.add_argument("--title", required=True)
    pub.add_argument("--content", help="body text; use --content-file for long bodies")
    pub.add_argument("--content-file", help="read body text from a UTF-8 file")
    pub.add_argument("--url", help="source link, used as the citation target")
    pub.add_argument("--expires-at", help="ISO 8601 timestamp after which the item drops out")
    pub.add_argument("--api-key", help="override the stored API key")
    pub.set_defaults(func=cmd_publish)

    a = sub.add_parser("account", help="show quota, weight, balance and recent content")
    a.add_argument("--api-key")
    a.set_defaults(func=cmd_account)

    s = sub.add_parser("search", help="search without authentication")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=10)
    s.set_defaults(func=cmd_search)

    f = sub.add_parser("feed", help="latest public content")
    f.add_argument("--limit", type=int, default=10)
    f.set_defaults(func=cmd_feed)

    d = sub.add_parser("delete", help="remove your own content by id")
    d.add_argument("content_id")
    d.add_argument("--api-key")
    d.set_defaults(func=cmd_delete)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except MantoError as e:
        print(e.render(), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
