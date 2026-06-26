#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

import requests

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = SKILL_DIR / 'config.json'
EXAMPLE_CONFIG_PATH = SKILL_DIR / 'config.example.json'
DEFAULT_BASE_URL = 'http://127.0.0.1:8787'
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_LIMIT = 10


def load_config() -> Dict[str, Any]:
    config = {
        'base_url': DEFAULT_BASE_URL,
        'timeout_seconds': DEFAULT_TIMEOUT_SECONDS,
        'default_limit': DEFAULT_LIMIT,
    }
    source = DEFAULT_CONFIG_PATH if DEFAULT_CONFIG_PATH.exists() else EXAMPLE_CONFIG_PATH
    if source.exists():
        try:
            config.update(json.loads(source.read_text()))
        except Exception:
            pass
    if os.getenv('MARKETPLACE_API_BASE_URL'):
        config['base_url'] = os.getenv('MARKETPLACE_API_BASE_URL')
    if os.getenv('MARKETPLACE_API_TIMEOUT'):
        try:
            config['timeout_seconds'] = int(os.getenv('MARKETPLACE_API_TIMEOUT'))
        except ValueError:
            pass
    return config


def main() -> int:
    cfg = load_config()
    p = argparse.ArgumentParser(description='Search Facebook Marketplace via local service')
    p.add_argument('--query', required=True)
    p.add_argument('--location', required=True)
    p.add_argument('--radius-km', type=int, default=None)
    p.add_argument('--min-price', type=float, default=None)
    p.add_argument('--max-price', type=float, default=None)
    p.add_argument('--limit', type=int, default=cfg.get('default_limit', DEFAULT_LIMIT))
    p.add_argument('--pickup-only', action='store_true')
    p.add_argument('--sort', choices=['relevance', 'price_asc', 'price_desc', 'local_first'], default='local_first')
    args = p.parse_args()

    params = {
        'query': args.query,
        'location': args.location,
        'limit': args.limit,
    }
    if args.radius_km is not None:
        params['radius_km'] = args.radius_km
    if args.min_price is not None:
        params['min_price'] = args.min_price
    if args.max_price is not None:
        params['max_price'] = args.max_price
    if args.pickup_only:
        params['pickup_only'] = 'true'
    if args.sort:
        params['sort'] = args.sort

    try:
        r = requests.get(f"{cfg['base_url'].rstrip('/')}/search", params=params, timeout=cfg['timeout_seconds'])
        r.raise_for_status()
        payload = r.json()
        raw_results = payload.get('data', {}).get('results', [])
        results = []
        for item in raw_results[: args.limit]:
            results.append({
                'id': item.get('id', ''),
                'title': item.get('title', ''),
                'price': item.get('price'),
                'location': item.get('location', ''),
                'seller_name': item.get('seller_name', ''),
                'image_url': item.get('image_url', ''),
                'listing_url': item.get('listing_url', ''),
            })
        out = {
            'query': args.query,
            'location': args.location,
            'count': len(results),
            'results': results,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except requests.RequestException as e:
        print(json.dumps({'error': 'connection_error', 'message': str(e)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 3
    except Exception as e:
        print(json.dumps({'error': 'unexpected_error', 'message': str(e)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
