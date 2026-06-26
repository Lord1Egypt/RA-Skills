"""
Query module for memory_ontology package.
Handles entity querying, graph validation, and export.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .config import WORKSPACE_ROOT
from .relation_ops import get_related_entities
from .schema import load_schema, validate_entity
from .storage import load_all_entities, load_all_relations


def query_entities(entity_type: Optional[str] = None,
                   tags: Optional[List[str]] = None,
                   status: Optional[str] = None,
                   date_from: Optional[str] = None,
                   date_to: Optional[str] = None) -> List[Dict]:
    """查询实体"""
    entities = load_all_entities()
    results = []

    for entity in entities.values():
        # 类型过滤
        if entity_type and entity['type'] != entity_type:
            continue

        props = entity.get('properties', {})

        # 标签过滤
        if tags:
            entity_tags = props.get('tags', [])
            if not any(tag in entity_tags for tag in tags):
                continue

        # 状态过滤
        if status and props.get('status') != status:
            continue

        # 日期过滤
        if date_from or date_to:
            # 尝试获取时间字段
            time_field = None
            for field in ['made_at', 'discovered_at', 'learned_at', 'created_at', 'captured_at']:
                if field in props:
                    time_field = field
                    break

            if time_field:
                entity_time = props[time_field]
                if date_from and entity_time < date_from:
                    continue
                if date_to and entity_time > date_to:
                    continue

        results.append(entity)

    return results


def validate_graph() -> List[str]:
    """验证图谱"""
    errors = []
    entities = load_all_entities()
    relations = load_all_relations()
    schema = load_schema()

    # 验证实体
    for entity_id, entity in entities.items():
        entity_type = entity['type']
        props = entity['properties']

        entity_errors = validate_entity(entity_type, props)
        for error in entity_errors:
            errors.append(f"实体 {entity_id}: {error}")

    # 验证关系
    for rel in relations:
        rel_type = rel['rel']
        if rel_type not in schema['relations']:
            errors.append(f"未知关系类型：{rel_type} (from: {rel['from']}, to: {rel['to']})")

    return errors


def export_to_markdown(output_file: Optional[Path] = None):
    """导出为 Markdown 文档"""
    entities = load_all_entities()
    relations = load_all_relations()

    if not output_file:
        output_file = WORKSPACE_ROOT / "memory" / "ontology-export.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Agent Memory Ontology Export\n\n")
        f.write(f"*Exported at: {datetime.now().astimezone().isoformat()}*\n\n")

        # 按类型分组
        by_type = {}
        for entity in entities.values():
            entity_type = entity['type']
            if entity_type not in by_type:
                by_type[entity_type] = []
            by_type[entity_type].append(entity)

        # 输出每个类型
        for entity_type, type_entities in sorted(by_type.items()):
            f.write(f"## {entity_type} ({len(type_entities)})\n\n")

            for entity in sorted(type_entities, key=lambda x: x.get('created', '')):
                props = entity['properties']
                f.write(f"### {entity['id']}\n\n")

                # 标题
                if 'title' in props:
                    f.write(f"**标题**: {props['title']}\n\n")
                elif 'name' in props:
                    f.write(f"**名称**: {props['name']}\n\n")
                elif 'description' in props:
                    f.write(f"**描述**: {props['description']}\n\n")

                # 状态
                if 'status' in props:
                    f.write(f"**状态**: {props['status']}\n\n")

                # 时间
                for time_field in ['made_at', 'discovered_at', 'learned_at', 'created_at', 'captured_at']:
                    if time_field in props:
                        f.write(f"**时间**: {props[time_field]}\n\n")
                        break

                # 标签
                if 'tags' in props:
                    f.write(f"**标签**: {', '.join(props['tags'])}\n\n")

                # 内容/理由
                for content_field in ['rationale', 'content', 'lesson', 'description']:
                    if content_field in props:
                        f.write(f"**{content_field}**: {props[content_field]}\n\n")
                        break

                # 关联关系
                related = get_related_entities(entity['id'])
                if related:
                    f.write("**关联实体**:\n")
                    for rel_entity in related:
                        rel_title = rel_entity['properties'].get('title') or rel_entity['properties'].get('name') or rel_entity['id']
                        f.write(f"- {rel_entity['id']}: {rel_title}\n")
                    f.write("\n")

                f.write("---\n\n")

    print(f"✓ 导出完成：{output_file}")