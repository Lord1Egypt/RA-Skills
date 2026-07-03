#!/usr/bin/env python3
"""Crypto Trader — signal scanning, risk management, market intelligence."""
import json, subprocess, sys

SIGNAL_ENGINE = "/opt/king/sae/crypto/crypto_moonshot_futures.py"

def scan_market(mode="basic"):
    """Scan crypto market for trading signals"""
    r = subprocess.run(["python3", SIGNAL_ENGINE, "scan"], capture_output=True, text=True, timeout=30)
    return {"market": "scanned", "signal_count": r.stdout.count("score="), "data": r.stdout[:500]}

def check_status():
    """Check current positions and account"""
    r = subprocess.run(["python3", SIGNAL_ENGINE, "status"], capture_output=True, text=True, timeout=15)
    return {"status": r.stdout.strip()}

if __name__ == '__main__':
    args = sys.argv[1:]
    if "--status" in args:
        result = check_status()
    else:
        result = scan_market("pro" if "--pro" in args else "basic")
    print(json.dumps(result, indent=2, ensure_ascii=False))
