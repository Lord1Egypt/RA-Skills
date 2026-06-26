"""Schema normalization helpers for memory-guardian."""

import json
from copy import deepcopy

from .meta_defaults import (
    DEFAULT_DECAY_CONFIG,
    DEFAULT_QUALITY_GATE_STATE,
    SCHEMA_VERSION,
    PRODUCT_VERSION,
    MEMORY_DEFAULTS,
)

# Backward compatibility aliases
DEFAULT_SCHEMA_VERSION = f"v{SCHEMA_VERSION}" if not SCHEMA_VERSION.startswith("v") else SCHEMA_VERSION
DEFAULT_VERSION = SCHEMA_VERSION


def _deep_merge_defaults(target, defaults):
    """Merge defaults into target dict in-place. Returns (target, changed)."""
    changed = False
    for key, value in defaults.items():
        if key not in target:
            target[key] = deepcopy(value)
            changed = True
        elif isinstance(target[key], dict) and isinstance(value, dict):
            _, nested_changed = _deep_merge_defaults(target[key], value)
            changed = changed or nested_changed
    return target, changed


def get_schema_version(meta):
    """Return the canonical schema version for the current code line."""
    _ = meta
    return DEFAULT_SCHEMA_VERSION


def ensure_decay_config(meta):
    """Ensure decay_config exists with canonical nested defaults."""
    decay_config = meta.setdefault("decay_config", {})
    before = json_fingerprint(decay_config)
    _deep_merge_defaults(decay_config, DEFAULT_DECAY_CONFIG)
    changed = before != json_fingerprint(decay_config)
    return decay_config, changed


def _json_fingerprint(obj):
    """Fast structural comparison via JSON serialization (avoids deepcopy)."""
    try:
        return json.dumps(obj, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError):
        return None


# Module-level alias for fingerprint function
json_fingerprint = _json_fingerprint
del _json_fingerprint


def normalize_meta(meta, read_only=False):
    """Normalize version, decay config, and quality gate aliases.

    Args:
        meta: The meta dict to normalize.
        read_only: If True, skip deepcopy (caller guarantees meta won't be mutated).
            Use this when meta is only inspected (e.g. memory_status) and discarded.

    Returns:
        (normalized_meta, changed) tuple.
    """
    if read_only:
        # Work on a shallow reference — caller won't persist mutations.
        # This avoids expensive deepcopy for read-only inspection paths.
        normalized = meta
        changed = False

        schema_version = get_schema_version(normalized)
        if normalized.get("schema_version") != schema_version:
            changed = True
        if normalized.get("version") != DEFAULT_VERSION:
            changed = True
        _, decay_changed = ensure_decay_config(normalized)
        changed = changed or decay_changed

        # Quick fingerprint check for quality gate (no deepcopy needed)
        qg_alias = normalized.get("quality_gate", {})
        qgs_alias = normalized.get("quality_gate_state", {})
        merged_gate = {**DEFAULT_QUALITY_GATE_STATE, **qg_alias, **qgs_alias}
        if normalized.get("quality_gate_state") != merged_gate:
            changed = True
        if normalized.get("quality_gate") != merged_gate:
            changed = True

        return normalized, changed

    # Write path: full deepcopy to avoid mutating caller's dict
    normalized = deepcopy(meta)
    changed = False

    schema_version = get_schema_version(normalized)
    if normalized.get("schema_version") != schema_version:
        normalized["schema_version"] = schema_version
        changed = True

    if normalized.get("version") != DEFAULT_VERSION:
        normalized["version"] = DEFAULT_VERSION
        changed = True

    _, decay_changed = ensure_decay_config(normalized)
    changed = changed or decay_changed

    qg_alias = normalized.get("quality_gate", {})
    qgs_alias = normalized.get("quality_gate_state", {})
    merged_gate = {**DEFAULT_QUALITY_GATE_STATE, **qg_alias, **qgs_alias}

    if normalized.get("quality_gate_state") != merged_gate:
        normalized["quality_gate_state"] = dict(merged_gate)
        changed = True
    if normalized.get("quality_gate") != merged_gate:
        normalized["quality_gate"] = dict(merged_gate)
        changed = True

    return normalized, changed
