#!/usr/bin/env python3
"""
core/entity_heat.py — Infoseek 实体热度预测（v2.4.0 MINOR 新增）

V2.3.0/v2.3.1 提供的是实体「当前热度」（hit_count_30d + 衰减）。
V2.4.0 引入预测：根据历史时间序列预测 days_ahead 天后的衰减后热度，
区分 rising/stable/falling 三档，给上层做"哪个实体即将变火"的判断。

数据源：
  ① entity_tracker（v2.1.0）→ 当前 hit_count_30d + last_seen_at
  ② claim_store（v2.3.1）→ 历史时间序列

主接口：
  predict_heat(name, days_ahead=7) → {
    'entity': str,
    'current_heat': float,
    'predicted_heat': float,
    'trend': 'rising|stable|falling',
    'confidence': float,
    'last_seen': iso_date,
    'days_since_last_seen': int,
    'recommendation': 'hot|warm|cold|stale'
  }

  get_heat_ranking(top_n=20) → [predict_heat dict] 按 predicted_heat 降序

CLI: python core/entity_heat.py [name] [days_ahead]
      python core/entity_heat.py --ranking [top_n]
"""

import sys
import math
import datetime
from pathlib import Path
from typing import List, Dict, Optional

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))


def _safe_load_tracker():
    """v2.4.2 PATCH (P2): 返回模块级 EntityTracker 单例"""
    try:
        from entity_tracker import get_tracker
        return get_tracker(), _date_diff_days  # 同时返回 diff_fn
    except Exception:
        return None, None


def _date_diff_days(date_str: str, base: Optional['datetime.date'] = None) -> int:
    """计算 days since（从 entity_tracker 导入的回退）"""
    try:
        from entity_tracker import _date_diff_days as _real_fn
        return _real_fn(date_str, base)
    except Exception:
        return 999


def _safe_load_claim_store():
    """v2.4.3 PATCH (P2): 用 ClaimStore 单例"""
    try:
        from claim_store import get_claim_store
        return get_claim_store()
    except Exception:
        return None


def _linear_trend(daily_counts: List[int]) -> float:
    """简单线性回归斜率（每天变化量）
    daily_counts 按时间升序，长度 0/1 时返回 0
    """
    n = len(daily_counts)
    if n < 2:
        return 0.0
    xs = list(range(n))
    mean_x = (n - 1) / 2
    mean_y = sum(daily_counts) / n
    num = sum((xs[i] - mean_x) * (daily_counts[i] - mean_y) for i in range(n))
    den = sum((xs[i] - mean_x) ** 2 for i in range(n))
    return num / den if den > 0 else 0.0


def _classify_trend(slope: float, mean_y: float) -> str:
    if mean_y < 0.5:
        return 'stable'
    rel = slope / max(mean_y, 1)
    if rel > 0.1:
        return 'rising'
    if rel < -0.1:
        return 'falling'
    return 'stable'


def _recommendation(predicted: float, days_since: int) -> str:
    if days_since > 30:
        return 'stale'
    if predicted >= 5:
        return 'hot'
    if predicted >= 1:
        return 'warm'
    return 'cold'


def _confidence_from_samples(n_samples: int, days_ahead: int) -> float:
    """样本量 + 预测跨度 → 置信度（0-1）"""
    if n_samples == 0:
        return 0.0
    # 样本越多越好，预测越远越差
    sample_score = min(1.0, math.log2(n_samples + 1) / 4.0)
    horizon_penalty = max(0.3, 1.0 - days_ahead * 0.05)
    return round(sample_score * horizon_penalty, 2)


def _predict_heat_error(name: str, days_ahead: int, source: str, err: str) -> Dict:
    """v2.4.1 PATCH: predict_heat 容错降级字典（DEF-C）"""
    return {
        'entity': name,
        'current_heat': 0.0,
        'predicted_heat': 0.0,
        'trend': 'unknown',
        'confidence': 0.0,
        'last_seen': None,
        'days_since_last_seen': 999,
        'recommendation': 'cold',
        'days_ahead': days_ahead,
        'history_samples': 0,
        'slope_per_day': 0.0,
        'error_source': source,
        'error': err,
    }


def predict_heat(name: str, days_ahead: int = 7,
                 tracker=None, claim_store=None) -> Dict:
    """预测单个实体的 days_ahead 天后热度

    参数:
        name: canonical 实体名
        days_ahead: 向前预测天数（默认 7）
        tracker / claim_store: 可选依赖注入（None = 自动加载）

    返回预测字典
    """
    if tracker is not None:
        tr = tracker
        try:
            from entity_tracker import _date_diff_days
            diff_fn = _date_diff_days
        except Exception:
            diff_fn = None
    else:
        tr, diff_fn = _safe_load_tracker()
    store = claim_store if claim_store is not None else _safe_load_claim_store()

    # v2.4.1 PATCH: DEF-C 容错 — tracker/store 抛错时不崩溃，返回默认值
    current_heat = 0.0
    last_seen = None
    days_since = 999
    try:
        if tr is not None:
            ent = tr._find_entity(name)
            if ent:
                current_heat = float(ent.get('hit_count_30d', 0))
                last_seen = ent.get('last_seen_at')
                if last_seen and diff_fn:
                    days_since = diff_fn(last_seen)
    except Exception as e:
        return _predict_heat_error(name, days_ahead, 'tracker', str(e))

    # 历史时间序列（claim_store）
    daily_counts = []
    n_samples = 0
    today = datetime.date.today()
    recent_count_30d = 0  # v2.4.2 PATCH (DEF-A): claim_store 30天声明数兜底
    try:
        if store is not None:
            claims = store.get_claims(name)
            per_day = {}
            for c in claims:
                ts = c.get('timestamp', '')
                try:
                    d = datetime.date.fromisoformat(ts)
                except Exception:
                    continue
                per_day[d] = per_day.get(d, 0) + 1
                # DEF-A: 30 天内的声明计为活跃声明
                if (today - d).days <= 30:
                    recent_count_30d += 1
            sorted_days = sorted(per_day.items())
            daily_counts = [v for _, v in sorted_days[-90:]]
            n_samples = len(daily_counts)
    except Exception as e:
        return _predict_heat_error(name, days_ahead, 'claim_store', str(e))

    # v2.4.2 PATCH (DEF-A): tracker hit=0 时用 claim_store 30天声明数兜底
    current_heat = max(current_heat, float(recent_count_30d))

    # 线性趋势 + 衰减外推
    slope = _linear_trend(daily_counts)
    mean = sum(daily_counts) / max(len(daily_counts), 1)
    trend_increment = slope * days_ahead
    trend_value = max(0, mean + trend_increment)
    # 若 stale（days_since>30）走衰减分支
    if days_since > 30:
        # 90 天半衰期
        decay_factor = 0.5 ** (days_ahead / 90)
        predicted = current_heat * decay_factor
    else:
        # 活跃实体：当前值 + 趋势增量 + 短期衰减
        decay_factor = 0.5 ** (days_ahead / 90)
        # v2.4.2 PATCH (DEF-B 方案B): trend_weight 加权防止 current=0 时趋势"无中生有"
        # 当前活跃度越高，趋势外推权重越大；current=0 时 trend_weight=0 跳过趋势
        trend_weight = min(1.0, current_heat / max(mean, 1.0))
        predicted = max(0, current_heat * decay_factor + trend_value * 0.3 * trend_weight)

    trend = _classify_trend(slope, mean)
    rec = _recommendation(predicted, days_since)
    conf = _confidence_from_samples(n_samples, days_ahead)

    return {
        'entity': name,
        'current_heat': round(current_heat, 2),
        'predicted_heat': round(predicted, 2),
        'trend': trend,
        'confidence': conf,
        'last_seen': last_seen,
        'days_since_last_seen': days_since,
        'recommendation': rec,
        'days_ahead': days_ahead,
        'history_samples': n_samples,
        'slope_per_day': round(slope, 3),
    }


def get_heat_ranking(top_n: int = 20, days_ahead: int = 7) -> List[Dict]:
    """返回全实体按 predicted_heat 降序的排名"""
    tr, _ = _safe_load_tracker()
    if tr is None:
        return []
    entities = tr._all_entities()
    scored = []
    for e in entities:
        name = e.get('name')
        if not name:
            continue
        pred = predict_heat(name, days_ahead=days_ahead, tracker=tr)
        if pred['recommendation'] in ('stale', 'cold') and pred['current_heat'] == 0:
            continue
        scored.append(pred)
    scored.sort(key=lambda x: (-x['predicted_heat'], -x['current_heat']))
    return scored[:top_n]


# v2.5.3 PATCH: predict_heat / get_heat_ranking 异步版本
# 让 MCP / async_research 等高频调用避免阻塞 event loop
async def predict_heat_async(name: str, days_ahead: int = 7,
                             tracker=None, claim_store=None) -> Dict:
    """v2.5.3 新增：predict_heat 异步版（asyncio.to_thread 包装同步实现）

    高频调用场景（如 get_heat_ranking 内 N 次 predict_heat）可并发
    """
    import asyncio
    return await asyncio.to_thread(
        predict_heat, name, days_ahead, tracker, claim_store
    )


async def get_heat_ranking_async(top_n: int = 20, days_ahead: int = 7) -> List[Dict]:
    """v2.5.3 新增：get_heat_ranking 异步版

    内部循环用 asyncio.gather 并发 predict_heat_async（每实体 1 个 task），
    避免阻塞 event loop；总时间 = max(单实体 predict_heat) 而非 sum(N)
    """
    import asyncio
    tr, _ = _safe_load_tracker()
    if tr is None:
        return []
    entities = tr._all_entities()
    # 第一遍：快速过滤（hit_total 阈值）+ 并发 predict_heat
    candidates = []
    for e in entities:
        name = e.get('name')
        if not name:
            continue
        candidates.append(name)
    if not candidates:
        return []
    scored = await asyncio.gather(
        *[predict_heat_async(n, days_ahead=days_ahead, tracker=tr) for n in candidates]
    )
    # 过滤 cold/stale + 排序
    out = []
    for s in scored:
        if s.get('recommendation') in ('stale', 'cold') and s.get('current_heat', 0) == 0:
            continue
        out.append(s)
    out.sort(key=lambda x: (-x.get('predicted_heat', 0), -x.get('current_heat', 0)))
    return out[:top_n]


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    import json as _json
    args = sys.argv[1:]
    if args and args[0] == '--ranking':
        top_n = int(args[1]) if len(args) > 1 else 20
        ranking = get_heat_ranking(top_n=top_n)
        print(_json.dumps(ranking, ensure_ascii=False, indent=2))
        return
    if not args:
        print("usage: entity_heat.py <entity_name> [days_ahead]  |  --ranking [top_n]")
        sys.exit(1)
    name = args[0]
    days = int(args[1]) if len(args) > 1 else 7
    print(_json.dumps(predict_heat(name, days_ahead=days), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
