"""Universal latest-comparable-year selection for annual planning data."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, fields
import math
import re
from typing import Any


_RECORD_FIELDS = frozenset(
    {"record_id", "year", "regime_id", "comparable", "evidence_status"}
)
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_EVIDENCE_STATUSES = frozenset(
    {
        "official",
        "corroborated",
        "reference",
        "inferred",
        "partial",
        "missing",
        "conflict",
        "masked",
    }
)


def _mathematical_int(
    value: Any,
    name: str,
    *,
    minimum: int,
    maximum: int,
) -> int:
    if isinstance(value, bool):
        raise TypeError(f"{name} must be a mathematical integer")
    if isinstance(value, int):
        result = value
    elif isinstance(value, float) and math.isfinite(value) and value.is_integer():
        result = int(value)
    else:
        raise TypeError(f"{name} must be a mathematical integer")
    if result < minimum or result > maximum:
        raise ValueError(f"{name} is outside its supported range")
    return result


def year_window(target_year: Any) -> tuple[int, int, int, int]:
    """Return the exact target-year through target-minus-three search order."""

    year = _mathematical_int(
        target_year, "target_year", minimum=2000, maximum=2100
    )
    return year, year - 1, year - 2, year - 3


@dataclass(frozen=True)
class _AnnualRecord:
    record_id: str
    year: int
    regime_id: str
    comparable: bool
    evidence_status: str


def _record(value: Any) -> _AnnualRecord:
    if not isinstance(value, Mapping) or set(value) != _RECORD_FIELDS:
        raise ValueError("annual record fields do not match the contract")
    record_id = value["record_id"]
    regime_id = value["regime_id"]
    if not isinstance(record_id, str) or _SAFE_ID.fullmatch(record_id) is None:
        raise ValueError("annual record ID is unsafe")
    if not isinstance(regime_id, str) or _SAFE_ID.fullmatch(regime_id) is None:
        raise ValueError("annual regime ID is unsafe")
    year = _mathematical_int(value["year"], "record year", minimum=1900, maximum=2100)
    comparable = value["comparable"]
    if not isinstance(comparable, bool):
        raise TypeError("annual comparable flag must be boolean")
    status = value["evidence_status"]
    if not isinstance(status, str) or status not in _EVIDENCE_STATUSES:
        raise ValueError("annual evidence status is unsupported")
    return _AnnualRecord(record_id, year, regime_id, comparable, status)


@dataclass(frozen=True, init=False)
class YearSelection:
    primary_year: int | None
    trend_years: tuple[int, ...]
    fallback_distance: int | None
    selected_record_ids: tuple[str, ...]
    selected_evidence_statuses: tuple[str, ...]
    rejected_years: tuple[int, ...]
    reason_codes: tuple[str, ...]

    def __init__(self) -> None:
        raise TypeError("YearSelection is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "YearSelection":
        if set(values) != {item.name for item in fields(cls)}:
            raise TypeError("YearSelection factory fields do not match the contract")
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary_year": self.primary_year,
            "trend_years": list(self.trend_years),
            "fallback_distance": self.fallback_distance,
            "selected_record_ids": list(self.selected_record_ids),
            "selected_evidence_statuses": list(self.selected_evidence_statuses),
            "rejected_years": list(self.rejected_years),
            "reason_codes": list(self.reason_codes),
        }


def select_latest_comparable(
    records: Iterable[Mapping[str, Any]],
    *,
    target_year: Any,
    maximum_trend_years: Any = 3,
) -> YearSelection:
    """Select one latest basis and up to three comparable trend years.

    Source status is preserved but does not override recency.  Callers decide
    whether a status may support calculation; this selector only enforces the
    independent annual fallback and regime boundary.
    """

    window = year_window(target_year)
    year = window[0]
    limit = _mathematical_int(
        maximum_trend_years,
        "maximum_trend_years",
        minimum=1,
        maximum=3,
    )
    if isinstance(records, (str, bytes, bytearray, Mapping)):
        raise TypeError("records must be an iterable of annual mappings")
    try:
        normalized = tuple(_record(item) for item in records)
    except TypeError as error:
        raise TypeError("records must be an iterable of annual mappings") from error
    ids = tuple(item.record_id for item in normalized)
    if len(ids) != len(set(ids)):
        raise ValueError("annual record IDs must be unique")

    rejected_years: set[int] = set()
    reasons: set[str] = set()
    candidates: list[_AnnualRecord] = []
    for item in normalized:
        if item.year not in window:
            rejected_years.add(item.year)
            reasons.add("outside_year_window_rejected")
        elif not item.comparable:
            rejected_years.add(item.year)
            reasons.add("noncomparable_record_rejected")
        else:
            candidates.append(item)

    if not candidates:
        reasons.add("no_comparable_year")
        return YearSelection._create(
            primary_year=None,
            trend_years=(),
            fallback_distance=None,
            selected_record_ids=(),
            selected_evidence_statuses=(),
            rejected_years=tuple(sorted(rejected_years, reverse=True)),
            reason_codes=tuple(sorted(reasons)),
        )

    primary_year = max(item.year for item in candidates)
    primary_regimes = {
        item.regime_id for item in candidates if item.year == primary_year
    }
    if len(primary_regimes) != 1:
        rejected_years.update(item.year for item in candidates)
        reasons.add("latest_year_regime_conflict")
        return YearSelection._create(
            primary_year=None,
            trend_years=(),
            fallback_distance=None,
            selected_record_ids=(),
            selected_evidence_statuses=(),
            rejected_years=tuple(sorted(rejected_years, reverse=True)),
            reason_codes=tuple(sorted(reasons)),
        )
    regime = next(iter(primary_regimes))
    comparable: list[_AnnualRecord] = []
    for item in candidates:
        if item.regime_id != regime:
            rejected_years.add(item.year)
            reasons.add("regime_break_rejected")
        else:
            comparable.append(item)

    trend_years = tuple(
        sorted({item.year for item in comparable}, reverse=True)[:limit]
    )
    trend_set = set(trend_years)
    if len({item.year for item in comparable}) > limit:
        reasons.add("trend_year_limit_applied")
        rejected_years.update(
            item.year for item in comparable if item.year not in trend_set
        )
    selected = tuple(
        sorted(
            (item for item in comparable if item.year in trend_set),
            key=lambda item: (-item.year, item.record_id),
        )
    )
    fallback = year - primary_year
    reasons.add("current_year_selected" if fallback == 0 else "fallback_used")
    return YearSelection._create(
        primary_year=primary_year,
        trend_years=trend_years,
        fallback_distance=fallback,
        selected_record_ids=tuple(item.record_id for item in selected),
        selected_evidence_statuses=tuple(item.evidence_status for item in selected),
        rejected_years=tuple(sorted(rejected_years, reverse=True)),
        reason_codes=tuple(sorted(reasons)),
    )


__all__ = ["YearSelection", "select_latest_comparable", "year_window"]
