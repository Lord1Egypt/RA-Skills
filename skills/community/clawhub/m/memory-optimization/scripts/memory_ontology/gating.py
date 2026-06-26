"""
Phase 8 Gating module for memory_ontology package.
Handles Write-Time Gating for memory entities.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

from .entity_ops import create_entity, get_entity
from .storage import _write_to_graph, load_all_entities


def get_or_create_source(source_type: str) -> Optional[Dict]:
    """获取或创建 MemorySource 实体

    Args:
        source_type: 来源类型 (如 'kg_extractor', 'user_input')

    Returns:
        MemorySource 实体，如果失败返回 None
    """
    entities = load_all_entities()

    # 查找已存在的来源
    for entity in entities.values():
        if entity['type'] == 'MemorySource' and entity['properties'].get('source_type') == source_type:
            return entity

    # 创建新来源
    now = datetime.now().astimezone().isoformat()
    source_props = {
        'source_type': source_type,
        'reliability': 0.5,  # 默认值
        'use_count': 0,
        'last_used': now,
        'accuracy_history': [],
        'avg_accuracy': 0.5,
        'tags': ['#memory-source', f'#{source_type}']
    }

    try:
        return create_entity('MemorySource', source_props)
    except Exception as e:
        print(f"Warning: Failed to create MemorySource: {e}")
        return None


def update_source_reliability(source_id: str, correct: bool) -> bool:
    """根据准确率反馈更新来源可靠性

    使用指数移动平均更新可靠性，结合历史准确率。

    Args:
        source_id: MemorySource 实体 ID
        correct: 本次是否正确

    Returns:
        成功返回 True
    """
    source = get_entity(source_id, refresh_strength=False)
    if not source or source['type'] != 'MemorySource':
        return False

    props = source['properties']
    history = props.get('accuracy_history', [])

    # 添加新记录
    now = datetime.now().astimezone().isoformat()
    history.append({'timestamp': now, 'correct': correct})

    # 保留最近 20 条记录
    history = history[-20:]

    # 计算平均准确率
    if history:
        accuracy = sum(1 for h in history if h['correct']) / len(history)
        props['avg_accuracy'] = accuracy
        # 可靠性 = 指数移动平均
        old_reliability = props.get('reliability', 0.5)
        props['reliability'] = 0.7 * old_reliability + 0.3 * accuracy

    props['accuracy_history'] = history
    props['use_count'] = props.get('use_count', 0) + 1
    props['last_used'] = now

    # 更新实体
    update_op = {
        "op": "update",
        "entity": {"id": source_id, "properties": props, "updated": now},
        "timestamp": now
    }
    _write_to_graph(json.dumps(update_op, ensure_ascii=False) + '\n')

    return True


def get_default_gating_policy(policy_id: str = 'gate_default') -> Optional[Dict]:
    """获取或创建默认门控策略

    Args:
        policy_id: 策略 ID，默认 'gate_default'

    Returns:
        GatingPolicy 实体
    """
    entities = load_all_entities()

    # 查找已存在的策略
    for entity in entities.values():
        if entity['type'] == 'GatingPolicy' and entity['id'] == policy_id:
            return entity

    # 创建默认策略
    now = datetime.now().astimezone().isoformat()
    policy_props = {
        'id': policy_id,
        'threshold': 0.5,  # >= 0.5 STORE
        'auto_archive_below': 0.3,  # < 0.3 REJECT, 之间 ARCHIVE
        'weights': {
            'source_reputation': 0.40,
            'novelty': 0.35,
            'reliability': 0.25
        },
        'enabled': True,
        'updated_at': now,
        'description': 'Default gating policy based on Selective Memory paper',
        'tags': ['#gating-policy', '#aeam']
    }

    try:
        return create_entity('GatingPolicy', policy_props, entity_id=policy_id)
    except Exception as e:
        print(f"Warning: Failed to create GatingPolicy: {e}")
        return None


def get_all_active_entities() -> List[Dict]:
    """获取所有活跃（非归档、非合并）实体

    Returns:
        活跃实体列表
    """
    entities = load_all_entities()
    active = []

    for entity in entities.values():
        props = entity.get('properties', {})

        # 跳过已归档的
        if props.get('is_archived'):
            continue

        # 跳过已合并的
        if props.get('consolidated_into'):
            continue
        if props.get('merged_into'):
            continue

        active.append(entity)

    return active


def get_all_archived_entities() -> List[Dict]:
    """获取所有归档实体

    Returns:
        ArchivedMemory 实体列表
    """
    from .entity_ops import get_entities_by_type
    return get_entities_by_type('ArchivedMemory')