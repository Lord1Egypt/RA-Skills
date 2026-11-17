"""Named review-dimension blueprint sets (审查维度集).

Addresses a design gap in onboarding: historically the wizard only preset a
single global ``dimensions`` list, so a later user request scoped to a specific
area (e.g. "review the frontend", "audit the API layer") would still fall back
to that one global set. This module introduces ``dimension_sets`` — named
presets, each bundling a subset of dimensions plus optional per-dimension focus
overrides — so onboarding can pre-provision several scope-specific blueprints
and the runtime can route a scoped goal to the matching set.

A set entry has the shape::

    "<name>":
      dimensions: [correctness, security, ...]   # <= canonical dims
      focus:                                      # optional
        "<dimension>": "extra focus text for this scope"

The global ``dimensions`` list remains the default for whole-project/full review;
``dimension_sets`` are additive overrides keyed by named scope.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from iterate_cli.scan import ScanResult

# Canonical dimension ids (single source of truth; kept in sync by
# tests/test_dimension_lock.py and scripts/validate.py). Referencing this here
# (rather than importing from iterate_cli.doctor) avoids a circular import while
# staying the same value set the schema enum locks.
CANONICAL_DIMENSIONS: tuple[str, ...] = (
    "correctness",
    "security",
    "performance",
    "architecture",
    "style-tests",
    "tech-debt",
    "spec-compliance",
    "frontend-backend",
    "ui-ux",
)

# Named presets offered during onboarding, keyed by scope name. ``dims`` are
# the base dimension keys for that scope. The scanner prunes these by what the
# project actually contains (see ``suggest_dimension_sets``).
DIMENSION_SET_CATALOG: dict[str, dict[str, Any]] = {
    "frontend": {
        "dimensions": ["ui-ux", "frontend-backend", "performance", "correctness"],
    },
    "api": {
        "dimensions": ["security", "architecture", "frontend-backend", "correctness"],
    },
    "security": {
        "dimensions": ["security", "correctness", "architecture"],
    },
    "performance": {
        "dimensions": ["performance", "architecture", "correctness"],
    },
    "style-tests": {
        "dimensions": ["style-tests", "correctness", "tech-debt"],
    },
}

# Scope-name charset (safe for use as an ITERATE.md anchor / config key).
_SCOPE_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

# Focus override shape: an optional mapping dimension -> free text.
DIMENSION_SET_STRUCT_DESC = "dimension_sets.<name> must map to {dimensions: [...], focus?: {...}}"


def is_valid_set_name(name: str) -> bool:
    """Return True when ``name`` is usable as a dimension-set key.

    Restricts scope names to alphanumerics/underscore/dot/dash so a user-supplied
    name can never smuggle TOC-breaking or injection characters into either the
    config key or an ITERATE.md anchor.
    """
    return bool(_SCOPE_NAME_RE.match(name))


def _normalize_set(
    raw: Any, on_drop_dimension: Callable[[str], None] | None = None
) -> dict[str, Any] | None:
    """Normalize a raw dimension-set value to ``{dimensions, focus}``.

    Returns None when the shape is invalid. Focus overrides are kept only for
    dimensions actually present in that set's ``dimensions``, so a stale focus
    key can never reference a disabled dimension. Non-canonical dimension ids
    are dropped; ``on_drop_dimension`` (when given) is called with each so a
    caller that writes the result back can announce the loss.
    """
    if not isinstance(raw, dict):
        return None

    dims_raw = raw.get("dimensions")
    if not isinstance(dims_raw, list) or not dims_raw:
        return None
    if not all(isinstance(d, str) for d in dims_raw):
        return None
    dims = []
    for d in dims_raw:
        if d in CANONICAL_DIMENSIONS:
            dims.append(d)
        elif on_drop_dimension is not None:
            on_drop_dimension(d)
    if not dims:
        return None

    # Deduplicate while preserving order (schema requires uniqueItems).
    seen: set[str] = set()
    dims_out: list[str] = []
    for d in dims:
        if d not in seen:
            seen.add(d)
            dims_out.append(d)

    focus_raw = raw.get("focus") or {}
    focus: dict[str, str] = {}
    if isinstance(focus_raw, dict):
        for dim, text in focus_raw.items():
            # Guard `isinstance(dim, str)` first: `dim in seen` on an
            # unhashable YAML key (e.g. a sequence) would raise TypeError
            # instead of dropping the malformed entry.
            if isinstance(dim, str) and dim in seen and isinstance(text, str) and text.strip():
                focus[dim] = text.strip()

    return {"dimensions": dims_out, **({"focus": focus} if focus else {})}


def normalize_dimension_sets(
    raw: Any,
    on_drop: Callable[[str], None] | None = None,
    on_drop_dimension: Callable[[str, str], None] | None = None,
) -> dict[str, dict[str, Any]]:
    """Normalize an arbitrary dimension_sets value to a clean ``{name: {...}}`` map.

    Malformed entries are dropped (rather than raising) so a hand-edited config
    degrades gracefully while valid entries are preserved.

    Args:
        raw: The raw ``dimension_sets`` value from a config.
        on_drop: Optional callback invoked with each dropped set name. Callers
            that WRITE the normalized result back to disk (refresh) MUST pass
            this (e.g. ``tui.warning``) — silently deleting a hand-written
            entry on the next ``iterate refresh`` with exit 0 and no output
            was data loss the operator never saw. Read-only callers may omit it.
        on_drop_dimension: Optional callback invoked with ``(set_name,
            dimension)`` for each non-canonical dimension id dropped from a set.
            Without it, a dropped dimension is reported through ``on_drop``
            (so a writing caller still announces the loss).

    Returns:
        Ordered mapping of scope-name -> normalized set spec.
    """
    if not isinstance(raw, dict):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for name, raw_set in raw.items():
        if not isinstance(name, str) or not is_valid_set_name(name):
            if on_drop is not None:
                on_drop(str(name))
            continue

        def _report_dimension(
            dimension: str, _name: str = name,
        ) -> None:
            if on_drop_dimension is not None:
                on_drop_dimension(_name, dimension)
            elif on_drop is not None:
                on_drop(f"{_name}.dimensions: {dimension}")

        normalized = _normalize_set(raw_set, on_drop_dimension=_report_dimension)
        if normalized is not None:
            out[name] = normalized
        elif on_drop is not None:
            on_drop(name)
    return out


def suggest_dimension_sets(scan: ScanResult) -> dict[str, dict[str, Any]]:
    """Suggest scope-specific dimension sets based on scan results.

    Prunes the fixed catalog by what the project actually contains. The caller
    (wizard) lets the user confirm/adjust the enabled sets.

    Returns:
        Ordered mapping of scope-name -> normalized set spec. Always includes
        the ``security``, ``performance`` and ``style-tests`` cross-cutting
        audits regardless of stack; layer-specific sets are added only when
        detected.
    """
    from iterate_cli.scan import _has_api_layer

    # Seed EMPTY (not with the full catalog): the `if name not in catalog`
    # checks below were always False when seeded from DIMENSION_SET_CATALOG,
    # making those branches dead code whose "correct" behaviour depended on
    # this initialization detail. Seeding empty makes the add/prune logic
    # honest in both directions.
    catalog: dict[str, dict[str, Any]] = {}

    if scan.has_frontend:
        catalog["frontend"] = {"dimensions": list(DIMENSION_SET_CATALOG["frontend"]["dimensions"])}
    # (No prune needed: an empty seed means "frontend" is only present when
    # just added above.)

    if _has_api_layer(scan):
        catalog["api"] = {"dimensions": list(DIMENSION_SET_CATALOG["api"]["dimensions"])}

    # Cross-cutting audits always offered.
    for name in ("security", "performance", "style-tests"):
        catalog.setdefault(name, {"dimensions": list(DIMENSION_SET_CATALOG[name]["dimensions"])})

    return catalog


def merge_dimension_sets(
    existing: dict[str, dict[str, Any]],
    suggested: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Merge suggested sets into existing, preserving user customisation.

    Existing user sets win (never overwritten by a suggestion); only sets that
    are absent are defaulted from the scan suggestion. Used by refresh so a
    newly-detected layer (e.g. frontend added after onboarding) gets its preset
    without clobbering a manually-configured one.
    """
    out = {name: dict(spec) for name, spec in existing.items()}
    for name, spec in suggested.items():
        out.setdefault(name, dict(spec))
    return out