from __future__ import annotations

from ima_runtime.shared.types import ClarificationRequest, GatewayRequest, RouteDecision


def route_request(request: GatewayRequest) -> RouteDecision | ClarificationRequest:
    from ima_runtime.capabilities.video.routes import build_video_task_spec

    result = build_video_task_spec(request)
    if isinstance(result, ClarificationRequest):
        return result
    return RouteDecision(capability="video", reason=f"video task_type={result.task_type}")
