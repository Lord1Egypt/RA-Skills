#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_IN = DATA / 'loop-venues.latest.json'
DEFAULT_OUT = DATA / 'loop-ranked.latest.json'


def apy_score(x: float):
    if x >= 0.20:
        return 1.0
    if x >= 0.15:
        return 0.85
    if x >= 0.12:
        return 0.72
    if x >= 0.10:
        return 0.62
    if x >= 0.08:
        return 0.50
    return 0.20


def liquidity_score(liq: float):
    if liq >= 20_000_000:
        return 1.0
    if liq >= 10_000_000:
        return 0.85
    if liq >= 5_000_000:
        return 0.70
    if liq >= 3_000_000:
        return 0.60
    if liq >= 1_000_000:
        return 0.40
    return 0.20


def duration_score(days: float):
    if 21 <= days <= 120:
        return 1.0
    if 7 <= days < 21:
        return 0.65
    if 120 < days <= 150:
        return 0.65
    return 0.30


def leverage_score(band: str):
    return {
        'moderate': 0.80,
        'light': 0.55,
        'aggressive': 0.95,
        'none': 0.0,
    }.get(band or 'none', 0.25)


def verified_integrations(integrations: list):
    return [i for i in integrations if i.get('venueConfidence') == 'verified-live']


def integration_score(integrations: list):
    if not integrations:
        return 0.0
    if verified_integrations(integrations):
        return 0.95
    confirmed = any(i.get('venueConfidence') == 'confirmed-by-user' for i in integrations)
    if confirmed:
        return 0.90
    return 0.60


def borrow_asset_bonus(symbol: str):
    s = (symbol or '').upper()
    if s == 'USDC':
        return 1.0
    if s in ('USDT', 'FRXUSD', 'DAI', 'USD0', 'RLUSD'):
        return 0.75
    if 'USD' in s:
        return 0.65
    return 0.35


def spread_score(pt_apy: float, borrow_apy):
    if borrow_apy is None:
        return 0.45
    spread = pt_apy - borrow_apy
    if spread >= 0.10:
        return 1.0
    if spread >= 0.07:
        return 0.82
    if spread >= 0.05:
        return 0.70
    if spread >= 0.03:
        return 0.55
    if spread >= 0.01:
        return 0.40
    return 0.15


def lltv_score(x):
    if x is None:
        return 0.35
    if x >= 0.91:
        return 0.95
    if x >= 0.86:
        return 0.80
    if x >= 0.80:
        return 0.65
    if x >= 0.75:
        return 0.50
    return 0.30


def utilization_penalty(util):
    if util is None:
        return 0.0
    if util >= 0.98:
        return -0.18
    if util >= 0.95:
        return -0.12
    if util >= 0.90:
        return -0.06
    return 0.0


def borrow_depth_score(borrow_usd, supply_usd):
    x = max(borrow_usd or 0.0, supply_usd or 0.0)
    if x >= 20_000_000:
        return 1.0
    if x >= 10_000_000:
        return 0.85
    if x >= 5_000_000:
        return 0.72
    if x >= 1_000_000:
        return 0.50
    if x >= 100_000:
        return 0.30
    return 0.10


def pick_best_verified_route(pt_apy: float, integrations: list):
    best = None
    best_score = -999
    for i in verified_integrations(integrations):
        route_score = (
            0.40 * spread_score(pt_apy, i.get('borrowApy')) +
            0.20 * lltv_score(i.get('lltv')) +
            0.20 * borrow_depth_score(i.get('borrowAssetsUsd'), i.get('supplyAssetsUsd')) +
            0.20 * borrow_asset_bonus(i.get('loanAssetSymbol') or (i.get('borrowAssets') or [None])[0])
        ) + utilization_penalty(i.get('utilization'))
        if route_score > best_score:
            best_score = route_score
            best = i
    return best, max(best_score, 0.0)


def verdict(score: float):
    if score >= 0.78:
        return 'strong'
    if score >= 0.64:
        return 'good'
    if score >= 0.50:
        return 'mixed'
    return 'avoid'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(DEFAULT_IN))
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text())
    ranked = []
    for m in payload['markets']:
        pt_apy_raw = m.get('impliedApy') or 0.0
        apy = apy_score(pt_apy_raw)
        liq = liquidity_score(m.get('liquidityUsd') or 0.0)
        dur = duration_score(m.get('daysToExpiry') or 0.0)
        integ = integration_score(m.get('integrations') or [])
        lev = leverage_score(m.get('practicalLeverageBand'))
        best_route, route_score = pick_best_verified_route(pt_apy_raw, m.get('integrations') or [])

        score = round(
            0.24 * apy +
            0.16 * liq +
            0.12 * dur +
            0.16 * integ +
            0.12 * lev +
            0.20 * route_score,
            4,
        )
        ranked.append({
            **m,
            'loopApyScore': apy,
            'loopLiquidityScore': liq,
            'loopDurationScore': dur,
            'loopIntegrationScore': integ,
            'loopLeverageScore': lev,
            'bestVerifiedRoute': best_route,
            'bestVerifiedRouteScore': round(route_score, 4),
            'loopScore': score,
            'verdict': verdict(score),
        })

    ranked.sort(
        key=lambda x: (
            -x['loopScore'],
            -(x.get('bestVerifiedRouteScore') or 0),
            -(x.get('impliedApy') or 0),
            x.get('daysToExpiry') or 99999,
        )
    )
    out = {
        'generatedAt': payload.get('generatedAt'),
        'sourceLoopCandidateCount': payload.get('loopCandidateCount'),
        'rankedCount': len(ranked),
        'markets': ranked,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(str(out_path))
    print(f"Ranked {len(ranked)} PT loop candidates")


if __name__ == '__main__':
    main()
