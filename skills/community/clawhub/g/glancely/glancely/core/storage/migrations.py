"""Per-component SQL migration runner.

Each component owns `skills/<name>/migrations/*.sql`. Files are applied in
lexicographic order. Applied state is tracked in `_migrations`, keyed by
(component, name). Re-running is a no-op.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from .db import get_connection

_BOOTSTRAP_SQL = """
CREATE TABLE IF NOT EXISTS _migrations (
    component  TEXT NOT NULL,
    name       TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (component, name)
);
"""


def _bootstrap(conn: sqlite3.Connection) -> None:
    conn.executescript(_BOOTSTRAP_SQL)
    conn.commit()


def _applied(conn: sqlite3.Connection, component: str) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM _migrations WHERE component = ?",
        (component,),
    ).fetchall()
    return {row["name"] for row in rows}


def _migration_files(migrations_dir: Path) -> list[Path]:
    if not migrations_dir.is_dir():
        return []
    return sorted(p for p in migrations_dir.glob("*.sql") if p.is_file())


def apply_component_migrations(component: str, migrations_dir: Path, conn: sqlite3.Connection | None = None) -> list[str]:
    """Apply all unapplied migrations for one component. Returns names applied."""
    own_conn = conn is None
    conn = conn or get_connection()
    try:
        _bootstrap(conn)
        already = _applied(conn, component)
        applied: list[str] = []
        for path in _migration_files(migrations_dir):
            if path.name in already:
                continue
            sql = path.read_text(encoding="utf-8")
            try:
                conn.executescript(sql)
                conn.execute(
                    "INSERT INTO _migrations (component, name) VALUES (?, ?)",
                    (component, path.name),
                )
                conn.commit()
                applied.append(path.name)
            except sqlite3.Error as exc:
                conn.rollback()
                raise RuntimeError(f"Migration {component}/{path.name} failed: {exc}") from exc
        return applied
    finally:
        if own_conn:
            conn.close()


def apply_all_migrations(skills_root: Path, user_root: Path | None = None) -> dict[str, list[str]]:
    """Apply migrations from both the skill-internal and user component dirs."""
    if user_root is None:
        user_root = Path(os.environ.get("GLANCE_HOME", Path.home() / ".glancely")) / "components"

    results: dict[str, list[str]] = {}
    roots = [skills_root, user_root] if user_root.is_dir() else [skills_root]
    for root in roots:
        # Support passing a single component directory directly.
        if (root / "component.toml").is_file():
            applied = apply_component_migrations(root.name, root / "migrations")
            if applied:
                results[root.name] = applied
        for child in sorted(p for p in root.iterdir() if p.is_dir()):
            if (child / "component.toml").is_file():
                applied = apply_component_migrations(child.name, child / "migrations")
                if applied:
                    results[child.name] = applied
    return results


if __name__ == "__main__":
    import json
    import sys

    skills_root = Path(__file__).resolve().parents[2] / "skills"
    if len(sys.argv) > 1:
        skills_root = Path(sys.argv[1]).resolve()
    print(json.dumps(apply_all_migrations(skills_root), indent=2))
