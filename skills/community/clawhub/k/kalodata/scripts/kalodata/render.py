"""Stdout rendering helpers: TOON blocks, help hints, structured errors, empty states."""

from __future__ import annotations

from . import toon


def out(text: str = "") -> None:
    print(text)


def emit_help(lines: list[str]) -> None:
    lines = [ln for ln in lines if ln]
    if not lines:
        return
    if len(lines) == 1:
        out(f"help[1]: {lines[0]}")
        return
    out(f"help[{len(lines)}]:")
    for ln in lines:
        out(f"  {ln}")


def emit_error(message: str, help_lines: list[str] | None = None) -> None:
    out(f"error: {message}")
    emit_help(help_lines or [])


def emit_empty(noun: str, context: str, help_lines: list[str] | None = None) -> None:
    out(f"{noun}: 0 results ({context})")
    emit_help(help_lines or [])


def emit_table(noun: str, rows: list[dict], fields) -> None:
    out(toon.tabular(noun, rows, list(fields)))


def emit_detail(noun: str, data: dict) -> None:
    out(toon.kv(noun, data))


def clip(value, limit: int = 48):
    if isinstance(value, str) and len(value) > limit:
        return value[: limit - 1] + "…"
    return value


def truncate_text(d: dict, key: str, limit: int, full: bool, notes: list[str], escape: str) -> None:
    """Truncate a long text field in place, recording a `--full` escape-hatch note."""
    v = d.get(key)
    if not full and isinstance(v, str) and len(v) > limit:
        d[key] = v[:limit] + f"... (truncated, {len(v)} chars total)"
        notes.append(escape)
