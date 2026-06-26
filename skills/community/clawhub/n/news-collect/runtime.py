from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from skill_runtime.writing_core import OPENING_TYPES, STRUCTURE_TYPES, build_angle_pack


PROFILE_SOURCES: dict[str, list[str]] = {
    "mixed_daily": ["hackernews", "github", "36kr", "wallstreetcn", "weibo"],
    "global_latest": ["hackernews", "github", "producthunt"],
    "global_ai": ["hackernews", "github", "ai_newsletters"],
    "cn_media": ["36kr", "wallstreetcn", "tencent", "weibo", "v2ex"],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or datetime.now().strftime("%Y%m%d-%H%M%S")


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def truncate_text(value: Any, limit: int) -> str:
    cleaned = clean_text(value)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(limit - 1, 0)].rstrip() + "…"


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = read_text(path)
    if not text.startswith("---"):
        return {}, text.strip()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, flags=re.DOTALL)
    if not match:
        return {}, text.strip()

    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter must be a mapping: {path}")
    return frontmatter, match.group(2).strip()


def normalize_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = clean_text(value).lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def normalize_int(value: Any, default: int, *, minimum: int = 1, maximum: int = 50) -> int:
    if value in {None, ""}:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(parsed, maximum))


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [clean_text(item) for item in value if clean_text(item)]
    return [part.strip() for part in str(value).split(",") if part.strip()]


def parse_json_output(stdout: str) -> Any:
    stripped = stdout.strip()
    if not stripped:
        return []

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        for start_char, end_char in (("[", "]"), ("{", "}")):
            start = stripped.find(start_char)
            end = stripped.rfind(end_char)
            if start != -1 and end != -1 and end > start:
                return json.loads(stripped[start : end + 1])
    raise ValueError("Vendor skill did not return valid JSON.")


def resolve_request(path: Path) -> dict[str, Any]:
    frontmatter, notes = parse_frontmatter(path)

    profile = clean_text(frontmatter.get("profile") or "mixed_daily").lower()
    if profile == "custom":
        sources = normalize_list(frontmatter.get("sources"))
        if not sources:
            raise ValueError("`profile: custom` requires a non-empty `sources` field.")
    elif profile in PROFILE_SOURCES:
        sources = PROFILE_SOURCES[profile]
    else:
        supported = ", ".join(["mixed_daily", "global_latest", "global_ai", "cn_media", "custom"])
        raise ValueError(f"Unsupported profile `{profile}`. Supported values: {supported}")

    keyword = clean_text(frontmatter.get("keyword"))
    title = clean_text(frontmatter.get("title")) or clean_text(frontmatter.get("name"))
    limit = normalize_int(frontmatter.get("limit"), default=10)
    deep = normalize_bool(frontmatter.get("deep"), default=False)
    slug = slugify(title or keyword or profile)
    today = datetime.now()

    return {
        "profile": profile,
        "sources": sources,
        "keyword": keyword,
        "title": title or f"{profile} 资讯扫描",
        "limit": limit,
        "deep": deep,
        "notes": notes,
        "slug": slug,
        "date": today.strftime("%Y%m%d"),
        "raw_date": today.strftime("%Y-%m-%d"),
    }


def build_command(*, workspace_root: Path, vendor_root: Path, request: dict[str, Any]) -> list[str]:
    python_path = workspace_root / ".venv" / "bin" / "python"
    interpreter = python_path if python_path.exists() else Path(sys.executable)
    command = [
        str(interpreter),
        str(vendor_root / "scripts" / "fetch_news.py"),
        "--source",
        ",".join(request["sources"]),
        "--limit",
        str(request["limit"]),
        "--no-save",
    ]
    if request["keyword"]:
        command.extend(["--keyword", request["keyword"]])
    if request["deep"]:
        command.append("--deep")
    return command


def pick_recommended_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chosen: list[dict[str, Any]] = []
    seen_titles: set[str] = set()
    seen_sources: set[str] = set()

    for item in items:
        title = clean_text(item.get("title"))
        source = clean_text(item.get("source")) or "未知来源"
        if not title or title in seen_titles:
            continue
        if source in seen_sources and len(seen_sources) < 3:
            continue
        chosen.append(item)
        seen_titles.add(title)
        seen_sources.add(source)
        if len(chosen) >= 3:
            return chosen

    for item in items:
        title = clean_text(item.get("title"))
        if not title or title in seen_titles:
            continue
        chosen.append(item)
        seen_titles.add(title)
        if len(chosen) >= 3:
            break
    return chosen


def angle_hint(item: dict[str, Any]) -> str:
    source = clean_text(item.get("source"))
    if "GitHub" in source:
        return "适合延展成“工具能力变化会怎样改写工作流”的实战角度。"
    if "Weibo" in source:
        return "适合写成“舆论热点背后真正值得关注的结构变化”。"
    if any(token in source for token in ["36氪", "华尔街", "腾讯", "V2EX"]):
        return "适合拆成“行业动态 -> 业务影响 -> 个人行动”的评论结构。"
    return "适合写成“这件事为什么值得现在关注”的观点型长文。"


def format_item(index: int, item: dict[str, Any]) -> str:
    title = clean_text(item.get("title")) or f"候选条目 {index}"
    url = clean_text(item.get("url"))
    source = clean_text(item.get("source")) or "未知来源"
    time_label = clean_text(item.get("time")) or "Unknown Time"
    heat = clean_text(item.get("heat")) or "无热度字段"
    summary = truncate_text(item.get("summary") or item.get("content") or "", 140) or "原始结果未附带摘要，可回看 raw JSON。"
    extras: list[str] = []
    if clean_text(item.get("hn_url")):
        extras.append(f"讨论链接：{item['hn_url']}")
    if item.get("smart_fill"):
        extras.append("该条目为补位结果，建议二次核验。")

    lines = [f"{index}. [{title}]({url})" if url else f"{index}. {title}"]
    lines.append(f"- 来源：{source} | 时间：{time_label} | 热度：{heat}")
    lines.append(f"- 摘要：{summary}")
    for extra in extras:
        lines.append(f"- 备注：{extra}")
    return "\n".join(lines)


def build_report(
    *,
    request: dict[str, Any],
    items: list[dict[str, Any]],
    recommended_topics: list[dict[str, Any]],
    raw_path: Path,
    request_path: Path,
    stderr_text: str,
) -> str:
    source_counts = Counter(clean_text(item.get("source")) or "未知来源" for item in items)
    source_summary = "、".join(f"{name}（{count}）" for name, count in source_counts.most_common()) or "无结果"
    summary_lines = [
        f"- 共抓取 {len(items)} 条候选信息，覆盖 {len(source_counts)} 个来源：{source_summary}",
        f"- 扫描 profile：`{request['profile']}`；实际来源：{', '.join(request['sources'])}",
        f"- 关键词过滤：{request['keyword'] or '未设置'}；深抓正文：{'开启' if request['deep'] else '关闭'}",
    ]
    if request["notes"]:
        summary_lines.append(f"- 请求备注：{truncate_text(request['notes'], 120)}")
    if stderr_text.strip():
        summary_lines.append(f"- Vendor stderr：{truncate_text(stderr_text, 120)}")

    if items:
        candidate_lines = [format_item(index, item) for index, item in enumerate(items, start=1)]
    else:
        candidate_lines = ["- 本次扫描未获取到候选条目，可调整 `profile`、`keyword` 或 `limit` 后重试。"]

    if recommended_topics:
        recommendation_lines = []
        writeworthiness_lines = []
        cut_lines = []
        angle_lines = []
        headline_lines = []
        avoid_lines = []
        for index, item in enumerate(recommended_topics, start=1):
            title = clean_text(item.get("title")) or f"候选题目 {index}"
            source = clean_text(item.get("source")) or "未知来源"
            heat = clean_text(item.get("heat")) or "无热度字段"
            angle_pack = item.get("angle_pack") or {}
            recommendation_lines.extend(
                [
                    f"{index}. {title}",
                    f"- 推荐理由：来源 {source}，热度信号 {heat}。",
                    f"- 写作角度：{angle_hint(item)}",
                    f"- 值得写评分：{angle_pack.get('writeworthiness_score', 'N/A')}",
                ]
            )
            writeworthiness_lines.extend(
                [
                    f"### {index}. {title}",
                    "",
                    f"- `writeworthiness_score`：{angle_pack.get('writeworthiness_score', 'N/A')}",
                    f"- `primary_reader`：{angle_pack.get('primary_reader', '未识别')}",
                    f"- `primary_pain_point`：{angle_pack.get('primary_pain_point', '未识别')}",
                    f"- `shareability_note`：{angle_pack.get('shareability_note', '未识别')}",
                    "",
                ]
            )
            cut_lines.extend(
                [
                    f"### {index}. {title}",
                    "",
                    f"- 推荐切口：{angle_hint(item)}",
                    f"- 更适合先打的痛点：{angle_pack.get('primary_pain_point', '未识别')}",
                    "",
                ]
            )
            angle_lines.extend(
                [
                    f"### {index}. {title}",
                    "",
                    f"- `recommended_structure`：{STRUCTURE_TYPES.get(angle_pack.get('recommended_structure', ''), angle_pack.get('recommended_structure', 'unknown'))}",
                    f"- `recommended_opening_type`：{OPENING_TYPES.get(angle_pack.get('recommended_opening_type', ''), angle_pack.get('recommended_opening_label', 'unknown'))}",
                    "",
                ]
            )
            headline_lines.extend([f"### {index}. {title}", ""])
            for candidate_title in angle_pack.get("title_angles") or []:
                headline_lines.append(f"- {candidate_title}")
            headline_lines.append("")
            avoid_lines.extend(
                [
                    f"### {index}. {title}",
                    "",
                    f"- `evidence_gap`：{angle_pack.get('evidence_gap', '未识别')}",
                    f"- `risk_note`：{angle_pack.get('risk_note', '未识别')}",
                    "",
                ]
            )
    else:
        recommendation_lines = ["- 当前没有足够结果生成推荐选题。"]
        writeworthiness_lines = ["- 当前结果不足，暂时无法给出稳定的写作价值判断。"]
        cut_lines = ["- 当前结果不足，暂时无法推荐稳定切口。"]
        angle_lines = ["- 当前结果不足，建议先换关键词或放宽来源。"]
        headline_lines = ["- 当前没有足够结果生成标题方向。"]
        avoid_lines = ["- 当前不建议强行写成长文，容易变成空泛趋势稿。"]

    lines = [
        f"# 资讯扫描报告：{request['title']}",
        "",
        "## 基础信息",
        "",
        f"- `date`：{request['date']}",
        f"- `slug`：{request['slug']}",
        f"- `title`：{request['title']}",
        f"- `profile`：{request['profile']}",
        f"- `sources`：{', '.join(request['sources'])}",
        f"- `keyword`：{request['keyword'] or '未设置'}",
        f"- `limit`：{request['limit']}",
        f"- `deep`：{'true' if request['deep'] else 'false'}",
        f"- `request_path`：{request_path}",
        "",
        "## 扫描摘要",
        "",
        *summary_lines,
        "",
        "## 候选条目",
        "",
        *candidate_lines,
        "",
        "## 推荐选题",
        "",
        *recommendation_lines,
        "",
        "## 写作价值判断",
        "",
        *writeworthiness_lines,
        "",
        "## 推荐切口",
        "",
        *cut_lines,
        "",
        "## 推荐框架与开头",
        "",
        *angle_lines,
        "",
        "## 标题方向",
        "",
        *headline_lines,
        "",
        "## 不建议写法",
        "",
        *avoid_lines,
        "",
        "## 原始数据位置",
        "",
        f"- Raw JSON：{raw_path}",
    ]
    return "\n".join(lines) + "\n"


def run_news_collect(input_path: Path, *, workspace_root: Path, vendor_root: Path) -> dict[str, Any]:
    request = resolve_request(input_path)
    command = build_command(workspace_root=workspace_root, vendor_root=vendor_root, request=request)

    completed = subprocess.run(
        command,
        cwd=vendor_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "news-aggregator-skill 执行失败："
            + (clean_text(completed.stderr) or clean_text(completed.stdout) or "未知错误")
        )

    items = parse_json_output(completed.stdout)
    if not isinstance(items, list):
        raise ValueError("Expected news scan output to be a JSON list.")
    recommended_items = pick_recommended_items(items)
    recommended_topics = []
    for item in recommended_items:
        title = clean_text(item.get("title"))
        summary = truncate_text(item.get("summary") or item.get("content") or "", 180)
        source = clean_text(item.get("source"))
        angle_pack = build_angle_pack(
            topic=title or request["title"],
            summary=summary or angle_hint(item),
            reader_hint="希望把资讯转成公众号观点文的读者",
            source_hint=source,
            evidence_gap="需要二次核验原文与上下文，避免只根据资讯摘要下结论。",
        )
        enriched_item = dict(item)
        enriched_item["angle_pack"] = angle_pack
        enriched_item["writeworthiness_score"] = angle_pack["writeworthiness_score"]
        recommended_topics.append(enriched_item)

    inbox_dir = workspace_root / "content-production" / "inbox"
    raw_path = inbox_dir / "raw" / "news" / request["raw_date"] / f"{request['slug']}.json"
    report_path = inbox_dir / f"{request['date']}-{request['slug']}-news-report.md"

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "request": {
            "profile": request["profile"],
            "sources": request["sources"],
            "keyword": request["keyword"],
            "limit": request["limit"],
            "deep": request["deep"],
            "title": request["title"],
            "request_path": str(input_path),
        },
        "vendor_skill_path": str(vendor_root),
        "command": command,
        "stderr": completed.stderr,
        "items": items,
        "recommended_topics": recommended_topics,
    }

    write_text(raw_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    write_text(
        report_path,
        build_report(
            request=request,
            items=items,
            recommended_topics=recommended_topics,
            raw_path=raw_path,
            request_path=input_path,
            stderr_text=completed.stderr,
        ),
    )

    return {
        "slug": request["slug"],
        "title": request["title"],
        "profile": request["profile"],
        "sources": request["sources"],
        "item_count": len(items),
        "recommended_count": len(recommended_topics),
        "raw_path": raw_path,
        "report_path": report_path,
    }
