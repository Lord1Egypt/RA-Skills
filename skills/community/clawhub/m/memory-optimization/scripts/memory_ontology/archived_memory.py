"""
Archived memory module for memory_ontology package.
Handles cold storage and recovery of archived entities.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .config import ONTOLOGY_DIR
from .entity_ops import create_entity, get_entity
from .gating import get_all_archived_entities
from .storage import _write_to_graph


def archive_entity_to_cold_storage(entity_id: str, reason: str,
                                  significance_score: float = 0.5,
                                  strength: float = 1.0) -> Optional[str]:
    """将实体归档到冷存储

    Args:
        entity_id: 要归档的实体 ID
        reason: 归档原因 (below_threshold, superseded, decay, manual)
        significance_score: 归档时的显著性评分
        strength: 归档时的记忆强度

    Returns:
        冷存储文件路径，失败返回 None
    """
    entity = get_entity(entity_id, refresh_strength=False)
    if not entity:
        return None

    now = datetime.now().astimezone().isoformat()

    # 创建冷存储目录
    cold_dir = ONTOLOGY_DIR / "cold-storage"
    cold_dir.mkdir(parents=True, exist_ok=True)

    cold_file = cold_dir / f"{entity_id}.json"

    # 写入冷存储文件
    with open(cold_file, 'w', encoding='utf-8') as f:
        json.dump({
            'archived_at': now,
            'archived_reason': reason,
            'original_entity': entity,
            'significance_score_at_archive': significance_score,
            'strength_at_archive': strength
        }, f, ensure_ascii=False, indent=2)

    # 创建 ArchivedMemory 引用实体
    archived_props = {
        'original_id': entity_id,
        'archived_reason': reason,
        'archived_at': now,
        'cold_storage_path': str(cold_file),
        'original_entity': entity,  # 冗余存储以支持快速恢复
        'significance_score_at_archive': significance_score,
        'strength_at_archive': strength,
        'access_count': 0,
        'last_accessed': None,
        'tags': ['#archived', f'#{reason}']
    }

    try:
        create_entity('ArchivedMemory', archived_props)
    except Exception as e:
        print(f"Warning: Failed to create ArchivedMemory entity: {e}")

    # 标记原始实体为已归档
    update_op = {
        "op": "update",
        "entity": {
            "id": entity_id,
            "properties": {
                'is_archived': True,
                'archived_at': now,
                'archived_reason': reason,
                'cold_storage_path': str(cold_file)
            },
            "updated": now
        },
        "timestamp": now
    }
    _write_to_graph(json.dumps(update_op, ensure_ascii=False) + '\n')

    return str(cold_file)


def recover_entity_from_cold_storage(archived_memory_id: str) -> Optional[Dict]:
    """从冷存储恢复实体到活跃 KG

    Args:
        archived_memory_id: ArchivedMemory 实体 ID

    Returns:
        恢复后的实体，失败返回 None
    """
    archived = get_entity(archived_memory_id, refresh_strength=False)
    if not archived or archived['type'] != 'ArchivedMemory':
        return None

    props = archived['properties']
    original_id = props['original_id']
    cold_path = props.get('cold_storage_path')

    # 从冷存储文件读取
    if cold_path and Path(cold_path).exists():
        with open(cold_path, 'r', encoding='utf-8') as f:
            cold_data = json.load(f)
            original_entity = cold_data.get('original_entity')
    else:
        original_entity = props.get('original_entity')

    if not original_entity:
        return None

    # 恢复实体：创建新版本（带 supersession 链接）
    now = datetime.now().astimezone().isoformat()

    # 标记旧实体已被 supersession
    update_op = {
        "op": "update",
        "entity": {
            "id": original_id,
            "properties": {
                'is_archived': False,  # 恢复活跃状态
                'superseded_by': None,  # 清除替代关系
                'recovered_from_archive': now
            },
            "updated": now
        },
        "timestamp": now
    }
    _write_to_graph(json.dumps(update_op, ensure_ascii=False) + '\n')

    # 增加归档实体的访问计数
    archived_props = archived['properties']
    archived_props['access_count'] = archived_props.get('access_count', 0) + 1
    archived_props['last_accessed'] = now

    update_archived_op = {
        "op": "update",
        "entity": {
            "id": archived_memory_id,
            "properties": archived_props,
            "updated": now
        },
        "timestamp": now
    }
    _write_to_graph(json.dumps(update_archived_op, ensure_ascii=False) + '\n')

    return original_entity


def list_cold_storage_entities(reason: Optional[str] = None) -> List[Dict]:
    """列出冷存储中的实体

    Args:
        reason: 可选，按归档原因过滤

    Returns:
        ArchivedMemory 实体列表
    """
    all_archived = get_all_archived_entities()

    if reason:
        return [a for a in all_archived if a['properties'].get('archived_reason') == reason]

    return all_archived