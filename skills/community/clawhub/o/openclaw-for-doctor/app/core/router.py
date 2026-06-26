from __future__ import annotations

from app.core.models import ReasoningMode, RoleStage, TaskExecutionProfile, TaskRequest, UseCase

LOOKUP_HINTS = {
    "guideline",
    "guidelines",
    "icd",
    "dose",
    "dosing",
    "criteria",
    "contraindication",
    "contraindications",
    "evidence",
    "citation",
}

DISCUSSION_HINTS = {
    "case",
    "differential",
    "unclear",
    "complex",
    "tradeoff",
    "risk",
    "conflict",
    "comorbidity",
}

ASSISTANT_HINTS = {
    "draft",
    "generate",
    "prepare",
    "organize",
    "workflow",
    "protocol",
    "ppt",
    "slides",
    "teaching material",
    "manuscript",
}

MENTOR_HINTS = {
    "teach",
    "coach",
    "board",
    "residency",
    "fellowship",
    "question bank",
    "oral exam",
}


class ProfileRouter:
    """Choose role stage and reasoning mode by use-case and intent."""

    def build_profile(self, request: TaskRequest) -> TaskExecutionProfile:
        role_stage = request.requested_role or self._infer_role(request)
        reasoning_mode = request.reasoning_mode or self._infer_mode(request)
        evidence_policy = "high" if reasoning_mode == ReasoningMode.strict else "balanced"
        return TaskExecutionProfile(
            role_stage=role_stage,
            reasoning_mode=reasoning_mode,
            use_case=request.use_case,
            evidence_policy=evidence_policy,
        )

    def _infer_role(self, request: TaskRequest) -> RoleStage:
        text = f"{request.query} {request.case_summary or ''}".lower()

        if any(h in text for h in MENTOR_HINTS):
            return RoleStage.mentor
        if any(h in text for h in ASSISTANT_HINTS):
            return RoleStage.trusted_assistant
        if any(h in text for h in DISCUSSION_HINTS):
            return RoleStage.discussion_partner
        if any(h in text for h in LOOKUP_HINTS):
            return RoleStage.encyclopedia

        if request.use_case in {UseCase.diagnosis, UseCase.treatment_rehab}:
            return RoleStage.discussion_partner
        if request.use_case in {UseCase.teaching, UseCase.research}:
            return RoleStage.trusted_assistant

        return RoleStage.encyclopedia

    def _infer_mode(self, request: TaskRequest) -> ReasoningMode:
        if request.use_case in {UseCase.diagnosis, UseCase.treatment_rehab}:
            return ReasoningMode.strict
        if request.use_case in {UseCase.teaching, UseCase.research}:
            return ReasoningMode.innovative
        return ReasoningMode.strict
