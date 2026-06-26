"""Pytest configuration for PVM tests."""

import sys
import uuid
from pathlib import Path

import pytest

# Ensure src/ is on the path so `from pvm.models import ...` works
_root = Path(__file__).parent.parent
sys.path.insert(0, str(_root / "src"))

from pvm.vault import Vault


@pytest.fixture
def vault():
    """Each test gets its own in-memory vault for complete isolation."""
    # Use a UUID-keyed in-memory database — each call gets a fresh DB
    db_uri = f"file:{uuid.uuid4().hex}?mode=memory&cache=shared"
    return Vault(db_uri, uri=True)
