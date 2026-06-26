#!/usr/bin/env python3
"""Official NBA injury-report provider and source-aware team injury merge."""

from __future__ import annotations

import os
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo
from typing import Any

try:
    from .nba_common import NBAReportError
    from .provider_espn import fetch_team_injuries
    from .vendor_pdf_text import extract_text_blocks
except ImportError:  # pragma: no cover - script execution path
    from nba_common import NBAReportError
    from provider_espn import fetch_team_injuries
    from vendor_pdf_text import extract_text_blocks

DEFAULT_REPORT_BASE_URL = "https://ak-static.cms.nba.com/referee/injury"
DEFAULT_LISTING_URL = "https://www.nba.com/referee/injury-report"
USER_AGENT = "nba-tr-openclaw/2.0"
STATUS_ORDER = ("Out", "Doubtful", "Questionable", "Day-To-Day", "Probable")
COLUMN_DATE_MAX = 100
COLUMN_TIME_MAX = 195
COLUMN_MATCHUP_MAX = 260
COLUMN_TEAM_MAX = 420
COLUMN_PLAYER_MAX = 580
COLUMN_STATUS_MAX = 666
REPORT_TIME_PATTERN = re.compile(r"Injury Report:\s*(\d{2}/\d{2}/\d{2})\s+(\d{2}:\d{2})\s+(AM|PM)", re.IGNORECASE)
TEAM_NOT_SUBMITTED_PATTERN = re.compile(r"^(?P<team>.+?)\s+NOT YET SUBMITTED$", re.IGNORECASE)


def resolve_report_base_url(base_url: str | None = None) -> str:
    return (base_url or os.environ.get("NBA_TR_NBA_INJURY_BASE_URL") or DEFAULT_REPORT_BASE_URL).rstrip("/")


def resolve_listing_url(listing_url: str | None = None) -> str:
    return (listing_url or os.environ.get("NBA_TR_NBA_INJURY_LISTING_URL") or DEFAULT_LISTING_URL).rstrip("/")


def canonical_status(value: str | None) -> str:
    lowered = str(value or "").strip().lower()
    if "day" in lowered:
        return "Day-To-Day"
    if "question" in lowered:
        return "Questionable"
    if "doubt" in lowered:
        return "Doubtful"
    if "prob" in lowered:
        return "Probable"
    if "out" in lowered or "缺阵" in lowered:
        return "Out"
    return str(value or "Unknown").strip() or "Unknown"


def normalize_official_player_name(value: str | None) -> str:
    text = re.sub(r"\s+", " ", str(value or "").strip())
    if "," not in text:
        return text
    last_name, first_name = [part.strip() for part in text.split(",", 1)]
    if not last_name or not first_name:
        return text
    return f"{first_name} {last_name}".strip()


def _request(url: str, *, method: str = "GET") -> urllib.request.addinfourl:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        method=method,
    )
    return urllib.request.urlopen(request, timeout=20)


def _head_exists(url: str) -> bool:
    try:
        with _request(url, method="HEAD") as response:
            return response.status == 200
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        return False


def _fetch_bytes(url: str) -> bytes:
    try:
        with _request(url, method="GET") as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise NBAReportError(f"官方 NBA injury report 请求失败: HTTP {exc.code}", kind="nba_http_error") from exc
    except (urllib.error.URLError, socket.timeout, TimeoutError, ssl.SSLError) as exc:
        raise NBAReportError(f"无法连接官方 NBA injury report 数据源: {exc}", kind="nba_connection_failed") from exc


def _parse_listing_candidates(listing_url: str) -> list[tuple[datetime, str]]:
    try:
        html = _fetch_bytes(listing_url).decode("utf-8", errors="replace")
    except NBAReportError:
        return []
    pattern = re.compile(r"/referee/injury/(Injury-Report_(\d{4}-\d{2}-\d{2})_(\d{2})_(\d{2})(AM|PM)\.pdf)")
    candidates: list[tuple[datetime, str]] = []
    et = ZoneInfo("America/New_York")
    for filename, date_text, hour_text, minute_text, meridiem in pattern.findall(html):
        hour = int(hour_text)
        minute = int(minute_text)
        if meridiem.upper() == "PM" and hour != 12:
            hour += 12
        if meridiem.upper() == "AM" and hour == 12:
            hour = 0
        published_at = datetime.strptime(date_text, "%Y-%m-%d").replace(tzinfo=et) + timedelta(hours=hour, minutes=minute)
        url = urllib.parse.urljoin(listing_url + "/", f"../referee/injury/{filename}")
        candidates.append((published_at, url))
    return candidates


def _candidate_urls(reference_time_et: datetime, *, base_url: str, lookback_hours: int = 36) -> list[tuple[datetime, str]]:
    rounded = reference_time_et.replace(minute=(reference_time_et.minute // 15) * 15, second=0, microsecond=0)
    candidates: list[tuple[datetime, str]] = []
    for step in range(0, lookback_hours * 4 + 1):
        current = rounded - timedelta(minutes=step * 15)
        hour = current.strftime("%I")
        minute = current.strftime("%M")
        meridiem = current.strftime("%p")
        filename = f"Injury-Report_{current.strftime('%Y-%m-%d')}_{hour}_{minute}{meridiem}.pdf"
        candidates.append((current, f"{base_url}/{filename}"))
    return candidates


def discover_latest_report(reference_time: datetime, *, base_url: str | None = None, listing_url: str | None = None) -> dict[str, Any]:
    report_base_url = resolve_report_base_url(base_url)
    report_listing_url = resolve_listing_url(listing_url)
    et = ZoneInfo("America/New_York")
    reference_time_et = reference_time.astimezone(et)

    candidates = [item for item in _parse_listing_candidates(report_listing_url) if item[0] <= reference_time_et]
    candidates.sort(key=lambda item: item[0], reverse=True)
    for published_at, url in candidates:
        if _head_exists(url):
            return {"reportDateTime": published_at, "url": url, "source": "official_nba_injury_report"}

    for published_at, url in _candidate_urls(reference_time_et, base_url=report_base_url):
        if _head_exists(url):
            return {"reportDateTime": published_at, "url": url, "source": "official_nba_injury_report"}

    raise NBAReportError("当前未找到可用的官方 NBA injury report。", kind="not_found")


def _group_rows(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for block in blocks:
        existing = next(
            (
                row
                for row in rows
                if row["page"] == block["page"] and abs(float(row["y"]) - float(block["y"])) <= 1.1
            ),
            None,
        )
        if existing is None:
            existing = {"page": block["page"], "y": block["y"], "cells": []}
            rows.append(existing)
        existing["cells"].append({"x": block["x"], "text": block["text"]})
    for row in rows:
        row["cells"].sort(key=lambda item: float(item["x"]))
    rows.sort(key=lambda item: (item["page"], item["y"]))
    return rows


def _row_to_columns(row: dict[str, Any]) -> dict[str, str]:
    columns = {
        "date": "",
        "time": "",
        "matchup": "",
        "team": "",
        "playerName": "",
        "status": "",
        "reason": "",
    }
    for cell in row["cells"]:
        x = float(cell["x"])
        text = str(cell["text"]).strip()
        if not text:
            continue
        if x < COLUMN_DATE_MAX:
            columns["date"] = text
        elif x < COLUMN_TIME_MAX:
            columns["time"] = text
        elif x < COLUMN_MATCHUP_MAX:
            columns["matchup"] = text
        elif x < COLUMN_TEAM_MAX:
            columns["team"] = text
        elif x < COLUMN_PLAYER_MAX:
            columns["playerName"] = text
        elif x < COLUMN_STATUS_MAX:
            columns["status"] = text
        else:
            columns["reason"] = text
    return columns


def _parse_report_datetime(rows: list[dict[str, Any]]) -> datetime | None:
    et = ZoneInfo("America/New_York")
    for row in rows:
        text = " ".join(cell["text"] for cell in row["cells"])
        match = REPORT_TIME_PATTERN.search(text)
        if not match:
            continue
        date_text, clock_text, meridiem = match.groups()
        return datetime.strptime(f"{date_text} {clock_text} {meridiem}", "%m/%d/%y %I:%M %p").replace(tzinfo=et)
    return None


def _append_reason(existing: str | None, addition: str | None) -> str:
    return " ".join(part for part in (str(existing or "").strip(), str(addition or "").strip()) if part).strip()


def parse_official_report(pdf_bytes: bytes, *, source_url: str) -> dict[str, Any]:
    rows = _group_rows(extract_text_blocks(pdf_bytes))
    report_datetime = _parse_report_datetime(rows)
    entries: list[dict[str, Any]] = []
    team_statuses: list[dict[str, Any]] = []
    current_date = ""
    current_time = ""
    current_matchup = ""
    current_team = ""
    previous_entry: dict[str, Any] | None = None
    pending_reason = ""

    for row in rows:
        columns = _row_to_columns(row)
        full_text = " ".join(cell["text"] for cell in row["cells"]).strip()
        if not full_text or full_text.startswith("Page "):
            continue
        if "Game Date" in full_text and "Player Name" in full_text:
            continue
        if full_text.startswith("Injury Report:"):
            continue

        if columns["date"]:
            current_date = columns["date"]
        if columns["time"]:
            current_time = columns["time"]
        if columns["matchup"]:
            current_matchup = columns["matchup"]
        if columns["team"]:
            current_team = columns["team"]

        if (
            pending_reason
            and previous_entry
            and not columns["playerName"]
            and not columns["status"]
            and (columns["date"] or columns["time"] or columns["matchup"] or columns["team"])
        ):
            previous_entry["reason"] = _append_reason(previous_entry.get("reason"), pending_reason)
            pending_reason = ""

        not_submitted = TEAM_NOT_SUBMITTED_PATTERN.match(columns["team"] or "") or TEAM_NOT_SUBMITTED_PATTERN.match(full_text)
        if not_submitted:
            if pending_reason and previous_entry:
                previous_entry["reason"] = _append_reason(previous_entry.get("reason"), pending_reason)
                pending_reason = ""
            team_statuses.append(
                {
                    "gameDate": current_date,
                    "gameTime": current_time,
                    "matchup": current_matchup,
                    "team": not_submitted.group("team"),
                    "status": "NOT YET SUBMITTED",
                    "source": "official_nba_injury_report",
                }
            )
            previous_entry = None
            continue

        if columns["playerName"] and columns["status"]:
            status = canonical_status(columns["status"])
            inline_reason = str(columns["reason"] or "").strip()
            reason = inline_reason
            if pending_reason:
                context_changed = bool(
                    previous_entry
                    and (
                        previous_entry.get("gameDate") != current_date
                        or previous_entry.get("gameTime") != current_time
                        or previous_entry.get("matchup") != current_matchup
                        or previous_entry.get("team") != current_team
                    )
                )
                if inline_reason and previous_entry:
                    previous_entry["reason"] = _append_reason(previous_entry.get("reason"), pending_reason)
                elif context_changed and previous_entry and not previous_entry.get("reason"):
                    previous_entry["reason"] = _append_reason(previous_entry.get("reason"), pending_reason)
                else:
                    reason = _append_reason(pending_reason, inline_reason)
                pending_reason = ""
            entry = {
                "gameDate": current_date,
                "gameTime": current_time,
                "matchup": current_matchup,
                "team": current_team,
                "playerName": columns["playerName"],
                "status": status,
                "reason": reason,
                "source": "official_nba_injury_report",
                "sourceUrl": source_url,
            }
            entries.append(entry)
            previous_entry = entry
            continue

        if columns["reason"] and not columns["playerName"] and not columns["status"]:
            pending_reason = _append_reason(pending_reason, columns["reason"])

    if pending_reason and previous_entry:
        previous_entry["reason"] = _append_reason(previous_entry.get("reason"), pending_reason)

    return {
        "reportDateTime": report_datetime.isoformat() if report_datetime else None,
        "entries": entries,
        "teamStatuses": team_statuses,
        "sourceUrl": source_url,
        "source": "official_nba_injury_report",
    }


def fetch_official_report(reference_time: datetime, *, base_url: str | None = None, listing_url: str | None = None) -> dict[str, Any]:
    discovered = discover_latest_report(reference_time, base_url=base_url, listing_url=listing_url)
    parsed = parse_official_report(_fetch_bytes(discovered["url"]), source_url=discovered["url"])
    parsed["reportDateTime"] = parsed.get("reportDateTime") or discovered["reportDateTime"].isoformat()
    return parsed


def _official_game_date(start_time_utc: str) -> date:
    parsed = datetime.fromisoformat(str(start_time_utc).replace("Z", "+00:00"))
    return parsed.astimezone(ZoneInfo("America/New_York")).date()


def _summary_injury_items(summary_lines: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for line in summary_lines:
        parts = [part.strip() for part in str(line).split(" - ") if part.strip()]
        if not parts:
            continue
        status = canonical_status(parts[1] if len(parts) > 1 else "")
        if status not in STATUS_ORDER:
            continue
        items.append(
            {
                "playerName": parts[0],
                "position": "",
                "status": status,
                "detail": parts[2] if len(parts) > 2 else "",
                "primarySource": "espn_summary",
                "sources": ["espn_summary"],
            }
        )
    return items


def _espn_team_injury_items(team_id: str | None, *, base_url: str | None = None) -> list[dict[str, Any]]:
    if not team_id:
        return []
    try:
        payload = fetch_team_injuries(team_id, base_url=base_url)["data"]
    except NBAReportError:
        return []
    containers: list[Any] = []
    for key in ("injuries", "items", "athletes", "entries"):
        value = payload.get(key)
        if isinstance(value, list):
            containers.extend(value)
    items: list[dict[str, Any]] = []
    for entry in containers:
        if not isinstance(entry, dict):
            continue
        athlete = entry.get("athlete") or entry.get("player") or {}
        name = athlete.get("displayName") or athlete.get("fullName") or athlete.get("shortName") or entry.get("displayName")
        if not name:
            continue
        status = entry.get("status") or entry.get("type") or {}
        status_text = status.get("description") if isinstance(status, dict) else status
        canonical = canonical_status(status_text)
        if canonical not in STATUS_ORDER:
            continue
        items.append(
            {
                "playerName": str(name),
                "position": str(((athlete.get("position") or {}).get("abbreviation")) or entry.get("position") or ""),
                "status": canonical,
                "detail": str(entry.get("detail") or entry.get("description") or entry.get("shortComment") or ""),
                "primarySource": "espn_team_injuries",
                "sources": ["espn_team_injuries"],
            }
        )
    return items


def resolve_team_injury_sources(
    *,
    team_abbr: str,
    team_id: str | None,
    team_display_name: str,
    summary_lines: list[str],
    start_time_utc: str,
    away_abbr: str,
    home_abbr: str,
    reference_time: datetime,
    espn_base_url: str | None = None,
    official_base_url: str | None = None,
    official_listing_url: str | None = None,
) -> dict[str, Any]:
    normalized_team_name = team_display_name.strip()
    official_items: list[dict[str, Any]] = []
    official_team_status = None
    report_datetime = None
    sources: list[str] = []
    matchup_key = f"{away_abbr}@{home_abbr}"
    official_date = _official_game_date(start_time_utc).strftime("%m/%d/%Y")

    try:
        report = fetch_official_report(reference_time, base_url=official_base_url, listing_url=official_listing_url)
        report_datetime = report.get("reportDateTime")
        report_entries = report.get("entries") or []
        report_statuses = report.get("teamStatuses") or []
        official_items = [
            {
                "playerName": normalize_official_player_name(entry["playerName"]),
                "position": "",
                "status": entry["status"],
                "detail": entry.get("reason") or "",
                "primarySource": "official_nba_injury_report",
                "sources": ["official_nba_injury_report"],
            }
            for entry in report_entries
            if entry.get("matchup") == matchup_key
            and entry.get("gameDate") == official_date
            and str(entry.get("team") or "").strip() == normalized_team_name
            and entry.get("status") in STATUS_ORDER
        ]
        official_team_status = next(
            (
                status
                for status in report_statuses
                if status.get("matchup") == matchup_key
                and status.get("gameDate") == official_date
                and str(status.get("team") or "").strip() == normalized_team_name
            ),
            None,
        )
        if official_items or official_team_status:
            sources.append("official_nba_injury_report")
    except NBAReportError:
        report_datetime = None

    espn_items = _espn_team_injury_items(team_id, base_url=espn_base_url)
    if espn_items:
        sources.append("espn_team_injuries")
    summary_items = _summary_injury_items(summary_lines)
    if summary_items:
        sources.append("espn_summary")

    merged: dict[str, dict[str, Any]] = {}
    for item in official_items + espn_items + summary_items:
        key = str(item.get("playerName") or "").casefold().strip()
        if not key:
            continue
        existing = merged.get(key)
        if existing is None:
            merged[key] = dict(item)
            continue
        if existing.get("primarySource") != "official_nba_injury_report" and item.get("primarySource") == "official_nba_injury_report":
            merged[key] = dict(item)
            existing = merged[key]
        else:
            if not existing.get("detail") and item.get("detail"):
                existing["detail"] = item["detail"]
            if not existing.get("position") and item.get("position"):
                existing["position"] = item["position"]
            existing["sources"] = sorted(set((existing.get("sources") or []) + (item.get("sources") or [])))

    items = sorted(
        merged.values(),
        key=lambda item: (STATUS_ORDER.index(item["status"]) if item.get("status") in STATUS_ORDER else len(STATUS_ORDER), item["playerName"]),
    )
    return {
        "items": items,
        "provisional": bool(official_team_status and official_team_status.get("status") == "NOT YET SUBMITTED"),
        "reportDateTime": report_datetime,
        "sources": sorted(set(sources)),
        "primarySource": (
            "official_nba_injury_report"
            if official_items
            else ("espn_team_injuries" if espn_items else ("espn_summary" if summary_items else "unavailable"))
        ),
    }
