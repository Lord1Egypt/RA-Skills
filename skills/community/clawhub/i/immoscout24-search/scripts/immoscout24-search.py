#!/usr/bin/env python3
"""
ImmoScout24 Search via Mobile API
Usage:
  python3 immoscout24-search.py --region /de/bayern/passau-kreis --type apartmentbuy --max-price 300000
  python3 immoscout24-search.py --region /de/bayern/passau-kreis --type housebuy --max-price 350000
  python3 immoscout24-search.py --expose 166875438

Real estate types: apartmentbuy, housebuy, apartmentrent, houserent
Region format: /de/{bundesland}/{kreis-oder-stadt}
  Examples:
    /de/bayern/passau-kreis
    /de/bayern/passau
"""
import argparse
import json
import sys
import uuid
import requests


def create_session():
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'ImmoScout_27.3_26.0_._iOS',
        'Accept': 'application/json',
        'Accept-Language': 'de-DE',
        'X-Device-Id': str(uuid.uuid4()),
    })
    return s


def search_listings(session, region, real_estate_type, max_price=None, min_rooms=None, max_pages=5):
    all_items = []
    for page in range(1, max_pages + 1):
        params = {
            'realestatetype': real_estate_type,
            'searchType': 'region',
            'geocodes': region,
            'pagenumber': page,
        }
        if max_price:
            params['price'] = f'-{max_price}'
        if min_rooms:
            params['numberofrooms'] = f'{min_rooms}-'

        resp = session.post(
            'https://api.mobile.immobilienscout24.de/search/list',
            params=params,
            json={'supportedREsultListType': [], 'userData': {}}
        )
        if resp.status_code != 200:
            print(f"Error page {page}: {resp.status_code} {resp.text[:200]}", file=sys.stderr)
            break

        data = resp.json()
        items = data.get('resultListItems', [])
        total = data.get('totalResults', 0)
        num_pages = data.get('numberOfPages', 1)

        for entry in items:
            if entry.get('type') != 'EXPOSE_RESULT':
                continue
            item = entry.get('item', {})
            attrs = item.get('attributes', [])
            all_items.append({
                'id': item.get('id'),
                'title': (item.get('title') or '').replace('\n', ' ').strip(),
                'url': f"https://www.immobilienscout24.de/expose/{item.get('id')}",
                'address': item.get('address', {}).get('line', ''),
                'postcode': item.get('address', {}).get('postcode', ''),
                'price': attrs[0].get('value', '') if len(attrs) > 0 else '',
                'area': attrs[1].get('value', '') if len(attrs) > 1 else '',
                'rooms': attrs[2].get('value', '') if len(attrs) > 2 else '',
                'published': item.get('published', ''),
                'isPrivate': item.get('isPrivate', False),
                'type': item.get('realEstateType', ''),
            })

        if page >= num_pages:
            break

    return {'total': total, 'listings': all_items}


def get_expose_details(session, expose_id):
    resp = session.get(f'https://api.mobile.immobilienscout24.de/expose/{expose_id}')
    if resp.status_code != 200:
        return {'error': f'{resp.status_code}: {resp.text[:200]}'}

    data = resp.json()
    txt = json.dumps(data, ensure_ascii=False)

    # Extract key fields from the nested structure
    result = {'id': expose_id, 'url': f'https://www.immobilienscout24.de/expose/{expose_id}'}

    # Parse sections for structured data
    sections = []
    if isinstance(data, list):
        sections = data
    elif isinstance(data, dict):
        sections = data.get('sections', data.get('items', [data]))

    for section in sections if isinstance(sections, list) else [sections]:
        if not isinstance(section, dict):
            continue
        for attr in section.get('attributes', []):
            if not isinstance(attr, dict):
                continue
            label = attr.get('label', '').rstrip(':').strip()
            text = attr.get('text', attr.get('value', ''))
            if label and text:
                result[label] = text

        # Check nested sections
        for sub in section.get('sections', []):
            if not isinstance(sub, dict):
                continue
            for attr in sub.get('attributes', []):
                if not isinstance(attr, dict):
                    continue
                label = attr.get('label', '').rstrip(':').strip()
                text = attr.get('text', attr.get('value', ''))
                if label and text:
                    result[label] = text

    # Extract obj_ fields from tracking/metadata
    for key in ['obj_heatingType', 'obj_parkingSpace', 'obj_condition', 'obj_buildingEnergyRatingType',
                'obj_thermalCharacteristic', 'obj_yearConstructed', 'obj_numberOfRooms', 
                'obj_livingSpace', 'obj_purchasePrice', 'obj_cellar', 'obj_lift']:
        idx = txt.find(f'"{key}"')
        if idx >= 0:
            # Extract value after the key
            val_start = txt.find(':', idx) + 1
            val_end = txt.find(',', val_start)
            if val_end < 0:
                val_end = txt.find('}', val_start)
            val = txt[val_start:val_end].strip().strip('"')
            result[key] = val

    return result


def main():
    parser = argparse.ArgumentParser(description='ImmoScout24 Mobile API Search')
    parser.add_argument('--region', help='Region geocode (e.g., /de/bayern/passau-kreis)')
    parser.add_argument('--type', default='apartmentbuy',
                        help='Real estate type: apartmentbuy, housebuy, apartmentrent, houserent')
    parser.add_argument('--max-price', type=int, help='Maximum price in EUR')
    parser.add_argument('--min-rooms', type=float, help='Minimum number of rooms')
    parser.add_argument('--max-pages', type=int, default=5, help='Max pages to fetch (default: 5)')
    parser.add_argument('--expose', help='Get details for a specific expose ID')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='Output format')
    args = parser.parse_args()

    session = create_session()

    if args.expose:
        result = get_expose_details(session, args.expose)
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            for k, v in result.items():
                print(f'{k}: {v}')
        return

    if not args.region:
        parser.error('--region is required for search')

    result = search_listings(session, args.region, args.type, args.max_price, args.min_rooms, args.max_pages)

    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Total: {result['total']} listings\n")
        for i, listing in enumerate(result['listings'], 1):
            print(f"[{i}] {listing['title']}")
            print(f"    Price: {listing['price']} | Area: {listing['area']} | Rooms: {listing['rooms']}")
            print(f"    Location: {listing['address']}")
            print(f"    Published: {listing['published']}")
            print(f"    URL: {listing['url']}")
            print()


if __name__ == '__main__':
    main()
