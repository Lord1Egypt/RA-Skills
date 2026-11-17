#!/usr/bin/env python3
"""netbox_api.py — minimal NetBox REST CLI for batch operations.

Usage:
  netbox_api.py get  "/api/dcim/devices/?limit=100&fields=name,rack,position"
  netbox_api.py patch /api/dcim/devices/42/ '{"name":"x","position":3}'
  netbox_api.py delete /api/dcim/cables/56/
  netbox_api.py all  "/api/dcim/interfaces/?limit=500"   # follows `next`, prints JSON list

Env: NETBOX_BASE (your instance, e.g. https://netbox.example.com).
Auth: --token *** flag, else read from ~/.config/netbox/token (chmod 600,
      one token per line). Never hardcode the token in files or commits.
TLS: certificate verification ON by default. Internal/self-signed CAs:
     export NETBOX_INSECURE_TLS=1 (equivalent to curl -k).
Stdout: JSON. Exit: 0 ok, 1 HTTP error, 2 usage/auth error.

Pagination: `all` follows the `next` URL from each response — never steps
`offset` by a guessed limit. (A step/limit mismatch, or relying on the server
default page size when you didn't pass `limit`, silently skips whole pages.)
Note: the server caps `limit` at MAX_PAGE_SIZE (default 1000); `next` handles it.
"""
import json, os, sys, urllib.request, ssl

BASE = os.environ.get("NETBOX_BASE", "https://netbox.example.com").rstrip("/")
def _load_token():
    """Token from --token flag (removed from argv) or ~/.config/netbox/token."""
    if "--token" in sys.argv:
        i = sys.argv.index("--token")
        tok = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
        del sys.argv[i:i + 2]  # keep cmd/path parsing positional
        return tok.strip()
    try:
        p = os.path.expanduser("~/.config/netbox/token")
        return open(p).read().strip()
    except OSError:
        return ""

TOK = _load_token()
ctx = ssl.create_default_context()  # certificate verification ON by default
if os.environ.get("NETBOX_INSECURE_TLS"):
    # Opt-out for internal/self-signed CAs (equivalent to curl -k).
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


def req(method, path, payload=None):
    url = path if path.startswith("http") else BASE + path  # `next` is absolute
    r = urllib.request.Request(url,
                               data=json.dumps(payload).encode() if payload is not None else None,
                               method=method)
    r.add_header("Authorization", "Bearer " + TOK)
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, context=ctx) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "null")
    except urllib.error.URLError as e:
        print(f"error: cannot reach {url} — {e.reason}", file=sys.stderr)
        return 0, None


def main():
    if not TOK:
        print("error: no API token — pass --token *** or put it in "
              "~/.config/netbox/token (chmod 600)", file=sys.stderr)
        return 2
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == "get":
        st, body = req("GET", path)
    elif cmd == "patch":
        st, body = req("PATCH", path, json.loads(sys.argv[3]))
    elif cmd == "delete":
        st, body = req("DELETE", path)
    elif cmd == "all":
        out, cur, st = [], path, 200
        while True:
            st, c = req("GET", cur)
            if st != 200:
                break
            out += c["results"]
            if not c.get("next"):
                break
            cur = c["next"]  # follow the server-computed next page
        body = out
    else:
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(body, indent=1))
    return 0 if st in (200, 204) else 1


if __name__ == "__main__":
    sys.exit(main())
