#!/usr/bin/env python3
"""
core/entity_trajectory.py — Infoseek 跨会话实体轨迹（v2.4.0 MINOR 新增）

V2.3.0/v2.3.1 的 entity_profile 只存 first_seen/last_seen/topics（粗粒度）。
V2.4.0 引入轨迹函数，从两个数据源拼接：

  ① claim_store（v2.3.1 持久）→ 时间序列（date, claim_count）
  ② entity_profiles（v2.3.0）→ first_seen/last_seen + topics 聚合

主接口：
  trace_entity(name, days_back=90) → {
    'entity': str,
    'timeline': [{date, claim_count, sources_count, topic_hits, conflict_flag}],
    'subjects_seen': [str],        # 推断自 sources 的主题词
    'total_occurrences': int,
    'active_days': int,
    'avg_claims_per_day': float,
    'is_rising': bool,             # 近 7 天 vs 前 7 天对比
  }

CLI: python core/entity_trajectory.py <entity_name> [days_back]
"""

import sys
import datetime
from collections import Counter
from pathlib import Path
from typing import List, Dict, Optional

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))


def _safe_load_claim_store():
    """v2.4.3 PATCH (P2): 用 ClaimStore 单例（共享 DEFAULT_FILE）"""
    try:
        from claim_store import get_claim_store
        return get_claim_store()
    except Exception:
        return None


def _truncate_subject(title: str, limit: int = 40) -> str:
    """主题词截断（P3 词边界修复：避免 title[:20] 在中文标题中被拦腰截断）

    优先按标点/空格切到句首完整段；无分隔符时按 limit 截断。
    """
    t = (title or '').strip()
    if len(t) <= limit:
        return t
    for sep in ('，', '。', '；', '、', ',', '.', ';', ' '):
        head = t.split(sep, 1)[0].strip()
        if 0 < len(head) < limit:
            return head
    return t[:limit]


def _safe_load_profile():
    """v2.4.3 PATCH (P2): 用 EntityProfile 单例"""
    try:
        from entity_profile import get_profile
        return get_profile()
    except Exception:
        return None


def _safe_extract_topics(text: str, limit: int = 5) -> List[str]:
    try:
        from entity_profile import EntityProfile
        return EntityProfile._extract_topics(None, text, limit)  # type: ignore
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════
# 主入口：trace_entity
# ═══════════════════════════════════════════════════════════

def trace_entity(name: str, days_back: int = 90,
                 claim_store=None, profile=None) -> Dict:
    """追踪实体在 days_back 天窗口内的时间轨迹

    参数:
        name: canonical 实体名
        days_back: 回溯天数（默认 90）
        claim_store: 可选 ClaimStore 实例（None = 自动加载）
        profile: 可选 EntityProfile 实例（None = 自动加载）

    返回轨迹字典（见模块 docstring）
    """
    store = claim_store if claim_store is not None else _safe_load_claim_store()
    prof = profile if profile is not None else _safe_load_profile()

    # 时间窗
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days_back)

    # ① claim_store 时间序列
    timeline: Dict[str, Dict] = {}
    sources_count: Counter = Counter()
    subjects_seen: set = set()
    total = 0
    if store is not None:
        claims = store.get_claims(name)
        for c in claims:
            ts = c.get('timestamp', '')
            try:
                d = datetime.date.fromisoformat(ts)
            except Exception:
                continue
            if d < start or d > today:
                continue
            bucket = timeline.setdefault(ts, {
                'date': ts,
                'claim_count': 0,
                'sources_count': 0,
                'topic_hits': [],
                'conflict_flag': False,
            })
            bucket['claim_count'] += 1
            src = c.get('source', '')
            if src:
                sources_count[src] += 1
            bucket['sources_count'] = len([k for k, v in sources_count.items() if v > 0])
            title = c.get('source_title', '')
            if title:
                topics = _safe_extract_topics(title)
                for t in topics:
                    if t and t not in bucket['topic_hits']:
                        bucket['topic_hits'].append(t)
                # 用 source_title 推断 subject
                if len(title) > 3:
                    subjects_seen.add(title[:20])
            total += 1

    # ② profile 兜底（取 first_seen/last_seen/topics）
    profile_topics = []
    last_seen = None
    first_seen = None
    if prof is not None:
        p = prof.get_profile(name)
        if p:
            profile_topics = p.get('topics', [])
            last_seen = p.get('last_seen')
            first_seen = p.get('first_seen')
            if first_seen:
                try:
                    d = datetime.date.fromisoformat(first_seen)
                    if start <= d <= today and first_seen not in timeline:
                        timeline[first_seen] = {
                            'date': first_seen, 'claim_count': 0,
                            'sources_count': 0, 'topic_hits': profile_topics[:3],
                            'conflict_flag': False,
                        }
                except Exception:
                    pass

    # 排序 + 整合
    timeline_list = sorted(timeline.values(), key=lambda x: x['date'])
    active_days = len(timeline_list)
    avg = round(total / max(active_days, 1), 2)

    # rising 判断：近 7 vs 前 7
    last7 = sum(b['claim_count'] for b in timeline_list
                if _safe_datedelta(today, b['date']) <= 7)
    prev_keys = [b for b in timeline_list if 7 < _safe_datedelta(today, b['date']) <= 14]
    prev7 = sum(b['claim_count'] for b in prev_keys)
    is_rising = last7 > prev7 and last7 > 0

    return {
        'entity': name,
        'timeline': timeline_list,
        'subjects_seen': sorted(subjects_seen)[:10],
        'total_occurrences': total,
        'active_days': active_days,
        'avg_claims_per_day': avg,
        'is_rising': is_rising,
        'first_seen': first_seen,
        'last_seen': last_seen,
        'profile_topics': profile_topics,
        'window': {'start': start.isoformat(), 'end': today.isoformat(), 'days': days_back},
    }


def _safe_datedelta(today: datetime.date, iso_date: str) -> int:
    try:
        d = datetime.date.fromisoformat(iso_date)
        return (today - d).days
    except Exception:
        return 999999


# ═══════════════════════════════════════════════════════════
# 多实体批量
# ═══════════════════════════════════════════════════════════

def trace_entities(names: List[str], days_back: int = 90) -> List[Dict]:
    """批量追踪多个实体的轨迹"""
    return [trace_entity(n, days_back=days_back) for n in names]


# v2.5.3 PATCH: trace_entity 异步版本
async def trace_entity_async(name: str, days_back: int = 90,
                             claim_store=None, profile=None) -> Dict:
    """v2.5.3 新增：trace_entity 异步版（asyncio.to_thread 包装）"""
    import asyncio
    return await asyncio.to_thread(
        trace_entity, name, days_back, claim_store, profile
    )


async def trace_entities_async(names: List[str], days_back: int = 90) -> List[Dict]:
    """v2.5.3 新增：批量 trace（asyncio.gather 并发）"""
    import asyncio
    return await asyncio.gather(
        *[trace_entity_async(n, days_back=days_back) for n in names]
    )


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    import json as _json
    if len(sys.argv) < 2:
        print("usage: entity_trajectory.py <entity_name> [days_back]")
        sys.exit(1)
    name = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    res = trace_entity(name, days_back=days)
    print(_json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
