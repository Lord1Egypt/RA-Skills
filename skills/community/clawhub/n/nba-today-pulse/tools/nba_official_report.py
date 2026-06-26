#!/usr/bin/env python3
"""Fast NBA.com official story lookup and deterministic summary rendering."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timedelta
from typing import Any

from nba_common import NBAReportError
from nba_pulse_core import command_options
from nba_teams import canonicalize_team_abbr, extract_teams_from_text, format_matchup_display, team_display_name
from nba_today_report import load_candidate_events, normalize_competitors
from provider_nba import fetch_nba_game_story, fetch_nba_game_story_url, find_game_id_by_matchup, find_game_id_by_schedule, public_game_story_payload
from timezone_resolver import resolve_timezone


GAME_URL_RE = re.compile(r"https?://[^\s)>\]}]+/game/[^\s)>\]}，。]+", re.IGNORECASE)
GAME_URL_PARTS_RE = re.compile(r"/game/(?P<away>[a-z0-9-]+)-vs-(?P<home>[a-z0-9-]+)-(?P<game_id>\d+)", re.IGNORECASE)


def _clean_url(value: str) -> str:
    return str(value or "").strip().rstrip(".,，。；;!?！？)")


def extract_game_url(command: str | None) -> str | None:
    match = GAME_URL_RE.search(command or "")
    return _clean_url(match.group(0)) if match else None


def _target_from_url(url: str) -> dict[str, Any]:
    match = GAME_URL_PARTS_RE.search(url or "")
    away = canonicalize_team_abbr(match.group("away")) if match else ""
    home = canonicalize_team_abbr(match.group("home")) if match else ""
    game_id = str(match.group("game_id") or "") if match else ""
    return {
        "url": url,
        "away": {"abbr": away, "name": away},
        "home": {"abbr": home, "name": home},
        "gameId": game_id,
        "status": "",
        "startTime": "",
        "venue": "",
    }


def _reference_now(tz: str | None) -> datetime:
    resolved = resolve_timezone(tz)
    raw = (os.environ.get("NBA_TR_NOW_ISO") or "").strip()
    if raw:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=resolved.tzinfo)
        return parsed.astimezone(resolved.tzinfo)
    return datetime.now(resolved.tzinfo)


def _target_date(date_text: str | None, tz: str | None) -> datetime.date:
    if date_text:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    return _reference_now(tz).date()


def _team_from_competitor(competitor: dict[str, Any]) -> dict[str, str]:
    team = competitor.get("team") or {}
    abbr = canonicalize_team_abbr(team.get("abbreviation"))
    return {
        "abbr": abbr,
        "name": str(team.get("displayName") or team.get("shortDisplayName") or abbr),
    }


def _event_target(event: dict[str, Any], *, date_text: str, tz: str | None, team: str | None = None) -> dict[str, Any] | None:
    competition = (event.get("competitions") or [{}])[0]
    away_competitor, home_competitor = normalize_competitors(competition.get("competitors") or [])
    away = _team_from_competitor(away_competitor)
    home = _team_from_competitor(home_competitor)
    if not away["abbr"] or not home["abbr"]:
        teams = extract_teams_from_text(str(event.get("shortName") or ""))
        if len(teams) >= 2:
            away["abbr"], home["abbr"] = teams[0], teams[1]
    if not away["abbr"] or not home["abbr"]:
        return None
    requested_team = canonicalize_team_abbr(team) if team else ""
    if requested_team and requested_team not in {away["abbr"], home["abbr"]}:
        return None
    provider_dates = [(_target_date(date_text, tz) + timedelta(days=offset)).isoformat() for offset in (-1, 0, 1)]
    game_id = ""
    for provider_date in provider_dates:
        game_id = find_game_id_by_schedule(provider_date, away["abbr"], home["abbr"]) or ""
        if game_id:
            break
    if not game_id:
        for provider_date in provider_dates:
            game_id = find_game_id_by_matchup(provider_date, away["abbr"], home["abbr"]) or ""
            if game_id:
                break
    status = ((competition.get("status") or {}).get("type") or {})
    start_raw = str(competition.get("date") or event.get("date") or "")
    return {
        "gameId": game_id,
        "away": away,
        "home": home,
        "status": str(status.get("detail") or status.get("description") or status.get("state") or ""),
        "startTime": start_raw,
        "venue": str((((competition.get("venue") or {}) or {}).get("fullName")) or ""),
    }


def _targets_from_schedule(*, command: str, tz: str | None, date_text: str | None, team: str | None, opponent: str | None, scope: str) -> list[dict[str, Any]]:
    target_day = _target_date(date_text, tz)
    resolved = resolve_timezone(tz)
    events = load_candidate_events(target_day, resolved, None)
    requested_team = canonicalize_team_abbr(team) if team else ""
    requested_opponent = canonicalize_team_abbr(opponent) if opponent else ""
    targets: list[dict[str, Any]] = []
    for event in events:
        target = _event_target(event, date_text=target_day.isoformat(), tz=tz, team=requested_team or None)
        if not target:
            continue
        abbrs = {target["away"]["abbr"], target["home"]["abbr"]}
        if requested_opponent and requested_opponent not in abbrs:
            continue
        targets.append(target)
    if scope != "multi_all" and requested_team:
        return targets[:1]
    return targets


def _phase_label(summary: dict[str, Any], *, lang: str = "zh") -> str:
    phase = str(summary.get("phase") or "")
    if phase == "post":
        return "赛后复盘" if lang == "zh" else "Postgame recap"
    if phase == "pregame":
        return "赛前前瞻" if lang == "zh" else "Pregame preview"
    return "官方报道" if lang == "zh" else "Official report"


def _unique_strings(values: list[Any], *, limit: int) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
        if len(result) >= limit:
            break
    return result


def _story_is_headline_only(summary: dict[str, Any]) -> bool:
    themes = {str(theme or "") for theme in (summary.get("themes") or [])}
    return "headline_fallback" in themes or not (summary.get("bulletsZh") or summary.get("compactZh"))


def _clean_story_paragraphs(story: dict[str, Any], *, limit: int = 24) -> list[str]:
    paragraphs: list[str] = []
    for item in story.get("content") or []:
        text = re.sub(r"\s+", " ", str(item or "")).strip()
        if not text:
            continue
        paragraphs.append(text)
        if len(paragraphs) >= limit:
            break
    return paragraphs


def _build_ai_context(target: dict[str, Any], story: dict[str, Any]) -> dict[str, Any]:
    away = target.get("away") or {}
    home = target.get("home") or {}
    summary = story.get("storyFullSummary") or {}
    paragraphs = _clean_story_paragraphs(story)
    available = bool(story.get("available")) and bool(paragraphs or story.get("headline"))
    return {
        "available": available,
        "reason": "" if available else str(story.get("reason") or "missing_story_content"),
        "gameId": target.get("gameId") or story.get("gameId") or "",
        "matchup": {
            "away": away.get("abbr") or "",
            "home": home.get("abbr") or "",
            "text": f"{away.get('abbr') or ''} @ {home.get('abbr') or ''}".strip(),
        },
        "status": target.get("status") or "",
        "startTime": target.get("startTime") or "",
        "venue": target.get("venue") or "",
        "headline": story.get("headline") or summary.get("headline") or "",
        "date": story.get("date") or summary.get("date") or "",
        "byline": story.get("byline") or summary.get("byline") or "",
        "bytitle": story.get("bytitle") or summary.get("bytitle") or "",
        "storyType": story.get("storyType") or summary.get("storyType") or "",
        "paragraphCount": len(paragraphs),
        "cleanedParagraphs": paragraphs,
        "sourceLabel": story.get("sourceLabel") or summary.get("sourceLabel") or "NBA.com",
        "sourceUrl": story.get("url") or summary.get("url") or "",
    }


def _build_daily_summary(reports: list[dict[str, Any]]) -> dict[str, Any]:
    available = [report for report in reports if report.get("available")]
    unavailable = [report for report in reports if not report.get("available")]
    summaries = [report.get("storyFullSummary") or {} for report in available]
    post_count = sum(1 for summary in summaries if summary.get("phase") == "post")
    pregame_count = sum(1 for summary in summaries if summary.get("phase") == "pregame")
    headline_only = [report for report in available if _story_is_headline_only(report.get("storyFullSummary") or {})]
    substantive = [report for report in available if report not in headline_only]
    theme_counts: dict[str, int] = {}
    for summary in summaries:
        for theme in summary.get("themes") or []:
            key = str(theme or "").strip()
            if not key:
                continue
            theme_counts[key] = theme_counts.get(key, 0) + 1
    top_themes = [
        theme
        for theme, _count in sorted(theme_counts.items(), key=lambda item: (-item[1], item[0]))
        if theme != "headline_fallback"
    ][:8]
    bullets: list[str] = []
    bullets_en: list[str] = []
    if reports:
        bullets.append(
            f"今天共定位 {len(reports)} 场比赛的 NBA.com 官方报道，其中可用 {len(available)} 篇，赛后复盘 {post_count} 篇，赛前前瞻 {pregame_count} 篇。"
        )
        bullets_en.append(
            f"Located {len(reports)} NBA.com official game stories today: {len(available)} available, with {post_count} postgame recaps and {pregame_count} pregame previews."
        )
    if post_count:
        bullets.append("当前官方报道主线以赛后 Game 1 复盘为主，重点集中在赢球核心、效率差和系列赛开局语境。")
        bullets_en.append("The current story mix is recap-heavy, centered on Game 1 outcomes, star engines, efficiency gaps, and opening-series context.")
    elif pregame_count:
        bullets.append("当前官方报道主线以赛前前瞻为主，重点集中在系列赛背景、阵容可用性和关键对位。")
        bullets_en.append("The current story mix is preview-heavy, centered on series context, availability, and matchup-defining questions.")
    if theme_counts.get("series_context", 0) >= 2:
        bullets.append("多篇复盘都把比赛放在首轮系列赛开局语境中，强调 Game 1 对后续叙事和心理位置的影响。")
        bullets_en.append("Multiple stories frame the results through first-round Game 1 context and how the opener can shape the tone of the series.")
    if theme_counts.get("standout_scorer", 0) >= 2:
        bullets.append("个人得分主线很突出：多篇报道都以关键球员的高分或复出表现解释胜负。")
        bullets_en.append("Individual scoring leads stand out, with multiple stories explaining the result through star production or a major return performance.")
    if theme_counts.get("shooting_edge", 0) >= 1:
        bullets.append("至少一篇复盘明确把命中率差和防守压制写成比赛被拉开的核心原因。")
        bullets_en.append("At least one recap explicitly identifies the shooting gap and defensive control as the reason the game broke open.")
    candidate_story_bullets: list[str] = []
    for report in substantive:
        first_bullet = str(((report.get("storyFullSummary") or {}).get("bulletsZh") or [""])[0] or "")
        if first_bullet and "标题只提供" not in first_bullet:
            candidate_story_bullets.append(first_bullet)
    story_bullets = _unique_strings(candidate_story_bullets, limit=2)
    if len(bullets) < 4:
        bullets.extend(story_bullets[: 4 - len(bullets)])
    if headline_only:
        names = _unique_strings([_story_line(report, lang="zh", zh_locale=None) for report in headline_only], limit=3)
        bullets.append(f"{'、'.join(names)} 目前只有标题级或低信号报道，已在单场卡片中按信息不足处理。")
        names_en = _unique_strings([_story_line(report, lang="en", zh_locale=None) for report in headline_only], limit=3)
        bullets_en.append(f"{', '.join(names_en)} currently only have title-level or otherwise low-signal coverage, so they were treated as thin stories.")
    if unavailable:
        names = _unique_strings([_story_line(report, lang="zh", zh_locale=None) for report in unavailable], limit=3)
        bullets.append(f"{'、'.join(names)} 暂无可用 NBA.com 报道，没有生成正文摘要。")
        names_en = _unique_strings([_story_line(report, lang="en", zh_locale=None) for report in unavailable], limit=3)
        bullets_en.append(f"{', '.join(names_en)} do not currently have an available NBA.com story, so no body summary was generated.")
    bullets = _unique_strings(bullets, limit=6)
    bullets_en = _unique_strings(bullets_en, limit=6)
    return {
        "availableCount": len(available),
        "unavailableCount": len(unavailable),
        "postCount": post_count,
        "pregameCount": pregame_count,
        "headlineOnlyCount": len(headline_only),
        "compactZh": "；".join(bullet.rstrip("。") for bullet in bullets[:2]) + ("。" if bullets else ""),
        "compactEn": " ".join(bullet.rstrip(".") for bullet in bullets_en[:2]) + ("." if bullets_en else ""),
        "bulletsZh": bullets,
        "bulletsEn": bullets_en,
        "themes": top_themes,
    }


def _report_from_story(target: dict[str, Any], story: dict[str, Any]) -> dict[str, Any]:
    ai_context = _build_ai_context(target, story)
    public_story = public_game_story_payload(story)
    summary = public_story.get("storyFullSummary") or {}
    away = target.get("away") or {}
    home = target.get("home") or {}
    return {
        "gameId": target.get("gameId") or public_story.get("gameId") or "",
        "matchup": {
            "away": away.get("abbr") or "",
            "home": home.get("abbr") or "",
            "text": f"{away.get('abbr') or ''} @ {home.get('abbr') or ''}".strip(),
        },
        "status": target.get("status") or "",
        "startTime": target.get("startTime") or "",
        "venue": target.get("venue") or "",
        "available": bool(public_story.get("available")),
        "reason": public_story.get("reason") or "",
        "officialStory": public_story,
        "storyFullSummary": summary,
        "aiContext": ai_context,
    }


def build_official_report_payload(
    *,
    command: str = "",
    tz: str | None = None,
    date_text: str | None = None,
    team: str | None = None,
    opponent: str | None = None,
    lang: str = "zh",
    zh_locale: str | None = None,
    scope: str = "single",
) -> dict[str, Any]:
    detected = command_options(command, tz_hint=tz) if command else {}
    tz = tz or str(detected.get("tz") or "") or None
    date_text = date_text or (str(detected.get("date")) if detected.get("date") else None)
    team = team or (str(detected.get("team")) if detected.get("team") else None)
    opponent = opponent or (str(detected.get("opponent")) if detected.get("opponent") else None)
    lang = lang or str(detected.get("lang") or "zh")
    zh_locale = zh_locale or (str(detected.get("zh_locale")) if detected.get("zh_locale") else None)
    scope = scope or str(detected.get("scope") or "single")
    requested_date = _target_date(date_text, tz).isoformat()
    url = extract_game_url(command)
    if url:
        targets = [_target_from_url(url)]
        scope = "single"
    else:
        targets = _targets_from_schedule(command=command, tz=tz, date_text=requested_date, team=team, opponent=opponent, scope=scope)
    reports: list[dict[str, Any]] = []
    for target in targets:
        if target.get("url"):
            story = fetch_nba_game_story_url(str(target["url"]), timeout_seconds=8)
        elif target.get("gameId"):
            story = fetch_nba_game_story(str(target["gameId"]), target["away"]["abbr"], target["home"]["abbr"], timeout_seconds=8)
        else:
            story = {"available": False, "reason": "missing_game_id", "url": "", "storyFullSummary": {}}
        reports.append(_report_from_story(target, story))
    payload = {
        "intent": "official_report",
        "scope": scope,
        "requestedDate": requested_date,
        "timezone": tz or resolve_timezone(tz).name,
        "lang": lang,
        "zhLocale": zh_locale,
        "reports": reports,
    }
    if scope == "multi_all" or len(reports) > 1:
        payload["dailySummary"] = _build_daily_summary(reports)
    return payload


def _story_line(report: dict[str, Any], *, lang: str, zh_locale: str | None) -> str:
    matchup = report.get("matchup") or {}
    away = matchup.get("away") or ""
    home = matchup.get("home") or ""
    if away and home:
        return format_matchup_display(away, home, lang=lang, zh_locale=zh_locale)
    return "NBA.com game page"


def render_official_report_markdown(payload: dict[str, Any]) -> str:
    lang = str(payload.get("lang") or "zh")
    zh_locale = payload.get("zhLocale")
    reports = payload.get("reports") or []
    is_en = lang == "en"
    if len(reports) == 1 and payload.get("scope") != "multi_all":
        report = reports[0]
        summary = report.get("storyFullSummary") or {}
        story = report.get("officialStory") or {}
        lines = [
            "# NBA Official Report Summary" if is_en else "# NBA 官方报道总结",
            f"Requester timezone: {payload.get('timezone') or ''}" if is_en else f"请求方时区: {payload.get('timezone') or ''}",
            f"Requested date: {payload.get('requestedDate') or ''}" if is_en else f"请求日期: {payload.get('requestedDate') or ''}",
            f"Game: {_story_line(report, lang=lang, zh_locale=zh_locale)}" if is_en else f"比赛: {_story_line(report, lang=lang, zh_locale=zh_locale)}",
        ]
        if not report.get("available"):
            lines.append(
                f"No NBA.com story is currently available. Reason: {report.get('reason') or story.get('reason') or 'unavailable'}"
                if is_en
                else f"暂无可用 NBA.com 报道。原因: {report.get('reason') or story.get('reason') or 'unavailable'}"
            )
            if story.get("url"):
                lines.append(f"Source link: {story.get('url')}" if is_en else f"来源链接: {story.get('url')}")
            return "\n".join(lines)
        lines.extend(
            [
                "",
                "## Report Details" if is_en else "## 报道信息",
                f"- Headline: {summary.get('headline') or story.get('headline') or ''}" if is_en else f"- 官方标题: {summary.get('headline') or story.get('headline') or ''}",
                f"- Type: {_phase_label(summary, lang=lang)}" if is_en else f"- 文章类型: {_phase_label(summary, lang=lang)}",
                f"- Date: {summary.get('date') or story.get('date') or ''}" if is_en else f"- 日期: {summary.get('date') or story.get('date') or ''}",
                f"- Author: {summary.get('byline') or story.get('byline') or story.get('bytitle') or 'Unspecified'}" if is_en else f"- 作者: {summary.get('byline') or story.get('byline') or story.get('bytitle') or '未标注'}",
                f"- Paragraphs: {summary.get('paragraphCount') or 0}" if is_en else f"- 段落数: {summary.get('paragraphCount') or 0}",
                "",
                "## Story Summary" if is_en else "## 全文摘要",
            ]
        )
        bullets = (summary.get("bulletsEn") or []) if is_en else (summary.get("bulletsZh") or [])
        compact_key = "compactEn" if is_en else "compactZh"
        if not bullets and summary.get(compact_key):
            bullets = [summary[compact_key]]
        for bullet in bullets[:8]:
            lines.append(f"- {bullet}")
        themes = summary.get("themes") or []
        if themes:
            lines.extend(["", "## Themes" if is_en else "## 主题标签", (", " if is_en else "、").join(str(theme) for theme in themes[:10])])
        lines.extend(["", "## Source" if is_en else "## 来源", str(summary.get("url") or story.get("url") or "")])
        return "\n".join(lines)
    daily_summary = payload.get("dailySummary") or _build_daily_summary(reports)
    lines = [
        f"# NBA Official Report Summary ({payload.get('requestedDate') or ''})" if is_en else f"# NBA 官方报道总结 ({payload.get('requestedDate') or ''})",
        f"Requester timezone: {payload.get('timezone') or ''}" if is_en else f"请求方时区: {payload.get('timezone') or ''}",
        "",
    ]
    if not reports:
        lines.append("No NBA.com stories are currently available." if is_en else "暂无可用 NBA.com 报道。")
        return "\n".join(lines)
    lines.append("## Daily Overview" if is_en else "## 今日报道总述")
    summary_bullets = (daily_summary.get("bulletsEn") or []) if is_en else (daily_summary.get("bulletsZh") or [])
    if not summary_bullets:
        summary_bullets = ["No aggregate NBA.com story summary is currently available."] if is_en else ["暂无可聚合的 NBA.com 官方报道摘要。"]
    for bullet in summary_bullets[:6]:
        lines.append(f"- {bullet}")
    themes = daily_summary.get("themes") or []
    if themes:
        lines.append(f"- Themes: {', '.join(str(theme) for theme in themes[:8])}" if is_en else f"- 主题标签: {'、'.join(str(theme) for theme in themes[:8])}")
    lines.extend(["", "## Game-by-Game" if is_en else "## 单场报道"])
    for report in reports:
        summary = report.get("storyFullSummary") or {}
        story = report.get("officialStory") or {}
        lines.append(f"### {_story_line(report, lang=lang, zh_locale=zh_locale)}")
        if not report.get("available"):
            lines.append(
                f"No NBA.com story is currently available. Reason: {report.get('reason') or story.get('reason') or 'unavailable'}"
                if is_en
                else f"暂无可用 NBA.com 报道。原因: {report.get('reason') or story.get('reason') or 'unavailable'}"
            )
            lines.append("")
            continue
        lines.append(f"- Type: {_phase_label(summary, lang=lang)}" if is_en else f"- 类型: {_phase_label(summary, lang=lang)}")
        lines.append(f"- Headline: {summary.get('headline') or story.get('headline') or ''}" if is_en else f"- 标题: {summary.get('headline') or story.get('headline') or ''}")
        card_bullets = (summary.get("bulletsEn") or []) if is_en else (summary.get("bulletsZh") or [])
        compact_key = "compactEn" if is_en else "compactZh"
        if not card_bullets and summary.get(compact_key):
            card_bullets = [summary[compact_key]]
        for bullet in card_bullets[:3]:
            lines.append(f"- {bullet}")
        lines.append(f"- Source: {summary.get('url') or story.get('url') or ''}" if is_en else f"- 来源: {summary.get('url') or story.get('url') or ''}")
        lines.append("")
    return "\n".join(lines).rstrip()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch and summarize NBA.com official game reports.")
    parser.add_argument("--command", default="")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team")
    parser.add_argument("--opponent")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--zh-locale", choices=("cn", "hk", "tw"))
    parser.add_argument("--scope", default="single", choices=("single", "multi_all", "multi_explicit"))
    parser.add_argument("--format", default="markdown", choices=("markdown", "json"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        payload = build_official_report_payload(
            command=args.command,
            tz=args.tz,
            date_text=args.date,
            team=args.team,
            opponent=args.opponent,
            lang=args.lang,
            zh_locale=args.zh_locale,
            scope=args.scope,
        )
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_official_report_markdown(payload))
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}")
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    raise SystemExit(main())
