#!/usr/bin/env python3
"""Build deterministic search URLs for multiple engines.

No network calls are performed by this script. It only composes URLs from
local templates so an agent can inspect or open them later.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote_plus


CATALOG_PATH = Path(__file__).resolve().parents[1] / "resources" / "engine-catalog.json"

TIME_MAP = {
    "google": {"hour": "qdr:h", "day": "qdr:d", "week": "qdr:w", "month": "qdr:m", "year": "qdr:y"},
    "google-hk": {"hour": "qdr:h", "day": "qdr:d", "week": "qdr:w", "month": "qdr:m", "year": "qdr:y"},
    "bing-cn": {"day": "ez1", "week": "ez2", "month": "ez3"},
    "bing-int": {"day": "ez1", "week": "ez2", "month": "ez3"},
    "brave": {"day": "pd", "week": "pw", "month": "pm", "year": "py"},
}
SAFE_MAP = {
    "google": {"off": "off", "moderate": "medium", "strict": "active"},
    "google-hk": {"off": "off", "moderate": "medium", "strict": "active"},
    "bing-cn": {"off": "off", "moderate": "moderate", "strict": "strict"},
    "bing-int": {"off": "off", "moderate": "moderate", "strict": "strict"},
    "duckduckgo": {"off": "-1", "moderate": "0", "strict": "1"},
}
LANG_PARAM_MAP = {
    "google": "lr",
    "google-hk": "lr",
    "bing-cn": "setlang",
    "bing-int": "setlang",
}


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Missing engine catalog: {CATALOG_PATH}")
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_index(catalog: dict) -> tuple[dict, dict]:
    engines = {e["id"]: e for e in catalog["engines"]}
    aliases = {}
    for engine in catalog["engines"]:
        aliases[engine["id"]] = engine["id"]
        for alias in engine.get("aliases", []):
            aliases[alias] = engine["id"]
    return engines, aliases


def parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def normalize_engine_ids(raw_ids: list[str], aliases: dict[str, str]) -> list[str]:
    normalized = []
    unknown = []
    for raw in raw_ids:
        key = raw.strip().lower()
        if key in aliases:
            normalized.append(aliases[key])
        else:
            unknown.append(raw)
    if unknown:
        known = ", ".join(sorted(aliases.keys()))
        raise ValueError(f"Unknown engines: {', '.join(unknown)}. Known ids/aliases: {known}")
    deduped = []
    seen = set()
    for eid in normalized:
        if eid not in seen:
            seen.add(eid)
            deduped.append(eid)
    return deduped


def compose_query(args: argparse.Namespace) -> str:
    parts: list[str] = []
    if args.site:
        parts.append(f"site:{args.site}")
    if args.filetype:
        parts.append(f"filetype:{args.filetype}")
    if args.exact:
        parts.append(f'"{args.exact}"')
    if args.query:
        parts.append(args.query.strip())
    if args.or_terms:
        terms = [t.strip() for t in args.or_terms.split(",") if t.strip()]
        if terms:
            parts.append("(" + " OR ".join(terms) + ")")
    for term in args.exclude:
        term = term.strip()
        if term:
            parts.append(f"-{term}")
    query = " ".join(parts).strip()
    if not query:
        raise ValueError("Composed query is empty. Provide --query or one of the operator arguments.")
    return query


def append_params(engine_id: str, base_url: str, args: argparse.Namespace) -> str:
    sep = "&" if "?" in base_url else "?"
    extras = []

    if args.time:
        time_map = TIME_MAP.get(engine_id, {})
        if args.time in time_map:
            if engine_id.startswith("bing"):
                extras.append(f"filters=ex1%3a%22{time_map[args.time]}%22")
            elif engine_id == "brave":
                extras.append(f"time_period={time_map[args.time]}")
            else:
                extras.append(f"tbs={time_map[args.time]}")

    if args.safe:
        safe_map = SAFE_MAP.get(engine_id, {})
        if args.safe in safe_map:
            if engine_id.startswith("bing"):
                extras.append(f"adlt={safe_map[args.safe]}")
            elif engine_id == "duckduckgo":
                extras.append(f"kp={safe_map[args.safe]}")
            else:
                extras.append(f"safe={safe_map[args.safe]}")

    if args.lang:
        lang_key = LANG_PARAM_MAP.get(engine_id)
        if lang_key:
            extras.append(f"{lang_key}={quote_plus(args.lang)}")

    if extras:
        return base_url + sep + "&".join(extras)
    return base_url


def choose_engines(args: argparse.Namespace, catalog: dict, aliases: dict[str, str], engines: dict[str, dict]) -> list[str]:
    explicit = []
    if args.engine:
        explicit.extend(parse_csv(args.engine))
    if args.compare:
        explicit.extend(parse_csv(args.compare))
    if explicit:
        return normalize_engine_ids(explicit, aliases)

    if args.preset:
        preset_ids = catalog["presets"].get(args.preset)
        if not preset_ids:
            known = ", ".join(sorted(catalog["presets"].keys()))
            raise ValueError(f"Unknown preset: {args.preset}. Known presets: {known}")
        return normalize_engine_ids(preset_ids, aliases)

    if args.region:
        selected = [eid for eid, data in engines.items() if data.get("region") == args.region]
        if selected:
            # keep concise defaults per region
            if args.region == "cn":
                return [eid for eid in ["baidu", "sogou", "toutiao"] if eid in selected]
            return [eid for eid in ["google", "bing-int", "brave"] if eid in selected]

    return [catalog.get("defaultEngine", "google")]


def render(entries: list[dict], fmt: str) -> str:
    if fmt == "json":
        return json.dumps({"results": entries}, ensure_ascii=False, indent=2)
    if fmt == "markdown":
        lines = ["# Search URLs", ""]
        for item in entries:
            lines.append(f"- **{item['engine_name']}** (`{item['engine_id']}`): {item['url']}")
        return "\n".join(lines)
    return "\n".join(f"[{item['engine_id']}] {item['url']}" for item in entries)


def build_entries(args: argparse.Namespace) -> list[dict]:
    catalog = load_catalog()
    engines, aliases = build_index(catalog)
    query = compose_query(args)
    query_encoded = quote_plus(query)
    selected_ids = choose_engines(args, catalog, aliases, engines)

    entries = []
    for engine_id in selected_ids:
        engine = engines[engine_id]
        url = engine["url"].replace("{query}", query_encoded)
        url = append_params(engine_id, url, args)
        entries.append(
            {
                "engine_id": engine_id,
                "engine_name": engine["name"],
                "region": engine["region"],
                "query": query,
                "url": url,
            }
        )
    return entries


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build search URLs across multiple engines without making network calls."
    )
    parser.add_argument("--query", default="", help="Base query text.")
    parser.add_argument("--engine", help="Single engine id or comma-separated ids.")
    parser.add_argument("--compare", help="Comma-separated engine ids for compare mode.")
    parser.add_argument("--preset", choices=["balanced", "cn-research", "privacy", "knowledge"])
    parser.add_argument("--region", choices=["cn", "global"], help="Choose default engine set by region.")
    parser.add_argument("--site", help="Restrict to a site, e.g. github.com")
    parser.add_argument("--filetype", help="Restrict to a file type, e.g. pdf")
    parser.add_argument("--exact", help="Exact phrase to quote.")
    parser.add_argument("--exclude", action="append", default=[], help="Exclude term; may be passed multiple times.")
    parser.add_argument("--or-terms", help="Comma-separated alternative terms to join with OR.")
    parser.add_argument("--time", choices=["hour", "day", "week", "month", "year"])
    parser.add_argument("--lang", help="Language/locale hint, e.g. en, zh-CN, ja")
    parser.add_argument("--safe", choices=["off", "moderate", "strict"])
    parser.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    try:
        entries = build_entries(args)
        print(render(entries, args.format))
        return 0
    except Exception as exc:  # noqa: BLE001 - deliberate CLI error boundary
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
