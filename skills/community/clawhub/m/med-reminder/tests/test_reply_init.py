"""
`reply.py init` (#10): first-run state creation without the agent composing
JSON — global answers only, refuses to overwrite an existing file.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import dispatch
import safe_write as sw
from reply import handle_init

REPO = Path(__file__).parent.parent


@pytest.fixture
def state_file(tmp_path, monkeypatch):
    sf = tmp_path / "meds-state.json"
    monkeypatch.setattr(sw, "STATE_FILE", sf)
    monkeypatch.setattr(sw, "LOG_FILE", tmp_path / "sw.log")
    monkeypatch.setattr(dispatch, "STATE_FILE", sf)
    return sf


def test_init_creates_a_valid_empty_state(state_file, capsys):
    handle_init("America/Chicago", "23:00", "06:30", None, "telegram", dry_run=False)
    state = json.loads(state_file.read_text(encoding="utf-8"))
    sw.validate(state)
    assert state["meds"] == []
    g = state["global"]
    assert g["timezone"] == "America/Chicago"
    assert g["quiet_hours"] == {"start": "23:00", "end": "06:30"}
    assert g["digest_time"] == "07:00"            # wake + 30
    assert g["delivery_channel"] == "telegram" and g["paused"] is False
    assert "Add meds with add-med" in capsys.readouterr().out


def test_init_explicit_digest_time(state_file):
    handle_init("America/Chicago", "23:00", "06:30", "09:15", "sms", dry_run=False)
    assert json.loads(state_file.read_text(encoding="utf-8"))["global"]["digest_time"] == "09:15"


def test_digest_default_pulled_out_of_quiet_hours(state_file):
    # quiet 07:20–07:00 (asleep almost all day): wake+30 = 07:30 is quiet again
    handle_init("America/Chicago", "07:20", "07:00", None, "sms", dry_run=False)
    assert json.loads(state_file.read_text(encoding="utf-8"))["global"]["digest_time"] == "07:15"


def test_init_refuses_an_existing_file(state_file, capsys):
    state_file.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        handle_init("America/Chicago", "23:00", "06:30", None, "telegram", dry_run=False)
    assert "already exists" in capsys.readouterr().out
    assert state_file.read_text(encoding="utf-8") == "{}"


@pytest.mark.parametrize("args", [
    ("Mars/Olympus", "23:00", "06:30", None, "telegram"),
    ("America/Chicago", "11pm", "06:30", None, "telegram"),
    ("America/Chicago", "23:00", "6:30", None, "telegram"),
    ("America/Chicago", "23:00", "06:30", "25:00", "telegram"),
    ("America/Chicago", "23:00", "06:30", None, "  "),
])
def test_init_rejects_bad_input(state_file, args):
    with pytest.raises(SystemExit):
        handle_init(*args, dry_run=False)
    assert not state_file.exists()


def test_init_dry_run_writes_nothing(state_file, capsys):
    handle_init("America/Chicago", "23:00", "06:30", None, "telegram", dry_run=True)
    assert "[DRY RUN]" in capsys.readouterr().out
    assert not state_file.exists()


def test_init_cli_then_add_med(tmp_path):
    sf = tmp_path / "meds-state.json"
    env = dict(os.environ, MEDS_TEST="1", MEDS_LOG_FILE=str(tmp_path / "r.log"),
               MEDS_HISTORY_FILE=str(tmp_path / "h.jsonl"),
               MEDS_FAKE_NOW="2026-04-21T09:00:00-07:00")

    def run(args, stdin=None):
        return subprocess.run([sys.executable, str(REPO / "reply.py"), "--state", str(sf)]
                              + args, input=stdin, capture_output=True, text=True,
                              timeout=60, cwd=str(REPO), env=env)

    r = run(["init", "--timezone", "America/Los_Angeles", "--quiet-start", "22:00",
             "--quiet-end", "07:00", "--channel", "telegram"])
    assert r.returncode == 0, r.stdout + r.stderr
    med = {"name": "Metformin", "type": "pill", "dose": "500", "unit": "mg",
           "paused": False,
           "schedule": {"frequency": "once_daily", "times": ["08:00"]},
           "escalation": {"late_threshold_minutes": 30, "missed_threshold_minutes": 90,
                          "late_message": "Late {name}", "missed_message": "Missed {name}"}}
    r = run(["add-med", "--json", "-"], json.dumps(med))
    assert r.returncode == 0, r.stdout + r.stderr
    assert json.loads(sf.read_text(encoding="utf-8"))["meds"][0]["id"] == "med-001"
