#!/usr/bin/env python3
"""
Get account performance summary from Google Ads API
"""

import os
import sys
import argparse
from google.ads.googleads.client import GoogleAdsClient

def get_account_summary(manager_account_id, days=30):
    """Get performance summary for the account."""
    
    # Load config from env with proto_plus setting
    config = {
        "developer_token": os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "client_id": os.environ.get("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_ADS_CLIENT_SECRET"),
        "refresh_token": os.environ.get("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "").replace("-", ""),
        "use_proto_plus": True
    }
    
    client = GoogleAdsClient.load_from_dict(config)
    ga_service = client.get_service("GoogleAdsService")
    
    query = f"""
        SELECT
            customer.id,
            customer.descriptive_name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM customer
        WHERE segments.date DURING LAST_{days}_DAYS
    """
    
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = manager_account_id.replace('-', '')
    search_request.query = query
    
    print(f"Account Summary (Last {days} Days)")
    print("-" * 80)
    
    try:
        results = ga_service.search(request=search_request)
        
        total_impressions = 0
        total_clicks = 0
        total_cost = 0
        total_conversions = 0
        
        for row in results:
            customer = row.customer
            metrics = row.metrics
            
            cost = metrics.cost_micros / 1000000 if metrics.cost_micros else 0
            
            print(f"Account: {customer.descriptive_name} ({customer.id})")
            print(f"  Impressions: {metrics.impressions:,}")
            print(f"  Clicks: {metrics.clicks:,}")
            print(f"  Cost: ${cost:,.2f}")
            print(f"  Conversions: {metrics.conversions}")
            print(f"  Conv. Value: ${metrics.conversions_value:,.2f}")
            print()
            
            total_impressions += metrics.impressions
            total_clicks += metrics.clicks
            total_cost += cost
            total_conversions += metrics.conversions
        
        print("-" * 80)
        print("TOTALS:")
        print(f"  Impressions: {total_impressions:,}")
        print(f"  Clicks: {total_clicks:,}")
        print(f"  Cost: ${total_cost:,.2f}")
        print(f"  Conversions: {total_conversions}")
        
        if total_clicks > 0:
            cpc = total_cost / total_clicks
            print(f"  Avg CPC: ${cpc:.2f}")
        
        if total_impressions > 0:
            ctr = (total_clicks / total_impressions) * 100
            print(f"  CTR: {ctr:.2f}%")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Get Google Ads account summary')
    parser.add_argument('--account', required=True, help='Account ID (with dashes)')
    parser.add_argument('--days', type=int, default=30, help='Number of days (default: 30)')
    
    args = parser.parse_args()
    
    get_account_summary(args.account, args.days)

if __name__ == '__main__':
    main()
