"""
JEPAdapter — Mapping Layer
Converts FriendlyEvent to strict JEP04Event.
"""
from typing import Any, Dict, Optional

from .types import FriendlyEvent, JEP04Event, Verb
from .codec import JEPCodec


class JEPAdapter:
    @staticmethod
    def to_jep04(friendly: FriendlyEvent) -> JEP04Event:
        verb = Verb(friendly.primitive)
        when = JEPCodec.iso_to_unix(friendly.timestamp)
        nonce = JEPCodec.generate_nonce()

        # Build what payload
        what_payload = {}
        if friendly.assertion:
            what_payload["assertion"] = friendly.assertion
        if friendly.delegate_to:
            what_payload["delegate_to"] = friendly.delegate_to
        if friendly.terminate_of:
            what_payload["terminate_of"] = friendly.terminate_of
        if friendly.verify_of:
            what_payload["verify_of"] = friendly.verify_of
            what_payload["verification_result"] = friendly.verification_result
        if friendly.confidence is not None:
            what_payload["confidence"] = friendly.confidence
        what = JEPCodec.compute_what(what_payload) if what_payload else None

        # ref from prev_event_id or verify_of
        ref = None
        if friendly.verify_of and len(friendly.verify_of) > 0:
            ref = friendly.verify_of[0]
        elif friendly.prev_event_id:
            ref = friendly.prev_event_id

        extensions = friendly.extensions or {}

        # JAC extensions
        if friendly.verification_result or friendly.confidence is not None:
            jac_result = {}
            if friendly.verification_result:
                jac_result["verification_result"] = friendly.verification_result
            if friendly.confidence is not None:
                jac_result["confidence"] = friendly.confidence
            extensions["https://jac.org/result"] = jac_result

        if friendly.delegate_to:
            extensions["https://jac.org/assign"] = {
                "assignee": friendly.delegate_to,
                "assigner": friendly.issuer
            }

        if verb == Verb.TERMINATE and friendly.terminate_of:
            extensions["https://jac.org/fault"] = {
                "expected_parent": friendly.terminate_of,
                "fault_type": "orphan_termination",
                "fault_reason": "Terminate references a non-existent or expired event"
            }

        if friendly.target:
            extensions["https://jep.org/subject"] = {
                "id": friendly.target,
                "predicate": friendly.assertion.get("predicate") if friendly.assertion else None
            }

        return JEP04Event(
            jep="1", verb=verb, who=friendly.issuer, when=when,
            what=what, nonce=nonce, aud=friendly.target, ref=ref,
            sig=friendly.signature or "",
            task_based_on=friendly.parent_task_hash,
            extensions=extensions if extensions else None,
        )

    @staticmethod
    def from_jep04(event: JEP04Event) -> FriendlyEvent:
        assertion = None
        delegate_to = None
        terminate_of = None
        verify_of = None
        verification_result = None
        confidence = None

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
            event_id=event.nonce, primitive=event.verb.value,
            issuer=event.who, timestamp=JEPCodec.unix_to_iso(event.when),
            target=event.aud, assertion=assertion,
            delegate_to=delegate_to, terminate_of=terminate_of,
            verify_of=[event.ref] if event.ref else None,
            verification_result=verification_result,
            confidence=confidence, prev_event_id=event.ref,
            parent_task_hash=event.task_based_on,
            signature=event.sig, extensions=event.extensions,
        )
