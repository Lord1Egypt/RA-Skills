#!/usr/bin/env python3
"""
Kindle Monitor — Claude Code 状态监视屏服务器

监听 Claude Code hooks 转发过来的事件，渲染成 e-ink 友好的 HTML，
让 Kindle / 旧 iPad / 旧手机的浏览器一眼看到："正在做什么 / 等不等用户"。

启动:  python3 server.py
打开:  http://<Mac-IP>:8787/  (Kindle 浏览器)
事件:  POST http://localhost:8787/event  (hooks 调)
"""
import json
import os
import socket
import sys
import threading
import time
from collections import deque
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html import escape

PORT = int(os.environ.get("KINDLE_MONITOR_PORT", "8787"))
REFRESH_SEC = int(os.environ.get("KINDLE_MONITOR_REFRESH", "3"))
WAITING_TIMEOUT_SEC = int(os.environ.get("KINDLE_MONITOR_WAITING_TIMEOUT", "300"))  # 5 分钟没新事件自动解锁
TOOL_STALL_SEC = int(os.environ.get("KINDLE_MONITOR_TOOL_STALL", "20"))  # PreToolUse 后 N 秒还没等到 Post，认为在等用户确认
LOG_FILE = os.path.expanduser("~/.claude/kindle-monitor/events.jsonl")
EVENT_BUFFER = 8  # 最近 N 条事件展示在仪表盘

# ---------- 共享状态 ----------
state = {
    "status": "idle",           # idle / thinking / tool / waiting / done / error
    "tool": None,               # 当前工具名
    "tool_input": None,         # 当前工具的简短输入摘要
    "tool_started_at": None,    # 当前工具的开始时间，用于探测"等用户确认"
    "tool_session": None,       # 当前 tool 来自哪个 session
    "session_id": None,
    "project": None,            # cwd 短名
    "last_event_at": None,
    "session_start_at": None,
    "tool_count": 0,
    "message": None,            # 最近的提示消息（Notification）
    "needs_attention": False,   # 是否在等用户
    "waiting_session": None,    # 哪个 session 在等确认 (粘性，多session下不被冲掉)
    "waiting_project": None,    # 等确认那个 session 的项目名
    "waiting_since": None,      # 进入 waiting 的时间，用于超时兜底
    "waiting_inferred": False,  # 是否是基于 tool stall 推断出的 waiting（vs Notification 显式触发）
}
recent = deque(maxlen=EVENT_BUFFER)
state_lock = threading.Lock()


def short(text, n=80):
    if not text:
        return ""
    text = str(text).replace("\n", " ").strip()
    return text if len(text) <= n else text[:n - 1] + "…"


def fmt_duration(start_iso):
    if not start_iso:
        return "—"
    try:
        start = datetime.fromisoformat(start_iso)
        sec = int((datetime.now() - start).total_seconds())
        if sec < 60:
            return f"{sec}s"
        if sec < 3600:
            return f"{sec // 60}m{sec % 60:02d}s"
        return f"{sec // 3600}h{(sec % 3600) // 60:02d}m"
    except Exception:
        return "—"


def derive_project(payload):
    cwd = payload.get("cwd") or os.getcwd()
    return os.path.basename(cwd) or cwd


def clear_waiting_lock():
    """清掉 waiting 锁（不动 banner 状态本身）。"""
    state["waiting_session"] = None
    state["waiting_project"] = None
    state["waiting_since"] = None
    state["waiting_inferred"] = False


def waiting_expired():
    """检查 waiting 是否已超时。"""
    since = state.get("waiting_since")
    if not since:
        return False
    try:
        t0 = datetime.fromisoformat(since)
        return (datetime.now() - t0).total_seconds() > WAITING_TIMEOUT_SEC
    except Exception:
        return False


def check_stall_and_promote():
    """如果当前在 tool 执行状态，但 PreToolUse 已经过去 TOOL_STALL_SEC 秒还没 PostToolUse，
    认为是在等用户确认（Claude Code 不一定为权限确认发 Notification），把状态升级为 waiting。
    """
    if state.get("status") != "tool":
        return
    started = state.get("tool_started_at")
    if not started:
        return
    try:
        t0 = datetime.fromisoformat(started)
        elapsed = (datetime.now() - t0).total_seconds()
    except Exception:
        return
    if elapsed < TOOL_STALL_SEC:
        return
    # 升级为 waiting (基于推断)
    tool = state.get("tool") or "?"
    tool_input = state.get("tool_input") or ""
    state["status"] = "waiting"
    state["needs_attention"] = True
    state["message"] = f"[推断] {tool} 已 {int(elapsed)}s 未返回，可能在等你确认: {tool_input}"
    state["waiting_session"] = state.get("tool_session")
    state["waiting_project"] = state.get("project")
    state["waiting_since"] = datetime.now().isoformat(timespec="seconds")
    state["waiting_inferred"] = True


def update_state(event_type, payload):
    """根据 hook 事件更新共享 state。

    多 session 规则：waiting 状态是粘性的——
    一旦某 session 进入 waiting，其他 session 的事件只追加到事件流，
    不会改 banner 状态。只有该 session 自己的 UserPromptSubmit / Stop / SessionEnd
    才能解除 waiting。
    """
    with state_lock:
        now = datetime.now().isoformat(timespec="seconds")
        evt_session = payload.get("session_id")
        state["last_event_at"] = now

        # 如果当前处于 waiting，且事件不是来自 waiting session，
        # 仅追加事件流，不动 banner / message / 项目名
        # 但若 waiting 已超时，先把锁解掉再走正常路径
        if state.get("status") == "waiting" and waiting_expired():
            clear_waiting_lock()
            state["status"] = "idle"
            state["message"] = None
            state["needs_attention"] = False

        # 如果是基于推断（waiting_inferred）的 waiting，PostToolUse / Stop / UserPromptSubmit
        # 任一到来都说明判错了或确认完成了，立刻解锁走正常路径
        if state.get("waiting_inferred") and event_type in (
            "PostToolUse", "Stop", "UserPromptSubmit", "SessionEnd"
        ):
            clear_waiting_lock()
            state["message"] = None
            state["needs_attention"] = False
            # status 让下面的状态机自己设

        is_locked = (
            state.get("status") == "waiting"
            and state.get("waiting_session")
            and evt_session
            and evt_session != state["waiting_session"]
        )

        if is_locked:
            # 仍然加入 recent 事件流（带 [其他 session] 标记）
            tool_input = payload.get("tool_input") or {}
            summary_other = (
                payload.get("message")
                or tool_input.get("command")
                or tool_input.get("file_path")
                or tool_input.get("pattern")
                or tool_input.get("path")
                or ""
            )
            recent.appendleft({
                "t": now,
                "type": f"~{event_type}",   # ~ 前缀表示"来自其他 session"
                "tool": payload.get("tool_name"),
                "summary": short(summary_other, 50),
            })
            return

        # 正常路径：更新 session/project/状态机
        state["session_id"] = evt_session or state["session_id"]
        state["project"] = derive_project(payload)

        if event_type == "SessionStart":
            state["status"] = "idle"
            state["session_start_at"] = now
            state["tool_count"] = 0
            state["needs_attention"] = False
            state["message"] = None

        elif event_type == "UserPromptSubmit":
            state["status"] = "thinking"
            state["needs_attention"] = False
            state["message"] = None
            # 如果是 waiting session 自己提交了 prompt，说明已确认
            if evt_session and evt_session == state.get("waiting_session"):
                clear_waiting_lock()

        elif event_type == "PreToolUse":
            tool_name = payload.get("tool_name") or payload.get("tool") or "?"
            tool_input = payload.get("tool_input") or {}
            # 摘要：Bash 取 command，Write/Edit 取 file_path，其他取整体 short
            summary = (
                tool_input.get("command")
                or tool_input.get("file_path")
                or tool_input.get("pattern")
                or tool_input.get("path")
                or json.dumps(tool_input, ensure_ascii=False)[:80]
            )
            state["status"] = "tool"
            state["tool"] = tool_name
            state["tool_input"] = short(summary, 100)
            state["tool_count"] += 1
            state["tool_started_at"] = now
            state["tool_session"] = evt_session
            state["needs_attention"] = False
            state["message"] = None

        elif event_type == "PostToolUse":
            state["status"] = "thinking"
            state["tool_started_at"] = None
            state["tool_session"] = None

        elif event_type == "Notification":
            state["status"] = "waiting"
            state["needs_attention"] = True
            state["message"] = short(payload.get("message"), 140)
            # 标记 waiting session（粘性，带超时戳）
            state["waiting_session"] = evt_session
            state["waiting_project"] = state["project"]
            state["waiting_since"] = now
            state["waiting_inferred"] = False  # 显式 Notification

        elif event_type == "Stop":
            state["status"] = "done"
            state["needs_attention"] = False
            state["tool"] = None
            state["tool_input"] = None
            state["tool_started_at"] = None
            state["tool_session"] = None
            state["message"] = None
            # 如果 waiting 那个 session 自己 Stop 了，清锁
            if evt_session and evt_session == state.get("waiting_session"):
                clear_waiting_lock()

        elif event_type == "SessionEnd":
            state["status"] = "idle"
            state["tool_started_at"] = None
            state["tool_session"] = None
            if evt_session and evt_session == state.get("waiting_session"):
                clear_waiting_lock()

        elif event_type == "Error":
            state["status"] = "error"
            state["needs_attention"] = True
            state["message"] = short(payload.get("message"), 140)

        recent.appendleft({
            "t": now,
            "type": event_type,
            "tool": state.get("tool"),
            "summary": state.get("tool_input") or state.get("message") or "",
        })


def log_event(event_type, payload):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "t": datetime.now().isoformat(timespec="seconds"),
                "type": event_type,
                "payload": payload,
            }, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ---------- HTML 渲染 ----------

STATUS_LABEL = {
    "idle": "就绪",
    "thinking": "思考中",
    "tool": "执行中",
    "waiting": "请 确 认",
    "done": "已完成",
    "error": "✕ 出错",
}

# 中央大字状态对应的视觉强度（e-ink 友好的纯黑白配色）
STATUS_BANNER_BG = {
    "idle": "#ffffff",
    "thinking": "#ffffff",
    "tool": "#ffffff",
    "waiting": "#000000",   # 等用户：反白震一下
    "done": "#ffffff",
    "error": "#000000",
}
STATUS_BANNER_FG = {
    "idle": "#000000",
    "thinking": "#000000",
    "tool": "#000000",
    "waiting": "#ffffff",
    "done": "#000000",
    "error": "#ffffff",
}


def render_html():
    with state_lock:
        # 即使没有新事件来，每次 render 也检查一遍
        # 1. tool 执行卡住 → 推断为 waiting
        check_stall_and_promote()
        # 2. waiting 是否过期
        if state.get("status") == "waiting" and waiting_expired():
            clear_waiting_lock()
            state["status"] = "idle"
            state["message"] = None
            state["needs_attention"] = False
        s = dict(state)
        events = list(recent)

    label = STATUS_LABEL.get(s["status"], s["status"])
    bg = STATUS_BANNER_BG.get(s["status"], "#ffffff")
    fg = STATUS_BANNER_FG.get(s["status"], "#000000")

    # 构建事件列表 HTML
    rows = []
    for e in events:
        t_short = e["t"].split("T")[1] if "T" in e["t"] else e["t"]
        summary = short(e.get("summary") or "", 50)
        line = f"{t_short}  {e['type']:>14}  {summary}"
        rows.append(f"<div class='ev'>{escape(line)}</div>")
    events_html = "\n".join(rows) or "<div class='ev'>—</div>"

    duration = fmt_duration(s["session_start_at"])
    last_at = s["last_event_at"] or "—"
    if "T" in str(last_at):
        last_at = str(last_at).split("T")[1]

    tool_line = ""
    if s["status"] == "tool" and s["tool"]:
        tool_line = f"<div class='tool'>{escape(s['tool'])}</div>"
        if s["tool_input"]:
            tool_line += f"<div class='tool-input'>{escape(s['tool_input'])}</div>"

    msg_line = ""
    if s["message"]:
        msg_line = f"<div class='msg'>{escape(s['message'])}</div>"

    # waiting 时显示是哪个项目在等
    waiting_line = ""
    if s["status"] == "waiting" and s.get("waiting_project"):
        waiting_line = f"<div class='waiting-proj'>项目：{escape(s['waiting_project'])}</div>"

    # e-ink 友好：纯黑白 + 大字号 + 不要圆角阴影 + meta refresh
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="{REFRESH_SEC}">
<title>Claude Code Monitor</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: Helvetica, Arial, sans-serif;
    background: #ffffff;
    color: #000000;
    padding: 20px;
    -webkit-text-size-adjust: 100%;
  }}
  .banner {{
    background: {bg};
    color: {fg};
    text-align: center;
    padding: 28px 12px;
    font-size: 56px;
    font-weight: bold;
    letter-spacing: 0.05em;
    border: 3px solid #000;
    margin-bottom: 18px;
  }}
  .tool {{ font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 6px; }}
  .tool-input {{
    font-family: Menlo, Courier, monospace;
    font-size: 18px; text-align: center; margin-bottom: 16px;
    word-break: break-all;
  }}
  .waiting-proj {{
    font-size: 24px; font-weight: bold; text-align: center;
    margin: 6px 0 14px; letter-spacing: 0.04em;
  }}
  .msg {{
    border: 2px solid #000; padding: 10px 14px;
    font-size: 22px; margin: 16px 0;
    background: #fff;
  }}
  .meta {{
    border-top: 1px solid #000;
    padding-top: 10px; margin-top: 18px;
    font-size: 18px;
    display: table; width: 100%;
  }}
  .meta div {{ display: table-cell; padding: 4px 0; }}
  .meta b {{ display: block; font-size: 14px; }}
  h2 {{ font-size: 18px; margin: 18px 0 6px; border-bottom: 1px solid #000; padding-bottom: 4px; }}
  .ev {{ font-family: Menlo, Courier, monospace; font-size: 14px; line-height: 1.55; }}
  .footer {{ margin-top: 22px; font-size: 12px; text-align: center; }}
</style>
</head>
<body>
  <div class="banner">{label}</div>
  {waiting_line}
  {tool_line}
  {msg_line}
  <div class="meta">
    <div><b>项目</b>{escape(s['project'] or '—')}</div>
    <div><b>工具数</b>{s['tool_count']}</div>
    <div><b>时长</b>{duration}</div>
    <div><b>更新</b>{last_at}</div>
  </div>
  <h2>最近事件</h2>
  {events_html}
  <div class="footer">每 {REFRESH_SEC} 秒自动刷新 · session: {escape((s['session_id'] or '—')[:8])}</div>
</body></html>
"""


# ---------- HTTP Server ----------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # 安静些
        pass

    def _send(self, status, body, ctype="text/html; charset=utf-8"):
        body_bytes = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body_bytes)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body_bytes)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, render_html())
        elif self.path == "/raw.json":
            with state_lock:
                payload = {"state": dict(state), "recent": list(recent)}
            self._send(200, json.dumps(payload, ensure_ascii=False, indent=2),
                       "application/json; charset=utf-8")
        elif self.path == "/healthz":
            self._send(200, "ok", "text/plain")
        elif self.path == "/reset":
            with state_lock:
                clear_waiting_lock()
                state["status"] = "idle"
                state["message"] = None
                state["needs_attention"] = False
                state["tool"] = None
                state["tool_input"] = None
                recent.clear()
            self._send(200, "<html><body><h1>已重置</h1><a href='/'>返回</a></body></html>")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/event":
            self._send(404, "not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            data = json.loads(raw or "{}")
        except Exception as e:
            self._send(400, f"bad json: {e}", "text/plain")
            return
        event_type = data.get("event") or data.get("hook_event_name") or "Unknown"
        update_state(event_type, data)
        log_event(event_type, data)
        self._send(200, "ok", "text/plain")


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    ip = get_lan_ip()
    print(f"Kindle Monitor running")
    print(f"  Mac:    http://localhost:{PORT}/")
    print(f"  Kindle: http://{ip}:{PORT}/")
    print(f"  Hook:   POST http://localhost:{PORT}/event")
    print(f"  Logs:   {LOG_FILE}")
    print(f"  Refresh every {REFRESH_SEC}s, Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye.")
        server.shutdown()


if __name__ == "__main__":
    sys.exit(main())
