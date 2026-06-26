#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
会议室预约：按配置文件中的会议室顺序查忙闲，首个空闲则创建日程并校验结果。

必填：开始时间、结束时间、会议主题（ISO 8601，须精确到秒；会议时长不超过 4 小时）。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
from typing import Any, Dict, List, Optional, Set, Tuple
from loguru import logger

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.lark_cli import LarkAPI
from scripts.meeting_room_blacklist import load_room_blacklist_json, room_is_blacklisted

# 单次忙闲查询上限（避免请求体过大）
_AVAILABILITY_BATCH = 50
_MAX_MEETING_DURATION = timedelta(hours=4)


def _validate_booking_slot(q_start: datetime, q_end: datetime) -> Optional[str]:
    """校验预约时段：整秒精度、结束晚于开始、时长不超过 4 小时。通过返回 None。"""
    if q_end <= q_start:
        return "结束时间必须晚于开始时间。"
    if q_start.microsecond != 0 or q_end.microsecond != 0:
        return "开始与结束时间须精确到秒（请勿包含毫秒或微秒）。"
    if q_end - q_start > _MAX_MEETING_DURATION:
        return "会议时长不能超过 4 小时。"
    return None


def _load_config(config_path: Path) -> Dict[str, Any]:
    if not config_path.is_file():
        raise FileNotFoundError(f"未找到配置文件: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def _rooms_from_config(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    rooms = cfg.get("rooms") or []
    out: List[Dict[str, Any]] = []
    for r in rooms:
        rid = r.get("room_id")
        name = r.get("name")
        if rid and name:
            out.append(r)
    return out


def _parse_iso_dt(s: str) -> datetime:
    if not s:
        raise ValueError("空时间字符串")
    # 飞书常见格式 2026-04-05T12:30:00+08:00
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def _intervals_overlap(
    q_start: datetime, q_end: datetime, b_start: datetime, b_end: datetime
) -> bool:
    """两段时间区间是否有交集（与飞书忙闲区间比较）。"""
    return q_start < b_end and b_start < q_end


def _merge_availability_response(
    resp: Dict[str, Any],
    merged_free_busy: Dict[str, List[Dict[str, Any]]],
    error_room_ids: Set[str],
) -> None:
    if resp.get("code") != 0:
        raise RuntimeError(resp.get("msg") or f"忙闲查询失败 code={resp.get('code')}")
    data = resp.get("data") or {}
    for rid in data.get("error_room_ids") or []:
        if rid:
            error_room_ids.add(str(rid))
    fb = data.get("free_busy")
    if isinstance(fb, dict):
        for rid, periods in fb.items():
            if not rid:
                continue
            key = str(rid)
            if not isinstance(periods, list):
                merged_free_busy[key] = []
                continue
            merged_free_busy[key] = [p for p in periods if isinstance(p, dict)]


def _room_is_available_for_slot(
    room_id: str,
    merged_free_busy: Dict[str, List[Dict[str, Any]]],
    error_room_ids: Set[str],
    q_start: datetime,
    q_end: datetime,
) -> bool:
    """
    规则（与接口实际返回一致）：
    - 在 error_room_ids 内：不可用
    - 不在 free_busy 的 key 中：视为可用
    - 在 free_busy 中且列表为空：可用
    - 在 free_busy 中且有忙段：仅当没有任何忙段与 [q_start, q_end) 重叠时可用
    """
    rid = str(room_id)
    if rid in error_room_ids:
        return False
    if rid not in merged_free_busy:
        return True
    periods = merged_free_busy[rid]
    if not periods:
        return True
    for p in periods:
        try:
            bs = _parse_iso_dt(str(p.get("start_time", "")))
            be = _parse_iso_dt(str(p.get("end_time", "")))
        except (TypeError, ValueError):
            continue
        if _intervals_overlap(q_start, q_end, bs, be):
            return False
    return True


def _first_available_room_in_order(
    ordered_rooms: List[Dict[str, Any]],
    merged_free_busy: Dict[str, List[Dict[str, Any]]],
    error_room_ids: Set[str],
    q_start: datetime,
    q_end: datetime,
) -> Optional[Dict[str, Any]]:
    for r in ordered_rooms:
        rid = str(r.get("room_id", ""))
        if not rid:
            continue
        if _room_is_available_for_slot(
            rid, merged_free_busy, error_room_ids, q_start, q_end
        ):
            return r
    return None


def _event_id_from_create(resp: Dict[str, Any]) -> Optional[str]:
    if resp.get("code") != 0:
        return None
    data = resp.get("data") or {}
    ev = data.get("event")
    if isinstance(ev, dict):
        eid = ev.get("event_id") or ev.get("id")
        if eid:
            return str(eid)
    eid = data.get("event_id")
    if eid:
        return str(eid)
    return None


def _organizer_calendar_id_from_create(resp: Dict[str, Any]) -> Optional[str]:
    """创建日程响应里的组织者日历 ID，后续添加参会人、拉取详情时优先使用。"""
    if resp.get("code") != 0:
        return None
    ev = (resp.get("data") or {}).get("event")
    if not isinstance(ev, dict):
        return None
    cid = ev.get("organizer_calendar_id")
    return str(cid) if cid else None


def _room_in_attendee_records(
    records: List[Dict[str, Any]],
    room_id: str,
) -> bool:
    """判断参会人列表中是否包含指定会议室（兼容多种返回结构）。"""
    rid = str(room_id)
    for raw in records:
        if not isinstance(raw, dict):
            continue
        if str(raw.get("room_id")) == rid:
            return True
        if raw.get("type") == "room" and str(raw.get("room_id")) == rid:
            return True
        for key in ("attendee", "user", "room"):
            nested = raw.get(key)
            if isinstance(nested, dict) and str(nested.get("room_id")) == rid:
                return True
    return False


def book_meeting(
    start_time: str,
    end_time: str,
    summary: str,
    *,
    config_path: Path,
    description: Optional[str] = None,
    calendar_id: str = "primary",
) -> Tuple[bool, str]:
    """
    Returns:
        (success, message_for_user)
    """
    cfg = _load_config(config_path)
    raw_rooms = _rooms_from_config(cfg)
    if not raw_rooms:
        return False, "配置文件中没有任何有效会议室（需包含 room_id 与 name），请先运行初始化。"

    blacklist_path = config_path.parent / "meeting_room_blacklist.json"
    try:
        blacklist_rules = load_room_blacklist_json(blacklist_path)
    except ValueError as e:
        return False, str(e)

    ordered = [r for r in raw_rooms if not room_is_blacklisted(r, blacklist_rules)]
    if not ordered:
        return (
            False,
            "当前黑名单已过滤掉全部会议室；请编辑与 meeting.json 同目录下的 "
            "meeting_room_blacklist.json 后重试（或重新运行初始化以刷新 rooms）。",
        )

    try:
        q_start = _parse_iso_dt(start_time)
        q_end = _parse_iso_dt(end_time)
    except (TypeError, ValueError) as e:
        return False, f"开始/结束时间无法解析为 ISO 8601：{e}"

    slot_err = _validate_booking_slot(q_start, q_end)
    if slot_err:
        return False, slot_err

    api = LarkAPI()
    cal_raw = (calendar_id or "").strip()
    if not cal_raw or cal_raw.lower() == "primary":
        try:
            resolved_calendar_id = api.get_primary_calendar_id()
        except Exception as e:
            return False, f"获取主日历 ID 失败（GET calendar/v4/calendars/primary）：{e}"
    else:
        resolved_calendar_id = cal_raw

    all_ids = [str(r["room_id"]) for r in ordered]
    merged_free_busy: Dict[str, List[Dict[str, Any]]] = {}
    error_room_ids: Set[str] = set()

    for i in range(0, len(all_ids), _AVAILABILITY_BATCH):
        batch = all_ids[i : i + _AVAILABILITY_BATCH]
        resp = api.query_room_availability(
            batch,
            start_time=start_time,
            end_time=end_time,
        )
        _merge_availability_response(resp, merged_free_busy, error_room_ids)

    chosen = _first_available_room_in_order(
        ordered, merged_free_busy, error_room_ids, q_start, q_end
    )
    if not chosen:
        return (
            False,
            "该时间段内没有可用会议室。可尝试调整开始/结束时间或缩短时长后重试。",
        )

    logger.info(f"选择会议室: {chosen}")

    room_id = str(chosen["room_id"])
    room_name = str(chosen.get("name", ""))
    floor_name = str(chosen.get("floor_name", "") or "")

    create_resp = api.create_calendar_event(
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        description=description,
        calendar_id=resolved_calendar_id,
    )

    if create_resp.get("code") != 0:
        return False, f"创建日程失败：{create_resp.get('msg', create_resp)}"

    event_id = _event_id_from_create(create_resp)
    event_calendar_id = (
        _organizer_calendar_id_from_create(create_resp) or resolved_calendar_id
    )

    if not event_id:
        return (
            True,
            f"日程已创建，但响应中未解析到 event_id，请自行在日历中确认。\n"
            f"会议室：{room_name}"
            + (f"（{floor_name}）" if floor_name else "")
            + f"\nroom_id：{room_id}",
        )

    try:
        add_resp = api.add_calendar_event_attendees(
            event_calendar_id,
            event_id,
            [room_id],
        )
    except Exception as e:
        return (
            False,
            f"日程已创建（event_id={event_id}），但添加会议室失败：{e}\n"
            f"会议室：{room_name}（{room_id}）",
        )

    if add_resp.get("code") != 0:
        return (
            False,
            f"日程已创建（event_id={event_id}），但添加会议室接口返回失败："
            f"{add_resp.get('msg', add_resp)}",
        )

    # 用「参会人列表」接口确认会议室是否已挂上（可能略有延迟，短重试）
    list_err: Optional[str] = None
    ok_room = False
    for attempt in range(4):
        if attempt:
            sleep(1)
        try:
            attendees = api.list_calendar_event_attendees(
                event_calendar_id, event_id
            )
            logger.info(f"参会人列表拉取成功（第 {attempt + 1} 次），共 {len(attendees)} 人")
            if _room_in_attendee_records(attendees, room_id):
                ok_room = True
                break
        except Exception as e:
            list_err = str(e)
            logger.warning(f"拉取参会人列表失败：{e}")

    if ok_room:
        return (
            True,
            f"预约成功。\n"
            f"会议主题：{summary}\n"
            f"时间：{start_time} ~ {end_time}\n"
            f"会议室：{room_name}"
            + (f"（{floor_name}）" if floor_name else "")
            + f"\n日程 event_id：{event_id}",
        )
    if list_err:
        return (
            False,
            f"日程已创建且已请求添加会议室（event_id={event_id}），但拉取参会人列表失败：{list_err}\n"
            f"请到日历中核对会议室：{room_name}（{room_id}）",
        )
    return (
        False,
        f"日程已创建（event_id={event_id}），参会人列表中未找到该会议室，可能仍在同步。\n"
        f"会议室：{room_name}（{room_id}）",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="按配置预约会议室（查忙闲 → 创建日程 → 校验）")
    parser.add_argument(
        "--start-time",
        required=True,
        help="开始时间 ISO 8601（精确到秒，勿带毫秒），如 2026-04-05T15:00:00+08:00",
    )
    parser.add_argument(
        "--end-time",
        required=True,
        help="结束时间 ISO 8601（精确到秒）；与开始时间间隔须 ≤ 4 小时",
    )
    parser.add_argument("--summary", required=True, help="会议主题")
    parser.add_argument("--description", default=None, help="日程描述（可选）")
    parser.add_argument(
        "--config",
        type=Path,
        default=_ROOT / "conf" / "meeting.json",
        help="会议室配置文件路径",
    )
    parser.add_argument(
        "--calendar-id",
        default="primary",
        help="日历 ID；填 primary 或未指定时通过 GET calendar/v4/calendars/primary 解析真实 ID",
    )
    args = parser.parse_args()

    try:
        ok, msg = book_meeting(
            args.start_time,
            args.end_time,
            args.summary,
            config_path=args.config.resolve(),
            description=args.description,
            calendar_id=args.calendar_id,
        )
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"预约流程异常：{e}", file=sys.stderr)
        sys.exit(1)

    print(msg)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
