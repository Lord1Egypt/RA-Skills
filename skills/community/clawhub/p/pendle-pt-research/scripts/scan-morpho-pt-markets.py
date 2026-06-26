#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_PT_INPUT = DATA / 'ranked.latest.json'
DEFAULT_OUT = DATA / 'morpho-pt-markets.latest.json'
GRAPHQL_URL = 'https://api.morpho.org/graphql'


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def gql(query: str, variables: dict):
    req = Request(
        GRAPHQL_URL,
        data=json.dumps({'query': query, 'variables': variables}).encode(),
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8', errors='ignore'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(DEFAULT_PT_INPUT))
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    ap.add_argument('--chain', default='ethereum')
    ap.add_argument('--stable-only', action='store_true')
    ap.add_argument('--min-apy', type=float, default=0.08)
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text())
    pts = []
    for m in payload['markets']:
        if (m.get('chain') or '').lower() != args.chain.lower():
            continue
        if args.stable_only and m.get('assetFamily') != 'stable':
            continue
        if (m.get('impliedApy') or 0.0) < args.min_apy:
            continue
        if not m.get('ptAddress'):
            continue
        pts.append(m)

    pt_by_addr = {m['ptAddress'].lower(): m for m in pts}
    addresses = list(pt_by_addr.keys())

    query = '''
    query Markets($addrs:[String!]) {
      markets(first: 200, where: { chainId_in:[1], collateralAssetAddress_in:$addrs, listed:true }) {
        items {
          marketId
          lltv
          collateralAsset { address symbol name }
          loanAsset { address symbol name }
          state {
            borrowApy
            supplyApy
            borrowAssetsUsd
            supplyAssetsUsd
            utilization
          }
        }
      }
    }
    '''
    obj = gql(query, {'addrs': addresses})
    items = obj['data']['markets']['items']

    rows = []
    for it in items:
        caddr = (it.get('collateralAsset') or {}).get('address', '').lower()
        src = pt_by_addr.get(caddr)
        rows.append({
            'protocol': 'Morpho',
            'marketId': it.get('marketId'),
            'ptAddress': caddr,
            'ptSymbol': (it.get('collateralAsset') or {}).get('symbol'),
            'ptName': (it.get('collateralAsset') or {}).get('name'),
            'loanAssetAddress': (it.get('loanAsset') or {}).get('address'),
            'loanAssetSymbol': (it.get('loanAsset') or {}).get('symbol'),
            'loanAssetName': (it.get('loanAsset') or {}).get('name'),
            'lltv': float(it.get('lltv') or 0) / 1e18,
            'borrowApy': (it.get('state') or {}).get('borrowApy'),
            'supplyApy': (it.get('state') or {}).get('supplyApy'),
            'borrowAssetsUsd': (it.get('state') or {}).get('borrowAssetsUsd'),
            'supplyAssetsUsd': (it.get('state') or {}).get('supplyAssetsUsd'),
            'utilization': (it.get('state') or {}).get('utilization'),
            'verified': True,
            'sourceType': 'live-graphql',
            'matchedPendleMarket': {
                'marketAddress': src.get('marketAddress') if src else None,
                'impliedApy': src.get('impliedApy') if src else None,
                'daysToExpiry': src.get('daysToExpiry') if src else None,
                'underlyingSymbol': src.get('underlyingSymbol') if src else None,
                'liquidityUsd': src.get('liquidityUsd') if src else None,
                'bestFit': src.get('bestFit') if src else None,
            },
        })

    out = {
        'generatedAt': iso_now(),
        'sourceRankedCount': len(pts),
        'verifiedMarketCount': len(rows),
        'markets': rows,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(str(out_path))
    print(f'Verified {len(rows)} Morpho PT-collateral markets')


if __name__ == '__main__':
    main()
