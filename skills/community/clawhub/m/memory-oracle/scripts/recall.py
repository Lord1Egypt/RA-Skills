#!/usr/bin/env python3
"""
memory-oracle: recall.py
LIGHT process — three-slot context retrieval.
Zero API tokens. Runs before each agent response.

Usage:
  recall.py --query "user's message"
  recall.py --query "text" --verbose    # Show scores and metadata
  recall.py --query "text" --json       # Machine-readable output
  recall.py --budget 3000               # Override token budget
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
from init_db import load_settings, utcnow

SETTINGS = load_settings()


def get_db():
    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    if not os.path.exists(db_path):
        # Graceful degradation: fall back to grep
        return None
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn


def estimate_tokens(text: str) -> int:
    """Rough token estimate: chars / chars_per_token."""
    return max(1, len(text) // SETTINGS["recall"]["chars_per_token"])


def compute_live_score(row, now: datetime) -> float:
    """Compute real-time score with decay and access boost."""
    base = row["base_importance"]
    created = datetime.fromisoformat(row["created_at"])
    days_old = max(0, (now - created).total_seconds() / 86400)
    decay_rate = SETTINGS["scoring"]["decay_rate_per_day"]
    recency = 1.0 / (1.0 + days_old * decay_rate)
    access_boost = 1.0 + (row["access_count"] * SETTINGS["scoring"]["access_boost_per_hit"])
    score = base * recency * access_boost
    return min(score, SETTINGS["scoring"]["max_score"])


def slot_guardrails(conn, budget_tokens: int) -> tuple:
    """Slot 1: Always-present guardrails."""
    rows = conn.execute(
        "SELECT id, content FROM guardrails WHERE active=1 ORDER BY created_at ASC"
    ).fetchall()

    results = []
    used_tokens = 0

    for row in rows:
        tokens = estimate_tokens(row["content"])
        if used_tokens + tokens > budget_tokens:
            break
        results.append({
            "id": row["id"],
            "content": row["content"],
            "slot": "guardrail",
            "tokens": tokens,
        })
        used_tokens += tokens

    return results, used_tokens


def slot_fresh(conn, budget_tokens: int, now: datetime) -> tuple:
    """Slot 2: Facts from the last 24 hours by importance."""
    window = SETTINGS["recall"]["fresh_window_hours"]
    cutoff = (now - timedelta(hours=window)).isoformat()
    max_facts = SETTINGS["recall"]["max_facts_per_slot"]

    rows = conn.execute(
        """SELECT id, type, content, base_importance, access_count, created_at, score
           FROM facts
           WHERE status='active' AND created_at > ?
           ORDER BY base_importance DESC, created_at DESC
           LIMIT ?""",
        (cutoff, max_facts),
    ).fetchall()

    results = []
    used_tokens = 0

    for row in rows:
        tokens = estimate_tokens(row["content"])
        if used_tokens + tokens > budget_tokens:
            break
        results.append({
            "id": row["id"],
            "type": row["type"],
            "content": row["content"],
            "score": round(compute_live_score(row, now), 3),
            "slot": "fresh",
            "tokens": tokens,
            "age_hours": round((now - datetime.fromisoformat(row["created_at"])).total_seconds() / 3600, 1),
        })
        used_tokens += tokens

    return results, used_tokens


def slot_relevant(conn, query: str, budget_tokens: int, now: datetime, exclude_ids: set) -> tuple:
    """Slot 3: FTS5 search + score ranking."""
    max_facts = SETTINGS["recall"]["max_facts_per_slot"]

    # Sanitize query for FTS5
    fts_query = _sanitize_fts_query(query)

    results = []
    used_tokens = 0

    if fts_query:
        # FTS5 search with BM25 ranking
        try:
            rows = conn.execute(
                """SELECT f.id, f.type, f.content, f.base_importance, f.access_count,
                          f.created_at, f.score, bm25(facts_fts) AS rank
                   FROM facts_fts
                   JOIN facts f ON facts_fts.rowid = f.rowid
                   WHERE facts_fts MATCH ? AND f.status='active'
                   ORDER BY rank
                   LIMIT ?""",
                (fts_query, max_facts * 2),
            ).fetchall()
        except sqlite3.OperationalError:
            rows = []
    else:
        rows = []

    # If FTS returned nothing, fall back to top-scored facts
    if not rows:
        rows = conn.execute(
            """SELECT id, type, content, base_importance, access_count, created_at, score,
                      0 AS rank
               FROM facts
               WHERE status='active'
               ORDER BY score DESC
               LIMIT ?""",
            (max_facts,),
        ).fetchall()

    # Score and filter
    scored = []
    for row in rows:
        if row["id"] in exclude_ids:
            continue
        live_score = compute_live_score(row, now)
        # Combine FTS rank with live score (FTS rank is negative, lower=better)
        fts_bonus = max(0, -row["rank"] * 0.1) if row["rank"] != 0 else 0
        combined = live_score + fts_bonus
        scored.append((combined, row))

    scored.sort(key=lambda x: x[0], reverse=True)

    for combined_score, row in scored[:max_facts]:
        tokens = estimate_tokens(row["content"])
        if used_tokens + tokens > budget_tokens:
            break
        results.append({
            "id": row["id"],
            "type": row["type"],
            "content": row["content"],
            "score": round(combined_score, 3),
            "slot": "relevant",
            "tokens": tokens,
        })
        used_tokens += tokens

    return results, used_tokens


def _sanitize_fts_query(query: str) -> str:
    """Make a user query safe for FTS5 MATCH."""
    # Remove all non-alphanumeric chars except spaces (keeps unicode letters)
    cleaned = re.sub(r"[^\w\s]", " ", query, flags=re.UNICODE)
    # Split into words, filter short ones and FTS5 reserved operators
    fts_reserved = {"AND", "OR", "NOT", "NEAR"}
    words = [
        w for w in cleaned.split()
        if len(w) >= 3 and w.upper() not in fts_reserved
    ]
    if not words:
        return ""
    # Use OR for broader matching, cap at 8 terms
    return " OR ".join(words[:8])


def log_access(conn, facts: list, query: str):
    """Record access for scoring feedback."""
    now = utcnow().isoformat()
    for fact in facts:
        conn.execute(
            "INSERT INTO access_log (fact_id, query, slot, accessed_at) VALUES (?, ?, ?, ?)",
            (fact["id"], query[:200], fact["slot"], now),
        )
        # Bump access count on the fact
        conn.execute(
            "UPDATE facts SET access_count = access_count + 1, accessed_at = ? WHERE id = ?",
            (now, fact["id"]),
        )
    conn.commit()


def fallback_grep(query: str, budget_tokens: int) -> list:
    """Grep-based fallback when SQLite is unavailable."""
    memory_path = os.path.expanduser(SETTINGS["paths"]["memory_md"])
    if not os.path.exists(memory_path):
        return []

    with open(memory_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    query_words = set(query.lower().split())
    scored = []

    for line in lines:
        line = line.strip()
        if len(line) < 10 or line.startswith("#"):
            continue
        line_words = set(line.lower().split())
        overlap = len(query_words & line_words)
        if overlap > 0:
            scored.append((overlap, line))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    used = 0
    for overlap, line in scored[:10]:
        tokens = estimate_tokens(line)
        if used + tokens > budget_tokens:
            break
        results.append({
            "id": "grep",
            "type": "unknown",
            "content": line,
            "score": overlap,
            "slot": "grep_fallback",
            "tokens": tokens,
        })
        used += tokens

    return results


def format_injection(facts: list) -> str:
    """Format facts for context injection."""
    if not facts:
        return ""

    sections = {"guardrail": [], "fresh": [], "relevant": [], "grep_fallback": []}
    for f in facts:
        sections.get(f["slot"], []).append(f)

    lines = ["<memory_context>"]

    if sections["guardrail"]:
        lines.append("## Critical rules (always active)")
        for f in sections["guardrail"]:
            lines.append(f"- {f['content']}")

    if sections["fresh"]:
        lines.append("## Recent context (last 24h)")
        for f in sections["fresh"]:
            lines.append(f"- [{f['type']}] {f['content']}")

    if sections["relevant"]:
        lines.append("## Relevant background")
        for f in sections["relevant"]:
            lines.append(f"- [{f['type']}] {f['content']}")

    if sections["grep_fallback"]:
        lines.append("## Background (from MEMORY.md)")
        for f in sections["grep_fallback"]:
            lines.append(f"- {f['content']}")

    lines.append("</memory_context>")
    return "\n".join(lines)


def format_verbose(facts: list) -> str:
    """Format facts with metadata for user inspection."""
    if not facts:
        return "No facts found."

    lines = []
    for f in facts:
        meta_parts = [f"slot={f['slot']}", f"score={f.get('score', '?')}"]
        if "age_hours" in f:
            meta_parts.append(f"age={f['age_hours']}h")
        meta_parts.append(f"tokens={f['tokens']}")
        meta = ", ".join(meta_parts)
        lines.append(f"[{f.get('type', 'unknown')}] {f['content']}\n  ({meta})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Memory Oracle — Recall")
    parser.add_argument("--query", type=str, required=True, help="Query text (user's message)")
    parser.add_argument("--budget", type=int, default=None, help="Override token budget")
    parser.add_argument("--verbose", action="store_true", help="Show scores and metadata")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--no-log", action="store_true", help="Don't log access")
    args = parser.parse_args()

    total_budget = args.budget or SETTINGS["recall"]["budget_tokens"]
    now = utcnow()

    conn = get_db()

    if conn is None:
        # Graceful degradation
        if SETTINGS["recall"]["fallback_to_grep"]:
            facts = fallback_grep(args.query, total_budget)
            if args.json:
                print(json.dumps({"mode": "grep_fallback", "facts": facts}))
            elif args.verbose:
                print(format_verbose(facts))
            else:
                print(format_injection(facts))
            return
        else:
            print("ERROR: Database not available and fallback disabled.", file=sys.stderr)
            sys.exit(1)

    # Calculate slot budgets
    guard_budget = int(total_budget * SETTINGS["recall"]["slot_guardrails_pct"])
    fresh_budget = int(total_budget * SETTINGS["recall"]["slot_fresh_pct"])
    relevant_budget = total_budget - guard_budget - fresh_budget

    # Retrieve from each slot
    guard_facts, guard_used = slot_guardrails(conn, guard_budget)
    fresh_facts, fresh_used = slot_fresh(conn, fresh_budget, now)

    # Pass already-retrieved IDs to avoid duplicates in relevant slot
    exclude = {f["id"] for f in guard_facts + fresh_facts}
    # Give unused budget from other slots to relevant
    remaining_budget = relevant_budget + (guard_budget - guard_used) + (fresh_budget - fresh_used)
    relevant_facts, relevant_used = slot_relevant(conn, args.query, remaining_budget, now, exclude)

    all_facts = guard_facts + fresh_facts + relevant_facts

    # Log access
    if not args.no_log and all_facts:
        log_access(conn, all_facts, args.query)

    conn.close()

    # Output
    total_tokens = guard_used + fresh_used + relevant_used
    if args.json:
        print(json.dumps({
            "mode": "sqlite",
            "total_tokens": total_tokens,
            "budget": total_budget,
            "slots": {
                "guardrail": {"count": len(guard_facts), "tokens": guard_used},
                "fresh": {"count": len(fresh_facts), "tokens": fresh_used},
                "relevant": {"count": len(relevant_facts), "tokens": relevant_used},
            },
            "facts": all_facts,
        }, ensure_ascii=False, indent=2))
    elif args.verbose:
        print(f"Recall: {len(all_facts)} facts, {total_tokens}/{total_budget} tokens")
        print(f"  Guardrails: {len(guard_facts)}, Fresh: {len(fresh_facts)}, Relevant: {len(relevant_facts)}")
        print()
        print(format_verbose(all_facts))
    else:
        print(format_injection(all_facts))


if __name__ == "__main__":
    main()
