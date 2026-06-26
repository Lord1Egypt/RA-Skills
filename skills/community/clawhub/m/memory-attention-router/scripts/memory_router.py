#!/usr/bin/env python3
"""
Memory Attention Router
-----------------------
A deterministic SQLite-backed memory router for OpenClaw skills.

Commands:
  init
  add --input-json '<json>'
  route --input-json '<json>'
  reflect --input-json '<json>'
  refresh --input-json '<json>'
  list [--limit N]
  inspect --memory-id ID
  packets [--limit N]
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sqlite3
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DEFAULT_DB_BASENAME = ".openclaw-memory-router.sqlite3"

ROLE_TO_TYPES: dict[str, tuple[str, ...]] = {
    "planner": ("preference", "procedure", "summary"),
    "executor": ("preference", "procedure", "episode", "reflection"),
    "critic": ("reflection", "preference", "summary"),
    "responder": ("preference", "summary", "procedure"),
}
TYPE_PRIORITY = {
    "preference": 0,
    "procedure": 1,
    "summary": 2,
    "reflection": 3,
    "episode": 4,
}
BLOCK_PRIORITY = {
    "task_scoped": 0,
    "session_scoped": 1,
    "durable_global": 2,
    "recent_fallback": 3,
}


@dataclass
class Candidate:
    row: sqlite3.Row
    block: str
    score: float
    reasons: list[str]


@dataclass
class BlockDecision:
    name: str
    score: float
    candidate_count: int
    selected: bool
    reasons: list[str]
    top_memory_ids: list[str]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def error(msg: str, code: int = 1) -> None:
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(code)


def infer_default_db_path() -> str:
    """
    Resolve one stable default DB path.
    If the script lives in <workspace>/skills/<skill>/scripts/, default to:
    <workspace>/.openclaw-memory-router.sqlite3
    Otherwise, fallback to the skill root directory.
    """
    script_path = Path(__file__).resolve()
    skill_root = script_path.parent.parent
    if skill_root.parent.name == "skills":
        return str((skill_root.parent.parent / DEFAULT_DB_BASENAME).resolve())
    return str((skill_root / DEFAULT_DB_BASENAME).resolve())


def get_db_path(cli_db: str | None) -> str:
    return cli_db or os.environ.get("MAR_DB_PATH") or infer_default_db_path()


def connect(cli_db: str | None = None) -> sqlite3.Connection:
    db_path = get_db_path(cli_db)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def load_schema() -> str:
    return Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")


def ensure_schema(conn: sqlite3.Connection) -> dict[str, Any]:
    conn.executescript(load_schema())
    conn.commit()
    return {"ok": True, "initialized": True}


def loads_json_field(raw: str | None, fallback: Any) -> Any:
    if raw is None or raw == "":
        return fallback
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return fallback


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def clamp_score(value: Any, fallback: float = 0.5) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return fallback
    return max(0.0, min(1.0, number))


def tokenize_for_match(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z0-9_]{2,}", text)
    deduped: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if token not in seen:
            deduped.append(token)
            seen.add(token)
    return deduped[:16]


def build_match_query(*parts: str) -> str:
    tokens: list[str] = []
    for part in parts:
        tokens.extend(tokenize_for_match(part))
    if not tokens:
        return ""
    unique_tokens = dedupe_keep_order(tokens, limit=12)
    return " OR ".join(f'"{token}"' for token in unique_tokens)


def hours_ago_score(ts: str | None) -> float:
    if not ts:
        return 0.5
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return 0.5
    delta_hours = max((datetime.now(timezone.utc) - dt).total_seconds() / 3600.0, 0.0)
    return max(0.1, min(1.0, math.exp(-delta_hours / 336.0)))


def timestamp_sort_value(ts: str | None) -> float:
    if not ts:
        return 0.0
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def overlap_score(a_terms: Iterable[str], b_terms: Iterable[str]) -> float:
    a = set(a_terms)
    b = set(b_terms)
    if not a or not b:
        return 0.0
    inter = a & b
    denom = max(len(a | b), 1)
    return len(inter) / denom


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "memory_type": row["memory_type"],
        "abstraction_level": row["abstraction_level"],
        "role_scope": row["role_scope"],
        "session_id": row["session_id"],
        "task_id": row["task_id"],
        "title": row["title"],
        "summary": row["summary"],
        "details": loads_json_field(row["details_json"], {}),
        "keywords": loads_json_field(row["keywords_json"], []),
        "tags": loads_json_field(row["tags_json"], []),
        "source_refs": loads_json_field(row["source_refs_json"], []),
        "importance": row["importance"],
        "confidence": row["confidence"],
        "success_score": row["success_score"],
        "recency_ts": row["recency_ts"],
        "valid_from_ts": row["valid_from_ts"],
        "valid_to_ts": row["valid_to_ts"],
        "is_active": row["is_active"],
        "replaced_by_memory_id": row["replaced_by_memory_id"],
        "retired_reason": row["retired_reason"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def upsert_fts(
    conn: sqlite3.Connection,
    mem_id: str,
    title: str,
    summary: str,
    keywords: list[str],
    tags: list[str],
) -> None:
    conn.execute("DELETE FROM memories_fts WHERE id = ?", (mem_id,))
    conn.execute(
        "INSERT INTO memories_fts(id, title, summary, keywords, tags) VALUES (?, ?, ?, ?, ?)",
        (mem_id, title, summary, " ".join(keywords), " ".join(tags)),
    )


def insert_edge(
    conn: sqlite3.Connection,
    from_id: str,
    to_id: str,
    edge_type: str,
    weight: float = 0.5,
) -> str:
    edge_id = f"edge_{uuid.uuid4().hex[:12]}"
    conn.execute(
        """
        INSERT INTO memory_edges(id, from_memory_id, to_memory_id, edge_type, weight, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (edge_id, from_id, to_id, edge_type, clamp_score(weight), now_iso()),
    )
    return edge_id


def validate_memory_payload(payload: dict[str, Any]) -> None:
    required = ["memory_type", "title", "summary"]
    for key in required:
        if not payload.get(key):
            error(f"missing required field: {key}")
    if payload["memory_type"] not in {
        "episode",
        "summary",
        "reflection",
        "procedure",
        "preference",
    }:
        error(
            "memory_type must be one of episode|summary|reflection|procedure|preference"
        )
    role_scope = payload.get("role_scope", "global")
    if role_scope not in {"planner", "executor", "critic", "responder", "global"}:
        error("role_scope must be one of planner|executor|critic|responder|global")
    abstraction_level = int(payload.get("abstraction_level", 0))
    if abstraction_level < 0 or abstraction_level > 3:
        error("abstraction_level must be between 0 and 3")


def retire_memories(
    conn: sqlite3.Connection,
    stale_ids: list[str],
    replacement_memory_id: str | None = None,
    refresh_reason: str | None = None,
) -> tuple[list[str], list[str]]:
    ts = now_iso()
    deactivated: list[str] = []
    edge_ids: list[str] = []

    for mid in stale_ids:
        existing = conn.execute(
            "SELECT id FROM memories WHERE id = ?", (mid,)
        ).fetchone()
        if not existing:
            continue
        conn.execute(
            """
            UPDATE memories
            SET is_active = 0,
                valid_to_ts = ?,
                replaced_by_memory_id = COALESCE(?, replaced_by_memory_id),
                retired_reason = COALESCE(?, retired_reason),
                updated_at = ?
            WHERE id = ?
            """,
            (ts, replacement_memory_id, refresh_reason, ts, mid),
        )
        deactivated.append(mid)
        if replacement_memory_id:
            edge_ids.append(
                insert_edge(conn, replacement_memory_id, mid, "contradicts", 0.95)
            )

    return deactivated, edge_ids


def add_memory(conn: sqlite3.Connection, payload: dict[str, Any]) -> dict[str, Any]:
    validate_memory_payload(payload)
    mem_id = payload.get("id") or f"mem_{uuid.uuid4().hex[:12]}"
    ts = now_iso()
    keywords = [
        str(x).strip() for x in ensure_list(payload.get("keywords")) if str(x).strip()
    ]
    tags = [str(x).strip() for x in ensure_list(payload.get("tags")) if str(x).strip()]
    source_refs = [
        str(x).strip()
        for x in ensure_list(payload.get("source_refs"))
        if str(x).strip()
    ]
    replaces_memory_id = payload.get("replaces_memory_id")

    row = {
        "id": mem_id,
        "memory_type": payload["memory_type"],
        "abstraction_level": int(payload.get("abstraction_level", 0)),
        "role_scope": payload.get("role_scope", "global"),
        "session_id": payload.get("session_id"),
        "task_id": payload.get("task_id"),
        "title": normalize_text(payload["title"]),
        "summary": normalize_text(payload["summary"]),
        "details_json": json.dumps(
            payload.get("details", {}), ensure_ascii=False, sort_keys=True
        ),
        "keywords_json": json.dumps(keywords, ensure_ascii=False),
        "tags_json": json.dumps(tags, ensure_ascii=False),
        "source_refs_json": json.dumps(source_refs, ensure_ascii=False),
        "importance": clamp_score(payload.get("importance", 0.5)),
        "confidence": clamp_score(payload.get("confidence", 0.5)),
        "success_score": clamp_score(payload.get("success_score", 0.5)),
        "recency_ts": payload.get("recency_ts", ts),
        "valid_from_ts": payload.get("valid_from_ts"),
        "valid_to_ts": payload.get("valid_to_ts"),
        "is_active": 1,
        "replaced_by_memory_id": None,
        "retired_reason": None,
        "created_at": ts,
        "updated_at": ts,
    }

    conn.execute(
        """
        INSERT INTO memories (
          id, memory_type, abstraction_level, role_scope, session_id, task_id, title, summary,
          details_json, keywords_json, tags_json, source_refs_json, importance, confidence,
          success_score, recency_ts, valid_from_ts, valid_to_ts, is_active, replaced_by_memory_id,
          retired_reason, created_at, updated_at
        ) VALUES (
          :id, :memory_type, :abstraction_level, :role_scope, :session_id, :task_id, :title, :summary,
          :details_json, :keywords_json, :tags_json, :source_refs_json, :importance, :confidence,
          :success_score, :recency_ts, :valid_from_ts, :valid_to_ts, :is_active, :replaced_by_memory_id,
          :retired_reason, :created_at, :updated_at
        )
        """,
        row,
    )

    upsert_fts(conn, mem_id, row["title"], row["summary"], keywords, tags)

    for edge in ensure_list(payload.get("edges")):
        if not isinstance(edge, dict):
            continue
        target = edge.get("to_memory_id")
        edge_type = edge.get("edge_type")
        if target and edge_type in {
            "similar",
            "supports",
            "contradicts",
            "extends",
            "derived_from",
        }:
            insert_edge(conn, mem_id, target, edge_type, edge.get("weight", 0.5))

    deactivated: list[str] = []
    edge_ids: list[str] = []
    if replaces_memory_id:
        deactivated, edge_ids = retire_memories(
            conn,
            [str(replaces_memory_id)],
            replacement_memory_id=mem_id,
            refresh_reason="Replaced by a newly added memory.",
        )

    conn.commit()
    return {
        "ok": True,
        "memory_id": mem_id,
        "replaces_memory_id": replaces_memory_id,
        "retired_memory_ids": deactivated,
        "edge_ids": edge_ids,
    }


def fetch_candidate_pool(
    conn: sqlite3.Connection, payload: dict[str, Any], allowed_types: tuple[str, ...]
) -> list[sqlite3.Row]:
    session_id = payload.get("session_id")
    task_id = payload.get("task_id")
    goal = payload.get("goal", "")
    constraints = " ".join(ensure_list(payload.get("user_constraints")))
    failures = " ".join(ensure_list(payload.get("recent_failures")))
    unresolved = " ".join(ensure_list(payload.get("unresolved_questions")))

    placeholders = ",".join("?" for _ in allowed_types)
    rows_by_id: dict[str, sqlite3.Row] = {}

    def ingest(rows: list[sqlite3.Row]) -> None:
        for row in rows:
            rows_by_id[row["id"]] = row

    match_query = build_match_query(goal, constraints, failures, unresolved)
    if match_query:
        fts_rows = conn.execute(
            f"""
            SELECT m.*
            FROM memories m
            JOIN memories_fts f ON m.id = f.id
            WHERE m.is_active = 1
              AND m.memory_type IN ({placeholders})
              AND memories_fts MATCH ?
            LIMIT 80
            """,
            [*allowed_types, match_query],
        ).fetchall()
        ingest(fts_rows)

    if task_id:
        task_rows = conn.execute(
            f"""
            SELECT * FROM memories
            WHERE is_active = 1 AND memory_type IN ({placeholders}) AND task_id = ?
            ORDER BY importance DESC, updated_at DESC
            LIMIT 40
            """,
            [*allowed_types, task_id],
        ).fetchall()
        ingest(task_rows)

    if session_id:
        session_rows = conn.execute(
            f"""
            SELECT * FROM memories
            WHERE is_active = 1 AND memory_type IN ({placeholders}) AND session_id = ?
            ORDER BY importance DESC, updated_at DESC
            LIMIT 40
            """,
            [*allowed_types, session_id],
        ).fetchall()
        ingest(session_rows)

    durable_rows = conn.execute(
        f"""
        SELECT * FROM memories
        WHERE is_active = 1
          AND memory_type IN ({placeholders})
          AND (abstraction_level >= 2 OR role_scope = 'global')
        ORDER BY importance DESC, updated_at DESC
        LIMIT 40
        """,
        [*allowed_types],
    ).fetchall()
    ingest(durable_rows)

    recent_rows = conn.execute(
        f"""
        SELECT * FROM memories
        WHERE is_active = 1 AND memory_type IN ({placeholders})
        ORDER BY updated_at DESC
        LIMIT 50
        """,
        [*allowed_types],
    ).fetchall()
    ingest(recent_rows)

    return list(rows_by_id.values())


def classify_block(row: sqlite3.Row, payload: dict[str, Any]) -> str:
    task_id = payload.get("task_id")
    session_id = payload.get("session_id")
    if task_id and row["task_id"] == task_id:
        return "task_scoped"
    if session_id and row["session_id"] == session_id:
        return "session_scoped"
    if row["role_scope"] == "global" or int(row["abstraction_level"]) >= 2:
        return "durable_global"
    return "recent_fallback"


def edge_bonus(conn: sqlite3.Connection, mem_id: str) -> tuple[float, float]:
    rows = conn.execute(
        """
        SELECT from_memory_id, to_memory_id, edge_type, weight
        FROM memory_edges
        WHERE from_memory_id = ? OR to_memory_id = ?
        """,
        (mem_id, mem_id),
    ).fetchall()
    support = 0.0
    contradiction = 0.0
    for row in rows:
        if row["edge_type"] in {"supports", "extends", "similar", "derived_from"}:
            support += float(row["weight"])
        elif row["edge_type"] == "contradicts":
            if row["to_memory_id"] == mem_id:
                contradiction += float(row["weight"])
    return min(support, 1.0), min(contradiction, 1.0)


def score_block(
    name: str, rows: list[sqlite3.Row], payload: dict[str, Any], step_role: str
) -> BlockDecision:
    if not rows:
        return BlockDecision(
            name=name,
            score=0.0,
            candidate_count=0,
            selected=False,
            reasons=["empty"],
            top_memory_ids=[],
        )

    goal_terms = tokenize_for_match(str(payload.get("goal", "")))
    unresolved_terms = tokenize_for_match(
        " ".join(str(x) for x in ensure_list(payload.get("unresolved_questions")))
    )
    failure_terms = tokenize_for_match(
        " ".join(str(x) for x in ensure_list(payload.get("recent_failures")))
    )

    role_signal = max(
        1.0 if row["role_scope"] in {step_role, "global"} else 0.0 for row in rows
    )
    goal_signal = max(
        overlap_score(
            goal_terms,
            tokenize_for_match(
                " ".join(
                    [
                        row["title"] or "",
                        row["summary"] or "",
                        " ".join(loads_json_field(row["keywords_json"], [])),
                    ]
                )
            ),
        )
        for row in rows
    )
    unresolved_signal = (
        max(
            overlap_score(
                unresolved_terms,
                tokenize_for_match(
                    " ".join(
                        [
                            row["summary"] or "",
                            " ".join(loads_json_field(row["tags_json"], [])),
                        ]
                    )
                ),
            )
            for row in rows
        )
        if unresolved_terms
        else 0.0
    )
    failure_signal = (
        max(
            overlap_score(
                failure_terms,
                tokenize_for_match(
                    " ".join(
                        [
                            row["summary"] or "",
                            " ".join(loads_json_field(row["tags_json"], [])),
                        ]
                    )
                ),
            )
            for row in rows
        )
        if failure_terms
        else 0.0
    )
    freshness_signal = max(
        hours_ago_score(row["recency_ts"] or row["updated_at"]) for row in rows
    )
    scope_bias = {
        "task_scoped": 1.0 if payload.get("task_id") else 0.0,
        "session_scoped": 1.0 if payload.get("session_id") else 0.0,
        "durable_global": 0.72,
        "recent_fallback": 0.55,
    }[name]

    score = (
        0.30 * scope_bias
        + 0.24 * role_signal
        + 0.22 * goal_signal
        + 0.12 * unresolved_signal
        + 0.06 * freshness_signal
        + 0.06 * failure_signal
    )

    top_rows = sorted(
        rows,
        key=lambda row: (
            -clamp_score(row["importance"]),
            -timestamp_sort_value(row["updated_at"]),
            TYPE_PRIORITY.get(row["memory_type"], 99),
        ),
    )[:4]
    reasons = [
        f"scope-bias:{scope_bias:.2f}",
        f"role-signal:{role_signal:.2f}",
        f"goal-signal:{goal_signal:.2f}",
    ]
    if unresolved_terms:
        reasons.append(f"unresolved-signal:{unresolved_signal:.2f}")
    if failure_terms:
        reasons.append(f"failure-signal:{failure_signal:.2f}")

    return BlockDecision(
        name=name,
        score=round(score, 6),
        candidate_count=len(rows),
        selected=False,
        reasons=reasons,
        top_memory_ids=[row["id"] for row in top_rows],
    )


def score_row(
    conn: sqlite3.Connection,
    row: sqlite3.Row,
    payload: dict[str, Any],
    step_role: str,
    block_name: str,
    block_score: float,
) -> Candidate:
    goal = payload.get("goal", "")
    constraints = " ".join(ensure_list(payload.get("user_constraints")))
    failures = " ".join(ensure_list(payload.get("recent_failures")))
    unresolved = " ".join(ensure_list(payload.get("unresolved_questions")))
    task_id = payload.get("task_id")
    session_id = payload.get("session_id")

    mem_text = " ".join(
        [
            row["title"] or "",
            row["summary"] or "",
            " ".join(loads_json_field(row["keywords_json"], [])),
            " ".join(loads_json_field(row["tags_json"], [])),
        ]
    )
    req_terms = tokenize_for_match(" ".join([goal, constraints, failures, unresolved]))
    mem_terms = tokenize_for_match(mem_text)

    role_scope = row["role_scope"]
    role_match = 1.0 if role_scope in {step_role, "global"} else 0.0
    goal_overlap = overlap_score(req_terms, mem_terms)
    task_match = 1.0 if task_id and row["task_id"] == task_id else 0.0
    session_match = 1.0 if session_id and row["session_id"] == session_id else 0.0
    freshness = hours_ago_score(row["recency_ts"] or row["updated_at"])
    support, contradiction = edge_bonus(conn, row["id"])

    importance = clamp_score(row["importance"])
    confidence = clamp_score(row["confidence"])
    success = clamp_score(row["success_score"])

    score = (
        0.16 * role_match
        + 0.18 * goal_overlap
        + 0.14 * task_match
        + 0.08 * session_match
        + 0.13 * importance
        + 0.10 * confidence
        + 0.08 * success
        + 0.06 * freshness
        + 0.08 * support
        + 0.06 * block_score
        - 0.04 * contradiction
    )

    reasons: list[str] = [f"block:{block_name}"]
    if role_match:
        reasons.append(f"role:{role_scope}")
    if task_match:
        reasons.append("task-match")
    if session_match:
        reasons.append("session-match")
    if goal_overlap > 0:
        reasons.append(f"overlap:{goal_overlap:.2f}")
    if importance >= 0.75:
        reasons.append("high-importance")
    if support > 0:
        reasons.append(f"graph-support:{support:.2f}")
    if contradiction > 0:
        reasons.append(f"graph-contradiction:{contradiction:.2f}")

    return Candidate(row=row, block=block_name, score=round(score, 6), reasons=reasons)


def dedupe_keep_order(items: list[str], limit: int | None = None) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        item = normalize_text(item)
        if not item or item in seen:
            continue
        out.append(item)
        seen.add(item)
        if limit and len(out) >= limit:
            break
    return out


def extract_constraints(
    selected: list[sqlite3.Row], user_constraints: list[str]
) -> list[str]:
    items = list(user_constraints)
    for row in selected:
        if row["memory_type"] != "preference":
            continue
        items.append(row["summary"])
        details = loads_json_field(row["details_json"], {})
        if isinstance(details, dict):
            for key in ("hard_constraint", "constraint", "must"):
                value = details.get(key)
                if isinstance(value, str):
                    items.append(value)
                elif isinstance(value, list):
                    items.extend(str(x) for x in value)
    return dedupe_keep_order(items, limit=4)


def extract_relevant_facts(selected: list[sqlite3.Row]) -> list[str]:
    items: list[str] = []
    for row in selected:
        if row["memory_type"] in {"summary", "episode"}:
            items.append(row["summary"])
    return dedupe_keep_order(items, limit=3)


def extract_procedures(selected: list[sqlite3.Row]) -> list[str]:
    items = [row["summary"] for row in selected if row["memory_type"] == "procedure"]
    return dedupe_keep_order(items, limit=3)


def extract_pitfalls(
    selected: list[sqlite3.Row], recent_failures: list[str]
) -> list[str]:
    items = list(recent_failures)
    for row in selected:
        if row["memory_type"] == "reflection":
            items.append(row["summary"])
        tags = loads_json_field(row["tags_json"], [])
        if any(tag in {"failure", "pitfall", "warning"} for tag in tags):
            items.append(row["summary"])
    return dedupe_keep_order(items, limit=3)


def route_memory(conn: sqlite3.Connection, payload: dict[str, Any]) -> dict[str, Any]:
    goal = normalize_text(str(payload.get("goal", "")))
    if not goal:
        error("route requires goal")

    step_role = payload.get("step_role", "planner")
    if step_role not in ROLE_TO_TYPES:
        error("step_role must be planner|executor|critic|responder")

    allowed_types = ROLE_TO_TYPES[step_role]
    pool = fetch_candidate_pool(conn, payload, allowed_types)

    rows_by_block: dict[str, list[sqlite3.Row]] = {name: [] for name in BLOCK_PRIORITY}
    for row in pool:
        rows_by_block[classify_block(row, payload)].append(row)

    block_decisions = [
        score_block(name, rows, payload, step_role)
        for name, rows in rows_by_block.items()
    ]
    block_decisions.sort(key=lambda block: (-block.score, BLOCK_PRIORITY[block.name]))
    selected_block_names = {
        block.name for block in block_decisions[:3] if block.candidate_count > 0
    }

    selected_blocks_debug: list[dict[str, Any]] = []
    for block in block_decisions:
        selected_flag = block.name in selected_block_names
        selected_blocks_debug.append(
            {
                "block": block.name,
                "selected": selected_flag,
                "score": block.score,
                "candidate_count": block.candidate_count,
                "reasons": block.reasons,
                "top_memory_ids": block.top_memory_ids,
            }
        )

    scored: list[Candidate] = []
    block_score_lookup = {block.name: block.score for block in block_decisions}
    for block_name in selected_block_names:
        for row in rows_by_block[block_name]:
            scored.append(
                score_row(
                    conn,
                    row,
                    payload,
                    step_role,
                    block_name,
                    block_score_lookup[block_name],
                )
            )

    scored.sort(
        key=lambda cand: (
            -cand.score,
            TYPE_PRIORITY.get(cand.row["memory_type"], 99),
            -clamp_score(cand.row["importance"]),
            -timestamp_sort_value(cand.row["updated_at"]),
            BLOCK_PRIORITY.get(cand.block, 99),
        )
    )

    selected_rows = [cand.row for cand in scored[:5]]
    packet = {
        "goal": goal,
        "step_role": step_role,
        "hard_constraints": extract_constraints(
            selected_rows,
            [str(x) for x in ensure_list(payload.get("user_constraints"))],
        ),
        "relevant_facts": extract_relevant_facts(selected_rows),
        "procedures_to_follow": extract_procedures(selected_rows),
        "pitfalls_to_avoid": extract_pitfalls(
            selected_rows, [str(x) for x in ensure_list(payload.get("recent_failures"))]
        ),
        "open_questions": dedupe_keep_order(
            [str(x) for x in ensure_list(payload.get("unresolved_questions"))], limit=5
        ),
        "selected_memory_ids": [row["id"] for row in selected_rows],
    }

    packet_id = f"pkt_{uuid.uuid4().hex[:12]}"
    conn.execute(
        """
        INSERT INTO working_memory_packets(id, session_id, task_id, step_role, goal, packet_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            packet_id,
            payload.get("session_id") or "unknown-session",
            payload.get("task_id"),
            step_role,
            goal,
            json.dumps(packet, ensure_ascii=False),
            now_iso(),
        ),
    )
    conn.commit()

    debug = {
        "selected_blocks": selected_blocks_debug,
        "selected_memories": [
            {
                "id": cand.row["id"],
                "memory_type": cand.row["memory_type"],
                "block": cand.block,
                "score": cand.score,
                "title": cand.row["title"],
                "reasons": cand.reasons,
            }
            for cand in scored[:8]
        ],
    }

    return {"ok": True, "packet_id": packet_id, "packet": packet, "debug": debug}


def reflect_memory(conn: sqlite3.Connection, payload: dict[str, Any]) -> dict[str, Any]:
    goal = normalize_text(str(payload.get("goal", "")))
    outcome = normalize_text(str(payload.get("outcome", ""))) or "unknown"
    worked = [str(x) for x in ensure_list(payload.get("what_worked"))]
    failed = [str(x) for x in ensure_list(payload.get("what_failed"))]
    lessons = [str(x) for x in ensure_list(payload.get("lessons"))]
    next_time = [str(x) for x in ensure_list(payload.get("next_time"))]
    session_id = payload.get("session_id")
    task_id = payload.get("task_id")

    reflection_bits: list[str] = []
    if goal:
        reflection_bits.append(f"Goal: {goal}.")
    reflection_bits.append(f"Outcome: {outcome}.")
    if worked:
        reflection_bits.append("Worked: " + "; ".join(worked) + ".")
    if failed:
        reflection_bits.append("Failed: " + "; ".join(failed) + ".")
    if lessons:
        reflection_bits.append("Lessons: " + "; ".join(lessons) + ".")
    if next_time:
        reflection_bits.append("Next time: " + "; ".join(next_time) + ".")

    reflection_summary = " ".join(reflection_bits).strip()
    reflection_payload = {
        "memory_type": "reflection",
        "abstraction_level": 2,
        "role_scope": "critic",
        "session_id": session_id,
        "task_id": task_id,
        "title": payload.get("reflection_title")
        or f"Reflection for {goal or task_id or session_id or 'task'}",
        "summary": reflection_summary,
        "details": {
            "goal": goal,
            "outcome": outcome,
            "what_worked": worked,
            "what_failed": failed,
            "lessons": lessons,
            "next_time": next_time,
        },
        "keywords": tokenize_for_match(
            " ".join([goal, outcome, *worked, *failed, *lessons, *next_time])
        ),
        "tags": ["reflection"] + (["failure"] if failed else ["success"]),
        "source_refs": ensure_list(payload.get("source_refs")),
        "importance": clamp_score(payload.get("importance", 0.8)),
        "confidence": clamp_score(payload.get("confidence", 0.8)),
        "success_score": (
            0.9 if outcome.lower() in {"completed", "success", "succeeded"} else 0.5
        ),
    }
    reflection_result = add_memory(conn, reflection_payload)

    out = {"ok": True, "reflection_memory_id": reflection_result["memory_id"]}

    if payload.get("create_procedure"):
        proc_steps = [*worked, *lessons, *next_time]
        proc_steps = dedupe_keep_order(proc_steps, limit=5)
        if proc_steps:
            proc_summary = "Follow this workflow: " + " | ".join(proc_steps)
            procedure_payload = {
                "memory_type": "procedure",
                "abstraction_level": 2,
                "role_scope": "planner",
                "session_id": session_id,
                "task_id": task_id,
                "title": payload.get("procedure_title")
                or f"Procedure for {goal or task_id or session_id or 'task'}",
                "summary": proc_summary,
                "details": {"steps": proc_steps},
                "keywords": tokenize_for_match(" ".join([goal, *proc_steps])),
                "tags": ["procedure", "derived"],
                "source_refs": ensure_list(payload.get("source_refs")),
                "importance": clamp_score(payload.get("procedure_importance", 0.82)),
                "confidence": clamp_score(payload.get("procedure_confidence", 0.78)),
                "success_score": 0.85,
                "edges": [
                    {
                        "to_memory_id": reflection_result["memory_id"],
                        "edge_type": "derived_from",
                        "weight": 0.8,
                    }
                ],
            }
            proc_result = add_memory(conn, procedure_payload)
            out["procedure_memory_id"] = proc_result["memory_id"]

    return out


def refresh_memory(conn: sqlite3.Connection, payload: dict[str, Any]) -> dict[str, Any]:
    stale_ids = [
        str(x) for x in ensure_list(payload.get("stale_memory_ids")) if str(x).strip()
    ]
    replacement = payload.get("replacement_memory_id")
    reason = (
        normalize_text(str(payload.get("refresh_reason", ""))) or "Retired by refresh."
    )

    if not stale_ids:
        error("refresh requires stale_memory_ids")

    deactivated, edge_ids = retire_memories(
        conn,
        stale_ids,
        replacement_memory_id=str(replacement) if replacement else None,
        refresh_reason=reason,
    )
    conn.commit()
    return {
        "ok": True,
        "deactivated": deactivated,
        "replacement_memory_id": replacement,
        "refresh_reason": reason,
        "edge_ids": edge_ids,
    }


def list_memories(conn: sqlite3.Connection, limit: int) -> dict[str, Any]:
    rows = conn.execute(
        """
        SELECT id, memory_type, role_scope, task_id, session_id, title, importance, confidence,
               success_score, is_active, replaced_by_memory_id, retired_reason, updated_at
        FROM memories
        ORDER BY updated_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    items = [dict(row) for row in rows]
    return {"ok": True, "items": items}


def inspect_memory(conn: sqlite3.Connection, memory_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM memories WHERE id = ?", (memory_id,)).fetchone()
    if not row:
        error(f"memory not found: {memory_id}")
    edge_rows = conn.execute(
        """
        SELECT * FROM memory_edges
        WHERE from_memory_id = ? OR to_memory_id = ?
        ORDER BY created_at DESC
        """,
        (memory_id, memory_id),
    ).fetchall()
    return {
        "ok": True,
        "memory": row_to_dict(row),
        "edges": [dict(r) for r in edge_rows],
    }


def list_packets(conn: sqlite3.Connection, limit: int) -> dict[str, Any]:
    rows = conn.execute(
        """
        SELECT id, session_id, task_id, step_role, goal, packet_json, created_at
        FROM working_memory_packets
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    items = []
    for row in rows:
        items.append(
            {
                "id": row["id"],
                "session_id": row["session_id"],
                "task_id": row["task_id"],
                "step_role": row["step_role"],
                "goal": row["goal"],
                "packet": loads_json_field(row["packet_json"], {}),
                "created_at": row["created_at"],
            }
        )
    return {"ok": True, "items": items}


def parse_payload(raw: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        error(f"invalid JSON input: {exc}")
    if not isinstance(payload, dict):
        error("input JSON must be an object")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Memory Attention Router")
    parser.add_argument(
        "--db",
        help="Override DB path; otherwise MAR_DB_PATH or default local file is used.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    p_add = sub.add_parser("add")
    p_add.add_argument("--input-json", required=True)

    p_route = sub.add_parser("route")
    p_route.add_argument("--input-json", required=True)

    p_reflect = sub.add_parser("reflect")
    p_reflect.add_argument("--input-json", required=True)

    p_refresh = sub.add_parser("refresh")
    p_refresh.add_argument("--input-json", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--limit", type=int, default=20)

    p_packets = sub.add_parser("packets")
    p_packets.add_argument("--limit", type=int, default=10)

    p_inspect = sub.add_parser("inspect")
    p_inspect.add_argument("--memory-id", required=True)

    args = parser.parse_args()
    conn = connect(args.db)

    try:
        schema_state = ensure_schema(conn)

        if args.cmd == "init":
            result = {"ok": True, **schema_state, "db_path": get_db_path(args.db)}
        elif args.cmd == "add":
            result = add_memory(conn, parse_payload(args.input_json))
        elif args.cmd == "route":
            result = route_memory(conn, parse_payload(args.input_json))
        elif args.cmd == "reflect":
            result = reflect_memory(conn, parse_payload(args.input_json))
        elif args.cmd == "refresh":
            result = refresh_memory(conn, parse_payload(args.input_json))
        elif args.cmd == "list":
            result = list_memories(conn, args.limit)
        elif args.cmd == "inspect":
            result = inspect_memory(conn, args.memory_id)
        elif args.cmd == "packets":
            result = list_packets(conn, args.limit)
        else:
            error(f"unknown command: {args.cmd}")
    finally:
        conn.close()

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
