"""Batch decision-card orchestration."""

from __future__ import annotations

from typing import Protocol

from hkipo_next.contracts.decision_card import BatchData, BatchItemResult, BatchSource, BatchSummary
from hkipo_next.contracts.errors import AppError, AppException
from hkipo_next.contracts.preferences import ProfileView
from hkipo_next.contracts.scoring import ParameterVersion
from hkipo_next.utils.normalization import normalize_symbol


class DecisionProvider(Protocol):
    """Contract for building decision cards."""

    def build_for_symbol(
        self,
        *,
        symbol: str,
        parameter_version: ParameterVersion,
        profile: ProfileView,
    ):
        ...


class BatchService:
    """Build decision-card results for multiple IPO symbols."""

    def __init__(self, decision_provider: DecisionProvider):
        self.decision_provider = decision_provider

    def run(
        self,
        *,
        raw_symbols: list[str],
        source: BatchSource,
        parameter_version: ParameterVersion,
        profile: ProfileView,
        active_parameter_version: str | None,
    ) -> BatchData:
        symbols = self._normalize_symbols(raw_symbols)
        if not symbols:
            raise AppException(AppError.arg("batch 至少需要一个可解析的 IPO 代码。"))

        items: list[BatchItemResult] = []
        partial_count = 0
        failure_count = 0

        for symbol in symbols:
            try:
                card = self.decision_provider.build_for_symbol(
                    symbol=symbol,
                    parameter_version=parameter_version,
                    profile=profile,
                )
                data_status = "partial" if card.source_issue_count else "complete"
                if data_status == "partial":
                    partial_count += 1
                items.append(
                    BatchItemResult(
                        symbol=card.symbol,
                        ok=True,
                        decision_card=card,
                        data_status=data_status,
                    )
                )
            except AppException as exc:
                failure_count += 1
                items.append(
                    BatchItemResult(
                        symbol=symbol,
                        ok=False,
                        error=exc.error,
                        data_status="error",
                    )
                )
            except Exception as exc:  # pragma: no cover - defensive path
                failure_count += 1
                items.append(
                    BatchItemResult(
                        symbol=symbol,
                        ok=False,
                        error=AppError.system(
                            "批处理单项执行失败。",
                            details={"symbol": symbol, "reason": str(exc)},
                        ),
                        data_status="error",
                    )
                )

        success_count = len([item for item in items if item.ok])
        return BatchData(
            source=source,
            items=items,
            summary=BatchSummary(
                total_items=len(items),
                success_count=success_count,
                partial_count=partial_count,
                failure_count=failure_count,
            ),
            active_parameter_version=active_parameter_version,
            risk_profile=profile.risk_profile,
        )

    @staticmethod
    def _normalize_symbols(raw_symbols: list[str]) -> list[str]:
        normalized: list[str] = []
        for raw_symbol in raw_symbols:
            symbol = normalize_symbol(raw_symbol)
            if symbol is not None and symbol not in normalized:
                normalized.append(symbol)
        return normalized
