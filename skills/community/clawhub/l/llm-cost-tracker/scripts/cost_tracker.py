#!/usr/bin/env python3
"""API Cost Tracker - Monitor LLM API spending across providers."""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Provider pricing per 1M tokens (as of March 2026)
PRICING = {
    "anthropic": {
        "claude-opus-4-6": {"input": 15.0, "output": 75.0},
        "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
        "claude-haiku-3-5": {"input": 0.80, "output": 4.0},
    },
    "openai": {
        "gpt-4o": {"input": 2.50, "output": 10.0},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-5.3-codex": {"input": 3.0, "output": 15.0},
        "o3": {"input": 10.0, "output": 40.0},
    },
    "google": {
        "gemini-2.5-pro": {"input": 1.25, "output": 10.0},
        "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    },
    "deepseek": {
        "deepseek-v3": {"input": 0.27, "output": 1.10},
        "deepseek-r1": {"input": 0.55, "output": 2.19},
    },
}

CONFIG_PATH = Path.home() / ".openclaw" / "cost-tracker.json"
DATA_PATH = Path.home() / ".openclaw" / "cost-data"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    default = {
        "budgets": {"daily": 10, "weekly": 50, "monthly": 200},
        "alertChannels": ["telegram"],
        "alertThresholds": [50, 75, 90, 100],
    }
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(default, indent=2))
    return default


def get_period_range(period):
    now = datetime.now()
    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start = now - timedelta(days=30)
    return start, now


def fetch_openai_usage(start, end):
    """Fetch usage from OpenAI API."""
    try:
        import urllib.request
        key = os.environ.get("OPENAI_API_KEY", "")
        if not key:
            return []
        url = f"https://api.openai.com/v1/usage?start_date={start.strftime('%Y-%m-%d')}&end_date={end.strftime('%Y-%m-%d')}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        results = []
        for entry in data.get("data", []):
            model = entry.get("snapshot_id", "unknown")
            input_tokens = entry.get("n_context_tokens_total", 0)
            output_tokens = entry.get("n_generated_tokens_total", 0)
            results.append({
                "provider": "openai",
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            })
        return results
    except Exception as e:
        print(f"Warning: Could not fetch OpenAI usage: {e}", file=sys.stderr)
        return []


def fetch_anthropic_usage(start, end):
    """Fetch usage from Anthropic API."""
    try:
        import urllib.request
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            return []
        # Anthropic doesn't have a public usage API yet - use local tracking
        return load_local_data("anthropic", start, end)
    except Exception as e:
        print(f"Warning: Could not fetch Anthropic usage: {e}", file=sys.stderr)
        return []


def load_local_data(provider, start, end):
    """Load locally tracked usage data."""
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    results = []
    for f in DATA_PATH.glob(f"{provider}_*.json"):
        try:
            data = json.loads(f.read_text())
            ts = datetime.fromisoformat(data.get("timestamp", ""))
            if start <= ts <= end:
                results.append(data)
        except (json.JSONDecodeError, ValueError):
            continue
    return results


def calculate_cost(provider, model, input_tokens, output_tokens):
    """Calculate cost for a given usage."""
    prices = PRICING.get(provider, {}).get(model, None)
    if not prices:
        # Fallback: find closest match
        for m, p in PRICING.get(provider, {}).items():
            if m in model or model in m:
                prices = p
                break
    if not prices:
        prices = {"input": 5.0, "output": 15.0}  # Conservative default

    input_cost = (input_tokens / 1_000_000) * prices["input"]
    output_cost = (output_tokens / 1_000_000) * prices["output"]
    return input_cost + output_cost


def log_usage(provider, model, input_tokens, output_tokens):
    """Log a usage entry locally."""
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    entry = {
        "provider": provider,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "timestamp": datetime.now().isoformat(),
        "cost": calculate_cost(provider, model, input_tokens, output_tokens),
    }
    fname = f"{provider}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    (DATA_PATH / fname).write_text(json.dumps(entry, indent=2))
    return entry


def generate_summary(period="month", provider_filter=None):
    """Generate cost summary report."""
    start, end = get_period_range(period)
    all_usage = []

    if not provider_filter or provider_filter == "openai":
        all_usage.extend(fetch_openai_usage(start, end))
    if not provider_filter or provider_filter == "anthropic":
        all_usage.extend(fetch_anthropic_usage(start, end))

    # Also load all local data
    for p in ["openai", "anthropic", "google", "deepseek"]:
        if not provider_filter or provider_filter == p:
            all_usage.extend(load_local_data(p, start, end))

    # Aggregate by provider+model
    agg = {}
    for entry in all_usage:
        key = (entry["provider"], entry["model"])
        if key not in agg:
            agg[key] = {"input_tokens": 0, "output_tokens": 0, "cost": 0}
        agg[key]["input_tokens"] += entry.get("input_tokens", 0)
        agg[key]["output_tokens"] += entry.get("output_tokens", 0)
        if "cost" in entry:
            agg[key]["cost"] += entry["cost"]
        else:
            agg[key]["cost"] += calculate_cost(
                entry["provider"], entry["model"],
                entry.get("input_tokens", 0), entry.get("output_tokens", 0)
            )

    # Format output
    total = 0
    print(f"\n{'Provider':<14}| {'Model':<22}| {'Tokens':<12}| {'Cost':>8}")
    print(f"{'-'*13} | {'-'*21}| {'-'*11}| {'-'*8}")
    for (prov, model), data in sorted(agg.items()):
        tokens = data["input_tokens"] + data["output_tokens"]
        cost = data["cost"]
        total += cost
        tokens_str = f"{tokens/1_000_000:.1f}M" if tokens > 1_000_000 else f"{tokens/1_000:.1f}K"
        print(f"{prov:<14}| {model:<22}| {tokens_str:<12}| ${cost:>7.2f}")
    print(f"{'':14}| {'TOTAL':<22}| {'':12}| ${total:>7.2f}")

    # Budget check
    config = load_config()
    budget = config["budgets"].get(period if period != "today" else "daily", 999999)
    pct = (total / budget * 100) if budget > 0 else 0
    print(f"\nBudget: ${total:.2f} / ${budget:.2f} ({pct:.0f}%)")
    if pct >= 90:
        print("WARNING: Approaching budget limit!")
    elif pct >= 75:
        print("CAUTION: 75%+ of budget used.")

    return total


def optimize_recommendations():
    """Analyze usage and suggest cost optimizations."""
    start, _ = get_period_range("week")
    _, end = get_period_range("today")

    print("\n=== Cost Optimization Recommendations ===\n")
    print("1. MODEL DOWNGRADES")
    print("   - Use Haiku/mini for classification, routing, and simple extraction")
    print("   - Reserve Opus/GPT-4o for complex reasoning and generation")
    print("   - Potential savings: 40-70% on simple tasks\n")
    print("2. CACHING")
    print("   - Enable prompt caching (Anthropic supports this natively)")
    print("   - Cache system prompts and frequently-used context")
    print("   - Potential savings: 20-40% on repeated patterns\n")
    print("3. CONTEXT OPTIMIZATION")
    print("   - Trim conversation history aggressively")
    print("   - Use summarization for long threads instead of full history")
    print("   - Load skills lazily (only when triggered)")
    print("   - Potential savings: 15-30% on token usage\n")
    print("4. BATCH PROCESSING")
    print("   - Group similar tasks and process in batches")
    print("   - Use async/background processing for non-urgent work")
    print("   - Schedule heavy tasks during off-peak hours\n")


def set_budget(amount, period):
    """Set a budget threshold."""
    config = load_config()
    config["budgets"][period] = amount
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    print(f"Budget set: ${amount}/{'day' if period == 'daily' else period}")


def main():
    parser = argparse.ArgumentParser(description="API Cost Tracker for OpenClaw")
    parser.add_argument("--summary", action="store_true", help="Show cost summary")
    parser.add_argument("--provider", choices=["openai", "anthropic", "google", "deepseek"])
    parser.add_argument("--all", action="store_true", help="All providers")
    parser.add_argument("--period", default="month", choices=["today", "week", "month"])
    parser.add_argument("--breakdown", choices=["model", "provider", "day"])
    parser.add_argument("--optimize", action="store_true", help="Show optimization tips")
    parser.add_argument("--set-budget", type=float, help="Set budget amount")
    parser.add_argument("--alert", default="telegram")
    parser.add_argument("--log", nargs=4, metavar=("PROVIDER", "MODEL", "IN_TOKENS", "OUT_TOKENS"))

    args = parser.parse_args()

    if args.set_budget:
        set_budget(args.set_budget, args.period if args.period != "today" else "daily")
    elif args.optimize:
        optimize_recommendations()
    elif args.log:
        entry = log_usage(args.log[0], args.log[1], int(args.log[2]), int(args.log[3]))
        print(f"Logged: ${entry['cost']:.4f}")
    else:
        provider = args.provider if not args.all else None
        generate_summary(args.period, provider)


if __name__ == "__main__":
    main()
