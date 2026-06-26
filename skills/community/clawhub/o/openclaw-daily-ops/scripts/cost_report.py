#!/usr/bin/env python3
"""
OpenClaw Daily Cost Report
Parses session JSONL files, computes today's API costs, posts to Discord.

Usage:
  python3 cost_report.py --config /path/to/config.json
  python3 cost_report.py --config /path/to/config.json --dry-run
"""

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request


def load_config(config_path):
    with open(os.path.expanduser(config_path)) as f:
        cfg = json.load(f)
    # Expand paths
    cfg["sessions_dir"] = os.path.expanduser(cfg["sessions_dir"])
    cfg["workspace_dir"] = os.path.expanduser(cfg["workspace_dir"])
    return cfg


def get_today_range(tz_offset_hours):
    """Returns (start, end) UTC datetimes for today in the configured timezone."""
    now_utc = datetime.now(timezone.utc)
    tz_delta = timedelta(hours=tz_offset_hours)
    now_local = now_utc + tz_delta
    today_local = now_local.date()

    # Midnight local time, converted back to UTC
    midnight_local = datetime.combine(today_local, datetime.min.time())
    start_utc = midnight_local - tz_delta
    end_utc = start_utc + timedelta(days=1)

    return start_utc.replace(tzinfo=timezone.utc), end_utc.replace(tzinfo=timezone.utc)


def resolve_display_name(session_key, channel_names):
    """Map a session key to a human-readable name."""
    for k, v in channel_names.items():
        if k in session_key:
            return v
    if "cron:" in session_key:
        return "cron:" + session_key.split("cron:")[1][:12]
    if "subagent:" in session_key:
        return "subagent:" + session_key.split("subagent:")[1][:12]
    return session_key[:24]


def parse_costs(cfg, today_start, today_end):
    sessions_dir = cfg["sessions_dir"]
    channel_names = cfg.get("channel_names", {})

    sessions_meta = {}
    sessions_json = os.path.join(sessions_dir, "sessions.json")
    if os.path.exists(sessions_json):
        try:
            with open(sessions_json) as f:
                sessions_meta = json.load(f)
        except Exception:
            pass

    # Build reverse map: jsonl path → session key
    path_to_key = {}
    for sk, meta in sessions_meta.items():
        sf = meta.get("sessionFile", "")
        if sf:
            path_to_key[sf] = sk

    session_costs = {}
    total_cost = 0.0
    total_tokens = 0

    for jsonl_path in glob.glob(os.path.join(sessions_dir, "*.jsonl")):
        session_key = path_to_key.get(jsonl_path, os.path.basename(jsonl_path))
        display = resolve_display_name(session_key, channel_names)

        session_total = 0.0
        session_tokens = 0

        try:
            with open(jsonl_path) as f:
                for line in f:
                    try:
                        msg = json.loads(line)
                        ts_str = msg.get("timestamp", "")
                        if not ts_str:
                            continue
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=timezone.utc)
                        if not (today_start <= ts < today_end):
                            continue
                        inner = msg.get("message", {})
                        if isinstance(inner, dict) and inner.get("role") == "assistant":
                            usage = inner.get("usage", {})
                            cost = usage.get("cost", {})
                            session_total += cost.get("total", 0)
                            session_tokens += usage.get("totalTokens", 0)
                    except Exception:
                        continue
        except Exception:
            continue

        # Include session if it has any activity (cost or tokens)
        # Even if cost is 0 (e.g., free models), show token usage
        if session_tokens > 0:
            session_costs[display] = {"cost": session_total, "tokens": session_tokens}
            total_cost += session_total
            total_tokens += session_tokens

    # Sort by cost first, then by tokens if costs are equal (e.g., all zero)
    sorted_sessions = sorted(session_costs.items(), key=lambda x: (x[1]["cost"], x[1]["tokens"]), reverse=True)
    return total_cost, total_tokens, sorted_sessions


def load_history(cost_log_path):
    if not os.path.exists(cost_log_path):
        return []
    try:
        with open(cost_log_path) as f:
            return json.load(f)
    except Exception:
        return []


def save_history(cost_log_path, history, today_str, total_cost, total_tokens, sorted_sessions):
    os.makedirs(os.path.dirname(cost_log_path), exist_ok=True)
    history.append({
        "date": today_str,
        "total_cost": total_cost,
        "total_tokens": total_tokens,
        "sessions": {k: v for k, v in sorted_sessions},
    })
    history = history[-90:]  # Keep 90 days
    with open(cost_log_path, "w") as f:
        json.dump(history, f, indent=2)
    return history


def format_tokens(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M tok"
    if n >= 1_000:
        return f"{n/1_000:.0f}K tok"
    return f"{n} tok"


def session_icon(cost):
    if cost >= 5:
        return "🔴"
    if cost >= 1:
        return "🟡"
    return "🟢"


def build_report(today_str, total_cost, total_tokens, sorted_sessions, history, zombie_summary, cfg):
    alert_high = cfg.get("alert_high_cost", 50)
    alert_low = cfg.get("alert_low_cost", 10)
    user_id = cfg.get("discord_user_id", "")

    lines = [f"📊 **Daily Cost Report — {today_str}**", ""]

    # Total
    lines.append(f"💰 **Total: ${total_cost:.2f}** · {format_tokens(total_tokens)}")
    lines.append("")

    # Per session
    if sorted_sessions:
        lines.append("**By Session:**")
        for name, data in sorted_sessions:
            icon = session_icon(data["cost"])
            lines.append(f"{icon} {name} — ${data['cost']:.2f} · {format_tokens(data['tokens'])}")
        lines.append("")

    # 7-day trend
    if len(history) >= 2:
        trend_days = history[-7:] if len(history) >= 7 else history
        trend_str = " → ".join(f"${d['total_cost']:.0f}" for d in trend_days)
        lines.append(f"**7-day trend:** {trend_str}")
        lines.append("")

    # Alert flags
    if total_cost >= alert_high:
        mention = f"<@{user_id}> " if user_id else ""
        lines.append(f"🚨 **{mention}HIGH BURN — ${total_cost:.2f} today**")
    elif total_cost <= alert_low and total_cost > 0:
        lines.append("✅ UNDER BUDGET")

    # Zombie summary
    if zombie_summary:
        lines.append(zombie_summary)

    return "\n".join(lines)


def post_discord(webhook_url, message):
    payload = json.dumps({"content": message[:2000]}).encode()
    req = Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "OpenClaw-DailyOps/1.0"},
        method="POST",
    )
    try:
        resp = urlopen(req, timeout=10)
        return True
    except Exception as e:
        code = getattr(e, "code", None)
        if code == 204:
            return True
        print(f"[cost_report] Discord post failed: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Daily Cost Report")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--dry-run", action="store_true", help="Print report without posting or saving")
    parser.add_argument("--zombie-summary", default="", help="Summary line from zombie_killer.py to append")
    args = parser.parse_args()

    cfg = load_config(args.config)
    tz_offset = cfg.get("timezone_offset_hours", -6)
    today_start, today_end = get_today_range(tz_offset)

    # Today's date string in local time
    now_local = datetime.now(timezone.utc) + timedelta(hours=tz_offset)
    today_str = now_local.strftime("%b %-d, %Y")
    today_date_str = now_local.strftime("%Y-%m-%d")

    # Parse costs
    total_cost, total_tokens, sorted_sessions = parse_costs(cfg, today_start, today_end)

    if total_cost == 0 and not sorted_sessions:
        print("[cost_report] No data for today — skipping")
        return

    # Load + save history
    cost_log_path = os.path.join(cfg["workspace_dir"], "state", "cost-log.json")
    history = load_history(cost_log_path)

    if not args.dry_run:
        history = save_history(cost_log_path, history, today_date_str, total_cost, total_tokens, sorted_sessions)

    # Build report
    report = build_report(today_str, total_cost, total_tokens, sorted_sessions, history, args.zombie_summary, cfg)

    if args.dry_run:
        print("=== DRY RUN — report not posted ===")
        print(report)
        return

    # Post
    webhook = cfg.get("discord_webhook", "")
    if not webhook or "YOUR_WEBHOOK" in webhook:
        print("[cost_report] No Discord webhook configured — printing report instead:")
        print(report)
        return

    if post_discord(webhook, report):
        print(f"[cost_report] Report posted — ${total_cost:.2f} today")
    else:
        print(f"[cost_report] Failed to post — ${total_cost:.2f} today")


if __name__ == "__main__":
    main()
