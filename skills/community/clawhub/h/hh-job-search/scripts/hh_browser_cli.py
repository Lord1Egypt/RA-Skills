#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Any

OPENCLAW_BIN = shutil.which("openclaw") or "openclaw"
DEFAULT_PROFILE = "chrome-relay"


class BrowserCliError(RuntimeError):
    pass


@dataclass
class BrowserResult:
    raw: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.raw.get("ok", True))

    @property
    def result(self) -> Any:
        return self.raw.get("result")

    @property
    def url(self) -> str | None:
        return self.raw.get("url")

    @property
    def target_id(self) -> str | None:
        return self.raw.get("targetId")


class BrowserCli:
    def __init__(self, profile: str = DEFAULT_PROFILE, timeout_ms: int = 30000):
        self.profile = profile
        self.timeout_ms = timeout_ms

    def _run(self, args: list[str]) -> dict[str, Any]:
        cmd = [OPENCLAW_BIN, "browser", "--browser-profile", self.profile, "--timeout", str(self.timeout_ms), "--json", *args]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise BrowserCliError(proc.stderr.strip() or proc.stdout.strip() or f"browser command failed: {' '.join(cmd)}")
        out = proc.stdout.strip()
        if not out:
            return {}
        try:
            return json.loads(out)
        except json.JSONDecodeError as e:
            raise BrowserCliError(f"failed to decode browser JSON: {e}\nSTDOUT:\n{out}") from e

    def status(self) -> dict[str, Any]:
        return self._run(["status"])

    def tabs(self) -> dict[str, Any]:
        return self._run(["tabs"])

    def navigate(self, url: str, target_id: str | None = None) -> BrowserResult:
        args = ["navigate", url]
        if target_id:
            args += ["--target-id", target_id]
        return BrowserResult(self._run(args))

    def evaluate(self, fn: str, target_id: str | None = None, retries: int = 0, retry_delay_ms: int = 1200) -> BrowserResult:
        args = ["evaluate", "--fn", fn]
        if target_id:
            args += ["--target-id", target_id]
        attempt = 0
        while True:
            try:
                return BrowserResult(self._run(args))
            except BrowserCliError as e:
                msg = str(e)
                retryable = "Execution context was destroyed" in msg or "ERR_ABORTED" in msg
                if not retryable or attempt >= retries:
                    raise
                time.sleep(retry_delay_ms / 1000)
                attempt += 1

    def current_page(self, target_id: str | None = None) -> BrowserResult:
        return self.evaluate("() => ({title: document.title, url: location.href, origin: location.origin})", target_id, retries=1)

    def navigate_js(self, url: str, target_id: str | None = None) -> BrowserResult:
        payload = json.dumps(url, ensure_ascii=False)
        try:
            return self.evaluate(f"() => {{ window.location.href = {payload}; return {{navigatingTo: {payload}}}; }}", target_id)
        except BrowserCliError as e:
            msg = str(e)
            if "Execution context was destroyed" in msg or "ERR_ABORTED" in msg:
                return BrowserResult({"ok": True, "result": {"navigatingTo": url}})
            raise

    def wait_time(self, ms: int, target_id: str | None = None) -> BrowserResult:
        args = ["wait", "--time", str(ms)]
        if target_id:
            args += ["--target-id", target_id]
        return BrowserResult(self._run(args))

    def ensure_ready(self) -> None:
        data = self.status()
        if not data.get("running") or not data.get("cdpReady"):
            raise BrowserCliError(f"browser profile {self.profile!r} is not attached/ready: {json.dumps(data, ensure_ascii=False)}")

    def current_target(self) -> str:
        tabs = self.tabs().get("tabs") or []
        if not tabs:
            raise BrowserCliError(f"browser profile {self.profile!r} has no attached tabs")
        return tabs[0]["targetId"]
