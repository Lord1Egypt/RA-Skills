"""
JEP Primitive Skills — Atomic Reference Implementations
Judge / Delegate / Terminate / Verify

Each skill is a minimal, self-contained atomic operation.
Any complex multi-agent collaboration can be decomposed into
an ordered combination of these four primitives.

Design constraints:
  - Each skill <= 200 lines of core logic
  - Strict JEP-04 event output via JEPAdapter
  - No business logic beyond the primitive semantics
  - Extensible via JAC-01 extension modules
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from .types import FriendlyEvent, JEP04Event, Verb, PrimitiveResult
from .codec import JEPCodec
from .adapter import JEPAdapter


# ---------------------------------------------------------------------------
# Primitive 1: JudgeSkill (J)
# ---------------------------------------------------------------------------

class JudgeSkill:
    """
    Initiate an observation assertion.
    Standard template for any agent declaring "I observe X at this time."
    """

    @staticmethod
    def execute(
        issuer: str,
        target: str,
        subject: str,
        predicate: str,
        value: Any,
        confidence: Optional[float] = None,
        parent_task_hash: Optional[str] = None,
        signature: Optional[str] = None,
        extensions: Optional[Dict[str, Any]] = None,
    ) -> PrimitiveResult:
        """
        Execute a Judge primitive.

        Args:
            issuer: Actor DID initiating the observation.
            target: Target world model or scene ID.
            subject: Identifier of the observed entity.
            predicate: Property being observed.
            value: Observed value (string, number, boolean, or JSON).
            confidence: Optional confidence score [0.0, 1.0].
            parent_task_hash: Optional JAC-01 parent task hash.
            signature: Optional JWS signature.
            extensions: Optional JAC/JEP extensions.

        Returns:
            PrimitiveResult with strict JEP-04 J event.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        assertion = {
            "subject": subject,
            "predicate": predicate,
            "value": value,
        }
        if confidence is not None:
            assertion["confidence"] = confidence

        friendly = FriendlyEvent(
            event_id=f"j-{JEPCodec.generate_nonce()}",
            primitive="J",
            issuer=issuer,
            timestamp=timestamp,
            target=target,
            assertion=assertion,
            confidence=confidence,
            prev_event_id=None,
            parent_task_hash=parent_task_hash,
            signature=signature,
            extensions=extensions,
        )

        jep_event = JEPAdapter.to_jep04(friendly)

        return PrimitiveResult(
            success=True,
            event=jep_event,
            message=f"Judge event created: {subject}.{predicate}={value} by {issuer}",
            next_suggested_primitive="V",
        )


# ---------------------------------------------------------------------------
# Primitive 2: DelegateSkill (D)
# ---------------------------------------------------------------------------

class DelegateSkill:
    """
    Transfer observation or confirmation authority to another agent.
    Declares "I authorize you to observe or confirm X."
    """

    @staticmethod
    def execute(
        issuer: str,
        delegate_to: str,
        target: str,
        scope: Optional[str] = None,
        prev_event_id: Optional[str] = None,
        signature: Optional[str] = None,
        extensions: Optional[Dict[str, Any]] = None,
    ) -> PrimitiveResult:
        """
        Execute a Delegate primitive.

        Args:
            issuer: Actor DID delegating authority.
            delegate_to: Actor DID receiving authority.
            target: Target world model or scene ID.
            scope: Optional delegation scope (e.g., "continuous_observation").
            prev_event_id: Optional prior event to chain from.
            signature: Optional JWS signature.
            extensions: Optional extensions.

        Returns:
            PrimitiveResult with strict JEP-04 D event.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        ext = extensions or {}
        if scope:
            ext["https://jac.org/assign"] = {
                "assigner": issuer,
                "assignee": delegate_to,
                "delegation_scope": scope,
            }

        friendly = FriendlyEvent(
            event_id=f"d-{JEPCodec.generate_nonce()}",
            primitive="D",
            issuer=issuer,
            timestamp=timestamp,
            target=target,
            delegate_to=delegate_to,
            prev_event_id=prev_event_id,
            signature=signature,
            extensions=ext if ext else None,
        )

        jep_event = JEPAdapter.to_jep04(friendly)

        return PrimitiveResult(
            success=True,
            event=jep_event,
            message=f"Delegate event created: {issuer} -> {delegate_to} for {target}",
            next_suggested_primitive="J",
        )


# ---------------------------------------------------------------------------
# Primitive 3: TerminateSkill (T)
# ---------------------------------------------------------------------------

class TerminateSkill:
    """
    Declare that a previously initiated observation assertion is no longer valid.
    Closes the lifecycle of a state.
    """

    @staticmethod
    def execute(
        issuer: str,
        terminate_of: str,
        target: str,
        reason: Optional[str] = None,
        prev_event_id: Optional[str] = None,
        signature: Optional[str] = None,
        extensions: Optional[Dict[str, Any]] = None,
    ) -> PrimitiveResult:
        """
        Execute a Terminate primitive.

        Args:
            issuer: Actor DID terminating the assertion.
            terminate_of: Event ID (nonce) of the J event being terminated.
            target: Target world model or scene ID.
            reason: Optional termination reason (e.g., "observation_expired").
            prev_event_id: Optional prior event to chain from.
            signature: Optional JWS signature.
            extensions: Optional extensions.

        Returns:
            PrimitiveResult with strict JEP-04 T event.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        ext = extensions or {}
        ext["https://jac.org/fault"] = {
            "expected_parent": terminate_of,
            "fault_type": "termination",
            "fault_reason": reason or "State terminated by issuer",
        }

        friendly = FriendlyEvent(
            event_id=f"t-{JEPCodec.generate_nonce()}",
            primitive="T",
            issuer=issuer,
            timestamp=timestamp,
            target=target,
            terminate_of=terminate_of,
            prev_event_id=prev_event_id,
            signature=signature,
            extensions=ext,
        )

        jep_event = JEPAdapter.to_jep04(friendly)

        return PrimitiveResult(
            success=True,
            event=jep_event,
            message=f"Terminate event created: {terminate_of} terminated by {issuer}",
            next_suggested_primitive="J",
        )


# ---------------------------------------------------------------------------
# Primitive 4: VerifySkill (V)
# ---------------------------------------------------------------------------

class VerifySkill:
    """
    Cross-validate or confirm one or more observation assertions from other agents.
    Provides credibility weighting for consensus engines.
    """

    @staticmethod
    def execute(
        issuer: str,
        verify_of: List[str],
        target: str,
        verification_result: str = "confirmed",
        confidence: Optional[float] = None,
        prev_event_id: Optional[str] = None,
        signature: Optional[str] = None,
        extensions: Optional[Dict[str, Any]] = None,
    ) -> PrimitiveResult:
        """
        Execute a Verify primitive.

        Args:
            issuer: Actor DID performing verification.
            verify_of: List of event IDs (nonces) being verified.
            target: Target world model or scene ID.
            verification_result: "confirmed", "rejected", or "partial".
            confidence: Optional confidence score [0.0, 1.0].
            prev_event_id: Optional prior event to chain from.
            signature: Optional JWS signature.
            extensions: Optional extensions.

        Returns:
            PrimitiveResult with strict JEP-04 V event.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        friendly = FriendlyEvent(
            event_id=f"v-{JEPCodec.generate_nonce()}",
            primitive="V",
            issuer=issuer,
            timestamp=timestamp,
            target=target,
            verify_of=verify_of,
            verification_result=verification_result,
            confidence=confidence,
            prev_event_id=prev_event_id,
            signature=signature,
            extensions=extensions,
        )

        jep_event = JEPAdapter.to_jep04(friendly)

        return PrimitiveResult(
            success=True,
            event=jep_event,
            message=f"Verify event created: {issuer} {verification_result} {len(verify_of)} event(s)",
            next_suggested_primitive="V",
        )
