#!/usr/bin/env python3
"""Disk-backed, model-free sequential runner. Python 3.10+; standard library only."""
import argparse
import contextlib
import ctypes
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid
import wave

VERSION = "1.0.0"
ACTIVE = {"starting", "running", "waiting_resource"}
TERMINAL = {"succeeded", "failed", "timed_out", "cancelled", "interrupted"}
SCRIPT = str(Path(__file__).resolve())


class Problem(Exception):
    def __init__(self, code, detail):
        self.code, self.detail = code, str(detail)[:400]
        super().__init__(self.detail)


def require(ok, detail):
    if not ok:
        raise Problem("E_SPEC", detail)


def atomic(path, value):
    path = Path(path)
    tmp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(value, f, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            f.flush()
            os.fsync(f.fileno())
        for attempt in range(10):
            try:
                os.replace(tmp, path)
                return
            except PermissionError:
                if attempt == 9:
                    raise
                time.sleep(.02)
    finally:
        tmp.unlink(missing_ok=True)


def read(path):
    path = Path(path)
    if path.stat().st_size > 8 * 1024 * 1024:
        raise Problem("E_SIZE", "JSON exceeds 8 MiB")
    return json.loads(path.read_text(encoding="utf-8-sig"))


class Lock:
    """Kernel-owned byte/flock lock, released even when a worker is killed."""
    def __init__(self, path):
        self.path, self.f = Path(path), None

    def acquire(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        f = open(self.path, "a+b")
        try:
            if f.seek(0, 2) == 0:
                f.write(b"0")
                f.flush()
            f.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            f.close()
            return False
        self.f = f
        return True

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    def __enter__(self):
        end = time.monotonic() + 8
        while not self.acquire():
            if time.monotonic() >= end:
                raise Problem("E_BUSY", str(self.path))
            time.sleep(.05)
        return self

    def __exit__(self, *args):
        self.close()


def held(path):
    lock = Lock(path)
    got = lock.acquire()
    lock.close()
    return not got


class RollingLog:
    def __init__(self, path, limit, backups=2):
        self.path, self.limit, self.backups = Path(path), limit, backups
        self.guard = threading.Lock()
        self.error = None

    def write(self, data):
        if not data:
            return
        with self.guard:
            try:
                while data:
                    size = self.path.stat().st_size if self.path.exists() else 0
                    if size >= self.limit:
                        for i in range(self.backups, 0, -1):
                            src = self.path if i == 1 else Path(str(self.path) + f".{i-1}")
                            dst = Path(str(self.path) + f".{i}")
                            if src.exists():
                                os.replace(src, dst)
                        size = 0
                    chunk, data = data[:self.limit-size], data[self.limit-size:]
                    with open(self.path, "ab") as f:
                        f.write(chunk)
            except OSError as e:
                self.error = str(e)[:200]


def check_keys(obj, keys, where):
    require(isinstance(obj, dict), f"{where}: expected object")
    require(not (set(obj) - set(keys.split())), f"{where}: unknown fields {set(obj)-set(keys.split())}")


def number(v, low, high, where, integer=False):
    require(type(v) in ((int,) if integer else (int, float)) and math.isfinite(v)
            and low <= v <= high, f"{where}: expected {low}..{high}")


def command(argv):
    require(isinstance(argv, list) and 1 <= len(argv) <= 256 and
            all(isinstance(x, str) and "\0" not in x and len(x) <= 32768 for x in argv), "argv: nonempty string array")
    require(bool(argv[0]), "argv[0] empty")
    require(Path(argv[0]).suffix.lower() not in {".bat", ".cmd"},
            "Use executable .exe or explicit PowerShell -File for batch tools")


def validate_spec(spec):
    check_keys(spec, "version name tasks total_timeout_s log_bytes resources resource_dir min_free_bytes", "job")
    require(spec.get("version") == 1, "version must be 1")
    require(isinstance(spec.get("name"), str) and 1 <= len(spec["name"]) <= 120, "name length 1..120")
    spec.setdefault("total_timeout_s", 86400)
    spec.setdefault("log_bytes", 262144)
    spec.setdefault("min_free_bytes", 0)
    spec.setdefault("resources", [])
    spec.setdefault("resource_dir", str(Path(tempfile.gettempdir()) / "long-task-runner-resources"))
    number(spec["total_timeout_s"], .1, 2592000, "total_timeout_s")
    number(spec["log_bytes"], 1024, 16777216, "log_bytes", True)
    number(spec["min_free_bytes"], 0, 10**16, "min_free_bytes", True)
    require(Path(spec["resource_dir"]).is_absolute(), "resource_dir must be absolute")
    require(isinstance(spec["resources"], list) and len(spec["resources"]) <= 16 and
            all(isinstance(x, str) and re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", x) for x in spec["resources"]), "resources: at most 16 simple keys")
    require(isinstance(spec.get("tasks"), list) and 1 <= len(spec["tasks"]) <= 1000, "tasks: 1..1000")
    ids = set()
    for t in spec["tasks"]:
        check_keys(t, "id argv cwd timeout_s effect replay_safe retry launch_limit env artifacts success_basis", "task")
        require(isinstance(t.get("id"), str) and re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", t["id"]) and t["id"] not in ids, "task ids must be unique simple keys")
        ids.add(t["id"])
        command(t.get("argv"))
        require(isinstance(t.get("cwd"), str) and Path(t["cwd"]).is_absolute() and Path(t["cwd"]).is_dir(), "cwd must be existing absolute directory")
        number(t.get("timeout_s"), .1, 2592000, "task timeout_s")
        require(t.get("effect") in {"local", "read_only", "external"}, "effect required: local/read_only/external")
        t.setdefault("replay_safe", False)
        require(type(t["replay_safe"]) is bool, "replay_safe must be boolean")
        require(not (t["effect"] == "external" and t["replay_safe"]), "external tasks cannot auto-replay")
        t.setdefault("launch_limit", 3)
        number(t["launch_limit"], 1, 20, "launch_limit", True)
        t.setdefault("retry", {})
        r = t["retry"]
        check_keys(r, "max_attempts exit_codes delay_s", "retry")
        r.setdefault("max_attempts", 1)
        r.setdefault("exit_codes", [])
        r.setdefault("delay_s", 5)
        number(r["max_attempts"], 1, 5, "max_attempts", True)
        number(r["delay_s"], .05, 3600, "delay_s")
        require(isinstance(r["exit_codes"], list) and len(r["exit_codes"]) <= 32 and
                all(type(x) is int and x != 0 for x in r["exit_codes"]), "retry exit_codes must exclude 0")
        require(r["max_attempts"] <= t["launch_limit"], "max_attempts exceeds launch_limit")
        require(r["max_attempts"] == 1 or (t["replay_safe"] and t["effect"] != "external" and r["exit_codes"]), "retries need safe replay and explicit exit codes")
        t.setdefault("env", {})
        require(isinstance(t["env"], dict) and len(t["env"]) <= 64 and all(
            isinstance(k, str) and isinstance(v, str) and "=" not in k and "\0" not in k+v for k, v in t["env"].items()), "env must be a string mapping")
        t.setdefault("artifacts", [])
        require(isinstance(t["artifacts"], list) and len(t["artifacts"]) <= 100, "artifacts: at most 100")
        require(t["artifacts"] or isinstance(t.get("success_basis"), str) and len(t["success_basis"].strip()) >= 8,
                "Use artifact checks or explain the exit-code success contract in success_basis")
        for a in t["artifacts"]:
            check_keys(a, "kind path min_bytes fresh sha256 required equals min_duration_s max_duration_s argv timeout_s read_only", "artifact")
            require(a.get("kind") in {"file", "json", "wav", "sha256", "command"}, "unknown artifact kind")
            if a["kind"] == "command":
                command(a.get("argv"))
                require(a.get("read_only") is True, "validator command requires read_only: true")
                number(a.get("timeout_s"), .1, 300, "validator timeout_s")
                continue
            require(isinstance(a.get("path"), str) and bool(a["path"]), "artifact path required")
            a.setdefault("min_bytes", 1)
            a.setdefault("fresh", True)
            number(a["min_bytes"], 1, 10**16, "min_bytes", True)
            require(type(a["fresh"]) is bool, "fresh must be boolean")
            if a["kind"] == "sha256":
                require(isinstance(a.get("sha256"), str) and re.fullmatch(r"[0-9a-fA-F]{64}", a["sha256"]), "sha256 required")
            if a["kind"] == "json":
                require(isinstance(a.get("required", []), list) and all(isinstance(k, str) for k in a.get("required", [])), "required: list of top-level JSON keys")
                require(isinstance(a.get("equals", {}), dict), "equals: JSON key/value object")
            if a["kind"] == "wav":
                number(a.get("min_duration_s", .001), .000001, 2592000, "min_duration_s")
                number(a.get("max_duration_s", 2592000), .000001, 2592000, "max_duration_s")
    return spec


def fingerprint(spec):
    return hashlib.sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def artifact_path(t, a):
    p = Path(a["path"])
    return p if p.is_absolute() else Path(t["cwd"]) / p


def signatures(t):
    found = {}
    for a in t["artifacts"]:
        if a["kind"] != "command":
            p = artifact_path(t, a)
            try:
                st = p.stat()
                found[str(p)] = [st.st_size, st.st_mtime_ns]
            except FileNotFoundError:
                found[str(p)] = None
    return found


class WindowsJob:
    """Gate child execution until assigned; KILL_ON_JOB_CLOSE contains descendants."""
    def __init__(self):
        from ctypes import wintypes as w
        class BASIC(ctypes.Structure):
            _fields_ = [("p", ctypes.c_int64), ("j", ctypes.c_int64), ("flags", w.DWORD),
                        ("min", ctypes.c_size_t), ("max", ctypes.c_size_t), ("active", w.DWORD),
                        ("affinity", ctypes.c_size_t), ("priority", w.DWORD), ("scheduling", w.DWORD)]
        class IO(ctypes.Structure):
            _fields_ = [(n, ctypes.c_uint64) for n in ("ro", "wo", "oo", "rb", "wb", "ob")]
        class EXT(ctypes.Structure):
            _fields_ = [("basic", BASIC), ("io", IO), ("process_memory", ctypes.c_size_t),
                        ("job_memory", ctypes.c_size_t), ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        self.k.CreateJobObjectW.argtypes = [ctypes.c_void_p, w.LPCWSTR]
        self.k.CreateJobObjectW.restype = w.HANDLE
        self.k.SetInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD]
        self.k.SetInformationJobObject.restype = w.BOOL
        self.k.AssignProcessToJobObject.argtypes = [w.HANDLE, w.HANDLE]
        self.k.AssignProcessToJobObject.restype = w.BOOL
        self.k.CloseHandle.argtypes = [w.HANDLE]
        self.h = self.k.CreateJobObjectW(None, None)
        if not self.h:
            raise ctypes.WinError(ctypes.get_last_error())
        info = EXT()
        info.basic.flags = 0x2000
        if not self.k.SetInformationJobObject(self.h, 9, ctypes.byref(info), ctypes.sizeof(info)):
            self.close()
            raise ctypes.WinError(ctypes.get_last_error())

    def assign(self, p):
        if not self.k.AssignProcessToJobObject(self.h, int(p._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.h:
            self.k.CloseHandle(self.h)
            self.h = None


def execute(argv, cwd, env, timeout, stop, log, on_pid=None):
    """Always drains output; timeout is wall time, silence is never failure."""
    job, p = None, None
    started = time.monotonic()
    try:
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        if os.name == "nt":
            job = WindowsJob()
            actual = [sys.executable, SCRIPT, "_child", "--", *argv]
        else:
            actual = argv
        p = subprocess.Popen(actual, cwd=cwd, env={**os.environ, **env}, stdin=subprocess.PIPE if job else subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=flags,
                             start_new_session=os.name != "nt")
        if job:
            job.assign(p)
            p.stdin.write(b"G")
            p.stdin.close()
        if on_pid:
            on_pid(p.pid)
        def drain():
            try:
                while chunk := p.stdout.read(16384):
                    log.write(chunk)
            except (OSError, ValueError):
                pass
        thread = threading.Thread(target=drain, daemon=True)
        thread.start()
        reason = None
        while p.poll() is None:
            reason = stop()
            if reason or log.error:
                reason = reason or "log_error"
                break
            if time.monotonic() - started >= timeout:
                reason = "timed_out"
                break
            time.sleep(.1)
        if job:
            job.close()
        else:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(p.pid, signal.SIGKILL)
        p.wait(timeout=10)
        thread.join(timeout=5)
        if thread.is_alive():
            raise Problem("E_PIPE", "Output pipe did not close after process tree termination")
        if log.error:
            raise Problem("E_LOG_IO", log.error)
        return p.returncode, reason
    finally:
        if job:
            job.close()
        if p:
            if p.poll() is None:
                if os.name != "nt":
                    with contextlib.suppress(ProcessLookupError):
                        os.killpg(p.pid, signal.SIGKILL)
                with contextlib.suppress(OSError):
                    p.kill()
                with contextlib.suppress(subprocess.TimeoutExpired):
                    p.wait(timeout=5)
            if p.stdout:
                p.stdout.close()
            if p.stdin and not p.stdin.closed:
                p.stdin.close()


def validate_artifacts(t, baseline, log, stop, recheck=False):
    paths = []
    for a in t["artifacts"]:
        if stop():
            raise Problem("E_STOP", stop())
        if a["kind"] == "command":
            rc, reason = execute(a["argv"], t["cwd"], t["env"], a["timeout_s"], stop, log)
            if reason or rc != 0:
                raise Problem("E_VALIDATION", f"Read-only validator: exit={rc}, reason={reason}")
            continue
        p = artifact_path(t, a)
        if not p.is_file() or p.stat().st_size < a["min_bytes"]:
            raise Problem("E_ARTIFACT", f"Missing, empty or undersized: {p}")
        st = p.stat()
        if not recheck and a["fresh"] and baseline.get(str(p)) == [st.st_size, st.st_mtime_ns]:
            raise Problem("E_STALE_ARTIFACT", str(p))
        if a["kind"] == "json":
            try:
                obj = read(p)
                if not isinstance(obj, dict) or any(k not in obj for k in a.get("required", [])) or any(k not in obj or obj[k] != v for k, v in a.get("equals", {}).items()):
                    raise ValueError("JSON keys/values do not match")
            except (ValueError, OSError) as e:
                raise Problem("E_ARTIFACT_JSON", f"{p}: {e}") from e
        elif a["kind"] == "wav":
            try:
                with wave.open(str(p), "rb") as w:
                    duration = w.getnframes() / w.getframerate()
                    if not a.get("min_duration_s", .001) <= duration <= a.get("max_duration_s", 2592000):
                        raise ValueError(f"duration={duration}")
                    expected = w.getnframes() * w.getnchannels() * w.getsampwidth()
                    actual = 0
                    while b := w.readframes(65536):
                        actual += len(b)
                        if stop():
                            raise Problem("E_STOP", stop())
                    if actual != expected:
                        raise ValueError("truncated PCM data")
            except (wave.Error, EOFError, ValueError) as e:
                raise Problem("E_ARTIFACT_WAV", f"{p}: {e}") from e
        elif a["kind"] == "sha256":
            h = hashlib.sha256()
            with open(p, "rb") as f:
                while chunk := f.read(1048576):
                    h.update(chunk)
                    if stop():
                        raise Problem("E_STOP", stop())
            if h.hexdigest() != a["sha256"].lower():
                raise Problem("E_ARTIFACT_HASH", str(p))
        paths.append(str(p.resolve()))
    return paths


def save_state(job, state, message=None):
    state["revision"] += 1
    state["updated_at"] = time.time()
    if message:
        state["change"] = message[:200]
        task_id = state.get("current")
        phase = next((t["status"] for t in state["tasks"] if t["id"] == task_id), state["status"])
        history = state.setdefault("change_history", [])
        history.append({"revision": state["revision"], "task": task_id, "phase": phase, "summary": state["change"]})
        state["changes_dropped"] = state.get("changes_dropped", 0) + max(0, len(history)-16)
        state["change_history"] = history[-16:]
    atomic(job / "state.json", state)
    if message:
        log = RollingLog(job / "events.jsonl", 65536, 1)
        log.write((json.dumps({"at": state["updated_at"], "revision": state["revision"], "status": state["status"], "change": state["change"]}, ensure_ascii=False) + "\n").encode())
        if log.error:
            raise Problem("E_LOG_IO", log.error)


def snapshot(job, since=None):
    state = read(job / "state.json")
    active = held(job / "worker.lock")
    effective = state["status"]
    if effective in ACTIVE and not active and time.time() - state["updated_at"] > 10:
        effective = "interrupted"
    tasks = state["tasks"]
    out = {"job": str(job), "status": effective, "revision": state["revision"],
           "changed": since is None or since != state["revision"] or effective != state["status"],
           "done": sum(t["status"] == "succeeded" for t in tasks), "total": len(tasks),
           "current": state.get("current"), "worker_active": active,
           "cancel_requested": (job / "cancel.json").exists(),
           "failures": [t["failure"] for t in tasks if t.get("failure")][:8],
           "artifacts": [p for t in tasks for p in t.get("artifacts", [])][:8],
           "state_path": str(job / "state.json"), "log_path": str(job / "process.log")}
    if out["changed"]:
        out["change"] = state.get("change", "")
    if since is not None and out["changed"]:
        history = state.get("change_history", [])
        groups = {}
        for event in history:
            if event["revision"] > since:
                key = event["task"] or "(job)"
                prior = groups.pop(key, {})
                groups[key] = {"task": event["task"], "phase": event["phase"], "events": prior.get("events", 0)+1, "summary": event["summary"]}
        out["delta"] = {"from_revision": since, "groups": list(groups.values())[-4:],
                        "omitted_groups": max(0, len(groups)-4),
                        "history_truncated": bool(history and state.get("changes_dropped") and since < history[0]["revision"])}
    if state.get("error"):
        out["error"] = state["error"]
    return out


def failure(state, rec, code, detail):
    state["failure_count"] += 1
    rec["failure"] = {"id": f"F{state['failure_count']:04d}", "code": code, "detail": str(detail)[:240]}
    state.setdefault("failure_history", []).append(dict(rec["failure"]))
    state["failure_history"] = state["failure_history"][-32:]


def worker(job, token):
    worker_lock = Lock(job / "worker.lock")
    if not worker_lock.acquire():
        return
    locks = []
    state = None
    try:
        with Lock(job / "control.lock"):
            state = read(job / "state.json")
            if state["token"] != token:
                return
            spec = validate_spec(read(job / "spec.json"))
            if fingerprint(spec) != state["spec_hash"]:
                raise Problem("E_SPEC_CHANGED", "Frozen spec changed; no work executed")
            state["worker_pid"] = os.getpid()
            state["status"] = "running"
            save_state(job, state, "worker started")
        start = time.monotonic()
        log = RollingLog(job / "process.log", spec["log_bytes"])
        def stop():
            if (job / "cancel.json").exists():
                return "cancelled"
            if time.monotonic() - start >= spec["total_timeout_s"]:
                return "timed_out"
            return None
        for key in sorted(set(spec["resources"])):
            lock = Lock(Path(spec["resource_dir"]) / (key + ".lock"))
            if not lock.acquire():
                state["status"] = "waiting_resource"
                save_state(job, state, "waiting for resource " + key)
                while not lock.acquire():
                    if reason := stop():
                        state["status"] = reason
                        save_state(job, state, reason + " while waiting for resource")
                        return
                    time.sleep(.2)
            locks.append(lock)
        state["status"] = "running"
        for t, rec in zip(spec["tasks"], state["tasks"]):
            if rec["status"] == "succeeded":
                try:
                    validate_artifacts(t, {}, log, stop, recheck=True)
                except Problem as e:
                    raise Problem("E_COMPLETED_INVALID", f"{t['id']}: {e.detail}") from e
                continue
            if reason := stop():
                state["status"] = reason
                save_state(job, state, reason)
                return
            if spec["min_free_bytes"]:
                import shutil
                if shutil.disk_usage(t["cwd"]).free < spec["min_free_bytes"]:
                    raise Problem("E_DISK_SPACE", f"Free space below min_free_bytes in {t['cwd']}")
            state["current"] = t["id"]
            for local_attempt in range(t["retry"]["max_attempts"]):
                if reason := stop():
                    state["status"] = reason
                    save_state(job, state, reason)
                    return
                if rec["launches"] >= t["launch_limit"]:
                    raise Problem("E_LAUNCH_LIMIT", t["id"])
                baseline = signatures(t)
                rec.update(status="running", launches=rec["launches"]+1, started_at=time.time(), failure=None)
                save_state(job, state, f"{t['id']} started (launch {rec['launches']})")
                def on_pid(pid):
                    rec["pid"] = pid
                    save_state(job, state)
                rc, reason = execute(t["argv"], t["cwd"], t["env"], t["timeout_s"], stop, log, on_pid)
                rec["pid"] = None
                rec["exit_code"] = rc
                rec["ended_at"] = time.time()
                if reason:
                    rec["status"] = reason
                    state["status"] = reason if reason in TERMINAL else "failed"
                    failure(state, rec, "E_"+reason.upper(), "Process tree stopped; automatic timeout replay disabled")
                    save_state(job, state, f"{t['id']}: {reason}")
                    return
                if rc == 0:
                    try:
                        rec["artifacts"] = validate_artifacts(t, baseline, log, stop)
                    except Problem as e:
                        rec["status"] = "failed"
                        state["status"] = stop() or "failed"
                        failure(state, rec, e.code, e.detail)
                        save_state(job, state, f"{t['id']}: validation failed")
                        return
                    rec["status"] = "succeeded"
                    save_state(job, state, f"{t['id']}: verified")
                    break
                retry = rc in t["retry"]["exit_codes"] and local_attempt+1 < t["retry"]["max_attempts"] and rec["launches"] < t["launch_limit"]
                if not retry:
                    rec["status"], state["status"] = "failed", "failed"
                    failure(state, rec, "E_EXIT", f"exit code {rc}")
                    save_state(job, state, f"{t['id']}: failed")
                    return
                rec["status"] = "retry_wait"
                save_state(job, state, f"{t['id']}: retryable exit {rc}")
                end = time.monotonic() + min(3600, t["retry"]["delay_s"] * 2**local_attempt)
                while time.monotonic() < end:
                    if reason := stop():
                        state["status"] = reason
                        save_state(job, state, reason + " during retry delay")
                        return
                    time.sleep(.1)
        state["status"], state["current"] = "succeeded", None
        save_state(job, state, "all commands exited successfully and checks passed; final review still required")
    except BaseException as e:
        if state:
            state["status"] = "failed"
            error_record = {}
            failure(state, error_record, getattr(e, "code", "E_WORKER"), str(e))
            state["error"] = error_record["failure"]
            with contextlib.suppress(Exception):
                save_state(job, state, "worker stopped on error")
    finally:
        for lock in reversed(locks):
            lock.close()
        worker_lock.close()


def spawn_worker(job, state):
    flags = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0
    p = subprocess.Popen([sys.executable, SCRIPT, "_worker", str(job), state["token"]],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=flags, start_new_session=os.name != "nt", close_fds=True)
    # It is deliberately detached; no model/API/wakeup command exists here.
    return p.pid


def launch(job, spec_path=None, resume=False, replay=False):
    job.mkdir(parents=True, exist_ok=True)
    with Lock(job / "control.lock"):
        exists = (job / "state.json").exists()
        if exists:
            state = read(job / "state.json")
            spec = validate_spec(read(job / "spec.json"))
            if fingerprint(spec) != state["spec_hash"]:
                raise Problem("E_SPEC_CHANGED", "Frozen spec hash mismatch")
            if spec_path and fingerprint(validate_spec(read(spec_path))) != state["spec_hash"]:
                raise Problem("E_ID_CONFLICT", "Job directory already belongs to a different spec")
            if not resume or held(job / "worker.lock") or state["status"] == "succeeded":
                return
            if state["status"] == "starting" and time.time()-state["updated_at"] < 10:
                return
            if os.name != "nt" and state["status"] in ACTIVE:
                raise Problem("E_RECOVERY_UNVERIFIED", "Crashed POSIX worker may leave descendants. Verify cleanup before creating another job.")
            require(state["generation"] < 6, "resume generation limit reached")
            for t, rec in zip(spec["tasks"], state["tasks"]):
                if rec["status"] != "succeeded" and rec["launches"]:
                    if not replay or not t["replay_safe"] or t["effect"] == "external":
                        raise Problem("E_REPLAY_UNSAFE", f"{t['id']}: requires safe local/read-only replay and --replay-safe")
                    if rec["launches"] >= t["launch_limit"]:
                        raise Problem("E_LAUNCH_LIMIT", t["id"])
                    rec["status"], rec["failure"] = "pending", None
            state["generation"] += 1
            state.pop("error", None)
            (job / "cancel.json").unlink(missing_ok=True)
        else:
            if resume:
                raise Problem("E_NOT_FOUND", "No job to resume")
            spec = validate_spec(read(spec_path))
            state = {"schema": 1, "name": spec["name"], "spec_hash": fingerprint(spec), "generation": 1,
                     "revision": 0, "failure_count": 0, "created_at": time.time(),
                     "tasks": [{"id": t["id"], "status": "pending", "launches": 0} for t in spec["tasks"]]}
            atomic(job / "spec.json", spec)
        state["status"], state["token"] = "starting", uuid.uuid4().hex
        save_state(job, state, "launch requested")
        try:
            spawn_worker(job, state)
        except Exception as e:
            state["status"] = "failed"
            state["error"] = {"code": "E_SPAWN", "detail": str(e)[:240]}
            save_state(job, state, "worker could not start")
            raise


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "_child":
        if sys.stdin.buffer.read(1) != b"G":
            return 125
        try:
            return subprocess.call(sys.argv[3:], stdin=subprocess.DEVNULL)
        except OSError as e:
            print(f"E_EXEC: {e}", file=sys.stderr)
            return 127
    if len(sys.argv) > 1 and sys.argv[1] == "_worker":
        worker(Path(sys.argv[2]).resolve(), sys.argv[3])
        return 0
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", action="version", version=VERSION)
    sub = p.add_subparsers(dest="action", required=True)
    for action in ("start", "status", "wait", "cancel", "resume", "logs"):
        a = sub.add_parser(action)
        a.add_argument("--job", required=True, type=Path)
        if action == "start":
            a.add_argument("--spec", required=True, type=Path)
        if action in {"status", "wait"}:
            a.add_argument("--since", type=int)
        if action == "wait":
            a.add_argument("--seconds", type=float, default=25)
        if action == "resume":
            a.add_argument("--replay-safe", action="store_true")
        if action == "logs":
            a.add_argument("--bytes", type=int, default=4096)
    args = p.parse_args()
    job = args.job.resolve()
    try:
        if args.action == "start":
            launch(job, args.spec)
        elif args.action == "resume":
            launch(job, resume=True, replay=args.replay_safe)
        elif args.action == "cancel":
            with Lock(job / "control.lock"):
                state = read(job / "state.json")
                if state["status"] not in TERMINAL or held(job / "worker.lock"):
                    atomic(job / "cancel.json", {"requested_at": time.time()})
        elif args.action == "logs":
            require(1 <= args.bytes <= 16384, "logs --bytes must be 1..16384")
            path = job / "process.log"
            if path.exists():
                with open(path, "rb") as f:
                    f.seek(max(0, path.stat().st_size-args.bytes))
                    emit({"log_path": str(path), "tail": f.read(args.bytes).decode("utf-8", "replace")})
            else:
                emit({"log_path": str(path), "tail": ""})
            return 0
        elif args.action == "wait":
            require(math.isfinite(args.seconds) and 0 <= args.seconds <= 55, "wait --seconds must be 0..55; obey the caller tool limit")
            end = time.monotonic() + args.seconds
            while True:
                snap = snapshot(job, args.since)
                if snap["status"] in TERMINAL or time.monotonic() >= end:
                    break
                time.sleep(min(.25, max(0, end-time.monotonic())))
        out = snapshot(job, getattr(args, "since", None))
        emit(out)
        return 0 if out["status"] == "succeeded" or args.action in {"start", "status", "cancel", "resume"} else (3 if out["status"] in ACTIVE else 2)
    except (Problem, OSError, ValueError, KeyError, TypeError) as e:
        emit({"error": getattr(e, "code", "E_IO"), "detail": str(e)[:400], "job": str(job)})
        return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
