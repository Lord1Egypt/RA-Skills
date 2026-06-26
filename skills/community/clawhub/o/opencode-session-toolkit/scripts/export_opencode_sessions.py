#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

LOCAL_TZ = datetime.now().astimezone().tzinfo
DEFAULT_SKIPPED_PART_TYPES = {"step-start", "step-finish"}
INVALID_PATH_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
WHITESPACE_RE = re.compile(r"\s+")


@dataclass(slots=True)
class SessionRecord:
    id: str
    project_id: str
    directory: str
    title: str
    version: str | None
    summary_additions: int | None
    summary_deletions: int | None
    summary_files: int | None
    time_created: int
    time_updated: int
    time_archived: int | None
    project_name: str | None
    project_worktree: str | None


@dataclass(slots=True)
class PartRecord:
    id: str | None
    created_ms: int | None
    type: str
    payload: dict[str, Any] | None
    raw_data: str | None


@dataclass(slots=True)
class MessageRecord:
    id: str
    created_ms: int
    role: str
    model_id: str | None
    provider_id: str | None
    agent: str | None
    mode: str | None
    finish: str | None
    raw_data: str | None
    payload: dict[str, Any] | None
    parts: list[PartRecord] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export OpenCode sessions to Markdown files. One session becomes one "
            "Markdown file."
        )
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to write exported Markdown files into.",
    )
    parser.add_argument(
        "--db-path",
        help="OpenCode SQLite database path. Defaults to `opencode db path`.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Export all sessions. Required when no other filter is provided.",
    )
    parser.add_argument(
        "--group-by-project",
        action="store_true",
        help="Create one folder per project under the output directory.",
    )
    parser.add_argument(
        "--project",
        action="append",
        default=[],
        help=(
            "Project matcher. Matches project id, project name, project worktree, "
            "or session directory by substring. Can be repeated."
        ),
    )
    parser.add_argument(
        "--session-id",
        action="append",
        default=[],
        help="Export only the specified session id. Can be repeated.",
    )
    parser.add_argument(
        "--title-contains",
        action="append",
        default=[],
        help="Filter sessions by title substring. Can be repeated.",
    )
    parser.add_argument(
        "--directory-contains",
        action="append",
        default=[],
        help="Filter sessions by directory substring. Can be repeated.",
    )
    parser.add_argument(
        "--start",
        help=(
            "Start of the time window. Accepts ISO datetime/date, Unix seconds, "
            "or Unix milliseconds."
        ),
    )
    parser.add_argument(
        "--end",
        help=(
            "End of the time window. Accepts ISO datetime/date, Unix seconds, "
            "or Unix milliseconds."
        ),
    )
    parser.add_argument(
        "--time-field",
        choices=("created", "updated"),
        default="updated",
        help="Time field used by --start/--end. Default: updated.",
    )
    parser.add_argument(
        "--filename-time-field",
        choices=("created", "updated"),
        default="created",
        help="Time field appended to exported filenames. Default: created.",
    )
    parser.add_argument(
        "--archived",
        choices=("include", "exclude", "only"),
        default="include",
        help="Archived session handling. Default: include.",
    )
    parser.add_argument(
        "--include-part-type",
        action="append",
        default=[],
        help="Only export the specified part type(s). Can be repeated.",
    )
    parser.add_argument(
        "--exclude-part-type",
        action="append",
        default=[],
        help="Exclude the specified part type(s). Can be repeated.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite files when the target filename already exists.",
    )
    args = parser.parse_args()
    ensure_filters_or_all(args)
    return args


def ensure_filters_or_all(args: argparse.Namespace) -> None:
    has_filter = any(
        [
            args.project,
            args.session_id,
            args.title_contains,
            args.directory_contains,
            args.start,
            args.end,
            args.archived != "include",
        ]
    )
    if not args.all and not has_filter:
        raise SystemExit(
            "Refusing to export every session implicitly. Use --all or add a filter."
        )


def resolve_db_path(explicit_path: str | None) -> Path:
    if explicit_path:
        db_path = Path(explicit_path).expanduser()
    else:
        try:
            result = subprocess.run(
                ["opencode", "db", "path"],
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise SystemExit("`opencode` command not found in PATH.") from exc
        except subprocess.CalledProcessError as exc:
            raise SystemExit(
                f"Failed to resolve OpenCode DB path: {exc.stderr.strip()}"
            ) from exc
        db_path = Path(result.stdout.strip()).expanduser()
    if not db_path.is_file():
        raise SystemExit(f"OpenCode DB not found: {db_path}")
    return db_path


def connect_db(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def parse_timestamp(raw: str | None) -> int | None:
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    if re.fullmatch(r"\d{10,16}", value):
        number = int(value)
        if len(value) <= 10:
            return number * 1000
        return number
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(
            f"Invalid datetime value: {raw}. Use ISO datetime/date or Unix time."
        ) from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LOCAL_TZ)
    return int(dt.timestamp() * 1000)


def to_display_time(timestamp_ms: int | None) -> str:
    if timestamp_ms is None:
        return "null"
    dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=LOCAL_TZ)
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def to_filename_time(timestamp_ms: int | None) -> str:
    if timestamp_ms is None:
        return "unknown-time"
    dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=LOCAL_TZ)
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def sanitize_path_component(value: str | None, fallback: str) -> str:
    text = (value or "").strip()
    text = INVALID_PATH_CHARS.sub("-", text)
    text = WHITESPACE_RE.sub(" ", text)
    text = text.strip(" .")
    text = re.sub(r"-{2,}", "-", text)
    return text or fallback


def sql_like_term(value: str) -> str:
    return f"%{value.strip()}%"


def load_sessions(connection: sqlite3.Connection, args: argparse.Namespace) -> list[SessionRecord]:
    conditions: list[str] = []
    parameters: list[Any] = []

    if args.session_id:
        placeholders = ", ".join("?" for _ in args.session_id)
        conditions.append(f"s.id IN ({placeholders})")
        parameters.extend(args.session_id)

    for term in args.project:
        conditions.append(
            "("
            "LOWER(s.project_id) LIKE LOWER(?) OR "
            "LOWER(COALESCE(p.name, '')) LIKE LOWER(?) OR "
            "LOWER(COALESCE(p.worktree, '')) LIKE LOWER(?) OR "
            "LOWER(s.directory) LIKE LOWER(?)"
            ")"
        )
        wildcard = sql_like_term(term)
        parameters.extend([wildcard, wildcard, wildcard, wildcard])

    for term in args.title_contains:
        conditions.append("LOWER(s.title) LIKE LOWER(?)")
        parameters.append(sql_like_term(term))

    for term in args.directory_contains:
        conditions.append("LOWER(s.directory) LIKE LOWER(?)")
        parameters.append(sql_like_term(term))

    time_column = "s.time_created" if args.time_field == "created" else "s.time_updated"
    start_ms = parse_timestamp(args.start)
    end_ms = parse_timestamp(args.end)
    if start_ms is not None:
        conditions.append(f"{time_column} >= ?")
        parameters.append(start_ms)
    if end_ms is not None:
        conditions.append(f"{time_column} <= ?")
        parameters.append(end_ms)

    if args.archived == "exclude":
        conditions.append("s.time_archived IS NULL")
    elif args.archived == "only":
        conditions.append("s.time_archived IS NOT NULL")

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    query = f"""
        SELECT
            s.id,
            s.project_id,
            s.directory,
            s.title,
            s.version,
            s.summary_additions,
            s.summary_deletions,
            s.summary_files,
            s.time_created,
            s.time_updated,
            s.time_archived,
            p.name AS project_name,
            p.worktree AS project_worktree
        FROM session AS s
        LEFT JOIN project AS p
            ON p.id = s.project_id
        WHERE {where_clause}
        ORDER BY s.time_updated DESC, s.id ASC
    """
    rows = connection.execute(query, parameters).fetchall()
    return [
        SessionRecord(
            id=row["id"],
            project_id=row["project_id"],
            directory=row["directory"],
            title=row["title"],
            version=row["version"],
            summary_additions=row["summary_additions"],
            summary_deletions=row["summary_deletions"],
            summary_files=row["summary_files"],
            time_created=row["time_created"],
            time_updated=row["time_updated"],
            time_archived=row["time_archived"],
            project_name=row["project_name"],
            project_worktree=row["project_worktree"],
        )
        for row in rows
    ]


def safe_json_loads(raw: str | None) -> dict[str, Any] | None:
    if raw is None:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else {"value": value}


def load_messages(connection: sqlite3.Connection, session_id: str) -> list[MessageRecord]:
    query = """
        SELECT
            m.id AS message_id,
            m.time_created AS message_time_created,
            m.data AS message_data,
            p.id AS part_id,
            p.time_created AS part_time_created,
            p.data AS part_data
        FROM message AS m
        LEFT JOIN part AS p
            ON p.message_id = m.id
        WHERE m.session_id = ?
        ORDER BY m.time_created ASC, p.time_created ASC, p.id ASC
    """
    rows = connection.execute(query, (session_id,)).fetchall()
    messages: list[MessageRecord] = []
    current: MessageRecord | None = None

    for row in rows:
        message_id = row["message_id"]
        if current is None or current.id != message_id:
            payload = safe_json_loads(row["message_data"])
            current = MessageRecord(
                id=message_id,
                created_ms=row["message_time_created"],
                role=str((payload or {}).get("role") or "unknown"),
                model_id=(payload or {}).get("modelID"),
                provider_id=(payload or {}).get("providerID"),
                agent=(payload or {}).get("agent"),
                mode=(payload or {}).get("mode"),
                finish=(payload or {}).get("finish"),
                raw_data=row["message_data"],
                payload=payload,
            )
            messages.append(current)

        if row["part_id"] is None:
            continue

        part_payload = safe_json_loads(row["part_data"])
        current.parts.append(
            PartRecord(
                id=row["part_id"],
                created_ms=row["part_time_created"],
                type=str((part_payload or {}).get("type") or "unknown"),
                payload=part_payload,
                raw_data=row["part_data"],
            )
        )

    return messages


def should_include_part(
    part_type: str,
    include_part_types: set[str],
    exclude_part_types: set[str],
) -> bool:
    if include_part_types:
        return part_type in include_part_types
    return part_type not in exclude_part_types


def render_kv_lines(items: Iterable[tuple[str, str | None]]) -> list[str]:
    lines: list[str] = []
    for key, value in items:
        if value is None or value == "":
            continue
        lines.append(f"- {key}: {value}")
    return lines


def render_text_block(text: str) -> list[str]:
    stripped = text.strip()
    if not stripped:
        return ["_Empty text._", ""]
    return [stripped, ""]


def render_json_block(payload: dict[str, Any] | None, raw_data: str | None) -> list[str]:
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        body = raw_data or ""
    return ["```json", body, "```", ""]


def render_part(part: PartRecord, index: int) -> list[str]:
    lines = [f"#### Part {index} · `{part.type}`"]
    lines.extend(
        render_kv_lines(
            [
                ("Part ID", f"`{part.id}`" if part.id else None),
                ("Created", to_display_time(part.created_ms)),
            ]
        )
    )
    if lines[-1:] and lines[-1] != "":
        lines.append("")

    payload = part.payload or {}
    if part.type == "text":
        text = payload.get("text")
        if isinstance(text, str):
            lines.extend(render_text_block(text))
        else:
            lines.extend(render_json_block(part.payload, part.raw_data))
        return lines

    if part.type == "reasoning":
        text = payload.get("text")
        if isinstance(text, str):
            lines.extend(["```text", text.strip(), "```", ""])
        else:
            lines.extend(render_json_block(part.payload, part.raw_data))
        return lines

    if part.type == "tool":
        state = payload.get("state") if isinstance(payload.get("state"), dict) else {}
        summary_lines = render_kv_lines(
            [
                ("Tool", f"`{payload.get('tool')}`" if payload.get("tool") else None),
                (
                    "Status",
                    f"`{state.get('status')}`" if state.get("status") else None,
                ),
                ("Title", state.get("title")),
                ("Description", state.get("description")),
            ]
        )
        lines.extend(summary_lines)
        if summary_lines:
            lines.append("")
        lines.extend(render_json_block(part.payload, part.raw_data))
        return lines

    lines.extend(render_json_block(part.payload, part.raw_data))
    return lines


def render_message(
    message: MessageRecord,
    index: int,
    include_part_types: set[str],
    exclude_part_types: set[str],
) -> list[str]:
    lines = [f"### Message {index} · `{message.role}` · {to_display_time(message.created_ms)}"]
    lines.extend(
        render_kv_lines(
            [
                ("Message ID", f"`{message.id}`"),
                ("Model", f"`{message.model_id}`" if message.model_id else None),
                (
                    "Provider",
                    f"`{message.provider_id}`" if message.provider_id else None,
                ),
                ("Agent", f"`{message.agent}`" if message.agent else None),
                ("Mode", f"`{message.mode}`" if message.mode else None),
                ("Finish", f"`{message.finish}`" if message.finish else None),
            ]
        )
    )
    lines.append("")

    visible_parts = [
        part
        for part in message.parts
        if should_include_part(part.type, include_part_types, exclude_part_types)
    ]
    if not visible_parts:
        lines.append("_No exported parts for this message after part-type filtering._")
        lines.append("")
        return lines

    for part_index, part in enumerate(visible_parts, start=1):
        lines.extend(render_part(part, part_index))
    return lines


def session_project_label(session: SessionRecord) -> str:
    if session.project_name:
        return session.project_name.strip()
    if session.project_id == "global":
        return "global"
    for candidate in (session.project_worktree, session.directory):
        if not candidate:
            continue
        name = Path(candidate).name.strip()
        if name:
            return name
    return session.project_id or "unknown-project"


def filename_for_session(session: SessionRecord, filename_time_field: str) -> str:
    timestamp_ms = (
        session.time_created if filename_time_field == "created" else session.time_updated
    )
    title = sanitize_path_component(session.title, "untitled-session")
    time_text = to_filename_time(timestamp_ms)
    return f"{title}_{time_text}.md"


def output_path_for_session(
    output_root: Path,
    session: SessionRecord,
    group_by_project: bool,
    filename_time_field: str,
    overwrite: bool,
) -> Path:
    directory = output_root
    if group_by_project:
        project_dir = sanitize_path_component(
            session_project_label(session), "unknown-project"
        )
        directory = output_root / project_dir
    directory.mkdir(parents=True, exist_ok=True)

    filename = filename_for_session(session, filename_time_field)
    path = directory / filename
    if overwrite or not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    unique_path = directory / f"{stem}_{sanitize_path_component(session.id, session.id)}{suffix}"
    return unique_path


def render_session_markdown(
    session: SessionRecord,
    messages: Sequence[MessageRecord],
    include_part_types: set[str],
    exclude_part_types: set[str],
) -> str:
    visible_part_count = sum(
        1
        for message in messages
        for part in message.parts
        if should_include_part(part.type, include_part_types, exclude_part_types)
    )
    lines = [
        f"# {session.title}",
        "",
        *render_kv_lines(
            [
                ("Session ID", f"`{session.id}`"),
                ("Project", f"`{session_project_label(session)}`"),
                ("Project ID", f"`{session.project_id}`"),
                ("Project Worktree", f"`{session.project_worktree}`" if session.project_worktree else None),
                ("Directory", f"`{session.directory}`"),
                ("Version", f"`{session.version}`" if session.version else None),
                ("Created", to_display_time(session.time_created)),
                ("Updated", to_display_time(session.time_updated)),
                (
                    "Archived",
                    to_display_time(session.time_archived)
                    if session.time_archived is not None
                    else "null",
                ),
                (
                    "Summary",
                    f"+{session.summary_additions or 0} / -{session.summary_deletions or 0} / files {session.summary_files or 0}",
                ),
                ("Messages", str(len(messages))),
                ("Exported Parts", str(visible_part_count)),
            ]
        ),
        "",
        "## Transcript",
        "",
    ]

    if not messages:
        lines.extend(["_No messages found for this session._", ""])
        return "\n".join(lines)

    for index, message in enumerate(messages, start=1):
        lines.extend(
            render_message(message, index, include_part_types, exclude_part_types)
        )
    return "\n".join(lines).rstrip() + "\n"


def export_sessions(
    connection: sqlite3.Connection,
    sessions: Sequence[SessionRecord],
    output_dir: Path,
    args: argparse.Namespace,
) -> list[Path]:
    include_part_types = set(args.include_part_type)
    exclude_part_types = set(args.exclude_part_type)
    if not include_part_types:
        exclude_part_types |= DEFAULT_SKIPPED_PART_TYPES

    written_files: list[Path] = []
    for session in sessions:
        messages = load_messages(connection, session.id)
        markdown = render_session_markdown(
            session,
            messages,
            include_part_types,
            exclude_part_types,
        )
        target_path = output_path_for_session(
            output_root=output_dir,
            session=session,
            group_by_project=args.group_by_project,
            filename_time_field=args.filename_time_field,
            overwrite=args.overwrite,
        )
        target_path.write_text(markdown, encoding="utf-8")
        written_files.append(target_path)
    return written_files


def print_summary(
    sessions: Sequence[SessionRecord],
    written_files: Sequence[Path],
    output_dir: Path,
) -> None:
    print(f"Matched sessions: {len(sessions)}")
    print(f"Written files: {len(written_files)}")
    print(f"Output directory: {output_dir}")
    if written_files:
        print("Sample files:")
        for path in written_files[:5]:
            print(f"- {path}")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = resolve_db_path(args.db_path)

    with connect_db(db_path) as connection:
        sessions = load_sessions(connection, args)
        if not sessions:
            print("Matched sessions: 0")
            print("Nothing exported.")
            return
        written_files = export_sessions(connection, sessions, output_dir, args)

    print_summary(sessions, written_files, output_dir)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
