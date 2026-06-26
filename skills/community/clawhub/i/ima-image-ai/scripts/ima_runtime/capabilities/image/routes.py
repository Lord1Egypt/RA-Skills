from __future__ import annotations

from ima_runtime.shared.inputs import validate_and_filter_inputs
from ima_runtime.shared.types import ClarificationRequest, GatewayRequest, TaskSpec

REFERENCE_HINTS = (
    "参考这张图",
    "把上一张图继续做",
    "保持同一个角色",
    "基于这张图改风格",
    "same character",
    "style transfer",
    "based on this image",
    "reference image",
)

def _build_task_spec(request: GatewayRequest, task_type: str) -> TaskSpec:
    input_images = tuple(validate_and_filter_inputs(task_type, list(request.input_images)))
    return TaskSpec(
        capability="image",
        task_type=task_type,
        prompt=request.prompt,
        input_images=input_images,
        extra_params=dict(request.extra_params),
    )


def _needs_reference_clarification(prompt: str, input_images: tuple[str, ...]) -> bool:
    if input_images:
        return False
    prompt_lower = prompt.lower()
    return any(hint in prompt or hint in prompt_lower for hint in REFERENCE_HINTS)


def build_image_task_spec(request: GatewayRequest) -> TaskSpec | ClarificationRequest:
    explicit_task_type = request.intent_hints.get("task_type")
    if explicit_task_type in ("text_to_image", "image_to_image"):
        return _build_task_spec(request, str(explicit_task_type))

    if _needs_reference_clarification(request.prompt or "", request.input_images):
        return ClarificationRequest(
            reason="missing reference image",
            question="你这次更像是图生图请求，请先上传要参考的图片，或者明确改成文生图。",
            options=("上传参考图", "改成文生图"),
        )

    if request.input_images:
        return _build_task_spec(request, "image_to_image")
    return _build_task_spec(request, "text_to_image")
