"""
Passport generator tests — generate-passport.py

Verifies HTML output contains correct med data, excludes paused meds,
handles edge cases (no meds, all paused, as_needed).
"""
import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import importlib, sys
_mod = importlib.util.spec_from_file_location(
    "generate_passport",
    Path(__file__).parent.parent / "generate-passport.py"
)
_gp = importlib.util.module_from_spec(_mod)
_mod.loader.exec_module(_gp)
build_html = _gp.build_html
from tests.conftest import make_state, make_med


def html_for(meds, name="", dob=""):
    state = make_state(meds=meds)
    return build_html(state, name, dob)


# ── Active meds appear ────────────────────────────────────────────────────────

def test_active_med_name_in_output():
    med = make_med(name="Metformin")
    h   = html_for([med])
    assert "Metformin" in h


def test_active_med_dose_in_output():
    med = make_med(dose="500", unit="mg")
    h   = html_for([med])
    assert "500mg" in h


# ── Paused meds excluded ──────────────────────────────────────────────────────

def test_paused_med_excluded():
    active = make_med(med_id="med-001", name="Metformin", paused=False)
    paused = make_med(med_id="med-002", name="Lisinopril", paused=True)
    h      = html_for([active, paused])
    assert "Metformin"  in h
    assert "Lisinopril" not in h


def test_paused_count_warning_shown():
    paused = make_med(med_id="med-001", name="Metformin", paused=True)
    h      = html_for([paused])
    assert "paused" in h.lower()


# ── Patient name and DOB ──────────────────────────────────────────────────────

def test_patient_name_in_header():
    med = make_med()
    h   = html_for([med], name="Jane Smith")
    assert "Jane Smith" in h


def test_dob_in_header():
    med = make_med()
    h   = html_for([med], name="Jane Smith", dob="1975-03-12")
    assert "1975-03-12" in h


def test_no_name_still_valid_html():
    med = make_med()
    h   = html_for([med], name="")
    assert "<!DOCTYPE html>" in h
    assert "Metformin" in h


# ── Schedule formatting ───────────────────────────────────────────────────────

def test_once_daily_schedule_shown():
    med = make_med(frequency="once_daily", times=["08:00"])
    h   = html_for([med])
    assert "Once daily" in h
    assert "8:00am" in h


def test_twice_daily_schedule_shown():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    h   = html_for([med])
    assert "Twice daily" in h
    assert "8:00am" in h
    assert "8:00pm" in h


def test_interval_schedule_shown():
    med = make_med(frequency="interval", interval_hours=6)
    h   = html_for([med])
    assert "Every 6h" in h


def test_as_needed_shown_as_active():
    med = make_med(frequency="as_needed")
    h   = html_for([med])
    assert "As needed" in h
    assert "Metformin" in h


# ── With food ─────────────────────────────────────────────────────────────────

def test_with_food_checkmark_present():
    med = make_med(with_food=True)
    h   = html_for([med])
    assert "&#10003;" in h or "✓" in h


# ── Notes ─────────────────────────────────────────────────────────────────────

def test_notes_appear():
    med = make_med(notes="Take with full glass of water")
    h   = html_for([med])
    assert "Take with full glass of water" in h


# ── Empty states ──────────────────────────────────────────────────────────────

def test_no_meds_shows_empty_message():
    h = html_for([])
    assert "No active medications" in h


def test_all_paused_shows_empty_and_warning():
    med = make_med(paused=True)
    h   = html_for([med])
    assert "No active medications" in h
    assert "paused" in h.lower()


# ── XSS: user content is escaped ─────────────────────────────────────────────

def test_xss_in_med_name_is_escaped():
    med = make_med(name='<script>alert("xss")</script>')
    h   = html_for([med])
    assert "<script>" not in h
    assert "&lt;script&gt;" in h


def test_xss_in_patient_name_is_escaped():
    med = make_med()
    h   = html_for([med], name='<img src=x onerror=alert(1)>')
    assert "<img" not in h


# ── generate-passport.py CLI integration ─────────────────────────────────────

def test_cli_writes_file(tmp_path):
    import subprocess, os
    state = {
        "version": "1",
        "global": {
            "timezone": "America/Los_Angeles",
            "quiet_hours": {"start": "22:00", "end": "07:00"},
            "paused": False,
            "digest_time": "08:00",
            "delivery_channel": "whatsapp",
        },
        "meds": [{
            "id": "med-001",
            "name": "Aspirin",
            "type": "pill",
            "dose": "81",
            "unit": "mg",
            "paused": False,
            "schedule": {"frequency": "once_daily", "times": ["08:00"],
                         "with_food": False, "notes": ""},
            "escalation": {"late_threshold_minutes": 30, "missed_threshold_minutes": 90,
                           "late_message": "x", "missed_message": "y"},
            "state": {"status": "pending", "last_taken": None, "last_reminded": None,
                      "next_due": None, "missed_count": 0, "history": []},
        }],
    }
    state_file   = tmp_path / "meds-state.json"
    out_file     = tmp_path / "passport.html"
    state_file.write_text(json.dumps(state))

    env = os.environ.copy()
    env["MEDS_STATE_FILE"] = str(state_file)

    script = Path(__file__).parent.parent / "generate-passport.py"
    result = subprocess.run(
        [sys.executable, str(script), "--name", "Test Patient",
         "--out", str(out_file), "--no-prompt"],
        capture_output=True, text=True, env=env,
    )
    assert result.returncode == 0, result.stderr
    assert out_file.exists()
    content = out_file.read_text()
    assert "Aspirin" in content
    assert "Test Patient" in content
