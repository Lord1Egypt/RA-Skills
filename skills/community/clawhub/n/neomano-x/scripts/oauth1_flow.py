#!/usr/bin/env python3
"""OAuth 1.0a 3-legged flow helper for X.

This helps obtain X_ACCESS_TOKEN and X_ACCESS_TOKEN_SECRET when the developer UI
does not show them.

Flow:
  1) auth-start  -> prints authorize URL
  2) user visits URL, logs in, is redirected to callback with oauth_verifier
  3) auth-finish -> exchanges oauth_verifier for access token + secret

Env required:
  X_API_KEY, X_API_SECRET

Optional:
  X_OAUTH_CALLBACK (default: https://example.com/callback)

Notes:
  - The callback URL must be allowed/configured in the app settings.
  - If the callback page 404s, that's fine; you just need the query params.
"""

import argparse
import os
import sys
from urllib.parse import parse_qs, urlparse


def require_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise SystemExit(f"ERROR: missing env {name}")
    return v


def auth_start() -> int:
    import requests
    from requests_oauthlib import OAuth1

    api_key = require_env("X_API_KEY")
    api_secret = require_env("X_API_SECRET")
    callback = os.environ.get("X_OAUTH_CALLBACK", "https://example.com/callback")

    url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1(api_key, client_secret=api_secret, callback_uri=callback)

    r = requests.post(url, auth=oauth, timeout=30)
    if r.status_code >= 300:
        raise SystemExit(f"ERROR: request_token failed: {r.status_code} {r.text}")

    qs = parse_qs(r.text)
    oauth_token = (qs.get("oauth_token") or [None])[0]
    oauth_token_secret = (qs.get("oauth_token_secret") or [None])[0]
    if not oauth_token or not oauth_token_secret:
        raise SystemExit(f"ERROR: unexpected response: {r.text}")

    auth_url = f"https://api.twitter.com/oauth/authorize?oauth_token={oauth_token}"

    print("AUTH_URL=" + auth_url)
    print("OAUTH_TOKEN=" + oauth_token)
    print("OAUTH_TOKEN_SECRET=" + oauth_token_secret)
    print("\nNext: open AUTH_URL, approve, then copy oauth_verifier from the redirect URL.")
    return 0


def auth_finish(oauth_token: str, oauth_token_secret: str, oauth_verifier: str) -> int:
    import requests
    from requests_oauthlib import OAuth1

    api_key = require_env("X_API_KEY")
    api_secret = require_env("X_API_SECRET")

    url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1(
        api_key,
        client_secret=api_secret,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
        verifier=oauth_verifier,
    )
    r = requests.post(url, auth=oauth, timeout=30)
    if r.status_code >= 300:
        raise SystemExit(f"ERROR: access_token failed: {r.status_code} {r.text}")

    qs = parse_qs(r.text)
    access_token = (qs.get("oauth_token") or [None])[0]
    access_token_secret = (qs.get("oauth_token_secret") or [None])[0]
    screen_name = (qs.get("screen_name") or [None])[0]

    if not access_token or not access_token_secret:
        raise SystemExit(f"ERROR: unexpected response: {r.text}")

    print("X_ACCESS_TOKEN=" + access_token)
    print("X_ACCESS_TOKEN_SECRET=" + access_token_secret)
    if screen_name:
        print("SCREEN_NAME=" + screen_name)
    return 0


def parse_redirect_url(url: str):
    parsed = urlparse(url)
    q = parse_qs(parsed.query)
    return (q.get("oauth_token") or [None])[0], (q.get("oauth_verifier") or [None])[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("auth-start")

    p2 = sub.add_parser("auth-finish")
    p2.add_argument("--oauth-token", required=True)
    p2.add_argument("--oauth-token-secret", required=True)
    p2.add_argument("--oauth-verifier", required=True)

    p3 = sub.add_parser("parse-redirect")
    p3.add_argument("--url", required=True, help="Redirect URL that contains oauth_token and oauth_verifier")

    args = ap.parse_args()

    if args.cmd == "auth-start":
        return auth_start()
    if args.cmd == "parse-redirect":
        tok, ver = parse_redirect_url(args.url)
        print(f"oauth_token={tok}")
        print(f"oauth_verifier={ver}")
        return 0
    if args.cmd == "auth-finish":
        return auth_finish(args.oauth_token, args.oauth_token_secret, args.oauth_verifier)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
