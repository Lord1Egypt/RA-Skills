#!/usr/bin/env python3
"""
taste_enrich_fix.py — Reliable item enrichment via Google Places API.

Fixes the bug in taste_full_enrich.py where update_item_enriched() fails to
persist `enriched: true` on source items due to loose name matching.

This script:
1. Reads items.jsonl for unenriched food/restaurant items
2. Looks up each via Google Places legacy GET API (proven to work)
3. Updates items.jsonl in-place with enriched=True and full metadata
4. Does NOT create signals — use taste_full_enrich.py or taste_scan.py for that

Usage:
    python3 scripts/taste_enrich_fix.py [--dry-run] [--limit N]

Confirmed working 2026-06-26: enriched The Butcher's Son and Hard Knox Cafe
after taste_full_enrich.py reported success but failed to persist.
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Re-enrich items via legacy Places GET API and persist enriched: true.')
    print("Usage: taste_enrich_fix.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)

import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone

TASTE_DIR = os.path.join(os.environ.get('AGENT_ROOT', os.environ.get("AGENT_ROOT", os.path.join(os.path.expanduser("~"), ".hermes"))), 'profiles', 'indigo', 'commons', 'data', 'ocas-taste')
ITEMS_FILE = f'{TASTE_DIR}/items.jsonl'

def load_api_key():
    """Read GOOGLE_PLACES_API_KEY from plaid.env."""
    with open(os.path.join(os.environ.get('AGENT_ROOT', os.environ.get("AGENT_ROOT", os.path.join(os.path.expanduser("~"), ".hermes"))), 'secrets', 'plaid.env')) as f:
        for line in f:
            line = line.strip()
            if line.startswith('GOOGLE_PLACES_API_KEY='):
                return line.split('=', 1)[1]
    return None

def places_search(name, city="San Francisco"):
    """Search Google Places via legacy GET API. Returns first result or None."""
    query = f"{name} restaurant {city}"
    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={urllib.parse.quote(query)}&key={load_api_key()}"
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
            results = data.get('results', [])
            if results:
                return results[0]
    except Exception as e:
        print(f"  API error for '{name}': {e}")
    return None

def extract_attrs(place):
    """Extract taste-relevant attributes from a Places API result."""
    types = place.get('types', [])
    cuisine_types = [t for t in types if t not in (
        'point_of_interest', 'establishment', 'food', 'store'
    )]
    price_map = {
        'PRICE_LEVEL_FREE': 0, 'PRICE_LEVEL_INEXPENSIVE': 1,
        'PRICE_LEVEL_MODERATE': 2, 'PRICE_LEVEL_EXPENSIVE': 3,
        'PRICE_LEVEL_VERY_EXPENSIVE': 4,
    }
    return {
        'name': place.get('name', ''),
        'cuisine': cuisine_types,
        'rating': place.get('rating'),
        'price_level': price_map.get(place.get('priceLevel', ''), 
                       1 if place.get('price_level') is None else place.get('price_level')),
        'formatted_address': place.get('formatted_address', ''),
        'neighborhood': place.get('vicinity', '').split(',')[0] if place.get('vicinity') else '',
        'city': None,  # parsed from address
        'maps_place_id': place.get('place_id', ''),
        'vibe': [],
    }

def get_unenriched_items():
    """Get unenriched food/restaurant items from items.jsonl."""
    items = []
    if not os.path.exists(ITEMS_FILE):
        return items
    with open(ITEMS_FILE) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                if not item.get('enriched', False) and item.get('domain') in ('food', 'restaurant'):
                    items.append(item)
            except:
                pass
    return items

def update_item_in_place(item_id, attrs):
    """Update an item in items.jsonl in-place, setting enriched=True."""
    now = datetime.now(timezone.utc).isoformat()
    
    # Read all items
    lines = []
    found = False
    with open(ITEMS_FILE) as f:
        for line in f:
            if not line.strip():
                lines.append(line)
                continue
            try:
                item = json.loads(line)
                if item.get('item_id') == item_id:
                    item['enriched'] = True
                    item['enriched_at'] = now
                    item['name'] = attrs['name'] or item.get('name', '')
                    item['metadata'] = {
                        'cuisine': attrs['cuisine'],
                        'rating': attrs['rating'],
                        'price_level': attrs['price_level'],
                        'formatted_address': attrs['formatted_address'],
                        'neighborhood': attrs['neighborhood'],
                        'maps_place_id': attrs['maps_place_id'],
                        'vibe': attrs['vibe'],
                        'source': 'taste_enrich_fix',
                    }
                    found = True
                lines.append(json.dumps(item, ensure_ascii=False) + '\n')
            except:
                lines.append(line)
    
    if not found:
        return False
    
    # Rewrite file
    with open(ITEMS_FILE, 'w') as f:
        f.writelines(lines)
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix unenriched food items via Places API')
    parser.add_argument('--dry-run', action='store_true', help='Only report, do not modify')
    parser.add_argument('--limit', type=int, default=0, help='Max items to process (0=no limit)')
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found in plaid.env")
        sys.exit(1)

    items = get_unenriched_items()
    print(f"Unenriched food/restaurant items: {len(items)}")
    
    if args.limit > 0:
        items = items[:args.limit]

    enriched = 0
    failed = 0

    for i, item in enumerate(items):
        name = item.get('venue_name', item.get('name', ''))
        city = item.get('city', 'San Francisco')
        item_id = item.get('item_id', '')

        if not name:
            continue

        print(f"[{i+1}/{len(items)}] {name}...", end=' ', flush=True)
        
        place = places_search(name, city)
        if not place:
            print("NO RESULT")
            failed += 1
            continue

        attrs = extract_attrs(place)
        print(f"OK → {attrs['name']} ★{attrs['rating']} ${attrs['price_level']}")

        if not args.dry_run:
            ok = update_item_in_place(item_id, attrs)
            if ok:
                enriched += 1
            else:
                print(f"  WARNING: failed to update item {item_id}")
                failed += 1
        else:
            enriched += 1

        time.sleep(0.3)  # Rate limit

    print(f"\n{'='*50}")
    print(f"Done ({'dry run' if args.dry_run else 'live'}):")
    print(f"  Enriched: {enriched}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(items)}")

if __name__ == '__main__':
    main()