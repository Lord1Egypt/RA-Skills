#!/usr/bin/env python3
"""
memory-oracle: maintenance.py
HEAVY process — memory hygiene: decay scores, prune dead facts,
archive cold tier, re-render MEMORY.md, vacuum SQLite.

Usage:
  maintenance.py                  # Full maintenance cycle
  maintenance.py --decay-only     # Only apply score decay
  maintenance.py --render-only    # Only re-render MEMORY.md
  maintenance.py --export FILE    # Export full state to JSON
  maintenance.py --stats          # Show memory statistics
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
from init_db import load_settings, utcnow

SETTINGS = load_settings()


def get_db():
    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn


def apply_decay(conn) -> dict:
    """Apply daily decay to all active fact scores."""
    now = utcnow()
    decay_rate = SETTINGS["scoring"]["decay_rate_per_day"]
    min_score = SETTINGS["scoring"]["min_score"]

    rows = conn.execute(
        "SELECT id, score, base_importance, access_count, created_at FROM facts WHERE status='active'"
    ).fetchall()

    updated = 0
    for row in rows:
        created = datetime.fromisoformat(row["created_at"])
        days_old = max(0, (now - created).total_seconds() / 86400)
        recency = 1.0 / (1.0 + days_old * decay_rate)
        access_boost = 1.0 + (row["access_count"] * SETTINGS["scoring"]["access_boost_per_hit"])
        new_score = max(min_score, row["base_importance"] * recency * access_boost)
        new_score = min(new_score, SETTINGS["scoring"]["max_score"])

        if abs(new_score - row["score"]) > 0.001:
            conn.execute(
                "UPDATE facts SET score=?, updated_at=? WHERE id=?",
                (round(new_score, 4), now.isoformat(), row["id"]),
            )
            updated += 1

    conn.commit()
    return {"decayed": updated, "total_active": len(rows)}


def archive_cold(conn) -> dict:
    """Move low-score facts to archived status."""
    threshold = SETTINGS["scoring"]["archive_threshold"]
    cutoff_days = SETTINGS["maintenance"]["cold_archive_after_days"]
    cutoff_date = (utcnow() - timedelta(days=cutoff_days)).isoformat()
    now = utcnow().isoformat()

    # Archive facts below threshold that are old enough
    result = conn.execute(
        """UPDATE facts SET status='archived', updated_at=?
           WHERE status='active' AND score < ? AND created_at < ?
           AND type != 'guardrail'""",
        (now, threshold, cutoff_date),
    )
    archived = result.rowcount

    conn.commit()
    return {"archived": archived}


def prune_dead(conn) -> dict:
    """Delete facts below delete threshold that are old enough."""
    threshold = SETTINGS["scoring"]["delete_threshold"]
    min_age = SETTINGS["maintenance"]["delete_min_age_days"]
    cutoff_date = (utcnow() - timedelta(days=min_age)).isoformat()

    # Count before delete
    count = conn.execute(
        "SELECT COUNT(*) FROM facts WHERE status IN ('archived','superseded','merged') AND score < ? AND created_at < ?",
        (threshold, cutoff_date),
    ).fetchone()[0]

    if count > 0:
        conn.execute(
            "DELETE FROM facts WHERE status IN ('archived','superseded','merged') AND score < ? AND created_at < ?",
            (threshold, cutoff_date),
        )
        conn.commit()

    return {"pruned": count}


def clean_daily_logs() -> dict:
    """Remove daily logs older than retention period."""
    logs_dir = os.path.expanduser(SETTINGS["paths"]["daily_logs"])
    if not os.path.exists(logs_dir):
        return {"cleaned": 0}

    max_age = SETTINGS["maintenance"]["max_daily_log_age_days"]
    cutoff = date.today() - timedelta(days=max_age)
    cleaned = 0

    for f in Path(logs_dir).glob("????-??-??.md"):
        try:
            file_date = date.fromisoformat(f.stem)
            if file_date < cutoff:
                f.unlink()
                cleaned += 1
        except ValueError:
            continue

    return {"cleaned": cleaned}


def render_memory_md(conn) -> dict:
    """Re-render MEMORY.md from top-scored facts in SQLite."""
    max_facts = SETTINGS["maintenance"]["memory_md_max_facts"]
    max_chars = SETTINGS["maintenance"]["memory_md_max_chars"]
    memory_path = os.path.expanduser(SETTINGS["paths"]["memory_md"])

    # Get guardrails
    guardrails = conn.execute(
        "SELECT content FROM guardrails WHERE active=1 ORDER BY created_at ASC"
    ).fetchall()

    # Get top facts by type
    facts_by_type = {}
    rows = conn.execute(
        """SELECT type, content, score, created_at
           FROM facts WHERE status='active' AND type != 'guardrail'
           ORDER BY score DESC LIMIT ?""",
        (max_facts,),
    ).fetchall()

    for row in rows:
        t = row["type"]
        if t not in facts_by_type:
            facts_by_type[t] = []
        facts_by_type[t].append(row)

    # Build markdown
    lines = ["# Memory", "", f"*Auto-generated by Memory Oracle — {date.today().isoformat()}*", ""]

    if guardrails:
        lines.append("## Critical rules")
        for g in guardrails:
            lines.append(f"- **{g['content']}**")
        lines.append("")

    # Type display order
    type_labels = {
        "identity": "About me",
        "project": "Active projects",
        "decision": "Key decisions",
        "preference": "Preferences",
        "tech_stack": "Tech stack",
        "contact": "People",
        "task": "Active tasks",
        "pattern": "Recurring patterns",
        "insight": "Insights",
    }

    for fact_type, label in type_labels.items():
        type_facts = facts_by_type.get(fact_type, [])
        if not type_facts:
            continue
        lines.append(f"## {label}")
        for f in type_facts:
            lines.append(f"- {f['content']}")
        lines.append("")

    content = "\n".join(lines)

    # Enforce max chars
    if len(content) > max_chars:
        content = content[:max_chars] + "\n\n*[truncated by Memory Oracle]*\n"

    # Write
    os.makedirs(os.path.dirname(memory_path), exist_ok=True)
    with open(memory_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"rendered_facts": sum(len(v) for v in facts_by_type.values()),
            "guardrails": len(guardrails), "chars": len(content)}


def vacuum_db(conn) -> dict:
    """Vacuum and optimize SQLite database."""
    # Rebuild FTS index
    conn.execute("INSERT INTO facts_fts(facts_fts) VALUES('rebuild')")
    conn.commit()

    # Get size before vacuum
    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    size_before = os.path.getsize(db_path)

    conn.execute("VACUUM")

    size_after = os.path.getsize(db_path)
    return {"size_before": size_before, "size_after": size_after,
            "saved_bytes": size_before - size_after}


def get_stats(conn) -> dict:
    """Get memory statistics."""
    stats = {}

    # Fact counts by status
    for status in ("active", "archived", "superseded", "merged"):
        count = conn.execute(
            "SELECT COUNT(*) FROM facts WHERE status=?", (status,)
        ).fetchone()[0]
        stats[f"facts_{status}"] = count

    # Fact counts by type
    type_counts = conn.execute(
        "SELECT type, COUNT(*) FROM facts WHERE status='active' GROUP BY type ORDER BY COUNT(*) DESC"
    ).fetchall()
    stats["facts_by_type"] = {r[0]: r[1] for r in type_counts}

    # Guardrails
    stats["guardrails_active"] = conn.execute(
        "SELECT COUNT(*) FROM guardrails WHERE active=1"
    ).fetchone()[0]

    # Score distribution
    for label, low, high in [("high", 2.0, 999), ("medium", 0.5, 2.0), ("low", 0.0, 0.5)]:
        stats[f"score_{label}"] = conn.execute(
            "SELECT COUNT(*) FROM facts WHERE status='active' AND score >= ? AND score < ?",
            (low, high),
        ).fetchone()[0]

    # Reflections
    stats["reflections_total"] = conn.execute("SELECT COUNT(*) FROM reflections").fetchone()[0]
    stats["reflections_applied"] = conn.execute(
        "SELECT COUNT(*) FROM reflections WHERE applied=1"
    ).fetchone()[0]

    # Access log
    stats["accesses_total"] = conn.execute("SELECT COUNT(*) FROM access_log").fetchone()[0]
    week_ago = (utcnow() - timedelta(days=7)).isoformat()
    stats["accesses_this_week"] = conn.execute(
        "SELECT COUNT(*) FROM access_log WHERE accessed_at >= ?", (week_ago,)
    ).fetchone()[0]

    # DB size
    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    stats["db_size_bytes"] = os.path.getsize(db_path)
    stats["db_size_mb"] = round(stats["db_size_bytes"] / 1048576, 2)

    return stats


def export_state(conn, export_path: str) -> dict:
    """Export full memory state to JSON for backup/migration."""
    state = {
        "exported_at": utcnow().isoformat(),
        "version": SETTINGS.get("version", 1),
        "facts": [],
        "guardrails": [],
        "reflections": [],
        "stats": get_stats(conn),
    }

    for row in conn.execute("SELECT * FROM facts ORDER BY score DESC").fetchall():
        state["facts"].append(dict(row))

    for row in conn.execute("SELECT * FROM guardrails").fetchall():
        state["guardrails"].append(dict(row))

    for row in conn.execute("SELECT * FROM reflections ORDER BY date DESC LIMIT 30").fetchall():
        state["reflections"].append(dict(row))

    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    return {"exported_to": export_path, "facts": len(state["facts"]),
            "guardrails": len(state["guardrails"])}


def main():
    parser = argparse.ArgumentParser(description="Memory Oracle — Maintenance")
    parser.add_argument("--decay-only", action="store_true")
    parser.add_argument("--render-only", action="store_true")
    parser.add_argument("--export", type=str, default=None, help="Export path")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    conn = get_db()
    results = {}

    if args.stats:
        results = get_stats(conn)
    elif args.export:
        results = export_state(conn, args.export)
    elif args.decay_only:
        results["decay"] = apply_decay(conn)
    elif args.render_only:
        results["render"] = render_memory_md(conn)
    else:
        # Full maintenance cycle
        results["decay"] = apply_decay(conn)
        results["archive"] = archive_cold(conn)
        results["prune"] = prune_dead(conn)
        results["logs"] = clean_daily_logs()
        results["render"] = render_memory_md(conn)

        # Vacuum weekly
        last_vacuum = conn.execute(
            "SELECT value FROM schema_meta WHERE key='last_vacuum'"
        ).fetchone()
        days_since = 999
        if last_vacuum:
            try:
                lv = datetime.fromisoformat(last_vacuum[0])
                days_since = (utcnow() - lv).days
            except ValueError:
                pass
        if days_since >= SETTINGS["maintenance"]["vacuum_interval_days"]:
            results["vacuum"] = vacuum_db(conn)
            conn.execute(
                "INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('last_vacuum', ?)",
                (utcnow().isoformat(),),
            )
            conn.commit()

    conn.close()

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        if args.stats:
            print("Memory Oracle — Statistics")
            for k, v in results.items():
                print(f"  {k}: {v}")
        elif args.export:
            print(f"Exported to {results['exported_to']}: {results['facts']} facts, {results['guardrails']} guardrails")
        else:
            print("Memory Oracle — Maintenance complete")
            for step, data in results.items():
                if isinstance(data, dict):
                    summary = ", ".join(f"{k}={v}" for k, v in data.items())
                    print(f"  {step}: {summary}")


if __name__ == "__main__":
    main()
