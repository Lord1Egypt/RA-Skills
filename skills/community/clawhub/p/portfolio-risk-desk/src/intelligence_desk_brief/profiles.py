"""Saved profile models and helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import re
from typing import Any

from intelligence_desk_brief.contracts import BriefType, CreateBriefRequest, DeliveryTarget
from intelligence_desk_brief.memory import resolve_workspace_id


@dataclass(frozen=True)
class SavedProfile:
    profile_id: str
    profile_name: str
    workspace_id: str
    portfolio_name: str | None
    holdings: list[str]
    watchlist: list[str]
    themes: list[str]
    brief_type: str
    lookback_hours: int
    max_items_per_theme: int | None
    benchmark_or_comparison_lens: str | None
    scenario_questions: list[str]
    created_at: str
    updated_at: str

    @classmethod
    def from_request(
        cls,
        request: CreateBriefRequest,
        *,
        profile_id: str | None = None,
        profile_name: str | None = None,
    ) -> "SavedProfile":
        timestamp = datetime.now(timezone.utc).isoformat()
        resolved_name = profile_name or request.profile_name or request.portfolio_name or "saved-profile"
        resolved_id = profile_id or request.profile_id or slugify_profile_name(resolved_name)
        return cls(
            profile_id=resolved_id,
            profile_name=resolved_name,
            workspace_id=resolve_workspace_id(request),
            portfolio_name=request.portfolio_name,
            holdings=list(request.holdings),
            watchlist=list(request.watchlist),
            themes=list(request.themes),
            brief_type=request.brief_type.value,
            lookback_hours=request.lookback_hours,
            max_items_per_theme=request.max_items_per_theme,
            benchmark_or_comparison_lens=request.benchmark_or_comparison_lens,
            scenario_questions=list(request.scenario_questions),
            created_at=timestamp,
            updated_at=timestamp,
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SavedProfile":
        return cls(
            profile_id=str(payload["profile_id"]),
            profile_name=str(payload["profile_name"]),
            workspace_id=str(payload["workspace_id"]),
            portfolio_name=payload.get("portfolio_name"),
            holdings=[str(item) for item in payload.get("holdings", [])],
            watchlist=[str(item) for item in payload.get("watchlist", [])],
            themes=[str(item) for item in payload.get("themes", [])],
            brief_type=str(payload.get("brief_type", "daily")),
            lookback_hours=int(payload.get("lookback_hours", 24)),
            max_items_per_theme=payload.get("max_items_per_theme"),
            benchmark_or_comparison_lens=payload.get("benchmark_or_comparison_lens"),
            scenario_questions=[str(item) for item in payload.get("scenario_questions", [])],
            created_at=str(payload.get("created_at") or ""),
            updated_at=str(payload.get("updated_at") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_request(self, *, delivery_target: DeliveryTarget = DeliveryTarget.INLINE) -> CreateBriefRequest:
        return CreateBriefRequest(
            portfolio_name=self.portfolio_name,
            workspace_id=self.workspace_id,
            profile_id=self.profile_id,
            profile_name=self.profile_name,
            holdings=list(self.holdings),
            watchlist=list(self.watchlist),
            themes=list(self.themes),
            brief_type=BriefType(self.brief_type),
            lookback_hours=self.lookback_hours,
            delivery_target=delivery_target,
            max_items_per_theme=self.max_items_per_theme,
            benchmark_or_comparison_lens=self.benchmark_or_comparison_lens,
            scenario_questions=list(self.scenario_questions),
        )


def slugify_profile_name(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "saved-profile"
