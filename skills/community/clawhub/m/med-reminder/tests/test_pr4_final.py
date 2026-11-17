"""
PR 4 final integration tests — the reply commands as one system with the
tick (issue #1 §6): command → event store → tick stages round-trips, the
CLI end-to-end in a subprocess (MEDS_FAKE_NOW per the testing plan), and
the `deferred` read-forever/never-written rule.
"""
import json
import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import pytest

import dispatch
import event_store
import safe_write as sw
from clock import FakeClock, parse_instant
from reply import handle_confirm, handle_snooze, handle_undo
from tests.conftest import local_dt, make_med, make_state, make_tick_env, utc

REPO = Path(__file__).parent.parent


# ── CLI end-to-end (subprocess, MEDS_FAKE_NOW per the testing plan) ───────────

@pytest.fixture
def cli_env(tmp_path):
    sf = tmp_path / "meds-state.json"
    sf.write_text(json.dumps(make_state(
        digest_time="23:59",
        meds=[make_med(med_id="med-001", frequency="once_daily", times=["08:00"])])),
        encoding="utf-8")

    env = dict(os.environ)
    env.update({
        "MEDS_TEST": "1",
        "MEDS_LOG_FILE": str(tmp_path / "reply.log"),
        "MEDS_HISTORY_FILE": str(tmp_path / "history.jsonl"),
    })

    def run(args, fake_now, input_text=None):
        env["MEDS_FAKE_NOW"] = fake_now
        return subprocess.run(
            [sys.executable, str(REPO / "reply.py"), "--state", str(sf)] + args,
            input=input_text, capture_output=True, text=True, timeout=60,
            cwd=str(REPO), env=env)

    return run, sf, tmp_path / "history.jsonl"


def test_cli_full_command_flow(cli_env):
    run, sf, hist = cli_env

    def T(hm):
        return f"2026-04-21T{hm}:00-07:00"

    r = run(["confirm", "med-001"], T("08:10"))
    assert r.returncode == 0 and "Logged as your 8:00am dose." in r.stdout

    r = run(["undo", "med-001"], T("08:12"))
    assert r.returncode == 0 and "Undid" in r.stdout

    r = run(["snooze", "med-001", "--minutes", "15"], T("08:13"))
    assert r.returncode == 0 and "Snoozed" in r.stdout

    r = run(["skip", "med-001"], T("08:14"))
    assert r.returncode == 0 and "Skipped" in r.stdout

    r = run(["undo", "med-001"], T("08:16"))
    assert r.returncode == 0 and "Undid: skipped" in r.stdout

    r = run(["status"], T("08:20"))
    assert r.returncode == 0 and "Metformin" in r.stdout

    r = run(["show-state"], T("08:21"))
    assert r.returncode == 0 and len(r.stdout.strip().splitlines()) == 1

    r = run(["pause", "med-001"], T("08:22"))
    assert r.returncode == 0
    r = run(["unpause", "med-001"], T("08:23"))
    assert r.returncode == 0

    r = run(["remove", "med-001", "--yes"], T("08:24"))
    assert r.returncode == 0
    assert json.loads(sf.read_text(encoding="utf-8"))["meds"] == []
    # history lines remain after the removal
    events = event_store.load_events(hist)
    assert {e["event"] for e in events} == {"taken", "undone", "snoozed", "skipped"}
    assert len(events) == 5


def test_cli_add_med_reads_stdin_and_rejects_quiet_conflict(cli_env):
    run, sf, _ = cli_env
    good = json.dumps(make_med(med_id="med-002", name="Vitamin D",
                               frequency="once_daily", times=["09:00"]))
    bad = json.dumps(make_med(med_id="med-003", name="Night Med",
                              frequency="once_daily", times=["23:00"]))

    r = run(["add-med", "--json", "-"], "2026-04-21T12:00:00-07:00", input_text=good)
    assert r.returncode == 0 and "Added Vitamin D" in r.stdout

    r = run(["add-med", "--json", "-"], "2026-04-21T12:01:00-07:00", input_text=bad)
    assert r.returncode != 0 and "inside quiet hours" in r.stdout
    assert len(json.loads(sf.read_text(encoding="utf-8"))["meds"]) == 2


def test_cli_position_and_digest_order(cli_env):
    run, sf, _ = cli_env
    state = json.loads((sf).read_text(encoding="utf-8"))
    state["global"]["last_digest_order"] = ["med-001"]
    state["global"]["last_digest_date"] = "2026-04-21"
    sf.write_text(json.dumps(state), encoding="utf-8")

    r = run(["confirm", "--position", "1"], "2026-04-21T08:10:00-07:00")
    assert r.returncode == 0
    assert "Position 1: Metformin (med-001)." in r.stdout

    # yesterday's order is refused
    state["global"]["last_digest_date"] = "2026-04-20"
    sf.write_text(json.dumps(state), encoding="utf-8")
    r = run(["skip", "--position", "1"], "2026-04-21T09:00:00-07:00")
    assert r.returncode != 0 and "no digest order for today" in r.stdout


# ── command → store → tick round-trips ────────────────────────────────────────

def test_snooze_confirm_loop_with_tick(tmp_path, monkeypatch):
    """reminder → snooze → snooze reminder → confirm → everything goes quiet."""
    env = make_tick_env(tmp_path, monkeypatch)
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])])
    monkeypatch.setattr(dispatch, "STATE_FILE", env.state_file)
    monkeypatch.setattr(sw, "STATE_FILE", env.state_file)

    env.run(local_dt(7, 55))                 # watermark init
    env.run(local_dt(8, 1))                  # the reminder
    handle_snooze("med-001", 30, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    env.run(local_dt(8, 36))                 # the snoozed reminder
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 40)))

    for t in ((8, 45), (9, 15), (10, 0)):
        env.run(local_dt(*t))

    assert env.sent_count("Reminder:") == 1   # 'Reminder (snoozed)' excluded
    assert env.sent_count("snoozed") == 1
    assert env.sent_count("Late:") == 0 and env.sent_count("Missed:") == 0
    assert env.events("missed") == []
    assert len(env.sent()) == 2              # nothing else was ever sent


def test_digest_position_undo_re_remind(tmp_path, monkeypatch):
    env = make_tick_env(tmp_path, monkeypatch)
    m1 = make_med(med_id="med-001", name="Metformin", times=["08:00"])
    m2 = make_med(med_id="med-002", name="Lisinopril", times=["21:00"])
    env.write(meds=[m1, m2], digest_time="07:30")
    monkeypatch.setattr(dispatch, "STATE_FILE", env.state_file)
    monkeypatch.setattr(sw, "STATE_FILE", env.state_file)

    env.run(local_dt(7, 35))                 # the digest lists both meds
    assert env.state()["global"]["last_digest_order"] == ["med-001", "med-002"]

    handle_confirm(None, None, dry_run=False, clock=FakeClock(local_dt(8, 10)),
                   position=1)
    handle_undo(None, dry_run=False, clock=FakeClock(local_dt(8, 15)), position=1)
    env.run(local_dt(8, 20))                 # re-reminded, new generation

    assert env.sent_count("Reminder") == 1
    assert env.events("send_intent")[-1]["generation"] == 1
    taken = [e for e in env.events() if e["event"] == "taken"]
    assert len(taken) == 1 and taken[0]["med_id"] == "med-001"


def test_double_dose_warning_after_command_confirm(tmp_path, monkeypatch):
    """AC 22 through the real command: a late same-day confirm (inside the
    12h min-gap before the next dose) puts the warning on tomorrow's
    reminder."""
    env = make_tick_env(tmp_path, monkeypatch)
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])])
    monkeypatch.setattr(dispatch, "STATE_FILE", env.state_file)
    monkeypatch.setattr(sw, "STATE_FILE", env.state_file)

    env.run(local_dt(7, 55))
    env.run(local_dt(8, 1))                 # day 1's plain reminder
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(21, 0)))
    env.run(local_dt(21, 5))
    env.run(local_dt(8, 1) + timedelta(days=1))    # day 2's reminder

    msgs = env.sent()
    assert "You logged Metformin" not in msgs[0]      # day 1: clean
    assert "You logged Metformin yesterday at 9:00pm" in msgs[-1]
    assert "Don't take another" in msgs[-1]


# ── `deferred` stays readable forever, and is never written (issue §1) ────────

def test_legacy_deferred_state_stays_readable_and_unwritten(tmp_path, monkeypatch,
                                                             capsys):
    from reply import handle_pause

    sf = tmp_path / "meds-state.json"
    med = make_med(med_id="med-001", status="deferred", times=["08:00"])
    med["state"]["history"].append({
        "timestamp": utc(local_dt(6, 0)).isoformat(),
        "event": "deferred",
        "dose_prescribed": "500mg",
    })
    sf.write_text(json.dumps(make_state(meds=[med])), encoding="utf-8")
    monkeypatch.setattr(dispatch, "STATE_FILE", sf)
    monkeypatch.setattr(sw, "STATE_FILE", sf)
    monkeypatch.setattr(sw, "LOG_FILE", tmp_path / "sw.log")

    # the legacy state loads and a PR 4 command works on top of it
    handle_pause("med-001", dry_run=False, clock=FakeClock(local_dt(12, 0)))
    assert "Paused" in capsys.readouterr().out
    on_disk = json.loads(sf.read_text(encoding="utf-8"))
    assert on_disk["meds"][0]["state"]["history"][-1]["event"] == "deferred"

    # no command writes `deferred` — the store vocabulary rejects it outright
    with pytest.raises(ValueError):
        event_store.new_event("med-001", "deferred", local_dt(12, 0))
    store_events = event_store.load_events(sw.history_file())
    assert all(e.get("event") != "deferred" for e in store_events)
