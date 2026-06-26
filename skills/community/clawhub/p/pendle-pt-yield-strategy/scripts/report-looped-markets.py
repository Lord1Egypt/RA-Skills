#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_IN = DATA / 'loop-ranked.latest.json'


def pct(x):
    return 'n/a' if x is None else f'{x*100:.2f}%'


def usd(x):
    if x is None:
        return 'n/a'
    if x >= 1_000_000_000:
        return f'${x/1_000_000_000:.2f}B'
    if x >= 1_000_000:
        return f'${x/1_000_000:.2f}M'
    if x >= 1_000:
        return f'${x/1_000:.0f}K'
    return f'${x:.0f}'


def integration_summary(integrations):
    if not integrations:
        return 'no verified money-market integration yet'
    bits = []
    for i in integrations[:2]:
        assets = ','.join(i.get('borrowAssets') or []) or 'unknown borrow asset'
        bits.append(f"{i.get('venue')} borrow {assets} ({i.get('venueConfidence')})")
    return '; '.join(bits)


def line(m):
    return (
        f"- {m['ptName']} | {m['chain']} | APY {pct(m.get('impliedApy'))} | "
        f"{m.get('daysToExpiry',0):.1f}d | liq {usd(m.get('liquidityUsd'))} | "
        f"loop score {m.get('loopScore',0):.2f} | leverage {m.get('practicalLeverageBand')} | "
        f"{integration_summary(m.get('integrations') or [])}"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(DEFAULT_IN))
    ap.add_argument('--top', type=int, default=10)
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text())
    markets = payload['markets']
    strong = [m for m in markets if m['verdict'] in ('strong', 'good')][:args.top]
    watch = [m for m in markets if m['verdict'] == 'mixed'][:args.top]
    unverified = [m for m in markets if not (m.get('integrations') or [])][:args.top]

    print(f"Pendle PT loop report ({payload['rankedCount']} ranked candidates)\n")
    print('Best PT looping ideas')
    for m in strong:
        print(line(m))

    print('\nWatchlist / thinner or shorter-duration ideas')
    for m in watch:
        print(line(m))

    print('\nUnverified integration candidates')
    for m in unverified:
        print(line(m))


if __name__ == '__main__':
    main()
