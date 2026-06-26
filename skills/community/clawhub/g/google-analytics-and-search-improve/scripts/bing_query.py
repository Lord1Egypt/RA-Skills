#!/usr/bin/env python3
"""Bing Webmaster Tools API data extraction tool.

Usage:
    python bing_query.py --mode query_stats -o bing_queries.json
    python bing_query.py --mode page_stats -o bing_pages.json
    python bing_query.py --mode rank_traffic -o bing_traffic.json
    python bing_query.py --mode query_detail --query "search term"
    python bing_query.py --mode page_detail --page "https://example.com/page"
    python bing_query.py --mode keyword --query "keyword" --country us
    python bing_query.py --mode links -o bing_links.json
    python bing_query.py --mode crawl_stats -o bing_crawl.json

Reads .env from: .skills-data/google-analytics-and-search-improve/.env
Env vars: BING_WEBMASTER_API_KEY, SITE_URL
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

import utils  # noqa: F401  — triggers .env loading & warning suppression
import requests


BASE_URL = "https://ssl.bing.com/webmaster/api.svc/json"


def get_api_key():
    api_key = os.environ.get("BING_WEBMASTER_API_KEY")
    if not api_key:
        print("Error: BING_WEBMASTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    return api_key


def api_get(endpoint, params=None):
    """Make a GET request to the Bing Webmaster API."""
    api_key = get_api_key()
    url = f"{BASE_URL}/{endpoint}"
    if params is None:
        params = {}
    params["apikey"] = api_key
    response = requests.get(url, params=params, timeout=30)
    if response.status_code != 200:
        print(f"Error: HTTP {response.status_code} — {response.text}", file=sys.stderr)
        sys.exit(1)
    return response.json()


def get_query_stats(site_url):
    """Get traffic statistics for top queries."""
    data = api_get("GetQueryStats", {"siteUrl": site_url})
    return data


def get_page_stats(site_url):
    """Get traffic statistics for top pages."""
    data = api_get("GetPageStats", {"siteUrl": site_url})
    return data


def get_rank_and_traffic_stats(site_url):
    """Get overall rank and traffic stats (daily impressions/clicks)."""
    data = api_get("GetRankAndTrafficStats", {"siteUrl": site_url})
    return data


def get_query_traffic_stats(site_url, query):
    """Get detailed traffic stats for a specific query."""
    data = api_get("GetQueryTrafficStats", {
        "siteUrl": site_url,
        "query": query,
    })
    return data


def get_page_query_stats(site_url, page_url):
    """Get query stats for a specific page."""
    data = api_get("GetPageQueryStats", {
        "siteUrl": site_url,
        "pageUrl": page_url,
    })
    return data


def get_query_page_detail_stats(site_url, query, page_url):
    """Get detailed stats for a specific query + page combination."""
    data = api_get("GetQueryPageDetailStats", {
        "siteUrl": site_url,
        "query": query,
        "pageUrl": page_url,
    })
    return data


def get_keyword(site_url, keyword, country, start_date, end_date):
    """Get keyword impression data for a country and date range."""
    data = api_get("GetKeyword", {
        "siteUrl": site_url,
        "query": keyword,
        "country": country,
        "stringStartDate": start_date,
        "stringEndDate": end_date,
    })
    return data


def get_related_keywords(site_url, keyword, country, start_date, end_date):
    """Get related keywords with impression data."""
    data = api_get("GetRelatedKeywords", {
        "siteUrl": site_url,
        "query": keyword,
        "country": country,
        "stringStartDate": start_date,
        "stringEndDate": end_date,
    })
    return data


def get_link_counts(site_url, page=0):
    """Get pages with inbound link counts."""
    data = api_get("GetLinkCounts", {
        "siteUrl": site_url,
        "page": page,
    })
    return data


def get_crawl_stats(site_url):
    """Get crawl statistics."""
    data = api_get("GetCrawlStats", {"siteUrl": site_url})
    return data


def get_crawl_issues(site_url):
    """Get crawl issues."""
    data = api_get("GetCrawlIssues", {"siteUrl": site_url})
    return data


def main():
    parser = argparse.ArgumentParser(description="Bing Webmaster Tools API query tool")
    parser.add_argument("--site-url", default=os.environ.get("SITE_URL"),
                        help="Site URL (or set SITE_URL env)")
    parser.add_argument("--mode", choices=[
        "query_stats", "page_stats", "rank_traffic",
        "query_detail", "page_detail", "query_page_detail",
        "keyword", "related_keywords",
        "links", "crawl_stats", "crawl_issues",
    ], default="query_stats")
    parser.add_argument("--query", help="Query string (for query_detail, keyword, related_keywords modes)")
    parser.add_argument("--page", help="Page URL (for page_detail, query_page_detail modes)")
    parser.add_argument("--country", default="us", help="Country code (for keyword modes, default: us)")
    parser.add_argument("--start-date",
                        default=(datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d"))
    parser.add_argument("--end-date",
                        default=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    if not args.site_url:
        print("Error: --site-url required or set SITE_URL", file=sys.stderr)
        sys.exit(1)

    result = None

    if args.mode == "query_stats":
        data = get_query_stats(args.site_url)
        result = {
            "mode": "query_stats",
            "site_url": args.site_url,
            "data": data,
        }

    elif args.mode == "page_stats":
        data = get_page_stats(args.site_url)
        result = {
            "mode": "page_stats",
            "site_url": args.site_url,
            "data": data,
        }

    elif args.mode == "rank_traffic":
        data = get_rank_and_traffic_stats(args.site_url)
        result = {
            "mode": "rank_traffic",
            "site_url": args.site_url,
            "data": data,
        }

    elif args.mode == "query_detail":
        if not args.query:
            print("Error: --query required for query_detail mode", file=sys.stderr)
            sys.exit(1)
        data = get_query_traffic_stats(args.site_url, args.query)
        result = {
            "mode": "query_detail",
            "site_url": args.site_url,
            "query": args.query,
            "data": data,
        }

    elif args.mode == "page_detail":
        if not args.page:
            print("Error: --page required for page_detail mode", file=sys.stderr)
            sys.exit(1)
        data = get_page_query_stats(args.site_url, args.page)
        result = {
            "mode": "page_detail",
            "site_url": args.site_url,
            "page": args.page,
            "data": data,
        }

    elif args.mode == "query_page_detail":
        if not args.query or not args.page:
            print("Error: --query and --page required for query_page_detail mode", file=sys.stderr)
            sys.exit(1)
        data = get_query_page_detail_stats(args.site_url, args.query, args.page)
        result = {
            "mode": "query_page_detail",
            "site_url": args.site_url,
            "query": args.query,
            "page": args.page,
            "data": data,
        }

    elif args.mode == "keyword":
        if not args.query:
            print("Error: --query required for keyword mode", file=sys.stderr)
            sys.exit(1)
        data = get_keyword(args.site_url, args.query, args.country,
                           args.start_date, args.end_date)
        result = {
            "mode": "keyword",
            "site_url": args.site_url,
            "query": args.query,
            "country": args.country,
            "date_range": {"start": args.start_date, "end": args.end_date},
            "data": data,
        }

    elif args.mode == "related_keywords":
        if not args.query:
            print("Error: --query required for related_keywords mode", file=sys.stderr)
            sys.exit(1)
        data = get_related_keywords(args.site_url, args.query, args.country,
                                    args.start_date, args.end_date)
        result = {
            "mode": "related_keywords",
            "site_url": args.site_url,
            "query": args.query,
            "country": args.country,
            "date_range": {"start": args.start_date, "end": args.end_date},
            "data": data,
        }

    elif args.mode == "links":
        data = get_link_counts(args.site_url)
        result = {
            "mode": "links",
            "site_url": args.site_url,
            "data": data,
        }

    elif args.mode == "crawl_stats":
        data = get_crawl_stats(args.site_url)
        result = {
            "mode": "crawl_stats",
            "site_url": args.site_url,
            "data": data,
        }

    elif args.mode == "crawl_issues":
        data = get_crawl_issues(args.site_url)
        result = {
            "mode": "crawl_issues",
            "site_url": args.site_url,
            "data": data,
        }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
