#!/usr/bin/env python3
"""Return a matchup-aware injury report using team-level injury data as the primary source."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from entity_guard import normalize_player_identity  # noqa: E402
from nba_common import NBAReportError  # noqa: E402
from nba_pulse_core import _reference_now, _target_date, resolve_requested_game  # noqa: E402
from nba_team_form_snapshot import build_team_form_snapshot  # noqa: E402
from nba_teams import normalize_team_input, provider_team_id  # noqa: E402
from nba_today_report import I18N, build_report_payload, format_matchup_line, validate_args  # noqa: E402
from provider_nba_injuries import STATUS_ORDER, resolve_team_injury_sources  # noqa: E402
from provider_nba import extract_team_player_averages, fetch_team_player_averages  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Return a matchup-aware NBA injury report.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team")
    parser.add_argument("--opponent")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--format", default="json", choices=("json", "markdown"))
    parser.add_argument("--base-url")
    return parser.parse_args(argv)


def _team_player_averages(team_abbr: str) -> dict[str, dict[str, float | None]]:
    team_id = provider_team_id(team_abbr, "nba")
    if not team_id:
        return {}
    try:
        payload = fetch_team_player_averages(team_id)["data"]
    except NBAReportError:
        return {}
    return extract_team_player_averages(payload)


def _attach_season_averages(
    items: list[dict[str, Any]],
    team_abbr: str,
    *,
    averages: dict[str, dict[str, float | None]] | None = None,
) -> list[dict[str, Any]]:
    if averages is None:
        averages = _team_player_averages(team_abbr)
    if not averages:
        return items
    lookup = {normalize_player_identity(name): stats for name, stats in averages.items()}
    for item in items:
        stats = lookup.get(normalize_player_identity(item.get("playerName")))
        if stats:
            item["seasonAverages"] = stats
    return items


def _group_injuries(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {status: [] for status in STATUS_ORDER}
    for item in items:
        status = item.get("status") or "Unknown"
        grouped.setdefault(status, []).append(item)
    return {status: grouped[status] for status in grouped if grouped[status]}


def _key_injured_players(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def score(item: dict[str, Any]) -> tuple[int, float]:
        status_rank = STATUS_ORDER.index(item["status"]) if item.get("status") in STATUS_ORDER else len(STATUS_ORDER)
        averages = item.get("seasonAverages") or {}
        impact = float(averages.get("PTS") or 0) + float(averages.get("REB") or 0) * 0.6 + float(averages.get("AST") or 0) * 0.7
        return (status_rank, -impact)

    return sorted(items, key=score)[:3]


def _player_impact_score(item: dict[str, Any]) -> float:
    averages = item.get("seasonAverages") or {}
    return float(averages.get("PTS") or 0) + float(averages.get("REB") or 0) * 0.6 + float(averages.get("AST") or 0) * 0.7


def _build_analysis(payload: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, list[str]]:
    team = payload.get("targetTeam") or {}
    opponent = payload.get("opponent") or {}
    snapshot = payload.get("teamSnapshot") or {}
    key_players = payload.get("keyInjuredPlayers") or []
    labels = payload.get("labels") or I18N["zh"]

    impact_lines: list[str] = []
    for item in key_players:
        name = str(item.get("playerName") or "").strip()
        status = str(item.get("status") or "").strip()
        detail = str(item.get("detail") or "").strip()
        averages = item.get("seasonAverages") or {}
        score = _player_impact_score(item)
        if not name or status not in {"Out", "Questionable", "Probable", "Day-To-Day"}:
            continue
        stats_bits: list[str] = []
        for key in ("PTS", "REB", "AST"):
            value = averages.get(key)
            if value is None:
                continue
            try:
                stats_bits.append(f"{float(value):.1f} {key}")
            except (TypeError, ValueError):
                continue
        stats_text = f"（赛季场均 {' / '.join(stats_bits)}）" if stats_bits and labels["timezone"] == "请求方时区" else (
            f" (season averages: {' / '.join(stats_bits)})" if stats_bits else ""
        )
        if labels["timezone"] == "请求方时区":
            if status == "Out":
                impact_lines.append(f"{name} 缺阵：{detail or '官方报告未提供额外原因'}{stats_text}")
            else:
                impact_lines.append(f"{name} {status}：{detail or '官方报告未提供额外原因'}{stats_text}")
        else:
            impact_lines.append(f"{name} {status}: {detail or 'No additional detail from the official report'}{stats_text}")
        if score <= 0:
            continue

    outlook_lines: list[str] = []
    record = (snapshot.get("team") or {}).get("record")
    recent = (snapshot.get("recentForm") or {}).get("record")
    rest_days = (snapshot.get("schedule") or {}).get("restDays")
    game_status = payload.get("gameStatus") or {}
    start_time = game_status.get("startTimeLocal")
    if labels["timezone"] == "请求方时区":
        if record or recent:
            outlook_lines.append(f"{team.get('abbr') or '目标球队'} 目前战绩 {record or '未知'}，最近5场 {recent or '未知'}。")
        if rest_days is not None:
            outlook_lines.append(f"赛程环境：休息 {rest_days} 天。")
        if opponent.get("abbr") and start_time:
            outlook_lines.append(f"比赛前瞻（分析）：{team.get('abbr') or ''} 将在 {start_time} 客场对阵 {opponent.get('abbr') or ''}。")
    else:
        if record or recent:
            outlook_lines.append(f"{team.get('abbr') or 'Target team'} is {record or 'unknown'} overall and {recent or 'unknown'} over the last five games.")
        if rest_days is not None:
            outlook_lines.append(f"Schedule context: {rest_days} rest day(s).")
        if opponent.get("abbr") and start_time:
            outlook_lines.append(
                f"Game outlook (analysis): {team.get('abbr') or ''} will face {opponent.get('abbr') or ''} at {start_time}."
            )

    return {"impact": impact_lines, "outlook": outlook_lines}


def _season_average_text(item: dict[str, Any], labels: dict[str, str]) -> str | None:
    averages = item.get("seasonAverages") or {}
    parts: list[str] = []
    for key in ("PTS", "REB", "AST", "STL", "BLK"):
        value = averages.get(key)
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        parts.append(f"{key} {number:.1f}")
    if not parts:
        return None
    return f"{labels['season_average']}: {', '.join(parts)}"


def _render_item(item: dict[str, Any], labels: dict[str, str]) -> str:
    bits = [str(item.get("playerName") or "")]
    if item.get("position"):
        bits.append(str(item["position"]))
    bits.append(str(item.get("status") or ""))
    if item.get("detail"):
        bits.append(str(item["detail"]))
    averages = _season_average_text(item, labels)
    text = " | ".join([bit for bit in bits if bit])
    return f"{text} ({averages})" if averages else text


def _unavailable_payload(*, tz: str | None, date_text: str | None, team_abbr: str | None, opponent_abbr: str | None, lang: str, message: str) -> dict[str, Any]:
    labels = I18N[lang]
    requested_date = date_text or _target_date(None, tz).isoformat()
    return {
        "factLayer": {
            "matchup": format_matchup_line(team_abbr, opponent_abbr),
            "primarySource": "unavailable",
            "reportDateTime": None,
        },
        "available": False,
        "requestedDate": requested_date,
        "matchup": {
            "away": team_abbr or "",
            "home": opponent_abbr or "",
            "text": format_matchup_line(team_abbr, opponent_abbr),
        },
        "targetTeam": {"abbr": team_abbr or ""},
        "opponent": {"abbr": opponent_abbr or ""},
        "gameStatus": {"state": "unavailable", "detail": message},
        "injuries": {},
        "keyInjuredPlayers": [],
        "teamSnapshot": {"available": False},
        "sources": [],
        "primarySource": "unavailable",
        "reportDateTime": None,
        "provisional": False,
        "analysis": {"impact": [], "outlook": []},
        "message": message,
        "labels": labels,
    }


def build_injury_report(
    *,
    tz: str | None,
    date_text: str | None,
    team: str | None,
    opponent: str | None,
    lang: str,
    base_url: str | None = None,
) -> dict[str, Any]:
    team_abbr = normalize_team_input(team)
    opponent_abbr = normalize_team_input(opponent)
    if not team_abbr:
        raise NBAReportError("未能识别球队缩写。", kind="invalid_arguments")
    try:
        resolved = resolve_requested_game(tz=tz, date_text=date_text, team=team_abbr, opponent=opponent_abbr, base_url=base_url)
    except NBAReportError as exc:
        if exc.kind == "not_found":
            return _unavailable_payload(
                tz=tz,
                date_text=date_text,
                team_abbr=team_abbr,
                opponent_abbr=opponent_abbr,
                lang=lang,
                message="当前条件下未找到对应比赛。",
            )
        raise

    report_args = argparse.Namespace(
        tz=tz,
        date=resolved.get("requestedDate"),
        team=team_abbr,
        view="game",
        lang=lang,
        format="json",
        base_url=base_url,
    )
    validate_args(report_args)
    report = build_report_payload(report_args)
    games = report["games"]
    if opponent_abbr:
        games = [game for game in games if opponent_abbr in {game["away"]["abbr"], game["home"]["abbr"]}]
    if not games:
        return _unavailable_payload(
            tz=tz,
            date_text=resolved.get("requestedDate"),
            team_abbr=team_abbr,
            opponent_abbr=opponent_abbr,
            lang=lang,
            message="当前条件下未找到对应比赛。",
        )
    game = games[0]
    side = "away" if game["away"]["abbr"] == team_abbr else "home"
    opponent_side = "home" if side == "away" else "away"
    reference_time = _reference_now(tz)
    with ThreadPoolExecutor(max_workers=2) as executor:
        injury_future = executor.submit(
            resolve_team_injury_sources,
            team_abbr=team_abbr,
            team_id=game[side].get("id") or provider_team_id(team_abbr, "espn"),
            team_display_name=game[side].get("displayName") or "",
            summary_lines=(game.get("injuries") or {}).get(team_abbr, []),
            start_time_utc=game.get("startTimeUtc") or "",
            away_abbr=game["away"]["abbr"],
            home_abbr=game["home"]["abbr"],
            reference_time=reference_time,
            espn_base_url=base_url,
        )
        averages_future = executor.submit(_team_player_averages, team_abbr)
        injury_resolution = injury_future.result()
        team_player_averages = averages_future.result()
    merged = _attach_season_averages(injury_resolution["items"], team_abbr, averages=team_player_averages)
    sources = list(injury_resolution["sources"])
    if any(item.get("seasonAverages") for item in merged):
        sources.append("nba_team_player_averages")
    snapshot = build_team_form_snapshot(game, side)
    grouped = _group_injuries(merged)
    payload = {
        "factLayer": {
            "matchup": format_matchup_line(game["away"]["abbr"], game["home"]["abbr"]),
            "primarySource": injury_resolution["primarySource"],
            "reportDateTime": injury_resolution["reportDateTime"],
        },
        "available": True,
        "requestedDate": report["requestedDate"],
        "matchup": {
            "away": game["away"],
            "home": game["home"],
            "text": format_matchup_line(game["away"]["abbr"], game["home"]["abbr"]),
        },
        "targetTeam": game[side],
        "opponent": game[opponent_side],
        "gameStatus": {
            "state": game.get("statusState") or "",
            "detail": game.get("displayStatusLocal") or game.get("statusDetail") or "",
            "startTimeLocal": game.get("startTimeLocal") or "",
            "eventId": game.get("eventId") or "",
        },
        "injuries": grouped,
        "keyInjuredPlayers": _key_injured_players(merged),
        "teamSnapshot": snapshot,
        "sources": sorted(set(sources)),
        "primarySource": injury_resolution["primarySource"],
        "reportDateTime": injury_resolution["reportDateTime"],
        "provisional": bool(injury_resolution["provisional"]),
        "analysis": {},
        "labels": report["labels"],
    }
    payload["analysis"] = _build_analysis(payload, merged)
    return payload


def render_markdown(payload: dict[str, Any]) -> str:
    labels = payload.get("labels") or I18N["zh"]
    team = payload.get("targetTeam") or {}
    matchup = payload.get("matchup") or {}
    game_status = payload.get("gameStatus") or {}
    title = "伤病报告" if labels["timezone"] == "请求方时区" else "Injury Report"
    lines = [f"# {team.get('abbr') or ''} {title}".strip()]
    lines.append(f"- {labels['requested_date']}: {payload.get('requestedDate') or labels['none']}")
    lines.append(f"- 对阵: {matchup.get('text') or labels['none']}" if labels["timezone"] == "请求方时区" else f"- Matchup: {matchup.get('text') or labels['none']}")
    lines.append(f"- {labels['status']}: {game_status.get('detail') or labels['none']}")
    if game_status.get("startTimeLocal"):
        lines.append(f"- {labels['start_time']}: {game_status['startTimeLocal']}")
    if payload.get("reportDateTime"):
        lines.append(
            f"- 官方报告时间: {payload['reportDateTime']}"
            if labels["timezone"] == "请求方时区"
            else f"- Official report time: {payload['reportDateTime']}"
        )
    if payload.get("provisional"):
        lines.append(
            "- 当前官方报告尚未完整提交，以下结果已降级并以 ESPN 为补充。"
            if labels["timezone"] == "请求方时区"
            else "- The official report is not yet fully submitted, so ESPN fallback data is being used provisionally."
        )
    if not payload.get("available"):
        if payload.get("message"):
            lines.append(f"- {payload['message']}")
        return "\n".join(lines)

    injuries = payload.get("injuries") or {}
    if injuries:
        lines.extend(["", "## 事实层" if labels["timezone"] == "请求方时区" else "## Fact Layer"])
        for status in STATUS_ORDER:
            items = injuries.get(status) or []
            if not items:
                continue
            lines.extend(["", f"#### {status}"])
            for item in items:
                lines.append(f"- {_render_item(item, labels)}")

    key_players = payload.get("keyInjuredPlayers") or []
    if key_players:
        lines.extend(["", "#### 关键伤员" if labels["timezone"] == "请求方时区" else "#### Key Injured Players"])
        for item in key_players:
            lines.append(f"- {_render_item(item, labels)}")

    snapshot = payload.get("teamSnapshot") or {}
    if snapshot.get("available"):
        recent = (snapshot.get("recentForm") or {}).get("record") or labels["none"]
        rest_days = (snapshot.get("schedule") or {}).get("restDays")
        lines.extend(["", "#### 球队快照（事实）" if labels["timezone"] == "请求方时区" else "#### Team Snapshot (Facts)"])
        lines.append(f"- {labels['records']}: {snapshot.get('team', {}).get('record') or labels['none']}")
        lines.append(f"- 最近5场: {recent}" if labels["timezone"] == "请求方时区" else f"- Last five: {recent}")
        if rest_days is not None:
            lines.append(f"- 休息天数: {rest_days}" if labels["timezone"] == "请求方时区" else f"- Rest days: {rest_days}")
        injury_count = (snapshot.get("injuries") or {}).get("count")
        lines.append(f"- 伤病人数: {injury_count}" if labels["timezone"] == "请求方时区" else f"- Injuries listed: {injury_count}")

    analysis = payload.get("analysis") or {}
    impact_lines = analysis.get("impact") or []
    outlook_lines = analysis.get("outlook") or []
    if impact_lines or outlook_lines:
        lines.extend(["", "## 分析层" if labels["timezone"] == "请求方时区" else "## Analysis Layer"])
        if impact_lines:
            lines.extend(["", "#### 关键影响（分析）" if labels["timezone"] == "请求方时区" else "#### Key Impact (Analysis)"])
            for line in impact_lines:
                lines.append(f"- {line}")
        if outlook_lines:
            lines.extend(["", "#### 比赛前瞻（分析）" if labels["timezone"] == "请求方时区" else "#### Game Outlook (Analysis)"])
            for line in outlook_lines:
                lines.append(f"- {line}")
    if payload.get("sources"):
        lines.extend(["", f"> sources: {', '.join(payload['sources'])}"])
        lines.append(f"> primarySource: {payload.get('primarySource') or 'unavailable'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        payload = build_injury_report(
            tz=args.tz,
            date_text=args.date,
            team=args.team,
            opponent=args.opponent,
            lang=args.lang,
            base_url=args.base_url,
        )
        if args.format == "markdown":
            print(render_markdown(payload))
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}", file=sys.stderr)
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    raise SystemExit(main())
