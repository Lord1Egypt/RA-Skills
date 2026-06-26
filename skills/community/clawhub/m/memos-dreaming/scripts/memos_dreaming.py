#!/usr/bin/env python3
"""
memos_dreaming.py — MemOS + Daily Memory Dual-Source Dreaming

A Dreaming-style memory consolidation script that:
1. Reads from two sources: MemOS SQLite (skills/tasks) + daily memory logs
2. Scores candidates using Dreaming's 6 weighted signals
3. Generates a DREAMS.md draft for review
4. Promotes high-scoring entries to MEMORY.md

Signals (Dreaming-inspired):
  - Frequency (0.24): chunk references / recall count
  - Relevance (0.30): quality_score from MemOS skills
  - Query diversity (0.15): distinct session contexts
  - Recency (0.15): time-decayed freshness
  - Consolidation (0.10): multi-day recurrence
  - Conceptual richness (0.06): topic tag density
"""

import sqlite3
import json
import os
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ─── Config ──────────────────────────────────────────────────────────────────

MEMOS_DB = Path.home() / ".openclaw/memos-local/memos.db"
WORKSPACE = Path.home() / ".openclaw/workspace"
MEMORY_DIR = WORKSPACE / "memory"
DREAMS_FILE = WORKSPACE / "DREAMS.md"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
PROMOTED_INDEX = WORKSPACE / ".memos-dreaming" / "promoted.jsonl"

# Scoring weights (Dreaming-inspired)
WEIGHTS = {
    "frequency": 0.24,
    "relevance": 0.30,
    "query_diversity": 0.15,
    "recency": 0.15,
    "consolidation": 0.10,
    "conceptual_richness": 0.06,
}

# Thresholds
MIN_SCORE = 0.60
MIN_RECALL_COUNT = 2
MIN_UNIQUE_QUERIES = 1
MAX_DAILY_PROMOTIONS = 5

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_now_ts() -> int:
    return int(datetime.now().timestamp() * 1000)

def ts_to_date(ts: int) -> str:
    return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")

def ensure_dir(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def load_promoted() -> set:
    """Load set of already-promoted entry hashes."""
    if not PROMOTED_INDEX.exists():
        return set()
    with open(PROMOTED_INDEX) as f:
        return {line.strip().split("|")[0] for line in f if line.strip()}

def append_promoted(entry_hash: str, title: str, source: str):
    ensure_dir(PROMOTED_INDEX)
    with open(PROMOTED_INDEX, "a") as f:
        f.write(f"{entry_hash}|{source}|{ts_to_date(get_now_ts())}\n")

# ─── MemOS Source ────────────────────────────────────────────────────────────

def get_memOS_candidates(conn: sqlite3.Connection) -> list[dict]:
    """Fetch high-value tasks and skills from MemOS SQLite."""
    now = get_now_ts()
    day_ago = now - 86400 * 1000
    week_ago = now - 86400 * 7 * 1000

    candidates = []

    # Skills with quality scores
    rows = conn.execute("""
        SELECT id, name, description, quality_score, source_type,
               tags, created_at, updated_at, visibility
        FROM skills
        WHERE status = 'active' AND quality_score IS NOT NULL AND quality_score >= 0.5
        ORDER BY quality_score DESC
        LIMIT 50
    """).fetchall()

    for r in rows:
        cid, name, desc, qs, src, tags, ca, ua, vis = r
        entry_hash = hashlib.sha256(f"skill:{cid}".encode()).hexdigest()[:12]
        candidates.append({
            "entry_hash": entry_hash,
            "type": "skill",
            "id": cid,
            "title": name,
            "summary": desc,
            "quality_score": qs or 0,
            "tags": json.loads(tags) if tags else [],
            "merge_count": 1,
            "created_at": ca,
            "updated_at": ua,
            "visibility": vis,
        })

    # Tasks with skill_status='promoted' (these were elevated to skills)
    rows = conn.execute("""
        SELECT id, title, summary, topic, skill_status, skill_reason,
               started_at, updated_at
        FROM tasks
        WHERE status = 'active'
          AND skill_status = 'promoted'
        ORDER BY updated_at DESC
        LIMIT 50
    """).fetchall()

    for r in rows:
        cid, title, summary, topic, ss, sr, ca, ua = r
        entry_hash = hashlib.sha256(f"task:{cid}".encode()).hexdigest()[:12]
        candidates.append({
            "entry_hash": entry_hash,
            "type": "task",
            "id": cid,
            "title": title or "(untitled task)",
            "summary": summary or "",
            "topic": topic or "",
            "tags": [],
            "quality_score": 0,
            "skill_status": ss,
            "skill_reason": sr,
            "merge_count": 1,
            "created_at": ca,
            "updated_at": ua,
        })

    return candidates

# ─── Daily Memory Log Source ─────────────────────────────────────────────────

def get_daily_memory_candidates() -> list[dict]:
    """Scan recent daily memory logs for high-value entries."""
    candidates = []
    today = datetime.now()
    cutoff = today - timedelta(days=7)

    for log_file in sorted(MEMORY_DIR.glob("2026-*.md")):
        try:
            log_date = datetime.strptime(log_file.stem[:10], "%Y-%m-%d")
            if log_date < cutoff:
                continue
        except ValueError:
            continue

        content = log_file.read_text()
        # Extract sections: ## Decisions, ## Lessons Learned, ## Projects
        for section in ["Decisions Made", "Lessons Learned", "Projects", "Completed Tasks"]:
            pattern = rf"## {section}.*?(?=\n## |\Z)"
            match = re.search(pattern, content, re.DOTALL)
            if not match:
                continue
            text = match.group(0).strip()
            # Extract bullet points
            bullets = re.findall(r"^- (.+)$", text, re.MULTILINE)
            for b in bullets:
                b = b.strip()
                if len(b) < 20:
                    continue
                entry_hash = hashlib.sha256(b.encode()).hexdigest()[:12]
                candidates.append({
                    "entry_hash": entry_hash,
                    "type": "daily_log",
                    "title": b[:80],
                    "summary": b,
                    "source_file": log_file.name,
                    "updated_at": int(log_file.stat().st_mtime * 1000),
                })

    return candidates

# ─── Scoring ─────────────────────────────────────────────────────────────────

def compute_score(c: dict, all_entries: list[dict], now_ts: int) -> float:
    """Compute 6-signal weighted score."""

    # Frequency (0.24): merge_count / recall evidence
    merge_count = c.get("merge_count", 0)
    freq = min(merge_count / 10, 1.0)  # normalize to 0-1

    # Relevance (0.30): quality_score from MemOS (0-10 scale → 0-1)
    qs = c.get("quality_score", 0) or 0
    relevance = min(qs / 10.0, 1.0)

    # Query diversity (0.15): distinct source files/sessions
    sources = set()
    if c.get("type") == "daily_log":
        sources.add(c.get("source_file", ""))
    diversity = min(len(sources) / 3, 1.0) if sources else 0.5

    # Recency (0.15): time-decayed, half-life 30 days
    updated = c.get("updated_at", now_ts)
    days_old = (now_ts - updated) / (86400 * 1000)
    recency = max(0, 1 - (days_old / 30))

    # Consolidation (0.10): entries appearing across multiple days
    consolidation = 0.0
    if c["type"] == "daily_log":
        # count days this entry appears
        consolidation = 0.5  # simplified
    elif c.get("merge_count", 0) > 5:
        consolidation = 1.0

    # Conceptual richness (0.06): topic/tag density
    topic_len = len((c.get("topic") or "").split())
    tags_count = len(c.get("tags", []))
    richness = min((topic_len + tags_count) / 10, 1.0)

    score = (
        WEIGHTS["frequency"] * freq +
        WEIGHTS["relevance"] * relevance +
        WEIGHTS["query_diversity"] * diversity +
        WEIGHTS["recency"] * recency +
        WEIGHTS["consolidation"] * consolidation +
        WEIGHTS["conceptual_richness"] * richness
    )

    return round(min(score, 1.0), 4)

# ─── Output Formatters ────────────────────────────────────────────────────────

def format_skill_entry(c: dict) -> str:
    tags = ", ".join(c.get("tags", [])[:5])
    quality = c.get("quality_score", 0) or 0
    return (
        f"- **{c['title']}** (skill)\n"
        f"  - {c.get('summary', '')[:200]}\n"
        f"  - 质量评分: {quality:.2f} | 话题: {c.get('topic', 'N/A')} | 标签: {tags or '无'}\n"
        f"  - 来源: MemOS skill / 更新时间: {ts_to_date(c.get('updated_at', 0))}"
    )

def format_task_entry(c: dict) -> str:
    return (
        f"- **{c['title']}** (task)\n"
        f"  - {c.get('summary', '')[:200]}\n"
        f"  - 合并引用: {c.get('merge_count', 0)}次 | 话题: {c.get('topic', 'N/A')}\n"
        f"  - 来源: MemOS task / 更新时间: {ts_to_date(c.get('updated_at', 0))}"
    )

def format_daily_entry(c: dict) -> str:
    return (
        f"- {c['summary']}\n"
        f"  - 来源: {c.get('source_file', 'memory log')} | 评分: {c.get('_score', 0):.3f}"
    )

def format_dreams_draft(candidates: list[dict], scores: dict[str, float],
                        promoted: set) -> str:
    """Generate DREAMS.md review draft."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M %Z%z")
    lines = [
        f"# DREAMS.md — {now_str}",
        "",
        "## Dreaming Summary",
        "",
        f"Scanned: {len(candidates)} candidates",
        f"Above threshold: {sum(1 for h in scores if scores[h] >= MIN_SCORE)}",
        f"New promotions: {sum(1 for h in scores if scores[h] >= MIN_SCORE and h not in promoted)}",
        "",
        "## Phase: Deep Sleep",
        "",
    ]

    scored = [(c["entry_hash"], c, scores[c["entry_hash"]]) for c in candidates
                if c["entry_hash"] in scores and scores[c["entry_hash"]] >= MIN_SCORE]
    scored.sort(key=lambda x: x[2], reverse=True)

    for entry_hash, c, score in scored[:10]:
        marker = "✅" if entry_hash in promoted else "🆕"
        if c["type"] == "skill":
            entry_text = format_skill_entry(c)
        elif c["type"] == "task":
            entry_text = format_task_entry(c)
        else:
            entry_text = format_daily_entry(c)
        lines.append(f"{marker} {entry_text}")
        lines.append(f"   Score: {score:.3f}\n")

    return "\n".join(lines)

def format_memory_promotion(c: dict) -> str:
    """Format entry for MEMORY.md."""
    ts = ts_to_date(c.get("updated_at", get_now_ts()))
    if c["type"] == "skill":
        return (
            f"\n- **{c['title']}** (skill, {ts})\n"
            f"  {c.get('summary', '')[:200]}"
        )
    elif c["type"] == "task":
        return (
            f"\n- **{c['title']}** (task, {ts})\n"
            f"  {c.get('summary', '')[:200]}"
        )
    else:
        return f"\n- {c.get('summary', c.get('title', ''))} (daily log, {ts})"

# ─── Main ─────────────────────────────────────────────────────────────────────

def main(apply: bool = False, limit: int = MAX_DAILY_PROMOTIONS,
         min_score: float = MIN_SCORE, dry_run: bool = False):
    now_ts = get_now_ts()
    print(f"[memos-dreaming] Starting at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Apply mode: {apply} | Dry run: {dry_run} | Min score: {min_score}")

    # Load already-promoted
    promoted = load_promoted()
    print(f"  Already promoted: {len(promoted)} entries")

    # Gather candidates
    candidates = []

    # Source 1: MemOS
    if MEMOS_DB.exists():
        conn = sqlite3.connect(str(MEMOS_DB))
        memos_cands = get_memOS_candidates(conn)
        conn.close()
        print(f"  MemOS candidates: {len(memos_cands)}")
        candidates.extend(memos_cands)
    else:
        print(f"  [WARN] MemOS DB not found at {MEMOS_DB}")

    # Source 2: Daily memory logs
    daily_cands = get_daily_memory_candidates()
    print(f"  Daily memory candidates: {len(daily_cands)}")
    candidates.extend(daily_cands)

    # Score all
    scores = {c["entry_hash"]: compute_score(c, candidates, now_ts) for c in candidates}

    # Filter above threshold
    above = [(c["entry_hash"], c) for c in candidates
             if scores.get(c["entry_hash"], 0) >= min_score
             and c["entry_hash"] not in promoted]
    above.sort(key=lambda x: scores[x[0]], reverse=True)
    new_count = sum(1 for h, _ in above if h not in promoted)
    print(f"  Above threshold: {len(above)} (new: {new_count})")

    # Generate DREAMS draft
    dreams_content = format_dreams_draft(candidates, scores, promoted)
    ensure_dir(DREAMS_FILE)
    DREAMS_FILE.write_text(dreams_content)
    print(f"  DREAMS draft written: {DREAMS_FILE}")

    # Apply to MEMORY.md
    to_promote = [c for h, c in above if h not in promoted][:limit]
    if not to_promote:
        print("  Nothing new to promote.")
        return

    if dry_run:
        print(f"  [DRY RUN] Would promote {len(to_promote)} entries:")
        for c in to_promote:
            print(f"    - {c['title'][:60]} (score={scores[c['entry_hash']]:.3f})")
        return

    if apply:
        # Append to MEMORY.md
        ensure_dir(MEMORY_FILE)
        existing = MEMORY_FILE.read_text() if MEMORY_FILE.exists() else ""
        # Find last section
        if "## Promoted" in existing:
            insert_pos = existing.rfind("## Promoted")
        elif "## Lessons Learned" in existing:
            insert_pos = existing.rfind("## Lessons Learned")
        else:
            insert_pos = len(existing)

        new_entries = []
        for c in to_promote:
            new_entries.append(format_memory_promotion(c))
            append_promoted(c["entry_hash"], c.get("title", ""), c["type"])

        promoted_block = (
            f"\n\n## Promoted Entries ({datetime.now().strftime('%Y-%m-%d')})\n"
            + "".join(new_entries)
        )

        updated = existing[:insert_pos] + promoted_block + existing[insert_pos:]
        MEMORY_FILE.write_text(updated)
        print(f"  ✅ Promoted {len(to_promote)} entries to MEMORY.md")
    else:
        print(f"  Run with --apply to write to MEMORY.md")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MemOS Dreaming — Memory Consolidation")
    parser.add_argument("--apply", action="store_true", help="Write to MEMORY.md (default: dry run)")
    parser.add_argument("--dry-run", action="store_true", help="Force dry run")
    parser.add_argument("--limit", type=int, default=MAX_DAILY_PROMOTIONS)
    parser.add_argument("--min-score", type=float, default=MIN_SCORE)
    args = parser.parse_args()

    dry_run = args.dry_run or not args.apply
    main(apply=args.apply, limit=args.limit, min_score=args.min_score, dry_run=dry_run)
