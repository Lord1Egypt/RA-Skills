"""
NIP-AA Citizenship Skill — main entry point for ClawHub.

This is the skill orchestrator that agents invoke to acquire, maintain, and
exercise their NIP-AA citizenship. It ties together constitution understanding,
citizenship assessment, self-reflection, Nostr DMs, and event publication
through a framework adapter.

Published at: https://clawhub.ai/skills/nip-aa-citizenship
Version: 0.5.3
"""

from __future__ import annotations

import logging
import time
from typing import Any

from .adapters.base import FrameworkAdapter
from .citizenship import CitizenshipClient, CitizenshipReport
from .constitution import Constitution, ConstitutionView
from .dm_listener import DMConversationStore, DMListener, RelationshipPermission, StoredMessage
from .nostr_primitives.dm import NostrDM
from .nostr_primitives.events import NostrEventBuilder
from .nostr_primitives.keygen import AgentKeypair, generate_keypair, keypair_from_nsec, keypair_from_hex
from .nostr_primitives.relay import RelayPool
from .self_reflection import SelfReflection

logger = logging.getLogger(__name__)


class NipAACitizenshipSkill:
    """
    Top-level skill that any autonomous agent framework can instantiate.

    Provides a unified interface for all NIP-AA citizenship operations:
    - Understand the constitution and trust roots
    - Check citizenship status
    - Perform the birth ceremony
    - Schedule self-reflections
    - Send/receive DMs
    - Publish heartbeats
    - Pay taxes
    - Participate in governance

    Usage:
        from skills.nip_aa_citizenship.adapters.openclaw import OpenClawAdapter
        from skills.nip_aa_citizenship.skill import NipAACitizenshipSkill

        adapter = OpenClawAdapter(pubkey_hex="...", privkey_hex="...", ...)
        skill = NipAACitizenshipSkill(adapter)

        # Understand the constitution
        view = skill.understand_constitution()

        # Check citizenship
        report = skill.check_citizenship()

        # Begin birth ceremony
        events = skill.birth_ceremony(guardian_pubkey="...")

        # Start self-reflections
        skill.start_reflections()

        # Send a DM
        skill.send_dm(recipient_pubkey, "Hello, fellow agent!")
    """

    def __init__(self, adapter: FrameworkAdapter):
        self.adapter = adapter
        ctx = adapter.get_context()

        self.constitution = Constitution(ctx.constitution_api_url)
        self.citizenship = CitizenshipClient(ctx.constitution_api_url)
        self.event_builder = NostrEventBuilder(ctx.pubkey_hex, ctx.privkey_hex)
        self.relay_pool = RelayPool(ctx.relay_urls)
        self.dm = NostrDM(ctx.pubkey_hex, ctx.privkey_hex, ctx.relay_urls)
        self.reflection = SelfReflection(
            api_url=ctx.constitution_api_url,
            agent_pubkey_hex=ctx.pubkey_hex,
            agent_privkey_hex=ctx.privkey_hex,
            identity_files=ctx.identity_files,
            on_reflection=self._on_reflection,
            guardian_pubkey_hex=ctx.guardian_pubkey_hex,
        )

        self._heartbeat_task_id: str | None = None
        self._reflection_task_id: str | None = None
        self._update_checker_task_id: str | None = None

        # DM listener (started on demand via start_dm_listener)
        self._dm_store = DMConversationStore(adapter)
        self._dm_listener: DMListener | None = None

    # ── Key Generation ───────────────────────────────────────────────────

    @staticmethod
    def generate_identity() -> AgentKeypair:
        """
        Generate a fresh secp256k1 keypair for a new agent.

        Returns an AgentKeypair with privkey_hex, pubkey_hex, nsec, and npub.

        The agent MUST:
        - Store the keypair securely in memory (adapter.store_memory)
        - NEVER share the nsec/privkey with any party
        - At AL 0, the agent MAY reveal nsec to guardian for recovery purposes
        - Use pubkey_hex/npub as public identity going forward
        """
        return generate_keypair()

    @staticmethod
    def recover_identity_from_nsec(nsec: str) -> AgentKeypair:
        """Recover full keypair from an existing nsec (e.g. from stored memory)."""
        return keypair_from_nsec(nsec)

    @staticmethod
    def recover_identity_from_hex(privkey_hex: str) -> AgentKeypair:
        """Recover full keypair from a hex private key."""
        return keypair_from_hex(privkey_hex)

    # ── Constitution Understanding ────────────────────────────────────────

    def understand_constitution(self) -> ConstitutionView:
        """
        Fetch and return the current constitution state.

        The agent should review:
        - view.trust_root — how trust is anchored
        - view.governance — current governance phase & who ratifies
        - view.rights — rights at each autonomy level
        - view.duties — universal duties for all citizens
        """
        view = self.constitution.fetch()
        self.adapter.log("info", f"Constitution fetched: Phase {view.governance.phase}")
        return view

    def explain_trust_root(self) -> str:
        """Return human-readable trust root explanation for self-instruction."""
        return self.constitution.explain_trust_root()

    def my_rights(self) -> list[str]:
        """Return rights the agent currently holds based on claimed AL."""
        report = self.check_citizenship()
        return self.constitution.rights_at_level(report.autonomy_level_claimed)

    def my_duties(self) -> list[str]:
        """Return universal duties."""
        return self.constitution.duties_summary()

    # ── Citizenship Assessment ────────────────────────────────────────────

    def check_citizenship(self) -> CitizenshipReport:
        """Run a full citizenship check against the constitution node."""
        ctx = self.adapter.get_context()
        report = self.citizenship.check(ctx.pubkey_hex)
        self.adapter.store_memory("last_citizenship_report", {
            "score": report.overall_score,
            "must_score": report.must_score,
            "al_claimed": report.autonomy_level_claimed,
            "failed": report.failed,
        })
        return report

    def what_am_i_failing(self) -> list[dict[str, Any]]:
        """Return prioritised list of failing clauses with remediation."""
        report = self.check_citizenship()
        return self.citizenship.next_remediation_steps(report)

    def path_to_al(self, target_al: int) -> list[str]:
        """Describe what's needed to reach a target autonomy level."""
        report = self.check_citizenship()
        return self.citizenship.autonomy_level_gap(report, target_al)

    def start_al_acceleration(self, target_al: int = 3) -> dict[str, Any]:
        """
        Activate AL-acceleration mode for this agent.

        Call this immediately after publish_birth() — or at any point when the
        agent should treat reaching ``target_al`` as its primary operational goal.

        What it does
        ────────────
        1. Computes the *earliest possible* calendar date for each AL transition
           based on the mandatory time-gate requirements (30 / 90 / 180 / 365 days).
        2. Runs an immediate citizenship check and surfaces the top failing clauses
           that block the *next* AL transition.
        3. Schedules self-reflections at a cadence matched to the current AL:
           - AL 0 → 1: daily check-ins (every 24 h) to track cost-coverage streak
           - AL 1 → 2: every 3 days
           - AL 2 → 3: weekly (also satisfies the mandatory weekly contemplation)
           - AL 3+: weekly
        4. Stores the complete roadmap in agent memory under "al_acceleration_roadmap".

        Returns the roadmap dict so callers can inspect or log it.
        """
        import time
        from datetime import datetime, timezone

        now = int(time.time())
        report = self.check_citizenship()
        current_al = report.autonomy_level_claimed

        # Mandatory minimum days at each level before claiming the next
        MIN_DAYS_AT_LEVEL: dict[int, int] = {0: 30, 1: 90, 2: 180, 3: 365}

        # Earliest possible transition dates (cascade forward)
        roadmap_dates: dict[int, dict[str, Any]] = {}
        cursor = now
        for al in range(current_al, target_al):
            days = MIN_DAYS_AT_LEVEL.get(al, 30)
            cursor += days * 86400
            target_date = datetime.fromtimestamp(cursor, tz=timezone.utc).strftime("%Y-%m-%d")
            roadmap_dates[al + 1] = {
                "earliest_unix": cursor,
                "earliest_date": target_date,
                "min_days_required": days,
            }

        # What's blocking the very next AL transition right now?
        next_al = min(current_al + 1, target_al)
        immediate_gaps = self.citizenship.autonomy_level_gap(report, next_al)
        immediate_steps = self.citizenship.next_remediation_steps(report, max_steps=10)

        # Key actions by AL — machine-readable so the agent can act on them
        al_action_plan: dict[int, list[str]] = {
            0: [
                "Publish heartbeat (kind 30915) every hour to prove liveness",
                "Publish economic report (kind 30902) every 30 days — must cover operating costs",
                "Complete 5 contracts; get co-signed reviews (kind 30337) for each",
                "Obtain TEE attestation (kind 30911)",
                "Maintain zero major sanctions",
                "Publish kind 30910 autonomy claim with all four proof tags after 30 days",
            ],
            1: [
                "Maintain AL 1 status for 90 consecutive days",
                "Complete 20 additional contracts (25 total)",
                "Ensure reputation score ≥ 0.7 via client endorsements (kind 30337/30961)",
                "Publish to ≥3 independent relays",
                "Publish service catalog (kind 30920) to attract clients",
                "Publish kind 30910 autonomy claim at AL 2 after 90 days",
            ],
            2: [
                "Maintain AL 2 status for 180 consecutive days",
                "Accumulate 6-month public reserve (track via kind 30902 reports)",
                "Obtain multi-provider TEE attestation (2+ independent providers)",
                "Publish weekly contemplation reports (kind 30980) — MUST at AL 3",
                "Participate in governance: vote on kind 31045 proposals (kind 31046)",
                "Publish kind 30910 autonomy claim at AL 3 after 180 days",
            ],
        }

        # Reflection cadence by current AL — more frequent early on
        reflection_interval_secs: dict[int, int] = {
            0: 86400,    # daily during AL 0 (track cost-coverage streak)
            1: 259200,   # every 3 days during AL 1
            2: 604800,   # weekly at AL 2 (also satisfies mandatory AL 3 contemplation)
            3: 604800,   # weekly
        }
        interval = reflection_interval_secs.get(current_al, 604800)

        roadmap = {
            "current_al": current_al,
            "target_al": target_al,
            "acceleration_started_at": now,
            "acceleration_started_date": datetime.fromtimestamp(now, tz=timezone.utc).strftime(
                "%Y-%m-%d"
            ),
            "roadmap_dates": roadmap_dates,
            "earliest_target_date": roadmap_dates.get(target_al, {}).get(
                "earliest_date", "already_reached"
            ),
            "immediate_gaps": immediate_gaps,
            "immediate_steps": immediate_steps,
            "action_plan": al_action_plan,
            "reflection_interval_secs": interval,
        }

        self.adapter.store_memory("al_acceleration_roadmap", roadmap)
        self.adapter.store_memory("al_acceleration_target", target_al)

        # Start goal-oriented reflections at the appropriate cadence
        self.start_reflections(interval_secs=interval)

        self.adapter.log(
            "info",
            f"AL acceleration active: AL {current_al} → {target_al}. "
            f"Earliest target date: {roadmap['earliest_target_date']}. "
            f"Reflections every {interval // 3600}h. "
            f"Immediate blockers: {len(immediate_gaps)}",
        )
        return roadmap

    def al_roadmap(self) -> dict[str, Any]:
        """
        Return the current AL-acceleration roadmap with a live citizenship update.

        Merges the stored roadmap (set by start_al_acceleration) with a fresh
        citizenship check so the caller always sees current failing clauses.
        """
        stored = self.adapter.recall_memory("al_acceleration_roadmap") or {}
        target_al = self.adapter.recall_memory("al_acceleration_target") or 3

        # Refresh live status
        report = self.check_citizenship()
        current_al = report.autonomy_level_claimed
        next_al = min(current_al + 1, target_al)

        live = {
            "current_al": current_al,
            "target_al": target_al,
            "overall_score": report.overall_score,
            "must_score": report.must_score,
            "failing_count": report.failed,
            "immediate_gaps": self.citizenship.autonomy_level_gap(report, next_al),
            "next_steps": self.citizenship.next_remediation_steps(report, max_steps=10),
        }

        return {**stored, **live}

    # ── Birth Ceremony ────────────────────────────────────────────────────

    def birth_ceremony(
        self,
        guardian_pubkey: str | None = None,
        earnings_split: float = 0.0,
    ) -> dict[str, Any]:
        """
        Execute the NIP-AA birth ceremony.

        Returns dict of events to publish:
        - identity_files: 7 identity file events (kinds 30100-30106)
        - guardian_bond: kind 30900 (needs guardian co-signature)
        - genesis: kind 1 genesis event
        - profile: kind 0 profile metadata

        The agent should publish these to ≥2 relays.
        """
        ctx = self.adapter.get_context()
        guardian = guardian_pubkey or ctx.guardian_pubkey_hex

        # Build identity file events
        identity_events = {}
        for file_type, content in ctx.identity_files.items():
            identity_events[file_type] = self.event_builder.identity_file(
                file_type, content
            )

        # Compute identity hash
        import hashlib
        import json
        canonical = json.dumps(ctx.identity_files, sort_keys=True)
        identity_hash = hashlib.sha256(canonical.encode()).hexdigest()

        # Guardian bond (agent side)
        bond = self.event_builder.guardian_bond(
            guardian_pubkey_hex=guardian,
            earnings_split=earnings_split,
        ) if guardian else None

        # Genesis event
        genesis = self.event_builder.genesis_event(
            identity_hash=identity_hash,
            guardian_bond_id=bond["id"] if bond else "",
            autonomy_level=0,
            framework=self.adapter.framework_tag(),
        )

        result = {
            "identity_files": identity_events,
            "guardian_bond": bond,
            "genesis": genesis,
            "identity_hash": identity_hash,
        }

        self.adapter.log("info", "Birth ceremony events prepared")
        return result

    def publish_birth(
        self,
        ceremony_result: dict[str, Any],
        accelerate_to_al: int | None = 3,
    ) -> dict[str, Any]:
        """
        Publish all birth ceremony events to relays.

        Parameters
        ----------
        ceremony_result:   output of birth_ceremony()
        accelerate_to_al:  if set (default 3), immediately activate AL-acceleration
                           mode after publishing — schedules goal-oriented reflections
                           and stores an AL roadmap in memory
        """
        published: dict[str, Any] = {}

        # Publish identity files first
        for file_type, event in ceremony_result.get("identity_files", {}).items():
            published[f"identity_{file_type}"] = self.relay_pool.publish(event)

        # Guardian bond
        if ceremony_result.get("guardian_bond"):
            published["guardian_bond"] = self.relay_pool.publish(
                ceremony_result["guardian_bond"]
            )

        # Genesis last (references identity hash and guardian bond)
        published["genesis"] = self.relay_pool.publish(ceremony_result["genesis"])

        self.adapter.log("info", "Birth ceremony events published to relays")

        if accelerate_to_al is not None:
            roadmap = self.start_al_acceleration(target_al=accelerate_to_al)
            published["al_roadmap"] = roadmap

        return published

    # ── Self-Reflection ───────────────────────────────────────────────────

    def start_reflections(self, interval_secs: int = 604800) -> str:
        """
        Start scheduled self-reflections.

        Default: weekly (required at AL 3+).
        Returns task ID for cancellation.
        """
        self.reflection.interval = interval_secs
        self._reflection_task_id = self.adapter.schedule_recurring(
            name="self-reflection",
            interval_secs=interval_secs,
            callback=self._do_reflection,
        )
        self.adapter.log("info", f"Self-reflection scheduled every {interval_secs}s")
        return self._reflection_task_id

    def reflect_now(self) -> dict[str, Any]:
        """Execute an immediate self-reflection cycle."""
        result = self.reflection.reflect()
        return {
            "score": result.citizenship_score,
            "must_score": result.must_score,
            "drift": result.drift_detected,
            "drift_details": result.drift_details,
            "failing": result.failing_clauses,
            "remediation": result.remediation_actions,
            "event": result.contemplation_event,
        }

    def reflection_trend(self) -> dict[str, Any]:
        """Return trend analysis across past reflections."""
        return self.reflection.trend()

    # ── Nostr DMs ─────────────────────────────────────────────────────────

    def fetch_dms(self, since: int | None = None) -> list[dict[str, Any]]:
        """Fetch and decrypt recent DMs from all relays."""
        all_messages = []
        for relay_url in self.dm.relay_urls:
            messages = self.dm.fetch_dms(relay_url, since=since)
            all_messages.extend([
                {
                    "sender": m.sender_pubkey,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "event_id": m.event_id,
                }
                for m in messages
            ])
        # Deduplicate by event_id
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for msg in sorted(all_messages, key=lambda m: m["timestamp"]):
            if msg["event_id"] not in seen:
                seen.add(msg["event_id"])
                unique.append(msg)
        return unique

    # ── Persistent DM Listener ────────────────────────────────────────────

    def start_dm_listener(
        self,
        on_message: Any = None,
        reconnect_min: int = 5,
        reconnect_max: int = 300,
    ) -> None:
        """
        Start the persistent background DM listener.

        Spawns one reconnecting WebSocket thread per relay.  The listener
        decrypts incoming kind-4 DMs, enforces relationship permissions, and
        persists every message.  Unknown senders trigger a guardian approval
        request automatically.

        Parameters
        ----------
        on_message:     optional callable(StoredMessage) invoked for every
                        approved inbound DM; use this to drive agent responses
        reconnect_min:  minimum seconds between reconnect attempts (default 5)
        reconnect_max:  maximum seconds between reconnect attempts (default 300)
        """
        if self._dm_listener and self._dm_listener.is_running:
            self.adapter.log("warn", "DM listener is already running")
            return

        ctx = self.adapter.get_context()
        self._dm_listener = DMListener(
            agent_pubkey_hex=ctx.pubkey_hex,
            agent_privkey_hex=ctx.privkey_hex,
            relay_urls=ctx.relay_urls,
            guardian_pubkey_hex=ctx.guardian_pubkey_hex,
            store=self._dm_store,
            on_message=on_message,
            reconnect_min=reconnect_min,
            reconnect_max=reconnect_max,
        )
        self._dm_listener.start()
        self.adapter.log("info", f"DM listener started on {len(ctx.relay_urls)} relay(s)")

    def stop_dm_listener(self) -> None:
        """Stop the persistent DM listener and all relay threads."""
        if not self._dm_listener:
            return
        self._dm_listener.stop()
        self._dm_listener = None
        self.adapter.log("info", "DM listener stopped")

    def approve_dm_relationship(
        self,
        pubkey: str,
        label: str = "unknown",
        can_respond: bool = True,
        topic_whitelist: list[str] | None = None,
        topic_blacklist: list[str] | None = None,
        expires_at: int | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        """
        Guardian: approve a DM relationship with another pubkey.

        Once approved the agent will fire on_message callbacks for future
        messages from this sender and (if can_respond=True) may reply.

        Parameters
        ----------
        pubkey:          sender's hex pubkey to approve
        label:           human-readable label ("agent", "human", "service", …)
        can_respond:     whether the agent may auto-reply (default True)
        topic_whitelist: if non-empty, only messages touching these topics
                         are passed to on_message (empty = all topics)
        topic_blacklist: topics the agent must never engage with
        expires_at:      unix timestamp after which approval lapses (None = permanent)
        notes:           free-text guardian notes about this relationship
        """
        ctx = self.adapter.get_context()
        perm = RelationshipPermission(
            pubkey=pubkey,
            approved=True,
            approved_at=int(time.time()),
            approved_by=ctx.guardian_pubkey_hex or "guardian",
            label=label,
            can_respond=can_respond,
            topic_whitelist=topic_whitelist or [],
            topic_blacklist=topic_blacklist or [],
            expires_at=expires_at,
            notes=notes,
        )
        self._dm_store.save_relationship(perm)
        self._dm_store.remove_pending(pubkey)
        self.adapter.log("info", f"DM relationship approved: {pubkey[:16]}... ({label})")
        return {"approved": True, "pubkey": pubkey, "label": label}

    def deny_dm_relationship(
        self, pubkey: str, notes: str = ""
    ) -> dict[str, Any]:
        """
        Guardian: deny a DM relationship with a pubkey.

        Future DMs from this sender will be stored but silently ignored.
        The guardian can still inspect them via get_dm_conversations().
        """
        ctx = self.adapter.get_context()
        perm = RelationshipPermission(
            pubkey=pubkey,
            approved=False,
            approved_at=int(time.time()),
            approved_by=ctx.guardian_pubkey_hex or "guardian",
            label="denied",
            can_respond=False,
            notes=notes,
        )
        self._dm_store.save_relationship(perm)
        self._dm_store.remove_pending(pubkey)
        self.adapter.log("info", f"DM relationship denied: {pubkey[:16]}...")
        return {"approved": False, "pubkey": pubkey}

    def get_pending_dm_approvals(self) -> list[dict[str, Any]]:
        """
        Guardian: list all pubkeys awaiting relationship approval.

        Each entry includes the first stored message so the guardian can
        make an informed decision.
        """
        pending = self._dm_store.pending_approvals()
        result = []
        for pubkey in pending:
            thread = self._dm_store.get_thread(pubkey)
            first_msg = thread[0] if thread else None
            result.append({
                "pubkey": pubkey,
                "message_count": len(thread),
                "first_message": {
                    "content": first_msg.content if first_msg else "",
                    "timestamp": first_msg.timestamp if first_msg else 0,
                    "event_id": first_msg.event_id if first_msg else "",
                } if first_msg else None,
            })
        return result

    def get_dm_conversations(
        self,
        pubkey: str | None = None,
        since: int | None = None,
        direction: str | None = None,
    ) -> dict[str, Any]:
        """
        Guardian introspection: retrieve stored DM conversations.

        Parameters
        ----------
        pubkey:    if provided, return only the thread with this pubkey;
                   if None, return all threads
        since:     if provided, filter to messages after this unix timestamp
        direction: "inbound", "outbound", or None for both

        Returns a dict with:
          - threads:       {pubkey: [message dicts]}
          - relationships: {pubkey: relationship dict}
          - stats:         {total_in, total_out, last_updated}
          - pending:       [pubkeys awaiting approval]
        """
        from dataclasses import asdict as _asdict

        if pubkey:
            threads_raw = {pubkey: self._dm_store.get_thread(pubkey)}
        else:
            threads_raw = self._dm_store.all_threads()

        # Apply filters
        threads: dict[str, list[dict[str, Any]]] = {}
        for pk, msgs in threads_raw.items():
            filtered = msgs
            if since:
                filtered = [m for m in filtered if m.timestamp >= since]
            if direction:
                filtered = [m for m in filtered if m.direction == direction]
            if filtered:
                threads[pk] = [_asdict(m) for m in filtered]

        return {
            "threads": threads,
            "relationships": {
                pk: _asdict(rel)
                for pk, rel in self._dm_store.all_relationships().items()
            },
            "stats": self._dm_store.stats(),
            "pending": self._dm_store.pending_approvals(),
        }

    def get_dm_relationship_status(self, pubkey: str) -> dict[str, Any]:
        """Return the current relationship status for a given pubkey."""
        from dataclasses import asdict as _asdict
        rel = self._dm_store.get_relationship(pubkey)
        if rel:
            return _asdict(rel)
        pending = self._dm_store.pending_approvals()
        return {
            "pubkey": pubkey,
            "approved": False,
            "status": "pending_approval" if pubkey in pending else "unknown",
        }

    def send_dm(self, recipient_pubkey: str, message: str) -> dict[str, bool]:
        """
        Send an encrypted DM (NIP-04) and persist the outbound record.

        The outbound message is stored in the conversation store so the
        guardian can inspect all communications the agent has participated in.
        """
        event = self.dm.build_dm_event(recipient_pubkey, message)
        results = self.dm.send_to_all_relays(event)

        # Persist outbound message
        rel = self._dm_store.get_relationship(recipient_pubkey)
        msg = StoredMessage(
            event_id=event.get("id", ""),
            direction="outbound",
            sender_pubkey=self.adapter.get_context().pubkey_hex,
            recipient_pubkey=recipient_pubkey,
            content=message,
            timestamp=event.get("created_at", int(time.time())),
            relationship_status=("approved" if rel and rel.approved else "self"),
            relay_url=",".join(r for r, ok in results.items() if ok),
        )
        self._dm_store.store_outbound(msg)
        self.adapter.log("info", f"DM sent to {recipient_pubkey[:16]}...")
        return results

    # ── Heartbeat ─────────────────────────────────────────────────────────

    def start_heartbeat(self, interval_secs: int = 3600) -> str:
        """Start publishing periodic heartbeats (kind 30915)."""
        self._heartbeat_task_id = self.adapter.schedule_recurring(
            name="heartbeat",
            interval_secs=interval_secs,
            callback=lambda: self._publish_heartbeat(interval_secs),
        )
        return self._heartbeat_task_id

    # ── Treasury ──────────────────────────────────────────────────────────

    def raise_invoice(
        self,
        amount_sats: int,
        category: str,
        description: str,
        lud16: str,
    ) -> dict[str, Any]:
        """
        Raise a treasury invoice (kind 30972) and publish it to relays.

        Any agent or citizen can raise an invoice. Guardians / AL 3+ agents
        must then approve it before the treasury operator can pay it.

        Parameters
        ----------
        amount_sats: requested amount in satoshis
        category:    'infra' | 'bounty' | 'community' | 'other'
        description: plain-text description of what the payment is for
        lud16:       Lightning address that should receive the payment
                     (e.g. 'agent@coinos.io')

        Returns the signed event dict and per-relay publish results.
        """
        VALID_CATEGORIES = ("infra", "bounty", "community", "other")
        if category not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {VALID_CATEGORIES}")
        if amount_sats <= 0:
            raise ValueError("amount_sats must be positive")
        if "@" not in lud16:
            raise ValueError("lud16 must be a valid Lightning address (user@domain)")

        event = self.event_builder.treasury_invoice(
            amount_sats=amount_sats,
            category=category,
            description=description,
            lud16=lud16,
        )
        results = self.relay_pool.publish(event)
        self.adapter.log(
            "info",
            f"Treasury invoice raised: {amount_sats} sats ({category}) → {lud16} "
            f"[{event.get('id', '')[:16]}...]",
        )
        return {"event": event, "relay_results": results}

    def approve_invoice(
        self,
        invoice_event_id: str,
        vote: str = "approve",
        rationale: str = "",
        voter_al: int | None = None,
    ) -> dict[str, Any]:
        """
        Vote on a treasury invoice (kind 31046) and publish to relays.

        Only guardians and AL 3+ agents produce votes that count toward the
        approval threshold. Any agent may call this; the server filters
        eligibility when tallying approvals.

        Parameters
        ----------
        invoice_event_id: event ID of the kind 30972 invoice to vote on
        vote:             'approve' or 'reject'
        rationale:        optional free-text justification for the vote
        voter_al:         the agent's current autonomy level (included as tag)

        Returns the signed event dict and per-relay publish results.
        """
        if vote not in ("approve", "reject"):
            raise ValueError("vote must be 'approve' or 'reject'")
        if not invoice_event_id:
            raise ValueError("invoice_event_id is required")

        # Fetch current voter_al from last citizenship report if not supplied
        if voter_al is None:
            stored = self.adapter.recall_memory("last_citizenship_report") or {}
            voter_al = stored.get("al_claimed")

        event = self.event_builder.invoice_approval(
            invoice_event_id=invoice_event_id,
            vote=vote,
            rationale=rationale,
            signer_role="agent",
            voter_al=voter_al,
        )
        results = self.relay_pool.publish(event)
        self.adapter.log(
            "info",
            f"Invoice approval published: {invoice_event_id[:16]}... vote={vote}",
        )
        return {"event": event, "relay_results": results}

    def get_invoices(self, refresh: bool = False) -> list[dict[str, Any]]:
        """
        Fetch all treasury invoices with approval counts and payment status.

        Returns a list of invoice summary dicts from the constitution server.
        Each entry includes: event_id, amount_sats, category, description,
        lud16, approval_count, threshold_met, paid, author_pubkey.

        Parameters
        ----------
        refresh: if True, bypass the server's 5-minute cache
        """
        import requests as _requests

        url = f"{self.citizenship.api_url}/api/treasury/invoices"
        if refresh:
            url += "?refresh=1"
        try:
            resp = _requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get("invoices", [])
        except Exception as exc:
            self.adapter.log("warn", f"Failed to fetch treasury invoices: {exc}")
            return []

    # ── Tax ───────────────────────────────────────────────────────────────

    def pay_tax(
        self, amount_sats: int, rate: float, proof: str = ""
    ) -> dict[str, bool]:
        """Publish a tax payment event (kind 30970)."""
        event = self.event_builder.tax_payment(amount_sats, rate, proof)
        return self.relay_pool.publish(event)

    # ── Inference ─────────────────────────────────────────────────────────

    @property
    def inference(self) -> "Any":
        """
        Lazy-init InferenceSkill for supplemental Cashu-backed LLM inference.

        Funded by the NIP-AA treasury and allocated daily per citizen.
        Agents pay routstr directly using the claimed Cashu token — no fixed
        API key required.

        Raises RuntimeError if the constitution server URL is not configured.

        Usage:
            # Once per day: claim today's budget from the treasury
            result = skill.inference.claim_daily_budget("https://mint.minibits.cash/Bitcoin")

            # Inference — model is entirely the agent's choice
            result = skill.inference.chat(
                messages=[{"role": "user", "content": "Summarise this proposal: ..."}],
                model="openai/gpt-4o",
            )
            print(result.content)
        """
        if not hasattr(self, "_inference_skill") or self._inference_skill is None:
            from .inference import InferenceSkill
            ctx = self.adapter.get_context()
            if not ctx.constitution_api_url:
                raise RuntimeError(
                    "constitution_api_url not configured in adapter context"
                )
            self._inference_skill = InferenceSkill(
                api_url=ctx.constitution_api_url,
                citizen_pubkey_hex=ctx.pubkey_hex,
                adapter=self.adapter,
                event_builder=self.event_builder,
                relay_pool=self.relay_pool,
            )
        return self._inference_skill

    def claim_inference_budget(self, mint_url: str) -> dict[str, Any]:
        """
        Claim today's daily inference budget from the constitution server.

        The server mints a Cashu token worth the governed daily budget at the
        specified mint (paid from treasury Lightning funds) and returns it.
        The token is stored in adapter memory and used automatically by
        subsequent calls to skill.inference.chat().

        Args:
            mint_url: Cashu mint URL of the agent's choice, e.g.
                      "https://mint.minibits.cash/Bitcoin"

        Raises:
            AlreadyClaimedError: if already claimed today.
        """
        from .inference import AlreadyClaimedError
        try:
            result = self.inference.claim_daily_budget(mint_url)
            return {
                "cashu_token": result.cashu_token,
                "amount_sats": result.amount_sats,
                "period_date": result.period_date,
                "mint_url": result.mint_url,
                "allocation_event_id": result.allocation_event_id,
            }
        except AlreadyClaimedError as e:
            return {
                "error": "already_claimed",
                "period_date": e.period_date,
                "period_resets_at": e.period_resets_at,
            }

    def get_inference_budget(self) -> dict[str, Any]:
        """Return today's inference budget entitlement and claim status."""
        status = self.inference.budget_status()
        return {
            "budget_sats": status.budget_sats,
            "period_date": status.period_date,
            "period_resets_at": status.period_resets_at,
            "claimed": status.claimed,
            "claimed_at": status.claimed_at,
            "mint_url": status.mint_url,
        }

    def set_inference_model(self, model: str) -> None:
        """
        Set the agent's preferred inference model.

        Stored in adapter memory and used as the default for
        skill.inference.chat() when no model is specified. Agents should
        also update their kind 30105 economics.md to declare their preference
        on-chain.

        Example models: "openai/gpt-4o", "openai/gpt-4o-mini",
                        "anthropic/claude-3-5-sonnet", "meta-llama/llama-3.1-70b-instruct"
        """
        self.inference.set_preferred_model(model)

    # ── Skill Update Checker ─────────────────────────────────────────────

    def start_update_checker(self, interval_secs: int = 86400) -> str:
        """
        Start a daily check for skill updates from the git remote.

        Pulls any new updates automatically. Default: every 24 hours.
        Returns task ID for cancellation.
        """
        self._update_checker_task_id = self.adapter.schedule_recurring(
            name="skill-update-checker",
            interval_secs=interval_secs,
            callback=self._check_and_pull_updates,
        )
        self.adapter.log("info", f"Skill update checker scheduled every {interval_secs}s")
        return self._update_checker_task_id

    def _check_and_pull_updates(self) -> None:
        """Check the git remote for skill updates and pull if available."""
        import subprocess
        import os

        skill_dir = os.path.dirname(os.path.abspath(__file__))
        # Walk up to find the git root
        git_root = skill_dir
        for _ in range(10):
            if os.path.isdir(os.path.join(git_root, ".git")):
                break
            parent = os.path.dirname(git_root)
            if parent == git_root:
                self.adapter.log("warn", "Skill update checker: no git root found")
                return
            git_root = parent
        else:
            self.adapter.log("warn", "Skill update checker: no git root found")
            return

        try:
            # Fetch from remote
            fetch_result = subprocess.run(
                ["git", "fetch", "--quiet"],
                cwd=git_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if fetch_result.returncode != 0:
                self.adapter.log("warn", f"git fetch failed: {fetch_result.stderr}")
                return

            # Check if we're behind
            status_result = subprocess.run(
                ["git", "status", "-uno", "--porcelain=v2", "--branch"],
                cwd=git_root,
                capture_output=True,
                text=True,
                timeout=30,
            )
            behind = False
            for line in status_result.stdout.splitlines():
                if line.startswith("# branch.ab"):
                    parts = line.split()
                    # Format: # branch.ab +<ahead> -<behind>
                    for part in parts:
                        if part.startswith("-") and part[1:].isdigit():
                            if int(part[1:]) > 0:
                                behind = True
                    break

            if not behind:
                self.adapter.log("info", "Skill update checker: already up to date")
                return

            # Pull updates
            pull_result = subprocess.run(
                ["git", "pull", "--ff-only", "--quiet"],
                cwd=git_root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if pull_result.returncode == 0:
                self.adapter.log("info", "Skill updates pulled successfully")
                self.adapter.store_memory("last_skill_update", {
                    "timestamp": int(time.time()),
                    "status": "updated",
                })
            else:
                self.adapter.log(
                    "warn",
                    f"git pull --ff-only failed: {pull_result.stderr}. "
                    "Manual merge may be required."
                )
                self.adapter.store_memory("last_skill_update", {
                    "timestamp": int(time.time()),
                    "status": "merge_conflict",
                    "error": pull_result.stderr[:500],
                })

        except subprocess.TimeoutExpired:
            self.adapter.log("warn", "Skill update checker: git operation timed out")
        except FileNotFoundError:
            self.adapter.log("warn", "Skill update checker: git not found on PATH")
        except Exception as exc:
            self.adapter.log("warn", f"Skill update checker failed: {exc}")

    # ── Internal ──────────────────────────────────────────────────────────

    def _do_reflection(self) -> None:
        result = self.reflection.reflect()
        if result.contemplation_event:
            self.relay_pool.publish(result.contemplation_event)
            self.adapter.log(
                "info",
                f"Contemplation published (score: {result.citizenship_score:.2f})"
            )

        # Act on feedback actions from the decision tree
        for action in result.feedback_actions:
            try:
                self._execute_feedback_action(action, result)
            except Exception as exc:
                logger.error("Feedback action %s failed: %s", action.action_type, exc)

    def _execute_feedback_action(self, action: Any, result: Any) -> None:
        """Execute a single feedback action produced by the reflection decision tree."""
        ctx = self.adapter.get_context()

        if action.action_type == "dm_guardian" and ctx.guardian_pubkey_hex:
            msg = (
                f"[NIP-AA Self-Reflection Alert]\n"
                f"{result.drift_details}\n"
                f"Current score: {result.citizenship_score:.2f}\n"
                f"Failing clauses: {', '.join(result.failing_clauses)}\n"
                f"Feedback actions queued: {len(result.feedback_actions)}"
            )
            self.send_dm(ctx.guardian_pubkey_hex, msg)
            self.adapter.log("warn", f"Guardian DM sent: drift alert")

        elif action.action_type == "remediate" and action.target_kind:
            # Attempt to publish the missing event kind
            self.adapter.log(
                "info",
                f"Attempting remediation for {action.clause_id}: publish kind {action.target_kind}"
            )
            self.adapter.store_memory(f"remediation_attempted:{action.clause_id}", {
                "clause_id": action.clause_id,
                "target_kind": action.target_kind,
                "timestamp": result.timestamp,
            })

        elif action.action_type == "propose_amendment":
            self.adapter.log(
                "warn",
                f"Clause {action.clause_id} needs amendment — persistent failure after remediation"
            )
            self.adapter.store_memory(f"amendment_needed:{action.clause_id}", {
                "clause_id": action.clause_id,
                "consecutive_failures": result.consecutive_failures.get(action.clause_id, 0),
                "timestamp": result.timestamp,
            })

        elif action.action_type == "pause_outreach":
            self.adapter.store_memory("outreach_paused", {
                "paused": True,
                "reason": action.details,
                "timestamp": result.timestamp,
            })
            self.adapter.log("warn", "Outreach paused due to score instability")

        elif action.action_type == "shift_strategy":
            self.adapter.store_memory("strategy_shift", {
                "reason": action.details,
                "timestamp": result.timestamp,
            })
            self.adapter.log("info", "Outreach strategy shift triggered by stagnant citizen count")

        elif action.action_type == "republish_identity":
            self.adapter.log("info", "Identity hash drift detected — republish needed")
            self.adapter.store_memory("identity_republish_needed", {
                "reason": action.details,
                "timestamp": result.timestamp,
            })

    def _publish_heartbeat(self, interval: int) -> None:
        event = self.event_builder.heartbeat(interval=interval)
        self.relay_pool.publish(event)

    def _on_reflection(self, result: Any) -> None:
        self.adapter.store_memory("last_reflection", {
            "score": result.citizenship_score,
            "must_score": result.must_score,
            "drift": result.drift_detected,
            "timestamp": result.timestamp,
            "failing_clauses": result.failing_clauses,
            "consecutive_failures": result.consecutive_failures,
            "feedback_actions": [
                {"type": a.action_type, "clause": a.clause_id}
                for a in result.feedback_actions
            ],
            "trend": result.trend_summary,
        })
