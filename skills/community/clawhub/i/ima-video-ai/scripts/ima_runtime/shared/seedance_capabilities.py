from __future__ import annotations

SEEDANCE_MODEL_IDS = {"ima-pro", "ima-pro-fast"}

SEEDANCE_MEDIA_CAPABILITIES = {
    "ima-pro": {
        "image_to_video": {"compliance_required": True, "supported_media": {"image"}},
        "first_last_frame_to_video": {"compliance_required": True, "supported_media": {"image"}},
        "reference_image_to_video": {
            "compliance_required": True,
            "supported_media": {"image", "video", "audio"},
            "catalog_form_fields": {"audio", "duration", "aspect_ratio", "resolution"},
        },
    },
    "ima-pro-fast": {
        "image_to_video": {"compliance_required": True, "supported_media": {"image"}},
        "first_last_frame_to_video": {"compliance_required": True, "supported_media": {"image"}},
        "reference_image_to_video": {
            "compliance_required": True,
            "supported_media": {"image", "video", "audio"},
            "catalog_form_fields": {"audio", "duration", "aspect_ratio", "resolution"},
        },
    },
}


def is_seedance_model(model_id: str | None) -> bool:
    return bool(model_id in SEEDANCE_MODEL_IDS)


def requires_seedance_compliance(task_type: str, model_id: str | None) -> bool:
    if not is_seedance_model(model_id):
        return False
    capability = SEEDANCE_MEDIA_CAPABILITIES.get(model_id, {}).get(task_type, {})
    return bool(capability.get("compliance_required"))


def supported_seedance_media(task_type: str, model_id: str | None) -> set[str]:
    if not is_seedance_model(model_id):
        return set()
    capability = SEEDANCE_MEDIA_CAPABILITIES.get(model_id, {}).get(task_type, {})
    return set(capability.get("supported_media", set()))
