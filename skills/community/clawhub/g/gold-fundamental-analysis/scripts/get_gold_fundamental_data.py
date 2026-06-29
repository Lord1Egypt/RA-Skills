#!/usr/bin/env python3
"""
Gold Fundamental Analysis Data Fetcher
======================================
Fetches data from 5 sources:
  1. FRED API — Macro indicators (Fed rate, CPI, 10Y yield, Real yield, DXY)
  2. CFTC COT — Commitment of Traders (Managed Money long/short)
  3. SPDR Gold ETF — Holdings via SSGA/GLD AUM
  4. Fed RSS — Monetary policy statements (7-day window)
  5. Investing.com — Economic calendar (high-impact USD events)

Usage:
  python3 get_gold_fundamental_data.py [--fred-key KEY]
  
Output: JSON to stdout
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import xml.etree.ElementTree as ET

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests module not installed. Run: pip install requests"}))
    sys.exit(1)

# ── Configuration ──────────────────────────────────────────────
FRED_API_KEY = os.environ.get("FRED_API_KEY", "01fa16f50b07eb27740820fd1cdecf50")
FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
CFTC_URL = "https://www.cftc.gov/dea/newcot/f_disagg.txt"
FED_RSS_URL = "https://www.federalreserve.gov/feeds/press_monetary.xml"
SSGA_GLD_URL = "https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-shares-gld"

# FRED series IDs
FRED_SERIES = {
    "fed_rate": "FEDFUNDS",
    "cpi": "CPIAUCSL",
    "core_cpi": "CPILFESL",
    "us10y_yield": "DGS10",
    "real_yield": "DFII10",
    "dxy": "DTWEXBGS",
}

# ── Helpers ────────────────────────────────────────────────────
def safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, {})
        else:
            return default
    return d if d != {} else default

def parse_date(s: str) -> Optional[str]:
    """Parse various date formats to YYYY-MM-DD."""
    for fmt in ["%Y-%m-%d", "%d %b %Y", "%a, %d %b %Y %H:%M:%S %Z",
                 "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"]:
        try:
            return datetime.strptime(s.strip(), fmt).strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            continue
    return None

# ── 1. FRED Macro Data ─────────────────────────────────────────
def fetch_fred_macro() -> dict:
    """Fetch latest 2 observations for each macro series."""
    result = {}
    for key, series_id in FRED_SERIES.items():
        try:
            params = {
                "series_id": series_id,
                "api_key": FRED_API_KEY,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 2,
            }
            resp = requests.get(FRED_BASE, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            obs = data.get("observations", [])
            if len(obs) >= 2:
                result[key] = {
                    "current": float(obs[0]["value"]) if obs[0]["value"] != "." else None,
                    "previous": float(obs[1]["value"]) if obs[1]["value"] != "." else None,
                    "current_date": obs[0]["date"],
                    "previous_date": obs[1]["date"],
                }
            elif len(obs) == 1:
                result[key] = {
                    "current": float(obs[0]["value"]) if obs[0]["value"] != "." else None,
                    "previous": None,
                }
            else:
                result[key] = {"error": "no data"}
        except Exception as e:
            result[key] = {"error": str(e)}
    return result


# ── 2. CFTC COT Data ───────────────────────────────────────────
def fetch_cftc_cot() -> dict:
    """Parse CFTC disaggregated COT report for gold futures."""
    try:
        resp = requests.get(CFTC_URL, timeout=15)
        resp.raise_for_status()
        text = resp.text
    except Exception as e:
        return {"error": str(e)}

    # Find the GOLD line
    for line in text.split("\n"):
        if '"GOLD - COMMODITY EXCHANGE INC."' not in line:
            continue
        
        # Parse CSV line (quoted fields)
        fields = []
        current = ""
        in_quotes = False
        for ch in line:
            if ch == '"':
                in_quotes = not in_quotes
            elif ch == ',' and not in_quotes:
                fields.append(current)
                current = ""
            else:
                current += ch
        fields.append(current)

        try:
            # Fields in disagg report:
            # 0: Market name
            # 1: Report date (YYMMDD)
            # 2: Date (YYYY-MM-DD)
            # 8: Managed Money Long
            # 9: Managed Money Short
            report_date = fields[2] if len(fields) > 2 else "unknown"
            mm_long = int(fields[8]) if len(fields) > 8 else 0
            mm_short = int(fields[9]) if len(fields) > 9 else 0
            net_position = mm_long - mm_short

            return {
                "date": report_date,
                "managed_money_long": mm_long,
                "managed_money_short": mm_short,
                "net_position": net_position,
                "net_position_label": "bullish" if net_position > 0 else "bearish",
            }
        except (ValueError, IndexError) as e:
            return {"error": f"parse error: {e}", "raw": line[:200]}

    return {"error": "GOLD line not found in COT report"}


# ── 3. SPDR Gold ETF Holdings ──────────────────────────────────
def fetch_spdr_holdings() -> dict:
    """Fetch GLD AUM from SSGA and compute approximate gold tonnage."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        }
        resp = requests.get(SSGA_GLD_URL, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text

        # Extract AUM from SSGA page
        # Look for pattern: "Assets Under Management" ... "$136,399.42 M"
        aum_match = re.search(r'Assets Under Management[^$]*\$([0-9,]+\.[0-9]{2})\s*([BM])', html, re.DOTALL)
        nav_match = re.search(r'NAV[^$]*\$([0-9,]+\.[0-9]{2})', html, re.DOTALL)
        
        if not aum_match:
            return {"error": "could not find AUM on SSGA page"}

        aum_str = aum_match.group(1).replace(",", "")
        aum_unit = aum_match.group(2)  # B or M
        aum_value = float(aum_str)
        
        # Convert B to M if needed
        if aum_unit == "B":
            aum_value *= 1000
        
        # Estimate gold price from NAV (NAV ≈ 0.10 * gold price per oz)
        # Actually GLD NAV tracks ~1/10th of gold price
        # More precisely: each share ≈ 0.095 oz gold
        gold_per_share_oz = 0.095  # approximate
        
        nav_value = None
        if nav_match:
            nav_value = float(nav_match.group(1).replace(",", ""))
            # estimated gold price = nav / gold_per_share_oz
            est_gold_price = nav_value / gold_per_share_oz
            # estimated tonnes = aum_millions * 1000000 / est_gold_price / 32150.7
            est_tonnes = (aum_value * 1_000_000) / est_gold_price / 32150.7
        else:
            # Rough estimate: GLD AUM / ~$90,000 per oz / 32150.7
            est_tonnes = (aum_value * 1_000_000) / 90000 / 32150.7
            est_gold_price = None
        
        return {
            "aum_usd_millions": aum_value,
            "nav": nav_value,
            "estimated_tonnes": round(est_tonnes, 2),
            "estimated_gold_price": round(est_gold_price, 2) if est_gold_price else None,
            "note": "GLD AUM from SSGA. Tonnes are estimated from NAV/gold price ratio."
        }

    except Exception as e:
        return {"error": str(e)}


# ── 4. Fed Statements (RSS) ────────────────────────────────────
def fetch_fed_statements() -> dict:
    """Parse Fed monetary policy RSS feed for last 7 days."""
    try:
        resp = requests.get(FED_RSS_URL, timeout=15)
        resp.raise_for_status()
        # Decode with BOM handling
        text = resp.content.decode('utf-8-sig')
        root = ET.fromstring(text)
        
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)
        
        recent_items = []
        for item in root.findall(".//item"):
            pub_date_str = item.findtext("pubDate", "")
            pub_date = None
            for fmt in ["%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"]:
                try:
                    pub_date = datetime.strptime(pub_date_str.strip(), fmt)
                    break
                except ValueError:
                    continue
            
            if pub_date is None:
                continue
                
            if pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=timezone.utc)
            
            if pub_date >= thirty_days_ago:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                desc = item.findtext("description", "")
                recent_items.append({
                    "title": title,
                    "date": pub_date.strftime("%Y-%m-%d"),
                    "link": link,
                    "summary": desc,
                })
        
        # Determine stance based on keywords in recent items
        all_text = " ".join([i["title"] + " " + i["summary"] for i in recent_items]).lower()
        
        hawkish_keywords = ["inflation risk", "tighten", "hawkish", "price stability", 
                           "inflation remains", "inflationary", "rate hike", "restrictive"]
        dovish_keywords = ["easing", "dovish", "accommodative", "rate cut", 
                          "soft landing", "disinflation", "progress on inflation"]
        
        hawkish_score = sum(1 for kw in hawkish_keywords if kw in all_text)
        dovish_score = sum(1 for kw in dovish_keywords if kw in all_text)
        
        if hawkish_score > dovish_score:
            stance = "hawkish"
        elif dovish_score > hawkish_score:
            stance = "dovish"
        else:
            stance = "neutral"
        
        # Generate summary
        if recent_items:
            summary = f"{len(recent_items)} Fed releases in past 30 days. "
            if recent_items:
                summary += f"Latest: {recent_items[0]['title']} ({recent_items[0]['date']})"
        else:
            summary = "No Fed monetary policy releases in past 30 days."
        
        return {
            "stance": stance,
            "confidence": round(abs(hawkish_score - dovish_score) / max(len(recent_items) or 1, 1), 2),
            "summary": summary,
            "recent_items": recent_items[:5],
        }

    except Exception as e:
        return {"error": str(e)}


# ── 5. Economic Calendar (ForexFactory via Faireconomy) ─────────
def fetch_economic_calendar() -> dict:
    """Fetch high/medium-impact USD economic events from ForexFactory JSON.
    Source: nfs.faireconomy.media (public JSON, no API key).
    """
    key_events = [
        "cpi", "ppi", "nfp", "gdp", "fomc", "ism", "retail sales",
        "nonfarm", "unemployment", "fed", "consumer confidence",
        "durable goods", "housing", "pce", "jobless", "current account",
        "trade balance", "industrial production", "building permits",
        "new home", "existing home", "philly fed", "empire state",
        "preliminary", "final ", "advanced ", "cb consumer", "sentiment",
        "cpi ", "core pce", "core cpi", "personal income", "personal spending",
        "wholesale inventories", "factory orders", "services pmi",
        "manufacturing pmi", "composite pmi", "s&p global"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    all_usd_events = []
    
    for source_url in [
        "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
        "https://nfs.faireconomy.media/ff_calendar_nextweek.json",
    ]:
        try:
            resp = requests.get(source_url, headers=headers, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            for e in data:
                if e.get("country") != "USD":
                    continue
                impact = e.get("impact", "").lower()
                if impact not in ("high", "medium"):
                    continue
                title_lower = e["title"].lower()
                if not any(kw in title_lower for kw in key_events):
                    continue
                all_usd_events.append({
                    "event": e["title"],
                    "date": e["date"],
                    "impact": impact,
                    "forecast": e.get("forecast", ""),
                    "previous": e.get("previous", ""),
                    "currency": "USD",
                })
        except Exception:
            continue
    
    # Sort by date
    all_usd_events.sort(key=lambda x: x["date"])
    
    if all_usd_events:
        return {
            "source": "ForexFactory (via faireconomy.media)",
            "upcoming_events": all_usd_events[:20],
        }
    
    return {
        "source": "unavailable",
        "upcoming_events": [],
        "note": "Could not fetch economic calendar data.",
    }


# ── Main ────────────────────────────────────────────────────────
def main():
    # Parse CLI args
    if "--fred-key" in sys.argv:
        idx = sys.argv.index("--fred-key")
        if idx + 1 < len(sys.argv):
            global FRED_API_KEY
            FRED_API_KEY = sys.argv[idx + 1]

    result = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "macro": fetch_fred_macro(),
        "cot": fetch_cftc_cot(),
        "etf": fetch_spdr_holdings(),
        "fed": fetch_fed_statements(),
        "economic_calendar": fetch_economic_calendar(),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
