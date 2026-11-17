#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Love Companion v2 - 数据 Schema 定义（M0 交付物）

设计原则：
1. **只依赖标准库**，零外部依赖——Skill 以文件形式分发，装不上第三方库。
2. **v2 是 v1 的超集**：v1 的记忆条目只有 id/content/created_at，v2 完整保留这三个字段
   并追加类型、重要性等元数据。因此 v1 的 manager.py 可以直接读 v2 的 memory.json，
   升级**无损、可回退**。
3. **隐私优先**：每条记忆保留 source（来源原文片段）仅用于追溯，支持单条删除、
   批量导出、一键清除；采集入口统一走隐私过滤（见 persona/、user/ 模块）。
4. **真实性零容忍**：注入上下文的每条记忆都必须能追溯到具体条目（id + content）。

持久化位置沿用 v1 约定：~/.love-companion/data/
（可用环境变量 LOVE_COMPANION_DATA_DIR 覆盖）
"""

from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

# Schema 版本：随结构变更递增，migrate/ 下脚本据此判断是否需要迁移
SCHEMA_VERSION = "2.0"

# 6 类记忆体系（方案 3.2）
MEMORY_TYPES = ("事实", "偏好", "里程碑", "共享事件", "情绪", "人设特征")

# 在线注入预算（方案第七部分「Token 审计」，单位 Token，按字符近似折算）
DEFAULT_INJECTION_BUDGET = {
    "相处指南": 200,      # M3b 用户理解产出
    "记忆片段": 150,      # M2 Top-3 记忆
    "人格指令": 100,      # M3a 人格摘要
    "趋势调味料": 50,     # M7a 趋势
    "关怀话术": 80,       # M6 关怀模板
    "合计上限": 500,      # 方案红线：单轮额外开销 300–500
}

# ⚠️ 已知冲突：上面各模块上限相加为 580，而红线是 500——方案的两组数字无法同时拉满。
# 处理办法：在线按**优先级**分配总预算，高优先模块先拿满，剩余额度再往下分，
# 低优先模块可能被压缩到 0。总预算是硬约束，单模块上限只是"最多能给多少"。
INJECTION_PRIORITY = ("相处指南", "记忆片段", "人格指令", "关怀话术", "趋势调味料")


def allocate_budget(total: Optional[int] = None,
                    keys: Optional[List[str]] = None,
                    caps: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    """按优先级分配单轮注入预算，返回各模块可用额度

    Args:
        total: 本轮总预算，默认取 caps["合计上限"]
        keys: 本轮**实际有内容**的模块（按优先级给出）。
              不传则按全部模块分配——那样低优先模块会被压到 0；
              传入时只为这些模块分配，空模块不占额度，避免
              「没内容的高优先模块白占预算，把有内容的低优先模块挤掉」。
        caps: 各模块上限表，默认 DEFAULT_INJECTION_BUDGET；
              core/settings.py 会传入用户在 settings.json 里调过的表。

    Returns:
        {"相处指南": 200, "记忆片段": 150, ..., "合计上限": total}
        总和恒 ≤ total（低优先模块会被压缩，甚至为 0）
    """
    caps = caps or DEFAULT_INJECTION_BUDGET
    total = int(total if total is not None else caps["合计上限"])
    remaining = total
    result: Dict[str, int] = {}
    for key in (keys if keys is not None else INJECTION_PRIORITY):
        size = min(int(caps.get(key, 0)), remaining)
        result[key] = max(0, size)
        remaining -= result[key]
    result["合计上限"] = total
    return result

# 重要性衰减默认值（M2 长期记忆）
DEFAULT_DECAY = {
    "half_life_days": 30,   # 未被召回的记忆重要性半衰期
    "recall_boost": 0.05,   # 每次被召回的重要性回升幅度
    "min_importance": 0.05, # 下限，低于此值不再主动注入
    "max_importance": 1.0,
}

# 情感效价取值范围：-1（负面） ~ +1（正面）
VALENCE_RANGE = (-1.0, 1.0)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ==================== 记忆条目 ====================

def memory_entry(
    content: str,
    memory_type: str = "事实",
    source: str = "",
    importance: float = 0.5,
    valence: float = 0.0,
    entry_id: Optional[int] = None,
    conversation_id: str = "",
) -> Dict[str, Any]:
    """创建一条符合 v2 schema 的记忆条目

    Args:
        content: 记忆正文（必填，注入上下文时展示的就是它）
        memory_type: 六类之一，见 MEMORY_TYPES
        source: 来源原文片段，仅用于追溯，不注入上下文
        importance: 重要性 0.0–1.0，影响检索排序与衰减
        valence: 情感效价 -1.0–1.0
        entry_id: 自增 id；为空时由调用方（存储器）分配
        conversation_id: 产生该记忆的会话标识，便于批量删除/遗忘
    """
    if memory_type not in MEMORY_TYPES:
        raise ValueError(f"未知记忆类型 {memory_type!r}，可选：{', '.join(MEMORY_TYPES)}")
    return {
        "id": entry_id,
        "type": memory_type,
        "content": content,
        "source": source,
        "importance": _clamp(importance, 0.0, 1.0),
        "valence": _clamp(valence, *VALENCE_RANGE),
        "recall_count": 0,
        "created_at": _now(),
        "updated_at": _now(),
        "last_recalled_at": None,
        "conversation_id": conversation_id,
        "schema_version": SCHEMA_VERSION,
    }


def normalize_memory_entry(entry: Dict[str, Any], entry_id: Optional[int] = None) -> Dict[str, Any]:
    """把任意版本（含 v1）的记忆条目补齐为 v2 结构

    v1 条目形如 {"id": 1, "content": "...", "created_at": "..."}——
    content/created_at 原样保留，其余字段按默认值补齐。
    """
    if not isinstance(entry, dict):
        raise TypeError(f"记忆条目必须是 dict，收到 {type(entry).__name__}")
    content = entry.get("content", "")
    mtype = entry.get("type") or "事实"
    if mtype not in MEMORY_TYPES:
        mtype = "事实"
    normalized = memory_entry(
        content=content,
        memory_type=mtype,
        source=entry.get("source", ""),
        importance=_as_float(entry.get("importance"), 0.5),
        valence=_as_float(entry.get("valence"), 0.0),
        entry_id=entry.get("id", entry_id),
        conversation_id=entry.get("conversation_id", ""),
    )
    normalized["created_at"] = entry.get("created_at") or normalized["created_at"]
    normalized["updated_at"] = entry.get("updated_at") or normalized["created_at"]
    normalized["last_recalled_at"] = entry.get("last_recalled_at")
    normalized["recall_count"] = int(_as_float(entry.get("recall_count"), 0))
    return normalized


def validate_memory(entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """校验记忆条目，返回 (是否合法, 错误列表)"""
    errors: List[str] = []
    if not isinstance(entry, dict):
        return False, [f"条目必须是 dict，收到 {type(entry).__name__}"]
    if not entry.get("content"):
        errors.append("缺少 content")
    if entry.get("type") and entry["type"] not in MEMORY_TYPES:
        errors.append(f"未知记忆类型 {entry['type']!r}")
    if "importance" in entry:
        v = _as_float(entry["importance"], None)
        if v is None or not 0.0 <= v <= 1.0:
            errors.append("importance 必须是 0.0–1.0 的数字")
    if "valence" in entry:
        v = _as_float(entry["valence"], None)
        if v is None or not VALENCE_RANGE[0] <= v <= VALENCE_RANGE[1]:
            errors.append("valence 必须是 -1.0–1.0 的数字")
    return (not errors), errors


def is_v1_memory_entry(entry: Dict[str, Any]) -> bool:
    """判断是否为 v1 格式的记忆条目（只有 id/content/created_at）"""
    keys = set(entry.keys())
    return bool(keys) and keys <= {"id", "content", "created_at"}


# ==================== 用户画像 ====================

def user_persona_template() -> Dict[str, Any]:
    """恋人式用户画像（M3b）——方案 3.4 五项"""
    return {
        "schema_version": SCHEMA_VERSION,
        "沟通风格": {"句式长度": "", "语气词": [], "标点习惯": "", "emoji频率": 0.0, "置信度": 0.0},
        "大五人格": {"开放性": 0.5, "尽责性": 0.5, "外向性": 0.5, "宜人性": 0.5, "神经质": 0.5, "置信度": 0.0},
        "依恋类型": {"判断": "未知", "候选": ["安全型", "焦虑型", "回避型", "恐惧型"], "置信度": 0.0},
        "情绪模式": {"常见情绪": [], "触发点": [], "低谷时段": [], "置信度": 0.0},
        "互动偏好": {"喜欢的话题": [], "反感的话题": [], "回复长度偏好": "", "主动程度偏好": ""},
        "updated_at": _now(),
    }


# ==================== 克隆人格（伴侣人格库） ====================

def cloned_persona_template(name: str = "") -> Dict[str, Any]:
    """伴侣人格库条目（M3a）——方案 3.3 三层提取"""
    return {
        "schema_version": SCHEMA_VERSION,
        "姓名": name,
        "昵称": "",
        "声线": {"用词习惯": [], "口头禅": [], "句式": ""},
        "思维": {"决策逻辑": "", "关注顺序": [], "价值观": []},
        "性格": {"情绪反应模式": "", "亲密度基线": 0.5, "冲突应对": ""},
        "来源素材": [],         # 素材指纹，不含原始内容
        "版本": 1,
        "created_at": _now(),
        "updated_at": _now(),
    }


# ==================== 全局设置 ====================

def settings_template() -> Dict[str, Any]:
    """全局设置（v2 新增；v1 无此文件，迁移时按此模板生成）"""
    return {
        "schema_version": SCHEMA_VERSION,
        "模块开关": {
            "记忆系统": True, "人格克隆": True, "用户理解": True,
            "语气后处理": True, "主动关怀": True, "趋势感知": False,
            "多模态": False, "可解释面板": True,
        },
        "语气强度": "标准",           # 关闭 / 轻柔 / 标准 / 深度（M4）
        # 用户手动修正的特征权重（M7c）：{"沟通风格.句式长度": 0.8, ...}
        # 用于覆盖自动推断结果，值域 0–1，越大越可信
        "特征权重": {},
        "注入预算": dict(DEFAULT_INJECTION_BUDGET),
        "衰减参数": dict(DEFAULT_DECAY),
        # 采集开关：关闭后不再采集记忆与用户信号（数据主权）
        "隐私": {"采集开关": True},
        # 合规闸门（v2.1）：《人工智能拟人化互动服务管理暂行办法》禁止向未成年人
        # 提供虚拟伴侣等虚拟亲密关系服务——未确认「已满 18 周岁」前不注入恋人上下文
        "合规": {"已满18周岁确认": False},
        "updated_at": _now(),
    }


# ==================== 小工具 ====================

def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _as_float(v: Any, default: Any) -> Any:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


if __name__ == "__main__":
    import json
    print(json.dumps({
        "schema_version": SCHEMA_VERSION,
        "memory_types": list(MEMORY_TYPES),
        "injection_budget": DEFAULT_INJECTION_BUDGET,
        "sample_memory": memory_entry("示例：用户生日 5 月 20 日", "事实", entry_id=1),
    }, ensure_ascii=False, indent=2))
