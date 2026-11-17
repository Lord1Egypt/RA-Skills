"""Target (tab) selection strategies.

ID exact match → create and navigate → first page-type target.
"""

from __future__ import annotations

from .cdp import CDP, CDPTarget


class TargetError(Exception):
    """Raised when no suitable tab can be found or created."""


class Target:
    """Selects a browser tab for interception."""

    def __init__(self, cdp: CDP) -> None:
        self._cdp = cdp

    async def select(
        self, target_id: str = "", url: str = ""
    ) -> CDPTarget:
        """Pick a tab using the first applicable strategy."""
        if target_id:
            return await self._by_id(target_id)
        if url:
            return await self._create_and_navigate(url)
        return await self._first_page()

    async def _by_id(self, target_id: str) -> CDPTarget:
        targets = await self._cdp.list_targets()
        for t in targets:
            if t.id == target_id:
                return t
        raise TargetError(f"target {target_id!r} not found")

    async def _create_and_navigate(self, url: str) -> CDPTarget:
        return await self._cdp.new_tab(url)

    async def _first_page(self) -> CDPTarget:
        targets = await self._cdp.list_targets()
        for t in targets:
            if t.type == "page":
                return t
        raise TargetError("no page target found")
