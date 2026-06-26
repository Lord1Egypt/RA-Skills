"""Service for upcoming IPO discovery."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Protocol

from hkipo_next.contracts.discovery import (
    DiscoveryData,
    DiscoveryFilter,
    DiscoveryIssue,
    DiscoveryItem,
    WindowType,
)
from hkipo_next.contracts.errors import AppError, AppException, ErrorCode
from hkipo_next.utils.normalization import normalize_symbol, parse_date, parse_optional_float


class DiscoveryAdapter(Protocol):
    """Contract for discovery data providers."""

    def fetch_margin_list(self) -> list[dict[str, Any]]:
        ...

    def fetch_ipo_brief(self, symbol: str) -> dict[str, Any] | None:
        ...


class DiscoveryService:
    """Compose discovery results into the canonical schema."""

    def __init__(self, adapter: DiscoveryAdapter):
        self.adapter = adapter

    def discover(self, *, window: WindowType, days: int) -> DiscoveryData:
        if days < 0:
            raise AppException(
                AppError.arg(
                    "days 必须为 0 或正整数。",
                    details={"days": days},
                )
            )

        try:
            raw_ipos = self.adapter.fetch_margin_list()
        except Exception as exc:
            raise AppException(
                AppError.source(
                    "无法获取当前招股 IPO 列表。",
                    details={"source": "aipo.margin_list", "reason": str(exc)},
                )
            ) from exc

        issues: list[DiscoveryIssue] = []
        filtered_items: list[DiscoveryItem] = []

        for raw in raw_ipos:
            item, item_issues = self._build_item(raw)
            issues.extend(item_issues)
            if self._matches_window(item, window, days):
                filtered_items.append(item)

        filtered_items.sort(
            key=lambda item: (
                self._sort_key(item, window),
                item.symbol or "",
            )
        )

        return DiscoveryData(
            filter=DiscoveryFilter(window=window, days=days),
            items=filtered_items,
            issues=issues,
            total_items=len(filtered_items),
        )

    def _build_item(self, raw: dict[str, Any]) -> tuple[DiscoveryItem, list[DiscoveryIssue]]:
        issues: list[DiscoveryIssue] = []
        symbol = normalize_symbol(raw.get("code"))
        source_tags = ["aipo.margin_list"]
        data_status = "complete"
        degradation_reason: str | None = None

        try:
            brief = self.adapter.fetch_ipo_brief(symbol or "") or {}
            if brief:
                source_tags.append("aipo.ipo_brief")
        except Exception as exc:
            brief = {}
            data_status = "partial"
            degradation_reason = "aipo_ipo_brief_unavailable"
            issues.append(
                DiscoveryIssue(
                    code=ErrorCode.E_SOURCE.value,
                    source="aipo.ipo_brief",
                    message="IPO 详情源暂时不可用，已返回最小可用发现结果。",
                    details={"symbol": symbol, "reason": str(exc)},
                )
            )

        deadline_date = parse_date(brief.get("apply_end") or raw.get("apply_end"))
        listing_date = parse_date(brief.get("listing_date") or raw.get("listing_date"))
        missing_fields: list[str] = []
        if deadline_date is None:
            missing_fields.append("deadline_date")
        if listing_date is None:
            missing_fields.append("listing_date")

        if missing_fields:
            data_status = "partial"
            degradation_reason = degradation_reason or "missing_fields"
            issues.append(
                DiscoveryIssue(
                    code=ErrorCode.E_SOURCE.value,
                    source="calendar.normalization",
                    message="IPO 发现结果存在字段缺失，已保留最小可用数据。",
                    details={"symbol": symbol, "missing_fields": missing_fields},
                )
            )

        return (
            DiscoveryItem(
                symbol=symbol,
                name=str(raw.get("name") or brief.get("name") or symbol or "未知标的"),
                deadline_date=deadline_date,
                listing_date=listing_date,
                entry_fee_hkd=parse_optional_float(brief.get("minimum_capital")),
                total_margin_hkd_100m=parse_optional_float(raw.get("total_margin")),
                source_tags=source_tags,
                data_status=data_status,
                degradation_reason=degradation_reason,
            ),
            issues,
        )

    @staticmethod
    def _matches_window(item: DiscoveryItem, window: WindowType, days: int) -> bool:
        today = date.today()
        upper_bound = today + timedelta(days=days)
        target_date = item.deadline_date if window == "deadline" else item.listing_date
        if target_date is None:
            return False
        return today <= target_date <= upper_bound

    @staticmethod
    def _sort_key(item: DiscoveryItem, window: WindowType) -> date:
        target_date = item.deadline_date if window == "deadline" else item.listing_date
        return target_date or date.max
