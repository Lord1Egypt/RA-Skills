#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sqlite3
import sys
import textwrap
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Iterable

API_URL = "https://openrouter.ai/api/v1/models"
DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "model-watcher.db"
SOURCE = "openrouter"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def epoch_to_iso(value: Any) -> str | None:
    if value in (None, "", 0):
        return None
    try:
        return dt.datetime.fromtimestamp(int(value), tz=dt.timezone.utc).replace(microsecond=0).isoformat()
    except Exception:
        return None


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def short_iso(iso_ts: str | None) -> str:
    if not iso_ts:
        return "-"
    return iso_ts.replace("T", " ").replace("+00:00", " UTC")


def get_provider(model_id: str) -> str | None:
    if "/" in model_id:
        return model_id.split("/", 1)[0]
    return None


def normalize_model(raw: dict[str, Any]) -> dict[str, Any]:
    model_id = raw["id"]
    arch = raw.get("architecture") or {}
    normalized = {
        "source": SOURCE,
        "model_id": model_id,
        "canonical_slug": raw.get("canonical_slug"),
        "name": raw.get("name") or model_id,
        "provider": get_provider(model_id),
        "description": raw.get("description"),
        "created_at": epoch_to_iso(raw.get("created")),
        "context_length": raw.get("context_length"),
        "modality": arch.get("modality"),
        "input_modalities_json": dump_json(arch.get("input_modalities") or []),
        "output_modalities_json": dump_json(arch.get("output_modalities") or []),
        "pricing_json": dump_json(raw.get("pricing") or {}),
        "top_provider_json": dump_json(raw.get("top_provider") or {}),
        "raw_json": dump_json(raw),
    }
    hash_payload = {
        k: normalized[k]
        for k in [
            "canonical_slug",
            "name",
            "description",
            "created_at",
            "context_length",
            "modality",
            "input_modalities_json",
            "output_modalities_json",
            "pricing_json",
            "top_provider_json",
        ]
    }
    normalized["content_hash"] = hashlib.sha256(dump_json(hash_payload).encode("utf-8")).hexdigest()
    return normalized


def fetch_models() -> list[dict[str, Any]]:
    req = urllib.request.Request(API_URL, headers={"User-Agent": "OpenClaw-ModelWatcher/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.load(response)
    items = payload.get("data")
    if not isinstance(items, list):
        raise RuntimeError("Unexpected API payload: missing data[]")
    return [normalize_model(item) for item in items if isinstance(item, dict) and item.get("id")]


def ensure_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS models (
          source TEXT NOT NULL,
          model_id TEXT NOT NULL,
          canonical_slug TEXT,
          name TEXT,
          provider TEXT,
          description TEXT,
          created_at TEXT,
          first_seen_at TEXT,
          last_seen_at TEXT,
          last_changed_at TEXT,
          is_active INTEGER NOT NULL DEFAULT 1,
          context_length INTEGER,
          modality TEXT,
          input_modalities_json TEXT,
          output_modalities_json TEXT,
          pricing_json TEXT,
          top_provider_json TEXT,
          raw_json TEXT,
          content_hash TEXT,
          PRIMARY KEY (source, model_id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
          run_id TEXT PRIMARY KEY,
          source TEXT NOT NULL,
          started_at TEXT NOT NULL,
          finished_at TEXT,
          status TEXT NOT NULL,
          models_total INTEGER,
          new_count INTEGER,
          updated_count INTEGER,
          missing_count INTEGER,
          error_message TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          run_id TEXT NOT NULL,
          source TEXT NOT NULL,
          model_id TEXT NOT NULL,
          event_type TEXT NOT NULL,
          event_at TEXT NOT NULL,
          summary_json TEXT
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_type_time ON events(event_type, event_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_model_time ON events(model_id, event_at)")
    conn.commit()


def open_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    ensure_db(conn)
    return conn


def existing_models(conn: sqlite3.Connection) -> dict[str, sqlite3.Row]:
    rows = conn.execute("SELECT * FROM models WHERE source = ?", (SOURCE,)).fetchall()
    return {row["model_id"]: row for row in rows}


def event_summary(model: dict[str, Any]) -> str:
    summary = {
        "name": model.get("name"),
        "provider": model.get("provider"),
        "context_length": model.get("context_length"),
        "created_at": model.get("created_at"),
        "canonical_slug": model.get("canonical_slug"),
    }
    return dump_json(summary)


def upsert_model(conn: sqlite3.Connection, model: dict[str, Any], first_seen_at: str, last_changed_at: str) -> None:
    conn.execute(
        """
        INSERT INTO models (
          source, model_id, canonical_slug, name, provider, description, created_at,
          first_seen_at, last_seen_at, last_changed_at, is_active, context_length,
          modality, input_modalities_json, output_modalities_json, pricing_json,
          top_provider_json, raw_json, content_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source, model_id) DO UPDATE SET
          canonical_slug=excluded.canonical_slug,
          name=excluded.name,
          provider=excluded.provider,
          description=excluded.description,
          created_at=excluded.created_at,
          last_seen_at=excluded.last_seen_at,
          last_changed_at=excluded.last_changed_at,
          is_active=1,
          context_length=excluded.context_length,
          modality=excluded.modality,
          input_modalities_json=excluded.input_modalities_json,
          output_modalities_json=excluded.output_modalities_json,
          pricing_json=excluded.pricing_json,
          top_provider_json=excluded.top_provider_json,
          raw_json=excluded.raw_json,
          content_hash=excluded.content_hash
        """,
        (
            model["source"],
            model["model_id"],
            model["canonical_slug"],
            model["name"],
            model["provider"],
            model["description"],
            model["created_at"],
            first_seen_at,
            first_seen_at,
            last_changed_at,
            model["context_length"],
            model["modality"],
            model["input_modalities_json"],
            model["output_modalities_json"],
            model["pricing_json"],
            model["top_provider_json"],
            model["raw_json"],
            model["content_hash"],
        ),
    )


def trim_decimal(value: float) -> str:
    text = f"{value:.2f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def format_unit_price(value: Any) -> str:
    try:
        price = float(value)
    except (TypeError, ValueError):
        return "-"
    if price <= 0:
        return "$0"
    per_m = price * 1_000_000
    per_k = price * 1_000
    if per_m >= 1000:
        return f"${trim_decimal(per_k)}/K"
    return f"${trim_decimal(per_m)}/M"


def format_price_line(pricing_json: str) -> str:
    try:
        pricing = json.loads(pricing_json or "{}")
    except Exception:
        pricing = {}
    prompt = pricing.get("prompt")
    completion = pricing.get("completion")
    extras = [k for k in pricing.keys() if k not in {"prompt", "completion"}]
    parts = []
    if prompt is not None:
        parts.append(f"in {format_unit_price(prompt)}")
    if completion is not None:
        parts.append(f"out {format_unit_price(completion)}")
    if extras:
        parts.append(f"extras {len(extras)}")
    return ", ".join(parts) if parts else "-"


def print_model_lines(rows: Iterable[sqlite3.Row], limit: int | None = None) -> None:
    count = 0
    for row in rows:
        if limit is not None and count >= limit:
            break
        print(f"- {row['model_id']} — {row['name']}")
        print(f"  first seen: {short_iso(row['first_seen_at'])}")
        print(f"  provider: {row['provider'] or '-'} | context: {row['context_length'] or '-'} | modality: {row['modality'] or '-'}")
        print(f"  pricing: {format_price_line(row['pricing_json'])}")
        count += 1
    if count == 0:
        print("- none")


def command_scan(args: argparse.Namespace) -> int:
    db = Path(args.db)
    conn = open_db(db)
    started_at = utc_now()
    run_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO runs(run_id, source, started_at, status) VALUES (?, ?, ?, ?)",
        (run_id, SOURCE, started_at, "running"),
    )
    conn.commit()
    try:
        models = fetch_models()
        now = utc_now()
        existing = existing_models(conn)
        seen_ids = set()
        new_count = updated_count = 0

        for model in models:
            model_id = model["model_id"]
            seen_ids.add(model_id)
            current = existing.get(model_id)
            if current is None:
                upsert_model(conn, model, first_seen_at=now, last_changed_at=now)
                conn.execute(
                    "INSERT INTO events(run_id, source, model_id, event_type, event_at, summary_json) VALUES (?, ?, ?, 'new', ?, ?)",
                    (run_id, SOURCE, model_id, now, event_summary(model)),
                )
                new_count += 1
            else:
                changed = current["content_hash"] != model["content_hash"]
                upsert_model(
                    conn,
                    model,
                    first_seen_at=current["first_seen_at"],
                    last_changed_at=now if changed else current["last_changed_at"],
                )
                conn.execute(
                    "UPDATE models SET last_seen_at = ?, is_active = 1 WHERE source = ? AND model_id = ?",
                    (now, SOURCE, model_id),
                )
                if changed:
                    conn.execute(
                        "INSERT INTO events(run_id, source, model_id, event_type, event_at, summary_json) VALUES (?, ?, ?, 'updated', ?, ?)",
                        (run_id, SOURCE, model_id, now, event_summary(model)),
                    )
                    updated_count += 1

        missing_count = 0
        for model_id, current in existing.items():
            if model_id not in seen_ids and current["is_active"]:
                conn.execute(
                    "UPDATE models SET is_active = 0 WHERE source = ? AND model_id = ?",
                    (SOURCE, model_id),
                )
                conn.execute(
                    "INSERT INTO events(run_id, source, model_id, event_type, event_at, summary_json) VALUES (?, ?, ?, 'missing', ?, ?)",
                    (run_id, SOURCE, model_id, now, dump_json({"name": current["name"]})),
                )
                missing_count += 1

        conn.execute(
            "UPDATE runs SET finished_at = ?, status = 'ok', models_total = ?, new_count = ?, updated_count = ?, missing_count = ? WHERE run_id = ?",
            (utc_now(), len(models), new_count, updated_count, missing_count, run_id),
        )
        conn.commit()
        print(f"run_id: {run_id}")
        print(f"source: {SOURCE}")
        print(f"models_total: {len(models)}")
        print(f"new: {new_count} | updated: {updated_count} | missing: {missing_count}")
        return 0
    except Exception as exc:
        conn.execute(
            "UPDATE runs SET finished_at = ?, status = 'error', error_message = ? WHERE run_id = ?",
            (utc_now(), str(exc), run_id),
        )
        conn.commit()
        print(f"scan failed: {exc}", file=sys.stderr)
        return 1


def command_brief_new(args: argparse.Namespace) -> int:
    conn = open_db(Path(args.db))
    row = conn.execute(
        "SELECT run_id, event_at FROM events WHERE source = ? AND event_type = 'new' ORDER BY id DESC LIMIT 1",
        (SOURCE,),
    ).fetchone()
    if row is None:
        print("No new models recorded yet.")
        return 0
    run_id = row["run_id"]
    models = conn.execute(
        """
        SELECT m.* FROM events e
        JOIN models m ON m.source = e.source AND m.model_id = e.model_id
        WHERE e.run_id = ? AND e.event_type = 'new'
        ORDER BY e.id ASC
        """,
        (run_id,),
    ).fetchall()
    print(f"OpenRouter new models from run {run_id}: {len(models)}")
    print_model_lines(models, limit=args.limit)
    return 0


def command_recent(args: argparse.Namespace) -> int:
    conn = open_db(Path(args.db))
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.days)).replace(microsecond=0).isoformat()
    rows = conn.execute(
        """
        SELECT * FROM models
        WHERE source = ? AND first_seen_at >= ?
        ORDER BY first_seen_at DESC, model_id ASC
        LIMIT ?
        """,
        (SOURCE, since, args.limit),
    ).fetchall()
    print(f"OpenRouter models first seen in last {args.days} day(s): {len(rows)}")
    print_model_lines(rows)
    return 0


def month_range(month: str | None) -> tuple[str, str, str]:
    today = dt.datetime.now(dt.timezone.utc)
    if month:
        start = dt.datetime.strptime(month, "%Y-%m").replace(tzinfo=dt.timezone.utc)
    else:
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    label = start.strftime("%Y-%m")
    return label, start.isoformat(), end.isoformat()


def command_monthly(args: argparse.Namespace) -> int:
    conn = open_db(Path(args.db))
    label, start, end = month_range(args.month)
    rows = conn.execute(
        """
        SELECT * FROM models
        WHERE source = ? AND first_seen_at >= ? AND first_seen_at < ?
        ORDER BY first_seen_at DESC, model_id ASC
        LIMIT ?
        """,
        (SOURCE, start, end, args.limit),
    ).fetchall()
    print(f"OpenRouter models first seen in {label}: {len(rows)}")
    print_model_lines(rows)
    return 0


def command_stats(args: argparse.Namespace) -> int:
    conn = open_db(Path(args.db))
    total = conn.execute("SELECT COUNT(*) AS c FROM models WHERE source = ? AND is_active = 1", (SOURCE,)).fetchone()["c"]
    added_7d = conn.execute(
        "SELECT COUNT(*) AS c FROM models WHERE source = ? AND first_seen_at >= ?",
        (SOURCE, (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)).replace(microsecond=0).isoformat()),
    ).fetchone()["c"]
    label, start, end = month_range(None)
    added_month = conn.execute(
        "SELECT COUNT(*) AS c FROM models WHERE source = ? AND first_seen_at >= ? AND first_seen_at < ?",
        (SOURCE, start, end),
    ).fetchone()["c"]
    providers = conn.execute(
        "SELECT COALESCE(provider, '-') AS provider, COUNT(*) AS c FROM models WHERE source = ? AND is_active = 1 GROUP BY provider ORDER BY c DESC, provider ASC LIMIT 10",
        (SOURCE,),
    ).fetchall()
    print(f"OpenRouter active models: {total}")
    print(f"Added in last 7 days: {added_7d}")
    print(f"Added in {label}: {added_month}")
    print("Top providers:")
    for row in providers:
        print(f"- {row['provider']}: {row['c']}")
    return 0


def command_show(args: argparse.Namespace) -> int:
    conn = open_db(Path(args.db))
    row = conn.execute(
        "SELECT * FROM models WHERE source = ? AND model_id = ?",
        (SOURCE, args.model_id),
    ).fetchone()
    if row is None:
        print(f"Model not found: {args.model_id}", file=sys.stderr)
        return 1
    print(f"model_id: {row['model_id']}")
    print(f"name: {row['name']}")
    print(f"provider: {row['provider'] or '-'}")
    print(f"created_at: {short_iso(row['created_at'])}")
    print(f"first_seen_at: {short_iso(row['first_seen_at'])}")
    print(f"last_seen_at: {short_iso(row['last_seen_at'])}")
    print(f"context_length: {row['context_length'] or '-'}")
    print(f"modality: {row['modality'] or '-'}")
    print(f"pricing: {format_price_line(row['pricing_json'])}")
    desc = (row['description'] or '').strip()
    if desc:
        print("description:")
        print(textwrap.fill(desc, width=100))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor and report OpenRouter model catalog changes")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite database path")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scan", help="Fetch OpenRouter models and sync local database")
    p.set_defaults(func=command_scan)

    p = sub.add_parser("brief-new", help="Show newly discovered models from the latest run that had new models")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=command_brief_new)

    p = sub.add_parser("recent", help="Show models first seen in the last N days")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=command_recent)

    p = sub.add_parser("monthly", help="Show models first seen in a month")
    p.add_argument("--month", help="Month in YYYY-MM format; default current UTC month")
    p.add_argument("--limit", type=int, default=200)
    p.set_defaults(func=command_monthly)

    p = sub.add_parser("stats", help="Show catalog stats")
    p.set_defaults(func=command_stats)

    p = sub.add_parser("show", help="Show one model")
    p.add_argument("--model-id", required=True)
    p.set_defaults(func=command_show)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
