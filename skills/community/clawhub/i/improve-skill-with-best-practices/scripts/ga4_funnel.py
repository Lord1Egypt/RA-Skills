#!/usr/bin/env python3
from __future__ import annotations
"""GA4 Funnel Exploration report via the Data API v1alpha.

Uses AlphaAnalyticsDataClient.run_funnel_report() — the only GA4 exploration
type that has a dedicated API method.  Free-form explorations are already
covered by ga4_query.py (runReport); path explorations have no API support.

Usage examples:

    # Quick funnel with event names (comma-separated)
    python ga4_funnel.py --steps "first_visit,page_view,signup,purchase"

    # With custom step names
    python ga4_funnel.py \
        --steps "first_visit,page_view,signup,purchase" \
        --step-names "First Visit,View Page,Sign Up,Purchase"

    # Open funnel (users can enter at any step)
    python ga4_funnel.py --steps "page_view,add_to_cart,purchase" --open

    # Breakdown by device category
    python ga4_funnel.py --steps "page_view,signup" --breakdown deviceCategory

    # Trended funnel (shows daily trend per step)
    python ga4_funnel.py --steps "page_view,purchase" --trended

    # Use a JSON config file for complex filters
    python ga4_funnel.py --config funnel_config.json

Reads .env from: .skills-data/google-analytics-and-search-improve/.env
Env vars: GA4_PROPERTY_ID
"""

import argparse
import json
import os
import sys
from pathlib import Path

from utils import require_google_credentials

# Auto-discover credentials before importing Google client libs
require_google_credentials()


# ---------------------------------------------------------------------------
# Imports from v1alpha (funnel API is alpha-only)
# ---------------------------------------------------------------------------

from google.analytics.data_v1alpha import AlphaAnalyticsDataClient
from google.analytics.data_v1alpha.types import (
    DateRange,
    Dimension,
    Funnel,
    FunnelBreakdown,
    FunnelEventFilter,
    FunnelFieldFilter,
    FunnelFilterExpression,
    FunnelFilterExpressionList,
    FunnelStep,
    RunFunnelReportRequest,
    StringFilter,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_event_filter(event_name: str) -> FunnelFilterExpression:
    """Create a FunnelFilterExpression matching a single event name."""
    return FunnelFilterExpression(
        funnel_event_filter=FunnelEventFilter(event_name=event_name),
    )


def _build_or_event_filter(event_names: list[str]) -> FunnelFilterExpression:
    """Create a FunnelFilterExpression matching any of several event names."""
    if len(event_names) == 1:
        return _build_event_filter(event_names[0])
    return FunnelFilterExpression(
        or_group=FunnelFilterExpressionList(
            expressions=[_build_event_filter(e) for e in event_names],
        ),
    )


def _build_field_filter(
    field_name: str,
    value: str,
    match_type: str = "EXACT",
) -> FunnelFilterExpression:
    """Create a FunnelFilterExpression matching a dimension field value."""
    mt = StringFilter.MatchType[match_type.upper()]
    return FunnelFilterExpression(
        funnel_field_filter=FunnelFieldFilter(
            field_name=field_name,
            string_filter=StringFilter(match_type=mt, value=value),
        ),
    )


def build_steps_from_events(
    event_names: list[str],
    step_names: list[str] | None = None,
) -> list[FunnelStep]:
    """Build FunnelStep list from simple event name strings.

    Each element in *event_names* can contain ``|`` to denote OR logic,
    e.g. ``"first_open|first_visit"`` matches either event.
    """
    steps = []
    for i, raw in enumerate(event_names):
        events = [e.strip() for e in raw.split("|") if e.strip()]
        name = step_names[i] if step_names and i < len(step_names) else events[0]
        steps.append(
            FunnelStep(
                name=name,
                filter_expression=_build_or_event_filter(events),
            )
        )
    return steps


def build_steps_from_config(config_steps: list[dict]) -> list[FunnelStep]:
    """Build FunnelStep list from a richer JSON config.

    Each dict may have:
        name            – step display name (required)
        events          – list of event names (OR logic)
        field_filter    – {field_name, value, match_type} for dimension match
        directly_followed_by – bool
        within_duration      – str like "300s"
    """
    steps = []
    for cfg in config_steps:
        # Build filter expression
        exprs: list[FunnelFilterExpression] = []
        for ev in cfg.get("events", []):
            exprs.append(_build_event_filter(ev))
        ff = cfg.get("field_filter")
        if ff:
            exprs.append(
                _build_field_filter(
                    ff["field_name"], ff["value"], ff.get("match_type", "EXACT"),
                )
            )

        if len(exprs) == 0:
            print(f"Error: step '{cfg.get('name')}' has no events or field_filter", file=sys.stderr)
            sys.exit(1)
        elif len(exprs) == 1:
            filter_expr = exprs[0]
        else:
            filter_expr = FunnelFilterExpression(
                or_group=FunnelFilterExpressionList(expressions=exprs),
            )

        step = FunnelStep(
            name=cfg["name"],
            filter_expression=filter_expr,
        )
        if cfg.get("directly_followed_by"):
            step.is_directly_followed_by = True
        if cfg.get("within_duration"):
            step.within_duration_from_prior_step = cfg["within_duration"]

        steps.append(step)

    return steps


# ---------------------------------------------------------------------------
# Report execution
# ---------------------------------------------------------------------------

def run_funnel_report(
    property_id: str,
    steps: list[FunnelStep],
    start_date: str = "28daysAgo",
    end_date: str = "yesterday",
    is_open_funnel: bool = False,
    breakdown_dimension: str | None = None,
    trended: bool = False,
) -> dict:
    """Execute a funnel report and return structured results."""
    client = AlphaAnalyticsDataClient()

    funnel = Funnel(steps=steps, is_open_funnel=is_open_funnel)

    request = RunFunnelReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        funnel=funnel,
    )

    if breakdown_dimension:
        request.funnel_breakdown = FunnelBreakdown(
            breakdown_dimension=Dimension(name=breakdown_dimension),
        )

    if trended:
        request.funnel_visualization_type = (
            RunFunnelReportRequest.FunnelVisualizationType.TRENDED_FUNNEL
        )

    response = client.run_funnel_report(request)
    return _parse_funnel_response(response)


def _parse_sub_report(sub_report) -> dict:
    """Parse a FunnelSubReport (funnel_table or funnel_visualization) into a dict."""
    dim_headers = [h.name for h in sub_report.dimension_headers]
    metric_headers = [h.name for h in sub_report.metric_headers]
    rows = []
    for row in sub_report.rows:
        r: dict = {}
        for i, dv in enumerate(row.dimension_values):
            r[dim_headers[i]] = dv.value
        for i, mv in enumerate(row.metric_values):
            val = mv.value
            try:
                val = float(val)
                if val == int(val):
                    val = int(val)
            except (ValueError, TypeError):
                pass
            r[metric_headers[i]] = val
        rows.append(r)
    return {"dimensions": dim_headers, "metrics": metric_headers, "rows": rows}


def _parse_funnel_response(response) -> dict:
    """Convert protobuf funnel response to a plain dict.

    NOTE: ``response.funnel_table`` and ``response.funnel_visualization`` are
    ``FunnelSubReport`` objects directly (they do **not** have an inner
    ``.sub_report`` attribute).
    """
    result = {}

    # --- funnel table (main data) ---
    if response.funnel_table:
        result["funnel_table"] = _parse_sub_report(response.funnel_table)

    # --- funnel visualization ---
    if response.funnel_visualization:
        result["funnel_visualization"] = _parse_sub_report(response.funnel_visualization)

    # --- sampling metadata ---
    if response.funnel_table and getattr(response.funnel_table, "metadata", None):
        meta = response.funnel_table.metadata
        if getattr(meta, "sampling_metadatas", None):
            samples = []
            for sm in meta.sampling_metadatas:
                samples.append({
                    "samples_read_count": sm.samples_read_count,
                    "sampling_space_size": sm.sampling_space_size,
                })
            result["sampling"] = samples

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="GA4 Funnel Exploration report (v1alpha API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python ga4_funnel.py --steps "first_visit,page_view,signup,purchase"
  python ga4_funnel.py --steps "page_view,add_to_cart,purchase" --open --breakdown deviceCategory
  python ga4_funnel.py --config funnel_config.json --trended
""",
    )
    parser.add_argument(
        "--property-id",
        default=os.environ.get("GA4_PROPERTY_ID"),
        help="GA4 property ID (or set GA4_PROPERTY_ID env)",
    )
    parser.add_argument(
        "--steps",
        help='Comma-separated event names for funnel steps. '
             'Use "|" within a step for OR logic, e.g. "first_open|first_visit,page_view,purchase"',
    )
    parser.add_argument(
        "--step-names",
        help="Comma-separated display names for each step (must match --steps count)",
    )
    parser.add_argument(
        "--config",
        help="Path to a JSON config file defining funnel steps (advanced mode)",
    )
    parser.add_argument("--start-date", default="28daysAgo")
    parser.add_argument("--end-date", default="yesterday")
    parser.add_argument(
        "--open", action="store_true",
        help="Open funnel — users can enter at any step (default: closed)",
    )
    parser.add_argument(
        "--breakdown",
        help="Dimension to break down by (e.g. deviceCategory, country, sessionSource)",
    )
    parser.add_argument(
        "--trended", action="store_true",
        help="Show trended funnel (daily trend per step)",
    )
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    if not args.property_id:
        print("Error: --property-id required or set GA4_PROPERTY_ID", file=sys.stderr)
        sys.exit(1)

    # --- Build funnel steps ---
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        steps = build_steps_from_config(config.get("steps", config))
        # Config may also specify other options
        if isinstance(config, dict):
            if "open" in config:
                args.open = config["open"]
            if "breakdown" in config and not args.breakdown:
                args.breakdown = config["breakdown"]
            if "trended" in config:
                args.trended = config["trended"]
    elif args.steps:
        event_list = [s.strip() for s in args.steps.split(",")]
        step_names = None
        if args.step_names:
            step_names = [n.strip() for n in args.step_names.split(",")]
        steps = build_steps_from_events(event_list, step_names)
    else:
        print("Error: provide --steps or --config", file=sys.stderr)
        sys.exit(1)

    if len(steps) < 2:
        print("Error: funnel requires at least 2 steps", file=sys.stderr)
        sys.exit(1)

    # --- Run report ---
    result = run_funnel_report(
        property_id=args.property_id,
        steps=steps,
        start_date=args.start_date,
        end_date=args.end_date,
        is_open_funnel=args.open,
        breakdown_dimension=args.breakdown,
        trended=args.trended,
    )

    result["query"] = {
        "property_id": args.property_id,
        "date_range": {"start": args.start_date, "end": args.end_date},
        "is_open_funnel": args.open,
        "breakdown": args.breakdown,
        "trended": args.trended,
        "step_count": len(steps),
        "steps": [s.name for s in steps],
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
