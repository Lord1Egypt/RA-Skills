from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SearchRequest:
    keyword: str = ""
    country: str = "australia"
    city: str = "melbourne"
    lang: str = "en"
    max_results: int = 20
    detail_limit: int = 10
    destination: str = ""
    budget_min: float | None = None
    budget_max: float | None = None
    bedrooms: float | None = None
    force_map: bool = True
    query_text: str = ""
    user_priorities: list[str] = field(default_factory=list)
    market_hint: str = "auto"
    source_hint: str = "auto"
    resolved_market: str = ""
    resolved_source_id: str = ""
    routing_reason: str = ""
    search_location_hint: str = ""
    country_is_default: bool = True
    city_is_default: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IntentDecision:
    intent: str
    reason: str
    mode: str = ""
    market: str = ""
    warnings: list[str] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ListingStrengthProfile:
    strengths: list[str] = field(default_factory=list)
    unit_features: list[str] = field(default_factory=list)
    amenities: list[str] = field(default_factory=list)
    property_services: list[str] = field(default_factory=list)
    target_audiences: list[str] = field(default_factory=list)
    source_phrases: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PublishPropertyRequest:
    mode: str = ""
    country: str = ""
    subdomain: str = ""
    property_type: str = "apartment"
    title: str = ""
    description: str = ""
    price: str | None = None
    location: str = ""
    images: list[str] = field(default_factory=list)
    floor_plans: list[str] = field(default_factory=list)
    rental_type: str = "entire"
    rent_period: str | None = None
    bedrooms: str | None = None
    bathrooms: str | None = None
    car_spaces: str | None = None
    floor_level: str | None = None
    floor: str | None = None
    area_size: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    unit_features: list[str] = field(default_factory=list)
    amenities: list[str] = field(default_factory=list)
    property_services: list[str] = field(default_factory=list)
    contact_name: str | None = None
    contact_email: str | None = None
    category_id: str | None = None
    postcode: str | None = None
    address: str | None = None
    publish_endpoint: str | None = None
    original_area_size: str | None = None
    area_unit: str | None = None
    lang: str = "en"
    query_text: str = ""
    market_hint: str = "auto"
    resolved_market: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PublishPropertyReport:
    request: PublishPropertyRequest
    intent: IntentDecision
    strength_profile: ListingStrengthProfile
    preflight: PreflightReport | None = None
    selected_source: str | None = None
    selected_runtime_mode: str | None = None
    generated_title: str = ""
    generated_description: str = ""
    readiness_status: str = ""
    missing_fields: list[str] = field(default_factory=list)
    required_missing_fields: list[str] = field(default_factory=list)
    recommended_missing_fields: list[str] = field(default_factory=list)
    follow_up_questions: list[str] = field(default_factory=list)
    contextual_follow_up_questions: list[str] = field(default_factory=list)
    command: list[str] = field(default_factory=list)
    publish_result: dict[str, Any] | None = None
    map_report: dict[str, Any] | None = None
    map_assessments: dict[str, Any] = field(default_factory=dict)
    map_verification_links: dict[str, str] = field(default_factory=dict)
    publish_facts: dict[str, Any] = field(default_factory=dict)
    area_conversion_warnings: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request.to_dict(),
            "intent": self.intent.to_dict(),
            "strength_profile": self.strength_profile.to_dict(),
            "preflight": self.preflight.to_dict() if self.preflight else None,
            "selected_source": self.selected_source,
            "selected_runtime_mode": self.selected_runtime_mode,
            "generated_title": self.generated_title,
            "generated_description": self.generated_description,
            "readiness_status": self.readiness_status,
            "missing_fields": list(self.missing_fields),
            "required_missing_fields": list(self.required_missing_fields),
            "recommended_missing_fields": list(self.recommended_missing_fields),
            "follow_up_questions": list(self.follow_up_questions),
            "contextual_follow_up_questions": list(self.contextual_follow_up_questions),
            "command": list(self.command),
            "publish_result": self.publish_result,
            "map_report": self.map_report,
            "map_assessments": dict(self.map_assessments),
            "map_verification_links": dict(self.map_verification_links),
            "publish_facts": dict(self.publish_facts),
            "area_conversion_warnings": list(self.area_conversion_warnings),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
        }


@dataclass
class PreflightCheck:
    name: str
    ok: bool
    message: str
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PreflightReport:
    ok: bool
    skill_root: str | None
    selected_runner: str | None
    checks: list[PreflightCheck] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    source_name: str | None = None
    runtime_mode: str | None = None
    detail_supported: bool | None = None
    logged_in: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "skill_root": self.skill_root,
            "selected_runner": self.selected_runner,
            "checks": [check.to_dict() for check in self.checks],
            "warnings": list(self.warnings),
            "source_name": self.source_name,
            "runtime_mode": self.runtime_mode,
            "detail_supported": self.detail_supported,
            "logged_in": self.logged_in,
        }


@dataclass
class RawListingSnapshot:
    id: str
    listing_id: str | None
    title: str
    price: str | None
    location: str | None
    url: str | None
    image_url: str | None
    images: list[str] = field(default_factory=list)
    description: str | None = None
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    geo_precision: str | None = None
    posted_time: str | None = None
    seller_name: str | None = None
    category: str | None = None
    detail_fetched: bool = False
    monthly_price_value: float | None = None
    price_value: float | None = None
    price_currency: str | None = None
    price_period: str | None = None
    inferred_bedrooms: float | None = None
    image_count: int = 0
    has_placeholder_image: bool = False
    raw: dict[str, Any] = field(default_factory=dict)

    def to_map_listing(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "listing_id": self.listing_id,
            "title": self.title,
            "price": self.price,
            "location": self.location,
            "url": self.url,
            "image_url": self.image_url,
            "description": self.description,
            "address": self.address,
            "lat": self.lat,
            "lng": self.lng,
            "geo_precision": self.geo_precision,
        }

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CandidateDecisionRow:
    source_id: str
    candidate_name: str
    status: str
    price: str
    location: str
    satisfied: list[str]
    missing_or_unknown: list[str]
    elimination_or_risk: list[str]
    listing_url: str
    map_verification_url: str | None = None
    map_assessment: dict[str, Any] = field(default_factory=dict)

    def to_display_row(self) -> dict[str, str]:
        return {
            "候选房源": self.candidate_name,
            "状态": self.status,
            "价格": self.price,
            "位置": self.location,
            "已满足": "；".join(self.satisfied) if self.satisfied else "无",
            "缺失/未知": "；".join(self.missing_or_unknown) if self.missing_or_unknown else "无",
            "淘汰原因/风险": "；".join(self.elimination_or_risk) if self.elimination_or_risk else "无",
            "房源链接": self.listing_url,
        }

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["display_row"] = self.to_display_row()
        return payload


@dataclass
class PipelineReport:
    request: SearchRequest
    preflight: PreflightReport
    selected_source: str | None = None
    selected_runtime_mode: str | None = None
    routing: dict[str, Any] = field(default_factory=dict)
    raw_listing_snapshots: list[RawListingSnapshot] = field(default_factory=list)
    map_report: dict[str, Any] | None = None
    candidate_rows: list[CandidateDecisionRow] = field(default_factory=list)
    hidden_candidates: list[dict[str, Any]] = field(default_factory=list)
    rendered_table: str = ""
    summary: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request.to_dict(),
            "preflight": self.preflight.to_dict(),
            "selected_source": self.selected_source,
            "selected_runtime_mode": self.selected_runtime_mode,
            "routing": dict(self.routing),
            "raw_listing_snapshots": [snapshot.to_dict() for snapshot in self.raw_listing_snapshots],
            "map_report": self.map_report,
            "candidate_rows": [row.to_dict() for row in self.candidate_rows],
            "hidden_candidates": list(self.hidden_candidates),
            "rendered_table": self.rendered_table,
            "summary": dict(self.summary),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
        }
