#!/usr/bin/env python3
"""
Price Tracker - Track single product across platforms with alerts.
Powered by SkillBoss API Hub for real-time price search and extraction.
"""

import argparse
import json
import csv
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional

import requests

# SkillBoss API Hub — unified AI & web capability router
SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"

PLATFORMS = {
    "amazon": {"fee_rate": 0.15, "name": "Amazon"},
    "ebay": {"fee_rate": 0.13, "name": "eBay"},
    "walmart": {"fee_rate": 0.10, "name": "Walmart"},
    "bestbuy": {"fee_rate": 0.12, "name": "Best Buy"},
}


def pilot(body: dict) -> dict:
    """Call SkillBoss API Hub /v1/pilot — auto-routes to optimal model/service."""
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


def search_product(keyword: str, platform: str) -> List[Dict]:
    """Search product prices via SkillBoss API Hub (web search + LLM extraction)."""
    # Step 1: web search for product listing on platform
    search_result = pilot({
        "type": "search",
        "inputs": {"query": f"site:{platform}.com {keyword} price buy"},
        "prefer": "balanced",
    })
    search_data = search_result["result"]

    # Step 2: LLM extracts structured price data from search results
    extract_result = pilot({
        "type": "chat",
        "inputs": {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"From these search results, extract the current price for '{keyword}' on {platform}. "
                        f"Return ONLY a valid JSON object with these fields: "
                        f'{{\"title\": string, \"price\": number, \"seller\": string, \"rating\": number, \"condition\": string}}. '
                        f"Search results: {str(search_data)[:3000]}"
                    ),
                }
            ]
        },
        "prefer": "balanced",
    })
    content = extract_result["result"]["choices"][0]["message"]["content"]

    try:
        json_match = re.search(r"\{[^{}]*\}", content, re.DOTALL)
        if json_match:
            product_data = json.loads(json_match.group())
            return [
                {
                    "title": product_data.get("title", keyword),
                    "price": float(product_data.get("price", 0.0)),
                    "platform": platform,
                    "seller": product_data.get("seller", "unknown"),
                    "rating": float(product_data.get("rating", 4.0)),
                    "condition": product_data.get("condition", "New"),
                    "url": f"https://{platform}.com/search?q={keyword.replace(' ', '+')}",
                }
            ]
    except (json.JSONDecodeError, AttributeError, ValueError):
        pass

    return []


def calculate_margin(buy_price: float, sell_price: float, buy_platform: str, sell_platform: str) -> float:
    """Calculate profit margin after fees."""
    buy_fee = buy_price * PLATFORMS[buy_platform]["fee_rate"]
    sell_fee = sell_price * PLATFORMS[sell_platform]["fee_rate"]
    estimated_shipping = 10.0  # Average shipping cost

    total_cost = buy_price + buy_fee + estimated_shipping
    revenue = sell_price - sell_fee

    profit = revenue - total_cost
    margin = profit / total_cost if total_cost > 0 else 0.0

    return margin


def analyze_arbitrage(products: List[Dict]) -> List[Dict]:
    """Analyze arbitrage opportunities across platforms."""
    opportunities = []

    for i, buy_product in enumerate(products):
        for j, sell_product in enumerate(products):
            if i == j:
                continue

            margin = calculate_margin(
                buy_product["price"],
                sell_product["price"],
                buy_product["platform"],
                sell_product["platform"],
            )

            opportunities.append(
                {
                    "buy_from": buy_product["platform"],
                    "buy_price": buy_product["price"],
                    "sell_on": sell_product["platform"],
                    "sell_price": sell_product["price"],
                    "margin": margin,
                    "margin_percent": f"{margin * 100:.1f}%",
                }
            )

    # Sort by margin descending
    opportunities.sort(key=lambda x: x["margin"], reverse=True)
    return opportunities


def format_alerts(products: List[Dict], opportunities: List[Dict], alert_below: Optional[float], alert_margin: Optional[float]) -> str:
    """Format price alerts and arbitrage opportunities."""
    alerts = []

    # Price drop alerts
    if alert_below:
        for product in products:
            if product["price"] <= alert_below:
                alerts.append(f"PRICE DROP: {product['title']} on {product['platform']}: ${product['price']:.2f} (below ${alert_below:.2f})")

    # Arbitrage opportunity alerts
    if alert_margin:
        for opp in opportunities:
            if opp["margin"] >= alert_margin:
                alerts.append(
                    f"ARBITRAGE: Buy from {opp['buy_from']} (${opp['buy_price']:.2f}) -> Sell on {opp['sell_on']} (${opp['sell_price']:.2f}) -> Margin: {opp['margin_percent']}"
                )

    return "\n".join(alerts) if alerts else "No alerts triggered."


def format_markdown(products: List[Dict], opportunities: List[Dict], alerts: str) -> str:
    """Format output as Markdown."""
    md = f"# Price Tracking Report\n\n"
    md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    md += "## Current Prices\n\n"
    md += "| Platform | Price | Seller | Rating | Condition |\n"
    md += "|----------|-------|--------|--------|-----------|\n"

    for product in products:
        md += f"| {product['platform']} | ${product['price']:.2f} | {product['seller']} | {product['rating']:.1f}/5 | {product['condition']} |\n"

    md += "\n## Arbitrage Opportunities\n\n"
    md += "| Buy From | Buy Price | Sell On | Sell Price | Margin |\n"
    md += "|----------|-----------|---------|------------|--------|\n"

    for opp in opportunities:
        color = "HIGH" if opp["margin"] >= 0.20 else "MED" if opp["margin"] >= 0.10 else "LOW"
        md += f"| {opp['buy_from']} | ${opp['buy_price']:.2f} | {opp['sell_on']} | ${opp['sell_price']:.2f} | [{color}] {opp['margin_percent']} |\n"

    if alerts:
        md += "\n## Alerts\n\n"
        md += alerts

    return md


def format_json(products: List[Dict], opportunities: List[Dict]) -> str:
    """Format output as JSON."""
    return json.dumps(
        {
            "timestamp": datetime.now().isoformat(),
            "products": products,
            "arbitrage_opportunities": opportunities,
        },
        indent=2,
    )


def main():
    parser = argparse.ArgumentParser(description="Track product prices across platforms")
    parser.add_argument("--product", required=True, help="Product name/keyword")
    parser.add_argument("--platforms", default="amazon,ebay,walmart,bestbuy", help="Comma-separated platforms")
    parser.add_argument("--alert-below", type=float, help="Alert when price drops below this amount")
    parser.add_argument("--alert-margin", type=float, help="Alert when arbitrage margin exceeds this fraction")
    parser.add_argument("--frequency", choices=["hourly", "daily", "weekly"], default="daily", help="Check frequency")
    parser.add_argument("--output", choices=["markdown", "json", "csv"], default="markdown", help="Output format")

    args = parser.parse_args()

    # Parse platforms
    platforms = [p.strip() for p in args.platforms.split(",")]
    platforms = [p for p in platforms if p in PLATFORMS]

    if not platforms:
        print(f"Error: No valid platforms specified. Available: {', '.join(PLATFORMS.keys())}")
        sys.exit(1)

    # Search for product across platforms via SkillBoss API Hub
    products = []
    for platform in platforms:
        results = search_product(args.product, platform)
        products.extend(results)

    # Analyze arbitrage opportunities
    opportunities = analyze_arbitrage(products)

    # Generate alerts
    alerts = format_alerts(products, opportunities, args.alert_below, args.alert_margin)

    # Format output
    if args.output == "markdown":
        output = format_markdown(products, opportunities, alerts)
    elif args.output == "json":
        output = format_json(products, opportunities)
    elif args.output == "csv":
        output = "Platform,Price,Seller,Rating\n"
        for product in products:
            output += f"{product['platform']},{product['price']},{product['seller']},{product['rating']}\n"
    else:
        output = format_markdown(products, opportunities, alerts)

    print(output)

    # Print alerts to stderr for cron integration
    if alerts:
        print("\n---ALERTS---", file=sys.stderr)
        print(alerts, file=sys.stderr)


if __name__ == "__main__":
    main()
