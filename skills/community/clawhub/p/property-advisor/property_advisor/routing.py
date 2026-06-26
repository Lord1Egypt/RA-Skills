from __future__ import annotations

import re
from dataclasses import dataclass, field, replace

from .analysis import safe_text, unique_strings
from .models import SearchRequest
from .source_registry import (
    candidate_sources_for_country,
    detect_source_signals,
    first_implemented_source,
    is_implemented_source,
    market_for_source,
    normalize_source_hint,
    unavailable_source_message,
)


UK_COUNTRY_TERMS = {
    "uk": 3,
    "u.k.": 3,
    "英国": 3,
    "england": 3,
    "scotland": 3,
    "wales": 3,
    "northern ireland": 3,
    "great britain": 3,
    "britain": 3,
    "united kingdom": 3,
}

UK_CITY_TERMS = {
    "london": 2,
    "manchester": 2,
    "birmingham": 2,
    "edinburgh": 2,
    "glasgow": 2,
    "liverpool": 2,
    "leeds": 2,
    "bristol": 2,
    "cambridge": 2,
    "oxford": 2,
    "nottingham": 2,
    "leicester": 2,
    "southampton": 2,
    "newcastle": 2,
    "sheffield": 2,
    "coventry": 2,
    "new malden": 2,
    "hayes": 2,
    "westminster": 2,
    "kensington": 2,
    "chelsea": 2,
    "canary wharf": 2,
    "croydon": 2,
    "islington": 2,
    "hackney": 2,
}

UK_ENTITY_TERMS = {
    "ofsted": 2,
    "council tax": 2,
    "tube": 2,
    "overground": 2,
    "gumtree": 2,
    "ucl": 2,
    "imperial college": 2,
    "kcl": 2,
    "king's college london": 2,
    "lse": 2,
    "university of oxford": 2,
    "university of cambridge": 2,
    "university of manchester": 2,
    "queen mary": 2,
}

NON_UK_TERMS = {
    "australia": 3,
    "melbourne": 3,
    "sydney": 3,
    "brisbane": 3,
    "perth": 3,
    "singapore": 3,
    "hong kong": 3,
    "dubai": 3,
    "abu dhabi": 3,
    "new zealand": 3,
    "auckland": 3,
    "canada": 3,
    "toronto": 3,
    "vancouver": 3,
    "united states": 3,
    "usa": 3,
    "new york": 3,
    "san francisco": 3,
}

UK_POSTCODE_RE = re.compile(r"\b([A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b", re.IGNORECASE)


@dataclass
class RoutingDecision:
    market: str | None
    reason: str
    source_id: str = ""
    search_location_hint: str = ""
    normalized_country: str = ""
    normalized_city: str = ""
    candidate_source_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    uk_signals: list[str] = field(default_factory=list)
    non_uk_signals: list[str] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "market": self.market,
            "reason": self.reason,
            "source_id": self.source_id,
            "search_location_hint": self.search_location_hint,
            "normalized_country": self.normalized_country,
            "normalized_city": self.normalized_city,
            "candidate_source_ids": list(self.candidate_source_ids),
            "warnings": list(self.warnings),
            "uk_signals": list(self.uk_signals),
            "non_uk_signals": list(self.non_uk_signals),
            "error": self.error,
        }


def apply_market_routing(request: SearchRequest) -> tuple[SearchRequest, RoutingDecision]:
    decision = route_search_request(request)
    routed = replace(request)
    routed.resolved_market = decision.market or ""
    routed.resolved_source_id = decision.source_id or decision.market or ""
    routed.routing_reason = decision.reason
    routed.search_location_hint = decision.search_location_hint
    if decision.market == "gt":
        if routed.country_is_default or not safe_text(routed.country):
            routed.country = decision.normalized_country or "united kingdom"
        if routed.city_is_default:
            routed.city = decision.normalized_city
    return routed, decision


def route_search_request(request: SearchRequest) -> RoutingDecision:
    requested_source = normalize_source_hint(request.source_hint)
    if requested_source != "auto":
        source_market = market_for_source(requested_source)
        if source_market and is_implemented_source(requested_source):
            location_hint = _extract_uk_location(request) if source_market == "gt" else ""
            return RoutingDecision(
                market=source_market,
                source_id=requested_source,
                reason=f"user_source_override:{requested_source}",
                search_location_hint=location_hint or ("uk" if source_market == "gt" else ""),
                normalized_country="united kingdom" if source_market == "gt" else (safe_text(request.country) or "australia"),
                normalized_city=_normalize_gt_city(request, location_hint) if source_market == "gt" else safe_text(request.city),
                candidate_source_ids=[requested_source],
            )
        return RoutingDecision(
            market=None,
            source_id=requested_source,
            reason=f"user_source_override:{requested_source}",
            normalized_country=safe_text(request.country),
            normalized_city=safe_text(request.city),
            candidate_source_ids=[requested_source],
            error=unavailable_source_message(requested_source),
        )

    requested_market = safe_text(request.market_hint).lower() or "auto"
    if requested_market == "ok":
        return RoutingDecision(
            market="ok",
            source_id="ok",
            reason="user_market_override:ok",
            normalized_country=safe_text(request.country) or "australia",
            normalized_city=safe_text(request.city),
            candidate_source_ids=["ok"],
        )
    if requested_market == "gt":
        location_hint = _extract_uk_location(request)
        return RoutingDecision(
            market="gt",
            source_id="gt",
            reason="user_market_override:gt",
            search_location_hint=location_hint or "uk",
            normalized_country="united kingdom",
            normalized_city=_normalize_gt_city(request, location_hint),
            candidate_source_ids=["gt"],
        )

    route_text = " ".join(
        part
        for part in (
            safe_text(request.keyword),
            safe_text(request.query_text),
            safe_text(request.country) if not request.country_is_default else "",
            safe_text(request.city) if not request.city_is_default else "",
            safe_text(request.destination),
            " ".join(safe_text(item) for item in request.user_priorities),
        )
        if part
    )
    lowered = route_text.lower()
    source_signals = detect_source_signals(route_text)
    explicit_external_sources = [
        source_id
        for source_id in source_signals
        if source_id not in {"ok", "gt"}
    ]
    if len(explicit_external_sources) == 1:
        source_id = explicit_external_sources[0]
        return RoutingDecision(
            market=market_for_source(source_id),
            source_id=source_id,
            reason=f"source_semantic_match:{source_id}",
            normalized_country=safe_text(request.country),
            normalized_city=safe_text(request.city),
            candidate_source_ids=source_signals,
            error=None if is_implemented_source(source_id) else unavailable_source_message(source_id),
        )
    if len(explicit_external_sources) > 1:
        return RoutingDecision(
            market=None,
            source_id="",
            reason="multiple_external_sources_requested",
            normalized_country=safe_text(request.country),
            normalized_city=safe_text(request.city),
            candidate_source_ids=source_signals,
            error="检测到多个尚未接入的外部房源平台，请明确本轮要使用哪个数据源。",
        )

    uk_signals, uk_score = _collect_signals(lowered, UK_COUNTRY_TERMS)
    city_signals, city_score = _collect_signals(lowered, UK_CITY_TERMS)
    entity_signals, entity_score = _collect_signals(lowered, UK_ENTITY_TERMS)
    postcode_match = UK_POSTCODE_RE.search(route_text.upper())
    if postcode_match:
        uk_signals.append(f"uk_postcode:{postcode_match.group(1).upper()}")
        uk_score += 3
    uk_signals.extend(city_signals)
    uk_signals.extend(entity_signals)
    uk_score += city_score + entity_score

    non_uk_signals, non_uk_score = _collect_signals(lowered, NON_UK_TERMS)
    uk_signals = unique_strings(uk_signals)
    non_uk_signals = unique_strings(non_uk_signals)
    if uk_score >= 2 and non_uk_score >= 2:
        return RoutingDecision(
            market=None,
            reason="mixed_geography_conflict",
            source_id="",
            search_location_hint="",
            normalized_country="",
            normalized_city="",
            candidate_source_ids=[],
            uk_signals=uk_signals,
            non_uk_signals=non_uk_signals,
            error="检测到英国与非英国地理信号同时存在，请明确指定英国市场还是其他市场。",
        )
    if uk_score >= 2:
        location_hint = _extract_uk_location(request, postcode_match.group(1).upper() if postcode_match else "")
        return RoutingDecision(
            market="gt",
            source_id="gt",
            reason="uk_semantic_match",
            search_location_hint=location_hint or "uk",
            normalized_country="united kingdom",
            normalized_city=_normalize_gt_city(request, location_hint),
            candidate_source_ids=candidate_sources_for_country("united kingdom"),
            uk_signals=uk_signals,
            non_uk_signals=non_uk_signals,
        )
    country = safe_text(request.country) or "australia"
    candidate_sources = candidate_sources_for_country(country)
    selected_source = first_implemented_source(candidate_sources)
    return RoutingDecision(
        market=market_for_source(selected_source) or "ok",
        source_id=selected_source,
        reason="default_non_uk_route",
        normalized_country=safe_text(request.country) or "australia",
        normalized_city=safe_text(request.city),
        candidate_source_ids=candidate_sources,
        uk_signals=uk_signals,
        non_uk_signals=non_uk_signals,
    )


def _collect_signals(text: str, weights: dict[str, int]) -> tuple[list[str], int]:
    matches: list[str] = []
    score = 0
    for term, weight in weights.items():
        if term in text:
            matches.append(term)
            score += weight
    return matches, score


def _extract_uk_location(request: SearchRequest, postcode: str = "") -> str:
    if postcode:
        return postcode
    raw_city = safe_text(request.city)
    if raw_city and raw_city.lower() in UK_CITY_TERMS:
        return raw_city
    text = " ".join(
        part
        for part in (safe_text(request.keyword), safe_text(request.query_text), safe_text(request.destination))
        if part
    ).lower()
    for term in UK_CITY_TERMS:
        if term in text:
            return term.title()
    match = UK_POSTCODE_RE.search(text.upper())
    if match:
        return match.group(1).upper()
    return ""


def _normalize_gt_city(request: SearchRequest, location_hint: str) -> str:
    raw_city = safe_text(request.city)
    if raw_city and raw_city.lower() in UK_CITY_TERMS:
        return raw_city
    if location_hint and not UK_POSTCODE_RE.fullmatch(location_hint.upper()):
        return location_hint
    return ""
