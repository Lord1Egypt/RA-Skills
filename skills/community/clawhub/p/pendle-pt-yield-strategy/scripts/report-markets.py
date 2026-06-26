#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_IN = DATA / 'ranked.latest.json'


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


def line(m):
    risk_note = m.get('riskNote') or ''
    subtype = m.get('stableSubtype')
    subtype_part = f"/{subtype}" if subtype else ''
    note_part = f" | note {risk_note}" if risk_note else ''
    alloc = m.get('allocationSuggestion') or ''
    alloc_part = f" | size {alloc}" if alloc else ''
    return (
        f"- {m['ptName']} | {m['chain']} | {m['daysToExpiry']:.1f}d to par | "
        f"APY {pct(m.get('impliedApy'))} | family {m.get('assetFamily','n/a')}{subtype_part} | risk {m['riskTier']} | "
        f"liq {usd(m.get('liquidityUsd'))} | vol/liq {m.get('volumeLiquidityRatio',0):.2f} | "
        f"fit {m['bestFit']} | score {m['finalScore']:.2f}{alloc_part}{note_part}"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(DEFAULT_IN))
    ap.add_argument('--top', type=int, default=10)
    args = ap.parse_args()
    payload = json.loads(Path(args.input).read_text())
    markets = payload['markets']
    hold = [m for m in markets if m['bestFit'] in ('hold-to-par', 'both')][:args.top]
    rot = [m for m in markets if m['bestFit'] in ('near-par rotation', 'both')][:args.top]
    avoid = [m for m in markets if m['verdict'] == 'avoid'][:args.top]

    print(f"Pendle PT market report ({payload['rankedCount']} ranked markets)\n")
    print('Best hold-to-par ideas')
    for m in hold:
        print(line(m))
    print('\nBest near-par rotation ideas')
    for m in rot:
        print(line(m))
    print('\nAvoid / low-conviction')
    for m in avoid:
        print(line(m))


if __name__ == '__main__':
    main()
