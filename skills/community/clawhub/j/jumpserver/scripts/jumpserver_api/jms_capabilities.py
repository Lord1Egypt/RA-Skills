from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .jms_types import JumpServerAPIError


@dataclass(frozen=True)
class CapabilitySpec:
    capability_id: str
    name: str
    category: str
    priority: str
    entrypoint: str
    handler: str
    trigger_description: str
    examples: tuple[str, ...]
    endpoints: tuple[str, ...]
    scripts: tuple[str, ...]
    input_params: tuple[str, ...]
    summary_strategy: str
    error_handling: str
    coverage: str


def metadata_root() -> Path:
    return Path(__file__).resolve().parents[2] / "references" / "metadata"


def metadata_path(filename: str) -> Path:
    return metadata_root() / filename


def _read_json_file(filename: str):
    path = metadata_path(filename)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise JumpServerAPIError("Metadata json file not found: %s" % path) from exc
    except json.JSONDecodeError as exc:
        raise JumpServerAPIError(
            "Invalid json metadata file: %s" % path,
            details="line=%s column=%s: %s" % (exc.lineno, exc.colno, exc.msg),
        ) from exc


@lru_cache(maxsize=None)
def load_capability_metadata() -> list[dict[str, object]]:
    payload = _read_json_file("capabilities.json")
    if not isinstance(payload, list):
        raise JumpServerAPIError(
            "Capability metadata must be a json array: %s" % metadata_path("capabilities.json")
        )
    items: list[dict[str, object]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise JumpServerAPIError(
                "Capability metadata item must be a mapping: index=%s" % index
            )
        items.append(item)
    return items

def _coerce_sequence(raw: dict[str, object], field_name: str, capability_id: str) -> tuple[str, ...]:
    value = raw.get(field_name)
    if not isinstance(value, list):
        raise JumpServerAPIError(
            "Capability metadata field must be a json array: capability_id=%s field=%s"
            % (capability_id, field_name)
        )
    return tuple(str(item) for item in value)


def _coerce_scalar(raw: dict[str, object], field_name: str, capability_id: str) -> str:
    value = raw.get(field_name)
    if value is None:
        raise JumpServerAPIError(
            "Capability metadata missing required field: capability_id=%s field=%s"
            % (capability_id, field_name)
        )
    return str(value)


def _build_capability(raw: dict[str, object]) -> CapabilitySpec:
    capability_id = _coerce_scalar(raw, "capability_id", "<unknown>")
    return CapabilitySpec(
        capability_id=capability_id,
        name=_coerce_scalar(raw, "name", capability_id),
        category=_coerce_scalar(raw, "category", capability_id),
        priority=_coerce_scalar(raw, "priority", capability_id),
        entrypoint=_coerce_scalar(raw, "entrypoint", capability_id),
        handler=_coerce_scalar(raw, "handler", capability_id),
        trigger_description=_coerce_scalar(raw, "trigger_description", capability_id),
        examples=_coerce_sequence(raw, "examples", capability_id),
        endpoints=_coerce_sequence(raw, "endpoints", capability_id),
        scripts=_coerce_sequence(raw, "scripts", capability_id),
        input_params=_coerce_sequence(raw, "input_params", capability_id),
        summary_strategy=_coerce_scalar(raw, "summary_strategy", capability_id),
        error_handling=_coerce_scalar(raw, "error_handling", capability_id),
        coverage=_coerce_scalar(raw, "coverage", capability_id),
    )


def _load_capabilities() -> tuple[CapabilitySpec, ...]:
    records = []
    seen_ids = set()
    for raw in load_capability_metadata():
        spec = _build_capability(raw)
        if spec.capability_id in seen_ids:
            raise JumpServerAPIError(
                "Duplicate capability_id in metadata: %s" % spec.capability_id
            )
        seen_ids.add(spec.capability_id)
        records.append(spec)
    return tuple(records)


CAPABILITIES = _load_capabilities()
CAPABILITY_BY_ID = {item.capability_id: item for item in CAPABILITIES}
