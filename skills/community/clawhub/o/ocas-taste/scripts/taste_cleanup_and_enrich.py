#!/usr/bin/env python3
"""
taste_cleanup_and_enrich.py — Clean up remaining unenriched items.

1. Deduplicate items with same normalized name
2. Strip location suffixes from venue names for better Google matching
3. Retry enrichment for remaining items
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Cross-source signal dedup plus retry of failed enrichments.')
    print("Usage: taste_cleanup_and_enrich.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)

import json
import os
import re
import sqlite3
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 taste_cleanup_and_enrich.py")
    sys.exit(0)


TASTE_DIR = 'os.path.expanduser("~/.hermes")/commons/data/ocas-taste'
TASTE_ITEMS = f'{TASTE_DIR}/items.jsonl'
TASTE_SIGNALS = f'{TASTE_DIR}/signals.jsonl'

def load_api_key():
    env = {}
    with open('os.path.expanduser("~/.hermes")/secrets/plaid.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env.get('GOOGLE_PLACES_API_KEY')

def places_search(name, city="San Francisco", max_results=3):
    payload = json.dumps({
        "textQuery": f"{name} {city}",
        "maxResultCount": max_results,
        "languageCode": "en",
    }).encode()
    req = urllib.request.Request(
        'https://places.googleapis.com/v1/places:searchText',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': load_api_key(),
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.types,places.rating,places.priceLevel,places.editorialSummary'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get('places', [])
    except:
        return []

def extract_attrs(place):
    types = place.get('types', [])
    cuisine = [t for t in types if t in (
        'restaurant', 'cafe', 'bar', 'bakery', 'meal_delivery',
        'meal_takeaway', 'food', 'night_club', 'liquor_store',
        'supermarket', 'grocery_or_supermarket'
    )]
    price_map = {
        'PRICE_LEVEL_FREE': 0, 'PRICE_LEVEL_INEXPENSIVE': 1,
        'PRICE_LEVEL_MODERATE': 2, 'PRICE_LEVEL_EXPENSIVE': 3,
        'PRICE_LEVEL_VERY_EXPENSIVE': 4,
    }
    return {
        'name': place.get('displayName', {}).get('text', ''),
        'address': place.get('formattedAddress', ''),
        'types': types,
        'cuisine': cuisine,
        'rating': place.get('rating'),
        'price_level': price_map.get(place.get('priceLevel', ''), -1),
        'summary': place.get('editorialSummary', ''),
    }

def clean_name(name):
    """Strip location suffixes and normalize for better Google matching."""
    # Strip parenthetical locations: (King St), (Polk), (Downtown SF), etc.
    name = re.sub(r'\s*\([^)]*\)\s*$', '', name)
    # Strip dash locations: - 470 Green St, - San Francisco, etc.
    name = re.sub(r'\s*[-–—]\s*\d+.*$', '', name)
    name = re.sub(r'\s*[-–—]\s*(san francisco|sf|soma|mission|castro|marina|north beach|hayes valley|fillmore|redwood city|palo alto|sunnyvale).*$', '', name, flags=re.IGNORECASE)
    # Strip "for N" suffixes
    name = re.sub(r'\s+for\s+\d+.*$', '', name)
    # Strip "know you are coming", "is confirmed", etc.
    name = re.sub(r'\s+(know you are coming|is confirmed|for \d+).*$', '', name)
    # Strip "Reservation at" prefix
    name = re.sub(r'^reservation at\s+', '', name, flags=re.IGNORECASE)
    # Strip trailing punctuation
    name = re.sub(r'[!?.]+$', '', name)
    return name.strip()

def main():
    api_key = load_api_key()
    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found")
        sys.exit(1)

    # Load all items
    items = []
    with open(TASTE_ITEMS) as f:
        for line in f:
            if line.strip():
                try:
                    items.append(json.loads(line))
                except:
                    pass

    print(f"Total items: {len(items)}")

    # Find unenriched restaurant/food items
    not_enriched = [i for i in items if not i.get('enriched') and i.get('domain') in ('restaurant', 'food')]
    print(f"Unenriched restaurants: {len(not_enriched)}")

    # Deduplicate by normalized name
    seen = {}
    deduped = []
    for item in not_enriched:
        name = item.get('venue_name', item.get('name', ''))
        norm = name.lower().strip()
        if norm not in seen:
            seen[norm] = item
            deduped.append(item)
        # else: duplicate, skip

    print(f"After dedup: {len(deduped)}")

    # Try to enrich each one with cleaned name
    enriched = 0
    failed = 0
    updated_items = []

    for i, item in enumerate(deduped):
        original_name = item.get('venue_name', item.get('name', ''))
        city = item.get('city', 'San Francisco')

        # Clean the name for better matching
        search_name = clean_name(original_name)

        if not search_name or len(search_name) < 3:
            # Try the original name if cleaning removed too much
            search_name = re.sub(r'\s*\([^)]*\)\s*$', '', original_name).strip()

        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{len(deduped)}")

        places = places_search(search_name, city)
        if not places:
            # Try without "the" prefix
            places = places_search(re.sub(r'^the\s+', '', search_name, flags=re.IGNORECASE), city)

        if not places:
            failed += 1
            print(f"  ✗ {original_name[:50]:50s} (tried: '{search_name}')")
            continue

        best = places[0]
        attrs = extract_attrs(best)

        # Update the item
        item['enriched'] = True
        item['enriched_at'] = datetime.now().strftime('%Y-%m-%d')
        item['rating'] = attrs['rating']
        item['price_level'] = attrs['price_level']
        item['address'] = attrs['address']
        if 'metadata' not in item:
            item['metadata'] = {}
        item['metadata']['cuisine'] = attrs['cuisine']
        item['metadata']['rating'] = attrs['rating']
        item['metadata']['price_level'] = attrs['price_level']
        item['metadata']['neighborhood'] = city

        enriched += 1
        print(f"  ✓ {original_name[:40]:40s} → {attrs['name'][:30]:30s} ★{attrs['rating']} ${attrs['price_level']}")

        time.sleep(0.25)

    # Now rewrite the items file with updated items
    # Build a lookup of updated items
    updated_lookup = {}
    for item in deduped:
        if item.get('enriched'):
            # Match by item_id or venue_name
            if item.get('item_id'):
                updated_lookup[item['item_id']] = item
            updated_lookup[item.get('venue_name', '').lower()] = item

    # Rewrite all items
    updated_count = 0
    for i, item in enumerate(items):
        item_id = item.get('item_id', '')
        venue = item.get('venue_name', '').lower()
        if item_id in updated_lookup:
            items[i] = updated_lookup[item_id]
            updated_count += 1
        elif venue in updated_lookup and not item.get('enriched'):
            items[i] = updated_lookup[venue]
            updated_count += 1

    with open(TASTE_ITEMS, 'w') as f:
        for item in items:
            f.write(json.dumps(item) + '\n')

    # Final count
    final_enriched = sum(1 for i in items if i.get('enriched'))
    final_not = sum(1 for i in items if not i.get('enriched'))

    print(f"\n{'='*60}")
    print(f"Cleanup enrichment complete:")
    print(f"  Newly enriched: {enriched}")
    print(f"  Failed: {failed}")
    print(f"  Total enriched: {final_enriched}/{len(items)} ({final_enriched/len(items)*100:.1f}%)")
    print(f"  Still not enriched: {final_not}")

if __name__ == '__main__':
    main()