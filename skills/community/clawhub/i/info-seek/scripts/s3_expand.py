#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/s3_expand.py — S3 锚点扩样选种骨架 (mod-v1.0.0)

把散落在 workspace/s2_anchor_observe 的一次性观测脚本
(observe_anchors_s3.py / filter_pipeline_s3.py / select_seeds_s4.py) 固化为
**skill 仓库内可复用**的扩样选种骨架，落地 ROADMAP L135 待办四项：
  - 扩样每主题≥20篇：make_synthetic_corpus(per_topic) 合成语料（无真实样本时 Agent 自造）
  - 词性维度落地：jieba.posseg 可选依赖（缺失降级名词性启发式）+ NOUN_POS 白名单
  - 通用词桶半自动构建：build_generic_bucket（后缀/前缀模式 + 跨域≥2）
  - 阈值敏感性网格：threshold_grid_scan（cover/topic 阈值扫描 hit 曲线）

数据格式见 references/s3-expand-schema.md。

== 纯离线只读 == 不挂接 infoseek 任何生产模块（不 import infoseek_zerodep_nlp /
不碰 _ZH_HIGH_FREQ 主链），实体分流用内置 ENTITY_TERMS + 后缀规则，零耦合。

CLI:
  python scripts/s3_expand.py --demo                  # 合成语料(11主题×20篇)→选种全链 self-check
  python scripts/s3_expand.py --corpus DIR --out DIR  # 真实语料目录(每主题一子目录或 topic_*.txt)→选种
  python scripts/s3_expand.py --grid                  # 仅跑阈值敏感性网格
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MOD_VERSION = "mod-v1.0.0"

# ---------------------------------------------------------------------------
# 常量（吸收 filter_pipeline_s3.py / select_seeds_s4.py 真源口径）
# ---------------------------------------------------------------------------
MIN_LEN, MAX_LEN = 2, 8
COVER_MIN = 0.15          # P1 覆盖率低门（S3_扩样校准结论.md §1.2 干净拐点）
NOUN_POS = {"n", "nz", "nv", "nvn", "vn", "nt", "ns", "nns"}  # 名词性白名单
# jieba 经 core/jieba_bridge 单源委托（infoseek 约束：全仓仅 bridge 裸 import jieba）
_ROOT = Path(__file__).resolve().parent.parent
for _p in (str(_ROOT / "core"), str(_ROOT / "scripts"), str(_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import jieba_bridge as _jb

_JIEBA_MOD = _jb.get_jieba()
_JIEBA_POSEG = _jb.get_posseg()
HAS_JIEBA = _JIEBA_MOD is not None

# 大类划分（方案 A 通用跨域 / 方案 B 金融大宗），用于 cat_cross_count
TOPIC_CATS: Dict[str, str] = {
    "低空经济": "A", "人形机器人": "A", "固态电池": "A", "创新药": "A",
    "量子计算": "A", "跨境电商": "A",
    "碳酸锂": "B", "工业硅": "B", "稀土": "B", "AI算力": "B", "铜": "B",
}
TOPIC_TERMS = list(TOPIC_CATS.keys())

# 实体分流：ORG/PRODUCT/PERSON 后缀 + 内置实体名
ENTITY_SUFFIX = ("公司", "集团", "股份", "科技", "工信部", "发改委", "海关", "局", "所")
ENTITY_TERMS = ("宁德时代", "赣锋锂业", "天齐锂业", "亿纬锂能", "摩根大通", "海关总署",
                "字节跳动", "特斯拉", "比亚迪", "英伟达", "华为", "腾讯", "工信部",
                "发改委", "乘联会")

# 通用词桶规则（S3_扩样校准结论.md §3，收紧后缀避免"造能力/技术持续"误入）
GENERIC_SUFFIX = ("格局", "规模", "链", "份额", "模式", "体系", "生态", "逻辑",
                  "路径", "结构", "中枢", "趋势")
GENERIC_PREFIX = ("同比", "环比", "市场", "核心", "产业", "行业", "技术", "业务",
                  "战略", "全球", "国内")
# 停用词（模板连词/功能词，跨主题但非锚，过滤候选）
STOPWORDS = {"板块", "持续", "扩张", "进入", "放量", "阶段", "成熟", "拉动", "增长",
             "稳步", "提升", "的", "量产", "进度", "领先", "近期", "动态", "领域",
             "突破", "指标", "态势", "进展", "特征", "增强", "制造", "能力", "优化",
             "技术", "产业", "市场", "供给缺口", "中枢", "中枢上"}

# ---------------------------------------------------------------------------
# 合成语料词表（无真实样本 → Agent 自造）
# ---------------------------------------------------------------------------
# 各主题专属术语（doc_hits 低、topic_cross=1，演示分布，不被选）
SPECIFIC_TERMS: Dict[str, List[str]] = {
    "低空经济": ["低空空域", "eVTOL", "无人机", "空域管理", "起降场", "飞行汽车"],
    "人形机器人": ["伺服电机", "减速器", "力传感器", "丝杠", "机器人本体", "运动控制"],
    "固态电池": ["半固态", "正极材料", "电解质", "锂盐", "电池量产", "隔膜"],
    "创新药": ["司美格鲁肽", "ADC", "靶点", "临床试验", "原料药", "仿制药"],
    "量子计算": ["量子比特", "量子纠缠", "量子通信", "超导量子", "拓扑量子"],
    "跨境电商": ["海外仓", "独立站", "跨境支付", "跨境物流", "关税", "贸易壁垒"],
    "碳酸锂": ["锂云母矿", "氢氧化锂", "磷酸铁锂", "锂资源", "锂矿"],
    "工业硅": ["金属硅", "多晶硅", "硅料", "有机硅", "硅片", "硅基"],
    "稀土": ["氧化镨钕", "镨钕", "稀土永磁", "永磁材料", "磁材", "钕铁硼"],
    "AI算力": ["智算中心", "光模块", "液冷", "GPU", "算力芯片", "服务器"],
    "铜": ["电解铜", "再生铜", "铜冶炼", "铜加工", "阴极铜", "废铜"],
}
# 跨主题 true anchor（每个出现于≥3个主题 → 触发主门，应选为 seed）
TRUE_ANCHORS: List[Tuple[str, List[str]]] = [
    ("技术壁垒", ["固态电池", "创新药", "人形机器人", "稀土"]),
    ("供需缺口", ["碳酸锂", "工业硅", "铜", "稀土"]),
    ("价格中枢", ["碳酸锂", "工业硅", "铜", "稀土"]),
    ("出口管制", ["稀土", "固态电池", "创新药"]),
    ("动力电池", ["固态电池", "人形机器人", "低空经济"]),
    ("能源转型", ["固态电池", "工业硅", "铜"]),
    ("具身智能", ["人形机器人", "固态电池", "AI算力"]),
    ("数据中心", ["AI算力", "固态电池", "跨境电商"]),
]
TRUE_ANCHOR_TERMS = {t for t, _ in TRUE_ANCHORS}  # 选种优先：真锚不进通用桶
# 边缘锚（仅跨 2 主题 → 演示 watch 观察桶）
EDGE_ANCHORS: List[Tuple[str, List[str]]] = [
    ("减速器技术", ["人形机器人", "固态电池"]),
    ("永磁材料", ["稀土", "人形机器人"]),
    ("硅基材料", ["工业硅", "固态电池"]),
]
# 通用框架词（跨全部主题 → 落入通用桶，显式白名单）
GENERIC_TERMS = ["产业链", "供应链", "产能", "需求", "成本", "价格", "规模", "格局",
                 "集中度", "市场份额", "技术路线", "商业模式", "应用场景", "产业趋势",
                 "供给", "出口"]
# 被锁定的长词（preprocess add_word，使碎片子串 cover=0）
LOCK_WORDS: List[str] = []
for _v in SPECIFIC_TERMS.values():
    LOCK_WORDS += _v
for _t, _ in TRUE_ANCHORS:
    LOCK_WORDS.append(_t)
LOCK_WORDS += GENERIC_TERMS
LOCK_WORDS += ENTITY_TERMS
for _t, _ in EDGE_ANCHORS:
    LOCK_WORDS.append(_t)
LOCK_SET = set(LOCK_WORDS)  # 锁定的领域词（真锚/术语/通用框架/实体）一律视为名词性
if HAS_JIEBA:  # 模块级锁词，候选抽取与过滤管线共享同一分词边界
    for _w in LOCK_SET:
        _JIEBA_MOD.add_word(_w)


# ---------------------------------------------------------------------------
# 合成语料生成器
# ---------------------------------------------------------------------------
def make_synthetic_corpus(per_topic: int = 20, seed: int = 42,
                          out_dir: Optional[str] = None) -> Dict[str, List[str]]:
    """生成 11 主题 × per_topic 篇合成中文语料。

    自带 true anchors（跨主题出现≥3）→ 演示选种主门；
    通用框架词 → 落入通用桶；实体 → 分流；碎片（长词子串）→ 覆盖率低被 P1 拒。
    若 out_dir 给定，写 corpus/<topic>_<NN>.txt（body 从首行正文起，无 DATE: 前缀）。
    """
    rng = random.Random(seed)
    corpus: Dict[str, List[str]] = {}
    for topic in TOPIC_TERMS:
        docs = []
        for i in range(per_topic):
            docs.append(_build_doc(rng, topic))
        corpus[topic] = docs
    if out_dir:
        od = Path(out_dir) / "corpus"
        od.mkdir(parents=True, exist_ok=True)
        for topic, docs in corpus.items():
            for idx, doc in enumerate(docs, 1):
                (od / f"{topic}_{idx:02d}.txt").write_text(doc, encoding="utf-8")
    return corpus


def _build_doc(rng: random.Random, topic: str) -> str:
    sp = SPECIFIC_TERMS.get(topic, [])
    specific = rng.sample(sp, k=min(3, len(sp)))
    anchors = [t for t, ts in TRUE_ANCHORS if topic in ts]
    if not anchors:  # 兜底：保证每主题有跨主题词（如量子计算）
        anchors = [t for t, _ in TRUE_ANCHORS]
    rng.shuffle(anchors)
    anchors = anchors[: rng.randint(2, 3)]
    edges = [t for t, ts in EDGE_ANCHORS if topic in ts]  # 跨2主题边缘锚→watch
    generics = rng.sample(GENERIC_TERMS, k=rng.randint(1, 2))
    entity = rng.choice(ENTITY_TERMS) if rng.random() < 0.4 else ""
    s = [f"{topic}板块，{specific[0]}产能持续扩张，{anchors[0]}进入放量阶段；"]
    if len(specific) > 1:
        s.append(f"{specific[1]}技术成熟，拉动{anchors[1] if len(anchors) > 1 else anchors[0]}需求增长，")
    s.append(f"{generics[0]}集中度稳步提升。")
    if entity:
        s.append(f"{entity}的{specific[-1]}量产进度领先，")
    s.append(f"{generics[-1] if len(generics) > 1 else generics[0]}格局优化。")
    if edges:  # 边缘锚独立成句，确保写入（激活 watch 观察桶）
        ew = rng.sample(edges, 1)[0]
        s.append(f"{ew}。")
    return "".join(s)


# ---------------------------------------------------------------------------
# 候选抽取（不挂主链，纯 n-gram 统计 + 跨主题聚合）
# ---------------------------------------------------------------------------
_CN = re.compile(r"[一-鿿]")


def extract_candidates(corpus: Dict[str, List[str]]) -> List[Dict]:
    """候选抽取：jieba 分词优先（token 天然有意义词，无跨词拼接伪词）；
    无 jieba 降级 n-gram（允许噪声，演示用）。

    返回候选 list（doc_hits>=3 且非停用词），每候选含：
      term, doc_hits, freq_total, topic_cross_count, cat_cross_count, consensus_doc_hits
    """
    if HAS_JIEBA:
        stat: Dict[str, Dict] = {}
        for topic, docs in corpus.items():
            cat = TOPIC_CATS.get(topic, "A")
            for doc in docs:
                toks = set()
                for w, _s, _e in _JIEBA_MOD.tokenize(doc):
                    if MIN_LEN <= len(w) <= MAX_LEN and all(_CN.match(c) for c in w):
                        toks.add(w)
                full = "".join(c for c in doc if _CN.match(c))
                for w in toks:
                    e = stat.setdefault(w, {"doc_hits": 0, "freq_total": 0,
                                          "topics": set(), "cats": set()})
                    e["doc_hits"] += 1
                    e["topics"].add(topic)
                    e["cats"].add(cat)
                    e["freq_total"] += full.count(w)
        cands = []
        for term, e in stat.items():
            if e["doc_hits"] < 3 or term in STOPWORDS:
                continue
            cands.append({
                "term": term, "doc_hits": e["doc_hits"], "freq_total": e["freq_total"],
                "topic_cross_count": len(e["topics"]), "cat_cross_count": len(e["cats"]),
                "consensus_doc_hits": e["doc_hits"] if e["doc_hits"] >= 2 else 0,
            })
        return cands
    # 降级：n-gram（无 jieba）
    stat: Dict[str, Dict] = {}
    for topic, docs in corpus.items():
        cat = TOPIC_CATS.get(topic, "A")
        for doc in docs:
            seen = set()
            chars = [c for c in doc if _CN.match(c)]
            n = len(chars)
            for L in range(MIN_LEN, MAX_LEN + 1):
                for s in range(n - L + 1):
                    gram = "".join(chars[s:s + L])
                    if gram in seen:
                        continue
                    seen.add(gram)
                    e = stat.setdefault(gram, {"doc_hits": 0, "freq_total": 0,
                                              "topics": set(), "cats": set()})
                    e["doc_hits"] += 1
                    e["freq_total"] += 1
                    e["topics"].add(topic)
                    e["cats"].add(cat)
            full = "".join(chars)
            for gram in seen:
                cnt = full.count(gram)
                if cnt > 1:
                    stat[gram]["freq_total"] += (cnt - 1)
    cands = []
    for term, e in stat.items():
        if e["doc_hits"] < 3 or term in STOPWORDS or len(term) < 3:
            continue
        cands.append({
            "term": term, "doc_hits": e["doc_hits"], "freq_total": e["freq_total"],
            "topic_cross_count": len(e["topics"]), "cat_cross_count": len(e["cats"]),
            "consensus_doc_hits": e["doc_hits"] if e["doc_hits"] >= 2 else 0,
        })
    return cands


# ---------------------------------------------------------------------------
# 预处理（jieba 分词边界 + 词性；可选依赖）
# ---------------------------------------------------------------------------
def _preprocess(corpus: Dict[str, List[str]]) -> List[Tuple[str, str, str, set, set, Dict[str, str]]]:
    """返回每篇 (name, topic, text, starts, ends, posmap)。

    starts/ends 为 jieba token 边界；posmap 为 word→pos（首次）。无 jieba 时边界空、posmap 空。
    """
    data = []
    if HAS_JIEBA:
        for w in set(LOCK_WORDS):
            _JIEBA_MOD.add_word(w)
    for topic, docs in corpus.items():
        for idx, doc in enumerate(docs, 1):
            name = f"{topic}_{idx:02d}"
            starts, ends, posmap = set(), set(), {}
            if HAS_JIEBA:
                tokens = list(_JIEBA_MOD.tokenize(doc))
                pairs = list(_JIEBA_POSEG.cut(doc))
                pmap = {}
                for w, flag in pairs:
                    pmap.setdefault(w, flag)
                for w, s, e in tokens:
                    starts.add(s)
                    ends.add(e)
                    # 锁定领域词强制名词性（jieba 对未登录 4 字词标 x，S3 结论 §2）
                    posmap[w] = "n" if w in LOCK_SET else pmap.get(w, "x")
            data.append((name, topic, doc, starts, ends, posmap))
    return data


def _heuristic_pos(term: str) -> str:
    """无 jieba 时名词性启发式（名词后缀→n，否则 x）。"""
    if term[-1] in "业链率机能量器化型度口质材源矿厂":
        return "n"
    return "x"


def _cover_of(term: str, starts: set, ends: set, text: str) -> Optional[float]:
    """term 在 text 中边界对齐占比（P1 覆盖率）。无边界数据→None（降级不判碎片）。"""
    if not starts:
        return None
    hits = [m.start() for m in re.finditer(re.escape(term), text)]
    if not hits:
        return None
    aligned = sum(1 for i in hits if i in starts and i + len(term) in ends)
    return aligned / len(hits)


# ---------------------------------------------------------------------------
# 过滤管线 P0-P3（吸收 filter_pipeline_s3.py）
# ---------------------------------------------------------------------------
_TIME = ("年", "月", "日", "季度", "周")
_CONN = ("的", "和", "与", "及", "或", "在", "对", "为", "是", "了", "也", "将", "等", "类", "方面", "相关", "通过", "基于")
_TMPL = ("第一", "第二", "第三", "近日", "目前", "显示", "表示", "指出", "认为", "预计")


def _p0_structural(term: str) -> Optional[str]:
    """P0 结构门：时间/功能连接/模板残片/标点/纯字母数字/<2或>8字。返回 gate 名或 None。"""
    if not (MIN_LEN <= len(term) <= MAX_LEN):
        return "len"
    if not _CN.match(term) or not all(_CN.match(c) for c in term):
        return "non_cn"
    if term[-1] in _TIME:
        return "time"
    if term in _CONN:
        return "conn"
    if term in _TMPL:
        return "tmpl"
    return None


def filter_pipeline(cands: List[Dict], corpus: Dict[str, List[str]]) -> List[Dict]:
    """P0 结构门 → P1 覆盖率碎片门(COVER_MIN) → P2 实体分流 → P3 通用门占位。

    返回 anchors list（dict：term, pos, is_entity, is_generic, cover, drop_gates,
    topic_cross_count, cat_cross_count, doc_hits, consensus_doc_hits, freq_total）。
    """
    prep = _preprocess(corpus)
    anchors = []
    for c in cands:
        term = c["term"]
        gate = _p0_structural(term)
        drop_gates = [gate] if gate else []
        # P2 实体分流
        is_entity = term in ENTITY_TERMS or term.endswith(ENTITY_SUFFIX)
        # P1 覆盖率（聚合该候选所有出现 doc）
        covers = []
        pos = None
        if HAS_JIEBA:
            for name, topic, text, starts, ends, posmap in prep:
                if term in text:
                    cov = _cover_of(term, starts, ends, text)
                    if cov is not None:
                        covers.append(cov)
                    if pos is None and term in posmap:
                        pos = posmap[term]
        else:
            pos = _heuristic_pos(term)
        cover = (sum(covers) / len(covers)) if covers else (None if not HAS_JIEBA else 0.0)
        if HAS_JIEBA and cover is not None and cover < COVER_MIN:
            drop_gates.append("fragment")
        anchors.append({
            "term": term,
            "pos": pos or _heuristic_pos(term),
            "is_entity": is_entity,
            "is_generic": False,  # 由 build_generic_bucket 回填
            "cover": cover,
            "drop_gates": drop_gates,
            "topic_cross_count": c["topic_cross_count"],
            "cat_cross_count": c["cat_cross_count"],
            "doc_hits": c["doc_hits"],
            "consensus_doc_hits": c["consensus_doc_hits"],
            "freq_total": c["freq_total"],
        })
    return anchors


# ---------------------------------------------------------------------------
# 通用词桶半自动（S3_扩样校准结论.md §3）
# ---------------------------------------------------------------------------
def _is_generic_rule(term: str, cat_cross: int) -> bool:
    """后缀(格局/规模/链/份额/模式…)或前缀(同比/市场/核心…) + 跨域≥2。"""
    if cat_cross < 2:
        return False
    if any(term.endswith(suf) for suf in GENERIC_SUFFIX):
        return True
    if any(term.startswith(pre) for pre in GENERIC_PREFIX):
        return True
    return False


def build_generic_bucket(anchors: List[Dict]) -> List[str]:
    """半自动通用词桶：显式白名单 + 规则命中(后缀/前缀+跨域≥2) + cover>=0.9，剔除实体。"""
    gw = set(GENERIC_TERMS)
    out = []
    for a in anchors:
        if a["is_entity"]:
            continue
        if a["term"] in TRUE_ANCHOR_TERMS:  # 真锚优先，剔除主题真锚（S3 结论 §3）
            continue
        cover_ok = (a["cover"] is None) or (a["cover"] >= 0.9)
        if (a["term"] in gw or _is_generic_rule(a["term"], a["cat_cross_count"])) and cover_ok:
            out.append(a["term"])
    # 回填 anchors.is_generic
    gs = set(out)
    for a in anchors:
        a["is_generic"] = a["term"] in gs
    return out


# ---------------------------------------------------------------------------
# 选种主门（吸收 select_seeds_s4.py）
# ---------------------------------------------------------------------------
def select_seeds(anchors: List[Dict], builtin: Optional[List[str]] = None) -> Dict:
    """硬排除：实体/通用桶/内置_ZH_HIGH_FREQ/drop_gate非空/<2字/非名词性pos。
    主门：topic_cross_count>=3 且 cover>=0.9 且 名词性pos → seeds(pending)
    观察桶：topic_cross_count==2 且 名词性pos → watch
    """
    builtin = builtin or []
    seeds, watch, excluded = [], [], {}
    for a in anchors:
        term = a["term"]
        reasons = []
        if a["is_entity"]:
            reasons.append("entity")
        if a["is_generic"]:
            reasons.append("generic")
        if term in builtin:
            reasons.append("builtin")
        if a["drop_gates"]:
            reasons.append("/".join(a["drop_gates"]))
        if len(term) < MIN_LEN:
            reasons.append("len")
        if a["pos"] not in NOUN_POS:
            reasons.append("non_noun_pos")
        if reasons:
            key = reasons[0]
            excluded[key] = excluded.get(key, 0) + 1
            continue
        tcc = a["topic_cross_count"]
        cover_ok = (a["cover"] is None) or (a["cover"] >= 0.9)
        if tcc >= 3 and cover_ok:
            seeds.append({
                "term": term, "status": "pending", "topic_cross_count": tcc,
                "cat_cross_count": a["cat_cross_count"], "cover": a["cover"],
                "doc_hits": a["doc_hits"], "consensus_doc_hits": a["consensus_doc_hits"],
                "freq_total": a["freq_total"], "pos": a["pos"], "len": len(term),
            })
        elif tcc == 2:
            watch.append({
                "term": term, "topic_cross_count": tcc,
                "cat_cross_count": a["cat_cross_count"], "cover": a["cover"],
                "doc_hits": a["doc_hits"], "pos": a["pos"], "len": len(term),
            })
    # 种子内子串对（去重提示）
    intra = []
    st = [s["term"] for s in seeds]
    for i in range(len(st)):
        for j in range(i + 1, len(st)):
            if st[i] in st[j] or st[j] in st[i]:
                intra.append((st[i], st[j]))
    return {
        "meta": {
            "phase": "S4", "rule": "topic>=3&cover>=0.9&noun_pos",
            "n_seeds": len(seeds), "n_watch_topic2": len(watch),
            "excluded_breakdown": excluded, "intra_seed_substring_pairs": intra,
        },
        "seeds": seeds, "watch_topic2": watch,
    }


# ---------------------------------------------------------------------------
# 阈值敏感性网格（S3_扩样校准结论.md §1.2）
# ---------------------------------------------------------------------------
def threshold_grid_scan(anchors: List[Dict],
                        cover_vals=(0.05, 0.10, 0.15, 0.20, 0.30),
                        topic_vals=(2, 3, 4)) -> Dict:
    """扫描 cover 碎片拒数 + topic 主门 seeds 数，输出 hit 曲线。"""
    grid = {"cover_fragment_reject": {}, "topic_seeds": {}}
    for cv in cover_vals:
        rej = sum(1 for a in anchors if a["cover"] is not None and 0 <= a["cover"] < cv
                  and not a["is_entity"] and a["pos"] in NOUN_POS)
        grid["cover_fragment_reject"][cv] = rej
    for tv in topic_vals:
        n = sum(1 for a in anchors
                if a["pos"] in NOUN_POS and not a["is_entity"] and not a["is_generic"]
                and (a["cover"] is None or a["cover"] >= 0.9)
                and a["topic_cross_count"] >= tv)
        grid["topic_seeds"][tv] = n
    return grid


# ---------------------------------------------------------------------------
# 语料加载（真实模式）
# ---------------------------------------------------------------------------
def load_corpus(corpus_dir: str) -> Dict[str, List[str]]:
    """从目录加载：①每主题一子目录 ②扁平 topic_*.txt（topic 取自文件名前缀）。"""
    d = Path(corpus_dir)
    corpus: Dict[str, List[str]] = {}
    subdirs = [p for p in d.iterdir() if p.is_dir()]
    if subdirs:
        for sd in subdirs:
            topic = sd.name
            corpus[topic] = [t.read_text(encoding="utf-8") for t in sorted(sd.glob("*.txt"))]
    else:
        for f in sorted(d.glob("*.txt")):
            m = re.match(r"^(.+?)_", f.stem)
            topic = m.group(1) if m else "default"
            corpus.setdefault(topic, []).append(f.read_text(encoding="utf-8"))
    return corpus


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def run(corpus: Dict[str, List[str]]) -> Dict:
    cands = extract_candidates(corpus)
    anchors = filter_pipeline(cands, corpus)
    generic = build_generic_bucket(anchors)
    sel = select_seeds(anchors)
    grid = threshold_grid_scan(anchors)
    return {
        "meta": {
            "mod_version": MOD_VERSION, "n_topics": len(corpus),
            "n_docs": sum(len(v) for v in corpus.values()),
            "n_candidates": len(cands), "n_anchors": len(anchors),
            "n_generic": len(generic), "has_jieba": HAS_JIEBA,
        },
        "anchors_filtered": anchors,
        "generic_bucket": generic,
        "seeds": sel,
        "grid": grid,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="S3 扩样选种骨架 (mod-v1.0.0)")
    ap.add_argument("--demo", action="store_true", help="合成语料(11×20)全链 self-check")
    ap.add_argument("--corpus", help="真实语料目录")
    ap.add_argument("--out", help="输出目录（写 anchors_filtered_S3.json 等）")
    ap.add_argument("--grid", action="store_true", help="仅跑阈值敏感性网格")
    ap.add_argument("--per-topic", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args(argv)

    if args.demo or (not args.corpus and not args.grid):
        corpus = make_synthetic_corpus(per_topic=args.per_topic, seed=args.seed,
                                        out_dir=args.out)
        print(f"[demo] 合成语料 {len(corpus)} 主题 × {args.per_topic} 篇，jieba={'ON' if HAS_JIEBA else 'OFF'}")
    elif args.corpus:
        corpus = load_corpus(args.corpus)
        print(f"[corpus] 加载 {len(corpus)} 主题，共 {sum(len(v) for v in corpus.values())} 篇")
    else:
        corpus = {}

    if args.grid:
        cands = extract_candidates(corpus)
        anchors = filter_pipeline(cands, corpus)
        grid = threshold_grid_scan(anchors)
        print(json.dumps(grid, ensure_ascii=False, indent=2))
        return 0

    res = run(corpus)
    m = res["meta"]
    print(f"[meta] candidates={m['n_candidates']} anchors={m['n_anchors']} "
          f"generic={m['n_generic']} seeds={res['seeds']['meta']['n_seeds']} "
          f"watch={res['seeds']['meta']['n_watch_topic2']}")
    print(f"[seeds] {[s['term'] for s in res['seeds']['seeds']]}")
    print(f"[generic] {res['generic_bucket'][:10]}...({len(res['generic_bucket'])}词)")
    print(f"[grid] cover_fragment_reject={res['grid']['cover_fragment_reject']}")
    print(f"[grid] topic_seeds={res['grid']['topic_seeds']}")
    print(f"[excluded] {res['seeds']['meta']['excluded_breakdown']}")
    if args.out:
        od = Path(args.out)
        od.mkdir(parents=True, exist_ok=True)
        (od / "anchors_filtered_S3.json").write_text(
            json.dumps({"anchors": res["anchors_filtered"]}, ensure_ascii=False, indent=2), encoding="utf-8")
        (od / "generic_bucket_S3.json").write_text(
            json.dumps({"generic_terms": res["generic_bucket"]}, ensure_ascii=False, indent=2), encoding="utf-8")
        (od / "learned_seeds_S4.json").write_text(
            json.dumps(res["seeds"], ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[out] 已写 {od}/anchors_filtered_S3.json, generic_bucket_S3.json, learned_seeds_S4.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
