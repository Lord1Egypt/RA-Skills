#!/usr/bin/env python3
"""
Styx Google Places Enrichment — enriches restaurant/food merchants from Styx
using the Google Places API (New).

For each restaurant transaction in Styx that hasn't been enriched yet:
1. Query Google Places API with merchant name + city
2. Extract: cuisine types, price level, rating, neighborhood, address
3. Store enriched data in the merchant record
4. Create/update Taste ItemRecord

Usage:
    python3 styx_places_enrich.py [--limit 50] [--dry-run] [--all]
"""

import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request


def parse_formatted_address(addr):
    """
    Parse Google Places formattedAddress → (city, state_or_region, postcode).

    US:  '525 Market St, San Francisco, CA 94105, USA'  → ('San Francisco', 'CA', '94105')
    UK:  '92 Station Rd., Soham, ELY CB7 5DZ, UK'      → ('Soham', 'UK', 'CB7 5DZ')
    City-only: 'Berkeley, CA, USA'                       → ('Berkeley', 'CA', None)
    """
    if not addr:
        return None, None, None
    parts = [p.strip() for p in addr.split(",")]
    if len(parts) < 2:
        return None, None, None
    # US with zip
    for i, p in enumerate(parts):
        m = re.match(r'^([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$', p)
        if m and i >= 1:
            city = parts[i - 1].strip()
            if re.match(r'^[A-Za-z\s\.\-\']+$', city):
                return city, m.group(1), m.group(2)
    # US city-only: 'City, ST, USA'
    if parts[-1] in ('USA', 'US') and len(parts) >= 3:
        state_part = parts[-2].strip()
        if re.match(r'^[A-Z]{2}$', state_part):
            city = parts[-3].strip()
            if re.match(r'^[A-Za-z\s\.\-\']+$', city):
                return city, state_part, None
    # UK
    if parts[-1].strip() in ('UK', 'United Kingdom') and len(parts) >= 3:
        region_postcode = parts[-2].strip()
        uk_m = re.match(r'^(.+?)\s+([A-Z]{1,2}\d[\dA-Z]?\s*\d[A-Z]{2})$', region_postcode)
        if uk_m and len(parts) >= 4:
            city = parts[-3].strip()
            return city, 'UK', uk_m.group(2).strip()
        city = parts[-2].strip()
        if re.match(r'^[A-Za-z\s\.\-\']+$', city):
            return city, 'UK', None
    # Generic international
    country = parts[-1].strip()
    if re.match(r'^[A-Za-z\s]+$', country) and len(parts) >= 2:
        city = parts[-2].strip()
        if re.match(r'^[A-Za-z\s\.\-\']+$', city) and city.lower() != country.lower():
            return city, country, None
    return None, None, None

STYX_DB = '~/.hermes/data/styx.db'
TXN_DB = '~/.hermes/data/transactions.db'
TASTE_ITEMS = '~/.hermes/commons/data/ocas-taste/items.jsonl'
TASTE_SIGNALS = '~/.hermes/commons/data/ocas-taste/signals.jsonl'

def load_api_key():
    env = {}
    with open('~/.hermes/secrets/plaid.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env.get('GOOGLE_PLACES_API_KEY')

def places_search(name, city="San Francisco", max_results=5):
    """Search Google Places API (New) for a business."""
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
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.types,places.rating,places.priceLevel,places.location,places.editorialSummary,places.regularOpeningHours'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get('places', [])
    except Exception as e:
        print(f"  Places API error: {e}")
        return []

def extract_taste_attributes(place):
    """Extract taste-relevant attributes from a Google Places result."""
    attrs = {
        'name': place.get('displayName', {}).get('text', ''),
        'address': place.get('formattedAddress', ''),
        'types': place.get('types', []),
        'rating': place.get('rating'),
        'price_level': place.get('priceLevel', ''),
        'summary': place.get('editorialSummary', ''),
        'hours': place.get('regularOpeningHours', {}).get('weekdayDescriptions', []),
        'location': place.get('location', {}),
    }

    # Map Google types to taste categories
    cuisine_types = []
    type_mapping = {
        'restaurant': 'restaurant',
        'cafe': 'cafe',
        'bar': 'bar',
        'bakery': 'bakery',
        'meal_delivery': 'delivery',
        'meal_takeaway': 'takeaway',
        'food': 'food',
        'night_club': 'nightlife',
        'liquor_store': 'liquor',
        'grocery_or_supermarket': 'grocery',
        'supermarket': 'supermarket',
        'convenience_store': 'convenience',
    }
    for t in attrs['types']:
        if t in type_mapping:
            cuisine_types.append(t)
    attrs['taste_categories'] = cuisine_types

    # Map price level
    price_map = {
        'PRICE_LEVEL_FREE': 0,
        'PRICE_LEVEL_INEXPENSIVE': 1,
        'PRICE_LEVEL_MODERATE': 2,
        'PRICE_LEVEL_EXPENSIVE': 3,
        'PRICE_LEVEL_VERY_EXPENSIVE': 4,
    }
    attrs['price_level_num'] = price_map.get(attrs['price_level'], -1)

    return attrs

def get_food_merchants(styx_conn, limit=None, all_merchants=False):
    """Get food/restaurant merchants from Styx that need enrichment."""
    styx_conn.execute(f'ATTACH DATABASE "{TXN_DB}" AS txndb')

    # Get merchants that are food-related
    query = '''
        SELECT DISTINCT m.id as merchant_id, m.name as merchant_name, m.city,
               COUNT(tm.id) as visit_count,
               MIN(t.date) as first_visit,
               MAX(t.date) as last_visit,
               AVG(t.amount) as avg_amount
        FROM merchants m
        JOIN transaction_merchants tm ON m.id = tm.merchant_id
        JOIN txndb.transactions t ON tm.transaction_id = t.transaction_id
        WHERE (m.category IN ('restaurant', 'cafe', 'bar', 'food', 'bakery', 'liquor_store', 'meal_delivery', 'meal_takeaway', 'supermarket')
           OR t.personal_finance_category = 'FOOD_AND_DRINK')
    '''
    if not all_merchants:
        query += " AND m.source != 'google_places'"
    query += ' GROUP BY m.id ORDER BY visit_count DESC'
    if limit:
        query += f' LIMIT {limit}'

    return styx_conn.execute(query).fetchall()

def load_taste_items():
    """Load existing Taste items for dedup. Checks name, normalized_name, and venue_name."""
    items = {}
    if os.path.exists(TASTE_ITEMS):
        with open(TASTE_ITEMS) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        for field in ('name', 'normalized_name', 'venue_name'):
                            val = item.get(field, '').lower().strip()
                            if val:
                                items[val] = item
                    except Exception:
                        pass
    return items

def save_taste_item(item):
    """Append an item to Taste's items.jsonl."""
    os.makedirs(os.path.dirname(TASTE_ITEMS), exist_ok=True)
    with open(TASTE_ITEMS, 'a') as f:
        f.write(json.dumps(item) + '\n')

def save_taste_signal(signal):
    """Append a signal to Taste's signals.jsonl."""
    os.makedirs(os.path.dirname(TASTE_SIGNALS), exist_ok=True)
    with open(TASTE_SIGNALS, 'a') as f:
        f.write(json.dumps(signal) + '\n')

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Styx Google Places Enrichment')
    parser.add_argument('--limit', type=int, default=50, help='Max merchants to enrich')
    parser.add_argument('--dry-run', action='store_true', help='Do not write to DB')
    parser.add_argument('--all', action='store_true', help='Include already-enriched merchants')
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found")
        sys.exit(1)

    styx_conn = sqlite3.connect(STYX_DB)
    taste_items = load_taste_items()

    print(f"Loaded {len(taste_items)} existing Taste items for dedup")

    # Get food merchants needing enrichment
    food_merchants = get_food_merchants(styx_conn, args.limit, args.all)
    total = len(food_merchants)

    print(f"Enriching {total} food/restaurant merchants from Styx...")
    print(f"{'='*60}")

    enriched = 0
    skipped = 0
    failed = 0

    for i, (mid, name, city, visits, first, last, avg_amt) in enumerate(food_merchants):
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{total}")

        # Check if already in Taste (by any name field)
        name_lower = name.lower()
        if name_lower in taste_items:
            skipped += 1
            continue

        # Search Google Places
        places = places_search(name, city or "San Francisco")
        if not places:
            failed += 1
            continue

        best = places[0]
        attrs = extract_taste_attributes(best)

        if not args.dry_run:
            # Update Styx merchant with enriched data
            cat = attrs['taste_categories'][0] if attrs['taste_categories'] else 'restaurant'
            styx_conn.execute(
                "UPDATE merchants SET category = ?, address = ?, city = ?, state = ?, zip = ?, source = 'google_places', confidence = 0.9, updated_at = datetime('now') WHERE id = ?",
                (cat, attrs['address'], *parse_formatted_address(attrs['address']), mid)
            )

            # Create Taste ItemRecord
            safe_name = name_lower.replace(' ', '-').replace("'", '')[:30]
            taste_item = {
                'item_id': f"item-{safe_name}",
                'venue_name': attrs['name'] or name,
                'name': attrs['name'] or name,
                'normalized_name': name_lower,
                'domain': 'food',
                'category': cat,
                'types': attrs['taste_categories'],
                'rating': attrs['rating'],
                'price_level': attrs['price_level_num'],
                'address': attrs['address'],
                'city': city or 'San Francisco',
                'summary': attrs['summary'],
                'source': 'styx_places',
                'styx_merchant_id': mid,
                'visit_count': visits,
                'first_visit': first,
                'last_visit': last,
                'avg_amount': round(avg_amt, 2) if avg_amt else None,
                'enriched': True,
                'enriched_at': time.strftime('%Y-%m-%d'),
                'signal_count': visits,
                'visit_dates': [first, last] if first and last else [],
                'metadata': {
                    'cuisine': attrs['taste_categories'],
                    'price_level': attrs['price_level_num'],
                    'neighborhood': city or 'San Francisco',
                    'rating': attrs['rating'],
                }
            }
            save_taste_item(taste_item)

            # Create ConsumptionSignal
            signal = {
                'domain': 'food',
                'source': 'styx',
                'name': attrs['name'] or name,
                'normalized_name': name_lower,
                'strength': min(0.5 + (visits * 0.05), 1.0),
                'first_seen': first,
                'last_seen': last,
                'visit_count': visits,
                'created_at': time.strftime('%Y-%m-%d'),
            }
            save_taste_signal(signal)

            enriched += 1

        print(f"  ✓ {name[:40]:40s} → {attrs['name'][:30]:30s} "
              f"(rating: {attrs['rating']}, price: {attrs['price_level']}, visits: {visits})")

        # Rate limiting
        time.sleep(0.3)

    if not args.dry_run:
        styx_conn.commit()

    styx_conn.close()

    print(f"\n{'='*60}")
    print(f"Enrichment complete ({'dry run' if args.dry_run else 'live'}):")
    print(f"  Enriched: {enriched}")
    print(f"  Skipped (already in Taste): {skipped}")
    print(f"  Failed (no Places result): {failed}")

if __name__ == '__main__':
    main()