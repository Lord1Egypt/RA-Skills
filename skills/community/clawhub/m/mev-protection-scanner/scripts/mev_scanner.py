#!/usr/bin/env python3
"""Base L2 MEV Protection Scanner - Detect sandwich attacks and frontrunning.

Read-only analysis: this script only queries a public Base JSON-RPC endpoint
(eth_getTransactionByHash / eth_getBlockByNumber) and never signs, sends, or
simulates a transaction on-chain, and never touches a private key.

RPC endpoint configuration (no credentials are hardcoded, defaulted, or
read from the environment as a key):
  - Default: https://mainnet.base.org (public, no key required)
  - Override with the BASE_RPC_URL environment variable or --rpc-url.
    The endpoint must be https:// and must not embed credentials. A
    keyed provider URL may be supplied whole via BASE_RPC_URL / --rpc-url
    if the operator chooses, but the script never assembles a URL from a
    key and never prints the endpoint or any request error text, so a key
    in the URL cannot leak into logs (v1.0.2: the ALCHEMY_API_KEY /
    --alchemy-key path was removed for exactly that reason).
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests

DEFAULT_RPC_URL = "https://mainnet.base.org"

# A transaction hash is exactly 0x followed by 64 hex characters. Anything
# else is rejected before it reaches the RPC endpoint.
TX_HASH_RE = re.compile(r"^0x[0-9a-fA-F]{64}$")

# Known DEX router addresses on Base (public, well-known contract addresses)
UNISWAP_V3_ROUTER = "0x2626664c2603336E57B271c5C0b26F421741e481"
AERODROME_ROUTER = "0xcF77a3Ba9A5CA399B7b97C77D8A436091617385B"

# Common MEV bot indicators
MEV_BOT_PATTERNS = [
    "0x0000000000000000000000000000000000000000",  # Placeholder
]


def _validate_rpc_url(url: str) -> str:
    """Accept only https:// endpoints with no embedded credentials.

    A key embedded in the URL would be visible in request-error text and
    logs (see _rpc_call); the endpoint is operator-supplied and treated
    as opaque, so it is never printed anywhere either."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("Invalid RPC URL (must be https://...)")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("Invalid RPC URL (must not embed credentials)")
    return url


def parse_hex_int(value, default: Optional[int] = None) -> Optional[int]:
    """Parse a hex quantity from an RPC response without raising.

    A malicious or malfunctioning RPC endpoint can return malformed values;
    treat those as missing data instead of crashing the scanner.
    """
    if value is None:
        return default
    try:
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.startswith(("0x", "0X")):
            return int(value, 16)
        return default
    except (ValueError, TypeError):
        return default


class MEVScanner:
    def __init__(self, rpc_url: str):
        # The endpoint is resolved by the caller (see main(): --rpc-url
        # defaults to $BASE_RPC_URL, else the public endpoint). This
        # constructor only validates it. The value is an endpoint URL,
        # not a credential: no key is read, assembled, or defaulted
        # anywhere in this skill.
        self.rpc_url = _validate_rpc_url(rpc_url)

    def _rpc_call(self, method: str, params: list) -> dict:
        """Make JSON-RPC call. Returns the result object, or {} on any failure."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        try:
            resp = requests.post(self.rpc_url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            # Fixed message only: requests exceptions can include the
            # request URL, so the exception text is never printed.
            print("RPC error: request failed", file=sys.stderr)
            return {}
        if not isinstance(data, dict):
            print("RPC error: unexpected non-object response", file=sys.stderr)
            return {}
        result = data.get("result", {})
        if not isinstance(result, dict):
            print("RPC error: unexpected non-object result", file=sys.stderr)
            return {}
        return result

    def get_transaction(self, tx_hash: str) -> Dict:
        """Get transaction details. tx_hash must already be validated."""
        result = self._rpc_call("eth_getTransactionByHash", [tx_hash])
        if not result:
            return {}
        value = parse_hex_int(result.get("value"), 0)
        gas_price = parse_hex_int(result.get("gasPrice"), 0)
        max_fee = parse_hex_int(result.get("maxFeePerGas"))
        max_priority = parse_hex_int(result.get("maxPriorityFeePerGas"))
        nonce = parse_hex_int(result.get("nonce"), 0)
        block_number = parse_hex_int(result.get("blockNumber"))
        return {
            "hash": tx_hash,
            "from": result.get("from", "") if isinstance(result.get("from"), str) else "",
            "to": result.get("to", "") if isinstance(result.get("to"), str) else "",
            "value": (value or 0) / 1e18,
            "gas_price": (gas_price or 0) / 1e9,
            "max_fee": max_fee / 1e9 if max_fee is not None else None,
            "max_priority": max_priority / 1e9 if max_priority is not None else None,
            "nonce": nonce or 0,
            "input": result.get("input", "") if isinstance(result.get("input"), str) else "",
            "block_number": block_number,
        }

    def get_block_transactions(self, block_num: int) -> List[Dict]:
        """Get all transactions in a block."""
        hex_num = hex(block_num)
        result = self._rpc_call("eth_getBlockByNumber", [hex_num, True])
        if not result:
            return []

        txs = []
        transactions = result.get("transactions", [])
        if not isinstance(transactions, list):
            return []
        for tx in transactions:
            if not isinstance(tx, dict):
                continue
            value = parse_hex_int(tx.get("value"), 0)
            gas_price = parse_hex_int(tx.get("gasPrice"), 0)
            tx_input = tx.get("input", "") if isinstance(tx.get("input"), str) else ""
            txs.append({
                "hash": tx.get("hash", "") if isinstance(tx.get("hash"), str) else "",
                "from": tx.get("from", "") if isinstance(tx.get("from"), str) else "",
                "to": tx.get("to", "") if isinstance(tx.get("to"), str) else "",
                "value": (value or 0) / 1e18,
                "gas_price": (gas_price or 0) / 1e9,
                "input": tx_input[:10],  # Method signature
            })
        return txs

    def analyze_sandwich_risk(self, tx_hash: str) -> Dict:
        """Analyze if a transaction was potentially sandwiched."""
        if not TX_HASH_RE.match(tx_hash):
            return {"error": "Invalid transaction hash: expected 0x followed by 64 hex characters"}
        tx = self.get_transaction(tx_hash)
        if not tx:
            return {"error": "Transaction not found"}

        if not tx["block_number"]:
            return {"error": "Transaction still pending"}

        block_num = tx["block_number"]

        # Get surrounding blocks
        prev_block = self.get_block_transactions(block_num - 1)
        current_block = self.get_block_transactions(block_num)
        next_block = self.get_block_transactions(block_num + 1)

        # Look for patterns:
        # 1. Similar large swap in block before (attacker positioning)
        # 2. Our tx in current block
        # 3. Reverse swap in block after (attacker closing)

        risk_score = 0
        indicators = []

        # Check if interacting with known DEX
        if tx.get("to", "").lower() in [UNISWAP_V3_ROUTER.lower(), AERODROME_ROUTER.lower()]:
            risk_score += 10
            indicators.append("DEX interaction")

        # Check gas price - unusually high might indicate gas auction
        if tx.get("gas_price", 0) > 0.5:  # > 0.5 gwei is high for Base
            risk_score += 15
            indicators.append("High gas price (possible gas auction)")

        # Check for similar transactions in surrounding blocks
        similar_prev = [t for t in prev_block if t["input"] == tx["input"][:10] and t["to"] == tx.get("to")]
        similar_next = [t for t in next_block if t["input"] == tx["input"][:10] and t["to"] == tx.get("to")]

        if similar_prev and similar_next:
            risk_score += 50
            indicators.append("Sandwich pattern detected (similar txs before/after)")
        elif similar_prev:
            risk_score += 20
            indicators.append("Possible frontrunning setup")

        # Large calldata is only a rough proxy for slippage exposure,
        # not a measurement of it — it cannot establish a slippage limit.
        if len(tx.get("input", "")) > 200:
            risk_score += 10
            indicators.append("Large input data - check slippage settings")

        # Clamp score
        risk_score = min(100, max(0, risk_score))

        return {
            "tx_hash": tx_hash,
            "risk_score": risk_score,
            "risk_level": "CRITICAL" if risk_score > 80 else "HIGH" if risk_score > 60 else "MEDIUM" if risk_score > 40 else "LOW",
            "indicators": indicators,
            "block_number": block_num,
            "gas_price_gwei": round(tx.get("gas_price", 0), 4),
            "to_address": tx.get("to", ""),
            "recommendations": self._get_recommendations(risk_score),
        }

    def _get_recommendations(self, risk_score: int) -> List[str]:
        """Get protection recommendations based on risk."""
        recs = []

        if risk_score > 80:
            recs.append("🚨 CRITICAL: Use Flashbots Protect or MEV Blocker RPC")
            recs.append("🚨 Split this trade into smaller chunks")
            recs.append("🚨 Consider waiting for lower congestion")

        if risk_score > 60:
            recs.append("⚠️ Set max slippage to 0.3% or lower")
            recs.append("⚠️ Use tight deadline (next 3 blocks)")
            recs.append("⚠️ Consider private mempool submission")

        if risk_score > 40:
            recs.append("💡 Enable slippage protection")
            recs.append("💡 Monitor mempool before executing")

        recs.append("✅ Always verify recipient contract address")
        recs.append("✅ Use gas-price-predictor for optimal timing")

        return recs

    def simulate_sandwich(self, victim_amount: float, slippage: float = 0.5) -> Dict:
        """Simulate sandwich attack profitability."""
        # Simplified model: attacker extracts ~slippage % of victim's trade
        extraction = victim_amount * (slippage / 100)
        attacker_cost = 0.001  # Gas cost estimate
        profit = extraction - attacker_cost

        return {
            "victim_trade_size": victim_amount,
            "slippage_tolerance": slippage,
            "extracted_value": round(extraction, 4),
            "attacker_gas_cost": attacker_cost,
            "attacker_profit": round(profit, 4),
            "profitable": profit > 0,
            "risk_to_user": "HIGH" if profit > 1 else "MEDIUM" if profit > 0.1 else "LOW",
        }

def main():
    parser = argparse.ArgumentParser(description="Base L2 MEV Protection Scanner")
    parser.add_argument("--rpc-url", default=os.environ.get("BASE_RPC_URL", DEFAULT_RPC_URL),
                        help="Base JSON-RPC endpoint (default: $BASE_RPC_URL or https://mainnet.base.org). Must be https://.")
    parser.add_argument("--check", metavar="TX_HASH", help="Check specific transaction hash (0x + 64 hex chars)")
    parser.add_argument("--simulate", type=float, help="Simulate sandwich for trade size (ETH, must be > 0)")
    parser.add_argument("--slippage", type=float, default=0.5, help="Slippage tolerance %% (0-100)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if args.simulate is not None and args.simulate <= 0:
        parser.error("--simulate amount must be greater than 0")
    if not 0 <= args.slippage <= 100:
        parser.error("--slippage must be between 0 and 100")

    try:
        scanner = MEVScanner(args.rpc_url)
    except ValueError as e:
        parser.error(str(e))

    if args.check:
        if not TX_HASH_RE.match(args.check):
            print("error: --check requires a transaction hash: 0x followed by 64 hex characters",
                  file=sys.stderr)
            sys.exit(2)
        result = scanner.analyze_sandwich_risk(args.check)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n🔍 MEV Risk Analysis")
            print(f"Transaction: {args.check}")
            print(f"Risk Score: {result.get('risk_score', 'N/A')}/100")
            print(f"Risk Level: {result.get('risk_level', 'N/A')}")
            print(f"\nIndicators:")
            for ind in result.get("indicators", []):
                print(f"  • {ind}")
            print(f"\nRecommendations:")
            for rec in result.get("recommendations", []):
                print(f"  {rec}")

    elif args.simulate:
        sim = scanner.simulate_sandwich(args.simulate, args.slippage)

        if args.json:
            print(json.dumps(sim, indent=2))
        else:
            print(f"\n🥪 Sandwich Attack Simulation")
            print(f"Victim trade: {args.simulate} ETH")
            print(f"Slippage tolerance: {args.slippage}%")
            print(f"\nAttacker extraction: ${sim['extracted_value']} ETH")
            print(f"Attacker profit: ${sim['attacker_profit']} ETH")
            print(f"Profitable for attacker: {sim['profitable']}")
            print(f"Risk to user: {sim['risk_to_user']}")

            if sim['profitable'] and sim['attacker_profit'] > 1:
                print("\n⚠️ This trade size is HIGHLY attractive to MEV bots!")
                print("⚠️ Use protection: Flashbots Protect, split order, or lower slippage")
    else:
        print("Use --check <tx_hash> to analyze a transaction, or --simulate <amount> to model risk")

if __name__ == "__main__":
    main()
