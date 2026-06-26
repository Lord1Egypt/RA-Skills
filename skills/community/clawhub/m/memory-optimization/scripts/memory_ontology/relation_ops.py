"""
Relation operations module for memory_ontology package.
Handles relation creation and retrieval.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

from .schema import load_schema
from .storage import _write_to_graph, load_all_entities, load_all_relations


def create_relation(from_id: str, rel_type: str, to_id: str, properties: Optional[Dict] = None):
    """创建关系"""
    schema = load_schema()

    # 验证关系类型
    if rel_type not in schema['relations']:
        raise ValueError(f"未知关系类型：{rel_type}")

    # 验证实体存在
    entities = load_all_entities()
    if from_id not in entities:
        raise ValueError(f"实体不存在：{from_id}")
    if to_id not in entities:
        raise ValueError(f"实体不存在：{to_id}")

    # 验证关系类型匹配
    rel_schema = schema['relations'][rel_type]
    from_entity = entities[from_id]
    to_entity = entities[to_id]

    from_types = rel_schema.get('from_types', [])
    to_types = rel_schema.get('to_types', [])

    if from_entity['type'] not in from_types:
        raise ValueError(f"关系 {rel_type} 不能从 {from_entity['type']} 类型发起，允许的类型：{from_types}")

    if to_entity['type'] not in to_types:
        raise ValueError(f"关系 {rel_type} 不能指向 {to_entity['type']} 类型，允许的类型：{to_types}")

    # 创建关系
    now = datetime.now().astimezone().isoformat()
    operation = {
        "op": "relate",
        "from": from_id,
        "rel": rel_type,
        "to": to_id,
        "properties": properties or {},
        "timestamp": now
    }

    _write_to_graph(json.dumps(operation, ensure_ascii=False) + '\n')

    return operation


def get_related_entities(entity_id: str, relation_type: Optional[str] = None) -> List[Dict]:
    """获取相关实体"""
    entities = load_all_entities()
    relations = load_all_relations()
    related = []

    for rel in relations:
        if rel['from'] == entity_id:
            if relation_type is None or rel['rel'] == relation_type:
                if rel['to'] in entities:
                    related.append(entities[rel['to']])
        elif rel['to'] == entity_id:
            if relation_type is None or rel['rel'] == relation_type:
                if rel['from'] in entities:
                    related.append(entities[rel['from']])

    return related