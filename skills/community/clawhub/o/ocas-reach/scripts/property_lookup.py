#!/usr/bin/env python3
"""
Property Lookup — RealtyAPI (Redfin/Zillow) + city/county assessor fallback.

Usage:
  python3 property_lookup.py autocomplete "<query>" [listingStatus]
  python3 property_lookup.py details_by_address "<address>"
  python3 property_lookup.py details_by_id <property_id> <listing_id>
  python3 property_lookup.py zillow_by_address "<address>"
  python3 property_lookup.py sf_assessor "<address fragment>"

Auth: requires `RT_KEY` env var (set in ~/.hermes/.env).
"""

import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 property_lookup.py")
    sys.exit(0)


REDFIN_BASE = "https://redfin.realtyapi.io"
ZILLOW_BASE = "https://zillow.realtyapi.io"
SF_OPENDATA = "https://data.sfgov.org/resource/wv5m-vpq2.json"
RT_KEY = os.environ.get("RT_KEY", "")


def _get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "body": e.read().decode("utf-8", "replace")[:500]}
    except urllib.error.URLError as e:
        return {"error": str(e.reason)}


def _realty_headers():
    return {"x-realtyapi-key": RT_KEY}


def autocomplete(query, listing_status="For_Sale_or_Sold"):
    qs = urllib.parse.urlencode({"query": query, "listingStatus": listing_status})
    return _get(f"{REDFIN_BASE}/autocomplete?{qs}", _realty_headers())


def details_by_address(address):
    qs = urllib.parse.urlencode({"property_address": address})
    return _get(f"{REDFIN_BASE}/detailsbyaddress?{qs}", _realty_headers())


def details_by_id(property_id, listing_id):
    qs = urllib.parse.urlencode({"property_id": property_id, "listing_id": listing_id})
    return _get(f"{REDFIN_BASE}/detailsbyid?{qs}", _realty_headers())


def zillow_by_address(address):
    qs = urllib.parse.urlencode({"propertyaddress": address})
    return _get(f"{ZILLOW_BASE}/byaddress?{qs}", _realty_headers())


def sf_assessor(fragment):
    where = f"property_location like '%{fragment.upper()}%'"
    qs = urllib.parse.urlencode({"$where": where, "$limit": 10})
    return _get(f"{SF_OPENDATA}?{qs}")


def main():
    if not RT_KEY and len(sys.argv) > 1 and sys.argv[1] != "sf_assessor":
        print("Error: RT_KEY environment variable not set.", file=sys.stderr)
        print("Add to ~/.hermes/.env: RT_KEY=rt_...", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    handlers = {
        "autocomplete": lambda: autocomplete(sys.argv[2], *(sys.argv[3:4] or ["For_Sale_or_Sold"])),
        "details_by_address": lambda: details_by_address(sys.argv[2]),
        "details_by_id": lambda: details_by_id(sys.argv[2], sys.argv[3]),
        "zillow_by_address": lambda: zillow_by_address(sys.argv[2]),
        "sf_assessor": lambda: sf_assessor(sys.argv[2]),
    }
    if cmd not in handlers:
        print(f"Unknown command: {cmd}\n{__doc__}", file=sys.stderr)
        sys.exit(1)
    try:
        result = handlers[cmd]()
    except IndexError:
        print(f"Missing arguments for `{cmd}`.\n{__doc__}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
