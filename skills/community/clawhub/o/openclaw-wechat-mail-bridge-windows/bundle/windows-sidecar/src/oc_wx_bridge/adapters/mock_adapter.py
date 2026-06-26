from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
import time
from typing import Callable
import uuid

from .base import ChatTarget
from ..models import AdapterHealth, IncomingMessage

LOGGER = logging.getLogger(__name__)


@dataclass
class MockAdapter:
    sidecar_id: str
    watch_poll_interval_sec: float

    def health(self) -> AdapterHealth:
        return AdapterHealth(ok=True, name="mock", detail="mock adapter ready")

    def list_groups(self) -> list[ChatTarget]:
        return [
            ChatTarget(chat_id="mock-group-001", chat_name="Ops Group"),
            ChatTarget(chat_id="mock-group-002", chat_name="Mail Group"),
        ]

    def watch(self, handler: Callable[[IncomingMessage], None]) -> None:
        LOGGER.info("mock adapter watch loop started")
        last_emit = 0.0
        while True:
            now = time.time()
            if now - last_emit >= 15:
                event_id = f"evt_{uuid.uuid4().hex}"
                message_id = f"mockmsg_{uuid.uuid4().hex[:10]}"
                ts = datetime.now(timezone.utc).isoformat()
                handler(
                    IncomingMessage(
                        event_id=event_id,
                        sidecar_id=self.sidecar_id,
                        chat_id="mock-group-001",
                        chat_name="Ops Group",
                        sender_display_name="MockUser",
                        message_id=message_id,
                        message_text="/mail someone@example.com",
                        message_time=ts,
                        observed_at=ts,
                    )
                )
                last_emit = now
            time.sleep(max(0.1, self.watch_poll_interval_sec))

    def send_text(self, chat_id: str, text: str) -> None:
        LOGGER.info("mock send to chat_id=%s text=%s", chat_id, text.replace("\n", "\\n"))

