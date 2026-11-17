#!/usr/bin/env python3
"""Search live Indeed job postings by keyword and location. 1 credit per page.

Usage:
  python3 search_listings.py "registered nurse" "Chicago, IL"
  python3 search_listings.py "backend engineer" "remote" --sort date
  python3 search_listings.py "data analyst" "London" --country gb
"""

import argparse

import _client


def main():
    parser = argparse.ArgumentParser(
        description="Search Indeed job postings via RolesAPI (GET /v1/listings)."
    )
    parser.add_argument("keyword", help='Search keywords, e.g. "backend engineer"')
    parser.add_argument("location", help='City, state, postal code, or "remote"')
    parser.add_argument("--country", default=None, help="Two-letter Indeed country edition code (default us)")
    parser.add_argument("--sort", choices=["date", "relevance"], default=None, help="Sort order")
    args = parser.parse_args()

    envelope = _client.request(
        "GET",
        "/v1/listings",
        params={
            "keyword": args.keyword,
            "location": args.location,
            "country": args.country,
            "sort": args.sort,
        },
    )
    _client.output(envelope)


if __name__ == "__main__":
    main()
