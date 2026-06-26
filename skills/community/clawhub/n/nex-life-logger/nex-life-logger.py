#!/usr/bin/env python3
"""
Nex Life Logger - CLI Tool
CC BY-NC 4.0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

AI-powered local activity tracker. Query your computer history via the command line.
Built by Nex AI (nex-ai.be)
"""
import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
import sys
import platform
from pathlib import Path

# Add lib directory to Python path
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SKILL_DIR, "lib")
sys.path.insert(0, LIB_DIR)

from config import DB_PATH, DATA_DIR

FOOTER = "[Nex Life Logger by Nex AI | nex-ai.be]"


def _check_db():
    """Check if the database exists. Print helpful message and exit if not."""
    if not DB_PATH.exists():
        print(
            "Life Logger database not found at %s.\n"
            "Run 'nex-life-logger service start' to begin collecting activity data."
            % DB_PATH,
            file=sys.stderr,
        )
        sys.exit(1)


def _check_llm():
    """Check if LLM is configured. Print helpful message and exit if not."""
    settings_path = DATA_DIR / "llm_settings.json"
    api_key = ""
    if settings_path.exists():
        try:
            s = json.loads(settings_path.read_text("utf-8"))
            api_key = s.get("api_key", "")
        except Exception:
            pass
    if not api_key:
        from config import AI_API_KEY
        api_key = AI_API_KEY
    if not api_key or api_key == "ollama":
        from config import AI_API_BASE
        if not AI_API_BASE:
            print(
                "LLM not configured. Run 'nex-life-logger config set-api-key' "
                "and 'nex-life-logger config set-provider <name>' first.",
                file=sys.stderr,
            )
            sys.exit(1)


def _db_conn():
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def _parse_duration(text):
    """Parse durations like '2h', '1d', '30m', '7d' into a timedelta."""
    m = re.match(r"^(\d+)\s*([hdmw])$", text.strip().lower())
    if not m:
        print("Invalid duration format: '%s'. Use e.g. 2h, 1d, 30m, 7d" % text, file=sys.stderr)
        sys.exit(1)
    val = int(m.group(1))
    unit = m.group(2)
    if unit == "m":
        return dt.timedelta(minutes=val)
    elif unit == "h":
        return dt.timedelta(hours=val)
    elif unit == "d":
        return dt.timedelta(days=val)
    elif unit == "w":
        return dt.timedelta(weeks=val)


def _print_footer():
    print("\n%s" % FOOTER)


# ============================================================
# SEARCH
# ============================================================

def cmd_search(args):
    _check_db()
    query = " ".join(args.query)
    if not query:
        print("Usage: nex-life-logger search <query> [--kind url] [--source chrome] [--limit 50] [--output json]", file=sys.stderr)
        sys.exit(1)

    sys.path.insert(0, LIB_DIR)
    from storage import (
        fts_search_activities, fts_search_transcripts,
        fts_search_summaries, fts_search_keywords,
    )

    limit = args.limit or 30
    output_json = getattr(args, "output", None) == "json"

    # Search all four tables using FTS5 (with LIKE fallback)
    act_results = fts_search_activities(
        query,
        kind=args.kind,
        source=args.source,
        since=args.since,
        until=args.until,
        limit=limit,
    )
    sum_results = fts_search_summaries(query, since=args.since, until=args.until, limit=min(limit, 10))
    kw_results = fts_search_keywords(query, category=args.category, limit=min(limit, 15))
    tr_results = fts_search_transcripts(query, since=args.since, until=args.until, limit=min(limit, 10))

    if output_json:
        payload = {
            "query": query,
            "filters": {
                "kind": args.kind,
                "source": args.source,
                "category": args.category,
                "since": args.since,
                "until": args.until,
                "limit": limit,
            },
            "activities": [{
                "timestamp": r["timestamp"][:19],
                "source": r["source"],
                "kind": r["kind"],
                "title": r.get("title") or "",
                "url": r.get("url") or "",
                "relevance": r.get("relevance", 0),
            } for r in act_results],
            "summaries": [{
                "period": r["period"],
                "date": r["start_date"],
                "snippet": (r.get("snippet") or "").replace("\n", " ")[:200],
            } for r in sum_results],
            "keywords": [{
                "keyword": r["keyword"],
                "category": r.get("category") or "",
                "frequency": r["freq"],
            } for r in kw_results],
            "transcripts": [{
                "video_id": r["video_id"],
                "title": r.get("title") or "",
                "snippet": (r.get("snippet") or "").replace("\n", " ")[:200],
            } for r in tr_results],
            "total": len(act_results) + len(sum_results) + len(kw_results) + len(tr_results),
        }
        print(json.dumps(payload, indent=2))
        return

    # Human-readable output
    print("Search results for: %s" % query)
    filters_active = []
    if args.kind:
        filters_active.append("kind=%s" % args.kind)
    if args.source:
        filters_active.append("source=%s" % args.source)
    if args.category:
        filters_active.append("category=%s" % args.category)
    if args.since:
        filters_active.append("since=%s" % args.since)
    if args.until:
        filters_active.append("until=%s" % args.until)
    if filters_active:
        print("Filters: %s" % ", ".join(filters_active))
    print("---")

    if act_results:
        print("\nActivities (%d matches):" % len(act_results))
        for r in act_results:
            ts = r["timestamp"][:19]
            rel = r.get("relevance", 0)
            title = (r.get("title") or "")[:100]
            print("- [%s] %s (%s) %s [rel: %.2f]" % (ts, r["kind"], r["source"], title, rel))

    if sum_results:
        print("\nSummaries (%d matches):" % len(sum_results))
        for r in sum_results:
            snippet = (r.get("snippet") or "").replace("\n", " ")[:120]
            print("- [%s] %s: %s..." % (r["start_date"], r["period"], snippet))

    if kw_results:
        print("\nKeywords (%d matches):" % len(kw_results))
        for r in kw_results:
            print("- %s (%s) frequency: %d" % (r["keyword"], r.get("category") or "?", r["freq"]))

    if tr_results:
        print("\nTranscripts (%d matches):" % len(tr_results))
        for r in tr_results:
            snippet = (r.get("snippet") or "").replace("\n", " ")[:100]
            print("- [%s] %s: %s..." % (r["video_id"], r.get("title") or "?", snippet))

    total = len(act_results) + len(sum_results) + len(kw_results) + len(tr_results)
    if total == 0:
        print("No results found.")
    else:
        print("\nTotal: %d results" % total)

    _print_footer()


# ============================================================
# SUMMARY
# ============================================================

def cmd_summary(args):
    _check_db()
    period = args.period
    conn = _db_conn()

    if args.date:
        target = args.date
    else:
        today = dt.date.today()
        if period == "daily":
            target = today.isoformat()
        elif period == "weekly":
            monday = today - dt.timedelta(days=today.weekday())
            target = monday.isoformat()
        elif period == "monthly":
            target = today.replace(day=1).isoformat()
        elif period == "yearly":
            target = today.replace(month=1, day=1).isoformat()
        else:
            print("Unknown period: %s" % period, file=sys.stderr)
            sys.exit(1)

    row = conn.execute(
        "SELECT content, start_date, end_date FROM summaries WHERE period = ? AND start_date = ?",
        (period, target),
    ).fetchone()
    conn.close()

    if row:
        print("%s Summary: %s to %s" % (period.capitalize(), row["start_date"], row["end_date"]))
        print("---")
        print(row["content"])
    else:
        print("No %s summary found for %s." % (period, target))
        print("Run 'nex-life-logger generate %s' to create one." % period)

    _print_footer()


# ============================================================
# ACTIVITIES
# ============================================================

def cmd_activities(args):
    _check_db()
    conn = _db_conn()

    now = dt.datetime.now(dt.timezone.utc)
    if args.last:
        delta = _parse_duration(args.last)
        start = (now - delta).isoformat()
        end = now.isoformat()
    elif args.since:
        start = args.since
        end = args.until or now.isoformat()
    else:
        start = (now - dt.timedelta(hours=24)).isoformat()
        end = now.isoformat()

    sql = "SELECT timestamp, source, kind, title, url, extra FROM activities WHERE timestamp >= ? AND timestamp < ?"
    params = [start, end]

    if args.kind:
        sql += " AND kind = ?"
        params.append(args.kind)

    sql += " ORDER BY timestamp DESC LIMIT 50"
    rows = conn.execute(sql, params).fetchall()
    conn.close()

    print("Activities (%d results)" % len(rows))
    print("---")
    for r in rows:
        ts = r["timestamp"][:19]
        extra = {}
        try:
            extra = json.loads(r["extra"] or "{}")
        except Exception:
            pass
        if r["kind"] == "search":
            print("- [%s] SEARCH: %s" % (ts, extra.get("search_query", "")))
        elif r["kind"] == "youtube":
            print("- [%s] YOUTUBE: %s (video: %s)" % (ts, r["title"] or "", extra.get("video_id", "")))
        elif r["kind"] == "app_focus":
            print("- [%s] APP: %s - %s" % (ts, extra.get("process", ""), r["title"] or ""))
        else:
            print("- [%s] WEB [%s]: %s" % (ts, r["source"], r["title"] or r["url"] or ""))

    if not rows:
        print("No activities found for the specified time range.")

    _print_footer()


# ============================================================
# KEYWORDS
# ============================================================

def cmd_keywords(args):
    _check_db()
    conn = _db_conn()
    limit = args.top or 20

    sql = "SELECT keyword, category, SUM(frequency) as total_freq, COUNT(DISTINCT source_date) as days_seen FROM keywords"
    params = []
    conditions = []

    if args.category:
        conditions.append("category = ?")
        params.append(args.category)
    if args.since:
        conditions.append("source_date >= ?")
        params.append(args.since)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " GROUP BY keyword ORDER BY total_freq DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    print("Top %d Keywords" % limit)
    print("---")
    for r in rows:
        print("- %s (%s) frequency: %d, days: %d" % (
            r["keyword"], r["category"] or "?", r["total_freq"], r["days_seen"]
        ))

    if not rows:
        print("No keywords found.")

    _print_footer()


# ============================================================
# TRANSCRIPT
# ============================================================

def cmd_transcript(args):
    _check_db()
    conn = _db_conn()
    row = conn.execute(
        "SELECT video_id, title, transcript FROM transcripts WHERE video_id = ?",
        (args.video_id,),
    ).fetchone()
    conn.close()

    if row:
        print("Transcript: %s" % (row["title"] or row["video_id"]))
        print("Video ID: %s" % row["video_id"])
        print("---")
        print(row["transcript"][:10000])
        if len(row["transcript"]) > 10000:
            print("\n... (truncated, full transcript is %d chars)" % len(row["transcript"]))
    else:
        print("No transcript found for video ID: %s" % args.video_id)

    _print_footer()


def cmd_transcripts(args):
    _check_db()
    conn = _db_conn()

    now = dt.datetime.now(dt.timezone.utc)
    if args.last:
        delta = _parse_duration(args.last)
        start = (now - delta).isoformat()
    else:
        start = (now - dt.timedelta(days=7)).isoformat()

    rows = conn.execute(
        """SELECT t.video_id, t.title, LENGTH(t.transcript) as size, a.timestamp
           FROM transcripts t
           JOIN activities a ON json_extract(a.extra, '$.video_id') = t.video_id
           WHERE a.kind = 'youtube' AND a.timestamp >= ?
           ORDER BY a.timestamp DESC LIMIT 30""",
        (start,),
    ).fetchall()
    conn.close()

    print("Recent Transcripts (%d)" % len(rows))
    print("---")
    for r in rows:
        size_kb = (r["size"] or 0) / 1024
        print("- [%s] %s (%s) %.1f KB" % (
            r["timestamp"][:19], r["title"] or "?", r["video_id"], size_kb
        ))

    if not rows:
        print("No recent transcripts found.")

    _print_footer()


# ============================================================
# STATS
# ============================================================

def cmd_stats(args):
    _check_db()
    conn = _db_conn()

    if args.date:
        day_start = args.date + "T00:00:00"
        day_end = args.date + "T23:59:59"
        total = conn.execute(
            "SELECT COUNT(*) FROM activities WHERE timestamp >= ? AND timestamp <= ?",
            (day_start, day_end),
        ).fetchone()[0]
        by_kind = conn.execute(
            "SELECT kind, COUNT(*) as cnt FROM activities WHERE timestamp >= ? AND timestamp <= ? GROUP BY kind ORDER BY cnt DESC",
            (day_start, day_end),
        ).fetchall()
        by_source = conn.execute(
            "SELECT source, COUNT(*) as cnt FROM activities WHERE timestamp >= ? AND timestamp <= ? GROUP BY source ORDER BY cnt DESC",
            (day_start, day_end),
        ).fetchall()
        kw_count = conn.execute(
            "SELECT COUNT(DISTINCT keyword) FROM keywords WHERE source_date = ?",
            (args.date,),
        ).fetchone()[0]
        conn.close()

        print("Stats for %s" % args.date)
        print("---")
        print("Total activities: %d" % total)
        print("Unique keywords: %d" % kw_count)
        print("\nBy type:")
        for r in by_kind:
            print("  %s: %d" % (r["kind"], r["cnt"]))
        print("\nBy source:")
        for r in by_source:
            print("  %s: %d" % (r["source"], r["cnt"]))

    else:
        total_act = conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0]
        total_sum = conn.execute("SELECT COUNT(*) FROM summaries").fetchone()[0]
        total_kw = conn.execute("SELECT COUNT(DISTINCT keyword) FROM keywords").fetchone()[0]
        try:
            total_tr = conn.execute("SELECT COUNT(*) FROM transcripts").fetchone()[0]
        except Exception:
            total_tr = 0
        date_range = conn.execute(
            "SELECT MIN(DATE(timestamp)), MAX(DATE(timestamp)) FROM activities"
        ).fetchone()
        by_kind = conn.execute(
            "SELECT kind, COUNT(*) as cnt FROM activities GROUP BY kind ORDER BY cnt DESC LIMIT 5"
        ).fetchall()
        by_source = conn.execute(
            "SELECT source, COUNT(*) as cnt FROM activities GROUP BY source ORDER BY cnt DESC LIMIT 5"
        ).fetchall()
        conn.close()

        db_size = 0
        if DB_PATH.exists():
            db_size = DB_PATH.stat().st_size

        print("Nex Life Logger Statistics")
        print("---")
        print("Total activities: %d" % total_act)
        print("Total summaries: %d" % total_sum)
        print("Total keywords: %d" % total_kw)
        print("Total transcripts: %d" % total_tr)
        if date_range[0]:
            print("Date range: %s to %s" % (date_range[0], date_range[1]))
        print("Database size: %.1f MB" % (db_size / 1024 / 1024))
        print("\nTop sources:")
        for r in by_source:
            print("  %s: %d" % (r["source"], r["cnt"]))
        print("\nTop types:")
        for r in by_kind:
            print("  %s: %d" % (r["kind"], r["cnt"]))

    _print_footer()


# ============================================================
# GENERATE
# ============================================================

def cmd_generate(args):
    _check_db()
    _check_llm()

    import user_filters
    user_filters.init(DATA_DIR)

    period = args.period
    today = dt.date.today()

    if period == "daily":
        from summarizer import generate_daily_summary
        target = dt.date.fromisoformat(args.date) if args.date else today - dt.timedelta(days=1)
        print("Generating daily summary for %s..." % target)
        result = generate_daily_summary(target)
        if result:
            print("---")
            print(result)
        else:
            print("No activities found for %s. Nothing to summarize." % target)

    elif period == "weekly":
        from summarizer import generate_weekly_summary
        if args.date:
            monday = dt.date.fromisoformat(args.date)
        else:
            monday = today - dt.timedelta(days=today.weekday() + 7)
        print("Generating weekly summary for week of %s..." % monday)
        result = generate_weekly_summary(monday)
        if result:
            print("---")
            print(result)
        else:
            print("No daily summaries found for that week. Generate daily summaries first.")

    elif period == "monthly":
        from summarizer import generate_monthly_summary
        if args.date:
            d = dt.date.fromisoformat(args.date)
            year, month = d.year, d.month
        else:
            prev = today.replace(day=1) - dt.timedelta(days=1)
            year, month = prev.year, prev.month
        print("Generating monthly summary for %d-%02d..." % (year, month))
        result = generate_monthly_summary(year, month)
        if result:
            print("---")
            print(result)
        else:
            print("No weekly summaries found for that month. Generate weekly summaries first.")

    elif period == "yearly":
        from summarizer import generate_yearly_summary
        year = int(args.date[:4]) if args.date else today.year - 1
        print("Generating yearly summary for %d..." % year)
        result = generate_yearly_summary(year)
        if result:
            print("---")
            print(result)
        else:
            print("No monthly summaries found for %d. Generate monthly summaries first." % year)

    else:
        print("Unknown period: %s" % period, file=sys.stderr)
        sys.exit(1)

    _print_footer()


# ============================================================
# EXPORT
# ============================================================

def cmd_export(args):
    _check_db()

    import user_filters
    user_filters.init(DATA_DIR)

    fmt = args.format
    output = args.output

    if not output:
        output = "life-logger-export.%s" % fmt

    from exporter import export_json, export_csv, export_html

    if fmt == "json":
        path = export_json(output)
        print("Exported to %s" % path)
    elif fmt == "csv":
        path = export_csv(output)
        print("Exported to %s" % path)
    elif fmt == "html":
        path = export_html(output)
        print("Exported to %s" % path)
    else:
        print("Unknown format: %s. Use json, csv, or html." % fmt, file=sys.stderr)
        sys.exit(1)

    _print_footer()


# ============================================================
# SERVICE
# ============================================================

def cmd_service(args):
    action = args.action
    system = platform.system()

    if action == "status":
        if system == "Linux":
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "nex-life-logger"],
                capture_output=True, text=True,
            )
            status = result.stdout.strip()
            if status == "active":
                print("Collector status: RUNNING")
            else:
                print("Collector status: STOPPED")
                print("Start with: nex-life-logger service start")
        elif system == "Darwin":
            result = subprocess.run(
                ["launchctl", "list"],
                capture_output=True, text=True,
            )
            if "com.nexai.life-logger" in result.stdout:
                print("Collector status: RUNNING")
            else:
                print("Collector status: STOPPED")
                print("Start with: nex-life-logger service start")
        else:
            print("Service management is available on Linux and macOS.")
            print("On Windows, run the collector manually:")
            print("  python %s/lib/collector_headless.py" % SKILL_DIR)

    elif action == "start":
        if system == "Linux":
            subprocess.run(["systemctl", "--user", "start", "nex-life-logger"])
            print("Collector started.")
        elif system == "Darwin":
            plist = os.path.expanduser("~/Library/LaunchAgents/com.nexai.life-logger.plist")
            if os.path.exists(plist):
                subprocess.run(["launchctl", "load", plist])
                print("Collector started.")
            else:
                print("LaunchAgent plist not found. Run setup.sh first.", file=sys.stderr)
                sys.exit(1)
        else:
            print("On Windows, run the collector manually:")
            print("  python %s/lib/collector_headless.py" % SKILL_DIR)

    elif action == "stop":
        if system == "Linux":
            subprocess.run(["systemctl", "--user", "stop", "nex-life-logger"])
            print("Collector stopped.")
        elif system == "Darwin":
            plist = os.path.expanduser("~/Library/LaunchAgents/com.nexai.life-logger.plist")
            if os.path.exists(plist):
                subprocess.run(["launchctl", "unload", plist])
                print("Collector stopped.")
            else:
                print("LaunchAgent plist not found.", file=sys.stderr)
                sys.exit(1)
        else:
            print("On Windows, stop the collector manually (Ctrl+C in the terminal).")

    elif action == "logs":
        if system == "Linux":
            subprocess.run(
                ["journalctl", "--user", "-u", "nex-life-logger", "-n", "50", "--no-pager"],
            )
        elif system == "Darwin":
            log_path = os.path.expanduser("~/.life-logger/collector.log")
            if os.path.exists(log_path):
                subprocess.run(["tail", "-50", log_path])
            else:
                print("No log file found at %s" % log_path)
        else:
            log_path = os.path.expanduser("~/.life-logger/life-logger.log")
            if os.path.exists(log_path):
                with open(log_path, "r") as f:
                    lines = f.readlines()
                    for line in lines[-50:]:
                        print(line, end="")
            else:
                print("No log file found at %s" % log_path)

    else:
        print("Unknown action: %s. Use status, start, stop, or logs." % action, file=sys.stderr)
        sys.exit(1)

    _print_footer()


# ============================================================
# CONFIG
# ============================================================

def cmd_config(args):
    action = args.action

    if action == "show":
        settings_path = DATA_DIR / "llm_settings.json"
        print("Nex Life Logger Configuration")
        print("---")
        print("Data directory: %s" % DATA_DIR)
        print("Database: %s" % DB_PATH)
        if DB_PATH.exists():
            print("Database size: %.1f MB" % (DB_PATH.stat().st_size / 1024 / 1024))
        else:
            print("Database: not created yet")

        if settings_path.exists():
            try:
                s = json.loads(settings_path.read_text("utf-8"))
                api_key = s.get("api_key", "")
                print("\nLLM Provider: %s" % s.get("provider", "custom"))
                print("API Base: %s" % s.get("api_base", "not set"))
                print("Model: %s" % s.get("model", "not set"))
                if api_key:
                    print("API Key: %s...%s" % (api_key[:8], api_key[-4:]))
                else:
                    print("API Key: not set")
            except Exception:
                print("\nLLM: configuration file exists but could not be read")
        else:
            print("\nLLM: not configured")
            print("Run 'nex-life-logger config set-api-key' to configure.")

        if settings_path.exists():
            try:
                s = json.loads(settings_path.read_text("utf-8"))
                poll = s.get("poll_interval")
                if poll:
                    print("Poll interval: %d seconds" % poll)
            except Exception:
                pass

        filters_path = DATA_DIR / "user_filters.json"
        if filters_path.exists():
            print("\nCustom filters: active")
        else:
            print("\nCustom filters: using defaults")

    elif action == "set-api-key":
        key = input("Enter your AI API key: ").strip()
        if not key:
            print("No key provided.", file=sys.stderr)
            sys.exit(1)
        from secure_key import store_api_key
        store_api_key(key)
        settings_path = DATA_DIR / "llm_settings.json"
        settings = {}
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text("utf-8"))
            except Exception:
                pass
        settings["api_key"] = key
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2), "utf-8")
        print("API key stored securely (%s...)" % key[:8])

    elif action == "set-provider":
        if not args.value:
            print("Usage: nex-life-logger config set-provider <name>", file=sys.stderr)
            print("Available providers: openai, qwen, groq, ollama, custom", file=sys.stderr)
            sys.exit(1)
        provider = args.value
        presets = {
            "openai": ("https://api.openai.com/v1", "gpt-4o"),
            "qwen": ("https://dashscope-us.aliyuncs.com/compatible-mode/v1", "qwen-plus"),
            "groq": ("https://api.groq.com/openai/v1", "llama-3.1-70b-versatile"),
            "ollama": ("http://localhost:11434/v1", "llama3"),
        }
        settings_path = DATA_DIR / "llm_settings.json"
        settings = {}
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text("utf-8"))
            except Exception:
                pass
        settings["provider"] = provider
        if provider in presets:
            settings["api_base"] = presets[provider][0]
            settings["model"] = presets[provider][1]
            print("Provider set to: %s" % provider)
            print("API Base: %s" % settings["api_base"])
            print("Model: %s" % settings["model"])
        else:
            print("Provider set to: %s (custom)" % provider)
            print("Set API base with: nex-life-logger config set-model <url>")
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2), "utf-8")

    elif action == "set-model":
        if not args.value:
            print("Usage: nex-life-logger config set-model <model-name>", file=sys.stderr)
            sys.exit(1)
        settings_path = DATA_DIR / "llm_settings.json"
        settings = {}
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text("utf-8"))
            except Exception:
                pass
        settings["model"] = args.value
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2), "utf-8")
        print("Model set to: %s" % args.value)

    elif action == "set-api-base":
        if not args.value:
            print("Usage: nex-life-logger config set-api-base <url>", file=sys.stderr)
            sys.exit(1)
        settings_path = DATA_DIR / "llm_settings.json"
        settings = {}
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text("utf-8"))
            except Exception:
                pass
        settings["api_base"] = args.value
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2), "utf-8")
        print("API base set to: %s" % args.value)

    elif action == "set-poll-interval":
        if not args.value:
            print("Usage: nex-life-logger config set-poll-interval <seconds>", file=sys.stderr)
            sys.exit(1)
        try:
            interval = int(args.value)
            if interval < 5 or interval > 3600:
                print("Poll interval must be between 5 and 3600 seconds.", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print("Poll interval must be a number in seconds.", file=sys.stderr)
            sys.exit(1)
        settings_path = DATA_DIR / "llm_settings.json"
        settings = {}
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text("utf-8"))
            except Exception:
                pass
        settings["poll_interval"] = interval
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2), "utf-8")
        print("Poll interval set to: %d seconds" % interval)

    elif action == "rebuild-fts":
        _check_db()
        sys.path.insert(0, LIB_DIR)
        from storage import rebuild_fts
        print("Rebuilding FTS5 search indexes...")
        rebuild_fts()
        print("FTS5 indexes rebuilt successfully.")

    else:
        print("Unknown config action: %s" % action, file=sys.stderr)
        print("Available: show, set-api-key, set-provider, set-model, set-api-base, set-poll-interval, rebuild-fts", file=sys.stderr)
        sys.exit(1)

    _print_footer()


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        prog="nex-life-logger",
        description="Nex Life Logger - AI-powered local activity tracker. Built by Nex AI (nex-ai.be)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # search
    p_search = subparsers.add_parser("search", help="Search across all tracked data (FTS5 powered)")
    p_search.add_argument("query", nargs="+", help="Search terms")
    p_search.add_argument("--since", help="Start date (ISO format)")
    p_search.add_argument("--until", help="End date (ISO format)")
    p_search.add_argument("--kind", choices=["url", "search", "youtube", "app_focus"], help="Filter activities by type")
    p_search.add_argument("--source", help="Filter activities by source (chrome, edge, brave, firefox, window)")
    p_search.add_argument("--category", choices=["topic", "tool", "language", "project", "domain", "search"], help="Filter keywords by category")
    p_search.add_argument("--limit", type=int, help="Max results per section (default: 30)")
    p_search.add_argument("--output", choices=["text", "json"], default="text", help="Output format (default: text)")
    p_search.set_defaults(func=cmd_search)

    # summary
    p_summary = subparsers.add_parser("summary", help="View AI-generated summaries")
    p_summary.add_argument("period", choices=["daily", "weekly", "monthly", "yearly"])
    p_summary.add_argument("--date", help="Specific date (ISO format)")
    p_summary.set_defaults(func=cmd_summary)

    # activities
    p_act = subparsers.add_parser("activities", help="View recent activities")
    p_act.add_argument("--last", help="Time window (e.g. 2h, 1d, 7d)")
    p_act.add_argument("--since", help="Start timestamp (ISO format)")
    p_act.add_argument("--until", help="End timestamp (ISO format)")
    p_act.add_argument("--kind", choices=["url", "search", "youtube", "app_focus"], help="Filter by type")
    p_act.set_defaults(func=cmd_activities)

    # keywords
    p_kw = subparsers.add_parser("keywords", help="View extracted keywords and topics")
    p_kw.add_argument("--top", type=int, help="Number of keywords (default: 20)")
    p_kw.add_argument("--category", choices=["topic", "tool", "language", "project", "domain", "search"])
    p_kw.add_argument("--since", help="Start date (ISO format)")
    p_kw.set_defaults(func=cmd_keywords)

    # transcript
    p_tr = subparsers.add_parser("transcript", help="Get a specific YouTube transcript")
    p_tr.add_argument("video_id", help="YouTube video ID")
    p_tr.set_defaults(func=cmd_transcript)

    # transcripts
    p_trs = subparsers.add_parser("transcripts", help="List recent transcripts")
    p_trs.add_argument("--last", help="Time window (e.g. 7d, 30d)", default="7d")
    p_trs.set_defaults(func=cmd_transcripts)

    # stats
    p_stats = subparsers.add_parser("stats", help="Database statistics")
    p_stats.add_argument("--date", help="Stats for a specific date (ISO format)")
    p_stats.set_defaults(func=cmd_stats)

    # generate
    p_gen = subparsers.add_parser("generate", help="Generate AI summaries on demand")
    p_gen.add_argument("period", choices=["daily", "weekly", "monthly", "yearly"])
    p_gen.add_argument("--date", help="Target date (ISO format)")
    p_gen.set_defaults(func=cmd_generate)

    # export
    p_exp = subparsers.add_parser("export", help="Export data to file")
    p_exp.add_argument("format", choices=["json", "csv", "html"])
    p_exp.add_argument("--output", help="Output file path")
    p_exp.set_defaults(func=cmd_export)

    # service
    p_svc = subparsers.add_parser("service", help="Manage background collector service")
    p_svc.add_argument("action", choices=["status", "start", "stop", "logs"])
    p_svc.set_defaults(func=cmd_service)

    # config
    p_cfg = subparsers.add_parser("config", help="View and manage configuration")
    p_cfg.add_argument("action", choices=["show", "set-api-key", "set-provider", "set-model", "set-api-base", "set-poll-interval", "rebuild-fts"])
    p_cfg.add_argument("value", nargs="?", help="Value for set commands")
    p_cfg.set_defaults(func=cmd_config)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        print("Need help? Visit nex-ai.be or open an issue on GitHub.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
