"""Fetch recent news headlines for an LSE stock from Yahoo Finance.

Outputs JSON for the OpenClaw agent (LLM) to analyze sentiment.
No ML dependencies — just raw headlines for the LLM to interpret.

Usage:
    uv run scripts/sentiment.py HSBA.L
    uv run scripts/sentiment.py HSBA.L --max-headlines 10
    uv run scripts/sentiment.py VOD
"""

import argparse
import json
import sys
from datetime import datetime, timezone

import yfinance as yf


def fetch_headlines(ticker: str, max_headlines: int = 50) -> dict:
    """Fetch recent news headlines from yfinance for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        raw_news = stock.news
    except Exception as e:
        return {
            "ticker": ticker,
            "headline_count": 0,
            "headlines": [],
            "error": f"Failed to fetch news: {e}",
        }

    if not raw_news or not isinstance(raw_news, list):
        return {
            "ticker": ticker,
            "headline_count": 0,
            "headlines": [],
        }

    headlines = []
    for item in raw_news[:max_headlines]:
        try:
            # yfinance >= 0.2.31 nests data under a "content" key
            content = item.get("content", item) if isinstance(item, dict) else {}

            title = (
                content.get("title")
                or content.get("headline")
                or item.get("title")
                or ""
            )
            publisher = (
                (content.get("provider") or {}).get("displayName")
                or content.get("publisher")
                or item.get("publisher")
                or ""
            )

            # Link: prefer canonicalUrl, fall back to clickThroughUrl or flat keys
            canon = content.get("canonicalUrl") or {}
            click = content.get("clickThroughUrl") or {}
            link = (
                canon.get("url")
                or click.get("url")
                or content.get("link")
                or item.get("link")
                or ""
            )

            # Publish time: ISO string or unix timestamp
            pub_raw = (
                content.get("pubDate")
                or content.get("displayTime")
                or item.get("providerPublishTime")
                or item.get("published")
            )
            if isinstance(pub_raw, (int, float)):
                published = datetime.fromtimestamp(pub_raw, tz=timezone.utc).isoformat()
            elif isinstance(pub_raw, str):
                published = pub_raw
            else:
                published = None

            if not title:
                continue

            headlines.append({
                "title": title,
                "publisher": publisher,
                "link": link,
                "published": published,
            })
        except Exception:
            # Skip malformed items without crashing
            continue

    return {
        "ticker": ticker,
        "headline_count": len(headlines),
        "headlines": headlines,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch recent news headlines for an LSE stock")
    parser.add_argument("ticker", help="Yahoo Finance ticker (e.g., HSBA.L)")
    parser.add_argument("--max-headlines", type=int, default=50, help="Maximum number of headlines to return")
    args = parser.parse_args()

    ticker = args.ticker if "." in args.ticker else f"{args.ticker}.L"
    result = fetch_headlines(ticker, max_headlines=args.max_headlines)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
