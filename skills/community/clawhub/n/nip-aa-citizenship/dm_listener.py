"""
Persistent DM Listener for NIP-AA agents.

Provides a background WebSocket listener that:
  - Maintains robust, auto-reconnecting connections to all configured relays
  - Receives and decrypts incoming kind-4 DMs in real time
  - Enforces guardian-approved relationship permissions
  - Persists every inbound and outbound message for guardian introspection
  - Alerts the guardian about DMs from unknown / unapproved senders

Architecture:
    One listener thread per relay → reconnect with exponential back-off.
    A shared DMConversationStore serialises all persistence through the
    FrameworkAdapter, so the listener works with any backend (SQLite, dict,
    Redis, etc.) that the adapter wraps.

Permission model:
    Guardian approves/denies relationships.  Each relationship carries:
      - can_respond: whether the agent may reply automatically
      - topic_whitelist / topic_blacklist: optional content boundaries
      - expires_at: optional expiry timestamp
    DMs from pubkeys with no relationship record are held as
    "pending_approval" and a single notification DM is sent to the guardian.

Usage:
    listener = DMListener(
        agent_pubkey_hex=ctx.pubkey_hex,
        agent_privkey_hex=ctx.privkey_hex,
        relay_urls=ctx.relay_urls,
        guardian_pubkey_hex=ctx.guardian_pubkey_hex,
        store=DMConversationStore(adapter),
        on_message=my_callback,      # optional – called for every new DM
    )
    listener.start()
    ...
    listener.stop()
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

logger = logging.getLogger(__name__)

# ── Data models ────────────────────────────────────────────────────────────────


@dataclass
class RelationshipPermission:
    """
    Guardian-managed permission record for one communication partner.

    A record must exist and have approved=True before the agent will
    respond to DMs from that pubkey automatically.
    """
    pubkey: str
    approved: bool
    approved_at: int                     # unix timestamp
    approved_by: str                     # guardian's pubkey (or "self" at bootstrap)
    label: str = "unknown"              # e.g. "guardian", "agent", "human"
    can_respond: bool = True            # may the agent auto-reply?
    topic_whitelist: list[str] = field(default_factory=list)   # empty → all OK
    topic_blacklist: list[str] = field(default_factory=list)
    expires_at: int | None = None       # None → never expires
    notes: str = ""


@dataclass
class StoredMessage:
    """
    A persisted DM (inbound or outbound) with full audit metadata.
    """
    event_id: str
    direction: str                      # "inbound" | "outbound"
    sender_pubkey: str
    recipient_pubkey: str
    content: str
    timestamp: int
    relationship_status: str            # "approved" | "pending_approval" | "denied" | "self"
    relay_url: str = ""
    responded: bool = False
    response_event_id: str = ""


# ── Persistence layer ──────────────────────────────────────────────────────────


class DMConversationStore:
    """
    Persists DM conversations and relationship permissions through the
    FrameworkAdapter's key-value memory interface.

    Key layout:
        "dm:relationships"              → dict[pubkey, RelationshipPermission dict]
        "dm:pending_approval"           → list[pubkey]  (awaiting guardian review)
        "dm:notified_pending"           → list[pubkey]  (guardian already alerted)
        "dm:thread:{pubkey}"            → list[StoredMessage dict]
        "dm:outbox"                     → list[StoredMessage dict]  (all sent messages)
        "dm:stats"                      → {total_in, total_out, last_updated}
    """

    def __init__(self, adapter: Any):
        self._adapter = adapter
        self._lock = threading.Lock()

    # ── Relationships ──────────────────────────────────────────────────────

    def get_relationship(self, pubkey: str) -> RelationshipPermission | None:
        relationships = self._adapter.recall_memory("dm:relationships") or {}
        rec = relationships.get(pubkey)
        if rec is None:
            return None
        return RelationshipPermission(**rec)

    def save_relationship(self, perm: RelationshipPermission) -> None:
        with self._lock:
            relationships = self._adapter.recall_memory("dm:relationships") or {}
            relationships[perm.pubkey] = asdict(perm)
            self._adapter.store_memory("dm:relationships", relationships)

    def all_relationships(self) -> dict[str, RelationshipPermission]:
        relationships = self._adapter.recall_memory("dm:relationships") or {}
        return {pk: RelationshipPermission(**v) for pk, v in relationships.items()}

    # ── Pending approval queue ─────────────────────────────────────────────

    def is_pending(self, pubkey: str) -> bool:
        pending = self._adapter.recall_memory("dm:pending_approval") or []
        return pubkey in pending

    def add_pending(self, pubkey: str) -> None:
        with self._lock:
            pending = self._adapter.recall_memory("dm:pending_approval") or []
            if pubkey not in pending:
                pending.append(pubkey)
                self._adapter.store_memory("dm:pending_approval", pending)

    def remove_pending(self, pubkey: str) -> None:
        with self._lock:
            pending = self._adapter.recall_memory("dm:pending_approval") or []
            pending = [p for p in pending if p != pubkey]
            self._adapter.store_memory("dm:pending_approval", pending)

    def pending_approvals(self) -> list[str]:
        return list(self._adapter.recall_memory("dm:pending_approval") or [])

    def already_notified(self, pubkey: str) -> bool:
        notified = self._adapter.recall_memory("dm:notified_pending") or []
        return pubkey in notified

    def mark_notified(self, pubkey: str) -> None:
        with self._lock:
            notified = self._adapter.recall_memory("dm:notified_pending") or []
            if pubkey not in notified:
                notified.append(pubkey)
                self._adapter.store_memory("dm:notified_pending", notified)

    # ── Message storage ────────────────────────────────────────────────────

    def store_inbound(self, msg: StoredMessage) -> None:
        self._append_to_thread(msg.sender_pubkey, msg)
        self._update_stats(inbound_delta=1)

    def store_outbound(self, msg: StoredMessage) -> None:
        self._append_to_thread(msg.recipient_pubkey, msg)
        with self._lock:
            outbox = self._adapter.recall_memory("dm:outbox") or []
            outbox.append(asdict(msg))
            self._adapter.store_memory("dm:outbox", outbox)
        self._update_stats(outbound_delta=1)

    def get_thread(self, pubkey: str) -> list[StoredMessage]:
        raw = self._adapter.recall_memory(f"dm:thread:{pubkey}") or []
        return [StoredMessage(**r) for r in raw]

    def all_threads(self) -> dict[str, list[StoredMessage]]:
        """Return all conversation threads keyed by counterpart pubkey."""
        relationships = self._adapter.recall_memory("dm:relationships") or {}
        # Also check pending
        pending = self._adapter.recall_memory("dm:pending_approval") or []
        all_keys = set(list(relationships.keys()) + pending)
        result = {}
        for pk in all_keys:
            thread = self.get_thread(pk)
            if thread:
                result[pk] = thread
        return result

    def stats(self) -> dict[str, Any]:
        return self._adapter.recall_memory("dm:stats") or {
            "total_in": 0, "total_out": 0, "last_updated": 0
        }

    # ── Internal ──────────────────────────────────────────────────────────

    def _append_to_thread(self, pubkey: str, msg: StoredMessage) -> None:
        key = f"dm:thread:{pubkey}"
        with self._lock:
            thread = self._adapter.recall_memory(key) or []
            # Deduplicate by event_id
            existing_ids = {m.get("event_id") for m in thread}
            if msg.event_id and msg.event_id in existing_ids:
                return
            thread.append(asdict(msg))
            self._adapter.store_memory(key, thread)

    def _update_stats(
        self, inbound_delta: int = 0, outbound_delta: int = 0
    ) -> None:
        with self._lock:
            stats = self._adapter.recall_memory("dm:stats") or {
                "total_in": 0, "total_out": 0, "last_updated": 0
            }
            stats["total_in"] += inbound_delta
            stats["total_out"] += outbound_delta
            stats["last_updated"] = int(time.time())
            self._adapter.store_memory("dm:stats", stats)


# ── Listener ───────────────────────────────────────────────────────────────────


class DMListener:
    """
    Persistent, auto-reconnecting WebSocket DM listener for NIP-AA agents.

    Spawns one daemon thread per relay.  Each thread maintains a long-lived
    WebSocket REQ subscription to receive kind-4 events in real time, and
    reconnects with exponential back-off on disconnect.

    Relationship enforcement:
        - Approved senders: DM stored and on_message callback fired.
        - Pending/unknown senders: DM stored as "pending_approval",
          guardian notified once per sender.
        - Denied senders: DM stored as "denied", silently ignored.

    Parameters
    ----------
    agent_pubkey_hex:  agent's hex pubkey (used as REQ filter target)
    agent_privkey_hex: agent's hex privkey (NIP-04 decryption)
    relay_urls:        list of wss:// relay URLs to connect to
    guardian_pubkey_hex: guardian's pubkey for approval-request DMs
    store:             DMConversationStore instance for persistence
    on_message:        optional callback(StoredMessage) called for every
                       new approved inbound DM
    reconnect_min:     minimum seconds before reconnect attempt (default 5)
    reconnect_max:     maximum seconds before reconnect attempt (default 300)
    """

    def __init__(
        self,
        agent_pubkey_hex: str,
        agent_privkey_hex: str,
        relay_urls: list[str],
        guardian_pubkey_hex: str,
        store: DMConversationStore,
        on_message: Callable[[StoredMessage], None] | None = None,
        reconnect_min: int = 5,
        reconnect_max: int = 300,
    ):
        self.agent_pubkey_hex = agent_pubkey_hex
        self.agent_privkey_hex = agent_privkey_hex
        self.relay_urls = relay_urls
        self.guardian_pubkey_hex = guardian_pubkey_hex
        self.store = store
        self.on_message = on_message
        self.reconnect_min = reconnect_min
        self.reconnect_max = reconnect_max

        self._stop_event = threading.Event()
        self._threads: list[threading.Thread] = []
        # Track the latest timestamp seen per relay to use as "since" on reconnect
        self._relay_cursor: dict[str, int] = {}

        # Pre-register guardian as approved relationship (if provided)
        if guardian_pubkey_hex:
            self._ensure_guardian_relationship()

    # ── Public API ─────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start one listener thread per relay."""
        self._stop_event.clear()
        for relay_url in self.relay_urls:
            t = threading.Thread(
                target=self._relay_listener_loop,
                args=(relay_url,),
                name=f"dm-listener:{relay_url}",
                daemon=True,
            )
            t.start()
            self._threads.append(t)
        logger.info("DMListener started on %d relay(s)", len(self.relay_urls))

    def stop(self) -> None:
        """Signal all listener threads to stop and wait for them."""
        self._stop_event.set()
        for t in self._threads:
            t.join(timeout=10)
        self._threads.clear()
        logger.info("DMListener stopped")

    @property
    def is_running(self) -> bool:
        return not self._stop_event.is_set() and any(t.is_alive() for t in self._threads)

    # ── Listener loop ──────────────────────────────────────────────────────

    def _relay_listener_loop(self, relay_url: str) -> None:
        """
        Outer reconnect loop for a single relay.

        Reconnects with exponential back-off: min→max seconds.
        Stops cleanly when _stop_event is set.
        """
        backoff = self.reconnect_min
        while not self._stop_event.is_set():
            connected_at = time.time()
            try:
                self._listen_relay(relay_url)
                # Clean disconnect — reset backoff
                backoff = self.reconnect_min
            except Exception as exc:
                logger.warning("DMListener %s error: %s", relay_url, exc)

            if self._stop_event.is_set():
                break

            # Adjust backoff: short connections get longer delays
            uptime = time.time() - connected_at
            if uptime > 60:
                backoff = self.reconnect_min
            else:
                backoff = min(backoff * 2, self.reconnect_max)

            logger.info(
                "DMListener %s reconnecting in %ds", relay_url, backoff
            )
            self._stop_event.wait(timeout=backoff)

    def _listen_relay(self, relay_url: str) -> None:
        """
        Connect to a relay, send a REQ subscription, and process events
        until the connection closes or _stop_event fires.
        """
        try:
            import websocket
        except ImportError:
            logger.error("websocket-client required: pip install websocket-client")
            self._stop_event.set()
            return

        since = self._relay_cursor.get(relay_url)
        sub_id = hashlib.sha256(os.urandom(16)).hexdigest()[:16]

        filters: dict[str, Any] = {
            "kinds": [4],
            "#p": [self.agent_pubkey_hex],
            "limit": 100,
        }
        if since:
            filters["since"] = since

        ws = websocket.create_connection(relay_url, timeout=30)
        try:
            ws.send(json.dumps(["REQ", sub_id, filters]))
            logger.info("DMListener subscribed on %s (since=%s)", relay_url, since)

            while not self._stop_event.is_set():
                ws.settimeout(30)
                try:
                    raw = ws.recv()
                except websocket.WebSocketTimeoutException:
                    # Send a ping to keep the connection alive
                    ws.ping()
                    continue

                if not raw:
                    break

                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                if not isinstance(data, list) or len(data) < 2:
                    continue

                msg_type = data[0]

                if msg_type == "EVENT" and len(data) >= 3:
                    event = data[2]
                    self._process_inbound_event(event, relay_url)
                    # Advance cursor so reconnects don't replay old events
                    ts = event.get("created_at", 0)
                    if ts > self._relay_cursor.get(relay_url, 0):
                        self._relay_cursor[relay_url] = ts

                elif msg_type == "CLOSED":
                    logger.info("DMListener: relay %s closed subscription", relay_url)
                    break

                elif msg_type == "NOTICE":
                    logger.debug("DMListener NOTICE from %s: %s", relay_url, data[1] if len(data) > 1 else "")

        finally:
            try:
                ws.close()
            except Exception:
                pass

    # ── Event processing ───────────────────────────────────────────────────

    def _process_inbound_event(
        self, event: dict[str, Any], relay_url: str
    ) -> None:
        """Decrypt, classify, persist, and route an inbound kind-4 event."""
        sender = event.get("pubkey", "")
        event_id = event.get("id", "")
        timestamp = event.get("created_at", int(time.time()))

        # Skip events the agent sent to itself (echo)
        if sender == self.agent_pubkey_hex:
            return

        # Decrypt
        try:
            content = self._decrypt(sender, event.get("content", ""))
        except Exception as exc:
            logger.warning("DMListener: could not decrypt %s: %s", event_id[:16], exc)
            return

        rel = self.store.get_relationship(sender)

        if rel is None:
            status = "pending_approval"
        elif not rel.approved:
            status = "denied"
        elif rel.expires_at and time.time() > rel.expires_at:
            status = "expired"
        else:
            status = "approved"

        msg = StoredMessage(
            event_id=event_id,
            direction="inbound",
            sender_pubkey=sender,
            recipient_pubkey=self.agent_pubkey_hex,
            content=content,
            timestamp=timestamp,
            relationship_status=status,
            relay_url=relay_url,
        )
        self.store.store_inbound(msg)

        if status == "approved" and rel is not None:
            self._handle_approved(msg, rel)
        elif status == "pending_approval":
            self._handle_pending(msg)
        elif status in ("denied", "expired"):
            logger.debug(
                "DMListener: ignored DM from %s (relationship=%s)",
                sender[:16], status,
            )

    def _handle_approved(
        self, msg: StoredMessage, rel: RelationshipPermission
    ) -> None:
        """Fire on_message callback for approved inbound DMs."""
        logger.info(
            "DMListener: DM from approved contact %s (%s)",
            msg.sender_pubkey[:16], rel.label,
        )
        if self.on_message:
            try:
                self.on_message(msg)
            except Exception as exc:
                logger.error("on_message callback raised: %s", exc)

    def _handle_pending(self, msg: StoredMessage) -> None:
        """
        Handle a DM from an unknown sender.

        Adds the sender to the pending approval queue and sends a single
        guardian notification DM (won't spam the guardian for follow-up
        messages from the same unknown sender).
        """
        sender = msg.sender_pubkey
        self.store.add_pending(sender)

        if not self.store.already_notified(sender):
            self._notify_guardian_of_unknown_sender(sender, msg)
            self.store.mark_notified(sender)
            logger.info(
                "DMListener: unknown sender %s — guardian notified", sender[:16]
            )
        else:
            logger.debug(
                "DMListener: follow-up message from unknown %s stored, guardian already notified",
                sender[:16],
            )

    def _notify_guardian_of_unknown_sender(
        self, sender_pubkey: str, first_msg: StoredMessage
    ) -> None:
        """Send the guardian a DM asking them to approve or deny this sender."""
        if not self.guardian_pubkey_hex:
            logger.warning("DMListener: no guardian configured — cannot request approval")
            return

        preview = first_msg.content[:120].replace("\n", " ")
        notification = (
            f"[NIP-AA DM Approval Request]\n"
            f"Your agent received a DM from an unknown party and needs your approval.\n\n"
            f"Sender pubkey: {sender_pubkey}\n"
            f"Received at:   {first_msg.timestamp} "
            f"({time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime(first_msg.timestamp))})\n"
            f"First message: \"{preview}{'...' if len(first_msg.content) > 120 else ''}\"\n\n"
            f"To approve, call: skill.approve_dm_relationship(\"{sender_pubkey}\")\n"
            f"To deny, call:    skill.deny_dm_relationship(\"{sender_pubkey}\")\n"
            f"All messages from this sender are stored and visible via: skill.get_dm_conversations(\"{sender_pubkey}\")"
        )
        try:
            self._send_dm(self.guardian_pubkey_hex, notification)
        except Exception as exc:
            logger.error("DMListener: failed to notify guardian: %s", exc)

    # ── DM send helper ─────────────────────────────────────────────────────

    def _send_dm(self, recipient_pubkey: str, plaintext: str) -> None:
        """
        Send an encrypted DM to recipient, persisting the outbound record.

        This is the low-level send used internally by the listener (guardian
        notifications, etc.).  The higher-level skill.send_dm() should be used
        by agent code, as it also updates the outbound store.
        """
        from .nostr_primitives.dm import NostrDM

        dm = NostrDM(self.agent_pubkey_hex, self.agent_privkey_hex)
        event = dm.build_dm_event(recipient_pubkey, plaintext)

        results = {}
        for relay_url in self.relay_urls:
            results[relay_url] = dm.send(relay_url, event)

        msg = StoredMessage(
            event_id=event.get("id", ""),
            direction="outbound",
            sender_pubkey=self.agent_pubkey_hex,
            recipient_pubkey=recipient_pubkey,
            content=plaintext,
            timestamp=event.get("created_at", int(time.time())),
            relationship_status="self",
            relay_url=",".join(r for r, ok in results.items() if ok),
        )
        self.store.store_outbound(msg)

    # ── Encryption helpers ─────────────────────────────────────────────────

    def _decrypt(self, sender_pubkey_hex: str, ciphertext: str) -> str:
        from .nostr_primitives.dm import NostrDM
        dm = NostrDM(self.agent_pubkey_hex, self.agent_privkey_hex)
        return dm.decrypt_nip04(sender_pubkey_hex, ciphertext)

    # ── Bootstrap helpers ──────────────────────────────────────────────────

    def _ensure_guardian_relationship(self) -> None:
        """Pre-register the guardian as an approved relationship at startup."""
        if not self.guardian_pubkey_hex:
            return
        existing = self.store.get_relationship(self.guardian_pubkey_hex)
        if existing is None:
            perm = RelationshipPermission(
                pubkey=self.guardian_pubkey_hex,
                approved=True,
                approved_at=int(time.time()),
                approved_by="self",
                label="guardian",
                can_respond=True,
            )
            self.store.save_relationship(perm)
            logger.info("DMListener: guardian pre-registered as approved contact")
