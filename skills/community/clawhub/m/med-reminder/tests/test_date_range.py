"""
PR 6 tests — per-med date ranges (start_date / end_date, local dates in
global.timezone; end inclusive).

Rows: schema/validate, add-med & edit-med acceptance (null clears, omission
preserves), tick enumeration bounds (effective start = max(active_since,
start_date); zero post-end phantom misses through normal ticks, catch-up
and watermark advance), and the one-time digest course-complete line.
"""
import datetime as dtmod
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import event_store
import safe_write as sw
from occurrence import at_local
from tests.conftest import local_dt, make_med, make_state, make_tick_env, TZ, utc

REPO = Path(__file__).parent.parent

MON = dtmod.date(2026, 4, 20)    # Mon
TUE = dtmod.date(2026, 4, 21)    # Tue
WED = MON + dtmod.timedelta(days=2)
FRI = MON + dtmod.timedelta(days=4)
SAT = MON + dtmod.timedelta(days=5)
NEXT_MON = MON + dtmod.timedelta(days=7)


def taken_on(day, at="08:10", hhmm="08:00"):
    """A taken event for the 08:00 occurrence on a local date."""
    return event_store.new_event("med-001", "taken", local_dt(*_hm(at), day=day.day),
                                 occurrence=at_local(day, hhmm, TZ, 0))


def _hm(hhmm):
    h, m = hhmm.split(":")
    return int(h), int(m)


# ── validate() (mirrors meds.schema.json) ────────────────────────────────────

def med_with(**extra):
    m = make_med(frequency="once_daily", times=["08:00"])
    m.update(extra)
    return m


def test_validate_accepts_date_range_and_equal_bounds():
    sw.validate(make_state(meds=[med_with(start_date="2026-04-20",
                                          end_date="2026-04-25")]))
    sw.validate(make_state(meds=[med_with(start_date="2026-04-20",
                                          end_date="2026-04-20")]))


def test_validate_accepts_null_and_absent_bounds():
    sw.validate(make_state(meds=[med_with(start_date=None, end_date=None)]))
    sw.validate(make_state(meds=[make_med()]))    # keys absent entirely


@pytest.mark.parametrize("bad", [
    "2026-04-1", "2026-4-01", "20260401", "2026/04/01", "04/01/2026",
    "2026-04-01T00:00:00Z", 20260401,
])
def test_validate_rejects_malformed_dates(bad):
    with pytest.raises(ValueError) as ei:
        sw.validate(make_state(meds=[med_with(start_date=bad)]))
    assert "start_date" in str(ei.value)


@pytest.mark.parametrize("bad", ["2026-02-30", "2026-04-31", "2026-13-01"])
def test_validate_rejects_impossible_calendar_dates(bad):
    with pytest.raises(ValueError) as ei:
        sw.validate(make_state(meds=[med_with(end_date=bad)]))
    assert "end_date" in str(ei.value)


def test_validate_rejects_end_before_start():
    with pytest.raises(ValueError) as ei:
        sw.validate(make_state(meds=[med_with(start_date="2026-04-25",
                                              end_date="2026-04-20")]))
    msg = str(ei.value)
    assert "end_date" in msg and "start_date" in msg and "on or after" in msg


def test_template_declares_nullable_date_fields():
    state = json.loads((REPO / "meds-state.template.json")
                       .read_text(encoding="utf-8"))
    med = state["meds"][0]
    assert med["start_date"] is None and med["end_date"] is None
    sw.validate(state)


# ── add-med / edit-med (CLI, exit-code conventions) ──────────────────────────

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

    return run, sf


def course_json(**extra):
    m = make_med(med_id="med-002", name="Azithro", frequency="once_daily",
                 times=["09:00"])
    m.update(extra)
    return json.dumps(m)


def test_add_med_accepts_date_range(cli_env):
    run, sf = cli_env
    r = run(["add-med", "--json", "-"], "2026-04-21T12:00:00-07:00",
            input_text=course_json(start_date="2026-04-22", end_date="2026-04-28"))
    assert r.returncode == 0 and "Added Azithro" in r.stdout
    med = json.loads(sf.read_text(encoding="utf-8"))["meds"][1]
    assert med["start_date"] == "2026-04-22"
    assert med["end_date"] == "2026-04-28"
    assert med["active_since_utc"]            # tracking anchor still set


def test_add_med_rejects_bad_date_and_inverted_range(cli_env):
    run, sf = cli_env
    r = run(["add-med", "--json", "-"], "2026-04-21T12:00:00-07:00",
            input_text=course_json(start_date="2026-04-22", end_date="not-a-date"))
    assert r.returncode == 2 and "end_date" in r.stdout
    r = run(["add-med", "--json", "-"], "2026-04-21T12:01:00-07:00",
            input_text=course_json(start_date="2026-04-28", end_date="2026-04-22"))
    assert r.returncode == 2 and "on or after" in r.stdout
    assert len(json.loads(sf.read_text(encoding="utf-8"))["meds"]) == 1


def test_edit_med_updates_clears_and_preserves_dates(cli_env):
    run, sf = cli_env
    r = run(["add-med", "--json", "-"], "2026-04-21T12:00:00-07:00",
            input_text=course_json(start_date="2026-04-22", end_date="2026-04-28"))
    assert r.returncode == 0

    # extend the end date
    r = run(["edit-med", "med-002", "--json", "-"], "2026-04-21T12:30:00-07:00",
            input_text=json.dumps({"end_date": "2026-04-30"}))
    assert r.returncode == 0
    med = json.loads(sf.read_text(encoding="utf-8"))["meds"][1]
    assert med["end_date"] == "2026-04-30" and med["start_date"] == "2026-04-22"

    # an edit that omits the fields keeps them
    r = run(["edit-med", "med-002", "--json", "-"], "2026-04-21T12:31:00-07:00",
            input_text=json.dumps({"dose": "250"}))
    assert r.returncode == 0
    med = json.loads(sf.read_text(encoding="utf-8"))["meds"][1]
    assert med["start_date"] == "2026-04-22" and med["end_date"] == "2026-04-30"

    # null clears both bounds
    r = run(["edit-med", "med-002", "--json", "-"], "2026-04-21T12:32:00-07:00",
            input_text=json.dumps({"start_date": None, "end_date": None}))
    assert r.returncode == 0
    med = json.loads(sf.read_text(encoding="utf-8"))["meds"][1]
    assert med["start_date"] is None and med["end_date"] is None

    # and a bad date still refuses with the field named
    r = run(["edit-med", "med-002", "--json", "-"], "2026-04-21T12:33:00-07:00",
            input_text=json.dumps({"end_date": "2026-02-30"}))
    assert r.returncode == 2 and "end_date" in r.stdout


# ── Tick enumeration ──────────────────────────────────────────────────────────

@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def once_daily(**kw):
    return make_med(frequency="once_daily", times=["08:00"], **kw)


def test_start_date_hides_occurrences_before_it(env):
    med = once_daily(start_date=WED.isoformat())       # starts Wednesday
    env.write(meds=[med])
    env.run(local_dt(7, 55))                           # Tuesday watermark
    env.run(local_dt(8, 5, day=22))                    # Wednesday 08:05
    # without start_date Tuesday's 08:00 dose would already be a stale miss
    assert env.sent_count("Reminder") == 1
    assert env.events("missed") == []
    assert env.sent_count("wasn't logged") == 0


def test_future_start_date_produces_no_events(env):
    env.write(meds=[once_daily(start_date=NEXT_MON.isoformat())])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    env.run(local_dt(8, 5, day=22))
    assert env.sent() == []
    assert env.events() == []      # not even a send intent
    assert env.heartbeat()["watermark_utc"] == utc(local_dt(8, 5, day=22)).isoformat()


def test_active_since_wins_when_later_than_start_date(env):
    med = once_daily(start_date=MON.isoformat())
    med["active_since_utc"] = utc(local_dt(7, 0, day=22)).isoformat()  # re-anchored
    env.write(meds=[med])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5, day=22))
    assert env.sent_count("Reminder") == 1     # Wednesday's dose only
    assert env.events("missed") == []          # Monday/Tuesday never enumerated


def test_end_date_day_still_fires(env):
    env.write(meds=[once_daily(end_date=TUE.isoformat())])  # last day Tuesday
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))                    # reminder on the last day
    assert env.sent_count("Reminder") == 1
    # it closes when the (out-of-course) next dose would arrive — missed
    # still fires for it, while Wednesday's dose itself is never enumerated
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))
    missed = env.events("missed")
    assert len(missed) == 1 and missed[0]["occurrence_key"] == "2026-04-21T08:00#0"


def test_after_end_date_no_reminders_nudges_or_misses(env):
    env.write(meds=[once_daily(end_date=TUE.isoformat())])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))                    # last-day reminder
    env.seed([taken_on(TUE)])                  # the last dose is confirmed
    for day in (22, 23, 24):
        env.run(local_dt(8, 5, day=day))       # would be reminder time
        env.run(local_dt(8, 40, day=day))      # would be nudge time
        env.run(local_dt(9, 40, day=day))      # would be missed time
    assert env.sent_count("Reminder") == 1     # only Tuesday's
    assert env.sent_count("Late:") == 0
    assert env.sent_count("Missed:") == 0
    assert env.events("missed") == []
    # the watermark is never pinned to a post-end occurrence
    assert env.heartbeat()["watermark_utc"] == utc(local_dt(9, 40, day=24)).isoformat()


def test_machine_off_spanning_end_date_zero_phantom_misses(env):
    env.write(meds=[once_daily(end_date=FRI.isoformat())])  # ends Friday
    env.run(local_dt(7, 55, day=24))           # Friday pre-dose tick
    env.run(local_dt(8, 5, day=24))            # Friday's last-day reminder
    env.seed([taken_on(FRI)])                  # the last dose is confirmed
    env.run(local_dt(8, 15, day=24))           # watermark advances — machine off
    sent_before = len(env.sent())
    env.run(local_dt(8, 0, day=27))            # Monday 08:00 — under the 72h cap
    assert env.events("missed") == []          # Sat/Sun/Mon doses never existed
    assert len(env.sent()) == sent_before      # nothing new for the med
    assert env.heartbeat()["watermark_utc"] == utc(local_dt(8, 0, day=27)).isoformat()


def test_capped_catchup_enumerates_only_up_to_end_date(env):
    env.write(meds=[once_daily(end_date=SAT.isoformat())])  # ends Saturday
    env.run(local_dt(12, 0, day=22))           # Wednesday — then off 5 days
    env.run(local_dt(12, 0, day=27))           # Monday — gap > 72h → capped
    missed = sorted(e["occurrence_key"] for e in env.events("missed"))
    assert missed == ["2026-04-25T08:00#0"]    # Saturday only; Sun/Mon dropped
    assert len([m for m in env.sent() if "Were you away?" in m]) == 1
    consolidated = [m for m in env.sent() if "wasn't logged" in m]
    assert len(consolidated) == 1 and consolidated[0].count("Metformin") == 1


def test_interval_med_anchors_at_future_start_date(env):
    med = make_med(frequency="interval", interval_hours=8,
                   start_date=WED.isoformat())
    med["active_since_utc"] = utc(local_dt(12, 0)).isoformat()
    env.write(meds=[med])
    env.run(local_dt(10, 0))                   # Tuesday: nothing due yet
    assert env.sent() == []
    # Wednesday midnight is inside quiet hours → the anchor shifts to 07:00
    assert env.med_state()["next_due"] == utc(local_dt(7, 0, day=22)).isoformat()
    env.run(local_dt(7, 5, day=22))
    assert env.sent_count("Reminder") == 1


# ── Digest ────────────────────────────────────────────────────────────────────

def digest_msgs(env):
    return [m for m in env.sent() if "Meds for" in m]


def test_digest_announces_course_complete_once(env):
    env.write(meds=[once_daily(end_date=MON.isoformat())], digest_time="07:30")
    env.run(local_dt(7, 0, day=20))            # Monday — end day, still listed
    env.run(local_dt(7, 32, day=20))
    assert len(digest_msgs(env)) == 1
    assert "Metformin 500mg |" in digest_msgs(env)[0]
    assert env.state()["global"]["last_digest_order"] == ["med-001"]

    env.run(local_dt(7, 32, day=21))           # Tuesday: course over
    msg = digest_msgs(env)[1]
    assert "Course complete: Metformin" in msg
    assert "Mon Apr 20" in msg
    assert "Metformin 500mg |" not in msg      # dropped from the listing
    assert env.state()["global"]["last_digest_order"] == []

    env.run(local_dt(7, 32, day=22))           # Wednesday: note already delivered
    assert len(digest_msgs(env)) == 2          # no third digest


def test_course_note_survives_a_missed_digest_day(env):
    env.write(meds=[once_daily(end_date=MON.isoformat())], digest_time="07:30")
    env.run(local_dt(7, 0, day=20))            # Monday pre-digest, then off all day
    env.run(local_dt(12, 0, day=21))           # Tuesday noon — >4h late, no digest
    assert digest_msgs(env) == []
    env.run(local_dt(7, 32, day=22))           # Wednesday's digest carries the note
    assert len(digest_msgs(env)) == 1
    assert "Course complete: Metformin" in digest_msgs(env)[0]


def test_digest_omits_meds_that_have_not_started(env):
    env.write(meds=[once_daily(start_date=NEXT_MON.isoformat())],
              digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    assert env.sent() == []                    # nothing to list, nothing to announce
    assert "last_digest_order" not in env.state()["global"]
