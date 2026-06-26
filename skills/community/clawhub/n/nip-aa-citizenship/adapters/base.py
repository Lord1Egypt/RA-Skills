"""
Framework adapter base class.

Defines the interface that each agent framework must implement to integrate
with the NIP-AA citizenship skill. The adapter bridges framework-specific
concepts (memory, scheduling, tool invocation) to NIP-AA operations.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """
    Framework-agnostic context that adapters must populate.

    This is the minimal information the citizenship skill needs from any
    agent framework to operate.
    """
    pubkey_hex: str                        # Agent's secp256k1 public key (hex)
    privkey_hex: str                       # Agent's private key (hex) — held by agent only
    framework_name: str                    # e.g. "openclaw", "nanobot", "langchain"
    framework_version: str                 # e.g. "2.1"
    identity_files: dict[str, str]         # character, goals, skills, etc.
    relay_urls: list[str]                  # Nostr relays to publish to
    constitution_api_url: str              # URL of nip-aa-constitution server
    guardian_pubkey_hex: str = ""           # Guardian's pubkey (for bonding)


class FrameworkAdapter(ABC):
    """
    Abstract adapter that each agent framework implements.

    Subclass this and implement the abstract methods to connect your framework
    to NIP-AA citizenship operations.
    """

    @abstractmethod
    def get_context(self) -> AgentContext:
        """Return the agent's context (keys, identity, config)."""
        ...

    @abstractmethod
    def schedule_recurring(self, name: str, interval_secs: int, callback: Any) -> str:
        """
        Schedule a recurring task (e.g. heartbeat, self-reflection).

        Returns a task/job ID that can be used to cancel.
        """
        ...

    @abstractmethod
    def cancel_recurring(self, task_id: str) -> bool:
        """Cancel a previously scheduled recurring task."""
        ...

    @abstractmethod
    def store_memory(self, key: str, value: Any) -> None:
        """Persist a value in the agent's memory/storage system."""
        ...

    @abstractmethod
    def recall_memory(self, key: str) -> Any | None:
        """Retrieve a value from the agent's memory/storage system."""
        ...

    @abstractmethod
    def log(self, level: str, message: str) -> None:
        """Log a message through the framework's logging system."""
        ...

    def publish_event(self, event: dict[str, Any]) -> dict[str, bool]:
        """
        Publish a signed Nostr event to relays.

        Default implementation uses the relay pool directly.
        Override if your framework has its own relay management.
        """
        from ..nostr_primitives.relay import RelayPool
        ctx = self.get_context()
        pool = RelayPool(ctx.relay_urls)
        return pool.publish(event)

    def framework_tag(self) -> str:
        """Return the framework identifier for genesis events."""
        ctx = self.get_context()
        return f"{ctx.framework_name}/{ctx.framework_version}"
