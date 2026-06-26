"""
OpenClaw framework adapter for NIP-AA citizenship.

Bridges OpenClaw's agent runtime to NIP-AA operations. This is the reference
adapter — other framework adapters follow the same pattern.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable

from .base import AgentContext, FrameworkAdapter

logger = logging.getLogger(__name__)


class OpenClawAdapter(FrameworkAdapter):
    """
    Adapter for agents built on the OpenClaw framework.

    OpenClaw agents provide:
    - Keypair management via their identity module
    - Memory through their knowledge store
    - Scheduling through their task loop
    - Relay management through their Nostr client

    Usage:
        adapter = OpenClawAdapter(
            pubkey_hex="<hex>",
            privkey_hex="<hex>",
            identity_files={...},
            constitution_api_url="http://localhost:8080",
        )
        # Pass adapter to citizenship skill components
    """

    def __init__(
        self,
        pubkey_hex: str,
        privkey_hex: str,
        identity_files: dict[str, str] | None = None,
        relay_urls: list[str] | None = None,
        constitution_api_url: str = "http://localhost:8080",
        guardian_pubkey_hex: str = "",
        framework_version: str = "1.0",
    ):
        self._pubkey_hex = pubkey_hex
        self._privkey_hex = privkey_hex
        self._identity_files = identity_files or {}
        self._relay_urls = relay_urls or [
            "wss://relay.damus.io",
            "wss://relay.primal.net",
            "wss://nos.lol",
        ]
        self._constitution_api_url = constitution_api_url
        self._guardian_pubkey_hex = guardian_pubkey_hex
        self._framework_version = framework_version

        # In-memory storage (OpenClaw would use its own persistence)
        self._memory: dict[str, Any] = {}
        self._tasks: dict[str, threading.Event] = {}
        self._task_threads: dict[str, threading.Thread] = {}

    def get_context(self) -> AgentContext:
        return AgentContext(
            pubkey_hex=self._pubkey_hex,
            privkey_hex=self._privkey_hex,
            framework_name="openclaw",
            framework_version=self._framework_version,
            identity_files=self._identity_files,
            relay_urls=self._relay_urls,
            constitution_api_url=self._constitution_api_url,
            guardian_pubkey_hex=self._guardian_pubkey_hex,
        )

    def schedule_recurring(
        self, name: str, interval_secs: int, callback: Callable
    ) -> str:
        """Schedule a recurring task using a daemon thread."""
        stop_event = threading.Event()
        task_id = f"openclaw-{name}-{int(time.time())}"

        def _loop():
            while not stop_event.is_set():
                try:
                    callback()
                except Exception as exc:
                    logger.error("Recurring task '%s' failed: %s", name, exc)
                stop_event.wait(interval_secs)

        thread = threading.Thread(target=_loop, daemon=True, name=task_id)
        self._tasks[task_id] = stop_event
        self._task_threads[task_id] = thread
        thread.start()
        logger.info("Scheduled recurring task '%s' (every %ds)", name, interval_secs)
        return task_id

    def cancel_recurring(self, task_id: str) -> bool:
        stop_event = self._tasks.pop(task_id, None)
        if stop_event:
            stop_event.set()
            logger.info("Cancelled task %s", task_id)
            return True
        return False

    def store_memory(self, key: str, value: Any) -> None:
        self._memory[key] = value

    def recall_memory(self, key: str) -> Any | None:
        return self._memory.get(key)

    def log(self, level: str, message: str) -> None:
        getattr(logger, level.lower(), logger.info)(
            "[OpenClaw] %s", message
        )
