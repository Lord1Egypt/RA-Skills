"""Completeness contract for MCP night-estimate responses."""

import math

from .fund_estimate_helpers import (
    normalized_calibration_evidence as _normalized_calibration_evidence,
    normalized_fx_status as _normalized_fx_status,
)


def _safe_count(value, fallback: int) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return fallback


def _has_finite_night_change(item: dict) -> bool:
    value = item.get("estimatedChangePercent")
    if isinstance(value, bool) or value is None:
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _is_ready_night_item(item: dict) -> bool:
    result_state = item.get("resultState")
    return bool(
        item.get("usable") is not False
        and item.get("status") == "ready"
        and result_state in {None, "ready"}
        and _has_finite_night_change(item)
    )


def normalize_night_response(payload: object, requested_view: str) -> dict:
    """Add stable completeness semantics to the backend night envelope."""

    result = dict(payload) if isinstance(payload, dict) else {
        "status": "market_unavailable",
        "items": [],
    }
    items = []
    for raw_item in result.get("items", []):
        if not isinstance(raw_item, dict):
            continue
        item = dict(raw_item)
        if not item.get("freshness") and result.get("freshness"):
            item["freshness"] = result["freshness"]
        item["usable"] = _is_ready_night_item(item)
        item["changePercentUnit"] = "percentage_points"
        item["view"] = result.get("view") or requested_view
        item["forecastFlagMeaning"] = "synthetic_overnight_or_holiday_projection"
        item["estimateMode"] = item.get("estimateMode") or (result.get("market") or {}).get("phase")
        fx_status = _normalized_fx_status(item)
        calibration = _normalized_calibration_evidence(item)
        if fx_status is not None:
            item["fxStatus"] = fx_status
        if calibration is not None:
            item["calibration"] = calibration
        items.append(item)
    raw_meta = result.get("meta")
    meta = dict(raw_meta) if isinstance(raw_meta, dict) else {}
    response_view = str(result.get("view") or requested_view).strip().lower()
    if response_view not in {"forecast", "last_close"}:
        response_view = requested_view

    ready_items = [item for item in items if _is_ready_night_item(item)]
    pending_items = [item for item in items if not _is_ready_night_item(item)]
    stale_codes = [
        str(item.get("code"))
        for item in ready_items
        if item.get("freshness") == "stale" and item.get("code")
    ]
    poller_pending_codes = [
        str(item.get("code"))
        for item in pending_items
        if item.get("reason") == "poller_pending" and item.get("code")
    ]
    timeout_pending_codes = [
        str(item.get("code"))
        for item in pending_items
        if item.get("reason") == "request_timeout" and item.get("code")
    ]
    pending_reasons = {}
    for item in pending_items:
        reason = str(
            item.get("reason")
            or (
                "invalid_estimate_frame"
                if item.get("status") == "ready"
                else "unknown"
            )
        )
        pending_reasons[reason] = pending_reasons.get(reason, 0) + 1
    raw_pending_reasons = meta.get("pendingReasons")
    if isinstance(raw_pending_reasons, dict):
        for reason, raw_count in raw_pending_reasons.items():
            normalized_reason = str(reason or "unknown")
            pending_reasons[normalized_reason] = max(
                pending_reasons.get(normalized_reason, 0),
                _safe_count(raw_count, 0),
            )

    # Items are the authoritative evidence. Backend counters may only reveal
    # omitted rows or make completeness stricter; they must never turn an
    # observed pending/invalid item into a ready frame.
    requested_count = max(
        len(items),
        _safe_count(meta.get("requestedCount"), len(items)),
        _safe_count(meta.get("returnedCount"), len(items)),
    )
    returned_count = len(items)
    ready_count = len(ready_items)
    missing_count = max(0, requested_count - returned_count)
    pending_count = max(
        len(pending_items) + missing_count,
        _safe_count(meta.get("pendingCount"), 0),
        sum(pending_reasons.values()),
    )
    observed_fresh_ready_count = sum(
        1
        for item in ready_items
        if item.get("freshness", "fresh") == "fresh"
    )
    if "freshReadyCount" in meta:
        fresh_ready_count = min(
            observed_fresh_ready_count,
            _safe_count(meta.get("freshReadyCount"), 0),
        )
    else:
        fresh_ready_count = observed_fresh_ready_count
    stale_ready_count = max(
        len(stale_codes),
        _safe_count(meta.get("staleReadyCount"), 0),
    )
    observed_partial_ready_count = sum(
        1
        for item in ready_items
        if item.get("availability") == "partial"
        or item.get("fxStatus") == "omitted"
    )
    # Recompute upward when the backend meta predates fxStatus=omitted.  The
    # quote remains ready/current; only evidence completeness is degraded.
    partial_ready_count = max(
        _safe_count(meta.get("partialReadyCount"), 0),
        observed_partial_ready_count,
    )
    weak_coverage_count = max(
        _safe_count(meta.get("weakCoverageCount"), 0),
        sum(1 for item in ready_items if item.get("weakCoverage") is True),
    )
    frame_refreshing = meta.get("frameRefreshing") is True or result.get("frameRefreshing") is True
    truncated = meta.get("truncated") is True
    complete = bool(
        requested_count > 0
        and not truncated
        and returned_count == requested_count
        and pending_count == 0
        and ready_count == returned_count
    )
    current_complete = bool(
        response_view == "forecast"
        and complete
        and not frame_refreshing
        and stale_ready_count == 0
        and fresh_ready_count == ready_count
    )
    poller_pending_count = _safe_count(
        pending_reasons.get("poller_pending"),
        len(poller_pending_codes),
    )
    timeout_pending_count = _safe_count(
        pending_reasons.get("request_timeout"),
        len(timeout_pending_codes),
    )
    warming = bool(
        frame_refreshing
        or poller_pending_count > 0
        or timeout_pending_count > 0
        or (
            meta.get("requestTimedOut") is True
            and pending_count > 0
            and (
                not pending_reasons
                or pending_reasons.get("request_timeout", 0) > 0
            )
        )
    )

    meta.update({
        "requestedCount": requested_count,
        "returnedCount": returned_count,
        "readyCount": ready_count,
        "pendingCount": pending_count,
        "freshReadyCount": fresh_ready_count,
        "staleReadyCount": stale_ready_count,
        "partialReadyCount": partial_ready_count,
        "weakCoverageCount": weak_coverage_count,
        "pendingReasons": pending_reasons,
    })
    return {
        **result,
        "view": response_view,
        "items": items,
        "meta": meta,
        "frameRefreshing": frame_refreshing,
        "warming": warming,
        # complete is completeness of the selected view. last_close can be a
        # complete historical snapshot while currentComplete remains false.
        "complete": complete,
        "currentComplete": current_complete,
        "evidenceComplete": bool(
            complete
            and partial_ready_count == 0
            and weak_coverage_count == 0
            and (
                response_view == "last_close"
                or current_complete
            )
        ),
        "staleCodes": stale_codes,
        "pollerPendingCodes": poller_pending_codes,
        "timeoutPendingCodes": timeout_pending_codes,
    }
