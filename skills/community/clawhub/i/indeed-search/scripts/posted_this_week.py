#!/usr/bin/env python3
"""List Indeed postings from the last 7 days. 1 credit per page, up to 3 pages.

Usage:
  python3 posted_this_week.py "product manager" --location "Austin, TX"
  python3 posted_this_week.py "data engineer" --max-pages 2
"""

import argparse

import _client


def main():
    parser = argparse.ArgumentParser(
        description="Postings from the last 7 days via RolesAPI (POST /v1/listings/posted-this-week)."
    )
    parser.add_argument("keyword", help='Search keywords, e.g. "product manager"')
    parser.add_argument("--location", default=None, help="City, state, or postal code (optional)")
    parser.add_argument("--country", default=None, help="Two-letter Indeed country edition code (default us)")
    parser.add_argument("--max-pages", type=int, default=None, help="Pages to fetch, 1 credit each")
    args = parser.parse_args()

    envelope = _client.request(
        "POST",
        "/v1/listings/posted-this-week",
        body={
            "keyword": args.keyword,
            "location": args.location,
            "country": args.country,
            "max_pages": args.max_pages,
        },
    )
    _client.output(envelope)


if __name__ == "__main__":
    main()
