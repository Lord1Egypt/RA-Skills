#!/usr/bin/env python3
"""
Look up Business Profile account_id + location_id(s) using an existing
refresh token. No browser needed. Retries with backoff on 429s.

  pip install google-auth requests
  python3 lookup_ids.py
"""

import getpass
import time
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def get_token(cid, csec, rtok):
    creds = Credentials(
        token=None, refresh_token=rtok, client_id=cid, client_secret=csec,
        token_uri="https://oauth2.googleapis.com/token",
    )
    creds.refresh(Request())
    return creds.token


def get_with_retry(url, headers, params=None, tries=6):
    for i in range(tries):
        r = requests.get(url, headers=headers, params=params, timeout=30)
        if r.status_code != 429:
            return r
        wait = 20 * (i + 1)
        print(f"   429 rate-limited, waiting {wait}s (attempt {i+1}/{tries})...")
        time.sleep(wait)
    return r


def main():
    cid = input("Client ID: ").strip()
    csec = getpass.getpass("Client secret (hidden): ").strip()
    rtok = getpass.getpass("Refresh token (hidden): ").strip()

    token = get_token(cid, csec, rtok)
    h = {"Authorization": f"Bearer {token}"}

    print("\nLooking up accounts...\n")
    ar = get_with_retry("https://mybusinessaccountmanagement.googleapis.com/v1/accounts", h)
    if ar.status_code != 200:
        print(f"Accounts call failed ({ar.status_code}):\n{ar.text[:600]}")
        if ar.status_code == 429:
            print("\n>>> Still rate-limited after retries. This means your Business Profile")
            print(">>> API quota is likely 0/min. You'll need a one-time quota increase.")
        return

    accounts = ar.json().get("accounts", [])
    if not accounts:
        print("No accounts on this Google login. Raw:", ar.text[:400])
        return

    for acct in accounts:
        name = acct.get("name", "")
        print(f"ACCOUNT: {name}   ({acct.get('accountName','')})")
        lr = get_with_retry(
            f"https://mybusinessbusinessinformation.googleapis.com/v1/{name}/locations",
            h, params={"readMask": "name,title,storefrontAddress"},
        )
        if lr.status_code != 200:
            print(f"   locations failed ({lr.status_code}): {lr.text[:300]}")
            continue
        for loc in lr.json().get("locations", []):
            addr = loc.get("storefrontAddress", {})
            city = addr.get("locality", "")
            print(f"   LOCATION: {loc.get('name','')}   title: {loc.get('title','')}   {city}")

    print("\nDone. Paste the ACCOUNT and LOCATION line(s) back to Claude.")


if __name__ == "__main__":
    main()
