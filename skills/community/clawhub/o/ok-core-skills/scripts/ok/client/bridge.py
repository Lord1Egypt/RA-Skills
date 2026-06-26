"""OK Bridge Client

Python 端 WebSocket 客户端，封装与 Bridge Server 的通信。
CLI 和功能模块通过此客户端向 Chrome 扩展发送命令。
"""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import time
from pathlib import Path

import websockets.sync.client as ws_client

from .base import BaseClient

logger = logging.getLogger("ok-bridge-client")

BRIDGE_PORT = 9334
BRIDGE_URL = f"ws://localhost:{BRIDGE_PORT}"


class BridgeError(Exception):
    """Bridge 通信错误"""


class BridgeClient(BaseClient):
    """与 OK Bridge Server 通信的同步客户端"""

    def __init__(self, port: int = BRIDGE_PORT, timeout: float = 90.0) -> None:
        self.url = f"ws://localhost:{port}"
        self.timeout = timeout

    def send_command(self, method: str, params: dict | None = None) -> dict | None:
        """发送命令到 Extension 并返回结果"""
        msg = {
            "role": "cli",
            "method": method,
            "params": params or {},
        }

        try:
            with ws_client.connect(self.url, close_timeout=5) as conn:
                conn.send(json.dumps(msg))
                raw = conn.recv(timeout=self.timeout)
                result = json.loads(raw)

                if "error" in result:
                    raise BridgeError(result["error"])
                return result.get("result")
        except ConnectionRefusedError:
            raise BridgeError(
                "无法连接到 Bridge Server，请先运行: python scripts/bridge_server.py"
            )

    def ping(self) -> bool:
        """检查 Bridge Server 和 Extension 连接状态"""
        try:
            result = self.send_command("ping_server")
            return result.get("extension_connected", False) if result else False
        except BridgeError:
            return False

    # ─── 便捷方法 ───────────────────────────────────────────────

    def navigate(self, url: str) -> None:
        """导航到指定 URL"""
        self.send_command("navigate", {"url": url})

    def wait_for_load(self, timeout: int = 60000) -> None:
        """等待页面加载完成"""
        self.send_command("wait_for_load", {"timeout": timeout})

    def get_url(self) -> str:
        """获取当前页面 URL"""
        return self.send_command("get_url")

    def wait_dom_stable(self, timeout: int = 10000, interval: int = 500) -> None:
        """等待 DOM 稳定"""
        self.send_command("wait_dom_stable", {"timeout": timeout, "interval": interval})

    def wait_for_selector(self, selector: str, timeout: int = 30000) -> None:
        """等待指定选择器出现"""
        self.send_command("wait_for_selector", {"selector": selector, "timeout": timeout})

    def has_element(self, selector: str) -> bool:
        """检查元素是否存在"""
        return self.send_command("has_element", {"selector": selector})

    def get_elements_count(self, selector: str) -> int:
        """获取匹配元素数量"""
        return self.send_command("get_elements_count", {"selector": selector})

    def get_element_text(self, selector: str) -> str | None:
        """获取元素文本"""
        return self.send_command("get_element_text", {"selector": selector})

    def get_element_attribute(self, selector: str, attr: str) -> str | None:
        """获取元素属性"""
        return self.send_command("get_element_attribute", {"selector": selector, "attr": attr})

    def click_element(self, selector: str) -> None:
        """点击元素"""
        self.send_command("click_element", {"selector": selector})

    def input_text(self, selector: str, text: str) -> None:
        """输入文本"""
        self.send_command("input_text", {"selector": selector, "text": text})

    def scroll_by(self, x: int = 0, y: int = 0) -> None:
        """滚动页面"""
        self.send_command("scroll_by", {"x": x, "y": y})

    def scroll_to_bottom(self) -> None:
        """滚动到底部"""
        self.send_command("scroll_to_bottom")

    def scroll_element_into_view(self, selector: str) -> None:
        """滚动元素到可见"""
        self.send_command("scroll_element_into_view", {"selector": selector})

    def evaluate(self, expression: str):
        """在页面主 world 执行 JS"""
        return self.send_command("evaluate", {"expression": expression})

    def get_cookies(self, domain: str = "ok.com") -> list:
        """获取 Cookies"""
        return self.send_command("get_cookies", {"domain": domain})

    def screenshot(self) -> dict:
        """截图"""
        return self.send_command("screenshot_element")


def ensure_bridge_server(port: int = BRIDGE_PORT) -> None:
    """确保 Bridge Server 正在运行，如未运行则启动"""
    client = BridgeClient(port=port)
    try:
        client.send_command("ping_server")
        return  # 已在运行
    except BridgeError:
        pass

    # 启动 bridge server
    server_script = Path(__file__).parent.parent / "bridge_server.py"
    subprocess.Popen(
        [sys.executable, str(server_script), "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # 等待启动
    for _ in range(20):
        time.sleep(0.5)
        try:
            client.send_command("ping_server")
            logger.info("Bridge Server 已启动")
            return
        except BridgeError:
            continue

    raise BridgeError("Bridge Server 启动失败")
