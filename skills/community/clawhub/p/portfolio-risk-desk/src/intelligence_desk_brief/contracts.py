"""Typed contract models derived from the tool contract document."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from enum import Enum
from typing import Any


class ContractValidationError(ValueError):
    """Raised when a request or response violates the contract."""


class BriefType(str, Enum):
    DAILY = "daily"
    ON_DEMAND = "on_demand"
    EARNINGS_REACTION = "earnings_reaction"


class DeliveryTarget(str, Enum):
    INLINE = "inline"
    NOTION = "notion"


class DeliveryStatus(str, Enum):
    INLINE_RETURNED = "inline_returned"
    HANDOFF_RECORDED = "handoff_recorded"
    FAILED = "failed"


class NotionWriteStatus(str, Enum):
    ACCEPTED = "accepted"
    CREATED = "created"
    UPDATED = "updated"
    FAILED = "failed"


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractValidationError(f"{name} must be an object.")
    return value


def _require_string(name: str, value: Any, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise ContractValidationError(f"{name} must be a string.")
    if not allow_empty and not value.strip():
        raise ContractValidationError(f"{name} must not be empty.")
    return value


def _optional_string(name: str, value: Any) -> str | None:
    if value is None:
        return None
    return _require_string(name, value)


def _optional_mapping(name: str, value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    return _require_mapping(name, value)


def _require_string_list(name: str, value: Any, *, default: list[str] | None = None) -> list[str]:
    if value is None:
        return list(default or [])
    if not isinstance(value, list):
        raise ContractValidationError(f"{name} must be an array of strings.")
    parsed: list[str] = []
    for index, item in enumerate(value):
        parsed.append(_require_string(f"{name}[{index}]", item))
    return parsed


def _require_object_list(name: str, value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ContractValidationError(f"{name} must be an array of objects.")
    parsed: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        parsed.append(_require_mapping(f"{name}[{index}]", item))
    return parsed


@dataclass
class CreateBriefRequest:
    portfolio_name: str | None
    workspace_id: str | None
    profile_id: str | None
    profile_name: str | None
    holdings: list[str]
    watchlist: list[str]
    themes: list[str]
    brief_type: BriefType
    lookback_hours: int
    delivery_target: DeliveryTarget
    max_items_per_theme: int | None
    benchmark_or_comparison_lens: str | None
    scenario_questions: list[str]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CreateBriefRequest":
        data = _require_mapping("create_brief.input", payload)
        themes = _require_string_list("themes", data.get("themes"))
        if not themes:
            raise ContractValidationError("themes must include at least one theme.")

        brief_type_raw = _require_string("brief_type", data.get("brief_type"))
        delivery_target_raw = _require_string("delivery_target", data.get("delivery_target"))

        lookback_hours = data.get("lookback_hours")
        if not isinstance(lookback_hours, int) or lookback_hours <= 0:
            raise ContractValidationError("lookback_hours must be a positive integer.")

        max_items_per_theme = data.get("max_items_per_theme")
        if max_items_per_theme is not None:
            if not isinstance(max_items_per_theme, int) or max_items_per_theme <= 0:
                raise ContractValidationError(
                    "max_items_per_theme must be a positive integer when provided."
                )

        try:
            brief_type = BriefType(brief_type_raw)
        except ValueError as error:
            raise ContractValidationError(
                "brief_type must be one of daily, on_demand, earnings_reaction."
            ) from error

        try:
            delivery_target = DeliveryTarget(delivery_target_raw)
        except ValueError as error:
            raise ContractValidationError(
                "delivery_target must be one of inline or notion."
            ) from error

        return cls(
            portfolio_name=_optional_string("portfolio_name", data.get("portfolio_name")),
            workspace_id=_optional_string("workspace_id", data.get("workspace_id")),
            profile_id=_optional_string("profile_id", data.get("profile_id")),
            profile_name=_optional_string("profile_name", data.get("profile_name")),
            holdings=_require_string_list("holdings", data.get("holdings"), default=[]),
            watchlist=_require_string_list("watchlist", data.get("watchlist"), default=[]),
            themes=themes,
            brief_type=brief_type,
            lookback_hours=lookback_hours,
            delivery_target=delivery_target,
            max_items_per_theme=max_items_per_theme,
            benchmark_or_comparison_lens=_optional_string(
                "benchmark_or_comparison_lens",
                data.get("benchmark_or_comparison_lens"),
            ),
            scenario_questions=_require_string_list(
                "scenario_questions",
                data.get("scenario_questions"),
                default=[],
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["brief_type"] = self.brief_type.value
        payload["delivery_target"] = self.delivery_target.value
        return payload


@dataclass
class UserFocus:
    portfolio_or_watchlist: str
    interested_industries: list[str]
    brief_objective: str
    factor_lens: list[str]
    comparison_baseline: str
    scenario_questions: list[str]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "UserFocus":
        data = _require_mapping("user_focus", payload)
        return cls(
            portfolio_or_watchlist=_require_string(
                "user_focus.portfolio_or_watchlist",
                data.get("portfolio_or_watchlist"),
            ),
            interested_industries=_require_string_list(
                "user_focus.interested_industries",
                data.get("interested_industries"),
            ),
            brief_objective=_require_string(
                "user_focus.brief_objective",
                data.get("brief_objective"),
            ),
            factor_lens=_require_string_list(
                "user_focus.factor_lens",
                data.get("factor_lens"),
            ),
            comparison_baseline=_require_string(
                "user_focus.comparison_baseline",
                data.get("comparison_baseline"),
            ),
            scenario_questions=_require_string_list(
                "user_focus.scenario_questions",
                data.get("scenario_questions"),
                default=[],
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ScenarioAnalysisItem:
    scenario: str
    confidence_level: str
    confidence_reason: str
    breaks_or_holds: list[str]
    affected_names: list[str]
    supporting_evidence_ids: list[str]
    supporting_evidence: list[dict[str, Any]]
    falsifiers: list[str]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ScenarioAnalysisItem":
        data = _require_mapping("scenario_analysis[]", payload)
        confidence_level = _require_string(
            "scenario_analysis[].confidence_level",
            data.get("confidence_level"),
        )
        if confidence_level not in {"low", "medium", "high"}:
            raise ContractValidationError(
                "scenario_analysis[].confidence_level must be low, medium, or high."
            )
        return cls(
            scenario=_require_string("scenario_analysis[].scenario", data.get("scenario")),
            confidence_level=confidence_level,
            confidence_reason=_require_string(
                "scenario_analysis[].confidence_reason",
                data.get("confidence_reason"),
            ),
            breaks_or_holds=_require_string_list(
                "scenario_analysis[].breaks_or_holds",
                data.get("breaks_or_holds"),
            ),
            affected_names=_require_string_list(
                "scenario_analysis[].affected_names",
                data.get("affected_names"),
            ),
            supporting_evidence_ids=_require_string_list(
                "scenario_analysis[].supporting_evidence_ids",
                data.get("supporting_evidence_ids"),
                default=[],
            ),
            supporting_evidence=_require_object_list(
                "scenario_analysis[].supporting_evidence",
                data.get("supporting_evidence"),
            ),
            falsifiers=_require_string_list(
                "scenario_analysis[].falsifiers",
                data.get("falsifiers"),
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CreateBriefResponse:
    brief_id: str
    date: str
    workspace_id: str
    profile_id: str | None
    profile_name: str | None
    summary: str
    user_focus: UserFocus
    current_exposure_map: list[dict[str, Any]]
    dominant_factors: list[dict[str, Any]]
    risk_map_changes: list[dict[str, Any]]
    key_drivers_and_readthroughs: list[dict[str, Any]]
    scenario_analysis: list[ScenarioAnalysisItem]
    signal_vs_noise: list[dict[str, Any]]
    watchpoints: list[dict[str, Any]]
    evidence_and_sources: list[dict[str, Any]]
    audit_trail: dict[str, Any]
    uncertainty_notes: list[str]
    delivery_status: DeliveryStatus
    delivery_metadata: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CreateBriefResponse":
        data = _require_mapping("create_brief.output", payload)
        response_date = _require_string("date", data.get("date"))
        try:
            date.fromisoformat(response_date)
        except ValueError as error:
            raise ContractValidationError("date must be a valid ISO date.") from error

        delivery_status_raw = _require_string("delivery_status", data.get("delivery_status"))
        try:
            delivery_status = DeliveryStatus(delivery_status_raw)
        except ValueError as error:
            raise ContractValidationError(
                "delivery_status must be inline_returned, handoff_recorded, or failed."
            ) from error

        return cls(
            brief_id=_require_string("brief_id", data.get("brief_id")),
            date=response_date,
            workspace_id=_require_string("workspace_id", data.get("workspace_id")),
            profile_id=_optional_string("profile_id", data.get("profile_id")),
            profile_name=_optional_string("profile_name", data.get("profile_name")),
            summary=_require_string("summary", data.get("summary")),
            user_focus=UserFocus.from_dict(data.get("user_focus")),
            current_exposure_map=_require_object_list(
                "current_exposure_map",
                data.get("current_exposure_map"),
            ),
            dominant_factors=_require_object_list(
                "dominant_factors",
                data.get("dominant_factors"),
            ),
            risk_map_changes=_require_object_list(
                "risk_map_changes",
                data.get("risk_map_changes"),
            ),
            key_drivers_and_readthroughs=_require_object_list(
                "key_drivers_and_readthroughs",
                data.get("key_drivers_and_readthroughs"),
            ),
            scenario_analysis=[
                ScenarioAnalysisItem.from_dict(item)
                for item in _require_object_list("scenario_analysis", data.get("scenario_analysis"))
            ],
            signal_vs_noise=_require_object_list(
                "signal_vs_noise",
                data.get("signal_vs_noise"),
            ),
            watchpoints=_require_object_list("watchpoints", data.get("watchpoints")),
            evidence_and_sources=_require_object_list(
                "evidence_and_sources",
                data.get("evidence_and_sources"),
            ),
            audit_trail=_require_mapping("audit_trail", data.get("audit_trail")),
            uncertainty_notes=_require_string_list(
                "uncertainty_notes",
                data.get("uncertainty_notes"),
            ),
            delivery_status=delivery_status,
            delivery_metadata=_optional_mapping("delivery_metadata", data.get("delivery_metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["delivery_status"] = self.delivery_status.value
        return payload


@dataclass
class WriteBriefToNotionInput:
    brief_payload: dict[str, Any]
    parent_page_id: str
    workspace_id: str
    database_id: str | None = None
    profile_id: str | None = None
    profile_name: str | None = None
    brief_title: str | None = None
    markdown: str | None = None
    delivery_payload: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WriteBriefToNotionInput":
        data = _require_mapping("write_brief_to_notion.input", payload)
        return cls(
            brief_payload=_require_mapping("brief_payload", data.get("brief_payload")),
            parent_page_id=_require_string("parent_page_id", data.get("parent_page_id")),
            workspace_id=_require_string("workspace_id", data.get("workspace_id")),
            database_id=_optional_string("database_id", data.get("database_id")),
            profile_id=_optional_string("profile_id", data.get("profile_id")),
            profile_name=_optional_string("profile_name", data.get("profile_name")),
            brief_title=_optional_string("brief_title", data.get("brief_title")),
            markdown=_optional_string("markdown", data.get("markdown")),
            delivery_payload=_optional_mapping("delivery_payload", data.get("delivery_payload")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WriteBriefToNotionOutput:
    notion_page_id: str
    url: str
    status: NotionWriteStatus
    delivery_metadata: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WriteBriefToNotionOutput":
        data = _require_mapping("write_brief_to_notion.output", payload)
        status_raw = _require_string("status", data.get("status"))
        try:
            status = NotionWriteStatus(status_raw)
        except ValueError as error:
            raise ContractValidationError("status must be accepted, created, updated, or failed.") from error
        return cls(
            notion_page_id=_require_string("notion_page_id", data.get("notion_page_id")),
            url=_require_string("url", data.get("url")),
            status=status,
            delivery_metadata=_optional_mapping("delivery_metadata", data.get("delivery_metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload
