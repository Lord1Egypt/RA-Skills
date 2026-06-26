#!/usr/bin/env python3
"""
Hemlane Rent Roll Extraction

Extracts tenant/lease data from Hemlane using GraphQL operations
derived from HAR files. Outputs structured rent roll data.

Usage:
  python3 extract_rent_roll.py --output /path/to/rent_roll.json
"""

import json
import argparse
from pathlib import Path

# GraphQL operation from tenant-reply HAR
# Extracted from: ODTenantsAndLeasesBucketCounts, TGTenantGroup
RENT_ROLL_QUERY = """
query ODTenantsAndLeasesBucketCounts($input: ODTenantsAndLeasesBucketCountsInput!) {
  ODTenantsAndLeasesBucketCounts(input: $input) {
    buckets {
      id
      name
      status
      tenants {
        id
        name
        email
        phone
        leaseStart
        leaseEnd
        rentAmount
        paymentStatus
        property {
          id
          address
          unit
        }
      }
    }
  }
}
"""

def extract_rent_roll(auth_headers, output_path=None):
    """
    Fetch rent roll from Hemlane GraphQL API.
    
    Requires:
    - auth_headers: dict with cookies, x-csrf-token, etc.
    - output_path: optional path to save JSON output
    """
    import requests
    
    endpoint = "https://app.hemlane.com/graphql"
    
    variables = {
        "input": {
            "filters": {},
            "pagination": {"limit": 100}
        }
    }
    
    response = requests.post(
        endpoint,
        json={"query": RENT_ROLL_QUERY, "variables": variables},
        headers=auth_headers
    )
    response.raise_for_status()
    
    data = response.json()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    return data

def main():
    parser = argparse.ArgumentParser(description='Extract rent roll from Hemlane')
    parser.add_argument('--output', '-o', help='Output JSON path')
    parser.add_argument('--auth-file', help='JSON file with auth headers')
    args = parser.parse_args()
    
    auth_headers = {}
    if args.auth_file:
        with open(args.auth_file) as f:
            auth_headers = json.load(f)
    
    result = extract_rent_roll(auth_headers, args.output)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
