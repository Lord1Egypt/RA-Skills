#!/usr/bin/env python3
"""
memory-oracle: reflect.py
HEAVY process — adaptive reflection over memory.
Light mode (daily): analyze today vs existing memory.
Deep mode (weekly): 7-day trend analysis.

Usage:
  reflect.py --light                    # Daily reflection
  reflect.py --deep                     # Weekly deep reflection
  reflect.py --auto                     # Auto-detect (deep on configured day)
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
from init_db import load_settings, generate_id, utcnow, content_hash

SETTINGS = load_settings()


def get_db():
    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn


def read_prompt(name: str) -> str:
    prompt_path = SCRIPT_DIR / "prompts" / name
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def call_claude_api(system_prompt: str, user_content: str) -> dict:
    """Call Claude API. Returns parsed JSON or None."""
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
            text = text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
            return json.loads(text)
    except Exception as e:
        print(f"API/parse error: {e}", file=sys.stderr)
        return None


def get_today_facts(conn) -> list:
    """Get facts created today."""
    today = date.today().isoformat()
    rows = conn.execute(
        """SELECT id, type, content, base_importance, score, created_at
           FROM facts WHERE status='active' AND created_at >= ?
           ORDER BY base_importance DESC""",
        (f"{today}T00:00:00",),
    ).fetchall()
    return [dict(r) for r in rows]


def get_memory_facts(conn, limit: int = 100) -> list:
    """Get top memory facts by score."""
    rows = conn.execute(
        """SELECT id, type, content, base_importance, score, access_count, created_at
           FROM facts WHERE status='active'
           ORDER BY score DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_recent_reflections(conn, days: int) -> list:
    """Get reflections from the last N days."""
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    rows = conn.execute(
        """SELECT date, mode, raw_output, confidence
           FROM reflections WHERE date >= ? AND applied=1
           ORDER BY date ASC""",
        (cutoff,),
    ).fetchall()
    results = []
    for r in rows:
        try:
            parsed = json.loads(r["raw_output"])
            parsed["_date"] = r["date"]
            parsed["_confidence"] = r["confidence"]
            results.append(parsed)
        except json.JSONDecodeError:
            continue
    return results


def get_access_log_week(conn) -> list:
    """Get access log for the last 7 days."""
    cutoff = (utcnow() - timedelta(days=7)).isoformat()
    rows = conn.execute(
        """SELECT fact_id, COUNT(*) as access_count
           FROM access_log WHERE accessed_at >= ?
           GROUP BY fact_id ORDER BY access_count DESC""",
        (cutoff,),
    ).fetchall()
    return [dict(r) for r in rows]


def apply_reflection(conn, reflection: dict, mode: str):
    """Apply score modifications from reflection output."""
    now = utcnow().isoformat()

    def safe_list(key):
        """Get a list from reflection dict, return [] if missing/None/wrong type."""
        val = reflection.get(key, [])
        return val if isinstance(val, list) else []

    def safe_dict(key):
        """Get a dict from reflection dict, return {} if missing/None/wrong type."""
        val = reflection.get(key, {})
        return val if isinstance(val, dict) else {}

    # Process contradictions
    for c in safe_list("contradictions"):
        old_id = c.get("old_fact_id")
        if old_id:
            conn.execute(
                "UPDATE facts SET status='superseded', score=score*?, updated_at=? WHERE id=?",
                (SETTINGS["scoring"]["superseded_multiplier"], now, old_id),
            )

    # Process priority shifts
    for p in safe_list("priority_shifts"):
        direction = p.get("direction")
        topic = p.get("topic", "")
        if not topic:
            continue

        mult = (
            SETTINGS["scoring"]["priority_boost_multiplier"]
            if direction == "boost"
            else SETTINGS["scoring"]["priority_decay_multiplier"]
        )
        # Apply to facts matching the topic via FTS
        try:
            matching = conn.execute(
                """SELECT f.id FROM facts_fts
                   JOIN facts f ON facts_fts.rowid = f.rowid
                   WHERE facts_fts MATCH ? AND f.status='active'""",
                (topic,),
            ).fetchall()
            for m in matching:
                conn.execute(
                    "UPDATE facts SET score=MIN(MAX(score*?, ?), ?), updated_at=? WHERE id=?",
                    (mult, SETTINGS["scoring"]["min_score"],
                     SETTINGS["scoring"]["max_score"], now, m["id"]),
                )
        except sqlite3.OperationalError:
            pass

    # Process patterns — create synthetic meta-facts
    for p in safe_list("patterns"):
        meta = p.get("suggested_meta_fact")
        if meta:

            chash = content_hash(meta)
            existing = conn.execute(
                "SELECT id FROM facts WHERE content_hash=?", (chash,)
            ).fetchone()
            if not existing:
                fid = generate_id("meta")
                conn.execute(
                    """INSERT INTO facts (id, type, content, content_hash, base_importance,
                       score, status, source, confidence, created_at, updated_at)
                       VALUES (?, 'pattern', ?, ?, ?, ?, 'active', 'reflection', 0.85, ?, ?)""",
                    (fid, meta, chash,
                     SETTINGS["scoring"]["new_topic_boost"],
                     SETTINGS["scoring"]["pattern_meta_score"],
                     now, now),
                )

    # Deep mode: process memory hygiene
    hygiene = safe_dict("memory_hygiene")

    # Merge candidates
    for merge in (hygiene.get("merge_candidates") or []):
        merged_content = merge.get("merged_content")
        fact_ids = merge.get("fact_ids", [])
        if merged_content and len(fact_ids) >= 2:

            chash = content_hash(merged_content)
            # Archive old facts
            for fid in fact_ids:
                conn.execute(
                    "UPDATE facts SET status='merged', updated_at=? WHERE id=?",
                    (now, fid),
                )
            # Create merged fact
            new_id = generate_id("mrg")
            conn.execute(
                """INSERT INTO facts (id, type, content, content_hash, base_importance,
                   score, status, source, confidence, created_at, updated_at)
                   VALUES (?, 'insight', ?, ?, 1.5, 2.0, 'active', 'merge', 0.9, ?, ?)""",
                (new_id, merged_content, chash, now, now),
            )

    # Promotion candidates
    for promo in (hygiene.get("promotion_candidates") or []):
        fid = promo.get("fact_id")
        promote_to = promo.get("promote_to")
        if fid and promote_to == "guardrail":
            row = conn.execute("SELECT content FROM facts WHERE id=?", (fid,)).fetchone()
            if row:
                gid = generate_id("grd")
                conn.execute(
                    "INSERT OR IGNORE INTO guardrails (id, content, created_at, source) VALUES (?, ?, ?, 'reflection')",
                    (gid, row["content"], now),
                )

    # Topic heatmap (deep mode)
    for item in safe_list("topic_heatmap"):
        delta = item.get("score_delta_recommendation", 0)
        topic = item.get("topic", "")
        if not topic or abs(delta) < 0.1:
            continue
        try:
            matching = conn.execute(
                """SELECT f.id, f.score FROM facts_fts
                   JOIN facts f ON facts_fts.rowid = f.rowid
                   WHERE facts_fts MATCH ? AND f.status='active'""",
                (topic,),
            ).fetchall()
            for m in matching:
                new_score = max(SETTINGS["scoring"]["min_score"],
                                min(m["score"] + delta, SETTINGS["scoring"]["max_score"]))
                conn.execute(
                    "UPDATE facts SET score=?, updated_at=? WHERE id=?",
                    (new_score, now, m["id"]),
                )
        except sqlite3.OperationalError:
            pass

    conn.commit()


def save_reflection(conn, reflection: dict, mode: str, applied: bool):
    """Save reflection to database and markdown digest."""
    now = utcnow().isoformat()
    today = date.today().isoformat()
    rid = generate_id("ref")
    confidence = reflection.get("confidence", 0.0)

    conn.execute(
        """INSERT INTO reflections (id, date, mode, confidence, raw_output, applied, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (rid, today, mode, confidence, json.dumps(reflection, ensure_ascii=False),
         1 if applied else 0, now),
    )
    conn.commit()

    # Write human-readable digest
    summary = reflection.get("daily_summary") or reflection.get("strategic_summary", "")
    if summary:
        reflections_dir = os.path.expanduser(SETTINGS["paths"]["reflections"])
        os.makedirs(reflections_dir, exist_ok=True)
        digest_path = os.path.join(reflections_dir, f"{today}-reflection.md")
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(f"# Reflection — {today} ({mode})\n\n")
            f.write(f"{summary}\n\n")
            if reflection.get("contradictions"):
                f.write(f"**Contradictions found:** {len(reflection['contradictions'])}\n")
            if reflection.get("new_topics"):
                f.write(f"**New topics:** {len(reflection['new_topics'])}\n")
            if reflection.get("patterns"):
                f.write(f"**Patterns detected:** {len(reflection['patterns'])}\n")
            if reflection.get("weekly_trends"):
                f.write(f"**Weekly trends:** {len(reflection['weekly_trends'])}\n")
            f.write(f"\nConfidence: {confidence:.2f}\n")


def save_failed(reflection_raw, mode: str, error: str):
    """Save failed reflection for debugging."""
    failed_dir = os.path.expanduser(SETTINGS["paths"]["failed_reflections"])
    os.makedirs(failed_dir, exist_ok=True)
    today = date.today().isoformat()
    path = os.path.join(failed_dir, f"{today}-{mode}-failed.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"error": error, "raw": reflection_raw, "timestamp": utcnow().isoformat()}, f, indent=2)


def run_light(conn) -> dict:
    """Daily light reflection."""
    today_facts = get_today_facts(conn)
    memory_facts = get_memory_facts(conn)
    last_reflection = get_recent_reflections(conn, 1)

    if not today_facts:
        return {"mode": "light", "skipped": True, "reason": "no new facts today"}

    prompt = read_prompt("reflect_light.txt")
    user_content = json.dumps({
        "TODAY_FACTS": today_facts,
        "MEMORY_FACTS": memory_facts[:50],
        "LAST_REFLECTION": last_reflection[-1] if last_reflection else None,
    }, ensure_ascii=False)

    result = call_claude_api(prompt, user_content)

    if not result or not isinstance(result, dict):
        save_failed(result, "light", "Invalid response structure")
        return {"mode": "light", "error": "invalid response", "stored": True}

    confidence = result.get("confidence", 0.0)
    applied = confidence >= SETTINGS["reflection"]["confidence_threshold"]

    if applied:
        apply_reflection(conn, result, "light")

    save_reflection(conn, result, "light", applied)

    return {
        "mode": "light",
        "confidence": confidence,
        "applied": applied,
        "contradictions": len(result.get("contradictions", [])),
        "new_topics": len(result.get("new_topics", [])),
        "patterns": len(result.get("patterns", [])),
        "stale_candidates": len(result.get("stale_candidates", [])),
    }


def run_deep(conn) -> dict:
    """Weekly deep reflection."""
    week_reflections = get_recent_reflections(conn, SETTINGS["reflection"]["deep_lookback_days"])
    memory_facts = get_memory_facts(conn, 150)
    access_log = get_access_log_week(conn)

    if not week_reflections:
        return {"mode": "deep", "skipped": True, "reason": "no weekly data"}

    prompt = read_prompt("reflect_deep.txt")
    user_content = json.dumps({
        "WEEK_REFLECTIONS": week_reflections,
        "MEMORY_FACTS": memory_facts,
        "FACT_ACCESS_LOG": access_log[:50],
    }, ensure_ascii=False)

    result = call_claude_api(prompt, user_content)

    if not result or not isinstance(result, dict):
        save_failed(result, "deep", "Invalid response structure")
        return {"mode": "deep", "error": "invalid response", "stored": True}

    confidence = result.get("confidence", 0.0)
    applied = confidence >= SETTINGS["reflection"]["confidence_threshold"]

    if applied:
        apply_reflection(conn, result, "deep")

    save_reflection(conn, result, "deep", applied)

    return {
        "mode": "deep",
        "confidence": confidence,
        "applied": applied,
        "trends": len(result.get("weekly_trends", [])),
        "merges": len(result.get("memory_hygiene", {}).get("merge_candidates", [])),
        "promotions": len(result.get("memory_hygiene", {}).get("promotion_candidates", [])),
        "archives": len(result.get("memory_hygiene", {}).get("archive_candidates", [])),
    }


def main():
    parser = argparse.ArgumentParser(description="Memory Oracle — Reflect")
    parser.add_argument("--light", action="store_true", help="Daily light reflection")
    parser.add_argument("--deep", action="store_true", help="Weekly deep reflection")
    parser.add_argument("--auto", action="store_true", help="Auto-detect mode")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not any([args.light, args.deep, args.auto]):
        args.auto = True

    conn = get_db()

    if args.auto:
        deep_day = SETTINGS["reflection"]["deep_day_of_week"]
        if date.today().weekday() == deep_day:
            mode = "deep"
        else:
            mode = "light"
    elif args.deep:
        mode = "deep"
    else:
        mode = "light"

    try:
        if mode == "deep":
            result = run_deep(conn)
        else:
            result = run_light(conn)
    except EnvironmentError as e:
        result = {"mode": mode, "error": str(e)}

    conn.close()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("skipped"):
            print(f"Reflect [{mode}]: skipped — {result.get('reason')}")
        elif result.get("error"):
            print(f"Reflect [{mode}]: error — {result.get('error')}")
        else:
            print(f"Reflect [{mode}]: confidence={result.get('confidence', 0):.2f}, applied={result.get('applied')}")
            if mode == "light":
                print(f"  Contradictions: {result.get('contradictions', 0)}, "
                      f"New topics: {result.get('new_topics', 0)}, "
                      f"Patterns: {result.get('patterns', 0)}")
            else:
                print(f"  Trends: {result.get('trends', 0)}, "
                      f"Merges: {result.get('merges', 0)}, "
                      f"Promotions: {result.get('promotions', 0)}")


if __name__ == "__main__":
    main()
