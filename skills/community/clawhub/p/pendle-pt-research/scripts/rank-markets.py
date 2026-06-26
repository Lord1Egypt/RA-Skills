#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_IN = DATA / 'markets.latest.json'
DEFAULT_OUT = DATA / 'ranked.latest.json'
RISK_OVERRIDES = DATA / 'risk-overrides.json'
MARKET_NOTES = DATA / 'market-notes.json'
STABLE_SUBTYPES = DATA / 'stable-subtype-overrides.json'


def load_overrides():
    if RISK_OVERRIDES.exists():
        return json.loads(RISK_OVERRIDES.read_text())
    return {'protocols': {}, 'underlyingHints': []}


def load_notes():
    if MARKET_NOTES.exists():
        return json.loads(MARKET_NOTES.read_text())
    return {
        'excludeMarketIds': [],
        'excludeProtocols': [],
        'excludeUnderlyingSymbols': [],
        'marketOverrides': {},
        'protocolOverrides': {},
        'notes': {},
    }


def load_stable_subtypes():
    if STABLE_SUBTYPES.exists():
        return json.loads(STABLE_SUBTYPES.read_text())
    return {'symbolHints': {}, 'protocolHints': {}}


def risk_tier(protocol: str, underlying: str, overrides: dict):
    p = (protocol or '').strip()
    u = (underlying or '').strip()
    protocol_map = overrides.get('protocols', {})
    if p in protocol_map:
        entry = protocol_map[p]
        return entry['tier'], float(entry['score']), entry.get('note', '')
    lower_underlying = u.lower()
    for hint in overrides.get('underlyingHints', []):
        if hint['match'].lower() in lower_underlying:
            return hint['tier'], float(hint['score']), hint.get('note', '')
    return 'medium', 0.5, 'No explicit override; default medium-risk heuristic.'


def time_scores(days: float):
    hold = 0.0
    rot = 0.0
    if 30 <= days <= 120:
        hold = 1.0
    elif 15 <= days < 30 or 120 < days <= 150:
        hold = 0.7
    elif 7 <= days < 15:
        hold = 0.4
    if 0 <= days <= 30:
        rot = 1.0
    elif 30 < days <= 45:
        rot = 0.6
    elif 45 < days <= 60:
        rot = 0.3
    return hold, rot


def apy_score(implied_apy: Optional[float]):
    if implied_apy is None:
        return 0.0
    x = implied_apy
    if x >= 0.25:
        return 1.0
    if x >= 0.18:
        return 0.85
    if x >= 0.12:
        return 0.7
    if x >= 0.08:
        return 0.55
    if x >= 0.04:
        return 0.35
    return 0.15


def liquidity_score(liq: float, ratio: float):
    liq_s = 0.0
    if liq >= 50_000_000:
        liq_s = 1.0
    elif liq >= 10_000_000:
        liq_s = 0.8
    elif liq >= 3_000_000:
        liq_s = 0.6
    elif liq >= 1_000_000:
        liq_s = 0.4
    elif liq >= 250_000:
        liq_s = 0.25
    ratio_s = min(max(ratio / 0.5, 0), 1.0)
    return round(0.7 * liq_s + 0.3 * ratio_s, 4)


STABLE_HINTS = ['usd', 'usdc', 'usdt', 'dai', 'fdusd', 'usde', 'susde', 'apyusd', 'apxusd', 'nusd', 'msusd', 'msy', 'usdg', 'reusd', 'upusdc', 'avusd', 'satusd']
ETH_HINTS = ['eth', 'steth', 'weth', 'oeth', 'sweth', 'rseth', 'ezeth', 'weeth', 'unieth']
BTC_HINTS = ['btc', 'wbtc', 'cbbtc', 'dlcbtc']


def asset_family(symbol: str, name: str):
    text = f"{symbol or ''} {name or ''}".lower()
    if any(h in text for h in STABLE_HINTS):
        return 'stable'
    if any(h in text for h in ETH_HINTS):
        return 'eth-beta'
    if any(h in text for h in BTC_HINTS):
        return 'btc-beta'
    return 'other'


def stable_subtype(symbol: str, name: str, protocol: str, family: str, subtype_overrides: dict):
    if family != 'stable':
        return None
    s = (symbol or '').strip()
    n = (name or '').strip()
    p = (protocol or '').strip()
    for key, subtype in (subtype_overrides.get('symbolHints') or {}).items():
        if key.lower() in s.lower() or key.lower() in n.lower():
            return subtype
    if p in (subtype_overrides.get('protocolHints') or {}):
        return subtype_overrides['protocolHints'][p]
    return 'stable-other'


def choose_bucket(hold_score: float, rot_score: float):
    if hold_score >= 0.65 and rot_score >= 0.65:
        return 'both'
    if hold_score >= rot_score:
        return 'hold-to-par'
    return 'near-par rotation'


def verdict(score: float):
    if score >= 0.8:
        return 'strong'
    if score >= 0.65:
        return 'good'
    if score >= 0.5:
        return 'mixed'
    return 'avoid'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(DEFAULT_IN))
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    ap.add_argument('--min-liquidity', type=float, default=250000)
    ap.add_argument('--chains', nargs='*', help='Filter by chain names, e.g. base ethereum arbitrum')
    ap.add_argument('--min-days', type=float, default=0)
    ap.add_argument('--max-days', type=float, default=99999)
    ap.add_argument('--risk', nargs='*', choices=['low', 'medium', 'high'])
    ap.add_argument('--asset-family', nargs='*', choices=['stable', 'eth-beta', 'btc-beta', 'other'])
    ap.add_argument('--stable-subtype', nargs='*', choices=['stable-major', 'stable-synthetic', 'stable-rwa', 'stable-other'])
    ap.add_argument('--stable-only', action='store_true')
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text())
    overrides = load_overrides()
    notes = load_notes()
    subtype_overrides = load_stable_subtypes()
    wanted_chains = {c.lower() for c in (args.chains or [])}
    wanted_risk = set(args.risk or [])
    wanted_families = set(args.asset_family or [])
    wanted_stable_subtypes = set(args.stable_subtype or [])
    if args.stable_only:
        wanted_families.add('stable')
    ranked = []
    for m in payload['markets']:
        if m.get('id') in set(notes.get('excludeMarketIds', [])):
            continue
        if m.get('protocol') in set(notes.get('excludeProtocols', [])):
            continue
        if m.get('underlyingSymbol') in set(notes.get('excludeUnderlyingSymbols', [])):
            continue
        if (m.get('liquidityUsd') or 0) < args.min_liquidity:
            continue
        days = float(m['daysToExpiry'])
        if days < args.min_days or days > args.max_days:
            continue
        if wanted_chains and str(m.get('chain', '')).lower() not in wanted_chains:
            continue
        family = asset_family(m.get('underlyingSymbol') or '', m.get('underlyingName') or '')
        subtype = stable_subtype(m.get('underlyingSymbol') or '', m.get('underlyingName') or '', m.get('protocol') or '', family, subtype_overrides)
        if wanted_families and family not in wanted_families:
            continue
        if wanted_stable_subtypes and subtype not in wanted_stable_subtypes:
            continue
        hold_time, rot_time = time_scores(days)
        apy = apy_score(m.get('impliedApy'))
        risk_label, risk_num, risk_note = risk_tier(m.get('protocol'), m.get('underlyingName') or m.get('underlyingSymbol'), overrides)
        protocol_override = (notes.get('protocolOverrides') or {}).get(m.get('protocol') or '')
        if protocol_override:
            risk_label = protocol_override.get('riskTier', risk_label)
            risk_num = float(protocol_override.get('riskScore', risk_num))
            risk_note = protocol_override.get('comment', risk_note)
        if wanted_risk and risk_label not in wanted_risk:
            continue
        liq = liquidity_score(m.get('liquidityUsd') or 0, m.get('volumeLiquidityRatio') or 0)
        hold_score = round(0.30 * hold_time + 0.30 * apy + 0.25 * risk_num + 0.15 * liq, 4)
        rot_score = round(0.30 * rot_time + 0.30 * apy + 0.20 * risk_num + 0.20 * liq, 4)
        best_fit = choose_bucket(hold_score, rot_score)
        final_score = max(hold_score, rot_score)
        market_note = ((notes.get('notes') or {}).get(m.get('id') or '') or {})
        if market_note.get('exclude'):
            continue
        score_adjustment = float(market_note.get('scoreAdjustment', 0.0))
        final_score = round(final_score + score_adjustment, 4)
        if market_note.get('bucket') in ('hold-to-par', 'near-par rotation', 'both'):
            best_fit = market_note['bucket']
        allocation_band = 'small'
        if family == 'stable' and subtype in ('stable-major', 'stable-rwa') and final_score >= 0.75:
            allocation_band = 'medium'
        elif final_score < 0.6 or risk_label == 'high':
            allocation_band = 'tiny'

        ranked.append({
            **m,
            'assetFamily': family,
            'stableSubtype': subtype,
            'riskTier': risk_label,
            'riskScore': risk_num,
            'riskNote': risk_note,
            'liquidityScore': liq,
            'apyScore': apy,
            'holdToParScore': hold_score,
            'rotationScore': rot_score,
            'bestFit': best_fit,
            'finalScore': final_score,
            'manualScoreAdjustment': score_adjustment,
            'manualComment': market_note.get('comment'),
            'allocationBand': allocation_band,
            'allocationSuggestion': {
                'tiny': 'watchlist / very small only',
                'small': 'small exploratory size',
                'medium': 'medium starter size if thesis still checks out',
            }[allocation_band],
            'verdict': verdict(final_score),
        })

    ranked.sort(key=lambda x: (-x['finalScore'], x['daysToExpiry']))
    result = {
        'generatedAt': payload['generatedAt'],
        'sourceMarketCount': payload['marketCount'],
        'rankedCount': len(ranked),
        'markets': ranked,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(str(out))
    print(f'Ranked {len(ranked)} PT markets')


if __name__ == '__main__':
    main()
