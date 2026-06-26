#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
会议室黑名单：从 JSON 读取规则，供初始化拉列表与预约脚本过滤共用。

配置文件默认与 meeting.json 同目录：`meeting_room_blacklist.json`。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

DEFAULT_NAME_SUBSTRINGS = ["面试间"]
DEFAULT_EXCLUDE_IF_CAPACITY_GT = 30


@dataclass(frozen=True)
class RoomBlacklistRules:
    """name_substrings：名称包含任一则排除；room_ids：显式排除；capacity 仅在接口返回 capacity 时生效。"""

    name_substrings: List[str]
    exclude_if_capacity_gt: Optional[int]
    room_ids: Set[str]

    @staticmethod
    def builtin_defaults() -> RoomBlacklistRules:
        return RoomBlacklistRules(
            name_substrings=list(DEFAULT_NAME_SUBSTRINGS),
            exclude_if_capacity_gt=DEFAULT_EXCLUDE_IF_CAPACITY_GT,
            room_ids=set(),
        )


def load_room_blacklist_json(path: Path) -> RoomBlacklistRules:
    if not path.is_file():
        return RoomBlacklistRules.builtin_defaults()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"会议室黑名单 JSON 无效 ({path}): {e}") from e
    if not isinstance(raw, dict):
        raise ValueError(f"会议室黑名单须为 JSON 对象: {path}")

    if "name_substrings" in raw:
        ns = raw["name_substrings"]
        if ns is None:
            name_substrings: List[str] = []
        elif isinstance(ns, list):
            name_substrings = [str(x) for x in ns if str(x).strip()]
        else:
            raise ValueError("name_substrings 须为字符串数组或 null")
    else:
        name_substrings = list(DEFAULT_NAME_SUBSTRINGS)

    if "exclude_if_capacity_gt" in raw:
        cap_raw = raw["exclude_if_capacity_gt"]
        if cap_raw is None:
            exclude_cap: Optional[int] = None
        else:
            exclude_cap = int(cap_raw)
    else:
        exclude_cap = DEFAULT_EXCLUDE_IF_CAPACITY_GT

    room_ids_raw = raw.get("room_ids")
    if room_ids_raw is None:
        room_ids_raw = []
    if not isinstance(room_ids_raw, list):
        raise ValueError("room_ids 须为字符串数组")
    room_ids = {str(x).strip() for x in room_ids_raw if str(x).strip()}

    return RoomBlacklistRules(
        name_substrings=name_substrings,
        exclude_if_capacity_gt=exclude_cap,
        room_ids=room_ids,
    )


def room_is_blacklisted(room: Dict[str, Any], rules: RoomBlacklistRules) -> bool:
    rid = str(room.get("room_id") or room.get("id") or "").strip()
    if rid and rid in rules.room_ids:
        return True
    name = str(room.get("name") or "")
    for sub in rules.name_substrings:
        if sub and sub in name:
            return True
    if rules.exclude_if_capacity_gt is not None:
        cap = room.get("capacity")
        try:
            if cap is not None and int(cap) > rules.exclude_if_capacity_gt:
                return True
        except (TypeError, ValueError):
            pass
    return False
