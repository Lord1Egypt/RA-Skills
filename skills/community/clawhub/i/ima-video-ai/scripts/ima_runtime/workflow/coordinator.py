from __future__ import annotations

from ima_runtime.gateway.planner import build_workflow_plan
from ima_runtime.shared.types import GatewayRequest, WorkflowPlanDraft
from ima_runtime.workflow.confirmation import to_confirmable_plan


def build_confirmable_plan(request: GatewayRequest) -> WorkflowPlanDraft:
    return to_confirmable_plan(build_workflow_plan(request))
