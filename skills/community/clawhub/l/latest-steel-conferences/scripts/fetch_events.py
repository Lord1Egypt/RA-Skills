#!/usr/bin/env python3
"""
Latest Steel Conferences - Event Fetcher
=========================================
Fetches and displays the latest steel industry conferences, webinars, and site tours
from Mysteel's official event listings page.

Source: https://www.mysteel.net/event-listings/

Usage:
    python fetch_events.py [options]

Options:
    --filter TYPE       Filter by event type: conferences, webinars, site-tours, all (default: all)
    --topic TOPIC       Filter by topic (case-insensitive, partial match)
    --date YYYY-MM-DD   Filter events on or after this date
    --limit N           Limit output to N events (default: 10, 0 = no limit)
    --export            Export all events to JSON file
    --format FORMAT     Output format: text, json (default: text)
    --all               Show all events including past ones (default: upcoming only)
    --help              Show this help message
"""

import json
import sys
import os
import argparse
from datetime import datetime, timezone

# Try to import playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: Playwright is not installed.", file=sys.stderr)
    print("Install it with: pip install playwright", file=sys.stderr)
    print("Then run: playwright install chromium", file=sys.stderr)
    sys.exit(1)

# ============================================================================
# Configuration
# ============================================================================

EVENTS_URL = "https://www.mysteel.net/event-listings/"
BASE_URL = "https://www.mysteel.net"

# Event type mapping
CONFERENCE_TYPES = {
    1: "Webinar",
    2: "Conference",
    3: "Site Tour",
}

# Reverse mapping for filtering
TYPE_FILTERS = {
    "conferences": 2,
    "webinars": 1,
    "site-tours": 3,
    "all": None,
}

# ============================================================================
# Data Fetching
# ============================================================================

def fetch_events_with_playwright(url=EVENTS_URL):
    """Fetch events using Playwright (headless browser)."""
    print("Launching browser...", file=sys.stderr)
    
    with sync_playwright() as p:
        # Launch headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Navigating to {url}...", file=sys.stderr)
        page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Wait a bit for any dynamic content
        page.wait_for_timeout(2000)
        
        print("Extracting event data...", file=sys.stderr)
        
        # Extract the __NUXT__ data from the page
        events_data = page.evaluate("""
            () => {
                const nuxt = window.__NUXT__;
                if (!nuxt || !nuxt.data || !nuxt.data[0]) {
                    return null;
                }
                return nuxt.data[0].conferenceList || null;
            }
        """)
        
        browser.close()
        
        if not events_data:
            print("Error: Could not extract event data from page.", file=sys.stderr)
            sys.exit(1)
        
        return events_data


# ============================================================================
# Data Processing
# ============================================================================

def ts_to_datetime(ts_ms):
    """Convert Unix timestamp in milliseconds to datetime object."""
    if ts_ms is None:
        return None
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)


def ts_to_date_str(ts_ms):
    """Convert Unix timestamp to human-readable date string."""
    if ts_ms is None:
        return "TBD"
    dt = ts_to_datetime(ts_ms)
    return dt.strftime("%b %d, %Y")


def ts_to_iso(ts_ms):
    """Convert Unix timestamp to ISO 8601 string."""
    if ts_ms is None:
        return None
    dt = ts_to_datetime(ts_ms)
    return dt.isoformat()


def format_date_range(start_ms, end_ms):
    """Format a date range for display."""
    start = ts_to_datetime(start_ms)
    end = ts_to_datetime(end_ms)

    if start is None:
        return "TBD"

    if end is None or start.date() == end.date():
        return start.strftime("%b %d, %Y")

    if start.month == end.month and start.year == end.year:
        return f"{start.strftime('%b %d')}-{end.strftime('%d, %Y')}"

    return f"{start.strftime('%b %d, %Y')} ~ {end.strftime('%b %d, %Y')}"


def enrich_event(event):
    """Add computed fields to an event."""
    enriched = dict(event)

    # Add human-readable fields
    enriched["startDateStr"] = ts_to_date_str(event.get("startTime"))
    enriched["endDateStr"] = ts_to_date_str(event.get("endTime"))
    enriched["dateRange"] = format_date_range(event.get("startTime"), event.get("endTime"))
    enriched["typeName"] = CONFERENCE_TYPES.get(event.get("conferenceType", 0), "Unknown")
    enriched["fullUrl"] = BASE_URL + event.get("conferenceUrl", "")
    enriched["startISO"] = ts_to_iso(event.get("startTime"))
    enriched["endISO"] = ts_to_iso(event.get("endTime"))

    return enriched


# ============================================================================
# Filtering
# ============================================================================

def filter_upcoming(events):
    """Filter to only upcoming events (start time >= now)."""
    now = datetime.now(timezone.utc)
    return [e for e in events if e.get("startTime") and ts_to_datetime(e["startTime"]) >= now]


def filter_by_type(events, type_name):
    """Filter events by conference type."""
    type_id = TYPE_FILTERS.get(type_name.lower())
    if type_id is None:
        return events
    return [e for e in events if e.get("conferenceType") == type_id]


def filter_by_topic(events, topic):
    """Filter events by topic (case-insensitive partial match)."""
    topic_lower = topic.lower()
    results = []
    for e in events:
        breeds = e.get("breedNames", [])
        # Check breed names
        for breed in breeds:
            if topic_lower in breed.lower():
                results.append(e)
                break
        else:
            # Also check event name and summary
            name = e.get("name", "").lower()
            summary = e.get("summary", "").lower()
            if topic_lower in name or topic_lower in summary:
                results.append(e)
    return results


def filter_by_date(events, date_str):
    """Filter events on or after a specific date."""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    return [e for e in events if e.get("startTime") and ts_to_datetime(e["startTime"]) >= target_date]


# ============================================================================
# Output Formatting
# ============================================================================

def format_text(events, title="Steel Industry Events"):
    """Format events as human-readable text."""
    if not events:
        return f"\n📅 {title}\n{'=' * 40}\n\nNo events found matching your criteria.\n"

    lines = []
    lines.append(f"\n📅 {title}")
    lines.append("=" * 50)
    lines.append(f"   Total: {len(events)} event(s)")
    lines.append(f"   Source: {EVENTS_URL}")
    lines.append(f"   Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    for i, event in enumerate(events, 1):
        lines.append(f"{i}. {event.get('name', 'Untitled').strip()}")
        lines.append(f"   📍 Location: {event.get('location', 'TBD')}")
        lines.append(f"   🗓️  Date: {event.get('dateRange', 'TBD')}")
        lines.append(f"   🌐 Language: {event.get('language', 'TBD')}")
        lines.append(f"   📋 Type: {event.get('typeName', 'Unknown')}")

        breeds = event.get("breedNames", [])
        if breeds:
            lines.append(f"   🏷️  Topics: {', '.join(breeds)}")

        lines.append(f"   🔗 URL: {event.get('fullUrl', '')}")

        summary = event.get("summary", "").strip()
        if summary:
            # Truncate long summaries for display
            if len(summary) > 200:
                summary = summary[:200] + "..."
            lines.append(f"   📝 Summary: {summary}")

        lines.append("")

    return "\n".join(lines)


def format_json(events, metadata=None):
    """Format events as JSON."""
    output = {
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "source": EVENTS_URL,
        "totalEvents": len(events),
        "events": [],
    }

    if metadata:
        output["metadata"] = metadata

    for event in events:
        output["events"].append({
            "id": event.get("id"),
            "name": event.get("name", "").strip(),
            "location": event.get("location", ""),
            "startDate": event.get("startISO"),
            "endDate": event.get("endISO"),
            "dateRange": event.get("dateRange", ""),
            "language": event.get("language", ""),
            "type": event.get("typeName", ""),
            "conferenceType": event.get("conferenceType"),
            "topics": event.get("breedNames", []),
            "url": event.get("fullUrl", ""),
            "imageUrl": event.get("imgUrl", ""),
            "summary": event.get("summary", "").strip(),
        })

    return json.dumps(output, indent=2, ensure_ascii=False)


def export_json(events, filepath=None):
    """Export events to a JSON file."""
    if filepath is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"steel_conferences_{timestamp}.json"

    json_str = format_json(events)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json_str)

    return filepath


# ============================================================================
# Main
# ============================================================================

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch latest steel industry conferences from Mysteel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fetch_events.py                          # Show upcoming events
  python fetch_events.py --filter webinars        # Show only webinars
  python fetch_events.py --topic "iron ore"       # Filter by topic
  python fetch_events.py --date 2026-11-01        # Events after date
  python fetch_events.py --limit 5                # Show next 5 events
  python fetch_events.py --export                 # Export to JSON file
  python fetch_events.py --format json            # Output as JSON
  python fetch_events.py --all                    # Include past events
        """,
    )
    parser.add_argument("--filter", choices=["conferences", "webinars", "site-tours", "all"],
                        default="all", help="Filter by event type (default: all)")
    parser.add_argument("--topic", type=str, default=None,
                        help="Filter by topic (case-insensitive)")
    parser.add_argument("--date", type=str, default=None,
                        help="Filter events on or after date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=10,
                        help="Limit output to N events (0 = no limit, default: 10)")
    parser.add_argument("--export", action="store_true",
                        help="Export all events to JSON file")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--all", action="store_true",
                        help="Show all events including past ones")
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Step 1: Fetch events using Playwright
    raw_events = fetch_events_with_playwright()
    
    if not raw_events:
        print("No events found.", file=sys.stderr)
        sys.exit(0)

    # Step 2: Enrich events
    events = [enrich_event(e) for e in raw_events]

    # Step 3: Apply filters
    metadata = {"filters": {}}

    # Filter: upcoming only (unless --all)
    if not args.all:
        events = filter_upcoming(events)
        metadata["filters"]["upcomingOnly"] = True
    else:
        metadata["filters"]["upcomingOnly"] = False

    # Filter: by type
    if args.filter != "all":
        events = filter_by_type(events, args.filter)
        metadata["filters"]["type"] = args.filter

    # Filter: by topic
    if args.topic:
        events = filter_by_topic(events, args.topic)
        metadata["filters"]["topic"] = args.topic

    # Filter: by date
    if args.date:
        events = filter_by_date(events, args.date)
        metadata["filters"]["dateFrom"] = args.date

    # Sort by start time (earliest first)
    events.sort(key=lambda e: e.get("startTime", 0))

    # Step 4: Limit output
    total_filtered = len(events)
    if args.limit > 0:
        events = events[:args.limit]

    metadata["totalFound"] = total_filtered
    metadata["totalDisplayed"] = len(events)

    # Step 5: Export or display
    if args.export:
        filepath = export_json(events)
        print(f"✅ Exported {len(events)} events to: {filepath}", file=sys.stderr)
        return

    # Output
    if args.format == "json":
        print(format_json(events, metadata))
    else:
        # Build title based on filters
        title_parts = ["Upcoming"]
        if args.filter != "all":
            title_parts.append(args.filter.capitalize())
        if args.topic:
            title_parts.append(f'"{args.topic}"')
        title_parts.append("Steel Industry Events")
        title = " ".join(title_parts)

        print(format_text(events, title))


if __name__ == "__main__":
    main()
