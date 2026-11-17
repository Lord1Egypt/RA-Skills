"""
Scheduler migration tests (issue #1 §5, AC 33-35).

Every OS interaction goes through the FakeOs double wired into
setup-tasks' `_run` seam (and doctor's) — no test ever touches a real
schtasks, crontab, launchctl or systemctl.

Cron strip covers the pre-PR3 marker format, duplicated blocks, our new
BEGIN/END blocks and stray per-dose lines, with foreign lines before and
after (AC 33). Windows covers folder enumeration, pythonw registration
and the register-verify-remove flow (AC 34-35).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

import doctor
from tests.conftest import load_setup_tasks

setup_tasks = load_setup_tasks()

FOREIGN = [
    "# backup job — not ours",
    "0 2 * * * /usr/local/bin/backup",
]


class FakeOs:
    """
    In-memory crontab + Task Scheduler + launchctl + systemctl for one test.
    `crontab=None` means "no crontab for user" (rc 1 + the classic stderr).
    """

    def __init__(self, crontab=None, tasks=None):
        self.crontab = list(crontab) if crontab is not None else None
        self.tasks = dict(tasks or {})      # windows: full task name -> True
        self.xml_by_task = {}               # windows: name -> XML passed to /create
        self.loaded_agents = set()          # launchd labels currently loaded
        self.enabled_timers = set()         # systemd units currently enabled
        self.calls = []
        self.fail_always = set()            # command substrings that always fail
        self.fail_after = {}                # substring -> N: fail on call > N
        self._counts = {}

    # -- plumbing ------------------------------------------------------------
    def _fail(self, cmd, key):
        return subprocess.CompletedProcess(cmd, 1, stdout="",
                                           stderr=f"fake failure: {key}")

    @staticmethod
    def _matches(key, cmd, joined):
        # a tuple key matches the command prefix exactly (e.g. ("crontab", "-")
        # must not also catch "crontab -l"); a string key is a substring
        if isinstance(key, tuple):
            return list(key) == list(cmd[:len(key)])
        return key in joined

    def __call__(self, cmd, **kw):
        self.calls.append(cmd)
        joined = " ".join(str(c) for c in cmd)
        for key in self.fail_always:
            if self._matches(key, cmd, joined):
                return self._fail(cmd, key)
        for key, n in self.fail_after.items():
            if self._matches(key, cmd, joined):
                self._counts[str(key)] = self._counts.get(str(key), 0) + 1
                if self._counts[str(key)] > n:
                    return self._fail(cmd, key)

        if cmd[:2] == ["crontab", "-l"]:
            if self.crontab is None:
                return subprocess.CompletedProcess(cmd, 1, stdout="",
                                                   stderr="no crontab for tester")
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout="\n".join(self.crontab), stderr="")
        if cmd[:2] == ["crontab", "-"]:
            self.crontab = kw.get("input", "").splitlines()
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        if cmd[0] == "schtasks":
            return self._schtasks(cmd)
        if cmd[0] == "launchctl":
            return self._launchctl(cmd)
        if cmd[0] == "systemctl":
            return self._systemctl(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    # -- doubles -------------------------------------------------------------
    def _schtasks(self, cmd):
        if cmd[1] == "/query" and "/fo" in cmd:            # folder enumeration
            rows = "".join(f'"{n}","2026-10-18 09:00:00","Ready",""\n'
                           for n in sorted(self.tasks))
            return subprocess.CompletedProcess(cmd, 0, stdout=rows, stderr="")
        if cmd[1] == "/query":                             # single task probe
            name = cmd[cmd.index("/tn") + 1]
            found = name in self.tasks
            return subprocess.CompletedProcess(cmd, 0 if found else 1, stdout="",
                                               stderr="" if found else "not found")
        if cmd[1] == "/create":
            name = cmd[cmd.index("/tn") + 1]
            xml_path = cmd[cmd.index("/xml") + 1]
            self.tasks[name] = True
            self.xml_by_task[name] = Path(xml_path).read_text(encoding="utf-16")
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        if cmd[1] == "/delete":
            self.tasks.pop(cmd[cmd.index("/tn") + 1], None)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        raise AssertionError(f"unmocked schtasks call: {cmd}")

    def _launchctl(self, cmd):
        if cmd[1] == "load":
            self.loaded_agents.add(Path(cmd[2]).stem)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        if cmd[1] == "unload":
            self.loaded_agents.discard(Path(cmd[2]).stem)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        if cmd[1] == "list":                               # label query
            loaded = cmd[2] in self.loaded_agents
            return subprocess.CompletedProcess(cmd, 0 if loaded else 1, stdout="",
                                               stderr="" if loaded else "not found")
        raise AssertionError(f"unmocked launchctl call: {cmd}")

    def _systemctl(self, cmd):
        unit = cmd[-1]
        if cmd[1:3] == ["--user", "enable"]:
            self.enabled_timers.add(unit)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        if cmd[1:3] == ["--user", "disable"]:
            self.enabled_timers.discard(unit)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        if cmd[1:3] == ["--user", "is-enabled"]:
            enabled = unit in self.enabled_timers
            return subprocess.CompletedProcess(cmd, 0 if enabled else 1,
                                               stdout="enabled\n" if enabled else "",
                                               stderr="" if enabled else "disabled")
        if cmd[1:3] == ["--user", "daemon-reload"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        raise AssertionError(f"unmocked systemctl call: {cmd}")


# ── fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def state_file(tmp_path):
    sf = tmp_path / "meds-state.json"
    sf.write_text("{}", encoding="utf-8")
    return sf


@pytest.fixture
def sandbox(tmp_path, monkeypatch, state_file):
    """
    Point one setup-tasks module instance at tmp_path: state file, registry
    files, legacy registry, launchd/systemd paths. Nothing may touch the
    repo dir or the real HOME.
    """
    monkeypatch.setattr(setup_tasks, "STATE_FILE", state_file)
    monkeypatch.setattr(setup_tasks, "SCRIPT_DIR", tmp_path)
    monkeypatch.setattr(setup_tasks, "LEGACY_REGISTRY_FILE",
                        tmp_path / ".registered-tasks.json")
    monkeypatch.setattr(setup_tasks, "launchd_plist_path",
                        lambda label: tmp_path / "LaunchAgents" / f"{label}.plist")
    monkeypatch.setattr(setup_tasks, "systemd_unit_dir",
                        lambda: tmp_path / "systemd-user")
    return state_file


def legacy_block(state_flag):
    """A pre-PR3 crontab block exactly as the old register_unix wrote it."""
    return [
        "# MedReminder",
        "# Daily med digest at 08:00",
        f'0 8 * * * "py" "dispatch.py" --state "{state_flag}" digest',
        "# Metformin: reminder at 08:00",
        f'0 8 * * * "py" "dispatch.py" --state "{state_flag}" fire med-001 0',
        "# Metformin: missed check at 09:30 (+90m)",
        f'30 9 * * * "py" "dispatch.py" --state "{state_flag}" miss med-001 0',
        "",
    ]


def migrate_cron(state_file, fake, minutes=5, platform_name="linux",
                 scheduler="cron"):
    old = sys.platform
    sys.platform = platform_name
    try:
        return setup_tasks.migrate(setup_tasks.state_hash(state_file), state_file,
                                   minutes, scheduler, run=fake)
    finally:
        sys.platform = old


# ── cron strip (pure; issue #1 §5) ─────────────────────────────────────────────

def test_strip_removes_legacy_block_keeps_foreign(state_file):
    flag = str(Path(state_file).resolve())
    lines = FOREIGN + legacy_block(flag) + FOREIGN
    out = setup_tasks.strip_crontab(lines, state_file, setup_tasks.state_hash(state_file))
    assert out == FOREIGN + FOREIGN


def test_strip_removes_duplicated_legacy_blocks(state_file):
    flag = str(Path(state_file).resolve())
    lines = legacy_block(flag) + legacy_block(flag) + FOREIGN
    out = setup_tasks.strip_crontab(lines, state_file, setup_tasks.state_hash(state_file))
    assert out == FOREIGN


def test_strip_removes_own_delimited_block_keeps_other_state(state_file, tmp_path):
    h = setup_tasks.state_hash(state_file)
    other = setup_tasks.state_hash(tmp_path / "other-state.json")
    mine = setup_tasks.build_cron_block(h, "*/5 * * * * mine")
    theirs = setup_tasks.build_cron_block(other, "*/5 * * * * theirs")
    out = setup_tasks.strip_crontab(mine + theirs + FOREIGN, state_file, h)
    assert out == theirs + FOREIGN


def test_strip_removes_stray_state_lines_anywhere(state_file, tmp_path):
    h = setup_tasks.state_hash(state_file)
    flag = str(Path(state_file).resolve())
    other_flag = str((tmp_path / "other.json").resolve())
    lines = [
        FOREIGN[0],
        f'0 8 * * * "py" "dispatch.py" --state "{flag}" fire med-001 0',
        FOREIGN[1],
        f'0 8 * * * "py" "dispatch.py" --state "{other_flag}" fire med-009 0',
    ]
    out = setup_tasks.strip_crontab(lines, state_file, h)
    assert out == [FOREIGN[0], FOREIGN[1],
                   f'0 8 * * * "py" "dispatch.py" --state "{other_flag}" fire med-009 0']


def test_strip_keeps_foreign_comment_after_legacy_entries(state_file):
    # A foreign comment directly after the block's last entry must survive:
    # labels belong to the block only while entries confirm them.
    flag = str(Path(state_file).resolve())
    lines = legacy_block(flag) + ["# my own note", "5 0 * * * /bin/thing"]
    out = setup_tasks.strip_crontab(lines, state_file, setup_tasks.state_hash(state_file))
    assert out == ["# my own note", "5 0 * * * /bin/thing"]


def test_strip_is_idempotent(state_file):
    flag = str(Path(state_file).resolve())
    h = setup_tasks.state_hash(state_file)
    lines = FOREIGN + legacy_block(flag) + setup_tasks.build_cron_block(h, "*/5 * * * * x")
    once = setup_tasks.strip_crontab(lines, state_file, h)
    assert setup_tasks.strip_crontab(once, state_file, h) == once


def test_find_legacy_cron_ignores_our_block(state_file):
    h = setup_tasks.state_hash(state_file)
    flag = str(Path(state_file).resolve())
    lines = setup_tasks.build_cron_block(
        h, f'*/5 * * * * "py" "dispatch.py" --state "{flag}" tick --tick-minutes 5')
    assert setup_tasks.find_legacy_cron(lines, state_file, h) == []
    assert setup_tasks.find_legacy_cron(lines + legacy_block(flag), state_file, h)


# ── cron migration flow (AC 33) ────────────────────────────────────────────────

def test_migrate_cron_consolidates_legacy_and_keeps_foreign(sandbox, state_file):
    flag = str(Path(state_file).resolve())
    fake = FakeOs(crontab=FOREIGN + legacy_block(flag) + legacy_block(flag) + FOREIGN)
    rc = migrate_cron(state_file, fake)
    assert rc == 0

    begins = [l for l in fake.crontab if l.strip().startswith("# MedReminder BEGIN")]
    assert len(begins) == 1                       # exactly one tick block
    assert not [l for l in fake.crontab if "fire med-001" in l or " digest" in l]
    assert not [l for l in fake.crontab if l.strip() == "# MedReminder"]
    # both foreign copies survive, in order
    assert [l for l in fake.crontab if l in FOREIGN] == FOREIGN + FOREIGN

    h = setup_tasks.state_hash(state_file)
    assert setup_tasks.verify_cron(h, run=fake)   # and the block queries back


def test_migrate_cron_is_idempotent(sandbox, state_file):
    flag = str(Path(state_file).resolve())
    fake = FakeOs(crontab=legacy_block(flag))
    assert migrate_cron(state_file, fake) == 0
    first = list(fake.crontab)
    assert migrate_cron(state_file, fake) == 0    # re-run: no duplicates
    assert fake.crontab == first
    assert sum(1 for l in fake.crontab if " tick --tick-minutes " in l) == 1


def test_migrate_cron_entry_shape(sandbox, state_file):
    fake = FakeOs(crontab=[])
    assert migrate_cron(state_file, fake, minutes=1) == 0
    entry = [l for l in fake.crontab if " tick --tick-minutes " in l][0]
    assert entry.startswith("*/1 * * * * ")
    assert f'--state "{Path(state_file).resolve()}"' in entry


def test_migrate_fresh_machine_no_crontab(sandbox, state_file):
    fake = FakeOs(crontab=None)                   # "no crontab for tester"
    assert migrate_cron(state_file, fake) == 0
    assert setup_tasks.verify_cron(setup_tasks.state_hash(state_file), run=fake)


def test_registry_written_after_success(sandbox, state_file):
    fake = FakeOs(crontab=[])
    migrate_cron(state_file, fake, minutes=5)
    h = setup_tasks.state_hash(state_file)
    entry = json.loads((setup_tasks.registry_file(h)).read_text(encoding="utf-8"))
    assert entry["scheduler"] == "cron"
    assert entry["tick_minutes"] == 5
    assert entry["state"] == str(Path(state_file).resolve())


def test_state_hash_separates_state_files(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text("{}", encoding="utf-8")
    b.write_text("{}", encoding="utf-8")
    ha, hb = setup_tasks.state_hash(a), setup_tasks.state_hash(b)
    assert ha != hb and len(ha) == 8


def test_two_state_files_never_collide(sandbox, tmp_path):
    a = tmp_path / "meds-state.json"
    b = tmp_path / "meds-state-b.json"
    b.write_text("{}", encoding="utf-8")
    fake = FakeOs(crontab=[])

    def begins():
        return [l for l in fake.crontab
                if l.strip().startswith("# MedReminder BEGIN")]

    assert migrate_cron(a, fake) == 0
    assert migrate_cron(b, fake) == 0             # both blocks coexist
    assert len(begins()) == 2
    assert migrate_cron(a, fake) == 0             # re-migrating A keeps B's block
    assert len(begins()) == 2


# ── register-verify-remove failure paths (AC 35) ───────────────────────────────

def test_registration_failure_leaves_legacy(sandbox, state_file, capsys):
    flag = str(Path(state_file).resolve())
    fake = FakeOs(crontab=legacy_block(flag))
    fake.fail_always.add(("crontab", "-"))        # the write fails
    rc = migrate_cron(state_file, fake)
    out = capsys.readouterr().out
    assert rc == 1
    assert "REMINDERS ARE NOT SCHEDULED" in out
    assert fake.crontab == legacy_block(flag)     # legacy untouched


def test_verification_failure_leaves_legacy(sandbox, state_file, capsys):
    flag = str(Path(state_file).resolve())
    fake = FakeOs(crontab=legacy_block(flag))
    # register reads (-l #1) and writes (-); the verification read (-l #2) fails
    fake.fail_after[("crontab", "-l")] = 1
    rc = migrate_cron(state_file, fake)
    assert rc == 1
    assert "REMINDERS ARE NOT SCHEDULED" in capsys.readouterr().out
    # the tick block may exist, but every legacy line is still in place
    assert any("fire med-001" in l for l in fake.crontab)
    assert any("miss med-001" in l for l in fake.crontab)


def test_dry_run_touches_nothing(sandbox, state_file):
    flag = str(Path(state_file).resolve())
    fake = FakeOs(crontab=legacy_block(flag))
    old = sys.platform
    sys.platform = "linux"
    try:
        rc = setup_tasks.migrate(setup_tasks.state_hash(state_file), state_file,
                                 5, "cron", run=fake, dry_run=True)
    finally:
        sys.platform = old
    assert rc == 0
    assert fake.crontab == legacy_block(flag)
    assert fake.calls == []                       # not even a read


# ── Windows folder enumeration + migration (AC 34) ─────────────────────────────

def test_parse_task_folder_names_filters_folder():
    csv_text = ('"\\MedReminder\\fire_med-001_0","2026-10-18 09:00:00","Ready",""\n'
                '"\\Other\\unrelated","2026-10-18 09:00:00","Ready",""\n'
                '"\\MedReminder\\tick-a1b2c3d4","2026-10-18 09:00:00","Ready",""\n')
    assert setup_tasks.parse_task_folder_names(csv_text) == \
        ["\\MedReminder\\fire_med-001_0", "\\MedReminder\\tick-a1b2c3d4"]


def test_windows_migration_removes_legacy_keeps_tick(sandbox, state_file):
    (setup_tasks.LEGACY_REGISTRY_FILE).write_text('["fire_med-001_0"]',
                                                  encoding="utf-8")
    fake = FakeOs(tasks={
        "\\MedReminder\\fire_med-001_0": True,
        "\\MedReminder\\check_med-001_0": True,
        "\\MedReminder\\miss_med-001_0": True,
        "\\MedReminder\\digest": True,
        "\\MedReminder\\reset-deferred": True,
        "\\Other\\unrelated": True,
    })
    rc = migrate_cron(state_file, fake, platform_name="win32")
    assert rc == 0
    assert sorted(fake.tasks) == sorted([
        "\\MedReminder\\" + setup_tasks.tick_task_name(setup_tasks.state_hash(state_file)),
        "\\Other\\unrelated"])
    assert not setup_tasks.LEGACY_REGISTRY_FILE.exists()   # stale registry gone


def test_windows_tick_uses_pythonw_and_settings(sandbox, state_file):
    fake = FakeOs(tasks={})
    migrate_cron(state_file, fake, platform_name="win32")
    h = setup_tasks.state_hash(state_file)
    xml = fake.xml_by_task[setup_tasks.tick_task_full_name(h)]
    assert "pythonw.exe" in xml
    for needle in ("<ExecutionTimeLimit>PT10M</ExecutionTimeLimit>",
                   "<MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>",
                   "<StartWhenAvailable>true</StartWhenAvailable>",
                   "<Interval>PT5M</Interval>",
                   f"tick --tick-minutes 5"):
        assert needle in xml, needle


def test_windows_registration_failure_leaves_legacy(sandbox, state_file, capsys):
    fake = FakeOs(tasks={"\\MedReminder\\fire_med-001_0": True})
    fake.fail_always.add("/create")
    rc = migrate_cron(state_file, fake, platform_name="win32")
    assert rc == 1
    assert "REMINDERS ARE NOT SCHEDULED" in capsys.readouterr().out
    assert list(fake.tasks) == ["\\MedReminder\\fire_med-001_0"]   # untouched


def test_windows_verification_failure_leaves_legacy(sandbox, state_file, capsys):
    fake = FakeOs(tasks={"\\MedReminder\\fire_med-001_0": True})
    fake.fail_always.add("/query /tn")            # create succeeds, query fails
    rc = migrate_cron(state_file, fake, platform_name="win32")
    assert rc == 1
    assert "REMINDERS ARE NOT SCHEDULED" in capsys.readouterr().out
    assert list(fake.tasks) == ["\\MedReminder\\fire_med-001_0",
                                "\\MedReminder\\" + setup_tasks.tick_task_name(
                                    setup_tasks.state_hash(state_file))]


def test_pythonw_preferred_falls_back(tmp_path, monkeypatch):
    exe = tmp_path / "python.exe"
    exe.write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "executable", str(exe))
    (tmp_path / "pythonw.exe").write_text("", encoding="utf-8")
    assert setup_tasks._pythonw().endswith("pythonw.exe")
    (tmp_path / "pythonw.exe").unlink()
    assert setup_tasks._pythonw() == str(exe)


# ── macOS launchd + cron fallback ──────────────────────────────────────────────

def test_plist_has_start_interval_and_args(state_file):
    plist = setup_tasks.build_plist("com.medreminder.tick.x", "/usr/bin/python3",
                                    "/dev/dispatch.py", state_file, 5)
    assert "<key>StartInterval</key>\n  <integer>300</integer>" in plist
    assert "<string>--state</string>" in plist
    assert f"<string>{Path(state_file).resolve()}</string>" in plist
    assert "<string>tick</string>" in plist
    assert "<string>5</string>" in plist


def test_mac_registers_launchd_and_strips_cron(sandbox, state_file):
    flag = str(Path(state_file).resolve())
    fake = FakeOs(crontab=legacy_block(flag))
    rc = migrate_cron(state_file, fake, platform_name="darwin")
    assert rc == 0
    h = setup_tasks.state_hash(state_file)
    assert setup_tasks.launchd_label(h) in fake.loaded_agents
    assert not [l for l in fake.crontab if "fire med-001" in l]   # legacy cron gone
    assert not [l for l in fake.crontab if " tick --tick-minutes " in l]  # no cron tick


def test_mac_falls_back_to_cron_when_launchd_fails(sandbox, state_file, capsys):
    fake = FakeOs(crontab=[])
    fake.fail_always.add("launchctl load")
    rc = migrate_cron(state_file, fake, platform_name="darwin")
    assert rc == 0
    assert "falling back to cron" in capsys.readouterr().out
    assert setup_tasks.verify_cron(setup_tasks.state_hash(state_file), run=fake)


# ── Linux systemd opt-in ───────────────────────────────────────────────────────

def test_timer_content_oncalendar_persistent():
    timer = setup_tasks.build_timer("medreminder-tick-x", 5)
    assert "OnCalendar=*:0/5" in timer
    assert "Persistent=true" in timer
    assert "Unit=medreminder-tick-x.service" in timer


def test_systemd_registers_and_verifies(sandbox, state_file):
    fake = FakeOs(crontab=[])
    rc = migrate_cron(state_file, fake, scheduler="systemd")
    assert rc == 0
    h = setup_tasks.state_hash(state_file)
    assert f"medreminder-tick-{h}.timer" in fake.enabled_timers
    d = setup_tasks.systemd_unit_dir()
    assert "OnCalendar=*:0/5" in (d / f"medreminder-tick-{h}.timer").read_text()
    svc = (d / f"medreminder-tick-{h}.service").read_text()
    assert "tick --tick-minutes 5" in svc


def test_systemd_failure_leaves_legacy(sandbox, state_file, capsys):
    flag = str(Path(state_file).resolve())
    fake = FakeOs(crontab=legacy_block(flag))
    fake.fail_always.add("enable")
    rc = migrate_cron(state_file, fake, scheduler="systemd")
    assert rc == 1
    assert "REMINDERS ARE NOT SCHEDULED" in capsys.readouterr().out
    assert any("fire med-001" in l for l in fake.crontab)


# ── clear ──────────────────────────────────────────────────────────────────────

def test_clear_cron_removes_block_and_legacy(sandbox, state_file):
    flag = str(Path(state_file).resolve())
    h = setup_tasks.state_hash(state_file)
    block = setup_tasks.build_cron_block(
        h, f'*/5 * * * * "py" "dispatch.py" --state "{flag}" tick --tick-minutes 5')
    fake = FakeOs(crontab=FOREIGN + block + legacy_block(flag))
    old = sys.platform
    sys.platform = "linux"
    try:
        assert setup_tasks.clear(h, state_file, run=fake) == 0
    finally:
        sys.platform = old
    assert fake.crontab == list(FOREIGN)
    assert not setup_tasks.registry_file(h).exists()


def test_clear_windows_keeps_other_states_tick(sandbox, state_file):
    other_h = "deadbeef"
    (setup_tasks.SCRIPT_DIR / f".registered-tasks.{other_h}.json").write_text(
        json.dumps({"scheduler": "windows",
                    "task": "\\MedReminder\\tick-deadbeef"}), encoding="utf-8")
    h = setup_tasks.state_hash(state_file)
    fake = FakeOs(tasks={
        "\\MedReminder\\fire_med-001_0": True,
        "\\MedReminder\\tick-deadbeef": True,
        "\\MedReminder\\" + setup_tasks.tick_task_name(h): True,
    })
    old = sys.platform
    sys.platform = "win32"
    try:
        setup_tasks.clear(h, state_file, run=fake)
    finally:
        sys.platform = old
    assert list(fake.tasks) == ["\\MedReminder\\tick-deadbeef"]


# ── doctor's scheduler checks (AC 35) ─────────────────────────────────────────

def doctor_scheduler_results(monkeypatch, state_file, fake, platform_name):
    monkeypatch.setattr(doctor, "STATE_FILE", state_file)
    monkeypatch.setattr(doctor, "_run", fake)
    monkeypatch.setattr(sys, "platform", platform_name)
    doctor.results.clear()
    doctor.check_scheduler()
    return doctor.results


def test_doctor_fails_when_tick_missing(monkeypatch, state_file):
    fake = FakeOs(crontab=[])
    results = doctor_scheduler_results(monkeypatch, state_file, fake, "linux")
    assert any(level == "fail" and "tick block missing" in msg
               for level, msg in results)


def test_doctor_ok_when_tick_registered(monkeypatch, state_file):
    h = setup_tasks.state_hash(state_file)
    flag = str(Path(state_file).resolve())
    block = setup_tasks.build_cron_block(
        h, f'*/5 * * * * "py" "dispatch.py" --state "{flag}" tick --tick-minutes 5')
    fake = FakeOs(crontab=list(block))
    results = doctor_scheduler_results(monkeypatch, state_file, fake, "linux")
    assert not [msg for level, msg in results if level == "fail"]


def test_doctor_fails_on_legacy_cron(monkeypatch, state_file):
    flag = str(Path(state_file).resolve())
    h = setup_tasks.state_hash(state_file)
    block = setup_tasks.build_cron_block(
        h, f'*/5 * * * * "py" "dispatch.py" --state "{flag}" tick --tick-minutes 5')
    fake = FakeOs(crontab=block + legacy_block(flag))
    results = doctor_scheduler_results(monkeypatch, state_file, fake, "linux")
    assert any(level == "fail" and "legacy" in msg for level, msg in results)


def test_doctor_windows_tick_and_legacy(monkeypatch, state_file):
    h = setup_tasks.state_hash(state_file)
    fake = FakeOs(tasks={"\\MedReminder\\" + setup_tasks.tick_task_name(h): True,
                         "\\MedReminder\\fire_med-001_0": True})
    results = doctor_scheduler_results(monkeypatch, state_file, fake, "win32")
    assert any(level == "fail" and "legacy task" in msg for level, msg in results)
    fake.tasks.pop("\\MedReminder\\fire_med-001_0")
    doctor.results.clear()
    doctor.check_scheduler()
    assert not [msg for level, msg in doctor.results if level == "fail"]
