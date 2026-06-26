#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = 'https://api-v2.pendle.finance/core'
CHAIN_IDS = [1, 10, 56, 146, 999, 5000, 8453, 9745, 42161, 80094]
CHAIN_NAMES = {
    1: 'ethereum',
    10: 'optimism',
    56: 'bnb',
    146: 'sonic',
    999: 'hyperliquid',
    5000: 'mantle',
    8453: 'base',
    9745: 'plume',
    42161: 'arbitrum',
    80094: 'berachain',
}
OUT = Path(__file__).resolve().parent.parent / 'data'
OUT.mkdir(parents=True, exist_ok=True)


def fetch_json(url: str):
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://app.pendle.finance',
        'Referer': 'https://app.pendle.finance/',
    })
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def days_to(expiry: str):
    dt = datetime.fromisoformat(expiry.replace('Z', '+00:00'))
    return (dt - datetime.now(timezone.utc)).total_seconds() / 86400


def normalize_market(m: dict):
    expiry = m.get('expiry')
    if not expiry:
        return None
    pt = m.get('pt') or {}
    if pt.get('baseType') != 'PT':
        return None
    liquidity = (m.get('liquidity') or {}).get('usd') or 0
    volume = (m.get('tradingVolume') or {}).get('usd') or 0
    pt_price = ((pt.get('price') or {}).get('usd')) or None
    sy = m.get('sy') or {}
    underlying = m.get('underlyingAsset') or {}
    protocol = m.get('protocol') or ''
    return {
        'id': m.get('id'),
        'chainId': m.get('chainId'),
        'chain': CHAIN_NAMES.get(m.get('chainId'), str(m.get('chainId'))),
        'marketAddress': m.get('address'),
        'marketSymbol': m.get('symbol'),
        'expiry': expiry,
        'daysToExpiry': round(days_to(expiry), 2),
        'ptSymbol': pt.get('symbol'),
        'ptName': pt.get('proName') or pt.get('name'),
        'ptAddress': pt.get('address'),
        'ptPriceUsd': pt_price,
        'underlyingSymbol': underlying.get('proSymbol') or underlying.get('symbol'),
        'underlyingName': underlying.get('proName') or underlying.get('name'),
        'underlyingPriceUsd': ((underlying.get('price') or {}).get('usd')),
        'sySymbol': sy.get('proSymbol') or sy.get('symbol'),
        'protocol': protocol,
        'liquidityUsd': liquidity,
        'tradingVolumeUsd': volume,
        'volumeLiquidityRatio': (volume / liquidity) if liquidity else 0,
        'impliedApy': m.get('impliedApy'),
        'aggregatedApy': m.get('aggregatedApy'),
        'underlyingApy': m.get('underlyingApy'),
        'ptDiscount': m.get('ptDiscount'),
        'ptRoi': m.get('ptRoi'),
        'ytFloatingApy': m.get('ytFloatingApy'),
        'isActive': m.get('isActive'),
        'isFeatured': m.get('isFeatured'),
        'isPopular': m.get('isPopular'),
        'isNew': m.get('isNew'),
        'categoryIds': m.get('categoryIds') or [],
        'assetRepresentation': m.get('assetRepresentation'),
        'simpleName': m.get('simpleName'),
        'dataUpdatedAt': m.get('dataUpdatedAt'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chain-id', type=int, action='append', help='Limit to one or more chain IDs')
    ap.add_argument('--page-size', type=int, default=100)
    ap.add_argument('--active-only', action='store_true')
    ap.add_argument('--out', default=str(OUT / 'markets.latest.json'))
    args = ap.parse_args()

    chain_ids = args.chain_id or CHAIN_IDS
    all_markets = []
    for chain_id in chain_ids:
        skip = 0
        while True:
            query = urlencode({'select': 'pro', 'limit': args.page_size, 'skip': skip})
            url = f'{API_BASE}/v1/{chain_id}/markets?{query}'
            payload = fetch_json(url)
            results = payload.get('results', [])
            for raw in results:
                nm = normalize_market(raw)
                if not nm:
                    continue
                if args.active_only and not nm['isActive']:
                    continue
                all_markets.append(nm)
            skip += len(results)
            total = payload.get('total', 0)
            if not results or skip >= total:
                break

    result = {
        'generatedAt': iso_now(),
        'marketCount': len(all_markets),
        'chains': [CHAIN_NAMES.get(c, str(c)) for c in chain_ids],
        'markets': sorted(all_markets, key=lambda x: (x['daysToExpiry'], -(x['impliedApy'] or 0))),
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2))
    print(str(out_path))
    print(f"Scanned {len(all_markets)} PT markets across {len(chain_ids)} chains")


if __name__ == '__main__':
    main()
