#!/usr/bin/env python3
"""Fetch one full normalized job posting by its 16-character job key. 1 credit.

Usage:
  python3 get_role.py a1b2c3d4e5f60718
  python3 get_role.py a1b2c3d4e5f60718 --country gb
  python3 get_role.py a1b2c3d4e5f60718 --fields title,company.name,salary
"""

import argparse

import _client


def main():
    parser = argparse.ArgumentParser(
        description="Fetch a role by job key via RolesAPI (GET /v1/roles/{job_key})."
    )
    parser.add_argument("job_key", help="16-character job key, e.g. a1b2c3d4e5f60718")
    parser.add_argument("--country", default=None, help="Two-letter Indeed country edition code (default us)")
    parser.add_argument("--fields", default=None, help="Comma-separated field projection, e.g. title,company.name,salary.min")
    args = parser.parse_args()

    envelope = _client.request(
        "GET",
        "/v1/roles/" + args.job_key,
        params={"country": args.country, "fields": args.fields},
    )
    _client.output(envelope)


if __name__ == "__main__":
    main()
