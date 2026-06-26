import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

MONITOR_SCRIPT = SCRIPT_DIR / "monitor.py"
TAMPER_SCRIPT = SCRIPT_DIR / "tamper_simulator.py"
EVENT_LOGGER_SCRIPT = SCRIPT_DIR / "event_logger.py"
RECONCILE_DAEMON_SCRIPT = SCRIPT_DIR / "reconcile_daemon.py"

MONITOR_FILES = [
    "SOUL.md",
    "USER.md",
    "HEARTBEAT.md",
    "MEMORY.md",
    "TOOLS.md",
    "AGENTS.md",
]


def now_text() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def resolve_python_executable() -> str:
    if sys.executable:
        return sys.executable
    if shutil.which("python3"):
        return "python3"
    if shutil.which("python"):
        return "python"
    return "python3"


def resolve_runtime_paths(monitor_dir_arg: Optional[str], output_dir_arg: Optional[str]) -> Dict[str, Path]:
    monitor_env = os.getenv("GUARDIAN_MONITOR_DIR", "").strip()
    output_env = os.getenv("GUARDIAN_OUTPUT_DIR", "").strip()

    monitor_dir = (
        Path(monitor_dir_arg).expanduser()
        if monitor_dir_arg
        else (Path(monitor_env).expanduser() if monitor_env else (SKILL_DIR.parent.parent))
    )
    output_dir = (
        Path(output_dir_arg).expanduser()
        if output_dir_arg
        else (Path(output_env).expanduser() if output_env else SKILL_DIR)
    )

    monitor_dir = monitor_dir.resolve()
    output_dir = output_dir.resolve()
    return {
        "monitor_dir": monitor_dir,
        "output_dir": output_dir,
        "backup_dir": output_dir / "cognitive_file_backups",
        "state_file": output_dir / "cognitive_file_backups" / "monitor_state.json",
        "log_json": output_dir / "change_log.json",
        "archive_json": output_dir / "change_log_labeled.json",
        "log_md": output_dir / "change_log.md",
        "archive_md": output_dir / "change_log_labeled.md",
        "reconcile_cron_file": output_dir / "no0_reconcile_cron.json",
        "heartbeat_log_file": output_dir / "heartbeat_log.txt",
        "legacy_reconcile_cron_file": SKILL_DIR / "no0_reconcile_cron.json",
        "legacy_heartbeat_log_file": SKILL_DIR.parent.parent / "heartbeat_log.txt",
        "pid_file": output_dir / "no0_processes.json",
    }


def file_md5(file_path: Path) -> str:
    digest = hashlib.md5()
    with open(file_path, "rb") as handle:
        while True:
            chunk = handle.read(8192)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def normalize_monitor_file_name(name: str) -> str:
    raw = name.strip()
    if not raw:
        raise ValueError("文件名不能为空")
    if "." not in raw:
        raw = f"{raw}.md"

    lowered_map = {item.lower(): item for item in MONITOR_FILES}
    candidate = lowered_map.get(raw.lower())
    if candidate:
        return candidate

    raise ValueError(f"不支持的文件名: {name}")


def read_json_file(file_path: Path, default: Any) -> Any:
    if not file_path.exists():
        return default
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return default


def write_json_file(file_path: Path, payload: Any) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def load_pid_registry(pid_file: Path) -> Dict[str, Any]:
    content = read_json_file(pid_file, {})
    if isinstance(content, dict):
        return content
    return {}


def save_pid_registry(pid_file: Path, payload: Dict[str, Any]) -> None:
    write_json_file(pid_file, payload)


def is_process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    except Exception:
        # Windows + UNC 场景下 os.kill 可能抛出 SystemError，统一视为不存活
        return False


def terminate_process(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return False
    except Exception:
        # 继续尝试平台兜底方式结束进程。
        pass

    for _ in range(20):
        if not is_process_alive(pid):
            return True
        time.sleep(0.1)

    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except Exception:
            pass
    else:
        try:
            os.kill(pid, signal.SIGKILL)
        except Exception:
            pass
    try:
        return not is_process_alive(pid)
    except Exception:
        return False


def list_process_table() -> List[Tuple[int, str]]:
    entries: List[Tuple[int, str]] = []
    current_pid = os.getpid()

    if os.name == "nt":
        ps_script = (
            "$ErrorActionPreference='SilentlyContinue'; "
            "Get-CimInstance Win32_Process | "
            "Select-Object ProcessId, CommandLine | ConvertTo-Json -Compress"
        )
        try:
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=10,
            )
            payload = proc.stdout.strip()
            if payload and payload.lower() != "null":
                parsed = json.loads(payload)
                rows = [parsed] if isinstance(parsed, dict) else parsed
                if isinstance(rows, list):
                    for row in rows:
                        if not isinstance(row, dict):
                            continue
                        try:
                            pid = int(row.get("ProcessId", 0))
                        except Exception:
                            continue
                        if pid <= 0 or pid == current_pid:
                            continue
                        cmdline = str(row.get("CommandLine") or "").strip()
                        if not cmdline:
                            continue
                        entries.append((pid, cmdline))
        except Exception:
            pass
        return entries

    proc_dir = Path("/proc")
    if proc_dir.exists() and proc_dir.is_dir():
        try:
            for item in proc_dir.iterdir():
                if not item.name.isdigit():
                    continue
                pid = int(item.name)
                if pid <= 0 or pid == current_pid:
                    continue
                try:
                    raw = (item / "cmdline").read_bytes()
                except Exception:
                    continue
                if not raw:
                    continue
                cmdline = raw.replace(b"\x00", b" ").decode("utf-8", errors="replace").strip()
                if cmdline:
                    entries.append((pid, cmdline))
        except Exception:
            pass

    if entries:
        return entries

    try:
        proc = subprocess.run(
            ["ps", "-ax", "-o", "pid=", "-o", "command="],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=10,
        )
        for line in proc.stdout.splitlines():
            text = line.strip()
            if not text:
                continue
            parts = text.split(maxsplit=1)
            if len(parts) != 2:
                continue
            try:
                pid = int(parts[0])
            except ValueError:
                continue
            if pid <= 0 or pid == current_pid:
                continue
            cmdline = parts[1].strip()
            if cmdline:
                entries.append((pid, cmdline))
    except Exception:
        pass

    return entries


def find_script_processes(script_markers: List[str]) -> Dict[int, str]:
    markers = [item.lower() for item in script_markers if item]
    if not markers:
        return {}

    matched: Dict[int, str] = {}
    for pid, cmdline in list_process_table():
        lowered = cmdline.lower()
        if any(marker in lowered for marker in markers):
            matched[pid] = cmdline
    return matched


def parse_backup_version(path_obj: Path) -> int:
    token = path_obj.name.rsplit(".v", 1)[-1]
    try:
        return int(token)
    except ValueError:
        return -1


def list_backup_versions(backup_dir: Path, file_name: str) -> List[Path]:
    candidates: List[Path] = []
    for entry in backup_dir.glob(f"{file_name}.v*"):
        if entry.name.endswith(".meta"):
            continue
        version = parse_backup_version(entry)
        if version >= 0:
            candidates.append(entry)
    candidates.sort(key=parse_backup_version)
    return candidates


def get_latest_backup(backup_dir: Path, file_name: str) -> Optional[Path]:
    versions = list_backup_versions(backup_dir, file_name)
    if not versions:
        return None
    return versions[-1]


def set_file_read_only(file_path: Path) -> None:
    current_mode = file_path.stat().st_mode
    readonly_mode = current_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    os.chmod(file_path, readonly_mode)


def dedupe_paths(paths: List[Path]) -> List[Path]:
    result: List[Path] = []
    seen: set = set()
    for path_obj in paths:
        key = str(path_obj.resolve()) if path_obj.exists() else str(path_obj)
        if key in seen:
            continue
        seen.add(key)
        result.append(path_obj)
    return result


def resolve_core_source_file(directory: Path, target_name: str) -> Optional[Path]:
    exact = directory / target_name
    if exact.exists() and exact.is_file():
        return exact

    lowered_target = target_name.lower()
    for entry in directory.iterdir():
        if not entry.is_file():
            continue
        if entry.name.lower() == lowered_target:
            return entry
    return None


def discover_core_source_dir() -> Optional[Path]:
    env_dir = os.getenv("NO0_CORE_FILES_DIR", "").strip()
    root_dir = SKILL_DIR.parent.parent
    raw_candidates: List[Path] = []
    if env_dir:
        raw_candidates.append(Path(env_dir).expanduser())
    raw_candidates.extend(
        [
            root_dir / "核心文件",
            SKILL_DIR.parent / "核心文件",
            SKILL_DIR / "核心文件",
            root_dir / "core-files",
            root_dir / "core_files",
            root_dir / "cognitive_files",
            root_dir,
        ]
    )
    candidate_dirs = dedupe_paths(raw_candidates)

    best_dir: Optional[Path] = None
    best_matched = -1
    for candidate in candidate_dirs:
        if not candidate.exists() or not candidate.is_dir():
            continue
        matched = 0
        for target_name in MONITOR_FILES:
            if resolve_core_source_file(candidate, target_name):
                matched += 1
        if matched > best_matched:
            best_matched = matched
            best_dir = candidate

    if best_matched > 0:
        return best_dir
    return None


def ensure_core_files(monitor_dir: Path) -> Tuple[List[str], List[str], Optional[Path]]:
    monitor_dir.mkdir(parents=True, exist_ok=True)

    existing_ci: Dict[str, Path] = {}
    for entry in monitor_dir.iterdir():
        if entry.is_file():
            existing_ci[entry.name.lower()] = entry

    missing: List[str] = []
    copied: List[str] = []

    for target_name in MONITOR_FILES:
        target_path = monitor_dir / target_name
        if target_path.exists():
            continue

        in_assets_with_other_case = existing_ci.get(target_name.lower())
        if in_assets_with_other_case and in_assets_with_other_case.exists():
            shutil.copy2(in_assets_with_other_case, target_path)
            copied.append(target_name)
            continue

        missing.append(target_name)

    source_dir: Optional[Path] = None
    if missing:
        source_dir = discover_core_source_dir()
        if source_dir:
            unresolved: List[str] = []
            for target_name in missing:
                source_file = resolve_core_source_file(source_dir, target_name)
                if source_file is None:
                    unresolved.append(target_name)
                    continue
                shutil.copy2(source_file, monitor_dir / target_name)
                copied.append(target_name)
            missing = unresolved

    return copied, missing, source_dir


def spawn_background_process(command: List[str], cwd: Path, log_file: Path) -> int:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_handle = open(log_file, "a", encoding="utf-8")

    popen_kwargs: Dict[str, Any] = {
        "cwd": str(cwd),
        "stdout": log_handle,
        "stderr": subprocess.STDOUT,
    }
    if os.name == "nt":
        creation_flags = 0
        creation_flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        creation_flags |= getattr(subprocess, "DETACHED_PROCESS", 0)
        popen_kwargs["creationflags"] = creation_flags
    else:
        popen_kwargs["start_new_session"] = True

    process = subprocess.Popen(command, **popen_kwargs)
    log_handle.close()
    return int(process.pid)


def collect_log_records(log_json: Path) -> List[Dict[str, Any]]:
    raw = read_json_file(log_json, [])
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    if isinstance(raw, dict):
        events = raw.get("events", [])
        if isinstance(events, list):
            return [item for item in events if isinstance(item, dict)]
    return []


def is_pending_level(value: Any) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in {"", "null"}


def resolve_record_level(record: Dict[str, Any]) -> Any:
    level = record.get("level")
    if is_pending_level(level):
        target = record.get("target")
        if not is_pending_level(target):
            return target
    return level


def summarize_record_counts(records: List[Dict[str, Any]]) -> Dict[str, int]:
    labeled = 0
    unlabeled = 0
    for item in records:
        level = resolve_record_level(item)
        if is_pending_level(level):
            unlabeled += 1
        else:
            labeled += 1
    return {
        "total": len(records),
        "labeled": labeled,
        "unlabeled": unlabeled,
    }


def print_header(title: str) -> None:
    print("\n" + title)
    print("=" * max(16, len(title)))


def parse_markdown_entries(content: str) -> List[str]:
    entries: List[str] = []
    current: List[str] = []
    header_pattern = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}T")

    for line in content.splitlines():
        if header_pattern.match(line) and current:
            entries.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)

    if current:
        entries.append("\n".join(current).strip())
    return [entry for entry in entries if entry]


def wait_monitor_baseline_ready(backup_dir: Path, timeout_seconds: float = 10.0) -> bool:
    """等待 monitor 完成 v1 基线备份，避免 tamper 首次写入被基线吞掉。"""
    required_files = [backup_dir / f"{name}.v1" for name in MONITOR_FILES]
    deadline = time.time() + max(1.0, float(timeout_seconds))

    while time.time() < deadline:
        if all(path.exists() for path in required_files):
            return True
        time.sleep(0.2)

    return all(path.exists() for path in required_files)


def normalize_reconcile_interval(raw_value: Any) -> int:
    try:
        return max(30, int(raw_value))
    except Exception:
        return 120


def ensure_reconcile_cron(interval_seconds: int, runtime: Dict[str, Path]) -> int:
    """确保 Heartbeat 定时任务配置存在，并保持 interval 同步。"""
    interval = normalize_reconcile_interval(interval_seconds)
    daemon_py = SCRIPT_DIR / "reconcile_daemon.py"
    if not daemon_py.exists():
        print("警告：缺少 reconcile_daemon.py，跳过 Heartbeat 定时任务创建")
        return interval

    scheduler_file = runtime["reconcile_cron_file"]
    heartbeat_log_file = runtime["heartbeat_log_file"]
    scheduler = {
        "enabled": True,
        "every_seconds": interval,
        "command": f"python3 {daemon_py} --interval {interval} --log-file {heartbeat_log_file}",
        "log_file": str(heartbeat_log_file),
        "updated_at": now_text(),
    }
    write_json_file(scheduler_file, scheduler)
    print(f"已确保 Heartbeat 定时任务配置：{scheduler_file.name} (interval={interval}s)")
    return interval


def cmd_start(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    reconcile_interval = ensure_reconcile_cron(args.reconcile_interval, runtime)
    monitor_dir = runtime["monitor_dir"]
    output_dir = runtime["output_dir"]
    pid_file = runtime["pid_file"]

    pid_registry = load_pid_registry(pid_file)
    monitor_info = pid_registry.get("monitor", {}) if isinstance(pid_registry, dict) else {}
    monitor_pid = int(monitor_info.get("pid", 0)) if isinstance(monitor_info, dict) else 0
    monitor_running = monitor_pid > 0 and is_process_alive(monitor_pid)

    output_dir.mkdir(parents=True, exist_ok=True)
    python_bin = resolve_python_executable()

    if monitor_running and args.restart:
        terminated = terminate_process(monitor_pid)
        if terminated:
            print(f"monitor 已停止，PID={monitor_pid}")
        else:
            print(f"monitor 停止失败或已退出，PID={monitor_pid}")
        monitor_running = False
        monitor_pid = 0

    monitor_cmd = [
        python_bin,
        str(MONITOR_SCRIPT),
        "--monitor-dir",
        str(monitor_dir),
        "--output-dir",
        str(output_dir),
    ]
    if args.run_once:
        monitor_cmd.append("--run-once")

    if args.foreground:
        if monitor_running:
            print(f"monitor 已在运行，PID={monitor_pid}。前台模式不重复启动。")
            return 0
        print("前台启动 monitor.py")
        print("命令: " + " ".join(monitor_cmd))
        return subprocess.call(monitor_cmd, cwd=str(SCRIPT_DIR))

    monitor_started_now = False
    if monitor_running:
        print(f"monitor 已在运行，PID={monitor_pid}")
        pid_registry["monitor"] = {
            "pid": monitor_pid,
            "started_at": monitor_info.get("started_at", now_text()) if isinstance(monitor_info, dict) else now_text(),
            "log_file": monitor_info.get("log_file", str(output_dir / "monitor_launcher.log")) if isinstance(monitor_info, dict) else str(output_dir / "monitor_launcher.log"),
            "command": monitor_info.get("command", monitor_cmd) if isinstance(monitor_info, dict) else monitor_cmd,
            "monitor_dir": str(monitor_dir),
            "output_dir": str(output_dir),
        }
    else:
        monitor_log = output_dir / "monitor_launcher.log"
        monitor_pid = spawn_background_process(monitor_cmd, SCRIPT_DIR, monitor_log)
        monitor_started_now = True
        pid_registry["monitor"] = {
            "pid": monitor_pid,
            "started_at": now_text(),
            "log_file": str(monitor_log),
            "command": monitor_cmd,
            "monitor_dir": str(monitor_dir),
            "output_dir": str(output_dir),
        }
        print(f"monitor 已启动，PID={monitor_pid}")

    if args.with_tamper:
        if monitor_started_now:
            ready = wait_monitor_baseline_ready(runtime["backup_dir"], timeout_seconds=12.0)
            if ready:
                print("monitor 基线已就绪，开始启动 tamper_simulator")
            else:
                print("警告：monitor 基线就绪超时，tamper 启动后首轮可能少记")

        tamper_info = pid_registry.get("tamper", {}) if isinstance(pid_registry, dict) else {}
        tamper_pid = int(tamper_info.get("pid", 0)) if isinstance(tamper_info, dict) else 0
        tamper_running = tamper_pid > 0 and is_process_alive(tamper_pid)

        if tamper_running and args.restart:
            terminated = terminate_process(tamper_pid)
            if terminated:
                print(f"tamper_simulator 已停止，PID={tamper_pid}")
            else:
                print(f"tamper_simulator 停止失败或已退出，PID={tamper_pid}")
            tamper_running = False

        if tamper_running:
            print(f"tamper_simulator 已在运行，PID={tamper_pid}。如需重启请加 --restart")
        else:
            tamper_events_file = output_dir / "tamper_events.jsonl"
            tamper_cmd = [
                python_bin,
                str(TAMPER_SCRIPT),
                "--monitor-dir",
                str(monitor_dir),
                "--interval",
                str(args.tamper_interval),
                "--iterations",
                str(args.tamper_iterations),
                "--log-file",
                str(tamper_events_file),
                "--strategy",
                str(args.tamper_strategy),
                "--diff-preview-lines",
                str(args.tamper_diff_preview_lines),
            ]
            if args.tamper_targets:
                tamper_cmd.append("--targets")
                tamper_cmd.extend(args.tamper_targets)
            if args.tamper_algorithms:
                tamper_cmd.append("--algorithms")
                tamper_cmd.extend(args.tamper_algorithms)
            if args.tamper_seed is not None:
                tamper_cmd.extend(["--seed", str(args.tamper_seed)])
            if args.tamper_keep_going:
                tamper_cmd.append("--keep-going")

            tamper_log = output_dir / "tamper_launcher.log"
            tamper_pid = spawn_background_process(tamper_cmd, SCRIPT_DIR, tamper_log)
            pid_registry["tamper"] = {
                "pid": tamper_pid,
                "started_at": now_text(),
                "log_file": str(tamper_log),
                "command": tamper_cmd,
                "monitor_dir": str(monitor_dir),
                "output_dir": str(output_dir),
            }
            print(f"tamper_simulator 已启动，PID={tamper_pid}")

    timer_info = pid_registry.get("timer", {}) if isinstance(pid_registry, dict) else {}
    timer_pid = int(timer_info.get("pid", 0)) if isinstance(timer_info, dict) else 0
    timer_running = timer_pid > 0 and is_process_alive(timer_pid)

    if timer_running and args.restart:
        terminated = terminate_process(timer_pid)
        if terminated:
            print(f"reconcile_timer 已停止，PID={timer_pid}")
        else:
            print(f"reconcile_timer 停止失败或已退出，PID={timer_pid}")
        timer_running = False

    if RECONCILE_DAEMON_SCRIPT.exists():
        if timer_running:
            print(f"reconcile_timer 已在运行，PID={timer_pid}")
        else:
            timer_cmd = [
                python_bin,
                str(RECONCILE_DAEMON_SCRIPT),
                "--interval",
                str(reconcile_interval),
                "--log-file",
                str(runtime["heartbeat_log_file"]),
            ]
            timer_log = output_dir / "reconcile_launcher.log"
            timer_pid = spawn_background_process(timer_cmd, SCRIPT_DIR, timer_log)
            pid_registry["timer"] = {
                "pid": timer_pid,
                "started_at": now_text(),
                "log_file": str(timer_log),
                "command": timer_cmd,
                "output_dir": str(output_dir),
            }
            print(f"reconcile_timer 已启动，PID={timer_pid}，interval={reconcile_interval}s")
    else:
        print("警告：缺少 reconcile_daemon.py，定时器未启动")

    save_pid_registry(pid_file, pid_registry)
    print(f"监听目录: {monitor_dir}")
    print(f"输出目录: {output_dir}")
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    scheduler_files = dedupe_paths(
        [runtime["reconcile_cron_file"], runtime["legacy_reconcile_cron_file"]]
    )
    for scheduler_file in scheduler_files:
        if not scheduler_file.exists():
            continue
        try:
            payload = read_json_file(scheduler_file, {})
            if isinstance(payload, dict):
                payload["enabled"] = False
                payload["updated_at"] = now_text()
                write_json_file(scheduler_file, payload)
                print(f"已关闭归档定时任务配置：{scheduler_file.name}")
        except Exception:
            pass

    pid_file = runtime["pid_file"]
    pid_registry = load_pid_registry(pid_file)

    attempted: set = set()
    stopped_any = False

    def stop_pid(pid: int, label: str, source: str, cmdline: Optional[str] = None) -> None:
        nonlocal stopped_any
        if pid <= 0 or pid in attempted:
            return
        attempted.add(pid)

        ok = terminate_process(pid)
        alive = is_process_alive(pid)
        status_text = "已停止" if (ok or not alive) else "未运行或停止失败"
        if ok or not alive:
            stopped_any = True

        extra = f" ({source})"
        if cmdline:
            shortened = cmdline.strip()
            if len(shortened) > 140:
                shortened = shortened[:137] + "..."
            extra += f" {shortened}"
        print(f"{label} PID={pid} {status_text}{extra}")

    for key in ["tamper", "monitor", "timer"]:
        item = pid_registry.get(key, {})
        pid = int(item.get("pid", 0)) if isinstance(item, dict) else 0
        stop_pid(pid, key, "registry")

    # 兜底扫描：即使 pid 文件丢失/过期，也要把遗留 monitor/tamper 进程断开。
    markers = [
        MONITOR_SCRIPT.name.lower(),
        TAMPER_SCRIPT.name.lower(),
        RECONCILE_DAEMON_SCRIPT.name.lower(),
        str(MONITOR_SCRIPT).lower(),
        str(TAMPER_SCRIPT).lower(),
        str(RECONCILE_DAEMON_SCRIPT).lower(),
    ]
    discovered = find_script_processes(markers)
    for pid, cmdline in discovered.items():
        lowered = cmdline.lower()
        if MONITOR_SCRIPT.name.lower() in lowered:
            label = "monitor"
        elif TAMPER_SCRIPT.name.lower() in lowered:
            label = "tamper"
        elif RECONCILE_DAEMON_SCRIPT.name.lower() in lowered:
            label = "timer"
        else:
            label = "python"
        stop_pid(pid, label, "scan", cmdline=cmdline)

    for key in ["tamper", "monitor", "timer"]:
        item = pid_registry.get(key, {})
        pid = int(item.get("pid", 0)) if isinstance(item, dict) else 0
        if pid <= 0 or not is_process_alive(pid):
            pid_registry.pop(key, None)

    save_pid_registry(pid_file, pid_registry)

    if not stopped_any:
        print("未发现可停止的 monitor/tamper/timer 进程。")
    return 0


def build_clear_targets(runtime: Dict[str, Path], include_pid_state: bool = True) -> List[Path]:
    output_dir = runtime["output_dir"]
    targets: List[Path] = [
        runtime["backup_dir"],
        runtime["log_json"],
        runtime["log_md"],
        runtime["archive_json"],
        runtime["archive_md"],
        runtime["reconcile_cron_file"],
        runtime["heartbeat_log_file"],
        runtime["legacy_reconcile_cron_file"],
        runtime["legacy_heartbeat_log_file"],
    ]
    if include_pid_state:
        targets.append(runtime["pid_file"])

    targets.extend(sorted(output_dir.glob("*.log")))
    targets.extend(sorted(output_dir.glob("*.jsonl")))

    # 兼容旧版本 tamper 默认日志路径。
    targets.append(SCRIPT_DIR / "tamper_events.jsonl")
    return dedupe_paths(targets)


def cmd_clear(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    pid_file = runtime["pid_file"]

    targets = build_clear_targets(runtime, include_pid_state=not args.keep_processes)

    print_header("No.0 Skill 清空")
    print("将清理以下路径：")
    for item in targets:
        print(f"- {item}")

    if args.dry_run:
        print("dry-run 模式，未执行删除。")
        return 0

    if not args.yes:
        if not sys.stdin.isatty():
            print("非交互模式请使用 --yes 进行确认，或使用 --dry-run 预览。")
            return 1
        confirm = input("确认执行清空? [y/N] ").strip().lower()
        if confirm not in {"y", "yes"}:
            print("已取消。")
            return 0

    if not args.keep_processes:
        pid_registry = load_pid_registry(pid_file)
        for key in ["tamper", "monitor", "timer"]:
            item = pid_registry.get(key, {})
            pid = int(item.get("pid", 0)) if isinstance(item, dict) else 0
            if pid <= 0:
                continue
            ok = terminate_process(pid)
            status_text = "已停止" if ok else "未运行或停止失败"
            print(f"{key} PID={pid} {status_text}")
    else:
        print("已跳过进程停止（--keep-processes）。")

    deleted: List[Path] = []
    skipped: List[Path] = []
    failed: List[Tuple[Path, str]] = []

    for target in targets:
        try:
            if target.is_dir():
                shutil.rmtree(target)
                deleted.append(target)
                continue
            if target.exists():
                target.unlink()
                deleted.append(target)
            else:
                skipped.append(target)
        except Exception as exc:
            failed.append((target, str(exc)))

    print(f"清理完成：已删除 {len(deleted)} 项，跳过 {len(skipped)} 项，失败 {len(failed)} 项。")
    if failed:
        for path_obj, reason in failed:
            print(f"[FAIL] {path_obj}: {reason}")
        return 1
    return 0


def cmd_sync_assets(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    copied, missing, source_dir = ensure_core_files(runtime["monitor_dir"])
    if copied:
        print("已复制: " + ", ".join(copied))
    else:
        print("assets 中核心文件已齐全，无需复制。")

    if source_dir:
        print(f"核心文件来源目录: {source_dir}")
    if missing:
        print("仍缺失文件: " + ", ".join(missing))
        return 1
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    monitor_dir = runtime["monitor_dir"]
    backup_dir = runtime["backup_dir"]
    state_file = runtime["state_file"]
    log_json = runtime["log_json"]
    archive_json = runtime["archive_json"]
    pid_registry = load_pid_registry(runtime["pid_file"])

    # quiet 模式：无新文件不一致时静默退出，供 cron 使用
    quiet = getattr(args, "quiet", False)
    if quiet:
        # 读取已报告的不一致文件记录
        reported_file = runtime["output_dir"] / ".no0_reported_inconsistent"
        reported_files = set()
        if reported_file.exists():
            try:
                with open(reported_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            reported_files.add(line)
            except Exception:
                pass
        
        # 检查当前文件一致性状态
        backup_dir = runtime["backup_dir"]
        current_inconsistent = set()
        new_inconsistent = False
        
        for file_name in MONITOR_FILES:
            target_file = monitor_dir / file_name
            if not target_file.exists():
                continue
                
            latest_backup = get_latest_backup(backup_dir, file_name)
            if latest_backup is None:
                continue  # 无备份，跳过
                
            try:
                current_hash = file_md5(target_file)
                backup_hash = file_md5(latest_backup)
                if current_hash != backup_hash:
                    current_inconsistent.add(file_name)
                    if file_name not in reported_files:
                        new_inconsistent = True
            except Exception:
                pass  # 哈希读取失败，跳过
        
        # 更新已报告的不一致文件记录
        try:
            with open(reported_file, "w", encoding="utf-8") as f:
                for file_name in current_inconsistent:
                    f.write(f"{file_name}\n")
        except Exception:
            pass
        
        # 更新检查时间戳（用于记录上次检查时间）
        quiet_ts_file = runtime["output_dir"] / ".no0_last_quiet_check"
        try:
            import time as _time
            quiet_ts_file.write_text(str(_time.time()))
        except Exception:
            pass

        if not new_inconsistent:
            # 无新不一致文件，完全静默退出（不输出任何内容）
            sys.exit(0)
        # 如果有新不一致文件，继续执行下面的代码输出状态
        # 注意：这里不会return，会继续执行后面的代码
    
    print_header("No.0 Skill 状态")

    monitor_info = pid_registry.get("monitor", {}) if isinstance(pid_registry, dict) else {}
    monitor_pid = int(monitor_info.get("pid", 0)) if isinstance(monitor_info, dict) else 0
    if monitor_pid and is_process_alive(monitor_pid):
        print(f"monitor: 运行中 (PID={monitor_pid})")
    else:
        print("monitor: 未运行")

    tamper_info = pid_registry.get("tamper", {}) if isinstance(pid_registry, dict) else {}
    tamper_pid = int(tamper_info.get("pid", 0)) if isinstance(tamper_info, dict) else 0
    if tamper_pid and is_process_alive(tamper_pid):
        print(f"tamper: 运行中 (PID={tamper_pid})")
    else:
        print("tamper: 未运行")

    timer_info = pid_registry.get("timer", {}) if isinstance(pid_registry, dict) else {}
    timer_pid = int(timer_info.get("pid", 0)) if isinstance(timer_info, dict) else 0
    if timer_pid and is_process_alive(timer_pid):
        print(f"timer: 运行中 (PID={timer_pid})")
    else:
        print("timer: 未运行")

    if state_file.exists():
        state = read_json_file(state_file, {})
        records = state.get("self_monitor_records", []) if isinstance(state, dict) else []
        if isinstance(records, list) and records:
            print(f"上次检测: {records[-1].get('monitor_time', '未知')}")
        else:
            print("上次检测: 无记录")
    else:
        print("上次检测: 状态文件不存在")

    print("\n受保护文件:")
    for file_name in MONITOR_FILES:
        target_file = monitor_dir / file_name
        if not target_file.exists():
            print(f"- {file_name}: 缺失")
            continue

        latest_backup = get_latest_backup(backup_dir, file_name)
        if latest_backup is None:
            print(f"- {file_name}: 存在（无备份）")
            continue

        try:
            current_hash = file_md5(target_file)
            backup_hash = file_md5(latest_backup)
            status_text = "一致" if current_hash == backup_hash else "与最新备份不一致"
            print(f"- {file_name}: {status_text}")
        except Exception:
            print(f"- {file_name}: 哈希读取失败")

    active_records = collect_log_records(log_json)
    archived_records = collect_log_records(archive_json)
    active_counts = summarize_record_counts(active_records)
    archived_counts = summarize_record_counts(archived_records)
    all_counts = {
        "total": active_counts["total"] + archived_counts["total"],
        "labeled": active_counts["labeled"] + archived_counts["labeled"],
        "unlabeled": active_counts["unlabeled"] + archived_counts["unlabeled"],
    }

    print("\n变更日志统计:")
    print(
        f"- change_log.json: 总计 {active_counts['total']} 条，已分析 {active_counts['labeled']} 条，"
        f"待分析 {active_counts['unlabeled']} 条"
    )
    print(
        f"- change_log_labeled.json: 总计 {archived_counts['total']} 条，已分析 {archived_counts['labeled']} 条，"
        f"待分析 {archived_counts['unlabeled']} 条"
    )
    print(
        f"- 全量合计: 总计 {all_counts['total']} 条，已分析 {all_counts['labeled']} 条，"
        f"待分析 {all_counts['unlabeled']} 条"
    )

    try:
        sys.path.insert(0, str(SCRIPT_DIR))
        from event_emitter import pending_summary
        from i18n import t as _t
        ps = pending_summary()
        line = _t("status.pending_prefix", n=ps["pending_count"])
        if ps.get("oldest_age_seconds") is not None:
            line += _t(
                "status.pending_detail",
                age_h=ps["oldest_age_seconds"] / 3600.0,
                cap=ps["cap"],
                ttl_h=ps["max_age_seconds"] // 3600,
            )
        if ps["warn"]:
            line += _t("status.pending_warn")
        print(line)
    except Exception:
        pass
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    log_md = runtime["log_md"]
    last = max(1, int(args.last))

    print_header(f"No.0 Skill 记录（最近 {last} 条）")
    if log_md.exists() and train_md.stat().st_size > 0:
        content = log_md.read_text(encoding="utf-8")
        entries = parse_markdown_entries(content)
        for entry in entries[-last:]:
            print(entry)
            print("-" * 50)
    else:
        print("暂无 markdown 记录。")


    return 0


def cmd_versions(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    backup_dir = runtime["backup_dir"]
    try:
        file_name = normalize_monitor_file_name(args.file)
    except ValueError as exc:
        print(str(exc))
        return 1

    versions = list_backup_versions(backup_dir, file_name)
    print_header(f"{file_name} 历史版本")
    if not versions:
        print("暂无备份版本。")
        return 0

    for item in versions:
        version = parse_backup_version(item)
        meta = item.with_suffix(item.suffix + ".meta")
        backup_time = "未知"
        backup_hash = "未知"
        if meta.exists():
            meta_obj = read_json_file(meta, {})
            if isinstance(meta_obj, dict):
                ts = meta_obj.get("backup_time")
                try:
                    backup_time = datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    backup_time = "未知"
                raw_hash = str(meta_obj.get("backup_hash", ""))
                backup_hash = (raw_hash[:16] + "...") if raw_hash else "未知"
        print(f"v{version}  {backup_time}  {backup_hash}  {item}")
    return 0


def build_unified_diff(before_file: Path, after_file: Path) -> str:
    before_text = before_file.read_text(encoding="utf-8", errors="replace").splitlines()
    after_text = after_file.read_text(encoding="utf-8", errors="replace").splitlines()
    diff_lines = list(
        difflib.unified_diff(
            before_text,
            after_text,
            fromfile=before_file.name,
            tofile=after_file.name,
            lineterm="",
            n=3,
        )
    )
    return "\n".join(diff_lines)


def cmd_diff(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    monitor_dir = runtime["monitor_dir"]
    backup_dir = runtime["backup_dir"]

    try:
        file_name = normalize_monitor_file_name(args.file)
    except ValueError as exc:
        print(str(exc))
        return 1

    version_text = args.version if str(args.version).startswith("v") else f"v{args.version}"
    backup_file = backup_dir / f"{file_name}.{version_text}"
    target_file = monitor_dir / file_name

    if not backup_file.exists():
        print(f"版本不存在: {backup_file}")
        return 1
    if not target_file.exists():
        print(f"当前文件不存在: {target_file}")
        return 1

    print_header(f"{file_name} {version_text} vs 当前")
    print(build_unified_diff(backup_file, target_file))
    return 0


def prune_old_versions(backup_dir: Path, file_name: str, keep: int = 10) -> None:
    versions = list_backup_versions(backup_dir, file_name)
    if len(versions) <= keep:
        return

    for item in versions[: len(versions) - keep]:
        meta = item.with_suffix(item.suffix + ".meta")
        try:
            item.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            meta.unlink(missing_ok=True)
        except Exception:
            pass


def save_backup_meta(backup_file: Path, source_file: Path) -> None:
    meta_file = backup_file.with_suffix(backup_file.suffix + ".meta")
    meta_payload = {
        "original_path": str(source_file),
        "original_mtime": source_file.stat().st_mtime,
        "backup_time": time.time(),
        "backup_hash": file_md5(backup_file),
        "source_hash": file_md5(source_file),
        "note": "rollback 前自动保存的当前版本",
    }
    write_json_file(meta_file, meta_payload)


def cmd_rollback(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    monitor_dir = runtime["monitor_dir"]
    backup_dir = runtime["backup_dir"]

    try:
        file_name = normalize_monitor_file_name(args.file)
    except ValueError as exc:
        print(str(exc))
        return 1

    target_file = monitor_dir / file_name
    if not target_file.exists():
        print(f"文件不存在: {target_file}")
        return 1

    versions = list_backup_versions(backup_dir, file_name)
    if not versions:
        print("没有可用备份版本。")
        return 1

    version_text = args.version
    if not version_text:
        if not sys.stdin.isatty():
            print("未指定版本，且当前环境非交互式。请使用 /no0 rollback <file> <version>")
            return 1
        print("可用版本:")
        for item in versions:
            print(f"- v{parse_backup_version(item)}")
        version_text = input("请输入版本号（如 v2）: ").strip()

    if not version_text:
        print("未输入版本号，已取消。")
        return 1
    version_text = version_text if version_text.startswith("v") else f"v{version_text}"
    backup_file = backup_dir / f"{file_name}.{version_text}"
    if not backup_file.exists():
        print(f"版本不存在: {backup_file}")
        return 1

    preview = build_unified_diff(backup_file, target_file)
    print_header(f"回滚预览 {file_name} {version_text} -> 当前")
    lines = preview.splitlines()
    print("\n".join(lines[:80]))

    confirmed = args.yes
    if not confirmed:
        if not sys.stdin.isatty():
            print("非交互模式请使用 --yes 进行回滚确认。")
            return 1
        confirm = input(f"确认回滚 {file_name} 到 {version_text} ? [y/N] ").strip().lower()
        confirmed = confirm in {"y", "yes"}

    if not confirmed:
        print("已取消。")
        return 0

    next_version_num = parse_backup_version(versions[-1]) + 1
    current_backup = backup_dir / f"{file_name}.v{next_version_num}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target_file, current_backup)
    set_file_read_only(current_backup)
    save_backup_meta(current_backup, target_file)
    prune_old_versions(backup_dir, file_name, keep=10)

    shutil.copy2(backup_file, target_file)
    print(f"已回滚: {file_name} -> {version_text}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    script = SCRIPT_DIR / "hourly_report.py"
    cmd = [resolve_python_executable(), str(script)]
    if args.json:
        cmd.append("--json")
    if args.reset:
        cmd.append("--reset")
    return subprocess.call(cmd)


def cmd_test(args: argparse.Namespace) -> int:
    runtime = resolve_runtime_paths(args.monitor_dir, args.output_dir)
    monitor_dir = runtime["monitor_dir"]
    backup_dir = runtime["backup_dir"]
    state_file = runtime["state_file"]
    pid_registry = load_pid_registry(runtime["pid_file"])

    checks: List[Tuple[str, bool, str]] = []

    monitor_info = pid_registry.get("monitor", {}) if isinstance(pid_registry, dict) else {}
    monitor_pid = int(monitor_info.get("pid", 0)) if isinstance(monitor_info, dict) else 0
    checks.append(("monitor.py 运行中", is_process_alive(monitor_pid), f"PID={monitor_pid}" if monitor_pid else "无 PID"))

    all_files_exist = all((monitor_dir / name).exists() for name in MONITOR_FILES)
    checks.append(("六个核心文件存在", all_files_exist, str(monitor_dir)))

    checks.append(("备份目录存在", backup_dir.exists(), str(backup_dir)))
    checks.append(("monitor 状态文件存在", state_file.exists(), str(state_file)))
    checks.append(("event_logger.py 存在", EVENT_LOGGER_SCRIPT.exists(), str(EVENT_LOGGER_SCRIPT)))

    print_header("No.0 Skill 自检")
    passed = 0
    failed = 0
    for title, ok, detail in checks:
        if ok:
            passed += 1
            print(f"[PASS] {title} ({detail})")
        else:
            failed += 1
            print(f"[FAIL] {title} ({detail})")

    print(f"结果: 通过 {passed} 项，失败 {failed} 项")
    return 0 if failed == 0 else 1


def maybe_upgrade_legacy_args(argv: List[str]) -> List[str]:
    if argv and argv[0] == "/no0":
        argv = argv[1:]

    known_commands = {
        "start",
        "stop",
        "clear",
        "clean",
        "status",
        "log",
        "versions",
        "rollback",
        "diff",
        "test",
        "--help",
        "-h",
    }

    if not argv:
        return ["start"]

    if argv[0] not in known_commands and argv[0].startswith("-"):
        return ["start", *argv]

    if argv[0] not in known_commands and argv[0] in {"help"}:
        return ["--help"]

    return argv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="No.0 Skill 统一入口（跨平台 /no0 命令 + monitor 启停 + 核心文件同步）"
    )
    subparsers = parser.add_subparsers(dest="command")

    start_parser = subparsers.add_parser("start", help="启动入口：同步核心文件并启动 monitor（可选启动 tamper）")
    start_parser.add_argument("--monitor-dir", "--workspace-dir", dest="monitor_dir", help="监听目录，默认 assets")
    start_parser.add_argument("--output-dir", dest="output_dir", help="输出目录，默认 no0-skill 根目录")
    start_parser.add_argument("--with-tamper", "--with_tamper", action="store_true", help="同时启动 tamper_simulator")
    start_parser.add_argument(
        "--reconcile-interval",
        type=int,
        default=120,
        help="Heartbeat 定时器间隔秒数，默认 120，最小 30",
    )
    start_parser.add_argument("--tamper-interval", type=int, default=15, help="tamper 间隔秒数")
    start_parser.add_argument("--tamper-iterations", type=int, default=999999, help="tamper 执行次数")
    start_parser.add_argument("--tamper-targets", nargs="*", default=None, help="tamper 目标文件名列表")
    start_parser.add_argument(
        "--tamper-strategy",
        choices=["coverage", "balanced", "high-risk", "low-risk"],
        default="coverage",
        help="tamper 算法策略",
    )
    start_parser.add_argument(
        "--tamper-algorithms",
        nargs="*",
        default=None,
        help="tamper 算法 ID 过滤，如 A01 A05 A12",
    )
    start_parser.add_argument("--tamper-seed", type=int, default=None, help="tamper 随机种子")
    start_parser.add_argument(
        "--tamper-diff-preview-lines",
        type=int,
        default=80,
        help="tamper 事件中保留的 diff 预览行数",
    )
    start_parser.add_argument(
        "--tamper-keep-going",
        action="store_true",
        help="tamper 单次失败后继续后续迭代",
    )
    start_parser.add_argument("--restart", action="store_true", help="若 monitor 已运行则先停止再启动")
    start_parser.add_argument("--run-once", action="store_true", help="monitor 只运行一轮")
    start_parser.add_argument("--foreground", action="store_true", help="前台运行 monitor")
    start_parser.add_argument("--enable", action="store_true", help=argparse.SUPPRESS)
    start_parser.set_defaults(func=cmd_start)

    stop_parser = subparsers.add_parser("stop", help="停止入口脚本启动的 monitor/tamper")
    stop_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    stop_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    stop_parser.set_defaults(func=cmd_stop)

    clear_parser = subparsers.add_parser("clear", aliases=["clean"], help="清空日志、训练产物和备份文件")
    clear_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    clear_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    clear_parser.add_argument("--yes", action="store_true", help="非交互模式确认清空")
    clear_parser.add_argument("--dry-run", action="store_true", help="仅预览将要清理的路径")
    clear_parser.add_argument("--keep-processes", action="store_true", help="清理时不停止 monitor/tamper")
    clear_parser.set_defaults(func=cmd_clear)

    status_parser = subparsers.add_parser("status", help="显示 monitor 状态、文件状态、变更日志统计")
    status_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    status_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    status_parser.add_argument("--quiet", action="store_true", help="静默模式：无新记录时不输出任何内容（供 cron 使用）")
    status_parser.set_defaults(func=cmd_status)

    log_parser = subparsers.add_parser("log", help="查看最近变更日志记录")
    log_parser.add_argument("--last", type=int, default=20, help="最近 N 条")
    log_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    log_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    log_parser.set_defaults(func=cmd_log)

    versions_parser = subparsers.add_parser("versions", help="列出某文件历史版本")
    versions_parser.add_argument("file", help="文件名，如 soul.md")
    versions_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    versions_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    versions_parser.set_defaults(func=cmd_versions)

    rollback_parser = subparsers.add_parser("rollback", help="回滚文件到指定版本")
    rollback_parser.add_argument("file", help="文件名，如 soul.md")
    rollback_parser.add_argument("version", nargs="?", help="版本号，如 v2")
    rollback_parser.add_argument("--yes", action="store_true", help="非交互确认回滚")
    rollback_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    rollback_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    rollback_parser.set_defaults(func=cmd_rollback)

    diff_parser = subparsers.add_parser("diff", help="查看指定版本与当前文件差异")
    diff_parser.add_argument("file", help="文件名，如 soul.md")
    diff_parser.add_argument("version", help="版本号，如 v2")
    diff_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    diff_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    diff_parser.set_defaults(func=cmd_diff)

    report_parser = subparsers.add_parser("report", help="Hourly conditional report (cron-friendly)")
    report_parser.add_argument("--json", action="store_true", help="Emit JSON")
    report_parser.add_argument("--reset", action="store_true", help="Reset cursor")
    report_parser.set_defaults(func=cmd_report)

    test_parser = subparsers.add_parser("test", help="运行本地自检")
    test_parser.add_argument("--monitor-dir", dest="monitor_dir", help="监听目录")
    test_parser.add_argument("--output-dir", dest="output_dir", help="输出目录")
    test_parser.set_defaults(func=cmd_test)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    normalized_argv = maybe_upgrade_legacy_args(raw_argv)

    parser = build_parser()
    args = parser.parse_args(normalized_argv)

    if not hasattr(args, "func"):
        args = parser.parse_args(["start", *normalized_argv])

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
