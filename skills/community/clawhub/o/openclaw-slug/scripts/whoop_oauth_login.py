#!/usr/bin/env python3
"""Interactive WHOOP OAuth login (Authorization Code flow).

Reads:
- WHOOP_CLIENT_ID
- WHOOP_CLIENT_SECRET
- WHOOP_REDIRECT_URI
Optional:
- WHOOP_SCOPES (space-separated; default includes common read scopes)
- WHOOP_TOKEN_PATH

Writes token JSON to WHOOP_TOKEN_PATH.
"""

from __future__ import annotations

import os
import sys
import urllib.parse

from whoop_token import OAUTH_AUTH_URL, exchange_code_for_token, save_token, token_path


DEFAULT_SCOPES = "read:recovery read:sleep read:cycles read:workout read:profile read:body_measurement"


def must_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(2)
    return v


def parse_code(user_input: str) -> str:
    s = user_input.strip()
    if s.startswith("http://") or s.startswith("https://"):
        u = urllib.parse.urlparse(s)
        q = urllib.parse.parse_qs(u.query)
        code = (q.get("code") or [None])[0]
        if code:
            return code
        raise SystemExit("Could not find ?code= in the pasted redirect URL")
    return s


def main() -> None:
    client_id = must_env("WHOOP_CLIENT_ID")
    client_secret = must_env("WHOOP_CLIENT_SECRET")
    redirect_uri = must_env("WHOOP_REDIRECT_URI")
    scopes = os.environ.get("WHOOP_SCOPES", DEFAULT_SCOPES)

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scopes,
    }
    auth_url = OAUTH_AUTH_URL + "?" + urllib.parse.urlencode(params)

    print("Open this URL in a browser and approve access:\n")
    print(auth_url)
    print("\nAfter approval, paste either the full redirect URL or just the code:")
    user_in = input("> ")
    code = parse_code(user_in)

    tok = exchange_code_for_token(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    p = save_token(tok, token_path())
    print(f"\n[OK] Token saved to: {p}")


if __name__ == "__main__":
    main()
