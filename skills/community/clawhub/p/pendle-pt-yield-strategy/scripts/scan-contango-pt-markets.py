#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_PT_INPUT = DATA / 'ranked.latest.json'
DEFAULT_OUT = DATA / 'contango-pt-markets.latest.json'
CONFIG_URL = 'https://raw.githubusercontent.com/contango-xyz/pendle-external-integration/main/config.json'


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def fetch_json(url: str):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json,text/plain,*/*'})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8', errors='ignore'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(DEFAULT_PT_INPUT))
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    ap.add_argument('--chain-id', type=int, default=1)
    ap.add_argument('--stable-only', action='store_true')
    ap.add_argument('--min-apy', type=float, default=0.08)
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text())
    targets = []
    for m in payload['markets']:
        if (m.get('chain') or '').lower() != 'ethereum':
            continue
        if args.stable_only and m.get('assetFamily') != 'stable':
            continue
        if (m.get('impliedApy') or 0.0) < args.min_apy:
            continue
        targets.append(m)

    by_pt = {(m.get('ptAddress') or '').lower(): m for m in targets}
    cfg = fetch_json(CONFIG_URL)
    contango = next((p for p in cfg.get('protocols', []) if (p.get('name') or '').lower() == 'contango'), None)
    pt_meta = ((contango or {}).get('metadata') or {}).get('pt') or []

    matched = []
    for item in pt_meta:
        if item.get('chainId') != args.chain_id:
            continue
        addr = (item.get('address') or '').lower()
        if addr in by_pt:
            src = by_pt[addr]
            matched.append({
                'protocol': 'Contango',
                'ptAddress': addr,
                'integrationUrl': item.get('integrationUrl'),
                'description': item.get('description'),
                'verified': True,
                'sourceType': 'live-github-config',
                'matchedPendleMarket': {
                    'marketAddress': src.get('marketAddress'),
                    'ptName': src.get('ptName'),
                    'impliedApy': src.get('impliedApy'),
                    'daysToExpiry': src.get('daysToExpiry'),
                    'underlyingSymbol': src.get('underlyingSymbol'),
                    'liquidityUsd': src.get('liquidityUsd'),
                },
            })

    out = {
        'generatedAt': iso_now(),
        'targetCount': len(targets),
        'contangoGlobalPtCount': len([x for x in pt_meta if x.get('chainId') == args.chain_id]),
        'verifiedMarketCount': len(matched),
        'markets': matched,
        'notes': 'Contango verification uses the public pendle-external-integration config repo. Zero matches means no exact support confirmation for the current target PT set, not that Contango lacks Pendle PT support globally.',
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(str(out_path))
    print(f"Verified {len(matched)} Contango PT routes out of {len(targets)} target PTs; Contango global PT entries on chain={args.chain_id}: {out['contangoGlobalPtCount']}")


if __name__ == '__main__':
    main()
