from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from ..models import AdapterHealth, IncomingMessage


@dataclass
class ChatTarget:
    chat_id: str
    chat_name: str


class WeChatDesktopAdapter(Protocol):
    def health(self) -> AdapterHealth:
        ...

    def list_groups(self) -> list[ChatTarget]:
        ...

    def watch(self, handler: Callable[[IncomingMessage], None]) -> None:
        ...

    def send_text(self, chat_id: str, text: str) -> None:
        ...

