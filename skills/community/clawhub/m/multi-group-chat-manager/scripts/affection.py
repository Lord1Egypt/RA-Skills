# -*- coding: utf-8 -*-
"""
好感度系统 - 加减分、日志、查询
"""

import json
import os
import sys
import time
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta

SKILL_DIR = Path(__file__).resolve().parent.parent
AFFECTION_FILE = SKILL_DIR / "affection.json"
LOG_DIR = SKILL_DIR / "logs"

# ── 从统一配置读取参数 ──
_script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_script_dir))
from config import load as load_config
_cfg = load_config()

LOCK_TIMEOUT = _cfg["affection"]["lock_timeout"]
LOCK_STALE = _cfg["affection"]["lock_stale_seconds"]
DEFAULT_SCORE = _cfg["affection"]["default_score"]
SMALL_GROUP_SCORE = _cfg["affection"]["small_group_default_score"]
SMALL_GROUP_IDS = _cfg["affection"]["small_group_ids"]
BRIEF_HOURS = _cfg["affection"]["brief_query_hours"]
DETAIL_MAX = _cfg["affection"]["detail_max_entries"]
MIN_SCORE = _cfg["affection"]["min_score"]
MAX_SCORE = _cfg["affection"]["max_score"]

# ── 文件锁配置 ──
LOCK_FILE = AFFECTION_FILE.with_suffix(".lock")


def _acquire_lock():
    """获取文件锁,阻塞等待。带超时和防死锁(自动打破过期锁)。"""
    deadline = time.time() + LOCK_TIMEOUT
    while time.time() < deadline:
        # 检查是否有过期锁(进程崩溃后留下的)
        if LOCK_FILE.exists():
            try:
                age = time.time() - LOCK_FILE.stat().st_mtime
                if age > LOCK_STALE:
                    LOCK_FILE.unlink(missing_ok=True)
                    continue
            except OSError:
                pass
            time.sleep(0.05 + random.random() * 0.02)
            continue

        # 尝试创建锁文件
        try:
            LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")
            return
        except OSError:
            time.sleep(0.05 + random.random() * 0.02)
            continue

    raise RuntimeError(f"好感度文件锁超时({LOCK_TIMEOUT}秒),无法获取锁")


def _release_lock():
    """释放文件锁"""
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink(missing_ok=True)
    except OSError:
        pass

# ── 加减分规则表 ──
RULES = {
    "friendly_chat":    {"name": "友善闲聊",     "points": 0.5, "type": "add", "desc": "正常聊天互动"},
    "share_creation":   {"name": "分享创作",     "points": 3,   "type": "add", "desc": "分享OC/同人/游戏等"},
    "feedback":         {"name": "建设性建议",   "points": 2,   "type": "add", "desc": "给他人创作提建议"},
    "share_resource":   {"name": "分享资源",     "points": 2,   "type": "add", "desc": "分享安全优质资源"},
    "defend_atmosphere":{"name": "维护氛围",     "points": 3,   "type": "add", "desc": "帮说话/维护群秩序"},
    "deep_discussion":  {"name": "深度讨论",     "points": 2,   "type": "add", "desc": "哲学/文学/技术讨论"},
    "greeting":         {"name": "主动招呼",     "points": 1,   "type": "add", "desc": "主动打招呼/AI特"},
    "argue_attack":     {"name": "争吵攻击",     "points": 5,   "type": "sub", "desc": "吵架/人身攻击"},
    "spam":             {"name": "刷屏灌水",     "points": 2,   "type": "sub", "desc": "无意义刷屏影响观感"},
    "disgusting":       {"name": "逆天内容",     "points": 10,  "type": "sub", "desc": "色情/引战/冲击内容"},
    "scam_ad":          {"name": "诈骗广告",     "points": 10,  "type": "sub", "desc": "诈骗或商业广告"},
    "scary":            {"name": "吓人整蛊",     "points": 5,   "type": "sub", "desc": "吓人图/整蛊/砍价等"},
    "negativity":       {"name": "负能量/踩隐私", "points": 5,  "type": "sub", "desc": "传播负能量/开盒/角色黑"},
}

# ── 内部工具 ──

def _load():
    if not AFFECTION_FILE.exists():
        return {}
    return json.loads(AFFECTION_FILE.read_text(encoding="utf-8"))

def _save(data):
    AFFECTION_FILE.parent.mkdir(parents=True, exist_ok=True)
    AFFECTION_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def _log_path(user_id):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{user_id}.json"

def _load_log(user_id):
    p = _log_path(user_id)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))

def _save_log(user_id, entries):
    p = _log_path(user_id)
    p.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def _now_iso():
    """return ISO 8601 string (GMT+8)"""
    return datetime.now(timezone(timedelta(hours=8))).isoformat()

def _now_local_str(iso_str):
    """将 ISO 时间转为本地时间字符串(+8时区)"""
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
        cn = dt.astimezone(timezone(timedelta(hours=8)))
        return cn.strftime("%m-%d %H:%M")
    except:
        return iso_str

# ── 公开接口 ──

def get_level(score):
    """根据分数返回等级名称"""
    if score < 40:
        return "无感"
    elif score < 70:
        return "及格"
    else:
        return "优秀"

def get_level_icon(score):
    """返回等级对应的图标"""
    if score < 40:
        return "❄️"
    elif score < 70:
        return "🌱"
    elif score < 85:
        return "☀️"
    else:
        return "⭐"

def get_score(user_id):
    """获取用户当前好感度"""
    data = _load()
    if user_id not in data:
        return DEFAULT_SCORE, get_level(DEFAULT_SCORE)
    score = data[user_id]["score"]
    return score, get_level(score)

def add_score(user_id, rule_key, reason="", actor="system"):
    """
    为某用户增减好感度(带日志)。

    参数:
        user_id:  QQ 号(字符串)
        rule_key: RULES 字典中的 key
        reason:   具体原因描述(如:分享了某游戏截图)
        actor:    操作者(system / 管理员)

    返回:
        (成功?, 消息文本)
    """
    if rule_key not in RULES:
        return False, f"错误:未知规则 '{rule_key}'"

    rule = RULES[rule_key]
    points = rule["points"]
    if rule["type"] == "sub":
        points = -points

    # 加锁:读-改-写原子操作
    _acquire_lock()
    try:
        data = _load()
        now = _now_iso()

        if user_id not in data:
            data[user_id] = {"score": DEFAULT_SCORE, "last_update": now}

        old_score = data[user_id]["score"]
        new_score = max(MIN_SCORE, min(MAX_SCORE, old_score + points))
        data[user_id]["score"] = round(new_score, 1)
        data[user_id]["last_update"] = now
        _save(data)
    finally:
        _release_lock()

    # 写入日志
    entry = {
        "timestamp": now,
        "rule": rule_key,
        "rule_name": rule["name"],
        "change": points,
        "old_score": old_score,
        "new_score": round(new_score, 1),
        "reason": reason,
        "actor": actor,
    }

    entries = _load_log(user_id)
    entries.append(entry)
    _save_log(user_id, entries)

    icon = get_level_icon(new_score)
    change_str = f"+{points}" if points > 0 else str(points)
    return (
        True,
        f"{icon} {rule['name']}:{change_str}分({old_score}→{new_score})",
    )


def set_initial(user_id, score, note=""):
    """手动设置初始好感度(用于初始化小群成员)"""
    _acquire_lock()
    try:
        data = _load()
        now = _now_iso()
        data[user_id] = {"score": score, "last_update": now}
        _save(data)
    finally:
        _release_lock()

    # 日志记录
    entry = {
        "timestamp": now,
        "rule": "__init__",
        "rule_name": "初始设置",
        "change": 0,
        "old_score": 0,
        "new_score": score,
        "reason": note,
        "actor": "system",
    }
    entries = _load_log(user_id)
    entries.append(entry)
    _save_log(user_id, entries)

    level = get_level(score)
    return f"已设置 {user_id} 初始好感度:{score}分({level})"


def init_small_group(user_ids):
    """批量设置小群群友初始好感度(85分)"""
    results = []
    for uid in user_ids:
        results.append(set_initial(uid, SMALL_GROUP_SCORE, "小群群友初始"))
    return results


def query_detail(user_id):
    """
    详细查询（供管理员使用）。
    
    返回完整好感度信息和所有加减分条目。
    """
    data = _load()
    if user_id not in data:
        return f"用户 {user_id} 暂无好感度记录"

    score = data[user_id]["score"]
    level = get_level(score)
    icon = get_level_icon(score)
    last_up = _now_local_str(data[user_id].get("last_update", ""))

    entries = _load_log(user_id)

    lines = [
        f"━━━ {user_id} 的好感度 ━━━",
        f"  {icon} {score}分({level})",
        f"  最后更新:{last_up}",
    ]

    if entries:
        lines.append(f"  共 {len(entries)} 条记录(最近20条):")
        lines.append("  ────────────────")
        for e in reversed(entries[-20:]):
            t = _now_local_str(e["timestamp"])
            ch = e["change"]
            sign = "+" if ch >= 0 else ""
            lines.append(f"  [{t}] {sign}{ch} {e['rule_name']}")
            if e.get("reason"):
                lines.append(f"         └ {e['reason']}")
    else:
        lines.append("  暂无加减分记录")

    return "\n".join(lines)


def query_brief(user_id, hours=24):
    """
    简要查询(供群友本人使用)。

    仅返回:当前分数 + 近 N 小时的简要加减分条目。
    """
    data = _load()
    if user_id not in data:
        return f"你目前还没有好感度记录哦~"

    score = data[user_id]["score"]
    level = get_level(score)
    icon = get_level_icon(score)

    now = datetime.now(timezone(timedelta(hours=8)))
    cutoff = now - timedelta(hours=hours)

    entries = _load_log(user_id)
    recent = [
        e
        for e in entries
        if datetime.fromisoformat(e["timestamp"]) >= cutoff
    ]

    lines = [
        f"{icon} 你的好感度:{score}分({level})",
    ]

    if recent:
        total_change = sum(e["change"] for e in recent)
        lines.append(
            f"  近{hours}小时共 {len(recent)} 次变动(总变动:{total_change:+d}分)"
        )
        lines.append("  ────────────────")
        for e in reversed(recent[-10:]):
            t = _now_local_str(e["timestamp"])
            ch = e["change"]
            sign = "+" if ch >= 0 else ""
            lines.append(f"  [{t}] {sign}{ch} {e['rule_name']}")
    else:
        lines.append(f"  近{hours}小时暂无加减分变动")

    return "\n".join(lines)


def status():
    """查看好感度系统整体状态"""
    data = _load()
    total = len(data)
    scores = [v["score"] for v in data.values()]
    avg = round(sum(scores) / len(scores), 1) if scores else 0

    log_count = sum(len(_load_log(uid)) for uid in data)

    lines = [
        f"━━━ 好感度系统状态 ━━━",
        f"  追踪用户:{total} 人",
        f"  平均好感度:{avg} 分",
        f"  日志条目:{log_count} 条",
        f"  等级分布:",
        f"    ⭐ 优秀(70+): {sum(1 for s in scores if s >= 70)} 人",
        f"    ☀️ 及格(40-69): {sum(1 for s in scores if 40 <= s < 70)} 人",
        f"    ❄️ 无感(0-39): {sum(1 for s in scores if s < 40)} 人",
    ]
    return "\n".join(lines)


# ── CLI 入口 ──

def _parse_args():
    import sys
    import io

    # Windows 控制台 UTF-8 兼容
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    args = sys.argv[1:]
    if not args:
        return None

    cmd = args[0]

    if cmd == "add" and len(args) >= 3:
        user_id = args[1]
        rule = args[2]
        reason = args[3] if len(args) >= 4 else ""
        success, msg = add_score(user_id, rule, reason)
        print(msg if success else f"❌ {msg}")
        return True

    elif cmd == "get" and len(args) >= 2:
        user_id = args[1]
        score, level = get_score(user_id)
        print(f"{user_id}: {score}分({level})")
        return True

    elif cmd == "detail" and len(args) >= 2:
        user_id = args[1]
        print(query_detail(user_id))
        return True

    elif cmd == "brief" and len(args) >= 2:
        user_id = args[1]
        hours = int(args[2]) if len(args) >= 3 else 24
        print(query_brief(user_id, hours))
        return True

    elif cmd == "init" and len(args) >= 3:
        user_id = args[1]
        score = int(args[2])
        print(set_initial(user_id, score))
        return True

    elif cmd == "init-group":
        if SMALL_GROUP_IDS:
            for r in init_small_group(SMALL_GROUP_IDS):
                print(r)
        else:
            print("⚠️ SMALL_GROUP_IDS 未配置")
        return True

    elif cmd == "rules":
        print("━━━ 加减分规则 ━━━")
        for k, v in RULES.items():
            sign = "+" if v["type"] == "add" else "-"
            print(f"  {k}: {sign}{v['points']} | {v['name']} - {v['desc']}")
        return True

    elif cmd == "status":
        print(status())
        return True

    else:
        print(
            "用法:\n"
            "  affection.py add <user_id> <rule_key> [reason]\n"
            "  affection.py get <user_id>\n"
            "  affection.py detail <user_id>\n"
            "  affection.py brief <user_id> [hours]\n"
            "  affection.py init <user_id> <score>\n"
            "  affection.py rules\n"
            "  affection.py status"
        )
        return None


if __name__ == "__main__":
    result = _parse_args()
    if result is None:
        exit(1)
