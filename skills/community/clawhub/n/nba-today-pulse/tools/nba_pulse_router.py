#!/usr/bin/env python3
"""Unified router for scene-specific NBA context scripts."""

from __future__ import annotations

import argparse
import json
import sys

from nba_common import NBAReportError
from nba_official_report import build_official_report_payload, render_official_report_markdown
from nba_pulse_core import (
    build_day_view,
    build_day_stats_view,
    build_game_scene,
    build_pregame_collection,
    command_has_explicit_date,
    command_options,
    infer_matchup_from_players,
    render_day_stats_markdown,
    render_day_scene,
    render_game_scene_markdown,
    render_pregame_collection_markdown,
    resolve_requested_game,
    scene_payload,
)
from nba_team_injury_report import build_injury_report, render_markdown as render_injury_markdown


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Route a natural-language NBA request to the minimal scene builder.")
    parser.add_argument("--command", default="")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team")
    parser.add_argument("--opponent")
    parser.add_argument("--lang")
    parser.add_argument("--zh-locale", choices=("cn", "hk", "tw"))
    parser.add_argument("--intent", choices=("day", "stats_day", "pregame", "live", "post", "injury", "scene", "official_report"))
    parser.add_argument("--analysis-mode", choices=("auto", "pregame", "live", "post"))
    parser.add_argument("--format", default="markdown", choices=("markdown", "json"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        detected = command_options(args.command or "", tz_hint=args.tz)
        lang = args.lang or str(detected["lang"])
        intent = args.intent or str(detected.get("intent") or "day")
        analysis_mode = args.analysis_mode or str(detected["analysis_mode"])
        detected_date = str(detected["date"]) if detected["date"] else None
        if command_has_explicit_date(args.command or "") and detected_date:
            date_text = detected_date
        else:
            date_text = args.date or detected_date
        team = args.team or (str(detected["team"]) if detected["team"] else None)
        opponent = args.opponent or (str(detected["opponent"]) if detected.get("opponent") else None)
        tz = args.tz or (str(detected["tz"]) if detected["tz"] else None)
        zh_locale = args.zh_locale or (str(detected["zh_locale"]) if detected.get("zh_locale") else None)
        scope = str(detected.get("scope") or "single")
        matchups = list(detected.get("matchups") or [])
        players = list(detected.get("players") or [])
        focus_section = detected.get("focus_section")
        followup_action = detected.get("followup_action")
        day_phase_filter = detected.get("day_phase_filter")

        if not team and players:
            inferred = infer_matchup_from_players(tz=tz, date_text=date_text, player_names=players)
            team = team or (str(inferred.get("team")) if inferred.get("team") else None)
            opponent = opponent or (str(inferred.get("opponent")) if inferred.get("opponent") else None)
            if team and intent == "day" and not day_phase_filter:
                intent = "scene"

        if intent == "official_report":
            payload = build_official_report_payload(
                command=args.command or "",
                tz=tz,
                date_text=date_text,
                team=team,
                opponent=opponent,
                lang=lang,
                zh_locale=zh_locale,
                scope=scope,
            )
            if args.format == "json":
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(render_official_report_markdown(payload))
            return 0

        if intent == "injury":
            if focus_section and team and analysis_mode in {"pregame", "live", "post"}:
                scene = build_game_scene(tz=tz, date_text=date_text, team=team, lang=lang, analysis_mode=analysis_mode, zh_locale=zh_locale)
                scene["intent"] = analysis_mode
                scene["focusSection"] = str(focus_section)
                if players:
                    scene["playerFocus"] = players[0]
                if args.format == "json":
                    print(json.dumps(scene_payload(scene), ensure_ascii=False, indent=2))
                else:
                    print(render_game_scene_markdown(scene))
                return 0
            payload = build_injury_report(tz=tz, date_text=date_text, team=team, opponent=opponent, lang=lang)
            if args.format == "json":
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(render_injury_markdown(payload))
            return 0

        if intent == "stats_day":
            payload = build_day_stats_view(tz=tz, date_text=date_text, lang=lang, zh_locale=zh_locale)
            if args.format == "json":
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(render_day_stats_markdown(payload))
            return 0

        if intent == "pregame":
            if scope == "multi_all":
                payload = build_pregame_collection(tz=tz, date_text=date_text, lang=lang, matchups=None, zh_locale=zh_locale)
                if args.format == "json":
                    print(
                        json.dumps(
                            {
                                "intent": payload["intent"],
                                "scope": payload["scope"],
                                "requestedDate": payload["requestedDate"],
                                "timezone": payload["timezone"],
                                "games": [scene_payload(scene) for scene in payload["games"]],
                            },
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                else:
                    print(render_pregame_collection_markdown(payload))
                return 0
            if scope == "multi_explicit":
                payload = build_pregame_collection(tz=tz, date_text=date_text, lang=lang, matchups=matchups, zh_locale=zh_locale)
                if args.format == "json":
                    print(
                        json.dumps(
                            {
                                "intent": payload["intent"],
                                "scope": payload["scope"],
                                "requestedDate": payload["requestedDate"],
                                "timezone": payload["timezone"],
                                "games": [scene_payload(scene) for scene in payload["games"]],
                            },
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                else:
                    print(render_pregame_collection_markdown(payload))
                return 0
            analysis_mode = "pregame"

        if intent == "live":
            analysis_mode = "live"
        elif intent == "post":
            analysis_mode = "post"

        if not team and (focus_section or followup_action):
            raise SystemExit("当前请求是单场 follow-up，但缺少可识别的球队或对局；请带上球队/对局，或在同一会话中由 skill 复用上一场比赛上下文。")

        if not team and intent == "day":
            if args.format == "json":
                print(json.dumps(build_day_view(tz=tz, date_text=date_text, lang=lang, zh_locale=zh_locale, phase_filter=day_phase_filter), ensure_ascii=False, indent=2))
            else:
                print(render_day_scene(tz=tz, date_text=date_text, lang=lang, zh_locale=zh_locale, phase_filter=day_phase_filter))
            return 0

        if not team:
            raise SystemExit("当前请求缺少可识别的球队或对局。")

        if opponent and not date_text:
            resolved = resolve_requested_game(tz=tz, date_text=date_text, team=team, opponent=opponent)
            if resolved.get("requestedDate"):
                date_text = str(resolved["requestedDate"])
        scene = build_game_scene(tz=tz, date_text=date_text, team=team, lang=lang, analysis_mode=analysis_mode, zh_locale=zh_locale)
        if intent in {"pregame", "live", "post"}:
            scene["intent"] = intent
        if focus_section:
            scene["focusSection"] = str(focus_section)
        if players:
            scene["playerFocus"] = players[0]
        if args.format == "json":
            print(json.dumps(scene_payload(scene), ensure_ascii=False, indent=2))
        else:
            print(render_game_scene_markdown(scene))
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}", file=sys.stderr)
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    raise SystemExit(main())
