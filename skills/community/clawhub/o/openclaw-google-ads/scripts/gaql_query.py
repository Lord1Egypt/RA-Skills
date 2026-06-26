#!/usr/bin/env python3
"""
Run custom GAQL queries against Google Ads API.
"""

import sys
import argparse
from google.ads.googleads.client import GoogleAdsClient
from google.protobuf.json_format import MessageToDict


def run_query(account_id, query):
    """Execute a GAQL query and print rows as dictionaries."""

    client = GoogleAdsClient.load_from_env()
    ga_service = client.get_service("GoogleAdsService")

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = account_id.replace('-', '')
    search_request.query = query

    print(f"Querying account: {account_id}")
    print(f"Query: {query}")
    print("-" * 80)

    try:
        results = ga_service.search(request=search_request)

        count = 0
        for row in results:
            count += 1
            print(f"\nRow {count}:")
            row_dict = MessageToDict(row._pb, preserving_proto_field_name=True)
            for key, value in row_dict.items():
                print(f"  {key}: {value}")

        print(f"\nTotal rows: {count}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Run GAQL query on Google Ads')
    parser.add_argument('--account', required=True, help='Account ID (with dashes)')
    parser.add_argument('--query', required=True, help='GAQL query string')

    args = parser.parse_args()
    run_query(args.account, args.query)


if __name__ == '__main__':
    main()
