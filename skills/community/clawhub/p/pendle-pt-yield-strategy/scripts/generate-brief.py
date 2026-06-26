#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_IN = DATA / 'ranked.latest.json'
DEFAULT_OUT = DATA / 'brief.latest.md'


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


def bullet(m):
    subtype = f"/{m['stableSubtype']}" if m.get('stableSubtype') else ''
    note = m.get('riskNote') or 'n/a'
    return (
        f"- **{m['ptName']}** ({m['chain']}) — {m['daysToExpiry']:.1f}d to par, APY {pct(m.get('impliedApy'))}, "
        f"family `{m.get('assetFamily','n/a')}{subtype}`, risk `{m['riskTier']}`, liquidity {usd(m.get('liquidityUsd'))}, "
        f"best fit `{m['bestFit']}`, suggested size `{m.get('allocationSuggestion','n/a')}`.\n"
        f"  - Risk note: {note}"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(DEFAULT_IN))
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    ap.add_argument('--top', type=int, default=8)
    args = ap.parse_args()
    payload = json.loads(Path(args.input).read_text())
    markets = payload['markets']
    hold = [m for m in markets if m['bestFit'] in ('hold-to-par', 'both')][:args.top]
    rot = [m for m in markets if m['bestFit'] in ('near-par rotation', 'both')][:args.top]
    avoid = [m for m in markets if m['verdict'] == 'avoid'][:args.top]
    stable = [m for m in markets if m.get('assetFamily') == 'stable']
    by_subtype = {}
    for m in stable:
        by_subtype.setdefault(m.get('stableSubtype') or 'stable-other', 0)
        by_subtype[m.get('stableSubtype') or 'stable-other'] += 1

    lines = []
    lines.append(f"# Pendle PT Research Brief\n")
    lines.append(f"Generated from {payload['rankedCount']} ranked markets.\n")
    if by_subtype:
        lines.append('## Stable subtype mix')
        for k, v in sorted(by_subtype.items()):
            lines.append(f"- {k}: {v}")
        lines.append('')
    lines.append('## Best hold-to-par ideas')
    for m in hold:
        lines.append(bullet(m))
    lines.append('')
    lines.append('## Best near-par rotation ideas')
    for m in rot:
        lines.append(bullet(m))
    lines.append('')
    lines.append('## Avoid / low-conviction')
    for m in avoid:
        lines.append(bullet(m))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(lines) + '\n')
    print(str(out))


if __name__ == '__main__':
    main()
