#!/usr/bin/env python3
"""
PaperTrade + ONDO 对冲机器人 - 本地 Web 控制面板

启动: python web_server.py
然后在浏览器打开 http://localhost:8765

功能:
- 可视化填写和保存 .env 配置
- 一键启动/停止对冲机器人
- 实时查看运行日志和账户状态
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).parent.resolve()
ENV_FILE = BASE_DIR / ".env"
ENV_EXAMPLE = BASE_DIR / ".env.example"
HTML_FILE = BASE_DIR / "index.html"
LOG_FILE = BASE_DIR / "bot.log"
PID_FILE = BASE_DIR / "bot.pid"

PORT = 8765


# ── 配置读写 ──────────────────────────────────────────────────
def load_env() -> dict:
    """读取 .env 文件为 dict"""
    env = {}
    if not ENV_FILE.exists():
        # 从 .env.example 复制默认值
        if ENV_EXAMPLE.exists():
            with open(ENV_EXAMPLE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip()
        return env
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def save_env(env: dict):
    """保存配置到 .env 文件"""
    lines = []
    # 保留注释和分组
    order = [
        "HEDGE_MODE",
        "PAPER_WALLET_PRIVATE_KEY",
        "PAPER_SESSION_KEY",
        "ONDO_KEY_ID",
        "ONDO_API_SECRET",
        "HEDGE_SYMBOL",
        "HEDGE_POSITION_SIZE",
        "HEDGE_PAPER_LEVERAGE",
        "HEDGE_ONDO_LEVERAGE",
        "HEDGE_TARGET_MOVE_PCT",
        "HEDGE_MAX_HOLD_SECONDS",
        "HEDGE_POLL_INTERVAL",
        "HEDGE_MAX_CYCLES",
        "HEDGE_DIRECTION",
    ]
    # 先写有序的
    written = set()
    for key in order:
        if key in env:
            lines.append(f"{key}={env[key]}")
            written.add(key)
    # 再写额外的
    for key, val in env.items():
        if key not in written:
            lines.append(f"{key}={val}")
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ── 进程管理 ──────────────────────────────────────────────────
def is_running() -> bool:
    """检查机器人进程是否在运行"""
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)  # signal 0 只检查进程是否存在
        return True
    except (ValueError, ProcessLookupError, PermissionError):
        return False


def get_pid() -> int | None:
    if PID_FILE.exists():
        try:
            return int(PID_FILE.read_text().strip())
        except ValueError:
            return None
    return None


def start_bot() -> dict:
    """启动对冲机器人"""
    if is_running():
        return {"success": False, "message": "机器人已在运行中"}
    # 清空旧日志
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    log_fp = open(LOG_FILE, "a", encoding="utf-8")
    # 使用 -u 禁用输出缓冲，确保日志实时写入文件
    proc = subprocess.Popen(
        [sys.executable, "-u", "main.py"],
        cwd=str(BASE_DIR),
        stdout=log_fp,
        stderr=subprocess.STDOUT,
        start_new_session=True,  # 独立进程组
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )
    PID_FILE.write_text(str(proc.pid))
    time.sleep(1)
    if is_running():
        return {"success": True, "message": f"机器人已启动 (PID: {proc.pid})", "pid": proc.pid}
    else:
        return {"success": False, "message": "机器人启动失败，请检查日志"}


def stop_bot() -> dict:
    """停止对冲机器人"""
    if not is_running():
        return {"success": False, "message": "机器人未运行"}
    pid = get_pid()
    if pid:
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            # 等待进程结束
            for _ in range(20):
                if not is_running():
                    break
                time.sleep(0.5)
            # 如果还在运行，强制杀死
            if is_running():
                os.killpg(os.getpgid(pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
    if PID_FILE.exists():
        PID_FILE.unlink()
    return {"success": True, "message": "机器人已停止"}


def tail_log(lines: int = 100) -> list[str]:
    """读取日志文件的最后 N 行"""
    if not LOG_FILE.exists():
        return []
    with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
        all_lines = f.readlines()
    return [line.rstrip() for line in all_lines[-lines:]]


# ── HTTP 服务器 ──────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # 静默日志

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status: int = 200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            if HTML_FILE.exists():
                self._send_html(HTML_FILE.read_text(encoding="utf-8"))
            else:
                self._send_html("<h1>index.html not found</h1>", 404)
            return

        if path == "/api/config":
            self._send_json({"success": True, "config": load_env()})
            return

        if path == "/api/status":
            running = is_running()
            pid = get_pid()
            self._send_json({
                "success": True,
                "running": running,
                "pid": pid,
                "log": tail_log(150),
            })
            return

        if path == "/api/log":
            self._send_json({"success": True, "log": tail_log(300)})
            return

        self._send_json({"success": False, "message": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}

        if path == "/api/config":
            try:
                save_env(data)
                self._send_json({"success": True, "message": "配置已保存到 .env"})
            except Exception as e:
                self._send_json({"success": False, "message": str(e)}, 500)
            return

        if path == "/api/start":
            result = start_bot()
            self._send_json(result, 200 if result["success"] else 400)
            return

        if path == "/api/stop":
            result = stop_bot()
            self._send_json(result)
            return

        self._send_json({"success": False, "message": "Not found"}, 404)


def main():
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print("=" * 60)
    print("  PaperTrade + ONDO 对冲机器人 - Web 控制面板")
    print("=" * 60)
    print(f"  服务地址: http://localhost:{PORT}")
    print(f"  项目目录: {BASE_DIR}")
    print(f"  配置文件: {ENV_FILE}")
    print(f"  日志文件: {LOG_FILE}")
    print("=" * 60)
    print("  按 Ctrl+C 停止服务")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
