from __future__ import annotations

from ima_runtime.shared.types import GatewayRequest, WorkflowPlanDraft, WorkflowStepDraft


def build_workflow_plan(request: GatewayRequest) -> WorkflowPlanDraft:
    summary = "Clarify image roles before video execution" if len(request.input_images) >= 2 else "Single-step video run"
    return WorkflowPlanDraft(
        summary=summary,
        steps=(
            WorkflowStepDraft(
                step_id="video-1",
                capability="video",
                goal="Resolve route and execute the requested video task",
            ),
        ),
    )
