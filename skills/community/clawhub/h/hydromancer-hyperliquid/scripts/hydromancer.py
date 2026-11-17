#!/usr/bin/env python3
"""Small, dependency-free client for the Hydromancer REST API (Hyperliquid data).

Usage:
  export HYDROMANCER_API_KEY=...            # never hard-code keys
  python hydromancer.py info '{"type": "clearinghouseState", "user": "0x..."}'
  python hydromancer.py positions 0xABC... [0xDEF ...]     # batchClearinghouseStates
  python hydromancer.py fills 0xABC... --hours 24          # userFillsByTime, follows the cursor
  python hydromancer.py liquidations --coin BTC --hours 6  # liquidationHistoryByTime
  python hydromancer.py usage                              # apiUsage for your key
Add --testnet to any command to use https://api-testnet.hydromancer.xyz.
"""
import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

MAINNET = "https://api.hydromancer.xyz"
TESTNET = "https://api-testnet.hydromancer.xyz"


def post_info(payload, testnet=False, max_retries=3, timeout=60):
    """POST /info with Bearer auth. Retries HTTP 429 using Retry-After, then retryAfterSecs."""
    key = os.environ.get("HYDROMANCER_API_KEY")
    if not key:
        sys.exit("Set HYDROMANCER_API_KEY (get a key: https://docs.hydromancer.xyz/readme/get-api-keys)")
    url = (TESTNET if testnet else MAINNET) + "/info"
    body = json.dumps(payload).encode()
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            # Cloudflare rejects the default "Python-urllib" agent with 403 / error code 1010.
            "User-Agent": "hydromancer-skill/0.1 (+https://docs.hydromancer.xyz)",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            try:
                return json.loads(raw.decode())
            except (UnicodeDecodeError, json.JSONDecodeError):
                sys.exit("Response was not JSON (binary endpoints such as perpSnapshots are not supported here)")
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")
            if e.code == 429 and attempt < max_retries:
                wait = _retry_after(e.headers.get("Retry-After"), text, attempt)
                time.sleep(wait + random.random())
                continue
            sys.exit(f"HTTP {e.code}: {text[:500]}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < max_retries:
                time.sleep(min(30.0, 2.0 ** attempt))
                continue
            sys.exit(f"Network error calling {url}: {e}")


def _retry_after(header, body, attempt):
    """Seconds to wait: Retry-After (seconds or HTTP date), then body retryAfterSecs, then backoff."""
    if header:
        try:
            return max(0.0, float(header))
        except ValueError:
            try:
                from email.utils import parsedate_to_datetime
                return max(0.0, parsedate_to_datetime(header).timestamp() - time.time())
            except (TypeError, ValueError):
                pass
    try:
        secs = json.loads(body).get("retryAfterSecs")
        if secs is not None:
            return max(0.0, float(secs))
    except (ValueError, AttributeError, json.JSONDecodeError):
        pass
    return min(30.0, 2.0 ** attempt)


def batch_positions(users, dex=None, testnet=False):
    """batchClearinghouseStates: up to 1,000 users per request (100 with dex="ALL_DEXES")."""
    out = []
    size = 100 if dex == "ALL_DEXES" else 1000
    for i in range(0, len(users), size):
        payload = {"type": "batchClearinghouseStates", "users": users[i:i + size]}
        if dex:
            payload["dex"] = dex
        out.append(post_info(payload, testnet))
    return out[0] if len(out) == 1 else out


def fills_by_time(user, start_ms, end_ms=None, testnet=False, max_pages=50, page_size=2000):
    """userFillsByTime, following the "time_txIndex" cursor from the last record of each page.

    Pages are capped at 2000 rows. Fills are de-duplicated by tid across pages."""
    page_size = max(1, min(page_size, 2000))
    fills, seen, cursor = [], set(), None
    for page_no in range(max_pages):
        payload = {"type": "userFillsByTime", "user": user, "limit": page_size}
        if cursor:
            payload["cursor"] = cursor
        else:
            payload["startTime"] = start_ms
        if end_ms is not None:
            payload["endTime"] = end_ms
        page = post_info(payload, testnet)
        rows = page if isinstance(page, list) else page.get("fills", page.get("data", []))
        if not rows:
            break
        for f in rows:
            key = f.get("tid", (f.get("time"), f.get("hash"), f.get("oid")))
            if key not in seen:
                seen.add(key)
                fills.append(f)
        last = rows[-1]
        nxt = last.get("cursor") or (f"{last['time']}_{last['txIndex']}" if "txIndex" in last else None)
        if not nxt or nxt == cursor or len(rows) < page_size:
            break
        cursor = nxt
        if page_no == max_pages - 1:
            print(f"warning: stopped after {max_pages} pages; results may be incomplete "
                  "(raise max_pages or narrow the time range)", file=sys.stderr)
    return fills


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--testnet", action="store_true", default=argparse.SUPPRESS)
    p = argparse.ArgumentParser(description="Hydromancer REST API helper", parents=[common])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("info", parents=[common], help="raw POST /info with a JSON payload (JSON endpoints only; "
                       "binary snapshot endpoints such as perpSnapshots are not decoded)")
    s.add_argument("payload")
    s = sub.add_parser("positions", parents=[common], help="batchClearinghouseStates for one or more users")
    s.add_argument("users", nargs="+")
    s.add_argument("--dex", help='HIP-3 dex name, or "ALL_DEXES"')
    s = sub.add_parser("fills", parents=[common], help="userFillsByTime with cursor pagination")
    s.add_argument("user")
    s.add_argument("--hours", type=float, default=24)
    s.add_argument("--page-size", type=int, default=2000)
    s = sub.add_parser("liquidations", parents=[common], help="liquidationHistoryByTime (market-wide if no --coin)")
    s.add_argument("--coin")
    s.add_argument("--hours", type=float, default=6)
    s.add_argument("--limit", type=int, default=500)
    sub.add_parser("usage", parents=[common], help="apiUsage for your key")
    a = p.parse_args()
    a.testnet = getattr(a, "testnet", False)
    if getattr(a, "hours", 1) <= 0:
        p.error("--hours must be positive")
    now = int(time.time() * 1000)
    if a.cmd == "info":
        try:
            payload = json.loads(a.payload)
        except json.JSONDecodeError as e:
            p.error(f"payload is not valid JSON: {e}")
        res = post_info(payload, a.testnet)
    elif a.cmd == "positions":
        res = batch_positions(a.users, a.dex, a.testnet)
    elif a.cmd == "fills":
        res = fills_by_time(a.user, now - int(a.hours * 3_600_000), end_ms=now, testnet=a.testnet,
                            page_size=a.page_size)
    elif a.cmd == "liquidations":
        payload = {"type": "liquidationHistoryByTime", "startTime": now - int(a.hours * 3_600_000),
                   "endTime": now, "limit": a.limit}
        if a.coin:
            payload["coin"] = a.coin
        res = post_info(payload, a.testnet)
    else:
        res = post_info({"type": "apiUsage"}, a.testnet)
    try:
        json.dump(res, sys.stdout, indent=2)
        print()
    except BrokenPipeError:  # e.g. piped into `head`
        sys.stderr.close()


if __name__ == "__main__":
    main()
