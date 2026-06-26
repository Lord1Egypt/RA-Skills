"""Tests for l3_confirm — L3 human confirmation flow."""

import json
import os
import pytest
from datetime import datetime

from l3_confirm import (
    create_confirmation,
    get_pending,
    get_status,
    _deadline_iso,
)


@pytest.fixture
def meta_path(tmp_path):
    p = str(tmp_path / "meta.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump({
            "version": "0.4.2",
            "memories": [],
            "conflicts": [],
            "security_rules": [],
            "entities": [],
            "l3_confirmations": [],
        }, f)
    return p


class TestCreateConfirmation:
    def test_creates_entry(self, meta_path):
        result = create_confirmation(meta_path, "ingest", {"content": "test"}, "test reason")
        assert result["status"] == "pending"
        assert result["action"] == "ingest"
        assert "sla_deadline" in result

    def test_persists(self, meta_path):
        create_confirmation(meta_path, "ingest", {"content": "test"})
        pending = get_pending(meta_path)
        assert len(pending) == 1


class TestGetPending:
    def test_empty(self, meta_path):
        assert get_pending(meta_path) == []

    def test_with_pending(self, meta_path):
        create_confirmation(meta_path, "ingest", {"content": "test"})
        pending = get_pending(meta_path)
        assert len(pending) == 1
        assert pending[0]["status"] == "pending"


class TestGetStatus:
    def test_empty(self, meta_path):
        status = get_status(meta_path)
        assert isinstance(status, dict)
        assert "total" in status
        assert status["total"] == 0


class TestDeadlineIso:
    def test_future_deadline(self):
        deadline = _deadline_iso(24)
        dt = datetime.fromisoformat(deadline)
        from mg_utils import CST
        assert dt > datetime.now(CST)

    def test_past_deadline(self):
        deadline = _deadline_iso(-1)
        dt = datetime.fromisoformat(deadline)
        from mg_utils import CST
        assert dt < datetime.now(CST)
