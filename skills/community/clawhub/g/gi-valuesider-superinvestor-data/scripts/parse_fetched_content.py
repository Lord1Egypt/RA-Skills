#!/usr/bin/env python3
"""
Parse ValueSider page content (e.g. from MCP web_fetch) into JSON.
Reads from stdin or --file. Use after fetching portfolio or activity URL.
Usage:
  python parse_fetched_content.py --type portfolio [--file path]
  python parse_fetched_content.py --type activity [--file path]
"""
from __future__ import annotations

import argparse
import json
import re
import sys


def _extract_summary(text: str) -> dict:
    summary = {}
    for pattern, key in [
        (r"Portfolio value:\s*(.+?)(?:\n|$)", "portfolio_value"),
        (r"Period:\s*(.+?)(?:\n|$)", "period"),
        (r"Number of stock:\s*(\d+)(?:\n|$)", "number_of_stocks"),
        (r"Update:\s*(.+?)(?:\n|$)", "update_date"),
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            summary[key] = m.group(1).strip()
    return summary


def _strip_md_link(s: str) -> str:
    """Take [text](url) -> text."""
    m = re.match(r"\[([^\]]+)\]\([^)]*\)", s.strip())
    return m.group(1).strip() if m else s.strip()


def parse_portfolio_content(text: str, guru_slug: str = "", source_url: str = "") -> dict:
    """Parse portfolio page text (e.g. from web_fetch) into structured JSON."""
    summary = _extract_summary(text)
    holdings = []
    lines = text.split("\n")
    i = 0
    ticker_re = re.compile(r"^[A-Z]{2,5}$")
    pct_re = re.compile(r"^(\d+\.?\d*%)$")
    shares_re = re.compile(r"^([\d,]+)$")
    price_re = re.compile(r"^\$[\d,]+\.?\d*$")
    value_re = re.compile(r"^\$[\d,]+\.?\d*$")
    activity_re = re.compile(r"^([+-]?\d+\.?\d*%)\s*\([^)]*\)$")  # e.g. -15.20% (-553,218)
    pct_change_re = re.compile(r"^[+-]?\d+\.?\d*%$")

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ticker_re.match(line) and len(line) >= 2 and len(line) <= 5:
            ticker = line
            stock_name = ""
            pct = ""
            shares = ""
            reported_price = ""
            value = ""
            activity = ""
            pct_change = ""
            i += 1
            while i < len(lines):
                rest = lines[i].strip()
                if not rest:
                    i += 1
                    continue
                if ticker_re.match(rest) and len(rest) >= 2 and len(rest) <= 5 and rest != ticker:
                    break
                if re.match(r"^\d+\s+of\s+\d+", rest) or "go to page" in rest.lower():
                    break
                if not stock_name and (rest.startswith("[") or (" INC" in rest or " CORP" in rest or " CO" in rest)):
                    stock_name = _strip_md_link(rest)
                elif pct_re.match(rest) and not pct:
                    pct = rest
                elif shares_re.match(rest) and rest.replace(",", "").isdigit() and not shares:
                    shares = rest
                elif price_re.match(rest):
                    if not reported_price:
                        reported_price = rest
                    elif not value:
                        value = rest
                elif value_re.match(rest) and not value:
                    value = rest
                elif activity_re.match(rest) or (rest.startswith("+") or rest.startswith("-")) and "%" in rest and "(" in rest:
                    activity = rest
                elif pct_change_re.match(rest) and not pct_change and activity:
                    pct_change = rest
                elif pct_change_re.match(rest) and not pct_change and not activity:
                    pct_change = rest
                i += 1
            holdings.append({
                "ticker": ticker,
                "stock_name": stock_name or ticker,
                "pct_of_portfolio": pct,
                "shares": shares,
                "reported_price": reported_price,
                "value": value,
                "activity": activity,
                "pct_change_to_portfolio": pct_change,
            })
            continue
        i += 1

    return {
        "source": source_url or "fetched",
        "guru_slug": guru_slug,
        "summary": summary,
        "holdings": holdings,
    }


def parse_activity_content(text: str, guru_slug: str = "", source_url: str = "") -> dict:
    """Parse portfolio-activity page text into structured JSON."""
    activities = []
    lines = text.split("\n")
    i = 0
    current_quarter = None
    quarter_re = re.compile(r"(20\d{2}\s*Q[1-4])(?:\s*\(\d+\s+results\))?")
    ticker_re = re.compile(r"^[A-Z]{2,5}$")

    while i < len(lines):
        line = lines[i].strip()
        qm = quarter_re.search(line)
        if qm and len(line) < 30:
            current_quarter = qm.group(1).strip()
            i += 1
            continue
        if ticker_re.match(line) and current_quarter and len(line) >= 2 and len(line) <= 5:
            ticker = line
            stock_name = ""
            activity_type = ""
            share_change = ""
            pct_change = ""
            reported_price = ""
            pct_portfolio = ""
            i += 1
            while i < len(lines):
                rest = lines[i].strip()
                if not rest:
                    i += 1
                    continue
                if quarter_re.search(rest) and len(rest) < 30:
                    break
                if ticker_re.match(rest) and len(rest) >= 2 and len(rest) <= 5 and rest != ticker:
                    break
                if not stock_name and (rest.startswith("[") or " INC" in rest or " CORP" in rest):
                    stock_name = _strip_md_link(rest)
                elif rest.lower() in ("buy", "sell"):
                    activity_type = rest
                elif re.match(r"^[+-][\d,]+$", rest):  # e.g. +3,418,974
                    share_change = rest
                elif re.match(r"^[+-]?\d+\.?\d*%$", rest):  # single percentage only
                    if not pct_change:
                        pct_change = rest
                    elif not pct_portfolio:
                        pct_portfolio = rest
                elif rest.startswith("$") and not rest.count("$") > 1:
                    reported_price = rest
                i += 1
            activities.append({
                "quarter": current_quarter,
                "ticker": ticker,
                "stock_name": stock_name or ticker,
                "activity_type": activity_type,
                "share_change": share_change,
                "pct_change_to_portfolio": pct_change,
                "reported_price": reported_price,
                "pct_of_portfolio": pct_portfolio,
            })
            continue
        i += 1

    return {
        "source": source_url or "fetched",
        "guru_slug": guru_slug,
        "activities": activities,
    }


def main():
    ap = argparse.ArgumentParser(description="Parse ValueSider fetched content to JSON")
    ap.add_argument("--type", choices=["portfolio", "activity"], required=True)
    ap.add_argument("--file", help="Read from file; otherwise stdin")
    ap.add_argument("--guru-slug", default="", help="Guru slug for output")
    ap.add_argument("--source-url", default="", help="Source URL for output")
    args = ap.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if args.type == "portfolio":
        out = parse_portfolio_content(text, guru_slug=args.guru_slug, source_url=args.source_url)
    else:
        out = parse_activity_content(text, guru_slug=args.guru_slug, source_url=args.source_url)

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
