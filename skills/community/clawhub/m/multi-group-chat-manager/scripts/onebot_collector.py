"""
OneBot 群消息采集器
====================
通过 OneBot v11 HTTP API (get_group_msg_history) 拉取完整群聊消息记录,
替代 AI 会话限制导致的 100 条上限问题。

负责:
- 上线恢复时拉取未处理的历史消息(意外中断恢复)
- 下线扫描时拉取本次会话窗口内的全部消息
- 消息预处理(提取文本、发送者、时间戳)
- 与 profiles.py / affection.py 集成完成画像+好感度更新

依赖:requests(唯一外部包依赖)
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin

import requests

# ── 修复 Windows 编码 ──
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

# ── 从统一配置读取 ──
sys.path.insert(0, str(SCRIPT_DIR))
from config import load as load_config
from memory import FluidMemory

# ── 常量 ──
# 默认群号从 config.json 的 onebot.groups 中读取第一个
# 也可通过 --group-id 参数指定

# FluideMemory 存储目录
MEMORY_DIR = str(SKILL_DIR / "profiles" / "memory")


def _get_fm():
    """获取 FluidMemory 实例"""
    return FluidMemory(MEMORY_DIR)


def get_onebot_config() -> dict:
    """读取 OneBot 配置,优先从 config.json 获取,否则用默认值"""
    cfg = load_config()
    obot = cfg.get("onebot", {})
    return {
        "base_url": obot.get("base_url", "http://127.0.0.1:3000"),
        "timeout": obot.get("timeout", 10),
    }


# ═════════════════════════════════════════════════════════
# 核心 API 调用
# ═════════════════════════════════════════════════════════

def _api_call(action: str, params: dict = None) -> dict:
    """
    调用 OneBot HTTP API。

    标准 OneBot v11 协议:
    POST /{action}  { params }
    → {"status": "ok", "retcode": 0, "data": {...}}

    兼容 LLBot 的可能差异。
    """
    obot = get_onebot_config()
    url = urljoin(obot["base_url"].rstrip("/") + "/", action)
    timeout = obot["timeout"]

    try:
        resp = requests.post(url, json=params or {}, timeout=timeout)
        data = resp.json()
    except requests.RequestException as e:
        return {"status": "failed", "retcode": -1, "data": None,
                "_error": f"HTTP 请求失败: {e}"}
    except json.JSONDecodeError as e:
        return {"status": "failed", "retcode": -1, "data": None,
                "_error": f"JSON 解析失败: {e}"}

    return data


def _parse_onebot_message(msg: dict) -> dict:
    """
    解析单条 OneBot 消息,提取结构化信息。

    OneBot v11 消息格式:
    {
        "message_id": int,
        "user_id": int,
        "time": int,          # Unix 时间戳
        "message": [...] | str,  # CQ 码数组或字符串
        "message_seq": int,   # 群消息序号
        "sender": {
            "user_id": int,
            "nickname": str,
            "card": str,       # 群名片(可选)
        }
    }
    """
    user_id = str(msg.get("user_id", "0"))
    sender = msg.get("sender", {})
    nickname = sender.get("card", "") or sender.get("nickname", "") or "未知"
    timestamp = msg.get("time", 0)
    message_seq = msg.get("message_seq", 0)
    message_id = msg.get("message_id", 0)

    # 提取纯文本内容
    raw_message = msg.get("message", "")
    text_content = _extract_text(raw_message)

    return {
        "user_id": user_id,
        "nickname": nickname,
        "timestamp": timestamp,
        "message_seq": message_seq,
        "message_id": message_id,
        "text": text_content,
        "raw": msg,
    }


def _extract_messages_from_response(result: dict) -> list:
    """
    从 OneBot API 响应中提取消息列表。

    兼容两种格式:
    - 标准 OneBot: data = [...]
    - LLBot:      data = { "messages": [...] }
    """
    data = result.get("data")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        msgs = data.get("messages", [])
        if isinstance(msgs, list):
            return msgs
    return []


def _extract_text(message: Any) -> str:
    """
    从 OneBot 消息中提取纯文本。

    OneBot 消息可以是:
    - 字符串(CQ码格式):"[CQ:at,qq=123] 你好"
    - 消息段数组:[{"type":"text","data":{"text":"你好"}}, ...]
    """
    if isinstance(message, str):
        # 简单去除 CQ 码
        import re
        return re.sub(r'\[CQ:[^\]]*\]', '', message).strip()

    if isinstance(message, list):
        parts = []
        for seg in message:
            if isinstance(seg, dict):
                if seg.get("type") == "text":
                    parts.append(seg.get("data", {}).get("text", ""))
                elif seg.get("type") == "at":
                    target = seg.get("data", {}).get("qq", "")
                    parts.append(f"@{target}")
                elif seg.get("type") == "reply":
                    # 忽略回复节点,它的 text 会被后续消息段覆盖
                    pass
        return " ".join(p.strip() for p in parts if p.strip())

    return str(message)


# ═════════════════════════════════════════════════════════
# 群消息采集
# ═════════════════════════════════════════════════════════

def fetch_group_messages(
    group_id: str,
    since_time: Optional[int] = None,
    until_time: Optional[int] = None,
    max_count: int = 500,
    since_seq: Optional[int] = None,
    until_seq: Optional[int] = None,
) -> List[dict]:
    """
    获取指定群在时间区间内的消息列表。

    LLBot / go-cqhttp 实现说明:
    - get_group_msg_history 每次返回最新 N 条(从新到旧排序)
    - 没有标准的分页参数
    - 用 message_seq 检测重复,递增 count 来覆盖更远
    - 最终返回从旧到新排序的列表

    参数:
        group_id: QQ 群号
        since_time: 起始 Unix 时间戳(含,None 表示不限制)
        until_time: 截止 Unix 时间戳(含,None 表示不限制)
        max_count: 最大拉取消息数
        since_seq: 起始 message_seq(含,与 since_time 二选一)
        until_seq: 截止 message_seq(含,与 until_time 二选一)

    返回:
        解析后的消息列表(从旧到新排序)
    """
    messages = []
    existing_seqs = set()

    # LLBot 无法真正分页,只能通过递增 count 覆盖更多历史
    # 分步拉取:先拉 count = batch_size,不够再拉到 2x
    steps = [20, 50, 100, 200, 500, 1000]
    current_count = 0

    for batch_size in steps:
        if len(messages) >= max_count:
            break
        if batch_size <= current_count:
            continue

        params = {"group_id": int(group_id), "count": batch_size}
        result = _api_call("get_group_msg_history", params)

        if result.get("status") != "ok" or result.get("retcode") != 0:
            break

        batch = _extract_messages_from_response(result)
        if not batch:
            break

        current_count = batch_size

        # LLBot 返回的 batch 是从新到旧排序的
        # 先反转成从旧到新方便处理
        if len(batch) >= 2:
            if batch[0].get("time", 0) > batch[-1].get("time", 0):
                batch.reverse()

        new_count = 0
        for msg in batch:
            if not isinstance(msg, dict):
                continue

            msg_seq = msg.get("message_seq", 0)
            if msg_seq in existing_seqs:
                continue

            parsed = _parse_onebot_message(msg)
            msg_ts = parsed["timestamp"]

            # 时间范围过滤
            if since_time and msg_ts < since_time:
                continue
            if until_time and msg_ts > until_time:
                continue

            # seq 范围过滤
            if since_seq and parsed["message_seq"] < since_seq:
                continue
            if until_seq and parsed["message_seq"] > until_seq:
                continue

            messages.append(parsed)
            existing_seqs.add(msg_seq)
            new_count += 1

        if new_count == 0:
            break

    messages.sort(key=lambda m: m["timestamp"])
    return messages[:max_count]


def fetch_recent_messages(group_id: str, count: int = 100) -> List[dict]:
    """获取最近 N 条群消息(简化接口,不需要时间参数)"""
    result = _api_call("get_group_msg_history", {
        "group_id": int(group_id),
        "count": count,
    })

    if result.get("status") != "ok" or result.get("retcode") != 0:
        return []

    batch = _extract_messages_from_response(result)
    messages = [_parse_onebot_message(msg) for msg in batch if isinstance(msg, dict)]
    messages.sort(key=lambda m: m["timestamp"])
    return messages


# ═════════════════════════════════════════════════════════
# 消息处理与画像提取辅助
# ═════════════════════════════════════════════════════════

def aggregate_by_user(messages: List[dict]) -> Dict[str, dict]:
    """
    按用户聚合消息。

    返回: { user_id: { "nickname": str, "messages": [str], "count": int, "time_range": (min,max) } }
    """
    users = {}
    for msg in messages:
        uid = msg["user_id"]
        if uid not in users:
            users[uid] = {
                "nickname": msg["nickname"],
                "messages": [],
                "count": 0,
                "first_seen": msg["timestamp"],
                "last_seen": msg["timestamp"],
            }
        users[uid]["messages"].append(msg["text"])
        users[uid]["count"] += 1
        users[uid]["first_seen"] = min(users[uid]["first_seen"], msg["timestamp"])
        users[uid]["last_seen"] = max(users[uid]["last_seen"], msg["timestamp"])

    return users


def fmt_timestamp(ts: int) -> str:
    """将 Unix 时间戳转为可读字符串(GMT+8)"""
    if not ts:
        return "未知"
    dt = datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=8)))
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _parse_timestamp(value: str) -> Optional[int]:
    """
    解析时间参数，同时支持：
    - Unix 秒级时间戳（如 1715731200）
    - ISO 8601 字符串（如 "2026-05-14T10:00:00" / "2026-05-14 10:00:00"）
    返回 Unix 时间戳(int)，解析失败返回 None。
    """
    if value is None:
        return None
    if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
        return int(value)
    if isinstance(value, str):
        # 尝试多种日期格式
        for fmt in [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%d",
        ]:
            try:
                dt = datetime.strptime(value, fmt)
                # 默认视为 GMT+8
                return int(dt.replace(tzinfo=timezone(timedelta(hours=8))).timestamp())
            except ValueError:
                continue
    return None


class ParseTS:
    """argparse type 工厂：接受 int 时间戳或 ISO 日期字符串"""
    def __call__(self, value: str) -> Optional[int]:
        return _parse_timestamp(value)
    def __repr__(self):
        return "时间戳(int) 或 ISO 日期字符串"


parse_timestamp = ParseTS()


# ═════════════════════════════════════════════════════════
# CLI 入口
# ═════════════════════════════════════════════════════════

def cmd_fetch(args):
    """采集群消息"""
    messages = fetch_group_messages(
        group_id=args.group_id,
        since_time=args.since,
        until_time=args.until,
        max_count=args.count,
        since_seq=args.since_seq,
        until_seq=args.until_seq,
    )

    # 输出 JSON
    output = {
        "group_id": args.group_id,
        "count": len(messages),
        "time_range": {
            "from": fmt_timestamp(messages[0]["timestamp"]) if messages else None,
            "to": fmt_timestamp(messages[-1]["timestamp"]) if messages else None,
        },
        "users": aggregate_by_user(messages),
        "messages": messages,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_recent(args):
    """获取最近 N 条消息"""
    messages = fetch_recent_messages(args.group_id, args.count)
    output = {
        "group_id": args.group_id,
        "count": len(messages),
        "time_range": {
            "from": fmt_timestamp(messages[0]["timestamp"]) if messages else None,
            "to": fmt_timestamp(messages[-1]["timestamp"]) if messages else None,
        },
        "users": aggregate_by_user(messages),
        "messages": messages,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_health(args):
    """检查 OneBot 连接是否正常"""
    obot = get_onebot_config()
    base = obot["base_url"]

    # 尝试获取登录号信息作为健康检查
    try:
        result = _api_call("get_login_info")
        if result.get("status") == "ok" and result.get("retcode") == 0:
            data = result.get("data", {})
            print(json.dumps({
                "status": "ok",
                "base_url": base,
                "user_id": str(data.get("user_id", "")),
                "nickname": data.get("nickname", ""),
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({
                "status": "error",
                "base_url": base,
                "error": f"OneBot 返回异常: {result}",
            }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "base_url": base,
            "error": str(e),
        }, ensure_ascii=False, indent=2))


def cmd_users(args):
    """按用户聚合消息并输出统计"""
    messages = fetch_group_messages(
        group_id=args.group_id,
        since_time=args.since,
        until_time=args.until,
        max_count=args.count,
    )

    aggregated = aggregate_by_user(messages)
    output = {
        "group_id": args.group_id,
        "total_messages": len(messages),
        "total_users": len(aggregated),
        "users": {
            uid: {
                "nickname": info["nickname"],
                "count": info["count"],
                "first_seen": fmt_timestamp(info["first_seen"]),
                "last_seen": fmt_timestamp(info["last_seen"]),
                "latest_messages": info["messages"][-5:],  # 最近5条
            }
            for uid, info in aggregated.items()
        },
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ═════════════════════════════════════════════════════════
# 集成扫描(采集 + 好感度)
# ═════════════════════════════════════════════════════════

def _call_affection_add(user_id: str, rule_key: str, reason: str) -> dict:
    """
    通过子进程调用 affection.py,避免直接的 Python 模块导入兼容性问题。
    返回 { "status": "ok" | "error", "score": float }

    注意: 不能用 text=True,因为
    1) Windows + 中文 locale 会用 GBK 解码管道,
    2) affection.py 输出 emoji(⭐)，GBK 无法解码
    3) reader thread 静默崩溃 → r.stdout = None → .strip() 爆罢
    """
    import subprocess
    try:
        r = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "affection.py"),
             "add", user_id, rule_key, reason],
            capture_output=True, timeout=15,
        )
        # 手动解码，避免 text=True 引发的 GBK 解码失败
        stdout = r.stdout.decode('utf-8', errors='replace') if r.stdout else ""
        stderr = r.stderr.decode('utf-8', errors='replace') if r.stderr else ""

        if r.returncode == 0:
            lines = stdout.split("\n")
            for line in lines:
                if "当前分数" in line:
                    import re
                    m = re.search(r'[\d.]+', line)
                    if m:
                        return {"status": "ok", "score": float(m.group())}
            return {"status": "ok", "score": None}
        else:
            return {"status": "error", "error": stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def cmd_scan(args):
    """
    全流程扫描:采集消息 → 好感度更新 → 画像强化。

    这是方向一+方向二+方向七的集成命令,供上下线流程调用。
    三层流水线:
      1. 采集(方向一):通过 OneBot 拉取群消息
      2. 好感度(方向七):规则引擎自动判定加减分
      3. 画像强化(方向二):匹配已有记忆 → 强化;输出消息原文供 AI 提取新特征

    参数:
        --group-id: QQ 群号
        --since: 起始时间戳(Unix秒)
        --until: 截止时间戳
        --max-msgs: 最大消息数
        --no-affection: 跳过好感度更新
        --no-profile: 跳过画像强化(仅采集+好感度)
        --dry-run: 仅采集和统计,不写入任何数据
    """
    messages = fetch_group_messages(
        group_id=args.group_id,
        since_time=args.since,
        until_time=args.until,
        max_count=args.max_msgs,
    )

    result = {
        "group_id": args.group_id,
        "status": "ok",
        "messages_fetched": len(messages),
        "time_range": {
            "from": fmt_timestamp(messages[0]["timestamp"]) if messages else None,
            "to": fmt_timestamp(messages[-1]["timestamp"]) if messages else None,
        },
        "users": {},       # 按用户聚合统计(含消息原文)
        "message_texts": [m["text"] for m in messages],  # AI 分析用
        "affection": {},   # 好感度更新结果
        "profile_reinforcements": {},  # 画像强化结果(方向二)
        "errors": [],
    }

    if not messages:
        result["message"] = "没有消息需要处理"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 按用户聚合
    aggregated = aggregate_by_user(messages)
    result["users"] = {
        uid: {
            "nickname": info["nickname"],
            "count": info["count"],
            "first_seen": fmt_timestamp(info["first_seen"]),
            "last_seen": fmt_timestamp(info["last_seen"]),
            "all_messages": info["messages"],  # AI 分析用
        }
        for uid, info in aggregated.items()
    }

    # ── 好感度更新(方向七)──
    if not args.no_affection and not args.dry_run:
        affection_results = {}
        for uid, info in aggregated.items():
            if info["count"] <= 0:
                continue
            r = _call_affection_add(uid, "friendly_chat", "群聊发言(OneBot 扫描)")
            affection_results[uid] = r
        result["affection"] = affection_results

    # ── 画像强化(方向二)──
    if not args.no_profile and not args.dry_run:
        fm = _get_fm()
        profile_results = {}
        for uid, info in aggregated.items():
            msg_texts = info["messages"]
            if not msg_texts:
                continue
            reinforced = fm.reinforce_by_messages(uid, msg_texts)
            if reinforced:
                profile_results[uid] = {
                    "nickname": info["nickname"],
                    "reinforced_count": len(reinforced),
                    "details": reinforced,
                }
        result["profile_reinforcements"] = profile_results
        if profile_results:
            total_reinforced = sum(
                r["reinforced_count"] for r in profile_results.values()
            )
            result["message"] = (
                f"采集 {len(messages)} 条消息,"
                f"涉及 {len(aggregated)} 位用户,"
                f"强化 {total_reinforced} 条记忆 | "
                f"时间范围 {result['time_range']['from']} ~ {result['time_range']['to']}"
            )
        else:
            result["message"] = (
                f"采集 {len(messages)} 条消息,"
                f"涉及 {len(aggregated)} 位用户,"
                f"无记忆被强化(已有画像特征未被提及) | "
                f"时间范围 {result['time_range']['from']} ~ {result['time_range']['to']}"
            )
    else:
        result["message"] = (
            f"采集 {len(messages)} 条消息,"
            f"涉及 {len(aggregated)} 位用户,"
            f"时间范围 {result['time_range']['from']} ~ {result['time_range']['to']}"
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OneBot 群消息采集器")
    sub = parser.add_subparsers(dest="command")

    # fetch - 按时间范围采集
    p_fetch = sub.add_parser("fetch", help="按时间范围采集群消息")
    p_fetch.add_argument("--group-id", required=True, help="QQ 群号（必填）")
    p_fetch.add_argument("--since", type=parse_timestamp, default=None, help="起始时间戳或 ISO 日期(如 2026-05-14T10:00:00)")
    p_fetch.add_argument("--until", type=parse_timestamp, default=None, help="截止时间戳或 ISO 日期")
    p_fetch.add_argument("--since-seq", type=int, default=None, help="起始 message_seq")
    p_fetch.add_argument("--until-seq", type=int, default=None, help="截止 message_seq")
    p_fetch.add_argument("--count", type=int, default=500, help="最大拉取数")

    # recent - 最近 N 条
    p_recent = sub.add_parser("recent", help="获取最近 N 条消息")
    p_recent.add_argument("--group-id", required=True, help="QQ 群号（必填）")
    p_recent.add_argument("--count", type=int, default=100, help="条数")

    # users - 按用户聚合
    p_users = sub.add_parser("users", help="按用户聚合统计")
    p_users.add_argument("--group-id", required=True, help="QQ 群号（必填）")
    p_users.add_argument("--since", type=parse_timestamp, default=None, help="起始时间戳或 ISO 日期")
    p_users.add_argument("--until", type=parse_timestamp, default=None, help="截止时间戳或 ISO 日期")
    p_users.add_argument("--count", type=int, default=500, help="最大拉取数")

    # scan - 全流程扫描（方向一+方向二+方向七集成）
    p_scan = sub.add_parser("scan", help="全流程扫描：采集→好感度→画像强化")
    p_scan.add_argument("--group-id", required=True, help="QQ 群号（必填）")
    p_scan.add_argument("--since", type=parse_timestamp, default=None, help="起始时间戳或 ISO 日期")
    p_scan.add_argument("--until", type=parse_timestamp, default=None, help="截止时间戳或 ISO 日期")
    p_scan.add_argument("--max-msgs", type=int, default=500, help="最大消息数")
    p_scan.add_argument("--no-affection", action="store_true", help="跳过好感度更新")
    p_scan.add_argument("--no-profile", action="store_true", help="跳过画像强化（仅采集+好感度）")
    p_scan.add_argument("--dry-run", action="store_true", help="仅采集和统计，不写入任何数据")

    # health - 连接检查
    p_health = sub.add_parser("health", help="检查 OneBot 连接")

    args = parser.parse_args()

    if args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "recent":
        cmd_recent(args)
    elif args.command == "users":
        cmd_users(args)
    elif args.command == "scan":
        cmd_scan(args)
    elif args.command == "health":
        cmd_health(args)
    else:
        parser.print_help()
