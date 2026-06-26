#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_MARKETS = DATA / 'ranked.latest.json'
DEFAULT_PENCOSYSTEM = DATA / 'pencosystem.latest.json'
DEFAULT_OUT = DATA / 'loop-venues.latest.json'


KNOWN_PARTNER_MATCHES = {
    'Morpho': {'category': 'money market'},
    'Euler': {'category': 'money market'},
    'Dolomite': {'category': 'money market'},
    'Contango': {'category': 'yield strategy'},
    'DeFi Saver': {'category': 'yield strategy'},
    'FiRM': {'category': 'money market'},
}


def infer_market_integrations(market: dict, partners: list, morpho_by_pt: dict, euler_by_pt: dict, contango_by_pt: dict):
    underlying = (market.get('underlyingSymbol') or '').lower()
    market_address = (market.get('marketAddress') or '').lower()
    chain = (market.get('chain') or '').lower()
    pt_address = (market.get('ptAddress') or '').lower()
    out = []

    partner_names = {p['name']: p for p in partners}

    def maybe_add(name, borrow_assets=None, confidence='ecosystem-live+heuristic', notes='', data_status='partner-live / market-mapping-heuristic', extra=None):
        if name not in partner_names:
            return
        p = partner_names[name]
        row = {
            'venue': name,
            'category': p.get('category'),
            'partnerUrl': p.get('url'),
            'borrowAssets': borrow_assets or ['USDC'],
            'venueConfidence': confidence,
            'notes': notes or p.get('description'),
            'dataStatus': data_status,
        }
        if extra:
            row.update(extra)
        out.append(row)

    # Protocol-verified Morpho matches win over heuristics.
    if pt_address in morpho_by_pt:
        for mm in morpho_by_pt[pt_address]:
            maybe_add(
                'Morpho',
                [mm.get('loanAssetSymbol') or 'unknown'],
                confidence='verified-live',
                notes=f"Verified via Morpho GraphQL: PT collateral supported against {mm.get('loanAssetSymbol')}.",
                data_status='protocol-live',
                extra={
                    'marketId': mm.get('marketId'),
                    'loanAssetSymbol': mm.get('loanAssetSymbol'),
                    'lltv': mm.get('lltv'),
                    'borrowApy': mm.get('borrowApy'),
                    'supplyAssetsUsd': mm.get('supplyAssetsUsd'),
                    'borrowAssetsUsd': mm.get('borrowAssetsUsd'),
                    'utilization': mm.get('utilization'),
                },
            )
        if 'Contango' in partner_names:
            maybe_add('Contango', ['USDC'], confidence='ecosystem-live', notes='Contango listed in Pendle ecosystem; verify this exact PT route in Contango app.', data_status='ecosystem-live')
        return out

    if pt_address in euler_by_pt:
        for ev in euler_by_pt[pt_address]:
            maybe_add(
                'Euler',
                [ev.get('unitOfAccountSymbol') or 'unknown'],
                confidence='verified-live',
                notes=f"Verified via Euler indexer: PT asset matched in Euler token/vault data ({ev.get('vaultSymbol')}).",
                data_status='protocol-live',
                extra={
                    'vault': ev.get('vault'),
                    'loanAssetSymbol': ev.get('unitOfAccountSymbol'),
                    'borrowCap': ev.get('borrowCap'),
                    'supplyCap': ev.get('supplyCap'),
                    'cash': ev.get('cash'),
                    'interestRate': ev.get('interestRate'),
                },
            )

    if pt_address in contango_by_pt:
        for cm in contango_by_pt[pt_address]:
            maybe_add(
                'Contango',
                ['unknown'],
                confidence='verified-live',
                notes='Verified via Contango public Pendle integration config.',
                data_status='protocol-live',
                extra={
                    'integrationUrl': cm.get('integrationUrl'),
                    'description': cm.get('description'),
                },
            )

    # Concrete confirmed example from user + known Pendle docs flow
    if market_address == '0xf5929a1c332ceab7918a4593a43db2b9ac20095f':
        maybe_add('Morpho', ['USDC'], confidence='confirmed-by-user', notes='User-confirmed PT reUSD -> Morpho -> borrow USDC path from Pendle Pencosystem tab.')
        maybe_add('Contango', ['USDC'], confidence='ecosystem-live', notes='Contango listed in Pendle Pencosystem; verify exact market support in app before execution.')
        return out

    if chain == 'ethereum':
        if any(k in underlying for k in ['apxusd', 'apyusd', 'reusd', 'reusde', 'nusd', 'msusd', 'msy', 'superusdc', 'avusd']):
            if not any(i.get('venue') == 'Morpho' for i in out):
                maybe_add('Morpho', ['USDC'])
            if not any(i.get('venue') == 'Euler' for i in out):
                maybe_add('Euler', ['USDC'])
            maybe_add('Contango', ['USDC'], notes='Contango is a Pendle ecosystem leverage route; confirm the exact PT market in-app.')
        elif any(k in underlying for k in ['usde', 'susde', 'srusde', 'jrusde']):
            if not any(i.get('venue') == 'Euler' for i in out):
                maybe_add('Euler', ['USDC'])
            if not any(i.get('venue') == 'Morpho' for i in out):
                maybe_add('Morpho', ['USDC'])
            maybe_add('Contango', ['USDC'])

    return out


def practical_leverage_band(implied_apy: float, days: float, integrations: list):
    if not integrations:
        return 'none'
    if implied_apy >= 0.14 and days >= 21:
        return 'moderate'
    if implied_apy >= 0.10:
        return 'light'
    return 'light'


def loopability_verdict(integrations: list, implied_apy: float, liquidity_usd: float, days: float):
    if not integrations:
        return 'unverified'
    if implied_apy >= 0.10 and liquidity_usd >= 3_000_000 and days >= 14:
        return 'high-priority'
    if implied_apy >= 0.08 and liquidity_usd >= 1_000_000:
        return 'candidate'
    return 'watchlist'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--markets', default=str(DEFAULT_MARKETS))
    ap.add_argument('--pencosystem', default=str(DEFAULT_PENCOSYSTEM))
    ap.add_argument('--morpho', default=str(DATA / 'morpho-pt-markets.latest.json'))
    ap.add_argument('--euler', default=str(DATA / 'euler-pt-markets.latest.json'))
    ap.add_argument('--contango', default=str(DATA / 'contango-pt-markets.latest.json'))
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    ap.add_argument('--stable-only', action='store_true')
    ap.add_argument('--min-apy', type=float, default=0.08)
    args = ap.parse_args()

    market_payload = json.loads(Path(args.markets).read_text())
    partner_payload = json.loads(Path(args.pencosystem).read_text()) if Path(args.pencosystem).exists() else {'partners': []}
    morpho_payload = json.loads(Path(args.morpho).read_text()) if Path(args.morpho).exists() else {'markets': []}
    euler_payload = json.loads(Path(args.euler).read_text()) if Path(args.euler).exists() else {'markets': [], 'matchedTokens': []}
    contango_payload = json.loads(Path(args.contango).read_text()) if Path(args.contango).exists() else {'markets': []}
    partners = partner_payload.get('partners', [])
    morpho_by_pt = {}
    for mm in morpho_payload.get('markets', []):
        morpho_by_pt.setdefault((mm.get('ptAddress') or '').lower(), []).append(mm)
    euler_by_pt = {}
    for tok in euler_payload.get('matchedTokens', []):
        addr = (tok.get('address') or '').lower()
        euler_by_pt.setdefault(addr, [])
    for em in euler_payload.get('markets', []):
        for addr in [*(em.get('collaterals') or []), em.get('asset')]:
            if addr:
                euler_by_pt.setdefault((addr or '').lower(), []).append(em)
    contango_by_pt = {}
    for cm in contango_payload.get('markets', []):
        contango_by_pt.setdefault((cm.get('ptAddress') or '').lower(), []).append(cm)

    rows = []
    for m in market_payload['markets']:
        if args.stable_only and m.get('assetFamily') != 'stable':
            continue
        implied_apy = m.get('impliedApy') or 0.0
        if implied_apy < args.min_apy:
            continue
        integrations = infer_market_integrations(m, partners, morpho_by_pt, euler_by_pt, contango_by_pt)
        rows.append({
            'marketAddress': m.get('marketAddress'),
            'ptAddress': m.get('ptAddress'),
            'ptName': m.get('ptName'),
            'chain': m.get('chain'),
            'underlyingSymbol': m.get('underlyingSymbol'),
            'impliedApy': implied_apy,
            'daysToExpiry': m.get('daysToExpiry'),
            'liquidityUsd': m.get('liquidityUsd'),
            'bestFit': m.get('bestFit'),
            'integrations': integrations,
            'practicalLeverageBand': practical_leverage_band(implied_apy, m.get('daysToExpiry') or 0, integrations),
            'loopabilityVerdict': loopability_verdict(integrations, implied_apy, m.get('liquidityUsd') or 0, m.get('daysToExpiry') or 0),
            'manualRoute': 'Pendle PT -> money market collateral -> borrow USDC -> buy more PT -> redeposit' if integrations else None,
            'automationRoute': 'Contango / other yield-strategy route if supported for this exact PT' if any(i.get('venue') == 'Contango' for i in integrations) else None,
            'dataStatus': 'mixed-live',
            'sources': {
                'pendleMarketData': 'live-api',
                'pencosystemDirectory': 'live-html',
                'marketIntegrationMapping': 'heuristic unless confirmed-by-user',
            },
        })

    result = {
        'generatedAt': market_payload.get('generatedAt'),
        'sourceMarketCount': market_payload.get('rankedCount'),
        'partnerCount': len(partners),
        'loopCandidateCount': len(rows),
        'markets': rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(str(out))
    print(f'Merged {len(rows)} loop candidates using {len(partners)} live Pencosystem partners')


if __name__ == '__main__':
    main()
