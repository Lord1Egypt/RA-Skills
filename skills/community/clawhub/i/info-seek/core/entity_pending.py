#!/usr/bin/env python3
"""
core/entity_pending.py — Infoseek 待入库队列管理（v2.1.1 新增）

v2.1.0 entity_enricher 抽取的候选实体入 pending 队列，本模块提供：
- approve(name): 人工确认入库
- reject(name, reason): 人工拒绝
- batch_approve_high_confidence(threshold): 批量入库
- list(min_confidence): 列出队列
- CLI: list / approve / reject / batch

数据源：运行时数据目录（默认 ~/.infoseek/pending_entities.json，可由 INFOSEEK_DATA_DIR / INFOSEEK_DB 配置；与 entity_enricher 共享）
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import date

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))

try:
    from state_dir import state_path
except ImportError:  # 作为 core 包导入时
    from .state_dir import state_path

# v2.1.1 bugfix: 统一通过 core.entities 模块访问，避免双重命名空间
import core.entities as _core_entities
ORG_ENTITIES = _core_entities.ORG_ENTITIES
PRODUCT_ENTITIES = _core_entities.PRODUCT_ENTITIES
TECH_ENTITIES = _core_entities.TECH_ENTITIES
PERSON_ENTITIES = _core_entities.PERSON_ENTITIES
METRIC_ENTITIES = _core_entities.METRIC_ENTITIES


class PendingEntitiesQueue:
    """v2.1.1 待入库队列管理（v2.1.2 升级：拒绝日志）"""

    QUEUE_FILE = 'pending_entities.json'
    REJECTED_FILE = 'rejected_entities.json'  # v2.1.2 新增

    def __init__(self):
        self.path = state_path(self.QUEUE_FILE)
        self.rejected_path = state_path(self.REJECTED_FILE)  # v2.1.2

    def _load(self) -> List[Dict]:
        if not self.path.exists():
            return []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, queue: List[Dict]):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(queue, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[entity_pending] 保存失败: {e}")

    def add(self, suggestion: Dict) -> bool:
        """加入待入库队列（重复则跳过）"""
        queue = self._load()
        if any(e.get('name') == suggestion.get('name') for e in queue):
            return False
        queue.append(suggestion)
        self._save(queue)
        return True

    def list(self, min_confidence: float = 0.0,
             category: Optional[str] = None) -> List[Dict]:
        """列出待入库实体（支持过滤）"""
        queue = self._load()
        result = [
            e for e in queue
            if e.get('confidence', 0) >= min_confidence
            and (category is None or e.get('category') == category)
        ]
        return result

    def approve(self, entity_name: str) -> bool:
        """人工确认入库"""
        queue = self._load()

        # 找到 target
        target = None
        target_idx = -1
        for i, e in enumerate(queue):
            if e.get('name') == entity_name:
                target = e
                target_idx = i
                break
        if not target:
            return False

        # v2.1.1 bugfix: 使用模块顶部 import 的列表引用（避免双重命名空间）
        target_map = {
            'ORG': ORG_ENTITIES,
            'PRODUCT': PRODUCT_ENTITIES,
            'TECH': TECH_ENTITIES,
            'PERSON': PERSON_ENTITIES,
            'METRIC': METRIC_ENTITIES,
        }

        # 实际入库
        target_list = target_map.get(target.get('category'), ORG_ENTITIES)
        target_list.append(target)

        # 从队列移除
        queue.pop(target_idx)
        self._save(queue)
        return True

    def reject(self, entity_name: str, reason: str = '') -> bool:
        """人工拒绝（v2.1.2: 写入 rejected_entities.json）"""
        queue = self._load()
        rejected_entity = None
        for i, e in enumerate(queue):
            if e.get('name') == entity_name:
                rejected_entity = queue.pop(i)
                break
        if not rejected_entity:
            return False

        # v2.1.2: 写入拒绝日志
        try:
            rejected_list = []
            if self.rejected_path.exists():
                with open(self.rejected_path, 'r', encoding='utf-8') as f:
                    rejected_list = json.load(f)

            from datetime import date
            rejected_entry = {
                'name': rejected_entity.get('name'),
                'aliases': rejected_entity.get('aliases', []),
                'category': rejected_entity.get('category'),
                'confidence': rejected_entity.get('confidence'),
                'source': rejected_entity.get('source'),
                'reject_reason': reason or '人工拒绝',
                'rejected_at': date.today().isoformat(),
                'original_created_at': rejected_entity.get('created_at'),
            }
            rejected_list.append(rejected_entry)

            with open(self.rejected_path, 'w', encoding='utf-8') as f:
                json.dump(rejected_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[entity_pending] 写入拒绝日志失败: {e}")

        self._save(queue)
        return True

    def batch_approve_high_confidence(self, threshold: float = 0.85) -> int:
        """批量入库高置信度候选"""
        queue = self._load()
        high_conf = [e for e in queue if e.get('confidence', 0) >= threshold]
        approved_count = 0

        for ent in high_conf:
            if self.approve(ent['name']):
                approved_count += 1

        return approved_count

    def count(self) -> int:
        """返回队列长度"""
        return len(self._load())

    def get_rejected(self) -> list:
        """v2.1.2: 返回拒绝日志列表"""
        if not self.rejected_path.exists():
            return []
        try:
            with open(self.rejected_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def get_rejected_sorted(self, reverse: bool = True) -> list:
        """v2.1.3: 按 rejected_at 时间排序的拒绝日志"""
        rejected = self.get_rejected()
        rejected.sort(key=lambda x: x.get('rejected_at', ''), reverse=reverse)
        return rejected

    def get_rejected_by_source(self, source: str = 'llm') -> list:
        """v2.1.3: 按来源分类的拒绝日志"""
        return [r for r in self.get_rejected() if r.get('source') == source]

    def count_rejected(self) -> int:
        """v2.1.2: 拒绝日志条数"""
        return len(self.get_rejected())

    def clear_rejected(self) -> int:
        """v2.1.3: 清空拒绝日志，返回清空条数"""
        count = self.count_rejected()
        if self.rejected_path.exists():
            try:
                with open(self.rejected_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except Exception:
                pass
        return count

    # ═══════════════════════════════════════════════════════════════
    # v2.2.1: 拒绝日志生命周期（防膨胀）
    # ═══════════════════════════════════════════════════════════════

    REJECTED_RETENTION_DAYS = 180  # 拒绝记录保留天数

    def get_rejected_stats(self) -> dict:
        """v2.2.1: 拒绝日志时间分布统计

        返回: {'total': N, 'oldest': 'YYYY-MM-DD', 'newest': 'YYYY-MM-DD', 'by_month': {...}}
        """
        rejected = self.get_rejected()
        dates = [r.get('rejected_at', '') for r in rejected if r.get('rejected_at')]
        dates.sort()
        by_month = {}
        for d in dates:
            month = d[:7]  # YYYY-MM
            by_month[month] = by_month.get(month, 0) + 1
        return {
            'total': len(rejected),
            'oldest': dates[0] if dates else None,
            'newest': dates[-1] if dates else None,
            'by_month': dict(sorted(by_month.items())),
        }

    def clean_old_rejected(self, days: int = REJECTED_RETENTION_DAYS) -> dict:
        """v2.2.1: 清理 N 天前的拒绝记录（防膨胀）

        参数:
            days: 保留天数（默认 180）

        返回: {'cleaned': N, 'kept': M, 'retention_days': days}
        """
        import datetime
        rejected = self.get_rejected()
        cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        kept, cleaned = [], 0
        for r in rejected:
            rejected_at = r.get('rejected_at', '')
            if rejected_at and rejected_at < cutoff:
                cleaned += 1
                continue
            kept.append(r)
        try:
            with open(self.rejected_path, 'w', encoding='utf-8') as f:
                json.dump(kept, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return {'cleaned': cleaned, 'kept': len(kept), 'retention_days': days}

    def clear(self):
        """清空队列"""
        self._save([])


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m core.entity_pending [list | approve NAME | reject NAME | batch]")
        sys.exit(1)

    cmd = sys.argv[1]
    q = PendingEntitiesQueue()

    if cmd == 'list':
        min_conf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
        pending = q.list(min_confidence=min_conf)
        print(f"Pending 队列 ({len(pending)} 条):")
        for e in pending:
            print(f"  - {e['name']:30s} ({e.get('category')}) conf={e.get('confidence')}")
    elif cmd == 'approve':
        if len(sys.argv) < 3:
            print("Usage: python -m core.entity_pending approve NAME")
            sys.exit(1)
        name = sys.argv[2]
        success = q.approve(name)
        print(f"{'✅' if success else '❌'} approve '{name}': {success}")
    elif cmd == 'reject':
        if len(sys.argv) < 3:
            print("Usage: python -m core.entity_pending reject NAME [REASON]")
            sys.exit(1)
        name = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else ''
        success = q.reject(name, reason)
        print(f"{'✅' if success else '❌'} reject '{name}': {success}")
    elif cmd == 'batch':
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.85
        count = q.batch_approve_high_confidence(threshold)
        print(f"✅ 批量入库 {count} 个 (threshold≥{threshold})")
    elif cmd == 'clear':
        q.clear()
        print("✅ Pending 队列已清空")
    elif cmd == 'rejected':
        # v2.1.3: 查看拒绝日志（按时间排序）
        rejected = q.get_rejected_sorted()
        print(f"拒绝日志 ({len(rejected)} 条, 按时间{'倒序' if True else '顺序'}):")
        for r in rejected:
            print(f"  [{r.get('rejected_at', '?')}] {r.get('name', '?')} "
                  f"(reason={r.get('reject_reason', '?')}, source={r.get('source', '?')})")
    elif cmd == 'rejected-by-source':
        # v2.1.3: 按来源分类查看
        source = sys.argv[2] if len(sys.argv) > 2 else 'llm'
        rejected = q.get_rejected_by_source(source)
        print(f"来源 '{source}' 的拒绝日志 ({len(rejected)} 条):")
        for r in rejected:
            print(f"  [{r.get('rejected_at', '?')}] {r.get('name', '?')} "
                  f"(reason={r.get('reject_reason', '?')})")
    elif cmd == 'clear-rejected':
        # v2.1.3: 清空拒绝日志
        count = q.clear_rejected()
        print(f"✅ 已清空 {count} 条拒绝日志")
    elif cmd == 'rejected-stats':
        # v2.2.1: 拒绝日志时间分布
        import json
        print(json.dumps(q.get_rejected_stats(), ensure_ascii=False, indent=2))
    elif cmd == 'clean-rejected':
        # v2.2.1: 清理 N 天前的拒绝记录
        days = int(sys.argv[2]) if len(sys.argv) > 2 else q.REJECTED_RETENTION_DAYS
        result = q.clean_old_rejected(days=days)
        print(f"✅ 清理完成: {result}")
    elif cmd == 'count':
        print(f"队列长度: {q.count()}")
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()