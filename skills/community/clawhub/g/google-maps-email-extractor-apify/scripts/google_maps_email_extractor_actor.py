#!/usr/bin/env python3
"""Run the Google Maps Email Extractor Apify actor from an agent-friendly CLI."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_ACTOR_ID = "f3dlnXVnBc6v8JMNK"
DEFAULT_TIMEOUT_SEC = 1800

VALID_CONTACT_RESULT_MODE = {"emailsOnly", "contactsOnly", "allPlaces"}
VALID_SEARCH_MATCHING = {"all", "only_includes", "only_exact"}
VALID_WEBSITE = {"allPlaces", "withWebsite", "withoutWebsite"}
VALID_MIN_STARS = {"", "two", "twoAndHalf", "three", "threeAndHalf", "four", "fourAndHalf"}
VALID_ALL_VISIBLE = {"", "all_visible", "all_places_no_search_ocr", "all_places_no_search_mouse"}

UNSUPPORTED_FIELDS = {
    "maxReviews",
    "reviewsStartDate",
    "reviewsSort",
    "reviewsFilterString",
    "reviewsOrigin",
    "scrapeReviewsPersonalData",
    "maxImages",
    "scrapeImageAuthors",
}


class SkillError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_token(explicit: str | None) -> str:
    token = explicit or os.getenv("APIFY_TOKEN", "")
    if not token:
        raise SkillError("Apify token missing. Pass --apify-token or set APIFY_TOKEN.")
    return token


def positive_int(value: Any, field: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise SkillError(f"{field} must be an integer.") from exc
    if number <= 0:
        raise SkillError(f"{field} must be > 0.")
    return number


def non_negative_int(value: Any, field: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise SkillError(f"{field} must be an integer.") from exc
    if number < 0:
        raise SkillError(f"{field} must be >= 0.")
    return number


def string_list(values: Any, field: str) -> list[str]:
    if values in (None, ""):
        return []
    if isinstance(values, str):
        return [line.strip() for line in values.splitlines() if line.strip()]
    if isinstance(values, list):
        return [str(value).strip() for value in values if str(value).strip()]
    raise SkillError(f"{field} must be a string or array of strings.")


def normalize_start_urls(values: Any) -> list[dict[str, str]]:
    if values in (None, ""):
        return []
    if not isinstance(values, list):
        raise SkillError("startUrls must be an array.")
    urls: list[dict[str, str]] = []
    for item in values:
        if isinstance(item, str) and item.strip():
            urls.append({"url": item.strip()})
        elif isinstance(item, dict) and isinstance(item.get("url"), str) and item["url"].strip():
            urls.append({"url": item["url"].strip()})
    return urls


def validate_enum(payload: dict[str, Any], field: str, allowed: set[str]) -> None:
    if field not in payload or payload[field] in (None, ""):
        return
    value = str(payload[field])
    if value not in allowed:
        raise SkillError(f"{field} must be one of: {', '.join(sorted(allowed))}.")
    payload[field] = value


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SkillError("Input payload must be a JSON object.")

    forbidden = sorted(field for field in UNSUPPORTED_FIELDS if field in payload)
    if forbidden:
        raise SkillError(
            "This actor extracts Google Maps email leads, not review rows or image lists. "
            f"Remove unsupported field(s): {', '.join(forbidden)}."
        )

    payload["startUrls"] = normalize_start_urls(payload.get("startUrls"))
    payload["placeIds"] = string_list(payload.get("placeIds"), "placeIds")
    payload["searchStringsArray"] = string_list(payload.get("searchStringsArray"), "searchStringsArray")

    payload["maxCrawledPlacesPerSearch"] = positive_int(
        payload.get("maxCrawledPlacesPerSearch", 50),
        "maxCrawledPlacesPerSearch",
    )
    payload["contactPagesLimit"] = positive_int(payload.get("contactPagesLimit", 2), "contactPagesLimit")
    if payload["contactPagesLimit"] > 10:
        raise SkillError("contactPagesLimit must be <= 10.")

    if "allPlacesZoom" in payload and payload["allPlacesZoom"] not in (None, ""):
        payload["allPlacesZoom"] = non_negative_int(payload["allPlacesZoom"], "allPlacesZoom")

    validate_enum(payload, "contactResultMode", VALID_CONTACT_RESULT_MODE)
    validate_enum(payload, "searchMatching", VALID_SEARCH_MATCHING)
    validate_enum(payload, "website", VALID_WEBSITE)
    validate_enum(payload, "placeMinimumStars", VALID_MIN_STARS)
    validate_enum(payload, "allPlacesNoSearchAction", VALID_ALL_VISIBLE)

    payload.setdefault("contactResultMode", "emailsOnly")
    payload.setdefault("website", "withWebsite")
    payload.setdefault("includePersonalData", True)
    payload.setdefault("skipClosedPlaces", True)
    payload.setdefault("language", "en")

    has_normal_search = bool(payload.get("searchStringsArray"))
    has_direct_sources = bool(payload.get("startUrls") or payload.get("placeIds"))
    has_all_visible = bool(payload.get("allPlacesNoSearchAction"))
    if not (has_normal_search or has_direct_sources or has_all_visible):
        raise SkillError("Provide searchStringsArray, startUrls, placeIds, or allPlacesNoSearchAction.")

    if has_normal_search and not str(payload.get("locationQuery") or "").strip() and not (
        str(payload.get("city") or "").strip()
        or str(payload.get("postalCode") or "").strip()
        or payload.get("customGeolocation")
    ):
        raise SkillError("Search terms need locationQuery, structured area fields, or customGeolocation.")

    if has_all_visible and not (
        str(payload.get("locationQuery") or "").strip()
        or str(payload.get("city") or "").strip()
        or str(payload.get("postalCode") or "").strip()
        or payload.get("customGeolocation")
    ):
        raise SkillError("allPlacesNoSearchAction requires a concrete location, structured area, or customGeolocation.")

    return payload


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.input_json:
        try:
            payload = json.loads(args.input_json)
        except json.JSONDecodeError as exc:
            raise SkillError(f"Invalid --input-json: {exc}") from exc
    elif args.input_file:
        try:
            payload = json.loads(Path(args.input_file).read_text(encoding="utf-8"))
        except OSError as exc:
            raise SkillError(f"Cannot read --input-file: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise SkillError(f"Invalid JSON in --input-file: {exc}") from exc
    else:
        raise SkillError("Provide --input-json or --input-file.")
    return normalize_payload(payload)


def apply_common_options(payload: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    payload["contactResultMode"] = args.result_mode
    payload["contactPagesLimit"] = positive_int(args.contact_pages, "contact-pages")
    payload["includePersonalData"] = not args.no_personal_data
    payload["website"] = "withWebsite"
    if args.allow_without_website:
        payload["website"] = "allPlaces"
    if args.category_keyword:
        payload["categoryFilterWords"] = args.category_keyword
    if args.minimum_stars:
        payload["placeMinimumStars"] = args.minimum_stars
    if args.keep_closed:
        payload["skipClosedPlaces"] = False
    return normalize_payload(payload)


def build_quick_search_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.query.strip():
        raise SkillError("--query is required.")
    if not args.location.strip():
        raise SkillError("--location is required.")
    payload: dict[str, Any] = {
        "searchStringsArray": [args.query.strip()],
        "locationQuery": args.location.strip(),
        "maxCrawledPlacesPerSearch": positive_int(args.limit, "limit"),
        "language": args.language,
    }
    return apply_common_options(payload, args)


def build_quick_url_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.url.strip():
        raise SkillError("--url is required.")
    payload: dict[str, Any] = {
        "startUrls": [{"url": args.url.strip()}],
        "maxCrawledPlacesPerSearch": positive_int(args.limit, "limit"),
        "language": args.language,
    }
    return apply_common_options(payload, args)


def build_quick_place_id_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.place_id.strip():
        raise SkillError("--place-id is required.")
    payload: dict[str, Any] = {
        "placeIds": [args.place_id.strip()],
        "maxCrawledPlacesPerSearch": positive_int(args.limit, "limit"),
        "language": args.language,
    }
    return apply_common_options(payload, args)


def run_actor(token: str, actor_id: str, payload: dict[str, Any], timeout_sec: int, budget_usd: float | None) -> dict[str, Any]:
    params: dict[str, str | int | float] = {
        "token": token,
        "timeout": timeout_sec,
        "clean": "true",
    }
    if budget_usd is not None:
        if budget_usd <= 0:
            raise SkillError("--budget-usd must be > 0.")
        params["maxTotalChargeUsd"] = budget_usd

    url = (
        f"https://api.apify.com/v2/acts/{urllib.parse.quote(actor_id, safe='')}/run-sync-get-dataset-items"
        f"?{urllib.parse.urlencode(params)}"
    )
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=body, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=min(timeout_sec + 30, 3600)) as response:
            raw = response.read().decode("utf-8", errors="replace")
            status_code = getattr(response, "status", 200)
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise SkillError(f"Apify API error {exc.code}: {text[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise SkillError(f"Network error calling Apify: {exc}") from exc

    if status_code >= 400:
        raise SkillError(f"Apify API error {status_code}: {raw[:1000]}")

    try:
        rows = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SkillError("Apify response is not valid JSON.") from exc

    if not isinstance(rows, list):
        raise SkillError("Expected actor output as JSON array.")

    return {
        "ok": True,
        "actorId": actor_id,
        "fetchedAt": utc_now(),
        "inputUsed": payload,
        "itemCount": len(rows),
        "rows": rows,
    }


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--apify-token", help="Apify API token (fallback: APIFY_TOKEN env)")
    parser.add_argument("--actor-id", default=DEFAULT_ACTOR_ID, help="Apify actor ID")
    parser.add_argument("--timeout-sec", type=int, default=DEFAULT_TIMEOUT_SEC, help="Run timeout in seconds")
    parser.add_argument("--budget-usd", type=float, help="Apify maxTotalChargeUsd run option")


def add_email_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=50, help="Target saved email leads")
    parser.add_argument("--language", default="en", help="Google Maps language code")
    parser.add_argument("--result-mode", default="emailsOnly", choices=sorted(VALID_CONTACT_RESULT_MODE))
    parser.add_argument("--contact-pages", type=int, default=2, help="Website pages to check per place")
    parser.add_argument("--no-personal-data", action="store_true", help="Set includePersonalData=false")
    parser.add_argument("--allow-without-website", action="store_true", help="Do not force website=withWebsite")
    parser.add_argument("--keep-closed", action="store_true", help="Do not set skipClosedPlaces=true")
    parser.add_argument("--category-keyword", action="append", help="Category keyword filter; can be repeated")
    parser.add_argument("--minimum-stars", choices=sorted(v for v in VALID_MIN_STARS if v), help="Minimum rating filter")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Google Maps Email Extractor actor on Apify")
    sub = parser.add_subparsers(dest="command", required=True)

    quick_search = sub.add_parser("quick-search", help="Run by search term and location")
    add_common_args(quick_search)
    add_email_args(quick_search)
    quick_search.add_argument("--query", required=True, help="Business search term")
    quick_search.add_argument("--location", required=True, help="Google Maps location query")

    quick_url = sub.add_parser("quick-url", help="Run by Google Maps URL")
    add_common_args(quick_url)
    add_email_args(quick_url)
    quick_url.add_argument("--url", required=True, help="Google Maps search/place/CID URL")

    quick_place = sub.add_parser("quick-place-id", help="Run by Google Place ID")
    add_common_args(quick_place)
    add_email_args(quick_place)
    quick_place.add_argument("--place-id", required=True, help="Google Place ID")

    run_cmd = sub.add_parser("run", help="Run a custom actor payload")
    add_common_args(run_cmd)
    run_cmd.add_argument("--input-json", help="Inline JSON payload")
    run_cmd.add_argument("--input-file", help="Path to JSON payload file")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        token = resolve_token(args.apify_token)
        if args.command == "quick-search":
            payload = build_quick_search_payload(args)
        elif args.command == "quick-url":
            payload = build_quick_url_payload(args)
        elif args.command == "quick-place-id":
            payload = build_quick_place_id_payload(args)
        else:
            payload = load_payload(args)
        result = run_actor(token, args.actor_id, payload, args.timeout_sec, args.budget_usd)
    except SkillError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
