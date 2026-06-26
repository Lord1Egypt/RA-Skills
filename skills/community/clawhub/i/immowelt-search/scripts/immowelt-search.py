#!/usr/bin/env python3
"""
Immowelt Real Estate Search (Austria & Germany) via HTML parsing.
Searches apartments and houses, fetches expose details for heating/energy/condition.

Usage:
  python3 immowelt-search.py --location wien --type apartment --max-price 300000
  python3 immowelt-search.py --location wien --type house --max-price 350000
  python3 immowelt-search.py --location niederoesterreich --type apartment --max-price 300000 --min-rooms 2
  python3 immowelt-search.py --expose 0a848843-86ba-4093-bd93-166258e909f7
  python3 immowelt-search.py --location wien --type apartment --format json

Locations use immowelt URL slug: wien, niederoesterreich, oberoesterreich,
  salzburg, steiermark, kaernten, tirol, vorarlberg, burgenland,
  bayern, berlin, hamburg, muenchen, etc.
Types: apartment (Wohnung kaufen), house (Haus kaufen)
Country: at (default), de
"""
import argparse
import json
import re
import sys
import time
import requests


BASE_URLS = {
    'at': 'https://www.immowelt.at',
    'de': 'https://www.immowelt.de',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'de-AT,de;q=0.9,en;q=0.5',
}

TYPE_MAP = {
    'apartment': 'wohnungen/kaufen',
    'house': 'haeuser/kaufen',
    'apartment-rent': 'wohnungen/mieten',
    'house-rent': 'haeuser/mieten',
}


def create_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def search_listings(session, country, location, property_type, max_price=None,
                    min_rooms=None, max_pages=5):
    """Search immowelt by scraping search result pages."""
    base = BASE_URLS.get(country, BASE_URLS['at'])
    slug = TYPE_MAP.get(property_type, property_type)
    all_items = []

    for page in range(1, max_pages + 1):
        url = f'{base}/liste/{location}/{slug}'
        params = {}
        if page > 1:
            params['cp'] = page
        if max_price:
            params['pma'] = max_price
        if min_rooms:
            params['rmi'] = min_rooms

        try:
            resp = session.get(url, params=params, timeout=20)
        except requests.RequestException as e:
            print(f"  [Request error page {page}: {e}]", file=sys.stderr)
            break

        if resp.status_code != 200:
            print(f"  [HTTP {resp.status_code} on page {page}]", file=sys.stderr)
            break

        text = resp.text
        cards = re.findall(
            r'data-testid="classified-card-mfe-([A-Z0-9]+)"(.*?)'
            r'(?=data-testid="classified-card-mfe-|data-testid="serp-core|$)',
            text, re.DOTALL
        )

        if not cards:
            break

        for card_id, card_html in cards:
            item = parse_card(card_id, card_html, base)
            if item:
                all_items.append(item)

        # Check if there's a next page
        if not re.search(r'aria-label="Seite ' + str(page + 1) + r'"', text):
            break

        time.sleep(0.3)

    return len(all_items), all_items


def parse_card(card_id, card_html, base_url):
    """Parse a single search result card from HTML."""
    item = {'id': card_id}

    # Extract expose link (UUID format)
    link_m = re.search(r'href="(?:' + re.escape(base_url) + r')?(/expose/[0-9a-f-]+)"', card_html)
    if link_m:
        item['url'] = f'{base_url}{link_m.group(1)}'
        item['expose_id'] = link_m.group(1).replace('/expose/', '')
    else:
        item['url'] = ''
        item['expose_id'] = ''

    # Extract title from covering link
    title_m = re.search(r'title="([^"]+)"', card_html)
    item['title'] = title_m.group(1) if title_m else ''

    # Extract price
    price_m = re.search(r'data-testid="cardmfe-price-testid"[^>]*>([^<]+)', card_html)
    if price_m:
        price_raw = price_m.group(1).strip()
        item['price_text'] = price_raw
        # Parse numeric price
        nums = re.findall(r'[\d.]+', price_raw.replace('.', '').replace(',', '.'))
        item['price'] = int(float(nums[0])) if nums else 0
    else:
        item['price_text'] = ''
        item['price'] = 0

    # Extract keyfacts from title (more reliable than keyfacts div)
    title = item.get('title', '')
    rooms_m = re.search(r'(\d+(?:,\d+)?)\s*Zimmer', title)
    item['rooms'] = int(float(rooms_m.group(1).replace(',', '.'))) if rooms_m else 0

    area_m = re.search(r'([\d,.]+)\s*m²', title)
    item['area'] = area_m.group(1) if area_m else ''

    floor_m = re.search(r'(\d+)\.\s*Geschoss|(\bEG\b)', title)
    if floor_m:
        item['floor'] = floor_m.group(1) or 'EG'
    else:
        item['floor'] = ''

    # Extract address
    addr_m = re.search(
        r'data-testid="cardmfe-description-box-address"[^>]*>(.*?)</div>',
        card_html, re.DOTALL
    )
    if addr_m:
        item['address'] = re.sub(r'<[^>]+>', ' ', addr_m.group(1)).strip()
        item['address'] = re.sub(r'\s+', ' ', item['address'])
    else:
        item['address'] = ''

    # Check for "new" tag
    item['is_new'] = bool(re.search(r'data-testid="cardmfe-tag-testid-new"', card_html))

    return item


def get_expose(session, expose_id, country='at'):
    """Fetch expose detail page and extract structured data."""
    base = BASE_URLS.get(country, BASE_URLS['at'])
    url = f'{base}/expose/{expose_id}'

    try:
        resp = session.get(url, timeout=20)
    except requests.RequestException as e:
        return {'error': str(e)}

    if resp.status_code != 200:
        return {'error': f'HTTP {resp.status_code}'}

    text = resp.text
    result = {'expose_id': expose_id, 'url': url}

    # Extract UFRN data
    m = re.search(
        r'window\["__UFRN_LIFECYCLE_SERVERREQUEST__"\]=JSON\.parse\("(.*?)"\);',
        text, re.DOTALL
    )
    if not m:
        result['error'] = 'No structured data found'
        return result

    try:
        raw = m.group(1).encode().decode('unicode_escape')
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        result['error'] = f'JSON parse error: {e}'
        return result

    # Find the classified data (usually under app_cldp)
    classified = None
    for app_key, app_val in data.items():
        if isinstance(app_val, dict) and 'data' in app_val:
            if 'classified' in app_val['data']:
                classified = app_val['data']['classified']
                break

    if not classified:
        result['error'] = 'No classified data in UFRN'
        return result

    # Basic info
    result['title'] = classified.get('title', '')[:200]
    sections = classified.get('sections', {})

    # Hard facts
    hf = sections.get('hardFacts', {})
    result['type_title'] = hf.get('title', '')
    for fact in hf.get('facts', []):
        ftype = fact.get('type', '')
        fval = fact.get('splitValue', fact.get('value', ''))
        if ftype == 'numberOfRooms':
            result['rooms'] = fval
        elif ftype == 'livingSpace':
            result['area'] = fval
        elif ftype == 'numberOfFloors':
            result['floor'] = fval
        elif ftype == 'plotArea':
            result['plot_area'] = fval

    # Price
    price_sec = sections.get('price', {})
    base_price = price_sec.get('base', {})
    main_price = base_price.get('main', {})
    price_val = main_price.get('value', {})
    if isinstance(price_val, dict):
        result['price'] = price_val.get('main', {}).get('ariaLabel', '')
    result['price_note'] = price_sec.get('note', '')

    # Energy section (heating, year, condition, energy class)
    energy = sections.get('energy', {})
    for feat in energy.get('features', []):
        ftype = feat.get('type', '')
        fval = feat.get('value', '')
        if ftype == 'yearOfConstruction':
            result['year'] = fval
        elif ftype == 'state':
            result['condition'] = fval
        elif ftype == 'heatingSystem':
            result['heating'] = fval
        elif ftype == 'energySource':
            result['energy_source'] = fval

    # Energy certificates (HWB, fGEE)
    for cert in energy.get('certificates', []):
        for scale in cert.get('scales', []):
            name = scale.get('name', '')
            eff = scale.get('efficiencyClass', {})
            rating = eff.get('rating', '')
            for sv in scale.get('values', []):
                val = sv.get('value', '')
                if 'HWB' in name or 'Heizwärme' in name:
                    result['hwb'] = val
                    result['hwb_class'] = rating
                elif 'fGEE' in name or 'Gesamtenergieeffizienz' in name:
                    result['fgee'] = val
                    result['fgee_class'] = rating

    # Location
    loc = sections.get('location', {})
    addr = loc.get('address', {})
    result['city'] = addr.get('city', '')
    result['zip'] = addr.get('zipCode', '')

    # Features (parking etc)
    features = sections.get('features', {})
    if isinstance(features, dict):
        feat_items = features.get('items', features.get('features', []))
        if isinstance(feat_items, list):
            feat_texts = []
            for fi in feat_items:
                if isinstance(fi, dict):
                    feat_texts.append(fi.get('value', fi.get('label', str(fi))))
                elif isinstance(fi, str):
                    feat_texts.append(fi)
            result['features'] = ', '.join(feat_texts[:15])

    # Tags
    tags = classified.get('tags', {})
    result['is_new'] = tags.get('isNew', False)
    result['is_exclusive'] = tags.get('isExclusive', False)

    # Metadata
    meta = classified.get('metadata', {})
    result['created'] = meta.get('creationDate', '')
    result['updated'] = meta.get('updateDate', '')

    return result


def main():
    parser = argparse.ArgumentParser(description='Immowelt Real Estate Search')
    parser.add_argument('--country', default='at', choices=['at', 'de'],
                        help='Country: at (Austria) or de (Germany)')
    parser.add_argument('--location',
                        help='Location slug (e.g., wien, niederoesterreich, bayern, berlin)')
    parser.add_argument('--type', default='apartment',
                        choices=['apartment', 'house', 'apartment-rent', 'house-rent'],
                        help='Property type')
    parser.add_argument('--max-price', type=int, help='Maximum price in EUR')
    parser.add_argument('--min-rooms', type=int, help='Minimum rooms')
    parser.add_argument('--max-pages', type=int, default=5, help='Max pages (default: 5)')
    parser.add_argument('--expose', help='Get expose details by UUID')
    parser.add_argument('--with-details', action='store_true',
                        help='Fetch expose page for each listing (slower)')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()

    session = create_session()

    if args.expose:
        result = get_expose(session, args.expose, args.country)
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            for k, v in result.items():
                if v:
                    print(f'{k}: {v}')
        return

    if not args.location:
        parser.error('--location is required for search')

    total, listings = search_listings(
        session, args.country, args.location, args.type,
        args.max_price, args.min_rooms, args.max_pages
    )

    if args.with_details:
        for listing in listings:
            if listing.get('expose_id'):
                detail = get_expose(session, listing['expose_id'], args.country)
                listing.update(detail)
                time.sleep(0.3)

    if args.format == 'json':
        print(json.dumps({'total': total, 'listings': listings},
                         indent=2, ensure_ascii=False))
    else:
        type_label = args.type.replace('-', ' ').title()
        print(f"=== {type_label} in {args.location} (max {args.max_price or 'any'} EUR) ===")
        print(f"Fetched: {len(listings)}\n")

        for i, l in enumerate(listings, 1):
            print(f"[{i}] {l.get('title', l.get('id', '?'))}")
            print(f"    Price: {l.get('price_text', l.get('price', '?'))}")
            print(f"    Rooms: {l.get('rooms', '?')} | Area: {l.get('area', '?')} m²")
            print(f"    Address: {l.get('address', l.get('city', '?'))}")
            if l.get('heating') or l.get('condition') or l.get('year'):
                print(f"    Heating: {l.get('heating', '?')} | Source: {l.get('energy_source', '?')}")
                print(f"    Condition: {l.get('condition', '?')} | Year: {l.get('year', '?')}")
            if l.get('hwb'):
                print(f"    HWB: {l.get('hwb', '?')} ({l.get('hwb_class', '?')})")
            if l.get('features'):
                print(f"    Features: {l.get('features', '')}")
            print(f"    URL: {l.get('url', '?')}")
            if l.get('is_new'):
                print(f"    [NEW LISTING]")
            print()


if __name__ == '__main__':
    main()
