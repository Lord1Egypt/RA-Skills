#!/usr/bin/env python3
"""
core/ner.py — Infoseek 命名实体识别算法（v2.0.0 新增 · v2.3.3 性能优化 · mod-v2.6.0 AC 自动机）

基于词典匹配 + 位置权重 + 跨语言别名展开的轻量 NER。

支持 5 类实体：ORG/PRODUCT/TECH/PERSON/METRIC
词典来源：core/entities.py（100+ 条目）
"""

import re
from typing import List, Dict, Optional

# v2.4.1 PATCH (DEF-E): EntityAliases 模块级单例 — 避免 extract_entities
# 每次都新建实例导致 priority_cache TTL 缓存形同虚设
_ENTITY_ALIASES_INSTANCE = None

# G8-apply: 公共入口类型契约守卫（纯 stdlib，scripts/entry_guard.py）
import sys as _eg_sys
from pathlib import Path as _eg_p
_eg_dir = str(_eg_p(__file__).resolve().parent.parent / 'scripts')
if _eg_dir not in _eg_sys.path:
    _eg_sys.path.insert(0, _eg_dir)
from entry_guard import (require_text, require_mapping, require_sequence, coerce_mapping_list)

def _get_aliases_mgr():
    global _ENTITY_ALIASES_INSTANCE
    if _ENTITY_ALIASES_INSTANCE is None:
        from entity_aliases import EntityAliases
        _ENTITY_ALIASES_INSTANCE = EntityAliases()
    return _ENTITY_ALIASES_INSTANCE


# 支持包内和独立调用两种模式
try:
    from .entities import get_all_entities
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from entities import get_all_entities


def _normalize(text: str) -> str:
    """文本归一化（统一小写 + 压缩空白为单空格，保留分词痕迹）

    P3 词边界（2026-09-10）：保留单空格 —— 原有 re.sub(r'\\s+','',...) 全去空格
    会把 \"OpenAI GPT-5\" 压成 \"openaigpt-5\"，致词边界前瞻失败漏提实体的回归
    （'openai' 后紧跟 'g' 字母）。保留空格后 \"openai gpt-5\" 边界天然成立。

    v2.5.1 性能优化（阶段B）：\\s+ 预编译为模块常量（_normalize 被调 81 万次，
    此前每次 re.sub 走字符串实参隐式查/编缓存）。
    """
    return _WHITESPACE_RE.sub(' ', text.lower()).strip()


_WHITESPACE_RE = re.compile(r'\s+')


# P3 词边界（2026-09-10）：拉丁字母/数字词加 \b 语义边界，
# 消除 'meta' 命中 'metadata'/'metaverse'、'pe' 命中 'openai' 类子串误报；
# 中文等非拉丁词不做边界收紧（保留子串语义——中文术语包含关系应命中，
# 如「失效」命中「失效模式」；而 'Meta' 别名 'meta' 命中 'Metadata' 属误报需拦截）。
_LATIN_EDGE_RE = re.compile(r'[A-Za-z0-9]')


_BOUNDARY_PAT_CACHE = {}


def _boundary_pattern(kw: str):
    """构造词边界正则（None = 无边界约束的裸词）

    v2.3.3 性能优化（P2-6）：正则编译结果按 kw 缓存。实体名/别名字典有限且
    跨源复用，避免每源重复 re.escape + re.compile（实测 re._compile 为融合
    阶段 tottime 第一热点）。
    """
    if not kw:
        return None
    cached = _BOUNDARY_PAT_CACHE.get(kw)
    if cached is not None:
        return cached
    pat = re.escape(kw)
    if _LATIN_EDGE_RE.match(kw[0]):
        pat = r'(?<![A-Za-z0-9_])' + pat
    if _LATIN_EDGE_RE.match(kw[-1]):
        pat += r'(?![A-Za-z0-9_])'
    compiled = re.compile(pat)
    _BOUNDARY_PAT_CACHE[kw] = compiled
    return compiled


def _match_entity(text_norm: str, entity: dict, budget: Optional[dict] = None,
                  slot: Optional[dict] = None, authoritative: bool = False) -> Optional[Dict]:
    """单条实体匹配（返回 span 范围 · P3 词边界版）

    拉丁字母/数字词强制词边界（前后不得邻接字母数字/下划线），
    中文词保持子串匹配；均可能命中多处的取首个位置（与旧 find 语义一致）。

    v2.5.1 阶段B：name_norm / alias_norm 从静态预算 budget 读取。
    v2.6.0 阶段C2：
      · authoritative=True（自动机扫描成功）：slot 为 Aho-Corasick 对全文本
        一次扫描的权威结果。自动机已遍历文本全部子串，故 slot 中没有的
        模式必然未出现——直接判定，绝不回退正则（这是消除 29 万次扇出的
        关键：未命中实体零正则调用）。
      · authoritative=False（自动机不可用/整体降级）：忽略 slot，回退到
        阶段B 的逐模式边界正则 search，行为与旧版完全一致。
    决策优先级（name 优先，否则按 budget 别名顺序取首个）两路径一致。
    """
    if budget is None:
        budget = _budget_entity(entity)
    name_norm = budget['name_norm']
    if name_norm:
        idx = None
        if authoritative:
            idx = (slot or {}).get('name')
        else:
            m = _boundary_pattern(name_norm).search(text_norm)
            if m:
                idx = m.start()
        if idx is not None:
            return {
                'entity_type': entity.get('category', 'UNKNOWN'),
                'entity_name': entity['name'],
                'span': (idx, idx + len(name_norm)),
                'match_method': 'name',
            }

    # 别名匹配（alias_norm 已静态预算并过滤 <2 字符）
    alias_hits = (slot or {}).get('alias') if authoritative else None
    for alias, alias_norm in budget['aliases_norm']:
        idx = None
        if authoritative:
            idx = alias_hits.get(alias) if alias_hits is not None else None
        else:
            m = _boundary_pattern(alias_norm).search(text_norm)
            if m:
                idx = m.start()
        if idx is not None:
            return {
                'entity_type': entity.get('category', 'UNKNOWN'),
                'entity_name': entity['name'],
                'matched_alias': alias,
                'span': (idx, idx + len(alias_norm)),
                'match_method': 'alias',
            }
    return None


# ── v2.5.1 阶段B：实体词典静态预算 ──────────────────────────────
# 词典内容稳定（entities.get_all_entities 有缓存），其 name/alias 的归一化
# 结果只需计算一次。按实体 id() 缓存预算；另存 (id,name) 指纹，实体对象被
# 替换（学习实体增删触发字典重建）时自动重算。
_ENTITY_BUDGET_CACHE: Dict[int, dict] = {}


def _budget_entity(entity: dict) -> dict:
    eid = id(entity)
    b = _ENTITY_BUDGET_CACHE.get(eid)
    if b is not None and b.get('_fp') == (eid, entity.get('name')):
        return b
    name_norm = _normalize(entity['name'])
    aliases_norm = []
    for alias in entity.get('aliases', []):
        alias_norm = _normalize(alias)
        if len(alias_norm) >= 2:
            aliases_norm.append((alias, alias_norm))
    b = {'name_norm': name_norm, 'aliases_norm': aliases_norm,
         '_fp': (eid, entity.get('name'))}
    _ENTITY_BUDGET_CACHE[eid] = b
    return b


def invalidate_entity_budget() -> None:
    """清空实体静态预算（学习实体增删 / 测试隔离时调用）。"""
    _ENTITY_BUDGET_CACHE.clear()
    global _AC_AUTO, _AC_SIG
    _AC_AUTO = None
    _AC_SIG = None


# ═══════════════════════════════════════════════════════════════
# v2.6.0 性能优化（阶段C/C2）：Aho-Corasick 多模式自动机
# ----------------------------------------------------------------
# 旧路径对每个实体的 name + 全部 alias 逐个跑边界正则 search（cProfile
# 实测 _match_entity 在 3000 源规模被调 29 万次、cum 11.5s）。改为把
# 全部实体的 name/alias 归一化模式装入 pyahocorasick 自动机，对每段
# 文本只做一次扫描 O(len(text)+命中数)，再在命中处做与旧正则等价的
# 拉丁词边界校验。
#
# 决策结构保持不变：仍 name 优先，否则按 budget 的别名顺序取首个，
# 因此产出实体/span/match_method 与旧路径逐字节一致，仅速度不同。
#
# 三级降级（任一触发即回退阶段B 的正则路径，行为完全一致）：
#   1) import ahocorasick 失败（未 pip install pyahocorasick）
#   2) 环境变量 INFOSEEK_AC_DISABLE=1
#   3) 自动机构建/扫描抛异常（按次静默回退，不污染主流程）
#
# 依赖登记：deps/registry.yaml 增 aho-corasick 条
# （pip: pyahocorasick / import: ahocorasick / required:false）。
# ═══════════════════════════════════════════════════════════════
import os as _ac_os

_AC_AUTO = None          # 已 make_automaton 的自动机（含 entity 身份负载）
_AC_SIG = None           # 自动机对应的词典签名
_AC_PROBED = False
_AC_AVAILABLE = False


def _probe_ac() -> bool:
    """惰性探测 ahocorasick 可用性（仅探一次）。

    INFOSEEK_AC_DISABLE=1 显式关闭；import 失败也关闭。
    """
    global _AC_PROBED, _AC_AVAILABLE
    if _AC_PROBED:
        return _AC_AVAILABLE
    _AC_PROBED = True
    if _ac_os.environ.get('INFOSEEK_AC_DISABLE', '').strip() in ('1', 'true', 'TRUE', 'yes'):
        _AC_AVAILABLE = False
        return False
    try:
        import ahocorasick as _ac_mod  # noqa: F401  (分发包 pyahocorasick)
        _AC_AVAILABLE = True
    except Exception:
        _AC_AVAILABLE = False
    return _AC_AVAILABLE


def _latin_edge_ok(text_norm: str, start: int, end: int) -> bool:
    """与 _boundary_pattern 的拉丁边界正则等价的命中处校验。

    模式首字符为拉丁/数字时，其前一字符不得是 [A-Za-z0-9_]；
    模式末字符为拉丁/数字时，其后一字符不得是 [A-Za-z0-9_]。
    中文模式调用方不会进入此校验（保留裸子串语义）。
    """
    if start > 0:
        c = text_norm[start - 1]
        if c.isascii() and (c.isalnum() or c == '_'):
            return False
    if end < len(text_norm):
        c = text_norm[end]
        if c.isascii() and (c.isalnum() or c == '_'):
            return False
    return True


def _runtime_alias_patterns(entities) -> Dict[int, list]:
    """收集每个实体的运行时动态别名（hot/cold，来自 aliases.json）。

    static 别名即 entities.py 内建别名（已由 _budget_entity 装入自动机），
    故此处只收 hot/cold，避免与 static 重复。返回
        {entity_id: [ (raw_alias, pat_norm, priority, order), ... ]}
    order 为原 L391-402 遍历中的全局次序（hot 先于 cold），用于等价地
    复现“取首个命中别名”的语义。构建异常返回 {}（调用方据空结果降级）。
    """
    out: Dict[int, list] = {}
    try:
        mgr = _get_aliases_mgr()
        order = 0
        for entity in entities:
            name = entity.get('name')
            if not name:
                continue
            pri = mgr.get_prioritized_aliases(name)
            rows = []
            for priority in ('hot', 'cold'):
                for raw in pri.get(priority, []):
                    pat_norm = _normalize(raw)
                    if len(pat_norm) >= 2:
                        rows.append((raw, pat_norm, priority, order))
                        order += 1
            if rows:
                out[id(entity)] = rows
    except Exception:
        return {}
    return out


def _runtime_alias_fingerprint(rt: Dict[int, list]) -> tuple:
    """动态别名指纹：热/冷别名增删、归一化内容或次序变化即令自动机失效。"""
    return tuple(
        (eid, tuple((r[0], r[1], r[2], r[3]) for r in rows))
        for eid, rows in sorted(rt.items())
    )


def _entities_signature(entities, rt_fingerprint: Optional[tuple] = None) -> tuple:
    """词典指纹：实体对象身份/数量/名称/类别或运行时别名变化即失效。"""
    base = (len(entities),
            tuple((id(e), e.get('name'), e.get('category')) for e in entities))
    if rt_fingerprint is not None:
        base = base + ('rt', rt_fingerprint)
    return base


def _ensure_ac_automaton(entities):
    """按当前词典构建（或复用）自动机；不可用/失败返 None。"""
    global _AC_AUTO, _AC_SIG
    try:
        import ahocorasick as _ac_mod
        rt = _runtime_alias_patterns(entities)
        rt_fp = _runtime_alias_fingerprint(rt)
        sig = _entities_signature(entities, rt_fp)
        if _AC_AUTO is not None and _AC_SIG == sig:
            return _AC_AUTO
        # pattern -> [ payload, ... ]，同模式多实体/多类别名聚合。
        # 统一 6 元组：(eid, kind, raw_alias, pat_norm, priority, order)
        #   kind='name'/'alias'（静态）：priority/order 均 None
        #   kind='rt'（hot/cold 动态）：priority/order 有效
        pat_payloads: Dict[str, list] = {}
        for entity in entities:
            budget = _budget_entity(entity)
            eid = id(entity)
            name_norm = budget['name_norm']
            if name_norm:
                pat_payloads.setdefault(name_norm, []).append(
                    (eid, 'name', None, name_norm, None, None))
            for alias, alias_norm in budget['aliases_norm']:
                pat_payloads.setdefault(alias_norm, []).append(
                    (eid, 'alias', alias, alias_norm, None, None))
            for raw, pat_norm, priority, order in rt.get(eid, ()):
                pat_payloads.setdefault(pat_norm, []).append(
                    (eid, 'rt', raw, pat_norm, priority, order))
        auto = _ac_mod.Automaton()
        for pat, payloads in pat_payloads.items():
            auto.add_word(pat, payloads)
        auto.make_automaton()
        _AC_AUTO = auto
        _AC_SIG = sig
        return auto
    except Exception:
        # 构建失败：不缓存，下次可重试；调用方回退正则
        return None


def _ac_scan(text_norm: str, entities) -> Optional[Dict[int, dict]]:
    """一次自动机扫描，返回 {entity_id: {'name': start, 'alias': {alias: start}}}。

    每个模式只记录最小合法起始位置；命中处做与旧正则等价的拉丁边界校验
    （中文模式裸子串）。自动机不可用或扫描异常时返 None（回退正则路径）。
    """
    if not _probe_ac():
        return None
    auto = _ensure_ac_automaton(entities)
    if auto is None:
        return None
    try:
        hits: Dict[int, dict] = {}
        n = len(text_norm)
        for end_idx, payloads in auto.iter(text_norm):
            for eid, kind, raw_alias, pat, priority, order in payloads:
                start = end_idx - len(pat) + 1
                edge = _LATIN_EDGE_RE.match(pat[0]) or _LATIN_EDGE_RE.match(pat[-1])
                if edge is not None and not _latin_edge_ok(text_norm, start, end_idx + 1):
                    continue
                slot = hits.get(eid)
                if slot is None:
                    slot = {'name': None, 'alias': {}, 'rt': {}}
                    hits[eid] = slot
                if kind == 'name':
                    if slot['name'] is None or start < slot['name']:
                        slot['name'] = start
                elif kind == 'alias':
                    prev = slot['alias'].get(raw_alias)
                    if prev is None or start < prev:
                        slot['alias'][raw_alias] = start
                else:  # kind == 'rt'（hot/cold 动态别名）
                    prev = slot['rt'].get(order)
                    if prev is None or start < prev[3]:
                        slot['rt'][order] = (priority, raw_alias, pat, start)
        return hits
    except Exception:
        return None


def extract_entities(text: str, entity_types: Optional[List[str]] = None) -> List[Dict]:
    """提取文本中的所有实体

    参数:
        text: 输入文本（中文/英文/混合）
        entity_types: 限制实体类型（默认 None = 全部 5 类）

    返回:
        实体列表 [{entity_type, entity_name, span, match_method, ...}, ...]
    """
    # G8-apply: 类型契约守卫（允许 None 透传降级为 []，拒绝 int/float/dict 等非文本）
    if text is not None and not isinstance(text, str):
        raise TypeError(f"text 需为文本(str)或 None，收到 {type(text).__name__}: {text!r}")
    if not text:
        return []

    text_norm = _normalize(text)
    entities = get_all_entities()

    # v2.6.0 阶段C2：Aho-Corasick 一次扫描得全部命中位置。成功（dict，可能
    # 为空）即权威，_match_entity 不再跑正则；返回 None 表示整体降级，
    # authoritative=False 回退阶段B 的逐模式边界正则（行为等价）。
    ac_hits = _ac_scan(text_norm, entities)
    authoritative = ac_hits is not None

    found = []
    for entity in entities:
        # 类型过滤
        if entity_types and entity.get('category') not in entity_types:
            continue
        budget = _budget_entity(entity)
        slot = ac_hits.get(id(entity)) if authoritative else None
        match = _match_entity(text_norm, entity, budget, slot, authoritative)
        if match:
            found.append(match)

    # 按 span 排序 + 去重（同一位置只保留一个）
    found.sort(key=lambda e: e['span'][0])
    deduped = []
    last_end = -1
    for e in found:
        if e['span'][0] >= last_end:
            deduped.append(e)
            last_end = e['span'][1]

    # v2.1.0 集成：自动调用 entity_tracker.record_hit 记录命中
    # v2.5.1 性能优化（阶段A）：接线已有模块级单例 get_tracker()，
    # 此前每次 extract_entities 都 EntityTracker() 新建（触发 _load_state 落盘读取）。
    try:
        from entity_tracker import get_tracker
        tracker = get_tracker()
        for e in deduped:
            tracker.record_hit(e['entity_name'])
    except Exception:
        pass  # 静默失败，不影响 NER 主流程

    # v2.1.1 集成：同时识别 aliases.json 中的运行时别名
    # v2.2.0 升级：高频别名优先检索（hot > cold > static）
    # v2.4.1 PATCH (DEF-E): 用模块级单例 mgr 让 priority_cache 真正生效
    # v2.3.3 性能优化（P2-6）：复用 L138 的 text_norm，避免对同一文本二次 re.sub
    # v2.6.0 C2：AC 权威路径下直接查 slot['rt']（hot/cold），零正则；
    #            static（内建别名）已由主循环命中，无需在此重复扫描。
    #            AC 不可用（非权威）时保留原 hot→static→cold 正则遍历。
    try:
        mgr = _get_aliases_mgr()
        found_names = {d['entity_name'] for d in deduped}
        if authoritative:
            # 权威路径：只补 hot/cold 动态别名（static 已被主循环覆盖）
            for entity_dict in entities:
                name = entity_dict['name']
                if name in found_names:
                    continue
                slot = ac_hits.get(id(entity_dict))
                rt = slot.get('rt') if slot else None
                if not rt:
                    continue
                # 原遍历中 hot 整体先于 cold（order 由 _runtime_alias_patterns
                # 全局递增），故 order 最小者即“首个命中”。
                order_min = min(rt.keys())
                priority, matched_alias, matched_norm, idx = rt[order_min]
                if idx < 0:
                    continue
                # span 重叠检查（防止子串误报，如 'pe' ⊂ 'openai'）
                overlap = False
                for d in deduped:
                    ds, de = d['span']
                    if ds >= 0 and not (idx + len(matched_norm) <= ds or idx >= de):
                        overlap = True
                        break
                if overlap:
                    continue
                deduped.append({
                    'entity_type': entity_dict.get('category', 'UNKNOWN'),
                    'entity_name': name,
                    'matched_alias': matched_alias,
                    'span': (idx, idx + len(matched_norm)),
                    'match_method': f'v220_alias_{priority}',
                })
        else:
            for entity_dict in get_all_entities():
                # 已识别的实体跳过（保持 deduped 语义）
                if entity_dict['name'] in found_names:
                    continue
                # v2.2.0: 获取分级别名（static/hot/cold），按优先级匹配
                prioritized = mgr.get_prioritized_aliases(entity_dict['name'])
                matched_alias = None
                match_priority = None
                # 优先级：hot（高频）→ static（权威）→ cold（低频）
                for priority, alias_list in [('hot', prioritized.get('hot', [])),
                                             ('static', prioritized.get('static', [])),
                                             ('cold', prioritized.get('cold', []))]:
                    for alias in alias_list:
                        alias_norm = _normalize(alias)
                        if len(alias_norm) < 2:
                            continue
                        if _boundary_pattern(alias_norm).search(text_norm):
                            matched_alias = alias
                            match_priority = priority
                            matched_norm = alias_norm
                            break
                    if matched_alias:
                        break
                if matched_alias:
                    # v2.3.0 修复：span 重叠检查（防止子串误报，如 'pe' ⊂ 'openai'）
                    idx = text_norm.find(matched_norm)
                    if idx >= 0:
                        overlap = False
                        for d in deduped:
                            ds, de = d['span']
                            if ds >= 0 and not (idx + len(matched_norm) <= ds or idx >= de):
                                overlap = True
                                break
                        if overlap:
                            continue
                    deduped.append({
                        'entity_type': entity_dict.get('category', 'UNKNOWN'),
                        'entity_name': entity_dict['name'],
                        'matched_alias': matched_alias,
                        'span': (idx, idx + len(matched_norm)) if idx >= 0 else (-1, -1),
                        'match_method': f'v220_alias_{match_priority}',
                    })
    except Exception:
        pass

    return deduped


# ═══════════════════════════════════════════════════════════════
# v2.5.1 性能优化（阶段A）：NER 结果缓存
# ----------------------------------------------------------------
# 同一批 sources 在主链 / entity_graph / conflict_v3 三处各跑一次
# extract_entities（cProfile 占 research 总 CPU ~55%）。此缓存按
# 文本身份复用结果，把三处重复 NER 降为一次。
#
# 设计要点：
# - 主键用 id(text)：同一 str 对象跨阶段传递时零成本命中（不重算 hash）。
# - 二级校验 hash(text)+len：对象被回收后 id 可能复用，hash 不同即判失效。
# - 有界（OrderedDict  FIFO 淘汰），防超长 research 内存无限增长。
# - 值深拷贝：调用方可能改返回的 dict/span，绝不能污染缓存。
# - 不缓存 entity_types 过滤态，过滤参数纳入缓存键。
# ═══════════════════════════════════════════════════════════════
import copy as _copy
from collections import OrderedDict as _OrderedDict

_NER_CACHE_MAX = 512
_NER_CACHE: '_OrderedDict[tuple, tuple]' = _OrderedDict()


def invalidate_ner_cache() -> None:
    """清空 NER 结果缓存（学习实体增删 / 测试隔离时调用）。"""
    _NER_CACHE.clear()


def extract_entities_cached(text: str, entity_types: Optional[List[str]] = None) -> List[Dict]:
    """extract_entities 的有缓存版本（阶段A 新增）。

    语义与返回结构与 extract_entities 完全一致，仅对同一文本的重复调用
    复用结果。返回深拷贝，调用方可安全修改。entity_types 序列化为可哈希键。
    """
    if text is not None and not isinstance(text, str):
        raise TypeError(f"text 需为文本(str)或 None，收到 {type(text).__name__}: {text!r}")
    if not text:
        return []

    type_key = tuple(entity_types) if entity_types else None
    cache_key = (id(text), type_key)
    bucket = _NER_CACHE.get(cache_key)
    # id 命中后用 hash+len 二次校验，防 str 对象回收后 id 复用致错配
    if bucket is not None:
        stored_hash, stored_len, result = bucket
        if stored_len == len(text) and stored_hash == hash(text):
            _NER_CACHE.move_to_end(cache_key)
            return _copy.deepcopy(result)
        # id 复用 / 内容已变：淘汰旧条目
        _NER_CACHE.pop(cache_key, None)

    result = extract_entities(text, entity_types)
    _NER_CACHE[cache_key] = (hash(text), len(text), result)
    if len(_NER_CACHE) > _NER_CACHE_MAX:
        _NER_CACHE.popitem(last=False)
    return _copy.deepcopy(result)


def extract_by_category(text: str, category: str) -> List[str]:
    """按类别提取（仅返回实体名称）"""
    entities = extract_entities(text)
    return [e['entity_name'] for e in entities if e.get('entity_type') == category]


def has_entity(text: str, entity_name: str) -> bool:
    """检测文本是否包含某个实体"""
    found = extract_entities(text)
    return any(e['entity_name'].lower() == entity_name.lower() for e in found)


def entity_coverage(text: str, reference_entities: List[str]) -> float:
    """计算 reference 实体在 text 中的覆盖率

    用于检测"同一主题不同源"对同一实体的覆盖一致性
    """
    if not reference_entities:
        return 1.0
    found = extract_entities(text)
    found_names = {e['entity_name'].lower() for e in found}
    covered = sum(1 for r in reference_entities if r.lower() in found_names)
    return covered / len(reference_entities)


# ═══════════════════════════════════════════════════════════════
# CLI 测试
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    test_texts = [
        "OpenAI 发布了 GPT-4o 模型，运行在 Microsoft Azure 云上。",
        "宝钢与 ArcelorMittal 在钢卷分切工艺上展开合作。",
        "宁德时代 PE 估值 25-30 倍，CATL 股价上涨。",
        "Claude 3.5 Sonnet 与 Gemini Pro 比较。",
        "Hugging Face 与 PyTorch 社区推动 LLM 训练。",
    ]
    for text in test_texts:
        entities = extract_entities(text)
        print(f"\n文本: {text}")
        print(f"  实体 ({len(entities)}):")
        for e in entities:
            print(f"    - {e['entity_type']:12s} | {e['entity_name']:20s} | match={e['match_method']}")