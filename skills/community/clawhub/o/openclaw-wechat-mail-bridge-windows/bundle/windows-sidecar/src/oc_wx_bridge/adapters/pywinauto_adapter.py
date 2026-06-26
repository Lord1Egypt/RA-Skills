from __future__ import annotations

from dataclasses import dataclass
import logging
import time
from typing import Callable

from .base import ChatTarget
from ..models import AdapterHealth, IncomingMessage

LOGGER = logging.getLogger(__name__)


@dataclass
class PywinautoAdapter:
    sidecar_id: str
    watch_poll_interval_sec: float
    _last_sent_text: str = ""
    _last_sent_at: float = 0.0

    def health(self) -> AdapterHealth:
        try:
            from pywinauto import findwindows  # type: ignore

            windows = findwindows.find_windows(title_re=".*微信.*")
            if not windows:
                return AdapterHealth(
                    ok=False,
                    name="pywinauto",
                    detail="pywinauto available, but WeChat window not found",
                )
            return AdapterHealth(
                ok=True,
                name="pywinauto",
                detail=f"pywinauto available, detected {len(windows)} WeChat window(s)",
            )
        except Exception as error:
            return AdapterHealth(
                ok=False,
                name="pywinauto",
                detail=f"pywinauto not ready: {error}",
            )

    def list_groups(self) -> list[ChatTarget]:
        try:
            from pywinauto import Application  # type: ignore

            app = Application(backend="uia").connect(title_re=".*微信.*", timeout=5)
            window = app.top_window()

            candidates: list[ChatTarget] = []
            seen: set[str] = set()
            for elem in window.descendants(control_type="ListItem"):
                try:
                    name = (elem.window_text() or "").strip()
                except Exception:
                    continue
                if not name or len(name) > 80:
                    continue
                if name in seen:
                    continue
                seen.add(name)
                candidates.append(ChatTarget(chat_id=name, chat_name=name))
                if len(candidates) >= 100:
                    break
            return candidates
        except Exception as error:
            LOGGER.warning("pywinauto list_groups failed error=%s", error)
            return []

    def watch(self, handler: Callable[[IncomingMessage], None]) -> None:
        LOGGER.info("pywinauto watch loop started")
        last_fingerprint = ""
        while True:
            try:
                from datetime import datetime, timezone
                import uuid
                from pywinauto import Application  # type: ignore

                app = Application(backend="uia").connect(title_re=".*微信.*", timeout=5)
                window = app.top_window()
                message_items = window.descendants(control_type="ListItem")
                tail_texts: list[str] = []
                for item in message_items[-12:]:
                    try:
                        txt = (item.window_text() or "").strip()
                    except Exception:
                        continue
                    if txt:
                        tail_texts.append(txt)
                if tail_texts:
                    latest = tail_texts[-1]
                    fingerprint = latest
                    if fingerprint != last_fingerprint:
                        if latest == self._last_sent_text and (time.time() - self._last_sent_at) < 4:
                            last_fingerprint = fingerprint
                            continue
                        ts = datetime.now(timezone.utc).isoformat()
                        handler(
                            IncomingMessage(
                                event_id=f"evt_{uuid.uuid4().hex}",
                                sidecar_id=self.sidecar_id,
                                chat_id="pywinauto-current-chat",
                                chat_name="WeChat Current Chat",
                                sender_display_name="unknown",
                                message_id="",
                                message_text=latest,
                                message_time=ts,
                                observed_at=ts,
                            )
                        )
                        last_fingerprint = fingerprint
            except Exception as error:
                LOGGER.debug("pywinauto watch tick failed error=%s", error)
            time.sleep(max(0.2, self.watch_poll_interval_sec))

    def send_text(self, chat_id: str, text: str) -> None:
        try:
            from pywinauto import Application  # type: ignore
            from pywinauto.keyboard import send_keys  # type: ignore

            app = Application(backend="uia").connect(title_re=".*微信.*", timeout=5)
            window = app.top_window()
            window.set_focus()

            # Best-effort navigation: Ctrl+F search target chat id/name then send.
            send_keys("^f")
            send_keys(chat_id, with_spaces=True, pause=0.02)
            send_keys("{ENTER}")
            send_keys(text, with_spaces=True, pause=0.01)
            send_keys("{ENTER}")
            self._last_sent_text = text
            self._last_sent_at = time.time()
            LOGGER.info("pywinauto send attempted chat_id=%s", chat_id)
        except Exception as error:
            raise RuntimeError(f"pywinauto send_text failed: {error}") from error
