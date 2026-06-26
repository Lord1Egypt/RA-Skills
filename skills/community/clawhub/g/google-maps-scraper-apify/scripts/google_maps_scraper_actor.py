#!/usr/bin/env python3
"""Run the Google Maps Scraper Apify actor from an agent-friendly CLI."""

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

DEFAULT_ACTOR_ID = "kLdarP5qiTvc9CwtP"
DEFAULT_TIMEOUT_SEC = 1800
VALID_REVIEWS_SORT = {"newest", "mostRelevant", "highestRanking", "lowestRanking"}


class SkillError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_token(explicit: str | None) -> str:
    token = explicit or os.getenv("APIFY_TOKEN", "")
    if not token:
        raise SkillError("Apify token missing. Pass --apify-token or set APIFY_TOKEN.")
    return token


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

    if not isinstance(payload, dict):
        raise SkillError("Input payload must be a JSON object.")
    return normalize_payload(payload)


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if "startUrls" in payload and isinstance(payload["startUrls"], list):
        normalized_urls: list[dict[str, str]] = []
        for item in payload["startUrls"]:
            if isinstance(item, str):
                normalized_urls.append({"url": item})
            elif isinstance(item, dict) and isinstance(item.get("url"), str):
                normalized_urls.append({"url": item["url"]})
        payload["startUrls"] = normalized_urls

    if "maxCrawledPlacesPerSearch" in payload:
        payload["maxCrawledPlacesPerSearch"] = positive_int(payload["maxCrawledPlacesPerSearch"], "maxCrawledPlacesPerSearch")
    if "maxReviews" in payload:
        payload["maxReviews"] = non_negative_int(payload["maxReviews"], "maxReviews")
    if "maxImages" in payload:
        payload["maxImages"] = non_negative_int(payload["maxImages"], "maxImages")

    reviews_sort = payload.get("reviewsSort")
    if reviews_sort and reviews_sort not in VALID_REVIEWS_SORT:
        raise SkillError(f"reviewsSort must be one of: {', '.join(sorted(VALID_REVIEWS_SORT))}.")

    return payload


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


def build_quick_search_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.query.strip():
        raise SkillError("--query is required.")
    if not args.location.strip():
        raise SkillError("--location is required.")
    if args.reviews_sort not in VALID_REVIEWS_SORT:
        raise SkillError(f"--reviews-sort must be one of: {', '.join(sorted(VALID_REVIEWS_SORT))}.")

    payload: dict[str, Any] = {
        "searchStringsArray": [args.query.strip()],
        "locationQuery": args.location.strip(),
        "maxCrawledPlacesPerSearch": positive_int(args.limit, "limit"),
        "language": args.language,
    }

    if args.details:
        payload["scrapePlaceDetailPage"] = True
    if args.with_contacts:
        payload["scrapeCompanyContacts"] = True
    if args.only_with_website:
        payload["website"] = "withWebsite"
    if args.reviews:
        payload["maxReviews"] = non_negative_int(args.reviews, "reviews")
        payload["reviewsSort"] = args.reviews_sort
    if args.images:
        payload["maxImages"] = non_negative_int(args.images, "images")

    return payload


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
    req = urllib.request.Request(
        url=url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Google Maps Scraper actor on Apify")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--apify-token", help="Apify API token (fallback: APIFY_TOKEN env)")
    common.add_argument("--actor-id", default=DEFAULT_ACTOR_ID, help="Apify actor ID")
    common.add_argument("--timeout-sec", type=int, default=DEFAULT_TIMEOUT_SEC, help="Run timeout in seconds")
    common.add_argument("--budget-usd", type=float, help="Apify maxTotalChargeUsd run option")

    quick = sub.add_parser("quick-search", parents=[common], help="Run a search term + location payload")
    quick.add_argument("--query", required=True, help="Google Maps search term")
    quick.add_argument("--location", required=True, help="Google Maps location query")
    quick.add_argument("--limit", type=int, default=25, help="Places per search")
    quick.add_argument("--language", default="en", help="Google Maps language code")
    quick.add_argument("--details", action="store_true", help="Enable scrapePlaceDetailPage")
    quick.add_argument("--with-contacts", action="store_true", help="Enable scrapeCompanyContacts")
    quick.add_argument("--only-with-website", action="store_true", help="Set website=withWebsite")
    quick.add_argument("--reviews", type=int, default=0, help="Reviews per place")
    quick.add_argument("--reviews-sort", default="newest", help="Review sort")
    quick.add_argument("--images", type=int, default=0, help="Additional images per place")

    run_cmd = sub.add_parser("run", parents=[common], help="Run a custom actor payload")
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
        else:
            payload = load_payload(args)
        result = run_actor(token, args.actor_id, payload, args.timeout_sec, args.budget_usd)
    except SkillError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
