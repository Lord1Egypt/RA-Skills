from __future__ import annotations

import logging
import time

from .bridge_client import BridgeClient
from .models import IncomingMessage
from .adapters.base import WeChatDesktopAdapter

LOGGER = logging.getLogger(__name__)


class MessageWatcher:
    def __init__(
        self,
        adapter: WeChatDesktopAdapter,
        bridge_client: BridgeClient,
        allow_groups: list[str],
    ) -> None:
        self._adapter = adapter
        self._bridge_client = bridge_client
        self._allow_groups = allow_groups
        self._seen_keys: dict[str, float] = {}
        self._seen_ttl_sec = 600
        self._seen_limit = 5000

    def run_forever(self) -> None:
        LOGGER.info("message watcher started")
        self._adapter.watch(self._handle_message)

    def _handle_message(self, message: IncomingMessage) -> None:
        if self._allow_groups and message.chat_name not in self._allow_groups and message.chat_id not in self._allow_groups:
            LOGGER.debug("message ignored by allowlist chat_id=%s chat_name=%s", message.chat_id, message.chat_name)
            return

        key = f"{message.chat_id}:{message.message_id}"
        now = time.time()
        self._prune_seen(now)
        if key in self._seen_keys:
            LOGGER.debug("message deduped key=%s", key)
            return
        self._seen_keys[key] = now

        try:
            response = self._bridge_client.post_event(message)
            LOGGER.info("event posted event_id=%s response=%s", message.event_id, response)
        except Exception as error:
            LOGGER.exception("failed to post event event_id=%s error=%s", message.event_id, error)

    def _prune_seen(self, now: float) -> None:
        if len(self._seen_keys) > self._seen_limit:
            keys = sorted(self._seen_keys.items(), key=lambda item: item[1])
            remove_count = len(self._seen_keys) - self._seen_limit
            for idx in range(remove_count):
                self._seen_keys.pop(keys[idx][0], None)

        expiry = now - self._seen_ttl_sec
        for key, ts in list(self._seen_keys.items()):
            if ts < expiry:
                self._seen_keys.pop(key, None)
