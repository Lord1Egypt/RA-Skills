#!/usr/bin/env python3
"""Runtime config normalization for the paper review mainline."""

from __future__ import annotations

from typing import Dict

from job_defaults import create_job_config


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "no", "off", ""}
    return bool(value)


def normalize_runtime_config(config: Dict) -> Dict:
    """Normalize config into the single supported runtime contract.

    refs:
    - refs: current review stage refs
    - styleProfileRefs: full style-learning refs
    """
    job = create_job_config(config)
    stage = config.get("stage") or config.get("stageProfile") or "stage1"

    active_refs = []
    for ref in job.get_active_refs(stage):
        ref_path = ref.get("path") or ref.get("pathPlaceholder")
        if not ref_path:
            continue
        normalized = dict(ref)
        normalized["path"] = ref_path
        active_refs.append(normalized)

    style_profile_refs = []
    for ref in job.get_style_profile_refs():
        ref_path = ref.get("path") or ref.get("pathPlaceholder")
        if not ref_path:
            continue
        normalized = dict(ref)
        normalized["path"] = ref_path
        style_profile_refs.append(normalized)

    target_path = (
        config.get("target", {}).get("path")
        or job.targetPath
        or job.defaultTarget.get("path")
        or job.defaultTarget.get("pathPlaceholder")
    )
    if not target_path:
        raise ValueError("missing target.path after config normalization")

    output_dir = config.get("outputDir") or job.outputDir or "outputs"
    enabled_checks = {
        "format": _as_bool(job.formatCheck.enabled),
        "terminology": _as_bool(job.termValidation.enabled),
        "style": True,
        "logic": True,
    }
    raw_enabled_checks = dict(job.enabledChecks or {})
    alias_map = {
        "formatCheck": "format",
        "format": "format",
        "termValidation": "terminology",
        "terminology": "terminology",
        "styleDeviation": "style",
        "styleImitation": "style",
        "style": "style",
        "logicCoherence": "logic",
        "logic": "logic",
    }
    for raw_key, value in raw_enabled_checks.items():
        canonical = alias_map.get(str(raw_key))
        if canonical:
            enabled_checks[canonical] = _as_bool(value)

    return {
        **config,
        "target": {**config.get("target", {}), "path": target_path},
        "refs": active_refs,
        "styleProfileRefs": style_profile_refs,
        "outputDir": output_dir,
        "stage": stage,
        "enabledChecks": enabled_checks,
    }
