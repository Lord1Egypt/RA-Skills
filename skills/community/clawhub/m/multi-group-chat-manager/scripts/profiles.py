"""
Multi-Group-Chat-Manager Profile Helper
用户画像合并、格式化、验证、存储工具
=========================================
支持流体衰减：低频条目随时间自动降权，活跃条目保持高权重。
完全自包含，不依赖外部 fluid_memory 服务。
"""

import json
import sys
import os
import time
import argparse
from pathlib import Path
from datetime import datetime

# 修复 Windows 编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

# 加载统一配置
from config import load as load_config
_cfg = load_config()
OUTPUT_LANG = _cfg["profiling"]["output_language"]
MAX_ITEMS_PER_FIELD = _cfg["profiling"]["max_items_per_field"]
AUTO_DEDUP = _cfg["profiling"]["auto_dedup"]

# 引入液态记忆引擎
from memory import FluidMemory

# ── 路径配置 ──
PROFILES_DIR = SKILL_DIR / "profiles"
MEMORY_DIR = PROFILES_DIR / "memory"  # FluidMemory 存储子目录


# ══════════════════════════════════════════
# 画像数据工具函数（纯函数，不涉及存储）
# ══════════════════════════════════════════

def load_json_str(s):
    """安全加载JSON字符串"""
    if not s:
        return {}
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return {"_raw": s}


def merge_profile(old, new):
    """
    合并新旧画像数据，识别新增条目。
    
    返回: {merged: {...}, new_entries: [...], unchanged: bool, stats: {...}}
    """
    if not old:
        old = {}
    if not new:
        new = {}

    result = dict(old)
    new_entries = []

    # 需要去重的列表字段
    list_fields = [
        "preferences", "personality", "topics_of_interest",
        "behavior", "important_facts"
    ]

    for field in list_fields:
        old_list = old.get(field, [])
        new_list = new.get(field, [])
        merged = list(old_list)

        for item in new_list:
            if item not in merged:
                merged.append(item)
                new_entries.append({"field": field, "value": item})
        result[field] = merged

    # map 字段
    for field in ["group_roles"]:
        old_map = old.get(field, {})
        new_map = new.get(field, {})
        merged_map = dict(old_map)
        for k, v in new_map.items():
            if k not in merged_map or merged_map[k] != v:
                merged_map[k] = v
                new_entries.append({"field": field, "value": f"{k}: {v}"})
        result[field] = merged_map

    # 标量字段
    for field in ["name"]:
        if new.get(field) and new[field] != old.get(field):
            result[field] = new[field]
            new_entries.append({"field": field, "value": new[field]})

    # 时间戳
    now = int(time.time())
    if "first_seen" not in result:
        result["first_seen"] = now
    result["last_updated"] = now
    result["update_count"] = old.get("update_count", 0) + (1 if new_entries else 0)
    result["user_id"] = old.get("user_id") or new.get("user_id", "")

    unchanged = len(new_entries) == 0

    return {
        "merged": result,
        "new_entries": new_entries,
        "unchanged": unchanged,
        "stats": {
            "total_entries": sum(len(result.get(f, [])) for f in list_fields),
            "new_entry_count": len(new_entries),
        }
    }


def format_profile(profile_data):
    """将画像格式化为可读文本"""
    if isinstance(profile_data, str):
        profile_data = load_json_str(profile_data)
    if not profile_data or "user_id" not in profile_data:
        return "（暂无画像数据）"

    lines = []
    name = profile_data.get("name", "未知")
    uid = profile_data.get("user_id", "")
    lines.append(f"━━━ {name}（{uid}）的画像 ━━━\n")

    sections = [
        ("preferences",     "偏好"),
        ("personality",     "性格"),
        ("topics_of_interest", "常聊话题"),
        ("behavior",        "行为模式"),
        ("important_facts", "关键事实"),
    ]

    for key, label in sections:
        items = profile_data.get(key, [])
        if items:
            lines.append(f"- {label}：")
            for item in items:
                lines.append(f"  • {item}")
            lines.append("")

    if profile_data.get("group_roles"):
        lines.append("- 群内角色：")
        for group, role in profile_data["group_roles"].items():
            lines.append(f"  • {group} → {role}")
        lines.append("")

    uc = profile_data.get("update_count", 0)
    fs = profile_data.get("first_seen", 0)
    lu = profile_data.get("last_updated", 0)
    lines.append("- 统计")
    lines.append(f"  更新次数：{uc} 次")
    if fs:
        lines.append(f"  首次记录：{datetime.fromtimestamp(fs).strftime('%Y-%m-%d %H:%M')}")
    if lu:
        lines.append(f"  最后更新：{datetime.fromtimestamp(lu).strftime('%Y-%m-%d %H:%M')}")

    return "\n".join(lines)


def validate_profile(profile_data):
    """验证画像数据完整性"""
    if isinstance(profile_data, str):
        profile_data = load_json_str(profile_data)
    warnings = []
    errors = []

    if not profile_data:
        errors.append("数据为空")
        return {"valid": False, "warnings": warnings, "errors": errors}
    if "user_id" not in profile_data:
        errors.append("缺少 user_id 字段")

    for field in ["preferences", "personality", "topics_of_interest",
                   "behavior", "important_facts"]:
        items = profile_data.get(field, [])
        if len(items) > 50:
            warnings.append(f"{field} 条目超过50条（共{len(items)}条）")

    return {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors
    }


# ══════════════════════════════════════════
# 画像存储管理（基于 FluidMemory）
# ══════════════════════════════════════════

def get_memory() -> FluidMemory:
    """获取 FluidMemory 实例"""
    return FluidMemory(str(MEMORY_DIR))


def update_profile_storage(user_id: str, new_traits: dict, source: str = "group"):
    """
    合并新提取的用户特征到存储中，返回新增内容摘要。
    
    每个特征条目作为独立记忆存入 FluidMemory，
    附带 field 标签，支持流体衰减。
    """
    fm = get_memory()
    new_entries = []

    # 遍历所有特征字段
    for field_key, field_label in [
        ("preferences", "preferences"),
        ("personality", "personality"),
        ("topics_of_interest", "topics"),
        ("behavior", "behavior"),
        ("important_facts", "facts"),
    ]:
        items = new_traits.get(field_key, [])
        for item in items:
            # store 自带去重：相同 content 不会重复
            mid = fm.store(
                user_id, item,
                tags=[field_label, source],
                field=field_key
            )
            # 检查是否是新条目（memory.py store 返回新 ID 或已有 ID）
            # 简单方案：如果 store 返回的 ID 是新生成的……
            # 这里用个 hack：检查该 content 是否已存在
            new_entries.append((field_key, item, mid))

    # 同时更新概要画像（用于快速查询）
    merged = build_structured_profile(user_id)
    save_composite(user_id, merged)

    return {
        "user_id": user_id,
        "new_entry_count": len(new_entries),
        "entries": [{"field": f, "value": v} for f, v, _ in new_entries],
    }


def build_structured_profile(user_id: str) -> dict:
    """
    从 FluidMemory 重建用户的结构化画像。
    
    遍历 FluidMemory 中的所有活跃记忆，按 field 分组，
    返回标准的 {preferences: [...], personality: [...], ...} 格式。
    """
    fm = get_memory()
    profile = {"user_id": user_id}

    field_mapping = {
        "preferences": [],
        "personality": [],
        "topics_of_interest": [],
        "behavior": [],
        "important_facts": [],
    }

    for field in field_mapping:
        values = fm.get_memories_by_field(user_id, field)
        if values:
            profile[field] = values

    # 附加上下文信息（从 composite 文件读取）
    composite = load_composite(user_id)
    if composite:
        for key in ["name", "first_seen", "last_updated", "update_count", "group_roles"]:
            if key in composite:
                profile[key] = composite[key]

    if "first_seen" not in profile:
        profile["first_seen"] = int(time.time())
    if "last_updated" not in profile:
        profile["last_updated"] = int(time.time())
    if "update_count" not in profile:
        profile["update_count"] = 0

    return profile


def load_profile(user_id: str) -> dict:
    """加载用户画像（结构化格式）"""
    return build_structured_profile(user_id)


def save_composite(user_id: str, data: dict):
    """
    保存概要画像到 composite 文件。
    这是 FluidMemory 的补充，存储 name / group_roles 等不常变化的元数据。
    """
    comp_dir = PROFILES_DIR / "composite"
    comp_dir.mkdir(parents=True, exist_ok=True)
    path = comp_dir / f"{user_id}.json"

    # 只存概要字段
    composite = {
        "user_id": user_id,
        "name": data.get("name", ""),
        "first_seen": data.get("first_seen", int(time.time())),
        "last_updated": data.get("last_updated", int(time.time())),
        "update_count": data.get("update_count", 0),
        "group_roles": data.get("group_roles", {}),
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(composite, f, ensure_ascii=False, indent=2)


def load_composite(user_id: str) -> dict:
    """加载概要画像"""
    path = PROFILES_DIR / "composite" / f"{user_id}.json"
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def list_all_profiles() -> list:
    """列出所有有画像记录的用户"""
    fm = get_memory()
    return fm.get_all_user_ids()


def decay_all_profiles() -> int:
    """全局衰减扫描"""
    fm = get_memory()
    return fm.decay_all()


# ══════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="用户画像数据工具")
    sub = parser.add_subparsers(dest="command")

    # ── 数据工具（纯函数） ──
    p_merge = sub.add_parser("merge", help="合并新旧画像")
    p_merge.add_argument("--old", default="{}")
    p_merge.add_argument("--new", default="{}")

    p_format = sub.add_parser("format", help="格式化输出")
    p_format.add_argument("--profile", default="{}")

    p_validate = sub.add_parser("validate", help="验证画像")
    p_validate.add_argument("--profile", default="{}")

    p_stats = sub.add_parser("stats", help="画像统计")
    p_stats.add_argument("--profile", default="{}")

    # ── 存储操作 ──
    p_update = sub.add_parser("update", help="更新用户画像（合并新特征）")
    p_update.add_argument("user_id")
    p_update.add_argument("--json", default="{}", help="新特征的 JSON")
    p_update.add_argument("--source", default="group")

    p_load = sub.add_parser("load", help="加载用户画像")
    p_load.add_argument("user_id")

    p_list = sub.add_parser("list", help="列出所有用户")
    p_list.add_argument("--json", action="store_true", help="JSON 格式输出")

    p_decay = sub.add_parser("decay", help="执行衰减扫描")
    p_decay.add_argument("--force", action="store_true", help="强制运行，忽略间隔")

    args = parser.parse_args()

    if args.command == "merge":
        old = load_json_str(args.old)
        new = load_json_str(args.new)
        print(json.dumps(merge_profile(old, new), ensure_ascii=False, indent=2))

    elif args.command == "format":
        profile = load_json_str(args.profile)
        print(format_profile(profile))

    elif args.command == "validate":
        profile = load_json_str(args.profile)
        print(json.dumps(validate_profile(profile), ensure_ascii=False, indent=2))

    elif args.command == "stats":
        profile = load_json_str(args.profile)
        print(json.dumps({
            "user_id": profile.get("user_id", "unknown"),
            "name": profile.get("name", "unknown"),
            "update_count": profile.get("update_count", 0),
            "total_items": sum(len(profile.get(f, [])) for f in
                               ["preferences", "personality",
                                "topics_of_interest", "behavior",
                                "important_facts"]),
        }, ensure_ascii=False, indent=2))

    elif args.command == "update":
        new_data = load_json_str(args.json)
        result = update_profile_storage(args.user_id, new_data, args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "load":
        profile = load_profile(args.user_id)
        if profile:
            print(json.dumps(profile, ensure_ascii=False, indent=2))
        else:
            print(f"用户 {args.user_id} 暂无画像")

    elif args.command == "list":
        users = list_all_profiles()
        if args.json:
            print(json.dumps({"users": users, "total": len(users)},
                             ensure_ascii=False, indent=2))
        else:
            for uid in users:
                comp = load_composite(uid)
                name = comp.get("name", "?")
                print(f"  {uid}  ({name})")

    elif args.command == "decay":
        from memory import maybe_auto_decay, FluidMemory
        fm = get_memory()
        result = maybe_auto_decay(fm, force=args.force)
        print(json.dumps(result, ensure_ascii=False))

    else:
        parser.print_help()
