#!/usr/bin/env python3
"""Fetch only the description slice of a job posting. 1 credit.

Usage:
  python3 get_description.py a1b2c3d4e5f60718
  python3 get_description.py a1b2c3d4e5f60718 --country gb
"""

import argparse

import _client


def main():
    parser = argparse.ArgumentParser(
        description="Fetch the description sub-resource via RolesAPI (GET /v1/roles/{job_key}/description)."
    )
    parser.add_argument("job_key", help="16-character job key, e.g. a1b2c3d4e5f60718")
    parser.add_argument("--country", default=None, help="Two-letter Indeed country edition code (default us)")
    args = parser.parse_args()

    envelope = _client.request(
        "GET",
        "/v1/roles/" + args.job_key + "/description",
        params={"country": args.country},
    )
    _client.output(envelope)


if __name__ == "__main__":
    main()
