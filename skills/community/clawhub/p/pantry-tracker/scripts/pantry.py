#!/usr/bin/env python3
"""
Pantry Tracker CLI — manages grocery items in Supabase.

Requires env vars:
  SUPABASE_URL      — project URL (https://xxx.supabase.co)
  SUPABASE_KEY      — anon key (not service role)

Usage:
  pantry.py add <name> [--category CAT] [--quantity QTY] [--expires DAYS] [--source SRC] [--order-id ID]
  pantry.py bulk-add <json-file>       # JSON array of items from email parsing
  pantry.py expiring [--days N]        # Items expiring within N days (default 3)
  pantry.py status                     # Full pantry overview
  pantry.py use <id-or-name>           # Mark item as used
  pantry.py toss <id-or-name>          # Mark item as tossed
  pantry.py refresh                    # Auto-update statuses based on dates
  pantry.py summary                    # Morning summary (for cron)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def _headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

def _request(method, path, data=None, params=None):
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=_headers(), method=method)
    try:
        with urlopen(req) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else []
    except HTTPError as e:
        err = e.read().decode()
        print(f"Error {e.code}: {err}", file=sys.stderr)
        sys.exit(1)

def add_item(args):
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=args.expires) if args.expires else None
    item = {
        "name": args.name,
        "category": args.category,
        "quantity": args.quantity,
        "purchased_at": now.isoformat(),
        "expires_at": expires.isoformat() if expires else None,
        "source": args.source,
        "order_id": args.order_id,
        "status": "fresh",
    }
    result = _request("POST", "pantry_items", item)
    print(f"Added: {result[0]['name']} (expires {result[0].get('expires_at', 'unknown')})")

def bulk_add(args):
    with open(args.json_file) as f:
        items = json.load(f)
    now = datetime.now(timezone.utc)
    rows = []
    for item in items:
        days = item.get("expires_days", 7)
        rows.append({
            "name": item["name"],
            "category": item.get("category"),
            "quantity": item.get("quantity"),
            "purchased_at": item.get("purchased_at", now.isoformat()),
            "expires_at": (now + timedelta(days=days)).isoformat(),
            "source": item.get("source"),
            "order_id": item.get("order_id"),
            "status": "fresh",
        })
    result = _request("POST", "pantry_items", rows)
    print(f"Added {len(result)} items to pantry.")
    for r in result:
        print(f"  - {r['name']} ({r.get('category', '?')}) expires {r.get('expires_at', '?')[:10]}")

def expiring(args):
    days = args.days or 3
    cutoff = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()
    params = {
        "status": "in.(fresh,use-soon)",
        "expires_at": f"lte.{cutoff}",
        "order": "expires_at.asc",
    }
    items = _request("GET", "pantry_items", params=params)
    if not items:
        print(f"Nothing expiring in the next {days} days.")
        return
    print(f"Items expiring within {days} days:")
    now = datetime.now(timezone.utc)
    for item in items:
        exp = datetime.fromisoformat(item["expires_at"].replace("Z", "+00:00"))
        delta = (exp - now).days
        urgency = "TODAY" if delta <= 0 else f"{delta}d left"
        print(f"  {'⚠️' if delta <= 1 else '🟡'} {item['name']} ({item.get('quantity', '?')}) — {urgency}")

def status_cmd(args):
    items = _request("GET", "pantry_items", params={
        "status": "in.(fresh,use-soon)",
        "order": "expires_at.asc",
    })
    if not items:
        print("Pantry is empty.")
        return
    now = datetime.now(timezone.utc)
    categories = {}
    for item in items:
        cat = item.get("category") or "other"
        categories.setdefault(cat, []).append(item)
    for cat, cat_items in sorted(categories.items()):
        print(f"\n## {cat.title()}")
        for item in cat_items:
            if item.get("expires_at"):
                exp = datetime.fromisoformat(item["expires_at"].replace("Z", "+00:00"))
                delta = (exp - now).days
                tag = f"{'⚠️ ' if delta <= 1 else '🟡 ' if delta <= 3 else ''}{delta}d"
            else:
                tag = "no expiry"
            print(f"  {item['name']} ({item.get('quantity', '?')}) — {tag}")

def use_item(args):
    _update_status(args.name, "used")

def toss_item(args):
    _update_status(args.name, "tossed")

def _update_status(name_or_id, new_status):
    # Try by name first (case-insensitive)
    items = _request("GET", "pantry_items", params={
        "name": f"ilike.*{name_or_id}*",
        "status": "in.(fresh,use-soon)",
        "limit": "1",
    })
    if not items:
        # Try by ID
        items = _request("GET", "pantry_items", params={"id": f"eq.{name_or_id}", "limit": "1"})
    if not items:
        print(f"Not found: {name_or_id}")
        sys.exit(1)
    item = items[0]
    _request("PATCH", "pantry_items", {"status": new_status}, params={"id": f"eq.{item['id']}"})
    print(f"{'✅ Used' if new_status == 'used' else '🗑️ Tossed'}: {item['name']}")

def refresh(args):
    now = datetime.now(timezone.utc)
    # Move fresh → use-soon (within 2 days)
    soon = (now + timedelta(days=2)).isoformat()
    _request("PATCH", "pantry_items", {"status": "use-soon"}, params={
        "status": "eq.fresh",
        "expires_at": f"lte.{soon}",
    })
    # Move use-soon → expired (past due)
    _request("PATCH", "pantry_items", {"status": "expired"}, params={
        "status": "in.(fresh,use-soon)",
        "expires_at": f"lte.{now.isoformat()}",
    })
    print("Pantry statuses refreshed.")

def summary(args):
    """Morning summary for cron delivery."""
    refresh(argparse.Namespace())  # auto-refresh first
    now = datetime.now(timezone.utc)
    
    # Expiring today or already expired
    urgent = _request("GET", "pantry_items", params={
        "status": "in.(use-soon,expired)",
        "order": "expires_at.asc",
    })
    
    # Expiring in 1-3 days
    soon_cutoff = (now + timedelta(days=3)).isoformat()
    upcoming = _request("GET", "pantry_items", params={
        "status": "eq.fresh",
        "expires_at": f"lte.{soon_cutoff}",
        "order": "expires_at.asc",
    })
    
    if not urgent and not upcoming:
        print("PANTRY_OK")
        return
    
    lines = []
    if urgent:
        lines.append("EAT OR TOSS TODAY:")
        for item in urgent:
            exp = datetime.fromisoformat(item["expires_at"].replace("Z", "+00:00")) if item.get("expires_at") else None
            delta = (exp - now).days if exp else 0
            status = "EXPIRED" if delta < 0 else "expires today"
            lines.append(f"  - {item['name']} ({item.get('quantity', '?')}) — {status}")
    
    if upcoming:
        lines.append("\nUSE SOON (next 3 days):")
        for item in upcoming:
            exp = datetime.fromisoformat(item["expires_at"].replace("Z", "+00:00"))
            delta = (exp - now).days
            lines.append(f"  - {item['name']} ({item.get('quantity', '?')}) — {delta}d left")
    
    print("\n".join(lines))

def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Set SUPABASE_URL and SUPABASE_KEY env vars.", file=sys.stderr)
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Pantry Tracker")
    sub = parser.add_subparsers(dest="command")
    
    p_add = sub.add_parser("add")
    p_add.add_argument("name")
    p_add.add_argument("--category", "-c")
    p_add.add_argument("--quantity", "-q")
    p_add.add_argument("--expires", "-e", type=int, help="Days until expiry")
    p_add.add_argument("--source", "-s")
    p_add.add_argument("--order-id")
    
    p_bulk = sub.add_parser("bulk-add")
    p_bulk.add_argument("json_file")
    
    p_exp = sub.add_parser("expiring")
    p_exp.add_argument("--days", "-d", type=int, default=3)
    
    sub.add_parser("status")
    
    p_use = sub.add_parser("use")
    p_use.add_argument("name")
    
    p_toss = sub.add_parser("toss")
    p_toss.add_argument("name")
    
    sub.add_parser("refresh")
    sub.add_parser("summary")
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cmds = {
        "add": add_item, "bulk-add": bulk_add, "expiring": expiring,
        "status": status_cmd, "use": use_item, "toss": toss_item,
        "refresh": refresh, "summary": summary,
    }
    cmds[args.command](args)

if __name__ == "__main__":
    main()
