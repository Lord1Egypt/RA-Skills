from __future__ import annotations

from typing import Any

from .analysis import (
    compact_assessment,
    detect_price_risk,
    extract_bedrooms,
    has_placeholder_image,
    join_for_markdown,
    parse_price_text,
    price_context,
    safe_text,
    unique_strings,
)
from .models import (
    CandidateDecisionRow,
    PipelineReport,
    PreflightCheck,
    PreflightReport,
    RawListingSnapshot,
    SearchRequest,
)
from .source_client import PropertyListingClient


class PropertyAdvisorOrchestrator:
    def __init__(self, listing_client: PropertyListingClient | Any, map_client: Any | None = None) -> None:
        self.listing_client = listing_client
        self.map_client = map_client

    def search(self, request: SearchRequest) -> PipelineReport:
        preflight = self._doctor()
        if not preflight.ok:
            return PipelineReport(
                request=request,
                preflight=preflight,
                selected_source=getattr(self.listing_client, "source_name", None),
                selected_runtime_mode=getattr(self.listing_client, "runtime_mode", None),
                routing=_routing_payload(request),
                summary={"visible_candidates": 0, "hidden_candidates": 0},
                warnings=list(preflight.warnings),
                errors=[f"{preflight.source_name or 'listing source'} preflight failed; fix runtime before retrying search."],
            )

        try:
            base_listings = self._fetch_search_results(request)
        except Exception as exc:
            warnings = list(preflight.warnings)
            if hasattr(self.listing_client, "drain_warnings"):
                warnings.extend(self.listing_client.drain_warnings())
            return PipelineReport(
                request=request,
                preflight=preflight,
                selected_source=getattr(self.listing_client, "source_name", None),
                selected_runtime_mode=getattr(self.listing_client, "runtime_mode", None),
                routing=_routing_payload(request),
                summary={
                    "visible_candidates": 0,
                    "hidden_candidates": 0,
                    "search_total": 0,
                    "detail_hydrated": 0,
                    "map_status": None,
                    "selected_source_id": request.resolved_source_id or request.resolved_market,
                },
                warnings=unique_strings(warnings),
                errors=[f"{getattr(self.listing_client, 'source_name', 'listing source')} search failed: {exc}"],
            )
        hydrated = self._hydrate_details(base_listings, request.detail_limit)
        snapshots = [self._build_snapshot(listing, index) for index, listing in enumerate(hydrated)]
        warnings: list[str] = list(preflight.warnings)
        if hasattr(self.listing_client, "drain_warnings"):
            warnings.extend(self.listing_client.drain_warnings())
        map_report: dict[str, Any] | None = None

        if request.force_map and self.map_client:
            map_report, map_warnings = self._run_map_pipeline(request, snapshots)
            warnings.extend(map_warnings)

        rows, hidden = self._build_rows(request, snapshots, map_report)
        rendered_table = render_candidate_table(rows)
        summary = {
            "visible_candidates": len(rows),
            "hidden_candidates": len(hidden),
            "search_total": len(base_listings),
            "detail_hydrated": sum(1 for snapshot in snapshots if snapshot.detail_fetched),
            "map_status": (map_report or {}).get("status"),
            "selected_source_id": request.resolved_source_id or request.resolved_market,
        }
        if hidden:
            warnings.append(f"有 {len(hidden)} 套候选缺少原帖链接，已从最终表格中隐藏。")
        if request.resolved_source_id in {"ok", "gt"} or request.resolved_market in {"ok", "gt"}:
            warnings.append("本轮使用已预检通过的可用数据源完成筛选；结果不代表已覆盖所有房产平台。")
        return PipelineReport(
            request=request,
            preflight=preflight,
            selected_source=getattr(self.listing_client, "source_name", None),
            selected_runtime_mode=getattr(self.listing_client, "runtime_mode", None),
            routing=_routing_payload(request),
            raw_listing_snapshots=snapshots,
            map_report=map_report,
            candidate_rows=rows,
            hidden_candidates=hidden,
            rendered_table=rendered_table,
            summary=summary,
            warnings=unique_strings(warnings),
            errors=[],
        )

    def _doctor(self) -> PreflightReport:
        if hasattr(self.listing_client, "doctor"):
            run_browser_smoke = getattr(self.listing_client, "source_name", "") != "gt-core-skill"
            return self.listing_client.doctor(run_browser_smoke=run_browser_smoke)
        return PreflightReport(
            ok=True,
            skill_root=None,
            selected_runner="injected",
            checks=[PreflightCheck(name="injected_client", ok=True, message="Using injected ok client.")],
            source_name=getattr(self.listing_client, "source_name", "injected"),
            runtime_mode=getattr(self.listing_client, "runtime_mode", "injected"),
            detail_supported=getattr(self.listing_client, "detail_supported", None),
        )

    def _fetch_search_results(self, request: SearchRequest) -> list[dict[str, Any]]:
        if request.keyword:
            return self.listing_client.search_property(
                keyword=request.keyword,
                country=request.country,
                city=request.city,
                lang=request.lang,
                max_results=request.max_results,
                query_text=request.query_text,
                search_location=request.search_location_hint,
            )
        return self.listing_client.browse_property(
            country=request.country,
            city=request.city,
            lang=request.lang,
            max_results=request.max_results,
            query_text=request.query_text,
            search_location=request.search_location_hint,
        )

    def _hydrate_details(self, listings: list[dict[str, Any]], detail_limit: int) -> list[dict[str, Any]]:
        hydrated: list[dict[str, Any]] = []
        for index, listing in enumerate(listings):
            detailed = dict(listing)
            url = safe_text(listing.get("url"))
            if index < detail_limit and url:
                try:
                    detail = self.listing_client.get_listing_detail(url=url)
                    detail = dict(detail)
                    detail = {**listing, **detail}
                    if not detail.get("url"):
                        detail["url"] = url
                    detail["detail_fetched"] = not bool(detail.get("detail_degraded")) and detail.get("detail_fetched", True) is not False
                    detailed = detail
                except Exception:
                    detailed["detail_fetched"] = False
            else:
                detailed["detail_fetched"] = False
            hydrated.append(detailed)
        return hydrated

    def _build_snapshot(self, listing: dict[str, Any], index: int) -> RawListingSnapshot:
        title = safe_text(listing.get("title")) or f"listing_{index + 1}"
        location = safe_text(listing.get("location")) or None
        url = safe_text(listing.get("url")) or None
        listing_id = safe_text(listing.get("listing_id")) or None
        snapshot_id = (
            safe_text(listing.get("id"))
            or listing_id
            or url
            or f"listing_{index + 1}"
        )
        images = list(listing.get("images") or [])
        image_url = safe_text(listing.get("image_url")) or None
        if image_url and image_url not in images:
            images = [image_url, *images]
        attributes = listing.get("attributes") if isinstance(listing.get("attributes"), dict) else {}
        bedrooms_text = safe_text(listing.get("bedrooms_text") or attributes.get("Number Of Bedrooms") or attributes.get("Bedrooms"))
        price_info = parse_price_text(listing.get("price"))
        return RawListingSnapshot(
            id=snapshot_id,
            listing_id=listing_id,
            title=title,
            price=safe_text(listing.get("price")) or None,
            location=location,
            url=url,
            image_url=image_url or (images[0] if images else None),
            images=[safe_text(image) for image in images if safe_text(image)],
            description=safe_text(listing.get("description")) or None,
            address=safe_text(listing.get("address")) or None,
            lat=_as_float(listing.get("lat")),
            lng=_as_float(listing.get("lng")),
            geo_precision=safe_text(listing.get("geo_precision")) or None,
            posted_time=safe_text(listing.get("posted_time")) or None,
            seller_name=safe_text(listing.get("seller_name")) or None,
            category=safe_text(listing.get("category")) or None,
            detail_fetched=bool(listing.get("detail_fetched")),
            monthly_price_value=price_info["monthly_value"],
            price_value=price_info["value"],
            price_currency=price_info["currency"],
            price_period=price_info["period"],
            inferred_bedrooms=extract_bedrooms(title, listing.get("description"), bedrooms_text),
            image_count=len(images),
            has_placeholder_image=has_placeholder_image(images),
            raw=dict(listing),
        )

    def _run_map_pipeline(
        self,
        request: SearchRequest,
        snapshots: list[RawListingSnapshot],
    ) -> tuple[dict[str, Any] | None, list[str]]:
        warnings: list[str] = []
        try:
            doctor = self.map_client.doctor()
        except Exception as exc:
            return None, [f"地图 skill doctor 失败：{exc}"]
        if doctor.get("status") != "ok":
            warnings.append("地图 skill doctor 未通过，本轮降级为无地图增强。")
            return doctor, warnings
        try:
            report = self.map_client.analyze_batch(
                listings=[snapshot.to_map_listing() for snapshot in snapshots],
                destination=request.destination,
                city=request.city,
            )
        except Exception as exc:
            return None, [f"地图增强失败：{exc}"]
        return report, warnings

    def _build_rows(
        self,
        request: SearchRequest,
        snapshots: list[RawListingSnapshot],
        map_report: dict[str, Any] | None,
    ) -> tuple[list[CandidateDecisionRow], list[dict[str, Any]]]:
        peer_prices = price_context(snapshots)
        map_items = {
            safe_text(item.get("id")): item
            for item in (map_report or {}).get("listings", [])
            if safe_text(item.get("id"))
        }
        rows: list[CandidateDecisionRow] = []
        hidden: list[dict[str, Any]] = []
        for snapshot in snapshots:
            if not snapshot.url:
                hidden.append(
                    {
                        "id": snapshot.id,
                        "candidate_name": snapshot.title,
                        "reason": "original_listing_url_missing",
                    }
                )
                continue
            map_item = map_items.get(snapshot.id)
            row = self._build_row(request, snapshot, map_item, peer_prices)
            rows.append(row)
        return rows, hidden

    def _build_row(
        self,
        request: SearchRequest,
        snapshot: RawListingSnapshot,
        map_item: dict[str, Any] | None,
        peer_prices: dict[str, Any],
    ) -> CandidateDecisionRow:
        satisfied: list[str] = ["保留原帖链接"]
        missing: list[str] = []
        risks = detect_price_risk(snapshot.monthly_price_value, peer_prices)
        if snapshot.image_count > 0 and not snapshot.has_placeholder_image:
            satisfied.append(f"有 {snapshot.image_count} 张房源图片")
        else:
            missing.append("图片不足或为占位图")
        detail_degraded_reason = safe_text(snapshot.raw.get("detail_degraded_reason"))
        if snapshot.detail_fetched:
            satisfied.append("已补齐房源详情")
        elif detail_degraded_reason:
            missing.append(detail_degraded_reason)
        else:
            missing.append("未补齐详情页字段")
        if request.budget_max is not None:
            if snapshot.monthly_price_value is not None and snapshot.monthly_price_value <= request.budget_max:
                satisfied.append("预算内")
            else:
                risks.append("预算可能不符或价格无法换算为月度对比")
        if request.budget_min is not None:
            if snapshot.monthly_price_value is not None and snapshot.monthly_price_value >= request.budget_min:
                satisfied.append("高于最低预算要求")
        if request.bedrooms is not None:
            if snapshot.inferred_bedrooms is not None and snapshot.inferred_bedrooms >= request.bedrooms:
                satisfied.append(f"推断卧室数约 {snapshot.inferred_bedrooms:g}")
            else:
                missing.append("卧室数未确认或可能不满足")
        else:
            if snapshot.inferred_bedrooms is not None:
                satisfied.append(f"推断卧室数约 {snapshot.inferred_bedrooms:g}")
            else:
                missing.append("卧室数待确认")
        attributes = snapshot.raw.get("attributes") if isinstance(snapshot.raw.get("attributes"), dict) else {}
        missing.append("面积待确认")
        if safe_text(snapshot.raw.get("bathrooms_text") or attributes.get("Number Of Bathrooms") or attributes.get("Bathrooms")):
            satisfied.append(f"卫浴信息：{safe_text(snapshot.raw.get('bathrooms_text') or attributes.get('Number Of Bathrooms') or attributes.get('Bathrooms'))}")
        else:
            missing.append("卫浴数待确认")

        map_assessment = (map_item or {}).get("assessments") or {}
        map_links = (map_item or {}).get("verification_links") or {}
        geo = (map_item or {}).get("geo") or {}
        map_status = (map_item or {}).get("status") or (map_report_status(map_item))

        if map_assessment:
            for key in ("transport_access", "daily_convenience", "environment_risk", "area_maturity"):
                detail = compact_assessment(map_assessment.get(key))
                if detail:
                    satisfied.append(detail)
            if geo.get("precision") == "area":
                missing.append("地图仅有区域级定位，楼栋级距离待人工复核")
            if geo.get("precision") == "missing":
                missing.append("自动地图定位失败")
            if geo.get("confidence") == "low":
                missing.append("地图定位低置信")
            limitations = (map_item or {}).get("limitations") or []
            if "route_time_is_estimated" in limitations:
                missing.append("通勤路线仅为直线估算")
            risk_summary = compact_assessment(map_assessment.get("environment_risk"))
            if risk_summary and "高" in risk_summary:
                risks.append(risk_summary)
        else:
            missing.append("未完成地图增强")

        status = "推荐"
        if any("异常低价" in risk or "疑似异常低价" in risk for risk in risks):
            status = "淘汰"
        elif any("环境风险偏高" in risk or "环境风险可做参考" in risk for risk in risks):
            status = "可继续关注"
        elif map_assessment and (geo.get("precision") == "missing" or geo.get("confidence") == "low"):
            status = "待人工复核"
        elif not map_assessment or map_status in {"partial", "degraded"}:
            status = "待补地图"
        elif snapshot.has_placeholder_image:
            status = "可继续关注"

        if not map_assessment and not risks:
            risks.append("地图未补强，本轮只完成房源初筛。")
        if snapshot.has_placeholder_image:
            risks.append("图片可信度一般，需打开原帖核对实拍信息。")
        return CandidateDecisionRow(
            source_id=snapshot.id,
            candidate_name=snapshot.title,
            status=status,
            price=snapshot.price or "价格待确认",
            location=snapshot.location or "位置待确认",
            satisfied=unique_strings(satisfied),
            missing_or_unknown=unique_strings(missing),
            elimination_or_risk=unique_strings(risks),
            listing_url=snapshot.url,
            map_verification_url=map_links.get("google_maps_manual"),
            map_assessment=map_assessment,
        )


def map_report_status(map_item: dict[str, Any] | None) -> str | None:
    if not map_item:
        return None
    geo = map_item.get("geo") or {}
    if geo.get("precision") == "missing":
        return "degraded"
    limitations = map_item.get("limitations") or []
    if "low_geocode_confidence" in limitations:
        return "partial"
    return "ok"


def render_candidate_table(rows: list[CandidateDecisionRow]) -> str:
    headers = [
        "候选房源",
        "状态",
        "价格",
        "位置",
        "已满足",
        "缺失/未知",
        "淘汰原因/风险",
        "房源链接",
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        display = row.to_display_row()
        values = [
            display["候选房源"],
            display["状态"],
            display["价格"],
            display["位置"],
            join_for_markdown(row.satisfied),
            join_for_markdown(row.missing_or_unknown),
            join_for_markdown(row.elimination_or_risk),
            row.listing_url,
        ]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _as_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _routing_payload(request: SearchRequest) -> dict[str, Any]:
    return {
        "market_hint": request.market_hint,
        "source_hint": request.source_hint,
        "resolved_market": request.resolved_market,
        "resolved_source_id": request.resolved_source_id,
        "reason": request.routing_reason,
        "search_location_hint": request.search_location_hint,
    }
