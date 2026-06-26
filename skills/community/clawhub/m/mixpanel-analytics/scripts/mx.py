#!/usr/bin/env python3
"""
Mixpanel Analytics CLI for OpenClaw agents.
Usage: mx.py <command> [options]
"""
import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

def get_base_url():
    region = os.environ.get("MIXPANEL_DATA_REGION", "us").lower()
    if region == "eu":
        return "https://data-eu.mixpanel.com/api/2.0"
    return "https://data.mixpanel.com/api/2.0"

def get_auth():
    """Returns (auth_header_value, project_id)"""
    sa_user = os.environ.get("MIXPANEL_SERVICE_ACCOUNT_USERNAME")
    sa_secret = os.environ.get("MIXPANEL_SERVICE_ACCOUNT_SECRET")
    api_secret = os.environ.get("MIXPANEL_API_SECRET")
    project_id = os.environ.get("MIXPANEL_PROJECT_ID", "")

    if sa_user and sa_secret:
        creds = base64.b64encode(f"{sa_user}:{sa_secret}".encode()).decode()
        return f"Basic {creds}", project_id
    elif api_secret:
        creds = base64.b64encode(f"{api_secret}:".encode()).decode()
        return f"Basic {creds}", project_id
    else:
        print("ERROR: Set MIXPANEL_SERVICE_ACCOUNT_USERNAME + MIXPANEL_SERVICE_ACCOUNT_SECRET or MIXPANEL_API_SECRET", file=sys.stderr)
        sys.exit(1)

def api_request(path, params=None):
    auth_header, project_id = get_auth()
    base = get_base_url()
    
    if params is None:
        params = {}
    if project_id and "project_id" not in params:
        params["project_id"] = project_id
    
    query = urllib.parse.urlencode(params)
    url = f"{base}{path}?{query}"
    
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)

def date_range(days):
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days)
    return str(start), str(end)

def cmd_events(args):
    """Top events in a date range."""
    from_date, to_date = date_range(args.days) if not args.from_date else (args.from_date, args.to_date)
    result = api_request("/events/names", {
        "type": "general",
        "limit": args.limit,
    })
    if isinstance(result, list):
        print(f"Top {len(result)} events:")
        for i, event in enumerate(result, 1):
            print(f"  {i:3}. {event}")
    else:
        print(json.dumps(result, indent=2))

def cmd_list_events(args):
    result = api_request("/events/names", {"type": "general", "limit": 255})
    if isinstance(result, list):
        for event in result:
            print(event)
    else:
        print(json.dumps(result, indent=2))

def cmd_segmentation(args):
    """Event count/unique over time."""
    if args.days:
        from_date, to_date = date_range(args.days)
    else:
        from_date, to_date = args.from_date, args.to_date
    
    params = {
        "event": args.event,
        "from_date": from_date,
        "to_date": to_date,
        "unit": args.unit,
        "type": args.type,
    }
    if args.where:
        params["where"] = args.where
    
    result = api_request("/segmentation", params)
    
    if "data" in result:
        data = result["data"]
        series = data.get("series", {})
        values = data.get("values", {})
        
        event_data = values.get(args.event, {})
        if not event_data:
            # Try first key
            event_data = next(iter(values.values()), {}) if values else {}
        
        print(f"Event: {args.event} | Type: {args.type} | Unit: {args.unit}")
        print(f"Period: {from_date} → {to_date}")
        print()
        
        if isinstance(event_data, dict):
            total = 0
            for date_key in sorted(event_data.keys()):
                val = event_data[date_key]
                print(f"  {date_key}: {val:,}")
                total += val
            print(f"\nTotal: {total:,}")
        else:
            print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2))

def cmd_funnels(args):
    """List all funnels."""
    result = api_request("/funnels/list")
    if isinstance(result, list):
        print(f"Funnels ({len(result)}):")
        for f in result:
            print(f"  ID: {f.get('funnel_id','?')} — {f.get('name','?')}")
    else:
        print(json.dumps(result, indent=2))

def cmd_funnel(args):
    """Funnel conversion analysis."""
    params = {
        "funnel_id": args.funnel_id,
        "from_date": args.from_date,
        "to_date": args.to_date,
        "unit": args.unit,
    }
    result = api_request("/funnels", params)
    
    if "data" in result:
        data = result["data"]
        meta = result.get("meta", {})
        
        print(f"Funnel: {args.funnel_id}")
        print(f"Period: {args.from_date} → {args.to_date}")
        print()
        
        steps = meta.get("steps", [])
        # Show overall conversion
        if "analysis" in data:
            analysis = data["analysis"]
            for step in analysis:
                count = step.get("count", 0)
                conv = step.get("overall_conv_ratio", 1.0) * 100
                step_conv = step.get("step_conv_ratio", 1.0) * 100
                event_name = step.get("event", "?")
                print(f"  Step {step.get('step_label','?')}: {event_name}")
                print(f"    Count: {count:,} | Step conv: {step_conv:.1f}% | Overall: {conv:.1f}%")
        else:
            print(json.dumps(data, indent=2))
    else:
        print(json.dumps(result, indent=2))

def cmd_retention(args):
    """Retention cohort analysis."""
    params = {
        "from_date": args.from_date,
        "to_date": args.to_date,
        "retention_type": args.retention_type,
        "unit": args.unit,
    }
    if args.born_event:
        params["born_event"] = args.born_event
    if args.event:
        params["event"] = args.event
    
    result = api_request("/retention", params)
    
    if isinstance(result, dict):
        print(f"Retention | Type: {args.retention_type} | Unit: {args.unit}")
        print(f"Period: {args.from_date} → {args.to_date}")
        print()
        # Print first few cohorts
        for date_key in sorted(list(result.keys())[:7]):
            cohort = result[date_key]
            counts = cohort.get("counts", [])
            first = counts[0] if counts else 0
            if first == 0:
                continue
            retention_pcts = [f"{(c/first*100):.0f}%" if first > 0 else "N/A" for c in counts[:5]]
            print(f"  {date_key}: {first:,} users | Retention: {' → '.join(retention_pcts)}")
    else:
        print(json.dumps(result, indent=2))

def cmd_profile(args):
    """Look up a user profile."""
    region = os.environ.get("MIXPANEL_DATA_REGION", "us").lower()
    base = "https://mixpanel.com/api/2.0" if region != "eu" else "https://eu.mixpanel.com/api/2.0"
    
    auth_header, project_id = get_auth()
    params = {
        "distinct_id": args.distinct_id,
    }
    if project_id:
        params["project_id"] = project_id
    
    query = urllib.parse.urlencode(params)
    url = f"{base}/engage?{query}"
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    
    results = result.get("results", [])
    if not results:
        print(f"No profile found for: {args.distinct_id}")
        return
    
    for profile in results:
        props = profile.get("$properties", {})
        print(f"Distinct ID: {profile.get('$distinct_id','?')}")
        print(f"Last seen: {props.get('$last_seen','?')}")
        print("\nProperties:")
        for k, v in sorted(props.items()):
            if not k.startswith("$"):
                print(f"  {k}: {v}")
        print("\nMixpanel Properties:")
        for k, v in sorted(props.items()):
            if k.startswith("$"):
                print(f"  {k}: {v}")

def cmd_export(args):
    """Export raw event data."""
    region = os.environ.get("MIXPANEL_DATA_REGION", "us").lower()
    base_url = "https://data-eu.mixpanel.com/api/2.0/export" if region == "eu" else "https://data.mixpanel.com/api/2.0/export"
    
    auth_header, project_id = get_auth()
    params = {
        "from_date": args.from_date,
        "to_date": args.to_date,
    }
    if args.event:
        params["event"] = json.dumps([args.event])
    if project_id:
        params["project_id"] = project_id
    if args.where:
        params["where"] = args.where
    
    query = urllib.parse.urlencode(params)
    url = f"{base_url}?{query}"
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    
    try:
        with urllib.request.urlopen(req) as resp:
            count = 0
            for line in resp:
                if not line.strip():
                    continue
                try:
                    event = json.loads(line.decode())
                    if args.output == "pretty":
                        print(json.dumps(event, indent=2))
                    else:
                        props = event.get("properties", {})
                        ts = props.get("time", "?")
                        if isinstance(ts, int):
                            ts = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                        name = event.get("event", "?")
                        uid = props.get("distinct_id", "?")
                        print(f"{ts} | {name} | {uid}")
                    count += 1
                    if args.limit and count >= args.limit:
                        break
                except json.JSONDecodeError:
                    continue
        print(f"\nExported: {count} events")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Mixpanel Analytics CLI for OpenClaw agents")
    sub = parser.add_subparsers(dest="command")

    p_events = sub.add_parser("events", help="Top events")
    p_events.add_argument("--days", type=int, default=30)
    p_events.add_argument("--from-date")
    p_events.add_argument("--to-date")
    p_events.add_argument("--limit", type=int, default=50)

    sub.add_parser("list-events", help="List all event names")

    p_seg = sub.add_parser("segmentation", help="Event count/uniques over time")
    p_seg.add_argument("--event", required=True)
    p_seg.add_argument("--days", type=int)
    p_seg.add_argument("--from-date")
    p_seg.add_argument("--to-date")
    p_seg.add_argument("--unit", default="day", choices=["minute", "hour", "day", "week", "month"])
    p_seg.add_argument("--type", default="general", choices=["general", "unique", "average"])
    p_seg.add_argument("--where", help="Filter expression")

    sub.add_parser("funnels", help="List all funnels")

    p_funnel = sub.add_parser("funnel", help="Funnel conversion analysis")
    p_funnel.add_argument("--funnel-id", required=True)
    p_funnel.add_argument("--from-date", required=True)
    p_funnel.add_argument("--to-date", required=True)
    p_funnel.add_argument("--unit", default="day")

    p_ret = sub.add_parser("retention", help="Retention cohort analysis")
    p_ret.add_argument("--from-date", required=True)
    p_ret.add_argument("--to-date", required=True)
    p_ret.add_argument("--retention-type", default="birth", choices=["birth", "compacted"])
    p_ret.add_argument("--unit", default="day", choices=["day", "week", "month"])
    p_ret.add_argument("--born-event", help="Trigger event for cohort")
    p_ret.add_argument("--event", help="Return event to measure")

    p_profile = sub.add_parser("profile", help="Look up user profile")
    p_profile.add_argument("--distinct-id", required=True)

    p_export = sub.add_parser("export", help="Export raw events")
    p_export.add_argument("--from-date", required=True)
    p_export.add_argument("--to-date", required=True)
    p_export.add_argument("--event")
    p_export.add_argument("--where")
    p_export.add_argument("--limit", type=int)
    p_export.add_argument("--output", default="table", choices=["table", "pretty"])

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "events": cmd_events,
        "list-events": cmd_list_events,
        "segmentation": cmd_segmentation,
        "funnels": cmd_funnels,
        "funnel": cmd_funnel,
        "retention": cmd_retention,
        "profile": cmd_profile,
        "export": cmd_export,
    }
    commands[args.command](args)

if __name__ == "__main__":
    main()
