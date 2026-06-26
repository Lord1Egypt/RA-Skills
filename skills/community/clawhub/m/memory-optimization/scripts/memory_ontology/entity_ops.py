"""
Entity operations module for memory_ontology package.
Handles entity CRUD operations and strength/decay management.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

from .config import (
    DECAY_RATES,
    ACCESS_DECAY_THRESHOLD_HOURS,
)
from .schema import validate_entity
from .storage import _write_to_graph, load_all_entities


def generate_entity_id(entity_type: str) -> str:
    """生成实体 ID"""
    timestamp = str(time.time()).encode('utf-8')
    random_seed = str(time.time_ns()).encode('utf-8')
    hash_input = timestamp + random_seed
    hash_hex = hashlib.md5(hash_input).hexdigest()[:8]

    prefix_map = {
        'Decision': 'dec',
        'Finding': 'find',
        'LessonLearned': 'lesson',
        'Commitment': 'commit',
        'ContextSnapshot': 'snapshot',
        'Note': 'note',
        'Task': 'task',
        'Project': 'proj',
        'Goal': 'goal',
        'Person': 'pers',
        'Milestone': 'mile',
        'Skill': 'skil',
        'Event': 'event',
        'SkillCard': 'skc',
        'ConflictReview': 'conf',
        'Preference': 'pref',
        # Phase 8: Write-Time Gating
        'SignificanceScore': 'sig',
        'MemorySource': 'src',
        'GatingPolicy': 'gate',
        'ArchivedMemory': 'arch',
        # Phase 4: Concept-Mediated Graph
        'Concept': 'concept'
    }

    prefix = prefix_map.get(entity_type, 'ent')
    return f"{prefix}_{hash_hex}"


def get_default_decay_rate(entity_type: str) -> float:
    """获取实体类型的默认衰减率"""
    return DECAY_RATES.get(entity_type, DECAY_RATES['default'])


def add_memory_evolution_fields(entity_type: str, properties: Dict) -> Dict:
    """为实本添加记忆进化字段（Phase 1b）"""
    now = datetime.now().astimezone().isoformat()

    # 如果没有提供 strength，使用默认值
    if 'strength' not in properties:
        properties['strength'] = 1.0

    # 如果没有提供 decay_rate，使用类型默认值
    if 'decay_rate' not in properties:
        properties['decay_rate'] = get_default_decay_rate(entity_type)

    # 如果没有提供 last_accessed，设置为当前时间
    if 'last_accessed' not in properties:
        properties['last_accessed'] = now

    # 如果没有提供 source_trust，使用默认值
    if 'source_trust' not in properties:
        properties['source_trust'] = 'medium'

    return properties


def create_entity(entity_type: str, properties: Dict, entity_id: Optional[str] = None,
                 provenance: Optional[List[str]] = None) -> Dict:
    """创建实体

    Phase 1b 增强: 自动添加 strength, decay_rate, last_accessed, provenance 字段
    """
    # 添加记忆进化字段
    properties = add_memory_evolution_fields(entity_type, properties)

    # 添加 provenance（如果提供）
    if provenance:
        existing_provenance = properties.get('provenance', [])
        if isinstance(existing_provenance, list):
            properties['provenance'] = existing_provenance + provenance
        else:
            properties['provenance'] = provenance

    # 验证
    errors = validate_entity(entity_type, properties)
    if errors:
        raise ValueError(f"实体验证失败:\n" + "\n".join(f"  - {e}" for e in errors))

    # 生成 ID
    if not entity_id:
        entity_id = generate_entity_id(entity_type)

    # 创建实体对象
    now = datetime.now().astimezone().isoformat()
    entity = {
        "id": entity_id,
        "type": entity_type,
        "properties": properties,
        "created": now,
        "updated": now
    }

    # 写入 graph.jsonl
    operation = {
        "op": "create",
        "entity": entity,
        "timestamp": now
    }

    _write_to_graph(json.dumps(operation, ensure_ascii=False) + '\n')

    return entity


def _read_entity_from_graph(entity_id: str) -> Optional[Dict]:
    """从 graph.jsonl 读取单个实体（不触发衰减）

    这是 get_entity() 的内部辅助方法，用于在不触发访问时衰减的情况下读取实体。
    """
    entities = load_all_entities()
    return entities.get(entity_id)


def get_entity(entity_id: str, refresh_strength: bool = True) -> Optional[Dict]:
    """获取单个实体

    访问时实时衰减：如果 last_accessed 超过 ACCESS_DECAY_THRESHOLD_HOURS 小时，
    自动应用衰减计算。

    Args:
        entity_id: 实体 ID
        refresh_strength: 是否刷新 strength 并更新 last_accessed（默认 True）
    """
    entity = _read_entity_from_graph(entity_id)
    if not entity:
        return None

    if refresh_strength:
        # 访问时实时衰减
        last_accessed = entity['properties'].get('last_accessed')
        if last_accessed:
            try:
                last_dt = datetime.fromisoformat(last_accessed.replace('Z', '+00:00'))
                hours_elapsed = (datetime.now().astimezone() - last_dt).total_seconds() / 3600

                if hours_elapsed >= ACCESS_DECAY_THRESHOLD_HOURS:
                    # 超过阈值，应用衰减
                    days_elapsed = hours_elapsed / 24.0
                    apply_decay_to_entity(entity_id, days_elapsed)
                    # 重新读取以获取更新后的值
                    entity = _read_entity_from_graph(entity_id)
                else:
                    # 刚访问过，只更新时间戳
                    refresh_entity_strength(entity_id)
                    entity = _read_entity_from_graph(entity_id)
            except (ValueError, TypeError):
                # last_accessed 格式错误，静默跳过
                pass
        else:
            # 首次访问，初始化 strength
            refresh_entity_strength(entity_id)
            entity = _read_entity_from_graph(entity_id)

    return entity


def refresh_entity_strength(entity_id: str) -> Optional[float]:
    """刷新实体 strength 并更新 last_accessed

    当实体被访问时调用，计算基于时间的衰减而非硬重置。
    衰减公式: new_strength = old_strength * (decay_rate ^ (days_elapsed / 30))

    Returns:
        更新后的 strength 值，如果实体不存在返回 None
    """
    entity = _read_entity_from_graph(entity_id)
    if not entity:
        return None

    now = datetime.now().astimezone().isoformat()
    props = entity['properties']
    last_accessed = props.get('last_accessed')

    if last_accessed:
        # 计算自上次访问以来的衰减
        try:
            last_dt = datetime.fromisoformat(last_accessed.replace('Z', '+00:00'))
            hours_elapsed = (datetime.now().astimezone() - last_dt).total_seconds() / 3600

            if hours_elapsed >= ACCESS_DECAY_THRESHOLD_HOURS:
                # 应用衰减
                days_elapsed = hours_elapsed / 24.0
                old_strength = props.get('strength', 1.0)
                decay_rate = props.get('decay_rate', 0.95)
                months_elapsed = days_elapsed / 30.0
                new_strength = old_strength * (decay_rate ** months_elapsed)
                new_strength = max(0.0, min(1.0, new_strength))
            else:
                # 刚访问过，不衰减
                new_strength = props.get('strength', 1.0)
        except (ValueError, TypeError) as e:
            # last_accessed 格式错误，静默跳过衰减
            new_strength = props.get('strength', 1.0)
    else:
        # 首次访问，strength 保持不变（已在创建时初始化为 1.0）
        new_strength = props.get('strength', 1.0)

    props['strength'] = new_strength
    props['last_accessed'] = now

    # 更新实体
    update_operation = {
        "op": "update",
        "entity": {
            "id": entity_id,
            "properties": {
                "strength": new_strength,
                "last_accessed": now
            },
            "updated": now
        },
        "timestamp": now
    }

    # 追加到 graph.jsonl（带文件锁）
    _write_to_graph(json.dumps(update_operation, ensure_ascii=False) + '\n')

    return new_strength


def mark_entity_consolidated(entity_id: str, skillcard_id: str) -> bool:
    """标记实体已被合并到 SkillCard

    使用 op: update 模式标记原始实体，这样在后续的 Consolidation Cycle 中
    不会再次被考虑合并。

    Args:
        entity_id: 被合并的原始实体 ID
        skillcard_id: 合并后生成的 SkillCard ID

    Returns:
        成功返回 True，失败返回 False
    """
    entity = get_entity(entity_id)
    if not entity:
        print(f"Warning: Entity {entity_id} not found for consolidation marking")
        return False

    now = datetime.now().astimezone().isoformat()

    # 使用 op: update 模式标记实体已被合并
    update_op = {
        "op": "update",
        "entity": {
            "id": entity_id,
            "properties": {"consolidated_into": skillcard_id},
            "updated": now
        },
        "timestamp": now
    }

    _write_to_graph(json.dumps(update_op, ensure_ascii=False) + '\n')
    return True


def apply_decay_to_entity(entity_id: str, days_elapsed: float) -> Optional[float]:
    """对实体应用衰减

    根据经过的时间和实体类型的衰减率计算新的 strength 值

    Args:
        entity_id: 实体 ID
        days_elapsed: 经过的天数

    Returns:
        新的 strength 值，如果实体不存在返回 None
    """
    # 使用 _read_entity_from_graph 避免递归调用 get_entity
    entity = _read_entity_from_graph(entity_id)
    if not entity:
        return None

    props = entity['properties']
    decay_rate = props.get('decay_rate', 0.95)

    # 计算衰减：strength *= decay_rate^(days_elapsed/30)
    # 假设 decay_rate 是每月的衰减率
    old_strength = props.get('strength', 1.0)
    months_elapsed = days_elapsed / 30.0
    new_strength = old_strength * (decay_rate ** months_elapsed)

    # 限制在 0-1 之间
    new_strength = max(0.0, min(1.0, new_strength))

    # 更新实体
    now = datetime.now().astimezone().isoformat()
    update_operation = {
        "op": "update",
        "entity": {
            "id": entity_id,
            "properties": {
                "strength": new_strength
            },
            "updated": now
        },
        "timestamp": now
    }

    _write_to_graph(json.dumps(update_operation, ensure_ascii=False) + '\n')

    return new_strength


def get_entities_by_strength(threshold: float = 0.1) -> List[Dict]:
    """获取 strength 低于阈值的实体列表（归档候选）

    Args:
        threshold: strength 阈值，默认 0.1

    Returns:
        strength 低于阈值的实体列表
    """
    entities = load_all_entities()
    weak_entities = []

    for entity in entities.values():
        props = entity.get('properties', {})
        strength = props.get('strength', 1.0)
        if strength < threshold:
            weak_entities.append(entity)

    return weak_entities


def get_entities_by_type(entity_type: str) -> List[Dict]:
    """获取指定类型的所有实体"""
    entities = load_all_entities()
    return [e for e in entities.values() if e['type'] == entity_type]


def get_strength_distribution() -> Dict[str, Dict]:
    """获取各类型实体的 strength 分布统计

    Returns:
        Dict[type -> {count, avg_strength, min_strength, max_strength}]
    """
    entities = load_all_entities()
    distribution = {}

    for entity in entities.values():
        entity_type = entity['type']
        props = entity.get('properties', {})
        strength = props.get('strength', 1.0)

        if entity_type not in distribution:
            distribution[entity_type] = {
                'count': 0,
                'total_strength': 0.0,
                'min_strength': 1.0,
                'max_strength': 0.0
            }

        d = distribution[entity_type]
        d['count'] += 1
        d['total_strength'] += strength
        d['min_strength'] = min(d['min_strength'], strength)
        d['max_strength'] = max(d['max_strength'], strength)

    # 计算平均值
    for d in distribution.values():
        if d['count'] > 0:
            d['avg_strength'] = d['total_strength'] / d['count']
        else:
            d['avg_strength'] = 0.0

    return distribution