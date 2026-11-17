"""
JEP-Guard Audit Skill — Core Types
Strictly aligned with:
  - JEP-04: Judgment Event Protocol (draft-wang-jep-judgment-event-protocol-04)
  - JAC-01: Judgment Accountability Chain (draft-wang-jac-01)
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class Verb(Enum):
    """JEP-04 Section 2.1: Four immutable core verbs."""
    JUDGE = "J"
    DELEGATE = "D"
    TERMINATE = "T"
    VERIFY = "V"


class ComplianceStandard(Enum):
    EU_AI_ACT = "eu_ai_act"
    US_CALIFORNIA = "us_california"
    US_COLORADO = "us_colorado"
    GENERIC = "generic"


class AuditSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    VIOLATION = "violation"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Layer 1: JEPCodec — Strict JEP-04 + JAC-01 Event Structure
# ---------------------------------------------------------------------------

@dataclass
class JEP04Event:
    """
    Strict JEP-04 event structure (Section 2.2).
    Fields: jep, verb, who, when, what, nonce, aud, ref, sig.
    Plus JAC-01 task_based_on and extensions.
    """
    jep: str = "1"
    verb: Verb = Verb.JUDGE
    who: str = ""                    # Actor identifier (URI/DID/public key hash)
    when: int = 0                    # Unix timestamp (seconds since epoch)
    what: Optional[str] = None       # Cryptographic multihash (sha256:..., sm3:...)
    nonce: str = ""                  # UUIDv4 (Section 2.3)
    aud: Optional[str] = None        # Intended recipient
    ref: Optional[str] = None        # Reference to related event hash/ID (HJS chain)
    sig: str = ""                    # JWS signature over canonicalized JSON
    # JAC-01 Core Field (Section 1.2)
    task_based_on: Optional[str] = None   # Hash of parent judgment event
    # JEP-04 Section 2.5 + JAC-01 Section 2.1: Extensions
    extensions: Optional[Dict[str, Any]] = None


@dataclass
class JACReceipt:
    """
    JAC-01 Section 3.1: Minimal implementation wrapper.
    Wraps a JEP04Event with verification helpers.
    """
    event: JEP04Event
    raw_canonical: str = ""          # RFC 8785 canonicalized JSON before signing


# ---------------------------------------------------------------------------
# Layer 2: JEPAdapter — Friendly API Types
# ---------------------------------------------------------------------------

@dataclass
class FriendlyEvent:
    """
    Developer-friendly event format consumed by GuardSkill API.
    Automatically mapped to JEP04Event by JEPAdapter.
    """
    event_id: str                    # Maps to nonce (or used as seed)
    primitive: str                   # J/D/T/V -> verb
    issuer: str                      # -> who
    timestamp: str                   # ISO 8601 -> when (Unix)
    target: Optional[str] = None     # -> aud (or into what payload)
    assertion: Optional[Dict[str, Any]] = None   # Serialized into what
    delegate_to: Optional[str] = None            # -> D verb payload
    terminate_of: Optional[str] = None             # -> T verb payload
    verify_of: Optional[List[str]] = None          # -> V verb ref
    verification_result: Optional[str] = None
    confidence: Optional[float] = None
    prev_event_id: Optional[str] = None          # -> ref
    parent_task_hash: Optional[str] = None         # -> task_based_on (JAC)
    signature: Optional[str] = None              # -> sig
    extensions: Optional[Dict[str, Any]] = None    # -> extensions


# ---------------------------------------------------------------------------
# Layer 3: GuardSkill — Audit Domain Types
# ---------------------------------------------------------------------------

@dataclass
class AuditChainLink:
    """A single verified link in the tamper-evident audit chain."""
    event: JEP04Event
    computed_hash: str
    hash_valid: bool
    signature_valid: bool
    chain_integrity: bool
    violations: List[str] = field(default_factory=list)


@dataclass
class AuditChain:
    """Complete audit chain for a session."""
    session_id: str
    links: List[AuditChainLink]
    chain_valid: bool
    violation_count: int
    warning_count: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class ComplianceReport:
    """Regulatory compliance report export."""
    report_id: str
    standard: ComplianceStandard
    session_id: str
    generated_at: datetime
    chain_summary: Dict[str, Any]
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    export_format: str
    raw_data: Optional[str] = None


@dataclass
class ViolationRule:
    """An audit rule that detects policy violations."""
    rule_id: str
    description: str
    severity: AuditSeverity
    check: Any  # Callable
