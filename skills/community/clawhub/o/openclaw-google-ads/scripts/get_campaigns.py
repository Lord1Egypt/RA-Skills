#!/usr/bin/env python3
"""
Get campaigns from Google Ads API
"""

import os
import sys
import argparse
from google.ads.googleads.client import GoogleAdsClient

def get_campaigns(manager_account_id, client_account_id=None):
    """List all campaigns for the specified account."""
    
    # Initialize client
    client = GoogleAdsClient.load_from_env()
    
    # Use client account if specified, otherwise use manager
    customer_id = client_account_id or manager_account_id
    
    ga_service = client.get_service("GoogleAdsService")
    
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY campaign.id
    """
    
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id.replace('-', '')
    search_request.query = query
    
    print(f"Campaigns for account: {customer_id}")
    print("-" * 80)
    
    try:
        results = ga_service.search(request=search_request)
        
        for row in results:
            campaign = row.campaign
            metrics = row.metrics
            
            cost = metrics.cost_micros / 1000000 if metrics.cost_micros else 0
            
            print(f"ID: {campaign.id}")
            print(f"Name: {campaign.name}")
            print(f"Status: {campaign.status.name}")
            print(f"Channel: {campaign.advertising_channel_type.name}")
            print(f"Impressions: {metrics.impressions}")
            print(f"Clicks: {metrics.clicks}")
            print(f"Cost: ${cost:.2f}")
            print(f"Conversions: {metrics.conversions}")
            print("-" * 80)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Get Google Ads campaigns')
    parser.add_argument('--account', required=True, help='Account ID (with dashes)')
    parser.add_argument('--client-account', help='Client account ID (for manager accounts)')
    
    args = parser.parse_args()
    
    get_campaigns(args.account, args.client_account)

if __name__ == '__main__':
    main()
