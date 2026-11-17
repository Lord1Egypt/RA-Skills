"""
infoseek_zerodep_nlp.py — 零依赖 NLP 原语（v1.2.0）
=====================================================================

设计目标
--------
1. **纯标准库即可运行核心**：中文/英文关键词抽取、句子切分、基础摘要，
   不依赖 jieba / summa / httpx 等任何第三方包。
2. **外部 NLP 优先，零依赖为最终兜底（优先级链）**：
   jieba（中文主路径）→ summa（英文主路径/中文次路径）→ **zerodep 共识**。
   前两级可用时以其结果为准（不降级、不经过标准库过滤）；
   仅当外部 NLP 不可用/无结果时，才启用零依赖共识兜底。
3. **冗余验证兜底精度（最终兜底分支的硬约束）**：
   当无外部 NLP 时，并行运行多重独立的纯标准库估计器
   （A 多粒度 n-gram / B 位置加权 / C 文档频率 / **D 内置高频词典锚点**），
   通过「加权共识投票」(weighted consensus voting) 只保留被多估计器共同认可
   的候选词，再经最长匹配抑制 + 停用词闸，在弱分词环境下保持高精度。
4. **单频专业词锚点（v1.1.0）**：内置小型跨领域高频词典（≈250 中 + 40 英），
   解决 n-gram 对「只出现 1 次的专业词/词表输入」全盲的长尾召回缺口。
5. **动态锚点受控消费（v1.2.0，S5 晋级真锚）**：经统一访问函数
   `_active_zh_anchors()` 在显式开关 `INFOSEEK_LEARNED_ANCHORS=1` 下，
   将 learned_anchor_store 中裁决为 accept 的词与基线词典并集消费；
   默认关闭时逐字节回退基线 `_ZH_HIGH_FREQ`。对 store 仅惰性、可降级访问，
   主链不产生任何顶层硬依赖（import 失败/存储损坏一律回退基线）。

这是 infoseek 跨多生态平台发行（WorkBuddy / ima / Claude / Dify / Coze / 通用 MCP）
的底座前提：核心在「零 pip 安装」下也能产出可信结果。

用法
----
    from infoseek_zerodep_nlp import extract_keywords, extract_keywords_detailed, summarize
    kws, engine = extract_keywords_detailed("一段中文文本……", max_kw=15)
    # engine ∈ {"jieba", "summa", "zerodep", "empty"}
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable, List, Sequence, Set, Tuple

# ── S7：dep_registry 事实层惰性 accessor（零漂移，仅外部 NLP 可选点消费）──
_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        import os as _os
        import sys as _sys
        _core = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'core')
        if _core not in _sys.path:
            _sys.path.insert(0, _core)
        import dep_registry as _mod
        _dr = _mod
    return _dr

# ---------------------------------------------------------------------------
# 内置资源（纯标准库，无外部字典文件依赖）
# ---------------------------------------------------------------------------

# 轻量中文停用词典（覆盖高频虚词/标点，足以支撑兜底分词精度）
_ZH_STOP = set(
    "的 了 和 是 在 我 有 他 这 中 大 来 上 国 个 到 说 们 为 子 也 你 得 着 下 就 都 "
    "与 及 或 把 被 让 使 从 向 对 等 而 且 但 若 因 故 所 以 于 之 其 此 该 各 某 何 "
    "一种 一样 一些 这样 那样 这些 那些 这个 那个 我们 你们 他们 它们 自己 什么 怎么 "
    "可以 能够 应该 需要 进行 通过 根据 由于 以及 并且 然而 因此 所以 但是 如果 虽然 "
    "目前 当前 已经 正在 将要 之后 之前 之间 对于 关于 由于 基于 方面 问题 情况 方式 "
    "一个 一种 一项 一名 一位 一部分 一种 一种 相关 主要 重要 基本 整体 总体 一定 可能"
    .split()
)

# 英文停用词（缩小版，覆盖最常见虚词）
_EN_STOP = set(
    "the a an and or but if then else when while of to in on at by for with from as is "
    "are was were be been being this that these those it its he she they we you i my "
    "your our their his her not no nor do does did done has have had can could may might "
    "will would shall should must about into over under between through during before "
    "after above below up down out off so than too very also more most such same other "
    "which who whom whose what why how all any each few many much one two new first"
    .split()
)

# ── 内置小型高频词典（v1.1.0 增强：词表式切词锚点）──────────────────
# 设计目的：n-gram 估计器只认「重复出现的字符串」，对**只出现 1 次的专业词**
# （如词表输入「人工智能 大模型 量化交易」、长尾主题词）天然无能为力。
# 内置一份**小而高频**的跨领域词表作「词典匹配估计器」（估计器 D）：
# 在零 jieba 环境下提供确定性切词锚点，单频专业词也能被召回；
# 精度由「共识投票 + 最长匹配抑制」兜底，词典只做候选供给，不直接定结果。
# 规模刻意保持小型（≈250 词，纯字面常量，零外部文件依赖）；
# 收录原则：跨调研场景高复现的实义词，**不收**停用/泛指词（那些在 _ZH_STOP）。
_ZH_HIGH_FREQ = frozenset(
    # ── 科技 / 互联网 / AI ──
    "人工智能 大模型 自然语言处理 深度学习 机器学习 神经网络 生成式 语言模型 "
    "智能体 算力 算法 数据 数据库 向量数据库 语义搜索 知识图谱 推荐系统 "
    "计算机视觉 语音识别 自动驾驶 机器人 芯片 半导体 操作系统 云计算 区块链 "
    "开源 代码 软件 互联网 数字化 信息化 服务器 传感器 无人机 新能源汽车 电动车 "
    # ── 金融 / 经济 / 商业 ──
    "量化交易 量化投资 交易策略 风险控制 风险管理 投资组合 资产管理 资产配置 "
    "基本面 技术分析 市场份额 商业模式 盈利模式 产业链 供应链 供应链金融 "
    "宏观经济 货币政策 财政政策 上市公司 融资 并购 估值 市值 股价 基金 债券 "
    "期货 期权 外汇 利率 通胀 通缩 营收 利润 现金流 初创公司 创业 竞争格局 "
    # ── 医疗 / 健康 / 生物 ──
    "医疗卫生 医疗健康 医疗器械 生物医药 临床试验 创新药 仿制药 中医药 "
    "基因编辑 细胞治疗 免疫治疗 疫苗 诊断 康复 养老 养生 健康管理 公共卫生 "
    # ── 能源 / 材料 / 工业 ──
    "新能源 可再生能源 光伏 风电 储能 锂电池 氢能 核能 石油 天然气 煤炭 电力 "
    "新材料 纳米材料 复合材料 高端制造 智能制造 工业互联网 自动化 装备制造 "
    "钢铁 水泥 化工 有色金属 碳排放 碳中和 碳达峰 节能环保 环境保护 污染治理 "
    # ── 消费 / 教育 / 文娱 / 社会 ──
    "电子商务 直播带货 社交媒体 内容平台 在线教育 职业教育 文化旅游 影视娱乐 "
    "游戏产业 品牌营销 消费者 用户体验 新零售 物流配送 房地产 基础设施 "
    "乡村振兴 现代农业 粮食安全 公共服务 社会保障 政府政策 法律法规 行业研究 "
    "市场研究 发展趋势 市场规模 竞争优势 核心技术 解决方案 产品服务".split()
)

# 小型英文领域词典（AI/科技/商业高频；与中文词典同一估计器机制）
_EN_HIGH_FREQ = frozenset(
    "machine learning deep learning neural network artificial intelligence "
    "large language model generative ai data science computer vision "
    "natural language processing vector database semantic search knowledge graph "
    "recommendation system autonomous driving cloud computing blockchain "
    "open source operating system semiconductor supply chain business model "
    "market share risk management asset allocation portfolio quantitative trading "
    "trading strategy interest rate cash flow startup merger acquisition "
    "healthcare medical device clinical trial gene therapy vaccine "
    "renewable energy solar wind energy storage lithium battery electric vehicle "
    "carbon neutral e-commerce social media online education video game "
    "user experience brand marketing market research industry trend".split()
)


def _active_zh_anchors() -> frozenset:
    """统一访问协议：返回当前生效的中文锚点词典（S5 晋级真锚）。

    - 默认（INFOSEEK_LEARNED_ANCHORS 未开启）：逐字节回退基线
      `_ZH_HIGH_FREQ`，行为与 v2.3.0 完全一致；
    - 显式开启：返回「基线 ∪ learned_anchor_store 中裁决为 accept 的词」。

    对 store 采用**函数内惰性 import + try/except 全包裹**：主链不产生任何
    顶层硬依赖；store 模块缺失、存储损坏、读取异常时一律优雅回退基线，
    保证零依赖核心在任何环境下都可用。store 单向依赖本模块，无循环风险。
    """
    try:
        # 双路惰性导入：优先 core 包路径（与 store 自身 from core import
        # state_dir 的编排一致）；回退顶层模块名（core/ 已在 sys.path 的
        # 编排，如脚本直跑注入 scripts/ 与 core/）。两种编排都兜住。
        try:
            from core import learned_anchor_store as _las
        except Exception:
            import learned_anchor_store as _las

        if not _las.is_enabled():
            return _ZH_HIGH_FREQ
        accepted = _las.active_terms("accept")
        if not accepted:
            return _ZH_HIGH_FREQ
        return _ZH_HIGH_FREQ | frozenset(accepted)
    except Exception:
        return _ZH_HIGH_FREQ

_CJK = re.compile(r"[一-鿿]")
_SENT_SPLIT = re.compile(r"(?<=[。！？!?；;\.\n])|(?<=[。！？!?])")
_WORD_EN = re.compile(r"[A-Za-z][A-Za-z0-9+#.\-]*")
_CJK_RUN = re.compile(r"[一-鿿]+")


# ---------------------------------------------------------------------------
# 句子切分（标准库）
# ---------------------------------------------------------------------------

def segment_sentences(text: str) -> List[str]:
    """按中英文标点/换行切句，过滤空句。"""
    if not text:
        return []
    parts = re.split(r"(?<=[。！？!?；;\n])", text)
    out = []
    for p in parts:
        p = p.strip()
        if p:
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# 标准库估计器（无外部依赖，多重冗余）
# ---------------------------------------------------------------------------

def _longest_match_suppress(counter: Counter) -> List[str]:
    """最长匹配抑制：按 (长度降序, 词频降序) 保留候选，丢弃被更长候选包含的短片段。

    例：「人工智能/人工/工智/智能」→ 仅留「人工智能」。这是无 jieba 时
    保证关键词精度的关键：避免把一个词拆成多个噪声片段进入共识投票。
    """
    items = sorted(counter.items(), key=lambda kv: (len(kv[0]), kv[1]), reverse=True)
    kept: List[str] = []
    kept_set: Set[str] = set()
    for gram, _ in items:
        if any(gram in k for k in kept_set):
            continue
        kept.append(gram)
        kept_set.add(gram)
    return kept


def _ngram_freq(text: str, n: int, min_count: int = 2) -> Counter:
    """从 CJK 连续串中抽取 n 元语法词频。"""
    c = Counter()
    for run in _CJK_RUN.findall(text):
        for i in range(len(run) - n + 1):
            gram = run[i:i + n]
            # 仅剔除「完全由停用字构成」的虚词 n-gram（如「的是」）或
            # 整词命中停用短语（如「正在」）；含实字的组合（如「大模型」含「大」）必须保留
            if gram in _ZH_STOP or all(ch in _ZH_STOP for ch in gram):
                continue
            c[gram] += 1
    return Counter({k: v for k, v in c.items() if v >= min_count})


def _zh_whole_runs(text: str, max_len: int = 4) -> Set[str]:
    """残片实义片段提取（v1.1.0 锚点掩码配套，精度优先）。

    锚点掩码后连续串被切成多个残片（如「大模型技术正在快速迭代」
    摘除「大模型」→「技术正在快速迭代」）。不直接整段成词（残片可能
    含虚词、跨边界），而是**以停用字为切点**，只保留纯实义片段：

      「技术正在快速迭代」→ 按「正在」切 → {技术, 快速迭代}
      「任务上表现」       → 按「上」切   → {任务, 表现}

    跨词噪声（「任务上表」「正在快速」）因含停用字被切碎，无法整段供给；
    残片真词则可在 A/B/C 间获得互证。仅收 2-max_len 的纯实义片段。
    """
    out: Set[str] = set()
    for run in _CJK_RUN.findall(text):
        # 以停用字切段：连续「非停用字」实义子串
        buf = ''
        for ch in run:
            if ch in _ZH_STOP:
                if 2 <= len(buf) <= max_len:
                    out.add(buf)
                buf = ''
            else:
                buf += ch
        if 2 <= len(buf) <= max_len:
            out.add(buf)
    return out


def _est_zh_ngram(text: str, top: int = 20) -> Set[str]:
    """估计器 A：多粒度 n 元语法词频（2/3/4 字组合）。

    修复（环境重置回归）：min_count=2 会滤掉单次候选（如空格分隔的短语列表
    「人工智能 大模型 …」每词只出现 1 次），导致估计器为空 → 关键词全丢。
    此时回退 min_count=1 重建（召回优先、精度由共识投票兜底）。
    """
    c = Counter()
    for n in (2, 3, 4):
        grams = _ngram_freq(text, n, min_count=2)
        if not grams:
            grams = _ngram_freq(text, n, min_count=1)
        c.update(grams)
    # v1.1.0：并入短残片整词（锚点掩码后有效残片供给）
    c.update(Counter({w: 1 for w in _zh_whole_runs(text)}))
    # 过滤内置停用词与单字噪声已由 _ngram_freq 处理
    return set(_longest_match_suppress(c)[:top])


def _est_zh_position(text: str, top: int = 20) -> Set[str]:
    """估计器 B：标题/首尾句加权抽取——出现在前 30% 文本的高频 2-3 字组合。"""
    sents = segment_sentences(text)
    if not sents:
        return set()
    head = " ".join(sents[: max(1, len(sents) // 3)])
    c = Counter()
    for run in _CJK_RUN.findall(head):
        for n in (2, 3, 4):
            for i in range(len(run) - n + 1):
                gram = run[i:i + n]
                if gram in _ZH_STOP or all(ch in _ZH_STOP for ch in gram):
                    continue
                c[gram] += 1
    # v1.1.0：head 内短残片整词纳入（锚点掩码配套）
    c.update(Counter({w: 1 for w in _zh_whole_runs(head)}))
    # 同时要求该候选在全文中也出现过（位置 + 全局双重约束 → 高精度）
    full = (
        set(_ngram_freq(text, 2).keys())
        | set(_ngram_freq(text, 3).keys())
        | set(_ngram_freq(text, 4).keys())
        | _zh_whole_runs(text)
    )
    cands = [w for w in _longest_match_suppress(c) if w in full]
    return set(cands[:top])


def _est_zh_docfreq(text: str, top: int = 20) -> Set[str]:
    """估计器 C：类 TF-IDF 文档频率——在多个句子中出现过的 2-3 字组合。"""
    sents = segment_sentences(text)
    if not sents:
        return set()
    # 构建每个句子的 n-gram 集合（去重）
    sent_grams = []
    for s in sents:
        grams = set()
        for run in _CJK_RUN.findall(s):
            for n in (2, 3, 4):
                for i in range(len(run) - n + 1):
                    g = run[i:i + n]
                    if g in _ZH_STOP or all(ch in _ZH_STOP for ch in g):
                        continue
                    grams.add(g)
        grams |= _zh_whole_runs(s)  # v1.1.0：句内短残片整词
        sent_grams.append(grams)
    # 文档频率
    df = Counter()
    for grams in sent_grams:
        for g in grams:
            df[g] += 1
    # 仅在 >=2 个句子出现的候选（跨句一致性 → 高精度）
    cand = {g for g, f in df.items() if f >= 2}
    # 按 (文档频率, 全局词频) 排序
    global_freq = Counter()
    for run in _CJK_RUN.findall(text):
        for n in (2, 3):
            for i in range(len(run) - n + 1):
                g = run[i:i + n]
                if any(ch in _ZH_STOP for ch in g):
                    continue
                global_freq[g] += 1
    return set(_longest_match_suppress(Counter({g: df[g] for g in cand}))[:top])


# ── 词典匹配估计器（v1.1.0：词表式切词锚点，估计器 D）──────────────

def _est_zh_dictionary(text: str, top: int = 20) -> Set[str]:
    """估计器 D：内置高频词典匹配——在文本/词表中识别已知高频实义词。

    与 A/B/C 的本质差异：不依赖词频重复，**只出现 1 次的专业词也能命中**
    （n-gram 对单频词全盲，这是长尾/词表输入召回归零的关键缺口）。

    两条匹配通道：
      1. 连续文本：词典词作为子串扫描（长词优先，最长匹配抑制）；
      2. 词表输入（空格/标点分隔的短语列表）：分段后整段或段内词典词命中。
    仅供给候选；是否成为最终关键词由共识投票裁决，避免词典泛匹配噪声。
    """
    hits: Set[str] = set()
    remain = text
    # 通道 1：按词典词长度降序做子串匹配；命中后从该片段摘除，
    # 使长词优先（如先「人工智能」再「智能」），天然最长匹配抑制。
    for w in sorted(_active_zh_anchors(), key=len, reverse=True):
        idx = remain.find(w)
        if idx >= 0:
            hits.add(w)
            # 摘除命中片段（用空格占位，不破坏其余字符相对位置）
            remain = remain[:idx] + ('　' * len(w)) + remain[idx + len(w):]
            if len(hits) >= top:
                return hits
    return hits


def _est_en_dictionary(text: str, top: int = 20) -> Set[str]:
    """估计器 D（英文）：内置领域词典匹配（多词短语整体命中）。

    对多词短语（如 "machine learning"）做不区分大小写子串匹配；
    单词通过 token 集合命中。长短语优先。
    """
    low = text.lower()
    hits: Set[str] = set()
    # 多词短语优先匹配
    for phrase in sorted(_EN_HIGH_FREQ, key=lambda p: (p.count(' '), len(p)), reverse=True):
        if ' ' in phrase and phrase in low:
            hits.add(phrase)
            if len(hits) >= top:
                return hits
    toks = set(_WORD_EN.findall(text.lower()))
    for w in _EN_HIGH_FREQ:
        if ' ' not in w and w in toks:
            hits.add(w)
    return hits


def _mask_zh_anchors(text: str) -> str:
    """用词典锚点掩码切分连续中文串（v1.1.0 关键去噪）。

    命中的词典词替换为等长空格，使 n-gram **不跨锚点成串**——
    根治无 jieba 时「人工智能大模型」被滑出「智能大模/能大模型」
    这类跨词噪声；统计估计器随后只在锚点外残片上运行。
    长词优先匹配（与 _est_zh_dictionary 同序），避免短锚点截断长词。
    """
    out = text
    for w in sorted(_active_zh_anchors(), key=len, reverse=True):
        i = out.find(w)
        while i >= 0:
            out = out[:i] + ('　' * len(w)) + out[i + len(w):]
            i = out.find(w)
    return out


def _mask_en_anchors(text: str) -> str:
    """英文锚点掩码：命中的领域短语/单词替换为空格（短语优先）。"""
    low = text.lower()
    spans: List[Tuple[int, int]] = []
    for phrase in sorted(_EN_HIGH_FREQ, key=lambda p: (p.count(' '), len(p)), reverse=True):
        plen = len(phrase)
        start = low.find(phrase)
        while start >= 0:
            end = start + plen
            # 仅在未被更长锚点覆盖时登记
            if not any(not (end <= a or start >= b) for a, b in spans):
                spans.append((start, end))
            start = low.find(phrase, start + 1)
    out = list(text)
    for a, b in spans:
        for k in range(a, b):
            if out[k].strip():
                out[k] = ' '
    return ''.join(out)


def _est_en_tfidf(text: str, top: int = 20) -> Set[str]:
    """估计器（英文）：标准库 TF-IDF 近似。"""
    sents = re.split(r"[.!?\n]+", text)
    sents = [s.strip() for s in sents if s.strip()]
    doc_freq = Counter()
    for s in sents:
        toks = {t.lower() for t in _WORD_EN.findall(s)} - _EN_STOP
        for t in toks:
            doc_freq[t] += 1
    if not sents:
        return set()
    n = len(sents)
    scored = {}
    for t, df in doc_freq.items():
        idf = math.log((n + 1) / (df + 1)) + 1.0
        tf = sum(1 for s in sents for w in _WORD_EN.findall(s) if w.lower() == t)
        scored[t] = tf * idf
    return {t for t, _ in sorted(scored.items(), key=lambda x: x[1], reverse=True)[:top]}


# ---------------------------------------------------------------------------
# 冗余共识验证（核心：兜底精度）
# ---------------------------------------------------------------------------

def redundant_consensus(estimator_sets: Iterable[Set[str]], min_votes: int = 2) -> Set[str]:
    """对多个估计器产出的关键词集合做共识投票。

    一个候选词只有在 >= min_votes 个独立估计器中同时出现，才被认定为
    「高置信关键词」。这把无外部 NLP 时的弱分词噪声压到最低，
    用多重冗余换精度（precision-first）。

    返回：被共识认可的候选集合（高精度子集）。
    """
    sets = [s for s in estimator_sets if s]
    if not sets:
        return set()
    if len(sets) == 1:
        return set(sets[0])  # 无冗余可投，原样返回
    counter: Counter = Counter()
    for s in sets:
        for w in s:
            counter[w] += 1
    return {w for w, v in counter.items() if v >= min_votes}


def weighted_consensus(
    estimator_sets: Sequence[Set[str]],
    weights: Sequence[float] | None = None,
    threshold: float | None = None,
) -> Tuple[Set[str], Counter]:
    """加权共识投票（v1.1.0 强化版）。

    与等票 `redundant_consensus` 的差异：
      - 各估计器可带**权重**（词典锚点命中确定性高，但它与 n-gram 证据
        形态不同，默认略低于「统计证据之间互证」）；
      - 阈值 `threshold` **自适应**：默认按有效估计器数量取
        「≥2 票」语义（= 2 个单位权重），并对 2 估计器情形自动收窄，
        避免短文本（英文 2 估计器）整集通过失去投票意义。

    Args:
        estimator_sets: 各估计器候选集（空集忽略）。
        weights: 每个估计器权重；None → 全 1.0。
        threshold: 通过阈值；None → 自适应（见上）。

    Returns:
        (共识通过的候选集, 各候选累计加权票 Counter)。
    """
    pairs = [(s, w) for i, (s, w) in enumerate(
        zip(estimator_sets, weights or [1.0] * len(list(estimator_sets)))) if s]
    if not pairs:
        return set(), Counter()
    if len(pairs) == 1:
        only = set(pairs[0][0])
        c = Counter({w: pairs[0][1] for w in only})
        return only, c
    score: Counter = Counter()
    for s, w in pairs:
        for term in s:
            score[term] += w
    if threshold is None:
        # 自适应：≥2 个单位权重；2 估计器时要求两侧互证（阈值=满分-半单位）
        threshold = 2.0 if len(pairs) >= 3 else sum(w for _, w in pairs) - 0.5
    return {term for term, v in score.items() if v >= threshold}, score


def _est_en_freq(text: str, top: int = 20) -> Set[str]:
    """英文冗余估计器：纯词频（无 IDF），与 _est_en_tfidf 形成双重校验。"""
    toks = [t.lower() for t in _WORD_EN.findall(text)] or []
    c = Counter(w for w in toks if w not in _EN_STOP and len(w) > 1)
    return {w for w, _ in c.most_common(top)}


def _optional_jieba(text: str, top: int) -> Set[str]:
    """可选增强：jieba.textrank（中文友好）。不可用时返回空集。

    2026-09-29：jieba 探测/初始化统一经 core/jieba_bridge（原裸
    `import jieba.analyse` 每次调用 try-import；收敛后进程内一次）。
    """
    import os as _os
    import sys as _sys
    _core = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'core')
    if _core not in _sys.path:
        _sys.path.insert(0, _core)
    try:
        import jieba_bridge as _jb
        return _jb.textrank(text, top)
    except Exception:
        return set()


def _optional_summa(text: str, top: int) -> Set[str]:
    """可选增强：summa.keywords（英文友好）。不可用时返回空集。"""
    try:
        if not _dep_reg().is_available("summa"):
            return set()
        from summa.keywords import keywords as summa_keywords  # 懒加载
        txt = summa_keywords(text, words=top)
        return {w.strip() for w in (txt or "").split("\n") if w.strip()}
    except Exception:
        return set()


# ---------------------------------------------------------------------------
# 对外主入口
# ---------------------------------------------------------------------------

def detect_lang(text: str) -> str:
    zh = len(_CJK.findall(text))
    en = len(_WORD_EN.findall(text))
    return "zh" if zh >= en else "en"


def extract_keywords_detailed(
    text: str,
    max_kw: int = 15,
    lang: str | None = None,
    min_votes: int = 2,
) -> Tuple[List[Tuple[str, float]], str]:
    """抽取关键词 + 引擎标识。

    优先级链（零依赖分词为**最终兜底**，不是首选）：
      1. **jieba**（中文主路径）——语义分词精度最高；
      2. **summa**（英文主路径 / 中文次路径）；
      3. **zerodep 零依赖共识**（最终防线）——多重标准库估计器 + 共识投票
         (min_votes) + 最长匹配抑制，仅在前两级不可用时启用。

    返回: ([(词, 置信分)], 引擎名)，引擎名 ∈ {"jieba", "summa", "zerodep", "empty"}。
    外部 NLP 结果不再经过标准库过滤（避免拉低 jieba 精度），置信分统一标记 3.0。
    """
    if not text or not text.strip():
        return [], "empty"

    lang = lang or detect_lang(text)

    # ── 1) 外部 NLP 主路径（优先）────────────────────────────────
    ext: Set[str] = set()
    ext_engine: str | None = None
    if lang == "zh":
        jb = _optional_jieba(text, max_kw)
        if jb:
            ext |= jb
            ext_engine = "jieba"
        if not ext:  # jieba 不可用或无结果 → summa 次之
            sm = _optional_summa(text, max_kw)
            if sm:
                ext |= sm
                ext_engine = "summa"
    else:
        sm = _optional_summa(text, max_kw)
        if sm:
            ext |= sm
            ext_engine = "summa"

    if ext:
        ranked = sorted(ext, key=len, reverse=True)[:max_kw]
        return [(w, 3.0) for w in ranked], ext_engine or "external"

    # ── 2) 零依赖共识（最终兜底）────────────────────────────────
    # v1.1.0：估计器从 3 个扩到 **4 个**（+ 词典匹配 D，锚定单频专业词）。
    # 统计估计器 A/B/C 吃「锚点掩码后文本」：词典锚点处断开连续串，
    # 杜绝 n-gram 跨词噪声（如「智能大模」）；锚点词由 D 独立供给。
    if lang == "zh":
        masked = _mask_zh_anchors(text)
        estimators: List[Set[str]] = [
            _est_zh_ngram(masked, max_kw),
            _est_zh_position(masked, max_kw),
            _est_zh_docfreq(masked, max_kw),
            _est_zh_dictionary(text, max_kw),
        ]
    else:
        masked_en = _mask_en_anchors(text)
        estimators: List[Set[str]] = [
            _est_en_tfidf(masked_en, max_kw),
            _est_en_freq(masked_en, max_kw),
            _est_en_dictionary(text, max_kw),
        ]

    # 分层共识合成（v1.1.0 重构：按证据可信度分层，而非全部混投）
    # 证据可信度：词典锚点（确定性命中）> 多估计器统计互证 > 单估计器单票（噪声）。
    n_stats = len(estimators) - 1
    stat_sets = estimators[:n_stats]
    dict_set = estimators[n_stats]

    # 统计层：A/B/C（英文 A/B）等权互证；阈值默认 ≥2 估计器
    _threshold = None if min_votes == 2 else float(min_votes)
    stat_consensus, stat_score = weighted_consensus(
        stat_sets, weights=[1.0] * n_stats, threshold=_threshold)

    # 覆盖估计器数（未加权；排序/置信用）
    cover: Counter = Counter()
    for s in stat_sets:
        for w in s:
            cover[w] += 1

    # ── 层 1：词典锚点——命中即高置信（确定性先验，不需向随机 n-gram 互证）──
    anchors = set(dict_set)
    # ── 层 2：统计共识——补「词表外」的多估计器互证词（锚点已含则不重复）──
    stat_won = set(_longest_match_suppress(Counter(stat_consensus))) - anchors

    # 最终精度闸：合并后整体最长匹配抑制（丢弃被长词包含的短片段）
    merged_raw = anchors | stat_won
    merged = set(_longest_match_suppress(Counter({w: 1 for w in merged_raw})))

    if merged:
        def _rank_key(w):
            # 锚点优先于统计词；同层按统计覆盖/票数、词长
            return (0 if w in anchors else 1,
                    -cover.get(w, 0), -stat_score.get(w, 0.0), -len(w))
        ranked = sorted(merged, key=_rank_key)[:max_kw]

        # 分层置信（统一 (0, 3] 量纲）：
        #   锚点 + 统计互证（被统计层也发现）→ 最高 ~2.8
        #   纯锚点（词表单频，统计层无证据）→ 2.4
        #   纯统计共识（词表外，跨估计器互证）→ 按覆盖数 ~2.0-2.6
        out: List[Tuple[str, float]] = []
        for w in ranked:
            if w in anchors:
                conf = 2.8 if cover.get(w, 0) >= 1 else 2.4
            else:
                conf = round(min(2.6, 1.6 + 0.4 * cover.get(w, 1)), 3)
            out.append((w, conf))
        return out, "zerodep"

    # 无锚点且无统计共识（极短/单句且词表无命中）：召回兜底。
    # 仅在「完全没有高置信证据」时，取统计层票数最高候选并显著降权 0.5
    # （保留旧语义；单票噪声与有效残片此层无法区分，故降权交调用方参考）。
    fallback_terms = _longest_match_suppress(Counter(dict(stat_score)))
    ranked = sorted(
        fallback_terms, key=lambda w: (stat_score[w], len(w)), reverse=True)[:max_kw]
    return [(w, round(float(stat_score[w]) * 0.5, 3)) for w in ranked], "zerodep"


def extract_keywords(
    text: str,
    max_kw: int = 15,
    lang: str | None = None,
    min_votes: int = 2,
) -> List[Tuple[str, float]]:
    """抽取关键词，返回 [(词, 置信分), ...]，按置信分降序（简单接口）。

    优先级链见 `extract_keywords_detailed`：jieba/summa 优先，
    零依赖共识为最终兜底。
    """
    kws, _ = extract_keywords_detailed(
        text, max_kw=max_kw, lang=lang, min_votes=min_votes
    )
    return kws


def summarize(text: str, max_sentences: int = 3, lang: str | None = None) -> str:
    """极简抽取式摘要：取「含最多共识关键词」的句子。"""
    sents = segment_sentences(text)
    if not sents:
        return ""
    kws = {w for w, _ in extract_keywords(text, max_kw=20, lang=lang)}
    if not kws:
        return " ".join(sents[:max_sentences])
    scored = []
    for s in sents:
        score = sum(1 for kw in kws if kw in s)
        scored.append((score, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    return " ".join(s for _, s in scored[:max_sentences])


# ---------------------------------------------------------------------------
# 自测（零 pip 依赖验证）：`python infoseek_zerodep_nlp.py`
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample_zh = (
        "人工智能大模型技术正在快速迭代。大模型在自然语言处理任务上表现突出，"
        "大模型推动了生成式人工智能的发展。多家科技公司发布了自研大模型产品，"
        "开源大模型生态也在迅速扩张。人工智能与大模型的结合正在重塑软件产业。"
    )
    sample_en = (
        "Vector databases index high-dimensional embeddings for semantic search. "
        "Embeddings power retrieval augmented generation in modern LLM applications. "
        "Semantic search relies on efficient vector similarity at scale."
    )

    print("=== 中文关键词（优先级链自测）===")
    zh_kw, zh_engine = extract_keywords_detailed(sample_zh, max_kw=10)
    assert zh_kw, "必须至少产出 1 个关键词"
    print(f"  engine={zh_engine}")
    for w, s in zh_kw:
        print(f"  {w:<10} score={s}")

    print("\n=== 英文关键词（优先级链自测）===")
    en_kw, en_engine = extract_keywords_detailed(sample_en, max_kw=10)
    assert en_kw, "必须至少产出 1 个关键词"
    print(f"  engine={en_engine}")
    for w, s in en_kw:
        print(f"  {w:<18} score={s}")

    print("\n=== 摘要 ===")
    print("  " + summarize(sample_zh, max_sentences=2))

    print("\n=== 零依赖兜底专项（v1.1.0）===")
    from unittest import mock as _mock
    with _mock.patch.object(__import__(__name__), '_optional_jieba', return_value=set()), \
         _mock.patch.object(__import__(__name__), '_optional_summa', return_value=set()):
        # 词表输入：单频专业词须被词典锚点召回
        kz, ez = extract_keywords_detailed(
            "人工智能 大模型 量化交易", max_kw=5)
        _kwset = {w for w, _ in kz}
        assert ez == "zerodep" and {"人工智能", "大模型", "量化交易"} <= _kwset, kz
        # 掩码去噪：连续文本不得产出跨词噪声
        kn, _ = extract_keywords_detailed(
            "人工智能大模型技术正在快速迭代。大模型在自然语言处理任务上表现突出。",
            max_kw=8)
        _noise = [w for w, _ in kn if "大模" in w and w != "大模型"]
        assert not _noise, f"跨词噪声={_noise}"
        print("  锚点召回 + 掩码去噪 断言通过")

    print("\n[OK] 零依赖核心在纯标准库下运行成功，无需任何 pip 安装。")
