"""
CLI module for memory_ontology package.
Handles command-line interface and entity printing.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict

from .config import DECAY_THRESHOLD
from .entity_ops import (
    create_entity,
    get_entity,
    get_entities_by_strength,
    get_strength_distribution,
    load_all_entities,
)
from .query import query_entities, validate_graph, export_to_markdown
from .relation_ops import create_relation, get_related_entities
from .storage import load_all_relations, compact_graph, ensure_ontology_dir
from .retrieval import ValueAwareRetriever


def print_entity(entity: Dict, verbose: bool = False):
    """打印实体"""
    props = entity['properties']

    # 基本信息
    entity_id = entity['id']
    entity_type = entity['type']

    # 标题/名称
    title = props.get('title') or props.get('name') or props.get('description', 'N/A')

    print(f"\n{'='*60}")
    print(f"{entity_type}: {entity_id}")
    print(f"{'='*60}")
    print(f"标题：{title}")

    # 状态
    if 'status' in props:
        print(f"状态：{props['status']}")

    # 时间
    for time_field in ['made_at', 'discovered_at', 'learned_at', 'created_at', 'captured_at']:
        if time_field in props:
            print(f"时间：{props[time_field]}")
            break

    # 标签
    if 'tags' in props:
        print(f"标签：{', '.join(props['tags'])}")

    # Phase 1b: 记忆进化字段
    if 'strength' in props:
        strength = props['strength']
        bar_len = int(strength * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"强度：[{bar}] {strength:.0%}")
    if 'last_accessed' in props:
        print(f"最后访问：{props['last_accessed']}")
    if 'provenance' in props and props['provenance']:
        provenance_str = ', '.join(props['provenance']) if isinstance(props['provenance'], list) else props['provenance']
        print(f"来源：{provenance_str}")
    if 'source_trust' in props:
        print(f"信任度：{props['source_trust']}")

    # 详细内容
    if verbose:
        for field, value in props.items():
            if field not in ['title', 'name', 'status', 'tags'] and not field.endswith('_at'):
                if isinstance(value, str) and len(value) > 200:
                    print(f"{field}: {value[:200]}...")
                else:
                    print(f"{field}: {value}")

    # 关联实体
    related = get_related_entities(entity_id)
    if related:
        print(f"\n关联实体 ({len(related)}):")
        for rel_entity in related:
            rel_title = rel_entity['properties'].get('title') or rel_entity['properties'].get('name') or rel_entity['id']
            print(f"  - {rel_entity['id']}: {rel_title}")


def main():
    parser = argparse.ArgumentParser(description='Agent Memory Ontology Manager')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # create 命令
    create_parser = subparsers.add_parser('create', help='创建实体')
    create_parser.add_argument('--type', required=True, help='实体类型')
    create_parser.add_argument('--props', required=True, help='属性 JSON')
    create_parser.add_argument('--id', help='实体 ID (可选，自动生成)')

    # relate 命令
    relate_parser = subparsers.add_parser('relate', help='创建关系')
    relate_parser.add_argument('--from', dest='from_id', required=True, help='源实体 ID')
    relate_parser.add_argument('--rel', required=True, help='关系类型')
    relate_parser.add_argument('--to', required=True, help='目标实体 ID')
    relate_parser.add_argument('--props', help='关系属性 JSON')

    # query 命令
    query_parser = subparsers.add_parser('query', help='查询实体')
    query_parser.add_argument('--type', help='实体类型')
    query_parser.add_argument('--tags', nargs='+', help='标签列表')
    query_parser.add_argument('--status', help='状态')
    query_parser.add_argument('--from', dest='date_from', help='起始日期')
    query_parser.add_argument('--to', dest='date_to', help='结束日期')
    query_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    # get 命令
    get_parser = subparsers.add_parser('get', help='获取实体')
    get_parser.add_argument('--id', required=True, help='实体 ID')
    get_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    # related 命令
    related_parser = subparsers.add_parser('related', help='获取相关实体')
    related_parser.add_argument('--id', required=True, help='实体 ID')
    related_parser.add_argument('--rel', help='关系类型')
    related_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证图谱')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有实体')
    list_parser.add_argument('--type', help='实体类型')
    list_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    # export 命令
    export_parser = subparsers.add_parser('export', help='导出为 Markdown')
    export_parser.add_argument('--output', '-o', help='输出文件路径')

    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='显示统计信息')

    # compact 命令
    compact_parser = subparsers.add_parser('compact', help='压缩 graph.jsonl，保留每个实体的最新版本')

    # gate 命令 (Phase 8: Write-Time Gating)
    gate_parser = subparsers.add_parser('gate', help='评估实体的显著性评分 (Write-Time Gating)')
    gate_parser.add_argument('--id', required=True, help='实体 ID')
    gate_parser.add_argument('--source', default='user_input', help='来源类型')

    # archived 命令 (Phase 8: 归档实体管理)
    archived_parser = subparsers.add_parser('archived', help='管理归档实体')
    archived_parser.add_argument('--list', dest='list_archived', action='store_true', help='列出归档实体')
    archived_parser.add_argument('--reason', help='按归档原因过滤')
    archived_parser.add_argument('--limit', type=int, help='返回数量限制')

    # retrieve 命令 (Phase 6: 价值感知检索)
    retrieve_parser = subparsers.add_parser('retrieve', help='价值感知检索 (按价值分数排序)')
    retrieve_parser.add_argument('--types', nargs='+', help='实体类型列表')
    retrieve_parser.add_argument('--query', help='搜索查询文本')
    retrieve_parser.add_argument('--min-score', type=float, default=0.3, help='最低价值分数 (默认 0.3)')
    retrieve_parser.add_argument('--limit', type=int, default=20, help='返回数量限制 (默认 20)')
    retrieve_parser.add_argument('--show-scores', action='store_true', help='显示价值分数')

    args = parser.parse_args()

    # 确保目录存在
    ensure_ontology_dir()

    if args.command == 'create':
        try:
            props = json.loads(args.props)
            entity = create_entity(args.type, props, args.id)
            print(f"✓ 创建实体成功：{entity['id']}")
            print_entity(entity, verbose=True)
        except Exception as e:
            print(f"✗ 创建失败：{e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'relate':
        try:
            props = json.loads(args.props) if args.props else None
            relation = create_relation(args.from_id, args.rel, args.to, props)
            print(f"✓ 创建关系成功：{args.from_id} --[{args.rel}]--> {args.to}")
        except Exception as e:
            print(f"✗ 创建关系失败：{e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'query':
        results = query_entities(
            entity_type=args.type,
            tags=args.tags,
            status=args.status,
            date_from=args.date_from,
            date_to=args.date_to
        )
        print(f"找到 {len(results)} 个实体:\n")
        for entity in results:
            print_entity(entity, verbose=args.verbose)

    elif args.command == 'get':
        entity = get_entity(args.id)
        if entity:
            print_entity(entity, verbose=args.verbose)
        else:
            print(f"✗ 实体不存在：{args.id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'related':
        related = get_related_entities(args.id, args.rel)
        print(f"找到 {len(related)} 个相关实体:\n")
        for entity in related:
            print_entity(entity, verbose=args.verbose)

    elif args.command == 'validate':
        errors = validate_graph()
        if errors:
            print(f"✗ 验证失败，发现 {len(errors)} 个错误:\n")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print("✓ 图谱验证通过")

    elif args.command == 'list':
        entities = load_all_entities()
        if args.type:
            entities = {k: v for k, v in entities.items() if v['type'] == args.type}

        print(f"共 {len(entities)} 个实体:\n")
        for entity in entities.values():
            print_entity(entity, verbose=args.verbose)

    elif args.command == 'export':
        export_to_markdown(Path(args.output) if args.output else None)

    elif args.command == 'stats':
        entities = load_all_entities()
        relations = load_all_relations()

        # 按类型统计
        by_type = {}
        for entity in entities.values():
            entity_type = entity['type']
            by_type[entity_type] = by_type.get(entity_type, 0) + 1

        print(f"\n📊 Agent Memory Ontology 统计\n")
        print(f"实体总数：{len(entities)}")
        print(f"关系总数：{len(relations)}")
        print(f"\n按类型分布:")
        for entity_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {entity_type}: {count}")

        # Phase 1b: Strength 分布
        print(f"\n📈 记忆强度分布 (Phase 1b):")
        strength_dist = get_strength_distribution()
        for entity_type, stats in sorted(strength_dist.items()):
            avg = stats.get('avg_strength', 0)
            bar_len = int(avg * 20)
            bar = '█' * bar_len + '░' * (20 - bar_len)
            print(f"  {entity_type}: [{bar}] {avg:.0%}")

        # 衰减候选
        weak_entities = get_entities_by_strength(DECAY_THRESHOLD)
        if weak_entities:
            print(f"\n🗑️ 衰减候选 (strength < {DECAY_THRESHOLD}): {len(weak_entities)} 个")
            for entity in weak_entities[:5]:
                props = entity['properties']
                title = props.get('title', entity['id'])
                strength = props.get('strength', 0)
                print(f"  - {entity['id']}: {title} (strength={strength:.2f})")
            if len(weak_entities) > 5:
                print(f"  ... 还有 {len(weak_entities) - 5} 个")

        # 最近创建的实体
        print(f"\n最近创建的实体:")
        sorted_entities = sorted(entities.values(), key=lambda x: x.get('created', ''), reverse=True)[:5]
        for entity in sorted_entities:
            props = entity['properties']
            title = props.get('title') or props.get('name') or entity['id']
            print(f"  - {entity['id']}: {title} ({entity['type']})")

    elif args.command == 'compact':
        result = compact_graph()
        kept = result.get('kept', 0)
        total = result.get('total_ops', 0)
        compacted = result.get('compacted_to', kept)
        if compacted == total:
            print(f"✓ 图谱已是最优状态，无需压缩 ({kept} 个实体)")
        else:
            print(f"✓ 图谱压缩完成: {total} → {compacted} 行 (保留 {kept} 个实体最新版本)")

    elif args.command == 'gate':
        # Phase 8: Write-Time Gating 评估
        from write_time_gating import WriteTimeGating
        gating = WriteTimeGating()
        entity = get_entity(args.id, refresh_strength=False)
        if not entity:
            print(f"✗ Entity not found: {args.id}", file=sys.stderr)
            sys.exit(1)
        source_type = getattr(args, 'source', 'user_input')
        result = gating.gate(entity, source_type)
        print(f"\n{'='*50}")
        print(f"Gate Result: {result.status}")
        print(f"Reason: {result.reason}")
        print(f"{'='*50}")
        print(f"Total Score: {result.score.total_score:.3f}")
        print(f"Breakdown:")
        print(f"  Source Reputation: {result.score.breakdown.source_reputation:.3f}")
        print(f"  Novelty:          {result.score.breakdown.novelty:.3f}")
        print(f"  Reliability:      {result.score.breakdown.reliability:.3f}")

    elif args.command == 'archived':
        # Phase 8: 归档实体管理
        from archived_memory_store import ArchivedMemoryStore
        store = ArchivedMemoryStore()
        if args.list_archived:
            archived = store.list_archived(reason=args.reason, limit=args.limit)
            print(f"\n{'='*50}")
            print(f"Archived Entities: {len(archived)}")
            print(f"{'='*50}")
            for a in archived:
                props = a['properties']
                print(f"\n{a['id']}")
                print(f"  Original: {props.get('original_id')}")
                print(f"  Reason: {props.get('archived_reason')}")
                print(f"  Archived: {props.get('archived_at')}")

    elif args.command == 'retrieve':
        # Phase 6: 价值感知检索
        retriever = ValueAwareRetriever()
        if args.query:
            results = retriever.retrieve_by_query(
                query=args.query,
                entity_types=args.types,
                min_value_score=args.min_score,
                limit=args.limit
            )
        else:
            results = retriever.retrieve(
                entity_types=args.types,
                min_value_score=args.min_score,
                limit=args.limit
            )

        print(f"\n{'='*60}")
        print(f"Value-Aware Retrieval: {len(results)} results")
        print(f"Min Score: {args.min_score}")
        print(f"{'='*60}\n")

        for entity in results:
            props = entity.get('properties', {})
            title = props.get('title') or props.get('name') or entity['id']
            entity_type = entity.get('type', 'Unknown')
            entity_id = entity.get('id', '')

            if args.show_scores:
                score = entity.get('value_score', 0)
                print(f"[{entity_type}] {entity_id}")
                print(f"  Title: {title}")
                print(f"  Value Score: {score:.3f}")
                print()
            else:
                print(f"[{entity_type}] {entity_id}: {title}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()