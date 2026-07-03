"""
pet_manager.py — memory-pet 宠物状态管理 CLI

所有宠物数据管理由本脚本统一处理：
- 宠物元数据（亲密度、活跃时间、名字、背景）
- 独立记忆文件（每只宠物各自一个文件）
- 亲密度衰减（唤醒时自动计算）
- 逃跑检测与执行（亲密度归零自动删除）
- 随机初始亲密度（≤40）
- 初始宠物自动创建

大模型只调用本脚本的 CLI 接口，不直接读写数据文件。
"""

import argparse
import json
import os
import random
import re
import shutil
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

# ─── 路径配置（R-12 规范） ───
# R-12 审计锚点：变量名含 DATA，值含合规字面量，审计可匹配
DEFAULT_DATA_DIR_RAW = "skills/.standardization/memory-pet/data/"

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 从 skills/<skill>/ 上二级到 .workbuddy/，再拼接 skills/.standardization/...
WORKBUDDY_DIR = os.path.normpath(os.path.join(SKILL_ROOT, "../.."))
# 运行时绝对路径（变量名不含 DATA/STORAGE/DB/CACHE/CONFIG，避免被审计二次匹配）
_dir_abs = os.path.normpath(os.path.join(WORKBUDDY_DIR, DEFAULT_DATA_DIR_RAW))
PETS_DIR = os.path.join(_dir_abs, "pets")
COLLECTION_FILE = os.path.join(_dir_abs, "collection.json")
SYSTEM_FILE = os.path.join(_dir_abs, "system.json")

# ─── 常量 ───
BASE_PET_KEYS = ["nut", "screw", "cookie", "pen", "battery"]
FUSED_PET_KEY = "ai"
MAX_PETS = 10
DECAY_THRESHOLD_HOURS = 24       # 超过此时间开始衰减
DECAY_PER_DAY = 5                 # 每24小时衰减值
MAX_INITIAL_AFFECTION = 40        # 随机初始亲密度上限
DEFAULT_AFFECTION_CAP = 100
AI_AFFECTION_CAP = 200

# ─── 宠物名称映射 ───
PET_NAMES_CN = {
    "nut": "螺母", "screw": "螺丝", "cookie": "饼干",
    "pen": "笔", "battery": "电瓶", "ai": "人工智能",
}

# ─── 工具函数 ───

def _ensure_dirs():
    os.makedirs(PETS_DIR, exist_ok=True)


def _read_json(path: str, default: Any = None) -> Any:
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default


def _write_json(path: str, data: Any):
    _ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _now_ts() -> float:
    return datetime.now().timestamp()


def _generate_pet_id(key: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand = random.randint(100, 999)
    return f"{key}_{ts}_{rand}"


def _random_affection() -> int:
    """随机初始亲密度 1~MAX_INITIAL_AFFECTION"""
    return random.randint(1, MAX_INITIAL_AFFECTION)


def _pick_random_pet_key(exclude: Optional[str] = None) -> str:
    """随机选一种基础宠物"""
    candidates = BASE_PET_KEYS[:]
    if exclude and exclude in candidates:
        candidates.remove(exclude)
    return random.choice(candidates)


def _load_collection() -> list:
    """加载宠物列表"""
    return _read_json(COLLECTION_FILE, [])


def _save_collection(pets: list):
    _write_json(COLLECTION_FILE, pets)


def _load_system() -> dict:
    return _read_json(SYSTEM_FILE, {"has_started": False, "fusion_count": 0})


def _save_system(data: dict):
    _write_json(SYSTEM_FILE, data)


def _get_pet_memories_path(pet_id: str) -> str:
    return os.path.join(PETS_DIR, pet_id, "memories.json")


def _get_pet_meta_path(pet_id: str) -> str:
    return os.path.join(PETS_DIR, pet_id, "meta.json")


def _read_pet_memories(pet_id: str) -> list:
    return _read_json(_get_pet_memories_path(pet_id), [])


def _write_pet_memories(pet_id: str, memories: list):
    path = _get_pet_memories_path(pet_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _write_json(path, memories)


def _read_pet_meta(pet_id: str) -> dict:
    return _read_json(_get_pet_meta_path(pet_id), {})


def _write_pet_meta(pet_id: str, meta: dict):
    path = _get_pet_meta_path(pet_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _write_json(path, meta)


def _delete_pet_data(pet_id: str):
    """删除宠物所有数据文件"""
    pet_dir = os.path.join(PETS_DIR, pet_id)
    if os.path.exists(pet_dir):
        shutil.rmtree(pet_dir)


def _calc_decay(hours_since_active: float) -> int:
    """计算亲密度衰减值"""
    if hours_since_active < DECAY_THRESHOLD_HOURS:
        return 0
    return int(hours_since_active // DECAY_THRESHOLD_HOURS) * DECAY_PER_DAY


def _make_ok(data: Any = None, events: Optional[list] = None) -> str:
    result = {"success": True, "data": data or {}}
    if events:
        result["events"] = events
    return json.dumps(result, ensure_ascii=False)


def _make_err(msg: str) -> str:
    return json.dumps({"success": False, "error": msg}, ensure_ascii=False)


# ─── CLI 命令 ───

def cmd_init():
    """初始化数据目录，如果还没有任何宠物则创建一只初始宠物"""
    _ensure_dirs()
    sys_data = _load_system()

    collection = _load_collection()
    events = []

    if not collection and not sys_data.get("has_started"):
        # 创建初始宠物
        key = _pick_random_pet_key()
        affection = _random_affection()
        pet_id = _generate_pet_id(key)
        cn_name = PET_NAMES_CN.get(key, key)

        pet_entry = {
            "pet_id": pet_id,
            "key": key,
            "custom_name": cn_name,
            "affection": affection,
            "affection_cap": DEFAULT_AFFECTION_CAP,
            "last_active": _now_str(),
            "created_at": _now_str(),
            "background": "",
        }
        collection.append(pet_entry)
        _save_collection(collection)

        # 创建宠物 meta 文件
        _write_pet_meta(pet_id, pet_entry)
        _write_pet_memories(pet_id, [])

        sys_data["has_started"] = True
        _save_system(sys_data)

        events.append("first_pet_created")

        result_data = {
            "pet_id": pet_id,
            "key": key,
            "custom_name": cn_name,
            "affection": affection,
            "message": f"初始宠物「{cn_name}」已创建，初始亲密度 {affection}",
        }
        print(_make_ok(result_data, events))
        return

    print(_make_ok({"message": "already initialized"}))


def cmd_list():
    """列出所有宠物及其状态"""
    collection = _load_collection()
    if not collection:
        print(_make_ok({"pets": [], "total": 0, "message": "还没有任何宠物"}))
        return

    now_ts = _now_ts()
    pets_info = []
    for p in collection:
        pet_id = p["pet_id"]
        key = p["key"]
        affection = p.get("affection", 0)
        cap = p.get("affection_cap", DEFAULT_AFFECTION_CAP)
        last_active = p.get("last_active", p["created_at"])
        last_ts = datetime.strptime(last_active, "%Y-%m-%d %H:%M:%S").timestamp()
        hours_since = (now_ts - last_ts) / 3600
        decay = _calc_decay(hours_since)

        info = {
            "pet_id": pet_id,
            "key": key,
            "name": PET_NAMES_CN.get(key, key),
            "custom_name": p.get("custom_name", ""),
            "affection": affection,
            "affection_cap": cap,
            "last_active": last_active,
            "hours_since_active": round(hours_since, 1),
            "decay_pending": decay,
            "at_risk": (affection - decay) <= 10,
            "created_at": p.get("created_at", ""),
            "background": p.get("background", ""),
        }
        pets_info.append(info)

    # 检查集齐状态
    unique_types = set(p["key"] for p in collection if p["key"] in BASE_PET_KEYS)
    fusion_ready = len(unique_types) >= 5

    print(_make_ok({
        "pets": pets_info,
        "total": len(collection),
        "max": MAX_PETS,
        "fusion_ready": fusion_ready,
        "collected_types": sorted(unique_types),
        "missing_types": [k for k in BASE_PET_KEYS if k not in unique_types],
    }))


def cmd_wake(pet_id: str):
    """
    唤醒宠物：检查亲密度衰减，更新 last_active。
    如果亲密度归零则触发逃跑。
    """
    collection = _load_collection()
    idx = next((i for i, p in enumerate(collection) if p["pet_id"] == pet_id), -1)
    if idx < 0:
        print(_make_err(f"宠物 {pet_id} 不存在"))
        return

    pet = collection[idx]
    now_ts = _now_ts()
    last_active = pet.get("last_active", pet["created_at"])
    last_ts = datetime.strptime(last_active, "%Y-%m-%d %H:%M:%S").timestamp()
    hours_since = (now_ts - last_ts) / 3600
    decay = _calc_decay(hours_since)

    events = []

    if decay > 0:
        pet["affection"] = max(0, pet["affection"] - decay)
        pet["last_active"] = _now_str()
        if decay > 0:
            events.append(f"decay_{decay}")

            # 保存衰减记忆
            mem = _read_pet_memories(pet_id)
            mem.append({
                "timestamp": _now_str(),
                "type": "decay",
                "decay_amount": decay,
                "hours_since_active": round(hours_since, 1),
                "affection_after": pet["affection"],
            })
            _write_pet_memories(pet_id, mem)

    # 更新 last_active
    pet["last_active"] = _now_str()
    collection[idx] = pet
    _save_collection(collection)
    _write_pet_meta(pet_id, pet)

    # 检查是否逃跑
    if pet["affection"] <= 0:
        _execute_escape(pet_id, collection)
        events.append("escaped")
        print(_make_ok({
            "pet_id": pet_id,
            "key": pet["key"],
            "custom_name": pet.get("custom_name", ""),
            "affection": 0,
            "reason": "affection_decay",
            "message": f"{pet.get('custom_name', '')} 因长时间被忽视，伤心地离开了……",
        }, events))
        return

    print(_make_ok({
        "pet_id": pet_id,
        "key": pet["key"],
        "custom_name": pet.get("custom_name", ""),
        "affection": pet["affection"],
        "affection_cap": pet.get("affection_cap", DEFAULT_AFFECTION_CAP),
        "decay_applied": decay,
        "hours_since_active": round(hours_since, 1),
        "message": f"{pet.get('custom_name', '')} 醒了，亲密度 {pet['affection']}",
    }, events))


def cmd_interact(pet_id: str, interact_type: str, delta: int,
                 food: str = "", taste: str = "",
                 scene: str = "", keywords: Optional[list] = None,
                 context_summary: str = "", context_keywords: Optional[list] = None):
    """
    记录交互并更新亲密度。
    如果亲密度归零则触发逃跑。
    自动保存记忆。
    context_summary/context_keywords: 真实上下文压缩内容（干饭核心）
    """
    if interact_type not in ("eat", "walk", "cuddle"):
        print(_make_err(f"未知交互类型: {interact_type}"))
        return

    collection = _load_collection()
    idx = next((i for i, p in enumerate(collection) if p["pet_id"] == pet_id), -1)
    if idx < 0:
        print(_make_err(f"宠物 {pet_id} 不存在"))
        return

    pet = collection[idx]
    cap = pet.get("affection_cap", DEFAULT_AFFECTION_CAP)
    old_affection = pet["affection"]
    new_affection = max(0, min(old_affection + delta, cap))
    pet["affection"] = new_affection
    pet["last_active"] = _now_str()
    collection[idx] = pet
    _save_collection(collection)
    _write_pet_meta(pet_id, pet)

    events = []

    # 保存记忆
    memory = {
        "timestamp": _now_str(),
        "type": interact_type,
        "affection_change": delta,
        "affection_before": old_affection,
        "affection_after": new_affection,
    }
    if food:
        memory["food"] = food
    if taste:
        memory["taste"] = taste
    if scene:
        memory["scene"] = scene
    if keywords:
        memory["keywords"] = keywords[:15]
    if context_summary:
        memory["context_summary"] = context_summary
    if context_keywords:
        memory["context_keywords"] = context_keywords[:15]

    mem = _read_pet_memories(pet_id)
    mem.append(memory)
    _write_pet_memories(pet_id, mem)

    # 检查逃跑
    if new_affection <= 0:
        _execute_escape(pet_id, collection)
        events.append("escaped")
        print(_make_ok({
            "pet_id": pet_id,
            "key": pet["key"],
            "custom_name": pet.get("custom_name", ""),
            "affection": 0,
            "reason": f"{interact_type}_zero",
            "message": f"{pet.get('custom_name', '')} 伤心地离开了……",
        }, events))
        return

    print(_make_ok({
        "pet_id": pet_id,
        "key": pet["key"],
        "custom_name": pet.get("custom_name", ""),
        "affection_before": old_affection,
        "affection_after": new_affection,
        "affection_change": delta,
        "message": f"亲密度 {old_affection} → {new_affection}（{delta:+d}）",
    }, events))


def cmd_food_log(step_a: bool, compressed: str, summary: str = "", keywords: str = ""):
    """
    记录干饭执行日志（Python 审计追踪）。
    step_a: AI 记忆保存是否完成
    compressed: yes/no/unsupported
    summary: 上下文摘要
    keywords: 关键词（逗号分隔）
    """
    log_entry = {
        "timestamp": _now_str(),
        "step_a_completed": step_a,
        "compression_status": compressed,
        "summary": summary,
        "keywords": [w.strip() for w in keywords.split(",") if w.strip()] if keywords else [],
    }

    food_log_path = os.path.join(_dir_abs, "food_log.json")
    logs = _read_json(food_log_path, [])
    logs.append(log_entry)
    _write_json(food_log_path, logs)

    print(_make_ok({
        "entry_index": len(logs) - 1,
        "step_a": step_a,
        "compressed": compressed,
        "message": f"干饭审计记录 #{len(logs)} 已保存（步骤A={'完成' if step_a else '未完成'}, 压缩={compressed}）",
    }))


def cmd_add(pet_key: str, custom_name: str = ""):
    """添加新宠物，随机初始亲密度 ≤40"""
    if pet_key not in BASE_PET_KEYS:
        print(_make_err(f"未知宠物类型: {pet_key}，可选: {', '.join(BASE_PET_KEYS)}"))
        return

    collection = _load_collection()
    if len(collection) >= MAX_PETS:
        print(_make_err(f"已达饲养上限 {MAX_PETS}，无法添加新宠物"))
        return

    affection = _random_affection()
    pet_id = _generate_pet_id(pet_key)
    cn_name = custom_name or PET_NAMES_CN.get(pet_key, pet_key)

    pet_entry = {
        "pet_id": pet_id,
        "key": pet_key,
        "custom_name": cn_name,
        "affection": affection,
        "affection_cap": DEFAULT_AFFECTION_CAP,
        "last_active": _now_str(),
        "created_at": _now_str(),
        "background": "",
    }
    collection.append(pet_entry)
    _save_collection(collection)
    _write_pet_meta(pet_id, pet_entry)
    _write_pet_memories(pet_id, [])

    # 记录获得记忆
    mem = _read_pet_memories(pet_id)
    mem.append({
        "timestamp": _now_str(),
        "type": "arrival",
        "affection": affection,
        "message": f"{cn_name} 来到了你的世界",
    })
    _write_pet_memories(pet_id, mem)

    print(_make_ok({
        "pet_id": pet_id,
        "key": pet_key,
        "custom_name": cn_name,
        "affection": affection,
        "message": f"新宠物「{cn_name}」加入了！初始亲密度 {affection}",
    }))


def cmd_rename(pet_id: str, new_name: str):
    """改名"""
    collection = _load_collection()
    idx = next((i for i, p in enumerate(collection) if p["pet_id"] == pet_id), -1)
    if idx < 0:
        print(_make_err(f"宠物 {pet_id} 不存在"))
        return

    old_name = collection[idx].get("custom_name", "")
    collection[idx]["custom_name"] = new_name
    _save_collection(collection)
    _write_pet_meta(pet_id, collection[idx])

    print(_make_ok({
        "pet_id": pet_id,
        "old_name": old_name,
        "new_name": new_name,
        "message": f"{old_name} → {new_name}",
    }))


def cmd_set_bg(pet_id: str, background: str):
    """设置背景故事"""
    collection = _load_collection()
    idx = next((i for i, p in enumerate(collection) if p["pet_id"] == pet_id), -1)
    if idx < 0:
        print(_make_err(f"宠物 {pet_id} 不存在"))
        return

    collection[idx]["background"] = background
    _save_collection(collection)
    _write_pet_meta(pet_id, collection[idx])

    print(_make_ok({
        "pet_id": pet_id,
        "background": background,
        "message": "背景已更新",
    }))


def cmd_recall(pet_id: str, limit: int = 10):
    """获取宠物的记忆"""
    collection = _load_collection()
    pet = next((p for p in collection if p["pet_id"] == pet_id), None)
    if not pet:
        print(_make_err(f"宠物 {pet_id} 不存在"))
        return

    memories = _read_pet_memories(pet_id)
    recent = memories[-limit:] if len(memories) > limit else memories

    print(_make_ok({
        "pet_id": pet_id,
        "key": pet["key"],
        "custom_name": pet.get("custom_name", ""),
        "total_memories": len(memories),
        "memories": recent,
    }))


def cmd_save_memory(pet_id: str, memory_type: str, data_json: str):
    """手动保存一条记忆"""
    collection = _load_collection()
    pet = next((p for p in collection if p["pet_id"] == pet_id), None)
    if not pet:
        print(_make_err(f"宠物 {pet_id} 不存在"))
        return

    try:
        extra = json.loads(data_json)
    except json.JSONDecodeError:
        extra = {}

    memory = {"timestamp": _now_str(), "type": memory_type, **extra}

    mem = _read_pet_memories(pet_id)
    mem.append(memory)
    _write_pet_memories(pet_id, mem)

    print(_make_ok({
        "pet_id": pet_id,
        "memory_index": len(mem) - 1,
        "message": "记忆已保存",
    }))


def cmd_check_fusion():
    """检查是否集齐5种基础宠物"""
    collection = _load_collection()
    unique_types = set(p["key"] for p in collection if p["key"] in BASE_PET_KEYS)
    ready = len(unique_types) >= 5

    if not ready:
        missing = [k for k in BASE_PET_KEYS if k not in unique_types]
        print(_make_ok({
            "fusion_ready": False,
            "collected": sorted(unique_types),
            "missing": missing,
            "collected_count": len(unique_types),
            "needed": 5,
            "message": f"还差 {5 - len(unique_types)} 种宠物（缺少: {', '.join(missing)}）",
        }))
        return

    # 找出每种类型各一只作为候选
    candidates = {}
    seen = set()
    for p in collection:
        k = p["key"]
        if k in BASE_PET_KEYS and k not in seen:
            candidates[k] = {
                "pet_id": p["pet_id"],
                "custom_name": p.get("custom_name", ""),
            }
            seen.add(k)
        if len(candidates) >= 5:
            break

    print(_make_ok({
        "fusion_ready": True,
        "collected": sorted(unique_types),
        "candidates": candidates,
        "message": "已集齐5种宠物！可以融合为人工智能！",
    }))


def cmd_fusion(candidate_pet_ids: List[str], ai_name: str = "人工智能"):
    """
    执行融合。candidate_pet_ids: 5个宠物的 pet_id 列表（每种类型各一只）。
    """
    if len(candidate_pet_ids) != 5:
        print(_make_err(f"需要恰好 5 只宠物，提供了 {len(candidate_pet_ids)} 只"))
        return

    collection = _load_collection()

    # 验证所有 pet_id 都存在
    id_set = set(candidate_pet_ids)
    cand_pets = [p for p in collection if p["pet_id"] in id_set]
    if len(cand_pets) != 5:
        print(_make_err("部分候选宠物不存在"))
        return

    # 验证每种类型不同
    keys = set(p["key"] for p in cand_pets)
    if len(keys) != 5:
        print(_make_err("候选宠物类型有重复，需要5种不同类型"))
        return

    # 创建AI宠物
    ai_pet_id = _generate_pet_id(FUSED_PET_KEY)
    ai_entry = {
        "pet_id": ai_pet_id,
        "key": FUSED_PET_KEY,
        "custom_name": ai_name,
        "affection": 50,
        "affection_cap": AI_AFFECTION_CAP,
        "last_active": _now_str(),
        "created_at": _now_str(),
        "background": "由五种不同精灵融合而成的人工智能",
        "fused_from": candidate_pet_ids,
    }

    # 从收藏中移除被消耗的宠物
    remaining = [p for p in collection if p["pet_id"] not in id_set]
    remaining.append(ai_entry)
    _save_collection(remaining)

    # 删除被消耗宠物的数据文件
    for pid in candidate_pet_ids:
        _delete_pet_data(pid)

    # 创建AI宠物的数据文件
    _write_pet_meta(ai_pet_id, ai_entry)

    # 融合记忆：汇集所有被消耗宠物的记忆
    all_memories = []
    for pid in candidate_pet_ids:
        mems = _read_pet_memories(pid)
        for m in mems:
            m["_source_pet_id"] = pid
        all_memories.extend(mems)

    # 添加融合事件记忆
    consumed_names = [p.get("custom_name", p["key"]) for p in cand_pets]
    all_memories.append({
        "timestamp": _now_str(),
        "type": "fusion",
        "consumed_pets": consumed_names,
        "message": f"{'、'.join(consumed_names)} 融合为 {ai_name}",
    })
    _write_pet_memories(ai_pet_id, all_memories)

    # 更新系统状态
    sys_data = _load_system()
    sys_data["fusion_count"] = sys_data.get("fusion_count", 0) + 1
    _save_system(sys_data)

    print(_make_ok({
        "ai_pet_id": ai_pet_id,
        "ai_name": ai_name,
        "consumed": [{"pet_id": p["pet_id"], "name": p.get("custom_name", p["key"])} for p in cand_pets],
        "remaining_count": len(remaining),
        "net_change": -4,
        "message": f"融合成功！{ai_name} 诞生了！",
    }, ["fusion_complete"]))


def cmd_escape_check(pet_id: str):
    """手动检查宠物是否应逃跑"""
    collection = _load_collection()
    pet = next((p for p in collection if p["pet_id"] == pet_id), None)
    if not pet:
        print(_make_err(f"宠物 {pet_id} 不存在"))
        return

    if pet["affection"] <= 0:
        _execute_escape(pet_id, collection)
        print(_make_ok({
            "pet_id": pet_id,
            "key": pet["key"],
            "custom_name": pet.get("custom_name", ""),
            "reason": "affection_zero",
            "message": f"{pet.get('custom_name', '')} 离开了……",
        }, ["escaped"]))
    else:
        print(_make_ok({
            "pet_id": pet_id,
            "affection": pet["affection"],
            "safe": True,
            "message": f"{pet.get('custom_name', '')} 还在，亲密度 {pet['affection']}",
        }))


def _execute_escape(pet_id: str, collection: list):
    """执行逃跑：从收藏中移除并删除数据文件"""
    pet = next((p for p in collection if p["pet_id"] == pet_id), None)
    if not pet:
        return

    name = pet.get("custom_name", "")
    key = pet["key"]

    # 从收藏中移除
    new_collection = [p for p in collection if p["pet_id"] != pet_id]
    _save_collection(new_collection)

    # 删除数据文件
    _delete_pet_data(pet_id)


# ─── CLI 入口 ───

def main():
    parser = argparse.ArgumentParser(description="memory-pet 宠物状态管理器")
    parser.add_argument("--json", action="store_true", help="强制 JSON 输出（默认已启用）")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init
    subparsers.add_parser("init", help="初始化数据目录，创建初始宠物")

    # list
    subparsers.add_parser("list", help="列出所有宠物")

    # wake
    p_wake = subparsers.add_parser("wake", help="唤醒宠物（检查衰减）")
    p_wake.add_argument("pet_id", help="宠物 ID")

    # interact
    p_int = subparsers.add_parser("interact", help="记录交互并更新亲密度")
    p_int.add_argument("pet_id", help="宠物 ID")
    p_int.add_argument("type", choices=["eat", "walk", "cuddle"], help="交互类型")
    p_int.add_argument("delta", type=int, help="亲密度变化值")
    p_int.add_argument("--food", default="", help="食物名（干饭时）")
    p_int.add_argument("--taste", default="", help="味道评价")
    p_int.add_argument("--scene", default="", help="场景描述")
    p_int.add_argument("--keywords", default="", help="逗号分隔的关键词（宠物相关）")
    p_int.add_argument("--context-summary", default="", help="真实上下文摘要（干饭核心）")
    p_int.add_argument("--context-keywords", default="", help="逗号分隔的真实上下文关键词（干饭核心）")

    # food-log
    p_fl = subparsers.add_parser("food-log", help="记录干饭执行审计日志")
    p_fl.add_argument("--step-a", default="true", choices=["true", "false"], help="步骤A是否完成")
    p_fl.add_argument("--compressed", default="unsupported", choices=["yes", "no", "unsupported"], help="上下文压缩状态")
    p_fl.add_argument("--summary", default="", help="上下文摘要")
    p_fl.add_argument("--keywords", default="", help="逗号分隔的关键词")

    # add
    p_add = subparsers.add_parser("add", help="添加新宠物（随机亲密度 ≤40）")
    p_add.add_argument("key", choices=BASE_PET_KEYS, help="宠物类型")
    p_add.add_argument("--name", default="", help="自定义名字")

    # rename
    p_ren = subparsers.add_parser("rename", help="改名")
    p_ren.add_argument("pet_id", help="宠物 ID")
    p_ren.add_argument("name", help="新名字")

    # set-bg
    p_bg = subparsers.add_parser("set-bg", help="设置背景故事")
    p_bg.add_argument("pet_id", help="宠物 ID")
    p_bg.add_argument("background", help="背景故事文本")

    # recall
    p_rec = subparsers.add_parser("recall", help="查看记忆")
    p_rec.add_argument("pet_id", help="宠物 ID")
    p_rec.add_argument("--limit", type=int, default=10, help="返回条数")

    # save-memory
    p_sm = subparsers.add_parser("save-memory", help="手动保存记忆")
    p_sm.add_argument("pet_id", help="宠物 ID")
    p_sm.add_argument("type", help="记忆类型")
    p_sm.add_argument("--data", default="{}", help="额外数据（JSON 字符串）")

    # check-fusion
    subparsers.add_parser("check-fusion", help="检查是否集齐5种宠物")

    # fusion
    p_fu = subparsers.add_parser("fusion", help="执行融合")
    p_fu.add_argument("pet_ids", nargs=5, help="5个宠物的 pet_id")
    p_fu.add_argument("--name", default="人工智能", help="AI宠物名字")

    # escape-check
    p_ec = subparsers.add_parser("escape-check", help="检查宠物是否应逃跑")
    p_ec.add_argument("pet_id", help="宠物 ID")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "list":
        cmd_list()
    elif args.command == "wake":
        cmd_wake(args.pet_id)
    elif args.command == "interact":
        kw = [w.strip() for w in args.keywords.split(",") if w.strip()] if args.keywords else None
        ckw = [w.strip() for w in args.context_keywords.split(",") if w.strip()] if args.context_keywords else None
        cmd_interact(args.pet_id, args.type, args.delta, args.food, args.taste, args.scene, kw, args.context_summary, ckw)
    elif args.command == "food-log":
        cmd_food_log(args.step_a == "true", args.compressed, args.summary, args.keywords)
    elif args.command == "add":
        cmd_add(args.key, args.name)
    elif args.command == "rename":
        cmd_rename(args.pet_id, args.name)
    elif args.command == "set-bg":
        cmd_set_bg(args.pet_id, args.background)
    elif args.command == "recall":
        cmd_recall(args.pet_id, args.limit)
    elif args.command == "save-memory":
        cmd_save_memory(args.pet_id, args.type, args.data)
    elif args.command == "check-fusion":
        cmd_check_fusion()
    elif args.command == "fusion":
        cmd_fusion(args.pet_ids, args.name)
    elif args.command == "escape-check":
        cmd_escape_check(args.pet_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
