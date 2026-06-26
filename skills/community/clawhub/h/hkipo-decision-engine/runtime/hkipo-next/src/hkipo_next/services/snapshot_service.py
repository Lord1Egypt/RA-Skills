"""Service for standardized IPO snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol

from hkipo_next.contracts.errors import AppError, AppException, ErrorCode
from hkipo_next.contracts.snapshot import (
    SnapshotConflict,
    SnapshotConflictValue,
    SnapshotData,
    SnapshotFieldConfidence,
    SnapshotFieldSource,
    SnapshotIssue,
    SnapshotQuality,
)
from hkipo_next.utils.normalization import (
    normalize_symbol,
    parse_date,
    parse_optional_float,
    parse_price_range,
    split_sponsors,
    value_to_repr,
)


class SnapshotAdapter(Protocol):
    """Contract for snapshot data providers."""

    def fetch_ipo_brief(self, symbol: str) -> dict[str, Any] | None:
        ...

    def fetch_aastocks_detail(self, symbol: str) -> dict[str, Any] | None:
        ...

    def fetch_aastocks_upcoming_ipos(self) -> list[dict[str, Any]]:
        ...


@dataclass(frozen=True)
class SnapshotFieldValue:
    value: Any
    source: str


class SnapshotService:
    """Aggregate legacy sources into the canonical snapshot schema."""

    SOURCE_PRIORITY = ["aipo.ipo_brief", "aastocks.detail", "aastocks.upcoming"]
    FIELD_PRIORITY = {
        "company_name": ["aastocks.detail", "aastocks.upcoming"],
        "industry": ["aipo.ipo_brief", "aastocks.detail", "aastocks.upcoming"],
        "sponsors": ["aipo.ipo_brief", "aastocks.detail"],
        "offer_price_floor": ["aipo.ipo_brief", "aastocks.detail", "aastocks.upcoming"],
        "offer_price_ceiling": ["aipo.ipo_brief", "aastocks.detail", "aastocks.upcoming"],
        "lot_size": ["aastocks.detail", "aastocks.upcoming"],
        "entry_fee_hkd": ["aipo.ipo_brief", "aastocks.upcoming"],
        "deadline_date": ["aipo.ipo_brief", "aastocks.upcoming"],
        "listing_date": ["aipo.ipo_brief", "aastocks.detail", "aastocks.upcoming"],
    }
    QUALITY_FIELDS = [
        "offer_price_floor",
        "offer_price_ceiling",
        "lot_size",
        "entry_fee_hkd",
        "deadline_date",
        "listing_date",
    ]

    def __init__(self, adapter: SnapshotAdapter):
        self.adapter = adapter

    def snapshot(self, *, symbol: str) -> SnapshotData:
        normalized_symbol = normalize_symbol(symbol)
        if not normalized_symbol:
            raise AppException(
                AppError.arg(
                    "snapshot 命令需要有效的 IPO 代码。",
                    details={"symbol": symbol},
                )
            )

        issues: list[SnapshotIssue] = []
        aipo_brief = self._load_source(
            fetcher=lambda: self.adapter.fetch_ipo_brief(normalized_symbol),
            source="aipo.ipo_brief",
            issues=issues,
        )
        aastocks_detail = self._load_source(
            fetcher=lambda: self.adapter.fetch_aastocks_detail(normalized_symbol),
            source="aastocks.detail",
            issues=issues,
        )
        aastocks_upcoming_list = self._load_source(
            fetcher=self.adapter.fetch_aastocks_upcoming_ipos,
            source="aastocks.upcoming",
            issues=issues,
        )
        aastocks_upcoming = self._find_upcoming_row(aastocks_upcoming_list, normalized_symbol)

        if not aipo_brief and not aastocks_detail and not aastocks_upcoming:
            raise AppException(
                AppError.source(
                    "未找到对应 IPO 的快照数据。",
                    details={"symbol": normalized_symbol},
                )
            )

        normalized_sources = {
            "aipo.ipo_brief": self._normalize_aipo_brief(aipo_brief),
            "aastocks.detail": self._normalize_aastocks_detail(aastocks_detail),
            "aastocks.upcoming": self._normalize_aastocks_upcoming(aastocks_upcoming),
        }

        resolved_fields: dict[str, SnapshotFieldValue] = {}
        conflicts: list[SnapshotConflict] = []
        missing_fields: list[str] = []
        field_confidence: list[SnapshotFieldConfidence] = []

        for field_name, priority in self.FIELD_PRIORITY.items():
            candidates = self._collect_candidates(field_name, normalized_sources, priority)
            resolved = candidates[0] if candidates else SnapshotFieldValue(value=None, source=priority[0])
            resolved_fields[field_name] = resolved

            if resolved.value in (None, [], "") and field_name in self.QUALITY_FIELDS:
                missing_fields.append(field_name)
                issues.append(
                    SnapshotIssue(
                        code=ErrorCode.E_SOURCE.value,
                        source="snapshot.quality",
                        message="关键字段缺失，需要人工复核。",
                        details={"field_name": field_name},
                    )
                )

            conflict = self._build_conflict(field_name, candidates, resolved)
            if conflict is not None:
                conflicts.append(conflict)
                issues.append(
                    SnapshotIssue(
                        code=ErrorCode.E_SOURCE.value,
                        source="snapshot.quality",
                        message="多个来源返回冲突值，已按固定优先级选值。",
                        details={
                            "field_name": field_name,
                            "selected_source": resolved.source,
                            "selected_value": value_to_repr(resolved.value),
                        },
                    )
                )

            confidence = self._calculate_confidence(resolved, candidates)
            field_confidence.append(
                SnapshotFieldConfidence(
                    field_name=field_name,
                    confidence=confidence,
                )
            )

        overall_confidence = round(
            sum(
                confidence.confidence
                for confidence in field_confidence
                if confidence.field_name in self.QUALITY_FIELDS
            )
            / len(self.QUALITY_FIELDS),
            2,
        )

        quality = SnapshotQuality(
            missing_fields=missing_fields,
            conflicts=conflicts,
            field_confidence=field_confidence,
            overall_confidence=overall_confidence,
        )

        field_sources = [
            SnapshotFieldSource(field_name=name, source=field.source)
            for name, field in resolved_fields.items()
            if field.value not in (None, [], "")
        ]

        return SnapshotData(
            symbol=normalized_symbol,
            company_name=resolved_fields["company_name"].value,
            industry=resolved_fields["industry"].value,
            sponsors=resolved_fields["sponsors"].value or [],
            offer_price_floor=resolved_fields["offer_price_floor"].value,
            offer_price_ceiling=resolved_fields["offer_price_ceiling"].value,
            lot_size=resolved_fields["lot_size"].value,
            entry_fee_hkd=resolved_fields["entry_fee_hkd"].value,
            deadline_date=resolved_fields["deadline_date"].value,
            listing_date=resolved_fields["listing_date"].value,
            source_priority=self.SOURCE_PRIORITY,
            field_sources=field_sources,
            issues=issues,
            quality=quality,
        )

    def _load_source(
        self,
        *,
        fetcher: Callable[[], Any],
        source: str,
        issues: list[SnapshotIssue],
    ) -> Any:
        try:
            return fetcher() or {}
        except Exception as exc:
            issues.append(
                SnapshotIssue(
                    code=ErrorCode.E_SOURCE.value,
                    source=source,
                    message="快照来源不可用，已尝试从其他来源继续生成。",
                    details={"reason": str(exc)},
                )
            )
            return {}

    @staticmethod
    def _find_upcoming_row(rows: Any, symbol: str) -> dict[str, Any]:
        if not isinstance(rows, list):
            return {}
        for row in rows:
            row_symbol = normalize_symbol(row.get("symbol"))
            if row_symbol == symbol:
                return row
        return {}

    @staticmethod
    def _normalize_aipo_brief(payload: dict[str, Any]) -> dict[str, Any]:
        floor = parse_optional_float(payload.get("ipo_price_floor"))
        ceiling = parse_optional_float(payload.get("ipo_price_ceiling"))
        if floor is not None and floor <= 0:
            floor = None
        if ceiling is not None and ceiling <= 0:
            ceiling = None
        if floor is None and ceiling is not None:
            floor = ceiling
        if ceiling is None and floor is not None:
            ceiling = floor

        return {
            "industry": payload.get("industry") or None,
            "sponsors": split_sponsors(payload.get("sponsors")),
            "offer_price_floor": floor,
            "offer_price_ceiling": ceiling,
            "entry_fee_hkd": parse_optional_float(payload.get("minimum_capital")),
            "deadline_date": parse_date(payload.get("apply_end")),
            "listing_date": parse_date(payload.get("listing_date")),
        }

    @staticmethod
    def _normalize_aastocks_detail(payload: dict[str, Any]) -> dict[str, Any]:
        floor, ceiling = parse_price_range(payload.get("offer_price_range"))
        return {
            "company_name": payload.get("name_tc") or payload.get("name_en") or None,
            "industry": payload.get("industry") or None,
            "sponsors": split_sponsors(payload.get("sponsors")),
            "offer_price_floor": floor,
            "offer_price_ceiling": ceiling,
            "lot_size": payload.get("lot_size"),
            "listing_date": parse_date(payload.get("listing_date")),
        }

    @staticmethod
    def _normalize_aastocks_upcoming(payload: dict[str, Any]) -> dict[str, Any]:
        floor, ceiling = parse_price_range(payload.get("offer_price_range"))
        return {
            "company_name": payload.get("name_tc") or None,
            "industry": payload.get("industry") or None,
            "offer_price_floor": floor,
            "offer_price_ceiling": ceiling,
            "lot_size": payload.get("lot_size"),
            "entry_fee_hkd": parse_optional_float(payload.get("entry_fee")),
            "deadline_date": parse_date(payload.get("subscription_deadline")),
            "listing_date": parse_date(payload.get("listing_date")),
        }

    @staticmethod
    def _collect_candidates(
        field_name: str,
        normalized_sources: dict[str, dict[str, Any]],
        priority: list[str],
    ) -> list[SnapshotFieldValue]:
        candidates: list[SnapshotFieldValue] = []
        for source in priority:
            value = normalized_sources.get(source, {}).get(field_name)
            if value not in (None, [], ""):
                candidates.append(SnapshotFieldValue(value=value, source=source))
        return candidates

    @staticmethod
    def _build_conflict(
        field_name: str,
        candidates: list[SnapshotFieldValue],
        resolved: SnapshotFieldValue,
    ) -> SnapshotConflict | None:
        if len(candidates) < 2:
            return None

        unique_values = {value_to_repr(candidate.value) for candidate in candidates}
        if len(unique_values) == 1:
            return None

        return SnapshotConflict(
            field_name=field_name,
            selected_source=resolved.source,
            selected_value=value_to_repr(resolved.value),
            alternatives=[
                SnapshotConflictValue(
                    source=candidate.source,
                    value=value_to_repr(candidate.value),
                )
                for candidate in candidates
            ],
        )

    @staticmethod
    def _calculate_confidence(
        resolved: SnapshotFieldValue,
        candidates: list[SnapshotFieldValue],
    ) -> float:
        if resolved.value in (None, [], ""):
            return 0.0
        if len(candidates) == 1:
            return 0.75 if resolved.source.startswith("aipo.") else 0.7

        unique_values = {value_to_repr(candidate.value) for candidate in candidates}
        if len(unique_values) == 1:
            return 0.95
        return 0.45
