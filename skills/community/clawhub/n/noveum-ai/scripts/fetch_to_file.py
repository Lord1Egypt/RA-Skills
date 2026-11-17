#!/usr/bin/env python3
"""Stream any Noveum GET endpoint to a local file — never into agent context.

Large Noveum payloads (dataset items with fullContent, traces with spans,
NovaPilot/AutoFix reports) can be many megabytes. Pulling them into an agent's
context window truncates them (corrupt JSON) and crowds out the actual task.
This script streams the body to disk in chunks and prints only a small summary,
so the agent can then inspect the file selectively (grep / jq / python).

Usage:
    NOVEUM_API_KEY=... python fetch_to_file.py \
        "/v1/datasets/<slug>/items?fullContent=true" --out /tmp/items.json

    NOVEUM_API_KEY=... python fetch_to_file.py \
        "/v1/traces?project=my-app&size=100&includeSpans=true" --out /tmp/traces.json

Env: NOVEUM_API_KEY (required), NOVEUM_ENDPOINT (default https://api.noveum.ai/api).
Prints: {"savedTo", "bytes", "sha256", "status"} + a short head preview.
Exit codes: 0 saved · 2 configuration/HTTP/network error.
Stdlib only; GET requests only.
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_ENDPOINT = "https://api.noveum.ai/api"
REQUEST_TIMEOUT_S = 120  # large exports can be slow to first byte
CHUNK_BYTES = 1 << 16
# Preview stays small on purpose — the whole point is not to flood context.
PREVIEW_CHARS = 400


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="API path incl. query, starting with /v1/...")
    ap.add_argument("--out", required=True, help="file to write the body to")
    args = ap.parse_args()

    api_key = os.environ.get("NOVEUM_API_KEY", "").strip()
    if not api_key:
        print("CONFIG ERROR: set NOVEUM_API_KEY.")
        return 2
    if not args.path.startswith("/"):
        print("CONFIG ERROR: path must start with '/', e.g. /v1/datasets/x/items")
        return 2
    endpoint = os.environ.get("NOVEUM_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")

    url = f"{endpoint}{args.path}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    digest = hashlib.sha256()
    total = 0
    head = b""
    declared_len = None
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as res, open(
            args.out, "wb"
        ) as out:
            status = res.status
            cl = res.headers.get("Content-Length")
            declared_len = int(cl) if cl and cl.isdigit() else None
            while True:
                chunk = res.read(CHUNK_BYTES)
                if not chunk:
                    break
                if len(head) < PREVIEW_CHARS:
                    head += chunk[: PREVIEW_CHARS - len(head)]
                digest.update(chunk)
                out.write(chunk)
                total += len(chunk)
    except urllib.error.HTTPError as e:
        print(f"HTTP ERROR {e.code} from {url}:")
        print(e.read().decode(errors="replace")[:600])
        return 2
    except urllib.error.URLError as e:
        print(f"NETWORK ERROR reaching {url}: {e.reason}")
        return 2
    except OSError as e:
        # Mid-body timeout/reset after urlopen succeeded — a partial file exists.
        try:
            os.remove(args.out)
        except OSError:
            pass
        print(f"NETWORK ERROR mid-download from {url}: {e} (partial file removed)")
        return 2

    # http.client deliberately does NOT raise on short bodies; a dropped
    # connection would otherwise masquerade as success — the exact corruption
    # this tool exists to prevent.
    if declared_len is not None and total != declared_len:
        try:
            os.remove(args.out)
        except OSError:
            pass
        print(
            f"TRUNCATED DOWNLOAD: got {total} of {declared_len} declared bytes "
            f"from {url} — partial file removed. Retry, or page with smaller size."
        )
        return 2

    print(
        json.dumps(
            {
                "savedTo": os.path.abspath(args.out),
                "bytes": total,
                "sha256": digest.hexdigest(),
                "status": status,
                "contentLength": declared_len,
            }
        )
    )
    print(f"head: {head.decode(errors='replace')}")
    print(
        "Inspect selectively (do NOT read the whole file into context), e.g.:\n"
        f"  python3 -c \"import json;d=json.load(open('{args.out}'));"
        "print(type(d), list(d)[:8] if isinstance(d, dict) else len(d))\""
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
