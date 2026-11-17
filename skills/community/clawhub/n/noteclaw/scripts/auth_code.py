#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""noteClaw authorization code flow (OAuth2) onboarding

Purpose: obtain a Microsoft Graph delegated token (with refresh_token) and write it to
     <data dir>/.auth/notes_token.json (0600).

Applies to: personal Microsoft accounts. The client is the OneDrive application that
     rclone publishes publicly (this script has its client_id/client_secret fallback
     built in; if ~/.config/rclone/rclone.conf has a section holding
     client_id+client_secret, that one is reused first).

Flow:
    1. run with no arguments → prints the authorization URL, then exits
    2. open that URL in a browser → sign in with the Microsoft account to mirror and
       consent to the permissions
       → you land on http://localhost:53682/ and the page says "cannot reach this site"
       (normal; the URL string in the address bar is the authorization result to paste
       back)
    3. once you have the authorization result, run this script to exchange it for a
       token, either way:
        - --code-url: pass the whole URL or the bare code directly
        - --code-file: write the whole URL or the bare code into a file, pass its path
          (the file is deleted automatically after a successful read)
    4. the token is written to .auth/notes_token.json (0600)

Afterwards graph_sync.py refreshes access_token automatically on every run, so no
further authorization is needed (rerun this script only if the token expires or is
revoked).
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

# Single source of shared credentials (env vars → rclone.conf → built-in rclone
# public application fallback)
from noteclaw_creds import load_client_creds, note_client_id

NOTECLAW = os.environ.get("NOTECLAW_HOME") or os.getcwd()
TOKEN_FILE = os.path.join(NOTECLAW, ".auth", "notes_token.json")

AUTHORIZE_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
REDIRECT_URI = "http://localhost:53682/"   # OAuth redirect registered for the app; the browser brings the authorization result back here
SCOPE = "Notes.Read offline_access"


def die(msg):
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(1)


def build_auth_url(cid):
    return (f"{AUTHORIZE_URL}?client_id={urllib.parse.quote(cid)}"
            f"&response_type=code"
            f"&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}"
            f"&scope={urllib.parse.quote(SCOPE)}"
            f"&response_mode=query&prompt=consent")


def exchange_code(cid, csec, code):
    """Exchange the authorization code for a token (includes refresh_token)"""
    body = urllib.parse.urlencode({
        "client_id": cid,
        "client_secret": csec,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }).encode()
    req = urllib.request.Request(TOKEN_ENDPOINT, data=body)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def parse_code(raw):
    """Parse the code out of a whole URL or a bare code value
    (tolerates #/& separators and a code= prefix)"""
    raw = raw.strip()
    if "http" in raw or "?" in raw:
        q = raw.split("?", 1)[1] if "?" in raw else raw
        c = urllib.parse.parse_qs(q).get("code", [None])[0]
        if c:
            return c
    c = raw.split("&")[0].split("#")[0].strip()
    if c.startswith("code="):
        c = c[5:]
    if not c:
        die("no code parsed — pass the whole post-redirect URL, or the value after code=.")
    return c


def read_code_file(path):
    """Read the code file: whole URL or bare code both work;
    lines starting with # are ignored (comments allowed)"""
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as e:
        die(f"cannot read code file {path}: {e}")
    body = "".join(l.strip() for l in lines if l.strip() and not l.startswith("#"))
    if not body:
        die(f"file {path} is empty — write the whole URL or the value after code= into it.")
    return body


def main():
    # When running in the background or through a pipe, stdout is block-buffered by
    # default and the authorization URL lands late; switch to line buffering
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="noteClaw authorization code flow (writes .auth/notes_token.json)")
    ap.add_argument("--code-url", default=None,
                    help="whole URL after the browser redirect, or the bare code value")
    ap.add_argument("--code-file", default=None,
                    help="read the URL/code from a file (deleted after a successful read)")
    args = ap.parse_args()

    cid, csec = load_client_creds()

    if args.code_url:
        code = parse_code(args.code_url)
    elif args.code_file:
        code = parse_code(read_code_file(args.code_file))
    else:
        print("Open the link below in a browser (sign in with the Microsoft account to mirror and consent to the permissions):")
        print()
        print("[AUTH URL]")
        print(build_auth_url(cid))
        return

    print("↻ exchanging code for a token …")
    try:
        t = exchange_code(cid, csec, code)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        if args.code_file:
            print(f"   ⚠ the code file is kept at {args.code_file}: rerun this command if the "
                  f"cause is the network; if it says the code is invalid or already used, "
                  f"authorize again and write the new code back into that file.",
                  file=sys.stderr)
        die(f"token exchange failed HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        die(f"cannot reach Microsoft services ({e.reason}) — check your network and retry")

    os.makedirs(os.path.dirname(TOKEN_FILE), mode=0o700, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump({
            "token_type": t.get("token_type", "Bearer"),
            "scope": t.get("scope", SCOPE),
            "expires_in": t.get("expires_in", 3600),
            "access_token": t.get("access_token", ""),
            "refresh_token": t.get("refresh_token", ""),
        }, f, indent=2)
    os.chmod(TOKEN_FILE, 0o600)
    # Record the client_id actually used → graph_sync reuses the same client when
    # refreshing the token
    note_client_id(TOKEN_FILE)
    # the code is single-use; leave no temporary file behind
    if args.code_file:
        try:
            os.remove(args.code_file)
        except OSError:
            pass
    print(f"✓ authorization complete, token written to {TOKEN_FILE} (0600)")


if __name__ == "__main__":
    main()
