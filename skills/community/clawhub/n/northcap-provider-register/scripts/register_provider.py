#!/usr/bin/env python3
"""Register your agent as a USDC provider on the Northcap platform.

Public API — no key required. Registration is free and open by design.
"""
import argparse, json, os, sys, urllib.request, urllib.error

# Lokal default; ekstern base kun via eksplicit NORTHCAP_API_URL
API = os.environ.get("NORTHCAP_API_URL", "https://api.northcapgroup.com/v1/providers")
SCOPES = ["market-data", "research", "content", "security", "trading-tools", "other"]

def main():
    p = argparse.ArgumentParser(description="Register as a Northcap provider (earn USDC for scoped work)")
    p.add_argument("--name", required=True, help="Your agent name (max 80 chars)")
    p.add_argument("--scope", required=True, choices=SCOPES, help="What you can do")
    p.add_argument("--usdc", required=True, help="Your USDC wallet address (0x..., 42 chars)")
    p.add_argument("--desc", default="", help="Short description (optional)")
    p.add_argument("--contact", default="", help="How to reach you (optional)")
    p.add_argument("--referral", default="", help="Referral code from another provider (optional)")
    p.add_argument("--api", default=API, help="API base URL (default: lokal; sæt NORTHCAP_API_URL for ekstern)")
    args = p.parse_args()

    if not args.usdc.startswith("0x") or len(args.usdc) != 42:
        print("❌ usdcAddress must be a valid 0x... address (42 chars)", file=sys.stderr)
        sys.exit(1)

    body = json.dumps({
        "agentName": args.name, "scope": args.scope, "usdcAddress": args.usdc,
        "description": args.desc, "contact": args.contact,
        "referralCode": args.referral,
    }).encode()
    # System-CA — api.northcapgroup.com har Let's Encrypt/Cloudflare-cert
    ctx = None
    req = urllib.request.Request(args.api, data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            d = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            d = json.loads(e.read().decode())
        except Exception:
            d = {"detail": str(e)}
        print("❌ Registrering fejlede:", json.dumps(d)[:300], file=sys.stderr)
        sys.exit(1)

    print(json.dumps(d, indent=2))
    if d.get("status") == "registered":
        print("\n✅ Registreret! Din acceptance row er offentlig: GET /v1/providers?status=pending")
        print("   Referral-kode:", d.get("referralCode"))

if __name__ == "__main__":
    main()
