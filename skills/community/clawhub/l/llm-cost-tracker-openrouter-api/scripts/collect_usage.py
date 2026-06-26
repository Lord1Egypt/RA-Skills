#!/usr/bin/env python3
"""
collect_usage.py — Collect OpenRouter request facts into append-only SQLite DB.

One row per completed OpenRouter API request. Canonical cost = usage.cost.total.
Portable: auto-detects all paths, works on any machine with OpenClaw installed.

Usage:
    python3 scripts/collect_usage.py              # collect today's requests
    python3 scripts/collect_usage.py --date 2026-04-24  # specific UTC date
    python3 scripts/collect_usage.py --backfill         # scan all sessions
    python3 scripts/collect_usage.py --init             # first-run wizard
    python3 scripts/collect_usage.py --verify           # validate DB health
    python3 scripts/collect_usage.py --dry-run          # preview without writing
"""
import os, sys, json, sqlite3, argparse
from datetime import datetime, timezone, timedelta

# ─── Portable path detection ────────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(SKILL_DIR, "config")
DB_PATH = os.path.join(CONFIG_DIR, "usage.db")

# ─── Schema ────────────────────────────────────────────────────────────────
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
CREATE INDEX IF NOT EXISTS idx_facts_created  ON request_facts(created_at_utc);
CREATE INDEX IF NOT EXISTS idx_facts_model    ON request_facts(model);
CREATE INDEX IF NOT EXISTS idx_facts_req_id   ON request_facts(openrouter_request_id);
"""

UPSERT_SQL = """
INSERT INTO request_facts (
    openrouter_request_id, created_at_utc, model, provider, status,
    prompt_tokens, completion_tokens, total_tokens, reasoning_tokens,
    cached_tokens, cache_write_tokens, billed_cost, currency, streamed,
    raw_usage_json, raw_response_json, inserted_at_utc
) VALUES (
    :openrouter_request_id, :created_at_utc, :model, :provider, :status,
    :prompt_tokens, :completion_tokens, :total_tokens, :reasoning_tokens,
    :cached_tokens, :cache_write_tokens, :billed_cost, :currency, :streamed,
    :raw_usage_json, :raw_response_json, :inserted_at_utc
)
ON CONFLICT(openrouter_request_id) DO UPDATE SET
    model               = excluded.model,
    provider            = excluded.provider,
    status              = excluded.status,
    prompt_tokens       = excluded.prompt_tokens,
    completion_tokens   = excluded.completion_tokens,
    total_tokens        = excluded.total_tokens,
    reasoning_tokens    = excluded.reasoning_tokens,
    cached_tokens       = excluded.cached_tokens,
    cache_write_tokens  = excluded.cache_write_tokens,
    billed_cost         = excluded.billed_cost,
    streamed            = excluded.streamed,
    raw_usage_json      = excluded.raw_usage_json,
    raw_response_json   = excluded.raw_response_json
"""


# ─── DB helpers ────────────────────────────────────────────────────────────
def get_conn():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    for stmt in SCHEMA.strip().split(";"):
        stmt = stmt.strip()
        if stmt:
            conn.execute(stmt)
    return conn


# ─── Config ────────────────────────────────────────────────────────────────
def load_config():
    """Load config/env.json. Returns dict with optional SESSIONS_DIR, UTC_OFFSET_HOURS."""
    env_path = os.path.join(CONFIG_DIR, "env.json")
    if os.path.exists(env_path):
        try:
            with open(env_path) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def find_sessions_dir(config=None):
    """
    Find the OpenClaw sessions directory.
    Priority: config SESSIONS_DIR > auto-detect common locations.
    Returns (path_or_None, jsonl_count).
    """
    config = config or {}

    if config.get("SESSIONS_DIR"):
        d = os.path.expanduser(config["SESSIONS_DIR"])
        if os.path.isdir(d):
            count = sum(1 for f in os.listdir(d) if ".jsonl" in f)
            return d, count

    candidates = [
        os.path.expanduser("~/.openclaw/agents/main/sessions"),
        "/data/.openclaw/agents/main/sessions",
        "/root/.openclaw/agents/main/sessions",
        os.path.expanduser("~/Library/Application Support/openclaw/agents/main/sessions"),
    ]

    for d in candidates:
        if os.path.isdir(d):
            count = sum(1 for f in os.listdir(d) if ".jsonl" in f)
            return d, count

    return None, 0


def list_session_files(sessions_dir):
    """List all parseable session files (includes .reset files, excludes trajectory)."""
    return sorted([
        f for f in os.listdir(sessions_dir)
        if ".jsonl" in f and "trajectory" not in f
    ], reverse=True)


# ─── Usage extraction ───────────────────────────────────────────────────────
def extract_usage(msg):
    """
    Extract usage fields from an OpenRouter assistant message.
    Returns None if usage or cost.total is absent.
    """
    usage = msg.get("usage", {})
    if not usage:
        return None

    cost_data = usage.get("cost", {})
    billed_cost = None
    if isinstance(cost_data, dict):
        billed_cost = cost_data.get("total")
    elif isinstance(cost_data, (int, float)):
        billed_cost = float(cost_data)

    if billed_cost is None:
        return None

    return {
        "prompt_tokens":      usage.get("input", 0),
        "completion_tokens":  usage.get("output", 0),
        "total_tokens":       usage.get("totalTokens", 0),
        "reasoning_tokens":   usage.get("reasoning", 0),
        "cached_tokens":      usage.get("cacheRead", 0),
        "cache_write_tokens": usage.get("cacheWrite", 0),
        "billed_cost":        billed_cost,
        "raw_usage":          usage,
    }


# ─── Session parsing ────────────────────────────────────────────────────────
def parse_session_file(fpath):
    """
    Parse one session JSONL file → list of request fact dicts.
    Handles both regular .jsonl and .jsonl.reset.* files.
    Deduplication by openrouter_request_id (responseId) — idempotent.
    """
    entries = []
    try:
        with open(fpath) as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []

    facts = []
    current_model = None

    for entry in entries:
        etype = entry.get("type", "")

        if etype == "model_change":
            current_model = entry.get("modelId") or entry.get("data", {}).get("modelId")
            continue

        if etype == "custom" and entry.get("customType") == "model-snapshot":
            data = entry.get("data", {})
            current_model = data.get("modelId") or current_model
            continue

        if etype != "message":
            continue

        msg = entry.get("message", {})
        if msg.get("role") != "assistant":
            continue

        usage_data = extract_usage(msg)
        if usage_data is None:
            continue

        response_id = msg.get("responseId") or entry.get("responseId")
        if not response_id:
            ts = entry.get("timestamp", "")
            response_id = f"no-responseId-{ts}"

        raw_ts = entry.get("timestamp", "")
        ts_clean = raw_ts.replace("Z", "+00:00").replace("+00:00", "")
        try:
            created_at = datetime.fromisoformat(ts_clean).replace(tzinfo=None)
        except (ValueError, OSError):
            created_at = datetime.now(timezone.utc).replace(tzinfo=None)

        model = (
            msg.get("model")
            or entry.get("modelId")
            or current_model
            or "unknown"
        )
        provider = msg.get("provider") or "openrouter"
        streamed = 1 if msg.get("api") == "openai-chatcompletions-stream" else 0

        facts.append({
            "openrouter_request_id": response_id,
            "created_at_utc":         created_at.isoformat(),
            "model":                  model,
            "provider":               provider,
            "status":                 msg.get("stopReason") or "completed",
            "prompt_tokens":          usage_data["prompt_tokens"],
            "completion_tokens":      usage_data["completion_tokens"],
            "total_tokens":           usage_data["total_tokens"],
            "reasoning_tokens":       usage_data["reasoning_tokens"],
            "cached_tokens":          usage_data["cached_tokens"],
            "cache_write_tokens":     usage_data["cache_write_tokens"],
            "billed_cost":            usage_data["billed_cost"],
            "currency":               "USD",
            "streamed":               streamed,
            "raw_usage_json":          json.dumps(usage_data["raw_usage"]),
            "raw_response_json":       json.dumps({
                "responseId": response_id,
                "model":      model,
                "provider":   provider,
                "stopReason": msg.get("stopReason"),
            }),
            "inserted_at_utc":        datetime.now(timezone.utc).isoformat(),
        })

    return facts


# ─── DB upsert ─────────────────────────────────────────────────────────────
def upsert_facts(conn, facts):
    """Upsert all facts. Returns count of operations."""
    c = conn.cursor()
    count = 0
    for fact in facts:
        try:
            c.execute(UPSERT_SQL, fact)
            count += 1
        except Exception:
            pass
    conn.commit()
    return count


# ─── Verification ───────────────────────────────────────────────────────────
def verify_db(conn):
    """Validate DB health. Returns (ok, issues)."""
    c = conn.cursor()
    issues = []

    total = c.execute("SELECT COUNT(*) FROM request_facts").fetchone()[0]
    if total == 0:
        issues.append("DB is empty — run --backfill first")
        return False, issues

    c.execute("SELECT COUNT(*) FROM request_facts WHERE billed_cost = 0 AND total_tokens > 0")
    zero_cost = c.fetchone()[0]
    if zero_cost > 0:
        # Not an error — free-tier models have tokens but $0 cost
        issues.append(f"Note: {zero_cost} rows have tokens but $0 cost (free-tier models)")

    c.execute("SELECT COUNT(*) FROM request_facts WHERE model IS NULL OR model = ''")
    no_model = c.fetchone()[0]
    if no_model > 0:
        issues.append(f"{no_model} rows have no model")

    row = c.execute("SELECT MIN(created_at_utc), MAX(created_at_utc) FROM request_facts").fetchone()
    if row[0]:
        issues.append(f"Data range: {row[0][:10]} → {row[1][:10]}")

    total_cost = c.execute("SELECT SUM(billed_cost) FROM request_facts").fetchone()[0] or 0
    issues.append(f"Total billed in DB: ${total_cost:.4f} ({total} requests)")

    ok = len([i for i in issues if not i.startswith("Data range") and not i.startswith("Total") and not i.startswith("Note:")]) == 0
    return ok, issues


# ─── Main commands ─────────────────────────────────────────────────────────
def collect(target_date=None, dry_run=False, backfill=False, verbose=False, verify_only=False):
    config = load_config()
    sessions_dir, jsonl_count = find_sessions_dir(config)

    if not sessions_dir:
        print("ERROR: Sessions directory not found.")
        print("  Set SESSIONS_DIR in config/env.json to override.")
        return 1

    conn = get_conn()

    if verify_only:
        ok, issues = verify_db(conn)
        print("DB Health Check:")
        for issue in issues:
            print(f"  {issue}")
        print("OK" if ok else "Issues found (see above)")
        conn.close()
        return 0 if ok else 1

    jsonl_files = list_session_files(sessions_dir)
    print(f"Sessions: {sessions_dir} ({len(jsonl_files)} files)")

    if not jsonl_files:
        print("No session files found")
        conn.close()
        return 0

    if backfill:
        print(f"Backfill: scanning {len(jsonl_files)} files...")
        total_ops = 0
        for i, fname in enumerate(jsonl_files):
            if verbose and (i + 1) % 20 == 0:
                print(f"  [{i+1}/{len(jsonl_files)}] {total_ops} facts so far...")
            fpath = os.path.join(sessions_dir, fname)
            facts = parse_session_file(fpath)
            if not dry_run:
                total_ops += upsert_facts(conn, facts)
        print(f"Done: {total_ops} facts collected")
        conn.close()
        return 0

    # Default: collect for today UTC or a range of days
    if target_date is None:
        target_dates = [(datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(args.days)]
    else:
        target_dates = [target_date]

    print(f"Collecting requests for {', '.join(target_dates)} (UTC)...")
    total_facts = 0
    total_cost = 0.0

    for fname in jsonl_files:
        fpath = os.path.join(sessions_dir, fname)
        facts = parse_session_file(fpath)

        date_facts = []
        for f in facts:
            ts_clean = f["created_at_utc"].replace("Z", "").split("+")[0]
            try:
                dt = datetime.fromisoformat(ts_clean).replace(tzinfo=None)
                if dt.strftime("%Y-%m-%d") in target_dates:
                    date_facts.append(f)
            except Exception:
                continue

        if not date_facts:
            continue

        total_facts += len(date_facts)
        total_cost += sum(x["billed_cost"] for x in date_facts)

        if not dry_run:
            upsert_facts(conn, date_facts)
            if verbose:
                print(f"  {fname}: {len(date_facts)} requests, ${sum(x['billed_cost'] for x in date_facts):.4f}")

    if total_facts == 0:
        print(f"  No requests found for {target_date}")
    else:
        print(f"Total: {total_facts} requests, ${total_cost:.4f} billed")
        if dry_run:
            print("  [dry-run — not written]")

    conn.close()
    return 0


def run_init(verbose=False):
    """First-run wizard: ensure DB exists, backfill, verify."""
    config = load_config()
    os.makedirs(CONFIG_DIR, exist_ok=True)
    conn = get_conn()
    print(f"DB: {DB_PATH}")

    sessions_dir, _ = find_sessions_dir(config)
    if not sessions_dir:
        print("ERROR: Sessions directory not found.")
        print("  Tried: ~/.openclaw/agents/main/sessions and common alternatives")
        print("  Set SESSIONS_DIR in config/env.json to override.")
        conn.close()
        return 1

    jsonl_files = list_session_files(sessions_dir)
    print(f"Sessions: {sessions_dir} ({len(jsonl_files)} files)")

    print("Running backfill...")
    total_ops = 0
    for fname in jsonl_files:
        fpath = os.path.join(sessions_dir, fname)
        facts = parse_session_file(fpath)
        total_ops += upsert_facts(conn, facts)
    print(f"Backfill done: {total_ops} facts collected")

    ok, issues = verify_db(conn)
    print("\nHealth Check:")
    for issue in issues:
        print(f"  {issue}")

    db_size_kb = os.path.getsize(DB_PATH) / 1024
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM request_facts")
    row_count = c.fetchone()[0]
    print(f"\nDB: {db_size_kb:.0f} KB, {row_count:,} rows")
    print("All good!" if ok else "See issues above")

    conn.close()
    return 0 if ok else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect OpenRouter request facts")
    parser.add_argument("--date", default=None, help="Target UTC date YYYY-MM-DD (default: today)")
    parser.add_argument("--days", type=int, default=1, help="Collect data for the last N days (default: 1)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--backfill", action="store_true", help="Scan all sessions, collect all facts")
    parser.add_argument("--verify", action="store_true", help="Verify DB health only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--init", action="store_true", help="First-run wizard: create DB, backfill, verify")
    args = parser.parse_args()

    if args.init:
        sys.exit(run_init(verbose=args.verbose))

    sys.exit(collect(
        target_date=args.date,
        dry_run=args.dry_run,
        backfill=args.backfill,
        verbose=args.verbose,
        verify_only=args.verify,
    ))
