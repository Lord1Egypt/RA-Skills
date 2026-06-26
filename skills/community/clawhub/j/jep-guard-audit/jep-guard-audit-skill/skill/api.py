"""
JEP-Guard Audit Skill API
FastAPI HTTP service. Exposes friendly fields; internally maps to JEP-04 via JEPAdapter.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field

from .core import AuditEngine
from .types import FriendlyEvent, ComplianceStandard, AuditChain
from .adapter import JEPAdapter
from .codec import JEPCodec


class EventInput(BaseModel):
    """Developer-friendly JEP event input."""
    event_id: str
    primitive: str = Field(..., pattern="^[JDTV]$")
    issuer: str
    timestamp: str
    target: Optional[str] = None
    assertion: Optional[Dict[str, Any]] = None
    delegate_to: Optional[str] = None
    terminate_of: Optional[str] = None
    verify_of: Optional[List[str]] = None
    verification_result: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    prev_event_id: Optional[str] = None
    parent_task_hash: Optional[str] = None
    signature: Optional[str] = None
    extensions: Optional[Dict[str, Any]] = None


class IngestRequest(BaseModel):
    """Request to ingest events."""
    session_id: str
    events: List[EventInput]

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "loan-decision-001",
                "events": [
                    {
                        "event_id": "jep-1",
                        "primitive": "J",
                        "issuer": "gpt-4-agent",
                        "timestamp": "2026-04-26T09:00:00Z",
                        "target": "loan-decision",
                        "assertion": {"subject": "applicant_123", "predicate": "approval", "value": "approved"},
                        "confidence": 0.92,
                        "prev_event_id": None,
                        "parent_task_hash": None,
                        "signature": "eyJhbGciOiJFZERTQSJ9..."
                    },
                    {
                        "event_id": "jep-2",
                        "primitive": "V",
                        "issuer": "audit-bot",
                        "timestamp": "2026-04-26T09:00:05Z",
                        "target": "loan-decision",
                        "verify_of": ["jep-1"],
                        "verification_result": "confirmed",
                        "confidence": 0.98,
                        "prev_event_id": "jep-1",
                        "signature": "eyJhbGciOiJFZERTQSJ9..."
                    }
                ]
            }
        }


class ChainResponse(BaseModel):
    """Audit chain response with strict JEP-04 fields."""
    session_id: str
    chain_valid: bool
    total_events: int
    violation_count: int
    warning_count: int
    start_time: Optional[str]
    end_time: Optional[str]
    links: List[Dict[str, Any]]


class ExportRequest(BaseModel):
    """Request to export compliance report."""
    session_id: str
    standard: str = "generic"

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "loan-decision-001",
                "standard": "eu_ai_act"
            }
        }


class ExportResponse(BaseModel):
    """Compliance report response."""
    report_id: str
    standard: str
    session_id: str
    generated_at: str
    chain_summary: Dict[str, Any]
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    raw_data: str


app = FastAPI(
    title="JEP-Guard Audit Skill",
    description="Strict JEP-04 / JAC-01 Compliant Audit Chain with Friendly API",
    version="1.0.0"
)

engine = AuditEngine()


def _to_friendly(inp: EventInput) -> FriendlyEvent:
    return FriendlyEvent(
        event_id=inp.event_id,
        primitive=inp.primitive,
        issuer=inp.issuer,
        timestamp=inp.timestamp,
        target=inp.target,
        assertion=inp.assertion,
        delegate_to=inp.delegate_to,
        terminate_of=inp.terminate_of,
        verify_of=inp.verify_of,
        verification_result=inp.verification_result,
        confidence=inp.confidence,
        prev_event_id=inp.prev_event_id,
        parent_task_hash=inp.parent_task_hash,
        signature=inp.signature,
        extensions=inp.extensions,
    )


@app.post("/audit/ingest")
async def ingest(request: IngestRequest):
    for evt_in in request.events:
        engine.ingest(request.session_id, _to_friendly(evt_in))
    return {
        "session_id": request.session_id,
        "events_ingested": len(request.events),
        "status": "ok"
    }


@app.get("/audit/chain/{session_id}", response_model=ChainResponse)
async def get_chain(session_id: str):
    chain = engine.build_chain(session_id)
    return ChainResponse(
        session_id=chain.session_id,
        chain_valid=chain.chain_valid,
        total_events=len(chain.links),
        violation_count=chain.violation_count,
        warning_count=chain.warning_count,
        start_time=chain.start_time.isoformat() if chain.start_time else None,
        end_time=chain.end_time.isoformat() if chain.end_time else None,
        links=[
            {
                "nonce": l.event.nonce,
                "verb": l.event.verb.value,
                "who": l.event.who,
                "when": l.event.when,
                "what": l.event.what,
                "ref": l.event.ref,
                "task_based_on": l.event.task_based_on,
                "computed_hash": l.computed_hash,
                "hash_valid": l.hash_valid,
                "signature_valid": l.signature_valid,
                "chain_integrity": l.chain_integrity,
                "violations": l.violations,
            }
            for l in chain.links
        ]
    )


@app.post("/audit/export", response_model=ExportResponse)
async def export(request: ExportRequest):
    standard = ComplianceStandard(request.standard)
    report = engine.export_compliance(request.session_id, standard)
    return ExportResponse(
        report_id=report.report_id,
        standard=report.standard.value,
        session_id=report.session_id,
        generated_at=report.generated_at.isoformat(),
        chain_summary=report.chain_summary,
        findings=report.findings,
        recommendations=report.recommendations,
        raw_data=report.raw_data
    )


@app.get("/health")
async def health():
    return {"status": "ok", "skill": "jep-guard-audit", "version": "1.0.0", "protocol": "JEP-04", "jac": "JAC-01"}


@app.get("/")
async def root():
    return {
        "name": "JEP-Guard Audit Skill",
        "version": "1.0.0",
        "protocol": "JEP-04",
        "jac": "JAC-01",
        "description": "Strict JEP-04 / JAC-01 Compliant Audit Chain with Friendly API",
        "endpoints": ["/audit/ingest", "/audit/chain/{session_id}", "/audit/export"],
        "standards": ["generic", "eu_ai_act", "us_california", "us_colorado"],
        "architecture": ["GuardSkill (API)", "JEPAdapter (Mapping)", "JEPCodec (Protocol)"]
    }
