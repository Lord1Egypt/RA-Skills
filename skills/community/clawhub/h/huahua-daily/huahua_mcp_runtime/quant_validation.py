"""Validation shared by fund-quant MCP tool transports."""

from datetime import date, datetime
import math


_QUANT_FRAME_FIELDS = {
    "technicalValue",
    "valueBasis",
    "valueAsOf",
    "source",
    "targetNavDate",
    "latestOfficialNavDate",
    "estimateFreshness",
    "estimateStale",
    "fallbackReason",
    "lastGoodCapturedAt",
}
_QUANT_FRAME_LINEAGE_FIELDS = _QUANT_FRAME_FIELDS - {"technicalValue", "valueBasis"}
_QUANT_VIEWS = {"technical", "momentum", "risk", "full"}


def validate_quant_view(view: object) -> str:
    normalized = str(view or "").strip().lower()
    if normalized not in _QUANT_VIEWS:
        raise ValueError("view 仅支持 technical、momentum、risk 或 full")
    return normalized


def _validate_iso_date(name: str, value: object) -> str:
    normalized = str(value or "").strip()
    try:
        parsed = date.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{name} 必须使用 YYYY-MM-DD") from exc
    if parsed.isoformat() != normalized:
        raise ValueError(f"{name} 必须使用 YYYY-MM-DD")
    return normalized


def validate_quant_current_frame(frame: object) -> dict:
    if not isinstance(frame, dict):
        raise ValueError("current_frames 的每个估算帧必须是对象")
    unexpected = set(frame) - _QUANT_FRAME_FIELDS
    if unexpected:
        raise ValueError(f"current_frames 包含未知字段: {sorted(map(str, unexpected))}")
    normalized = dict(frame)
    basis = str(normalized.get("valueBasis") or "official_nav")
    if basis not in {"official_nav", "live_estimate"}:
        raise ValueError("valueBasis 仅支持 official_nav 或 live_estimate")
    normalized["valueBasis"] = basis
    technical_value = normalized.get("technicalValue")
    if technical_value is not None:
        try:
            technical_value = float(technical_value)
        except (TypeError, ValueError) as exc:
            raise ValueError("technicalValue 必须是正数") from exc
        if not math.isfinite(technical_value) or technical_value <= 0:
            raise ValueError("technicalValue 必须是正数")
        normalized["technicalValue"] = technical_value
    if basis == "live_estimate" and technical_value is None:
        raise ValueError("live_estimate 必须提供 technicalValue")
    if basis == "official_nav" and technical_value is not None:
        raise ValueError("official_nav 使用服务端官方净值，不接受 technicalValue")
    for name in ("valueAsOf", "targetNavDate", "latestOfficialNavDate"):
        if normalized.get(name):
            normalized[name] = _validate_iso_date(name, normalized[name])
    freshness = normalized.get("estimateFreshness")
    if freshness is not None and freshness not in {"fresh", "stale", "unavailable"}:
        raise ValueError("estimateFreshness 仅支持 fresh、stale 或 unavailable")
    if normalized.get("estimateStale") is not None and not isinstance(
        normalized["estimateStale"],
        bool,
    ):
        raise ValueError("estimateStale 必须是布尔值")
    captured_at = normalized.get("lastGoodCapturedAt")
    if captured_at:
        try:
            datetime.fromisoformat(str(captured_at).replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("lastGoodCapturedAt 必须是 ISO 8601 时间") from exc
    if basis == "official_nav" and any(
        normalized.get(name) is not None for name in _QUANT_FRAME_LINEAGE_FIELDS
    ):
        raise ValueError("official_nav 的日期、来源和新鲜度由服务端确定，不接受当前帧元数据")
    return normalized
