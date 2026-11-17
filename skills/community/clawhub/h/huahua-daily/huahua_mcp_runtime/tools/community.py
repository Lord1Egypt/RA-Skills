"""community MCP tool implementations."""

import asyncio  # noqa: F401
import json  # noqa: F401
import math
import os  # noqa: F401
import re  # noqa: F401
import time  # noqa: F401
from typing import Optional  # noqa: F401

from .binding import bind_runtime

_RUNTIME_DEPENDENCIES = ("_delete", "_get", "_post", "_require_token", "_validate_fund_code")

if False:  # pragma: no cover - populated by bind() before tool registration
    _delete = None
    _get = None
    _post = None
    _require_token = None
    _validate_fund_code = None


def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)


def _validate_uid(value, field_name: str = "UID") -> str:
    normalized = str(value or "").strip()
    if not re.fullmatch(r"\d{8}", normalized):
        raise ValueError(f"{field_name} 必须是 8 位数字")
    return normalized


async def get_danmaku(code: str) -> list:
    """
    获取某只基金今日弹幕/社区短消息。

    Args:
        code: 6 位基金代码。
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    data = await _get(f"/api/danmaku/{validated_code}")
    return data if isinstance(data, list) else []


async def send_danmaku(fund_code: str, text: str) -> dict:
    """
    发送某只基金的社区短消息。只有用户明确要求发言时才调用。
    弹幕颜色由 App 根据基金涨跌情况自动设置，无需手动指定。

    Args:
        fund_code: 6 位基金代码。
        text: 1-30 字。
    """
    _require_token()
    validated_code = _validate_fund_code(fund_code)
    normalized_text = str(text or "").strip()
    if not normalized_text:
        raise ValueError("弹幕内容不能为空")
    if len(normalized_text) > 30:
        raise ValueError(f"弹幕内容过长：{len(normalized_text)} 字，最多 30 字")
    return await _post("/api/danmaku/send", {
        "fund_code": validated_code,
        "text": normalized_text,
    })


async def get_notices(since: float = 0) -> list:
    """
    获取系统公告。

    Args:
        since: Unix 秒时间戳，只返回该时间之后的公告；默认返回最近公告。
    """
    data = await _get("/api/notices", params={"since": since})
    return data if isinstance(data, list) else []


async def get_community_ranking(tab: str = "weekly", page: int = 1, page_size: int = 50) -> dict:
    """
    获取喵舍收益率排行榜。

    Args:
        tab: 排行榜类型，可选 "weekly"（周收益）、"monthly"（月收益）、"total"（总收益）
        page: 页码，从 1 开始
        page_size: 每页条数，1-100，默认 50
    """
    _require_token()
    if tab not in ("weekly", "monthly", "total"):
        raise ValueError("tab 仅支持 weekly、monthly 或 total")
    return await _get("/api/community/ranking", params={
        "tab": tab,
        "page": max(1, page),
        "page_size": min(100, max(1, page_size)),
    })


async def get_community_my_rank() -> dict:
    """
    获取当前用户在各排行榜的排名。
    适合回答"我排第几"类问题。
    """
    _require_token()
    return await _get("/api/community/my-rank")


async def get_community_user(uid: str) -> dict:
    """
    获取喵舍用户详情，包含收益率和十大重仓（前5）。
    适合查看其他用户的投资组合。

    Args:
        uid: 用户的 8 位 UID
    """
    _require_token()
    normalized = _validate_uid(uid)
    return await _get(f"/api/community/user/{normalized}")


async def get_community_stats() -> dict:
    """
    获取当前用户的关注数和粉丝数。
    """
    _require_token()
    return await _get("/api/community/stats")


async def get_community_following() -> list:
    """
    获取当前用户的关注列表。
    """
    _require_token()
    data = await _get("/api/community/following")
    if isinstance(data, dict) and isinstance(data.get("following"), list):
        return data["following"]
    return data if isinstance(data, list) else []


async def search_community_users(query: str) -> list:
    """
    搜索喵舍用户，支持 UID 精确匹配和昵称模糊匹配。

    Args:
        query: 搜索关键词（UID 或昵称）
    """
    _require_token()
    normalized = str(query or "").strip()
    if not normalized:
        raise ValueError("搜索关键词不能为空")
    if len(normalized) > 50:
        raise ValueError("搜索关键词不能超过 50 字符")
    data = await _get("/api/community/search", params={"q": normalized})
    if isinstance(data, dict) and isinstance(data.get("users"), list):
        return data["users"]
    return data if isinstance(data, list) else []


async def get_community_notices(since: float = 0) -> list:
    """
    获取当前用户的社区定向通知（如排名变化、被关注等）。
    与 get_notices（系统公告）不同，这是用户个人的社区通知。

    Args:
        since: Unix 秒时间戳，只返回该时间之后的通知；默认返回最近通知。
    """
    _require_token()
    data = await _get("/api/community/notices", params={"since": since})
    return data if isinstance(data, list) else []


async def get_community_authorization() -> dict:
    """
    查询当前用户的喵舍社区授权状态。
    返回是否已授权、是否展示金额、是否匿名等信息。
    适合在首次使用社区功能前检查授权状态。
    """
    _require_token()
    return await _get("/api/community/authorization")


async def authorize_community(
    show_amount: bool = False,
    anonymous: bool = False,
) -> dict:
    """
    授权参与喵舍社区排行榜。调用前须向用户确认是否愿意公开持仓数据。
    授权后用户的收益率将出现在社区排行榜中。

    Args:
        show_amount: 是否公开展示持仓金额（默认 false，仅展示收益率）
        anonymous: 是否匿名参与（默认 false）
    """
    _require_token()
    return await _post("/api/community/authorize", {
        "authorized": True,
        "show_amount": show_amount,
        "anonymous": anonymous,
        "disclaimer_accepted": True,
    })


async def revoke_community_authorization() -> dict:
    """
    取消喵舍社区授权，退出排行榜。
    取消后用户的收益率数据将从排行榜中移除。
    """
    _require_token()
    return await _delete("/api/community/authorize")


async def follow_community_user(target_uid: str) -> dict:
    """
    关注/取消关注喵舍社区用户（取反操作）。
    若已关注则取消关注，若未关注则添加关注。

    Args:
        target_uid: 目标用户的 8 位 UID
    """
    _require_token()
    normalized = _validate_uid(target_uid, "target_uid")
    return await _post("/api/community/follow", {"target_uid": normalized})


async def analyze_jcti(
    personality_id: str,
    ye: float = 0,
    wen: float = 0,
    sui: float = 0,
    duan: float = 0,
) -> dict:
    """
    提交 JCTI（韭彩测试指标）四维分数，获取 AI 个性化投资人格分析。
    需要 VIP 或 PRO 会员权限。

    人格 ID 对照：
    - tepulang: 特普朗（高野高稳）
    - jiuhuang: 韭黄（高野高随）
    - faguo-dushen: 法国赌神（高野高短）
    - ji-wuli: 姬无力（低野低稳）
    - yingshengchong: 应声虫（低野高随）
    - shanmu: 山姆（低野高稳）
    - taozhongren: 套中人（低野高短）
    - tuoluowang: 陀螺王（高野低短）

    Args:
        personality_id: 人格 ID，如 "tepulang"
        ye: 野维度分数（0-100）
        wen: 稳维度分数（0-100）
        sui: 随维度分数（0-100）
        duan: 短维度分数（0-100）

    Returns:
        dict 包含 analysis 字段（AI 生成的个性化分析文本）
    """
    _require_token()
    valid_ids = {
        "tepulang", "jiuhuang", "faguo-dushen", "ji-wuli",
        "yingshengchong", "shanmu", "taozhongren", "tuoluowang",
    }
    normalized = str(personality_id or "").strip().lower()
    if normalized not in valid_ids:
        raise ValueError(f"无效的 personality_id：{personality_id}，有效值：{', '.join(sorted(valid_ids))}")
    for name, val in [("ye", ye), ("wen", wen), ("sui", sui), ("duan", duan)]:
        if (
            isinstance(val, bool)
            or not isinstance(val, (int, float))
            or not math.isfinite(float(val))
            or not 0 <= float(val) <= 100
        ):
            raise ValueError(f"{name} 分数必须在 0-100 之间，收到：{val}")
    return await _post("/api/jcti/analyze", {
        "scores": {"ye": ye, "wen": wen, "sui": sui, "duan": duan},
        "personality_id": normalized,
    })
