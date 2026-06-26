"""migrations: idempotency + per-component tracking."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import apply_all_migrations, get_connection


def _set_home(tmp):
    os.environ["GLANCE_HOME"] = tmp


def test_apply_creates_tables():
    with tempfile.TemporaryDirectory() as tmp:
        _set_home(tmp)
        applied = apply_all_migrations(REPO_ROOT / "glancely" / "examples")
        assert "mood" in applied and "reminder" in applied and "mit" in applied and "diary_logger" in applied
        with get_connection() as conn:
            tables = {r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
        assert "_migrations" in tables
        assert "mood_entries" in tables
        assert "reminders" in tables
        assert "mit_entries" in tables


def test_idempotent():
    with tempfile.TemporaryDirectory() as tmp:
        _set_home(tmp)
        first = apply_all_migrations(REPO_ROOT / "glancely" / "examples")
        second = apply_all_migrations(REPO_ROOT / "glancely" / "examples")
        assert first  # something happened the first time
        assert second == {}  # nothing the second time


if __name__ == "__main__":
    test_apply_creates_tables()
    test_idempotent()
    print("ok")
