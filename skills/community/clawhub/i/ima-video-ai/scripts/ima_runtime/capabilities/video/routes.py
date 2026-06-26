from __future__ import annotations

from ima_runtime.shared.config import VIDEO_TASK_TYPES
from ima_runtime.shared.inputs import validate_task_inputs
from ima_runtime.shared.types import ClarificationRequest, GatewayRequest, TaskSpec


def _build_task_spec(request: GatewayRequest, task_type: str) -> TaskSpec:
    input_images = tuple(validate_task_inputs(task_type, list(request.input_images), request.media_assets))
    return TaskSpec(
        capability="video",
        task_type=task_type,
        prompt=request.prompt,
        input_images=input_images,
        media_assets=request.media_assets,
        extra_params=dict(request.extra_params),
    )


def build_video_task_spec(request: GatewayRequest) -> TaskSpec | ClarificationRequest:
    explicit_task_type = request.intent_hints.get("task_type")
    if explicit_task_type in VIDEO_TASK_TYPES:
        return _build_task_spec(request, explicit_task_type)

    mode = request.intent_hints.get("video_mode")
    if mode == "first_last_frame":
        return _build_task_spec(request, "first_last_frame_to_video")
    if mode == "reference":
        return _build_task_spec(request, "reference_image_to_video")
    if len(request.input_images) == 1:
        return _build_task_spec(request, "image_to_video")
    if len(request.input_images) >= 2:
        return ClarificationRequest(
            reason="video image roles ambiguous",
            question="这两张图分别是什么角色？是首帧/尾帧，还是参考图，还是只动其中一张？",
            options=("首帧/尾帧", "参考图", "只动其中一张"),
        )
    return _build_task_spec(request, "text_to_video")
