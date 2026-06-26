#!/usr/bin/env python3
"""
Backtest Polymarket recommendation history.

Reads recommendation-history.md, scans pulse reports for event slugs,
fetches current market prices from Polymarket APIs, computes P&L for
each historical recommendation, and outputs structured JSON.

Usage:
    python3 backtest.py
    python3 backtest.py --history ~/polymarket-reports/recommendation-history.md
    python3 backtest.py --output backtest-results.json
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
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "polymarket-backtest/1.0",
}


# ---------------------------------------------------------------------------
# HTTP helpers
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
# History parsing
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
        # Skip header and separator rows
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
            entry_price_str = cells[4]  # e.g. "29.0%" or "N/A"
            entry_price = None
            if entry_price_str != "N/A":
                entry_price = float(entry_price_str.replace("%", "")) / 100.0

            ai_prob_str = cells[5]
            ai_prob = None
            if ai_prob_str != "N/A":
                ai_prob = float(ai_prob_str.replace("%", ""))

            edge_str = cells[6]  # e.g. "+27.0%"
            edge = None
            if edge_str != "N/A":
                edge = float(edge_str.replace("%", "").replace("+", ""))

            position_str = cells[9]  # e.g. "$550" or "N/A"
            position_usd = None
            if position_str != "N/A":
                position_usd = float(position_str.replace("$", "").replace(",", ""))

            records.append({
                "date": cells[0],
                "market": cells[1],
                "link": cells[2],            # polymarket event URL
                "direction": cells[3],       # "Buy Yes" or "Buy No"
                "entry_price": entry_price,  # decimal (0.29)
                "ai_prob": ai_prob,          # percentage (55.5)
                "edge": edge,                # percentage (27.0)
                "position_usd": position_usd,
                "end_date": cells[11] if len(cells) > 11 else None,
                "status": cells[12] if len(cells) > 12 else "Open",
            })
        except (ValueError, IndexError) as e:
            print(f"[WARN] Skipping malformed row: {line[:80]}... ({e})", file=sys.stderr)

    return records


# ---------------------------------------------------------------------------
# Pulse report scanning — extract event slugs
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

            # Gather title context from surrounding lines (look backwards for ## header)
            title_context = ""
            for j in range(max(0, i - 10), i):
                header_match = re.match(r"^##\s+\d+\.\s+(.+)", lines[j])
                if header_match:
                    title_context = header_match.group(1).strip()
                # Also check the old format "推荐 N: Title"
                rec_match = re.match(r"^##\s+推荐\s+\d+:\s+(.+)", lines[j])
                if rec_match:
                    title_context = rec_match.group(1).strip()

            slug_entries.append({
                "slug": slug,
                "title_context": title_context,
                "source_file": report_path.name,
            })

    return slug_entries


def normalize_text(text: str) -> str:
    """Normalize text for fuzzy matching: lowercase, strip punctuation, collapse spaces."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def match_record_to_slug(record: dict, slug_entries: list[dict],
                         event_cache: dict) -> str | None:
    """
    Match a history record (with truncated market name) to an event slug.

    Strategy (in priority order):
    1. Match against full market questions from the Gamma API (most reliable)
    2. Match against slug text converted to words
    3. Match against pulse report title contexts (may be in Chinese)
    """
    market_name = record["market"]
    # The history truncates to ~50 chars; some end with "..."
    market_clean = market_name.rstrip(".")
    market_norm = normalize_text(market_clean)
    market_words = set(market_norm.split())

    # === Strategy 1: Match against API market questions ===
    best_slug = None
    best_score = 0.0

    for slug, event_data in event_cache.items():
        if not event_data:
            continue
        markets = event_data.get("markets", [])
        for mkt in markets:
            question = mkt.get("question", "")
            question_norm = normalize_text(question)
            question_words = set(question_norm.split())

            # Exact substring match (highest confidence)
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

            # Word overlap — use Jaccard-like score weighted by word count
            if not market_words or not question_words:
                continue
            overlap = market_words & question_words
            # Require significant overlap
            overlap_ratio = len(overlap) / min(len(market_words), len(question_words))
            if overlap_ratio >= 0.5 and len(overlap) >= 3:
                score = 50 + len(overlap) + overlap_ratio * 10
                if score > best_score:
                    best_score = score
                    best_slug = slug

    if best_slug and best_score >= 50:
        return best_slug

    # === Strategy 2: Match against slug text ===
    for entry in slug_entries:
        slug = entry["slug"]
        slug_text = slug.replace("-", " ")
        slug_norm = normalize_text(slug_text)
        slug_words = set(slug_norm.split())
        # Remove numeric-only words from slug (they're often random IDs)
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

    # === Strategy 3: Match against pulse report title contexts ===
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
# Price fetching & P&L
# ---------------------------------------------------------------------------

def _parse_iso_datetime(s: str) -> datetime | None:
    """Parse ISO 8601 timestamp (e.g. '2025-02-07T12:00:00Z')."""
    if not s:
        return None
    try:
        s = s.replace("Z", "+00:00")
        return datetime.fromisoformat(s).replace(tzinfo=None)
    except (ValueError, TypeError):
        return None


def _parse_outcome_prices(market: dict) -> list[float]:
    """Parse outcomePrices field from a market dict."""
    raw = market.get("outcomePrices", "")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return []
    prices = []
    for p in raw:
        try:
            prices.append(float(p))
        except (ValueError, TypeError):
            prices.append(0.0)
    return prices


def _is_resolved_at_extreme(prices: list[float]) -> bool:
    """Check if outcome prices indicate a resolved market (>0.95 or <0.05)."""
    if not prices:
        return False
    return max(prices) >= 0.95 or min(prices) <= 0.05


def _select_best_market(markets: list[dict], market_hint: str,
                        rec_date: datetime | None,
                        entry_price: float | None,
                        direction: str) -> dict:
    """
    Three-layer validation to select the best sub-market.

    Layer 1: Text matching (existing logic)
    Layer 2: Temporal validation (core fix — penalize pre-resolved markets)
    Layer 3: Entry price consistency
    """
    if not markets:
        return {}

    if len(markets) == 1:
        return markets[0]

    hint_norm = normalize_text(market_hint) if market_hint else ""
    hint_words = set(hint_norm.split()) if hint_norm else set()

    scored: list[tuple[int, dict]] = []
    for m in markets:
        score = 0
        q_norm = normalize_text(m.get("question", ""))
        q_words = set(q_norm.split())
        market_id = m.get("id", "?")

        # --- Layer 1: Text matching ---
        if hint_norm and q_norm:
            if hint_norm in q_norm or q_norm in hint_norm:
                score += 999
            else:
                overlap = len(hint_words & q_words)
                if overlap >= 2:
                    score += overlap * 10

        # --- Layer 2: Temporal validation ---
        if rec_date is not None:
            created_at = _parse_iso_datetime(m.get("createdAt", ""))
            updated_at = _parse_iso_datetime(m.get("updatedAt", ""))
            closed = m.get("closed", False)

            if created_at and created_at > rec_date:
                # Market didn't exist at recommendation time
                print(f"[DEBUG] Skipping market {market_id}: "
                      f"createdAt {created_at} > rec_date {rec_date}",
                      file=sys.stderr)
                score -= 2000
            elif closed:
                if updated_at and updated_at < rec_date:
                    # Resolved BEFORE the recommendation was made
                    print(f"[DEBUG] Penalizing market {market_id}: "
                          f"closed, updatedAt {updated_at} < rec_date {rec_date}",
                          file=sys.stderr)
                    score -= 1000
                else:
                    # Resolved AFTER recommendation — acceptable
                    score += 50
            else:
                # Still open
                score += 100

        # --- Layer 3: Entry price consistency ---
        outcome_prices = _parse_outcome_prices(m)
        if entry_price is not None and outcome_prices:
            if _is_resolved_at_extreme(outcome_prices):
                if direction == "Buy Yes":
                    settled_price = outcome_prices[0]
                else:
                    settled_price = (outcome_prices[1]
                                     if len(outcome_prices) > 1
                                     else 1.0 - outcome_prices[0])
                if abs(entry_price - settled_price) > 0.30:
                    score -= 500
            else:
                score += 5

        scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_market = scored[0]

    if len(scored) > 1:
        print(f"[DEBUG] Market selection scores: "
              f"{[(s, m.get('id', '?')) for s, m in scored]}",
              file=sys.stderr)

    return best_market


def get_price_data(event_data: dict, direction: str,
                   market_hint: str = "",
                   rec_date_str: str = "",
                   entry_price: float | None = None) -> dict:
    """
    Extract current price data for a position from event data.
    Returns {yes_price, no_price, closed, outcome_prices, question, token_ids}.
    """
    if not event_data:
        return {"error": "no event data"}

    markets = event_data.get("markets", [])
    if not markets:
        return {"error": "no markets in event"}

    # Parse recommendation date for temporal validation
    rec_date = None
    if rec_date_str:
        try:
            rec_date = datetime.strptime(rec_date_str.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                rec_date = datetime.strptime(rec_date_str.strip(), "%Y-%m-%d")
            except ValueError:
                pass

    # Select best market using three-layer validation
    market = _select_best_market(markets, market_hint, rec_date,
                                 entry_price, direction)

    # Parse CLOB token IDs
    ids_raw = market.get("clobTokenIds", "")
    if isinstance(ids_raw, str):
        try:
            ids_raw = json.loads(ids_raw)
        except (json.JSONDecodeError, TypeError):
            ids_raw = []

    yes_token = ids_raw[0] if len(ids_raw) >= 1 else None
    no_token = ids_raw[1] if len(ids_raw) >= 2 else None

    # Parse outcome prices from Gamma API (fallback if midpoint fails)
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

    # Fetch midpoint for the relevant token
    yes_mid = None
    no_mid = None
    if not closed:
        # Only fetch midpoints for open markets
        if direction == "Buy Yes" and yes_token:
            yes_mid = fetch_midpoint(yes_token)
            if yes_mid is not None:
                no_mid = 1.0 - yes_mid
        elif direction == "Buy No" and no_token:
            no_mid = fetch_midpoint(no_token)
            if no_mid is not None:
                yes_mid = 1.0 - no_mid
        # Fallback: try the other token
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
    }


def compute_pnl(record: dict, price_data: dict) -> dict:
    """Compute P&L for a single recommendation."""
    direction = record["direction"]
    entry_price = record["entry_price"]
    position_usd = record["position_usd"]

    if entry_price is None or position_usd is None:
        return {
            **record,
            "current_price": None,
            "shares": None,
            "current_value": None,
            "pnl": None,
            "pnl_pct": None,
            "resolved_status": "error",
            "error": "missing entry_price or position_usd",
        }

    if "error" in price_data:
        return {
            **record,
            "current_price": None,
            "shares": None,
            "current_value": None,
            "pnl": None,
            "pnl_pct": None,
            "resolved_status": "unmatched",
            "error": price_data["error"],
        }

    # Determine current price based on direction
    if direction == "Buy Yes":
        current_price = price_data.get("yes_price")
    else:  # Buy No
        current_price = price_data.get("no_price")

    if current_price is None:
        return {
            **record,
            "current_price": None,
            "shares": None,
            "current_value": None,
            "pnl": None,
            "pnl_pct": None,
            "resolved_status": "no_price",
            "error": "could not fetch current price",
        }

    shares = position_usd / entry_price
    closed = price_data.get("closed", False)

    if closed:
        # Market is settled
        outcome_prices = price_data.get("outcome_prices", [])
        if outcome_prices and (max(outcome_prices) >= 0.95 or min(outcome_prices) <= 0.05):
            # Determine winner
            yes_final = outcome_prices[0] if outcome_prices else 0
            if direction == "Buy Yes":
                exit_price = 1.0 if yes_final >= 0.95 else 0.0
            else:  # Buy No
                exit_price = 1.0 if yes_final <= 0.05 else 0.0

            current_value = shares * exit_price
            pnl = current_value - position_usd
            pnl_pct = (pnl / position_usd) * 100 if position_usd else 0

            won = exit_price >= 0.95
            return {
                **record,
                "current_price": exit_price,
                "shares": round(shares, 2),
                "current_value": round(current_value, 2),
                "pnl": round(pnl, 2),
                "pnl_pct": round(pnl_pct, 1),
                "resolved_status": "won" if won else "lost",
                "question": price_data.get("question", ""),
            }
        # Closed but prices not extreme — treat as settled at current prices
        current_value = shares * current_price
        pnl = current_value - position_usd
        pnl_pct = (pnl / position_usd) * 100 if position_usd else 0
        return {
            **record,
            "current_price": round(current_price, 4),
            "shares": round(shares, 2),
            "current_value": round(current_value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 1),
            "resolved_status": "closed",
            "question": price_data.get("question", ""),
        }

    # Open market — unrealized P&L
    current_value = shares * current_price
    pnl = current_value - position_usd
    pnl_pct = (pnl / position_usd) * 100 if position_usd else 0

    return {
        **record,
        "current_price": round(current_price, 4),
        "shares": round(shares, 2),
        "current_value": round(current_value, 2),
        "pnl": round(pnl, 2),
        "pnl_pct": round(pnl_pct, 1),
        "resolved_status": "open",
        "question": price_data.get("question", ""),
    }


# ---------------------------------------------------------------------------
# Categorization & aggregation
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS = {
    "crypto": ["bitcoin", "btc", "crypto", "ethereum", "eth", "coin", "token",
               "defi", "nft", "solana", "doge"],
    "geopolitics": ["iran", "russia", "ukraine", "ceasefire", "war", "strike",
                    "khamenei", "putin", "zelenskyy", "regime", "supreme leader",
                    "sanctions"],
    "sports": ["arsenal", "premier league", "nba", "nfl", "champion", "world cup",
               "tournament", "football", "soccer", "playoffs"],
    "tech": ["apple", "ai model", "anthropic", "openai", "google", "microsoft",
             "product line", "release", "launch"],
    "politics": ["gop", "republican", "democrat", "house", "senate", "midterm",
                 "election", "congress", "president", "vote"],
    "science": ["alien", "ufo", "space", "nasa", "climate", "pandemic"],
}


def categorize_market(market_name: str) -> str:
    """Categorize a market by keyword matching."""
    name_lower = market_name.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in name_lower)
        if score > 0:
            scores[category] = score
    if not scores:
        return "other"
    return max(scores, key=scores.get)


def compute_days_held(date_str: str) -> int:
    """Compute days from recommendation date to now."""
    try:
        rec_date = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return max(0, (now - rec_date).days)
    except ValueError:
        return 0


def aggregate_stats(results: list[dict]) -> dict:
    """Compute summary statistics from P&L results."""
    valid = [r for r in results if r.get("pnl") is not None]

    total_invested = sum(r["position_usd"] for r in valid)
    total_current = sum(r["current_value"] for r in valid)
    total_pnl = sum(r["pnl"] for r in valid)
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested else 0

    settled = [r for r in valid if r["resolved_status"] in ("won", "lost")]
    wins = [r for r in settled if r["resolved_status"] == "won"]
    losses = [r for r in settled if r["resolved_status"] == "lost"]
    open_positions = [r for r in valid if r["resolved_status"] == "open"]

    realized_pnl = sum(r["pnl"] for r in settled)
    unrealized_pnl = sum(r["pnl"] for r in open_positions)

    win_rate = (len(wins) / len(settled) * 100) if settled else None

    best = max(valid, key=lambda r: r["pnl"]) if valid else None
    worst = min(valid, key=lambda r: r["pnl"]) if valid else None

    edges = [r["edge"] for r in valid if r.get("edge") is not None]
    returns = [r["pnl_pct"] for r in valid if r.get("pnl_pct") is not None]
    avg_edge = sum(edges) / len(edges) if edges else None
    avg_return = sum(returns) / len(returns) if returns else None

    # By category
    by_category = {}
    for r in valid:
        cat = r.get("category", "other")
        if cat not in by_category:
            by_category[cat] = {"count": 0, "invested": 0, "pnl": 0}
        by_category[cat]["count"] += 1
        by_category[cat]["invested"] += r["position_usd"]
        by_category[cat]["pnl"] += r["pnl"]
    for cat in by_category:
        inv = by_category[cat]["invested"]
        by_category[cat]["pnl_pct"] = round(
            by_category[cat]["pnl"] / inv * 100, 1) if inv else 0
        by_category[cat]["invested"] = round(by_category[cat]["invested"], 2)
        by_category[cat]["pnl"] = round(by_category[cat]["pnl"], 2)

    # By direction
    by_direction = {}
    for r in valid:
        d = r["direction"]
        if d not in by_direction:
            by_direction[d] = {"count": 0, "invested": 0, "pnl": 0}
        by_direction[d]["count"] += 1
        by_direction[d]["invested"] += r["position_usd"]
        by_direction[d]["pnl"] += r["pnl"]
    for d in by_direction:
        inv = by_direction[d]["invested"]
        by_direction[d]["pnl_pct"] = round(
            by_direction[d]["pnl"] / inv * 100, 1) if inv else 0
        by_direction[d]["invested"] = round(by_direction[d]["invested"], 2)
        by_direction[d]["pnl"] = round(by_direction[d]["pnl"], 2)

    return {
        "total_recommendations": len(results),
        "matched": len(valid),
        "unmatched": len(results) - len(valid),
        "total_invested": round(total_invested, 2),
        "total_current_value": round(total_current, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_pct": round(total_pnl_pct, 1),
        "realized_pnl": round(realized_pnl, 2),
        "unrealized_pnl": round(unrealized_pnl, 2),
        "settled_count": len(settled),
        "open_count": len(open_positions),
        "win_count": len(wins),
        "loss_count": len(losses),
        "win_rate": round(win_rate, 1) if win_rate is not None else None,
        "best_trade": {
            "market": best["market"],
            "pnl": best["pnl"],
            "pnl_pct": best["pnl_pct"],
        } if best else None,
        "worst_trade": {
            "market": worst["market"],
            "pnl": worst["pnl"],
            "pnl_pct": worst["pnl_pct"],
        } if worst else None,
        "avg_edge": round(avg_edge, 1) if avg_edge is not None else None,
        "avg_actual_return": round(avg_return, 1) if avg_return is not None else None,
        "by_category": by_category,
        "by_direction": by_direction,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Backtest Polymarket recommendation history")
    parser.add_argument(
        "--history",
        default=str(Path.home() / "polymarket-reports" / "recommendation-history.md"),
        help="Path to recommendation-history.md")
    parser.add_argument(
        "--reports-dir",
        default=str(Path.home() / "polymarket-reports"),
        help="Directory containing market-pulse-*.md reports")
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output file (default: stdout)")
    parser.add_argument(
        "--flat", type=float, default=None,
        help="Use flat (equal) position sizing: override every position with this USD amount (e.g. --flat 100)")
    args = parser.parse_args()

    history_path = Path(args.history).expanduser()
    reports_dir = Path(args.reports_dir).expanduser()

    if not history_path.exists():
        print(f"[ERROR] History file not found: {history_path}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Parse history
    print("[INFO] Parsing recommendation history...", file=sys.stderr)
    records = parse_history(history_path)
    print(f"[INFO] Found {len(records)} recommendations", file=sys.stderr)

    # Apply flat position sizing if requested
    if args.flat is not None:
        flat_amt = args.flat
        print(f"[INFO] Flat mode: overriding all positions to ${flat_amt:.2f}", file=sys.stderr)
        for rec in records:
            rec["position_usd"] = flat_amt

    # Step 2: Scan pulse reports for slugs
    print("[INFO] Scanning pulse reports for event slugs...", file=sys.stderr)
    slug_entries = scan_pulse_reports(reports_dir)
    print(f"[INFO] Found {len(slug_entries)} slug references in reports", file=sys.stderr)

    # Step 3: Fetch event data for all unique slugs
    unique_slugs = list({e["slug"] for e in slug_entries})
    print(f"[INFO] Fetching data for {len(unique_slugs)} unique events...", file=sys.stderr)

    event_cache = {}
    failed_slugs = []
    for i, slug in enumerate(unique_slugs):
        print(f"[INFO]   ({i + 1}/{len(unique_slugs)}) {slug}", file=sys.stderr)
        data = fetch_event_data(slug)
        if data:
            event_cache[slug] = data
        else:
            failed_slugs.append(slug)
            # Try truncated slug (remove trailing numeric IDs)
            parts = slug.split("-")
            # Remove trailing parts that are purely numeric
            while parts and parts[-1].isdigit():
                parts.pop()
            short_slug = "-".join(parts)
            if short_slug and short_slug != slug:
                print(f"[INFO]     Retrying with truncated slug: {short_slug}", file=sys.stderr)
                data = fetch_event_data(short_slug)
                if data:
                    event_cache[slug] = data
                    event_cache[short_slug] = data
        time.sleep(0.3)

    if failed_slugs:
        still_missing = [s for s in failed_slugs if s not in event_cache]
        if still_missing:
            print(f"[WARN] {len(still_missing)} slugs could not be fetched", file=sys.stderr)

    # Step 4: Match records to slugs & compute P&L
    print("[INFO] Matching records and computing P&L...", file=sys.stderr)
    results = []
    unmatched_names = []

    for record in records:
        slug = match_record_to_slug(record, slug_entries, event_cache)
        record["category"] = categorize_market(record["market"])
        record["days_held"] = compute_days_held(record["date"])

        if slug:
            record["event_slug"] = slug
            record["link"] = f"https://polymarket.com/event/{slug}"
            event_data = event_cache.get(slug)

            # Fetch price data (with midpoint call)
            price_data = get_price_data(event_data, record["direction"],
                                        market_hint=record["market"],
                                        rec_date_str=record["date"],
                                        entry_price=record["entry_price"])
            result = compute_pnl(record, price_data)
            time.sleep(0.2)
        else:
            record["event_slug"] = None
            result = {
                **record,
                "current_price": None,
                "shares": None,
                "current_value": None,
                "pnl": None,
                "pnl_pct": None,
                "resolved_status": "unmatched",
                "error": "could not match to event slug",
            }
            unmatched_names.append(record["market"])

        results.append(result)

    # Step 5: Aggregate
    print("[INFO] Computing aggregate statistics...", file=sys.stderr)
    summary = aggregate_stats(results)

    output = {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "sizing": f"flat ${args.flat:.2f}" if args.flat else "variable",
        "summary": summary,
        "positions": results,
        "unmatched": unmatched_names,
    }

    json_str = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        out_path = Path(args.output).expanduser()
        out_path.write_text(json_str, encoding="utf-8")
        print(f"[INFO] Output written to {out_path}", file=sys.stderr)
    else:
        print(json_str)

    # Print summary to stderr
    print(f"\n[SUMMARY]", file=sys.stderr)
    print(f"  Matched: {summary['matched']}/{summary['total_recommendations']}", file=sys.stderr)
    print(f"  Total Invested: ${summary['total_invested']:,.2f}", file=sys.stderr)
    print(f"  Total P&L: ${summary['total_pnl']:,.2f} ({summary['total_pnl_pct']}%)", file=sys.stderr)
    if summary['win_rate'] is not None:
        print(f"  Win Rate: {summary['win_rate']}%", file=sys.stderr)
    if unmatched_names:
        print(f"  Unmatched markets:", file=sys.stderr)
        for name in unmatched_names:
            print(f"    - {name}", file=sys.stderr)


if __name__ == "__main__":
    main()
