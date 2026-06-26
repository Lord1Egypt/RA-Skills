from __future__ import annotations

import uuid
from typing import List, Optional

from app.core.models import (
    Citation,
    ExecutionContext,
    ReasoningMode,
    RoleStage,
    TaskExecutionProfile,
    TaskRequest,
    TaskResult,
    UseCase,
)
from app.core.router import ProfileRouter

EVIDENCE_REGISTRY = {
    "sepsis": [
        Citation(
            source="Surviving Sepsis Campaign",
            title="International Guidelines for Management of Sepsis and Septic Shock",
            evidence_level="Guideline",
            note="Prioritize 1-hour bundle for suspected septic shock and source control.",
        )
    ],
    "stroke": [
        Citation(
            source="AHA/ASA",
            title="Guidelines for Early Management of Acute Ischemic Stroke",
            evidence_level="Guideline",
            note="Rapid triage, brain imaging, and reperfusion windows are critical.",
        )
    ],
    "diabetes": [
        Citation(
            source="ADA",
            title="Standards of Care in Diabetes",
            evidence_level="Guideline",
            note="Individualized glycemic targets and cardio-renal risk reduction are core.",
        )
    ],
    "pneumonia": [
        Citation(
            source="IDSA/ATS",
            title="Community-Acquired Pneumonia in Adults",
            evidence_level="Guideline",
            note="Use severity scoring to support admission and empiric treatment selection.",
        )
    ],
}

DEFAULT_CITATIONS = [
    Citation(
        source="Cochrane",
        title="Systematic Review Methodology",
        evidence_level="Systematic Review",
        note="Prefer higher-level evidence and explicitly mark uncertainty.",
    ),
    Citation(
        source="GRADE Working Group",
        title="GRADE Framework",
        evidence_level="Methodology",
        note="Separate certainty of evidence from strength of recommendation.",
    ),
]


class DoctorAssistantEngine:
    """Core assistant engine for OpenClaw Doctor workflows."""

    def __init__(self, router: Optional[ProfileRouter] = None):
        self.router = router or ProfileRouter()

    def execute(self, request: TaskRequest, task_id: Optional[str] = None) -> TaskResult:
        profile = self.router.build_profile(request)
        context = ExecutionContext(profile=profile)

        citations = self._collect_citations(request, context)
        summary = self._build_summary(request, profile)
        analysis = self._build_analysis(request, profile)
        action_plan = self._build_action_plan(request, profile)
        guardrails = self._build_guardrails(profile)
        next_expansion_tracks = self._build_next_tracks(profile)

        return TaskResult(
            task_id=task_id or str(uuid.uuid4()),
            role_stage=profile.role_stage,
            reasoning_mode=profile.reasoning_mode,
            use_case=profile.use_case,
            summary=summary,
            analysis=analysis,
            action_plan=action_plan,
            citations=citations,
            guardrails=guardrails,
            next_expansion_tracks=next_expansion_tracks,
        )

    def build_profile(self, request: TaskRequest) -> TaskExecutionProfile:
        return self.router.build_profile(request)

    def _collect_citations(self, request: TaskRequest, context: ExecutionContext) -> List[Citation]:
        if not request.require_citations:
            return []

        text = f"{request.query} {request.case_summary or ''}".lower()
        matched: list[Citation] = []
        for keyword, citations in EVIDENCE_REGISTRY.items():
            if keyword in text:
                matched.extend(citations)

        if not matched:
            matched = list(DEFAULT_CITATIONS)

        if context.profile.reasoning_mode == ReasoningMode.strict:
            return matched
        return matched[:1]

    def _build_summary(self, request: TaskRequest, profile: TaskExecutionProfile) -> str:
        if profile.role_stage == RoleStage.encyclopedia:
            return "Evidence-focused lookup completed with concise references and decision anchors."
        if profile.role_stage == RoleStage.discussion_partner:
            return "Case reasoning structured into differential hypotheses, uncertainty zones, and next tests."
        if profile.role_stage == RoleStage.trusted_assistant:
            return "Actionable deliverable drafted for clinical/teaching/research execution."
        return "Mentor mode output generated with teaching points and decision rationale."

    def _build_analysis(self, request: TaskRequest, profile: TaskExecutionProfile) -> List[str]:
        base = [
            f"Use-case: {profile.use_case.value}",
            f"Role-stage: {profile.role_stage.value}",
            "Focus on problem representation before committing to a single diagnosis.",
        ]

        if profile.reasoning_mode == ReasoningMode.strict:
            base.append("Strict mode enabled: prefer guideline-backed claims and clearly state uncertainty.")
        else:
            base.append("Innovative mode enabled: include testable alternatives and explain validation needs.")

        if profile.use_case in {UseCase.diagnosis, UseCase.treatment_rehab}:
            base.append("Clinical priority: time-sensitive threats, contraindications, and follow-up triggers.")
        elif profile.use_case == UseCase.teaching:
            base.append("Teaching priority: convert decisions into teachable checkpoints and questions.")
        else:
            base.append("Research priority: identify evidence gaps and candidate study directions.")

        return base

    def _build_action_plan(self, request: TaskRequest, profile: TaskExecutionProfile) -> List[str]:
        if profile.use_case in {UseCase.diagnosis, UseCase.treatment_rehab}:
            return [
                "Create structured problem list: syndromes, severity, and immediate red flags.",
                "Rank differential diagnosis with evidence for and against each hypothesis.",
                "Define next 24-hour and 72-hour workup/treatment checkpoints.",
                "Package final recommendation for channel delivery to requesting doctor.",
            ]

        if profile.use_case == UseCase.teaching:
            return [
                "Generate a 10-slide teaching skeleton: case stem, decision pivots, and pitfalls.",
                "Add one evidence-backed key message per slide.",
                "Prepare quiz prompts for resident debrief.",
                "Send materials and revision checklist back to the doctor.",
            ]

        return [
            "Build a focused literature matrix by outcome, comparator, and population.",
            "Draft candidate hypothesis with measurable endpoints.",
            "List data requirements, confounders, and feasibility constraints.",
            "Return abstract-level concept note for quick expert review.",
        ]

    def _build_guardrails(self, profile: TaskExecutionProfile) -> List[str]:
        guardrails = [
            "Assistant output supports clinicians; it is not autonomous medical decision-making.",
            "Always verify patient-specific contraindications and local protocol constraints.",
            "Escalate to senior supervision for unstable patients or high-risk interventions.",
        ]
        if profile.reasoning_mode == ReasoningMode.innovative:
            guardrails.append("Innovative suggestions are hypothesis-level and require validation before adoption.")
        return guardrails

    def _build_next_tracks(self, profile: TaskExecutionProfile) -> List[str]:
        return [
            "Clinical core: differential diagnosis and treatment-rehab co-pilot.",
            "Teaching extension: case conference deck and residency coaching assistant.",
            "Research extension: literature synthesis and protocol ideation workflows.",
        ]
