#!/usr/bin/env python3
"""
Memory Decay Engine
批量衰减引擎 - 定期扫描所有实体，应用衰减并归档 weak 实体

使用方法:
    python3 scripts/decay_engine.py run          # 运行完整衰减周期
    python3 scripts/decay_engine.py run --dry-run  # 模拟运行（不写入）
    python3 scripts/decay_engine.py stats        # 查看统计
    python3 scripts/decay_engine.py candidates   # 查看 weak 实体候选
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict, Optional

# 添加父目录到路径以便导入 memory_ontology
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory_ontology import (
    load_all_entities,
    get_entities_by_strength,
    get_strength_distribution,
    apply_decay_to_entity,
    DECAY_THRESHOLD,
    ACCESS_DECAY_THRESHOLD_HOURS,
    GRAPH_FILE,
    ONTOLOGY_DIR,
)


class DecayEngine:
    """记忆衰减引擎

    批量处理所有实体，应用基于时间的衰减，并归档 weak 实体。
    """

    def __init__(self, kg_dir: Optional[str] = None):
        """初始化衰减引擎

        Args:
            kg_dir: 知识图谱目录路径（可选，默认使用 memory_ontology 配置）
        """
        # 可以通过环境变量覆盖 KG_DIR
        if kg_dir:
            os.environ['KG_DIR'] = kg_dir

        self.stats = {
            'entities_processed': 0,
            'entities_decayed': 0,
            'entities_archived': 0,
            'entities_strength_reset': 0,
            'entities_skipped': 0,
            'entities_error': 0,
        }

    def apply_decay_all(self, dry_run: bool = False) -> Dict:
        """对所有实体应用衰减

        遍历所有实体，计算自上次访问以来的衰减并应用。

        Args:
            dry_run: 如果 True，只计算不写入

        Returns:
            统计信息字典
        """
        # Pre-load all entities once to avoid O(n²) file reads
        all_entities = load_all_entities()

        stats = {
            'processed': 0,
            'decayed': 0,
            'skipped_no_last_accessed': 0,
            'skipped_recently_accessed': 0,
            'errors': 0,
        }

        for entity_id in all_entities.keys():
            entity = all_entities.get(entity_id)
            if not entity:
                stats['errors'] += 1
                continue

            stats['processed'] += 1

            # 跳过已合并的实体
            if entity['properties'].get('consolidated_into'):
                stats['skipped_recently_accessed'] += 1
                continue

            last_accessed = entity['properties'].get('last_accessed')
            if not last_accessed:
                stats['skipped_no_last_accessed'] += 1
                continue

            # 计算自上次访问以来的衰减
            try:
                from datetime import datetime
                last_dt = datetime.fromisoformat(last_accessed.replace('Z', '+00:00'))
                hours_elapsed = (datetime.now().astimezone() - last_dt).total_seconds() / 3600

                if hours_elapsed >= ACCESS_DECAY_THRESHOLD_HOURS:
                    days_elapsed = hours_elapsed / 24.0
                    old_strength = entity['properties'].get('strength', 1.0)

                    if not dry_run:
                        new_strength = apply_decay_to_entity(entity_id, days_elapsed)
                    else:
                        # 模拟计算
                        decay_rate = entity['properties'].get('decay_rate', 0.95)
                        months_elapsed = days_elapsed / 30.0
                        new_strength = old_strength * (decay_rate ** months_elapsed)
                        new_strength = max(0.0, min(1.0, new_strength))

                    stats['decayed'] += 1
                else:
                    stats['skipped_recently_accessed'] += 1

            except (ValueError, TypeError):
                stats['errors'] += 1
                continue

        # 更新全局统计
        self.stats['entities_processed'] += stats['processed']
        self.stats['entities_decayed'] += stats['decayed']
        self.stats['entities_skipped'] += stats['skipped_no_last_accessed'] + stats['skipped_recently_accessed']
        self.stats['entities_error'] += stats['errors']

        return stats

    def archive_weak(self, dry_run: bool = False) -> Dict:
        """归档 weak 实体

        找出 strength 低于阈值的实体，标记为 archived 状态。

        Args:
            dry_run: 如果 True，只计算不写入

        Returns:
            统计信息字典
        """
        stats = {
            'weak_candidates': 0,
            'archived': 0,
            'skipped_consolidated': 0,
            'skipped_already_archived': 0,
            'errors': 0,
        }

        weak_entities = get_entities_by_strength(DECAY_THRESHOLD)
        stats['weak_candidates'] = len(weak_entities)

        for entity in weak_entities:
            entity_id = entity['id']
            props = entity['properties']

            # 跳过已合并的实体
            if props.get('consolidated_into'):
                stats['skipped_consolidated'] += 1
                continue

            # 跳过已归档的实体
            if props.get('status') == 'archived':
                stats['skipped_already_archived'] += 1
                continue

            # Phase 8: 高显著性实体衰减更慢
            # 有效阈值 = DECAY_THRESHOLD + (0.3 - significance) * 0.1
            # 高显著性 (0.8) -> threshold = 0.13
            # 低显著性 (0.3) -> threshold = 0.07
            significance = props.get('significance_score', 0.5)
            effective_threshold = DECAY_THRESHOLD + (0.3 - significance) * 0.1
            current_strength = props.get('strength', 1.0)

            # 如果当前强度仍高于有效阈值，跳过
            if current_strength >= effective_threshold:
                continue

            if not dry_run:
                try:
                    _archive_entity(entity_id)
                    stats['archived'] += 1
                except Exception:
                    stats['errors'] += 1
                    continue
            else:
                stats['archived'] += 1

        # 更新全局统计
        self.stats['entities_archived'] += stats['archived']

        return stats

    def run(self, dry_run: bool = False) -> Dict:
        """运行完整的衰减周期

        1. 对所有实体应用衰减
        2. 归档 weak 实体

        Args:
            dry_run: 如果 True，只计算不写入

        Returns:
            完整统计信息字典
        """
        print(f"\n{'='*60}")
        print(f"Memory Decay Engine {'(DRY RUN)' if dry_run else ''}")
        print(f"{'='*60}\n")

        # 1. 应用衰减
        print("Step 1: 应用衰减...")
        decay_stats = self.apply_decay_all(dry_run)
        print(f"  处理: {decay_stats['processed']} 实体")
        print(f"  衰减: {decay_stats['decayed']} 实体")
        print(f"  跳过: {decay_stats['skipped_no_last_accessed']} (无last_accessed)")
        print(f"  跳过: {decay_stats['skipped_recently_accessed']} (最近访问)")
        print(f"  错误: {decay_stats['errors']}")

        # 2. 归档 weak 实体
        print("\nStep 2: 归档 weak 实体...")
        archive_stats = self.archive_weak(dry_run)
        print(f"  候选: {archive_stats['weak_candidates']} 实体")
        print(f"  归档: {archive_stats['archived']} 实体")
        print(f"  跳过: {archive_stats['skipped_consolidated']} (已合并)")
        print(f"  跳过: {archive_stats['skipped_already_archived']} (已归档)")
        print(f"  错误: {archive_stats['errors']}")

        print(f"\n{'='*60}")
        print("统计汇总:")
        print(f"  实体处理: {self.stats['entities_processed']}")
        print(f"  实体衰减: {self.stats['entities_decayed']}")
        print(f"  实体归档: {self.stats['entities_archived']}")
        print(f"  实体跳过: {self.stats['entities_skipped']}")
        print(f"  错误计数: {self.stats['entities_error']}")
        print(f"{'='*60}\n")

        return self.stats


def _archive_entity(entity_id: str) -> bool:
    """标记实体为 archived 状态

    使用 op: update 模式标记实体状态。
    """
    import json
    import fcntl
    from datetime import datetime

    now = datetime.now().astimezone().isoformat()

    update_op = {
        "op": "update",
        "entity": {
            "id": entity_id,
            "properties": {"status": "archived"},
            "updated": now
        },
        "timestamp": now
    }

    # 原子写入
    lock_file = GRAPH_FILE.with_suffix('.lock')
    with open(lock_file, 'w') as lock_f:
        fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX)
        try:
            with open(GRAPH_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(update_op, ensure_ascii=False) + '\n')
        finally:
            fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)

    return True


def show_stats():
    """显示记忆强度统计"""
    entities = load_all_entities()
    print(f"\n{'='*60}")
    print("Memory Decay Stats")
    print(f"{'='*60}\n")

    print(f"实体总数: {len(entities)}")

    # Strength 分布
    print(f"\n记忆强度分布:")
    dist = get_strength_distribution()
    for entity_type, stats in sorted(dist.items()):
        avg = stats.get('avg_strength', 0)
        bar_len = int(avg * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"  {entity_type}: [{bar}] {avg:.0%} (count={stats['count']})")

    # Weak 候选
    print(f"\nWeak 候选 (strength < {DECAY_THRESHOLD}):")
    weak = get_entities_by_strength(DECAY_THRESHOLD)
    print(f"  数量: {len(weak)}")

    if weak:
        print(f"\n  候选实体:")
        for entity in weak[:10]:
            props = entity['properties']
            title = props.get('title', entity['id'])
            strength = props.get('strength', 0)
            status = props.get('status', 'active')
            print(f"    - {entity['id']}: {title} (strength={strength:.3f}, status={status})")
        if len(weak) > 10:
            print(f"    ... 还有 {len(weak) - 10} 个")

    print(f"\n{'='*60}\n")


def show_candidates():
    """显示待归档候选实体"""
    weak = get_entities_by_strength(DECAY_THRESHOLD)
    consolidated = [e for e in weak if e['properties'].get('consolidated_into')]

    print(f"\n{'='*60}")
    print(f"Weak 实体候选 (strength < {DECAY_THRESHOLD})")
    print(f"{'='*60}\n")

    print(f"总数: {len(weak)}")
    print(f"已合并: {len(consolidated)}")
    print(f"待归档: {len(weak) - len(consolidated)}")

    if weak:
        print(f"\n候选列表:")
        for entity in weak:
            props = entity['properties']
            title = props.get('title', entity['id'])
            strength = props.get('strength', 0)
            status = props.get('status', 'active')
            consolidated = props.get('consolidated_into', '')
            archived = ' [已归档]' if status == 'archived' else ''
            merged = f' [已合并到 {consolidated}]' if consolidated else ''
            print(f"  {entity['id']}: {title}")
            print(f"    strength={strength:.4f}, status={status}{archived}{merged}")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Memory Decay Engine - 批量衰减引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/decay_engine.py run          # 运行完整衰减周期
  python3 scripts/decay_engine.py run --dry-run  # 模拟运行
  python3 scripts/decay_engine.py stats        # 查看统计
  python3 scripts/decay_engine.py candidates   # 查看候选实体
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # run 命令
    run_parser = subparsers.add_parser('run', help='运行衰减周期')
    run_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='模拟运行，不写入任何更改'
    )

    # stats 命令
    subparsers.add_parser('stats', help='显示统计信息')

    # candidates 命令
    subparsers.add_parser('candidates', help='显示待归档候选实体')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 确保 ontology 目录存在
    ONTOLOGY_DIR.mkdir(parents=True, exist_ok=True)
    if not GRAPH_FILE.exists():
        GRAPH_FILE.touch()

    if args.command == 'run':
        engine = DecayEngine()
        engine.run(dry_run=args.dry_run)

    elif args.command == 'stats':
        show_stats()

    elif args.command == 'candidates':
        show_candidates()


if __name__ == '__main__':
    main()
