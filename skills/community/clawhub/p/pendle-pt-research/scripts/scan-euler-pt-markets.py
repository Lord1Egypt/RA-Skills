#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
DEFAULT_PT_INPUT = DATA / 'ranked.latest.json'
DEFAULT_OUT = DATA / 'euler-pt-markets.latest.json'
GRAPHQL_URL = 'https://indexer.euler.finance/graphql'


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
    with urlopen(req, timeout=45) as resp:
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

    target_market_addrs = {(m.get('marketAddress') or '').lower(): m for m in targets}
    target_pt_addrs = {(m.get('ptAddress') or '').lower(): m for m in targets}

    token_query = '''
    query Tokens($chain:Int!, $limit:Int!) {
      tokenlists(where:{chainId:$chain, isPendlePT:true}, limit:$limit) {
        items { address name symbol pendleMarket }
      }
    }
    '''
    token_items = gql(token_query, {'chain': args.chain_id, 'limit': 1000})['data']['tokenlists']['items']

    matched_tokens = []
    for t in token_items:
        addr = (t.get('address') or '').lower()
        pm = (t.get('pendleMarket') or '').lower()
        if addr in target_pt_addrs or pm in target_market_addrs:
            matched_tokens.append(t)

    # Build a vault-side lookup for matched tokens if any are present.
    rows = []
    if matched_tokens:
        token_addrs = [(t.get('address') or '').lower() for t in matched_tokens]
        vault_query = '''
        query Vaults($chain:Int!, $limit:Int!) {
          apiEulerVaults(where:{chainId:$chain}, limit:$limit) {
            items {
              vault vaultName vaultSymbol asset assetName assetSymbol unitOfAccount unitOfAccountSymbol
              borrowCap supplyCap totalAssets totalBorrows cash collaterals interestRate
            }
          }
          vaultStatusLatests(where:{chainId:$chain}, limit:$limit) {
            items { vault totalBorrows totalShares cash interestRate }
          }
        }
        '''
        data = gql(vault_query, {'chain': args.chain_id, 'limit': 1000})['data']
        vaults = data['apiEulerVaults']['items']
        status_by_vault = {v['vault'].lower(): v for v in data['vaultStatusLatests']['items']}
        for v in vaults:
            asset = (v.get('asset') or '').lower()
            cols = [(c or '').lower() for c in (v.get('collaterals') or [])]
            if asset in token_addrs or any(c in token_addrs for c in cols):
                st = status_by_vault.get((v.get('vault') or '').lower(), {})
                rows.append({
                    'protocol': 'Euler',
                    'vault': v.get('vault'),
                    'vaultName': v.get('vaultName'),
                    'vaultSymbol': v.get('vaultSymbol'),
                    'asset': v.get('asset'),
                    'assetSymbol': v.get('assetSymbol'),
                    'unitOfAccountSymbol': v.get('unitOfAccountSymbol'),
                    'borrowCap': v.get('borrowCap'),
                    'supplyCap': v.get('supplyCap'),
                    'totalAssets': v.get('totalAssets'),
                    'totalBorrows': v.get('totalBorrows'),
                    'cash': v.get('cash'),
                    'interestRate': v.get('interestRate') or st.get('interestRate'),
                    'collaterals': v.get('collaterals') or [],
                    'verified': True,
                    'sourceType': 'live-graphql',
                })

    out = {
        'generatedAt': iso_now(),
        'targetCount': len(targets),
        'matchedTokenCount': len(matched_tokens),
        'verifiedMarketCount': len(rows),
        'matchedTokens': matched_tokens,
        'markets': rows,
        'notes': 'Euler verification is considered protocol-live only when target Pendle PTs match Euler tokenlist and vault relationships. Zero matches means no current verification for this target PT set, not that Euler has no Pendle PT support globally.',
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(str(out_path))
    print(f'Matched {len(matched_tokens)} Euler PT tokens and {len(rows)} verified Euler PT markets')


if __name__ == '__main__':
    main()
