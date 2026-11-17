#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""modes_switch.py — flip a whole machine stack with one command.

One mode = VPN on/off + which background agents run + which local services run
+ a model tier. Everything comes from a YAML matrix (templates/modes.yaml), so
this script holds no machine-specific knowledge.

Usage:
    python modes_switch.py <mode> [--config templates/modes.yaml] [--dry-run]
    python modes_switch.py --list
    python modes_switch.py --state
    python modes_switch.py --selftest      # fake stack, end to end, zero real effect

Design rules (learned the hard way — see references/patterns.md):
  * write the target mode to the state file FIRST, then mutate, so a crash
    mid-switch cannot leave watchdogs resurrecting the old mode
  * stop processes by pidfile or by listening port only; never fuzzy-match names
  * a pid from a pidfile is only trusted when its start time matches the live
    process (PID reuse silently "confirms" a process that is not yours)
  * every step is idempotent: already-right = no-op, reported as such

Stdlib only. Windows first (netstat / tasklist / taskkill); see SKILL.md for
the three POSIX swaps.
"""

import json
import os
import socket
import subprocess
import sys
import time

_IS_WIN = os.name == "nt"
_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0) if _IS_WIN else 0
_DETACH = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW) if _IS_WIN else 0
_ON_WINDOWS_FLAG = "start_new_session"
PID_FRESH_S = 300        # pidfile start_time vs real process start time tolerance
SERVICE_WAIT_S = 15      # how long to wait for a started service port to open
KILL_WAIT_S = 3

# ---------------------------------------------------------------- YAML subset

def _scalar(raw):
    s = raw.strip()
    if not s:
        return None
    if len(s) > 1 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in inner.split(",")] if inner else []
    if s.startswith("{") and s.endswith("}") and ":" in s:
        out = {}
        for pair in s[1:-1].split(","):        # flat flow map only, e.g. {a: 1, b: x}
            key, _, raw = pair.partition(":")
            out[key.strip()] = _scalar(raw)
        return out
    low = s.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        return s


def _parse_block(lines, i, indent):
    """lines: [(indent, text)]. Returns (value, next_index)."""
    if lines[i][1].startswith("-"):
        items = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("-"):
            rest = lines[i][1][1:].strip()
            i += 1
            if not rest:                                    # "- " then a nested block
                if i < len(lines) and lines[i][0] > indent:
                    val, i = _parse_block(lines, i, lines[i][0])
                else:
                    val = None
            elif ":" in rest:                               # map item
                key, _, raw = rest.partition(":")
                key = key.strip()
                item = {}
                if raw.strip():
                    item[key] = _scalar(raw)
                elif i < len(lines) and lines[i][0] > indent:
                    item[key], i = _parse_block(lines, i, lines[i][0])
                else:
                    item[key] = None
                if i < len(lines) and lines[i][0] > indent:  # remaining keys of the item
                    more, i = _parse_block(lines, i, lines[i][0])
                    if isinstance(more, dict):
                        item.update(more)
                val = item
            else:
                val = _scalar(rest)
            items.append(val)
        return items, i
    out = {}
    while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("-"):
        key, _, raw = lines[i][1].partition(":")
        key = key.strip()
        i += 1
        if raw.strip():
            out[key] = _scalar(raw)
        elif i < len(lines) and lines[i][0] > indent:
            out[key], i = _parse_block(lines, i, lines[i][0])
        else:
            out[key] = None
    return out, i


def load_yaml_subset(text):
    """Parse the subset documented in templates/modes.yaml."""
    lines = []
    for raw in text.splitlines():
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        lines.append((len(line) - len(line.lstrip()), line.strip()))
    if not lines:
        return {}
    value, _ = _parse_block(lines, 0, lines[0][0])
    return value


# ---------------------------------------------------------------- config / state

def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = load_yaml_subset(f.read()) or {}
    return cfg, os.path.dirname(os.path.abspath(path))


def resolve(base, path):
    """Relative config paths resolve against the config file's directory."""
    return path if os.path.isabs(path) else os.path.normpath(os.path.join(base, path))


def state_path(cfg, base):
    return resolve(base, cfg.get("state_file") or "../modes_state.json")


def valid_modes(cfg):
    return list((cfg.get("modes") or {}).keys())


def read_state(cfg, base):
    """Missing/corrupt/unknown mode -> default_mode (never guess into a bad mode)."""
    fallback = cfg.get("default_mode") or (valid_modes(cfg) or ["default"])[0]
    try:
        with open(state_path(cfg, base), encoding="utf-8") as f:
            mode = json.load(f).get("mode", fallback)
        return mode if mode in valid_modes(cfg) else fallback
    except Exception:
        return fallback


def write_state(cfg, base, mode, log=print):
    modes = cfg.get("modes") or {}
    data = {"mode": mode, "name": modes.get(mode, {}).get("name", mode),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    path = state_path(cfg, base)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)          # atomic: a half-written state file blinds the watchdogs
    log(f"state written: {mode} ({data['name']})")


# ---------------------------------------------------------------- probes

def port_alive(port, host="127.0.0.1", timeout=2):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except Exception:
        return False


def _run(argv, timeout=15, cwd=None):
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                          cwd=cwd, encoding="utf-8", errors="replace",
                          creationflags=_NO_WINDOW)


def _listen_pids(port):
    """PIDs listening on exactly this port. Exact port match, never a substring
    (:3001 must not match :30010)."""
    if _IS_WIN:
        out = _run(["netstat", "-ano", "-p", "TCP"], timeout=8)
        pids = set()
        for line in (out.stdout or "").splitlines():
            if "LISTENING" not in line:
                continue
            parts = line.split()
            if len(parts) < 2 or ":" not in parts[1]:
                continue
            if parts[1].rsplit(":", 1)[-1] == str(port) and parts[-1].isdigit():
                pids.add(int(parts[-1]))
        return sorted(pids)
    pids = set()
    for argv in (["lsof", "-ti", f"tcp:{port}", "-sTCP:LISTEN"], ["fuser", f"{port}/tcp"]):
        try:
            out = _run(argv, timeout=8)                      # POSIX swap 1
        except Exception:
            continue
        for tok in (out.stdout or "").split():
            if tok.isdigit():
                pids.add(int(tok))
        if pids:
            break
    return sorted(pids)


def pid_alive(pid):
    if _IS_WIN:
        try:
            out = _run(["tasklist", "/FI", f"PID eq {int(pid)}", "/NH"], timeout=8)
            return str(int(pid)) in (out.stdout or "")
        except Exception:
            return False
    try:
        os.kill(int(pid), 0)                                 # POSIX swap 2
        return True
    except PermissionError:
        return True
    except Exception:
        return False


def _process_start_ms(pid):
    """Live process start time in epoch ms, or None when it cannot be read."""
    if not _IS_WIN:
        return None
    ps = ("(Get-CimInstance Win32_Process -Filter \"ProcessId=%d\" | "
          "Select-Object -First 1).CreationDate.ToUniversalTime()"
          ".Subtract([datetime]'1970-01-01').TotalMilliseconds" % int(pid))
    try:
        out = _run(["powershell", "-NoProfile", "-Command", ps], timeout=10)
        return int(float((out.stdout or "").strip()))
    except Exception:
        return None


def stop_pid(pid):
    pid = int(pid)
    try:
        if _IS_WIN:
            _run(["taskkill", "/PID", str(pid), "/F"], timeout=10)
        else:
            os.kill(pid, 15)                                 # POSIX swap 3 (SIGTERM)
    except Exception:
        return False
    deadline = time.time() + KILL_WAIT_S
    while time.time() < deadline:
        if not pid_alive(pid):
            break
        time.sleep(0.2)
    return not pid_alive(pid)


# ---------------------------------------------------------------- pidfiles

def pidfile_path(cfg, base, profile):
    name = ((cfg.get("gateway") or {}).get("pidfile")) or "gateway.pid"
    return os.path.join(resolve(base, cfg.get("profiles_dir") or "../profiles"), profile, name)


def read_pidfile(cfg, base, profile):
    """Returns (pid, start_time). A bare integer pidfile is accepted."""
    try:
        with open(pidfile_path(cfg, base, profile), encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None, None
    if isinstance(data, dict):
        return data.get("pid"), data.get("start_time")
    if isinstance(data, int):
        return data, None
    return None, None


def gateway_alive(cfg, base, profile):
    """pidfile pid must exist AND (when a start_time is recorded) match the live
    process — a reused PID otherwise looks exactly like a healthy agent."""
    pid, start_time = read_pidfile(cfg, base, profile)
    if not pid or not pid_alive(pid):
        return False
    if not start_time:
        return True                      # no start_time recorded: pid-only check
    live = _process_start_ms(pid)
    if live is None:
        return True                      # cannot read it, do not declare a live agent dead
    tol = PID_FRESH_S * 1000
    return any(abs(live - int(start_time) * scale) <= tol for scale in (1, 10, 1000))


# ---------------------------------------------------------------- actions

def _spawn(argv, cwd=None, log=print, what=""):
    """Detached, no console window: the child must outlive this switch."""
    kwargs = {"cwd": cwd, "stdin": subprocess.DEVNULL,
              "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if _IS_WIN:
        kwargs["creationflags"] = _DETACH
    else:
        kwargs[_ON_WINDOWS_FLAG] = True
    subprocess.Popen([str(a) for a in argv], **kwargs)
    log(f"started {what or argv[0]}")


def _argv(cmd):
    """A command may be a path string or an argv list ([python, script.py])."""
    if not cmd:
        return []
    return [str(x) for x in cmd] if isinstance(cmd, list) else [str(cmd)]


def set_vpn(cfg, base, desired, dry=False, log=print):
    vpn = cfg.get("vpn") or {}
    cmd = _argv(vpn.get("cmd"))
    if desired is True:
        desired = "on"
    elif desired is False:
        desired = "off"
    desired = desired or "keep"
    if not cmd:
        log("vpn: not managed by this config (cmd is empty)" if desired != "keep" else "vpn: keep")
        return
    def current():
        try:
            out = _run(cmd + _argv(vpn.get("status_args") or ["status"]), timeout=8)
            return vpn.get("connected_marker", "Connected") in (out.stdout or "")
        except Exception:
            return False
    up = current()
    args = None
    if desired == "on" and not up:
        args = _argv(vpn.get("on_args") or ["connect"])
    elif desired == "off" and up:
        args = _argv(vpn.get("off_args") or ["disconnect"])
    if args is None:
        log(f"vpn: already {desired} ({'up' if up else 'down'})")
        return
    if dry:
        log(f"vpn: WOULD run {' '.join(cmd + args)}")
        return
    _run(cmd + args, timeout=10)
    log(f"vpn: {' '.join(args)} -> requested")
    if desired == "on":
        time.sleep(int(vpn.get("settle_s") or 0))   # tunnel comes up asynchronously


def ensure_agent(cfg, base, profile, want, dry=False, log=print):
    alive = gateway_alive(cfg, base, profile)
    if want:
        if alive:
            log(f"agent {profile}: running")
            return
        start_argv = (cfg.get("gateway") or {}).get("start_argv")
        if not start_argv:
            log(f"agent {profile}: missing and no gateway.start_argv configured")
            return
        home = os.path.dirname(pidfile_path(cfg, base, profile))
        if dry:
            log(f"agent {profile}: WOULD start {start_argv} (cwd={home})")
            return
        _spawn(start_argv, cwd=home, log=log, what=f"agent {profile}")
    else:
        if not alive:
            log(f"agent {profile}: already offline")
            return
        pid, _ = read_pidfile(cfg, base, profile)
        if dry:
            log(f"agent {profile}: WOULD stop pid {pid}")
            return
        ok = stop_pid(pid)
        log(f"agent {profile}: {'stopped' if ok else 'stop FAILED (pid ' + str(pid) + ')'}")


def ensure_service(cfg, base, svc, want, dry=False, log=print):
    name, port = svc.get("name"), int(svc.get("port"))
    if want:
        if port_alive(port):
            log(f"service {name}:{port} running")
            return
        start_argv = svc.get("start_argv")
        if not start_argv:
            log(f"service {name}:{port} down, no start_argv (monitor only)")
            return
        if dry:
            log(f"service {name}:{port} WOULD start {start_argv}")
            return
        _spawn(start_argv, log=log, what=f"service {name}")
        deadline = time.time() + SERVICE_WAIT_S
        while time.time() < deadline and not port_alive(port):
            time.sleep(0.5)
        log(f"service {name}:{port} {'up' if port_alive(port) else 'did NOT come up'}")
    else:
        if not port_alive(port):
            log(f"service {name}:{port} already offline")
            return
        pids = _listen_pids(port)
        if dry:
            log(f"service {name}:{port} WOULD stop pid(s) {pids}")
            return
        if not pids:
            log(f"service {name}:{port} up but no owner pid found - left alone")
            return
        ok = all(stop_pid(p) for p in pids)
        log(f"service {name}:{port} {'stopped' if ok else 'stop FAILED'}")


def set_model_job(cfg, base, mode_cfg, dry=False, log=print):
    cmd = (cfg.get("model_job") or {}).get("cmd") or []
    model = mode_cfg.get("model") or {}
    if not cmd:
        return
    if not model.get("model"):
        log("model tier: mode has no model block - skipped")
        return
    argv = [str(a).replace("{model}", str(model.get("model", "")))
            .replace("{provider}", str(model.get("provider", ""))) for a in cmd]
    if dry:
        log(f"model tier: WOULD run {' '.join(argv)}")
        return
    out = _run(argv, timeout=15)
    log(f"model tier: {model.get('model')} ({'ok' if out.returncode == 0 else 'FAILED'})")


# ---------------------------------------------------------------- main flow

def switch(mode, cfg, base, dry=False, log=print):
    modes = cfg.get("modes") or {}
    if mode not in modes:
        log(f"unknown mode: {mode} (available: {', '.join(modes)})")
        return 1
    mode_cfg = modes[mode] or {}
    log(f"switch -> {mode_cfg.get('name', mode)}" + (" [dry-run]" if dry else ""))

    # 1. state first: a crash mid-switch then leaves the watchdogs aiming at the
    #    NEW mode, never resurrecting pieces the user just switched away from.
    if not dry:
        write_state(cfg, base, mode, log=log)

    # 2. VPN
    set_vpn(cfg, base, mode_cfg.get("vpn", "keep"), dry=dry, log=log)

    # 3. agents: iterate every profile directory, so a mode only names what it wants
    want_agents = set(mode_cfg.get("profiles") or [])
    profiles_dir = resolve(base, cfg.get("profiles_dir") or "../profiles")
    if os.path.isdir(profiles_dir):
        for name in sorted(os.listdir(profiles_dir)):
            if os.path.isdir(os.path.join(profiles_dir, name)):
                ensure_agent(cfg, base, name, name in want_agents, dry=dry, log=log)

    # 4. services: iterate every configured service, same reason
    want_services = set(mode_cfg.get("services") or [])
    for svc in cfg.get("services") or []:
        ensure_service(cfg, base, svc, svc.get("name") in want_services, dry=dry, log=log)

    # 5. model tier
    set_model_job(cfg, base, mode_cfg, dry=dry, log=log)
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

    cfg, base = load_config(cfg_path)
    if "--list" in argv:
        for name in valid_modes(cfg):
            print(f"{name}\t{(cfg['modes'][name] or {}).get('name', name)}")
        return 0
    if "--state" in argv:
        print(read_state(cfg, base))
        return 0
    mode = argv[0] if argv else read_state(cfg, base)
    return switch(mode, cfg, base, dry=dry)


# ---------------------------------------------------------------- selftest

def selftest():
    """Whole flow against a fake stack in a temp dir: fake VPN CLI, fake agent
    (writes its own pidfile), fake service (really binds a port). No effect on
    anything real. Run: python modes_switch.py --selftest"""
    assert load_yaml_subset(
        "a: 1\nb:\n  c: [x, y]\n  d:\n    - name: n\n      port: 2\n"
    ) == {"a": 1, "b": {"c": ["x", "y"], "d": [{"name": "n", "port": 2}]}}, "yaml subset"
    assert _listen_pids(1) == [] or True   # smoke: must not raise

    import tempfile
    tmp = tempfile.mkdtemp(prefix="modes_selftest_")
    py = sys.executable
    log = lambda m: print("   " + str(m))

    def free_port():
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        p = s.getsockname()[1]
        s.close()
        return p

    port_a, port_b = free_port(), free_port()
    with open(os.path.join(tmp, "fake_vpn.py"), "w", encoding="utf-8") as f:
        f.write("import os,sys\n"
                "d=os.path.dirname(os.path.abspath(__file__))\n"
                "flag=os.path.join(d,'vpn_state')\n"
                "open(os.path.join(d,'vpn_calls.log'),'a').write(sys.argv[1]+'\\n')\n"
                "a=sys.argv[1] if len(sys.argv)>1 else ''\n"
                "if a=='status': print('Connected' if os.path.exists(flag) else 'Disconnected')\n"
                "elif a=='connect': open(flag,'w').write('up')\n"
                "elif a=='disconnect': os.path.exists(flag) and os.remove(flag)\n")
    with open(os.path.join(tmp, "fake_agent.py"), "w", encoding="utf-8") as f:
        f.write("import json,os,time\n"
                "p=os.path.join(os.getcwd(),'gateway.pid')\n"
                "json.dump({'pid':os.getpid(),'start_time':int(time.time())},open(p,'w'))\n"
                "time.sleep(120)\n")
    with open(os.path.join(tmp, "fake_service.py"), "w", encoding="utf-8") as f:
        f.write("import socket,sys,time\n"
                "s=socket.socket();s.bind(('127.0.0.1',int(sys.argv[1])));s.listen(5)\n"
                "time.sleep(300)\n")
    with open(os.path.join(tmp, "modes.yaml"), "w", encoding="utf-8") as f:
        f.write(
            "state_file: state.json\n"
            "default_mode: work\n"
            "vpn:\n"
            f"  cmd: [{py}, {os.path.join(tmp, 'fake_vpn.py')}]\n"
            "  settle_s: 0\n"
            "profiles_dir: profiles\n"
            "gateway:\n"
            f"  start_argv: [{py}, {os.path.join(tmp, 'fake_agent.py')}]\n"
            "services:\n"
            "  - name: fake-a\n"
            f"    port: {port_a}\n"
            f"    start_argv: [{py}, {os.path.join(tmp, 'fake_service.py')}, {port_a}]\n"
            "  - name: fake-b\n"
            f"    port: {port_b}\n"
            f"    start_argv: [{py}, {os.path.join(tmp, 'fake_service.py')}, {port_b}]\n"
            "model_job:\n"
            f"  cmd: [{py}, -c, pass, {{model}}]\n"
            "modes:\n"
            "  work:\n"
            "    name: Work\n"
            "    vpn: on\n"
            "    profiles: [fake-agent]\n"
            "    services: [fake-a]\n"
            "    model: {model: local-model, provider: local}\n"
            "  game:\n"
            "    name: Game\n"
            "    vpn: off\n"
            "    profiles: []\n"
            "    services: [fake-b]\n"
            "    model: {model: cloud-model, provider: cloud}\n"
        )
    os.makedirs(os.path.join(tmp, "profiles", "fake-agent"), exist_ok=True)
    cfg, base = load_config(os.path.join(tmp, "modes.yaml"))
    try:
        assert switch("nope", cfg, base, log=log) == 1, "unknown mode must fail"
        assert switch("work", cfg, base, dry=True, log=log) == 0, "dry-run rc"
        assert not os.path.exists(os.path.join(tmp, "state.json")), "dry-run must not write state"
        assert switch("work", cfg, base, log=log) == 0, "work switch rc"
        st = json.load(open(os.path.join(tmp, "state.json"), encoding="utf-8"))
        assert st["mode"] == "work", "state written first"
        assert port_alive(port_a), "service fake-a should be up"
        assert gateway_alive(cfg, base, "fake-agent"), "fake agent pidfile not trusted"
        assert read_state(cfg, base) == "work", "read_state round trip"
        assert switch("game", cfg, base, log=log) == 0, "game switch rc"
        assert not port_alive(port_a), "fake-a must be stopped by port"
        assert port_alive(port_b), "fake-b must be started"
        assert not gateway_alive(cfg, base, "fake-agent"), "fake agent must be stopped"
        calls = open(os.path.join(tmp, "vpn_calls.log"), encoding="utf-8").read().split()
        assert "connect" in calls and "disconnect" in calls, f"vpn toggled: {calls}"
        # corrupted / unknown state must fall back, not crash
        json.dump({"mode": "garbage"}, open(os.path.join(tmp, "state.json"), "w"))
        assert read_state(cfg, base) == "work", "unknown mode -> default_mode"
        print("selftest OK")
        return 0
    finally:
        for svc in cfg.get("services") or []:
            for p in _listen_pids(svc["port"]):
                stop_pid(p)
        pid, _ = read_pidfile(cfg, base, "fake-agent")
        if pid and pid_alive(pid):
            stop_pid(pid)
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
