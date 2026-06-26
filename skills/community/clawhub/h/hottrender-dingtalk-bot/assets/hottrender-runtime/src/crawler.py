"""Basic crawling orchestration for daily trends and keyword hotspots."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.config import load_provider_config
from src.errors import user_error_message
from src.models import TrendItem, now_shanghai_iso
from src.providers import build_provider


DEFAULT_REGIONS = ["jp", "us", "tw", "kr"]
DEFAULT_DAILY_PLATFORMS = ["google", "youtube", "x"]
DEFAULT_KEYWORD_PLATFORMS = ["google", "youtube"]

REGION_LABELS = {
    "jp": "日本",
    "us": "美国",
    "tw": "台湾",
    "kr": "韩国",
}


def parse_csv(value: str | list[str] | tuple[str, ...] | None, default: list[str]) -> list[str]:
    """Parse a comma-separated option."""

    if isinstance(value, (list, tuple)):
        items = [str(item).strip() for item in value]
    else:
        items = [item.strip() for item in str(value or "").split(",")]
    parsed = [item for item in items if item]
    return parsed or list(default)


def fetch_daily_trends(
    *,
    regions: list[str] | None = None,
    platforms: list[str] | None = None,
    limit: int = 10,
    config_path: str | Path | None = None,
) -> dict[str, Any]:
    """Fetch daily trend lists across regions and platforms."""

    return _collect(
        mode="daily",
        regions=regions or DEFAULT_REGIONS,
        platforms=platforms or DEFAULT_DAILY_PLATFORMS,
        limit=limit,
        config_path=config_path,
        keywords=[],
        time_range="24h",
    )


def fetch_keyword_hotspots(
    *,
    keywords: list[str],
    regions: list[str] | None = None,
    platforms: list[str] | None = None,
    time_range: str = "7d",
    limit: int = 10,
    config_path: str | Path | None = None,
) -> dict[str, Any]:
    """Fetch custom keyword hotspot search results."""

    if not keywords:
        raise ValueError("at least one keyword is required")
    return _collect(
        mode="keyword",
        regions=regions or DEFAULT_REGIONS,
        platforms=platforms or DEFAULT_KEYWORD_PLATFORMS,
        limit=limit,
        config_path=config_path,
        keywords=keywords,
        time_range=time_range,
    )


def write_result(payload: dict[str, Any], output: str | Path | None, markdown: bool = True) -> None:
    """Write JSON and optional Markdown output."""

    if not output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    if suffix == ".json":
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    elif suffix == ".md" or markdown:
        output_path.write_text(render_markdown(payload), encoding="utf-8")
        json_path = output_path.with_suffix(".json")
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def render_markdown(payload: dict[str, Any]) -> str:
    """Render a compact Markdown report for human inspection."""

    mode = payload.get("mode", "")
    title = "四地区每日热点趋势" if mode == "daily" else "垂类关键词热点"
    lines = [
        f"# {title}",
        "",
        f"- 生成时间: {payload.get('generated_at', '')}",
        f"- 地区: {', '.join(_region_label(region) for region in payload.get('regions', []))}",
        f"- 平台: {', '.join(payload.get('platforms', []))}",
    ]
    if payload.get("keywords"):
        lines.append(f"- 关键词: {', '.join(payload['keywords'])}")
    lines.append("")

    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for item in payload.get("items", []):
        grouped.setdefault(item["region"], {}).setdefault(item["platform"], []).append(item)
    if not grouped:
        lines.extend(["暂无热点数据。", ""])
    for region in payload.get("regions", []):
        region_items = grouped.get(region, {})
        if not region_items:
            continue
        lines.extend([f"## {_region_label(region)}", ""])
        for platform in payload.get("platforms", []):
            items = region_items.get(platform, [])
            if not items:
                continue
            lines.extend([f"### {platform}", ""])
            for idx, item in enumerate(items, start=1):
                rank = item.get("rank") or idx
                keyword = f" [{item['keyword']}]" if item.get("keyword") else ""
                lines.append(f"{rank}. {item['title_original']}{keyword}")
                lines.append(f"   - 链接: {item['raw_url']}")
            lines.append("")

    errors = payload.get("errors", {})
    if errors:
        lines.extend(["## 抓取失败", ""])
        for key, message in errors.items():
            lines.append(f"- {key}: {message}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _collect(
    *,
    mode: str,
    regions: list[str],
    platforms: list[str],
    limit: int,
    config_path: str | Path | None,
    keywords: list[str],
    time_range: str,
) -> dict[str, Any]:
    provider_config = load_provider_config(config_path)
    items: list[TrendItem] = []
    errors: dict[str, str] = {}
    for platform in platforms:
        provider = build_provider(platform, provider_config.get(platform, {}))
        for region in regions:
            try:
                if mode == "daily":
                    fetched = provider.fetch_trends(region)[:limit]
                else:
                    fetched = []
                    for keyword in keywords:
                        fetched.extend(provider.search(region, keyword, time_range=time_range, limit=limit))
                    fetched = _dedupe(fetched)[: max(limit * max(len(keywords), 1), limit)]
                items.extend(fetched)
            except Exception as exc:
                errors[f"{platform}:{region}"] = user_error_message(exc)
    return {
        "mode": mode,
        "generated_at": now_shanghai_iso(),
        "regions": regions,
        "platforms": platforms,
        "keywords": keywords,
        "time_range": time_range,
        "items": [item.to_dict() for item in _dedupe(items)],
        "errors": errors,
    }


def _dedupe(items: list[TrendItem]) -> list[TrendItem]:
    seen = set()
    result = []
    for item in items:
        key = item.dedup_key()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _region_label(region: str) -> str:
    return REGION_LABELS.get(region, region)
