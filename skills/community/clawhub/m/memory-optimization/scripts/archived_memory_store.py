#!/usr/bin/env python3
"""
Archived Memory Store - Cold Storage Manager (Phase 8: AEAM)

管理归档到冷存储的记忆实体，提供恢复、搜索、列表等功能。

Usage:
    python3 scripts/archived_memory_store.py list
    python3 scripts/archived_memory_store.py recover --id arch_xxx
    python3 scripts/archived_memory_store.py search --query "some text"
    python3 scripts/archived_memory_store.py delete --id arch_xxx
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

# 路径配置
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory_ontology import (
    ONTOLOGY_DIR,
    GRAPH_FILE,
    load_all_entities,
    get_all_archived_entities,
    get_entity,
    recover_entity_from_cold_storage,
)


# ============== 冷存储管理器 ==============

class ArchivedMemoryStore:
    """冷存储管理器

    管理归档到冷存储的记忆实体，支持：
    - 列出归档实体
    - 从冷存储恢复实体
    - 搜索归档实体
    - 永久删除
    - 获取存储统计
    """

    def __init__(self, cold_storage_dir: Optional[Path] = None):
        """
        Args:
            cold_storage_dir: 冷存储目录路径，默认 ontology/cold-storage/
        """
        self.cold_storage_dir = cold_storage_dir or (ONTOLOGY_DIR / "cold-storage")
        self.cold_storage_dir.mkdir(parents=True, exist_ok=True)

    def list_archived(self, reason: Optional[str] = None,
                      limit: Optional[int] = None) -> List[Dict]:
        """
        列出所有归档实体

        Args:
            reason: 可选，按归档原因过滤
            limit: 可选，返回数量限制

        Returns:
            ArchivedMemory 实体列表
        """
        all_archived = get_all_archived_entities()

        if reason:
            all_archived = [
                a for a in all_archived
                if a['properties'].get('archived_reason') == reason
            ]

        # 按归档时间倒序
        all_archived.sort(
            key=lambda x: x['properties'].get('archived_at', ''),
            reverse=True
        )

        if limit:
            return all_archived[:limit]

        return all_archived

    def recover_entity(self, archived_memory_id: str) -> Optional[Dict]:
        """
        从冷存储恢复实体到活跃 KG

        Args:
            archived_memory_id: ArchivedMemory 实体 ID

        Returns:
            恢复后的原始实体，失败返回 None
        """
        return recover_entity_from_cold_storage(archived_memory_id)

    def search_archived(self, query: str, limit: int = 10) -> List[Dict]:
        """
        在归档实体中搜索

        使用简单的文本匹配搜索归档实体的原始内容。

        Args:
            query: 搜索查询
            limit: 返回结果数量限制

        Returns:
            匹配的 ArchivedMemory 实体列表
        """
        all_archived = get_all_archived_entities()
        query_lower = query.lower()
        results = []

        for archived in all_archived:
            props = archived['properties']
            original = props.get('original_entity', {})

            if not original:
                continue

            # 提取原始实体文本
            orig_props = original.get('properties', {})
            text_parts = []

            for field in ['title', 'content', 'rationale', 'lesson', 'description']:
                if field in orig_props and orig_props[field]:
                    text_parts.append(str(orig_props[field]).lower())

            text = ' '.join(text_parts)

            if query_lower in text:
                results.append(archived)

                # 添加匹配信息
                archived['_match_info'] = {
                    'matched_in': [f for f in ['title', 'content', 'rationale', 'lesson', 'description']
                                  if f in orig_props and query_lower in str(orig_props[f]).lower()]
                }

            if len(results) >= limit:
                break

        return results

    def permanently_delete(self, archived_memory_id: str) -> bool:
        """
        永久删除冷存储中的实体

        注意：只删除 ArchivedMemory 引用和冷存储文件，
        不删除原始实体（如果需要恢复，先调用 recover）

        Args:
            archived_memory_id: ArchivedMemory 实体 ID

        Returns:
            是否成功
        """
        from memory_ontology import _write_to_graph

        archived = get_entity(archived_memory_id, refresh_strength=False)
        if not archived or archived['type'] != 'ArchivedMemory':
            return False

        props = archived['properties']

        # 删除冷存储文件
        cold_path = props.get('cold_storage_path')
        if cold_path and Path(cold_path).exists():
            try:
                Path(cold_path).unlink()
            except Exception as e:
                print(f"Warning: Failed to delete cold storage file: {e}")

        # 删除 ArchivedMemory 实体（通过标记为 deleted）
        now = datetime.now().astimezone().isoformat()
        update_op = {
            "op": "update",
            "entity": {
                "id": archived_memory_id,
                "properties": {
                    '_deleted': True,
                    'deleted_at': now
                },
                "updated": now
            },
            "timestamp": now
        }
        _write_to_graph(json.dumps(update_op, ensure_ascii=False) + '\n')

        return True

    def get_stats(self) -> Dict:
        """
        获取冷存储统计信息

        Returns:
            Dict with storage stats
        """
        all_archived = get_all_archived_entities()

        # 按原因分组
        by_reason: Dict[str, int] = {}
        total_size = 0
        oldest = None
        newest = None

        for archived in all_archived:
            props = archived['properties']

            # 按原因统计
            reason = props.get('archived_reason', 'unknown')
            by_reason[reason] = by_reason.get(reason, 0) + 1

            # 冷存储大小
            cold_path = props.get('cold_storage_path')
            if cold_path and Path(cold_path).exists():
                total_size += Path(cold_path).stat().st_size

            # 最老/最新
            archived_at = props.get('archived_at', '')
            if archived_at:
                if oldest is None or archived_at < oldest:
                    oldest = archived_at
                if newest is None or archived_at > newest:
                    newest = archived_at

        return {
            'total_count': len(all_archived),
            'by_reason': by_reason,
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'oldest_archive': oldest,
            'newest_archive': newest
        }

    def purge_old(self, days: int = 90, dry_run: bool = True) -> Dict:
        """
        清理旧的归档实体

        Args:
            days: 超过此天数的归档将被删除
            dry_run: 如果 True，只返回统计信息，不实际删除

        Returns:
            Dict with purge results
        """
        from datetime import timedelta

        all_archived = get_all_archived_entities()
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_iso = cutoff_date.isoformat()

        to_delete = []
        for archived in all_archived:
            props = archived['properties']
            archived_at = props.get('archived_at', '')
            if archived_at and archived_at < cutoff_iso:
                to_delete.append(archived)

        result = {
            'dry_run': dry_run,
            'cutoff_days': days,
            'cutoff_date': cutoff_iso,
            'candidates': len(to_delete),
            'deleted': 0
        }

        if not dry_run:
            for archived in to_delete:
                if self.permanently_delete(archived['id']):
                    result['deleted'] += 1

        return result


# ============== CLI 接口 ==============

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Archived Memory Store Manager')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出归档实体')
    list_parser.add_argument('--reason', help='按归档原因过滤')
    list_parser.add_argument('--limit', type=int, help='返回数量限制')
    list_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    # recover 命令
    recover_parser = subparsers.add_parser('recover', help='从冷存储恢复实体')
    recover_parser.add_argument('--id', required=True, help='ArchivedMemory ID')

    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索归档实体')
    search_parser.add_argument('--query', required=True, help='搜索查询')
    search_parser.add_argument('--limit', type=int, default=10, help='结果数量限制')

    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='永久删除归档实体')
    delete_parser.add_argument('--id', required=True, help='ArchivedMemory ID')

    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='冷存储统计')

    # purge 命令
    purge_parser = subparsers.add_parser('purge', help='清理旧归档')
    purge_parser.add_argument('--days', type=int, default=90, help='超过此天数的归档将删除')
    purge_parser.add_argument('--dry-run', action='store_true', help='只显示统计，不实际删除')
    purge_parser.add_argument('--execute', action='store_true', help='执行清理')

    args = parser.parse_args()

    store = ArchivedMemoryStore()

    if args.command == 'list':
        archived = store.list_archived(reason=args.reason, limit=args.limit)

        print(f"\n{'='*60}")
        print(f"Archived Entities: {len(archived)}")
        print(f"{'='*60}")

        if args.reason:
            print(f"Filter: reason={args.reason}")

        for a in archived:
            props = a['properties']
            orig = props.get('original_entity', {})
            orig_props = orig.get('properties', {}) if orig else {}
            title = orig_props.get('title', orig.get('id', 'Unknown'))

            print(f"\n{a['id']}")
            print(f"  Original: {props.get('original_id')}")
            print(f"  Reason: {props.get('archived_reason')}")
            print(f"  Archived: {props.get('archived_at')}")
            print(f"  Title: {title}")

            if args.verbose:
                print(f"  Significance: {props.get('significance_score_at_archive', 'N/A')}")
                print(f"  Strength: {props.get('strength_at_archive', 'N/A')}")
                print(f"  Access Count: {props.get('access_count', 0)}")
                cold_path = props.get('cold_storage_path')
                if cold_path:
                    print(f"  Cold Path: {cold_path}")

    elif args.command == 'recover':
        print(f"\nRecovering {args.id}...")
        result = store.recover_entity(args.id)

        if result:
            print(f"✓ Successfully recovered")
            print(f"  Entity ID: {result.get('id')}")
            print(f"  Type: {result.get('type')}")
            title = result.get('properties', {}).get('title', 'N/A')
            print(f"  Title: {title}")
        else:
            print(f"✗ Failed to recover {args.id}")

    elif args.command == 'search':
        results = store.search_archived(args.query, limit=args.limit)

        print(f"\n{'='*60}")
        print(f"Search Results for: '{args.query}'")
        print(f"Found: {len(results)}")
        print(f"{'='*60}")

        for r in results:
            props = r['properties']
            orig = props.get('original_entity', {})
            orig_props = orig.get('properties', {}) if orig else {}
            title = orig_props.get('title', orig.get('id', 'Unknown'))
            match_info = r.get('_match_info', {})

            print(f"\n{r['id']}")
            print(f"  Title: {title}")
            print(f"  Matched in: {', '.join(match_info.get('matched_in', []))}")
            print(f"  Archived: {props.get('archived_at')}")

    elif args.command == 'delete':
        confirm = input(f"Permanently delete {args.id}? This cannot be undone. (yes/no): ")
        if confirm.lower() == 'yes':
            if store.permanently_delete(args.id):
                print(f"✓ Deleted {args.id}")
            else:
                print(f"✗ Failed to delete {args.id}")
        else:
            print("Cancelled")

    elif args.command == 'stats':
        stats = store.get_stats()

        print(f"\n{'='*60}")
        print(f"Cold Storage Statistics")
        print(f"{'='*60}")
        print(f"Total Archived: {stats['total_count']}")
        print(f"Total Size: {stats['total_size_mb']:.2f} MB")
        print(f"\nBy Reason:")
        for reason, count in stats['by_reason'].items():
            print(f"  {reason}: {count}")
        print(f"\nOldest: {stats['oldest_archive'] or 'N/A'}")
        print(f"Newest: {stats['newest_archive'] or 'N/A'}")

    elif args.command == 'purge':
        dry_run = not args.execute
        result = store.purge_old(days=args.days, dry_run=dry_run)

        print(f"\n{'='*60}")
        print(f"Purge {'Simulation' if dry_run else 'Execution'}")
        print(f"{'='*60}")
        print(f"Cutoff: {result['days']} days ({result['cutoff_date']})")
        print(f"Candidates: {result['candidates']}")

        if dry_run:
            print(f"\nNote: This was a dry run. Use --execute to actually delete.")
        else:
            print(f"Deleted: {result['deleted']}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
