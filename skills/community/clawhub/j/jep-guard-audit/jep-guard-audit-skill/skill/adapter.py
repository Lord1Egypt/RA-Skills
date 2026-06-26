"""
JEPAdapter — Mapping Layer
Converts developer-friendly FriendlyEvent fields to strict JEP04Event fields.

Friendly Field          -> JEP-04 Field       -> JAC-01 Field
-----------------------    ------------------    ------------------
event_id                 -> nonce (UUIDv4)
primitive (J/D/T/V)      -> verb
issuer                   -> who
timestamp (ISO)          -> when (Unix)
target                   -> aud (or into what)
assertion (dict)         -> what (multihash)
delegate_to              -> what (multihash) + extensions
terminate_of             -> what (multihash)
verify_of (list)         -> ref
verification_result      -> extensions[JAC-Result]
confidence               -> extensions[JAC-Result]
prev_event_id            -> ref
parent_task_hash         -> task_based_on
signature                -> sig
extensions               -> extensions
"""
from typing import Any, Dict, Optional

from .types import FriendlyEvent, JEP04Event, Verb
from .codec import JEPCodec


class JEPAdapter:
    """
    One-way adapter: FriendlyEvent -> JEP04Event.
    Zero business logic. Pure field mapping + canonicalization.
    """

    @staticmethod
    def to_jep04(friendly: FriendlyEvent) -> JEP04Event:
        """
        Convert a FriendlyEvent to a strict JEP04Event.
        Automatically generates nonce, computes what multihash, converts timestamps.
        """
        # Map primitive to verb
        verb = Verb(friendly.primitive)

        # Convert ISO timestamp to Unix seconds
        when = JEPCodec.iso_to_unix(friendly.timestamp)

        # Generate UUIDv4 nonce from event_id (or fresh if not UUID)
        nonce = JEPCodec.generate_nonce()

        # Compute 'what' multihash from assertion payload
        what_payload = JEPAdapter._build_what_payload(friendly, verb)
        what = JEPCodec.compute_what(what_payload) if what_payload else None

        # Map verify_of -> ref (JEP-04 ref points to related event hash/ID)
        ref = None
        if friendly.verify_of and len(friendly.verify_of) > 0:
            ref = friendly.verify_of[0]  # Primary reference
        elif friendly.prev_event_id:
            ref = friendly.prev_event_id

        # Assemble extensions
        extensions = friendly.extensions or {}

        # JAC-01 Result extension: verification_result + confidence
        if friendly.verification_result is not None or friendly.confidence is not None:
            jac_result = {}
            if friendly.verification_result:
                jac_result["verification_result"] = friendly.verification_result
            if friendly.confidence is not None:
                jac_result["confidence"] = friendly.confidence
            extensions["https://jac.org/result"] = jac_result

        # JAC-01 Assign extension: delegate_to
        if friendly.delegate_to:
            extensions["https://jac.org/assign"] = {
                "assignee": friendly.delegate_to,
                "assigner": friendly.issuer
            }

        # JAC-01 Fault extension: terminate_of without prior event
        if verb == Verb.TERMINATE and friendly.terminate_of:
            extensions["https://jac.org/fault"] = {
                "expected_parent": friendly.terminate_of,
                "fault_type": "orphan_termination",
                "fault_reason": "Terminate references a non-existent or expired event"
            }

        # JEP-04 Subject Reference extension: target -> subject
        if friendly.target:
            extensions["https://jep.org/subject"] = {
                "id": friendly.target,
                "predicate": friendly.assertion.get("predicate") if friendly.assertion else None
            }

        return JEP04Event(
            jep="1",
            verb=verb,
            who=friendly.issuer,
            when=when,
            what=what,
            nonce=nonce,
            aud=friendly.target,
            ref=ref,
            sig=friendly.signature or "",
            task_based_on=friendly.parent_task_hash,
            extensions=extensions if extensions else None,
        )

    @staticmethod
    def _build_what_payload(friendly: FriendlyEvent, verb: Verb) -> Optional[Dict[str, Any]]:
        """
        Build the payload that gets hashed into the 'what' multihash.
        JEP-04: 'what' is the cryptographic multihash of decision content.
        """
        payload: Dict[str, Any] = {}

        if friendly.assertion:
            payload["assertion"] = friendly.assertion

        if verb == Verb.DELEGATE and friendly.delegate_to:
            payload["delegate_to"] = friendly.delegate_to

        if verb == Verb.TERMINATE and friendly.terminate_of:
            payload["terminate_of"] = friendly.terminate_of

        if verb == Verb.VERIFY and friendly.verify_of:
            payload["verify_of"] = friendly.verify_of
            payload["verification_result"] = friendly.verification_result

        if friendly.confidence is not None:
            payload["confidence"] = friendly.confidence

        return payload if payload else None

    @staticmethod
    def from_jep04(event: JEP04Event) -> FriendlyEvent:
        """
        Reverse mapping: JEP04Event -> FriendlyEvent (for API responses).
        Used when returning chain inspection results to developers.
        """
        # Decode what payload (best-effort; what is a hash, original data may be lost)
        assertion = None
        delegate_to = None
        terminate_of = None
        verify_of = None
        verification_result = None
        confidence = None

        # Extract from extensions if available
        if event.extensions:
            jac_result = event.extensions.get("https://jac.org/result")
            if jac_result:
                verification_result = jac_result.get("verification_result")
                confidence = jac_result.get("confidence")

            jac_assign = event.extensions.get("https://jac.org/assign")
            if jac_assign:
                delegate_to = jac_assign.get("assignee")

            jac_fault = event.extensions.get("https://jac.org/fault")
            if jac_fault:
                terminate_of = jac_fault.get("expected_parent")

        return FriendlyEvent(
            event_id=event.nonce,
            primitive=event.verb.value,
            issuer=event.who,
            timestamp=JEPCodec.unix_to_iso(event.when),
            target=event.aud,
            assertion=assertion,
            delegate_to=delegate_to,
            terminate_of=terminate_of,
            verify_of=[event.ref] if event.ref else None,
            verification_result=verification_result,
            confidence=confidence,
            prev_event_id=event.ref,
            parent_task_hash=event.task_based_on,
            signature=event.sig,
            extensions=event.extensions,
        )
