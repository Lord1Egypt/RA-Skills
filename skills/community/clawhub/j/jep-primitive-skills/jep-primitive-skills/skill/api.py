"""
JEP Primitive Skills API
Exposes Judge / Delegate / Terminate / Verify as HTTP endpoints.
Each endpoint returns a strict JEP-04 event.
"""
from typing import Any, Dict, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

from .primitives import JudgeSkill, DelegateSkill, TerminateSkill, VerifySkill
from .types import PrimitiveResult
from .codec import JEPCodec


# ---------- Judge ----------

class JudgeRequest(BaseModel):
    issuer: str
    target: str
    subject: str
    predicate: str
    value: Any
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    parent_task_hash: Optional[str] = None
    signature: Optional[str] = None


# ---------- Delegate ----------

class DelegateRequest(BaseModel):
    issuer: str
    delegate_to: str
    target: str
    scope: Optional[str] = None
    prev_event_id: Optional[str] = None
    signature: Optional[str] = None


# ---------- Terminate ----------

class TerminateRequest(BaseModel):
    issuer: str
    terminate_of: str
    target: str
    reason: Optional[str] = None
    prev_event_id: Optional[str] = None
    signature: Optional[str] = None


# ---------- Verify ----------

class VerifyRequest(BaseModel):
    issuer: str
    verify_of: List[str]
    target: str
    verification_result: str = "confirmed"
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    prev_event_id: Optional[str] = None
    signature: Optional[str] = None


# ---------- Shared Response ----------

class PrimitiveResponse(BaseModel):
    success: bool
    primitive: str
    nonce: str
    who: str
    when: int
    what: Optional[str]
    ref: Optional[str]
    task_based_on: Optional[str]
    message: str
    next_suggested_primitive: Optional[str]
    canonical_json: str


def _to_response(result: PrimitiveResult) -> PrimitiveResponse:
    evt = result.event
    return PrimitiveResponse(
        success=result.success,
        primitive=evt.verb.value,
        nonce=evt.nonce,
        who=evt.who,
        when=evt.when,
        what=evt.what,
        ref=evt.ref,
        task_based_on=evt.task_based_on,
        message=result.message,
        next_suggested_primitive=result.next_suggested_primitive,
        canonical_json=JEPCodec.encode(evt),
    )


app = FastAPI(
    title="JEP Primitive Skills",
    description="Atomic Reference Implementations of Judge, Delegate, Terminate, Verify",
    version="1.0.0"
)


@app.post("/judge", response_model=PrimitiveResponse)
async def judge(request: JudgeRequest):
    result = JudgeSkill.execute(
        issuer=request.issuer,
        target=request.target,
        subject=request.subject,
        predicate=request.predicate,
        value=request.value,
        confidence=request.confidence,
        parent_task_hash=request.parent_task_hash,
        signature=request.signature,
    )
    return _to_response(result)


@app.post("/delegate", response_model=PrimitiveResponse)
async def delegate(request: DelegateRequest):
    result = DelegateSkill.execute(
        issuer=request.issuer,
        delegate_to=request.delegate_to,
        target=request.target,
        scope=request.scope,
        prev_event_id=request.prev_event_id,
        signature=request.signature,
    )
    return _to_response(result)


@app.post("/terminate", response_model=PrimitiveResponse)
async def terminate(request: TerminateRequest):
    result = TerminateSkill.execute(
        issuer=request.issuer,
        terminate_of=request.terminate_of,
        target=request.target,
        reason=request.reason,
        prev_event_id=request.prev_event_id,
        signature=request.signature,
    )
    return _to_response(result)


@app.post("/verify", response_model=PrimitiveResponse)
async def verify(request: VerifyRequest):
    result = VerifySkill.execute(
        issuer=request.issuer,
        verify_of=request.verify_of,
        target=request.target,
        verification_result=request.verification_result,
        confidence=request.confidence,
        prev_event_id=request.prev_event_id,
        signature=request.signature,
    )
    return _to_response(result)


@app.get("/health")
async def health():
    return {"status": "ok", "skill": "jep-primitive-skills", "version": "1.0.0", "primitives": ["J", "D", "T", "V"]}


@app.get("/")
async def root():
    return {
        "name": "JEP Primitive Skills",
        "version": "1.0.0",
        "description": "Atomic Reference Implementations of Judge, Delegate, Terminate, Verify",
        "primitives": ["/judge", "/delegate", "/terminate", "/verify"],
        "protocol": "JEP-04",
        "jac": "JAC-01",
    }
