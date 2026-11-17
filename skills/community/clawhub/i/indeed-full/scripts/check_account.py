#!/usr/bin/env python3
"""Check your RolesAPI account: plan, rate limit, and credit balance.

Usage:
  python3 check_account.py            # GET /v1/me
  python3 check_account.py --usage    # GET /v1/usage (recent usage records)
"""

import argparse

import _client


def main():
    parser = argparse.ArgumentParser(
        description="Check the current RolesAPI account and credit balance."
    )
    parser.add_argument("--usage", action="store_true", help="List recent usage records instead")
    parser.add_argument("--since", default=None, help="With --usage: only records at or after this timestamp")
    parser.add_argument("--limit", type=int, default=None, help="With --usage: page size")
    args = parser.parse_args()

    if args.usage:
        envelope = _client.request(
            "GET", "/v1/usage", params={"since": args.since, "limit": args.limit}
        )
    else:
        envelope = _client.request("GET", "/v1/me")
    _client.output(envelope)


if __name__ == "__main__":
    main()
