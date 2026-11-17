#!/usr/bin/env python3
"""
core/conflict_weight.py — 冲突检测多源加权（P1-2 G2 修复，v2.5.0）

按来源可信度加权冲突严重度评级：
- 来源 credibility 取自 references/trusted-sources.json（4 级白名单的 domain→credibility）
- max_cred ≥ 80（至少一方高可信矛盾）→ severity 升一档（low→medium, medium→high, high 不变）
- min_cred < 40（全部低可信/未知域）→ 附加 low_evidence=True（不降级，仅提示证据弱）
- 输出附加字段：weighted / max_cred / min_cred / sources_cred / low_evidence

零破坏：新增字段不覆盖原 severity 语义之外的任何字段；env INFOSEEK_CONFLICT_WEIGHT=0 关闭。
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union

CORE_DIR = Path(__file__).parent

# 默认可信度（未命中白名单的中性值）
DEFAULT_CREDIBILITY = 50
# 高可信阈值（≥ → 冲突升级一档）
HIGH_CRED = 80
# 低可信阈值（< → 全部来源证据弱标记）
LOW_CRED = 40

_SEVERITY_ORDER = ['low', 'medium', 'high']
_SEVERITY_UP = {'low': 'medium', 'medium': 'high', 'high': 'high'}

_CRED_CACHE: Optional[Dict[str, int]] = None
# L1 (v1.7.1 PATCH): 缓存对应的文件 mtime；热改后自动失效重载
# （消除与 scripts/trusted_kb.py 实时读文件消费者的缓存不对称）
_CRED_CACHE_MTIME: Optional[float] = None


def enabled() -> bool:
    """加权开关（默认开；0 关闭回退原 severity）"""
    v = os.environ.get('INFOSEEK_CONFLICT_WEIGHT', '1')
    return v not in ('0', 'false', 'False', 'no')


def domain_of(url: str) -> str:
    """URL → 域名（去协议/路径/端口/www.）"""
    if not url:
        return ''
    m = re.search(r'(?:https?://)?(?:www\.)?([^/:?#]+)', url)
    return m.group(1).lower() if m else ''


def load_credibility_map(force: bool = False) -> Dict[str, int]:
    """加载 trusted-sources.json 的 domain→credibility 映射（mtime 感知模块级缓存）

    文件热改（trusted_kb.kb_add 运行时写回）后自动失效重载，
    与实时读文件消费者（scripts/trusted_kb.py）保持一致。
    文件缺失/损坏 → 空映射（全部来源落默认分）。
    """
    global _CRED_CACHE, _CRED_CACHE_MTIME
    path = CORE_DIR.parent / 'references' / 'trusted-sources.json'
    try:
        mtime = path.stat().st_mtime if path.exists() else None
    except OSError:
        mtime = None
    if _CRED_CACHE is not None and not force and mtime == _CRED_CACHE_MTIME:
        return _CRED_CACHE
    mapping = {}
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding='utf-8'))
            # 双源合并(C 方案交集消歧)：kb_sources(verified 优先) + white_list 补全
            # 兼容分支：旧 sources[] 结构(单测 mock / 残留文件) 回退
            segs = data.get('kb_sources', []) + data.get('white_list', [])
            if not segs and data.get('sources'):
                segs = data['sources']
            for s in segs:
                dom = domain_of(s.get('domain', ''))
                cred = s.get('credibility')
                if dom and isinstance(cred, (int, float)) and dom not in mapping:
                    mapping[dom] = int(cred)
    except Exception:  # noqa: BLE001 白名单缺失不阻断冲突检测
        mapping = {}
    _CRED_CACHE = mapping
    _CRED_CACHE_MTIME = mtime
    return mapping


def source_credibility(url: str) -> int:
    """来源可信度：白名单命中 → credibility；未命中 → 默认 50"""
    dom = domain_of(url)
    if not dom:
        return DEFAULT_CREDIBILITY
    return load_credibility_map().get(dom, DEFAULT_CREDIBILITY)


def source_known(url: str) -> bool:
    """来源是否命中白名单（未命中 → 证据弱候选）"""
    dom = domain_of(url)
    if not dom:
        return False
    return dom in load_credibility_map()


def weight_conflict(conflict: Dict) -> Dict:
    """对单条冲突应用来源可信度加权（原地增补字段，返回同一 dict）"""
    if not enabled():
        return conflict

    a = conflict.get('claim_a', {})
    b = conflict.get('claim_b', {})
    url_a = a.get('source', '')
    url_b = b.get('source', '')
    cred_a = source_credibility(url_a)
    cred_b = source_credibility(url_b)
    known_a = source_known(url_a)
    known_b = source_known(url_b)
    max_cred = max(cred_a, cred_b)
    min_cred = min(cred_a, cred_b)

    # 高可信来源矛盾 → severity 升一档
    if max_cred >= HIGH_CRED:
        cur = conflict.get('severity', 'medium')
        conflict['severity'] = _SEVERITY_UP.get(cur, cur)

    conflict['weighted'] = True
    conflict['max_cred'] = max_cred
    conflict['min_cred'] = min_cred
    conflict['sources_cred'] = [
        {'source': url_a, 'domain': domain_of(url_a), 'credibility': cred_a, 'known': known_a},
        {'source': url_b, 'domain': domain_of(url_b), 'credibility': cred_b, 'known': known_b},
    ]
    # 证据弱：任一来源低于低可信阈值，或双方均未命中白名单
    if min_cred < LOW_CRED or (not known_a and not known_b):
        conflict['low_evidence'] = True
    return conflict


def weight_conflicts(conflicts: List[Dict]) -> List[Dict]:
    """批量加权（就地增补）"""
    for c in conflicts:
        weight_conflict(c)
    return conflicts


def main():
    """CLI: python -m core.conflict_weight <url1> <url2>"""
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m core.conflict_weight <url> [url...]")
        sys.exit(1)
    for url in sys.argv[1:]:
        print(f"{url} → domain={domain_of(url)}, credibility={source_credibility(url)}")


if __name__ == '__main__':
    main()