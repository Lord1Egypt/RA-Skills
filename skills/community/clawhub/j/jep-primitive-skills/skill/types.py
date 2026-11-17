"""
JEP Primitive Skills — Core Types
Strictly aligned with JEP-04 (draft-wang-jep-judgment-event-protocol-04)
and JAC-01 (draft-wang-jac-01).

Four atomic primitives form the complete collaboration grammar:
  J (Judge)     — Initiate an observation assertion
  D (Delegate)  — Transfer authority to another agent
  T (Terminate) — Close the lifecycle of a prior assertion
  V (Verify)    — Cross-validate an existing assertion

No fifth primitive is required.
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Verb(Enum):
    JUDGE = "J"
    DELEGATE = "D"
    TERMINATE = "T"
    VERIFY = "V"


@dataclass
class JEP04Event:
    """Strict JEP-04 event structure (Section 2.2)."""
    jep: str = "1"
    verb: Verb = Verb.JUDGE
    who: str = ""
    when: int = 0
    what: Optional[str] = None
    nonce: str = ""
    aud: Optional[str] = None
    ref: Optional[str] = None
    sig: str = ""
    task_based_on: Optional[str] = None
    extensions: Optional[Dict[str, Any]] = None


@dataclass
class FriendlyEvent:
    """Developer-friendly event format."""
    event_id: str
    primitive: str
    issuer: str
    timestamp: str
    target: Optional[str] = None
    assertion: Optional[Dict[str, Any]] = None
    delegate_to: Optional[str] = None
    terminate_of: Optional[str] = None
    verify_of: Optional[List[str]] = None
    verification_result: Optional[str] = None
    confidence: Optional[float] = None
    prev_event_id: Optional[str] = None
    parent_task_hash: Optional[str] = None
    signature: Optional[str] = None
    extensions: Optional[Dict[str, Any]] = None


@dataclass
class PrimitiveResult:
    """Result of executing a primitive skill."""
    success: bool
    event: JEP04Event
    message: str
    next_suggested_primitive: Optional[str] = None
