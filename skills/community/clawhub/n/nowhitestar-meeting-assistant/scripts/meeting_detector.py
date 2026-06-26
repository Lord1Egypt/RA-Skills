#!/usr/bin/env python3
"""
会议检测守护进程：检测常见会议/通话窗口，触发录制询问。

目标：不依赖日历，发现微信语音/视频电话、腾讯会议、Google Meet、飞书/Lark、Zoom 等会议场景。

策略：
- 优先读取 macOS 前台应用/窗口标题（System Events）
- 用窗口标题关键词判定会议状态，避免仅因微信/浏览器常驻而误报
- 检测持续 stable_sec 后才弹窗
- 同一 meeting signature 有 cooldown，避免重复询问
- 已在录制时不弹窗
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "meeting-assistant"
CONFIG_PATH = CONFIG_DIR / "config.json"
STATE_PATH = CONFIG_DIR / ".detector_state.json"
RECORDING_STATE_PATH = CONFIG_DIR / ".state.json"
PID_PATH = CONFIG_DIR / ".detector.pid"
LOG_PATH = CONFIG_DIR / "detector.log"
SCRIPT_DIR = Path(__file__).resolve().parent

DEFAULT_CONFIG = {
    "enabled": True,
    "interval_sec": 10,
    "stable_sec": 15,
    "prompt_cooldown_sec": 1800,
    "window_keywords": [
        # Zoom
        "Zoom Meeting", "Zoom 会议", "zoom.us", "Zoom Workplace",
        # Tencent Meeting / VooV
        "腾讯会议", "Tencent Meeting", "VooV Meeting", "WeMeet",
        # Google Meet (browser windows)
        "Google Meet", "meet.google.com", "Meet -",
        # Feishu / Lark
        "飞书会议", "Feishu Meeting", "Lark Meeting", "Lark | Meeting", "视频会议",
        # WeChat / WeCom calls
        "微信通话", "微信电话", "语音通话", "视频通话", "Voice Call", "Video Call",
        "WeChat Call", "WeChat Video", "企业微信", "WeCom",
        # Generic browser/app meeting hints
        "正在通话", "正在会议", "加入会议", "会议中", "通话中",
    ],
    "app_name_hints": [
        "zoom.us", "Zoom", "腾讯会议", "TencentMeeting", "VooV", "WeMeet",
        "Feishu", "Lark", "飞书", "WeChat", "微信", "企业微信", "WeCom",
        "Google Chrome", "Arc", "Safari", "Microsoft Edge", "Firefox",
    ],
    "target_app_names": [
        "zoom.us", "Zoom", "腾讯会议", "TencentMeeting", "VooV Meeting", "WeMeet",
        "Feishu", "Lark", "飞书", "WeChat", "微信", "企业微信", "WeCom",
        "Google Chrome", "Arc", "Safari", "Microsoft Edge", "Firefox"
    ],
    "dedicated_meeting_apps": [
        "zoom.us", "Zoom", "腾讯会议", "TencentMeeting", "VooV Meeting", "WeMeet"
    ],
    "ignore_window_keywords": [
        "Calendar", "日历", "Gmail", "Inbox", "Settings", "Preferences",
        "聊天", "通讯录", "朋友圈", "文件传输助手",
        "PolyMeet",
    ],
}


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)


AUDIO_DAEMON_SOCKET = Path.home() / ".config" / "meeting-assistant" / "audio_daemon.sock"
WINDOW_SCANNER = SCRIPT_DIR / "window_scanner"


def _query_audio_daemon():
    """通过 AudioDaemon 的 socket 获取窗口列表。"""
    if not AUDIO_DAEMON_SOCKET.exists():
        return None
    try:
        import socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(str(AUDIO_DAEMON_SOCKET))
        sock.sendall(b'{"action":"windows"}')
        sock.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk: break
            data += chunk
        sock.close()
        resp = json.loads(data.decode())
        return resp.get("windows", [])
    except Exception:
        return None


def _has_permission():
    """Quick check: can we read window titles?"""
    # Try AudioDaemon first (merged scanner)
    wins = _query_audio_daemon()
    if wins is not None:
        return True
    # Fallback: standalone window_scanner
    try:
        r = subprocess.run(
            [str(WINDOW_SCANNER)],
            capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0 and len(r.stdout.strip()) > 0
    except Exception:
        return False


def collect_windows(target_app_names=None):
    """返回 [{app, title}] 或 None。
    优先用 AudioDaemon 的 socket（如运行中），否则用 window_scanner。"""
    windows = _query_audio_daemon()
    if windows is None:
        try:
            r = subprocess.run(
                [str(WINDOW_SCANNER)],
                capture_output=True, text=True, timeout=5,
            )
            if r.returncode != 0:
                return None
            windows = json.loads(r.stdout)
        except Exception:
            return None

    if not windows:
        return []

    target_app_names = target_app_names or DEFAULT_CONFIG["target_app_names"]
    target_patterns = _compile_patterns(target_app_names)

    rows = []
    for w in windows:
        app = w.get("app", "")
        title = w.get("title", "")
        if not app or not title:
            continue
        if not any(p.search(app) for p in target_patterns):
            continue
        rows.append({"app": app.strip(), "title": title.strip()})
    return rows


def load_config():
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with CONFIG_PATH.open() as f:
            full = json.load(f)
    except Exception:
        return DEFAULT_CONFIG.copy()
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(full.get("meeting_detection", {}))
    return cfg


def load_state():
    if not STATE_PATH.exists():
        return {"prompted": {}}
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {"prompted": {}}


def save_state(state):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def is_recording_active():
    try:
        state = json.loads(RECORDING_STATE_PATH.read_text())
        if state.get("recording"):
            return True
    except Exception:
        pass
    return (CONFIG_DIR / ".recording_pid").exists()


def _osascript(script, timeout=3):
    return subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def collect_visible_apps():
    """无需辅助功能权限的兜底：只能看到可见 app 名，不能看到窗口标题。"""
    result = subprocess.run(["lsappinfo", "visibleProcessList"], capture_output=True, text=True, timeout=5)
    apps = re.findall(r'\-"([^"]+)"', result.stdout)
    return [a.replace("_", " ") for a in apps]


def _compile_patterns(words):
    return [re.compile(re.escape(w), re.I) for w in words if w]


def detect_meeting(cfg):
    """返回检测结果或 None。"""
    window_patterns = _compile_patterns(cfg.get("window_keywords", []))
    ignore_patterns = _compile_patterns(cfg.get("ignore_window_keywords", []))
    app_hints = _compile_patterns(cfg.get("app_name_hints", []))

    windows = collect_windows(cfg.get("target_app_names"))
    if windows is None:
        # 无辅助功能权限时用可见 app 名做简易检测
        try:
            visible_apps = collect_visible_apps()
            # 只检查你的真实会议 app
            dedicated = _compile_patterns(cfg.get("dedicated_meeting_apps", []))
            for app in visible_apps:
                if any(p.search(app) for p in dedicated):
                    return {
                        "active": True,
                        "title": app,
                        "app": app,
                        "window": "",
                        "signature": signature(app, "visible-app"),
                        "fallback": "visible_app",
                    }
            # 也用窗口关键词匹配 visible app 名（仅当 app 名包含会议词汇才触发）
            for app in visible_apps:
                if any(p.search(app) for p in ignore_patterns):
                    continue
                if any(p.search(app) for p in window_patterns):
                    return {
                        "active": True,
                        "title": app,
                        "app": app,
                        "window": "",
                        "signature": signature(app, "visible-keyword"),
                        "fallback": "visible_keyword",
                    }
        except Exception:
            pass
        return {
            "active": False,
            "permission_hint": "系统设置 → 隐私与安全性 → 辅助功能，添加 Python.app（/opt/homebrew/Cellar/python@3.14/.../Python.app）以获取完整窗口标题检测。",
        }

    matches = []
    for w in windows:
        haystack = f"{w['app']} {w['title']}"
        if any(p.search(haystack) for p in ignore_patterns):
            continue
        app_interesting = any(p.search(w["app"]) for p in app_hints)
        title_match = any(p.search(w["title"]) or p.search(haystack) for p in window_patterns)
        if title_match and app_interesting:
            matches.append(w)

    if matches:
        best = sorted(matches, key=lambda x: len(x.get("title", "")), reverse=True)[0]
        title = best.get("title") or best.get("app") or "检测到会议"
        return {
            "active": True,
            "title": normalize_title(title),
            "app": best.get("app", ""),
            "window": best.get("title", ""),
            "signature": signature(best.get("app", ""), title),
            "matches": matches[:5],
        }

    return {"active": False, "windows": windows[:10]}


def normalize_title(title):
    title = re.sub(r"\s+", " ", title).strip()
    title = title[:80]
    return title or "检测到会议"


def signature(app, title):
    raw = f"{app}|{title}".encode("utf-8", errors="ignore")
    return hashlib.sha1(raw).hexdigest()[:12]


def recently_prompted(state, sig, cooldown_sec):
    prompted = state.setdefault("prompted", {})
    now = time.time()
    # 顺手清理过期记录
    for key, ts in list(prompted.items()):
        if now - float(ts) > cooldown_sec * 2:
            prompted.pop(key, None)
    return sig in prompted and now - float(prompted[sig]) < cooldown_sec


def mark_prompted(state, sig):
    state.setdefault("prompted", {})[sig] = time.time()
    save_state(state)


def prompt_recording(title):
    daemon = SCRIPT_DIR / "meeting_daemon.py"
    subprocess.Popen(
        [sys.executable, str(daemon), "ask_record", title, f"detected::{signature('', title)}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def run_once(args):
    cfg = load_config()
    res = detect_meeting(cfg)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res.get("active") else 1


def run_daemon(args):
    cfg = load_config()
    if not cfg.get("enabled", True):
        log("meeting_detection disabled")
        return

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    PID_PATH.write_text(str(os.getpid()))
    interval = int(cfg.get("interval_sec", 10))
    stable_sec = int(cfg.get("stable_sec", 15))
    cooldown = int(cfg.get("prompt_cooldown_sec", 1800))

    state = load_state()
    active_since = None
    active_sig = None
    last_permission_error = 0

    log(f"meeting detector started (interval={interval}s stable={stable_sec}s cooldown={cooldown}s)")
    try:
        while True:
            cfg = load_config()
            if not cfg.get("enabled", True):
                time.sleep(interval)
                continue

            res = detect_meeting(cfg)
            now = time.time()

            hint = res.get("permission_hint")
            if hint and now - last_permission_error > 300:
                log(f"⚠️ {hint}")
                last_permission_error = now

            if not res.get("active"):
                active_since = None
                active_sig = None
                time.sleep(interval)
                continue

            sig = res.get("signature")
            if sig != active_sig:
                active_sig = sig
                active_since = now
                log(f"👀 detected candidate: {res.get('app')} | {res.get('window')}")
                time.sleep(interval)
                continue

            if now - (active_since or now) < stable_sec:
                time.sleep(interval)
                continue

            if is_recording_active():
                time.sleep(interval)
                continue

            state = load_state()
            if recently_prompted(state, sig, cooldown):
                time.sleep(interval)
                continue

            title = f"检测到会议：{res.get('title', '会议')}"
            mark_prompted(state, sig)
            log(f"🔔 prompt recording: {title}")
            prompt_recording(title)
            time.sleep(interval)
    finally:
        try:
            PID_PATH.unlink(missing_ok=True)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Detect active meeting/call windows and prompt recording")
    parser.add_argument("command", nargs="?", default="daemon", choices=["daemon", "once"])
    args = parser.parse_args()
    if args.command == "once":
        raise SystemExit(run_once(args))
    run_daemon(args)


if __name__ == "__main__":
    main()
