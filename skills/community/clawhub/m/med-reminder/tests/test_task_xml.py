"""
Task-XML tests — the Windows tick registers via generated Task Scheduler 2.0
XML with StartWhenAvailable (missed-run catch-up), IgnoreNew, the PT10M
execution limit and a baked-in --state path (issue #1 §5).

Rewritten for PR 3: the per-dose Task model and build_tasks() are gone —
one repeating tick task per state file replaces them. Paths are fed in
resolved form (tick_arguments resolves them; resolve() is idempotent).
"""
import xml.etree.ElementTree as ET
from pathlib import Path

from tests.conftest import load_setup_tasks

setup_tasks = load_setup_tasks()

NS = "{http://schemas.microsoft.com/windows/2004/02/mit/task}"

STATE_PATH = str(Path("C:/x/meds-state.json").resolve())


def build_xml(**kw):
    defaults = dict(python="C:/Python314/pythonw.exe",
                    dispatch="C:/dev/openclaw-med-reminder-skill/dispatch.py",
                    state_path=STATE_PATH,
                    tick_minutes=5, start_date="2026-08-21")
    defaults.update(kw)
    return setup_tasks.tick_task_xml(**defaults)


def parse(xml):
    return ET.fromstring(xml)


# ── settings the tick must carry ───────────────────────────────────────────────

def test_start_when_available_true():
    root = parse(build_xml())
    assert root.findtext(f"{NS}Settings/{NS}StartWhenAvailable") == "true"


def test_execution_time_limit_10m():
    # PT10M, not PT1H: with the 60s send timeout + tick-instance lock, a tick
    # running longer than 10 minutes is hung — killing it lets the next run go.
    root = parse(build_xml())
    assert root.findtext(f"{NS}Settings/{NS}ExecutionTimeLimit") == "PT10M"


def test_multiple_instances_ignore_new():
    root = parse(build_xml())
    assert root.findtext(f"{NS}Settings/{NS}MultipleInstancesPolicy") == "IgnoreNew"


def test_runs_on_battery():
    root = parse(build_xml())
    assert root.findtext(f"{NS}Settings/{NS}DisallowStartIfOnBatteries") == "false"
    assert root.findtext(f"{NS}Settings/{NS}StopIfGoingOnBatteries") == "false"


# ── action ─────────────────────────────────────────────────────────────────────

def test_action_bakes_state_and_tick():
    root = parse(build_xml())
    args = root.findtext(f"{NS}Actions/{NS}Exec/{NS}Arguments")
    cmd = root.findtext(f"{NS}Actions/{NS}Exec/{NS}Command")
    assert cmd == "C:/Python314/pythonw.exe"
    assert f'--state "{STATE_PATH}"' in args
    assert args.endswith("tick --tick-minutes 5")


def test_action_state_flag_survives_escaping():
    root = parse(build_xml(state_path=str(Path("C:/some where/meds-state.json").resolve())))
    args = root.findtext(f"{NS}Actions/{NS}Exec/{NS}Arguments")
    assert f'--state "{Path("C:/some where/meds-state.json").resolve()}"' in args


# ── trigger ────────────────────────────────────────────────────────────────────

def test_interval_trigger_repeats_every_tick_minutes():
    root = parse(build_xml(tick_minutes=1))
    rep = root.find(f"{NS}Triggers/{NS}TimeTrigger/{NS}Repetition")
    assert rep is not None
    assert rep.findtext(f"{NS}Interval") == "PT1M"
    assert rep.findtext(f"{NS}StopAtDurationEnd") == "false"


# ── description escaping ───────────────────────────────────────────────────────

def test_registration_info_present():
    root = parse(build_xml())
    assert "tick every 5 min" in (root.findtext(f"{NS}RegistrationInfo/{NS}Description")
                                  or "")
