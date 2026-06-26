#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lark-cli API 封装模块
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from zoneinfo import ZoneInfo

from loguru import logger
from .utils import run_lark_cli_as_bot, run_lark_cli_as_user


def _iso8601_to_calendar_event_time(
    iso_str: str,
    timezone_name: str = "Asia/Shanghai",
) -> Dict[str, str]:
    """
    将 ISO 8601 时间转为飞书创建日程所需的 start_time / end_time（具体时刻）。

    飞书约定：「全天」用 date，「指定时刻」用 timestamp + timezone；
    date 与 timestamp 不能同时传，否则服务端会按全天处理并忽略 timestamp。
    因此这里只输出秒级 Unix 时间戳字符串 + IANA 时区。
    """
    s = (iso_str or "").strip()
    if not s:
        raise ValueError("时间为空")
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(timezone_name))
    # Unix 秒级时间戳（UTC 瞬时）；timezone 用于飞书侧展示/解释
    return {
        "timestamp": str(int(dt.timestamp())),
        "timezone": timezone_name,
    }


class LarkAPI:
    """lark-cli API 封装类"""

    def __init__(self):
        """初始化 LarkAPI"""
        pass

    def _fetch_room_level_children(
        self,
        parent_level_id: Optional[str],
        page_size: int,
    ) -> List[Dict[str, Any]]:
        """分页拉取某一父层级下的直接子层级（不含递归）。"""
        items: List[Dict[str, Any]] = []
        page_token: Optional[str] = None
        while True:
            params: Dict[str, Any] = {"page_size": page_size}
            if parent_level_id:
                params["room_level_id"] = parent_level_id
            if page_token:
                params["page_token"] = page_token
            result = run_lark_cli_as_bot(
                "GET",
                "vc/v1/room_levels",
                params=params,
            )
            if result.get("code") != 0:
                raise RuntimeError(
                    result.get("msg") or f"room_levels 返回 code={result.get('code')}"
                )
            data = result.get("data") or {}
            batch = data.get("items") or []
            items.extend(batch)
            if not data.get("has_more"):
                break
            page_token = data.get("page_token")
            if not page_token:
                break
        return items

    def _build_room_level_tree(
        self,
        parent_level_id: Optional[str],
        page_size: int,
        depth: int,
    ) -> List[Dict[str, Any]]:
        """从指定父层级起构建树；depth 为从当前层算起的总层数（含本层），大于 1 时才继续拉子级。"""
        raw_items = self._fetch_room_level_children(parent_level_id, page_size)
        tree: List[Dict[str, Any]] = []
        next_depth = depth - 1
        for item in raw_items:
            node = dict(item)
            node["children"] = []
            if next_depth > 0 and item.get("has_child"):
                rid = item.get("room_level_id")
                if rid:
                    node["children"] = self._build_room_level_tree(
                        rid, page_size, next_depth
                    )
            tree.append(node)
        return tree

    def query_room_levels(
        self,
        parent_level_id: Optional[str] = None,
        page_size: int = 100,
        *,
        depth: int = 1,
    ) -> Dict[str, Any]:
        """
        查询会议室层级，按树形返回（节点含 children）。

        Args:
            parent_level_id: 父层级 ID；为 None 时从根层级开始
            page_size: 分页大小
            depth: 从当前父层级向下展开几层。1 仅直接子层级（children 均为 []）；
                2 多展开一层，以此类推。需要尽量拉全树时可设较大值（如 32）。

        Returns:
            {"code": 0, "data": {"items": [ 节点..., 每层含 children ]}, "msg": ""}
        """
        if depth < 1:
            raise ValueError("depth 必须 >= 1")

        try:
            tree = self._build_room_level_tree(parent_level_id, page_size, depth)
            out = {"code": 0, "data": {"items": tree}, "msg": ""}
            logger.debug(f"查询会议室层级树成功: depth={depth}, 根节点数={len(tree)}")
            return out
        except Exception as e:
            logger.error(f"查询会议室层级失败: {e}")
            raise

    def search_rooms(
        self,
        room_level_id: str,
        page_size: int = 100,
        page_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        搜索指定层级下的会议室

        Args:
            room_level_id: 会议室层级 ID（通常是职场层级）
            page_size: 分页大小
            page_token: 分页游标

        Returns:
            会议室列表数据
        """
        params = {
            "room_level_id": room_level_id,
            "page_size": page_size
        }
        if page_token:
            params["page_token"] = page_token
        #   lark-cli api GET /open-apis/vc/v1/rooms --as bot
        try:
            result = run_lark_cli_as_bot(
                "GET",
                "vc/v1/rooms",
                params=params
            )
            logger.debug(f"搜索会议室成功: {result}")
            return result
        except Exception as e:
            logger.error(f"搜索会议室失败: {e}")
            raise

    def get_room_detail(self, room_id: str) -> Dict[str, Any]:
        """
        获取会议室详情

        Args:
            room_id: 会议室 ID

        Returns:
            会议室详细信息
        """
        try:
            result = run_lark_cli_as_bot(
                "GET",
                f"vc/v1/rooms/{room_id}"
            )
            logger.debug(f"获取会议室详情成功: {result}")
            return result
        except Exception as e:
            logger.error(f"获取会议室详情失败: {e}")
            raise

    def query_room_availability(self, room_ids: List[str],
                                start_time: str, end_time: str) -> Dict[str, Any]:
        """
        查询会议室忙闲状态

        Args:
            room_ids: 会议室 ID 列表
            start_time: 开始时间 (ISO 8601 格式)
            end_time: 结束时间 (ISO 8601 格式)

        Returns:
            会议室忙闲状态数据
        """
        data = {
            "room_ids": room_ids,
            "time_min": start_time,
            "time_max": end_time
        }

        # https://open.feishu.cn/open-apis/meeting_room/freebusy/batch_get

        try:
            result = run_lark_cli_as_bot(
                "GET",
                "meeting_room/freebusy/batch_get",
                data=data
            )
            logger.debug(f"查询会议室忙闲状态成功: {result}")
            return result
        except Exception as e:
            logger.error(f"查询会议室忙闲状态失败: {e}")
            raise

    def get_primary_calendar(self) -> Dict[str, Any]:
        """
        查询当前身份的主日历元数据。

        GET /open-apis/calendar/v4/calendars/primary
        路径中不能使用字面量 primary 创建日程时，应先调用本接口取真实 calendar_id。
        """
        try:
            result = run_lark_cli_as_user("POST", "calendar/v4/calendars/primary")
            logger.info(f"查询主日历成功：{result}")
            return result
        except Exception as e:
            logger.error(f"查询主日历失败: {e}")
            raise

    def get_primary_calendar_id(self) -> str:
        """解析 get_primary_calendar 响应，返回主日历 calendar_id（如 cal_xxx）。"""
        resp = self.get_primary_calendar()
        if resp.get("code") != 0:
            raise RuntimeError(
                resp.get("msg") or f"主日历接口返回 code={resp.get('code')}"
            )
        data = resp.get("data") or {}
        cal = data.get("calendar")
        if isinstance(cal, dict):
            cid = cal.get("calendar_id") or cal.get("id")
            if cid:
                return str(cid)
        cid = data.get("calendar_id")
        if cid:
            return str(cid)
        cals = data.get("calendars")
        if isinstance(cals, list):
            for item in cals:
                if not isinstance(item, dict):
                    continue
                # 常见结构：{ "calendar": { "calendar_id": "..." }, "user_id": "..." }
                nested = item.get("calendar")
                if isinstance(nested, dict):
                    cid = nested.get("calendar_id") or nested.get("id")
                    if cid:
                        return str(cid)
                cid = item.get("calendar_id") or item.get("id")
                if cid:
                    return str(cid)
        raise RuntimeError(f"无法从主日历响应中解析 calendar_id: {data!r}")

    def create_calendar_event(self, summary: str, start_time: str, end_time: str,
                              description: Optional[str] = None,
                              calendar_id: Optional[str] = None,
                              *,
                              need_notification: bool = False,
                              event_timezone: str = "Asia/Shanghai") -> Dict[str, Any]:
        """
        创建日程（不含会议室参会人）。

        会议室需创建成功后调用 add_calendar_event_attendees 单独添加。

        Args:
            summary: 日程主题
            start_time: 开始时间 (ISO 8601 格式)
            end_time: 结束时间 (ISO 8601 格式)
            description: 日程描述
            calendar_id: 真实日历 ID；为 None 或 \"primary\" 时自动调用 get_primary_calendar_id()
            need_notification: 是否发送通知（默认 False，与 OpenAPI 示例一致）
            event_timezone: IANA 时区名，用于 body 内 date/timezone 字段（默认 Asia/Shanghai）

        Returns:
            创建的日程信息（含 data.event.event_id、organizer_calendar_id 等）
        """
        cal_id = (calendar_id or "").strip()
        if not cal_id or cal_id.lower() == "primary":
            cal_id = self.get_primary_calendar_id()

        data: Dict[str, Any] = {
            "summary": summary,
            "description": description or "",
            "need_notification": need_notification,
            "start_time": _iso8601_to_calendar_event_time(start_time, event_timezone),
            "end_time": _iso8601_to_calendar_event_time(end_time, event_timezone),
        }

        try:
            result = run_lark_cli_as_user(
                "POST",
                f"calendar/v4/calendars/{cal_id}/events",
                data=data
            )
            logger.info(f"创建日程成功: {summary}")
            return result
        except Exception as e:
            logger.error(f"创建日程失败: {e}")
            raise

    def add_calendar_event_attendees(
        self,
        calendar_id: str,
        event_id: str,
        room_ids: List[str],
        *,
        need_notification: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        向已创建的日程添加参会人（含会议室）。

        POST /open-apis/calendar/v4/calendars/:calendar_id/events/:event_id/attendees
        须使用 user 身份调用。
        """
        if not room_ids:
            raise ValueError("room_ids 不能为空")
        cal_id = (calendar_id or "").strip()
        if not cal_id or cal_id.lower() == "primary":
            cal_id = self.get_primary_calendar_id()

        data: Dict[str, Any] = {
            "attendees": [
                {"type": "resource", "room_id": str(rid)}
                for rid in room_ids
            ],
        }
        if need_notification is not None:
            data["need_notification"] = need_notification

        try:
            result = run_lark_cli_as_user(
                "POST",
                f"calendar/v4/calendars/{cal_id}/events/{event_id}/attendees",
                data=data,
            )
            logger.info(f"日程添加参会人成功: event_id={event_id}, rooms={room_ids}")
            return result
        except Exception as e:
            logger.error(f"日程添加参会人失败: {e}")
            raise

    def list_calendar_event_attendees(
        self,
        calendar_id: str,
        event_id: str,
        page_size: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        获取日程参会人列表（分页拉全）。

        GET /open-apis/calendar/v4/calendars/:calendar_id/events/:event_id/attendees
        使用 user 身份。
        """
        cal_id = (calendar_id or "").strip()
        if not cal_id or cal_id.lower() == "primary":
            cal_id = self.get_primary_calendar_id()

        items: List[Dict[str, Any]] = []
        page_token: Optional[str] = None
        while True:
            params: Dict[str, Any] = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            try:
                result = run_lark_cli_as_user(
                    "GET",
                    f"calendar/v4/calendars/{cal_id}/events/{event_id}/attendees",
                    params=params,
                )
            except Exception as e:
                logger.error(f"获取日程参会人列表失败: {e}")
                raise
            if result.get("code") != 0:
                raise RuntimeError(
                    result.get("msg")
                    or f"参会人列表接口 code={result.get('code')}"
                )
            data = result.get("data") or {}
            batch = data.get("items") or data.get("attendees") or []
            if isinstance(batch, list):
                items.extend([x for x in batch if isinstance(x, dict)])
            if not data.get("has_more"):
                break
            page_token = data.get("page_token")
            if not page_token:
                break
        logger.debug(f"日程参会人共 {len(items)} 条")
        return items

    def get_calendar_event(
        self,
        event_id: str,
        calendar_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取单个日程详情。calendar_id 为 None 或 primary 时自动解析主日历真实 ID。"""
        cal_id = (calendar_id or "").strip()
        if not cal_id or cal_id.lower() == "primary":
            cal_id = self.get_primary_calendar_id()
        try:
            result = run_lark_cli_as_user(
                "GET",
                f"calendar/v4/calendars/{cal_id}/events/{event_id}",
            )
            logger.debug("获取日程详情成功")
            return result
        except Exception as e:
            logger.error(f"获取日程详情失败: {e}")
            raise

    def get_calendar_events(self, calendar_id: Optional[str] = None,
                           start_time: Optional[str] = None,
                           end_time: Optional[str] = None) -> Dict[str, Any]:
        """
        获取日程列表

        Args:
            calendar_id: 真实日历 ID；为 None 或 \"primary\" 时自动解析主日历
            start_time: 开始时间
            end_time: 结束时间

        Returns:
            日程列表数据
        """
        cal_id = (calendar_id or "").strip()
        if not cal_id or cal_id.lower() == "primary":
            cal_id = self.get_primary_calendar_id()

        params = {}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time

        try:
            result = run_lark_cli_as_bot(
                "GET",
                f"calendar/v4/calendars/{cal_id}/events",
                params=params
            )
            logger.debug(f"获取日程列表成功")
            return result
        except Exception as e:
            logger.error(f"获取日程列表失败: {e}")
            raise
