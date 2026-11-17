#!/usr/bin/env python3
"""
core/contradiction_scorer.py — Infoseek 语义矛盾评分（mod-v2.5.0；v2.4.0 MINOR 引入，v2.5.0 叙述句事实槽召回增强）

V2.3.0/v2.3.1 的冲突检测仅判 "同实体 ≥2 异源" 就报，severity 写死 medium，
对真实「自相矛盾 / 客观一致 / 并非冲突」三者区分力差。

v2.4.0 引入轻量语义矛盾评分（无需 LLM 也可用，可选 LLM 增强）：

输入：claim_a + claim_b（同实体两条声明，结构见 conflict_v3._extract_fact_claims）
输出：{'score': 0-100, 'severity': 'high|medium|low|none',
        'reasons': [..], 'neg_hits': [..], 'shared_slots': [..]}

评分三段：
  ① 共享事实槽（predicate 集合 Jaccard）        0-30 分
  ② 否定/反义命中（精确词 + 同义对）              0-50 分
  ③ 极性相反（attribute 同槽 + polarity 不同）     ×1.4 乘数（出现在 ② 之后）

总分映射 severity：
  ≥60  high     → 明确矛盾（核心事实相反）
  30-59 medium  → 疑似矛盾（需复核）
  10-29 low     → 表述分歧（人称/视角差异）
  <10  none     → 实为一致

可选 LLM：`score_with_llm(claim_a, claim_b, llm_router)` 拼接 prompt 调 LLM 拿 0-100 分。
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set

CORE_DIR = Path(__file__).parent

# ─── 否定词（中英） ─────────────────────────────────────────
NEG_WORDS_ZH = {
    '不', '否', '非', '无', '未', '没', '别', '莫', '毋', '弗',
    '不开放', '不开源', '非开源', '不发布',
}
NEG_WORDS_EN = {
    'not', 'no', 'never', 'without', 'none', 'fail', "n't",
    'closed', 'proprietary',          # 与 open 对立
    'decline', 'reject', 'deny',
}

# ─── 反义对（同义簇） ─────────────────────────────────────────
ANTONYM_PAIRS = [
    ('开源', '闭源'), ('open source', 'closed source'),
    ('上涨', '下跌'), ('increase', 'decrease'),
    ('盈利', '亏损'), ('profit', 'loss'),
    ('增长', '下滑'), ('growth', 'decline'),
    ('同意', '拒绝'), ('agree', 'reject'),
    ('官方', '传闻'), ('official', 'rumor'),
    ('支持', '反对'), ('support', 'oppose'),
    ('即将', '搁置'), ('imminent', 'shelved'),
    ('公开', '保密'), ('public', 'classified'),
]

# ─── 谓词模板（事实槽提取用：把句子拆 (predicate, value)） ──
PRED_TEMPLATES_ZH = [
    r'(.{1,8}?)是(开源|闭源|公开|保密|盈利|亏损)',
    r'(.{1,12}?)(宣布|确认|否认|发布|停止)(.{1,20})',
    r'(.{1,12}?)(增长|下滑|上涨|下跌)\s*(\d+\.?\d*\s*%)',
]
PRED_TEMPLATES_EN = [
    r'(\w+\s+\w+)\s+is\s+(open|closed|public|profitable|loss)',
    r'(\w+\s+\w+)\s+(announce|confirm|deny|release|stop)\s+(.{1,40})',
]


# ═══════════════════════════════════════════════════════════
# 事实槽提取
# ═══════════════════════════════════════════════════════════

# DEF-15（v2.1.1 P2）：legacy 短语袋路有界预算。三路窗口统一——
# keyed 路 _build_keyed_slots（L394）与 time 路 _parse_time_spans（L553）
# 早已截断到 _KEYED_MAX_CHARS(50k)，唯独 legacy _extract_slots / _detect_negation
# 对全文线性展开 2-gram，500k 长文本实测 timeout(>150s)。此处复用同一窗口常量，
# 保持三路一致；legacy 只取弱信号 2-gram，截断仅损失 50k 之后近零贡献（长文本本就稀释）。
def _slot_window(text) -> str:
    """legacy 路统一文本窗口：非字符串归一 + 截断到有界预算。"""
    if not isinstance(text, str):
        text = '' if text is None else str(text)
    return text[:_KEYED_MAX_CHARS]


def _extract_slots(text: str) -> Set[str]:
    """从文本抽取事实槽（标准化字符串集合）。

    简化策略：用谓词模板抓 (predicate, value) 短语；未命中的退化为 n-gram 关键词集合。
    v2.4.1 PATCH (DEF-D): 模板/正则抛错时降级返回空集，reasons 留痕。
    """
    slots = set()
    t = _slot_window(text).strip()  # DEF-15：截断到 50k 有界窗口，防长文本 2-gram 超线性
    if not t:
        return slots
    try:
        # 模板命中
        for pat in PRED_TEMPLATES_ZH + PRED_TEMPLATES_EN:
            for m in re.finditer(pat, t):
                slot = ' '.join(g for g in m.groups() if g).strip().lower()
                if 4 <= len(slot) <= 60:
                    slots.add(slot)
        # 兜底：2-gram 关键词
        tokens = re.findall(r'[\w\u4e00-\u9fff]+', t.lower())
        for i in range(len(tokens) - 1):
            bigram = f'{tokens[i]} {tokens[i+1]}'
            if len(bigram) >= 4 and not _is_stop_bigram(bigram):
                slots.add(bigram)
    except Exception:
        # v2.4.1 PATCH: 容错 — re.finditer 抛错时返回空集
        return set()
    return slots


def _is_stop_bigram(bg: str) -> bool:
    """过滤无信息 bigram（虚词 + 助词）"""
    stops = {'的 是', '了 的', '和 的', 'in the', 'of the', 'to the', 'is a'}
    return bg in stops


# ═══════════════════════════════════════════════════════════
# GA11（v2.0.0）键控事实槽（keyed slots）—— A 层
#   旧口径：短语袋 Jaccard 相似度（长文本稀释，段落级恒 0）
#   新口径：slot_key=(主体键, 方面aspect) → value(数值/枚举/极性)，
#           仅当「同槽键且值冲突」才计矛盾；两路证据 max 融合不叠加。
# ═══════════════════════════════════════════════════════════

import json as _json
_SYN_PATH = CORE_DIR.parent / "references" / "contradiction-synonyms.json"
_syn_cache = None


def _load_synonyms() -> dict:
    """加载谓词同义归一表（mtime 感知缓存）；缺失/损坏返回空骨架。"""
    global _syn_cache
    try:
        mtime = _SYN_PATH.stat().st_mtime
    except Exception:
        return {"aspects": {}, "opposites": {}, "negation_zh": [],
                "negation_en": [], "subject_stopwords": {"zh": [], "en": []}}
    if _syn_cache is not None and _syn_cache[0] == mtime:
        return _syn_cache[1]
    try:
        data = _json.loads(_SYN_PATH.read_text(encoding="utf-8"))
        data.setdefault("aspects", {})
        data.setdefault("opposites", {})
        _syn_cache = (mtime, data)
        return data
    except Exception:
        return {"aspects": {}, "opposites": {}, "negation_zh": [],
                "negation_en": [], "subject_stopwords": {"zh": [], "en": []}}


# 数值/极性抽取
_NUM_PAT = re.compile(
    r'(\d+(?:\.\d+)?)\s*(%|％|亿|万|千|百|billion|million|thousand|bn|m|k)?',
    re.IGNORECASE)
_CN_NUM = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
           '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
_UNIT_SCALE = {'%': 1.0, '％': 1.0, '百': 100, '千': 1000, '万': 10000,
               '亿': 100000000, 'hundred': 100, 'thousand': 1000, 'k': 1000,
               'million': 1_000_000, 'm': 1_000_000, 'bn': 1_000_000_000,
               'billion': 1_000_000_000}

# 中文百分比特殊写法：百分之二十 / 百分之 20
_CN_PERCENT_PAT = re.compile(r'百分之\s*([零一二两三四五六七八九十\d]+(?:\.\d+)?)')


def _cn_number(token: str) -> Optional[float]:
    """简单中文数字（含 '十' 组合，覆盖 百分之二十 类写法）。"""
    token = token.strip()
    if not token:
        return None
    try:
        return float(token)
    except ValueError:
        pass
    if token == '十':
        return 10.0
    if '十' in token:
        left, _, right = token.partition('十')
        tens = _CN_NUM.get(left, 1) if left else 1
        ones = _CN_NUM.get(right, 0) if right else 0
        return float(tens * 10 + ones)
    if len(token) == 1 and token in _CN_NUM:
        return float(_CN_NUM[token])
    return None


# 方面类型：数值型才做就近抽数；枚举/动作/名词型仅走 opposites + 否定极性
NUMERIC_ASPECTS = {
    'revenue', 'profit', 'market_share', 'valuation', 'headcount',
    'founded_year', 'funding', 'pricing', 'product_spec', 'trend_dir',
    # v2.5.0 扩充：销量/机构评级（目标价）亦可承载数值冲突
    'sales_volume', 'analyst_rating',
}
# 数字 → 方面的就近距离（字符）：指标名词后侧窄窗（指标常在前、数值在后），
# 趋势词前窗为主（增长 12%），二者均收紧以避免跨指标串味
_METRIC_RADIUS = 10       # 指标名词（营收/利润/市值…），中文常隔"同比大幅增长"
_TREND_RADIUS = 5         # 趋势词（增长/下滑…），只收紧邻百分比
_TREND_ASPECTS = {'trend_dir'}
# 需排除的非指标数字（年份/季度）
_QUARTER_PAT = re.compile(r'[0-9一二三四两1-4]\s*季度')


def _scan_numbers(text_low: str):
    """全文单次扫描数值，返回 [{value, percent, center, is_year}]。

    排除：季度序号（3 季度）、无单位 4 位年份（1900-2099，标记 is_year 供 founded_year 用）。
    """
    out = []
    # 中文百分比：百分之二十（span 需映射回原文位置）
    for m in _CN_PERCENT_PAT.finditer(text_low):
        v = _cn_number(m.group(1))
        if v is not None:
            out.append({"value": v, "percent": True,
                        "center": (m.start() + m.end()) / 2, "is_year": False})
    # 屏蔽季度序号区间（避免把"三季度"的 3 当指标）
    masked = list(text_low)
    for qm in _QUARTER_PAT.finditer(text_low):
        for i in range(qm.start(), qm.end()):
            masked[i] = ' '
    masked = ''.join(masked)
    for m in _NUM_PAT.finditer(masked):
        raw, unit = m.group(1), (m.group(2) or '').lower()
        try:
            val = float(raw)
        except ValueError:
            continue
        is_pct = unit in ('%', '％')
        is_year = (not unit) and len(raw) == 4 and 1900 <= int(val) <= 2099
        if unit in _UNIT_SCALE and not is_pct:
            val = val * _UNIT_SCALE[unit]
        out.append({"value": val, "percent": is_pct,
                    "center": (m.start() + m.end()) / 2, "is_year": is_year})
    return out


def _term_positions(text_low: str, terms):
    """方面命中词在原文的所有 (term, center) 位置。"""
    pos = []
    for term in terms:
        start = 0
        while True:
            idx = text_low.find(term, start)
            if idx == -1:
                break
            pos.append((term, idx + len(term) / 2))
            start = idx + 1
    return pos


def _assign_numbers(text_low: str, membership: dict):
    """数值就近归属。

    槽语义：增长率（百分比）同时承载于「指标槽」与「趋势槽」——
      「营收增长 12%」的 12% 既进 revenue 也进 trend_dir：同值不冲突，
      异值时两槽各自检出（指标绝对口径与趋势口径都不漏）。
    防串味：
      - 百分比只归「最近的一个指标词」（半径内），不跨到次近指标
        （「营收增长 35%，利润率新高」35% 归 revenue/trend，不误判 profit）；
      - 裸绝对值只归最近指标，不进趋势槽；
      - 年份只归 founded_year。
    返回 {aspect: [{"kind":"number","value","percent","term"}, ...]}。
    """
    numbers = _scan_numbers(text_low)
    asp_pos = {}
    for asp in NUMERIC_ASPECTS:
        if asp in membership:
            asp_pos[asp] = _term_positions(text_low, membership[asp])

    def nearest_side(asp, num_center, num_start, num_end, radius, side=None):
        """找方面词相对数值的最近命中。

        side='left'：仅取数值左侧（词在数值前，财务句式「指标 趋势 数值」）；
        side='right'：仅取右侧紧邻（「数值 元/万」后置指标的少见句式）；
        side=None：两侧均可。返回 (distance, term, side)。
        """
        best = None
        for term, center in asp_pos.get(asp, []):
            on_left = center <= num_center
            d = abs(num_center - center)
            if d > radius:
                continue
            if side == 'left' and not on_left:
                continue
            if side == 'right' and on_left:
                continue
            cand = (d, term, 'left' if on_left else 'right')
            if best is None or cand[0] < best[0]:
                best = cand
        return best

    # 数值区间（用于左/右判定，避免用中心点跨标点误归属）
    def _num_span(num):
        # 由 center 反推不精确，改为在调用点用原始 match；这里近似用 ±2
        return num["center"] - 2, num["center"] + 2

    assigned: dict = {}
    for num in numbers:
        ns, ne = _num_span(num)
        # 1) 年份 → founded_year（左右均可）
        if num["is_year"]:
            hit = nearest_side('founded_year', num["center"], ns, ne, _METRIC_RADIUS)
            if hit:
                assigned.setdefault('founded_year', []).append(
                    {"kind": "number", "value": num["value"],
                     "percent": False, "term": hit[1]})
            continue

        # 2) 指标归属：左优先（当前指标在数值前）；左侧无候选时才接受右侧紧邻指标
        left_cands, right_cands = [], []
        for asp in asp_pos:
            if asp in _TREND_ASPECTS:
                continue
            hl = nearest_side(asp, num["center"], ns, ne, _METRIC_RADIUS, 'left')
            if hl:
                left_cands.append((hl[0], asp, hl[1]))
            hr = nearest_side(asp, num["center"], ns, ne, 3, 'right')
            if hr:
                right_cands.append((hr[0], asp, hr[1]))
        left_cands.sort()
        right_cands.sort()
        chosen = left_cands[0] if left_cands else (right_cands[0] if right_cands else None)
        if chosen:
            _, asp, term = chosen
            assigned.setdefault(asp, []).append(
                {"kind": "number", "value": num["value"],
                 "percent": num["percent"], "term": term})

        # 3) 百分比增长率额外进趋势槽（趋势词优先取左侧：增长 12%）
        if num["percent"] and 'trend_dir' in asp_pos:
            hit = (nearest_side('trend_dir', num["center"], ns, ne, _TREND_RADIUS, 'left')
                   or nearest_side('trend_dir', num["center"], ns, ne, _TREND_RADIUS, 'right'))
            if hit:
                assigned.setdefault('trend_dir', []).append(
                    {"kind": "number", "value": num["value"],
                     "percent": True, "term": hit[1]})

    # 同方面去重（同值同量纲）+ 限量
    for asp, vals in assigned.items():
        uniq, seen = [], set()
        for v in vals:
            key = (round(v["value"], 4), v["percent"])
            if key not in seen:
                seen.add(key)
                uniq.append(v)
        assigned[asp] = uniq[:8]
    return assigned


def _subject_key(claim: Dict, text: str) -> str:
    """主体键：契约优先（claim.entity / claim.subject / claim.entity_name），缺省全局键 ''。

    阶段0 主体贯通（openfix）：读取字段扩至 entity_name —— conflict_v3 产出的
    claim 用的是 entity_name 键（NER 口径），此前只读 entity/subject 导致生产
    链路主体键恒为空、keyed 路跨主体隔离失效。优先级 entity > subject >
    entity_name（显式契约字段优先，NER 字段兜底）。
    """
    if isinstance(claim, dict):
        for f in ('entity', 'subject', 'entity_name'):
            v = claim.get(f)
            if v and str(v).strip():
                return re.sub(r'\s+', '', str(v).strip().lower())
    return ''  # 全局默认主体键：两条无主体声明默认同一对比对象


def _aspect_membership(text_low: str, aspects: dict) -> dict:
    """文本命中了哪些方面簇 → {aspect: sorted(命中词, 长优先)}。

    多簇 aspect 成员（同词出现在多个簇）原样保留，冲突比对阶段以
    「同簇内 opposites」优先，再回退跨簇枚举成员比对做修正。
    """
    hits: Dict[str, list] = {}
    for asp, vocab in aspects.items():
        words = list(vocab.get("zh", [])) + list(vocab.get("en", []))
        matched = sorted({w.lower() for w in words if w and w.lower() in text_low},
                         key=len, reverse=True)
        if matched:
            hits[asp] = matched
    return hits


def _negated(text_low: str, keyword: str, syn: dict) -> bool:
    """关键词前 3 字内是否有否定词（中英）。"""
    idx = text_low.rfind(keyword)
    if idx == -1:
        return False
    pre = text_low[max(0, idx - 4): idx]
    for w in syn.get("negation_zh", []):
        if w and w in pre:
            return True
    pre_en = text_low[max(0, idx - 25): idx]
    toks = re.findall(r"[a-z']+", pre_en)
    for w in syn.get("negation_en", []):
        if w in toks or (w.startswith("n't") and "n't" in pre_en):
            return True
    return False


# 长文本保护裁决（v2.0.0 §8.16）：50k 字符截断 / 500 方面命中上限 / 200 槽值上限
_KEYED_MAX_CHARS = 50_000
_KEYED_MAX_ASPECT_HITS = 500
_KEYED_MAX_VALUES = 200


# ──────────────────────────────────────────────────────────────
# 词位值（term-value）抽取：无 opposites 登记方面的「同槽值不同」检测
# 缺口（P2-4/D-4）：`_enum_conflict` 仅覆盖 opposites 预定义词对，
# location（深圳↔北京）、person_change（赵远航↔孙启铭）、analyst_rating
# （增持↔中性）这类同槽不同值此前完全漏检。此处取「方面关键词后侧紧邻
# 词位」作槽值：值相同→不冲突；两侧存在互异值→计一次 term 冲突。
# ──────────────────────────────────────────────────────────────
_TERM_VALUE_ASPECTS = {'location', 'person_change', 'analyst_rating', 'listing_status'}
# 值词位形态：连续中文串，或以字母起首的拉丁串
_VALUE_RUN_PAT = re.compile(r"[\u4e00-\u9fff]{1,}|[a-z][a-z0-9\-]{0,}")
# 前置填充词（长优先，防「达」先剥「达到」）
_TERM_FILLERS = (
    "总部位于", "总部设于", "坐落于", "位于", "地处", "设于", "设在",
    "达到", "高达", "超过", "约为", "现任", "担任", "出任",
    "达", "逾", "约", "近", "系", "为", "是", "在",
)
# 尾部动作词（值词位后缀剥离：赵远航辞去职务 → 赵远航）
_TERM_TAIL_FILLERS = ("辞去职务", "辞去", "辞职", "卸任", "离职", "职务", "职位", "一职")
_TERM_VALUE_WINDOW = 24       # 关键词后侧扫描窗（字符）
_TERM_VALUE_MAX_CHARS = 12    # 值词位最长字符数（防长句误吞）
_TERM_VALUE_MIN_CHARS = 2     # 值词位最短字符数（单字噪声多，弃）


def _term_value(text_low: str, term: str, syn: dict) -> str:
    """取方面关键词后侧紧邻的枚举值词位（跳过空白/标点/填充词/停用词）。"""
    stop = set(syn.get("subject_stopwords", {}).get("zh", []))
    stop |= set(syn.get("subject_stopwords", {}).get("en", []))
    start = 0
    while True:
        idx = text_low.find(term, start)
        if idx < 0:
            return ""
        seg = text_low[idx + len(term): idx + len(term) + _TERM_VALUE_WINDOW]
        for m in _VALUE_RUN_PAT.finditer(seg):
            run = m.group(0)
            for f in _TERM_FILLERS:          # 剥离前置填充词
                while run.startswith(f):
                    run = run[len(f):]
            for f in _TERM_TAIL_FILLERS:      # 剥离尾部动作词
                while run.endswith(f) and len(run) > len(f):
                    run = run[:-len(f)]
            if not run or run in stop or run in _TERM_FILLERS:
                continue
            if len(run) < _TERM_VALUE_MIN_CHARS:
                continue
            return run[:_TERM_VALUE_MAX_CHARS]
        start = idx + 1


def _build_keyed_slots(claim: Dict, text: str, syn: dict) -> dict:
    """单条 claim → 键控槽表 {aspect: {"values":[...], "terms":[...], "negated"}}。

    数值归属走全文单次扫描 + 就近唯一归属（不跨方面串味）；
    非数值型方面承载枚举词、否定极性，并对 location/person_change/
    analyst_rating 作词位值抽取（v2.5.0/P2-4-D-4）。
    """
    t_low = text.lower()[:_KEYED_MAX_CHARS]  # 长文本保护：截断防超线性
    subj = _subject_key(claim, text)
    membership = _aspect_membership(t_low, syn.get("aspects", {}))
    # 命中方面数量上限（按方面名稳定排序截断，确定性可复现）
    if len(membership) > _KEYED_MAX_ASPECT_HITS:
        membership = {k: membership[k]
                      for k in sorted(membership)[:_KEYED_MAX_ASPECT_HITS]}
    numeric = _assign_numbers(t_low, membership)
    slots: Dict[str, dict] = {}
    for asp, terms in membership.items():
        neg_any = any(_negated(t_low, kw, syn) for kw in terms)
        term_values: list = []
        if asp in _TERM_VALUE_ASPECTS:
            for kw in terms:
                val = _term_value(t_low, kw, syn)
                if val and val not in term_values:
                    term_values.append(val)
            term_values = term_values[:_KEYED_MAX_VALUES]
        slots[asp] = {
            "subject": subj,
            "values": numeric.get(asp, [])[:_KEYED_MAX_VALUES],
            "terms": terms[:4],
            "enum_terms": terms,
            "term_values": term_values,
            "negated": neg_any,
            "polarity": None,
        }
    return slots


def _value_conflicts(asp: str, va: dict, vb: dict):
    """同槽键的值冲突迭代器，产出 (dedup_key, reason)。

    dedup_key 按归一化值对/极性构造，使同一冲突因跨多个方面槽时只计一次。
    """
    nums_a = [v for v in va.get("values", []) if v["kind"] == "number"]
    nums_b = [v for v in vb.get("values", []) if v["kind"] == "number"]
    num_hit = False
    for x in nums_a:
        for y in nums_b:
            if x["percent"] != y["percent"]:
                continue  # 量纲不同不比（5% vs 5亿 不构成同值冲突）
            xv, yv = x["value"], y["value"]
            if asp == 'founded_year':
                if abs(xv - yv) >= 1:
                    num_hit = True
                    yield ("num", round(min(xv, yv), 4), round(max(xv, yv), 4),
                           x["percent"]), f"成立年份冲突 {xv:g}↔{yv:g}"
                continue
            base = max(abs(xv), abs(yv), 1.0)
            rel = abs(xv - yv) / base
            if (x["percent"] and abs(xv - yv) >= 3 and rel >= 0.15) or \
               (not x["percent"] and rel >= 0.15):
                num_hit = True
                yield ("num", round(min(xv, yv), 4), round(max(xv, yv), 4),
                       x["percent"]), f"数值冲突 {xv:g}↔{yv:g}"
    # 词位值冲突（v2.5.0/P2-4-D-4）：非数值型方面的「同槽值不同」
    # （location 深圳↔北京、person_change 赵远航↔孙启铭）。仅在同槽无数值
    # 冲突时启用，避免同一方面重复计分。
    if not num_hit:
        only_a = sorted(set(va.get("term_values") or []) - set(vb.get("term_values") or []))
        only_b = sorted(set(vb.get("term_values") or []) - set(va.get("term_values") or []))
        if only_a and only_b:
            yield ("term", asp), f"词位值冲突 {only_a[0]}↔{only_b[0]}"
    # 否定极性冲突（同一方面，一肯定一否定），且非双否定
    if va.get("negated") != vb.get("negated") and (va.get("negated") or vb.get("negated")):
        yield ("pol", asp), "极性冲突（肯/否对立）"


def _values_conflict(asp: str, va: dict, vb: dict) -> Optional[str]:
    """同槽键两值是否冲突（单值版，返回首个原因或 None）。"""
    for _key, why in _value_conflicts(asp, va, vb):
        return why
    return None


def _enum_conflict(asp: str, sa: dict, sb: dict, syn: dict) -> Optional[str]:
    """枚举/反义簇冲突：opposites 表中互斥词对跨两条声明各命中其一。"""
    ta = set(sa.get("enum_terms", []))
    tb = set(sb.get("enum_terms", []))
    for pair in syn.get("opposites", {}).get(asp, []):
        pa, pb = pair[0].lower(), pair[1].lower()
        if (pa in ta and pb in tb) or (pb in ta and pa in tb):
            return f"反义冲突 {pair[0]}↔{pair[1]}"
    return None


def keyed_score(claim_a: Dict, claim_b: Dict, text_a: str, text_b: str) -> dict:
    """GA11 A 层：键控事实槽冲突评分。

    返回 {"score", "conflict_slots": [...], "slots_a", "slots_b", "reasons": [...]}。
    单冲突槽 35（medium）；2 槽 60（high 边界，保持 high 需明确矛盾）；≥3 槽 85。
    """
    syn = _load_synonyms()
    sa = _build_keyed_slots(claim_a, text_a, syn)
    sb = _build_keyed_slots(claim_b, text_b, syn)
    subj_a = _subject_key(claim_a, text_a)
    subj_b = _subject_key(claim_b, text_b)

    conflict_slots = []
    reasons = []
    # 冲突计数按「值对/反义对」去重：同一数值差异（如 12%↔35%）可能同时落在
    # revenue 与 trend_dir 两槽，但属同一冲突因，只计一次，避免分数虚高。
    conflict_keys = set()
    # 仅在主体键一致（或任一为全局默认键）时比对
    same_subject = (subj_a == subj_b) or subj_a == "" or subj_b == ""
    if same_subject:
        for asp in sorted(set(sa) & set(sb)):
            why = _enum_conflict(asp, sa[asp], sb[asp], syn)
            ckey = ("enum", asp)
            if why is not None:
                conflict_keys.add(ckey)
                conflict_slots.append(asp)
                reasons.append(f"[{asp}] {why}")
                continue
            for ckey2, why2 in _value_conflicts(asp, sa[asp], sb[asp]):
                if why2 and ckey2 not in conflict_keys:
                    conflict_keys.add(ckey2)
                    conflict_slots.append(asp)
                    reasons.append(f"[{asp}] {why2}")

    n = len(conflict_keys)
    if n >= 3:
        score = 85
    elif n == 2:
        score = 60
    elif n == 1:
        score = 35
    else:
        score = 0
    # 长文本保护：限制参与比对的文本规模（50k 字符 / 500 命中方面上限 / 200 槽值）
    return {"score": score, "conflict_slots": conflict_slots,
            "slots_a": sa, "slots_b": sb, "reasons": reasons}


# ═══════════════════════════════════════════════════════════
# 否定 / 反义检测
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
# P0-OPEN-06：时间事实槽（年月/季度 → ISO 区间比对）
#   独立于 aspect 关键词命中：直接从全文解析时间表达式，归一为 [start,end)
#   ISO 日期区间，区间不相交即时间冲突。解决「2023Q1 发布 ↔ 2024Q3 发布」
#   这类时间事实矛盾此前无法被键控槽捕获的问题。
# ═══════════════════════════════════════════════════════════

# 季度中文名 / 数字 / 英文缩写 → 1-4
_QUARTER_CN = {'一': 1, '二': 2, '三': 3, '四': 4, '1': 1, '2': 2,
               '3': 3, '4': 4}
_MONTH_CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
             '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}
_EN_MONTHS = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
              'jul': 7, 'aug': 8, 'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11,
              'dec': 12}


def _q_span(year: int, q: int):
    m0 = (q - 1) * 3 + 1
    if m0 > 9:
        return f'{year:04d}-{m0:02d}-01', f'{year + 1:04d}-01-01'
    return f'{year:04d}-{m0:02d}-01', f'{year:04d}-{m0 + 3:02d}-01'


def _m_span(year: int, m: int):
    if m == 12:
        return f'{year:04d}-12-01', f'{year + 1:04d}-01-01'
    return f'{year:04d}-{m:02d}-01', f'{year:04d}-{m + 1:02d}-01'


def _parse_time_spans(text: str) -> List[Dict[str, str]]:
    """从文本抽取时间表达式 → ISO [start,end) 区间列表。

    支持：2024年Q1 / 2024 第一季度 / 2024Q1 / Q1 2024 /
          2024年3月 / 2024-03 / 2024/3 / March 2024 / 2024年三月 / 单独年份。
    年月/季度精确到月/季；单独 4 位年作全年区间（粒度粗，冲突判定宽松）。
    """
    if not text:
        return []
    t = text[:_KEYED_MAX_CHARS]
    spans: List[Dict[str, str]] = []
    seen = set()

    def _add(label, s, e):
        k = (label, s, e)
        if k not in seen:
            seen.add(k)
            spans.append({'label': label, 'start': s, 'end': e})

    # 1) 年+季度：2024年Q1 / 2024Q1 / 2024 第一季度 / 2024 q3
    for m in re.finditer(
            r'(20\d{2})\s*年?\s*(?:q\s*([1-4])|第\s*([一二三四1-4])\s*季度)',
            t, re.IGNORECASE):
        y = int(m.group(1))
        if m.group(2):
            q = int(m.group(2))
        else:
            q = _QUARTER_CN[m.group(3)]
        s, e = _q_span(y, q)
        _add(f'{y}年Q{q}', s, e)
    # Q1 2024 / Q1'24（季度在前）
    for m in re.finditer(r'q\s*([1-4])\s*[\'’]?\s*(20\d{2})', t, re.IGNORECASE):
        q, y = int(m.group(1)), int(m.group(2))
        s, e = _q_span(y, q)
        _add(f'{y}年Q{q}', s, e)

    # 2) 年+月（数字）：2024年3月 / 2024-03 / 2024/3 / 2024.03
    for m in re.finditer(r'(20\d{2})\s*[年\-/.]\s*(\d{1,2})\s*月?', t):
        y, mo = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            s, e = _m_span(y, mo)
            _add(f'{y}年{mo}月', s, e)
    # 中文月：2024年三月 / 2024年十一月
    for m in re.finditer(r'(20\d{2})\s*年\s*(十一|十二|十|[一二三四五六七八九])月', t):
        y, mo = int(m.group(1)), _MONTH_CN[m.group(2)]
        s, e = _m_span(y, mo)
        _add(f'{y}年{mo}月', s, e)
    # 英文月：March 2024 / Mar 2024
    for m in re.finditer(
            r'(jan|feb|mar|apr|may|jun|jul|aug|sept?|oct|nov|dec)[a-z]*\.?\s+(20\d{2})',
            t, re.IGNORECASE):
        mo, y = _EN_MONTHS[m.group(1).lower()], int(m.group(2))
        s, e = _m_span(y, mo)
        _add(f'{y}年{mo}月', s, e)

    # 3) 单独年份（全年粒度）：已被更精确季/月覆盖的年不再重复添加
    precise_years = {int(sp['label'][:4]) for sp in spans}
    for m in re.finditer(r'(?<![\d/.\-])(20\d{2})(?![\d/.\-])', t):
        y = int(m.group(1))
        if y in precise_years:
            continue
        _add(f'{y}年', f'{y:04d}-01-01', f'{y + 1:04d}-01-01')

    return spans


def _spans_overlap(sa: Dict, sb: Dict) -> bool:
    """两个 ISO [start,end) 区间是否相交（端点相接不算重叠）。"""
    return sa['start'] < sb['end'] and sb['start'] < sa['end']


# ═══════════════════════════════════════════════════════════
# v2.1.2 事件槽批次（F-06 事件抽取 / F-04 期间裁决 / F-07 time 路主体闸）
#   F-06：标点分句 → 逐事件 {subject,aspect,value,polarity,time_span,event_sig}
#         （修「全文单次扫描数值归属」局限——多事实句各自独立归属，不跨句串味）
#   F-04：同主体同方面且双方期间均已知且不相交 → 降权（×0.5，不滤除、不归零）
#   F-07：time 路主体闸——同主体 → 事件级对齐；跨主体 → 不可对拍（消除跨主体时间误报）
# ═══════════════════════════════════════════════════════════

_EVENT_MAX_CHARS = 5_000     # 事件抽取窗口（事件主要在前段；与三路有界预算同构）
_EVENT_MAX_CLAUSES = 24      # 分句上限（防长文句数爆炸）
_EVENT_MAX_EVENTS = 40       # 事件数上限
_PERIOD_DISJOINT_DAMP = 0.5  # F-04 期间不相交降权系数（只降权，不滤除；最低保留 1）

# 标点分句：中英句末/分句标点 + 换行（英文句号须后接空白才算边界，避免小数点误切）
_CLAUSE_SPLIT_RE = re.compile(r'[。！？；;!?\n\r]+|(?<=\.)\s+')


def _split_clauses(text) -> List[str]:
    """F-06：按标点分句（零依赖）。非字符串归一（None→''，其余→str()），空句剔除，句数有界。"""
    if not isinstance(text, str):
        text = '' if text is None else str(text)
    if not text:
        return []
    t = text[:_EVENT_MAX_CHARS]
    parts = [p.strip() for p in _CLAUSE_SPLIT_RE.split(t)]
    return [p for p in parts if p][:_EVENT_MAX_CLAUSES]


def _stable_time_key(ts) -> str:
    """v2.2.0：时间区间稳定键（纳入完整 [start,end) 半开区间 + label）。

    同 start、不同 end 的区间必须得到不同键（修旧「仅取 spans[0]」时代
    无从区分的隐患）。ts 非 dict / 全空 → 'na'（无时间事件的稳定键）。
    """
    if not isinstance(ts, dict):
        return 'na'
    start = str(ts.get('start') or '').strip()
    end = str(ts.get('end') or '').strip()
    label = str(ts.get('label') or '').strip()
    if not start and not end and not label:
        return 'na'
    return f'{start or "?"}~{end or "?"}|{label}'


def _event_identity(subject: str, aspect: str, time_key: str) -> str:
    """v2.2.0：跨文本事件身份（三元签名 subject|aspect|time_key）。

    取代旧二元 event_sig（subject|aspect）：不同时间的同主体同方面事件
    必须可区分，但配对裁决仍按真实 [start,end) 区间对拍（见 F-04/F-07）。
    """
    return f'{subject}|{aspect}|{time_key}'


def _extract_events(text, subject: str = '') -> List[Dict]:
    """F-06：从文本抽取结构化事件列表（A 层零依赖）。

    逐句抽取（先按标点分句），每句产出若干事件：
      {'subject': 主体键, 'aspect': 方面, 'value': 数值槽 dict|None,
       'polarity': 'pos'|'neg', 'time_span': ISO 区间 dict|None,
       'time_key': 稳定时间键（含完整 [start,end)；无时间='na'）,
       'event_sig': f'{subject}|{aspect}|{time_key}'（v2.2.0 三元事件身份）}
    v2.2.0：单句多个时间 span 全部扇出（不再只取 spans[0]）。
    设计要点：
      - 分句独立归属数值/方面（修「全文单次扫描」的多事实句串味，F-06）；
      - 任何解析异常静默降级为空列表，绝不击穿主评分链（与三路健壮性契约一致）。
    """
    events: List[Dict] = []
    if not isinstance(text, str):
        text = '' if text is None else str(text)
    subj = subject if isinstance(subject, str) else ''
    _seen_events: set = set()
    try:
        syn = _load_synonyms()
        aspects = syn.get('aspects', {}) or {}
    except Exception:
        return events
    try:
        for clause in _split_clauses(text):
            low = clause.lower()
            try:
                membership = _aspect_membership(low, aspects)
            except Exception:
                membership = {}
            if not membership:
                continue
            try:
                numeric = _assign_numbers(low, membership) or {}
            except Exception:
                numeric = {}
            try:
                spans = _parse_time_spans(clause)
            except Exception:
                spans = []
            # v2.2.0 F-06：单句多个时间 span 全部扇出（不再只取 spans[0]）；
            #           该句无时间 → 产出一条 time_span=None 的事件。
            ts_list = spans if spans else [None]
            for asp in sorted(membership):
                terms = membership[asp]
                try:
                    neg = any(_negated(low, kw, syn) for kw in terms)
                except Exception:
                    neg = False
                vals = numeric.get(asp, []) or []
                _val = vals[0] if vals else None
                _pol = 'neg' if neg else 'pos'
                for ts in ts_list:
                    _tlabel = ts.get('label', '') if isinstance(ts, dict) else ''
                    # §2.3 单侧事实去重（五元组，**非**三元事件身份）：
                    # 同主体+同方面+同值+同极性+同时间标签 → 同一事实，跳过重复。
                    _dk = (subj, asp, str(_val), _pol, _tlabel)
                    if _dk in _seen_events:
                        continue
                    _seen_events.add(_dk)
                    _tkey = _stable_time_key(ts)
                    events.append({
                        'subject': subj,
                        'aspect': asp,
                        'value': _val,
                        'polarity': _pol,
                        'time_span': ts,
                        'time_key': _tkey,
                        'event_sig': _event_identity(subj, asp, _tkey),
                    })
                    if len(events) >= _EVENT_MAX_EVENTS:
                        return events
    except Exception:
        return events
    return events


def _period_adjudicate(events_a, events_b) -> Dict:
    """F-04 期间裁决（v2.2.0 三元键化）：对「同主体、同方面」事件对做期间比对。

    规则：
      双方期间均已知且**不相交** → 该方面判为非冲突（disjoint）；
      期间相同 / 相交 → 走现值冲突规则（overlap）；任一方缺期间 → 跳过该对（不裁决）。
    事件对按真实 time_span 的 [start,end) 半开区间逐对比较——即使 time_key 不同
    也不跳过（time_key 只是身份标签，区间关系才是裁决依据）。
    仅当双方事件主体键非空且相等时才参与（空主体不裁决，保持旧契约）。

    返回：
      disjoint_slots / overlap_slots : aspect 名列表（旧契约，保持不变）
      reasons                        : 人类可读理由（旧契约）
      slot_pairs                     : 逐对审计明细（v2.2.0 新增）
        [{subject, aspect, time_key_a, time_key_b, label_a, label_b, relation}]
        relation ∈ disjoint | overlap；聚合：任一 overlap → overlap；全部 disjoint → disjoint
    """
    pair_details: List[Dict] = []
    # 聚合仍按 (subject, aspect)，同方面多个区间对逐一累计
    agg: Dict[tuple, Dict] = {}
    for x in (events_a or []):
        if not isinstance(x, dict):
            continue
        sx, ax, tx = x.get('subject'), x.get('aspect'), x.get('time_span')
        if not sx or not ax or not tx:
            continue
        for y in (events_b or []):
            if not isinstance(y, dict):
                continue
            if y.get('subject') != sx or y.get('aspect') != ax:
                continue
            ty = y.get('time_span')
            if not ty:
                continue
            tka, tkb = x.get('time_key', 'na'), y.get('time_key', 'na')
            la = tx.get('label', '') if isinstance(tx, dict) else ''
            lb = ty.get('label', '') if isinstance(ty, dict) else ''
            try:
                relation = 'overlap' if _spans_overlap(tx, ty) else 'disjoint'
            except Exception:
                relation = 'overlap'
            pair_details.append({
                'subject': sx, 'aspect': ax,
                'time_key_a': tka, 'time_key_b': tkb,
                'label_a': la, 'label_b': lb, 'relation': relation})
            rec = agg.setdefault((sx, ax), {'disjoint': 0, 'overlap': 0,
                                            'la': la, 'lb': lb})
            rec[relation] += 1
    disjoint, overlap, reasons = [], [], []
    for (_subj, asp), rec in sorted(agg.items()):
        if rec['disjoint'] > 0 and rec['overlap'] == 0:
            disjoint.append(asp)
            reasons.append(
                f'期间裁决：[{asp}] 同主体同方面期间不相交'
                f'（{rec["la"]} ↔ {rec["lb"]}）→ 降权（不滤除）')
        else:
            overlap.append(asp)
    return {'disjoint_slots': sorted(set(disjoint)),
            'overlap_slots': sorted(set(overlap)),
            'reasons': reasons,
            'slot_pairs': pair_details}

def _event_time_score(events_a, events_b, subject: str = '') -> Dict:
    """F-07（v2.2.0）：主体内事件级时间比对。

    仅同主体同方面事件对参与，按真实 [start,end) 区间逐对对拍（不因 time_key
    不同而跳过）。event_pairs 每项为 dict：
      {subject, aspect, time_key_a, time_key_b, span_a, span_b, relation}
    任一对区间 overlap → 非冲突（score=0）；全部 disjoint → 粗粒度 35 / 细粒度 60。
    """
    ea = [e for e in (events_a or [])
          if isinstance(e, dict) and e.get('time_span')
          and (not subject or e.get('subject') == subject)]
    eb = [e for e in (events_b or [])
          if isinstance(e, dict) and e.get('time_span')
          and (not subject or e.get('subject') == subject)]
    if not ea and not eb:
        coverage = 'neither'
    elif ea and eb:
        coverage = 'both_timed'
    else:
        coverage = 'partial'
    pair_slots = []
    if coverage == 'both_timed':
        for x in ea:
            for y in eb:
                if x.get('aspect') and x.get('aspect') == y.get('aspect'):
                    pair_slots.append((x, y))
    _slots_a_all = [e['time_span'] for e in ea]
    _slots_b_all = [e['time_span'] for e in eb]
    if not pair_slots:
        # 无「同主体同方面」事件对 → 不可对拍（跨方面/跨主体时间差排除，修 F-07 误报）
        # coverage 取真实单侧覆盖（both_timed 但跨方面时仍不可对拍 → partial）
        _cov_nopair = 'partial' if coverage == 'both_timed' else coverage
        return {'score': 0, 'conflict': False,
                'time_slots_a': _slots_a_all, 'time_slots_b': _slots_b_all,
                'reasons': [], 'coverage': _cov_nopair, 'mode': 'event',
                'event_pairs': [],
                # v2.2.0 三元身份审计字段（无配对出口同样齐备）
                'event_time_score': 0,
                'event_disjoint_slots': [], 'event_overlap_slots': [],
                'event_slot_keys': []}
    ta = [x['time_span'] for x, _y in pair_slots]
    tb = [y['time_span'] for _x, y in pair_slots]
    event_pairs = []
    for x, y in pair_slots:
        try:
            rel = 'overlap' if _spans_overlap(x['time_span'], y['time_span']) else 'disjoint'
        except Exception:
            rel = 'overlap'
        event_pairs.append({
            'subject': x.get('subject'), 'aspect': x.get('aspect'),
            'time_key_a': x.get('time_key', 'na'),
            'time_key_b': y.get('time_key', 'na'),
            'span_a': x['time_span'], 'span_b': y['time_span'],
            'relation': rel})
    _disjoint_aspects = sorted({p['aspect'] for p in event_pairs
                                if p['relation'] == 'disjoint' and p['aspect']})
    _overlap_aspects = sorted({p['aspect'] for p in event_pairs
                               if p['relation'] == 'overlap' and p['aspect']})
    _event_slot_keys = sorted({
        f'{p["subject"] or ""}|{p["aspect"]}|{p.get("time_key_a") or "na"}'
        for p in event_pairs} | {
        f'{p["subject"] or ""}|{p["aspect"]}|{p.get("time_key_b") or "na"}'
        for p in event_pairs})
    if any(p['relation'] == 'overlap' for p in event_pairs):
        return {'score': 0, 'conflict': False, 'time_slots_a': ta, 'time_slots_b': tb,
                'reasons': [], 'coverage': 'both_timed', 'mode': 'event',
                'event_pairs': event_pairs,
                'event_time_score': 0,
                'event_disjoint_slots': _disjoint_aspects,
                'event_overlap_slots': _overlap_aspects,
                'event_slot_keys': _event_slot_keys}
    coarse = all('Q' not in s2['label'] and '月' not in s2['label'] for s2 in ta + tb)
    score = 35 if coarse else 60
    la = ' / '.join(f'{p["aspect"]}:{p["span_a"]["label"]}' for p in event_pairs)
    lb = ' / '.join(f'{p["aspect"]}:{p["span_b"]["label"]}' for p in event_pairs)
    return {'score': score, 'conflict': True, 'time_slots_a': ta, 'time_slots_b': tb,
            'coverage': 'both_timed', 'mode': 'event', 'event_pairs': event_pairs,
            'event_time_score': score,
            'event_disjoint_slots': sorted({p['aspect'] for p in event_pairs
                                            if p['aspect']}),
            'event_overlap_slots': [],
            'event_slot_keys': _event_slot_keys,
            'reasons': [f'时间事实冲突（事件级）：[{la}] ↔ [{lb}]'
                        f'（同主体同方面时间区间不相交）']}

def _event_matches(events_a, events_b) -> List[Dict]:
    """§4.3：产出事件级对拍明细（仅同主体同方面事件对参与）。

    每条记录 {subject, aspect, time_key_a, time_key_b, time_relation,
              value_relation, score}（v2.2.0 增加三元身份 time_key 字段）：
      time_relation:  'disjoint'（期间不相交，非冲突）| 'overlap'（相交/相同）
                      | 'missing'（任一方缺时间，交由 keyed/legacy 评估）
      value_relation: 'opposite_polarity' | 'same' | 'different_value' | 'unknown'
      score:          事件级时间贡献分（disjoint=0；overlap 按粒度 35/60；missing=0）
    与 period_adjudication 聚合字段互为明细/汇总，供 research report 解释。
    """
    out: List[Dict] = []
    for x in (events_a or []):
        if not isinstance(x, dict):
            continue
        sx, ax = x.get('subject'), x.get('aspect')
        if not sx or not ax:
            continue
        for y in (events_b or []):
            if not isinstance(y, dict):
                continue
            if y.get('subject') != sx or y.get('aspect') != ax:
                continue
            tx, ty = x.get('time_span'), y.get('time_span')
            if tx and ty:
                try:
                    tr = 'overlap' if _spans_overlap(tx, ty) else 'disjoint'
                except Exception:
                    tr = 'overlap'
            else:
                tr = 'missing'
            pol_x, pol_y = x.get('polarity'), y.get('polarity')
            if pol_x and pol_y and pol_x != pol_y:
                vr = 'opposite_polarity'
            elif x.get('value') is None or y.get('value') is None:
                vr = 'unknown'
            elif x.get('value') == y.get('value'):
                vr = 'same'
            else:
                vr = 'different_value'
            sc = 0 if tr == 'disjoint' else (35 if tr == 'overlap' else 0)
            out.append({'subject': sx, 'aspect': ax,
                        'time_key_a': x.get('time_key', 'na'),
                        'time_key_b': y.get('time_key', 'na'),
                        'time_relation': tr, 'value_relation': vr, 'score': sc})
    return out


def time_slot_score(text_a, text_b, subject: str = '', subject_b=None,
                    events_a=None, events_b=None) -> Dict:
    """P0-OPEN-06：时间事实槽比对（v2.1.2 F-07 扩展主体闸 + 事件级对齐）。

    返回 {score, conflict, time_slots_a, time_slots_b, reasons, coverage[,
          mode, event_pairs]}。
      coverage:
        'both_timed' 双方可对拍（已评估）
        'partial'    仅一条有时间，或跨主体/无同方面事件对（无法对拍 → 未评估）
        'neither'    两条都无时间（未评估）
      conflict=True 仅当双方可对拍且区间两两不相交（同主体同方面时间矛盾）。
    冲突分：精确粒度（季/月）60（high 边界）；仅全年粗粒度 35（medium，容忍跨年口径）。
    v2.1.2 行为：
      - 兼容旧调用 `time_slot_score(text_a, text_b)`（无主体）→ 沿用全文级逻辑，零回归；
      - 双方主体已知且相等 → **事件级对齐**（仅同主体同方面事件对）；
      - 双方主体已知但不等 → 跨主体 → 不可对拍（coverage='partial'，不误报）。
    """
    # P1(F-12)：公开函数类型守卫（None / 非字符串 → 空串），不依赖调用方预归一。
    text_a = text_a if isinstance(text_a, str) else ''
    text_b = text_b if isinstance(text_b, str) else ''
    sb = subject if subject_b is None else subject_b
    subject = subject if isinstance(subject, str) else ''
    sb = sb if isinstance(sb, str) else ''

    # F-07：双方主体已知 → 主体闸 + 事件级对齐
    if subject and sb:
        if subject != sb:
            return {'score': 0, 'conflict': False, 'time_slots_a': [], 'time_slots_b': [],
                    'reasons': [], 'coverage': 'partial', 'mode': 'event',
                    'event_pairs': [], 'note': 'cross_subject'}
        ea = events_a if events_a is not None else _extract_events(text_a, subject)
        eb = events_b if events_b is not None else _extract_events(text_b, subject)
        return _event_time_score(ea, eb, subject)

    # 兼容路径（任一主体缺失）→ 旧全文级逻辑（零回归）
    ta = _parse_time_spans(text_a)
    tb = _parse_time_spans(text_b)
    if not ta and not tb:
        coverage = 'neither'
    elif ta and tb:
        coverage = 'both_timed'
    else:
        coverage = 'partial'

    if coverage != 'both_timed':
        return {'score': 0, 'conflict': False, 'time_slots_a': ta,
                'time_slots_b': tb, 'reasons': [], 'coverage': coverage,
                'mode': 'fulltext', 'event_pairs': []}

    if any(_spans_overlap(a, b) for a in ta for b in tb):
        return {'score': 0, 'conflict': False, 'time_slots_a': ta,
                'time_slots_b': tb, 'reasons': [], 'coverage': coverage,
                'mode': 'fulltext', 'event_pairs': []}

    coarse = all('Q' not in s['label'] and '月' not in s['label']
                 for s in ta + tb)
    score = 35 if coarse else 60
    la = ' / '.join(s['label'] for s in ta)
    lb = ' / '.join(s['label'] for s in tb)
    return {'score': score, 'conflict': True, 'time_slots_a': ta,
            'time_slots_b': tb, 'coverage': coverage,
            'mode': 'fulltext', 'event_pairs': [],
            'reasons': [f'时间事实冲突：[{la}] ↔ [{lb}]（时间区间不相交）']}


# GA11：否定误报豁免——这些短语中的「不/未」表"恒定/达成"而非否定对立
NEG_EXEMPT = {
    "持平", "不变", "基本持平", "保持不变", "维持不变", "稳定", "不止",
    "不久", "不断", "不仅", "不少", "不错", "不可", "不到", "不下",
}


def _neg_hits(text_low: str) -> List[str]:
    """命中否定词，但剔除豁免短语内的假命中。"""
    hits = []
    for w in NEG_WORDS_ZH | NEG_WORDS_EN:
        if w not in text_low:
            continue
        if any(ex in text_low and w in ex for ex in NEG_EXEMPT):
            continue
        hits.append(w)
    return hits


def _detect_negation(text_a: str, text_b: str) -> Tuple[int, List[str]]:
    """返回 (neg_score 0-50, reason_list)"""
    score = 0
    reasons = []
    # DEF-15：与 _extract_slots / keyed / time 路统一 50k 有界窗口，防长文本全文 .lower() 超时
    a_low, b_low = _slot_window(text_a).lower(), _slot_window(text_b).lower()

    # 1. 否定词（豁免"持平/不变"等非对立用法）
    hit_a = _neg_hits(a_low)
    hit_b = _neg_hits(b_low)
    # 否定词不对称（一正一反） → 20 分
    if (hit_a and not hit_b) or (hit_b and not hit_a):
        score += 20
        reasons.append(f'否定词不对称：a={hit_a[:3]} b={hit_b[:3]}')
    elif hit_a and hit_b:
        score += 5  # 双否定抵消轻扣

    # 2. 反义对（一正一反） → 40 分（最强信号）
    for pos, neg in ANTONYM_PAIRS:
        pa, pb = pos.lower(), neg.lower()
        in_a_pos = pa in a_low, pa in b_low
        in_a_neg = pb in a_low, pb in b_low
        if (in_a_pos[0] and in_a_neg[1]) or (in_a_neg[0] and in_a_pos[1]):
            score += 40
            reasons.append(f'反义对命中：{pos}↔{neg}')
    return min(score, 50), reasons


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def _sev(total: int) -> str:
    if total >= 60:
        return 'high'
    if total >= 30:
        return 'medium'
    if total >= 10:
        return 'low'
    return 'none'


def score_legacy(claim_a: Dict, claim_b: Dict, text_a: str, text_b: str) -> dict:
    """v2.4.x 原口径（短语袋 Jaccard + 否定/反义），作为 max 融合的否定路保留。"""
    slots_a = _extract_slots(text_a)
    slots_b = _extract_slots(text_b)
    shared = slots_a & slots_b
    union = slots_a | slots_b
    jaccard = len(shared) / max(len(union), 1)
    slot_score = int(jaccard * 30)

    neg_score, reasons = _detect_negation(text_a, text_b)
    total = slot_score + neg_score
    if len(shared) >= 2 and neg_score > 0:
        total = min(int(total * 1.4), 100)
        reasons.append(f'极性放大：共享槽={len(shared)} + 反义命中')
    return {'score': total, 'severity': _sev(total), 'reasons': reasons,
            'shared_slots': sorted(shared)[:5],
            'slot_score': slot_score, 'neg_score': neg_score}


def score_contradiction(claim_a: Dict, claim_b: Dict) -> Dict:
    """计算两条声明的语义矛盾分（GA11 v2.0.0：keyed + negation 两路 max 融合）

    参数: claim_a / claim_b 至少含 'text' 字段（与 conflict_v3 同结构）；
          可选 'entity'/'subject' 提供键控主体（缺省两条默认同一对比对象）。
    返回: {'score': 0-100, 'severity': ..., 'reasons', 'neg_hits',
           'shared_slots', 'slot_score', 'neg_score',          # 老字段语义不变
           'keyed_score', 'conflict_slots', 'scorer_mode',     # GA11 新增
           'time_score', 'time_slots_a', 'time_slots_b',      # P0-OPEN-06 时间槽
           'time_coverage', 'verdict'}                          # P0-OPEN-06 判定/覆盖率
    scorer_mode: 'keyed'（键控槽路主导）| 'negation'（否定/反义路主导）
                 | 'time'（P0-OPEN-06 时间事实槽主导）。
    verdict（P0-OPEN-06）:
        'conflict'          检出矛盾（score>0）
        'no_conflict'       已充分评估（双方都有可对拍事实槽）且未发现冲突
        'not_assessable'    未评估——双方均缺可对拍事实槽（无时间/无键控槽/无共享槽）
    """
    # P1(F-12)：入参文本归一化。claim 为 dict 但 text=None（或 text 为数字等
    # 非字符串）时，旧代码 text_a=None 直接传入 score_legacy（未 try 包裹）→
    # `_detect_negation`/`_extract_slots` 调 None.strip()/lower() 抛 AttributeError，
    # 击穿整个矛盾评分。统一在入口归一：None / 非字符串 → 空串（不当 'None'/'123'
    # 字面量参与比对，避免伪造矛盾）；非 dict 入参沿用 str() 容错（None→''）。
    def _claim_text(c):
        if not isinstance(c, dict):
            return str(c) if c is not None else ''
        v = c.get('text', '')
        return v if isinstance(v, str) else ''

    text_a = _claim_text(claim_a)
    text_b = _claim_text(claim_b)

    # 路 1：v2.4.x 原口径（Jaccard 槽 + 否定/反义）
    legacy = score_legacy(claim_a, claim_b, text_a, text_b)
    # 路 2：GA11 键控事实槽（同槽键值冲突）
    keyed = {}
    keyed_score_val = 0
    try:
        keyed = keyed_score(claim_a if isinstance(claim_a, dict) else {'text': text_a},
                            claim_b if isinstance(claim_b, dict) else {'text': text_b},
                            text_a, text_b)
        keyed_score_val = keyed['score']
    except Exception:
        keyed = {'conflict_slots': [], 'reasons': [],
                 'slots_a': {}, 'slots_b': {}}
    # 路 3：P0-OPEN-06 时间事实槽（年月/季度 → ISO 区间比对）；
    #       v2.1.2 F-07：加主体闸 + 事件级对齐（主体已知时只比对同主体同方面事件）。
    # 容错：时间解析依赖正则，任何异常（如外部 mock re）都不得击穿主评分，
    # 降级为"未评估"，与 keyed 路的健壮性契约一致（L3-05 守护）。
    subj_a = _subject_key(claim_a, text_a)
    subj_b = _subject_key(claim_b, text_b)
    # F-06：事件优先取 claim 携带的（生产链在**原始 body** 上抽取，跨越 500/300 两级截断）；
    #      缺失则就地兜底抽取（直调 / 旧调用兼容）。抽取异常一律降级空列表。
    ev_a, ev_b = [], []
    try:
        ev_a = (claim_a.get('events') if isinstance(claim_a, dict)
                and claim_a.get('events') is not None
                else _extract_events(text_a, subj_a))
        ev_b = (claim_b.get('events') if isinstance(claim_b, dict)
                and claim_b.get('events') is not None
                else _extract_events(text_b, subj_b))
    except Exception:
        ev_a, ev_b = [], []
    try:
        tslot = time_slot_score(text_a, text_b, subj_a, subj_b, ev_a, ev_b)
        time_score_val = tslot['score']
    except Exception:
        tslot = {'score': 0, 'reasons': [], 'coverage': 'neither',
                 'time_slots_a': [], 'time_slots_b': [], 'conflict': False,
                 'mode': 'fulltext',
                 # v2.2.0 事件字段异常兜底齐备（顶层 .get 不再恒取默认空）
                 'event_time_score': 0, 'event_pairs': [],
                 'event_disjoint_slots': [], 'event_overlap_slots': [],
                 'event_slot_keys': []}
        time_score_val = 0

    # max 融合：三路证据取强，不叠加（避免同义复述被相似度抬分）
    trio = [
        (keyed_score_val, 'keyed', keyed.get('reasons', [])),
        (legacy['score'], 'negation', legacy['reasons']),
        (time_score_val, 'time', tslot['reasons']),
    ]
    trio.sort(key=lambda x: -x[0])
    total = trio[0][0]
    mode = trio[0][1]
    # reasons 汇聚所有命中证据路（主导路在前）
    reasons = list(trio[0][2])
    for _sc, _m, _rs in trio[1:]:
        if _sc > 0:
            reasons.extend(_rs)

    # ── F-04 期间裁决（v2.1.2）：同主体同方面且双方期间均已知且不相交 →
    #   判为非冲突，落地为**降权**（×0.5，最低保留 1）——只降权、不滤除、不归零。
    adj = _period_adjudicate(ev_a, ev_b)
    if adj['disjoint_slots'] and total > 0:
        total = max(1, int(round(total * _PERIOD_DISJOINT_DAMP)))
        reasons = reasons + adj['reasons']

    # ── P0-OPEN-06：无冲突 / 未评估 区分（覆盖率）──
    # 可对拍事实槽覆盖：键控槽交集（同主体同方面）、时间双侧、legacy 共享槽。
    sa = keyed.get('slots_a', {}) or {}
    sb = keyed.get('slots_b', {}) or {}
    shared_keyed = bool(set(sa) & set(sb))
    both_timed = tslot['coverage'] == 'both_timed'
    # legacy 的 shared_slots 是 2-gram 短语袋，长文本极易偶然共享，
    # 仅在其相似度真正贡献了非平凡槽分（≥2 个共享槽）时才视为"可对拍"。
    legacy_assessable = legacy.get('slot_score', 0) >= 2
    assessable = shared_keyed or both_timed or legacy_assessable
    if total > 0:
        verdict = 'conflict'
    elif assessable:
        verdict = 'no_conflict'
    else:
        verdict = 'not_assessable'

    return {
        'score': total,
        'severity': _sev(total),
        'reasons': reasons,
        'neg_hits': legacy['reasons'],          # 兼容旧字段名（仅否定路）
        'shared_slots': legacy['shared_slots'],
        'slot_score': legacy['slot_score'],
        'neg_score': legacy['neg_score'],
        # GA11 新增字段（老消费方无感）
        'keyed_score': keyed_score_val,
        'conflict_slots': keyed.get('conflict_slots', []),
        'scorer_mode': mode,
        # P0-OPEN-06 时间事实槽 + 判定/覆盖率
        'time_score': time_score_val,
        'time_slots_a': tslot['time_slots_a'],
        'time_slots_b': tslot['time_slots_b'],
        'time_coverage': tslot['coverage'],
        'assessable': assessable,
        'verdict': verdict,
        # v2.1.2 事件槽批次（F-06 事件计数 / F-04 期间裁决 / F-07 time 路模式）
        'event_count_a': len(ev_a),
        'event_count_b': len(ev_b),
        'period_disjoint_slots': adj['disjoint_slots'],
        'period_overlap_slots': adj['overlap_slots'],
        'period_pair_details': adj.get('slot_pairs', []),
        'period_adjudication': ('disjoint' if adj['disjoint_slots']
                                else 'overlap' if adj['overlap_slots'] else 'none'),
        'time_mode': tslot.get('mode', 'fulltext'),
        # §4.3 事件级对拍明细（与 period_adjudication 互为明细/汇总）
        'event_matches': _event_matches(ev_a, ev_b),
        # v2.2.0 事件时间路审计字段（三元事件身份对拍明细，向各调用路径收口）
        'event_time_score': tslot.get('event_time_score', 0),
        'event_pairs': tslot.get('event_pairs', []),
        'event_disjoint_slots': tslot.get('event_disjoint_slots', []),
        'event_overlap_slots': tslot.get('event_overlap_slots', []),
        'event_slot_keys': tslot.get('event_slot_keys', []),
        # v2.2.0 B 层时间槽抑制明细（纯 A 层调用默认空；hybrid 路径由 LLM 层覆盖）
        'llm_time_suppressed': [],
        'llm_time_suppressed_slots': [],
    }


# ═══════════════════════════════════════════════════════════
# 可选 LLM 增强
# ═══════════════════════════════════════════════════════════

def score_with_llm(claim_a: Dict, claim_b: Dict, llm_router=None) -> Dict:
    """调用 LLM 拿矛盾评分。llm_router=None 时降级到 score_contradiction

    返回格式同 score_contradiction，并多 'llm_used': bool / 'llm_raw': str
    """
    if llm_router is None:
        # 沙箱无 LLM：直接退化为本地版本
        res = score_contradiction(claim_a, claim_b)
        res['llm_used'] = False
        return res

    text_a = claim_a.get('text', '') if isinstance(claim_a, dict) else str(claim_a)
    text_b = claim_b.get('text', '') if isinstance(claim_b, dict) else str(claim_b)
    prompt = (
        f"判断下列两条声明是否表达相反事实（输出 0-100 分，0=完全一致，100=完全矛盾）。\n"
        f"声明 A：{text_a[:300]}\n"
        f"声明 B：{text_b[:300]}\n"
        f"仅输出一个整数。"
    )
    try:
        raw = llm_router(prompt)
        # v2.2.0：router 合法返回 None/非字符串时归一化，避免 raw.strip() 抛错
        # 被外层 except 误判为异常降级（llm_used 应保持 True）。
        raw = raw if isinstance(raw, str) else str(raw or '')
        m = re.search(r'\d{1,3}', raw)
        score = int(m.group(0)) if m else 0
        score = max(0, min(score, 100))
        local = score_contradiction(claim_a, claim_b)
        # 取 LLM 与本地的较大值（任一一方强烈判矛盾都尊重）
        final = max(score, local['score'])
        # v2.2.0 收口：以完整 A 层结果为底（自动携带全部 keyed/event/period/
        # 三元槽字段），仅覆盖 LLM 相关字段——杜绝内联白名单在版本演进时漏挂。
        result = dict(local)
        result.update({
            'score': final,
            'severity': 'high' if final >= 75 else 'medium' if final >= 45
                       else 'low' if final >= 15 else 'none',
            'reasons': local['reasons'] + [f'LLM={score}'],
            'neg_hits': local['reasons'],
            'llm_used': True,
            'llm_raw': raw.strip()[:200],
        })
        # 同步路径不做 B 层时间槽 disjoint 抑制，但显式挂空审计字段，
        # 保证跨路径字段齐备。
        result.setdefault('llm_time_suppressed', [])
        result.setdefault('llm_time_suppressed_slots', [])
        return result
    except Exception as e:
        res = score_contradiction(claim_a, claim_b)
        res['llm_used'] = False
        res['llm_error'] = str(e)
        return res


# ═══════════════════════════════════════════════════════════
# GA11 B 层（v2.0.0）：LLM 辅助 JSON 槽表 → 复用键控比对
#   opt-in：INFOSEEK_CONTRADICTION_LLM=1 或 enable_llm=True
#   降级链：B 不可用（无 provider/解析失败）→ A（score_contradiction）→ legacy
# ═══════════════════════════════════════════════════════════

import hashlib as _hashlib
_LLM_SLOT_CACHE: Dict[str, dict] = {}
_LLM_SLOT_CACHE_MAX = 512

_LLM_SLOT_PROMPT = """你是事实核查助手。从下面这条声明中抽取结构化事实槽，只输出 JSON，不要解释。

输出 schema：
{"slots": [{"subject": "主体(原文实体，无法判断用空串)", "aspect": "方面英文蛇形命名(如 revenue/profit/ceo_name/hq_city/founded_year)", "value": "归一化值(数字尽量转阿拉伯数字；枚举用小写中文或英文)", "unit": "单位(%, 亿, 万, 年, 人, 个, 或空串)", "polarity": "pos|neg|neutral", "time_label": "该事实对应的时间标签原文(如 2024年/2024Q1/2024年上半年/截至2023年，无法判断留空串)", "time_start": "时间起点整数年份YYYY(季度月度归并到该年，无法判断留空串)", "time_end": "时间终点整数年份YYYY(闭区间结束年；单年事实与time_start相同；无法判断留空串)"}]}
规则：
1) 抽取该声明的核心事实槽，忽略评价性措辞；同一方面若在不同时间各有明确取值，必须分别输出为多个槽(各自带时间字段)，不要只保留一个值；确实没有时间归属的事实 time_label/time_start/time_end 留空串。
2) 数值统一为阿拉伯数字并标注 unit；百分比 unit 用 %。
3) 布尔/肯否事实（如是否开源、是否发布）polarity 用 pos/neg，value 用枚举词。
4) 只输出 JSON。

声明：%TEXT%
JSON："""


def _hash_texts(a: str, b: str) -> str:
    return _hashlib.md5((a + "\u0001" + b).encode("utf-8")).hexdigest()


def _parse_llm_slot_json(content: str) -> dict:
    """从 LLM 输出中鲁棒提取 JSON 槽表。失败抛 ValueError。"""
    if not content:
        raise ValueError("empty llm content")
    txt = content.strip()
    # 去掉 ```json fence
    if "```" in txt:
        m = re.search(r"```(?:json)?\s*(.*?)```", txt, re.S)
        if m:
            txt = m.group(1).strip()
    # 截取首个 { 到末个 }
    s, e = txt.find("{"), txt.rfind("}")
    if s == -1 or e == -1 or e <= s:
        raise ValueError("no json object")
    data = _json.loads(txt[s:e + 1])
    if not isinstance(data, dict) or not isinstance(data.get("slots"), list):
        raise ValueError("bad schema")
    return data


def _norm_num(v, unit):
    """归一 LLM 给的数值（支持中文数字单位简单换算）。返回 (float, unit) 或 None。"""
    try:
        f = float(str(v).replace(",", "").strip())
    except (ValueError, TypeError):
        return None
    return f, (unit or "").strip()


def _llm_slot_span(slot: dict):
    """从 LLM 槽取可严格解析的半开区间 dict{label,start,end}（ISO [start,end)）。

    优先 time_start/time_end（均须为 4 位 YYYY 整数年，闭区间年→次年 01-01 半开）；
    退化用 time_label 经 _parse_time_spans 严格解析（年/季/月，支持「2024年」「2024Q1」）。
    返回 dict 或 None（任一时间缺失/模糊 → None，调用方走保守比对）。
    """
    if not isinstance(slot, dict):
        return None
    label = str(slot.get("time_label", "") or "").strip()
    ts = str(slot.get("time_start", "") or "").strip()
    te = str(slot.get("time_end", "") or "").strip()

    # 优先：time_start/time_end 均为 4 位年（YYYY 闭区间年 → [YYYY-01-01, (YYYY+1)-01-01)）
    ms, me = re.match(r"^(\d{4})$", ts), re.match(r"^(\d{4})$", te)
    if ms and me:
        ys, ye = int(ms.group(1)), int(me.group(1))
        if ye >= ys:
            return {"label": label or f"{ts}-{te}",
                    "start": f"{ys:04d}-01-01", "end": f"{ye + 1:04d}-01-01"}

    # 退化：time_label 严格解析（_parse_time_spans 仅抽年/季/月，模糊表述返回空）
    if label:
        parsed = _parse_time_spans(label)
        if len(parsed) == 1:
            return parsed[0]
    return None


def _slots_disjoint(span_a, span_b) -> bool:
    """两个 ISO [start,end) 区间是否不相交（端点相接算 disjoint；与 _spans_overlap 互补）。"""
    if not span_a or not span_b:
        return False
    return not _spans_overlap(span_a, span_b)


def _llm_slot_conflicts(slots_a: list, slots_b: list):
    """同 (主体, aspect) 槽位笛卡尔逐对比对 value/unit/polarity。

    v2.2.0：一对槽若双方时间均可严格解析且 [start,end) 不相交，则不判
    冲突（不同时期不同取值），计入 suppressed 明细；任一侧时间缺失或
    模糊时维持保守比对（旧 LLM 无时间字段 → 行为与 v2.1.2 一致）。
    返回 (conflicts, suppressed)。
    """
    def index(slots):
        out = {}
        for sl in slots:
            if not isinstance(sl, dict):
                continue
            asp = str(sl.get("aspect", "")).strip().lower()
            if not asp:
                continue
            subj = re.sub(r"\s+", "", str(sl.get("subject", "")).lower())
            out.setdefault((subj, asp), []).append(sl)
        return out

    ia, ib = index(slots_a), index(slots_b)
    conflicts = []
    suppressed = []
    seen = set()
    seen_supp = set()
    for key in set(ia) & set(ib):
        subj, asp = key
        for ka in ia[key]:
            for kb in ib[key]:
                spa = _llm_slot_span(ka)
                spb = _llm_slot_span(kb)
                va0 = str(ka.get("value", "")).strip()
                vb0 = str(kb.get("value", "")).strip()
                if _slots_disjoint(spa, spb):
                    ck = ("llm-time", subj, asp, spa.get("label"), spb.get("label"), va0, vb0)
                    if ck not in seen_supp:
                        seen_supp.add(ck)
                        suppressed.append({
                            "subject": subj, "aspect": asp,
                            "time_label_a": spa.get("label"), "time_label_b": spb.get("label"),
                            "span_a": {"start": spa.get("start"), "end": spa.get("end")},
                            "span_b": {"start": spb.get("start"), "end": spb.get("end")},
                            "value_a": va0, "value_b": vb0,
                            "kind": "time_disjoint",
                        })
                    continue
                pa, pb = ka.get("polarity"), kb.get("polarity")
                if pa and pb and pa in ("pos", "neg") and pb in ("pos", "neg") and pa != pb:
                    ck = ("llm-pol", subj, asp)
                    if ck not in seen:
                        seen.add(ck)
                        conflicts.append((ck, f"[LLM:{asp}] 肯否冲突", asp))
                    continue
                na = _norm_num(ka.get("value"), ka.get("unit"))
                nb = _norm_num(kb.get("value"), kb.get("unit"))
                if na and nb:
                    (xa, ua), (xb, ub) = na, nb
                    if ua == ub:
                        base = max(abs(xa), abs(xb), 1.0)
                        rel = abs(xa - xb) / base
                        if asp.endswith("year"):
                            hit = abs(xa - xb) >= 1
                        elif ua == "%":
                            hit = abs(xa - xb) >= 3 and rel >= 0.15
                        else:
                            hit = rel >= 0.15
                        if hit:
                            ck = ("llm-num", subj, asp, round(min(xa, xb), 4),
                                  round(max(xa, xb), 4), ua)
                            if ck not in seen:
                                seen.add(ck)
                                conflicts.append((ck, f"[LLM:{asp}] 数值冲突 {xa:g}{ua}↔{xb:g}{ua}", asp))
                else:
                    va = va0.lower()
                    vb = vb0.lower()
                    if va and vb and va != vb:
                        ck = ("llm-enum", subj, asp, va, vb)
                        if ck not in seen:
                            seen.add(ck)
                            conflicts.append((ck, f"[LLM:{asp}] 枚举冲突 {va}↔{vb}", asp))
    return conflicts, suppressed

def _llm_keyed_score(parsed_a: dict, parsed_b: dict) -> dict:
    """对两份 LLM 槽表做键控冲突评分（单 35/双 60/≥3 85）。

    v2.2.0：时间不相交的异值槽对被抑制，不计冲突，明细经
    llm_time_suppressed(_slots) 透出审计。
    """
    conflicts, suppressed = _llm_slot_conflicts(
        parsed_a.get("slots", []), parsed_b.get("slots", []))
    n = len({c[0] for c in conflicts})
    score = 85 if n >= 3 else 60 if n == 2 else 35 if n == 1 else 0
    return {"score": score,
            "conflict_slots": sorted({c[2] for c in conflicts}),
            "reasons": [c[1] for c in conflicts],
            "llm_time_suppressed": suppressed,
            "llm_time_suppressed_slots": sorted({sp["aspect"] for sp in suppressed})}


def score_contradiction_hybrid(claim_a: Dict, claim_b: Dict, *,
                               enable_llm: Optional[bool] = None,
                               llm_call_fn=None, temperature: float = 0.0) -> Dict:
    """GA11 C 混合分层：B(LLM JSON 槽) → A(本地键控) → legacy。

    - enable_llm=None 时读 env INFOSEEK_CONTRADICTION_LLM；
    - LLM 不可用（无 provider/超时/JSON 解析失败）自动降级本地，不抛错；
    - 两路 max 融合：LLM 槽表用于补充 A 层覆盖不到的表外方面。
    返回在 score_contradiction 基础上增补 llm_used/scorer_mode 细化。
    """
    base = score_contradiction(claim_a, claim_b)  # 已含 A(keyed)+legacy negation
    if enable_llm is None:
        enable_llm = os.environ.get("INFOSEEK_CONTRADICTION_LLM", "").lower() \
            in ("1", "true", "on", "yes")
    if not enable_llm:
        base["llm_used"] = False
        base["llm_time_suppressed"] = []
        base["llm_time_suppressed_slots"] = []
        return base

    text_a = claim_a.get("text", "") if isinstance(claim_a, dict) else str(claim_a)
    text_b = claim_b.get("text", "") if isinstance(claim_b, dict) else str(claim_b)
    cache_key = _hash_texts(text_a[:5000], text_b[:5000])
    try:
        if cache_key in _LLM_SLOT_CACHE:
            llm_res = _LLM_SLOT_CACHE[cache_key]
        else:
            if llm_call_fn is None:
                from core.llm_router import llm_call as _llm_call
            else:
                _llm_call = llm_call_fn

            # A/B 分别独立出槽，保证槽归属正确（结果按文本哈希缓存）
            # 用字面替换而非 str.format：模板 JSON 示例含裸花括号
            def _one(text):
                p = _LLM_SLOT_PROMPT.replace("%TEXT%", text[:2000])
                o = _llm_call(p, max_tokens=400, temperature=temperature)
                return _parse_llm_slot_json(
                    o.get("content", "") if isinstance(o, dict) else str(o))

            parsed_a = _one(text_a)
            parsed_b = _one(text_b)
            llm_res = _llm_keyed_score(parsed_a, parsed_b)
            if len(_LLM_SLOT_CACHE) >= _LLM_SLOT_CACHE_MAX:
                _LLM_SLOT_CACHE.clear()
            _LLM_SLOT_CACHE[cache_key] = llm_res

        final_score = max(base["score"], llm_res["score"])
        base["keyed_score"] = max(base.get("keyed_score", 0), llm_res["score"])
        base["conflict_slots"] = sorted(set(base.get("conflict_slots", []))
                                        | set(llm_res["conflict_slots"]))
        base["reasons"] = base.get("reasons", []) + [
            r for r in llm_res["reasons"] if r not in base.get("reasons", [])]
        supp = llm_res.get("llm_time_suppressed", [])
        base["llm_time_suppressed"] = supp
        base["llm_time_suppressed_slots"] = llm_res.get(
            "llm_time_suppressed_slots", [])
        base["score"] = final_score
        base["severity"] = _sev(final_score)
        base["scorer_mode"] = "llm_hybrid" if llm_res["score"] > 0 else base["scorer_mode"]
        base["llm_used"] = True
        return base
    except Exception as e:
        # 降级链：B 失败 → A/legacy（base 已是其结果）
        base["llm_used"] = False
        base.setdefault("llm_time_suppressed", [])
        base.setdefault("llm_time_suppressed_slots", [])
        base["llm_error"] = f"{type(e).__name__}:{str(e)[:80]}"
        return base


# v2.7.2 PATCH: score_contradiction 异步版本；v2.7.3 PATCH: 内部逻辑清理
async def score_contradiction_async(claim_a: Dict, claim_b: Dict, llm_router=None) -> Dict:
    """v2.7.2 新增；v2.7.3 PATCH 清理：score_contradiction 异步版

    当前实现：asyncio.to_thread 包装同步 score_contradiction（CPU 密集）
    v1.0.1 PATCH / G6: 补齐 LLM 分支 —— llm_router 提供时走 score_with_llm_async
    """
    import asyncio
    if llm_router:
        return await score_with_llm_async(claim_a, claim_b, llm_router=llm_router)
    # v2.8.0：无 router 分支也走结构化槽 hybrid（env INFOSEEK_CONTRADICTION_LLM
    # 开启时经同步 llm_call 抽槽，整体 to_thread 包裹避免阻塞事件循环）
    return await asyncio.to_thread(score_contradiction_hybrid, claim_a, claim_b)


async def score_with_llm_async(claim_a: Dict, claim_b: Dict, llm_router=None) -> Dict:
    """v1.0.1 PATCH / G6: score_with_llm 异步版（补齐 v2.7.3 未实现接口）。

    llm_router 兼容两种签名：
    - 同步可调用 `llm_router(prompt) -> str`（旧接口，to_thread 包装）
    - 异步可调用 `await llm_router(prompt) -> str`（新接口，直接 await）

    返回格式同 score_with_llm（含 llm_used/llm_raw）。
    """
    import asyncio
    import inspect

    if llm_router is None:
        res = await asyncio.to_thread(score_contradiction, claim_a, claim_b)
        res['llm_used'] = False
        return res

    text_a = claim_a.get('text', '') if isinstance(claim_a, dict) else str(claim_a)
    text_b = claim_b.get('text', '') if isinstance(claim_b, dict) else str(claim_b)
    prompt = (
        f"判断下列两条声明是否表达相反事实（输出 0-100 分，0=完全一致，100=完全矛盾）。\n"
        f"声明 A：{text_a[:300]}\n"
        f"声明 B：{text_b[:300]}\n"
        f"仅输出一个整数。"
    )
    try:
        if inspect.iscoroutinefunction(llm_router) or inspect.iscoroutinefunction(
                getattr(llm_router, '__call__', None)):
            raw = await llm_router(prompt)
        else:
            raw = await asyncio.to_thread(llm_router, prompt)
        # v2.2.0：router 合法返回 None/非字符串时归一化（同步路径对齐）。
        raw = raw if isinstance(raw, str) else str(raw or '')
        m = re.search(r'\d{1,3}', raw)
        score = int(m.group(0)) if m else 0
        score = max(0, min(score, 100))
        local = await asyncio.to_thread(score_contradiction, claim_a, claim_b)
        final = max(score, local['score'])
        # v2.2.0 收口：以完整 A 层结果为底（自动携带全部 event/period/三元槽字段），
        # 仅覆盖 LLM 相关字段——杜绝内联白名单在版本演进时漏挂。
        result = dict(local)
        result.update({
            'score': final,
            'severity': 'high' if final >= 75 else 'medium' if final >= 45
                       else 'low' if final >= 15 else 'none',
            'reasons': local['reasons'] + [f'LLM={score}'],
            'neg_hits': local['reasons'],
            'llm_used': True,
            'llm_raw': raw.strip()[:200],
        })
        # 异步路径当前不做 B 层时间槽 disjoint 抑制（保持既有语义），
        # 但显式挂空审计字段，保证跨路径字段齐备。
        result.setdefault('llm_time_suppressed', [])
        result.setdefault('llm_time_suppressed_slots', [])
        return result
    except Exception as e:
        res = await asyncio.to_thread(score_contradiction, claim_a, claim_b)
        res['llm_used'] = False
        res['llm_error'] = str(e)
        return res


async def score_contradictions_batch_async(claim_pairs: List[tuple]) -> List[Dict]:
    """v2.7.2 新增：批量异步评分（asyncio.gather 并发）"""
    import asyncio
    return await asyncio.gather(
        *[score_contradiction_async(a, b) for a, b in claim_pairs]
    )


# ═══════════════════════════════════════════════════════════
# CLI: python core/contradiction_scorer.py "<text_a>" "<text_b>"
# ═══════════════════════════════════════════════════════════

def main():
    import sys
    import json as _json
    if len(sys.argv) < 3:
        print("usage: contradiction_scorer.py <text_a> <text_b>")
        sys.exit(1)
    res = score_contradiction({'text': sys.argv[1]}, {'text': sys.argv[2]})
    print(_json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
