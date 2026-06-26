"""
Relay interaction primitives for NIP-AA agents.

Thin wrapper around WebSocket-based Nostr relay communication, used by both
the DM module and the event publisher.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from typing import Any

logger = logging.getLogger(__name__)


class RelayPool:
    """
    Manages connections to multiple Nostr relays for event publication and querying.

    Usage:
        pool = RelayPool(["wss://relay.damus.io", "wss://nos.lol"])
        pool.publish(event)
        events = pool.query({"kinds": [1], "#t": ["nip-aa"]})
    """

    def __init__(self, relay_urls: list[str], timeout: int = 10):
        self.relay_urls = relay_urls
        self.timeout = timeout

    def publish(self, event: dict[str, Any]) -> dict[str, bool]:
        """Publish a signed event to all relays. Returns {url: success}."""
        results = {}
        for url in self.relay_urls:
            results[url] = self._send_event(url, event)
        return results

    def query(
        self,
        filters: dict[str, Any],
        relay_url: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Query events from a single relay (or first available).

        Returns list of raw Nostr event dicts.
        """
        targets = [relay_url] if relay_url else self.relay_urls
        for url in targets:
            events = self._query_relay(url, filters)
            if events is not None:
                return events
        return []

    def query_all(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Query all relays and deduplicate by event ID."""
        seen: set[str] = set()
        results: list[dict[str, Any]] = []
        for url in self.relay_urls:
            events = self._query_relay(url, filters)
            if events:
                for event in events:
                    eid = event.get("id", "")
                    if eid and eid not in seen:
                        seen.add(eid)
                        results.append(event)
        return results

    # ── Internal ──────────────────────────────────────────────────────────

    def _send_event(self, relay_url: str, event: dict[str, Any]) -> bool:
        try:
            import websocket
            ws = websocket.create_connection(relay_url, timeout=self.timeout)
            ws.send(json.dumps(["EVENT", event]))
            resp = ws.recv()
            ws.close()
            logger.debug("Published to %s: %s", relay_url, resp)
            return True
        except Exception as exc:
            logger.warning("Publish to %s failed: %s", relay_url, exc)
            return False

    def _query_relay(
        self, relay_url: str, filters: dict[str, Any]
    ) -> list[dict[str, Any]] | None:
        try:
            import websocket
            ws = websocket.create_connection(relay_url, timeout=self.timeout)
            sub_id = hashlib.sha256(os.urandom(16)).hexdigest()[:16]
            ws.send(json.dumps(["REQ", sub_id, filters]))

            events: list[dict[str, Any]] = []
            while True:
                raw = ws.recv()
                data = json.loads(raw)
                if data[0] == "EOSE":
                    break
                if data[0] == "EVENT" and len(data) >= 3:
                    events.append(data[2])

            ws.close()
            return events
        except Exception as exc:
            logger.warning("Query %s failed: %s", relay_url, exc)
            return None
