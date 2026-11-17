#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trust_sources.py — 双源合并后唯一真源加载器 (v2.0)

数据来源：references/trusted-sources.v2.json
  white_list  (85条, 迁移自 py 硬编码 TIER1/2/3)
  kb_sources  (29条, 原 json trusted-sources.json)
公共 API（向后兼容签名，调用方零改动）：
  get_all_sources / compute_trust_bonus / get_tier_level /
  list_sources_by_domain / build_pattern_index / query_pattern_index /
  clear_pattern_index_cache
mtime 感知：v2.json 热改自动失效重载（与 conflict_weight L1 底座一致）。
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple

# G8-apply: 公共入口类型契约守卫（纯 stdlib，scripts/entry_guard.py）
import sys as _eg_sys
_eg_dir = str(Path(__file__).resolve().parent.parent / 'scripts')
if _eg_dir not in _eg_sys.path:
    _eg_sys.path.insert(0, _eg_dir)
from entry_guard import (require_text, require_mapping, require_sequence, coerce_mapping_list)

CORE_DIR = Path(__file__).parent
V2_PATH = CORE_DIR.parent / 'references' / 'trusted-sources.json'

# ── mtime 感知加载（复用 L1 底座） ──────────────────────────────────────
_V2_CACHE: Dict[int, Dict[str, List[dict]]] = {}
_V2_CACHE_MTIME: float = None
_PATTERN_HASH_CACHE: Dict[str, Dict[str, Tuple[int, int]]] = {}
_URL_QUERY_CACHE: Dict[Tuple[str, str], Tuple[int, int]] = {}


def _load_v2(force: bool = False) -> Dict[int, Dict[str, List[dict]]]:
    """按 tier 重建 {tier_num: {domain_key: [sources]}}。mtime 变化自动失效重载。

    失败语义：v2.json 缺失 → 空 tier（调用方降级到默认分，不抛）。
    """
    global _V2_CACHE, _V2_CACHE_MTIME
    try:
        m = V2_PATH.stat().st_mtime
    except FileNotFoundError:
        return {1: {}, 2: {}, 3: {}}
    if _V2_CACHE and not force and _V2_CACHE_MTIME == m:
        return _V2_CACHE
    data = json.loads(V2_PATH.read_text(encoding='utf-8'))
    tiers: Dict[int, Dict[str, List[dict]]] = {1: {}, 2: {}, 3: {}}
    for s in data.get('white_list', []):
        tiers.setdefault(s.get('tier', 4), {}).setdefault(
            s.get('domain_key', 'general'), []).append(s)
    # mtime 变了 → 重建并清派生缓存（pattern index / url query cache）
    _PATTERN_HASH_CACHE.clear()
    _URL_QUERY_CACHE.clear()
    _V2_CACHE = tiers
    _V2_CACHE_MTIME = m
    return tiers


def get_all_sources(domain: str = 'general') -> List[Dict]:
    """获取某领域的所有信任源（合并 tier1+tier2+tier3）"""
    t = _load_v2()
    sources = []
    for tier_num in (1, 2, 3):
        sources.extend(t[tier_num].get(domain, []) + t[tier_num].get('general', []))
    return sources


def compute_trust_bonus(url: str, domain: str = 'general', platform: str = '') -> int:
    """计算单个源在指定领域的信任加权（0-30）。

    v2.0：pattern 子串通道仅来自 white_list（含 patterns/tier/weight）。
    """
    # G8-apply: 类型契约守卫（允许 None 透传降级，拒绝 int/float/dict 等非文本）
    if url is not None and not isinstance(url, str):
        raise TypeError(f"url 需为文本(str)或 None，收到 {type(url).__name__}: {url!r}")
    url_lower = (url or '').lower()
    platform_lower = (platform or '').lower()
    bonus = 0
    idx = build_pattern_index(domain)
    for pat, (_tier, weight) in idx.items():
        if pat in url_lower or pat in platform_lower:
            bonus += weight
    return min(bonus, 30)


def get_tier_level(url: str, domain: str = 'general') -> int:
    """返回源的 tier 等级（1=最高，4=最低）

    v1.8.3 性能修复：委托 `query_pattern_index`（mtime 感知 pattern 索引 + URL 级缓存），
    替代原「遍历全部 tier × 全部 source × 全部 patterns」的无缓存线性扫描
    （实测 7.9µs → 0.4µs / 次，**20.4x**）。语义等价：两者均只匹配 url、
    均取命中的**最小 tier**、空 url / 未命中均返回 4。
    背景：v1.8.3 §8.4 tier 单源化后，链A compute_final_score_v2 新增本函数调用，
    若无缓存将使 1000 源评分链路退化。
    """
    tier, _weight = query_pattern_index(url, domain)
    return tier


def list_sources_by_domain(domain: str = 'general') -> dict:
    """列出某领域的所有源（按 tier 分组）"""
    t = _load_v2()
    return {
        'tier1': t[1].get(domain, []) + t[1].get('general', []),
        'tier2': t[2].get(domain, []) + t[2].get('general', []),
        'tier3': t[3].get(domain, []) + t[3].get('general', []),
    }


def build_pattern_index(domain: str = 'general') -> Dict[str, Tuple[int, int]]:
    """构建指定领域的 pattern → (tier, weight) hash 索引（mtime 感知缓存）"""
    if domain in _PATTERN_HASH_CACHE:
        return _PATTERN_HASH_CACHE[domain]
    t = _load_v2()
    idx: Dict[str, Tuple[int, int]] = {}
    for tier_num in (1, 2, 3):
        for source in t[tier_num].get(domain, []) + t[tier_num].get('general', []):
            for pat in source['patterns']:
                idx.setdefault(pat.lower(), (tier_num, source['weight']))
    _PATTERN_HASH_CACHE[domain] = idx
    return idx


def query_pattern_index(url: str, domain: str = 'general') -> Tuple[int, int]:
    """v2.6.1 PATCH: URL 缓存层；首次遍历 patterns 找最优，之后同 (url,domain) 直返。"""
    if not url:
        return (4, 0)
    url_lower = url.lower()
    cache_key = (url_lower, domain)
    if cache_key in _URL_QUERY_CACHE:
        return _URL_QUERY_CACHE[cache_key]
    idx = build_pattern_index(domain)
    best = (4, 0)
    for pat, (tier, weight) in idx.items():
        if pat in url_lower and tier < best[0]:
            best = (tier, weight)
    _URL_QUERY_CACHE[cache_key] = best
    return best


def clear_pattern_index_cache():
    """v2.5.0 新增；v2.6.1 PATCH: 同时清 URL 缓存"""
    _PATTERN_HASH_CACHE.clear()
    _URL_QUERY_CACHE.clear()


# 模块加载时预热常用 domain（mtime 后下次调用自动重建）
for _d in ['tech-research', 'finance-research', 'market-research',
           'policy-research', 'competitor-intel', 'general']:
    build_pattern_index(_d)


if __name__ == '__main__':
    import sys
    domain = sys.argv[1] if len(sys.argv) > 1 else 'general'
    sources = list_sources_by_domain(domain)
    for tier, items in sources.items():
        print(f"\n{tier.upper()} ({len(items)} sources):")
        for s in items:
            print(f"  - {s['name']:20s} weight={s['weight']:3d}  patterns={s['patterns']}")
