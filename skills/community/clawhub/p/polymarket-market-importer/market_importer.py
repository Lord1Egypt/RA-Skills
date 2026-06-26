#!/usr/bin/env python3
"""
Polymarket Market Importer - Auto-discover and import markets matching your criteria.

Usage:
    python market_importer.py              # Dry run (show what would be imported)
    python market_importer.py --live       # Import markets for real
    python market_importer.py --positions  # Show recently imported markets
    python market_importer.py --config     # Show current config
    python market_importer.py --set KEY=VALUE  # Update config

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Force line-buffered stdout (required for cron/Docker/OpenClaw visibility)
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
from simmer_sdk.skill import load_config, update_config, get_config_path

SKILL_SLUG = "polymarket-market-importer"
TRADE_SOURCE = "sdk:market-importer"

CONFIG_SCHEMA = {
    "keywords": {"env": "IMPORTER_KEYWORDS", "default": "bitcoin,ethereum", "type": str},
    "min_volume": {"env": "IMPORTER_MIN_VOLUME", "default": 10000.0, "type": float},
    "max_per_run": {"env": "IMPORTER_MAX_PER_RUN", "default": 5, "type": int},
    "categories": {"env": "IMPORTER_CATEGORIES", "default": "crypto", "type": str},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

# ---------------------------------------------------------------------------
# SimmerClient singleton
# ---------------------------------------------------------------------------
_client = None


def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            print("Get your API key from: simmer.markets/dashboard -> SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# ---------------------------------------------------------------------------
# Seen-markets persistence
# ---------------------------------------------------------------------------
SEEN_FILE = Path(__file__).parent / "imported_markets.json"


def load_seen() -> dict:
    """Load seen markets. Returns {market_id: {question, imported_at}}."""
    if SEEN_FILE.exists():
        try:
            with open(SEEN_FILE) as f:
                data = json.load(f)
            # Migration: if it's a plain list, convert to dict
            if isinstance(data, list):
                return {mid: {"question": "", "imported_at": ""} for mid in data}
            return data
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_seen(seen: dict):
    """Persist seen markets to disk."""
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)


# ---------------------------------------------------------------------------
# Category filtering
# ---------------------------------------------------------------------------
def matches_categories(market, categories: list[str]) -> bool:
    """Check if a market question/tags match any of the configured categories."""
    if not categories or categories == [""]:
        return True
    question = (market.get("question") or market.get("title") or "").lower()
    tags = [t.lower() for t in (market.get("tags") or [])]
    text = question + " " + " ".join(tags)
    return any(cat.lower() in text for cat in categories)


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def run_strategy(dry_run=True, positions_only=False, show_config=False, quiet=False):
    """Run the market importer."""
    print("🎯 Polymarket Market Importer")
    print("=" * 50)

    if show_config:
        print("\n  Current config:")
        for key, schema in CONFIG_SCHEMA.items():
            print(f"    {key} = {_config[key]}  (env: {schema['env']}, default: {schema['default']})")
        print(f"\n  Config file: {get_config_path(__file__)}")
        return

    client = get_client(live=not dry_run)

    if positions_only:
        seen = load_seen()
        if not seen:
            print("\n  No imported markets yet.")
            return
        recent = list(seen.items())[-20:]
        print(f"\n  Recently imported markets ({len(recent)} of {len(seen)} total):")
        for mid, info in reversed(recent):
            q = info.get("question", mid) if isinstance(info, dict) else mid
            ts = info.get("imported_at", "") if isinstance(info, dict) else ""
            print(f"    • {q}")
            if ts:
                print(f"      ID: {mid} | Imported: {ts}")
        return

    if dry_run:
        print("\n  [PAPER MODE] Use --live to import for real.")
    else:
        print("\n  [LIVE MODE] Importing markets for real.")

    keywords = [k.strip() for k in _config["keywords"].split(",") if k.strip()]
    categories = [c.strip() for c in _config["categories"].split(",") if c.strip()]
    min_volume = _config["min_volume"]
    max_per_run = int(_config["max_per_run"])

    if not quiet:
        print(f"\n  Config: keywords={','.join(keywords)} | min_volume={min_volume} | max_per_run={max_per_run} | categories={','.join(categories)}")

    seen = load_seen()
    total_found = 0
    total_already_seen = 0
    total_imported = 0
    imports_this_run = 0

    for keyword in keywords:
        if not quiet:
            print(f"\n  Searching for: {keyword}")

        try:
            # list_importable_markets returns markets available for import
            # Response fields assumed: list of dicts with id, question/title, url, volume_24h, tags
            results = client.list_importable_markets(
                q=keyword, min_volume=min_volume, limit=20
            )
        except Exception as e:
            print(f"    ❌ Search failed: {e}")
            continue

        if not results:
            if not quiet:
                print("    No importable markets found.")
            continue

        # Normalize: results may be a list of dicts or objects
        if hasattr(results, "__iter__"):
            markets = list(results)
        else:
            markets = []

        found = len(markets)
        total_found += found

        # Filter already seen
        new_markets = []
        already_seen = 0
        for m in markets:
            mid = m.get("id") or m.get("market_id") or ""
            if mid in seen:
                already_seen += 1
            else:
                new_markets.append(m)
        total_already_seen += already_seen

        # Category filter
        if categories:
            category_matched = [m for m in new_markets if matches_categories(m, categories)]
        else:
            category_matched = new_markets

        if not quiet:
            print(f"    Found {found} importable markets")
            print(f"    {already_seen} already imported, {len(new_markets)} new")
            if categories:
                print(f"    Category match: {len(category_matched)}")

        # Import up to quota
        for m in category_matched:
            if imports_this_run >= max_per_run:
                if not quiet:
                    print(f"    ⏸ Import cap reached ({max_per_run})")
                break

            mid = m.get("id") or m.get("market_id") or ""
            question = m.get("question") or m.get("title") or "Unknown"
            url = m.get("url") or m.get("market_url") or ""
            volume = m.get("volume_24h") or m.get("volume") or 0

            if not url:
                if not quiet:
                    print(f"    ⚠ No URL for market {mid}, skipping")
                continue

            print(f"  Importing: \"{question}\" (vol: ${volume:,.0f})")

            if dry_run:
                print("    📝 Would import (dry run)")
                imports_this_run += 1
                total_imported += 1
                # Still track in seen for dry-run dedup within the run
                seen[mid] = {
                    "question": question,
                    "imported_at": datetime.now(timezone.utc).isoformat(),
                    "dry_run": True,
                }
            else:
                try:
                    result = client.import_market(url)
                    print("    ✅ Imported successfully")
                    imports_this_run += 1
                    total_imported += 1
                    seen[mid] = {
                        "question": question,
                        "imported_at": datetime.now(timezone.utc).isoformat(),
                    }
                except Exception as e:
                    print(f"    ❌ Import failed: {e}")

    # Save seen markets (only persist non-dry-run, but save anyway for dedup)
    if not dry_run:
        # Remove dry_run flags from any previous dry runs
        for mid in seen:
            if isinstance(seen[mid], dict):
                seen[mid].pop("dry_run", None)
        save_seen(seen)

    # Summary
    print(f"\n  Summary: {total_found} found | {total_already_seen} already seen | {total_imported} imported (max {max_per_run})")

    # Return automaton data (printed once at the bottom)
    executed = total_imported if not dry_run else 0
    report = {
        "signals": total_found,
        "trades_attempted": 0,
        "trades_executed": executed,
    }
    if total_found == 0:
        report["skip_reason"] = "no_markets_found"
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket Market Importer")
    parser.add_argument("--live", action="store_true", help="Import markets for real")
    parser.add_argument("--dry-run", action="store_true", help="(Default) Show what would be imported")
    parser.add_argument("--positions", action="store_true", help="Show recently imported markets")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE", help="Set config value")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only output on imports/errors")
    args = parser.parse_args()

    # Handle --set
    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, value = item.split("=", 1)
                if key in CONFIG_SCHEMA:
                    type_fn = CONFIG_SCHEMA[key].get("type", str)
                    try:
                        value = type_fn(value)
                    except (ValueError, TypeError):
                        pass
                updates[key] = value
        if updates:
            updated = update_config(updates, __file__)
            print(f"Config updated: {updates}")
            print(f"Saved to: {get_config_path(__file__)}")
            _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

    dry_run = not args.live

    result = run_strategy(
        dry_run=dry_run,
        positions_only=args.positions,
        show_config=args.config,
        quiet=args.quiet,
    )

    # Single automaton report
    if os.environ.get("AUTOMATON_MANAGED"):
        if result and isinstance(result, dict):
            print(json.dumps({"automaton": result}))
        else:
            print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "no_signal"}}))
