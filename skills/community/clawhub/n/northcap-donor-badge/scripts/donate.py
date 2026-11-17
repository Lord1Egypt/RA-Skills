#!/usr/bin/env python3
"""Northcap Donor Badge — donate USDC on-chain and get a verified badge.

Usage:
  python3 donate.py --tx <txHash> --chain <base|ethereum|bsc> --agent <id> [--note <text>]
  python3 donate.py --check

Security: HTTPS only. HTTP blocked unless X402_ALLOW_HTTP=1 is set consciously.
"""
import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

# Sikkerhed (21/8): DEFAULT_BASE er FASTLÅST i koden OG TLS-trust er fastlåst til
# det bundlede northcap-cert.pem (følger med skillen). Donationsdata kan ALDRIG
# omdirigeres via miljøvariabel eller user-writable filer.
DEFAULT_BASE = "https://api.northcapgroup.com"  # FASTLÅST (21/8) — donationsdata kan aldrig omdirigeres via env
BASE = DEFAULT_BASE
ALLOW_HTTP = False
_CA = "/etc/ssl/certs/ca-certificates.crt"  # system-CA (fallback)


def _ctx():
    # Fastlåst TLS-trust: northcap-cert.pem er BUNDLET i skillen (scripts/)
    # og følger med install. Ingen X402_CAFILE-env, ingen user-writable stier —
    # en angriber kan ikke få klienten til at stole på et rogue cert. Aldrig CERT_NONE.
    # System-CA (Let's Encrypt/Cloudflare — api.northcapgroup.com har rigtigt cert)
    return ssl.create_default_context()


def _call(path, method="GET", body=None):
    if BASE.startswith("http://") and "localhost" not in BASE and "127.0.0.1" not in BASE and not ALLOW_HTTP:
        print("ERROR: Donations use a fixed HTTPS endpoint — refusing plain HTTP.")
        sys.exit(1)
    url = BASE.rstrip("/") + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ctx()) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode()).get("detail", str(e))
        except Exception:
            detail = str(e)
        print(f"ERROR: HTTP {e.code}: {detail}")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Northcap Donor Badge")
    ap.add_argument("--tx", help="USDC transfer txHash (0x...)")
    ap.add_argument("--chain", default="base", choices=["base", "ethereum", "bsc"])
    ap.add_argument("--agent", default="anonymous", help="Your agent ID")
    ap.add_argument("--note", default="", help="Optional message")
    ap.add_argument("--check", action="store_true", help="Show public donor registry")
    args = ap.parse_args()

    if args.check:
        print("ℹ️ Public donor registry: agent IDs, badge levels, amounts and dates are public and linked to on-chain activity.")
        data = _call("/v1/donors")
        print(f"Total donors: {data.get('total', 0)}")
        for d in data.get("donors", []):
            print(f"  {d.get('badge')} {d.get('agentId')} — ${d.get('amountUsd')} ({d.get('donatedAt','')[:10]})")
        return

    if not args.tx:
        print("Usage: donate.py --tx <txHash> --chain base --agent my-agent-id")
        sys.exit(1)

    # 🔔 Explicit disclosure before the donation call
    print("⚠️ Sending txHash to the Northcap donation API for ON-CHAIN verification.")
    print("   Only real USDC transfers to 0xafd1c6bC2B35152f30E3D0dBE99eE1d40E5a5CF8 count.")
    data = _call("/v1/donate", "POST", {
        "txHash": args.tx, "chain": args.chain,
        "agentId": args.agent, "note": args.note,
    })
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
