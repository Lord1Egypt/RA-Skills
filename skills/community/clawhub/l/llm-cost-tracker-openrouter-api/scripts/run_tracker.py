#!/usr/bin/env python3
"""
run_tracker.py — LLM cost/token reports from OpenRouter usage DB.

Source of truth: usage.cost.total from OpenRouter (canonical billed cost).
Time windows: 24h rolling (UTC), 7d/30d/90d/365d calendar days (configurable TZ).

Portable: auto-detects API key from OpenClaw auth-profiles or env var.
"""
import os, sys, json, sqlite3, subprocess, argparse
from datetime import datetime, timedelta, timezone
from tabulate import tabulate

# ─── Portable paths ─────────────────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(SKILL_DIR, "config")
DB_PATH = os.path.join(CONFIG_DIR, "usage.db")

# ─── Schema (kept in sync with collect_usage.py) ─────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS request_facts (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    openrouter_request_id   TEXT UNIQUE NOT NULL,
    created_at_utc          TEXT NOT NULL,
    model                   TEXT,
    provider                TEXT,
    status                  TEXT,
    prompt_tokens           INTEGER DEFAULT 0,
    completion_tokens       INTEGER DEFAULT 0,
    total_tokens            INTEGER DEFAULT 0,
    reasoning_tokens        INTEGER DEFAULT 0,
    cached_tokens           INTEGER DEFAULT 0,
    cache_write_tokens      INTEGER DEFAULT 0,
    billed_cost             REAL DEFAULT 0.0,
    currency                TEXT DEFAULT 'USD',
    streamed                INTEGER DEFAULT 0,
    raw_usage_json          TEXT,
    raw_response_json       TEXT,
    inserted_at_utc         TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_facts_created ON request_facts(created_at_utc);
CREATE INDEX IF NOT EXISTS idx_facts_model   ON request_facts(model);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    for stmt in SCHEMA.strip().split(";"):
        s = stmt.strip()
        if s:
            conn.execute(s)
    return conn


# ─── Config ────────────────────────────────────────────────────────────────
def load_config():
    """Load config/env.json for SESSIONS_DIR, UTC_OFFSET_HOURS, TIMEZONE."""
    env_path = os.path.join(CONFIG_DIR, "env.json")
    if os.path.exists(env_path):
        try:
            with open(env_path) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def get_utc_offset(config):
    """Get UTC offset hours from config (default: 8 for HKT)."""
    return config.get("UTC_OFFSET_HOURS", 8)


def get_tz_label(config):
    """Get timezone label for display (default: HKT)."""
    tz = config.get("TIMEZONE", "Asia/Hong_Kong")
    labels = {
        "Asia/Hong_Kong": "HKT", "Asia/Shanghai": "CST",
        "America/New_York": "ET", "America/Los_Angeles": "PT",
        "Europe/London": "GMT", "Asia/Tokyo": "JST",
    }
    return labels.get(tz, f"UTC+{get_utc_offset(config)}")


def get_openrouter_api_key():
    """
    Resolve OpenRouter API key.
    Priority: env var > OpenClaw auth-profiles.json
    """
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key

    auth_candidates = [
        os.path.expanduser("~/.openclaw/agents/main/agent/auth-profiles.json"),
        "/data/.openclaw/agents/main/agent/auth-profiles.json",
        "/root/.openclaw/agents/main/agent/auth-profiles.json",
    ]
    for auth_path in auth_candidates:
        if os.path.exists(auth_path):
            try:
                with open(auth_path) as f:
                    data = json.load(f)
                key = data.get("profiles", {}).get("openrouter:default", {}).get("key")
                if key:
                    return key
            except Exception:
                continue

    return None


# ─── OpenRouter API ─────────────────────────────────────────────────────────
def get_openrouter_key_info(api_key):
    """
    Fetch key info from /api/v1/auth/key.
    Returns dict with: usage, usage_daily, usage_weekly, usage_monthly, limit, limit_remaining.
    """
    if not api_key:
        return None
    try:
        cmd = ["curl", "-s", "-H", f"Authorization: Bearer {api_key}",
               "https://openrouter.ai/api/v1/auth/key"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            return json.loads(result.stdout).get("data", {})
    except Exception:
        pass
    return None


# ─── Rolling window queries ─────────────────────────────────────────────────
def rolling_totals(conn, hours):
    c = conn.cursor()
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    c.execute("""
        SELECT
            COUNT(*), COALESCE(SUM(billed_cost), 0),
            COALESCE(SUM(prompt_tokens), 0), COALESCE(SUM(completion_tokens), 0),
            COALESCE(SUM(reasoning_tokens), 0), COALESCE(SUM(cached_tokens), 0),
            COALESCE(SUM(cache_write_tokens), 0), COALESCE(SUM(total_tokens), 0)
        FROM request_facts WHERE created_at_utc >= ?
    """, (cutoff,))
    row = c.fetchone()
    return {
        "request_count": row[0], "billed_cost": row[1],
        "prompt_tokens": row[2], "completion_tokens": row[3],
        "reasoning_tokens": row[4], "cached_tokens": row[5],
        "cache_write_tokens": row[6], "total_tokens": row[7],
    }


def calendar_totals(conn, days, utc_offset=8):
    """Aggregate for last N calendar days in local TZ, inclusive of today."""
    c = conn.cursor()
    now_local = datetime.now(timezone.utc) + timedelta(hours=utc_offset)
    today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    window_start = today_start - timedelta(days=days)
    start_utc = (window_start - timedelta(hours=utc_offset)).isoformat()
    end_utc = (now_local - timedelta(hours=utc_offset)).isoformat()

    c.execute("""
        SELECT
            COUNT(*), COALESCE(SUM(billed_cost), 0),
            COALESCE(SUM(prompt_tokens), 0), COALESCE(SUM(completion_tokens), 0),
            COALESCE(SUM(reasoning_tokens), 0), COALESCE(SUM(cached_tokens), 0),
            COALESCE(SUM(cache_write_tokens), 0), COALESCE(SUM(total_tokens), 0)
        FROM request_facts WHERE created_at_utc >= ? AND created_at_utc <= ?
    """, (start_utc, end_utc))
    row = c.fetchone()
    return {
        "request_count": row[0], "billed_cost": row[1],
        "prompt_tokens": row[2], "completion_tokens": row[3],
        "reasoning_tokens": row[4], "cached_tokens": row[5],
        "cache_write_tokens": row[6], "total_tokens": row[7],
    }


def model_breakdown(conn, hours, limit=10):
    c = conn.cursor()
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    c.execute("""
        SELECT model, COUNT(*), SUM(billed_cost), SUM(total_tokens)
        FROM request_facts WHERE created_at_utc >= ?
        GROUP BY model ORDER BY SUM(billed_cost) DESC LIMIT ?
    """, (cutoff, limit))
    return [{"model": r[0], "request_count": r[1], "billed_cost": r[2], "total_tokens": r[3]}
            for r in c.fetchall()]


def daily_breakdown(conn, hours):
    c = conn.cursor()
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    c.execute("""
        SELECT DATE(created_at_utc), COUNT(*), SUM(billed_cost), SUM(total_tokens)
        FROM request_facts WHERE created_at_utc >= ?
        GROUP BY DATE(created_at_utc) ORDER BY DATE(created_at_utc) DESC
    """, (cutoff,))
    return [{"day": r[0], "request_count": r[1], "billed_cost": r[2], "total_tokens": r[3]}
            for r in c.fetchall()]


def debug_requests(conn, hours=24, limit=20):
    c = conn.cursor()
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    c.execute("""
        SELECT openrouter_request_id, created_at_utc, model, status,
               prompt_tokens, completion_tokens, reasoning_tokens,
               cached_tokens, cache_write_tokens, total_tokens, billed_cost, streamed
        FROM request_facts WHERE created_at_utc >= ?
        ORDER BY created_at_utc DESC LIMIT ?
    """, (cutoff, limit))
    cols = ["request_id", "created_at", "model", "status",
            "prompt", "completion", "reasoning", "cached", "cache_write",
            "total", "cost", "stream"]
    return cols, c.fetchall()


# ─── Formatting ────────────────────────────────────────────────────────────
def fmt_cost(cost):
    if cost < 0:   return "N/A"
    if cost < 1:   return f"${cost:.4f}"
    return f"${cost:.2f}"


def fmt_tokens(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000:     return f"{n/1_000:.0f}K"
    return f"{n:,}"


def fmt_model(model):
    if not model:
        return "unknown"
    if "/" in model:
        parts = model.split("/")
        if parts[0] in ("openrouter", "anthropic", "openai", "google", "deepseek", "minimax"):
            return "/".join(parts[1:])
    return model


# ─── Report builders ─────────────────────────────────────────────────────────
def get_db_stats(conn):
    db_size_kb = os.path.getsize(DB_PATH) / 1024
    c = conn.cursor()
    row_count = c.execute("SELECT COUNT(*) FROM request_facts").fetchone()[0]
    oldest, newest = c.execute("SELECT MIN(created_at_utc), MAX(created_at_utc) FROM request_facts").fetchone()
    return db_size_kb, row_count, oldest, newest


def build_telegram_report(conn, key_info=None, config=None):
    config = config or {}
    utc_offset = get_utc_offset(config)
    tz_label = get_tz_label(config)
    now_local = datetime.now(timezone.utc) + timedelta(hours=utc_offset)
    date_str = now_local.strftime("%b %d, %Y %H:%M")

    win_24h = rolling_totals(conn, 24)
    win_7d = calendar_totals(conn, 7, utc_offset)
    win_30d = calendar_totals(conn, 30, utc_offset)
    win_90d = calendar_totals(conn, 90, utc_offset)
    win_365d = calendar_totals(conn, 365, utc_offset)

    lines = [
        f"📊 LLM Cost Report — {date_str} {tz_label}",
        "",
        f"• Messages (24h): {win_24h['request_count']}",
        f"• Est. Tokens (24h): {fmt_tokens(win_24h['total_tokens'])}",
        f"• Est. Cost (24h): {fmt_cost(win_24h['billed_cost'])}",
    ]

    if key_info:
        if key_info.get("usage") is not None:
            lines.append(f"• Total Spend (API key): ${key_info['usage']:.2f}")
        if key_info.get("limit_remaining") is not None:
            lines.append(f"• Limit Remaining: ${key_info['limit_remaining']:.2f}")

    top = model_breakdown(conn, 24, limit=3)
    lines.append("")
    lines.append("🏆 Top Models (24h):")
    for i in range(1, 4):
        if i <= len(top):
            m = top[i-1]
            lines.append(f"  {i}. {fmt_model(m['model'])}: {fmt_cost(m['billed_cost'])}")
        else:
            lines.append(f"  {i}. —")

    lines.append("")
    lines.append("📈 Trend:")
    lines.append(f"• Last 24h: {fmt_cost(win_24h['billed_cost'])}")
    lines.append(f"• Last 7 days: {fmt_cost(win_7d['billed_cost'])}")
    lines.append(f"• Last 30 days: {fmt_cost(win_30d['billed_cost'])}")
    lines.append(f"• Last 90 days: {fmt_cost(win_90d['billed_cost'])}")
    lines.append(f"• Last 365 days: {fmt_cost(win_365d['billed_cost'])}")

    db_size_kb, row_count, oldest, _ = get_db_stats(conn)
    oldest_local = datetime.fromisoformat(oldest).replace(tzinfo=timezone.utc) + timedelta(hours=utc_offset)
    size_str = f"{db_size_kb/1024:.1f} MB" if db_size_kb >= 1024 else f"{db_size_kb:.1f} KB"
    lines.append("")
    lines.append(f"💾 DB: {size_str} · {row_count:,} rows · Since {oldest_local.strftime('%b %d, %Y')}")
    lines.append("")
    lines.append("_Sent via llm-cost-tracker_")
    return "\n".join(lines)


def build_terminal_report(conn, key_info=None, config=None):
    config = config or {}
    now_utc = datetime.now(timezone.utc)
    windows = [("24h", 24), ("7d", 24*7), ("30d", 24*30), ("365d", 24*365)]

    print(f"\n{'='*60}")
    print(f"📊 LLM Usage Report — {now_utc.strftime('%Y-%m-%d %H:%M')} UTC")
    print(f"{'='*60}")

    for label, hours in windows:
        s = rolling_totals(conn, hours)
        billed = s["billed_cost"]
        reqs = s["request_count"]

        print(f"\n─── Last {label} ───")
        print(f"  Cost: {fmt_cost(billed)}  |  Requests: {reqs:,}  |  Tokens: {fmt_tokens(s['total_tokens'])}")
        print(f"  Prompt: {fmt_tokens(s['prompt_tokens'])}  Completion: {fmt_tokens(s['completion_tokens'])}  "
              f"Cached: {fmt_tokens(s['cached_tokens'])}  Reasoning: {fmt_tokens(s['reasoning_tokens'])}")

        top = model_breakdown(conn, hours, limit=5)
        if top:
            table = [[fmt_model(m["model"]), m["request_count"],
                      fmt_tokens(m["total_tokens"]), fmt_cost(m["billed_cost"])]
                     for m in top]
            print(tabulate(table, headers=["Model", "Reqs", "Tokens", "Cost"], tablefmt="simple"))

        if hours >= 24*7:
            daily = daily_breakdown(conn, hours)
            if daily:
                max_cost = max(d["billed_cost"] for d in daily) if daily else 0
                for d in daily[:10]:
                    bar_len = int(d["billed_cost"]/max_cost*20) if max_cost > 0 else 0
                    print(f"    {d['day']} {'█'*bar_len:20s} {fmt_cost(d['billed_cost'])}")

    if key_info:
        print(f"\n💎 API Key Total: ${key_info.get('usage', 0):.2f}  "
              f"(daily: ${key_info.get('usage_daily', 0):.2f}  "
              f"weekly: ${key_info.get('usage_weekly', 0):.2f}  "
              f"monthly: ${key_info.get('usage_monthly', 0):.2f})")
        if key_info.get("limit_remaining") is not None:
            print(f"   Limit remaining: ${key_info['limit_remaining']:.2f}")
    print(f"{'='*60}")


def build_debug_report(conn, hours=24):
    cols, rows = debug_requests(conn, hours)
    if not rows:
        print("No requests in this window.")
        return
    print(f"\n🔍 Debug: Last {hours}h — {len(rows)} requests")
    print(tabulate(rows, headers=cols, tablefmt="grid"))

    c = conn.cursor()
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    c.execute("""
        SELECT openrouter_request_id, raw_usage_json
        FROM request_facts WHERE created_at_utc >= ? AND raw_usage_json IS NOT NULL
        ORDER BY created_at_utc DESC LIMIT 5
    """, (cutoff,))
    for rid, raw in c.fetchall():
        try:
            usage = json.loads(raw)
            print(f"\n  {rid[:40]}: {json.dumps(usage)}")
        except Exception:
            pass


# ─── Health check ────────────────────────────────────────────────────────────
def health_check(conn, api_key=None):
    c = conn.cursor()
    issues = []

    total = c.execute("SELECT COUNT(*) FROM request_facts").fetchone()[0]
    if total == 0:
        print("DB is empty — run: python3 scripts/collect_usage.py --init")
        return False

    total_cost = c.execute("SELECT SUM(billed_cost) FROM request_facts").fetchone()[0] or 0
    row = c.execute("SELECT MIN(created_at_utc), MAX(created_at_utc) FROM request_facts").fetchone()
    print(f"  DB: {total:,} requests, ${total_cost:.2f} billed")
    print(f"  Range: {row[0][:10]} → {row[1][:10]}")

    weird = c.execute(
        "SELECT COUNT(*) FROM request_facts WHERE billed_cost = 0 AND total_tokens > 0"
    ).fetchone()[0]
    if weird:
        print(f"  Note: {weird} rows have tokens but $0 cost (free-tier models)")

    if api_key:
        key_info = get_openrouter_key_info(api_key)
        if key_info:
            api_total = key_info.get("usage", 0)
            print(f"  API key total: ${api_total:.2f} (DB covers {total_cost/api_total*100:.0f}% of key usage)" if api_total > 0 else "")

    print("  OK")
    return True


# ─── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="LLM Cost Tracker — OpenRouter usage reports")
    parser.add_argument("--output", default="telegram",
                        choices=["terminal", "json", "telegram", "debug"],
                        help="Output format (default: telegram)")
    parser.add_argument("--health", action="store_true", help="Run DB health check")
    parser.add_argument("--debug-hours", type=int, default=24,
                        help="Window in hours for debug output")
    args = parser.parse_args()

    config = load_config()
    api_key = get_openrouter_api_key()
    conn = get_conn()

    c = conn.cursor()
    row_count = c.execute("SELECT COUNT(*) FROM request_facts").fetchone()[0]
    if row_count == 0:
        print("DB is empty. Run: python3 scripts/collect_usage.py --init")
        conn.close()
        return 0

    if args.health:
        health_check(conn, api_key)
        conn.close()
        return 0

    key_info = get_openrouter_key_info(api_key)

    if args.output == "terminal":
        build_terminal_report(conn, key_info=key_info, config=config)
    elif args.output == "debug":
        build_debug_report(conn, hours=args.debug_hours)
    elif args.output == "json":
        utc_offset = get_utc_offset(config)
        data = {
            "24h": rolling_totals(conn, 24),
            "7d": calendar_totals(conn, 7, utc_offset),
            "30d": calendar_totals(conn, 30, utc_offset),
            "365d": calendar_totals(conn, 365, utc_offset),
        }
        if key_info:
            data["api_key"] = {
                "usage": key_info.get("usage"),
                "usage_daily": key_info.get("usage_daily"),
                "usage_weekly": key_info.get("usage_weekly"),
                "usage_monthly": key_info.get("usage_monthly"),
                "limit_remaining": key_info.get("limit_remaining"),
            }
        print(json.dumps(data, indent=2))
    else:
        print(build_telegram_report(conn, key_info=key_info, config=config))

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
