#!/usr/bin/env python3
"""
transfer_security_check.py — AML security check for transfer recipient addresses (MistTrack integration)

Integrates MistTrack risk scoring into the transfer flow for the following skills:
  - bitget-wallet-skill        (check recipient address before transfer / swap)
  - Trust Wallet wallet-core  (check before building signed tx with toAddress)
  - Trust Wallet trust-web3-provider (check before handling eth_sendTransaction / ton_sendTransaction)
  - Binance spot              (check recipient address before withdrawal)
  - Binance margin-trading    (check recipient address before withdrawal)
  - Binance derivatives-trading-usds-futures (check recipient address before withdrawal)
  - OKX Agent Skills          (OnchainOS: check recipient address before withdrawal)

Usage:
  python3 scripts/transfer_security_check.py --address <address> --chain <chain_code>
  python3 scripts/transfer_security_check.py --address <address> --chain eth --json

Supported chain codes (case-insensitive):
  # bitget-wallet-skill format:
  eth, sol, bnb, trx, base, arbitrum, optimism, matic, ton, suinet, avax, zksync, ltc, doge, bch
  # Trust Wallet wallet-core CoinType format (aliases):
  bitcoin, btc, solana, tron, polygon, smartchain, bsc, tonchain
  # Binance Skills network format (uppercase also accepted):
  BSC, ARBI, OPT, POLYGON, AVAX, BASE, ZKSYNC, ETH, BTC, SOL, TRX, BNB, LTC, DOGE, BCH, TON
  # OKX API v5 chain format (coin prefix stripped automatically, e.g. USDT-ERC20, BTC-Bitcoin):
  erc20, trc20, bitcoin, solana, arbitrum one, optimism, avalanche c-chain, zksync era, bep20

Unsupported chains (not in MistTrack, returns exit 3):
  aptos, cosmos, atom

Exit codes:
  0  ALLOW  — low risk, transfer may proceed
  1  WARN   — moderate/high risk, requires explicit user confirmation
  2  BLOCK  — severe risk, transfer should be rejected
  3  ERROR  — API unavailable, invalid parameters, or unsupported chain

Environment variables:
  MISTTRACK_API_KEY  — MistTrack API key (takes priority over --api-key)

Examples:
  export MISTTRACK_API_KEY=your_key
  # Bitget Wallet flow
  python3 scripts/transfer_security_check.py --address 0x... --chain eth
  # Trust Wallet wallet-core flow
  python3 scripts/transfer_security_check.py --address 1A... --chain bitcoin
  python3 scripts/transfer_security_check.py --address 0x... --chain polygon --json
  # Binance Skills flow (network parameter, case-insensitive)
  python3 scripts/transfer_security_check.py --address 0x... --chain BSC
  python3 scripts/transfer_security_check.py --address 0x... --chain ARBI
  python3 scripts/transfer_security_check.py --address 0x... --chain OPT --json
  # OKX Agent Skills flow (full USDT-ERC20 format supported)
  python3 scripts/transfer_security_check.py --address 0x... --chain USDT-ERC20 --json
"""

import argparse
import json
import os
import sys
from typing import Optional

import requests

# ─── Constants ───────────────────────────────────────────────────────────────

BASE_URL = "https://openapi.misttrack.io"
REQUEST_TIMEOUT = 30  # seconds

# Map chain identifiers → MistTrack coin parameter
# Covers bitget-wallet-skill, Trust Wallet wallet-core, and Binance Skills network names.
# All keys are lowercase; --chain input is lowercased automatically in parse_args.
CHAIN_TO_COIN: dict[str, str] = {
    # ── bitget-wallet-skill chain codes ─────────────────────────────────────
    "eth": "ETH",
    "sol": "SOL",
    "bnb": "BNB",
    "trx": "TRX",
    "base": "ETH-Base",
    "arbitrum": "ETH-Arbitrum",
    "optimism": "ETH-Optimism",
    "matic": "POL-Polygon",
    "ton": "TON",
    "suinet": "SUI",
    "avax": "AVAX-Avalanche",
    "zksync": "ETH-zkSync",
    "ltc": "LTC",
    "doge": "DOGE",
    "bch": "BCH",
    # ── Trust Wallet wallet-core CoinType aliases ────────────────────────────
    "bitcoin": "BTC",           # CoinType.bitcoin
    "btc": "BTC",               # short alias
    "solana": "SOL",            # CoinType.solana (alias for sol)
    "tron": "TRX",              # CoinType.tron (alias for trx)
    "polygon": "POL-Polygon",   # CoinType.polygon (alias for matic)
    "smartchain": "BNB",        # CoinType.smartChain
    "bsc": "BNB",               # BNB Chain / BEP20 — Binance Skills & common abbreviation
    "tonchain": "TON",          # alias distinguishing from bitget's 'ton'
    # ── Binance Skills network identifiers ───────────────────────────────────
    # (Binance withdrawal API `network` parameter; lowercased by parse_args)
    # Chains already covered above via lowercase aliases (eth, sol, bnb, trx,
    # btc, ltc, doge, bch, ton, avax, base, zksync, polygon/matic, bsc) need
    # no duplicate entry — only Binance-specific shorthand names are added here.
    "arbi": "ETH-Arbitrum",     # Binance network code for Arbitrum One
    "opt": "ETH-Optimism",      # Binance network code for OP Mainnet
    "op": "ETH-Optimism",       # short alias used by some Binance contexts
    "azec": "ETH-zkSync",       # Binance alternate network code for zkSync Era
    # ── OKX API v5 chain identifiers ─────────────────────────────────────────
    # (OKX withdrawal API `chain` parameter; lowercased and stripped of "CCY-" prefix)
    "erc20": "ETH",             # ETH
    "trc20": "TRX",             # TRX
    "bep20": "BNB",             # BSC
    "arbitrum one": "ETH-Arbitrum",
    "avalanche c-chain": "AVAX-Avalanche",
    "zksync era": "ETH-zkSync",
    "bitcoin cash": "BCH",
}

# Chains that are not yet supported by MistTrack — exit cleanly with an explanation
UNSUPPORTED_CHAINS: dict[str, str] = {
    "aptos": "MistTrack does not support Aptos (APT) chain address lookups. Please verify the recipient identity manually.",
    "cosmos": "MistTrack does not support Cosmos Hub (ATOM) native token address lookups. Please verify the recipient identity manually.",
    "atom": "MistTrack does not support Cosmos Hub (ATOM) native token address lookups. Please verify the recipient identity manually.",
}

# Risk level → decision mapping
RISK_DECISION: dict[str, str] = {
    "Low": "ALLOW",
    "Moderate": "WARN",
    "High": "WARN",
    "Severe": "BLOCK",
}

# Exit codes
EXIT_ALLOW = 0
EXIT_WARN = 1
EXIT_BLOCK = 2
EXIT_ERROR = 3

# ANSI colours (disabled when JSON mode is active)
COLOUR = {
    "green": "\033[32m",
    "yellow": "\033[33m",
    "orange": "\033[91m",
    "red": "\033[31m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}

RISK_COLOUR = {
    "Low": COLOUR["green"],
    "Moderate": COLOUR["yellow"],
    "High": COLOUR["orange"],
    "Severe": COLOUR["red"],
}

# ─── API helpers ─────────────────────────────────────────────────────────────


def _get(endpoint: str, params: dict) -> dict:
    """Perform a GET request to MistTrack API, raising on HTTP errors."""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def get_risk_score(coin: str, address: str, api_key: str) -> dict:
    """
    Call v2/risk_score (synchronous) for the given address.
    Returns the full API response dict.
    """
    return _get(
        "v2/risk_score",
        {"coin": coin, "address": address, "api_key": api_key},
    )


def get_address_labels(coin: str, address: str, api_key: str) -> dict:
    """
    Call v1/address_labels for the given address.
    Returns the full API response dict.
    """
    return _get(
        "v1/address_labels",
        {"coin": coin, "address": address, "api_key": api_key},
    )


# ─── Decision logic ──────────────────────────────────────────────────────────


def decide(
    score: int,
    risk_level: str,
    label_type: str,
    label_list: list,
) -> str:
    """
    Determine ALLOW / WARN / BLOCK based on risk score and address labels.

    Special case: known exchange deposit addresses (label_type == "exchange")
    with Low or Moderate risk are treated as ALLOW — users commonly send funds
    to Binance / Coinbase / OKX deposit addresses which may have moderate scores
    due to aggregated exchange activity, not personal risk.
    """
    decision = RISK_DECISION.get(risk_level, "WARN")

    # Whitelist: verified exchange addresses at Low/Moderate score
    if label_type == "exchange" and decision in ("ALLOW", "WARN") and score <= 70:
        decision = "ALLOW"

    return decision


# ─── Output helpers ───────────────────────────────────────────────────────────


def print_result(
    decision: str,
    score: int,
    risk_level: str,
    detail_list: list,
    label_type: str,
    label_list: list,
    risk_report_url: str,
    address: str,
    coin: str,
    chain: str,
    json_output: bool,
) -> None:
    result = {
        "decision": decision,
        "score": score,
        "risk_level": risk_level,
        "detail_list": detail_list,
        "label_type": label_type,
        "label_list": label_list,
        "risk_report_url": risk_report_url,
        "address": address,
        "coin": coin,
        "chain": chain,
    }

    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Human-readable output
    c = COLOUR
    rc = RISK_COLOUR.get(risk_level, "")

    decision_icon = {"ALLOW": "✅", "WARN": "⚠️ ", "BLOCK": "❌"}.get(decision, "❓")

    print(f"\n{c['bold']}Recipient Address Security Check Report{c['reset']}")
    print("─" * 50)
    print(f"Address:       {address}")
    print(f"Chain / Token: {chain} ({coin})")

    labels_str = ", ".join(label_list) if label_list else "—"
    print(f"Labels:        {labels_str} [{label_type or 'unknown'}]")
    print(
        f"Risk score:    {rc}{score} ({risk_level}){c['reset']}"
    )
    if detail_list:
        print(f"Risk details:  {', '.join(detail_list)}")
    if risk_report_url:
        print(f"Full report:   {risk_report_url}")
    print("─" * 50)
    print(f"Decision:      {decision_icon} {decision}")

    if decision == "ALLOW":
        print(f"{c['green']}This address has a low risk level. Transfer may proceed.{c['reset']}")
    elif decision == "WARN":
        print(
            f"{c['yellow']}This address has {risk_level} risk. Please confirm the recipient's identity before continuing.\n"
            f"Explicitly confirm to proceed.{c['reset']}"
        )
    elif decision == "BLOCK":
        print(
            f"{c['red']}This address has Severe risk. It is strongly recommended to cancel this transfer.\n"
            f"Do not send any assets to this address.{c['reset']}"
        )
    print()


def print_error(message: str, json_output: bool) -> None:
    if json_output:
        print(json.dumps({"decision": "ERROR", "error": message}, ensure_ascii=False, indent=2))
    else:
        print(f"\n⚠️  Address security check failed\nReason: {message}", file=sys.stderr)
        print("Unable to verify recipient address risk. Let the user decide whether to proceed.\n", file=sys.stderr)


# ─── Main ────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    all_supported = sorted(set(list(CHAIN_TO_COIN.keys()) + list(UNSUPPORTED_CHAINS.keys())))
    parser = argparse.ArgumentParser(
        description=(
            "Check AML risk for a transfer recipient address\n"
            "Supports Bitget Wallet Skill, Trust Wallet Skills (wallet-core / trust-web3-provider)\n"
            "and Binance and OKX Agent Skills integrations\n"
            "--chain is case-insensitive (BSC == bsc), and handles OKX USDT-ERC20 format automatically"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--address", "-a",
        required=True,
        help="Recipient address (transfer target)",
    )
    parser.add_argument(
        "--chain", "-c",
        required=True,
        # choices validation happens after lowercasing in post-parse step
        help=(
            f"Chain identifier (case-insensitive)\n"
            f"Supported (MistTrack data available): {', '.join(sorted(CHAIN_TO_COIN.keys()))}\n"
            f"Unsupported (exit 3): {', '.join(sorted(UNSUPPORTED_CHAINS.keys()))}\n"
            f"Binance format examples: BSC, ARBI, OPT\n"
            f"OKX format examples: USDT-ERC20, BTC-Bitcoin (coin prefix stripped automatically)"
        ),
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="MistTrack API Key (lower priority than MISTTRACK_API_KEY env var)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output result in JSON format (suitable for machine parsing by agents)",
    )
    args = parser.parse_args()

    # Normalize chain identifier to lowercase
    args.chain = args.chain.strip().lower()

    # OKX specific handling: strip "CCY-" prefix (e.g. "usdt-erc20" -> "erc20", "btc-bitcoin" -> "bitcoin")
    if "-" in args.chain:
        # Check if the right part maps to a valid chain, if so strip the left part
        right_part = args.chain.split("-", 1)[1].strip()
        if right_part in CHAIN_TO_COIN or right_part in UNSUPPORTED_CHAINS:
            args.chain = right_part

    # Validate after normalization (replaces argparse choices= validation)
    if args.chain not in CHAIN_TO_COIN and args.chain not in UNSUPPORTED_CHAINS:
        valid = sorted(set(list(CHAIN_TO_COIN.keys()) + list(UNSUPPORTED_CHAINS.keys())))
        parser.error(
            f"argument --chain/-c: invalid choice: '{args.chain}'\n"
            f"Valid choices (case-insensitive): {', '.join(valid)}"
        )

    return args


def main() -> None:
    args = parse_args()

    # 1. Handle unsupported chains first
    if args.chain in UNSUPPORTED_CHAINS:
        print_error(UNSUPPORTED_CHAINS[args.chain], args.json_output)
        sys.exit(EXIT_ERROR)

    # 2. Resolve API key
    api_key: Optional[str] = os.environ.get("MISTTRACK_API_KEY") or args.api_key
    if not api_key:
        print_error(
            "MISTTRACK_API_KEY env var is not set and --api-key was not provided.\n"
            "Run: export MISTTRACK_API_KEY=your_api_key",
            args.json_output,
        )
        sys.exit(EXIT_ERROR)

    # 2. Map chain → coin
    coin = CHAIN_TO_COIN[args.chain]
    address = args.address.strip()

    # 3. Call MistTrack APIs
    try:
        # 3a. Risk score (primary signal)
        risk_resp = get_risk_score(coin, address, api_key)

        if not risk_resp.get("success"):
            msg = risk_resp.get("msg", "unknown error")
            print_error(f"MistTrack API returned failure: {msg}", args.json_output)
            sys.exit(EXIT_ERROR)

        data = risk_resp.get("data", {})
        score: int = data.get("score", 0)
        risk_level: str = data.get("risk_level", "Low")
        detail_list: list = data.get("detail_list", [])
        risk_report_url: str = data.get("risk_report_url", "")

        # 3b. Address labels (for whitelist logic)
        label_type = ""
        label_list: list = []
        try:
            label_resp = get_address_labels(coin, address, api_key)
            if label_resp.get("success"):
                label_data = label_resp.get("data", {})
                label_type = label_data.get("label_type", "")
                label_list = label_data.get("label_list", [])
        except Exception:
            # Labels are supplementary; don't fail if unavailable
            pass

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        if status == 402:
            print_error("MistTrack subscription has expired. Please renew at https://dashboard.misttrack.io", args.json_output)
        elif status == 429:
            print_error("MistTrack API rate limit exceeded. Please retry later.", args.json_output)
        else:
            print_error(f"HTTP request failed (status {status}): {e}", args.json_output)
        sys.exit(EXIT_ERROR)

    except requests.exceptions.Timeout:
        print_error("MistTrack API request timed out (30s). Please check your network connection and retry.", args.json_output)
        sys.exit(EXIT_ERROR)

    except requests.exceptions.RequestException as e:
        print_error(f"Network request error: {e}", args.json_output)
        sys.exit(EXIT_ERROR)

    # 4. Make decision
    decision = decide(score, risk_level, label_type, label_list)

    # 5. Print result
    print_result(
        decision=decision,
        score=score,
        risk_level=risk_level,
        detail_list=detail_list,
        label_type=label_type,
        label_list=label_list,
        risk_report_url=risk_report_url,
        address=address,
        coin=coin,
        chain=args.chain,
        json_output=args.json_output,
    )

    # 6. Exit with appropriate code
    exit_map = {"ALLOW": EXIT_ALLOW, "WARN": EXIT_WARN, "BLOCK": EXIT_BLOCK}
    sys.exit(exit_map.get(decision, EXIT_ERROR))


if __name__ == "__main__":
    main()
