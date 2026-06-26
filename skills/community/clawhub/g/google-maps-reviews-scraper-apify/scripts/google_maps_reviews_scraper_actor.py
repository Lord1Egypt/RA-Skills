#!/usr/bin/env python3
"""Run the Google Maps Reviews Scraper Apify actor from an agent-friendly CLI."""

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

DEFAULT_ACTOR_ID = "V2kIsQs3Ta9C9kkEt"
DEFAULT_TIMEOUT_SEC = 1800
VALID_REVIEWS_SORT = {"newest", "mostRelevant", "highestRanking", "lowestRanking"}
VALID_REVIEWS_ORIGIN = {"google", "all"}


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


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if "startUrls" in payload and isinstance(payload["startUrls"], list):
        urls: list[dict[str, str]] = []
        for item in payload["startUrls"]:
            if isinstance(item, str):
                urls.append({"url": item})
            elif isinstance(item, dict) and isinstance(item.get("url"), str):
                urls.append({"url": item["url"]})
        payload["startUrls"] = urls

    if not payload.get("startUrls") and not payload.get("placeIds"):
        raise SkillError("Provide startUrls or placeIds.")

    payload["maxReviews"] = positive_int(payload.get("maxReviews", 100), "maxReviews")

    reviews_sort = payload.get("reviewsSort", "newest")
    if reviews_sort not in VALID_REVIEWS_SORT:
        raise SkillError(f"reviewsSort must be one of: {', '.join(sorted(VALID_REVIEWS_SORT))}.")
    payload["reviewsSort"] = reviews_sort

    reviews_origin = payload.get("reviewsOrigin", "google")
    if reviews_origin not in VALID_REVIEWS_ORIGIN:
        raise SkillError("reviewsOrigin must be google or all.")
    payload["reviewsOrigin"] = reviews_origin

    payload.setdefault("language", "en")
    payload.setdefault("personalData", True)
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
    if not isinstance(payload, dict):
        raise SkillError("Input payload must be a JSON object.")
    return normalize_payload(payload)


def quick_common_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "maxReviews": positive_int(args.max_reviews, "max-reviews"),
        "reviewsSort": args.reviews_sort,
        "reviewsOrigin": args.reviews_origin,
        "language": args.language,
        "personalData": not args.no_personal_data,
    }
    if args.reviews_start_date:
        payload["reviewsStartDate"] = args.reviews_start_date
    return payload


def build_quick_url_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.url.strip():
        raise SkillError("--url is required.")
    payload = quick_common_payload(args)
    payload["startUrls"] = [{"url": args.url.strip()}]
    return normalize_payload(payload)


def build_quick_place_id_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.place_id.strip():
        raise SkillError("--place-id is required.")
    payload = quick_common_payload(args)
    payload["placeIds"] = [args.place_id.strip()]
    return normalize_payload(payload)


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


def add_review_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--max-reviews", type=int, default=100, help="Reviews per place")
    parser.add_argument("--reviews-sort", default="newest", help="newest, mostRelevant, highestRanking, or lowestRanking")
    parser.add_argument("--reviews-origin", default="google", help="google or all")
    parser.add_argument("--reviews-start-date", help="YYYY-MM-DD or relative value such as '3 months'")
    parser.add_argument("--language", default="en", help="Google Maps language code")
    parser.add_argument("--no-personal-data", action="store_true", help="Set personalData=false")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Google Maps Reviews Scraper actor on Apify")
    sub = parser.add_subparsers(dest="command", required=True)

    quick_url = sub.add_parser("quick-url", help="Run by Google Maps URL")
    add_common_args(quick_url)
    add_review_args(quick_url)
    quick_url.add_argument("--url", required=True, help="Google Maps place/CID/review URL")

    quick_place = sub.add_parser("quick-place-id", help="Run by Google Place ID")
    add_common_args(quick_place)
    add_review_args(quick_place)
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
        if args.command == "quick-url":
            payload = build_quick_url_payload(args)
        elif args.command == "quick-place-id":
            payload = build_quick_place_id_payload(args)
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
