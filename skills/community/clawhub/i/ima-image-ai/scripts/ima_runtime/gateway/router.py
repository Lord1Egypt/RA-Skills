from __future__ import annotations

from ima_runtime.capabilities.image.routes import build_image_task_spec
from ima_runtime.shared.types import ClarificationRequest, GatewayRequest, RouteDecision


def route_request(request: GatewayRequest) -> RouteDecision | ClarificationRequest:
    result = build_image_task_spec(request)
    if isinstance(result, ClarificationRequest):
        return result
    return RouteDecision(capability="image", reason=f"image task_type={result.task_type}")
