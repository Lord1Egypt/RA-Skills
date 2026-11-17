#!/usr/bin/env python3
"""Fetch one full normalized job posting from a pasted Indeed URL. 1 credit.

Usage:
  python3 get_role_by_url.py "https://www.indeed.com/viewjob?jk=a1b2c3d4e5f60718"
  python3 get_role_by_url.py "https://www.indeed.com/viewjob?jk=a1b2c3d4e5f60718" --fields title,salary
"""

import argparse

import _client


def main():
    parser = argparse.ArgumentParser(
        description="Fetch a role from an Indeed URL via RolesAPI (GET /v1/roles/by-url)."
    )
    parser.add_argument("url", help="Indeed viewjob URL")
    parser.add_argument("--fields", default=None, help="Comma-separated field projection, e.g. title,company.name,salary.min")
    args = parser.parse_args()

    envelope = _client.request(
        "GET",
        "/v1/roles/by-url",
        params={"url": args.url, "fields": args.fields},
    )
    _client.output(envelope)


if __name__ == "__main__":
    main()
