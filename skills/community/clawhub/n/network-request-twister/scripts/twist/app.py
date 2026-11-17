"""Application orchestrator.

Wires together browser launch, CDP connection, target selection, and
interception into a single async run() entry point.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from .browser import Browser
from .cdp import CDP, CDPTarget
from .config import Config, load_config
from .intercept import Intercept
from .logger import get as get_logger, init as init_logger
from .observe import Observe, ObserveOptions
from .target import Target


@dataclass
class Options:
    """All CLI-parsed runtime options."""

    host: str = "127.0.0.1"
    port: int = 9222
    launch: bool = False
    launch_browser: str = "chrome"
    launch_args: list[str] = field(default_factory=list)
    url: str = ""
    config_file: str = ""
    config_data: bytes | None = None
    list_targets: bool = False
    target: str = ""
    verbose: bool = False
    timeout: int = 15
    observe: ObserveOptions = field(default_factory=ObserveOptions)


class TwistApp:
    """Top-level application that owns the full lifecycle."""

    def __init__(self, opts: Options) -> None:
        self._opts = opts
        self._browser: Browser | None = None
        self._cdp: CDP | None = None
        self._config: Config | None = None
        self._task: asyncio.Task[Any] | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run(self) -> None:
        """Execute the main application logic."""
        init_logger(verbose=self._opts.verbose)
        log = get_logger()

        if self._opts.list_targets:
            await self._run_list_targets()
            return

        if self._opts.observe.enabled:
            await self._run_observe()
            return

        await self._run_intercept()

    async def shutdown(self) -> None:
        """Clean up resources."""
        if self._browser is not None:
            self._browser.stop()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _setup_session(self) -> CDP:
        """Launch browser, connect CDP, select target, attach. Returns the connected CDP.

        Does NOT navigate — callers must navigate after enabling required CDP domains
        to ensure interception covers the initial document request.
        """
        log = get_logger()

        host = self._opts.host
        if self._opts.launch:
            host = "127.0.0.1"

        self._browser = Browser(launch=self._opts.launch, port=self._opts.port)
        self._browser.start(
            browser_type=self._opts.launch_browser,
            extra_args=self._opts.launch_args,
            url="about:blank",
        )
        if self._browser.launched:
            log.info(
                "browser launched",
                extra={"ctx": {"browser": self._opts.launch_browser, "port": self._opts.port}},
            )

        self._cdp = CDP(host, self._opts.port, self._opts.timeout, self._opts.verbose)
        try:
            await self._cdp.connect()
        except Exception:
            if self._browser.launched:
                self._browser.stop()
            raise

        target_selector = Target(self._cdp)
        select_url = "" if self._opts.launch else self._opts.url
        selected = await target_selector.select(
            target_id=self._opts.target, url=select_url
        )

        await self._cdp.attach_to_target(selected.id)
        await self._cdp.close_browser()

        log.info(
            "target selected", extra={"ctx": {"id": selected.id, "url": selected.url}}
        )

        return self._cdp

    async def _run_list_targets(self) -> None:
        log = get_logger()
        self._cdp = CDP(self._opts.host, self._opts.port, self._opts.timeout, self._opts.verbose)
        await self._cdp.connect()
        try:
            targets = await self._cdp.list_targets()
            log.info("targets listed", extra={"ctx": {"count": len(targets)}})
            _print_targets(targets)
        finally:
            await self._cdp.close()

    async def _run_intercept(self) -> None:
        log = get_logger()

        config_data = self._opts.config_data
        if config_data is None:
            raise ValueError("config_data is required for interception")
        self._config = load_config(config_data)
        log.info(
            "config loaded",
            extra={"ctx": {"name": self._config.name, "rules": len(self._config.rules)}},
        )

        await self._setup_session()

        intercept = Intercept(self._cdp, self._config)  # type: ignore[arg-type]
        log.info("interception started")
        await intercept.start(navigate_url=self._opts.url)

    async def _run_observe(self) -> None:
        log = get_logger()

        await self._setup_session()

        observe = Observe(self._cdp, self._opts.observe)  # type: ignore[arg-type]
        log.info("observation started")
        await observe.start(navigate_url=self._opts.url)


# ------------------------------------------------------------------
# Target display
# ------------------------------------------------------------------


def _print_targets(targets: list[CDPTarget]) -> None:
    try:
        from wcwidth import wcswidth
    except ImportError:
        wcswidth = len

    def _display_width(s: str) -> int:
        return wcswidth(s) if wcswidth is not len else len(s)

    def _pad_right(s: str, width: int) -> str:
        dw = _display_width(s)
        return s + " " * (width - dw) if dw < width else s

    def _truncate(s: str, width: int) -> str:
        if _display_width(s) <= width:
            return s
        result: list[str] = []
        w = 0
        for ch in s:
            cw = 2 if ord(ch) > 127 else 1
            if w + cw > width - 3:
                break
            result.append(ch)
            w += cw
        return "".join(result) + "..."

    id_w = 34
    title_w = 30
    print(f"{_pad_right('ID', id_w)}  {_pad_right('TITLE', title_w)}  URL")
    for t in targets:
        if t.type != "page":
            continue
        tid = _truncate(t.id, id_w)
        ttl = _truncate(t.title, title_w)
        url = t.url
        if _display_width(url) > 80:
            url = _truncate(url, 77) + "..."
        print(f"{_pad_right(tid, id_w)}  {_pad_right(ttl, title_w)}  {url}")
