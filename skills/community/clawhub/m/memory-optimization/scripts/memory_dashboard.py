#!/usr/bin/env python3
"""
Memory Health Dashboard — 可视化记忆系统健康状态

显示：
- 记忆强度分布直方图
- Consolidation 进度（SkillCards, ConflictReviews）
- 存储使用统计
- 实体年龄分布
- 衰减预测（哪些实体即将弱化）
- Memory Health Score（综合评分）

使用方法:
    python3 scripts/memory_dashboard.py              # 摘要视图
    python3 scripts/memory_dashboard.py full        # 完整视图
    python3 scripts/memory_dashboard.py decay       # 衰减预测
    python3 scripts/memory_dashboard.py compact    # 紧凑视图
    python3 scripts/memory_dashboard.py json        # JSON 输出（供其他工具使用）
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

SCRIPT_DIR = Path(__file__).parent

# Add scripts directory to path for imports
sys.path.insert(0, str(SCRIPT_DIR))
from memory_ontology import load_all_entities, ONTOLOGY_DIR, GRAPH_FILE  # noqa: E402

KG_DIR = ONTOLOGY_DIR


# ========== Health Score Weights ==========

STRENGTH_WEIGHTS = {
    'strong': 1.0,      # strength >= 0.8
    'medium': 0.5,     # strength 0.5-0.8
    'weak': 0.1,       # strength < 0.5
}

DECAY_WARNING_THRESHOLD = 0.15  # warn when entity will decay below 0.1 within 30 days


class MemoryDashboard:
    """Memory Health Dashboard — 分析和可视化记忆系统健康状态"""

    def __init__(self):
        self.entities: Dict[str, Dict] = {}
        self._loaded = False

    def _load(self):
        """Lazy load entities and schema"""
        if not self._loaded:
            self.entities = load_all_entities()
            self._loaded = True

    # ---- Computation Methods ----

    def compute_health_score(self) -> Dict[str, Any]:
        """计算综合 Memory Health Score (0-100)"""
        self._load()
        if not self.entities:
            return {'score': 0, 'grade': 'F', 'factors': {}}

        total = len(self.entities)
        strong = medium = weak = 0

        for entity in self.entities.values():
            strength = entity.get('properties', {}).get('strength', 1.0)
            if strength >= 0.8:
                strong += 1
            elif strength >= 0.5:
                medium += 1
            else:
                weak += 1

        # Weighted score
        score = (
            (strong / total) * STRENGTH_WEIGHTS['strong'] +
            (medium / total) * STRENGTH_WEIGHTS['medium'] +
            (weak / total) * STRENGTH_WEIGHTS['weak']
        ) * 100

        # Determine grade
        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'
        elif score >= 60:
            grade = 'C'
        elif score >= 40:
            grade = 'D'
        else:
            grade = 'F'

        return {
            'score': round(score, 1),
            'grade': grade,
            'factors': {
                'strong': strong,
                'medium': medium,
                'weak': weak,
                'total': total,
            }
        }

    def get_strength_histogram(self) -> Dict[str, Any]:
        """记忆强度分布直方图（每10%一个桶）"""
        self._load()
        buckets = {f'{i*10}-{i*10+10}': 0 for i in range(10)}
        buckets['100'] = 0

        for entity in self.entities.values():
            strength = entity.get('properties', {}).get('strength', 1.0)
            bucket_idx = min(int(strength * 10), 9)
            bucket_key = f'{bucket_idx*10}-{bucket_idx*10+10}'
            buckets[bucket_key] += 1

        # Compute overall stats
        strengths = [e.get('properties', {}).get('strength', 1.0) for e in self.entities.values()]
        avg = sum(strengths) / len(strengths) if strengths else 0

        return {
            'buckets': buckets,
            'avg': round(avg, 3),
            'median': sorted(strengths)[len(strengths) // 2] if strengths else 0,
        }

    def get_consolidation_progress(self) -> Dict[str, Any]:
        """Consolidation 进度统计"""
        self._load()
        skill_cards = 0
        conflict_reviews = 0
        pending_consolidation = 0

        for entity in self.entities.values():
            etype = entity['type']
            if etype == 'SkillCard':
                skill_cards += 1
            elif etype == 'ConflictReview':
                conflict_reviews += 1
            elif etype == 'Episode':
                # Episodes that might need consolidation
                props = entity.get('properties', {})
                strength = props.get('strength', 1.0)
                if strength >= 0.7:
                    pending_consolidation += 1

        return {
            'skill_cards': skill_cards,
            'conflict_reviews': conflict_reviews,
            'pending_episodes': pending_consolidation,
        }

    def get_storage_stats(self) -> Dict[str, Any]:
        """存储使用统计"""
        graph_path = GRAPH_FILE
        if graph_path.exists():
            with open(graph_path) as f:
                lines = f.readlines()
            size_kb = graph_path.stat().st_size / 1024
            line_count = len(lines)
        else:
            size_kb = 0
            line_count = 0

        self._load()
        entity_types = {}
        for entity in self.entities.values():
            t = entity['type']
            entity_types[t] = entity_types.get(t, 0) + 1

        return {
            'file_size_kb': round(size_kb, 1),
            'entity_count': len(self.entities),
            'line_count': line_count,
            'by_type': entity_types,
        }

    def get_age_distribution(self) -> Dict[str, Any]:
        """实体年龄分布（按创建时间）"""
        self._load()
        now = datetime.now(timezone.utc)
        age_buckets = {
            '< 1 week': 0,
            '1-2 weeks': 0,
            '2-4 weeks': 0,
            '1-3 months': 0,
            '> 3 months': 0,
        }

        for entity in self.entities.values():
            created_str = entity.get('created', '')
            if not created_str:
                continue
            try:
                if '+' in created_str or 'Z' in created_str:
                    created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                else:
                    created = datetime.fromisoformat(created_str)
                age_days = (now - created.replace(tzinfo=now.tzinfo)).days

                if age_days < 7:
                    age_buckets['< 1 week'] += 1
                elif age_days < 14:
                    age_buckets['1-2 weeks'] += 1
                elif age_days < 28:
                    age_buckets['2-4 weeks'] += 1
                elif age_days < 90:
                    age_buckets['1-3 months'] += 1
                else:
                    age_buckets['> 3 months'] += 1
            except (ValueError, TypeError):
                continue

        return age_buckets

    def get_decay_forecast(self) -> List[Dict[str, Any]]:
        """预测哪些实体将在未来30天内衰减到危险水平"""
        self._load()
        warnings = []

        for entity in self.entities.values():
            props = entity.get('properties', {})
            strength = props.get('strength', 1.0)
            decay_rate = props.get('decay_rate', 0.95)

            # Simple exponential decay: after 30 days
            days = 30
            future_strength = strength * (decay_rate ** (days / 30))

            if future_strength < DECAY_WARNING_THRESHOLD and strength > 0.1:
                warnings.append({
                    'id': entity['id'],
                    'type': entity['type'],
                    'title': props.get('title', entity['id']),
                    'current_strength': round(strength, 3),
                    'future_strength': round(future_strength, 3),
                    'decay_rate': decay_rate,
                    'days_to_danger': self._days_to_strength(strength, decay_rate, DECAY_WARNING_THRESHOLD),
                })

        # Sort by days_to_danger ascending
        warnings.sort(key=lambda x: x['days_to_danger'] if x['days_to_danger'] else 999)
        return warnings[:10]  # top 10 most urgent

    def _days_to_strength(self, current: float, decay_rate: float, target: float) -> Optional[int]:
        """计算从 current 衰减到 target 需要多少天"""
        if current <= target:
            return 0
        if decay_rate >= 1.0:
            return None  # won't decay
        # exponential decay: target = current * decay_rate^(days/30)
        # days = 30 * log(target/current) / log(decay_rate)
        try:
            days = 30 * math.log(target / current) / math.log(decay_rate)
            return round(days) if days > 0 else None
        except (ValueError, ZeroDivisionError):
            return None

    def get_tag_cloud(self) -> Dict[str, int]:
        """标签云 — 最常用的标签"""
        self._load()
        tag_counts: Dict[str, int] = {}
        for entity in self.entities.values():
            tags = entity.get('properties', {}).get('tags', [])
            for tag in tags:
                if isinstance(tag, str) and tag.startswith('#'):
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return dict(sorted(tag_counts.items(), key=lambda x: -x[1])[:20])

    def get_provenance_breakdown(self) -> Dict[str, int]:
        """来源分类统计"""
        self._load()
        provenance: Dict[str, int] = {}
        for entity in self.entities.values():
            provs = entity.get('properties', {}).get('provenance', [])
            for p in provs:
                if isinstance(p, str):
                    # Normalize: extract the source type (e.g., 'inference:preference_engine' -> 'inference')
                    key = p.split(':')[0] if ':' in p else p
                    provenance[key] = provenance.get(key, 0) + 1
        return provenance

    # ---- Rendering Methods ----

    def render_health_score(self) -> str:
        """渲染 Health Score 卡片"""
        health = self.compute_health_score()
        f = health['factors']
        total = f['total']
        pct = lambda n: f'{n/total*100:.0f}%' if total else '0%'

        grade_colors = {'A': '🟢', 'B': '🔵', 'C': '🟡', 'D': '🟠', 'F': '🔴'}
        emoji = grade_colors.get(health['grade'], '⚪')

        def bar_str(n, width=20):
            b = '█' * (n * width // max(total, 1))
            return b.ljust(width)

        return f"""
╔══════════════════════════════════════════════════════════════╗
║                  🧠 MEMORY HEALTH SCORE                       ║
╠══════════════════════════════════════════════════════════════╣
║  Overall: {emoji} Grade {health['grade']}  ({health['score']}/100)                    ║
║                                                              ║
║  Strong (≥80%):   {pct(f['strong']):>5}  █{bar_str(f['strong']):<20} ║
║  Medium (50-80%): {pct(f['medium']):>5}  █{bar_str(f['medium']):<20} ║
║  Weak (<50%):    {pct(f['weak']):>5}  █{bar_str(f['weak']):<20} ║
║                                                              ║
║  Total Entities: {f['total']}                                         ║
╚══════════════════════════════════════════════════════════════╝"""

    def render_strength_histogram(self) -> str:
        """渲染记忆强度直方图"""
        hist = self.get_strength_histogram()
        buckets = hist['buckets']
        max_count = max(buckets.values()) if buckets else 1

        lines = ['\n📊 MEMORY STRENGTH DISTRIBUTION']
        lines.append('─' * 52)
        lines.append(f"  Average: {hist['avg']:.0%}   Median: {hist['median']:.0%}")
        lines.append('─' * 52)

        bucket_keys = ['0-10', '10-20', '20-30', '30-40', '40-50',
                       '50-60', '60-70', '70-80', '80-90', '90-100']
        for key in bucket_keys:
            count = buckets.get(f'{key}', 0)
            bar_len = int(count / max(max_count, 1) * 30) if max_count else 0
            bar = '█' * bar_len
            lines.append(f"  {key:>7}% |{bar:<30}| {count:>4}")

        lines.append('─' * 52)
        return '\n'.join(lines)

    def render_consolidation_progress(self) -> str:
        """渲染 Consolidation 进度"""
        progress = self.get_consolidation_progress()
        total = sum(progress.values())

        return f"""
🔗 CONSOLIDATION PROGRESS
{'─' * 40}
  SkillCards (semantic memory):   {progress['skill_cards']:>4}
  ConflictReviews (pending):      {progress['conflict_reviews']:>4}
  Episodes ready for merge:        {progress['pending_episodes']:>4}
{'':─<40}
  Consolidation coverage:         {progress['skill_cards'] / max(total, 1) * 100:>4.0f}%"""

    def render_storage_stats(self) -> str:
        """渲染存储统计"""
        stats = self.get_storage_stats()
        types_lines = '\n'.join(
            f"    {t}: {c}" for t, c in sorted(stats['by_type'].items(), key=lambda x: -x[1])
        )
        return f"""
💾 STORAGE STATS
{'─' * 40}
  File:        {stats['file_size_kb']:.1f} KB
  Entities:    {stats['entity_count']}
  By type:     {types_lines if types_lines else '  (none)'}"""

    def render_decay_forecast(self) -> str:
        """渲染衰减预测"""
        warnings = self.get_decay_forecast()
        if not warnings:
            return """
⚠️  DECAY FORECAST (30-day)
{'─' * 40}
  ✅ No entities at immediate risk"""

        lines = ['''
⚠️  DECAY FORECAST (30-day)
''' + '─' * 52]
        lines.append(f"  {'Entity':<25} {'Type':<12} {'Now':>6} {'30d':>6} {'Days':>5}")
        lines.append('─' * 52)
        for w in warnings[:8]:
            days = w['days_to_danger'] if w['days_to_danger'] else 'N/A'
            lines.append(
                f"  {w['title'][:24]:<25} {w['type']:<12} "
                f"{w['current_strength']:>5.0%} {w['future_strength']:>5.0%} {str(days):>5}"
            )
        return '\n'.join(lines)

    def render_age_distribution(self) -> str:
        """渲染年龄分布"""
        ages = self.get_age_distribution()
        total = sum(ages.values())
        max_val = max(ages.values()) if ages else 1

        lines = ['\n📅 ENTITY AGE DISTRIBUTION']
        lines.append('─' * 44)
        for label, count in ages.items():
            bar_len = int(count / max(max_val, 1) * 24)
            bar = '█' * bar_len
            pct = f'{count/total*100:.0f}%' if total else '0%'
            lines.append(f"  {label:<14}|{bar:<24}| {count:>3} ({pct})")
        lines.append('─' * 44)
        return '\n'.join(lines)

    def render_tag_cloud(self) -> str:
        """渲染标签云"""
        tags = self.get_tag_cloud()
        if not tags:
            return '\n🏷️  TAG CLOUD\n  (no tags found)'
        tag_str = '  '.join(f'{tag}({c})' for tag, c in list(tags.items())[:10])
        return f"""
🏷️  TOP TAGS
{'─' * 44}
  {tag_str}"""

    def render_full(self) -> str:
        """渲染完整仪表盘"""
        self._load()
        parts = [
            self.render_health_score(),
            self.render_strength_histogram(),
            self.render_consolidation_progress(),
            self.render_storage_stats(),
            self.render_decay_forecast(),
            self.render_age_distribution(),
            self.render_tag_cloud(),
        ]
        return '\n'.join(parts)

    def render_compact(self) -> str:
        """渲染紧凑视图"""
        health = self.compute_health_score()
        stats = self.get_storage_stats()
        consolidation = self.get_consolidation_progress()
        hist = self.get_strength_histogram()
        return (
            f"🧠 Memory Health: {health['grade']}({health['score']}) | "
            f"Entities: {stats['entity_count']} | "
            f"SkillCards: {consolidation['skill_cards']} | "
            f"Avg Strength: {hist['avg']:.0%}"
        )

    def render_json(self) -> str:
        """JSON 输出"""
        self._load()
        data = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'health_score': self.compute_health_score(),
            'strength_histogram': self.get_strength_histogram(),
            'consolidation': self.get_consolidation_progress(),
            'storage': self.get_storage_stats(),
            'decay_forecast': self.get_decay_forecast(),
            'age_distribution': self.get_age_distribution(),
            'tag_cloud': self.get_tag_cloud(),
            'provenance': self.get_provenance_breakdown(),
        }
        return json.dumps(data, indent=2, ensure_ascii=False)


# ========== CLI ==========

def main():
    parser = argparse.ArgumentParser(description='Memory Health Dashboard')
    parser.add_argument(
        'view', nargs='?', default='summary',
        choices=['summary', 'full', 'decay', 'compact', 'json'],
        help='Dashboard view (default: summary)'
    )
    args = parser.parse_args()

    dashboard = MemoryDashboard()

    # Handle JSON view separately
    if args.view == 'json':
        print(dashboard.render_json())
        return

    # Header
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"\n{'='*56}")
    print(f"  🧠  Agent Memory Health Dashboard  |  {now}")
    print(f"{'='*56}")

    if args.view == 'summary':
        print(dashboard.render_health_score())
        print(dashboard.render_strength_histogram())
        print(dashboard.render_consolidation_progress())
        print(dashboard.render_storage_stats())
        print(dashboard.render_decay_forecast())

    elif args.view == 'full':
        print(dashboard.render_full())

    elif args.view == 'decay':
        print(dashboard.render_decay_forecast())
        print(dashboard.render_age_distribution())

    elif args.view == 'compact':
        print(dashboard.render_compact())

    print()  # trailing newline


if __name__ == '__main__':
    main()
