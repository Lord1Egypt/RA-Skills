#!/usr/bin/env python3
"""Discover KOL contacts and similar creators through AIsa WaveInflu APIs."""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.aisa.one/apis/v1"
EMAIL_LOOKUP_PATH = "/waveinflu/email-lookup"
SIMILAR_PATH = "/waveinflu/similar"
USER_AGENT = "AIsa KOL Creator Discovery Skill/1.0"


def ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def api_key() -> str:
    key = os.getenv("AISA_API_KEY", "").strip()
    if not key:
        raise SystemExit("AISA_API_KEY is not set.")
    return key


def post_json(path: str, payload: dict[str, Any], retries: int = 2) -> dict[str, Any]:
    url = API_BASE + path
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(
                request, timeout=120, context=ssl_context()
            ) as response:
                text = response.read().decode("utf-8")
                result = json.loads(text) if text else {}
                if not isinstance(result, dict):
                    raise RuntimeError(f"Unexpected response from {url}")
                code = result.get("code")
                if code is not None and code != 1000:
                    message = result.get("message") or "Unknown AIsa API error"
                    raise RuntimeError(f"AIsa API code {code} from {url}: {message}")
                return result
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if attempt < retries and (exc.code == 429 or exc.code >= 500):
                time.sleep(2**attempt)
                continue
            raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
        except urllib.error.URLError as exc:
            if attempt < retries:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(f"Request failed for {url}: {exc.reason}") from exc

    raise RuntimeError(f"Request failed for {url}")


def response_data(response: dict[str, Any]) -> dict[str, Any]:
    data = response.get("data")
    return data if isinstance(data, dict) else {}


def profile_platform(url: str) -> str | None:
    host = urllib.parse.urlsplit(url).netloc.lower()
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "tiktok.com" in host:
        return "tiktok"
    if "instagram.com" in host:
        return "instagram"
    return None


def validate_profile_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Invalid profile URL: {url}")
    platform = profile_platform(url)
    if not platform:
        raise ValueError(
            "Profile URL must be from TikTok, Instagram, or YouTube: " + url
        )
    path = parsed.path.lower()
    post_patterns = {
        "youtube": ("/watch", "/shorts/", "/clip/"),
        "tiktok": ("/video/",),
        "instagram": ("/p/", "/reel/", "/reels/", "/tv/"),
    }
    if "youtu.be" in parsed.netloc.lower() or any(
        marker in path for marker in post_patterns[platform]
    ):
        raise ValueError("Use a creator profile URL, not a post or video URL: " + url)
    return url.strip()


def lookup_email(url: str) -> dict[str, Any]:
    return response_data(post_json(EMAIL_LOOKUP_PATH, {"url": url}))


def csv_values(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def similar_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.platform:
        raise ValueError("--platform must be youtube or tiktok.")
    if not args.seed_profile_url and not args.content_direction:
        raise ValueError(
            "Provide --seed-profile-url, --content-direction, or both."
        )

    payload: dict[str, Any] = {
        "platform": args.platform,
        "limit": args.limit,
    }
    if args.seed_profile_url:
        seed = validate_profile_url(args.seed_profile_url)
        if profile_platform(seed) not in {"youtube", "tiktok"}:
            raise ValueError(
                "WaveInflu similar matching accepts only YouTube or TikTok seed URLs."
            )
        payload["seedProfileUrl"] = seed
    if args.content_direction:
        if len(args.content_direction) > 800:
            raise ValueError("--content-direction must be 800 characters or fewer.")
        payload["contentDirection"] = args.content_direction

    filters: dict[str, Any] = {}
    if csv_values(args.regions):
        filters["regions"] = csv_values(args.regions)
    if csv_values(args.languages):
        filters["languages"] = csv_values(args.languages)
    for arg_name, api_name in (
        ("min_followers", "minFollowers"),
        ("max_followers", "maxFollowers"),
        ("min_average_views", "minVideosAverageViews"),
        ("max_average_views", "maxVideosAverageViews"),
    ):
        value = getattr(args, arg_name, None)
        if value is not None:
            filters[api_name] = value
    if filters:
        payload["filters"] = filters
    return payload


def find_similar(args: argparse.Namespace) -> dict[str, Any]:
    return response_data(post_json(SIMILAR_PATH, similar_payload(args)))


def creator_profile(creator: dict[str, Any]) -> str:
    profile = str(creator.get("profileUrl") or "").strip()
    if profile:
        return profile
    platform = str(creator.get("platform") or "").lower()
    handle = str(
        creator.get("platformHandle") or creator.get("username") or ""
    ).strip().lstrip("@")
    if not handle:
        return ""
    if platform == "youtube":
        return f"https://www.youtube.com/@{handle}"
    if platform == "tiktok":
        return f"https://www.tiktok.com/@{handle}"
    return ""


def primary_email(data: dict[str, Any]) -> str | None:
    email = data.get("email")
    if isinstance(email, str) and email.strip():
        return email.strip()
    emails = data.get("emails")
    if isinstance(emails, list):
        for value in emails:
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def normalized_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    return urllib.parse.urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", "")
    )


def compact_number(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return "—"
    number = float(value)
    for divisor, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "K")):
        if abs(number) >= divisor:
            rendered = f"{number / divisor:.1f}".rstrip("0").rstrip(".")
            return rendered + suffix
    return str(int(number) if number.is_integer() else round(number, 1))


def md_escape(value: Any) -> str:
    return str(value if value not in (None, "") else "—").replace("|", "\\|")


def percentage(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return "—"
    return f"{float(value) * 100:.0f}%"


def report_markdown(report: dict[str, Any]) -> str:
    scope = report["scope"]
    rows = report["creators"]
    lines = [
        "# KOL Contact & Similar Creator Report",
        "",
        "## Scope",
        "",
        f"- Seed profile: {scope['seedProfileUrl']}",
        f"- Seed platform: {scope['seedPlatform']}",
        f"- Target discovery platform: {scope['targetPlatform']}",
        f"- Content direction: {scope.get('contentDirection') or '—'}",
        f"- Filters: {json.dumps(scope.get('filters') or {}, ensure_ascii=False)}",
        f"- Similar creators requested: {scope['requested']}",
        f"- Similar creators returned: {scope['returned']}",
        f"- Emails found: {report['coverage']['emailsFound']} / {len(rows)}",
        "",
        "## Recommended Outreach List",
        "",
        "| Role | Rank | Creator | Platform | Profile | Similarity | Followers | Avg. views | Region / language | Email | Lookup status |",
        "|---|---:|---|---|---|---:|---:|---:|---|---|---|",
    ]
    for row in rows:
        region_language = " / ".join(
            value for value in (row.get("region"), row.get("language")) if value
        ) or "—"
        lines.append(
            "| "
            + " | ".join(
                [
                    md_escape(row.get("role")),
                    md_escape(row.get("rank")),
                    md_escape(row.get("creator")),
                    md_escape(row.get("platform")),
                    md_escape(row.get("profileUrl")),
                    percentage(row.get("similarityScore")),
                    compact_number(row.get("followerCount")),
                    compact_number(row.get("averagePlayCount")),
                    md_escape(region_language),
                    md_escape(row.get("email") or "Not found"),
                    md_escape(row.get("lookupStatus")),
                ]
            )
            + " |"
        )

    coverage = report["coverage"]
    lines.extend(
        [
            "",
            "## Coverage Notes",
            "",
            f"- Email found: {coverage['emailsFound']}",
            f"- Email not found: {coverage['notFound']}",
            f"- Lookup failed: {coverage['lookupFailed']}",
        ]
    )
    for note in report.get("notes", []):
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_text(path: str | None, content: str) -> None:
    if path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")


def write_json(path: str | None, data: Any) -> None:
    content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    write_text(path, content)


def command_lookup(args: argparse.Namespace) -> None:
    results = []
    for raw_url in args.profile_urls:
        url = validate_profile_url(raw_url)
        try:
            data = lookup_email(url)
            results.append({"profileUrl": url, "status": "found" if primary_email(data) else "not_found", "data": data})
        except RuntimeError as exc:
            results.append({"profileUrl": url, "status": "lookup_failed", "error": str(exc)})
    write_json(args.out, {"results": results})


def command_similar(args: argparse.Namespace) -> None:
    write_json(args.out, find_similar(args))


def command_research(args: argparse.Namespace) -> None:
    seed_url = validate_profile_url(args.profile_url)
    seed_platform = profile_platform(seed_url) or "unknown"
    if not args.platform and seed_platform in {"youtube", "tiktok"}:
        args.platform = seed_platform
    if seed_platform == "instagram":
        if not args.platform:
            raise SystemExit(
                "Instagram seeds require --platform youtube or tiktok for similar creators."
            )
        if not args.content_direction:
            raise SystemExit(
                "Instagram seeds require --content-direction because similarity matching accepts only YouTube/TikTok seeds."
            )
    if not args.platform:
        raise SystemExit("Could not infer target platform; pass --platform youtube or tiktok.")
    if args.limit > 25 and not args.allow_large_enrichment:
        raise SystemExit(
            "More than 25 email lookups requires --allow-large-enrichment after confirming quota scope."
        )

    notes: list[str] = []
    try:
        seed_data = lookup_email(seed_url)
        seed_status = "Found" if primary_email(seed_data) else "Not found"
    except RuntimeError as exc:
        seed_data = {}
        seed_status = "Lookup failed"
        notes.append(f"Seed email lookup failed: {exc}")

    args.seed_profile_url = seed_url if seed_platform in {"youtube", "tiktok"} else None
    similar_data = find_similar(args)
    raw_creators = similar_data.get("data")
    creators = raw_creators if isinstance(raw_creators, list) else []

    seed_row = {
        "role": "Seed",
        "rank": "—",
        "creator": seed_data.get("username") or seed_url,
        "platform": seed_data.get("platform") or seed_platform,
        "profileUrl": seed_data.get("profileLink") or seed_url,
        "similarityScore": None,
        "followerCount": None,
        "averagePlayCount": None,
        "region": seed_data.get("region"),
        "language": None,
        "email": primary_email(seed_data),
        "lookupStatus": seed_status,
    }
    rows = [seed_row]
    seen = {normalized_url(seed_row["profileUrl"])}

    for creator in creators:
        if not isinstance(creator, dict):
            continue
        profile_url = creator_profile(creator)
        if not profile_url:
            continue
        key = normalized_url(profile_url)
        if key in seen:
            continue
        seen.add(key)
        email_data: dict[str, Any] = {}
        lookup_status = "Not found"
        try:
            email_data = lookup_email(profile_url)
            lookup_status = "Found" if primary_email(email_data) else "Not found"
        except RuntimeError as exc:
            lookup_status = "Lookup failed"
            notes.append(f"Email lookup failed for {profile_url}: {exc}")

        email = primary_email(email_data) or primary_email(creator)
        if email and lookup_status != "Found":
            lookup_status = "Found in similarity result"

        rows.append(
            {
                "role": "Similar",
                "rank": len(rows),
                "creator": creator.get("channelTitle") or creator.get("username") or creator.get("platformHandle") or "Unknown",
                "platform": creator.get("platform") or args.platform,
                "profileUrl": profile_url,
                "similarityScore": creator.get("similarityScore"),
                "followerCount": creator.get("followerCount"),
                "averagePlayCount": creator.get("averagePlayCount"),
                "region": creator.get("region") or email_data.get("region"),
                "language": creator.get("language"),
                "email": email,
                "lookupStatus": lookup_status,
            }
        )

    found = sum(1 for row in rows if row.get("email"))
    failed = sum(1 for row in rows if row.get("lookupStatus") == "Lookup failed")
    report = {
        "scope": {
            "seedProfileUrl": seed_url,
            "seedPlatform": seed_platform,
            "targetPlatform": args.platform,
            "contentDirection": args.content_direction,
            "filters": similar_payload(args).get("filters", {}),
            "requested": args.limit,
            "returned": max(0, len(rows) - 1),
        },
        "coverage": {
            "emailsFound": found,
            "notFound": len(rows) - found - failed,
            "lookupFailed": failed,
        },
        "creators": rows,
        "quota": {
            "seedEmailLookup": seed_data.get("quota"),
            "similarCreators": similar_data.get("quota"),
        },
        "notes": notes,
    }
    write_text(args.out, report_markdown(report))
    if args.json_out:
        write_json(args.json_out, report)


def add_similar_args(parser: argparse.ArgumentParser, include_seed: bool = True) -> None:
    parser.add_argument("--platform", choices=["youtube", "tiktok"])
    if include_seed:
        parser.add_argument("--seed-profile-url")
    parser.add_argument("--content-direction")
    parser.add_argument("--limit", type=int, default=10, choices=range(1, 101), metavar="1-100")
    parser.add_argument("--regions", help="Comma-separated region codes.")
    parser.add_argument("--languages", help="Comma-separated language codes.")
    parser.add_argument("--min-followers", type=int)
    parser.add_argument("--max-followers", type=int)
    parser.add_argument("--min-average-views", type=int)
    parser.add_argument("--max-average-views", type=int)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find KOL emails and similar creators through AIsa WaveInflu APIs."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    lookup = commands.add_parser("lookup", help="Look up creator emails.")
    lookup.add_argument("profile_urls", nargs="+")
    lookup.add_argument("--out", help="Optional JSON output path.")
    lookup.set_defaults(func=command_lookup)

    similar = commands.add_parser("similar", help="Find similar creators.")
    add_similar_args(similar)
    similar.add_argument("--out", help="Optional JSON output path.")
    similar.set_defaults(func=command_similar)

    research = commands.add_parser(
        "research", help="Run lookup, similar discovery, and email enrichment."
    )
    research.add_argument("profile_url")
    add_similar_args(research, include_seed=False)
    research.add_argument("--allow-large-enrichment", action="store_true")
    research.add_argument("--out", help="Optional Markdown output path.")
    research.add_argument("--json-out", help="Optional JSON output path.")
    research.set_defaults(func=command_research)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except ValueError as exc:
        parser.error(str(exc))
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
