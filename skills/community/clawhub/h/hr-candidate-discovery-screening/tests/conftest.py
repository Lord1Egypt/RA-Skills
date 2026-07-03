from __future__ import annotations

import sys
from pathlib import Path

import pytest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def initialized_database(tmp_path):
    from db import Database

    database = Database(tmp_path / "recruitment.db")
    database.initialize()
    return database
