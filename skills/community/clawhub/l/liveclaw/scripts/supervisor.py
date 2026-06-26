#!/usr/bin/env python3
"""
永久自愈推流守护进程 (supervisor) — v23 精简版
- 移除 Xvfb 和 Dashboard 窗口监护（不再需要）
- 仅监护 stream_daemon + tts_worker
- 每 30 秒巡检一次
"""
import json, os, sys, time, subprocess, datetime
from pathlib import Path

try:
    from platform_utils import (
        get_work_dir, get_python_cmd, is_windows, is_linux, is_mac,
        get_platform_tag,
        daemonize, start_daemon_process, new_session_kwargs,
        find_process_by_script, find_process_by_name,
        is_process_alive, register_signal_handlers,
        get_rotating_logger
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import (
        get_work_dir, get_python_cmd, is_windows, is_linux, is_mac,
        get_platform_tag,
        daemonize, start_daemon_process, new_session_kwargs,
        find_process_by_script, find_process_by_name,
        is_process_alive, register_signal_handlers,
        get_rotating_logger
    )

WORK_DIR = get_work_dir()
WORK_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE   = str(WORK_DIR / "supervisor.log")
PID_FILE   = str(WORK_DIR / "supervisor.pid")
CHECK_INTERVAL = 30  # 秒

# ── 日志（带轮转，最大 2MB × 2 备份 = 6MB）──────────────
_logger = get_rotating_logger("supervisor", LOG_FILE,
                              max_bytes=2 * 1024 * 1024, backup_count=2)

def log(msg, level="INFO"):
    if level == "ERROR":
        _logger.error(msg)
    elif level == "WARN":
        _logger.warning(msg)
    else:
        _logger.info(msg)

def read_pid(path):
    try:
        return int(Path(path).read_text().strip())
    except Exception:
        return None

# ── 启动 stream_daemon ──────────────────────────────────────

def _script_path(name: str) -> str:
    """定位工作目录中的脚本路径（兼容脚本在 scripts/ 子目录的情况）"""
    p = WORK_DIR / name
    if p.exists():
        return str(p)
    p2 = WORK_DIR / "scripts" / name
    if p2.exists():
        return str(p2)
    return str(p)

def start_stream_daemon():
    log("Starting stream_daemon...")
    env = {**os.environ}
    pid = start_daemon_process(
        _script_path("stream_daemon.py"),
        log_file=str(WORK_DIR / "daemon.log"),
        env=env
    )
    (WORK_DIR / "daemon.pid").write_text(str(pid))
    log(f"stream_daemon started PID={pid}")
    return pid

def ensure_stream():
    """确保 stream_daemon 进程存活"""
    pid = read_pid(str(WORK_DIR / "daemon.pid"))
    if pid and is_process_alive(pid):
        return pid

    pids = find_process_by_script("stream_daemon.py")
    alive = [p for p in pids if is_process_alive(p)]
    if alive:
        return alive[0]

    return start_stream_daemon()

# ── 启动 / 确保 tts_worker ─────────────────────────────────────

_tts_enabled_cache = None
_tts_config_mtime = 0

def _is_tts_enabled() -> bool:
    global _tts_enabled_cache, _tts_config_mtime
    config_path = WORK_DIR / "config.json"
    if not config_path.exists():
        _tts_enabled_cache = False
        return False
    try:
        current_mtime = config_path.stat().st_mtime
        if current_mtime == _tts_config_mtime and _tts_enabled_cache is not None:
            return _tts_enabled_cache
        _tts_config_mtime = current_mtime
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        _tts_enabled_cache = bool(cfg.get("tts_secret_id")) and bool(cfg.get("tts_secret_key"))
        return _tts_enabled_cache
    except Exception:
        _tts_enabled_cache = False
        return False

def start_tts_worker():
    log("Starting tts_worker...")
    env = {**os.environ}
    pid = start_daemon_process(
        str(WORK_DIR / "tts_worker.py"),
        log_file=str(WORK_DIR / "tts_worker.log"),
        env=env
    )
    (WORK_DIR / "tts_worker.pid").write_text(str(pid))
    log(f"tts_worker started PID={pid}")
    return pid

def ensure_tts_worker():
    if not _is_tts_enabled():
        return -1

    pid = read_pid(str(WORK_DIR / "tts_worker.pid"))
    if pid and is_process_alive(pid):
        return pid

    pids = find_process_by_script("tts_worker.py")
    alive = [p for p in pids if is_process_alive(p)]
    if alive:
        return alive[0]

    return start_tts_worker()

# ── 主循环 ──────────────────────────────────────────────────

_running = True

def _sig_handler(signum, frame):
    global _running
    log(f"Supervisor received signal {signum}, exiting...", "WARN")
    _running = False

# 默认忽略 SIGTERM（抗 OpenClaw 容器定期清理非自管进程）
# 只响应 SIGINT（Ctrl+C 调试）或 SIGKILL（setup.py --stop 强制杀）
# setup.py --stop 先 SIGTERM（被忽略），2s 后 SIGKILL（强制终止）
import signal as _signal
_signal.signal(_signal.SIGTERM, _signal.SIG_IGN)
_signal.signal(_signal.SIGINT, _sig_handler)

def main_loop():
    log(f"Supervisor main loop started (PID={os.getpid()}) "
        f"Platform={get_platform_tag()} Mode=Pillow (no Xvfb/Dashboard)")

    while _running:
        try:
            spid = ensure_stream()
            tpid = ensure_tts_worker()
            parts = f"Stream={spid}"
            if tpid > 0:
                parts += f" TTS={tpid}"
            log(f"Health OK — {parts}")
        except Exception as e:
            log(f"Error in health check: {e}", "ERROR")
        time.sleep(CHECK_INTERVAL)

# ── 入口 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--no-daemon" in sys.argv:
        Path(PID_FILE).write_text(str(os.getpid()))
        main_loop()
    else:
        if is_windows():
            print("Supervisor starting (Windows mode)...")
            Path(PID_FILE).write_text(str(os.getpid()))
            main_loop()
        else:
            print("Daemonizing supervisor...")
            daemonize(LOG_FILE)
            Path(PID_FILE).write_text(str(os.getpid()))
            main_loop()
