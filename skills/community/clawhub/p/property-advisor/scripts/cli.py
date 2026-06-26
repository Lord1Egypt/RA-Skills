#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from property_advisor import (
    GTCoreSkillClient,
    OKCoreSkillClient,
    PipelineReport,
    PreflightReport,
    PropertyAdvisorOrchestrator,
    PublishPropertyOrchestrator,
    PublicOsmMapClient,
    SearchRequest,
    apply_market_routing,
    classify_user_intent,
    infer_publish_request,
)
from property_advisor.analysis import unique_strings
from property_advisor.profile import ProfileStore
from property_advisor.publish import load_publish_payload_file


def emit(payload: dict, exit_code: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Property Advisor orchestration CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Run ok-core-skill, gt-core-skill, and map-skill preflight checks")
    doctor.add_argument("--ok-skill-root", default="")
    doctor.add_argument("--gt-skill-root", default="")
    doctor.add_argument("--skip-browser-smoke", action="store_true")

    route = subparsers.add_parser("route", help="Classify user intent as consumer search, business publish, or clarify")
    route.add_argument("--query-text", default="")
    route.add_argument("--mode", choices=["auto", "sale", "rent"], default="auto")
    route.add_argument("--market", choices=["auto", "ok", "gt"], default="auto")
    route.add_argument("--source", default="auto")

    search = subparsers.add_parser("search", help="Run the full listing -> detail -> map -> decision pipeline")
    search.add_argument("--keyword", default="")
    search.add_argument("--country", default="australia")
    search.add_argument("--city", default="melbourne")
    search.add_argument("--lang", default="en")
    search.add_argument("--max-results", type=int, default=20)
    search.add_argument("--detail-limit", type=int, default=10)
    search.add_argument("--destination", default="")
    search.add_argument("--budget-min", type=float)
    search.add_argument("--budget-max", type=float)
    search.add_argument("--bedrooms", type=float)
    search.add_argument("--query-text", default="")
    search.add_argument("--priority", action="append", default=[])
    search.add_argument("--skip-map", action="store_true")
    search.add_argument("--map-fixture-dir", default="")
    search.add_argument("--ok-skill-root", default="")
    search.add_argument("--gt-skill-root", default="")
    search.add_argument("--market", choices=["auto", "ok", "gt"], default="auto")
    search.add_argument("--source", default="auto", help="Preferred source id, e.g. ok, gt, zillow, rightmove. Defaults to auto.")
    search.add_argument("--memory-dir", default="", help="Override local profile memory directory.")
    search.add_argument("--no-memory", action="store_true", help="Do not read or update local profile memory.")

    publish = subparsers.add_parser("publish", help="Prepare, fill, or publish a business-side property listing")
    publish.add_argument("--payload-file", default="", help="JSON file using PublishPropertyRequest fields")
    publish.add_argument("--query-text", default="")
    publish.add_argument("--market", choices=["auto", "ok", "gt"], default="auto")
    publish.add_argument("--mode", choices=["auto", "sale", "rent"], default="auto")
    publish.add_argument("--country", default="")
    publish.add_argument("--subdomain", default="")
    publish.add_argument("--property-type", default="")
    publish.add_argument("--title", default="")
    publish.add_argument("--description", default="")
    publish.add_argument("--price", default="")
    publish.add_argument("--location", default="")
    publish.add_argument("--image", action="append", default=[])
    publish.add_argument("--floor-plan", action="append", default=[])
    publish.add_argument("--rental-type", default="entire")
    publish.add_argument("--rent-period", default="")
    publish.add_argument("--bedrooms", default="")
    publish.add_argument("--bathrooms", default="")
    publish.add_argument("--car-spaces", default="")
    publish.add_argument("--floor-level", default="")
    publish.add_argument("--floor", default="")
    publish.add_argument("--area-size", default="")
    publish.add_argument("--phone", default="")
    publish.add_argument("--whatsapp", default="")
    publish.add_argument("--unit-feature", action="append", default=[])
    publish.add_argument("--amenity", action="append", default=[])
    publish.add_argument("--property-service", action="append", default=[])
    publish.add_argument("--contact-name", default="")
    publish.add_argument("--contact-email", default="")
    publish.add_argument("--category-id", default="", help="Required for GT dry-run payloads")
    publish.add_argument("--postcode", default="")
    publish.add_argument("--address", default="")
    publish.add_argument("--publish-endpoint", default="")
    publish.add_argument("--area-unit", choices=["sqm", "sqft", "sq m", "sq ft"], default="")
    publish.add_argument("--lang", default="en")
    publish.add_argument("--confirm-submit", action="store_true", help="Actually submit; otherwise only dry-run/fill form")
    publish.add_argument("--save-draft", action="store_true")
    publish.add_argument("--dry-run", action="store_true")
    publish.add_argument("--ok-skill-root", default="")
    publish.add_argument("--gt-skill-root", default="")

    watch = subparsers.add_parser("watch", help="Save a listing to the local watched list")
    watch.add_argument("--url", required=True)
    watch.add_argument("--title", default="")
    watch.add_argument("--source", default="")
    watch.add_argument("--note", default="")
    watch.add_argument("--memory-dir", default="")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "doctor":
        map_client = PublicOsmMapClient()
        ok_report = _safe_ok_doctor(args.ok_skill_root or None, skip_browser_smoke=args.skip_browser_smoke)
        gt_report = _safe_gt_doctor(args.gt_skill_root or None, skip_browser_smoke=args.skip_browser_smoke)
        payload = {
            "ok_core_skill": ok_report.to_dict(),
            "gt_core_skill": gt_report.to_dict(),
            "public_osm_map_context": map_client.doctor(),
        }
        exit_code = 0 if payload["ok_core_skill"]["ok"] and payload["public_osm_map_context"].get("status") == "ok" else 2
        return emit(payload, exit_code=exit_code)

    if args.command == "route":
        decision = classify_user_intent(args.query_text, mode_hint=args.mode, market_hint=args.market)
        payload = decision.to_dict()
        if decision.intent == "consumer_search":
            routed_request, routing = apply_market_routing(
                SearchRequest(query_text=args.query_text, market_hint=args.market, source_hint=args.source)
            )
            payload["routing"] = routing.to_dict()
            payload["resolved_source_id"] = routed_request.resolved_source_id
        return emit(payload, exit_code=0 if not decision.error and not payload.get("routing", {}).get("error") else 2)

    if args.command == "watch":
        store = ProfileStore(args.memory_dir or None)
        path = store.watch_listing(url=args.url, title=args.title, source_id=args.source, note=args.note)
        return emit({"ok": True, "watched_path": str(path)}, exit_code=0)

    if args.command == "publish":
        try:
            request = (
                load_publish_payload_file(args.payload_file)
                if args.payload_file
                else infer_publish_request(
                    query_text=args.query_text,
                    market_hint=args.market,
                    mode=args.mode,
                    country=args.country,
                    subdomain=args.subdomain,
                    property_type=args.property_type,
                    title=args.title,
                    description=args.description,
                    price=args.price or None,
                    location=args.location,
                    images=args.image,
                    floor_plans=args.floor_plan,
                    rental_type=args.rental_type,
                    rent_period=args.rent_period or None,
                    bedrooms=args.bedrooms or None,
                    bathrooms=args.bathrooms or None,
                    car_spaces=args.car_spaces or None,
                    floor_level=args.floor_level or None,
                    floor=args.floor or None,
                    area_size=args.area_size or None,
                    phone=args.phone or None,
                    whatsapp=args.whatsapp or None,
                    unit_features=args.unit_feature,
                    amenities=args.amenity,
                    property_services=args.property_service,
                    contact_name=args.contact_name or None,
                    contact_email=args.contact_email or None,
                    category_id=args.category_id or None,
                    postcode=args.postcode or None,
                    address=args.address or None,
                    publish_endpoint=args.publish_endpoint or None,
                    area_unit=args.area_unit or None,
                    lang=args.lang,
                )
            )
            if args.payload_file:
                request.query_text = args.query_text or request.query_text
                request.market_hint = args.market if args.market != "auto" else request.market_hint
        except Exception as exc:
            return emit({"errors": [str(exc)]}, exit_code=2)
        orchestrator = PublishPropertyOrchestrator(
            ok_skill_root=args.ok_skill_root or None,
            gt_skill_root=args.gt_skill_root or None,
        )
        report = orchestrator.publish(
            request,
            confirm_submit=args.confirm_submit,
            save_draft=args.save_draft,
            dry_run=args.dry_run,
        )
        return emit(report.to_dict(), exit_code=0 if not report.errors else 2)

    request = SearchRequest(
        keyword=args.keyword,
        country=args.country,
        city=args.city,
        lang=args.lang,
        max_results=args.max_results,
        detail_limit=args.detail_limit,
        destination=args.destination,
        budget_min=args.budget_min,
        budget_max=args.budget_max,
        bedrooms=args.bedrooms,
        force_map=not args.skip_map,
        query_text=args.query_text,
        user_priorities=args.priority,
        market_hint=args.market,
        source_hint=args.source,
        country_is_default=not _arg_provided("--country"),
        city_is_default=not _arg_provided("--city"),
    )
    profile_store = None if args.no_memory else ProfileStore(args.memory_dir or None)
    if profile_store:
        profile = profile_store.load()
        profile_store.update_from_request(profile, request)
        request = profile_store.apply_to_request(request, profile)
    routed_request, routing = apply_market_routing(request)
    if routing.error:
        report = PipelineReport(
            request=routed_request,
            preflight=PreflightReport(
                ok=False,
                skill_root=None,
                selected_runner=None,
                warnings=list(routing.warnings),
                source_name=routing.source_id or "source-router",
            ),
            routing=routing.to_dict(),
            selected_source=routing.source_id or None,
            summary={"visible_candidates": 0, "hidden_candidates": 0},
            warnings=list(routing.warnings),
            errors=[routing.error],
        )
        return emit(report.to_dict(), exit_code=2)
    try:
        listing_client = _build_listing_client(
            routed_request,
            ok_skill_root=args.ok_skill_root or None,
            gt_skill_root=args.gt_skill_root or None,
        )
    except Exception as exc:
        report = PipelineReport(
            request=routed_request,
            preflight=PreflightReport(
                ok=False,
                skill_root=args.gt_skill_root or None,
                selected_runner=None,
                warnings=[str(exc)],
                source_name=routed_request.resolved_source_id or ("gt-core-skill" if routed_request.resolved_market == "gt" else "ok-core-skill"),
            ),
            routing=routing.to_dict(),
            selected_source=routed_request.resolved_source_id or routed_request.resolved_market or None,
            summary={"visible_candidates": 0, "hidden_candidates": 0},
            warnings=[str(exc)],
            errors=[str(exc)],
        )
        return emit(report.to_dict(), exit_code=2)
    map_client = None if args.skip_map else PublicOsmMapClient(fixture_dir=args.map_fixture_dir or None)
    orchestrator = PropertyAdvisorOrchestrator(listing_client, map_client)
    report = orchestrator.search(routed_request)
    report.routing = routing.to_dict()
    report.warnings = unique_strings(report.warnings + routing.warnings)
    if profile_store:
        profile_store.record_search(routed_request, report)
    exit_code = 0 if not report.errors else 2
    return emit(report.to_dict(), exit_code=exit_code)


def _build_listing_client(request: SearchRequest, *, ok_skill_root: str | None, gt_skill_root: str | None):
    if request.resolved_source_id == "gt" or request.resolved_market == "gt":
        return GTCoreSkillClient(skill_root=gt_skill_root or None)
    if request.resolved_source_id in {"", "ok"} or request.resolved_market == "ok":
        return OKCoreSkillClient(skill_root=ok_skill_root or None)
    raise RuntimeError(f"数据源 {request.resolved_source_id} 尚未接入可执行 client。")


def _safe_ok_doctor(skill_root: str | None, *, skip_browser_smoke: bool) -> PreflightReport:
    try:
        client = OKCoreSkillClient(skill_root=skill_root or None)
    except Exception as exc:
        return PreflightReport(
            ok=False,
            skill_root=skill_root or None,
            selected_runner=None,
            warnings=[str(exc)],
            source_name="ok-core-skill",
            runtime_mode="ok",
            detail_supported=True,
        )
    try:
        return client.doctor(run_browser_smoke=not skip_browser_smoke)
    except Exception as exc:
        return PreflightReport(
            ok=False,
            skill_root=str(client.skill_root),
            selected_runner=None,
            warnings=[str(exc)],
            source_name="ok-core-skill",
            runtime_mode="ok",
            detail_supported=True,
        )


def _arg_provided(name: str) -> bool:
    return any(arg == name or arg.startswith(f"{name}=") for arg in sys.argv[1:])


def _safe_gt_doctor(skill_root: str | None, *, skip_browser_smoke: bool) -> PreflightReport:
    try:
        client = GTCoreSkillClient(skill_root=skill_root or None)
    except Exception as exc:
        return PreflightReport(
            ok=False,
            skill_root=skill_root or None,
            selected_runner=None,
            warnings=[str(exc)],
            source_name="gt-core-skill",
        )
    return client.doctor(run_browser_smoke=not skip_browser_smoke)


if __name__ == "__main__":
    raise SystemExit(main())
