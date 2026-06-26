#!/usr/bin/env python3
"""Query usage statistics and quota from a new-api deployment."""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

QUOTA_ENDPOINT = "/api/usage/token/"
LOG_ENDPOINT = "/api/log/token"


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def request_json(url: str, api_key: str, timeout: int) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    req = Request(url, headers=headers, method="GET")
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def query_quota(base_url: str, api_key: str, timeout: int) -> dict:
    url = f"{normalize_base_url(base_url)}{QUOTA_ENDPOINT}"
    return request_json(url, api_key, timeout)


def query_usage(base_url: str, api_key: str, timeout: int) -> dict:
    params = urlencode({"key": api_key})
    url = f"{normalize_base_url(base_url)}{LOG_ENDPOINT}?{params}"
    return request_json(url, api_key, timeout)


def format_timestamp(ts: int) -> str:
    if ts == 0:
        return "Never"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def format_quota(quota: int) -> str:
    return f"{quota:,}"


def quota_to_usd(quota: int) -> str:
    usd = quota / 500000
    return f"${usd:.3f}"


def apply_record_filter(records: list[dict], today_only: bool) -> list[dict]:
    if not today_only:
        return records
    today = datetime.now().date()
    filtered = []
    for r in records:
        ts = int(r.get("created_at", 0) or 0)
        if ts <= 0:
            continue
        if datetime.fromtimestamp(ts).date() == today:
            filtered.append(r)
    return filtered


def print_by_model(records: list[dict]):
    model_stats = defaultdict(
        lambda: {
            "count": 0,
            "quota": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
        }
    )

    for r in records:
        model = r.get("model_name", "unknown")
        model_stats[model]["count"] += 1
        model_stats[model]["quota"] += int(r.get("quota", 0) or 0)
        model_stats[model]["prompt_tokens"] += int(r.get("prompt_tokens", 0) or 0)
        model_stats[model]["completion_tokens"] += int(r.get("completion_tokens", 0) or 0)

    sorted_models = sorted(model_stats.items(), key=lambda x: x[1]["quota"], reverse=True)

    print(f"\n{'=' * 80}")
    print("  Usage by Model")
    print(f"{'=' * 80}")
    print(f"{'Model':<30} {'Calls':>8} {'Quota (USD)':>12} {'Input':>12} {'Output':>10}")
    print("-" * 80)

    total_quota = 0
    total_calls = 0
    for model, stats in sorted_models:
        usd = quota_to_usd(stats["quota"])
        total_quota += stats["quota"]
        total_calls += stats["count"]
        print(
            f"{model:<30} {stats['count']:>8} {usd:>12} "
            f"{format_quota(stats['prompt_tokens']):>12} {format_quota(stats['completion_tokens']):>10}"
        )

    print("-" * 80)
    print(f"{'TOTAL':<30} {total_calls:>8} {quota_to_usd(total_quota):>12}")
    print(f"{'=' * 80}\n")


def print_quota(quota_data: dict):
    if not quota_data.get("code"):
        print(f"Error: {quota_data.get('message', 'Unknown error')}")
        return

    q = quota_data.get("data", {})
    print(f"\n{'=' * 60}")
    print("  Token Info")
    print(f"{'=' * 60}")
    print(f"  Name:       {q.get('name', 'Unknown')}")
    print(f"  Total:      {quota_to_usd(int(q.get('total_granted', 0) or 0))}")
    print(f"  Used:       {quota_to_usd(int(q.get('total_used', 0) or 0))}")
    print(f"  Remaining:  {quota_to_usd(int(q.get('total_available', 0) or 0))}")
    print(f"  Expires:    {format_timestamp(int(q.get('expires_at', 0) or 0))}")
    print(f"{'=' * 60}\n")


def print_summary(quota_data: dict, usage_data: dict, limit: int, today_only: bool):
    print_quota(quota_data)

    if not usage_data.get("success") and not usage_data.get("data"):
        print(f"Usage log error: {usage_data.get('message', 'Unknown error')}")
        return

    all_records = usage_data.get("data", [])
    records = apply_record_filter(all_records, today_only=today_only)

    if not records:
        msg = "No usage records found for today." if today_only else "No usage records found."
        print(msg)
        return

    total_quota = sum(int(r.get("quota", 0) or 0) for r in records)
    total_prompt = sum(int(r.get("prompt_tokens", 0) or 0) for r in records)
    total_completion = sum(int(r.get("completion_tokens", 0) or 0) for r in records)

    print(f"  Usage Statistics ({len(records)} records)")
    print(f"  Total Quota:    {format_quota(total_quota)}")
    print(f"  Input Tokens:   {format_quota(total_prompt)}")
    print(f"  Output Tokens:  {format_quota(total_completion)}")
    print(f"{'=' * 60}\n")

    print(f"Recent {min(limit, len(records))} calls:")
    print("-" * 100)
    print(f"{'Time':<20} {'Model':<22} {'Quota':>10} {'Input':>8} {'Output':>8} {'Time(ms)':>8}")
    print("-" * 100)

    for record in records[:limit]:
        time_str = format_timestamp(int(record.get("created_at", 0) or 0))
        model = str(record.get("model_name", "unknown"))[:20]
        quota = format_quota(int(record.get("quota", 0) or 0))
        prompt = format_quota(int(record.get("prompt_tokens", 0) or 0))
        completion = format_quota(int(record.get("completion_tokens", 0) or 0))
        use_time = int(record.get("use_time", 0) or 0)
        print(f"{time_str:<20} {model:<22} {quota:>10} {prompt:>8} {completion:>8} {use_time:>8}")


def main():
    parser = argparse.ArgumentParser(description="Query new-api usage statistics and quota")
    parser.add_argument("--base-url", required=True, help="new-api base URL")
    parser.add_argument("--key", "-k", required=True, help="API key")
    parser.add_argument("--limit", "-l", type=int, default=100, help="Number of records to show")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    parser.add_argument("--quota-only", "-q", action="store_true", help="Only show quota/balance")
    parser.add_argument("--by-model", "-m", action="store_true", help="Show usage grouped by model")
    parser.add_argument("--today", action="store_true", default=True, help="Show today's records only (default)")
    parser.add_argument("--all-records", action="store_true", help="Show all records")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout in seconds")
    args = parser.parse_args()

    if args.limit <= 0:
        print("Error: --limit must be > 0", file=sys.stderr)
        sys.exit(2)

    if args.timeout <= 0:
        print("Error: --timeout must be > 0", file=sys.stderr)
        sys.exit(2)

    today_only = not args.all_records

    try:
        quota_data = query_quota(args.base_url, args.key, timeout=args.timeout)

        if args.quota_only:
            if args.json:
                print(json.dumps(quota_data, indent=2, ensure_ascii=False))
            else:
                print_quota(quota_data)
            return

        usage_data = query_usage(args.base_url, args.key, timeout=args.timeout)

        if args.json:
            payload = {"quota": quota_data, "usage": usage_data}
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return

        records = apply_record_filter(usage_data.get("data", []), today_only=today_only)
        if args.by_model:
            if not records:
                msg = "No usage records found for today." if today_only else "No usage records found."
                print(msg)
                return
            print_quota(quota_data)
            print_by_model(records)
            return

        print_summary(quota_data, usage_data, limit=args.limit, today_only=today_only)

    except HTTPError as e:
        print(f"HTTP error ({e.code}): {e.reason}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error querying API: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
