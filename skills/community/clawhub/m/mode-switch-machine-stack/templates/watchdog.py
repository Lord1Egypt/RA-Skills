#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""watchdog.py — mode-adaptive watchdog skeleton.

Reads the mode state file written by modes_switch.py and keeps exactly that
mode's pieces alive: expected agents and expected services get started if they
are missing. It never kills anything (killing is the switcher's job — a watchdog
with kill rights is how you lose a session mid-flight).

Same YAML matrix, same stdlib, no extra config.

Usage:
    python watchdog.py [--config templates/modes.yaml] [--dry-run]
    python watchdog.py --status
    python watchdog.py --selftest

Run it from cron / Task Scheduler every few minutes. A round is cheap but not
silent: no network call, no repair when nothing is missing, and no alert unless
something it cannot fix is still down (a failed repair, or a service with no
start_argv to repair with) — but it prints one overview line and rewrites its
own counter file (watchdog_state.json) every round. That counter is its
heartbeat: a dead watchdog otherwise looks exactly like a quiet one.

Design rules (see references/patterns.md):
  * the mode comes from the state file, never from an env var or a hardcoded list
  * read that file fail-open: missing/corrupt/unknown mode -> default_mode
    (modes_switch.read_state). Detecting that fallback and alerting on it is a
    deliberate extension point, not implemented here — a blind watchdog that
    silently picks the wrong mode is worse than none, so if you rely on the
    default, wire the alert.
  * repairs are rate limited; an unreachable service must not be restarted 300
    times a day
  * one writer per state file: the watchdog keeps its own counter file
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modes_switch as ms   # config/state/pid/port helpers — one implementation only

REPAIR_PER_HOUR = 6


# ---------------------------------------------------------------- pure logic

def mode_targets(cfg, mode):
    """(agents, services) that this mode expects. Pure — safe to unit test."""
    modes = cfg.get("modes") or {}
    mode_cfg = modes.get(mode) or {}
    return set(mode_cfg.get("profiles") or []), set(mode_cfg.get("services") or [])


def due_for_repair(state, now, limit=REPAIR_PER_HOUR):
    """Sliding one-hour budget for repairs; True = allowed to act now."""
    recent = [t for t in state.get("repair_ts", []) if now - t < 3600]
    return len(recent) < limit, recent


# ---------------------------------------------------------------- state

def wd_state_path(cfg, base):
    if cfg.get("watchdog_state_file"):
        return ms.resolve(base, cfg["watchdog_state_file"])
    return os.path.join(os.path.dirname(ms.state_path(cfg, base)), "watchdog_state.json")


def load_wd_state(cfg, base):
    try:
        with open(wd_state_path(cfg, base), encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}                      # missing/corrupt -> fail open, no markers


def save_wd_state(cfg, base, state):
    path = wd_state_path(cfg, base)
    try:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
        os.replace(tmp, path)          # atomic: never leave half a JSON file
    except Exception:
        pass


# ---------------------------------------------------------------- alerting

def send_alert(cfg, base, text, state, now, dry=False, log=print):
    alert = cfg.get("alert") or {}
    argv = ms._argv(alert.get("cmd"))
    if not argv:
        log(f"alert: {text}  (no alert.cmd configured)")
        return state
    last = float(state.get("last_alert_ts", 0))
    if now - last < float(alert.get("min_interval_s") or 1800):
        log(f"alert throttled: {text}")
        return state
    argv = [str(a).replace("{text}", text) for a in argv]
    if dry:
        log(f"alert: WOULD send '{text}'")
        return state
    try:
        ms._run(argv, timeout=15)
    except Exception as e:              # a broken alert channel must not kill the watchdog
        log(f"alert FAILED ({e}): {text}")
    state["last_alert_ts"] = now
    log(f"alert sent: {text}")
    return state


# ---------------------------------------------------------------- round

def run_round(cfg, base, dry=False, log=print):
    mode = ms.read_state(cfg, base)
    agents, services = mode_targets(cfg, mode)
    log(f"mode={mode} expected agents={sorted(agents)} services={sorted(services)}")

    state = load_wd_state(cfg, base)
    now = time.time()
    state["last_run_ts"] = now
    problems = []

    # agents
    profiles_dir = ms.resolve(base, cfg.get("profiles_dir") or "../profiles")
    if os.path.isdir(profiles_dir):
        for name in sorted(os.listdir(profiles_dir)):
            if name not in agents or not os.path.isdir(os.path.join(profiles_dir, name)):
                continue
            if ms.gateway_alive(cfg, base, name):
                continue
            allowed, recent = due_for_repair(state, now)
            if not allowed:
                problems.append(f"agent {name} down, repair budget spent")
                continue
            start_argv = (cfg.get("gateway") or {}).get("start_argv")
            if not start_argv:
                problems.append(f"agent {name} down, no gateway.start_argv")
                continue
            if dry:
                log(f"agent {name}: WOULD start")
                continue
            ms._spawn(start_argv, cwd=os.path.dirname(ms.pidfile_path(cfg, base, name)),
                      log=log, what=f"agent {name} (watchdog repair)")
            state["repair_ts"] = recent + [now]
            log(f"agent {name}: restarted by watchdog")

    # services
    for svc in cfg.get("services") or []:
        name = svc.get("name")
        if name not in services or ms.port_alive(svc.get("port")):
            continue
        allowed, recent = due_for_repair(state, now)
        if not allowed:
            problems.append(f"service {name} down, repair budget spent")
            continue
        start_argv = svc.get("start_argv")
        if not start_argv:
            problems.append(f"service {name} down, no start_argv (monitor only)")
            continue
        if dry:
            log(f"service {name}: WOULD start")
            continue
        ms._spawn(start_argv, log=log, what=f"service {name} (watchdog repair)")
        state["repair_ts"] = recent + [now]
        log(f"service {name}: restarted by watchdog")

    if problems:
        state = send_alert(cfg, base, "; ".join(problems), state, now, dry=dry, log=log)
    if not dry:
        save_wd_state(cfg, base, state)
    return 0


def main(argv):
    argv = list(argv)
    cfg_path = "templates/modes.yaml"
    if "--config" in argv:
        i = argv.index("--config")
        cfg_path = argv[i + 1]
        del argv[i:i + 2]
    dry = "--dry-run" in argv
    argv = [a for a in argv if a != "--dry-run"]
    if "--selftest" in argv:
        return selftest()

    cfg, base = ms.load_config(cfg_path)
    if "--status" in argv:
        mode = ms.read_state(cfg, base)
        agents, services = mode_targets(cfg, mode)
        print(json.dumps({"mode": mode, "agents": sorted(agents),
                          "services": sorted(services)}, ensure_ascii=False))
        return 0
    return run_round(cfg, base, dry=dry)


# ---------------------------------------------------------------- selftest

def selftest():
    """Pure logic: mode targets, unknown-mode fallback, repair throttle, state IO."""
    cfg = {"default_mode": "work",
           "modes": {"work": {"profiles": ["a"], "services": ["s1"]},
                     "game": {"profiles": [], "services": ["s2"]}}}
    assert mode_targets(cfg, "work") == ({"a"}, {"s1"}), "work targets"
    assert mode_targets(cfg, "game") == (set(), {"s2"}), "game targets"
    assert mode_targets(cfg, "nope") == (set(), set()), "unknown mode -> empty targets"

    now = 1_000_000.0
    state = {}
    for i in range(REPAIR_PER_HOUR):
        allowed, recent = due_for_repair(state, now + i)
        assert allowed, "repairs allowed inside the budget"
        state["repair_ts"] = recent + [now + i]
    allowed, _ = due_for_repair(state, now + 10)
    assert not allowed, "repair budget must run out"
    allowed, recent = due_for_repair(state, now + 3700)
    assert allowed, "budget must replenish after an hour"
    assert all(t > now - 3600 for t in recent), "old timestamps fall out of the window"

    state = send_alert({"alert": {}}, "", "x", state, now, dry=True, log=lambda m: None)
    assert state.get("last_alert_ts") is None, "no alert.cmd -> nothing sent"
    cfg_alert = {"alert": {"cmd": [sys.executable, "-c", "pass", "{text}"], "min_interval_s": 1800}}
    state = send_alert(cfg_alert, ".", "boom", {}, now, dry=True, log=lambda m: None)
    assert state.get("last_alert_ts") is None, "dry-run must not record an alert"
    state = send_alert(cfg_alert, ".", "boom", {}, now, dry=False, log=lambda m: None)
    assert state["last_alert_ts"] == now, "sent alert is recorded"
    state = send_alert(cfg_alert, ".", "boom2", state, now + 5, dry=False, log=lambda m: None)
    assert state["last_alert_ts"] == now, "second alert inside the window is throttled"

    # state file IO round trip, in a temp dir
    import tempfile
    tmp = tempfile.mkdtemp(prefix="watchdog_selftest_")
    base_cfg = {"state_file": os.path.join(tmp, "modes_state.json")}
    assert load_wd_state(base_cfg, tmp) == {}, "missing state file -> fail open"
    with open(wd_state_path(base_cfg, tmp), "w", encoding="utf-8") as f:
        f.write("{not json")
    assert load_wd_state(base_cfg, tmp) == {}, "corrupt state file -> fail open"
    save_wd_state(base_cfg, tmp, {"repair_ts": [1.0]})
    assert load_wd_state(base_cfg, tmp) == {"repair_ts": [1.0]}, "round trip"
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
