from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.schemas import (
    ActionRequest,
    AuditLogResponse,
    EvaluationResponse,
    HealthResponse,
    PolicyCreate,
    PolicyResponse,
    PolicyUpdate,
)
from app.seed import default_policies
from app.service import create_policy, evaluate, get_policy, list_audit_logs, list_policies, update_policy


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Agent Policy & Guardrails Engine", version="0.1.0", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@app.post("/policies", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
def create_policy_endpoint(payload: PolicyCreate, db: Session = Depends(get_db)) -> PolicyResponse:
    try:
        policy = create_policy(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PolicyResponse.model_validate(policy)


@app.get("/policies", response_model=list[PolicyResponse])
def list_policies_endpoint(db: Session = Depends(get_db)) -> list[PolicyResponse]:
    return [PolicyResponse.model_validate(p) for p in list_policies(db)]


@app.get("/policies/{policy_id}", response_model=PolicyResponse)
def get_policy_endpoint(policy_id: str, db: Session = Depends(get_db)) -> PolicyResponse:
    policy = get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return PolicyResponse.model_validate(policy)


@app.patch("/policies/{policy_id}", response_model=PolicyResponse)
def update_policy_endpoint(policy_id: str, payload: PolicyUpdate, db: Session = Depends(get_db)) -> PolicyResponse:
    policy = get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    try:
        updated = update_policy(db, policy, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PolicyResponse.model_validate(updated)


@app.delete("/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def disable_policy_endpoint(policy_id: str, db: Session = Depends(get_db)) -> Response:
    policy = get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    policy.enabled = False
    db.add(policy)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_endpoint(action: ActionRequest, db: Session = Depends(get_db)) -> EvaluationResponse:
    result = evaluate(db, action)
    return EvaluationResponse(action_id=action.action_id, action_type=action.action_type, result=result)


@app.get("/audit", response_model=list[AuditLogResponse])
def list_audit_logs_endpoint(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=500),
) -> list[AuditLogResponse]:
    return [AuditLogResponse.model_validate(log) for log in list_audit_logs(db, limit=limit)]


@app.post("/seed", response_model=list[PolicyResponse])
def seed_default_policies(db: Session = Depends(get_db)) -> list[PolicyResponse]:
    created: list[PolicyResponse] = []
    for policy in default_policies():
        if get_policy(db, policy.policy_id):
            continue
        created.append(PolicyResponse.model_validate(create_policy(db, policy)))
    return created
