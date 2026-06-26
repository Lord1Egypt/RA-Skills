#!/usr/bin/env python3
"""
Extract the OpenTable restaurant id + slug from a URL the user pastes.

OpenTable uses several URL shapes:
    https://www.opentable.com/r/carbone-new-york           (slug page, rid not in URL)
    https://www.opentable.com/booking/details?rid=12345&...
    https://www.opentable.com/restaurant/profile/12345
    https://www.opentable.com/restref/client/?rid=12345&...
    https://www.opentable.com/s?...                        (search page, no rid)

This script accepts any of them and emits:
    { "rid": "12345" | null, "url_path": "carbone-new-york" | null, "source": "..." }

When only a slug is available (the /r/<slug> shape), rid is null — that's
fine because book.py accepts either and the profile URL falls back to
the slug form. Most booking links only need slug OR rid.

Usage:
    python3 extract_rid.py "https://www.opentable.com/r/carbone-new-york"
"""
from __future__ import annotations

import json
import re
import sys
from urllib.parse import urlparse, parse_qs


_SLUG_RE    = re.compile(r"^/r/([^/?#]+)")
_PROFILE_RE = re.compile(r"^/restaurant/profile/(\d+)")


def parse(url: str) -> dict:
    try:
        u = urlparse(url)
    except Exception as e:
        return {"rid": None, "url_path": None, "source": "parse_error", "error": str(e)}

    if "opentable.com" not in (u.netloc or ""):
        return {"rid": None, "url_path": None, "source": "not_opentable"}

    qs = parse_qs(u.query or "")
    rid = None
    for key in ("rid", "restref", "restaurantId"):
        if key in qs and qs[key]:
            rid = qs[key][0]
            break

    url_path = None
    path = u.path or "/"

    m = _SLUG_RE.match(path)
    if m:
        url_path = m.group(1)

    m = _PROFILE_RE.match(path)
    if m and not rid:
        rid = m.group(1)

    source = (
        "slug_page"       if url_path and path.startswith("/r/") else
        "booking_link"    if path.startswith("/booking/")         else
        "profile_page"    if path.startswith("/restaurant/")      else
        "restref"         if path.startswith("/restref/")         else
        "search_page"     if path.startswith("/s")                else
        "unknown"
    )
    return {
        "rid":      rid,
        "url_path": url_path,
        "source":   source,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: extract_rid.py <opentable_url>"}))
        return 1
    print(json.dumps(parse(sys.argv[1]), separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
