from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import websockets.sync.client as ws_client

from .errors import BridgeError

logger = logging.getLogger("gumtree-bridge-client")

BRIDGE_PORT = 9335
BRIDGE_URL = f"ws://localhost:{BRIDGE_PORT}"


class BridgePage:
    def __init__(self, bridge_url: str = BRIDGE_URL, timeout: float = 90.0) -> None:
        self._bridge_url = bridge_url
        self._timeout = timeout

    def _call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        msg: dict[str, Any] = {"role": "cli", "method": method}
        if params:
            msg["params"] = params
        try:
            with ws_client.connect(self._bridge_url, close_timeout=5) as conn:
                conn.send(json.dumps(msg, ensure_ascii=False))
                raw = conn.recv(timeout=self._timeout)
        except OSError as exc:
            raise BridgeError(f"无法连接到 bridge server（{self._bridge_url}）: {exc}") from exc

        result = json.loads(raw)
        if "error" in result and result["error"]:
            raise BridgeError(result["error"])
        return result.get("result")

    def navigate(self, url: str) -> None:
        self._call("navigate", {"url": url})

    def wait_for_load(self, timeout: int = 60000) -> None:
        self._call("wait_for_load", {"timeout": timeout})

    def wait_dom_stable(self, timeout: int = 10000, interval: int = 500) -> None:
        self._call("wait_dom_stable", {"timeout": timeout, "interval": interval})

    def evaluate(self, expression: str) -> Any:
        return self._call("evaluate", {"expression": expression})

    def is_server_running(self) -> bool:
        try:
            with ws_client.connect(self._bridge_url, open_timeout=3, close_timeout=5) as conn:
                conn.send(json.dumps({"role": "cli", "method": "ping_server"}, ensure_ascii=False))
                raw = conn.recv(timeout=5)
        except Exception:
            return False

        result = json.loads(raw)
        return "result" in result

    def is_extension_connected(self) -> bool:
        try:
            with ws_client.connect(self._bridge_url, open_timeout=3, close_timeout=5) as conn:
                conn.send(json.dumps({"role": "cli", "method": "ping_server"}, ensure_ascii=False))
                raw = conn.recv(timeout=5)
        except Exception:
            return False

        result = json.loads(raw)
        return bool(result.get("result", {}).get("extension_connected"))


def _open_chrome() -> None:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if os.path.exists(path):
            subprocess.Popen([path])
            return

    for cmd in [["open", "-a", "Google Chrome"], ["google-chrome"], ["chromium-browser"]]:
        try:
            subprocess.Popen(cmd)
            return
        except FileNotFoundError:
            continue
    logger.warning("找不到 Chrome，请手动打开浏览器")


def ensure_bridge_ready(port: int = BRIDGE_PORT) -> None:
    client = BridgePage(bridge_url=f"ws://localhost:{port}")

    if not client.is_server_running():
        logger.info("Bridge server 未运行，正在启动...")
        server_script = Path(__file__).resolve().parent.parent / "bridge_server.py"
        kwargs: dict[str, Any] = {
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
        }
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
        subprocess.Popen(
            [sys.executable, str(server_script), "--port", str(port)],
            **kwargs,
        )

        for _ in range(10):
            time.sleep(1)
            if client.is_server_running():
                logger.info("Bridge server 已启动")
                break
        else:
            raise BridgeError("Bridge server 启动超时，请手动运行 scripts/bridge_server.py")

    if client.is_extension_connected():
        return

    logger.info("浏览器扩展未连接，正在打开 Chrome...")
    _open_chrome()

    for _ in range(20):
        time.sleep(1)
        if client.is_extension_connected():
            logger.info("浏览器扩展已连接")
            return

    raise BridgeError("等待 Gumtree Bridge 扩展连接超时，请确认扩展已安装并启用")
