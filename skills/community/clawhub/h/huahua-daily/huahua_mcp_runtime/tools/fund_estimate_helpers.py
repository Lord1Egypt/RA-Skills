"""Estimate validation helpers shared by fund MCP tools."""

import math

from ..estimate_frame_contract import (
    CURRENT_ESTIMATE_SOURCES,
    estimate_frame_available,
)

from ..validation import (
    DATA_SOURCE_MODES,
    LEGACY_DATA_SOURCE_MODES,
    normalize_data_source_mode,
)

_HISTORICAL_ESTIMATE_SOURCES = CURRENT_ESTIMATE_SOURCES - {
    "estimate_official_confirmation",
    "huahua",
    "huahua_estimate",
    "official_published",
    "realtime",
    "sina_official_current",
}


def normalized_calibration_evidence(item: object) -> dict | None:
    """Project daytime/night calibration fields into one public shape.

    Daytime P5 frames keep the model audit in ``breakdown`` using snake-case,
    while night holdings frames expose the same facts at item level using
    camel-case.  Public MCP consumers should not have to know which serving
    path produced the frame.
    """

    if not isinstance(item, dict):
        return None
    breakdown = item.get("breakdown")
    breakdown = breakdown if isinstance(breakdown, dict) else {}

    reason = item.get("calibrationReason")
    if reason is None:
        reason = item.get("calibration_reason")
    if reason is None:
        reason = breakdown.get("calibrationReason")
    if reason is None:
        reason = breakdown.get("calibration_reason")

    weight = item.get("calibrationWeight")
    if weight is None:
        weight = item.get("calibration_weight")
    if weight is None:
        weight = breakdown.get("calibrationWeight")
    if weight is None:
        weight = breakdown.get("calibration_weight")

    model_version = item.get("calibrationModelVersion")
    if model_version is None:
        model_version = item.get("calibration_model_version")
    if model_version is None:
        model_version = breakdown.get("calibrationModelVersion")
    if model_version is None:
        model_version = breakdown.get("calibration_model_version")

    applied = item.get("calibrated")
    if applied is None:
        applied = breakdown.get("calibrated")

    # Index-direct night estimates deliberately have ``calibrated=false`` but
    # no holdings model.  Do not manufacture an unknown model record for them.
    if reason is None and weight is None and model_version is None and applied is not True:
        return None
    return {
        "applied": applied is True,
        "reason": str(reason) if reason is not None else None,
        "weight": weight,
        "modelVersion": (
            str(model_version) if model_version is not None else None
        ),
    }


def normalized_fx_status(item: object) -> str | None:
    """Return the stable FX disposition without making FX a serving gate."""

    if not isinstance(item, dict):
        return None
    breakdown = item.get("breakdown")
    breakdown = breakdown if isinstance(breakdown, dict) else {}
    status = item.get("fxStatus") or item.get("fx_status")
    if status is None:
        status = breakdown.get("fxStatus") or breakdown.get("fx_status")
    normalized = str(status or "").strip().lower()
    aliases = {
        "applied": "applied",
        "complete": "complete",
        "not_required": "not_required",
        "omitted": "omitted",
        "missing": "omitted",
    }
    if normalized in aliases:
        return aliases[normalized]
    reason = str(item.get("reason") or "").strip().lower()
    if breakdown.get("fx_degraded") is True or reason in {
        "fx_missing",
        "fx_omitted",
    }:
        return "omitted"
    return None


def estimate_evidence_summary(item: dict) -> dict:
    """Normalize estimate quality without hiding the backend provenance."""

    if not isinstance(item, dict):
        return {
            "status": None,
            "partial": False,
            "evidenceComplete": False,
            "coverage": None,
            "proxyCoverage": None,
            "fxDegraded": False,
        }
    decision = item.get("estimateDecision")
    decision = decision if isinstance(decision, dict) else {}
    breakdown = item.get("breakdown")
    breakdown = breakdown if isinstance(breakdown, dict) else {}
    status = str(decision.get("status") or "").strip().lower() or None
    coverage = decision.get("coverage")
    if coverage is None:
        coverage = breakdown.get("coverage")
    proxy_coverage = breakdown.get("proxy_coverage")
    proxy_coverage = (
        dict(proxy_coverage)
        if isinstance(proxy_coverage, dict)
        else None
    )
    fx_status = normalized_fx_status(item)
    fx_degraded = bool(
        breakdown.get("fx_degraded") is True
        or fx_status == "omitted"
    )
    calibration = normalized_calibration_evidence(item)
    proxy_incomplete = bool(
        proxy_coverage is not None
        and proxy_coverage.get("complete") is not True
    )
    partial = bool(
        status == "partial"
        or proxy_incomplete
        or fx_degraded
        or breakdown.get("serving_degraded") is True
        or str(item.get("availability") or "").strip().lower() == "partial"
    )
    available = estimate_frame_available(item)
    return {
        "status": status,
        "partial": partial,
        "evidenceComplete": bool(
            available
            and status != "unavailable"
            and not partial
        ),
        "coverage": coverage,
        "proxyCoverage": proxy_coverage,
        "fxDegraded": fx_degraded,
        **({"fxStatus": fx_status} if fx_status is not None else {}),
        **({"calibration": calibration} if calibration is not None else {}),
    }


def estimate_index_audit_evidence(decision: dict) -> dict:
    """Keep typed index identity and fallback evidence for MCP diagnostics."""

    if not isinstance(decision, dict):
        return {}
    return {
        key: decision.get(key)
        for key in (
            "instrumentType", "canonicalIndexId", "trackedIndexName",
            "officialIndexName", "officialIndexCode", "market",
            "quoteProvider", "quoteDate", "targetNavDate", "sourceKind",
            "fallbackReason", "fallbackTargetCode", "fallbackRelation",
        )
        if decision.get(key) is not None
    }


def estimate_audit_payload(estimate: dict, requested_mode: str) -> dict:
    """Normalize portfolio estimate provenance, quality and index evidence."""

    decision = estimate.get("estimateDecision")
    decision = decision if isinstance(decision, dict) else {}
    selection = estimate.get("dataSourceSelection")
    selection = selection if isinstance(selection, dict) else {}
    fallback = decision.get("fallback")
    fallback = fallback if isinstance(fallback, dict) else None
    evidence = estimate_evidence_summary(estimate)
    return {
        "preference": decision.get("preference")
        or estimate.get("dataSourceMode")
        or requested_mode,
        "provider": decision.get("provider"),
        "engine": decision.get("engine"),
        "status": decision.get("status"),
        "reason": decision.get("reason"),
        "coverage": evidence.get("coverage"),
        "proxyCoverage": evidence.get("proxyCoverage"),
        "fxDegraded": evidence.get("fxDegraded") is True,
        **(
            {"fxStatus": evidence.get("fxStatus")}
            if evidence.get("fxStatus") is not None
            else {}
        ),
        **(
            {"calibration": evidence.get("calibration")}
            if isinstance(evidence.get("calibration"), dict)
            else {}
        ),
        "partial": evidence.get("partial") is True,
        "evidenceComplete": evidence.get("evidenceComplete") is True,
        "fallback": fallback,
        "usedProvider": selection.get("usedProvider"),
        "fellBackToHuahua": selection.get("fellBackToHuahua") is True,
        "policyRevision": decision.get("policyRevision")
        or estimate.get("policyRevision"),
        **estimate_index_audit_evidence(decision),
    }


def sanitize_estimate_frame(item):
    """Never expose obsolete calculation details as a usable current frame."""

    if not isinstance(item, dict):
        return item
    sanitized = dict(item)
    fx_status = normalized_fx_status(sanitized)
    calibration = normalized_calibration_evidence(sanitized)
    if fx_status is not None:
        sanitized["fxStatus"] = fx_status
    if calibration is not None:
        sanitized["calibration"] = calibration
    if not estimate_frame_available(sanitized):
        sanitized.pop("breakdown", None)
        sanitized.pop("_breakdown_payload", None)
        sanitized["estimatedNav"] = None
        sanitized["estimatedChangePercent"] = None
        if "gsz" in sanitized:
            sanitized["gsz"] = ""
        if "gszzl" in sanitized:
            sanitized["gszzl"] = ""
        if "marketPriceChangePercent" in sanitized:
            sanitized["marketPriceChangePercent"] = None
    return sanitized


def sanitize_source_preview_payload(payload):
    if not isinstance(payload, dict):
        return payload
    data = payload.get("data")
    if not isinstance(data, dict):
        return payload
    sanitized_data = {}
    for mode, raw_item in data.items():
        if not isinstance(raw_item, dict):
            continue
        item = sanitize_estimate_frame(raw_item)
        snapshot = item.get("last_estimate_snap")
        if isinstance(snapshot, dict):
            source = str(snapshot.get("source") or "")
            date = str(snapshot.get("date") or "")[:10]
            display_date = str(item.get("display_date") or "")[:10]
            decision = snapshot.get("estimateDecision")
            nav = snapshot.get("nav")
            change = snapshot.get("change")
            try:
                nav_value = float(nav)
                change_value = float(change)
            except (TypeError, ValueError):
                nav_value = float("nan")
                change_value = float("nan")
            snapshot_unavailable = (
                isinstance(decision, dict)
                and str(decision.get("status") or "").lower() == "unavailable"
            )
            if (
                source not in _HISTORICAL_ESTIMATE_SOURCES
                or not date
                or (display_date and date != display_date)
                or not math.isfinite(nav_value)
                or nav_value <= 0
                or not math.isfinite(change_value)
                or snapshot_unavailable
            ):
                item.pop("last_estimate_snap", None)
        sanitized_data[mode] = item
    return {**payload, "data": sanitized_data}


def validate_public_data_source_mode(value, field: str) -> str:
    normalized = str(value or "").strip().lower()
    if (
        normalized not in DATA_SOURCE_MODES
        and normalized not in LEGACY_DATA_SOURCE_MODES
    ):
        raise ValueError(f"{field} 仅支持 source_a、source_b 或 huahua")
    return normalize_data_source_mode(normalized)
