#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import statistics
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

DEFAULT_ROOT = Path.home() / ".openclaw" / "agents"


@dataclass
class SessionMeta:
    agent: str
    session_id: str
    session_key: str | None = None
    display_name: str | None = None
    label: str | None = None
    channel: str | None = None
    group_channel: str | None = None
    group_id: str | None = None
    space: str | None = None
    chat_type: str | None = None
    status: str | None = None
    model_provider: str | None = None
    model: str | None = None
    started_at: str | None = None
    updated_at: str | None = None
    spawned_by: str | None = None
    spawned_by_session_id: str | None = None
    spawn_depth: int | None = None
    subagent_role: str | None = None
    session_file: str | None = None
    cwd: str | None = None


@dataclass
class UsageRow:
    timestamp: str
    agent: str
    session_id: str
    session_key: str | None
    session_label: str | None
    parent_session_key: str | None
    parent_session_id: str | None
    spawn_depth: int | None
    subagent_role: str | None
    channel: str | None
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    total_tokens: int
    cost_input_usd: float
    cost_output_usd: float
    cost_cache_read_usd: float
    cost_cache_write_usd: float
    cost_total_usd: float


@dataclass
class Totals:
    calls: int
    total_tokens: int
    cost_total_usd: float
    agents: int
    sessions: int
    models: int
    first_timestamp: str | None
    last_timestamp: str | None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Summarize local OpenClaw model usage from session JSONL files.")
    p.add_argument(
        "command",
        choices=[
            "overview",
            "summary",
            "current",
            "recent",
            "rows",
            "agents",
            "top-agents",
            "daily",
            "sessions",
            "top-sessions",
            "subagents",
            "session-tree",
            "dashboard",
        ],
        nargs="?",
        default="overview",
    )
    p.add_argument("--root", default=str(DEFAULT_ROOT), help="OpenClaw agents root (default: ~/.openclaw/agents)")
    p.add_argument("--agent", action="append", help="Limit to one or more agents")
    p.add_argument("--provider", action="append", help="Limit to one or more providers")
    p.add_argument("--model", action="append", help="Limit to one or more models")
    p.add_argument("--session-id", action="append", help="Limit to one or more session IDs")
    p.add_argument("--channel", action="append", help="Limit to one or more channels")
    p.add_argument("--since-days", type=int, default=30, help="Look back N days (default: 30, 0 = all)")
    p.add_argument("--limit", type=int, default=5, help="Limit rows for top/recent/daily/session listings (default: 5)")
    p.add_argument("--json", action="store_true", help="Emit JSON output")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    p.add_argument("--out", help="Output path for generated dashboard HTML")
    p.add_argument("--title", default="OpenClaw Model Usage Dashboard", help="Dashboard title for HTML output")
    return p


def iter_agent_dirs(root: Path, agents: set[str] | None) -> Iterable[tuple[str, Path]]:
    if not root.exists():
        return
    for agent_dir in sorted(root.iterdir()):
        if not agent_dir.is_dir():
            continue
        agent = agent_dir.name
        if agents and agent not in agents:
            continue
        yield agent, agent_dir


def iter_session_files(root: Path, agents: set[str] | None) -> Iterable[tuple[str, Path]]:
    for agent, agent_dir in iter_agent_dirs(root, agents):
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.exists():
            continue
        for path in sorted(sessions_dir.glob("*.jsonl")):
            yield agent, path


def parse_timestamp(value: str | None) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except Exception:
        return None


def epoch_ms_to_iso(value: Any) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def load_sessions_index(root: Path, agents: set[str] | None) -> dict[tuple[str, str], SessionMeta]:
    by_session: dict[tuple[str, str], SessionMeta] = {}
    key_to_session_id: dict[tuple[str, str], str] = {}
    global_key_to_session_id: dict[str, str] = {}

    for agent, agent_dir in iter_agent_dirs(root, agents):
        index_path = agent_dir / "sessions" / "sessions.json"
        if not index_path.exists():
            continue
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue

        for session_key, item in data.items():
            if not isinstance(item, dict):
                continue
            session_id = item.get("sessionId")
            if not isinstance(session_id, str):
                continue
            meta = SessionMeta(
                agent=agent,
                session_id=session_id,
                session_key=session_key if isinstance(session_key, str) else None,
                display_name=item.get("displayName") if isinstance(item.get("displayName"), str) else None,
                label=item.get("label") if isinstance(item.get("label"), str) else None,
                channel=item.get("channel") if isinstance(item.get("channel"), str) else None,
                group_channel=item.get("groupChannel") if isinstance(item.get("groupChannel"), str) else None,
                group_id=item.get("groupId") if isinstance(item.get("groupId"), str) else None,
                space=item.get("space") if isinstance(item.get("space"), str) else None,
                chat_type=item.get("chatType") if isinstance(item.get("chatType"), str) else None,
                status=item.get("status") if isinstance(item.get("status"), str) else None,
                model_provider=item.get("modelProvider") if isinstance(item.get("modelProvider"), str) else None,
                model=item.get("model") if isinstance(item.get("model"), str) else None,
                started_at=epoch_ms_to_iso(item.get("startedAt")),
                updated_at=epoch_ms_to_iso(item.get("updatedAt")),
                spawned_by=item.get("spawnedBy") if isinstance(item.get("spawnedBy"), str) else None,
                spawned_by_session_id=None,
                spawn_depth=int(item.get("spawnDepth")) if isinstance(item.get("spawnDepth"), int) else None,
                subagent_role=item.get("subagentRole") if isinstance(item.get("subagentRole"), str) else None,
                session_file=item.get("sessionFile") if isinstance(item.get("sessionFile"), str) else None,
                cwd=item.get("spawnedWorkspaceDir") if isinstance(item.get("spawnedWorkspaceDir"), str) else None,
            )
            by_session[(agent, session_id)] = meta
            if meta.session_key:
                key_to_session_id[(agent, meta.session_key)] = session_id
                global_key_to_session_id[meta.session_key] = session_id

    for meta in by_session.values():
        if meta.spawned_by:
            meta.spawned_by_session_id = key_to_session_id.get((meta.agent, meta.spawned_by)) or global_key_to_session_id.get(meta.spawned_by)

    return by_session


def extract_text_content(message: dict[str, Any]) -> str | None:
    content = message.get("content")
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str):
                return part["text"]
    if isinstance(content, str):
        return content
    return None


def infer_meta_from_text(text: str) -> dict[str, Any]:
    inferred: dict[str, Any] = {}
    if "[Subagent Context]" not in text and "# Subagent Context" not in text:
        return inferred

    depth_match = re.search(r"subagent \(depth\s+(\d+)/(\d+)\)", text, flags=re.IGNORECASE)
    if depth_match:
        inferred["spawn_depth"] = int(depth_match.group(1))

    task_match = re.search(r"\[Subagent Task\]:\s*(.+)", text)
    if task_match:
        inferred["label"] = task_match.group(1).strip()

    requester_match = re.search(r"Requester session:\s*(\S+)", text)
    if requester_match:
        inferred["spawned_by"] = requester_match.group(1).strip()

    session_match = re.search(r"Your session:\s*(\S+)", text)
    if session_match:
        inferred["session_key"] = session_match.group(1).strip()

    channel_match = re.search(r"Requester channel:\s*([^\n]+)", text)
    if channel_match:
        channel_text = channel_match.group(1).strip()
        if channel_text:
            inferred["channel"] = channel_text.split()[0]

    if inferred:
        inferred.setdefault("subagent_role", "leaf")
    return inferred


def load_session_hints(root: Path, agents: set[str] | None) -> dict[tuple[str, str], dict[str, Any]]:
    hints: dict[tuple[str, str], dict[str, Any]] = {}
    for agent, path in iter_session_files(root, agents):
        session_id = path.stem
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if line_number == 1 and obj.get("type") == "session":
                        hints[(agent, session_id)] = obj
                        header_id = obj.get("id")
                        if isinstance(header_id, str) and header_id:
                            hints.setdefault((agent, header_id), obj)
                        continue
                    if obj.get("type") != "message":
                        continue
                    message = obj.get("message") or {}
                    if message.get("role") != "user":
                        continue
                    text = extract_text_content(message)
                    if not text:
                        continue
                    inferred = infer_meta_from_text(text)
                    if inferred:
                        hints.setdefault((agent, session_id), {}).update(inferred)
                    break
        except OSError:
            continue
    return hints


def merge_session_meta(index_meta: SessionMeta | None, hint: dict[str, Any] | None, agent: str, session_id: str) -> SessionMeta:
    meta = index_meta or SessionMeta(agent=agent, session_id=session_id)
    if hint:
        if isinstance(hint.get("timestamp"), str) and not meta.started_at:
            meta.started_at = hint["timestamp"]
        if isinstance(hint.get("cwd"), str) and not meta.cwd:
            meta.cwd = hint["cwd"]
        if isinstance(hint.get("label"), str) and not meta.label:
            meta.label = hint["label"]
        if isinstance(hint.get("channel"), str) and not meta.channel:
            meta.channel = hint["channel"]
        if isinstance(hint.get("session_key"), str) and not meta.session_key:
            meta.session_key = hint["session_key"]
        if isinstance(hint.get("spawned_by"), str) and not meta.spawned_by:
            meta.spawned_by = hint["spawned_by"]
        if isinstance(hint.get("spawn_depth"), int) and meta.spawn_depth is None:
            meta.spawn_depth = hint["spawn_depth"]
        if isinstance(hint.get("subagent_role"), str) and not meta.subagent_role:
            meta.subagent_role = hint["subagent_role"]
    if not meta.session_file:
        meta.session_file = str(DEFAULT_ROOT / agent / "sessions" / f"{session_id}.jsonl")
    return meta


def load_rows(
    root: Path,
    agents: set[str] | None,
    providers: set[str] | None,
    models: set[str] | None,
    session_ids: set[str] | None,
    channels: set[str] | None,
    since_days: int,
) -> tuple[list[UsageRow], dict[tuple[str, str], SessionMeta]]:
    rows: list[UsageRow] = []
    cutoff = None
    if since_days and since_days > 0:
        cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)

    session_index = load_sessions_index(root, agents)
    session_hints = load_session_hints(root, agents)
    session_meta: dict[tuple[str, str], SessionMeta] = {}

    session_files = list(iter_session_files(root, agents))
    for agent, path in session_files:
        session_id = path.stem
        meta = merge_session_meta(session_index.get((agent, session_id)), session_hints.get((agent, session_id)), agent, session_id)
        session_meta[(agent, session_id)] = meta

    key_to_session_id = {(meta.agent, meta.session_key): meta.session_id for meta in session_meta.values() if meta.session_key}
    global_key_to_session_id = {meta.session_key: meta.session_id for meta in session_meta.values() if meta.session_key}
    for meta in session_meta.values():
        if meta.spawned_by and not meta.spawned_by_session_id:
            meta.spawned_by_session_id = key_to_session_id.get((meta.agent, meta.spawned_by)) or global_key_to_session_id.get(meta.spawned_by)

    for agent, path in session_files:
        session_id = path.stem
        meta = session_meta[(agent, session_id)]
        if session_ids and session_id not in session_ids:
            continue
        if channels and (meta.channel not in channels):
            continue
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("type") != "message":
                        continue
                    message = obj.get("message") or {}
                    if message.get("role") != "assistant":
                        continue
                    usage = message.get("usage") or {}
                    provider = message.get("provider")
                    model = message.get("model")
                    ts = obj.get("timestamp")
                    if not isinstance(provider, str) or not isinstance(model, str) or not isinstance(ts, str):
                        continue
                    dt = parse_timestamp(ts)
                    if cutoff and (dt is None or dt < cutoff):
                        continue
                    if providers and provider not in providers:
                        continue
                    if models and model not in models:
                        continue
                    cost = usage.get("cost") or {}
                    rows.append(
                        UsageRow(
                            timestamp=ts,
                            agent=agent,
                            session_id=session_id,
                            session_key=meta.session_key,
                            session_label=meta.label or meta.display_name,
                            parent_session_key=meta.spawned_by,
                            parent_session_id=meta.spawned_by_session_id,
                            spawn_depth=meta.spawn_depth,
                            subagent_role=meta.subagent_role,
                            channel=meta.channel,
                            provider=provider,
                            model=model,
                            input_tokens=int(usage.get("input") or 0),
                            output_tokens=int(usage.get("output") or 0),
                            cache_read_tokens=int(usage.get("cacheRead") or 0),
                            cache_write_tokens=int(usage.get("cacheWrite") or 0),
                            total_tokens=int(usage.get("totalTokens") or 0),
                            cost_input_usd=float(cost.get("input") or 0.0),
                            cost_output_usd=float(cost.get("output") or 0.0),
                            cost_cache_read_usd=float(cost.get("cacheRead") or 0.0),
                            cost_cache_write_usd=float(cost.get("cacheWrite") or 0.0),
                            cost_total_usd=float(cost.get("total") or 0.0),
                        )
                    )
        except OSError:
            continue
    rows.sort(key=lambda r: r.timestamp)
    return rows, session_meta


def summarise_by_model(rows: list[UsageRow]) -> dict[str, Any]:
    by_model: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_read_tokens": 0,
            "cache_write_tokens": 0,
            "total_tokens": 0,
            "cost_total_usd": 0.0,
            "agents": set(),
            "sessions": set(),
            "last_timestamp": None,
        }
    )
    for row in rows:
        item = by_model[(row.provider, row.model)]
        item["calls"] += 1
        item["input_tokens"] += row.input_tokens
        item["output_tokens"] += row.output_tokens
        item["cache_read_tokens"] += row.cache_read_tokens
        item["cache_write_tokens"] += row.cache_write_tokens
        item["total_tokens"] += row.total_tokens
        item["cost_total_usd"] += row.cost_total_usd
        item["agents"].add(row.agent)
        item["sessions"].add(row.session_id)
        item["last_timestamp"] = row.timestamp
    models_out = []
    for (provider, model), item in sorted(by_model.items(), key=lambda kv: kv[1]["cost_total_usd"], reverse=True):
        models_out.append(
            {
                "provider": provider,
                "model": model,
                "calls": item["calls"],
                "input_tokens": item["input_tokens"],
                "output_tokens": item["output_tokens"],
                "cache_read_tokens": item["cache_read_tokens"],
                "cache_write_tokens": item["cache_write_tokens"],
                "total_tokens": item["total_tokens"],
                "cost_total_usd": round(item["cost_total_usd"], 6),
                "agents": sorted(item["agents"]),
                "sessions": len(item["sessions"]),
                "last_timestamp": item["last_timestamp"],
            }
        )
    return {"rows": len(rows), "models": models_out}


def summarise_by_agent(rows: list[UsageRow]) -> dict[str, Any]:
    by_agent: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "calls": 0,
            "total_tokens": 0,
            "cost_total_usd": 0.0,
            "models": set(),
            "sessions": set(),
            "last_timestamp": None,
        }
    )
    for row in rows:
        item = by_agent[row.agent]
        item["calls"] += 1
        item["total_tokens"] += row.total_tokens
        item["cost_total_usd"] += row.cost_total_usd
        item["models"].add(f"{row.provider}/{row.model}")
        item["sessions"].add(row.session_id)
        item["last_timestamp"] = row.timestamp
    agents_out = []
    for agent, item in sorted(by_agent.items(), key=lambda kv: kv[1]["cost_total_usd"], reverse=True):
        agents_out.append(
            {
                "agent": agent,
                "calls": item["calls"],
                "sessions": len(item["sessions"]),
                "total_tokens": item["total_tokens"],
                "cost_total_usd": round(item["cost_total_usd"], 6),
                "models": sorted(item["models"]),
                "last_timestamp": item["last_timestamp"],
            }
        )
    return {"rows": len(rows), "agents": agents_out}


def summarise_daily(rows: list[UsageRow]) -> dict[str, Any]:
    by_day: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(lambda: {"calls": 0, "total_tokens": 0, "cost_total_usd": 0.0})
    for row in rows:
        key = (row.timestamp[:10], row.provider, row.model)
        item = by_day[key]
        item["calls"] += 1
        item["total_tokens"] += row.total_tokens
        item["cost_total_usd"] += row.cost_total_usd
    daily_out = []
    for (day, provider, model), item in sorted(by_day.items(), key=lambda kv: (kv[0][0], kv[1]["cost_total_usd"]), reverse=True):
        daily_out.append(
            {
                "date": day,
                "provider": provider,
                "model": model,
                "calls": item["calls"],
                "total_tokens": item["total_tokens"],
                "cost_total_usd": round(item["cost_total_usd"], 6),
            }
        )
    return {"rows": len(rows), "daily": daily_out}


def summarise_by_session(rows: list[UsageRow], session_meta: dict[tuple[str, str], SessionMeta]) -> dict[str, Any]:
    by_session: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "calls": 0,
            "total_tokens": 0,
            "cost_total_usd": 0.0,
            "models": set(),
            "first_timestamp": None,
            "last_timestamp": None,
        }
    )
    for row in rows:
        key = (row.agent, row.session_id)
        item = by_session[key]
        item["calls"] += 1
        item["total_tokens"] += row.total_tokens
        item["cost_total_usd"] += row.cost_total_usd
        item["models"].add(f"{row.provider}/{row.model}")
        item["first_timestamp"] = item["first_timestamp"] or row.timestamp
        item["last_timestamp"] = row.timestamp

    all_keys = set(by_session) | set(session_meta)
    sessions_out = []
    for key in sorted(
        all_keys,
        key=lambda k: (
            by_session.get(k, {}).get("cost_total_usd", 0.0),
            by_session.get(k, {}).get("last_timestamp")
            or (session_meta.get(k).updated_at if session_meta.get(k) else "")
            or (session_meta.get(k).started_at if session_meta.get(k) else ""),
        ),
        reverse=True,
    ):
        item = by_session.get(key) or {
            "calls": 0,
            "total_tokens": 0,
            "cost_total_usd": 0.0,
            "models": set(),
            "first_timestamp": None,
            "last_timestamp": None,
        }
        meta = session_meta.get(key) or SessionMeta(agent=key[0], session_id=key[1])
        sessions_out.append(
            {
                "agent": key[0],
                "session_id": key[1],
                "session_key": meta.session_key,
                "label": meta.label or meta.display_name,
                "channel": meta.channel,
                "spawn_depth": meta.spawn_depth,
                "subagent_role": meta.subagent_role,
                "parent_session_key": meta.spawned_by,
                "parent_session_id": meta.spawned_by_session_id,
                "calls": item["calls"],
                "total_tokens": item["total_tokens"],
                "cost_total_usd": round(item["cost_total_usd"], 6),
                "models": sorted(item["models"]),
                "started_at": meta.started_at or item["first_timestamp"],
                "last_timestamp": item["last_timestamp"] or meta.updated_at or meta.started_at,
                "status": meta.status,
            }
        )
    return {"rows": len(rows), "sessions": sessions_out}


def summarise_subagents(rows: list[UsageRow], session_meta: dict[tuple[str, str], SessionMeta]) -> dict[str, Any]:
    session_summary = summarise_by_session(rows, session_meta)["sessions"]
    subagents = [item for item in session_summary if item.get("spawn_depth") is not None or item.get("parent_session_id") or item.get("parent_session_key")]
    return {"rows": len(rows), "subagents": subagents}


def summarise_session_tree(rows: list[UsageRow], session_meta: dict[tuple[str, str], SessionMeta]) -> dict[str, Any]:
    sessions = summarise_by_session(rows, session_meta)["sessions"]
    nodes = {item["session_id"]: {**item, "children": []} for item in sessions}
    roots: list[dict[str, Any]] = []
    for item in nodes.values():
        parent_id = item.get("parent_session_id")
        if parent_id and parent_id in nodes:
            nodes[parent_id]["children"].append(item)
        else:
            roots.append(item)

    def rollup(node: dict[str, Any]) -> tuple[int, float, int]:
        total_tokens = int(node.get("total_tokens") or 0)
        total_cost = float(node.get("cost_total_usd") or 0.0)
        total_calls = int(node.get("calls") or 0)
        for child in node["children"]:
            child_tokens, child_cost, child_calls = rollup(child)
            total_tokens += child_tokens
            total_cost += child_cost
            total_calls += child_calls
        node["tree_total_tokens"] = total_tokens
        node["tree_cost_total_usd"] = round(total_cost, 6)
        node["tree_calls"] = total_calls
        node["children"].sort(key=lambda item: (item.get("tree_cost_total_usd") or 0.0, item.get("last_timestamp") or ""), reverse=True)
        return total_tokens, total_cost, total_calls

    for root in roots:
        rollup(root)
    roots.sort(key=lambda item: (item.get("tree_cost_total_usd") or 0.0, item.get("last_timestamp") or ""), reverse=True)
    return {"rows": len(rows), "trees": roots}


def compute_totals(rows: list[UsageRow]) -> Totals:
    return Totals(
        calls=len(rows),
        total_tokens=sum(row.total_tokens for row in rows),
        cost_total_usd=round(sum(row.cost_total_usd for row in rows), 6),
        agents=len({row.agent for row in rows}),
        sessions=len({row.session_id for row in rows}),
        models=len({(row.provider, row.model) for row in rows}),
        first_timestamp=rows[0].timestamp if rows else None,
        last_timestamp=rows[-1].timestamp if rows else None,
    )


def build_overview(rows: list[UsageRow], session_meta: dict[tuple[str, str], SessionMeta], limit: int) -> dict[str, Any]:
    totals = compute_totals(rows)
    by_model = summarise_by_model(rows)
    by_agent = summarise_by_agent(rows)
    by_session = summarise_by_session(rows, session_meta)
    current = asdict(rows[-1]) if rows else None
    return {
        "rows": len(rows),
        "totals": asdict(totals),
        "current": current,
        "top_models": by_model["models"][:limit],
        "top_agents": by_agent["agents"][:limit],
        "top_sessions": by_session["sessions"][:limit],
    }


def build_dashboard_payload(rows: list[UsageRow], session_meta: dict[tuple[str, str], SessionMeta], limit: int) -> dict[str, Any]:
    return {
        "overview": build_overview(rows, session_meta, limit),
        "daily": summarise_daily(rows)["daily"],
        "recent": [asdict(row) for row in rows[-limit:][::-1]],
    }


def fmt_money(value: float) -> str:
    return f"${value:,.4f}"


def fmt_tokens(value: int) -> str:
    return f"{value:,} tok"


def fmt_number(value: int | float) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.2f}"
    return f"{int(value):,}"


def fmt_timestamp(value: str | None) -> str:
    if not value:
        return "—"
    return value.replace("T", " ").replace("Z", " UTC")


def compact_model_name(provider: str, model: str) -> str:
    return f"{provider}/{model}"


def compact_session_name(item: dict[str, Any]) -> str:
    primary, secondary = session_display_parts(item)
    return primary if not secondary else f"{primary} | {secondary}"


def is_probably_uuidish(value: str | None) -> bool:
    return bool(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{8}-[0-9a-f-]{27,36}", value, flags=re.IGNORECASE))


def humanize_channel(value: str | None) -> str | None:
    if not value:
        return None
    mapping = {"discord": "Discord", "telegram": "Telegram", "whatsapp": "WhatsApp", "signal": "Signal", "slack": "Slack"}
    return mapping.get(value.lower(), value.replace('-', ' ').title())


def normalize_session_label(label: str | None, channel: str | None = None) -> tuple[str | None, str | None]:
    if not isinstance(label, str) or not label.strip():
        return None, None
    label = label.strip()
    route_match = re.fullmatch(r"([a-z]+):([^#]*)#(.+)", label)
    if route_match:
        route_channel, _, tail = route_match.groups()
        channel_name = humanize_channel(route_channel) or route_channel.title()
        return f"{channel_name} · {tail}", label
    if is_probably_uuidish(label):
        return None, label
    return label, None


def session_display_parts(item: dict[str, Any]) -> tuple[str, str | None]:
    label, original_label = normalize_session_label(item.get("session_label") or item.get("label") or item.get("display_name"), item.get("channel"))
    if label:
        secondary_bits = []
        if item.get("channel"):
            secondary_bits.append(humanize_channel(item.get("channel")) or str(item.get("channel")))
        if item.get("spawn_depth") is not None:
            secondary_bits.append(f"depth {item['spawn_depth']}")
        elif item.get("parent_session_id"):
            secondary_bits.append("subagent")
        if item.get("status"):
            secondary_bits.append(str(item["status"]))
        secondary = " • ".join(bit for bit in secondary_bits if bit)
        if not secondary and original_label and original_label != label:
            secondary = original_label
        return label, secondary or None

    channel_name = humanize_channel(item.get("channel"))
    if item.get("spawn_depth") is not None or item.get("parent_session_id"):
        depth = item.get("spawn_depth")
        role = item.get("subagent_role")
        primary = f"Subagent depth {depth}" if depth is not None else "Subagent session"
        secondary_bits = [channel_name, role, f"agent {item['agent']}" if item.get('agent') else None]
        return primary, " • ".join(bit for bit in secondary_bits if bit) or None

    if channel_name:
        primary = f"{channel_name} session"
        secondary_bits = [f"agent {item['agent']}" if item.get('agent') else None, item.get('status')]
        if item.get("session_id") and not is_probably_uuidish(str(item["session_id"])):
            secondary_bits.append(str(item["session_id"]))
        return primary, " • ".join(bit for bit in secondary_bits if bit) or None

    if item.get("agent") == "main":
        return "Main session", str(item.get("status")) if item.get("status") else None
    if item.get("agent"):
        return f"{item['agent']} session", str(item.get("status")) if item.get("status") else None
    session_id = str(item.get("session_id") or "session")
    if is_probably_uuidish(session_id):
        return f"Session {session_id[:8]}", session_id
    return session_id, None


def render_session_cell(item: dict[str, Any]) -> str:
    primary, secondary = session_display_parts(item)
    detail = secondary or (str(item.get("session_id")) if item.get("session_id") and primary != item.get("session_id") else None)
    safe_primary = html.escape(primary)
    safe_detail = html.escape(detail) if detail else ""
    detail_html = f'<span class="table-subline">{safe_detail}</span>' if detail else ''
    return f'<div class="table-primary-cell"><strong>{safe_primary}</strong>{detail_html}</div>'


def render_ranked(items: list[tuple[str, str]], empty: str = "(none)") -> str:
    if not items:
        return empty
    return "\n".join(f"{idx}. {left} — {right}" for idx, (left, right) in enumerate(items, 1))


def render_text_summary(data: dict[str, Any], limit: int) -> str:
    totals = data["totals"]
    header = f"Usage overview — {fmt_money(totals['cost_total_usd'])}, {fmt_tokens(totals['total_tokens'])}, {totals['calls']} calls"
    scope = f"Agents {totals['agents']} | Sessions {totals['sessions']} | Models {totals['models']}"
    lines = [header, scope]
    current = data.get("current")
    if current:
        label = f" | {current['session_label']}" if current.get("session_label") else ""
        lines.append(f"Current: {compact_model_name(current['provider'], current['model'])} | {current['agent']} | {current['session_id']}{label}")

    lines.append("")
    lines.append("Top agents")
    lines.append(
        render_ranked(
            [
                (item["agent"], f"{fmt_money(item['cost_total_usd'])}, {fmt_tokens(item['total_tokens'])}, {item['sessions']} sessions")
                for item in data["top_agents"][:limit]
            ]
        )
    )
    lines.append("")
    lines.append("Top sessions")
    lines.append(
        render_ranked(
            [
                (compact_session_name(item), f"{fmt_money(item['cost_total_usd'])}, {fmt_tokens(item['total_tokens'])}, {item['calls']} calls")
                for item in data["top_sessions"][:limit]
            ]
        )
    )
    lines.append("")
    lines.append("Top models")
    lines.append(
        render_ranked(
            [
                (compact_model_name(item["provider"], item["model"]), f"{fmt_money(item['cost_total_usd'])}, {fmt_tokens(item['total_tokens'])}, {item['calls']} calls")
                for item in data["top_models"][:limit]
            ]
        )
    )
    return "\n".join(lines)


def render_text_agents(data: dict[str, Any], limit: int) -> str:
    totals = compute_totals_from_collection(data["agents"], key_name="agent")
    lines = [f"Top agents — {len(data['agents'])} total"]
    if totals:
        lines.append(f"Shown by cost. Combined: {fmt_money(totals['cost_total_usd'])}, {fmt_tokens(totals['total_tokens'])}, {totals['sessions']} sessions")
    lines.append(
        render_ranked(
            [
                (item["agent"], f"{fmt_money(item['cost_total_usd'])}, {fmt_tokens(item['total_tokens'])}, {item['calls']} calls, {item['sessions']} sessions")
                for item in data["agents"][:limit]
            ]
        )
    )
    return "\n".join(lines)


def render_text_daily(data: dict[str, Any], limit: int) -> str:
    lines = [f"Daily usage — showing {min(limit, len(data['daily']))} of {len(data['daily'])}"]
    lines.append(
        render_ranked(
            [
                (f"{item['date']} | {compact_model_name(item['provider'], item['model'])}", f"{fmt_money(item['cost_total_usd'])}, {fmt_tokens(item['total_tokens'])}, {item['calls']} calls")
                for item in data["daily"][:limit]
            ]
        )
    )
    return "\n".join(lines)


def render_text_current(rows: list[UsageRow]) -> str:
    if not rows:
        return "No usage rows found."
    row = rows[-1]
    parts = [
        f"Current model: {compact_model_name(row.provider, row.model)}",
        f"Agent: {row.agent}",
        f"Session: {row.session_id}",
    ]
    if row.session_label:
        parts.append(f"Label: {row.session_label}")
    if row.parent_session_id:
        parts.append(f"Parent session: {row.parent_session_id}")
    parts.extend([f"Timestamp: {row.timestamp}", f"Tokens: {fmt_tokens(row.total_tokens)}", f"Cost: {fmt_money(row.cost_total_usd)}"])
    return "\n".join(parts)


def render_text_recent(rows: list[UsageRow], limit: int) -> str:
    if not rows:
        return "No usage rows found."
    return render_ranked(
        [
            (
                f"{row.timestamp} | {row.agent} | {row.session_id}" + (f" | {row.session_label}" if row.session_label else ""),
                f"{compact_model_name(row.provider, row.model)}, {fmt_tokens(row.total_tokens)}, {fmt_money(row.cost_total_usd)}",
            )
            for row in rows[-limit:][::-1]
        ]
    )


def render_text_sessions(data: dict[str, Any], limit: int, key: str = "sessions", title: str | None = None) -> str:
    items = data[key][:limit]
    heading = title or ("Top subagents" if key == "subagents" else "Top sessions")
    lines = [f"{heading} — showing {len(items)} of {len(data[key])}"]
    lines.append(
        render_ranked(
            [
                (
                    f"{item['agent']} | {compact_session_name(item)}",
                    f"{fmt_money(item['cost_total_usd'])}, {fmt_tokens(item['total_tokens'])}, {item['calls']} calls",
                )
                for item in items
            ]
        )
    )
    return "\n".join(lines)


def render_tree_node(node: dict[str, Any], depth: int = 0) -> list[str]:
    indent = "  " * depth
    label = f" [{node['label']}]" if node.get("label") else ""
    line = (
        f"{indent}- {node['agent']} | {node['session_id']}{label} | "
        f"direct {fmt_money(node['cost_total_usd'])}/{fmt_tokens(node['total_tokens'])} | "
        f"tree {fmt_money(node['tree_cost_total_usd'])}/{fmt_tokens(node['tree_total_tokens'])}"
    )
    lines = [line]
    for child in node["children"]:
        lines.extend(render_tree_node(child, depth + 1))
    return lines


def render_text_session_tree(data: dict[str, Any], limit: int) -> str:
    lines = [f"Session trees — showing {min(limit, len(data['trees']))} of {len(data['trees'])}"]
    for root in data["trees"][:limit]:
        lines.extend(render_tree_node(root))
    return "\n".join(lines)


def compute_totals_from_collection(items: list[dict[str, Any]], key_name: str) -> dict[str, Any] | None:
    if not items:
        return None
    return {
        key_name + "s": len(items),
        "cost_total_usd": round(sum(float(item.get("cost_total_usd") or 0.0) for item in items), 6),
        "total_tokens": sum(int(item.get("total_tokens") or 0) for item in items),
        "sessions": sum(int(item.get("sessions") or 0) for item in items),
    }


def render_trend_chart(points: list[tuple[str, dict[str, float | int]]]) -> str:
    if not points:
        return '<div class="empty-state">No recent trend data.</div>'
    costs = [float(vals["cost_total_usd"]) for _, vals in points]
    max_cost = max(costs) or 1.0
    rows = []
    for day, vals in reversed(points):
        cost = float(vals["cost_total_usd"])
        width = max(8.0, (cost / max_cost) * 100) if cost > 0 else 0.0
        rows.append(
            ''.join([
                '<div class="trend-row">',
                f'<div class="trend-row-head"><strong>{html.escape(day)}</strong><span>{html.escape(fmt_money(cost))}</span></div>',
                '<div class="trend-bar-track" aria-hidden="true">',
                f'<div class="trend-bar-fill" style="width:{width:.1f}%"></div>',
                '</div>',
                f'<div class="trend-row-meta"><span>{html.escape(fmt_number(int(vals["calls"])))} calls</span><span>{html.escape(fmt_number(int(vals["total_tokens"])))} tok</span></div>',
                '</div>',
            ])
        )
    return '<div class="trend-list" role="img" aria-label="Daily cost bars for the last seven days">' + ''.join(rows) + '</div>'


def render_dashboard_table(headers: list[str], rows: list[list[str]], empty: str = "No data.") -> str:
    if not rows:
        return f'<div class="empty-state">{html.escape(empty)}</div>'
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body_rows = ["<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows]
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'


def render_dashboard_html(data: dict[str, Any], title: str, limit: int) -> str:
    overview = data["overview"]
    totals = overview["totals"]
    current = overview.get("current")
    top_agents = overview["top_agents"][:limit]
    top_sessions = overview["top_sessions"][:limit]
    top_models = overview["top_models"][:limit]
    recent = data["recent"][:limit]

    day_totals: dict[str, dict[str, float | int]] = {}
    for item in data["daily"]:
        entry = day_totals.setdefault(item["date"], {"cost_total_usd": 0.0, "total_tokens": 0, "calls": 0})
        entry["cost_total_usd"] = float(entry["cost_total_usd"]) + float(item.get("cost_total_usd") or 0.0)
        entry["total_tokens"] = int(entry["total_tokens"]) + int(item.get("total_tokens") or 0)
        entry["calls"] = int(entry["calls"]) + int(item.get("calls") or 0)
    recent_days = sorted(day_totals.items())[-7:]

    cards = [
        ("Total cost", fmt_money(float(totals["cost_total_usd"])), f"{totals['calls']} calls"),
        ("Total tokens", fmt_number(int(totals["total_tokens"])), f"Across {totals['models']} models"),
        ("Sessions", fmt_number(int(totals["sessions"])), f"{totals['agents']} agents"),
        ("Window", fmt_timestamp(totals.get("first_timestamp")), f"to {fmt_timestamp(totals.get('last_timestamp'))}"),
    ]
    cards_html = "".join(
        f'<article class="stat-card"><span class="eyebrow">{html.escape(label)}</span><strong>{html.escape(value)}</strong><span class="muted">{html.escape(sub)}</span></article>'
        for label, value, sub in cards
    )

    current_html = '<div class="empty-state">No current usage row found.</div>'
    if current:
        current_html = "".join(
            [
                '<div class="current-grid">',
                f'<div><span class="eyebrow">Current model</span><strong>{html.escape(compact_model_name(current["provider"], current["model"]))}</strong></div>',
                f'<div><span class="eyebrow">Agent</span><strong>{html.escape(current["agent"])}</strong></div>',
                f'<div><span class="eyebrow">Session</span>{render_session_cell(current)}</div>',
                f'<div><span class="eyebrow">Last activity</span><strong>{html.escape(fmt_timestamp(current["timestamp"]))}</strong></div>',
                '</div>',
            ]
        )

    agents_table = render_dashboard_table(
        ["Agent", "Cost", "Tokens", "Calls", "Sessions", "Last activity"],
        [
            [
                html.escape(item["agent"]),
                fmt_money(item["cost_total_usd"]),
                fmt_number(item["total_tokens"]),
                fmt_number(item["calls"]),
                fmt_number(item["sessions"]),
                html.escape(fmt_timestamp(item.get("last_timestamp"))),
            ]
            for item in top_agents
        ],
        empty="No agent data.",
    )
    sessions_table = render_dashboard_table(
        ["Session", "Agent", "Cost", "Tokens", "Calls", "Status"],
        [
            [
                render_session_cell(item),
                html.escape(item["agent"]),
                fmt_money(item["cost_total_usd"]),
                fmt_number(item["total_tokens"]),
                fmt_number(item["calls"]),
                html.escape(item.get("status") or "—"),
            ]
            for item in top_sessions
        ],
        empty="No session data.",
    )
    models_table = render_dashboard_table(
        ["Model", "Cost", "Tokens", "Calls", "Agents", "Sessions"],
        [
            [
                html.escape(compact_model_name(item["provider"], item["model"])),
                fmt_money(item["cost_total_usd"]),
                fmt_number(item["total_tokens"]),
                fmt_number(item["calls"]),
                fmt_number(len(item.get("agents") or [])),
                fmt_number(item["sessions"]),
            ]
            for item in top_models
        ],
        empty="No model data.",
    )
    recent_table = render_dashboard_table(
        ["When", "Agent", "Session", "Model", "Tokens", "Cost"],
        [
            [
                html.escape(fmt_timestamp(item["timestamp"])),
                html.escape(item["agent"]),
                render_session_cell(item),
                html.escape(compact_model_name(item["provider"], item["model"])),
                fmt_number(item["total_tokens"]),
                fmt_money(item["cost_total_usd"]),
            ]
            for item in recent
        ],
        empty="No recent activity.",
    )

    trend_summary = ''
    if recent_days:
        trend_costs = [float(vals["cost_total_usd"]) for _, vals in recent_days]
        trend_calls = [int(vals["calls"]) for _, vals in recent_days]
        trend_tokens = [int(vals["total_tokens"]) for _, vals in recent_days]
        trend_summary = ''.join([
            '<div class="trend-summary">',
            f'<span class="trend-pill"><strong>{html.escape(fmt_money(sum(trend_costs)))}</strong><span>7-day spend</span></span>',
            f'<span class="trend-pill"><strong>{html.escape(fmt_money(max(trend_costs)))}</strong><span>Peak day</span></span>',
            f'<span class="trend-pill"><strong>{html.escape(fmt_money(statistics.mean(trend_costs)))}</strong><span>Avg / day</span></span>',
            f'<span class="trend-pill"><strong>{html.escape(fmt_number(sum(trend_calls)))}</strong><span>Total calls</span></span>',
            f'<span class="trend-pill"><strong>{html.escape(fmt_number(sum(trend_tokens)))}</strong><span>Total tokens</span></span>',
            '</div>',
        ])
    spark = render_trend_chart(recent_days)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ color-scheme: dark; --bg:#07111f; --panel:#0f1b2d; --text:#ecf3ff; --muted:#9bb0cb; --accent:#6ee7b7; --border:rgba(255,255,255,.08); }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif; background: radial-gradient(circle at top, #15314f 0%, var(--bg) 38%, #030712 100%); color:var(--text); }}
    .page {{ max-width:1180px; margin:0 auto; padding:24px 16px 48px; }}
    .hero {{ display:grid; gap:16px; grid-template-columns:1.5fr 1fr; margin-bottom:18px; }}
    .panel {{ background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02)); border:1px solid var(--border); border-radius:20px; padding:18px; box-shadow:0 12px 40px rgba(0,0,0,.25); }}
    h1,h2,p {{ margin:0; }}
    .hero h1 {{ font-size:clamp(1.8rem, 4vw, 3rem); line-height:1.05; margin-bottom:10px; }}
    .eyebrow {{ display:block; text-transform:uppercase; letter-spacing:.12em; color:var(--accent); font-size:.72rem; margin-bottom:8px; }}
    .muted {{ color:var(--muted); }}
    .meta {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:10px; color:var(--muted); font-size:.95rem; }}
    .stats {{ display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:14px; margin-bottom:18px; }}
    .stat-card strong {{ display:block; font-size:clamp(1.3rem, 3vw, 2rem); margin-bottom:8px; }}
    .section-grid {{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:14px; margin-bottom:14px; }}
    .table-wrap {{ overflow:auto; margin-top:12px; }}
    .table-primary-cell strong {{ display:block; font-size:.96rem; line-height:1.3; }}
    .table-subline {{ display:block; margin-top:4px; color:var(--muted); font-size:.78rem; word-break:break-word; }}
    table {{ width:100%; border-collapse:collapse; min-width:520px; }}
    th, td {{ text-align:left; padding:10px 12px; border-bottom:1px solid var(--border); font-size:.94rem; }}
    th {{ color:var(--muted); font-weight:600; background:rgba(15,27,45,.96); }}
    .current-grid {{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:12px; margin-top:12px; }}
    .trend-box {{ display:grid; gap:12px; }}
    .trend-summary {{ display:flex; flex-wrap:wrap; gap:10px; }}
    .trend-pill {{ display:inline-flex; flex-direction:column; gap:3px; padding:10px 12px; border-radius:999px; background:rgba(255,255,255,.04); border:1px solid var(--border); min-width:110px; }}
    .trend-pill strong {{ font-size:1rem; }}
    .trend-pill span {{ color:var(--muted); font-size:.78rem; }}
    .trend-chart {{ padding:12px; border-radius:16px; background:linear-gradient(180deg, rgba(110,231,183,.06), rgba(255,255,255,.02)); border:1px solid var(--border); }}
    .trend-list {{ display:grid; gap:12px; }}
    .trend-row {{ display:grid; gap:7px; }}
    .trend-row-head, .trend-row-meta {{ display:flex; align-items:center; justify-content:space-between; gap:10px; }}
    .trend-row-head strong {{ font-size:.95rem; }}
    .trend-row-head span {{ font-weight:600; }}
    .trend-row-meta {{ color:var(--muted); font-size:.82rem; }}
    .trend-bar-track {{ height:10px; border-radius:999px; background:rgba(255,255,255,.06); overflow:hidden; }}
    .trend-bar-fill {{ height:100%; border-radius:999px; background:linear-gradient(90deg, rgba(110,231,183,.72), rgba(110,231,183,1)); box-shadow:0 0 0 1px rgba(255,255,255,.08) inset; min-width:8px; }}
    .empty-state {{ padding:18px; border:1px dashed var(--border); border-radius:14px; color:var(--muted); text-align:center; margin-top:10px; }}
    .footer {{ margin-top:18px; color:var(--muted); font-size:.85rem; }}
    @media (max-width: 820px) {{ .hero, .section-grid, .stats, .current-grid {{ grid-template-columns:1fr; }} .page {{ padding:16px 12px 36px; }} .panel {{ border-radius:16px; }} table {{ min-width:460px; }} .trend-summary {{ gap:8px; }} .trend-pill {{ min-width:calc(50% - 4px); }} .trend-chart {{ padding:10px; }} .trend-row-head strong, .trend-row-head span {{ font-size:.92rem; }} .trend-row-meta {{ font-size:.78rem; }} }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <article class="panel">
        <span class="eyebrow">OpenClaw model usage</span>
        <h1>{html.escape(title)}</h1>
        <p class="muted">Local-first static dashboard generated from session logs. No server. No browser drama. Just a portable report.</p>
        <div class="meta">
          <span>{fmt_number(totals['calls'])} calls</span>
          <span>{fmt_number(totals['sessions'])} sessions</span>
          <span>{fmt_number(totals['agents'])} agents</span>
          <span>{fmt_number(totals['models'])} models</span>
        </div>
      </article>
      <article class="panel">
        <span class="eyebrow">Current context</span>
        <h2>Latest activity</h2>
        {current_html}
      </article>
    </section>
    <section class="stats">{cards_html}</section>
    <section class="section-grid">
      <article class="panel"><span class="eyebrow">Top agents</span><h2>Who is spending the budget</h2>{agents_table}</article>
      <article class="panel"><span class="eyebrow">Top models</span><h2>Which models are doing the work</h2>{models_table}</article>
    </section>
    <section class="section-grid">
      <article class="panel"><span class="eyebrow">Top sessions</span><h2>Most expensive sessions</h2>{sessions_table}</article>
      <article class="panel"><span class="eyebrow">Daily trend</span><h2>Recent cost pulse</h2><div class="trend-box">{trend_summary}<div class="trend-chart">{spark}</div></div></article>
    </section>
    <section class="panel"><span class="eyebrow">Recent activity</span><h2>Latest assistant usage rows</h2>{recent_table}</section>
    <p class="footer">Generated locally by openclaw-model-usage. Self-contained HTML output for easy sharing or opening on your phone.</p>
  </main>
</body>
</html>'''


def main() -> int:
    args = build_parser().parse_args()
    rows, session_meta = load_rows(
        root=Path(args.root).expanduser(),
        agents=set(args.agent) if args.agent else None,
        providers=set(args.provider) if args.provider else None,
        models=set(args.model) if args.model else None,
        session_ids=set(args.session_id) if args.session_id else None,
        channels=set(args.channel) if args.channel else None,
        since_days=args.since_days,
    )

    command = args.command
    if command in {"overview", "summary"}:
        payload: Any = build_overview(rows, session_meta, args.limit)
    elif command in {"agents", "top-agents"}:
        payload = summarise_by_agent(rows)
    elif command == "daily":
        payload = summarise_daily(rows)
    elif command in {"sessions", "top-sessions"}:
        payload = summarise_by_session(rows, session_meta)
    elif command == "subagents":
        payload = summarise_subagents(rows, session_meta)
    elif command == "session-tree":
        payload = summarise_session_tree(rows, session_meta)
    elif command == "current":
        payload = asdict(rows[-1]) if rows else None
    elif command == "recent":
        payload = [asdict(r) for r in rows[-args.limit:][::-1]]
    elif command == "rows":
        payload = [asdict(r) for r in rows[-args.limit:]]
    elif command == "dashboard":
        payload = build_dashboard_payload(rows, session_meta, args.limit)
    else:
        raise AssertionError("unexpected command")

    if command == "dashboard":
        output_path = Path(args.out).expanduser() if args.out else Path("dist") / "dashboard.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_dashboard_html(payload, args.title, args.limit), encoding="utf-8")
        if args.json:
            print(json.dumps({"output": str(output_path.resolve()), "title": args.title, "rows": payload["overview"]["rows"]}, indent=2 if args.pretty else None))
        else:
            print(f"Wrote dashboard HTML to {output_path.resolve()}")
        return 0

    if args.json:
        print(json.dumps(payload, indent=2 if args.pretty else None))
        return 0

    if command in {"overview", "summary"}:
        print(render_text_summary(payload, args.limit))
    elif command in {"agents", "top-agents"}:
        print(render_text_agents(payload, args.limit))
    elif command == "daily":
        print(render_text_daily(payload, args.limit))
    elif command in {"sessions", "top-sessions"}:
        print(render_text_sessions(payload, args.limit))
    elif command == "subagents":
        print(render_text_sessions(payload, args.limit, key="subagents", title="Top subagents"))
    elif command == "session-tree":
        print(render_text_session_tree(payload, args.limit))
    elif command == "current":
        print(render_text_current(rows))
    else:
        print(render_text_recent(rows, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
