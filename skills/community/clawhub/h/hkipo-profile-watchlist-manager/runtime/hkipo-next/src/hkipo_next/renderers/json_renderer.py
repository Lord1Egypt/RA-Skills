"""JSON rendering helpers."""

from __future__ import annotations

import json

from pydantic import BaseModel


def render_model_as_json(model: BaseModel) -> str:
    return json.dumps(
        model.model_dump(mode="json"),
        ensure_ascii=False,
        indent=2,
    )
