#!/usr/bin/env python3
"""
get_latest_news.py — Fetch the latest available AI news dataset

Usage:
    python get_latest_news.py [--tier guest|pro_core|pro_plus] [--timezone TIMEZONE]

When users ask for "today's AI news", "current AI news", or "latest AI news",
use this tool instead of get_news_dataset.py. This tool automatically
finds the most recent available data and includes freshness metadata.

Workflow:
1. Detect client timezone
2. Call /v1/data/resolve-latest?client_timezone=xxx to get freshness metadata with local time
3. Check if we already have that canonical date cached locally
4. If cached: use local data
5. If not cached: call /v1/data/download?date=xxx (canonical date)
6. Combine metadata + data and display to LLM with local time info
"""

import os
import sys
import json
import argparse

# Ensure lib directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.schemas import NetworkError, get_client_timezone
from lib.remote_client import resolve_latest_enhanced, download_dataset, download_pro_dataset
from lib.data_store import get_cached, save_cached, record_delivery
from lib.compression import decompress
from lib.tool_output import format_latest_dataset, format_error, format_automation_safe_dataset, format_context_only_dataset
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
    format_preferences_for_agent,
    get_preference_summary,
)


def main():
    parser = argparse.ArgumentParser(description="Fetch latest available AI news dataset")
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

    tier = args.tier
    base_url = args.base_url

    # Validate tier
    if tier not in ("guest", "pro_core", "pro_plus"):
        print(json.dumps({"status": "error", "message": f"Invalid tier: {tier}"}, ensure_ascii=False))
        sys.exit(1)

    # Get client timezone (from arg, env, or local system)
    client_timezone = args.timezone or get_client_timezone()

    try:
        # Step 1: Resolve latest metadata with timezone enhancement
        if tier == "guest":
            metadata = resolve_latest_enhanced(tier, client_timezone=client_timezone, base_url=base_url)
        else:
            api_key = os.getenv("AINEWS_ACCESS_TOKEN")
            metadata = resolve_latest_enhanced(tier, client_timezone=client_timezone, base_url=base_url, api_key=api_key)

        # Get canonical source date (prefer enhanced field, fall back to legacy)
        resolved_source_date = metadata.get("resolved_source_date", metadata.get("resolved_date", ""))
        if not resolved_source_date:
            print(format_error("Could not resolve latest date"))
            sys.exit(1)

        # Step 2: Check if we have this canonical date cached locally
        cached_data_json = get_cached(resolved_source_date, tier)
        if cached_data_json:
            # Use cached data
            data = json.loads(cached_data_json)
        else:
            # Download fresh data using canonical date
            if tier == "guest":
                raw_bytes = download_dataset(resolved_source_date, tier, base_url=base_url)
            else:
                api_key = os.getenv("AINEWS_ACCESS_TOKEN")
                raw_bytes = download_pro_dataset(resolved_source_date, tier, base_url=base_url, api_key=api_key)
            data_json_str = decompress(raw_bytes)
            save_cached(resolved_source_date, tier, data_json_str)
            data = json.loads(data_json_str)

        # Step 3: Combine metadata + data
        result = metadata.copy()
        result["data"] = data

        # Extract info for output
        record_count = len(data.get("data", []))

        # Record delivery using the canonical date
        record_delivery(resolved_source_date, tier, record_count)

        # Load growth state and record usage
        growth_state = load_growth_state()
        growth_state = record_news_success(growth_state, scope="latest")
        save_growth_state(growth_state)

        # Load preferences
        preferences = load_preferences()
        preference_summary = get_preference_summary(preferences)

        # Context-only output for isolated session continuation.
        if args.context_only:
            output = format_context_only_dataset(
                result,
                tier,
                query_type="latest",
                preferences=preferences,
                preference_summary=preference_summary,
            )
            print(output)
            return

        # Automation-safe output for scheduled-task setup/runtime.
        if args.automation_safe:
            output = format_automation_safe_dataset(
                result,
                tier,
                query_type="latest",
                preferences=preferences,
                preference_summary=preference_summary,
            )
            print(output)
            return

        # Format output for interactive LLM flow
        output = format_latest_dataset(result, tier)
        prefs_set = has_preferences_set(preferences)

        # If preferences are set, append preference application context
        # BEFORE rendering news so Agent knows how to filter/sort
        if prefs_set:
            output += "\n\n---\n\n"
            output += format_preferences_for_agent(preferences)
            output += "\n\n---\n\n"

        output = append_engagement_delivery(output, metadata)

        # Select and append growth tip (onboarding, preference, automation, or workflow hint)
        prefs_set = has_preferences_set(preferences)
        tip_type = select_growth_tip(growth_state, prefs_set)

        if tip_type:
            tip_content = render_growth_tip(tip_type)
            if tip_content:
                output += tip_content
                # Mark suggestion shown to trigger cooldown
                growth_state = mark_tip_shown(growth_state, tip_type)
                save_growth_state(growth_state)

        output = append_notice_delivery(output, metadata)

        # Append agent handoff context (for continuation)
        data_date = metadata.get("resolved_source_date", metadata.get("resolved_date", ""))
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
