from __future__ import annotations

import json
import re
from dataclasses import replace
from pathlib import Path
from typing import Any

from .analysis import safe_text, unique_strings
from .models import (
    IntentDecision,
    ListingStrengthProfile,
    PreflightCheck,
    PreflightReport,
    PublishPropertyReport,
    PublishPropertyRequest,
    SearchRequest,
)
from .routing import route_search_request


CONSUMER_SEARCH = "consumer_search"
BUSINESS_PUBLISH = "business_publish"
CLARIFY = "clarify"
READINESS_BLOCKED_REQUIRED = "blocked_required"
READINESS_THIN_BUT_PUBLISHABLE = "thin_but_publishable"
READINESS_READY_TO_PREVIEW = "ready_to_preview"
READINESS_READY_TO_SUBMIT = "ready_to_submit"

_SQM_TO_SQFT = 10.7639
_AREA_UNIT_SQM = "sqm"
_AREA_UNIT_SQFT = "sqft"

_CHINESE_NUMBERS = {
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}

_SALE_TERMS = ("出售", "卖房", "售卖", "for sale", "sell", "sale", "selling")
_RENT_TERMS = ("出租", "放租", "招租", "for rent", "rent out", "lease out", "rental listing")
_PUBLISH_TERMS = (
    "发布",
    "发房源",
    "发帖",
    "房产广告",
    "房源广告",
    "post listing",
    "publish",
    "advertise",
    "listing",
    "房东",
    "中介",
)
_SEARCH_TERMS = (
    "找房",
    "找 ",
    "帮我找",
    "看看",
    "筛选",
    "比较",
    "推荐",
    "search",
    "look for",
    "looking for",
    "find",
)

_COUNTRY_HINTS = {
    "dubai": ("uae", "ae"),
    "迪拜": ("uae", "ae"),
    "uae": ("uae", "ae"),
    "united arab emirates": ("uae", "ae"),
    "emirates": ("uae", "ae"),
    "singapore": ("singapore", "sg"),
    "新加坡": ("singapore", "sg"),
    "melbourne": ("australia", "au"),
    "墨尔本": ("australia", "au"),
    "sydney": ("australia", "au"),
    "悉尼": ("australia", "au"),
    "australia": ("australia", "au"),
    "澳洲": ("australia", "au"),
    "澳大利亚": ("australia", "au"),
    "london": ("uk", "gb"),
    "伦敦": ("uk", "gb"),
    "united kingdom": ("uk", "gb"),
    "uk": ("uk", "gb"),
    "hong kong": ("hong_kong", "hk"),
    "japan": ("japan", "jp"),
    "tokyo": ("japan", "jp"),
    "usa": ("usa", "us"),
    "united states": ("usa", "us"),
    "canada": ("canada", "ca"),
    "new zealand": ("new_zealand", "nz"),
    "malaysia": ("malaysia", "my"),
}

_KNOWN_LOCATIONS = (
    "Dubai Marina",
    "Downtown Dubai",
    "Business Bay",
    "Jumeirah Village Circle",
    "Palm Jumeirah",
    "Dubai",
    "迪拜",
    "Melbourne",
    "墨尔本",
    "Southbank",
    "Sydney",
    "悉尼",
    "Singapore",
    "新加坡",
    "London",
    "伦敦",
    "Canary Wharf",
    "Richmond",
)

_PROPERTY_TYPE_ALIASES = {
    "apartment": ("apartment", "flat", "unit", "公寓"),
    "villa": ("villa", "别墅"),
    "townhouse": ("townhouse", "town house", "联排"),
    "land": ("land", "土地", "地块"),
    "other": ("house", "studio", "房子", "住宅"),
}

_STRENGTH_RULES = (
    (("near metro", "metro", "地铁", "train", "tram", "tube", "station"), "交通便利，靠近公共交通", (), (), ()),
    (("furnished", "家具", "拎包入住", "ready to move", "ready-to-move"), "家具齐全，可拎包入住", ("Furnished",), (), ()),
    (("bright", "采光", "阳光", "sunny"), "采光条件好", (), (), ()),
    (("balcony", "阳台"), "带阳台", ("Balcony",), (), ()),
    (("view", "景观", "sea view", "city view"), "景观视野好", (), (), ()),
    (("parking", "车位", "garage"), "停车便利", ("Covered Parking",), (), ()),
    (("pool", "泳池", "swimming"), "配套泳池", (), ("Swimming Pool",), ()),
    (("gym", "健身"), "配套健身房", (), ("Gym",), ()),
    (("security", "安保", "保安"), "安保配套", (), ("Security",), ()),
    (("school", "学校", "university", "大学"), "适合学生或家庭，周边教育资源便利", (), (), ("学生", "家庭")),
    (("family", "家庭", "kids"), "适合家庭居住", (), (), ("家庭",)),
    (("invest", "投资", "yield", "回报"), "具备投资展示价值", (), (), ("投资买家",)),
)

_FIELD_QUESTIONS = {
    "mode": "这套房源是要出售还是出租？",
    "country_or_subdomain": "要发布到哪个 OK 国家站或子域？例如 uae/ae、australia/au、singapore/sg。",
    "property_type": "房源类型是什么？例如 apartment、villa、townhouse、land 或 other。",
    "location": "房源位置在哪里？请给区域或可用于平台地点选择的地址关键词。",
    "price": "价格是多少？出租请说明周期，例如 8000/month；出售请给总价。",
    "contact": "发布时使用哪个联系电话或 WhatsApp？",
    "images": "请提供至少一张本地图片绝对路径，例如 /Users/a58/Desktop/house/1.jpg。",
    "image_paths_absolute": "图片需要是本地绝对路径，不能是相对路径或远程 URL。",
    "property_type_supported_for_rent": "出租暂不支持 land，请改为可出租的类型，或确认这是否应按出售发布。",
    "category_id": "GT 发布需要 Gumtree category_id；请提供分类 ID，或先只生成 OK 发布草稿。",
    "postcode": "GT/英国发布需要 postcode，用于 Gumtree 位置和地图复核。",
    "address": "请补充更具体地址或楼名；如果不方便提供，至少给区域和 postcode。",
    "publish_endpoint": "如需真实发布到 Gumtree，请确认 session 中已有 publish_endpoint，或提供 --publish-endpoint。",
}


def classify_user_intent(query_text: str, *, mode_hint: str = "auto", market_hint: str = "auto") -> IntentDecision:
    text = safe_text(query_text)
    lowered = text.lower()
    mode = infer_publish_mode(text, mode_hint=mode_hint)
    publish_signals = _collect_terms(lowered, _PUBLISH_TERMS)
    if mode:
        publish_signals.append(f"mode:{mode}")
    if re.search(r"(我要|我想|帮我|please|帮忙).{0,8}(出租|出售|卖房|发房源|发布)", text, re.IGNORECASE):
        publish_signals.append("owner_publish_phrase")
    if re.search(r"(出租|出售).{0,12}(一套|我的|房源|公寓|别墅|apartment|villa|flat)", text, re.IGNORECASE):
        publish_signals.append("listing_owner_action")

    search_signals = _collect_terms(lowered, _SEARCH_TERMS)
    if re.search(r"(找|寻找|search|look for|find).{0,12}(租房|房源|apartment|flat|studio)", text, re.IGNORECASE):
        search_signals.append("consumer_search_phrase")

    publish_signals = unique_strings(publish_signals)
    search_signals = unique_strings(search_signals)
    requested_market = safe_text(market_hint).lower()

    if publish_signals and search_signals:
        return IntentDecision(
            intent=CLARIFY,
            reason="mixed_consumer_and_business_signals",
            mode=mode,
            market=requested_market,
            signals=publish_signals + search_signals,
            error="检测到找房和发布房源信号同时存在，需要先确认用户目标。",
        )
    if publish_signals:
        return IntentDecision(
            intent=BUSINESS_PUBLISH,
            reason="business_publish_signals",
            mode=mode,
            market=_resolve_publish_market(market_hint),
            signals=publish_signals,
        )
    return IntentDecision(
        intent=CONSUMER_SEARCH,
        reason="default_consumer_search",
        mode=mode,
        market=_resolve_publish_market(market_hint),
        signals=search_signals,
    )


def infer_publish_mode(query_text: str, *, mode_hint: str = "auto") -> str:
    explicit = safe_text(mode_hint).lower()
    if explicit in {"sale", "rent"}:
        return explicit
    lowered = safe_text(query_text).lower()
    sale = any(term in lowered for term in _SALE_TERMS)
    rent = any(term in lowered for term in _RENT_TERMS)
    if sale and not rent:
        return "sale"
    if rent and not sale:
        return "rent"
    return ""


def build_publish_request_from_payload(payload: dict[str, Any]) -> PublishPropertyRequest:
    allowed = PublishPropertyRequest.__dataclass_fields__
    values = {key: value for key, value in payload.items() if key in allowed}
    return PublishPropertyRequest(**values)


def infer_publish_request(
    *,
    query_text: str = "",
    market_hint: str = "auto",
    mode: str = "auto",
    country: str = "",
    subdomain: str = "",
    property_type: str = "",
    title: str = "",
    description: str = "",
    price: str | None = None,
    location: str = "",
    images: list[str] | None = None,
    floor_plans: list[str] | None = None,
    rental_type: str = "entire",
    rent_period: str | None = None,
    bedrooms: str | None = None,
    bathrooms: str | None = None,
    car_spaces: str | None = None,
    floor_level: str | None = None,
    floor: str | None = None,
    area_size: str | None = None,
    phone: str | None = None,
    whatsapp: str | None = None,
    unit_features: list[str] | None = None,
    amenities: list[str] | None = None,
    property_services: list[str] | None = None,
    contact_name: str | None = None,
    contact_email: str | None = None,
    category_id: str | None = None,
    postcode: str | None = None,
    address: str | None = None,
    publish_endpoint: str | None = None,
    area_unit: str | None = None,
    lang: str = "en",
) -> PublishPropertyRequest:
    text = safe_text(query_text)
    inferred_country, inferred_subdomain = _infer_country(text)
    resolved_country = safe_text(country) or inferred_country
    resolved_subdomain = safe_text(subdomain) or ""
    resolved_type = safe_text(property_type) or _infer_property_type(text) or "apartment"
    inferred_area_value, inferred_area_unit = _infer_area_detail(text)
    resolved_area, original_area, resolved_area_unit, _area_warnings = _normalize_area_fields(
        safe_text(area_size) or inferred_area_value,
        safe_text(area_unit) or inferred_area_unit,
    )
    return PublishPropertyRequest(
        mode=infer_publish_mode(text, mode_hint=mode),
        country=resolved_country,
        subdomain=resolved_subdomain,
        property_type=resolved_type,
        title=safe_text(title),
        description=safe_text(description),
        price=safe_text(price) or _infer_price(text),
        location=safe_text(location) or _infer_location(text),
        images=images or [],
        floor_plans=floor_plans or [],
        rental_type=safe_text(rental_type) or "entire",
        rent_period=safe_text(rent_period) or _infer_rent_period(text),
        bedrooms=safe_text(bedrooms) or _infer_bedrooms(text),
        bathrooms=safe_text(bathrooms) or _infer_bathrooms(text),
        car_spaces=safe_text(car_spaces) or _infer_car_spaces(text),
        floor_level=safe_text(floor_level) or None,
        floor=safe_text(floor) or None,
        area_size=resolved_area,
        phone=safe_text(phone) or _infer_phone(text),
        whatsapp=safe_text(whatsapp) or None,
        unit_features=unit_features or [],
        amenities=amenities or [],
        property_services=property_services or [],
        contact_name=safe_text(contact_name) or None,
        contact_email=safe_text(contact_email) or _infer_email(text),
        category_id=safe_text(category_id) or None,
        postcode=safe_text(postcode) or _infer_postcode(text),
        address=safe_text(address) or None,
        publish_endpoint=safe_text(publish_endpoint) or None,
        original_area_size=original_area,
        area_unit=resolved_area_unit,
        lang=safe_text(lang) or "en",
        query_text=text,
        market_hint=safe_text(market_hint) or "auto",
        resolved_market=_resolve_publish_market(market_hint),
    )


class PublishPropertyOrchestrator:
    def __init__(
        self,
        ok_client: Any | None = None,
        gt_client: Any | None = None,
        map_client: Any | None = None,
        *,
        ok_skill_root: str | None = None,
        gt_skill_root: str | None = None,
    ) -> None:
        self.ok_client = ok_client
        self.gt_client = gt_client
        self.map_client = map_client
        self.ok_skill_root = ok_skill_root
        self.gt_skill_root = gt_skill_root

    def publish(
        self,
        request: PublishPropertyRequest,
        *,
        confirm_submit: bool = False,
        save_draft: bool = False,
        dry_run: bool = False,
    ) -> PublishPropertyReport:
        request, area_conversion_warnings = normalize_publish_request(request)
        intent = classify_user_intent(
            request.query_text,
            mode_hint=request.mode or "auto",
            market_hint=request.market_hint or request.resolved_market or "auto",
        )
        if not request.query_text and (request.mode or request.price or request.location):
            intent.intent = BUSINESS_PUBLISH
            intent.reason = "structured_publish_request"

        market, route_payload = route_publish_market(request)
        route_warnings = list(route_payload.get("warnings") or [])
        if route_payload.get("error"):
            intent.intent = CLARIFY
            intent.reason = safe_text(route_payload.get("reason")) or "publish_market_routing_error"
            intent.error = safe_text(route_payload.get("error"))
            intent.warnings = unique_strings(intent.warnings + route_warnings)

        prepared = replace(request, resolved_market=market)
        strength_profile = extract_listing_strengths(prepared)
        prepared = enrich_publish_request(prepared, strength_profile, map_assessments={})
        missing, recommended, validation_warnings = validate_publish_request(
            prepared,
            confirm_submit=confirm_submit,
            market=market,
        )
        map_report: dict[str, Any] | None = None
        map_assessments: dict[str, Any] = {}
        map_links: dict[str, str] = {}
        map_warnings: list[str] = []
        if not missing and intent.intent not in {CONSUMER_SEARCH, CLARIFY}:
            map_report, map_assessments, map_links, map_warnings = self._run_publish_map(prepared)
            if map_assessments:
                prepared = enrich_publish_request(prepared, strength_profile, map_assessments=map_assessments)
                missing, recommended, validation_warnings = validate_publish_request(
                    prepared,
                    confirm_submit=confirm_submit,
                    market=market,
                )
        readiness = determine_publish_readiness(
            missing,
            recommended,
            confirm_submit=confirm_submit,
        )
        questions = build_contextual_follow_up_questions(
            prepared,
            required_missing=missing,
            recommended_missing=recommended,
            market=market,
            readiness=readiness,
        )
        publish_facts = build_publish_facts(prepared, strength_profile, map_assessments)
        warnings = unique_strings(list(validation_warnings) + route_warnings + map_warnings)

        if intent.intent == CONSUMER_SEARCH and request.query_text:
            return PublishPropertyReport(
                request=prepared,
                intent=intent,
                strength_profile=strength_profile,
                generated_title=prepared.title,
                generated_description=prepared.description,
                readiness_status=readiness,
                missing_fields=missing,
                required_missing_fields=missing,
                recommended_missing_fields=recommended,
                follow_up_questions=questions,
                contextual_follow_up_questions=questions,
                map_report=map_report,
                map_assessments=map_assessments,
                map_verification_links=map_links,
                publish_facts=publish_facts,
                area_conversion_warnings=area_conversion_warnings,
                warnings=warnings,
                errors=["当前请求更像 C 端找房，请改用 search 流程或明确说明要发布房源。"],
            )

        if intent.intent == CLARIFY:
            return PublishPropertyReport(
                request=prepared,
                intent=intent,
                strength_profile=strength_profile,
                generated_title=prepared.title,
                generated_description=prepared.description,
                readiness_status=readiness,
                missing_fields=missing,
                required_missing_fields=missing,
                recommended_missing_fields=recommended,
                follow_up_questions=questions or ["请确认这次是要找房，还是要发布自己的出租/出售房源？"],
                contextual_follow_up_questions=questions,
                map_report=map_report,
                map_assessments=map_assessments,
                map_verification_links=map_links,
                publish_facts=publish_facts,
                area_conversion_warnings=area_conversion_warnings,
                warnings=warnings,
                errors=[intent.error or "发布意图不明确。"],
            )

        if missing:
            return PublishPropertyReport(
                request=prepared,
                intent=intent,
                strength_profile=strength_profile,
                generated_title=prepared.title,
                generated_description=prepared.description,
                readiness_status=readiness,
                missing_fields=missing,
                required_missing_fields=missing,
                recommended_missing_fields=recommended,
                follow_up_questions=questions,
                contextual_follow_up_questions=questions,
                map_report=map_report,
                map_assessments=map_assessments,
                map_verification_links=map_links,
                publish_facts=publish_facts,
                area_conversion_warnings=area_conversion_warnings,
                warnings=warnings,
                errors=["发布资料不完整，已停止调用发布命令。"],
            )

        try:
            publisher = self._publisher_for_market(market)
        except Exception as exc:
            source_name = "gt-core-skill" if market == "gt" else "ok-core-skill"
            preflight = PreflightReport(
                ok=False,
                skill_root=self.gt_skill_root if market == "gt" else self.ok_skill_root,
                selected_runner=None,
                warnings=[str(exc)],
                source_name=source_name,
                runtime_mode=market,
            )
            return PublishPropertyReport(
                request=prepared,
                intent=intent,
                strength_profile=strength_profile,
                preflight=preflight,
                selected_source=source_name,
                selected_runtime_mode=market,
                generated_title=prepared.title,
                generated_description=prepared.description,
                readiness_status=readiness,
                missing_fields=missing,
                required_missing_fields=missing,
                recommended_missing_fields=recommended,
                follow_up_questions=questions,
                contextual_follow_up_questions=questions,
                map_report=map_report,
                map_assessments=map_assessments,
                map_verification_links=map_links,
                publish_facts=publish_facts,
                area_conversion_warnings=area_conversion_warnings,
                warnings=warnings + [str(exc)],
                errors=[f"{source_name} runtime unavailable: {exc}"],
            )
        preflight = self._doctor(publisher, dry_run=dry_run)
        if not preflight.ok:
            return PublishPropertyReport(
                request=prepared,
                intent=intent,
                strength_profile=strength_profile,
                preflight=preflight,
                selected_source=getattr(publisher, "source_name", None),
                selected_runtime_mode=getattr(publisher, "runtime_mode", None),
                generated_title=prepared.title,
                generated_description=prepared.description,
                readiness_status=readiness,
                missing_fields=missing,
                required_missing_fields=missing,
                recommended_missing_fields=recommended,
                follow_up_questions=questions,
                contextual_follow_up_questions=questions,
                map_report=map_report,
                map_assessments=map_assessments,
                map_verification_links=map_links,
                publish_facts=publish_facts,
                area_conversion_warnings=area_conversion_warnings,
                warnings=warnings + list(preflight.warnings),
                errors=[f"{preflight.source_name or 'publisher'} preflight failed; fix runtime before publishing."],
            )

        try:
            result = publisher.publish_property(
                prepared,
                submit=confirm_submit,
                save_draft=save_draft,
                dry_run=dry_run,
            )
        except Exception as exc:
            return PublishPropertyReport(
                request=prepared,
                intent=intent,
                strength_profile=strength_profile,
                preflight=preflight,
                selected_source=getattr(publisher, "source_name", None),
                selected_runtime_mode=getattr(publisher, "runtime_mode", None),
                generated_title=prepared.title,
                generated_description=prepared.description,
                readiness_status=readiness,
                missing_fields=missing,
                required_missing_fields=missing,
                recommended_missing_fields=recommended,
                follow_up_questions=questions,
                contextual_follow_up_questions=questions,
                command=getattr(publisher, "last_command", []) or [],
                map_report=map_report,
                map_assessments=map_assessments,
                map_verification_links=map_links,
                publish_facts=publish_facts,
                area_conversion_warnings=area_conversion_warnings,
                warnings=warnings + list(preflight.warnings),
                errors=[str(exc)],
            )

        return PublishPropertyReport(
            request=prepared,
            intent=intent,
            strength_profile=strength_profile,
            preflight=preflight,
            selected_source=getattr(publisher, "source_name", None),
            selected_runtime_mode=getattr(publisher, "runtime_mode", None),
            generated_title=prepared.title,
            generated_description=prepared.description,
            readiness_status=readiness,
            missing_fields=missing,
            required_missing_fields=missing,
            recommended_missing_fields=recommended,
            follow_up_questions=questions,
            contextual_follow_up_questions=questions,
            command=getattr(publisher, "last_command", []) or [],
            publish_result=result,
            map_report=map_report,
            map_assessments=map_assessments,
            map_verification_links=map_links,
            publish_facts=publish_facts,
            area_conversion_warnings=area_conversion_warnings,
            warnings=unique_strings(warnings + list(preflight.warnings)),
            errors=[] if _publish_result_ok(result) else [safe_text(result.get("error")) or "发布命令返回失败。"],
        )

    def _publisher_for_market(self, market: str) -> Any:
        if market == "gt":
            if self.gt_client is None:
                from .gt_client import GTPublishSkillClient

                self.gt_client = GTPublishSkillClient(skill_root=self.gt_skill_root or None)
            return self.gt_client
        if self.ok_client is None:
            from .ok_client import OKCoreSkillClient

            self.ok_client = OKCoreSkillClient(skill_root=self.ok_skill_root or None)
        return self.ok_client

    def _doctor(self, publisher: Any, *, dry_run: bool) -> PreflightReport:
        if hasattr(publisher, "doctor"):
            return publisher.doctor(run_browser_smoke=not dry_run)
        return PreflightReport(
            ok=True,
            skill_root=None,
            selected_runner="injected",
            checks=[PreflightCheck(name="injected_publisher", ok=True, message="Using injected publisher.")],
            source_name=getattr(publisher, "source_name", "injected"),
            runtime_mode=getattr(publisher, "runtime_mode", "injected"),
        )

    def _run_publish_map(
        self,
        request: PublishPropertyRequest,
    ) -> tuple[dict[str, Any] | None, dict[str, Any], dict[str, str], list[str]]:
        location_text = _publish_location_for_map(request)
        if not location_text:
            return None, {}, {}, []
        if self.map_client is False:
            return None, {}, {}, ["地图增强已被调用方禁用。"]
        map_client = self.map_client
        if map_client is None:
            from .map_client import PublicOsmMapClient

            map_client = PublicOsmMapClient()
            self.map_client = map_client
        try:
            doctor = map_client.doctor()
        except Exception as exc:
            return None, {}, {}, [f"地图 skill doctor 失败：{exc}"]
        if doctor.get("status") != "ok":
            return doctor, {}, {}, ["地图 skill doctor 未通过，本轮发布文案不加入地图结论。"]
        listing = {
            "id": "publish_draft",
            "title": request.title or generate_listing_title(request, ListingStrengthProfile()),
            "price": request.price,
            "location": request.location or request.postcode or request.address,
            "address": request.address or request.postcode,
            "description": request.query_text or request.description,
            "url": None,
            "image_url": request.images[0] if request.images else None,
        }
        try:
            report = map_client.analyze_batch(
                listings=[listing],
                destination="",
                city=request.location or request.postcode or "",
            )
        except Exception as exc:
            return None, {}, {}, [f"地图增强失败，本轮发布文案不加入地图结论：{exc}"]
        items = [item for item in report.get("listings", []) if isinstance(item, dict)]
        if not items:
            return report, {}, {}, ["地图增强未返回 listing 结果，本轮发布文案不加入地图结论。"]
        first = items[0]
        assessments = first.get("assessments") if isinstance(first.get("assessments"), dict) else {}
        links = first.get("verification_links") if isinstance(first.get("verification_links"), dict) else {}
        return report, dict(assessments), {str(k): safe_text(v) for k, v in links.items() if safe_text(v)}, []


def extract_listing_strengths(request: PublishPropertyRequest) -> ListingStrengthProfile:
    text = " ".join(
        part
        for part in (
            request.query_text,
            " ".join(request.unit_features),
            " ".join(request.amenities),
            " ".join(request.property_services),
        )
        if safe_text(part)
    )
    lowered = text.lower()
    strengths: list[str] = []
    unit_features: list[str] = list(request.unit_features)
    amenities: list[str] = list(request.amenities)
    property_services: list[str] = list(request.property_services)
    target_audiences: list[str] = []
    source_phrases: list[str] = []
    for terms, strength, units, amens, audiences in _STRENGTH_RULES:
        matched = [term for term in terms if term in lowered]
        if not matched:
            continue
        strengths.append(strength)
        unit_features.extend(units)
        amenities.extend(amens)
        target_audiences.extend(audiences)
        source_phrases.extend(matched)
    return ListingStrengthProfile(
        strengths=unique_strings(strengths),
        unit_features=unique_strings(unit_features),
        amenities=unique_strings(amenities),
        property_services=unique_strings(property_services),
        target_audiences=unique_strings(target_audiences),
        source_phrases=unique_strings(source_phrases),
    )


def enrich_publish_request(
    request: PublishPropertyRequest,
    strength_profile: ListingStrengthProfile,
    *,
    map_assessments: dict[str, Any] | None = None,
) -> PublishPropertyRequest:
    mode = request.mode
    if mode == "rent" and not request.rent_period:
        request = replace(request, rent_period="month")
    title = generate_listing_title(request, strength_profile)
    description = generate_listing_description(request, strength_profile, map_assessments=map_assessments or {})
    return replace(
        request,
        title=title,
        description=description,
        unit_features=unique_strings(request.unit_features + strength_profile.unit_features),
        amenities=unique_strings(request.amenities + strength_profile.amenities),
        property_services=unique_strings(request.property_services + strength_profile.property_services),
    )


def generate_listing_title(request: PublishPropertyRequest, strength_profile: ListingStrengthProfile) -> str:
    property_label = _property_label(request.property_type)
    bed = _bedroom_title(request.bedrooms)
    lead = "For rent" if request.mode == "rent" else "For sale" if request.mode == "sale" else "Property"
    pieces = [lead]
    if "家具齐全，可拎包入住" in strength_profile.strengths and request.mode == "rent":
        pieces.append("furnished")
    if bed:
        pieces.append(bed)
    pieces.append(property_label)
    if request.location:
        pieces.append(f"in {request.location}")
    if "交通便利，靠近公共交通" in strength_profile.strengths:
        pieces.append("near transit")
    return " ".join(pieces)


def generate_listing_description(
    request: PublishPropertyRequest,
    strength_profile: ListingStrengthProfile,
    *,
    map_assessments: dict[str, Any] | None = None,
) -> str:
    intro_parts = []
    location_label = safe_text(request.address) or safe_text(request.location) or safe_text(request.postcode)
    if location_label:
        intro_parts.append(f"This {_property_label(request.property_type)} is located in {location_label}.")
    else:
        intro_parts.append(f"This {_property_label(request.property_type)} is available for {request.mode or 'listing'}.")
    if request.price:
        period = f" per {request.rent_period}" if request.mode == "rent" and request.rent_period else ""
        intro_parts.append(f"Price: {request.price}{period}.")
    details: list[str] = []
    if request.bedrooms:
        details.append(f"{request.bedrooms} bedroom(s)")
    if request.bathrooms:
        details.append(f"{request.bathrooms} bathroom(s)")
    if request.area_size:
        if request.original_area_size and request.area_unit == _AREA_UNIT_SQM:
            details.append(f"about {request.area_size} sqft ({request.original_area_size} sqm)")
        else:
            details.append(f"{request.area_size} sqft")
    if request.car_spaces:
        details.append(f"{request.car_spaces} car space(s)")
    if details:
        intro_parts.append("Key details: " + ", ".join(details) + ".")
    explicit_highlights = _explicit_highlights(strength_profile)
    if explicit_highlights:
        intro_parts.append("Owner-provided highlights: " + "; ".join(explicit_highlights) + ".")
    if strength_profile.target_audiences:
        intro_parts.append("Suitable for: " + ", ".join(strength_profile.target_audiences) + ".")
    map_copy = _map_assessments_to_copy(map_assessments or {})
    if map_copy:
        intro_parts.append("Public map screening: " + " ".join(map_copy))
    return " ".join(intro_parts)


def validate_publish_request(
    request: PublishPropertyRequest,
    *,
    confirm_submit: bool,
    market: str,
) -> tuple[list[str], list[str], list[str]]:
    missing: list[str] = []
    recommended: list[str] = []
    warnings: list[str] = []
    if request.mode not in {"sale", "rent"}:
        missing.append("mode")
    if not request.country and not request.subdomain and market == "ok":
        missing.append("country_or_subdomain")
    if not request.property_type:
        missing.append("property_type")
    if request.mode == "rent" and request.property_type == "land":
        missing.append("property_type_supported_for_rent")
    if not (request.location or request.address or request.postcode):
        missing.append("location")
    if not request.price:
        missing.append("price")
    if not (request.phone or request.whatsapp or request.contact_email):
        missing.append("contact")
    invalid_images = [path for path in request.images if _invalid_local_image_path(path)]
    if invalid_images:
        missing.append("image_paths_absolute")
    if confirm_submit and not request.images:
        missing.append("images")
    if market == "gt" and not request.category_id:
        missing.append("category_id")
    if market == "gt" and not request.postcode:
        missing.append("postcode")

    if not request.images:
        recommended.append("images")
        warnings.append("正式发布前建议至少提供一张本地图片绝对路径。")
    for field_name, value in (
        ("bedrooms", request.bedrooms),
        ("bathrooms", request.bathrooms),
        ("area_size", request.area_size),
    ):
        if not value:
            recommended.append(field_name)
    if request.mode == "rent" and not request.rent_period:
        recommended.append("rent_period")
    if market == "gt" and confirm_submit and not request.publish_endpoint:
        recommended.append("publish_endpoint")
    return unique_strings(missing), unique_strings(recommended), unique_strings(warnings)


def build_follow_up_questions(fields: list[str]) -> list[str]:
    questions = [_FIELD_QUESTIONS[field] for field in fields if field in _FIELD_QUESTIONS]
    return questions[:6]


def build_contextual_follow_up_questions(
    request: PublishPropertyRequest,
    *,
    required_missing: list[str],
    recommended_missing: list[str],
    market: str,
    readiness: str,
) -> list[str]:
    questions = build_follow_up_questions(required_missing)
    property_label = _property_label(request.property_type)
    if request.mode == "rent":
        if "bedrooms" in recommended_missing or "bathrooms" in recommended_missing or "area_size" in recommended_missing:
            questions.append(f"这套出租 {property_label} 的卧室数、卫浴数和面积分别是多少？")
        if "rent_period" in recommended_missing:
            questions.append("租金周期是按月、按周还是其他周期？")
        if not _has_any_strength(request, ("furnished", "家具", "拎包入住", "unfurnished", "不带家具")):
            questions.append("房源是 furnished、part-furnished 还是 unfurnished？")
        if not _has_any_strength(request, ("available", "入住", "可入住", "move in", "move-in")):
            questions.append("可入住时间是什么时候？押金和 bills 是否需要在描述中说明？")
    else:
        if "bedrooms" in recommended_missing or "bathrooms" in recommended_missing or "area_size" in recommended_missing:
            questions.append(f"这套出售 {property_label} 的卧室数、卫浴数和建筑面积分别是多少？")
        if not _has_any_strength(request, ("view", "balcony", "parking", "renovated", "景观", "阳台", "车位", "装修")):
            questions.append("是否有景观、阳台、车位、装修状态或其他明确卖点？")

    if not request.images:
        questions.append("是否有至少一张本地图片绝对路径？正式提交前通常需要图片。")
    if not (request.unit_features or request.amenities or request.property_services):
        questions.append("有哪些可以确认的楼内设施或房源特色？只写真实可确认项。")
    if request.location or request.address or request.postcode:
        questions.append("是否有你希望重点突出的交通、学校、商圈或生活配套？未确认的信息不会写入文案。")
    if market == "gt":
        if not request.postcode:
            questions.append("英国/Gumtree 发布需要 postcode，请补充完整或外码。")
        if not request.category_id:
            questions.append("请提供 Gumtree category_id，或提供你希望发布到的 Gumtree 分类名称供映射。")
        if not request.publish_endpoint:
            questions.append("如需真实发布，请确认 Gumtree session 已配置 publish_endpoint，或提供 --publish-endpoint。")
    limit = 6 if readiness == READINESS_BLOCKED_REQUIRED else 5
    return unique_strings(questions)[:limit]


def determine_publish_readiness(
    missing: list[str],
    recommended: list[str],
    *,
    confirm_submit: bool,
) -> str:
    if missing:
        return READINESS_BLOCKED_REQUIRED
    if confirm_submit:
        return READINESS_READY_TO_SUBMIT
    if recommended:
        return READINESS_THIN_BUT_PUBLISHABLE
    return READINESS_READY_TO_PREVIEW


def normalize_publish_request(request: PublishPropertyRequest) -> tuple[PublishPropertyRequest, list[str]]:
    unit = _normalize_area_unit(request.area_unit)
    if request.original_area_size and unit == _AREA_UNIT_SQM and request.area_size:
        return replace(request, area_unit=unit), [
            f"面积已从 {request.original_area_size} sqm 换算为约 {request.area_size} sqft。"
        ]
    normalized_area, original_area, normalized_unit, warnings = _normalize_area_fields(request.area_size, unit)
    if normalized_area == request.area_size and original_area == request.original_area_size and normalized_unit == request.area_unit:
        return request, warnings
    return replace(
        request,
        area_size=normalized_area,
        original_area_size=request.original_area_size or original_area,
        area_unit=normalized_unit,
    ), warnings


def route_publish_market(request: PublishPropertyRequest) -> tuple[str, dict[str, Any]]:
    explicit = safe_text(request.market_hint).lower()
    if explicit in {"ok"}:
        return "ok", {"market": "ok", "reason": "user_market_override:ok", "warnings": []}
    if explicit in {"gt", "gumtree"}:
        return "gt", {"market": "gt", "reason": "user_market_override:gt", "warnings": []}
    if safe_text(request.resolved_market).lower() in {"ok", "gt"} and explicit not in {"", "auto"}:
        market = safe_text(request.resolved_market).lower()
        return market, {"market": market, "reason": "resolved_market_override", "warnings": []}
    country = safe_text(request.country).lower()
    subdomain = safe_text(request.subdomain).lower()
    if country in {"uk", "gb", "united kingdom", "england", "scotland", "wales"} or subdomain in {"gb", "uk"}:
        return "gt", {"market": "gt", "reason": "uk_publish_country_match", "warnings": [], "uk_signals": [country or subdomain]}
    route_text = " ".join(
        part
        for part in (
            request.query_text,
            request.title,
            request.location,
            request.address or "",
            request.postcode or "",
            request.country,
            request.subdomain,
        )
        if safe_text(part)
    )
    decision = route_search_request(
        SearchRequest(
            keyword="",
            country=request.country,
            city=request.location,
            destination=request.address or request.postcode or "",
            query_text=route_text,
            market_hint="auto",
            country_is_default=not bool(safe_text(request.country)),
            city_is_default=not bool(safe_text(request.location)),
        )
    )
    payload = decision.to_dict()
    market = decision.market or ""
    if not market and decision.error:
        return "", payload
    return market or "ok", payload


def build_publish_facts(
    request: PublishPropertyRequest,
    strength_profile: ListingStrengthProfile,
    map_assessments: dict[str, Any],
) -> dict[str, Any]:
    return {
        "mode": request.mode,
        "market": request.resolved_market,
        "property_type": request.property_type,
        "price": request.price,
        "rent_period": request.rent_period,
        "location": request.location,
        "address": request.address,
        "postcode": request.postcode,
        "bedrooms": request.bedrooms,
        "bathrooms": request.bathrooms,
        "area_size": request.area_size,
        "original_area_size": request.original_area_size,
        "area_unit": request.area_unit,
        "unit_features": list(request.unit_features),
        "amenities": list(request.amenities),
        "property_services": list(request.property_services),
        "owner_provided_strengths": list(strength_profile.strengths),
        "map_assessment_keys": list(map_assessments.keys()),
        "description_policy": "generated_from_user_fields_and_map_assessments_only",
    }


def ok_publish_args(request: PublishPropertyRequest, *, submit: bool, save_draft: bool, dry_run: bool) -> list[str]:
    args = ["publish-property"]
    if request.country:
        args.extend(["--country", request.country])
    if request.subdomain:
        args.extend(["--subdomain", request.subdomain])
    args.extend(["--mode", request.mode])
    args.extend(["--property-type", request.property_type])
    args.extend(["--lang", request.lang])
    args.extend(["--title", request.title])
    args.extend(["--description", request.description])
    _add_optional(args, "--price", request.price)
    _add_optional(args, "--location", request.location)
    for image in request.images:
        args.extend(["--image", image])
    for floor_plan in request.floor_plans:
        args.extend(["--floor-plan", floor_plan])
    if request.mode == "rent":
        _add_optional(args, "--rental-type", request.rental_type or "entire")
        _add_optional(args, "--rent-period", request.rent_period or "month")
    _add_optional(args, "--bedrooms", request.bedrooms)
    _add_optional(args, "--bathrooms", request.bathrooms)
    if request.mode == "sale":
        _add_optional(args, "--car-spaces", request.car_spaces)
    _add_optional(args, "--floor-level", request.floor_level)
    _add_optional(args, "--floor", request.floor)
    _add_optional(args, "--area-size", request.area_size)
    _add_optional(args, "--phone", request.phone)
    _add_optional(args, "--whatsapp", request.whatsapp)
    for value in request.unit_features:
        args.extend(["--unit-feature", value])
    for value in request.amenities:
        args.extend(["--amenity", value])
    for value in request.property_services:
        args.extend(["--property-service", value])
    if submit:
        args.append("--submit")
    if save_draft:
        args.append("--save-draft")
    if dry_run:
        args.append("--dry-run")
    return args


def gt_publish_payload(request: PublishPropertyRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": request.title,
        "description": request.description,
        "category_id": _json_number_or_text(request.category_id),
    }
    if request.price:
        payload["price"] = _json_number_or_text(request.price)
    if request.location or request.postcode or request.address:
        payload["location"] = {
            key: value
            for key, value in {
                "postcode": request.postcode,
                "display_name": request.location,
                "address": request.address,
            }.items()
            if value
        }
    if request.images:
        payload["images"] = list(request.images)
    attributes = {
        "property_type": request.property_type,
        "listing_mode": request.mode,
        "rental_type": request.rental_type if request.mode == "rent" else None,
        "rent_period": request.rent_period if request.mode == "rent" else None,
        "bedrooms": request.bedrooms,
        "bathrooms": request.bathrooms,
        "car_spaces": request.car_spaces,
        "area_size": request.area_size,
        "unit_features": request.unit_features,
        "amenities": request.amenities,
        "property_services": request.property_services,
    }
    payload["attributes"] = {key: value for key, value in attributes.items() if value not in (None, "", [])}
    contact = {
        "name": request.contact_name,
        "email": request.contact_email,
        "phone": request.phone,
        "whatsapp": request.whatsapp,
    }
    clean_contact = {key: value for key, value in contact.items() if value}
    if clean_contact:
        payload["contact"] = clean_contact
    return payload


def load_publish_payload_file(path: str) -> PublishPropertyRequest:
    payload_path = Path(path).expanduser()
    data = json.loads(payload_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("publish payload must be a JSON object")
    return build_publish_request_from_payload(data)


def _collect_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]


def _resolve_publish_market(market_hint: str) -> str:
    hint = safe_text(market_hint).lower()
    if hint in {"gt", "gumtree"}:
        return "gt"
    if hint in {"ok"}:
        return "ok"
    if hint in {"auto", ""}:
        return ""
    return "ok"


def _publish_location_for_map(request: PublishPropertyRequest) -> str:
    return safe_text(request.address) or safe_text(request.postcode) or safe_text(request.location)


def _has_any_strength(request: PublishPropertyRequest, terms: tuple[str, ...]) -> bool:
    lowered = " ".join(
        part
        for part in (
            request.query_text,
            " ".join(request.unit_features),
            " ".join(request.amenities),
            " ".join(request.property_services),
        )
        if safe_text(part)
    ).lower()
    return any(term.lower() in lowered for term in terms)


def _explicit_highlights(strength_profile: ListingStrengthProfile) -> list[str]:
    return unique_strings(_strength_description(item) for item in strength_profile.strengths)


def _map_assessments_to_copy(map_assessments: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for key in ("transport_access", "daily_convenience", "environment_risk", "area_maturity"):
        assessment = map_assessments.get(key)
        if not isinstance(assessment, dict):
            continue
        copy = _assessment_to_copy(assessment)
        if copy:
            lines.append(copy)
    return lines


def _assessment_to_copy(assessment: dict[str, Any]) -> str:
    conclusion = safe_text(assessment.get("conclusion"))
    if not conclusion or any(term in conclusion for term in ("失败", "无法自动判断", "自动地图定位失败")):
        return ""
    evidence_values = assessment.get("evidence") if isinstance(assessment.get("evidence"), list) else []
    evidence = [safe_text(item) for item in evidence_values if safe_text(item)]
    evidence = [item for item in evidence if not any(term in item for term in ("未拿到", "缺少可用定位"))]
    confidence = safe_text(assessment.get("confidence"))
    limitations = assessment.get("limitations") if isinstance(assessment.get("limitations"), list) else []
    caution = ""
    if confidence == "low" or any(item in limitations for item in ("area_level_location", "straight_line_estimate_only", "low_geocode_confidence")):
        caution = " This is a screening note and should be manually verified."
    if evidence:
        return f"{conclusion} Evidence: {' '.join(evidence[:2])}{caution}"
    return f"{conclusion}{caution}"


def _infer_country(text: str) -> tuple[str, str]:
    lowered = safe_text(text).lower()
    for term, value in _COUNTRY_HINTS.items():
        if term in lowered:
            return value
    return "", ""


def _infer_property_type(text: str) -> str:
    lowered = safe_text(text).lower()
    for normalized, aliases in _PROPERTY_TYPE_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            return normalized
    return ""


def _infer_location(text: str) -> str:
    raw = safe_text(text)
    lowered = raw.lower()
    for location in _KNOWN_LOCATIONS:
        if location.lower() in lowered:
            return location
    match = re.search(r"(?:in|at|位于|在)\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3})", raw)
    if match:
        return match.group(1).strip()
    return ""


def _infer_price(text: str) -> str | None:
    raw = safe_text(text)
    patterns = [
        r"((?:AED|AUD|SGD|USD|GBP|HKD|NZD|A\$|S\$|HK\$|£|\$)\s*[\d,]+(?:\.\d+)?)",
        r"([\d,]+(?:\.\d+)?\s*(?:AED|AUD|SGD|USD|GBP|HKD|NZD|万|元|块))",
        r"(?:price|rent|售价|租金|价格)\D{0,8}([\d,]+(?:\.\d+)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, raw, re.IGNORECASE)
        if match:
            return match.group(1).replace(",", "")
    return None


def _infer_rent_period(text: str) -> str | None:
    lowered = safe_text(text).lower()
    if any(token in lowered for token in ("per week", "/week", "/wk", "weekly", "周租", "每周")):
        return "week"
    if any(token in lowered for token in ("per year", "/year", "/yr", "yearly", "年租", "每年")):
        return "year"
    if any(token in lowered for token in ("per day", "/day", "daily", "日租", "每天")):
        return "day"
    if any(token in lowered for token in ("quarter", "季度")):
        return "quarter"
    if any(token in lowered for token in ("per month", "/month", "/mo", "monthly", "月租", "每月")):
        return "month"
    return None


def _infer_bedrooms(text: str) -> str | None:
    lowered = safe_text(text).lower()
    if "studio" in lowered:
        return "Studio"
    match = re.search(r"(\d+|[一二两三四五六七八九十])\s*(?:br|bed|beds|bedroom|bedrooms|居室|卧室|房|室)", lowered)
    if match:
        return _normalized_count(match.group(1))
    return None


def _infer_bathrooms(text: str) -> str | None:
    lowered = safe_text(text).lower()
    match = re.search(r"(\d+|[一二两三四五六七八九十])\s*(?:bath|baths|bathroom|bathrooms|卫生间|卫浴|卫)", lowered)
    return _normalized_count(match.group(1)) if match else None


def _infer_car_spaces(text: str) -> str | None:
    lowered = safe_text(text).lower()
    match = re.search(r"(\d+)\s*(?:car space|parking|车位)", lowered)
    return match.group(1) if match else None


def _infer_area(text: str) -> str | None:
    return _infer_area_detail(text)[0]


def _infer_area_detail(text: str) -> tuple[str | None, str | None]:
    lowered = safe_text(text).lower()
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:sqft|sq ft|平方英尺|平尺|sq\.?\s*ft)", lowered)
    if match:
        return match.group(1), _AREA_UNIT_SQFT
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:sqm|sq m|m2|㎡|平米|平方米|平)(?:左右|约)?", lowered)
    if match:
        return match.group(1), _AREA_UNIT_SQM
    return None, None


def _normalize_area_fields(area_value: str | None, area_unit: str | None) -> tuple[str | None, str | None, str | None, list[str]]:
    value = safe_text(area_value)
    unit = _normalize_area_unit(area_unit)
    if not value:
        return None, None, unit, []
    if unit == _AREA_UNIT_SQM:
        number = _as_float(value)
        if number is None:
            return value, value, unit, []
        sqft = int(round(number * _SQM_TO_SQFT))
        return str(sqft), _trim_number(number), unit, [f"面积已从 {_trim_number(number)} sqm 换算为约 {sqft} sqft。"]
    if unit == _AREA_UNIT_SQFT:
        return _trim_number(_as_float(value)) if _as_float(value) is not None else value, None, unit, []
    return value, None, unit, []


def _normalize_area_unit(area_unit: str | None) -> str | None:
    unit = safe_text(area_unit).lower()
    if unit in {"sqm", "sq m", "m2", "㎡", "平", "平米", "平方米"}:
        return _AREA_UNIT_SQM
    if unit in {"sqft", "sq ft", "sq. ft", "平方英尺", "平尺"}:
        return _AREA_UNIT_SQFT
    return unit or None


def _normalized_count(value: str) -> str:
    text = safe_text(value)
    if text.isdigit():
        return text
    number = _CHINESE_NUMBERS.get(text)
    return str(number) if number is not None else text


def _as_float(value: Any) -> float | None:
    text = safe_text(value).replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _trim_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _infer_phone(text: str) -> str | None:
    match = re.search(r"(?:phone|tel|电话|手机|联系)\D{0,8}(\+?\d[\d\s\-()]{6,}\d)", safe_text(text), re.IGNORECASE)
    if match:
        return re.sub(r"\s+", "", match.group(1))
    return None


def _infer_email(text: str) -> str | None:
    match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", safe_text(text))
    return match.group(0) if match else None


def _infer_postcode(text: str) -> str | None:
    match = re.search(r"\b([A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b", safe_text(text), re.IGNORECASE)
    return match.group(1).upper() if match else None


def _property_label(property_type: str) -> str:
    labels = {
        "apartment": "apartment",
        "villa": "villa",
        "townhouse": "townhouse",
        "land": "land",
        "other": "property",
    }
    return labels.get(property_type, "property")


def _strength_description(strength: str) -> str:
    mapping = {
        "交通便利，靠近公共交通": "convenient access to public transport",
        "家具齐全，可拎包入住": "furnished and ready to move in",
        "采光条件好": "bright natural light",
        "带阳台": "balcony",
        "景观视野好": "good views",
        "停车便利": "convenient parking",
        "配套泳池": "swimming pool access",
        "配套健身房": "gym access",
        "安保配套": "security amenities",
        "适合学生或家庭，周边教育资源便利": "convenient for students or families",
        "适合家庭居住": "suitable for families",
        "具备投资展示价值": "investment-friendly positioning",
    }
    return mapping.get(strength, strength)


def _bedroom_title(bedrooms: str | None) -> str:
    text = safe_text(bedrooms)
    if not text:
        return ""
    if text.lower() == "studio":
        return "studio"
    return f"{text}BR"


def _invalid_local_image_path(path: str) -> bool:
    value = safe_text(path)
    if not value:
        return True
    if re.match(r"https?://", value, re.IGNORECASE):
        return True
    return not Path(value).expanduser().is_absolute()


def _add_optional(args: list[str], flag: str, value: Any) -> None:
    text = safe_text(value)
    if text:
        args.extend([flag, text])


def _json_number_or_text(value: Any) -> Any:
    text = safe_text(value)
    if not text:
        return value
    numeric = text.replace(",", "")
    try:
        if "." in numeric:
            return float(numeric)
        return int(numeric)
    except ValueError:
        return text


def _publish_result_ok(result: dict[str, Any]) -> bool:
    if result.get("success") is True or result.get("ok") is True:
        return True
    if result.get("dry_run") is True and result.get("ok") is not False:
        return True
    return False
