#!/usr/bin/env python3
"""
Continuous terminal monitor for Polymarket resolution tracking.

Fetches event data and resolution source data on a schedule, compares states,
and outputs color-coded alerts to the terminal.

Usage:
    python monitor.py --slug <event_slug> [--interval <minutes>] [--state-dir <path>]
    python monitor.py --slug which-company-has-the-best-ai-model-end-of-february --interval 60
    python monitor.py --slug which-company-has-the-best-ai-model-end-of-february --once
"""

import argparse
import json
import os
import re
import signal
import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_event import fetch_event, extract_slug
from scrape_source import scrape_source


# ---------------------------------------------------------------------------
# Default arena URL (fallback if detection fails)
# ---------------------------------------------------------------------------

ARENA_URL_DEFAULT = "https://arena.ai/leaderboard/text/overall-no-style-control"


# ---------------------------------------------------------------------------
# ANSI color codes
# ---------------------------------------------------------------------------

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    DIM = "\033[2m"
    MAGENTA = "\033[95m"


# ---------------------------------------------------------------------------
# Alert system
# ---------------------------------------------------------------------------

class AlertHandler(ABC):
    """Base class for alert handlers.

    Subclass and implement handle() to receive alerts.
    Alert dict structure:
        {
            "type": "CRITICAL" | "WARNING" | "INFO" | "ALERT",
            "message": str,
            "data": dict,
            "timestamp": str (ISO format)
        }
    """

    @abstractmethod
    def handle(self, alert: dict) -> None:
        ...


class ConsoleAlertHandler(AlertHandler):
    """Print alerts to terminal with color coding."""

    TYPE_STYLES = {
        "CRITICAL": (Colors.RED + Colors.BOLD, "CRITICAL"),
        "WARNING": (Colors.YELLOW, "WARNING"),
        "INFO": (Colors.DIM, "INFO"),
        "ALERT": (Colors.MAGENTA + Colors.BOLD, "ALERT"),
    }

    def handle(self, alert: dict) -> None:
        alert_type = alert.get("type", "INFO")
        style, label = self.TYPE_STYLES.get(alert_type, (Colors.RESET, alert_type))
        ts = alert.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts)
            time_str = dt.strftime("%H:%M")
        except (ValueError, TypeError):
            time_str = ts[:5] if ts else "??:??"

        msg = alert.get("message", "")
        print(f"{style}[{time_str}] {label}: {msg}{Colors.RESET}")


class FileAlertHandler(AlertHandler):
    """Write alerts as JSON lines to a log file."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        os.makedirs(os.path.dirname(os.path.abspath(log_path)) or ".", exist_ok=True)

    def handle(self, alert: dict) -> None:
        line = json.dumps(alert, ensure_ascii=False) + "\n"
        with open(self.log_path, "a") as f:
            f.write(line)


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state(state_dir: str, slug: str) -> dict | None:
    """Load previous monitoring state from disk."""
    state_file = os.path.join(state_dir, f"{slug}-state.json")
    if os.path.exists(state_file):
        with open(state_file) as f:
            return json.load(f)
    return None


def save_state(state_dir: str, slug: str, state: dict) -> None:
    """Save current state to disk (both latest and timestamped snapshot)."""
    os.makedirs(state_dir, exist_ok=True)

    state_file = os.path.join(state_dir, f"{slug}-state.json")
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    snapshot_file = os.path.join(state_dir, f"{slug}-{ts}.json")
    with open(snapshot_file, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Candidate name extraction from sub-market questions
# ---------------------------------------------------------------------------

def extract_candidate_name(question: str) -> str:
    """Extract candidate name from a sub-market question.

    Handles patterns like:
    - "Will Anthropic have the best AI model at the end of February 2026?"
    - "Will Google win?"
    - "Anthropic?"
    """
    # Pattern: "Will X have the best..."
    m = re.match(r'^Will\s+(.+?)\s+have\s+the\s+best\b', question, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Pattern: "Will X win..." / "Will X be..."
    m = re.match(r'^Will\s+(.+?)\s+(?:win|be|become|reach|get)\b', question, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Fallback: strip trailing "?" and common suffixes
    candidate = question.rstrip("?").strip()
    for suffix in [" at the end of ", " by end of ", " in "]:
        idx = candidate.lower().find(suffix)
        if idx > 0:
            candidate = candidate[:idx].strip()
    return candidate


def build_market_prices(event_data: dict) -> dict:
    """Extract candidate -> price mapping from event data."""
    prices = {}
    for market in event_data.get("markets", []):
        question = market.get("question", "")
        outcome_prices = market.get("outcome_prices", [])

        if len(outcome_prices) >= 1:
            candidate = extract_candidate_name(question)
            yes_price = outcome_prices[0]
            prices[candidate] = yes_price

    return prices


# ---------------------------------------------------------------------------
# Resolution source detection
# ---------------------------------------------------------------------------

def detect_resolution_source(event_data: dict) -> dict:
    """Detect the resolution data source from event description.

    Returns: {"type": str, "url": str, "metric": str}
    """
    description = event_data.get("description", "")
    desc_lower = description.lower()

    # Check for arena.ai / lmarena.ai leaderboard
    if any(kw in desc_lower for kw in ["arena.ai", "lmarena.ai", "lmsys", "chatbot arena"]):
        url_matches = re.findall(r'(https?://[^\s<>"()]+(?:arena|lmarena)[^\s<>"()]*)', description)
        url = ARENA_URL_DEFAULT
        if url_matches:
            url = max(url_matches, key=len).rstrip(".,;)")
        return {
            "type": "arena_leaderboard",
            "url": url,
            "metric": "Arena Score (Elo)",
        }

    # Generic URL extraction
    urls = re.findall(r'https?://[^\s<>"]+', description)
    if urls:
        return {
            "type": "generic_url",
            "url": urls[0],
            "metric": "unknown",
        }

    return {
        "type": "unknown",
        "url": "",
        "metric": "unknown",
    }


def fetch_resolution_data(source: dict) -> dict:
    """Fetch resolution data based on the detected source type."""
    source_type = source.get("type", "unknown")
    url = source.get("url", "")

    if source_type == "arena_leaderboard":
        return scrape_source(url, "arena_leaderboard")
    elif source_type == "generic_url" and url:
        return scrape_source(url, "generic")
    else:
        return {
            "success": False,
            "error": "Cannot determine resolution data source",
            "suggestion": "Manually review the market description for resolution criteria",
        }


# ---------------------------------------------------------------------------
# Comparison & alerting logic
# ---------------------------------------------------------------------------

def compare_states(prev: dict | None, curr: dict, handlers: list[AlertHandler]) -> list[dict]:
    """Compare previous and current state, generate alerts."""
    now_str = datetime.now(timezone.utc).isoformat()
    alerts = []

    def emit(alert_type: str, message: str, data: dict = None):
        alert = {
            "type": alert_type,
            "message": message,
            "data": data or {},
            "timestamp": now_str,
        }
        alerts.append(alert)
        for h in handlers:
            h.handle(alert)

    curr_mapping = curr.get("resolution_data", {}).get("market_mapping", {})
    curr_prices = curr.get("market_prices", {})

    if prev is None:
        # First run — report current state
        if curr_mapping:
            sorted_orgs = sorted(curr_mapping.items(), key=lambda x: x[1]["score"], reverse=True)
            leader = sorted_orgs[0] if sorted_orgs else None
            second = sorted_orgs[1] if len(sorted_orgs) > 1 else None

            if leader and second:
                gap = leader[1]["score"] - second[1]["score"]
                ci_1 = f"+-{leader[1]['ci']}" if leader[1].get('ci') else ""
                ci_2 = f"+-{second[1]['ci']}" if second[1].get('ci') else ""
                emit("INFO",
                     f"#{leader[1]['rank']} {leader[0]} {leader[1]['score']}{ci_1} | "
                     f"#{second[1]['rank']} {second[0]} {second[1]['score']}{ci_2} | "
                     f"Gap: {gap:.0f}",
                     {"leader": leader[0], "second": second[0], "gap": gap})

            if curr_prices:
                price_parts = []
                for org, price in sorted(curr_prices.items(), key=lambda x: x[1], reverse=True)[:3]:
                    price_parts.append(f"{org} {price*100:.1f}%")
                emit("INFO", f"Market: {' | '.join(price_parts)}")

            if leader and curr_prices:
                market_leader = max(curr_prices.items(), key=lambda x: x[1]) if curr_prices else None
                if market_leader and market_leader[0] == leader[0]:
                    emit("INFO", "Status: ALIGNED")
                elif market_leader:
                    emit("ALERT",
                         f"MISALIGNED: Data leader={leader[0]}, Market leader={market_leader[0]}",
                         {"data_leader": leader[0], "market_leader": market_leader[0]})
        return alerts

    # Compare with previous state
    prev_mapping = prev.get("resolution_data", {}).get("market_mapping", {})
    prev_prices = prev.get("market_prices", {})

    if not curr_mapping:
        emit("WARNING", "No resolution data available this cycle")
        return alerts

    # Find leaders
    curr_sorted = sorted(curr_mapping.items(), key=lambda x: x[1]["score"], reverse=True)
    prev_sorted = sorted(prev_mapping.items(), key=lambda x: x[1]["score"], reverse=True) if prev_mapping else []

    curr_leader = curr_sorted[0] if curr_sorted else None
    prev_leader = prev_sorted[0] if prev_sorted else None

    # Check for leader change
    if curr_leader and prev_leader and curr_leader[0] != prev_leader[0]:
        emit("CRITICAL",
             f"Leader changed! {curr_leader[0]} {curr_leader[1]['score']:.0f} > "
             f"{prev_leader[0]} (was {prev_leader[1]['score']:.0f})",
             {"new_leader": curr_leader[0], "old_leader": prev_leader[0]})
    elif curr_leader and len(curr_sorted) > 1:
        curr_second = curr_sorted[1]
        curr_gap = curr_leader[1]["score"] - curr_second[1]["score"]

        prev_gap = None
        if prev_leader and prev_sorted and len(prev_sorted) > 1:
            prev_second = prev_sorted[1]
            prev_gap = prev_leader[1]["score"] - prev_second[1]["score"]

        # Check score changes
        changes = []
        for org, data in curr_mapping.items():
            if org in prev_mapping:
                old_score = prev_mapping[org]["score"]
                new_score = data["score"]
                if old_score != new_score:
                    changes.append((org, old_score, new_score))

        if changes:
            for org, old_s, new_s in changes:
                direction = "up" if new_s > old_s else "down"
                emit("INFO", f"{org} score changed {old_s:.0f} -> {new_s:.0f} ({direction})",
                     {"org": org, "old_score": old_s, "new_score": new_s})

        # Check if gap narrowed
        if prev_gap is not None and curr_gap < prev_gap:
            ci_1 = curr_leader[1].get("ci", 0) or 0
            ci_2 = curr_second[1].get("ci", 0) or 0
            overlap = (ci_1 + ci_2) > curr_gap

            if curr_gap <= 3 or overlap:
                emit("WARNING",
                     f"Gap narrowed to {curr_gap:.0f} (was {prev_gap:.0f}), CI overlap: {overlap}",
                     {"gap": curr_gap, "prev_gap": prev_gap, "ci_overlap": overlap})
            else:
                emit("INFO",
                     f"Gap: {curr_gap:.0f} (was {prev_gap:.0f})",
                     {"gap": curr_gap, "prev_gap": prev_gap})
        elif not changes:
            emit("INFO", "No change.")

    # Check price vs data alignment
    if curr_prices and curr_leader:
        market_leader = max(curr_prices.items(), key=lambda x: x[1]) if curr_prices else None
        if market_leader and market_leader[0] != curr_leader[0]:
            emit("ALERT",
                 f"Market price vs data misalignment: Market favors {market_leader[0]} "
                 f"({market_leader[1]*100:.1f}%), data favors {curr_leader[0]}",
                 {"market_leader": market_leader[0], "data_leader": curr_leader[0]})

    # Check for significant price changes
    if curr_prices and prev_prices:
        for org in curr_prices:
            if org in prev_prices:
                price_change = curr_prices[org] - prev_prices[org]
                if abs(price_change) >= 0.02:
                    emit("WARNING",
                         f"{org} market price changed {prev_prices[org]*100:.1f}% -> {curr_prices[org]*100:.1f}%",
                         {"org": org, "old_price": prev_prices[org], "new_price": curr_prices[org]})

    return alerts


# ---------------------------------------------------------------------------
# Main monitoring loop
# ---------------------------------------------------------------------------

def print_header(event_data: dict, source: dict, interval: int):
    """Print the monitoring header."""
    now = datetime.now(timezone.utc)
    title = event_data.get("title", "Unknown")
    end_date = event_data.get("end_date", "")

    remaining = ""
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            delta = end_dt - now
            if delta.total_seconds() > 0:
                hours = int(delta.total_seconds() // 3600)
                remaining = f" ({hours}h remaining)"
        except (ValueError, TypeError):
            pass

    print(f"\n{Colors.BOLD}{'=' * 58}{Colors.RESET}")
    print(f"{Colors.BOLD}[{now.strftime('%Y-%m-%d %H:%M UTC')}] Resolution Tracker Started{Colors.RESET}")
    print(f"Market: {title}")
    print(f"Source: {source.get('url', 'unknown')}")
    if end_date:
        print(f"Resolution: {end_date}{remaining}")
    print(f"Interval: {interval} min")
    print(f"{Colors.BOLD}{'-' * 58}{Colors.RESET}")


def run_cycle(slug: str, state_dir: str, handlers: list[AlertHandler], source: dict = None) -> dict:
    """Run one monitoring cycle. Returns the current state."""
    # 1. Fetch event data
    try:
        event_data = fetch_event(slug)
    except Exception as e:
        now_str = datetime.now(timezone.utc).isoformat()
        for h in handlers:
            h.handle({"type": "WARNING", "message": f"Failed to fetch event: {e}",
                      "data": {}, "timestamp": now_str})
        return {}

    # 2. Detect and fetch resolution source
    if source is None:
        source = detect_resolution_source(event_data)

    resolution_data = fetch_resolution_data(source)

    # 3. Build market prices mapping
    market_prices = build_market_prices(event_data)

    # 4. Build current state
    current_state = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "event_title": event_data.get("title", ""),
        "market_prices": market_prices,
        "resolution_data": {
            "success": resolution_data.get("success", False),
            "method": resolution_data.get("method", ""),
            "market_mapping": resolution_data.get("market_mapping", {}),
            "models_count": resolution_data.get("models_count", 0),
        },
        "source": source,
    }

    # 5. Load previous state and compare
    prev_state = load_state(state_dir, slug)
    compare_states(prev_state, current_state, handlers)

    # 6. Save state
    save_state(state_dir, slug, current_state)

    return current_state


# Graceful shutdown
_running = True


def _signal_handler(signum, frame):
    global _running
    _running = False
    print(f"\n{Colors.YELLOW}[INFO] Shutting down gracefully...{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Monitor Polymarket resolution data")
    parser.add_argument("--slug", required=True, help="Event slug or Polymarket URL")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in minutes (default: 60)")
    parser.add_argument("--state-dir", default=os.path.expanduser("~/polymarket-tracking"),
                        help="Directory for state files (default: ~/polymarket-tracking/)")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit")
    parser.add_argument("--alert-log", type=str, default=None,
                        help="Also write alerts to this log file")
    args = parser.parse_args()

    slug = extract_slug(args.slug)

    # Set up alert handlers
    handlers: list[AlertHandler] = [ConsoleAlertHandler()]
    if args.alert_log:
        handlers.append(FileAlertHandler(args.alert_log))

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Initial fetch to get event info and detect source
    print(f"[INFO] Initializing tracker for: {slug}", file=sys.stderr)
    try:
        event_data = fetch_event(slug)
    except Exception as e:
        print(f"[ERROR] Failed to fetch event: {e}", file=sys.stderr)
        sys.exit(1)

    source = detect_resolution_source(event_data)

    if args.once:
        print_header(event_data, source, 0)
        state = run_cycle(slug, args.state_dir, handlers, source)
        print(f"{Colors.BOLD}{'-' * 58}{Colors.RESET}")
        if state:
            print(f"{Colors.GREEN}State saved to {args.state_dir}/{slug}-state.json{Colors.RESET}")
        return

    # Continuous monitoring
    print_header(event_data, source, args.interval)

    global _running
    while _running:
        run_cycle(slug, args.state_dir, handlers, source)

        if not _running:
            break

        next_check = datetime.now(timezone.utc) + timedelta(minutes=args.interval)
        print(f"{Colors.DIM}  Next check in {args.interval}min ({next_check.strftime('%H:%M UTC')}){Colors.RESET}")

        # Sleep in small increments for responsive shutdown
        sleep_seconds = args.interval * 60
        for _ in range(sleep_seconds):
            if not _running:
                break
            time.sleep(1)

    print(f"\n{Colors.BOLD}{'=' * 58}{Colors.RESET}")
    print(f"{Colors.GREEN}Monitor stopped. State saved to {args.state_dir}/{Colors.RESET}")


if __name__ == "__main__":
    main()
