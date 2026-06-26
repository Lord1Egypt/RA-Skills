"""Routing helpers for STT, model providers, and output modules."""

from __future__ import annotations

import platform


VALID_STT_PROFILES = {"mac_local_first", "local_cli_then_remote", "remote_only"}
VALID_MODEL_PROFILES = {"openai_direct", "aihubmix_gateway"}
VALID_OUTPUTS = {"telegram", "feishu"}


def resolve_stt_profile(raw_value: str, *, local_command: str = "", system_name: str | None = None) -> str:
    normalized = str(raw_value or "").strip().lower()
    if normalized in VALID_STT_PROFILES:
        return normalized
    actual_system = (system_name or platform.system()).strip()
    if actual_system == "Darwin":
        return "mac_local_first"
    if str(local_command or "").strip():
        return "local_cli_then_remote"
    return "remote_only"


def resolve_model_profile(raw_value: str) -> str:
    normalized = str(raw_value or "").strip().lower()
    if normalized in VALID_MODEL_PROFILES:
        return normalized
    return "aihubmix_gateway"


def parse_outputs(raw_value: str) -> tuple[str, ...]:
    values = []
    seen = set()
    for item in str(raw_value or "").split(","):
        normalized = item.strip().lower()
        if not normalized or normalized not in VALID_OUTPUTS or normalized in seen:
            continue
        seen.add(normalized)
        values.append(normalized)
    return tuple(values)

