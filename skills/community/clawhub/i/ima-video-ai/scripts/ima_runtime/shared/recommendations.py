from __future__ import annotations

from dataclasses import dataclass

from ima_runtime.shared.catalog import normalize_model_id
from ima_runtime.shared.errors import to_user_facing_model_name

TASK_TYPE_RECOMMENDATIONS = {
    "text_to_video": {
        "recommended_models": (
            {
                "model_id": "ima-pro-fast",
                "display_name": "Seedance 2.0 Fast",
                "note": "no-subscription recommendation",
            },
            {
                "model_id": "wan2.6-t2v",
                "display_name": "wan2.6-t2v",
                "note": "stable alternative",
            },
        ),
        "premium_models": (
            {"model_id": "ima-pro", "display_name": "Seedance 2.0"},
        ),
    },
    "image_to_video": {
        "recommended_models": (
            {
                "model_id": "ima-pro-fast",
                "display_name": "Seedance 2.0 Fast",
                "note": "no-subscription recommendation",
            },
            {
                "model_id": "wan2.6-i2v",
                "display_name": "wan2.6-i2v",
                "note": "stable alternative",
            },
        ),
        "premium_models": (
            {"model_id": "ima-pro", "display_name": "Seedance 2.0"},
        ),
    },
    "reference_image_to_video": {
        "recommended_models": (
            {
                "model_id": "kling-video-o1",
                "display_name": "kling-video-o1",
                "note": "recommended",
            },
            {
                "model_id": "ima-pro-fast",
                "display_name": "Seedance 2.0 Fast",
                "note": "second choice; no-subscription recommendation",
            },
        ),
        "premium_models": (
            {"model_id": "ima-pro", "display_name": "Seedance 2.0"},
        ),
    },
    "first_last_frame_to_video": {
        "recommended_models": (
            {
                "model_id": "kling-video-o1",
                "display_name": "kling-video-o1",
                "note": "recommended",
            },
            {
                "model_id": "ima-pro-fast",
                "display_name": "Seedance 2.0 Fast",
                "note": "second choice; no-subscription recommendation",
            },
        ),
        "premium_models": (
            {"model_id": "ima-pro", "display_name": "Seedance 2.0"},
        ),
    },
}


@dataclass(frozen=True)
class SuggestedModelChoice:
    model: dict | None
    is_catalog_recommended: bool


def get_task_type_recommendation_metadata(task_type: str) -> dict[str, tuple[dict[str, str], ...]]:
    return TASK_TYPE_RECOMMENDATIONS.get(
        task_type,
        {"recommended_models": (), "premium_models": ()},
    )


def catalog_model_lookup(models: list[dict]) -> dict[str, str]:
    available_models: dict[str, str] = {}
    for model in models:
        canonical_model_id = normalize_model_id(model.get("model_id")) or model.get("model_id")
        if not canonical_model_id or canonical_model_id in available_models:
            continue
        available_models[canonical_model_id] = to_user_facing_model_name(
            model.get("name"),
            canonical_model_id,
        )
    return available_models


def format_recommendation_entry(recommendation: dict[str, str], available_models: dict[str, str]) -> str:
    model_id = recommendation["model_id"]
    display_name = recommendation["display_name"]
    note = recommendation.get("note")
    parts = []
    if model_id != display_name:
        parts.append(f"{display_name} ({model_id})")
    else:
        parts.append(display_name)

    catalog_display_name = available_models.get(model_id)
    if catalog_display_name and catalog_display_name not in {display_name, model_id}:
        parts.append(f"catalog label: {catalog_display_name}")

    if note:
        parts.append(note)

    return " - ".join(parts)


def build_recommendation_lines(task_type: str, models: list[dict]) -> list[str]:
    metadata = get_task_type_recommendation_metadata(task_type)
    available_models = catalog_model_lookup(models)
    lines = [f"Recommended for {task_type}:"]

    if metadata["recommended_models"]:
        for recommendation in metadata["recommended_models"]:
            lines.append(f"- {format_recommendation_entry(recommendation, available_models)}")
    elif available_models:
        for model_id, display_name in list(available_models.items())[:3]:
            if display_name and display_name != model_id:
                lines.append(f"- {display_name} ({model_id})")
            else:
                lines.append(f"- {model_id}")
    else:
        lines.append("- No catalog models were returned for this task type.")

    for premium_model in metadata["premium_models"]:
        premium_model_id = premium_model["model_id"]
        premium_display_name = premium_model["display_name"]
        lines.append(
            f"Premium note: {premium_display_name} (--model-id {premium_model_id}) "
            "requires an active subscription plan."
        )

    return lines


def resolve_suggested_model(task_type: str, models: list[dict]) -> SuggestedModelChoice:
    metadata = get_task_type_recommendation_metadata(task_type)
    models_by_id: dict[str, dict] = {}
    for model in models:
        canonical_model_id = normalize_model_id(model.get("model_id")) or model.get("model_id")
        if canonical_model_id and canonical_model_id not in models_by_id:
            models_by_id[canonical_model_id] = model

    for recommendation in metadata["recommended_models"]:
        preferred = models_by_id.get(recommendation["model_id"])
        if preferred:
            return SuggestedModelChoice(model=preferred, is_catalog_recommended=True)

    return SuggestedModelChoice(model=models[0] if models else None, is_catalog_recommended=False)


def pick_recommended_model(task_type: str, models: list[dict]) -> dict | None:
    return resolve_suggested_model(task_type, models).model
