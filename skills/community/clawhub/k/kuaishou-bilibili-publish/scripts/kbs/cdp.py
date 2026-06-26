"""CDP WebSocket 客户端（Browser, Page），用于快手 / B 站 / 抖音发布自动化。"""

from __future__ import annotations

import json
import logging
import platform as _platform
import random
import time
from typing import Any

import requests
import websockets.sync.client as ws_client

logger = logging.getLogger(__name__)


class CDPError(Exception):
    """CDP 通信异常。"""


class ElementNotFoundError(CDPError):
    """页面元素未找到。"""

    def __init__(self, selector: str) -> None:
        self.selector = selector
        super().__init__(f"未找到元素: {selector}")


# --- UA / Stealth（与 xiaohongshu-skills/xhs/stealth 对齐）---
_CHROME_FULL_VER = "136.0.0.0"


def build_ua_override(chrome_full_ver: str | None = None) -> dict:
    ver = chrome_full_ver or _CHROME_FULL_VER
    major = ver.split(".")[0]
    system = _platform.system()
    brands = [
        {"brand": "Chromium", "version": major},
        {"brand": "Google Chrome", "version": major},
        {"brand": "Not-A.Brand", "version": "24"},
    ]
    full_version_list = [
        {"brand": "Chromium", "version": ver},
        {"brand": "Google Chrome", "version": ver},
        {"brand": "Not-A.Brand", "version": "24.0.0.0"},
    ]
    if system == "Darwin":
        arch = "arm" if _platform.machine() == "arm64" else "x86"
        ua = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{ver} Safari/537.36"
        )
        nav_platform = "MacIntel"
        ua_platform = "macOS"
        platform_ver = "14.5.0"
    elif system == "Windows":
        arch = "x86"
        ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{ver} Safari/537.36"
        )
        nav_platform = "Win32"
        ua_platform = "Windows"
        platform_ver = "15.0.0"
    else:
        arch = "x86"
        ua = (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{ver} Safari/537.36"
        )
        nav_platform = "Linux x86_64"
        ua_platform = "Linux"
        platform_ver = "6.5.0"
    return {
        "userAgent": ua,
        "platform": nav_platform,
        "userAgentMetadata": {
            "brands": brands,
            "fullVersionList": full_version_list,
            "platform": ua_platform,
            "platformVersion": platform_ver,
            "architecture": arch,
            "model": "",
            "mobile": False,
            "bitness": "64",
            "wow64": False,
        },
    }


def _webgl() -> tuple[str, str]:
    system = _platform.system()
    if system == "Darwin":
        return (
            "Apple Inc.",
            "ANGLE (Apple, ANGLE Metal Renderer: Apple M1, Unspecified Version)",
        )
    if system == "Windows":
        return (
            "Google Inc. (Intel)",
            "ANGLE (Intel, Intel(R) UHD Graphics 630 (CML GT2), Direct3D11)",
        )
    return (
        "Google Inc. (Mesa)",
        "ANGLE (Mesa, Mesa Intel(R) UHD Graphics 630 (CML GT2), OpenGL 4.6)",
    )


_V, _R = _webgl()
_STEALTH_JS_TEMPLATE = """
(() => {
    const wd = Object.getOwnPropertyDescriptor(Navigator.prototype, 'webdriver');
    if (wd && wd.get) {
        Object.defineProperty(Navigator.prototype, 'webdriver', {
            get: new Proxy(wd.get, { apply: () => false }),
            configurable: true,
        });
    }
    if (!window.chrome) window.chrome = {};
    if (!window.chrome.runtime) {
        window.chrome.runtime = { connect: () => {}, sendMessage: () => {} };
    }
    Object.defineProperty(navigator, 'vendor', {
        get: () => 'Google Inc.',
        configurable: true,
    });
    Object.defineProperty(navigator, 'languages', {
        get: () => ['zh-CN', 'zh', 'en-US', 'en'],
        configurable: true,
    });
    const overrideWebGL = (proto) => {
        const original = proto.getParameter;
        proto.getParameter = function(p) {
            if (p === 37445) return '$$WEBGL_VENDOR$$';
            if (p === 37446) return '$$WEBGL_RENDERER$$';
            return original.call(this, p);
        };
    };
    overrideWebGL(WebGLRenderingContext.prototype);
    if (typeof WebGL2RenderingContext !== 'undefined') {
        overrideWebGL(WebGL2RenderingContext.prototype);
    }
})();
"""
STEALTH_JS = _STEALTH_JS_TEMPLATE.replace("$$WEBGL_VENDOR$$", _V).replace("$$WEBGL_RENDERER$$", _R)


class CDPClient:
    """底层 CDP WebSocket 通信客户端。"""

    def __init__(self, ws_url: str) -> None:
        self._ws = ws_client.connect(ws_url, max_size=50 * 1024 * 1024)
        self._id = 0
        self._callbacks: dict[int, Any] = {}

    def send(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        msg: dict[str, Any] = {"id": self._id, "method": method}
        if params:
            msg["params"] = params
        self._ws.send(json.dumps(msg))
        return self._wait_for(self._id)

    def _wait_for(self, msg_id: int, timeout: float = 30.0) -> dict:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                raw = self._ws.recv(timeout=max(0.1, deadline - time.monotonic()))
            except TimeoutError:
                break
            data = json.loads(raw)
            if data.get("id") == msg_id:
                if "error" in data:
                    raise CDPError(f"CDP 错误: {data['error']}")
                return data.get("result", {})
        raise CDPError(f"等待 CDP 响应超时 (id={msg_id})")

    def close(self) -> None:
        import contextlib

        with contextlib.suppress(Exception):
            self._ws.close()


class Page:
    """CDP 页面对象。"""

    def __init__(self, cdp: CDPClient, target_id: str, session_id: str) -> None:
        self._cdp = cdp
        self.target_id = target_id
        self.session_id = session_id
        self._ws = cdp._ws
        self._id_counter = 1000

    def _send_session(self, method: str, params: dict | None = None) -> dict:
        self._id_counter += 1
        msg: dict[str, Any] = {
            "id": self._id_counter,
            "method": method,
            "sessionId": self.session_id,
        }
        if params:
            msg["params"] = params
        self._ws.send(json.dumps(msg))
        return self._wait_session(self._id_counter)

    def _wait_session(self, msg_id: int, timeout: float = 120.0) -> dict:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                raw = self._ws.recv(timeout=max(0.1, deadline - time.monotonic()))
            except TimeoutError:
                break
            data = json.loads(raw)
            if data.get("id") == msg_id:
                if "error" in data:
                    raise CDPError(f"CDP 错误: {data['error']}")
                return data.get("result", {})
        raise CDPError(f"等待 session 响应超时 (id={msg_id})")

    def navigate(self, url: str) -> None:
        logger.info("导航到: %s", url)
        self._send_session("Page.navigate", {"url": url})

    def wait_for_load(self, timeout: float = 60.0) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                state = self.evaluate("document.readyState")
                if state == "complete":
                    return
            except CDPError:
                pass
            time.sleep(0.5)
        logger.warning("等待页面加载超时")

    def evaluate(self, expression: str, timeout: float = 30.0) -> Any:
        result = self._send_session(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": False,
            },
        )
        if "exceptionDetails" in result:
            raise CDPError(f"JS 执行异常: {result['exceptionDetails']}")
        remote_obj = result.get("result", {})
        return remote_obj.get("value")

    def query_selector(self, selector: str) -> str | None:
        result = self._send_session(
            "Runtime.evaluate",
            {
                "expression": f"document.querySelector({json.dumps(selector)})",
                "returnByValue": False,
            },
        )
        remote_obj = result.get("result", {})
        if remote_obj.get("subtype") == "null" or remote_obj.get("type") == "undefined":
            return None
        return remote_obj.get("objectId")

    def has_element(self, selector: str) -> bool:
        return self.evaluate(f"document.querySelector({json.dumps(selector)}) !== null") is True

    def wait_for_element(self, selector: str, timeout: float = 30.0) -> str:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            oid = self.query_selector(selector)
            if oid:
                return oid
            time.sleep(0.5)
        raise ElementNotFoundError(selector)

    def click_element(self, selector: str) -> None:
        box = self.evaluate(
            f"""
            (() => {{
                const el = document.querySelector({json.dumps(selector)});
                if (!el) return null;
                el.scrollIntoView({{block: 'center'}});
                const rect = el.getBoundingClientRect();
                return {{x: rect.left + rect.width / 2, y: rect.top + rect.height / 2}};
            }})()
            """
        )
        if not box:
            return
        x = box["x"] + random.uniform(-3, 3)
        y = box["y"] + random.uniform(-3, 3)
        self.mouse_move(x, y)
        time.sleep(random.uniform(0.03, 0.08))
        self.mouse_click(x, y)

    def input_text(self, selector: str, text: str) -> None:
        self.evaluate(
            f"""
            (() => {{
                const el = document.querySelector({json.dumps(selector)});
                if (!el) return;
                el.focus();
                el.value = {json.dumps(text)};
                el.dispatchEvent(new Event('input', {{bubbles: true}}));
                el.dispatchEvent(new Event('change', {{bubbles: true}}));
            }})()
            """
        )

    def input_content_editable(self, selector: str, text: str) -> None:
        self.evaluate(
            f"""
            (() => {{
                const el = document.querySelector({json.dumps(selector)});
                if (!el) return;
                el.focus();
                el.value = {json.dumps(text)};
                el.dispatchEvent(new Event('input', {{bubbles: true}}));
                el.dispatchEvent(new Event('change', {{bubbles: true}}));
            }})()
            """
        )

    def set_file_input(self, selector: str, files: list[str]) -> None:
        doc = self._send_session("DOM.getDocument", {"depth": 0})
        root_node_id = doc["root"]["nodeId"]
        result = self._send_session(
            "DOM.querySelector",
            {"nodeId": root_node_id, "selector": selector},
        )
        node_id = result.get("nodeId", 0)
        if node_id == 0:
            raise ElementNotFoundError(selector)
        self._send_session(
            "DOM.setFileInputFiles",
            {"nodeId": node_id, "files": files},
        )
        # 触发 change 事件（某些网站需要）
        self.evaluate(f"""
            (() => {{
                const el = document.querySelector({json.dumps(selector)});
                if (el) {{
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }})()
        """)

    def set_file_input_by_index(self, index: int, files: list[str]) -> None:
        """设置第 index 个 `input[type=file]` 的文件。"""
        uid = f"kbs-f-{random.randint(0, 1_000_000_000)}"
        ok = self.evaluate(
            f"""
            (() => {{
                const list = document.querySelectorAll('input[type=file]');
                const inp = list[{index}];
                if (!inp) return false;
                inp.setAttribute('data-kbs-tmp', '{uid}');
                return true;
            }})()
            """
        )
        if not ok:
            raise ElementNotFoundError(f"input[type=file]:nth({index})")
        try:
            self.set_file_input(f'input[type=file][data-kbs-tmp="{uid}"]', files)
        finally:
            self.evaluate(
                f"""
                (() => {{
                    const el = document.querySelector('input[type=file][data-kbs-tmp="{uid}"]');
                    if (el) el.removeAttribute('data-kbs-tmp');
                }})()
                """
            )

    def set_file_input_by_accept_hint(self, hint: str, files: list[str]) -> None:
        """设置第一个 `accept` 属性包含 hint 的文件输入框。"""
        uid = f"kbs-a-{random.randint(0, 1_000_000_000)}"
        ok = self.evaluate(
            f"""
            (() => {{
                const hint = {json.dumps(hint)};
                const list = document.querySelectorAll('input[type=file]');
                for (const inp of list) {{
                    const a = (inp.accept || '').toLowerCase();
                    if (a.includes(hint.toLowerCase())) {{
                        inp.setAttribute('data-kbs-tmp', '{uid}');
                        return true;
                    }}
                }}
                return false;
            }})()
            """
        )
        if not ok:
            raise ElementNotFoundError(f'input[type=file][accept*="{hint}"]')
        try:
            self.set_file_input(f'input[type=file][data-kbs-tmp="{uid}"]', files)
        finally:
            self.evaluate(
                f"""
                (() => {{
                    const el = document.querySelector('input[type=file][data-kbs-tmp="{uid}"]');
                    if (el) el.removeAttribute('data-kbs-tmp');
                }})()
                """
            )

    def body_text(self) -> str:
        return self.evaluate("document.body ? document.body.innerText : ''") or ""

    def mouse_move(self, x: float, y: float) -> None:
        self._send_session(
            "Input.dispatchMouseEvent",
            {"type": "mouseMoved", "x": x, "y": y},
        )

    def mouse_click(self, x: float, y: float, button: str = "left") -> None:
        self._send_session(
            "Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": x, "y": y, "button": button, "clickCount": 1},
        )
        self._send_session(
            "Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": x, "y": y, "button": button, "clickCount": 1},
        )

    def press_key(self, key: str) -> None:
        key_map = {
            "Enter": {"key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13},
            "Tab": {"key": "Tab", "code": "Tab", "windowsVirtualKeyCode": 9},
        }
        info = key_map.get(key, {"key": key, "code": key})
        self._send_session("Input.dispatchKeyEvent", {"type": "keyDown", **info})
        self._send_session("Input.dispatchKeyEvent", {"type": "keyUp", **info})

    def inject_stealth(self) -> None:
        self._send_session(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": STEALTH_JS},
        )

    def scroll_to_bottom(self) -> None:
        self.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_element_into_view(self, selector: str) -> None:
        self.evaluate(
            f"""
            (() => {{
                const el = document.querySelector({json.dumps(selector)});
                if (el) el.scrollIntoView({{behavior: 'instant', block: 'center'}});
            }})()
            """
        )

    def click_by_inner_text_then_center(self, substring: str) -> bool:
        """先标记可点击元素，再取中心坐标点击（更接近真实用户）。"""
        sub = json.dumps(substring)
        box = self.evaluate(
            f"""
            (() => {{
                const sub = {sub};
                const all = document.querySelectorAll('button, a, span, div');
                for (const el of all) {{
                    const t = (el.textContent || '').trim();
                    if (!t || !t.includes(sub)) continue;
                    const r = el.getBoundingClientRect();
                    if (r.width < 2 || r.height < 2) continue;
                    el.scrollIntoView({{block: 'center'}});
                    return {{x: r.left + r.width / 2, y: r.top + r.height / 2}};
                }}
                return null;
            }})()
            """
        )
        if not box:
            return False
        x = float(box["x"]) + random.uniform(-2, 2)
        y = float(box["y"]) + random.uniform(-2, 2)
        self.mouse_move(x, y)
        time.sleep(0.05)
        self.mouse_click(x, y)
        return True


class Browser:
    """Chrome CDP 控制器。"""

    def __init__(self, host: str = "127.0.0.1", port: int = 9222) -> None:
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self._cdp: CDPClient | None = None
        self._chrome_version: str | None = None

    def connect(self) -> None:
        resp = requests.get(f"{self.base_url}/json/version", timeout=5)
        resp.raise_for_status()
        info = resp.json()
        ws_url = info["webSocketDebuggerUrl"]
        browser_str = info.get("Browser", "")
        if "/" in browser_str:
            self._chrome_version = browser_str.split("/", 1)[1]
        logger.info("连接到 Chrome: %s (version=%s)", ws_url, self._chrome_version)
        self._cdp = CDPClient(ws_url)

    def _setup_page(self, page: Page) -> Page:
        import contextlib

        page.inject_stealth()
        page._send_session(
            "Emulation.setUserAgentOverride",
            build_ua_override(self._chrome_version),
        )
        page._send_session(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": random.randint(1366, 1920),
                "height": random.randint(768, 1080),
                "deviceScaleFactor": 1,
                "mobile": False,
            },
        )
        for perm in ("geolocation", "notifications", "midi", "camera", "microphone"):
            with contextlib.suppress(CDPError):
                assert self._cdp is not None
                self._cdp.send(
                    "Browser.setPermission",
                    {"permission": {"name": perm}, "setting": "denied"},
                )
        page._send_session("Page.enable")
        page._send_session("DOM.enable")
        page._send_session("Runtime.enable")
        return page

    def new_page(self, url: str = "about:blank") -> Page:
        if not self._cdp:
            self.connect()
        assert self._cdp is not None
        result = self._cdp.send("Target.createTarget", {"url": url})
        target_id = result["targetId"]
        result = self._cdp.send(
            "Target.attachToTarget",
            {"targetId": target_id, "flatten": True},
        )
        session_id = result["sessionId"]
        return self._setup_page(Page(self._cdp, target_id, session_id))

    def get_or_create_page(self) -> Page:
        if not self._cdp:
            self.connect()
        assert self._cdp is not None
        import contextlib

        resp = requests.get(f"{self.base_url}/json", timeout=5)
        targets = resp.json()
        for target in targets:
            if target.get("type") == "page" and target.get("url") in (
                "about:blank",
                "chrome://newtab/",
            ):
                target_id = target["id"]
                with contextlib.suppress(Exception):
                    result = self._cdp.send(
                        "Target.attachToTarget",
                        {"targetId": target_id, "flatten": True},
                    )
                    session_id = result.get("sessionId")
                    if session_id:
                        logger.debug("复用空白 tab: %s", target_id)
                        return self._setup_page(Page(self._cdp, target_id, session_id))
        return self.new_page()

    def get_existing_page(self) -> Page | None:
        if not self._cdp:
            self.connect()
        assert self._cdp is not None
        resp = requests.get(f"{self.base_url}/json", timeout=5)
        targets = resp.json()
        for target in targets:
            if target.get("type") == "page" and target.get("url") != "about:blank":
                target_id = target["id"]
                result = self._cdp.send(
                    "Target.attachToTarget",
                    {"targetId": target_id, "flatten": True},
                )
                session_id = result["sessionId"]
                page = Page(self._cdp, target_id, session_id)
                page._send_session("Page.enable")
                page._send_session("DOM.enable")
                page._send_session("Runtime.enable")
                page.inject_stealth()
                return page
        return None

    def close_page(self, page: Page) -> None:
        import contextlib

        if self._cdp:
            with contextlib.suppress(CDPError):
                self._cdp.send("Target.closeTarget", {"targetId": page.target_id})

    def close(self) -> None:
        if self._cdp:
            self._cdp.close()
            self._cdp = None


def wait_until_upload_hints(
    page: Page,
    ready_hints: tuple[str, ...],
    fail_hints: tuple[str, ...],
    timeout: float = 300.0,
    poll: float = 2.0,
) -> str:
    """轮询 `document.body.innerText`，直到出现就绪/失败提示或超时。

    Returns:
        ``\"ready\"`` | ``\"fail\"`` | ``\"timeout\"``
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            text = page.body_text()
        except CDPError:
            text = ""
        for h in fail_hints:
            if h and h in text:
                return "fail"
        for h in ready_hints:
            if h and h in text:
                return "ready"
        time.sleep(poll)
    return "timeout"
