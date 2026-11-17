#!/usr/bin/env python3
"""
taste_full_enrich.py — Comprehensive restaurant extraction and enrichment.

1. Scans styx transactions for food merchants not in taste
2. Scans email extractions for restaurants not in taste
3. Cross-source dedup (email + calendar + styx for same restaurant = one entry)
4. Enriches ALL unenriched items already in taste (from calendar/email scans)
5. Enriches all newly found restaurants via Google Places API

Usage:
    python3 taste_full_enrich.py [--dry-run] [--limit N]
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Full pipeline: email/calendar scan + Styx delta + enrichment of unenriched items.')
    print("Usage: taste_full_enrich.py [options]")
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

STYX_DB = os.path.expanduser('~/.hermes/data/styx.db')
TXN_DB = os.path.expanduser('~/.hermes/data/transactions.db')
TASTE_DIR = os.path.expanduser('~/.hermes/commons/data/ocas-taste')
TASTE_ITEMS = f'{TASTE_DIR}/items.jsonl'
TASTE_SIGNALS = f'{TASTE_DIR}/signals.jsonl'
EXTRACTIONS = f'{TASTE_DIR}/extractions.jsonl'

def load_api_key():
    env = {}
    with open(os.path.expanduser('~/.hermes/secrets/plaid.env')) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env.get('GOOGLE_PLACES_API_KEY')

def places_search(name, city="San Francisco", max_results=3):
    payload = json.dumps({
        "textQuery": f"{name} restaurant {city}",
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
    except Exception as e:
        print(f"  API error for '{name}': {e}")
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

def normalize_name(name):
    name = name.lower().strip()
    prefixes = ['the ', 'a ', 'an ']
    for p in prefixes:
        if name.startswith(p):
            name = name[len(p):]
    name = re.sub(r'\s*[-–—]\s*(san francisco|sf|mission|soma|castro|marina|north beach|hayes valley|fillmore).*$', '', name)
    name = re.sub(r'\s+(restaurant|cafe|bar|grill|kitchen|bistro|taqueria|pizzeria|bakery|market|deli)$', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def load_known_venues():
    known = set()
    for path in [TASTE_ITEMS, TASTE_SIGNALS]:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    if line.strip():
                        try:
                            obj = json.loads(line)
                            for field in ('name', 'normalized_name', 'venue_name'):
                                val = obj.get(field, '').strip()
                                if val:
                                    known.add(val.lower())
                                    known.add(normalize_name(val))
                        except:
                            pass
    return known

def save_item(item):
    os.makedirs(os.path.dirname(TASTE_ITEMS), exist_ok=True)
    with open(TASTE_ITEMS, 'a') as f:
        f.write(json.dumps(item) + '\n')

def save_signal(signal):
    os.makedirs(os.path.dirname(TASTE_SIGNALS), exist_ok=True)
    with open(TASTE_SIGNALS, 'a') as f:
        f.write(json.dumps(signal) + '\n')

def get_styx_missing(known_venues):
    conn = sqlite3.connect(STYX_DB)
    conn.execute(f'ATTACH DATABASE "{TXN_DB}" AS txndb')
    query = '''
        SELECT DISTINCT m.id, m.name, m.normalized_name, m.city,
               COUNT(tm.id) as visits, MIN(t.date) as first_visit, MAX(t.date) as last_visit
        FROM merchants m
        JOIN transaction_merchants tm ON m.id = tm.merchant_id
        JOIN txndb.transactions t ON tm.transaction_id = t.transaction_id
        WHERE (m.category IN ('restaurant', 'cafe', 'bar', 'food', 'bakery', 'liquor_store', 'meal_delivery', 'meal_takeaway', 'supermarket')
           OR t.personal_finance_category = 'FOOD_AND_DRINK')
        GROUP BY m.id ORDER BY visits DESC
    '''
    results = []
    for row in conn.execute(query).fetchall():
        mid, name, norm_name, city, visits, first, last = row
        if name.lower() not in known_venues and normalize_name(name) not in known_venues:
            results.append({
                'source': 'styx', 'merchant_id': mid, 'name': name,
                'city': city or 'San Francisco', 'visits': visits,
                'first_visit': first, 'last_visit': last,
            })
    conn.close()
    return results

def get_email_missing(extractions, known_venues):
    restaurants = defaultdict(lambda: {'count': 0, 'dates': []})
    for e in extractions:
        subject = e.get('subject', '')
        sender = e.get('sender', '')
        date = e.get('date', '')
        sender_lower = sender.lower()
        if not any(fs in sender_lower for fs in ['doordash', 'opentable', 'yelp', 'grubhub', 'ubereats', 'postmates', 'tock', 'resy', 'instacart']):
            continue
        name = None
        for pattern in [r'from ([A-Z][A-Za-z\s&\']+?) is confirmed', r'from ([A-Z][A-Za-z\s&\']+?) order', r'order from ([A-Z][A-Za-z\s&\']+?)[\s,]']:
            match = re.search(pattern, subject)
            if match:
                name = match.group(1).strip()
                break
        if not name and 'doordash' in sender_lower:
            parts = subject.split(' from ')
            if len(parts) > 1:
                name = parts[1].split(' is ')[0].split(' order')[0].strip()
        if name and 2 < len(name) < 60:
            norm = normalize_name(name)
            if norm not in known_venues and name.lower() not in known_venues:
                restaurants[norm]['name'] = name
                restaurants[norm]['count'] += 1
                restaurants[norm]['source'] = 'email'
                if date:
                    restaurants[norm]['dates'].append(date)
    return list(restaurants.values())

def get_unenriched_items():
    """Get all items in taste that are NOT yet enriched."""
    unenriched = []
    if os.path.exists(TASTE_ITEMS):
        with open(TASTE_ITEMS) as f:
            for line in f:
                if line.strip():
                    try:
                        item = json.loads(line)
                        if not item.get('enriched') and item.get('domain') in ('restaurant', 'food', 'travel'):
                            unenriched.append(item)
                    except:
                        pass
    return unenriched

def update_item_enriched(item_id, attrs, city):
    """Update an existing item in-place to mark it enriched."""
    # Read all items
    items = []
    with open(TASTE_ITEMS) as f:
        for line in f:
            if line.strip():
                try:
                    items.append(json.loads(line))
                except:
                    pass
    
    # Update matching item
    updated = False
    for item in items:
        if item.get('item_id') == item_id or item.get('venue_name', '').lower() == attrs.get('name', '').lower():
            item['enriched'] = True
            item['enriched_at'] = datetime.now().strftime('%Y-%m-%d')
            item['rating'] = attrs.get('rating')
            item['price_level'] = attrs.get('price_level')
            item['address'] = attrs.get('address', item.get('address', ''))
            if 'metadata' not in item:
                item['metadata'] = {}
            item['metadata']['cuisine'] = attrs.get('cuisine', [])
            item['metadata']['rating'] = attrs.get('rating')
            item['metadata']['price_level'] = attrs.get('price_level')
            item['metadata']['neighborhood'] = city
            updated = True
            break
    
    # Rewrite file
    with open(TASTE_ITEMS, 'w') as f:
        for item in items:
            f.write(json.dumps(item) + '\n')
    
    return updated

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--limit', type=int, default=0, help='0 = no limit')
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found")
        sys.exit(1)

    known_venues = load_known_venues()
    print(f"Known venues in taste: {len(known_venues)}")

    # === PHASE 1: Find missing restaurants from all sources ===
    print("\n=== PHASE 1: Finding missing restaurants ===")
    all_missing = []

    styx = get_styx_missing(known_venues)
    print(f"Styx food merchants missing: {len(styx)}")
    all_missing.extend(styx)

    extractions = []
    if os.path.exists(EXTRACTIONS):
        with open(EXTRACTIONS) as f:
            for line in f:
                if line.strip():
                    try:
                        extractions.append(json.loads(line))
                    except:
                        pass
    email = get_email_missing(extractions, known_venues)
    print(f"Email restaurants missing: {len(email)}")
    all_missing.extend(email)

    # Cross-source dedup
    deduped = {}
    for r in all_missing:
        norm = normalize_name(r['name'])
        if norm not in deduped:
            deduped[norm] = dict(r)
        else:
            deduped[norm]['visits'] = max(deduped[norm].get('visits', 1), r.get('visits', 1))

    new_restaurants = list(deduped.values())
    print(f"New restaurants to enrich (after dedup): {len(new_restaurants)}")

    # === PHASE 2: Enrich existing unenriched items ===
    print("\n=== PHASE 2: Enriching existing unenriched items ===")
    unenriched = get_unenriched_items()
    print(f"Unenriched items in taste: {len(unenriched)}")

    if args.limit > 0:
        new_restaurants = new_restaurants[:args.limit]
        unenriched = unenriched[:args.limit]

    # === PHASE 3: Run enrichment ===
    print(f"\n{'='*60}")
    print(f"Starting enrichment...")
    print(f"{'='*60}")

    enriched = 0
    failed = 0
    conn = None

    # First: enrich existing items
    for i, item in enumerate(unenriched):
        name = item.get('venue_name', item.get('name', ''))
        city = item.get('city', 'San Francisco')
        item_id = item.get('item_id', '')

        if not name:
            continue

        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{len(unenriched)}")

        places = places_search(name, city)
        if not places:
            failed += 1
            continue

        best = places[0]
        attrs = extract_attrs(best)

        if not args.dry_run:
            update_item_enriched(item_id, attrs, city)

            # Also create/update signal
            signal = {
                'domain': item.get('domain', 'restaurant'),
                'source': item.get('source', 'enrichment'),
                'name': attrs['name'] or name,
                'normalized_name': name.lower(),
                'strength': 0.7,
                'first_seen': item.get('first_visit', item.get('created_at', datetime.now().strftime('%Y-%m-%d'))),
                'last_seen': datetime.now().strftime('%Y-%m-%d'),
                'visit_count': item.get('signal_count', 1),
                'created_at': datetime.now().strftime('%Y-%m-%d'),
            }
            save_signal(signal)

            enriched += 1

        print(f"  ✓ {name[:40]:40s} → {attrs['name'][:30]:30s} ★{attrs['rating']} ${attrs['price_level']}")
        time.sleep(0.25)

    # Then: add new restaurants
    for i, r in enumerate(new_restaurants):
        name = r['name']
        city = r.get('city', 'San Francisco')
        visits = r.get('visits', r.get('count', 1))
        source = r.get('source', 'unknown')

        places = places_search(name, city)
        if not places:
            failed += 1
            continue

        best = places[0]
        attrs = extract_attrs(best)

        if not args.dry_run:
            safe_name = normalize_name(name).replace(' ', '-')[:30]
            now = datetime.now().strftime('%Y-%m-%d')

            item = {
                'item_id': f"item-{safe_name}",
                'venue_name': attrs['name'] or name,
                'name': attrs['name'] or name,
                'normalized_name': name.lower(),
                'domain': 'restaurant' if 'restaurant' in attrs['types'] else 'food',
                'category': attrs['cuisine'][0] if attrs['cuisine'] else 'restaurant',
                'types': attrs['cuisine'],
                'rating': attrs['rating'],
                'price_level': attrs['price_level'],
                'address': attrs['address'],
                'city': city,
                'summary': attrs['summary'],
                'source': source,
                'visit_count': visits,
                'enriched': True,
                'enriched_at': now,
                'signal_count': visits,
                'metadata': {
                    'cuisine': attrs['cuisine'],
                    'price_level': attrs['price_level'],
                    'neighborhood': city,
                    'rating': attrs['rating'],
                }
            }
            save_item(item)

            signal = {
                'domain': 'restaurant' if 'restaurant' in attrs['types'] else 'food',
                'source': source,
                'name': attrs['name'] or name,
                'normalized_name': name.lower(),
                'strength': min(0.5 + (visits * 0.05), 1.0),
                'first_seen': r.get('first_visit', now),
                'last_seen': r.get('last_visit', now),
                'visit_count': visits,
                'created_at': now,
            }
            save_signal(signal)

            if source == 'styx' and 'merchant_id' in r:
                try:
                    if conn is None:
                        conn = sqlite3.connect(STYX_DB)
                    cat = attrs['cuisine'][0] if attrs['cuisine'] else 'restaurant'
                    conn.execute(
                        "UPDATE merchants SET category=?, address=?, source='google_places', confidence=0.9, updated_at=datetime('now') WHERE id=?",
                        (cat, attrs['address'], r['merchant_id'])
                    )
                except:
                    pass

            enriched += 1

        print(f"  + {name[:40]:40s} → {attrs['name'][:30]:30s} ★{attrs['rating']} ${attrs['price_level']} [{source}]")
        time.sleep(0.25)

    if conn:
        conn.commit()
        conn.close()

    print(f"\n{'='*60}")
    print(f"Enrichment complete ({'dry run' if args.dry_run else 'live'}):")
    print(f"  Enriched: {enriched}")
    print(f"  Failed: {failed}")
    print(f"  Total processed: {len(unenriched) + len(new_restaurants)}")

if __name__ == '__main__':
    main()