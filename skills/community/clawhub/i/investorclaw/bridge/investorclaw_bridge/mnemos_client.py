# SPDX-License-Identifier: Apache-2.0
"""MnemosClient — Python HTTP client to mnemos-rs container.

Mirrors the Rust trait `MnemosClient` defined in mnemos-os/mnemos-rs.
Same wire contract; different language. ic-engine code uses this wherever
it needs to read/write memories — never imports mnemos internals directly
(per GRAEAE module-boundary discipline).

In the v4.0 deploy, mnemos-rs runs as a sibling container on compose's
bridge network at `MNEMOS_BASE` (default `http://mnemos:5002`). This
client uses MCP-HTTP to call its tools.

Module boundary contract: this is THE ONLY file in ic-engine bridge that
talks to mnemos. Everything else routes through this module.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class Memory:
    """A single memory record. Mirrors mnemos-rs Memory struct shape."""
    id: str
    content: str
    category: str
    tags: list[str]
    created_at: str
    metadata: dict[str, Any] | None = None


class MnemosClient:
    """HTTP client to mnemos-rs. Async-first.

    Construction:
        client = MnemosClient.from_env()         # reads MNEMOS_BASE + MNEMOS_AUTH_TOKEN
        client = MnemosClient(base_url, token)   # explicit
    """

    def __init__(
        self,
        base_url: str = "http://mnemos:5002",
        auth_token: str | None = None,
        timeout_sec: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self._headers = (
            {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        )
        self._timeout = timeout_sec

    @classmethod
    def from_env(cls) -> "MnemosClient":
        return cls(
            base_url=os.environ.get("MNEMOS_BASE", "http://mnemos:5002"),
            auth_token=os.environ.get("MNEMOS_AUTH_TOKEN"),
        )

    # ─── Memory operations (matching mnemos MCP tool catalog) ──────────

    async def search_memories(
        self,
        query: str,
        category: str | None = None,
        limit: int = 10,
        min_score: float = 0.3,
    ) -> list[Memory]:
        """Full-text + semantic search."""
        # TODO[v4.0-impl]: switch to MCP-HTTP /mcp tools/call for canonical wire
        # protocol. Using REST shim for v0.1 simplicity until mnemos-rs MCP
        # transport landing is confirmed by codex orientation.
        body = {"query": query, "limit": limit, "min_score": min_score}
        if category:
            body["category"] = category
        async with httpx.AsyncClient(timeout=self._timeout) as h:
            r = await h.post(
                f"{self.base_url}/memories/search",
                json=body,
                headers=self._headers,
            )
            r.raise_for_status()
            return [_memory_from_dict(m) for m in r.json().get("results", [])]

    async def create_memory(
        self,
        content: str,
        category: str = "imported",
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Memory:
        """Persist a new memory observation."""
        body = {
            "content": content,
            "category": category,
            "tags": tags or [],
        }
        if metadata:
            body["metadata"] = metadata
        async with httpx.AsyncClient(timeout=self._timeout) as h:
            r = await h.post(
                f"{self.base_url}/memories",
                json=body,
                headers=self._headers,
            )
            r.raise_for_status()
            return _memory_from_dict(r.json())

    async def list_memories(
        self,
        category: str | None = None,
        limit: int = 50,
    ) -> list[Memory]:
        params: dict[str, Any] = {"limit": limit}
        if category:
            params["category"] = category
        async with httpx.AsyncClient(timeout=self._timeout) as h:
            r = await h.get(
                f"{self.base_url}/memories",
                params=params,
                headers=self._headers,
            )
            r.raise_for_status()
            return [_memory_from_dict(m) for m in r.json().get("memories", [])]

    async def health(self) -> bool:
        """True if mnemos-rs is up and healthy."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as h:
                r = await h.get(f"{self.base_url}/healthz")
                return r.status_code == 200
        except (httpx.RequestError, httpx.HTTPStatusError):
            return False


def _memory_from_dict(d: dict[str, Any]) -> Memory:
    return Memory(
        id=d["id"],
        content=d["content"],
        category=d.get("category", "imported"),
        tags=d.get("tags", []),
        created_at=d.get("created_at") or d.get("created", ""),
        metadata=d.get("metadata"),
    )
