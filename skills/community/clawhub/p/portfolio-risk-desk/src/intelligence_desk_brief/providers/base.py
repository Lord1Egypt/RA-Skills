"""Provider interfaces for future live adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from intelligence_desk_brief.contracts import (
    CreateBriefRequest,
    WriteBriefToNotionInput,
    WriteBriefToNotionOutput,
)
from intelligence_desk_brief.memory import MemoryContext, MemoryRecord


class RetrievalAdapter(ABC):
    @abstractmethod
    def collect(self, request: CreateBriefRequest) -> list[dict[str, Any]]:
        """Return raw evidence items for the request."""


class MemoryAdapter(ABC):
    @abstractmethod
    def recall_context(self, request: CreateBriefRequest) -> MemoryContext:
        """Return recalled brief context for the current request."""

    @abstractmethod
    def store_brief(self, request: CreateBriefRequest, record: MemoryRecord) -> None:
        """Persist useful brief state for future comparison."""


class DeliveryAdapter(ABC):
    @abstractmethod
    def write_brief(self, request: WriteBriefToNotionInput) -> WriteBriefToNotionOutput:
        """Persist or hand off a rendered brief through a delivery channel."""
