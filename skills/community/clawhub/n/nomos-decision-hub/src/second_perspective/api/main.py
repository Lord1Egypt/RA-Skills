from __future__ import annotations

import logging
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, status
from pydantic import BaseModel

from ..governance.approval import ApprovalError
from ..hub import HubReportNotFoundError, IntelligentDecisionHub, SessionNotFoundError
from ..hub.repository import InMemoryHubReportRepository, InMemorySessionRepository
from ..models.hub import HubAnalysisRequest, HubReport
from ..models.schemas import (
    ApprovalRequest,
    DecisionRecord,
    DecisionRequest,
    DeltaVar,
    DeviationSignal,
    ReconstructionSession,
)
from ..observability import ObservabilityMiddleware, get_metrics
from ..repository import InMemoryDecisionRepository
from ..security.kms import get_signer
from ..service import DecisionNotFoundError, DecisionService
from ..tenant import TENANT_HEADER, resolve_tenant_from_claims, reset_tenant, set_tenant
from ..version import VERSION
from .authz import authz_enforced, require_scope
from .ratelimit import RateLimitMiddleware, rate_limit_enabled
from .security import verify_api_key

logger = logging.getLogger(__name__)

app = FastAPI(
    title="NOMOS Intelligent Decision-Hub",
    version=VERSION,
    description=(
        "Auditable decision orchestration with deterministic evaluation, causal "
        "counterfactuals, scenario stress tests, cognitive risk challenges, and governance."
    ),
)


@app.middleware("http")
async def log_request_lifecycle(request: Request, call_next):
    logger.info("request start method=%s path=%s", request.method, request.url.path)
    response = await call_next(request)
    logger.info(
        "request done method=%s path=%s status=%d",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


# ── v0.5 enterprise control-plane middleware ──


@app.middleware("http")
async def identity_middleware(request: Request, call_next):
    """Resolve and stash verified OIDC claims for authorization (opt-in)."""
    if authz_enforced():
        authorization = request.headers.get("Authorization", "")
        _, _, token = authorization.partition(" ")
        if token and os.getenv("SP_OIDC_ISSUER", "").strip():
            try:
                from .security import _get_oidc_config, _verify_oidc_token

                config = _get_oidc_config()
                if config is not None:
                    claims = _verify_oidc_token(token, config)
                    if claims is not None:
                        request.state.oidc_claims = claims
            except Exception:
                pass
    return await call_next(request)


@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    """Resolve the active tenant into a contextvar for the request lifetime."""
    tenant_id = request.headers.get(TENANT_HEADER)
    if not tenant_id and authz_enforced():
        claims = getattr(request.state, "oidc_claims", None)
        tenant_id = resolve_tenant_from_claims(claims)
    token = None
    if tenant_id:
        token = set_tenant(tenant_id)
    try:
        return await call_next(request)
    finally:
        if token is not None:
            reset_tenant(token)


_observability = ObservabilityMiddleware(app=None)


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    return await _observability(request, call_next)


_rl = rate_limit_enabled()
if _rl > 0:
    _rate_limiter = RateLimitMiddleware(app=None, rate_per_minute=_rl)

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        return await _rate_limiter(request, call_next)


# KMS detached-signature helper (no-op until SP_KMS_SECRET is configured).
_signer = get_signer()


def _attach_kms_signature(response: Response, *parts: str) -> None:
    if not _signer.is_configured():
        return
    payload = "::".join(parts).encode("utf-8")
    response.headers["X-Nomos-Kms-Signature"] = _signer.sign(payload)


def _build_service() -> DecisionService:
    dsn = os.getenv("SP_DATABASE_DSN", "").strip()
    if dsn:
        from ..persistence.postgres import (
            PostgresDecisionRepository,
            PostgresHubReportRepository,
        )

        return DecisionService(
            repository=PostgresDecisionRepository(dsn)
        )

    return DecisionService(repository=InMemoryDecisionRepository())


def _build_hub(service: DecisionService) -> IntelligentDecisionHub:
    dsn = os.getenv("SP_DATABASE_DSN", "").strip()
    if dsn:
        from ..persistence.postgres import PostgresHubReportRepository, PostgresSessionRepository

        return IntelligentDecisionHub(
            service=service,
            repository=PostgresHubReportRepository(dsn),
            session_repository=PostgresSessionRepository(dsn),
        )

    return IntelligentDecisionHub(
        service=service,
        repository=InMemoryHubReportRepository(),
        session_repository=InMemorySessionRepository(),
    )


service = _build_service()
hub = _build_hub(service)

# Fail fast if production is started without any authentication configured.
from .security import assert_auth_configured

assert_auth_configured()


def _build_identity_response(authorization: str | None = None) -> dict:
    """Build a lightweight identity snapshot for the /auth/me endpoint.

    When OIDC is configured, the token is fully verified (signature, expiry,
    audience, issuer) before any claim is returned. Unverified claims are never
    exposed, so a forged JWT cannot impersonate an identity via this endpoint.
    """
    if not authorization:
        return {"mode": "none", "subject": "anonymous"}
    scheme, _, supplied = authorization.partition(" ")
    if scheme.casefold() != "bearer" or not supplied:
        return {"mode": "none", "subject": "anonymous"}
    oidc_issuer = os.getenv("SP_OIDC_ISSUER", "").strip()
    if oidc_issuer:
        try:
            from .security import _get_oidc_config, _verify_oidc_token

            config = _get_oidc_config()
            if config is not None:
                claims = _verify_oidc_token(supplied, config)
                if claims is not None:
                    return {
                        "mode": "oidc",
                        "issuer": oidc_issuer,
                        "subject": claims.get("sub", ""),
                        "name": claims.get("preferred_username", claims.get("name", "")),
                        "email": claims.get("email", ""),
                        "groups": claims.get("groups", []),
                    }
        except Exception:
            pass
    return {"mode": "api_key", "subject": "bearer-authenticated"}


def _decode_oidc_token(token: str) -> dict:  # pragma: no cover - retained for compatibility
    """Deprecated: previously returned unverified claims.

    Kept only for backwards import compatibility. Identity endpoints must use
    verified claims via security._verify_oidc_token instead.
    """
    try:
        from jose import jwt

        return jwt.get_unverified_claims(token)
    except Exception:
        return {}


@app.get("/health", operation_id="healthCheck")
def health_check() -> dict[str, str]:
    return {"status": "ok", "version": VERSION}


@app.get("/v1/metrics", operation_id="metricsSnapshot")
def metrics_snapshot() -> dict:
    """In-process observability snapshot (v0.5)."""
    return get_metrics().snapshot()


@app.get("/v1/auth/me", operation_id="authWhoAmI")
def auth_me(authorization: str | None = Header(default=None)) -> dict:
    return _build_identity_response(authorization)


@app.post(
    "/v1/hub/analyze",
    response_model=HubReport,
    operation_id="analyzeDecisionHub",
    dependencies=[Depends(verify_api_key), Depends(require_scope("hub:analyze"))],
)
def analyze_decision_hub(request: HubAnalysisRequest, response: Response) -> HubReport:
    report = hub.analyze(request)
    _attach_kms_signature(response, report.hub_run_id, report.report_hash)
    return report


@app.get(
    "/v1/hub/reports/{hub_run_id}",
    response_model=HubReport,
    operation_id="getDecisionHubReport",
    dependencies=[Depends(verify_api_key)],
)
def get_decision_hub_report(hub_run_id: str) -> HubReport:
    try:
        return hub.get_report(hub_run_id)
    except HubReportNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hub report not found.",
        ) from exc


@app.post(
    "/v1/decisions/evaluate",
    response_model=DecisionRecord,
    operation_id="evaluateDecision",
    dependencies=[Depends(verify_api_key), Depends(require_scope("decisions:write"))],
)
def evaluate_decision(request: DecisionRequest, response: Response) -> DecisionRecord:
    record = service.evaluate(request)
    _attach_kms_signature(response, record.result.decision_id, record.record_hash)
    return record


@app.get(
    "/v1/decisions/{decision_id}",
    response_model=DecisionRecord,
    operation_id="getDecision",
    dependencies=[Depends(verify_api_key)],
)
def get_decision(decision_id: str) -> DecisionRecord:
    try:
        return service.get(decision_id)
    except DecisionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found.",
        ) from exc


@app.get(
    "/v1/decisions/{decision_id}/history",
    response_model=list[DecisionRecord],
    operation_id="getDecisionHistory",
    dependencies=[Depends(verify_api_key)],
)
def get_decision_history(decision_id: str) -> list[DecisionRecord]:
    try:
        return service.history(decision_id)
    except DecisionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found.",
        ) from exc


@app.post(
    "/v1/decisions/{decision_id}/approval",
    response_model=DecisionRecord,
    operation_id="recordDecisionApproval",
    dependencies=[Depends(verify_api_key), Depends(require_scope("decisions:approve"))],
)
def record_decision_approval(
    decision_id: str,
    approval: ApprovalRequest,
    response: Response,
) -> DecisionRecord:
    try:
        record = service.approve(decision_id, approval)
        _attach_kms_signature(response, decision_id, record.record_hash)
        return record
    except DecisionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found.",
        ) from exc
    except ApprovalError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


# ── Session endpoints ──


class StartSessionRequest(BaseModel):
    """Request body for starting a reconstruction session."""

    decision: DecisionRequest
    deviation_signals: list[DeviationSignal] = []
    max_iterations: int = 5
    max_evidence_requests: int = 20


class AdvanceSessionRequest(BaseModel):
    """Request body for advancing a session."""

    delta_vars: list[DeltaVar] = []


class HumanSessionDecisionRequest(BaseModel):
    """Request body for recording a human decision on a session."""

    approved: bool = False
    evidence_status: dict[str, str] = {}


@app.post(
    "/v1/hub/sessions",
    response_model=ReconstructionSession,
    operation_id="startReconstructionSession",
    dependencies=[Depends(verify_api_key)],
)
def start_reconstruction_session(body: StartSessionRequest) -> ReconstructionSession:
    return hub.start_session(
        body.decision,
        body.deviation_signals,
        max_iterations=body.max_iterations,
        max_evidence_requests=body.max_evidence_requests,
    )


@app.post(
    "/v1/hub/sessions/{session_id}/advance",
    response_model=ReconstructionSession,
    operation_id="advanceReconstructionSession",
    dependencies=[Depends(verify_api_key)],
)
def advance_reconstruction_session(
    session_id: str,
    body: AdvanceSessionRequest,
) -> ReconstructionSession:
    try:
        return hub.advance_session(session_id, body.delta_vars)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        ) from exc


@app.post(
    "/v1/hub/sessions/{session_id}/human-decision",
    response_model=ReconstructionSession,
    operation_id="humanSessionDecision",
    dependencies=[Depends(verify_api_key)],
)
def human_session_decision(
    session_id: str,
    body: HumanSessionDecisionRequest,
) -> ReconstructionSession:
    try:
        return hub.human_session_decision(
            session_id,
            approved=body.approved,
            evidence_status=body.evidence_status,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        ) from exc


@app.get(
    "/v1/hub/sessions/{session_id}",
    response_model=ReconstructionSession,
    operation_id="getReconstructionSession",
    dependencies=[Depends(verify_api_key)],
)
def get_reconstruction_session(session_id: str) -> ReconstructionSession:
    try:
        return hub.get_session(session_id)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        ) from exc
