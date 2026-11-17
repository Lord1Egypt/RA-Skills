"""Shared fixtures for med reminder tests."""
import json
import sys
from pathlib import Path

# Make dispatch importable without installing
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Los_Angeles")


def make_state(paused=False, quiet_start="22:00", quiet_end="07:00",
               digest_time="08:00", meds=None):
    return {
        "version": "1",
        "global": {
            "timezone": "America/Los_Angeles",
            "quiet_hours": {"start": quiet_start, "end": quiet_end},
            "paused": paused,
            "digest_time": digest_time,
            "delivery_channel": "whatsapp",
        },
        "meds": meds if meds is not None else [],
    }


def make_med(
    med_id="med-001",
    name="Metformin",
    med_type="pill",
    dose="500",
    unit="mg",
    paused=False,
    frequency="once_daily",
    times=None,
    interval_hours=None,
    day_of_week=None,
    with_food=False,
    notes="",
    late_threshold=30,
    missed_threshold=90,
    status="pending",
    last_taken=None,
    last_reminded=None,
    next_due=None,
    confirmed_dose=None,
    missed_count=0,
    history=None,
    include_confirmed_dose=True,
    start_date=None,
    end_date=None,
):
    sched = {"frequency": frequency, "with_food": with_food, "notes": notes}
    if frequency == "interval":
        sched["interval_hours"] = interval_hours
    elif frequency != "as_needed":
        sched["times"] = times if times is not None else ["08:00"]
        if frequency == "weekly" and day_of_week is not None:
            sched["day_of_week"] = day_of_week

    return {
        "id": med_id,
        "name": name,
        "type": med_type,
        "dose": dose,
        "unit": unit,
        "paused": paused,
        "schedule": sched,
        "escalation": {
            "late_threshold_minutes": late_threshold,
            "missed_threshold_minutes": missed_threshold,
            "late_message": "Late: {name} {dose}{unit}",
            "missed_message": "Missed: {name} {dose}{unit}",
        },
        "state": {
            "status": status,
            "last_taken": last_taken,
            "last_reminded": last_reminded,
            "next_due": next_due,
            "missed_count": missed_count,
            "history": history if history is not None else [],
            # include_confirmed_dose=False builds a legacy state block (pre-per-dose files)
            **({"confirmed_dose": confirmed_dose} if include_confirmed_dose else {}),
        },
        # optional per-med calendar bounds (PR 6) — present only when set
        **({"start_date": start_date} if start_date is not None else {}),
        **({"end_date": end_date} if end_date is not None else {}),
    }


def local_dt(hour, minute=0, second=0, tz=TZ,
             year=2026, month=4, day=21):
    """Build a timezone-aware datetime in TZ."""
    return datetime(year, month, day, hour, minute, second, tzinfo=tz)


# ── Tick engine fixture (issue #1 PR 2) ───────────────────────────────────────

def make_tick_env(tmp_path, monkeypatch):
    """
    Wire a real state file + the fake sender into dispatch/safe_write.

    Returns a small helper object: write(state), run(now), sent(), events(),
    state(), plus sender switches (fail/heal/sleep). `run` normalizes `now`
    to UTC — pass aware datetimes in any timezone.
    """
    import dispatch
    import event_store
    import safe_write as sw
    import tick
    from clock import FakeClock

    sf = tmp_path / "meds-state.json"
    monkeypatch.setattr(sw, "STATE_FILE", sf)
    monkeypatch.setattr(sw, "LOG_FILE", tmp_path / "sw.log")
    monkeypatch.setattr(dispatch, "STATE_FILE", sf)
    monkeypatch.setattr(dispatch, "LOG_FILE", tmp_path / "dispatch.log")

    out = tmp_path / "sent.txt"
    fail_flag = tmp_path / "sender-fail"
    sleep_flag = tmp_path / "sender-sleep"
    monkeypatch.setattr(
        dispatch, "SEND_CMD",
        f'"{sys.executable}" "{Path(__file__).parent / "fake_sender.py"}"')
    monkeypatch.setenv("FAKE_SEND_OUT", str(out))
    monkeypatch.setenv("FAKE_SEND_FAIL", str(fail_flag))
    fail_match = tmp_path / "sender-fail-match"
    monkeypatch.setenv("FAKE_SEND_FAIL_MATCH", str(fail_match))
    monkeypatch.setenv("FAKE_SEND_SLEEP", str(sleep_flag))

    class Env:
        state_file = sf
        sent_file = out

        def write(self, meds=None, digest_time="01:37", **kw):
            # digest_time parked outside test hours by default so digest
            # messages don't pollute stage assertions; digest tests override
            sf.write_text(json.dumps(make_state(meds=meds if meds is not None else [],
                                                digest_time=digest_time, **kw)),
                          encoding="utf-8")

        def run(self, now, tick_minutes=5, dry_run=False):
            return tick.run_tick(dry_run=dry_run, clock=FakeClock(now),
                                 tick_minutes=tick_minutes)

        def sent(self):
            if not out.exists():
                return []
            return [m for m in out.read_text(encoding="utf-8").split("\n---\n") if m]

        def sent_count(self, needle=None):
            msgs = self.sent()
            return len(msgs) if needle is None else sum(1 for m in msgs if needle in m)

        def events(self, kind=None):
            evs = event_store.load_events(sw.history_file())
            return [e for e in evs if e.get("event") == kind] if kind else evs

        def seed(self, events):
            event_store.append_events(sw.history_file(), events)

        def state(self):
            return json.loads(sf.read_text(encoding="utf-8"))

        def med_state(self, i=0):
            return self.state()["meds"][i]["state"]

        def heartbeat(self):
            return json.loads((tmp_path / "tick-heartbeat.json").read_text(encoding="utf-8"))

        def fail_sends(self):
            fail_flag.write_text("1", encoding="utf-8")

        def heal_sends(self):
            fail_flag.unlink(missing_ok=True)
            fail_match.unlink(missing_ok=True)

        def fail_sends_containing(self, needle):
            fail_match.write_text(needle, encoding="utf-8")

        def sleep_sends(self, seconds):
            sleep_flag.write_text(str(seconds), encoding="utf-8")

        def wake_sends(self):
            sleep_flag.unlink(missing_ok=True)

    return Env()


def iso(dt):
    return dt.isoformat()


def utc(local):
    """Normalize an aware datetime to UTC — every tick comparison runs there."""
    from datetime import timezone
    return local.astimezone(timezone.utc)


def load_setup_tasks():
    """Import setup-tasks.py (hyphenated filename) by path."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "setup_tasks", Path(__file__).parent.parent / "setup-tasks.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
