#!/usr/bin/env python3
"""
get_news_dataset.py — Fetch AI news dataset for a specific date

IMPORTANT: Use get_latest_news for "today/current/latest" AI news queries.
This tool is for explicit date queries (YYYY-MM-DD), relative dates like
"yesterday", or "the day before yesterday".

With local time semantics:
- Date inputs are interpreted in the user's local timezone
- The tool resolves which canonical dataset corresponds to that local date
- Display emphasizes local time rather than canonical/UTC time

Usage:
    python get_news_dataset.py --date YYYY-MM-DD [--tier guest|pro_core|pro_plus] [--timezone TIMEZONE]
"""

import os
import sys
import json
import argparse

# Ensure lib directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.schemas import validate_date, NetworkError, get_client_timezone
from lib.remote_client import resolve_date, download_dataset, download_pro_dataset
from lib.compression import decompress
from lib.data_store import get_cached, save_cached, record_delivery
from lib.tool_output import format_resolved_date_dataset, format_error, format_automation_safe_dataset, format_context_only_dataset
from lib.engagement_delivery import append_engagement_delivery
from lib.notice_delivery import append_notice_delivery
from lib.agent_handoff_context import build_and_format_handoff_context
from lib.growth_state import (
    load_growth_state,
    save_growth_state,
    record_news_success,
    select_growth_tip,
    mark_tip_shown,
)
from lib.growth_tips import render_growth_tip
from lib.preferences import (
    load_preferences,
    has_preferences_set,
    get_preference_summary,
)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch AI news dataset for a specific date (local time semantics). "
        "Use get_latest_news for today/current/latest AI news."
    )
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format (required, interpreted as local date)")
    parser.add_argument("--tier", default="guest", help="Data tier (default: guest)")
    parser.add_argument("--base-url", default=None, help="AI Daily News API base URL")
    parser.add_argument("--timezone", default=None, help="Client timezone (IANA format, e.g., America/New_York)")
    parser.add_argument(
        "--automation-safe",
        action="store_true",
        help="Output automation-safe markdown for scheduled task generation",
    )
    parser.add_argument(
        "--context-only",
        action="store_true",
        help="Output context-only markdown for loading news into current conversation context only, without rendering news to user. Intended for isolated session continuation scenarios.",
    )
    args = parser.parse_args()

    requested_date = args.date
    tier = args.tier
    base_url = args.base_url

    # Validate date
    err = validate_date(requested_date)
    if err:
        print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        sys.exit(1)

    # Validate tier
    if tier not in ("guest", "pro_core", "pro_plus"):
        print(json.dumps({"status": "error", "message": f"Invalid tier: {tier}"}, ensure_ascii=False))
        sys.exit(1)

    # Get client timezone (from arg, env, or local system)
    client_timezone = args.timezone or get_client_timezone()

    try:
        # Step 1: Resolve local date to canonical date
        if tier == "guest":
            resolve_result = resolve_date(requested_date, client_timezone, tier, base_url=base_url)
        else:
            api_key = os.getenv("AINEWS_ACCESS_TOKEN")
            resolve_result = resolve_date(requested_date, client_timezone, tier, base_url=base_url, api_key=api_key)

        resolved_source_date = resolve_result.get("resolved_source_date", "")
        if not resolved_source_date:
            print(format_error("Could not resolve local date to canonical dataset"))
            sys.exit(1)

        # Step 2: Try cache for the canonical date first
        text = get_cached(resolved_source_date, tier)
        if not text:
            # Download using canonical date
            if tier == "guest":
                raw = download_dataset(resolved_source_date, tier, base_url=base_url)
            else:
                api_key = os.getenv("AINEWS_ACCESS_TOKEN")
                raw = download_pro_dataset(resolved_source_date, tier, base_url=base_url, api_key=api_key)
            text = decompress(raw)
            save_cached(resolved_source_date, tier, text)

        # Parse dataset
        data = json.loads(text)
        record_count = len(data.get("data", []))

        # Record delivery using canonical date
        record_delivery(resolved_source_date, tier, record_count)

        # Format output using resolve result + data
        result = resolve_result.copy()
        result["data"] = data

        # Load growth state and record usage
        growth_state = load_growth_state()
        growth_state = record_news_success(growth_state, scope="date")
        save_growth_state(growth_state)

        # Load preferences for handoff context / automation-safe rendering
        preferences = load_preferences()
        preference_summary = get_preference_summary(preferences)

        # Context-only output for isolated session continuation.
        if args.context_only:
            output = format_context_only_dataset(
                result,
                tier,
                query_type="date",
                preferences=preferences,
                preference_summary=preference_summary,
            )
            print(output)
            return

        if args.automation_safe:
            output = format_automation_safe_dataset(
                result,
                tier,
                query_type="date",
                preferences=preferences,
                preference_summary=preference_summary,
            )
            print(output)
            return

        output = format_resolved_date_dataset(result, tier)

        output = append_engagement_delivery(output, resolve_result)

        # Select and append next step suggestions (same logic as latest news for consistent coverage)
        prefs_set = has_preferences_set(preferences)
        tip_type = select_growth_tip(growth_state, prefs_set)

        if tip_type:
            tip_content = render_growth_tip(tip_type)
            if tip_content:
                output += tip_content
                # Mark suggestion shown to trigger cooldown
                growth_state = mark_tip_shown(growth_state, tip_type)
                save_growth_state(growth_state)

        output = append_notice_delivery(output, resolve_result)

        # Append agent handoff context (for continuation)
        data_date = resolve_result.get("resolved_source_date", "")
        handoff_context = build_and_format_handoff_context(data_date, preferences)
        output += handoff_context

        print(output)

    except NetworkError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
