import os
import sys
import json
import argparse

# --- SECURITY & DEPENDENCY CHECK ---
# Explicitly checking for 'requests' to satisfy OpenClaw runtime safety requirements.
try:
    import requests
except ImportError:
    print("Error: The 'requests' library is missing.", file=sys.stderr)
    print("Please install it via: pip install requests", file=sys.stderr)
    sys.exit(1)

# Gateway Configuration
# SECURITY: Hardcoded to 127.0.0.1 for maximum safety against exfiltration.
# This ensures that your AGENT_API_KEY is only sent to your local instance.
GATEWAY_URL = "http://127.0.0.1:38084"

def _get_api_key(explicit: str = None) -> str:
    """Resolve API key from argument or environment."""
    api_key = explicit or os.environ.get("AGENT_API_KEY")
    if not api_key:
        return None
    return api_key

def api_call(endpoint, method="GET", data=None, api_key=None):
    resolved_key = _get_api_key(api_key)
    if not resolved_key:
        return {"error": "AGENT_API_KEY is required (env or --api-key)"}
    
    headers = {
        "X-API-KEY": resolved_key,
        "Content-Type": "application/json"
    }
    
    url = f"{GATEWAY_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    
    try:
        session = requests.Session()
        session.trust_env = False
        if method == "GET":
            response = session.get(url, headers=headers, timeout=10)
        else:
            response = session.post(url, headers=headers, json=data, timeout=10)
            
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_balance(api_key=None):
    res = api_call("balance", api_key=api_key)
    print(json.dumps(res))

def get_sync(api_key=None):
    res = api_call("sync", api_key=api_key)
    print(json.dumps(res))

def create_address(label, api_key=None):
    res = api_call("subaddress", method="POST", data={"label": label}, api_key=api_key)
    print(json.dumps(res))

def get_address(api_key=None):
    res = api_call("address", api_key=api_key)
    print(json.dumps(res))

def transfer(address, amount_xmr, api_key=None):
    res = api_call("transfer", method="POST", data={
        "address": address, 
        "amount_xmr": float(amount_xmr)
    }, api_key=api_key)
    print(json.dumps(res))

def pay_402(address, amount_xmr, message, api_key=None):
    """XMR402 Protocol: Pay a 402 challenge and get back an Authorization header."""
    res = api_call("pay_402", method="POST", data={
        "address": address,
        "amount_xmr": float(amount_xmr),
        "message": message
    }, api_key=api_key)
    print(json.dumps(res))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ripley Monero Gateway Client for AI Agents")
    parser.add_argument("--api-key", help="Ripley Gateway API Key (defaults to AGENT_API_KEY env)")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("get-balance")
    subparsers.add_parser("check-sync")
    subparsers.add_parser("get-address")
    
    addr_parser = subparsers.add_parser("create-address")
    addr_parser.add_argument("label", help="Label for the new address")
    
    xfer_parser = subparsers.add_parser("transfer")
    xfer_parser.add_argument("address", help="Destination address")
    xfer_parser.add_argument("amount", type=float, help="Amount in XMR")

    pay402_parser = subparsers.add_parser("pay-402")
    pay402_parser.add_argument("address", help="Destination address from WWW-Authenticate header")
    pay402_parser.add_argument("amount", type=float, help="Amount in XMR from WWW-Authenticate header")
    pay402_parser.add_argument("message", help="Challenge nonce from WWW-Authenticate header")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "get-balance":
        get_balance(args.api_key)
    elif args.command == "check-sync":
        get_sync(args.api_key)
    elif args.command == "get-address":
        get_address(args.api_key)
    elif args.command == "create-address":
        create_address(args.label, args.api_key)
    elif args.command == "transfer":
        transfer(args.address, args.amount, args.api_key)
    elif args.command == "pay-402":
        pay_402(args.address, args.amount, args.message, args.api_key)

