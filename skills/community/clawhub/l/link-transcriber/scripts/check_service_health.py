#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from urllib import error, request

DEFAULT_API_BASE_URL = "https://linktranscriber.store"


def main() -> int:
    base_url = os.getenv("LINK_SKILL_API_BASE_URL", DEFAULT_API_BASE_URL).strip().rstrip("/")
    url = f"{base_url}/health"
    req = request.Request(url, headers={"Accept": "application/json"}, method="GET")
    try:
        with request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"Health check failed with HTTP {exc.code}: {body}", file=sys.stderr)
        return 1
    except error.URLError as exc:
        print(f"Health check request failed: {exc.reason}", file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
