#!/usr/bin/env python3
"""
音频录制控制器 — 支持两种后端：
  - daemon: ScreenCaptureKit 原生捕获（macOS 12.3+，推荐）
  - sox: BlackHole + SoX 传统方案

用法和原来一样：
  record_audio.py start "会议标题"
  record_audio.py stop
  record_audio.py status
"""

import json
import os
import socket
import struct
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "meeting-assistant"
CONFIG_PATH = CONFIG_DIR / "config.json"
SOCKET_PATH = CONFIG_DIR / "audio_daemon.sock"
STATE_PATH = CONFIG_DIR / ".state.json"
SCRIPT_DIR = Path(__file__).resolve().parent


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_config():
    cfg = {}
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    audio_cfg = cfg.get("audio", {})
    audio_cfg.setdefault("mic_device", ":0")
    audio_cfg.setdefault("system_audio_device", ":1")
    audio_cfg.setdefault("output_dir", str(SCRIPT_DIR.parent.parent / "meeting-recordings"))
    audio_cfg.setdefault("silence_threshold", 0.01)
    audio_cfg.setdefault("silence_duration_sec", 300)
    audio_cfg.setdefault("backend", "daemon")  # "daemon" or "sox"
    return audio_cfg


def socket_send(cmd):
    """发送命令到 audio_daemon Unix socket。"""
    if not SOCKET_PATH.exists():
        return None
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(str(SOCKET_PATH))
        sock.sendall(json.dumps(cmd).encode())
        sock.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        sock.close()
        return json.loads(data.decode()) if data else None
    except Exception as e:
        log(f"Socket error: {e}")
        return None


# ─── 后端: audio_daemon ──────────────────────────────

def daemon_start(title):
    cfg = load_config()
    resp = socket_send({"action": "start", "title": title})
    if resp and resp.get("status") == "recording":
        log(f"🎙 Recording started: {resp.get('file')}")
        return True
    log(f"❌ Start failed: {resp}")
    return False


def daemon_stop():
    resp = socket_send({"action": "stop"})
    if resp and resp.get("status") == "stopped":
        dur = resp.get("duration", 0)
        path = resp.get("file", "")
        log(f"⏹ Recording stopped: {dur}s → {path}")
        return {"path": path, "duration": dur}
    log(f"❌ Stop failed: {resp}")
    return None


def daemon_status():
    resp = socket_send({"action": "status"})
    return resp or {"recording": False}


def daemon_ensure_running():
    """如果 daemon 没在运行，尝试启动它。"""
    resp = socket_send({"action": "status"})
    if resp is not None:
        return True

    # 查找已安装的 AudioDaemon.app
    app_paths = [
        SCRIPT_DIR / "AudioDaemon.app",
        Path.home() / "Applications" / "Meeting Assistant.app",
        Path("/Applications/Meeting Assistant.app"),
    ]
    for app in app_paths:
        binary = app / "Contents/MacOS/audio_daemon"
        if binary.exists():
            log("🚀 启动 AudioDaemon...")
            subprocess.Popen(["open", str(app)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
            resp = socket_send({"action": "status"})
            if resp is not None:
                log("✅ AudioDaemon 已启动")
                return True
            break

    log("⚠️ AudioDaemon 未运行")
    return False


# ─── 后端: SoX + BlackHole ──────────────────────────

def sox_start(title):
    """SoX 双路录制（向后兼容）。"""
    cfg = load_config()
    output_dir = Path(cfg["output_dir"]).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    safe = title.replace("/", "_").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = output_dir / f"{safe}_{timestamp}.wav"

    state = {
        "recording": True,
        "title": title,
        "file_path": str(output),
        "started_at": datetime.now().isoformat(),
    }
    STATE_PATH.write_text(json.dumps(state, indent=2))

    listen_cmd = [
        "sox", "-q",
        "-t", "coreaudio", cfg["system_audio_device"],
        "-t", "coreaudio", cfg["mic_device"],
        "-t", "wav", str(output),
        "remix", "1,2",
        "gain", "-3",
    ]

    log(f"🎙 录制中: {output}")
    log(f"   后端: SoX (mic={cfg['mic_device']}, sys={cfg['system_audio_device']})")

    proc = subprocess.Popen(
        listen_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    (CONFIG_DIR / ".recording_pid").write_text(str(proc.pid))
    return True


def sox_stop():
    pid_path = CONFIG_DIR / ".recording_pid"
    if pid_path.exists():
        try:
            pid = int(pid_path.read_text().strip())
            os.kill(pid, 15)
            time.sleep(0.5)
            pid_path.unlink(missing_ok=True)
        except Exception:
            pass

    state = {"recording": False, "title": "", "file_path": ""}
    STATE_PATH.write_text(json.dumps(state, indent=2))

    log("⏹ 录制已停止")
    return {"path": "", "duration": 0}


def sox_status():
    state = {"recording": False, "title": ""}
    if STATE_PATH.exists():
        try:
            state = json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    if (CONFIG_DIR / ".recording_pid").exists():
        state["recording"] = True
    return state


# ─── 主入口 ──────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <start|stop|status> [标题]")
        sys.exit(1)

    cmd = sys.argv[1]
    cfg = load_config()
    backend = cfg.get("backend", "daemon")

    if backend == "daemon":
        if cmd == "start":
            title = sys.argv[2] if len(sys.argv) > 2 else "未命名会议"
            if daemon_ensure_running():
                daemon_start(title)
            else:
                log("⚠️ AudioDaemon 未运行，切换到 SoX 后端")
                sox_start(title)
        elif cmd == "stop":
            result = daemon_stop()
            if not result:
                sox_stop()
        elif cmd == "status":
            result = daemon_status()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"未知命令: {cmd}")
    else:
        if cmd == "start":
            title = sys.argv[2] if len(sys.argv) > 2 else "未命名会议"
            sox_start(title)
        elif cmd == "stop":
            sox_stop()
        elif cmd == "status":
            result = sox_status()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
