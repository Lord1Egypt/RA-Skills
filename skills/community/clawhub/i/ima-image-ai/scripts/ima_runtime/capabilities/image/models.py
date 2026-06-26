from __future__ import annotations

from ima_runtime.shared.catalog import canonicalize_model_id, extract_model_params, find_model_version
from ima_runtime.shared.types import ModelBinding, ModelCandidate


def build_image_model_binding(product_tree: list, model_id: str, version_id: str | None = None) -> ModelBinding:
    normalized_model_id = canonicalize_model_id(model_id) or model_id
    node = find_model_version(product_tree, normalized_model_id, version_id)
    if node is None:
        raise RuntimeError(f"Image model not found: model_id={normalized_model_id}, version_id={version_id}")

    params = extract_model_params(node)
    return ModelBinding(
        candidate=ModelCandidate(
            name=params["model_name"],
            model_id=params["model_id"],
            version_id=params["model_version"],
        ),
        attribute_id=params["attribute_id"],
        credit=params["credit"],
        resolved_params=params,
    )
