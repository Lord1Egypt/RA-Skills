#!/usr/bin/env python3
"""
Fetch Polymarket portfolio positions for review.

Dual-mode:
  --address 0x...    → Fetch real wallet positions via Data API
  --from-history ... → Build paper portfolio from recommendation-history.md

Outputs structured JSON with current prices, P&L, and days remaining.

Usage:
    python3 fetch_portfolio.py --from-history ~/polymarket-reports/recommendation-history.md --latest 9
    python3 fetch_portfolio.py --address 0xYourWalletAddress
    python3 fetch_portfolio.py --help
"""

import argparse
import http.client
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
DATA_API = "https://data-api.polymarket.com"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "polymarket-portfolio-review/1.0",
}


# ---------------------------------------------------------------------------
# HTTP helpers (reused from backtest.py)
# ---------------------------------------------------------------------------

def fetch_with_retry(url: str, max_retries: int = 3, backoff: float = 1.0):
    """GET JSON with exponential backoff."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except (urllib.error.URLError,
                http.client.IncompleteRead,
                http.client.RemoteDisconnected,
                TimeoutError,
                ConnectionResetError) as e:
            if attempt < max_retries - 1:
                wait = backoff * (2 ** attempt)
                print(f"[WARN] Retry {attempt + 1}/{max_retries}: {e}", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"[ERROR] Failed after {max_retries} retries: {url}", file=sys.stderr)
                return None


def fetch_midpoint(token_id: str) -> float | None:
    """Fetch midpoint price for a CLOB token."""
    try:
        data = fetch_with_retry(f"{CLOB_API}/midpoint?token_id={token_id}")
        if data:
            mid = data.get("mid")
            if mid is not None:
                return float(mid)
    except Exception as e:
        print(f"[WARN] Midpoint fetch failed for {token_id[:20]}...: {e}", file=sys.stderr)
    return None


def fetch_event_data(event_slug: str) -> dict | None:
    """Fetch event data from Gamma API by slug."""
    try:
        url = f"{GAMMA_API}/events/slug/{event_slug}"
        return fetch_with_retry(url)
    except Exception as e:
        print(f"[WARN] Event fetch failed for {event_slug}: {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# History parsing (reused from backtest.py)
# ---------------------------------------------------------------------------

def parse_history(filepath: Path) -> list[dict]:
    """Parse recommendation-history.md table into a list of records."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.strip().split("\n")

    records = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]
        if len(cells) < 10:
            continue
        if cells[0] in ("Date", "------", "---"):
            continue
        if set(cells[0]) <= {"-"}:
            continue

        try:
            # cells[2] is Link (polymarket URL), skip it
            entry_price_str = cells[4]
            entry_price = None
            if entry_price_str != "N/A":
                entry_price = float(entry_price_str.replace("%", "")) / 100.0

            ai_prob_str = cells[5]
            ai_prob = None
            if ai_prob_str != "N/A":
                ai_prob = float(ai_prob_str.replace("%", ""))

            edge_str = cells[6]
            edge = None
            if edge_str != "N/A":
                edge = float(edge_str.replace("%", "").replace("+", ""))

            position_str = cells[9]
            position_usd = None
            if position_str != "N/A":
                position_usd = float(position_str.replace("$", "").replace(",", ""))

            end_date = cells[11] if len(cells) > 11 else None
            status = cells[12] if len(cells) > 12 else "Open"

            records.append({
                "date": cells[0],
                "market": cells[1],
                "link": cells[2],
                "direction": cells[3],
                "entry_price": entry_price,
                "ai_prob": ai_prob,
                "edge": edge,
                "position_usd": position_usd,
                "end_date": end_date,
                "status": status,
            })
        except (ValueError, IndexError) as e:
            print(f"[WARN] Skipping malformed row: {line[:80]}... ({e})", file=sys.stderr)

    return records


# ---------------------------------------------------------------------------
# Pulse report scanning — extract event slugs (reused from backtest.py)
# ---------------------------------------------------------------------------

def scan_pulse_reports(report_dir: Path) -> list[dict]:
    """
    Scan all market-pulse-*.md files for polymarket.com/event/{slug} URLs.
    Returns a list of {slug, title_context} mappings.
    """
    slug_entries = []
    pattern = re.compile(r"https://polymarket\.com/event/([\w-]+)")

    for report_path in sorted(report_dir.glob("market-pulse-*.md")):
        text = report_path.read_text(encoding="utf-8")
        lines = text.split("\n")

        for i, line in enumerate(lines):
            match = pattern.search(line)
            if not match:
                continue
            slug = match.group(1)

            title_context = ""
            for j in range(max(0, i - 10), i):
                header_match = re.match(r"^##\s+\d+\.\s+(.+)", lines[j])
                if header_match:
                    title_context = header_match.group(1).strip()
                rec_match = re.match(r"^##\s+推荐\s+\d+:\s+(.+)", lines[j])
                if rec_match:
                    title_context = rec_match.group(1).strip()

            slug_entries.append({
                "slug": slug,
                "title_context": title_context,
                "source_file": report_path.name,
            })

    return slug_entries


# ---------------------------------------------------------------------------
# Text matching (reused from backtest.py)
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Normalize text for fuzzy matching."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def match_record_to_slug(record: dict, slug_entries: list[dict],
                         event_cache: dict) -> str | None:
    """
    Match a history record to an event slug using 3-tier strategy.
    """
    market_name = record["market"]
    market_clean = market_name.rstrip(".")
    market_norm = normalize_text(market_clean)
    market_words = set(market_norm.split())

    best_slug = None
    best_score = 0.0

    # Strategy 1: Match against API market questions
    for slug, event_data in event_cache.items():
        if not event_data:
            continue
        markets = event_data.get("markets", [])
        for mkt in markets:
            question = mkt.get("question", "")
            question_norm = normalize_text(question)
            question_words = set(question_norm.split())

            if market_norm in question_norm:
                score = 100 + len(market_norm)
                if score > best_score:
                    best_score = score
                    best_slug = slug
                continue

            if question_norm in market_norm:
                score = 100 + len(question_norm)
                if score > best_score:
                    best_score = score
                    best_slug = slug
                continue

            if not market_words or not question_words:
                continue
            overlap = market_words & question_words
            overlap_ratio = len(overlap) / min(len(market_words), len(question_words))
            if overlap_ratio >= 0.5 and len(overlap) >= 3:
                score = 50 + len(overlap) + overlap_ratio * 10
                if score > best_score:
                    best_score = score
                    best_slug = slug

    if best_slug and best_score >= 50:
        return best_slug

    # Strategy 2: Match against slug text
    for entry in slug_entries:
        slug = entry["slug"]
        slug_text = slug.replace("-", " ")
        slug_norm = normalize_text(slug_text)
        slug_words = set(slug_norm.split())
        slug_words = {w for w in slug_words if not w.isdigit()}

        if not slug_words:
            continue

        overlap = market_words & slug_words
        overlap_ratio = len(overlap) / min(len(market_words), len(slug_words))

        if overlap_ratio >= 0.5 and len(overlap) >= 2:
            score = 30 + len(overlap) + overlap_ratio * 10
            if score > best_score:
                best_score = score
                best_slug = slug

    if best_slug and best_score >= 30:
        return best_slug

    # Strategy 3: Match against pulse report title contexts
    for entry in slug_entries:
        slug = entry["slug"]
        title = entry["title_context"]
        if not title:
            continue

        title_norm = normalize_text(title)

        if market_norm in title_norm or title_norm in market_norm:
            score = 20 + len(market_norm)
            if score > best_score:
                best_score = score
                best_slug = slug

    return best_slug


# ---------------------------------------------------------------------------
# Price data extraction (reused from backtest.py)
# ---------------------------------------------------------------------------

def get_price_data(event_data: dict, direction: str,
                   market_hint: str = "") -> dict:
    """
    Extract current price data for a position from event data.
    Returns {yes_price, no_price, closed, outcome_prices, question, token_ids,
             end_date}.
    """
    if not event_data:
        return {"error": "no event data"}

    markets = event_data.get("markets", [])
    if not markets:
        return {"error": "no markets in event"}

    market = markets[0]
    if len(markets) > 1 and market_hint:
        hint_norm = normalize_text(market_hint)
        hint_words = set(hint_norm.split())
        best_market = None
        best_overlap = 0
        for m in markets:
            q_norm = normalize_text(m.get("question", ""))
            q_words = set(q_norm.split())
            if hint_norm in q_norm or q_norm in hint_norm:
                best_market = m
                best_overlap = 999
                break
            overlap = len(hint_words & q_words)
            if overlap > best_overlap:
                best_overlap = overlap
                best_market = m
        if best_market and best_overlap >= 2:
            market = best_market

    # Parse CLOB token IDs
    ids_raw = market.get("clobTokenIds", "")
    if isinstance(ids_raw, str):
        try:
            ids_raw = json.loads(ids_raw)
        except (json.JSONDecodeError, TypeError):
            ids_raw = []

    yes_token = ids_raw[0] if len(ids_raw) >= 1 else None
    no_token = ids_raw[1] if len(ids_raw) >= 2 else None

    # Parse outcome prices from Gamma API
    outcome_prices_raw = market.get("outcomePrices", "")
    if isinstance(outcome_prices_raw, str):
        try:
            outcome_prices_raw = json.loads(outcome_prices_raw)
        except (json.JSONDecodeError, TypeError):
            outcome_prices_raw = []

    outcome_prices = []
    for p in outcome_prices_raw:
        try:
            outcome_prices.append(float(p))
        except (ValueError, TypeError):
            outcome_prices.append(0.0)

    closed = market.get("closed", False)
    question = market.get("question", "")
    end_date_str = market.get("endDate", "")

    # Fetch midpoint for the relevant token
    yes_mid = None
    no_mid = None
    if not closed:
        if direction == "Buy Yes" and yes_token:
            yes_mid = fetch_midpoint(yes_token)
            if yes_mid is not None:
                no_mid = 1.0 - yes_mid
        elif direction == "Buy No" and no_token:
            no_mid = fetch_midpoint(no_token)
            if no_mid is not None:
                yes_mid = 1.0 - no_mid
        if yes_mid is None and no_mid is None:
            if yes_token:
                yes_mid = fetch_midpoint(yes_token)
                if yes_mid is not None:
                    no_mid = 1.0 - yes_mid
            if yes_mid is None and no_token:
                no_mid = fetch_midpoint(no_token)
                if no_mid is not None:
                    yes_mid = 1.0 - no_mid

    # Final fallback: use outcome_prices from Gamma
    if yes_mid is None and len(outcome_prices) >= 2:
        yes_mid = outcome_prices[0]
        no_mid = outcome_prices[1]

    return {
        "yes_price": yes_mid,
        "no_price": no_mid,
        "closed": closed,
        "outcome_prices": outcome_prices,
        "question": question,
        "token_ids": {"yes": yes_token, "no": no_token},
        "end_date": end_date_str,
    }


# ---------------------------------------------------------------------------
# Deduplication — aggregate same-market+direction recommendations
# ---------------------------------------------------------------------------

def deduplicate_positions(records: list[dict]) -> list[dict]:
    """
    Aggregate records for the same market+direction into single positions.

    For duplicate recommendations:
    - Cumulative position_usd (sum)
    - Weighted average entry_price
    - Keep all individual records for audit trail (_aggregated_from)
    """
    groups: dict[str, list[dict]] = {}
    for rec in records:
        # Normalize market name for grouping (strip trailing dots/ellipsis)
        market_key = normalize_text(rec["market"].rstrip("."))
        direction = rec["direction"]
        key = f"{market_key}||{direction}"
        if key not in groups:
            groups[key] = []
        groups[key].append(rec)

    deduped = []
    for key, group in groups.items():
        if len(group) == 1:
            rec = group[0].copy()
            rec["_aggregated_from"] = 1
            deduped.append(rec)
            continue

        # Aggregate: weighted average entry price, sum position
        total_usd = 0.0
        weighted_entry = 0.0
        valid_entries = 0

        for rec in group:
            if rec["entry_price"] is not None and rec["position_usd"] is not None:
                total_usd += rec["position_usd"]
                weighted_entry += rec["entry_price"] * rec["position_usd"]
                valid_entries += 1

        if valid_entries == 0 or total_usd == 0:
            rec = group[0].copy()
            rec["_aggregated_from"] = len(group)
            deduped.append(rec)
            continue

        avg_entry = weighted_entry / total_usd

        # Use the latest record as base (most recent recommendation)
        latest = max(group, key=lambda r: r["date"])
        aggregated = latest.copy()
        aggregated["entry_price"] = round(avg_entry, 4)
        aggregated["position_usd"] = round(total_usd, 2)
        aggregated["_aggregated_from"] = len(group)
        # Keep the latest AI prob and edge
        aggregated["ai_prob"] = latest.get("ai_prob")
        aggregated["edge"] = latest.get("edge")

        deduped.append(aggregated)

    return deduped


# ---------------------------------------------------------------------------
# Paper portfolio mode
# ---------------------------------------------------------------------------

def build_paper_positions(history_path: Path, reports_dir: Path,
                          latest_n: int = 9) -> dict:
    """
    Build paper portfolio from recommendation-history.md.

    Flow: parse history → filter Open → take latest N → deduplicate →
          match slug → fetch prices → compute P&L → return JSON.
    """
    errors = []

    # Step 1: Parse history
    print("[INFO] Parsing recommendation history...", file=sys.stderr)
    all_records = parse_history(history_path)
    print(f"[INFO] Found {len(all_records)} total recommendations", file=sys.stderr)

    # Step 2: Filter to Open only
    open_records = [r for r in all_records if r.get("status", "Open") == "Open"]
    print(f"[INFO] {len(open_records)} open recommendations", file=sys.stderr)

    # Step 3: Take latest N
    # Records are in chronological order; take the last N
    if latest_n and latest_n < len(open_records):
        selected = open_records[-latest_n:]
        print(f"[INFO] Selected latest {latest_n} open recommendations", file=sys.stderr)
    else:
        selected = open_records
        print(f"[INFO] Using all {len(selected)} open recommendations", file=sys.stderr)

    if not selected:
        return {
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "paper",
            "total_positions": 0,
            "summary": {
                "total_invested": 0,
                "total_current_value": 0,
                "total_pnl": 0,
                "total_pnl_pct": 0,
            },
            "positions": [],
            "errors": ["No open recommendations found"],
        }

    # Step 4: Deduplicate
    deduped = deduplicate_positions(selected)
    print(f"[INFO] After deduplication: {len(deduped)} unique positions "
          f"(from {len(selected)} records)", file=sys.stderr)

    # Step 5: Scan pulse reports for slugs
    print("[INFO] Scanning pulse reports for event slugs...", file=sys.stderr)
    slug_entries = scan_pulse_reports(reports_dir)
    print(f"[INFO] Found {len(slug_entries)} slug references in reports", file=sys.stderr)

    # Step 6: Fetch event data for all unique slugs
    unique_slugs = list({e["slug"] for e in slug_entries})
    print(f"[INFO] Fetching data for {len(unique_slugs)} unique events...", file=sys.stderr)

    event_cache = {}
    for i, slug in enumerate(unique_slugs):
        print(f"[INFO]   ({i + 1}/{len(unique_slugs)}) {slug}", file=sys.stderr)
        data = fetch_event_data(slug)
        if data:
            event_cache[slug] = data
        else:
            # Try truncated slug
            parts = slug.split("-")
            while parts and parts[-1].isdigit():
                parts.pop()
            short_slug = "-".join(parts)
            if short_slug and short_slug != slug:
                print(f"[INFO]     Retrying with truncated slug: {short_slug}",
                      file=sys.stderr)
                data = fetch_event_data(short_slug)
                if data:
                    event_cache[slug] = data
                    event_cache[short_slug] = data
        time.sleep(0.3)

    # Step 7: Match and compute P&L for each position
    print("[INFO] Matching positions and computing P&L...", file=sys.stderr)
    positions = []

    for rec in deduped:
        slug = match_record_to_slug(rec, slug_entries, event_cache)
        if not slug:
            errors.append(f"Could not match: {rec['market']}")
            positions.append({
                "market": rec["market"],
                "direction": rec["direction"],
                "entry_price": rec["entry_price"],
                "current_price": None,
                "shares": None,
                "position_usd": rec["position_usd"],
                "current_value": None,
                "pnl": None,
                "pnl_pct": None,
                "days_remaining": None,
                "end_date": rec.get("end_date"),
                "event_slug": None,
                "token_ids": None,
                "_aggregated_from": rec.get("_aggregated_from", 1),
                "error": "could not match to event slug",
            })
            continue

        event_data = event_cache.get(slug)
        price_data = get_price_data(event_data, rec["direction"], rec["market"])
        time.sleep(0.2)

        if "error" in price_data:
            errors.append(f"Price fetch error for {rec['market']}: {price_data['error']}")
            positions.append({
                "market": rec["market"],
                "direction": rec["direction"],
                "entry_price": rec["entry_price"],
                "current_price": None,
                "shares": None,
                "position_usd": rec["position_usd"],
                "current_value": None,
                "pnl": None,
                "pnl_pct": None,
                "days_remaining": None,
                "end_date": rec.get("end_date"),
                "event_slug": slug,
                "token_ids": None,
                "_aggregated_from": rec.get("_aggregated_from", 1),
                "error": price_data["error"],
            })
            continue

        # Determine current price
        direction = rec["direction"]
        if direction == "Buy Yes":
            current_price = price_data.get("yes_price")
        else:
            current_price = price_data.get("no_price")

        entry_price = rec["entry_price"]
        position_usd = rec["position_usd"]

        if current_price is None or entry_price is None or position_usd is None:
            errors.append(f"Missing price data for {rec['market']}")
            positions.append({
                "market": rec["market"],
                "direction": rec["direction"],
                "entry_price": entry_price,
                "current_price": None,
                "shares": None,
                "position_usd": position_usd,
                "current_value": None,
                "pnl": None,
                "pnl_pct": None,
                "days_remaining": None,
                "end_date": rec.get("end_date"),
                "event_slug": slug,
                "token_ids": price_data.get("token_ids"),
                "_aggregated_from": rec.get("_aggregated_from", 1),
                "error": "missing price data",
            })
            continue

        shares = position_usd / entry_price
        current_value = shares * current_price
        pnl = current_value - position_usd
        pnl_pct = (pnl / position_usd) * 100 if position_usd else 0

        # Compute days remaining
        days_remaining = None
        end_date = rec.get("end_date") or ""
        # Try to parse end_date from record first
        if end_date and end_date != "N/A":
            try:
                end_dt = datetime.strptime(end_date.strip(), "%Y-%m-%d")
                now = datetime.now(timezone.utc).replace(tzinfo=None)
                days_remaining = max(0, (end_dt - now).days)
            except ValueError:
                pass

        # Fallback: try end_date from API
        if days_remaining is None:
            api_end = price_data.get("end_date", "")
            if api_end:
                try:
                    # API format: "2026-12-31T00:00:00Z"
                    end_dt = datetime.strptime(api_end[:10], "%Y-%m-%d")
                    now = datetime.now(timezone.utc).replace(tzinfo=None)
                    days_remaining = max(0, (end_dt - now).days)
                    if not end_date or end_date == "N/A":
                        end_date = api_end[:10]
                except ValueError:
                    pass

        positions.append({
            "market": price_data.get("question") or rec["market"],
            "direction": rec["direction"],
            "entry_price": round(entry_price, 4),
            "current_price": round(current_price, 4),
            "shares": round(shares, 2),
            "position_usd": round(position_usd, 2),
            "current_value": round(current_value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 1),
            "days_remaining": days_remaining,
            "end_date": end_date if end_date and end_date != "N/A" else None,
            "event_slug": slug,
            "token_ids": price_data.get("token_ids"),
            "_aggregated_from": rec.get("_aggregated_from", 1),
        })

    # Step 8: Compute summary
    valid = [p for p in positions if p.get("pnl") is not None]
    total_invested = sum(p["position_usd"] for p in valid)
    total_current = sum(p["current_value"] for p in valid)
    total_pnl = sum(p["pnl"] for p in valid)
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested else 0

    return {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "paper",
        "total_positions": len(positions),
        "summary": {
            "total_invested": round(total_invested, 2),
            "total_current_value": round(total_current, 2),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": round(total_pnl_pct, 1),
        },
        "positions": positions,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Wallet mode
# ---------------------------------------------------------------------------

def fetch_wallet_positions(address: str) -> list[dict] | None:
    """
    Fetch wallet positions from the Polymarket Data API.
    GET {DATA_API}/positions?user={address}
    """
    url = f"{DATA_API}/positions?user={address}"
    print(f"[INFO] Fetching wallet positions for {address[:10]}...", file=sys.stderr)
    data = fetch_with_retry(url)
    if data is None:
        print("[ERROR] Failed to fetch wallet positions", file=sys.stderr)
        return None
    # data may be a list of position objects
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "positions" in data:
        return data["positions"]
    return data if isinstance(data, list) else []


def enrich_wallet_positions(raw_positions: list[dict]) -> dict:
    """
    Enrich raw wallet positions with event data, midpoints, days remaining.
    """
    errors = []
    positions = []

    # Group by condition_id to avoid duplicate event fetches
    event_cache = {}

    for pos in raw_positions:
        # Parse raw position fields (Data API format varies)
        condition_id = pos.get("market", pos.get("conditionId", ""))
        token_id = pos.get("asset", pos.get("tokenId", pos.get("asset_id", "")))
        size = float(pos.get("size", pos.get("shares", 0)))
        avg_price = float(pos.get("avgPrice", pos.get("avg_price", 0)))
        side = pos.get("side", pos.get("outcome", ""))  # "Yes" or "No"

        if size <= 0:
            continue

        direction = f"Buy {side}" if side in ("Yes", "No") else "Buy Yes"
        entry_price = avg_price if avg_price > 0 else None
        position_usd = size * avg_price if avg_price > 0 else None

        # Fetch midpoint
        current_price = fetch_midpoint(token_id) if token_id else None
        time.sleep(0.2)

        # Try to get event data for enrichment
        event_slug = pos.get("event_slug", pos.get("eventSlug"))
        market_slug = pos.get("slug", pos.get("market_slug", ""))
        question = pos.get("question", pos.get("title", ""))
        end_date = pos.get("endDate", pos.get("end_date", ""))

        # Compute values
        shares = size
        current_value = shares * current_price if current_price else None
        pnl = (current_value - position_usd) if (current_value and position_usd) else None
        pnl_pct = (pnl / position_usd * 100) if (pnl is not None and position_usd) else None

        # Days remaining
        days_remaining = None
        if end_date:
            try:
                end_dt = datetime.strptime(end_date[:10], "%Y-%m-%d")
                now = datetime.now(timezone.utc).replace(tzinfo=None)
                days_remaining = max(0, (end_dt - now).days)
            except ValueError:
                pass

        p = {
            "market": question or condition_id,
            "direction": direction,
            "entry_price": round(entry_price, 4) if entry_price else None,
            "current_price": round(current_price, 4) if current_price else None,
            "shares": round(shares, 2),
            "position_usd": round(position_usd, 2) if position_usd else None,
            "current_value": round(current_value, 2) if current_value else None,
            "pnl": round(pnl, 2) if pnl is not None else None,
            "pnl_pct": round(pnl_pct, 1) if pnl_pct is not None else None,
            "days_remaining": days_remaining,
            "end_date": end_date[:10] if end_date else None,
            "event_slug": event_slug,
            "token_ids": {"asset": token_id},
            "_aggregated_from": 1,
        }

        if current_price is None:
            p["error"] = "could not fetch current price"
            errors.append(f"No price for: {question or condition_id}")

        positions.append(p)

    # Summary
    valid = [p for p in positions if p.get("pnl") is not None]
    total_invested = sum(p["position_usd"] for p in valid if p["position_usd"])
    total_current = sum(p["current_value"] for p in valid if p["current_value"])
    total_pnl = sum(p["pnl"] for p in valid)
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested else 0

    return {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "wallet",
        "total_positions": len(positions),
        "summary": {
            "total_invested": round(total_invested, 2),
            "total_current_value": round(total_current, 2),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": round(total_pnl_pct, 1),
        },
        "positions": positions,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Polymarket portfolio positions for review",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Paper portfolio from recommendation history (latest 9 open positions):
  python3 fetch_portfolio.py --from-history ~/polymarket-reports/recommendation-history.md --latest 9

  # Real wallet positions:
  python3 fetch_portfolio.py --address 0xYourWalletAddress

  # Paper portfolio, all open positions:
  python3 fetch_portfolio.py --from-history ~/polymarket-reports/recommendation-history.md
        """)

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--address",
        type=str,
        help="Wallet address (0x...) to fetch real positions via Data API")
    mode_group.add_argument(
        "--from-history",
        type=str,
        help="Path to recommendation-history.md for paper portfolio mode")

    parser.add_argument(
        "--latest",
        type=int,
        default=None,
        help="Only use the latest N open recommendations (paper mode only)")
    parser.add_argument(
        "--reports-dir",
        type=str,
        default=str(Path.home() / "polymarket-reports"),
        help="Directory containing market-pulse-*.md reports (default: ~/polymarket-reports)")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (default: stdout)")

    args = parser.parse_args()

    # Dispatch to the right mode
    if args.address:
        # Wallet mode
        raw_positions = fetch_wallet_positions(args.address)
        if raw_positions is None:
            print("[ERROR] Could not fetch wallet positions", file=sys.stderr)
            sys.exit(1)
        if not raw_positions:
            print("[WARN] No positions found for this wallet", file=sys.stderr)
        result = enrich_wallet_positions(raw_positions)
    else:
        # Paper portfolio mode
        history_path = Path(args.from_history).expanduser()
        reports_dir = Path(args.reports_dir).expanduser()

        if not history_path.exists():
            print(f"[ERROR] History file not found: {history_path}", file=sys.stderr)
            sys.exit(1)

        result = build_paper_positions(
            history_path=history_path,
            reports_dir=reports_dir,
            latest_n=args.latest,
        )

    # Output
    json_str = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        out_path = Path(args.output).expanduser()
        out_path.write_text(json_str, encoding="utf-8")
        print(f"[INFO] Output written to {out_path}", file=sys.stderr)
    else:
        print(json_str)

    # Print summary to stderr
    summary = result.get("summary", {})
    print(f"\n[SUMMARY]", file=sys.stderr)
    print(f"  Mode: {result.get('mode', 'unknown')}", file=sys.stderr)
    print(f"  Positions: {result.get('total_positions', 0)}", file=sys.stderr)
    print(f"  Total Invested: ${summary.get('total_invested', 0):,.2f}", file=sys.stderr)
    print(f"  Total Current Value: ${summary.get('total_current_value', 0):,.2f}",
          file=sys.stderr)
    print(f"  Total P&L: ${summary.get('total_pnl', 0):,.2f} "
          f"({summary.get('total_pnl_pct', 0)}%)", file=sys.stderr)
    if result.get("errors"):
        print(f"  Errors ({len(result['errors'])}):", file=sys.stderr)
        for err in result["errors"]:
            print(f"    - {err}", file=sys.stderr)


if __name__ == "__main__":
    main()
