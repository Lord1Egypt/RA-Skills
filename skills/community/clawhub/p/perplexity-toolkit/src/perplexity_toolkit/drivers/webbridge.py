"""Kimi WebBridge driver implementation."""

import json
import logging
import time as _time
import urllib.error
import urllib.request
from typing import Any, Callable, Optional

from .base import BrowserDriver

logger = logging.getLogger(__name__)


def _truncate(value, limit: int = 300) -> str:
    s = str(value)
    return s if len(s) <= limit else s[:limit] + "..."


# ── Classification & custom error ────────────────────────────────


def _classify_error(msg: str) -> str:
    """Classify an error string into a WebBridgeError kind."""
    if not isinstance(msg, str):
        return "protocol"
    msg_lower = msg.lower()
    if "502" in msg or "bad gateway" in msg_lower:
        return "http_502"
    if "timed out" in msg_lower or "timeout" in msg_lower:
        return "timeout"
    if "connection" in msg_lower or "refused" in msg_lower or "unreachable" in msg_lower:
        return "connect"
    return "protocol"


class WebBridgeError(RuntimeError):
    """Classified WebBridge failure with a machine-readable `.kind`."""

    def __init__(self, kind: str, message: str):
        self.kind = kind
        super().__init__(message)


# ── Internal transport (replaceable for tests) ───────────────────


def _urlopen_json(url: str, payload: dict, timeout: float = 30) -> dict:
    """Default transport: urllib POST → JSON dict."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raw = resp.read().decode("utf-8", errors="replace")
            return {"error": f"HTTP {resp.status}: {raw[:200]}"}
        return json.loads(resp.read().decode("utf-8"))


# ── Driver ───────────────────────────────────────────────────────


class WebBridgeDriver(BrowserDriver):
    """Browser driver using Kimi WebBridge daemon (localhost:10086)."""

    def __init__(self, url: str = "http://127.0.0.1:10086/command",
                 session: str = "perplexity-search",
                 *,
                 transport: Optional[Callable[[str, dict], dict]] = None,
                 sleep: Callable[[float], None] = _time.sleep):
        self.url = url
        self.session = session
        self._transport = transport or _urlopen_json
        self._sleep = sleep

    # ── Internal send helpers ──────────────────────────────────

    def _send(self, action: str, args: Optional[dict] = None) -> dict:
        """Low-level send: returns a dict (may contain ``\"error\": …``)."""
        payload = {
            "action": action,
            "args": args or {},
            "session": self.session,
        }
        logger.debug("WebBridge -> %s action=%s", self.url, action)
        try:
            resp = self._transport(self.url, payload)
        except Exception as e:
            msg = f"WebBridge transport error: {e}"
            logger.error(msg)
            return {"error": msg}
        if resp.get("error"):
            logger.warning("WebBridge action=%s returned error: %s",
                           action, resp["error"])
        else:
            logger.debug("WebBridge <- action=%s ok", action)
        return resp

    # ── Idempotent accessors (list_tabs / snapshot / read-only evaluate) ──
    # These call `_send_checked` which may raise WebBridgeError on error
    # with a one-retry-after-2s for timeouts and 502s.

    def _send_checked(self, action: str, args: Optional[dict] = None,
                      *, retry: bool = False) -> dict:
        """Like _send but raises WebBridgeError (classified) on failure."""
        for attempt in range(2 if retry else 1):
            resp = self._send(action, args)
            err = resp.get("error")
            if not err:
                return resp
            kind = _classify_error(str(err))
            if retry and attempt + 1 < 2 and kind in ("timeout", "http_502", "connect"):
                self._sleep(2)
                continue
            raise WebBridgeError(kind, str(err))
        # Not reached
        raise WebBridgeError("protocol", "unreachable")  # pragma: no cover

    def evaluate(self, code: str, *, mutating: bool = True) -> Any:
        """Execute JS; raises WebBridgeError on error.

        Default ``mutating=True`` (safe — no automatic retry). Set
        ``mutating=False`` for read-only probes (one retry on timeout/502).
        """
        resp = self._send_checked("evaluate", {"code": code},
                                  retry=not mutating)
        val = resp.get("data", {}).get("value", "")
        if isinstance(val, str):
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                return val
        return val

    def list_tabs(self) -> dict:
        return self._send("list_tabs", {})

    def snapshot(self) -> dict:
        return self._send("snapshot", {})

    # ── State-changing actions (navigate / click / fill / cdp / …) ──
    # These always return dicts and NEVER retry.

    def navigate(self, url: str, new_tab: bool = True,
                 group_title: str = "") -> dict:
        args: dict = {"url": url, "newTab": new_tab}
        if group_title:
            args["group_title"] = group_title
        result = self._send("navigate", args)
        # Reopen in a new tab when the saved tab went stale.
        if not result.get("ok") and not new_tab:
            err = result.get("error", "") or str(result)
            if "No tab" in err or "Bad Gateway" in err:
                logger.warning("Tab stale, opening new tab")
                args["newTab"] = True
                result = self._send("navigate", args)
        return result

    def click(self, selector: str) -> dict:
        return self._send("click", {"selector": selector})

    def fill(self, selector: str, value: str) -> dict:
        return self._send("fill", {"selector": selector, "value": value})

    def screenshot(self, path: Optional[str] = None) -> dict:
        args: dict = {"format": "png"}
        if path:
            args["path"] = path
        return self._send("screenshot", args)

    def close(self) -> dict:
        return self._send("close_session", {})

    def cdp(self, method: str, params: Optional[dict] = None) -> dict:
        args: dict = {"method": method}
        if params:
            args["params"] = params
        return self._send("cdp", args)