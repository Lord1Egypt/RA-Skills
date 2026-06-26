#!/usr/bin/env python3
"""
Neodomain AI - Authentication Script
Send verification code and login to get access token.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

BASE_URL = "https://story.neodomain.cn"


def send_code(contact: str) -> dict:
    """Send verification code to phone or email."""
    url = f"{BASE_URL}/user/login/send-unified-code"
    data = json.dumps({"contact": contact}).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
        sys.exit(1)


def login(contact: str, code: str, invitation_code: str = None) -> dict:
    """Login with verification code to get access token."""
    url = f"{BASE_URL}/user/login/unified-login"
    payload = {"contact": contact, "code": code}
    if invitation_code:
        payload["invitationCode"] = invitation_code
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("success"):
                return result.get("data", {})
            else:
                print(f"Login failed: {result.get('errMessage')}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Neodomain AI Authentication")
    parser.add_argument("--send-code", action="store_true", help="Send verification code")
    parser.add_argument("--login", action="store_true", help="Login with code")
    parser.add_argument("--contact", required=True, help="Phone number or email")
    parser.add_argument("--code", help="Verification code (for login)")
    parser.add_argument("--invitation-code", help="Invitation code (optional)")
    
    args = parser.parse_args()
    
    if args.send_code:
        result = send_code(args.contact)
        if result.get("success"):
            print("✅ Verification code sent successfully!")
        else:
            print(f"❌ Failed: {result.get('errMessage')}")
            sys.exit(1)
    
    elif args.login:
        if not args.code:
            print("❌ Error: --code is required for login")
            sys.exit(1)
        
        result = login(args.contact, args.code, args.invitation_code)
        print("\n✅ Login successful!")
        print(f"\nAccess Token:")
        print(result.get("authorization"))
        print(f"\nUser Info:")
        print(f"  User ID: {result.get('userId')}")
        print(f"  Nickname: {result.get('nickname')}")
        print(f"  Email: {result.get('email')}")
        print(f"  Mobile: {result.get('mobile')}")
        print("\n📝 Add to your environment:")
        print(f'export NEODOMAIN_ACCESS_TOKEN="{result.get("authorization")}"')
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
