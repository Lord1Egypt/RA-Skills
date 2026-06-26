#!/usr/bin/env python3
"""
multisig_analysis.py — Multisig address identification and permission analysis

Identifies and parses multisig addresses, analyzing signers and permission structures.
Supports BTC, ETH/EVM-compatible chains (Gnosis Safe), and TRX native permission multisig.

Usage:
  python3 scripts/multisig_analysis.py --address <address> --chain <chain>
  python3 scripts/multisig_analysis.py --address <address> --chain eth --json

Supported chain codes:
  btc, bitcoin                             — Bitcoin (P2SH / P2WSH / P2TR format-based)
  eth                                      — Ethereum (Gnosis Safe)
  bnb, bsc, smartchain                     — BNB Smart Chain (Gnosis Safe)
  matic, polygon                           — Polygon (Gnosis Safe)
  base                                     — Base (Gnosis Safe)
  arbitrum, arb                            — Arbitrum One (Gnosis Safe)
  optimism, op                             — OP Mainnet (Gnosis Safe)
  avax, avalanche                          — Avalanche (Gnosis Safe)
  zksync                                   — zkSync Era (Gnosis Safe)
  trx, tron                                — TRON (native permission multisig)

Unsupported chains (returns exit 2):
  sol, ton, ltc, doge, bch, aptos, cosmos

Exit codes:
  0  IS_MULTISIG      — confirmed or likely multisig address
  1  NOT_MULTISIG     — confirmed non-multisig (regular address)
  2  UNSUPPORTED      — unsupported chain
  3  ERROR            — API call failed or query error

Examples:
  # BTC P2SH multisig
  python3 scripts/multisig_analysis.py --address 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy --chain btc

  # ETH Gnosis Safe
  python3 scripts/multisig_analysis.py --address 0x849D52316331967b6fF1198e5E32A0eB168D039d --chain eth

  # TRX native multisig
  python3 scripts/multisig_analysis.py --address TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW --chain trx

  # JSON output (machine-readable)
  python3 scripts/multisig_analysis.py --address 0x... --chain eth --json
"""

import argparse
import json
import re
import sys
from typing import Optional

import requests

# ─── Constants ───────────────────────────────────────────────────────────────

REQUEST_TIMEOUT = 20  # seconds

# Exit codes
EXIT_IS_MULTISIG = 0
EXIT_NOT_MULTISIG = 1
EXIT_UNSUPPORTED = 2
EXIT_ERROR = 3

# ANSI colours (disabled in JSON mode)
COLOUR = {
    "cyan":   "\033[36m",
    "green":  "\033[32m",
    "yellow": "\033[33m",
    "red":    "\033[31m",
    "bold":   "\033[1m",
    "reset":  "\033[0m",
}

# Gnosis Safe Transaction Service base URLs per network
# ref: https://docs.safe.global/core-api/transaction-service-supported-networks
SAFE_API_URLS: dict[str, str] = {
    "eth":       "https://safe-transaction-mainnet.safe.global",
    "bnb":       "https://safe-transaction-bsc.safe.global",
    "bsc":       "https://safe-transaction-bsc.safe.global",
    "smartchain":"https://safe-transaction-bsc.safe.global",
    "matic":     "https://safe-transaction-polygon.safe.global",
    "polygon":   "https://safe-transaction-polygon.safe.global",
    "base":      "https://safe-transaction-base.safe.global",
    "arbitrum":  "https://safe-transaction-arbitrum.safe.global",
    "arb":       "https://safe-transaction-arbitrum.safe.global",
    "optimism":  "https://safe-transaction-optimism.safe.global",
    "op":        "https://safe-transaction-optimism.safe.global",
    "avax":      "https://safe-transaction-avalanche.safe.global",
    "avalanche": "https://safe-transaction-avalanche.safe.global",
    "zksync":    "https://safe-transaction-zksync.safe.global",
}

# Tron API public endpoint
TRON_API_URL = "https://api.trongrid.io"

# BTC chain identifiers
BTC_CHAINS = {"btc", "bitcoin"}

# TRX chain identifiers
TRX_CHAINS = {"trx", "tron"}

# All supported chains
SUPPORTED_CHAINS = set(SAFE_API_URLS.keys()) | BTC_CHAINS | TRX_CHAINS

# Chains we explicitly know are not supported
UNSUPPORTED_CHAINS: dict[str, str] = {
    "sol":     "Solana multisig on-chain query is not supported (no public standard interface).",
    "solana":  "Solana multisig on-chain query is not supported (no public standard interface).",
    "ton":     "TON multisig on-chain query is not supported.",
    "tonchain":"TON multisig on-chain query is not supported.",
    "ltc":     "LTC multisig requires checking the redeem script via a block explorer. Automatic query is not supported.",
    "doge":    "DOGE multisig requires checking the redeem script via a block explorer. Automatic query is not supported.",
    "bch":     "BCH multisig requires checking the redeem script via a block explorer. Automatic query is not supported.",
    "aptos":   "Aptos multisig on-chain query is not supported.",
    "cosmos":  "Cosmos multisig on-chain query is not supported.",
    "atom":    "Cosmos multisig on-chain query is not supported.",
    "sui":     "Sui multisig on-chain query is not supported.",
    "suinet":  "Sui multisig on-chain query is not supported.",
}


# ─── BTC Analysis ────────────────────────────────────────────────────────────

def analyze_btc(address: str) -> dict:
    """
    Analyze a Bitcoin address for potential multisig based on address format.

    - P2SH  (starts with '3')       : May be multisig (also used for single-sig P2SH-P2WPKH)
    - P2WSH (bc1q, 62 chars)        : Likely multisig (Pay-to-Witness-Script-Hash)
    - P2TR  (bc1p)                  : Taproot, may use MuSig2/Tapscript multisig
    - P2PKH (starts with '1')       : Single-sig, not multisig
    - P2WPKH (bc1q, ~42 chars)      : Single-sig SegWit
    """
    address = address.strip()

    # P2PKH — definitely single sig
    if re.match(r"^1[1-9A-HJ-NP-Za-km-z]{25,34}$", address):
        return {
            "is_multisig":   False,
            "confidence":    "high",
            "multisig_type": None,
            "address_type":  "P2PKH",
            "threshold":     None,
            "total_signers": None,
            "owners":        [],
            "note": "P2PKH address (starts with '1') is a single-sig format, not multisig.",
        }

    # P2SH — may be multisig
    if re.match(r"^3[1-9A-HJ-NP-Za-km-z]{25,34}$", address):
        return {
            "is_multisig":   True,
            "confidence":    "medium",
            "multisig_type": "P2SH",
            "address_type":  "P2SH",
            "threshold":     None,
            "total_signers": None,
            "owners":        [],
            "note": (
                "P2SH address (starts with '3') may be multisig or a single-sig P2SH-P2WPKH address. "
                "To confirm signers and threshold, check the Redeem Script on a block explorer (e.g. mempool.space)."
            ),
        }

    # Bech32/Bech32m addresses
    addr_lower = address.lower()

    # P2WSH — mainnet bc1q with 62 chars (SHA-256 witness program = 32 bytes → 62 bech32 chars)
    if addr_lower.startswith("bc1q") and len(address) == 62:
        return {
            "is_multisig":   True,
            "confidence":    "high",
            "multisig_type": "P2WSH",
            "address_type":  "P2WSH",
            "threshold":     None,
            "total_signers": None,
            "owners":        [],
            "note": (
                "P2WSH address (bc1q, 62 chars) is a SegWit multisig format. "
                "To get the signer list and threshold (m-of-n), check the Witness Script "
                "on a block explorer (e.g. mempool.space)."
            ),
        }

    # P2WPKH — bc1q with ~42 chars — single sig
    if addr_lower.startswith("bc1q") and len(address) <= 45:
        return {
            "is_multisig":   False,
            "confidence":    "high",
            "multisig_type": None,
            "address_type":  "P2WPKH",
            "threshold":     None,
            "total_signers": None,
            "owners":        [],
            "note": "P2WPKH address (bc1q, ~42 chars) is a single-sig SegWit format, not multisig.",
        }

    # P2TR — Taproot (bc1p) — may use MuSig2 or Tapscript multisig
    if addr_lower.startswith("bc1p"):
        return {
            "is_multisig":   True,
            "confidence":    "low",
            "multisig_type": "P2TR",
            "address_type":  "P2TR",
            "threshold":     None,
            "total_signers": None,
            "owners":        [],
            "note": (
                "P2TR address (bc1p, Taproot) may use MuSig2 aggregated signing or Tapscript multisig. "
                "Because MuSig2 signatures look identical to single-sig on-chain, "
                "multisig cannot be confirmed from the address format alone. "
                "Check the witness data of spending transactions via a block explorer (e.g. mempool.space)."
            ),
        }

    # Testnet / unknown format
    return {
        "is_multisig":   None,
        "confidence":    "unknown",
        "multisig_type": None,
        "address_type":  "unknown",
        "threshold":     None,
        "total_signers": None,
        "owners":        [],
        "note": f"Unrecognized BTC address format: {address}",
    }


# ─── ETH/EVM Analysis (Gnosis Safe) ─────────────────────────────────────────

def analyze_evm(address: str, chain: str) -> dict:
    """
    Query the Safe Transaction Service API to determine if the address is a
    Gnosis Safe multisig wallet and retrieve its owners/threshold.
    """
    base_url = SAFE_API_URLS[chain]
    url = f"{base_url}/api/v1/safes/{address}/"

    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise RuntimeError("Safe API request timed out (20s). Please check your network connection and retry.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network request error: {e}")

    if resp.status_code == 404:
        # Address is not a Gnosis Safe
        return {
            "is_multisig":   False,
            "confidence":    "high",
            "multisig_type": None,
            "address_type":  "EOA_or_other_contract",
            "threshold":     None,
            "total_signers": None,
            "owners":        [],
            "note": "This address is not a Gnosis Safe contract (Safe API returned 404).",
        }

    if resp.status_code != 200:
        raise RuntimeError(
            f"Safe API returned unexpected status {resp.status_code}: {resp.text[:200]}"
        )

    data = resp.json()
    owners: list[str] = data.get("owners", [])
    threshold: int = data.get("threshold", 0)
    nonce: int = data.get("nonce", 0)
    version: str = data.get("version", "")
    master_copy: str = data.get("masterCopy", "") or data.get("singleton", "")

    is_multisig = threshold > 1 or len(owners) > 1

    return {
        "is_multisig":   is_multisig,
        "confidence":    "high",
        "multisig_type": "gnosis_safe",
        "address_type":  "gnosis_safe",
        "threshold":     threshold,
        "total_signers": len(owners),
        "owners":        owners,
        "safe_version":  version,
        "master_copy":   master_copy,
        "nonce":         nonce,
        "note": (
            f"Gnosis Safe {version} contract. "
            f"Requires {threshold}/{len(owners)} signatures to execute transactions. "
            f"{nonce} transaction(s) executed so far."
        ) if is_multisig else (
            f"This address is a Gnosis Safe {version} contract, "
            f"but threshold is {threshold} with {len(owners)} signer(s) (single-sig or 1-of-1)."
        ),
    }


# ─── TRX Analysis ────────────────────────────────────────────────────────────

def _parse_permission(perm: dict) -> dict:
    """Parse a single Tron permission object into a structured dict."""
    keys = perm.get("keys", [])
    return {
        "permission_name": perm.get("permission_name", ""),
        "threshold":       perm.get("threshold", 1),
        "keys": [
            {
                "address": k.get("address", ""),
                "weight":  k.get("weight", 1),
            }
            for k in keys
        ],
    }


def analyze_trx(address: str) -> dict:
    """
    Call Tron's public API to get account details and parse multisig permission structure.
    A TRX account is considered multisig if:
      - owner_permission.threshold > 1, OR
      - owner_permission has more than one key, OR
      - any active_permission has threshold > 1 or multiple keys
    """
    url = f"{TRON_API_URL}/v1/accounts/{address}"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise RuntimeError("Tron API request timed out (20s). Please check your network connection and retry.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network request error: {e}")

    if resp.status_code != 200:
        raise RuntimeError(
            f"Tron API returned unexpected status {resp.status_code}: {resp.text[:200]}"
        )

    body = resp.json()
    accounts = body.get("data", [])
    if not accounts:
        raise RuntimeError(
            f"TRX address {address} not found (account does not exist or has not been activated)."
        )

    account = accounts[0]

    # Parse owner permission
    owner_perm_raw = account.get("owner_permission", {})
    owner_perm = _parse_permission(owner_perm_raw) if owner_perm_raw else None

    # Parse active permissions (list)
    active_perms_raw = account.get("active_permission", [])
    active_perms = [_parse_permission(p) for p in active_perms_raw]

    # Determine if multisig
    owner_is_multisig = False
    if owner_perm:
        owner_is_multisig = (
            owner_perm["threshold"] > 1 or len(owner_perm["keys"]) > 1
        )

    active_is_multisig = any(
        p["threshold"] > 1 or len(p["keys"]) > 1
        for p in active_perms
    )

    is_multisig = owner_is_multisig or active_is_multisig

    # Collect all unique signer addresses across all permissions
    all_signers: set[str] = set()
    if owner_perm:
        for k in owner_perm["keys"]:
            if k["address"]:
                all_signers.add(k["address"])
    for p in active_perms:
        for k in p["keys"]:
            if k["address"]:
                all_signers.add(k["address"])

    # Build summary note
    if is_multisig:
        details = []
        if owner_perm and owner_is_multisig:
            details.append(
                f"owner_permission: threshold {owner_perm['threshold']}, "
                f"{len(owner_perm['keys'])} authorized key(s)"
            )
        for p in active_perms:
            if p["threshold"] > 1 or len(p["keys"]) > 1:
                details.append(
                    f"active_permission '{p['permission_name']}': "
                    f"threshold {p['threshold']}, {len(p['keys'])} authorized key(s)"
                )
        note = "TRX native multisig account. Permission structure: " + "; ".join(details) + "."
    else:
        note = "This TRX address has a threshold of 1 with a single key — it is a regular single-sig account."

    return {
        "is_multisig":        is_multisig,
        "confidence":         "high",
        "multisig_type":      "tron_native" if is_multisig else None,
        "address_type":       "tron_account",
        "threshold":          owner_perm["threshold"] if owner_perm else None,
        "total_signers":      len(all_signers),
        "owners":             sorted(all_signers),
        "owner_permission":   owner_perm,
        "active_permissions": active_perms,
        "note":               note,
    }


# ─── Output helpers ───────────────────────────────────────────────────────────

def print_result(result: dict, address: str, chain: str, json_output: bool) -> None:
    output = {
        "address": address,
        "chain":   chain,
        **result,
    }

    if json_output:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    c = COLOUR
    is_multisig = result.get("is_multisig")
    confidence  = result.get("confidence", "unknown")
    multisig_type = result.get("multisig_type") or "—"
    address_type  = result.get("address_type") or "—"
    threshold     = result.get("threshold")
    total_signers = result.get("total_signers")
    owners        = result.get("owners", [])

    # Confidence badge
    conf_badge = {
        "high":    f"{c['green']}high{c['reset']}",
        "medium":  f"{c['yellow']}medium{c['reset']}",
        "low":     f"{c['yellow']}low{c['reset']}",
        "unknown": f"{c['red']}unknown{c['reset']}",
    }.get(confidence, confidence)

    if is_multisig is True:
        status_icon = f"{c['cyan']}✅ Multisig address{c['reset']}"
    elif is_multisig is False:
        status_icon = f"{c['yellow']}— Not multisig{c['reset']}"
    else:
        status_icon = f"{c['red']}❓ Unable to confirm{c['reset']}"

    print(f"\n{c['bold']}Multisig Address Analysis Report{c['reset']}")
    print("─" * 52)
    print(f"Address:       {address}")
    print(f"Chain:         {chain}")
    print(f"Address type:  {address_type}")
    print(f"Conclusion:    {status_icon}  (confidence: {conf_badge})")

    if multisig_type and multisig_type != "—":
        print(f"Multisig type: {multisig_type}")

    if threshold is not None:
        print(f"Threshold:     {threshold} / {total_signers} (at least {threshold} signer(s) required)")

    if owners:
        print(f"Signers:       {len(owners)} total")
        for i, owner in enumerate(owners, 1):
            print(f"  [{i:02d}] {owner}")

    # TRX advanced detail
    owner_perm   = result.get("owner_permission")
    active_perms = result.get("active_permissions", [])
    safe_version = result.get("safe_version")
    nonce        = result.get("nonce")

    if owner_perm and (
        owner_perm["threshold"] > 1 or len(owner_perm["keys"]) > 1
    ):
        print(f"\n{c['bold']}Owner permission (threshold {owner_perm['threshold']}):  {c['reset']}")
        for k in owner_perm["keys"]:
            print(f"  Address {k['address']}  weight {k['weight']}")

    if active_perms:
        for ap in active_perms:
            if ap["threshold"] > 1 or len(ap["keys"]) > 1:
                print(
                    f"{c['bold']}Active permission "
                    f"'{ap['permission_name']}' "
                    f"(threshold {ap['threshold']}): {c['reset']}"
                )
                for k in ap["keys"]:
                    print(f"  Address {k['address']}  weight {k['weight']}")

    if safe_version:
        print(f"Safe version:  {safe_version}")
    if nonce is not None:
        print(f"Tx count:      {nonce}")

    print("─" * 52)
    note = result.get("note", "")
    if note:
        print(f"Note: {note}")
    print()


def print_error(message: str, json_output: bool) -> None:
    if json_output:
        print(json.dumps(
            {"is_multisig": None, "error": message},
            ensure_ascii=False, indent=2
        ))
    else:
        print(f"\n❌  Multisig analysis failed\nReason: {message}\n", file=sys.stderr)


# ─── Argument parsing ────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    all_chains = sorted(SUPPORTED_CHAINS | set(UNSUPPORTED_CHAINS.keys()))
    parser = argparse.ArgumentParser(
        description=(
            "Multisig address identification and permission analysis tool\n"
            "Supports BTC (P2SH/P2WSH/P2TR), ETH/EVM (Gnosis Safe), TRX (native permission multisig)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--address", "-a",
        required=True,
        help="Blockchain address to analyze",
    )
    parser.add_argument(
        "--chain", "-c",
        required=True,
        choices=all_chains,
        help=(
            f"Chain identifier\n"
            f"Supported: {', '.join(sorted(SUPPORTED_CHAINS))}\n"
            f"Unsupported (exit 2): {', '.join(sorted(UNSUPPORTED_CHAINS.keys()))}"
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output result in JSON format (suitable for machine parsing by agents)",
    )
    return parser.parse_args()


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()
    chain   = args.chain.lower()
    address = args.address.strip()

    # 1. Handle explicitly unsupported chains
    if chain in UNSUPPORTED_CHAINS:
        print_error(UNSUPPORTED_CHAINS[chain], args.json_output)
        sys.exit(EXIT_UNSUPPORTED)

    # 2. Route to the correct analyzer
    try:
        if chain in BTC_CHAINS:
            result = analyze_btc(address)
        elif chain in TRX_CHAINS:
            result = analyze_trx(address)
        else:
            result = analyze_evm(address, chain)
    except RuntimeError as e:
        print_error(str(e), args.json_output)
        sys.exit(EXIT_ERROR)

    # 3. Print result
    print_result(result, address, chain, args.json_output)

    # 4. Exit code
    is_multisig = result.get("is_multisig")
    if is_multisig is True or is_multisig is None:
        sys.exit(EXIT_IS_MULTISIG)
    else:
        sys.exit(EXIT_NOT_MULTISIG)


if __name__ == "__main__":
    main()
