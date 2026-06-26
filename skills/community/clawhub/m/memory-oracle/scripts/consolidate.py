#!/usr/bin/env python3
"""
memory-oracle: consolidate.py
HEAVY process — LLM-powered fact extraction from daily logs.
Uses Claude API to catch facts that rule-based capture missed.

Usage:
  consolidate.py                      # Process today's log
  consolidate.py --date 2026-03-20    # Process specific date
  consolidate.py --pending            # Process pending queue
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
from init_db import load_settings, content_hash, generate_id, utcnow

SETTINGS = load_settings()


def get_db():
    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn


def read_daily_log(target_date: str) -> str:
    """Read a daily log file."""
    logs_dir = os.path.expanduser(SETTINGS["paths"]["daily_logs"])
    log_path = os.path.join(logs_dir, f"{target_date}.md")
    if not os.path.exists(log_path):
        return ""
    with open(log_path, "r", encoding="utf-8") as f:
        return f.read()


def read_prompt(name: str) -> str:
    """Read a prompt template."""
    prompt_path = SCRIPT_DIR / "prompts" / name
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def call_claude_api(system_prompt: str, user_content: str) -> dict:
    """Call Claude API. Returns parsed JSON or None on failure."""
    import urllib.request
    import urllib.error

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set")

    payload = {
        "model": SETTINGS["api"]["model"],
        "max_tokens": SETTINGS["api"]["max_tokens"],
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_content}],
    }

    req = urllib.request.Request(
        SETTINGS["api"]["base_url"],
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=SETTINGS["api"]["timeout_seconds"]) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = ""
            for block in data.get("content", []):
                if block.get("type") == "text":
                    text += block["text"]
            # Parse JSON from response
            text = text.strip()
            # Strip markdown fences if present
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
            return json.loads(text)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"API error: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return None


def store_llm_facts(conn, facts_data: list, target_date: str) -> int:
    """Store LLM-extracted facts in SQLite."""
    now = utcnow().isoformat()
    stored = 0

    for fact in facts_data:
        if not isinstance(fact, dict):
            continue
        content = fact.get("content", "").strip()
        if not content or len(content) < 8:
            continue

        chash = content_hash(content)

        # Skip duplicates
        existing = conn.execute(
            "SELECT id, access_count, score FROM facts WHERE content_hash=? AND status='active'",
            (chash,),
        ).fetchone()
        if existing:
            # Bump — LLM also thought this was important
            conn.execute(
                "UPDATE facts SET access_count=access_count+1, score=MIN(score*1.1, ?), updated_at=? WHERE id=?",
                (SETTINGS["scoring"]["max_score"], now, existing["id"]),
            )
            continue

        fid = generate_id("llm")
        fact_type = fact.get("type", "insight")
        importance = min(fact.get("importance", 1.0), 3.0)
        confidence = min(fact.get("confidence", 0.8), 1.0)

        conn.execute(
            """INSERT INTO facts (id, type, content, content_hash, base_importance,
               score, status, source, source_session, confidence, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, 'active', 'consolidate', ?, ?, ?, ?)""",
            (fid, fact_type, content, chash, importance, importance,
             target_date, confidence, f"{target_date}T00:00:00", now),
        )

        # Auto-promote guardrails
        if fact_type == "guardrail":
            gid = generate_id("grd")
            conn.execute(
                "INSERT INTO guardrails (id, content, created_at, source) VALUES (?, ?, ?, 'consolidate')",
                (gid, content, now),
            )

        stored += 1

    conn.commit()
    return stored


def queue_pending(target_date: str, log_text: str):
    """Add to pending queue for retry."""
    pending_path = os.path.expanduser(SETTINGS["paths"]["pending_queue"])

    queue = []
    if os.path.exists(pending_path):
        with open(pending_path, "r", encoding="utf-8") as f:
            try:
                queue = json.load(f)
            except json.JSONDecodeError:
                queue = []

    queue.append({
        "task": "consolidate",
        "date": target_date,
        "log_chars": len(log_text),
        "queued_at": utcnow().isoformat(),
    })

    with open(pending_path, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)


def process_pending(conn):
    """Process any queued consolidation tasks."""
    pending_path = os.path.expanduser(SETTINGS["paths"]["pending_queue"])
    if not os.path.exists(pending_path):
        return 0

    with open(pending_path, "r", encoding="utf-8") as f:
        try:
            queue = json.load(f)
        except json.JSONDecodeError:
            return 0

    remaining = []
    processed = 0

    for item in queue:
        if item.get("task") != "consolidate":
            remaining.append(item)
            continue

        log_text = read_daily_log(item["date"])
        if not log_text:
            continue  # Drop it, log is gone

        prompt = read_prompt("consolidate.txt")
        result = call_claude_api(prompt, log_text)

        if result and isinstance(result, list):
            stored = store_llm_facts(conn, result, item["date"])
            print(f"  Pending {item['date']}: {stored} facts stored")
            processed += 1
        else:
            remaining.append(item)  # Keep for next retry

    with open(pending_path, "w", encoding="utf-8") as f:
        json.dump(remaining, f, indent=2)

    return processed


def main():
    parser = argparse.ArgumentParser(description="Memory Oracle — Consolidate")
    parser.add_argument("--date", type=str, default=None, help="Date to process (YYYY-MM-DD)")
    parser.add_argument("--pending", action="store_true", help="Process pending queue")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    target_date = args.date or date.today().isoformat()
    conn = get_db()

    results = {"date": target_date, "stored": 0, "pending_processed": 0}

    # Process pending queue first
    if args.pending or not args.date:
        results["pending_processed"] = process_pending(conn)

    # Process target date
    log_text = read_daily_log(target_date)
    if not log_text:
        results["note"] = "no daily log found"
    else:
        prompt = read_prompt("consolidate.txt")
        try:
            llm_facts = call_claude_api(prompt, log_text)
            if llm_facts and isinstance(llm_facts, list):
                results["stored"] = store_llm_facts(conn, llm_facts, target_date)
                results["extracted"] = len(llm_facts)
            else:
                queue_pending(target_date, log_text)
                results["note"] = "API failed, queued for retry"
        except EnvironmentError as e:
            queue_pending(target_date, log_text)
            results["note"] = str(e)

    conn.close()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Consolidate [{target_date}]: {results['stored']} new facts")
        if results.get("pending_processed"):
            print(f"  + {results['pending_processed']} pending tasks processed")
        if results.get("note"):
            print(f"  Note: {results['note']}")


if __name__ == "__main__":
    main()
