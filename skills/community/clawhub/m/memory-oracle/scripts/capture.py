#!/usr/bin/env python3
"""
memory-oracle: capture.py
LIGHT process — rule-based fact extraction from conversation turns.
Zero API tokens. Runs after each agent response.

Usage:
  capture.py --turn "conversation text"
  capture.py --turn "text" --guardrail     # Force guardrail type
  capture.py --turn "text" --session SID   # Attach session ID
  capture.py --flush                        # Flush buffered context
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
from init_db import content_hash, generate_id, load_settings, utcnow

SETTINGS = load_settings()
PATTERNS_PATH = SCRIPT_DIR / "config" / "patterns.json"


def load_patterns():
    with open(PATTERNS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_db(settings=None):
    s = settings or SETTINGS
    db_path = os.path.expanduser(s["paths"]["db"])
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found at {db_path}. Run init_db.py first.", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def extract_facts(text: str, patterns_data: dict, force_guardrail: bool = False) -> list:
    """Extract structured facts from text using pattern matching."""
    facts = []
    seen_hashes = set()

    # Check for explicit remember/forget signals
    is_explicit_remember = False
    is_explicit_forget = False

    for pat in patterns_data.get("explicit_remember", {}).get("patterns_en", []):
        if re.search(pat, text):
            is_explicit_remember = True
            break
    if not is_explicit_remember:
        for pat in patterns_data.get("explicit_remember", {}).get("patterns_ru", []):
            if re.search(pat, text):
                is_explicit_remember = True
                break

    for pat in patterns_data.get("explicit_forget", {}).get("patterns_en", []):
        if re.search(pat, text):
            is_explicit_forget = True
            break
    if not is_explicit_forget:
        for pat in patterns_data.get("explicit_forget", {}).get("patterns_ru", []):
            if re.search(pat, text):
                is_explicit_forget = True
                break

    # Split text into sentences for granular extraction
    sentences = re.split(r"(?<=[.!?。！？])\s+|\n+", text)

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < SETTINGS["capture"]["min_content_length"]:
            continue
        if len(sentence) > SETTINGS["capture"]["max_content_length"]:
            sentence = sentence[: SETTINGS["capture"]["max_content_length"]]

        matched_type = None
        matched_importance = SETTINGS["scoring"]["default_importance"]

        # Force guardrail if requested
        if force_guardrail:
            matched_type = "guardrail"
            matched_importance = SETTINGS["scoring"]["guardrail_importance"]
        else:
            # Try ALL fact type patterns — pick highest importance match
            best_type = None
            best_importance = 0.0

            for fact_type, type_info in patterns_data.get("fact_types", {}).items():
                type_imp = type_info.get("base_importance", SETTINGS["scoring"]["default_importance"])
                found = False

                # Try EN patterns
                for pat in type_info.get("patterns_en", []):
                    try:
                        if re.search(pat, sentence):
                            found = True
                            break
                    except re.error:
                        continue

                # Try RU patterns if EN didn't match
                if not found:
                    for pat in type_info.get("patterns_ru", []):
                        try:
                            if re.search(pat, sentence):
                                found = True
                                break
                        except re.error:
                            continue

                if found and type_imp > best_importance:
                    best_type = fact_type
                    best_importance = type_imp

            if best_type:
                matched_type = best_type
                matched_importance = best_importance

        # If explicit remember was triggered but no type pattern matched,
        # capture as "insight" — the user explicitly asked to remember
        if not matched_type and is_explicit_remember:
            matched_type = "insight"
            matched_importance = 1.5

        if not matched_type:
            continue

        # Apply explicit remember boost
        if is_explicit_remember:
            boost = patterns_data.get("explicit_remember", {}).get("importance_boost", 1.5)
            matched_importance *= boost

        # Dedup within this extraction
        chash = content_hash(sentence)
        if chash in seen_hashes:
            continue
        seen_hashes.add(chash)

        facts.append({
            "type": matched_type,
            "content": sentence,
            "content_hash": chash,
            "base_importance": round(matched_importance, 2),
            "is_forget": is_explicit_forget,
        })

    return facts


def store_facts(conn: sqlite3.Connection, facts: list, session_id: str = None, turn: int = None):
    """Store extracted facts in SQLite, handling dedup and updates."""
    now = utcnow().isoformat()
    stored = 0
    bumped = 0

    for fact in facts:
        # Handle explicit forget
        if fact.get("is_forget"):
            # Mark matching facts as archived
            conn.execute(
                "UPDATE facts SET status='archived', updated_at=? WHERE content_hash=? AND status='active'",
                (now, fact["content_hash"]),
            )
            continue

        # Check for existing fact with same content hash
        existing = conn.execute(
            "SELECT id, access_count, score FROM facts WHERE content_hash=? AND status='active'",
            (fact["content_hash"],),
        ).fetchone()

        if existing:
            # Bump access count and score
            new_count = existing[1] + 1
            boost = SETTINGS["scoring"]["access_boost_per_hit"]
            new_score = min(
                existing[2] + boost, SETTINGS["scoring"]["max_score"]
            )
            conn.execute(
                "UPDATE facts SET access_count=?, score=?, accessed_at=?, updated_at=? WHERE id=?",
                (new_count, new_score, now, now, existing[0]),
            )
            bumped += 1
        else:
            # Insert new fact
            fid = generate_id("cap")
            score = fact["base_importance"]
            conn.execute(
                """INSERT INTO facts (id, type, content, content_hash, base_importance,
                   score, status, source, source_session, source_turn,
                   confidence, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, 'active', 'capture', ?, ?, 0.9, ?, ?)""",
                (
                    fid, fact["type"], fact["content"], fact["content_hash"],
                    fact["base_importance"], score, session_id, turn, now, now,
                ),
            )

            # If guardrail, also add to guardrails table
            if fact["type"] == "guardrail":
                gid = generate_id("grd")
                conn.execute(
                    "INSERT INTO guardrails (id, content, created_at, source) VALUES (?, ?, ?, 'capture')",
                    (gid, fact["content"], now),
                )

            stored += 1

    conn.commit()
    return stored, bumped


def write_daily_log(text: str, settings: dict):
    """Append to today's daily log (maintains OpenClaw compatibility)."""
    logs_dir = os.path.expanduser(settings["paths"]["daily_logs"])
    os.makedirs(logs_dir, exist_ok=True)
    today = utcnow().strftime("%Y-%m-%d")
    log_path = os.path.join(logs_dir, f"{today}.md")

    timestamp = utcnow().strftime("%H:%M")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n- [{timestamp}] {text[:200]}\n")


def main():
    parser = argparse.ArgumentParser(description="Memory Oracle — Capture")
    parser.add_argument("--turn", type=str, help="Conversation turn text to process")
    parser.add_argument("--guardrail", action="store_true", help="Force guardrail classification")
    parser.add_argument("--session", type=str, default=None, help="Session ID")
    parser.add_argument("--turn-number", type=int, default=None, help="Turn number in session")
    parser.add_argument("--flush", action="store_true", help="Flush mode — process buffered context")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    if not args.turn and not args.flush:
        parser.print_help()
        sys.exit(1)

    patterns = load_patterns()
    conn = get_db()

    if args.flush:
        # Read SESSION-STATE.md if it exists and process it
        session_state = os.path.expanduser(
            os.path.join(SETTINGS["paths"]["workspace"], "SESSION-STATE.md")
        )
        if os.path.exists(session_state):
            with open(session_state, "r", encoding="utf-8") as f:
                text = f.read()
            facts = extract_facts(text, patterns)
            stored, bumped = store_facts(conn, facts, args.session)
            result = {"mode": "flush", "extracted": len(facts), "stored": stored, "bumped": bumped}
        else:
            result = {"mode": "flush", "extracted": 0, "stored": 0, "bumped": 0, "note": "no SESSION-STATE.md"}
    else:
        facts = extract_facts(args.turn, patterns, force_guardrail=args.guardrail)
        stored, bumped = store_facts(conn, facts, args.session, args.turn_number)
        write_daily_log(args.turn, SETTINGS)
        result = {"mode": "capture", "extracted": len(facts), "stored": stored, "bumped": bumped}

    conn.close()

    if args.json:
        print(json.dumps(result))
    else:
        print(f"Captured: {result['extracted']} extracted, {result['stored']} new, {result['bumped']} bumped")


if __name__ == "__main__":
    main()
