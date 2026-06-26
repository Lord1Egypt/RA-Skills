from __future__ import annotations

from ima_runtime.capabilities.image.routes import build_image_task_spec
from ima_runtime.shared.types import ClarificationRequest, GatewayRequest, WorkflowPlanDraft, WorkflowStepDraft


def build_workflow_plan(request: GatewayRequest) -> WorkflowPlanDraft:
    routed = build_image_task_spec(request)
    summary = "Clarify reference image before image execution" if isinstance(
        routed, ClarificationRequest
    ) else "Single-step image run"
    return WorkflowPlanDraft(
        summary=summary,
        steps=(
            WorkflowStepDraft(
                step_id="image-1",
                capability="image",
                goal="Resolve route and execute the requested image task",
            ),
        ),
    )
