#!/usr/bin/env python3
"""Read and export OpenCode sessions without mutating the source database."""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any

LOCAL_TZ = datetime.now().astimezone().tzinfo
CORE_TABLES = ("session", "message", "part", "project")
REQUIRED_COLUMNS = {
    "session": {
        "id",
        "project_id",
        "directory",
        "title",
        "time_created",
        "time_updated",
    },
    "message": {"id", "session_id", "time_created", "data"},
    "part": {"id", "message_id", "session_id", "time_created", "data"},
}
INVALID_PATH_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
WHITESPACE_RE = re.compile(r"\s+")
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def tool_version() -> str:
    version_path = Path(__file__).resolve().parents[1] / "VERSION"
    try:
        value = version_path.read_text(encoding="utf-8").strip()
    except OSError:
        return "development"
    return value or "development"


class UserError(RuntimeError):
    """An actionable command-line error without a traceback."""


@dataclass(slots=True)
class Capabilities:
    tables: dict[str, set[str]]
    indexes: dict[str, list[str]]

    def has_table(self, table_name: str) -> bool:
        return table_name in self.tables

    def has_columns(self, table_name: str, columns: Iterable[str]) -> bool:
        return set(columns).issubset(self.tables.get(table_name, set()))


@dataclass(slots=True)
class SessionRecord:
    id: str
    project_id: str
    directory: str
    title: str
    time_created: int
    time_updated: int
    time_archived: int | None = None
    version: str | None = None
    summary_additions: int | None = None
    summary_deletions: int | None = None
    summary_files: int | None = None
    project_name: str | None = None
    project_worktree: str | None = None


@dataclass(slots=True)
class PartRecord:
    id: str
    created_ms: int
    type: str
    payload: dict[str, Any] | None
    raw_data: str


@dataclass(slots=True)
class MessageRecord:
    id: str
    created_ms: int
    role: str
    model_id: str | None
    provider_id: str | None
    payload: dict[str, Any] | None
    raw_data: str
    parts: list[PartRecord] = field(default_factory=list)


@dataclass(slots=True)
class TimeBound:
    milliseconds: int
    inclusive: bool


def add_db_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--db-path",
        help="OpenCode SQLite path. Defaults to `opencode db path`.",
    )


def add_output_format(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format",
        choices=("table", "json"),
        default="table",
        help="Output format. Default: table.",
    )


def add_session_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--session-id",
        action="append",
        default=[],
        help="Exact session ID; repeat for OR matching.",
    )
    parser.add_argument(
        "--project",
        action="append",
        default=[],
        help="Literal project substring; repeat for OR matching.",
    )
    parser.add_argument(
        "--title",
        action="append",
        default=[],
        help="Literal title substring; repeat for OR matching.",
    )
    parser.add_argument(
        "--directory",
        action="append",
        default=[],
        help="Literal directory substring; repeat for OR matching.",
    )
    parser.add_argument(
        "--start", help="Inclusive ISO date/datetime or Unix timestamp."
    )
    parser.add_argument(
        "--end", help="Inclusive ISO datetime or inclusive local calendar date."
    )
    parser.add_argument(
        "--time-field",
        choices=("created", "updated"),
        default="updated",
        help="Time field used by --start/--end. Default: updated.",
    )
    parser.add_argument(
        "--archived",
        choices=("exclude", "include", "only"),
        default="exclude",
        help="Archived-session handling. Default: exclude.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect and export OpenCode sessions through a read-only SQLite connection."
    )
    parser.add_argument(
        "--version", action="version", version=f"opencode-sessions {tool_version()}"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    doctor = commands.add_parser(
        "doctor", help="Resolve the DB and report command capabilities."
    )
    add_db_argument(doctor)
    add_output_format(doctor)

    list_parser = commands.add_parser("list", help="List sessions and metadata.")
    add_db_argument(list_parser)
    add_output_format(list_parser)
    add_session_filters(list_parser)
    list_parser.add_argument(
        "--limit", type=positive_int, default=20, help="Maximum sessions. Default: 20."
    )

    show = commands.add_parser("show", help="Render one session transcript.")
    add_db_argument(show)
    show.add_argument("session_id")
    show.add_argument("--format", choices=("markdown", "json"), default="markdown")
    show.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Include reasoning and complete message/part payloads.",
    )

    search = commands.add_parser(
        "search", help="Search literal text without SQL wildcard semantics."
    )
    add_db_argument(search)
    add_output_format(search)
    add_session_filters(search)
    search.add_argument("query", help="Literal text to search for.")
    search.add_argument("--scope", choices=("all", "title", "messages"), default="all")
    search.add_argument(
        "--limit", type=positive_int, default=20, help="Maximum sessions. Default: 20."
    )

    export = commands.add_parser(
        "export", help="Export selected sessions into an output directory."
    )
    add_db_argument(export)
    add_session_filters(export)
    export.add_argument(
        "--all", action="store_true", help="Acknowledge an unfiltered full export."
    )
    export.add_argument("--output-dir", required=True)
    export.add_argument("--format", choices=("markdown", "jsonl"), default="markdown")
    export.add_argument("--group-by-project", action="store_true")
    export.add_argument("--overwrite", action="store_true")
    export.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview target paths and conflicts without writing files.",
    )
    export.add_argument(
        "--limit", type=positive_int, help="Optional maximum session count."
    )
    export.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Include reasoning and complete message/part payloads.",
    )

    schema = commands.add_parser(
        "schema", help="Show the live core-table schema and indexes."
    )
    add_db_argument(schema)
    add_output_format(schema)
    schema.add_argument("--table", choices=CORE_TABLES, action="append", default=[])
    return parser


def positive_int(raw: str) -> int:
    value = int(raw)
    if value < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return value


def resolve_db_path(explicit_path: str | None) -> Path:
    if explicit_path:
        path = Path(explicit_path).expanduser().resolve()
    else:
        try:
            result = subprocess.run(
                ["opencode", "db", "path"],
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise UserError(
                "`opencode` was not found. Pass --db-path explicitly."
            ) from exc
        except subprocess.CalledProcessError as exc:
            detail = exc.stderr.strip() or exc.stdout.strip() or "unknown error"
            raise UserError(f"`opencode db path` failed: {detail}") from exc
        raw_path = result.stdout.strip()
        if not raw_path:
            raise UserError("`opencode db path` returned an empty path.")
        path = Path(raw_path).expanduser().resolve()
    if not path.is_file():
        raise UserError(f"OpenCode database not found: {path}")
    return path


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    uri = f"{db_path.as_uri()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    try:
        connection.execute("PRAGMA trusted_schema = OFF")
    except sqlite3.DatabaseError:
        pass
    return connection


def quote_identifier(identifier: str) -> str:
    if identifier not in CORE_TABLES:
        raise UserError(f"Unsupported table: {identifier}")
    return f'"{identifier}"'


def inspect_capabilities(connection: sqlite3.Connection) -> Capabilities:
    known_tables = {
        str(row["name"])
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    tables: dict[str, set[str]] = {}
    indexes: dict[str, list[str]] = {}
    for table_name in CORE_TABLES:
        if table_name not in known_tables:
            continue
        quoted = quote_identifier(table_name)
        tables[table_name] = {
            str(row["name"])
            for row in connection.execute(f"PRAGMA table_info({quoted})")
        }
        indexes[table_name] = [
            str(row["name"])
            for row in connection.execute(f"PRAGMA index_list({quoted})")
        ]
    return Capabilities(tables=tables, indexes=indexes)


def require_capability(capabilities: Capabilities, table_name: str) -> None:
    missing = REQUIRED_COLUMNS[table_name] - capabilities.tables.get(table_name, set())
    if table_name not in capabilities.tables:
        raise UserError(f"Unsupported OpenCode database: missing `{table_name}` table.")
    if missing:
        fields = ", ".join(sorted(missing))
        raise UserError(
            f"Unsupported `{table_name}` schema; missing columns: {fields}."
        )


def parse_time_bound(raw: str | None, *, is_end: bool) -> TimeBound | None:
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    if re.fullmatch(r"\d{10,16}", value):
        number = int(value)
        return TimeBound(number * 1000 if len(value) <= 10 else number, True)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            day = date.fromisoformat(value)
        except ValueError as exc:
            raise UserError(f"Invalid date: {raw}") from exc
        day_start = datetime.combine(day, time.min, tzinfo=LOCAL_TZ)
        if is_end:
            next_day = day_start + timedelta(days=1)
            return TimeBound(int(next_day.timestamp() * 1000), False)
        return TimeBound(int(day_start.timestamp() * 1000), True)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise UserError(
            f"Invalid time `{raw}`; use ISO date/datetime or Unix time."
        ) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=LOCAL_TZ)
    return TimeBound(int(parsed.timestamp() * 1000), True)


def to_iso_utc(timestamp_ms: int | None) -> str | None:
    if timestamp_ms is None:
        return None
    return (
        datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def optional_column(
    capabilities: Capabilities, table: str, column: str, alias: str
) -> str:
    if capabilities.has_columns(table, {column}):
        return f"s.{column} AS {alias}"
    return f"NULL AS {alias}"


def substring_condition(expression: str, terms: Sequence[str]) -> tuple[str, list[str]]:
    cleaned = [term.strip() for term in terms if term.strip()]
    if not cleaned:
        return "", []
    clause = " OR ".join(f"instr(lower({expression}), lower(?)) > 0" for _ in cleaned)
    return f"({clause})", cleaned


def build_filter_clause(
    args: argparse.Namespace,
    capabilities: Capabilities,
) -> tuple[list[str], list[Any]]:
    conditions: list[str] = []
    parameters: list[Any] = []
    if args.session_id:
        placeholders = ", ".join("?" for _ in args.session_id)
        conditions.append(f"s.id IN ({placeholders})")
        parameters.extend(args.session_id)

    project_expressions = ["s.project_id", "s.directory"]
    if capabilities.has_columns("project", {"id", "name", "worktree"}):
        project_expressions.extend(["coalesce(p.name, '')", "coalesce(p.worktree, '')"])
    if args.project:
        term_clauses: list[str] = []
        for term in (value.strip() for value in args.project if value.strip()):
            term_clauses.append(
                "("
                + " OR ".join(
                    f"instr(lower({expr}), lower(?)) > 0"
                    for expr in project_expressions
                )
                + ")"
            )
            parameters.extend([term] * len(project_expressions))
        if term_clauses:
            conditions.append("(" + " OR ".join(term_clauses) + ")")

    for expression, values in (
        ("s.title", args.title),
        ("s.directory", args.directory),
    ):
        clause, params = substring_condition(expression, values)
        if clause:
            conditions.append(clause)
            parameters.extend(params)

    time_column = "s.time_created" if args.time_field == "created" else "s.time_updated"
    start = parse_time_bound(args.start, is_end=False)
    end = parse_time_bound(args.end, is_end=True)
    if start:
        conditions.append(f"{time_column} >= ?")
        parameters.append(start.milliseconds)
    if end:
        conditions.append(f"{time_column} {'<=' if end.inclusive else '<'} ?")
        parameters.append(end.milliseconds)
    if (
        start
        and end
        and (
            start.milliseconds > end.milliseconds
            or (start.milliseconds == end.milliseconds and not end.inclusive)
        )
    ):
        raise UserError("--start must not be later than --end.")

    has_archived = capabilities.has_columns("session", {"time_archived"})
    if args.archived == "only" and not has_archived:
        raise UserError("This database has no session.time_archived column.")
    if has_archived and args.archived == "exclude":
        conditions.append("s.time_archived IS NULL")
    elif has_archived and args.archived == "only":
        conditions.append("s.time_archived IS NOT NULL")
    return conditions, parameters


def load_sessions(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    args: argparse.Namespace,
    *,
    extra_conditions: Sequence[str] = (),
    extra_parameters: Sequence[Any] = (),
) -> list[SessionRecord]:
    require_capability(capabilities, "session")
    conditions, parameters = build_filter_clause(args, capabilities)
    conditions.extend(extra_conditions)
    parameters.extend(extra_parameters)
    where = " AND ".join(conditions) if conditions else "1 = 1"
    join = ""
    project_name = "NULL AS project_name"
    project_worktree = "NULL AS project_worktree"
    if capabilities.has_columns("project", {"id", "name", "worktree"}):
        join = "LEFT JOIN project AS p ON p.id = s.project_id"
        project_name = "p.name AS project_name"
        project_worktree = "p.worktree AS project_worktree"
    limit = getattr(args, "limit", None)
    limit_sql = " LIMIT ?" if limit else ""
    if limit:
        parameters.append(limit)
    query = f"""
        SELECT
            s.id,
            s.project_id,
            s.directory,
            s.title,
            s.time_created,
            s.time_updated,
            {optional_column(capabilities, "session", "time_archived", "time_archived")},
            {optional_column(capabilities, "session", "version", "version")},
            {optional_column(capabilities, "session", "summary_additions", "summary_additions")},
            {optional_column(capabilities, "session", "summary_deletions", "summary_deletions")},
            {optional_column(capabilities, "session", "summary_files", "summary_files")},
            {project_name},
            {project_worktree}
        FROM session AS s
        {join}
        WHERE {where}
        ORDER BY s.time_updated DESC, s.id ASC
        {limit_sql}
    """
    return [
        SessionRecord(
            id=str(row["id"]),
            project_id=str(row["project_id"]),
            directory=str(row["directory"]),
            title=str(row["title"]),
            time_created=int(row["time_created"]),
            time_updated=int(row["time_updated"]),
            time_archived=row["time_archived"],
            version=row["version"],
            summary_additions=row["summary_additions"],
            summary_deletions=row["summary_deletions"],
            summary_files=row["summary_files"],
            project_name=row["project_name"],
            project_worktree=row["project_worktree"],
        )
        for row in connection.execute(query, parameters)
    ]


def safe_json_loads(raw: str) -> dict[str, Any] | None:
    try:
        value = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None
    return value if isinstance(value, dict) else {"value": value}


def load_transcript(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    session_id: str,
) -> list[MessageRecord]:
    require_capability(capabilities, "message")
    require_capability(capabilities, "part")
    message_rows = connection.execute(
        """
        SELECT id, time_created, data
        FROM message
        WHERE session_id = ?
        ORDER BY time_created ASC, id ASC
        """,
        (session_id,),
    ).fetchall()
    messages: list[MessageRecord] = []
    by_id: dict[str, MessageRecord] = {}
    for row in message_rows:
        raw = str(row["data"])
        payload = safe_json_loads(raw)
        message = MessageRecord(
            id=str(row["id"]),
            created_ms=int(row["time_created"]),
            role=str((payload or {}).get("role") or "unknown"),
            model_id=string_or_none((payload or {}).get("modelID")),
            provider_id=string_or_none((payload or {}).get("providerID")),
            payload=payload,
            raw_data=raw,
        )
        messages.append(message)
        by_id[message.id] = message

    for row in connection.execute(
        """
        SELECT id, message_id, time_created, data
        FROM part
        WHERE session_id = ?
        ORDER BY message_id ASC, time_created ASC, id ASC
        """,
        (session_id,),
    ):
        message = by_id.get(str(row["message_id"]))
        if message is None:
            continue
        raw = str(row["data"])
        payload = safe_json_loads(raw)
        message.parts.append(
            PartRecord(
                id=str(row["id"]),
                created_ms=int(row["time_created"]),
                type=str((payload or {}).get("type") or "unknown"),
                payload=payload,
                raw_data=raw,
            )
        )
    return messages


def string_or_none(value: Any) -> str | None:
    return str(value) if value not in (None, "") else None


def project_label(session: SessionRecord) -> str:
    if session.project_name and session.project_name.strip():
        return session.project_name.strip()
    for candidate in (session.project_worktree, session.directory):
        if candidate:
            name = Path(candidate).name.strip()
            if name:
                return name
    return session.project_id or "unknown-project"


def session_summary(session: SessionRecord) -> dict[str, Any]:
    return {
        "id": session.id,
        "title": session.title,
        "project": project_label(session),
        "project_id": session.project_id,
        "directory": session.directory,
        "created": to_iso_utc(session.time_created),
        "updated": to_iso_utc(session.time_updated),
        "archived": to_iso_utc(session.time_archived),
    }


def format_table(rows: Sequence[dict[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "No results."
    rendered = [[single_line(row.get(column)) for column in columns] for row in rows]
    widths = [
        max(len(column), *(len(row[index]) for row in rendered))
        for index, column in enumerate(columns)
    ]
    header = "  ".join(
        column.ljust(widths[index]) for index, column in enumerate(columns)
    )
    separator = "  ".join("-" * width for width in widths)
    body = [
        "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))
        for row in rendered
    ]
    return "\n".join([header, separator, *body])


def single_line(value: Any) -> str:
    if value is None:
        return ""
    return WHITESPACE_RE.sub(" ", str(value)).strip()


def dynamic_fence(text: str, language: str = "") -> tuple[str, str]:
    longest = max(
        (len(match.group(0)) for match in re.finditer(r"`+", text)), default=0
    )
    fence = "`" * max(3, longest + 1)
    return f"{fence}{language}", fence


def fenced_block(text: str, language: str = "") -> list[str]:
    opening, closing = dynamic_fence(text, language)
    return [opening, text, closing, ""]


def inline_code(value: Any) -> str:
    text = single_line(value)
    longest = max(
        (len(match.group(0)) for match in re.finditer(r"`+", text)), default=0
    )
    fence = "`" * max(1, longest + 1)
    padding = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{fence}{padding}{text}{padding}{fence}"


def tool_summary(payload: dict[str, Any]) -> dict[str, Any]:
    state = payload.get("state") if isinstance(payload.get("state"), dict) else {}
    return {
        "tool": payload.get("tool"),
        "status": state.get("status"),
    }


def projected_messages(
    messages: Sequence[MessageRecord], include_sensitive: bool
) -> list[dict[str, Any]]:
    projected: list[dict[str, Any]] = []
    for message in messages:
        parts: list[dict[str, Any]] = []
        for part in message.parts:
            payload = part.payload or {}
            if include_sensitive:
                parts.append(
                    {
                        "id": part.id,
                        "type": part.type,
                        "created": to_iso_utc(part.created_ms),
                        "data": payload if part.payload is not None else part.raw_data,
                    }
                )
            elif part.type == "text" and isinstance(payload.get("text"), str):
                parts.append({"type": "text", "text": payload["text"]})
            elif part.type == "tool":
                parts.append({"type": "tool", **tool_summary(payload)})
        item: dict[str, Any] = {
            "id": message.id,
            "role": message.role,
            "created": to_iso_utc(message.created_ms),
            "model": message.model_id,
            "provider": message.provider_id,
            "parts": parts,
        }
        if include_sensitive:
            item["data"] = (
                message.payload if message.payload is not None else message.raw_data
            )
        projected.append(item)
    return projected


def render_session_markdown(
    session: SessionRecord,
    messages: Sequence[MessageRecord],
    *,
    include_sensitive: bool,
) -> str:
    omitted = sum(
        1
        for message in messages
        for part in message.parts
        if part.type not in {"text", "tool"}
    )
    lines = [
        f"# {single_line(session.title)}",
        "",
        f"- Session ID: {inline_code(session.id)}",
        f"- Project: {inline_code(project_label(session))}",
        f"- Project ID: {inline_code(session.project_id)}",
        f"- Directory: {inline_code(session.directory)}",
        f"- Created: {inline_code(to_iso_utc(session.time_created))}",
        f"- Updated: {inline_code(to_iso_utc(session.time_updated))}",
        f"- Messages: {len(messages)}",
    ]
    if session.time_archived is not None:
        lines.append(f"- Archived: {inline_code(to_iso_utc(session.time_archived))}")
    if omitted and not include_sensitive:
        lines.append(f"- Sensitive or non-display parts omitted: {omitted}")
    lines.extend(["", "## Transcript", ""])
    for message_index, message in enumerate(messages, start=1):
        lines.extend(
            [
                f"### Message {message_index} · {inline_code(message.role)}",
                "",
                f"- Message ID: {inline_code(message.id)}",
                f"- Created: {inline_code(to_iso_utc(message.created_ms))}",
            ]
        )
        if message.model_id:
            lines.append(f"- Model: {inline_code(message.model_id)}")
        if message.provider_id:
            lines.append(f"- Provider: {inline_code(message.provider_id)}")
        lines.append("")
        visible_index = 0
        for part in message.parts:
            payload = part.payload or {}
            if part.type == "text" and isinstance(payload.get("text"), str):
                visible_index += 1
                lines.extend([f"#### Part {visible_index} · text", ""])
                lines.extend(fenced_block(payload["text"], "text"))
            elif part.type == "tool":
                visible_index += 1
                summary = tool_summary(payload)
                lines.extend([f"#### Part {visible_index} · tool", ""])
                for key in ("tool", "status"):
                    if summary[key] not in (None, ""):
                        lines.append(f"- {key.title()}: {inline_code(summary[key])}")
                lines.append("")
            if include_sensitive:
                raw_json = (
                    json.dumps(payload, ensure_ascii=False, indent=2)
                    if part.payload is not None
                    else part.raw_data
                )
                lines.extend([f"#### Raw part · {inline_code(part.type)}", ""])
                lines.extend(fenced_block(raw_json, "json"))
        if include_sensitive:
            raw_message = (
                json.dumps(message.payload, ensure_ascii=False, indent=2)
                if message.payload is not None
                else message.raw_data
            )
            lines.extend(["#### Raw message", ""])
            lines.extend(fenced_block(raw_message, "json"))
    if not messages:
        lines.extend(["_No messages found._", ""])
    return "\n".join(lines).rstrip() + "\n"


def truncate_utf8(value: str, max_bytes: int) -> str:
    encoded = value.encode("utf-8")
    if len(encoded) <= max_bytes:
        return value
    shortened = encoded[:max_bytes]
    while shortened:
        try:
            return shortened.decode("utf-8").rstrip()
        except UnicodeDecodeError:
            shortened = shortened[:-1]
    return ""


def sanitize_component(
    value: str | None, fallback: str, *, max_bytes: int = 120
) -> str:
    text = INVALID_PATH_CHARS.sub("-", value or "")
    text = WHITESPACE_RE.sub(" ", text).strip(" .")
    text = re.sub(r"-{2,}", "-", text)
    text = truncate_utf8(text, max_bytes).strip(" .") or fallback
    if text.upper() in WINDOWS_RESERVED_NAMES:
        text = f"_{text}"
    return text


def output_filename(session: SessionRecord, suffix: str) -> str:
    title = sanitize_component(session.title, "untitled-session")
    created = datetime.fromtimestamp(
        session.time_created / 1000, tz=timezone.utc
    ).strftime("%Y-%m-%dT%H-%M-%SZ")
    session_id = sanitize_component(session.id, "unknown-session", max_bytes=64)
    return f"{title}_{created}_{session_id}.{suffix}"


def has_explicit_filter(args: argparse.Namespace) -> bool:
    text_filters = (
        args.session_id,
        args.project,
        args.title,
        args.directory,
    )
    return (
        any(any(value.strip() for value in values) for values in text_filters)
        or bool((args.start or "").strip())
        or bool((args.end or "").strip())
        or args.archived == "only"
    )


def write_files_atomically(
    files: Sequence[tuple[Path, str]],
    *,
    overwrite: bool,
) -> tuple[list[Path], list[Path]]:
    conflicts: list[Path] = []
    unchanged: list[Path] = []
    pending: list[tuple[Path, str]] = []
    for path, content in files:
        status = output_status(path, content, overwrite=overwrite)
        if status == "unchanged":
            unchanged.append(path)
        elif status == "conflict":
            conflicts.append(path)
        else:
            pending.append((path, content))
    if conflicts:
        preview = "\n".join(f"- {path}" for path in conflicts[:10])
        raise UserError(
            f"Refusing to overwrite changed output; pass --overwrite:\n{preview}"
        )

    written: list[Path] = []
    try:
        for path, content in pending:
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                handle.write(content)
                temp_path = Path(handle.name)
            try:
                os.replace(temp_path, path)
            finally:
                if temp_path.exists():
                    temp_path.unlink()
            written.append(path)
    except OSError as exc:
        raise UserError(f"Failed to write export output: {exc}") from exc
    return written, unchanged


def output_status(path: Path, content: str, *, overwrite: bool) -> str:
    if not path.exists() and not path.is_symlink():
        ancestor = path.parent
        while not ancestor.exists() and not ancestor.is_symlink():
            if ancestor == ancestor.parent:
                break
            ancestor = ancestor.parent
        if ancestor.exists() and not ancestor.is_dir():
            return "conflict"
        return "new"
    if path.is_symlink():
        return "overwrite" if overwrite else "conflict"
    if path.is_file():
        try:
            if path.read_text(encoding="utf-8") == content:
                return "unchanged"
        except (OSError, UnicodeError) as exc:
            raise UserError(f"Failed to inspect existing output {path}: {exc}") from exc
        return "overwrite" if overwrite else "conflict"
    return "conflict"


def handle_doctor(
    connection: sqlite3.Connection,
    db_path: Path,
    capabilities: Capabilities,
    args: argparse.Namespace,
) -> None:
    commands = {
        "list": capabilities.has_columns("session", REQUIRED_COLUMNS["session"]),
        "show": all(
            capabilities.has_columns(name, REQUIRED_COLUMNS[name])
            for name in ("session", "message", "part")
        ),
        "search-title": capabilities.has_columns(
            "session", REQUIRED_COLUMNS["session"]
        ),
        "search-messages": all(
            capabilities.has_columns(name, REQUIRED_COLUMNS[name])
            for name in ("session", "message")
        ),
        "export": all(
            capabilities.has_columns(name, REQUIRED_COLUMNS[name])
            for name in ("session", "message", "part")
        ),
    }
    data = {
        "database": str(db_path),
        "sqlite_version": sqlite3.sqlite_version,
        "tables": {
            name: sorted(columns) for name, columns in capabilities.tables.items()
        },
        "commands": commands,
        "read_only": True,
    }
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    print(f"Database: {db_path}")
    print(f"SQLite: {sqlite3.sqlite_version}")
    print("Read-only: yes")
    print("\nCommand capabilities:")
    print(
        format_table(
            [
                {"command": key, "available": "yes" if value else "no"}
                for key, value in commands.items()
            ],
            ("command", "available"),
        )
    )


def handle_list(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    args: argparse.Namespace,
) -> None:
    sessions = load_sessions(connection, capabilities, args)
    rows = [session_summary(session) for session in sessions]
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(format_table(rows, ("id", "title", "project", "directory", "updated")))


def load_one_session(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    session_id: str,
) -> SessionRecord:
    namespace = argparse.Namespace(
        session_id=[session_id],
        project=[],
        title=[],
        directory=[],
        start=None,
        end=None,
        time_field="updated",
        archived="include",
        limit=2,
    )
    sessions = load_sessions(connection, capabilities, namespace)
    if not sessions:
        raise UserError(f"Session not found: {session_id}")
    return sessions[0]


def handle_show(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    args: argparse.Namespace,
) -> None:
    session = load_one_session(connection, capabilities, args.session_id)
    messages = load_transcript(connection, capabilities, session.id)
    if args.include_sensitive:
        print("Warning: sensitive payload export enabled.", file=sys.stderr)
    if args.format == "json":
        data = {
            "session": session_summary(session),
            "messages": projected_messages(messages, args.include_sensitive),
            "include_sensitive": args.include_sensitive,
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(
            render_session_markdown(
                session, messages, include_sensitive=args.include_sensitive
            ),
            end="",
        )


def handle_search(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    args: argparse.Namespace,
) -> None:
    args.query = args.query.strip()
    if not args.query:
        raise UserError("Search query must not be empty.")
    clauses: list[str] = []
    parameters: list[Any] = []
    if args.scope in ("all", "title"):
        clauses.append(
            "(instr(lower(s.title), lower(?)) > 0 OR instr(lower(s.directory), lower(?)) > 0)"
        )
        parameters.extend([args.query, args.query])
    if args.scope in ("all", "messages"):
        require_capability(capabilities, "message")
        clauses.append(
            "EXISTS (SELECT 1 FROM message AS sm WHERE sm.session_id = s.id AND instr(lower(sm.data), lower(?)) > 0)"
        )
        parameters.append(args.query)
    sessions = load_sessions(
        connection,
        capabilities,
        args,
        extra_conditions=["(" + " OR ".join(clauses) + ")"],
        extra_parameters=parameters,
    )
    rows = [session_summary(session) for session in sessions]
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(format_table(rows, ("id", "title", "project", "directory", "updated")))


def handle_export(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    args: argparse.Namespace,
) -> None:
    if not args.all and not has_explicit_filter(args):
        raise UserError("Refusing an implicit full export; add a filter or pass --all.")
    sessions = load_sessions(connection, capabilities, args)
    if not sessions:
        print("Matched sessions: 0")
        print("Nothing exported.")
        return
    if args.include_sensitive:
        print("Warning: sensitive payload export enabled.", file=sys.stderr)
    output_root = Path(args.output_dir).expanduser().resolve()
    files: list[tuple[Path, str]] = []
    if args.format == "jsonl":
        lines: list[str] = []
        for session in sessions:
            messages = load_transcript(connection, capabilities, session.id)
            lines.append(
                json.dumps(
                    {
                        "session": session_summary(session),
                        "messages": projected_messages(
                            messages, args.include_sensitive
                        ),
                        "include_sensitive": args.include_sensitive,
                    },
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        files.append((output_root / "sessions.jsonl", "\n".join(lines) + "\n"))
    else:
        for session in sessions:
            messages = load_transcript(connection, capabilities, session.id)
            directory = output_root
            if args.group_by_project:
                directory /= sanitize_component(
                    project_label(session), "unknown-project"
                )
            files.append(
                (
                    directory / output_filename(session, "md"),
                    render_session_markdown(
                        session, messages, include_sensitive=args.include_sensitive
                    ),
                )
            )
    if args.dry_run:
        rows = [
            {
                "status": output_status(path, content, overwrite=args.overwrite),
                "path": str(path),
            }
            for path, content in files
        ]
        print(format_table(rows, ("status", "path")))
        print(f"Matched sessions: {len(sessions)}")
        print("Dry run: no files written.")
        if any(row["status"] == "conflict" for row in rows):
            raise UserError(
                "Dry run found output conflicts; pass --overwrite to replace them."
            )
        return
    written, unchanged = write_files_atomically(files, overwrite=args.overwrite)
    print(f"Matched sessions: {len(sessions)}")
    print(f"Written files: {len(written)}")
    print(f"Unchanged files: {len(unchanged)}")
    print(f"Output directory: {output_root}")


def handle_schema(
    connection: sqlite3.Connection,
    capabilities: Capabilities,
    args: argparse.Namespace,
) -> None:
    selected = args.table or list(CORE_TABLES)
    data: list[dict[str, Any]] = []
    for table_name in selected:
        columns = capabilities.tables.get(table_name)
        if columns is None:
            data.append(
                {"table": table_name, "available": False, "columns": [], "indexes": []}
            )
        else:
            data.append(
                {
                    "table": table_name,
                    "available": True,
                    "columns": sorted(columns),
                    "indexes": sorted(capabilities.indexes.get(table_name, [])),
                }
            )
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    rows = [
        {
            "table": item["table"],
            "available": "yes" if item["available"] else "no",
            "columns": ", ".join(item["columns"]),
            "indexes": ", ".join(item["indexes"]),
        }
        for item in data
    ]
    print(format_table(rows, ("table", "available", "columns", "indexes")))


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    db_path = resolve_db_path(args.db_path)
    with connect_read_only(db_path) as connection:
        capabilities = inspect_capabilities(connection)
        handlers = {
            "doctor": handle_doctor,
            "list": handle_list,
            "show": handle_show,
            "search": handle_search,
            "export": handle_export,
            "schema": handle_schema,
        }
        handler = handlers[args.command]
        if args.command == "doctor":
            handler(connection, db_path, capabilities, args)
        else:
            handler(connection, capabilities, args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except UserError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    except sqlite3.DatabaseError as exc:
        print(f"error: SQLite query failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)
