#!/bin/bash
# check-wallet.sh — Check native balance on any supported chain
# Usage: bash check-wallet.sh <address> <chain> [--json]
# Compatible with macOS bash 3.2+

set -uo pipefail

ADDRESS="${1:?Usage: check-wallet.sh <address> <chain>}"
CHAIN="${2:?Specify chain: ethereum|base|arbitrum|polygon|optimism|solana}"
JSON_MODE="${3:-}"

python3 << PYEOF
import json, sys, urllib.request

RPC = {
    'ethereum': 'https://eth.llamarpc.com',
    'base': 'https://mainnet.base.org',
    'arbitrum': 'https://arb1.arbitrum.io/rpc',
    'polygon': 'https://polygon-rpc.com',
    'optimism': 'https://mainnet.optimism.io',
}
NATIVE = {
    'ethereum': 'ETH', 'base': 'ETH', 'arbitrum': 'ETH',
    'polygon': 'MATIC', 'optimism': 'ETH', 'solana': 'SOL',
}

chain = "$CHAIN"
address = "$ADDRESS"
json_mode = "$JSON_MODE" == "--json"

if chain not in NATIVE:
    print(f"❌ Unsupported chain: {chain}")
    sys.exit(1)

symbol = NATIVE[chain]

if chain == 'solana':
    payload = json.dumps({"jsonrpc":"2.0","id":1,"method":"getBalance","params":[address]}).encode()
    req = urllib.request.Request("https://api.mainnet-beta.solana.com",
        data=payload, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        balance = data.get('result',{}).get('value',0) / 1e9
    except:
        balance = 0
else:
    rpc = RPC[chain]
    payload = json.dumps({"jsonrpc":"2.0","method":"eth_getBalance","params":[address,"latest"],"id":1}).encode()
    req = urllib.request.Request(rpc, data=payload, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        balance = int(data.get('result','0x0'), 16) / 1e18
    except:
        balance = 0

if json_mode:
    print(json.dumps({"address":address,"chain":chain,"balance":balance,"symbol":symbol}))
else:
    short = f"{address[:6]}...{address[-4:]}"
    print(f"💳 {chain} | {short}")
    print(f"   Balance: {balance:.6f} {symbol}")
PYEOF
