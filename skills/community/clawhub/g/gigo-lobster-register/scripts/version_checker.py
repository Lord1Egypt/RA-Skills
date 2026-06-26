from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class VersionCheckResult:
    local_version: str
    latest_stable: str | None
    latest_beta: str | None
    rollback_recommended: str | None
    blocked_versions: list[str]
    update_available: bool
    is_blocked: bool
    release_notes: str | None = None
    error: str | None = None


def load_local_version(repo_root: Path) -> str:
    version_path = repo_root / "VERSION"
    if version_path.exists():
        version = version_path.read_text(encoding="utf-8").strip()
        if version:
            return version

    manifest_path = repo_root / "manifest.json"
    if manifest_path.exists():
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        version = str(payload.get("version", "")).strip()
        if version:
            return version

    return "0.0.0"


def _parse_release(value: str) -> tuple[list[int], list[str]]:
    main, _, prerelease = value.partition("-")
    numeric_parts = [int(part) for part in main.split(".") if part.isdigit()]
    prerelease_parts = [part for part in re.split(r"[.\-]", prerelease) if part]
    return numeric_parts, prerelease_parts


def compare_versions(left: str, right: str) -> int:
    left_main, left_pre = _parse_release(left)
    right_main, right_pre = _parse_release(right)
    max_len = max(len(left_main), len(right_main))

    for index in range(max_len):
        left_value = left_main[index] if index < len(left_main) else 0
        right_value = right_main[index] if index < len(right_main) else 0
        if left_value != right_value:
            return 1 if left_value > right_value else -1

    if not left_pre and not right_pre:
        return 0
    if not left_pre:
        return 1
    if not right_pre:
        return -1

    max_pre_len = max(len(left_pre), len(right_pre))
    for index in range(max_pre_len):
        if index >= len(left_pre):
            return -1
        if index >= len(right_pre):
            return 1

        left_value = left_pre[index]
        right_value = right_pre[index]
        if left_value == right_value:
            continue

        if left_value.isdigit() and right_value.isdigit():
            return 1 if int(left_value) > int(right_value) else -1
        if left_value.isdigit():
            return -1
        if right_value.isdigit():
            return 1
        return 1 if left_value > right_value else -1

    return 0


def check_skill_version(config: dict[str, Any], repo_root: Path, offline: bool = False) -> VersionCheckResult:
    local_version = load_local_version(repo_root)
    result = VersionCheckResult(
        local_version=local_version,
        latest_stable=None,
        latest_beta=None,
        rollback_recommended=None,
        blocked_versions=[],
        update_available=False,
        is_blocked=False,
    )
    if offline:
        result.error = "offline_mode"
        return result

    url = f"{config['api_base'].rstrip('/')}/api/versions"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        result.error = str(error)
        return result

    latest_stable = payload.get("latest_stable")
    blocked_versions = [str(item) for item in payload.get("blocked_versions", [])]
    versions = payload.get("versions") or []
    latest_entry = next(
        (entry for entry in versions if entry.get("version") == latest_stable),
        None,
    )

    result.latest_stable = latest_stable
    result.latest_beta = payload.get("latest_beta")
    result.rollback_recommended = payload.get("rollback_recommended")
    result.blocked_versions = blocked_versions
    result.is_blocked = local_version in blocked_versions
    result.update_available = bool(latest_stable and compare_versions(latest_stable, local_version) > 0)
    result.release_notes = latest_entry.get("release_notes") if latest_entry else None
    return result
