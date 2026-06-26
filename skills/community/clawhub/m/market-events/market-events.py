#!/usr/bin/env python3
"""Market Events — upcoming earnings, dividends, and stock splits from FMP."""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

FMP_BASE_URL = "https://financialmodelingprep.com/stable"

ENDPOINT_MAP = {
    "earnings": "earnings-calendar",
    "dividends": "dividends-calendar",
    "splits": "splits-calendar",
}

EVENT_TYPE_ORDER = {"earnings": 0, "dividends": 1, "splits": 2}

ALL_TYPES = ["earnings", "dividends", "splits"]

FMP_PAGE_SIZE = 4000


def _fix_negative_range(argv):
    """Merge '--range -30d' into '--range=-30d' so argparse doesn't treat the value as a flag."""
    fixed = []
    i = 0
    while i < len(argv):
        if argv[i] == "--range" and i + 1 < len(argv):
            fixed.append(f"--range={argv[i + 1]}")
            i += 2
        else:
            fixed.append(argv[i])
            i += 1
    return fixed


def parse_args():
    parser = argparse.ArgumentParser(
        description="Report upcoming or recent earnings, dividends, and stock splits for a watchlist of tickers."
    )
    parser.add_argument("--tickers", help="Comma-separated list of ticker symbols")
    parser.add_argument("--file", help="Path to a .txt or .csv file of tickers")
    parser.add_argument("--range", default="7d", dest="range_str",
                        help="Lookahead/lookback window. Units: d(ays), w(eeks), y(ear). "
                             "Negative = look back. Examples: 7d, 2w, -30d, -1y. Default: 7d. Max: 365d/52w/1y.")
    parser.add_argument("--format", choices=["text", "json", "discord"], default="text",
                        help="Output format: text, json, or discord. Default: text.")
    parser.add_argument("--types", help="Comma-separated event types: earnings,dividends,splits. Default: all.")
    return parser.parse_args(_fix_negative_range(sys.argv[1:]))


def parse_range(range_str):
    """Parse a range string like '7d', '2w', or '-1y' into a signed integer number of days."""
    s = range_str.strip().lower()
    multiplier = 1
    if s.endswith("w"):
        multiplier = 7
        s = s[:-1]
    elif s.endswith("y"):
        multiplier = 365
        s = s[:-1]
    elif s.endswith("d"):
        s = s[:-1]
    try:
        value = int(s)
    except ValueError:
        print(f"Error: Invalid range '{range_str}'. Use a number + unit (e.g. 7d, 2w, -1y).", file=sys.stderr)
        sys.exit(1)
    days = value * multiplier
    if days == 0 or abs(days) > 365:
        print(f"Error: Range must be between 1 and 365 days (got {abs(days)} days).", file=sys.stderr)
        sys.exit(1)
    return days


MAX_API_DAYS = 90


def date_range_chunks(from_date, to_date):
    """Split a date range into chunks of at most MAX_API_DAYS for FMP API limits."""
    chunks = []
    cursor = from_date
    while cursor < to_date:
        chunk_end = min(cursor + timedelta(days=MAX_API_DAYS), to_date)
        chunks.append((cursor, chunk_end))
        cursor = chunk_end
    return chunks


def normalize_symbol(value):
    """Normalize API and user ticker symbols for matching."""
    return str(value or "").strip().upper()


def parse_ticker_file(path):
    """Read tickers from a .txt or .csv file."""
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    tickers = []
    ext = os.path.splitext(path)[1].lower()

    with open(path, "r", encoding="utf-8") as f:
        if ext == ".csv":
            reader = csv.reader(f)
            first = True
            for row in reader:
                if not row or not row[0].strip():
                    continue
                cell = row[0].strip()
                # Skip header: if first row contains lowercase or spaces, treat as header
                if first:
                    first = False
                    if any(c.islower() for c in cell) or " " in cell:
                        continue
                tickers.append(cell.upper())
        else:
            # Plain text
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                tickers.append(line.upper())

    return tickers


def resolve_tickers(args):
    """Build a deduplicated, uppercase set of tickers from --tickers and --file."""
    tickers = set()

    if args.tickers:
        for t in args.tickers.split(","):
            t = t.strip().upper()
            if t:
                tickers.add(t)

    if args.file:
        for t in parse_ticker_file(args.file):
            tickers.add(t)

    if not tickers:
        print("Error: No tickers provided. Use --tickers and/or --file.", file=sys.stderr)
        sys.exit(1)

    return tickers


def fetch_dividends_by_ticker(ticker, from_date, to_date, api_key):
    """Fetch dividends for a single ticker via /stable/dividends and filter by date range."""
    url = f"{FMP_BASE_URL}/dividends"
    params = {"symbol": ticker, "apikey": api_key}

    try:
        resp = requests.get(url, params=params, timeout=30)
    except requests.RequestException as e:
        print(f"Warning: Network error fetching dividends for {ticker}: {e}", file=sys.stderr)
        return []

    if resp.status_code == 401:
        print("Error: Invalid FMP API key (HTTP 401).", file=sys.stderr)
        sys.exit(1)
    elif resp.status_code == 429:
        print(f"Warning: Rate limited fetching dividends for {ticker} (HTTP 429). Skipping.", file=sys.stderr)
        return []
    elif resp.status_code >= 400:
        print(f"Warning: HTTP {resp.status_code} fetching dividends for {ticker}. Skipping.", file=sys.stderr)
        return []

    try:
        events = resp.json()
    except ValueError:
        print(f"Warning: Invalid JSON response for dividends/{ticker}. Skipping.", file=sys.stderr)
        return []

    if not isinstance(events, list):
        return []

    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")
    rows = []
    for ev in events:
        d = ev.get("date", "")
        if from_str <= d <= to_str:
            symbol = normalize_symbol(ev.get("symbol", ticker))
            rows.append({
                "date": d,
                "ticker": symbol,
                "event_type": "dividends",
                "raw": ev,
            })
    return rows


def handle_response_status(resp, context):
    """Return True when a response is usable; otherwise warn or exit."""
    if resp.status_code == 401:
        print("Error: Invalid FMP API key (HTTP 401).", file=sys.stderr)
        sys.exit(1)
    elif resp.status_code == 429:
        print(f"Warning: Rate limited fetching {context} (HTTP 429). Skipping.", file=sys.stderr)
        return False
    elif resp.status_code >= 400:
        print(f"Warning: HTTP {resp.status_code} fetching {context}. Skipping.", file=sys.stderr)
        return False
    return True


def fetch_events(event_type, from_date, to_date, api_key):
    """Fetch events from FMP for a given type and date range."""
    endpoint = ENDPOINT_MAP[event_type]
    url = f"{FMP_BASE_URL}/{endpoint}"
    events = []
    seen = set()
    first_page_full = False

    def add_page(page_events):
        for ev in page_events:
            if not isinstance(ev, dict):
                continue
            key = (
                normalize_symbol(ev.get("symbol")),
                ev.get("date", ""),
                event_type,
                json.dumps(ev, sort_keys=True, default=str),
            )
            if key not in seen:
                seen.add(key)
                events.append(ev)

    # FMP's omitted page and explicit page=0 responses are not always equivalent.
    params = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "apikey": api_key,
    }
    try:
        resp = requests.get(url, params=params, timeout=30)
    except requests.RequestException as e:
        print(f"Warning: Network error fetching {event_type}: {e}", file=sys.stderr)
        return None

    if not handle_response_status(resp, event_type):
        return None

    try:
        page_events = resp.json()
    except ValueError:
        print(f"Warning: Invalid JSON response for {event_type}. Skipping.", file=sys.stderr)
        return None

    if not isinstance(page_events, list):
        print(f"Warning: Unexpected JSON response for {event_type}. Skipping.", file=sys.stderr)
        return None

    add_page(page_events)
    first_page_full = len(page_events) >= FMP_PAGE_SIZE
    if not first_page_full:
        return events

    page = 0
    while True:
        params = {
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "page": page,
            "apikey": api_key,
        }

        try:
            resp = requests.get(url, params=params, timeout=30)
        except requests.RequestException as e:
            print(f"Warning: Network error fetching {event_type}: {e}", file=sys.stderr)
            return None

        if not handle_response_status(resp, event_type):
            return None

        try:
            page_events = resp.json()
        except ValueError:
            print(f"Warning: Invalid JSON response for {event_type}. Skipping.", file=sys.stderr)
            return None

        if not isinstance(page_events, list):
            print(f"Warning: Unexpected JSON response for {event_type}. Skipping.", file=sys.stderr)
            return None

        if not page_events:
            break

        add_page(page_events)
        if len(page_events) < FMP_PAGE_SIZE:
            break
        page += 1

    return events


def filter_events(events, ticker_set, event_type, from_date, to_date):
    """Keep only events matching the watchlist tickers, attaching event_type."""
    if not events:
        return []

    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")
    rows = []
    for ev in events:
        symbol = normalize_symbol(ev.get("symbol"))
        date = ev.get("date", "")
        if symbol in ticker_set and from_str <= date <= to_str:
            rows.append({
                "date": date,
                "ticker": symbol,
                "event_type": event_type,
                "raw": ev,
            })
    return rows


def format_revenue(value):
    """Format a revenue number into a human-readable string."""
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)

    if abs(v) >= 1_000_000_000:
        return f"{v / 1_000_000_000:.2f}B"
    elif abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.2f}M"
    else:
        return f"{v:.2f}"


def format_detail(row):
    """Build the detail string for a single event row."""
    ev = row["raw"]
    event_type = row["event_type"]

    if event_type == "earnings":
        parts = []
        eps_est = ev.get("epsEstimated")
        rev_est = ev.get("revenueEstimated")
        eps_act = ev.get("eps")
        rev_act = ev.get("revenue")

        if eps_est is not None:
            parts.append(f"EPS est: {eps_est}")
        if rev_est is not None:
            parts.append(f"Revenue est: {format_revenue(rev_est)}")
        if eps_act is not None:
            parts.append(f"EPS actual: {eps_act}")
        if rev_act is not None:
            parts.append(f"Revenue actual: {format_revenue(rev_act)}")

        return "  ".join(parts) if parts else "Earnings (no estimates available)"

    elif event_type == "dividends":
        parts = []
        div = ev.get("dividend")
        date = ev.get("date", "")
        pay_date = ev.get("paymentDate")
        rec_date = ev.get("recordDate")

        if div is not None:
            parts.append(f"Dividend: {div}")
        parts.append(f"Ex-date: {date}")
        if pay_date:
            parts.append(f"Pay date: {pay_date}")
        if rec_date:
            parts.append(f"Record date: {rec_date}")

        return "  ".join(parts)

    elif event_type == "splits":
        num = ev.get("numerator", "?")
        den = ev.get("denominator", "?")
        return f"Ratio: {num}:{den}"

    return ""


def format_text(rows, from_date, to_date, ticker_count, types):
    """Format events as a text table."""
    lines = []
    type_label = "/".join(types)
    header = (
        f"Market Events: {from_date.strftime('%Y-%m-%d')} → {to_date.strftime('%Y-%m-%d')} "
        f"({ticker_count} ticker{'s' if ticker_count != 1 else ''}, {type_label})"
    )
    sep = "─" * 70

    lines.append(header)
    lines.append(sep)

    if not rows:
        lines.append("No events found.")
        lines.append(sep)
        return "\n".join(lines)

    date_w = 12
    tick_w = 8
    type_w = 11

    lines.append(f"{'Date':<{date_w}}{'Ticker':<{tick_w}}{'Type':<{type_w}}Detail")

    for row in rows:
        lines.append(f"{row['date']:<{date_w}}{row['ticker']:<{tick_w}}{row['event_type']:<{type_w}}{row['detail']}")

    lines.append(sep)
    count = len(rows)
    lines.append(f"{count} event{'s' if count != 1 else ''} found.")
    return "\n".join(lines)


def format_json(rows, from_date, to_date, ticker_count, types):
    """Format events as JSON."""
    output = {
        "range": {"from": from_date.strftime("%Y-%m-%d"), "to": to_date.strftime("%Y-%m-%d")},
        "ticker_count": ticker_count,
        "types": types,
        "event_count": len(rows),
        "events": [
            {"date": r["date"], "ticker": r["ticker"], "event_type": r["event_type"],
             "detail": r["detail"], "raw": r["raw"]}
            for r in rows
        ],
    }
    return json.dumps(output, indent=2)


def format_discord(rows, from_date, to_date, ticker_count, types):
    """Format events for Discord chat display."""
    emoji_map = {"earnings": "💰", "dividends": "💵", "splits": "✂️"}
    type_label = "/".join(types)
    lines = [
        f"**Market Events** {from_date.strftime('%Y-%m-%d')} → {to_date.strftime('%Y-%m-%d')} "
        f"({ticker_count} ticker{'s' if ticker_count != 1 else ''}, {type_label})"
    ]

    if not rows:
        lines.append("No events found.")
        return "\n".join(lines)

    for row in rows:
        emoji = emoji_map.get(row["event_type"], "📌")
        lines.append(f"{emoji} **{row['ticker']}** {row['date']} — {row['detail']}")

    lines.append(f"_{len(rows)} event{'s' if len(rows) != 1 else ''} found._")
    return "\n".join(lines)


def main():
    args = parse_args()

    # Validate API key
    api_key = os.environ.get("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    # Resolve tickers
    tickers = resolve_tickers(args)

    # Parse range
    days = parse_range(args.range_str)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if days < 0:
        from_date = today + timedelta(days=days)
        to_date = today
    else:
        from_date = today
        to_date = today + timedelta(days=days)

    # Parse event types
    if args.types:
        types = [t.strip().lower() for t in args.types.split(",")]
        invalid = [t for t in types if t not in ALL_TYPES]
        if invalid:
            print(f"Error: Unknown event types: {', '.join(invalid)}. "
                  f"Valid types: earnings, dividends, splits.", file=sys.stderr)
            sys.exit(1)
    else:
        types = ALL_TYPES

    # Fetch and filter
    all_rows = []
    chunks = date_range_chunks(from_date, to_date)
    for event_type in types:
        for chunk_from, chunk_to in chunks:
            events = fetch_events(event_type, chunk_from, chunk_to, api_key)
            if events is not None:
                filtered = filter_events(events, tickers, event_type, chunk_from, chunk_to)
                all_rows.extend(filtered)

    # Build detail strings
    for row in all_rows:
        row["detail"] = format_detail(row)

    # Sort: date ascending, then event type order
    all_rows.sort(key=lambda r: (r["date"], EVENT_TYPE_ORDER.get(r["event_type"], 99)))

    # Output in requested format
    fmt = args.format
    if fmt == "json":
        print(format_json(all_rows, from_date, to_date, len(tickers), types))
    elif fmt == "discord":
        print(format_discord(all_rows, from_date, to_date, len(tickers), types))
    else:
        print(format_text(all_rows, from_date, to_date, len(tickers), types))


if __name__ == "__main__":
    main()
