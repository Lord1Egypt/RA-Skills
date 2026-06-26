"""
Multi-Group-Chat-Manager - 上下线会话状态管理
=========================================
管理多群聊的上下线状态，支持：
- 上线标记（记录 session_start + 自动注册活跃群）
- 按群下线（只处理指定群的扫描区间）
- 全局下线（遍历所有活跃群）
- 意外中断检测与恢复（遗留群扫最近24h）

状态文件：session_state.json（skill 根目录）
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List

# 修复 Windows 编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

STATE_FILE = SKILL_DIR / "session_state.json"

# ── 从统一配置读取参数 ──
sys.path.insert(0, str(SCRIPT_DIR))
from config import load as load_config
_cfg = load_config()
RECOVERY_WINDOW_HOURS = _cfg["session"]["recovery_window_hours"]
RECOVERY_MAX_MESSAGES = _cfg["session"]["recovery_max_messages"]
DEFAULT_MAX_MESSAGES = _cfg["session"]["default_max_messages"]


# ══════════════════════════════════════════
# 状态模型
# ══════════════════════════════════════════

def default_state() -> dict:
    return {
        "status": "offline",         # "online" | "offline"
        "session_start": None,       # 全局上线时间戳（ISO 8601）
        "groups": {},                # { chat_id: GroupState }
    }


def default_group(name: str = "") -> dict:
    return {
        "name": name,
        "session_start": None,       # 该群被激活的时间
        "last_active": None,         # 最后活跃时间（刷新用）
    }


# ══════════════════════════════════════════
# 状态读写
# ══════════════════════════════════════════

def _now_iso() -> str:
    """返回当前时间的 ISO 8601 格式字符串（带时区）"""
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def _now_ts() -> float:
    return time.time()


def iso_to_ts(iso_str: str) -> float:
    """将 ISO 8601 字符串转为时间戳"""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.timestamp()
    except (ValueError, TypeError):
        return 0


def load_state() -> dict:
    """加载会话状态"""
    if not STATE_FILE.exists():
        return default_state()
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 确保 key 完整
        for key in ["status", "session_start", "groups"]:
            if key not in data:
                data[key] = default_state()[key]
        return data
    except (json.JSONDecodeError, OSError):
        return default_state()


def save_state(state: dict):
    """保存会话状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════
# 核心操作
# ══════════════════════════════════════════

def go_online() -> dict:
    """
    执行上线操作。
    
    返回值:
        - "status": "ok" | "recovered"
        - "message": 描述文本
        - "recovered_groups": 意外中断恢复的群列表（如果有）
        - "session_start": 当前上线时间戳
    """
    state = load_state()
    now = _now_iso()
    result = {
        "status": "ok",
        "message": "",
        "recovered_groups": [],
        "session_start": now,
    }

    # 检查意外中断（上次 status == "online" 且有遗留群）
    if state.get("status") == "online" and state.get("groups"):
        recovered = []
        for chat_id, ginfo in list(state["groups"].items()):
            if not isinstance(ginfo, dict):
                continue  # 跳过遗留字符串值
            recovered.append({
                "chat_id": chat_id,
                "name": ginfo.get("name", chat_id),
                "session_start": ginfo.get("session_start"),
            })
        state["groups"] = {}
        result["status"] = "recovered"
        result["recovered_groups"] = recovered
        result["message"] = (
            f"检测到上次异常中断，{len(recovered)} 个群需要恢复扫描 "
            f"（最近 {RECOVERY_WINDOW_HOURS}h 内，最多 {RECOVERY_MAX_MESSAGES} 条消息）"
        )

    # 重置状态
    state["status"] = "online"
    state["session_start"] = now
    state["groups"] = state.get("groups", {})
    save_state(state)

    if not result["message"]:
        result["message"] = f"已上线，session_start: {now}"

    return result


def go_offline(chat_id: Optional[str] = None,
               group_name: str = "") -> dict:
    """
    执行下线操作。
    
    参数:
        chat_id: 指定群下线。None 表示全部群下线
        group_name: 群名（仅 chat_id 不为空时有效）
    
    返回值:
        - "status": "ok" | "no_active_groups" | "group_not_found"
        - "processed": [处理了的群列表] 或 None
        - "unprocessed": [未处理群列表] 或 None（仅全线下线时）
        - "message": 描述文本
        - "offline_time": 下线时间
    """
    state = load_state()
    now = _now_iso()
    result = {
        "status": "ok",
        "processed": [],
        "unprocessed": [],
        "message": "",
        "offline_time": now,
    }

    if not state.get("groups"):
        result["status"] = "no_active_groups"
        result["message"] = "当前没有激活的群聊会话"
        return result

    if chat_id:
        # 指定群下线
        if chat_id not in state["groups"]:
            result["status"] = "group_not_found"
            result["message"] = f"群 {group_name or chat_id} 不在活跃列表中"
            return result

        ginfo = state["groups"][chat_id]
        if not isinstance(ginfo, dict):
            # 遗留的字符串值，直接删除
            del state["groups"][chat_id]
            result["message"] = f"已清理遗留数据（{chat_id}）"
            save_state(state)
            return result

        scan_start = ginfo.get("session_start") or state.get("session_start")
        result["processed"].append({
            "chat_id": chat_id,
            "name": ginfo.get("name", group_name or chat_id),
            "scan_start": scan_start,
            "scan_end": now,
        })
        del state["groups"][chat_id]
        result["message"] = f"已在 {ginfo.get('name', group_name)} 执行下线扫描"

    else:
        # 全部群下线
        for cid, ginfo in list(state["groups"].items()):
            if not isinstance(ginfo, dict):
                continue  # 跳过遗留字符串值
            scan_start = ginfo.get("session_start") or state.get("session_start")
            result["processed"].append({
                "chat_id": cid,
                "name": ginfo.get("name", cid),
                "scan_start": scan_start,
                "scan_end": now,
            })
        state["groups"] = {}
        result["message"] = f"已对 {len(result['processed'])} 个活跃群执行全局下线扫描"

    # 如果所有群都处理完了，标记离线
    if not state["groups"]:
        state["status"] = "offline"

    save_state(state)
    return result


def register_group(chat_id: str, name: str = "") -> dict:
    """
    注册一个活跃群（当机器人在该群发言时自动调用）。
    如果该群已在 groups 中，仅刷新 last_active。
    
    返回值:
        - "new": True/False（是否是新激活的群）
        - "session_start": 该群的 session_start
    """
    state = load_state()

    if state.get("status") != "online":
        # 没人在线，不注册
        return {"new": False, "session_start": None}

    now = _now_iso()
    if chat_id not in state.get("groups", {}):
        ginfo = default_group(name)
        ginfo["session_start"] = now
        state["groups"][chat_id] = ginfo
        is_new = True
    else:
        state["groups"][chat_id]["last_active"] = now
        is_new = False

    save_state(state)
    return {
        "new": is_new,
        "session_start": state["groups"][chat_id]["session_start"],
    }


def get_status() -> dict:
    """获取当前状态概览"""
    state = load_state()
    now_ts = _now_ts()

    groups_info = []
    for cid, ginfo in state.get("groups", {}).items():
        if isinstance(ginfo, str):
            continue  # 跳过兼容性字段
        groups_info.append({
            "chat_id": cid,
            "name": ginfo.get("name", cid),
            "session_start": ginfo.get("session_start"),
            "last_active": ginfo.get("last_active"),
        })

    return {
        "status": state.get("status", "offline"),
        "session_start": state.get("session_start"),
        "active_group_count": len(groups_info),
        "groups": groups_info,
        "recovery_config": {
            "window_hours": RECOVERY_WINDOW_HOURS,
            "max_messages": RECOVERY_MAX_MESSAGES,
        }
    }


def is_online() -> bool:
    """快速检查当前是否在线"""
    state = load_state()
    return state.get("status") == "online"


def get_scan_windows() -> List[dict]:
    """
    获取所有活跃群及其扫描时间窗口（供下线扫描用）。
    
    返回值: [{ chat_id, name, scan_start, scan_end }, ...]
    """
    state = load_state()
    now = _now_iso()
    windows = []

    for cid, ginfo in state.get("groups", {}).items():
        if isinstance(ginfo, str):
            continue
        windows.append({
            "chat_id": cid,
            "name": ginfo.get("name", cid),
            "scan_start": ginfo.get("session_start") or state.get("session_start"),
            "scan_end": now,
        })

    return windows


# ══════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="上下线会话状态管理")
    sub = parser.add_subparsers(dest="command")

    p_online = sub.add_parser("online", help="上线")
    p_offline = sub.add_parser("offline", help="下线")
    p_offline.add_argument("--chat_id", default=None, help="指定群下线")
    p_offline.add_argument("--name", default="", help="群名")
    p_offline.add_argument("--all", action="store_true", help="全部群下线")

    p_register = sub.add_parser("register", help="注册活跃群")
    p_register.add_argument("chat_id")
    p_register.add_argument("--name", default="")

    p_status = sub.add_parser("status", help="查看状态")
    p_scans = sub.add_parser("scans", help="获取扫描窗口")

    args = parser.parse_args()

    if args.command == "online":
        result = go_online()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "offline":
        cid = args.chat_id
        if args.all:
            cid = None
        result = go_offline(chat_id=cid, group_name=args.name)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "register":
        result = register_group(args.chat_id, name=args.name)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "status":
        print(json.dumps(get_status(), ensure_ascii=False, indent=2))

    elif args.command == "scans":
        print(json.dumps(get_scan_windows(), ensure_ascii=False, indent=2))

    else:
        parser.print_help()
