#!/usr/bin/env python3
"""
anchor_adapter.py — v1 Anchor_Score 实现（mod-v2.0.2 标记 DEPRECATED）

版本维度声明（v1.8.1 治理）：本文件内 v2.0.2 为「模块内部版本 mod-v」，v1.7.x 为
「变更溯源标记」，均非 skill 对外版本（见 mcp_tools_common.SKILL_VERSION），不可比较大小。

v2.0.2 状态：
- 本文件保留为 v1 实现（向后兼容）
- 新代码请用 core/anchor_score_v2.compute_final_score_v2()
- v2.0.2 重构：纯函数式 + 模块化
- 旧 calculate_score() 仍可用，但内部调用 v2 + 发出 DeprecationWarning

演进史：
- v1.2.0: 四轴加权 + 双层复活
- v1.5.0: 五维 + 时间衰减
- v1.6.0: 第 6 维（跨平台）+ 跨主题分析
- v1.7.0: 第 8 维（语义相似度）
- v1.7.4: TF-IDF 退化修复 → Jaccard
- v1.8.1: domain_router 联动
- v1.9.0: 特殊 subject 字典展开
- v2.0.2: 重构为 core/anchor_score_v2.py（纯函数）
"""

from typing import List, Optional
import os
import re
import sys
import warnings
import functools
from pathlib import Path

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home())))
# v1.0.0 状态层中立：归档目录解析统一走 state_dir（env INFOSEEK_ARCHIVE → ~/infoseek-archives）
CORE_DIR = Path(__file__).parent.parent / 'core'
SCRIPTS_DIR = Path(__file__).parent
for _p in (str(CORE_DIR), str(SCRIPTS_DIR)):   # 幂等：模块加载期一次
    if _p not in sys.path:
        sys.path.insert(0, _p)
from state_dir import get_archives_dir
# GA5 分词单源化（v1.8.4）：唯一分词真源；_tokenize_subject 退化为薄封装委托
from text_tokenizer import tokenize_text

# ── S7：dep_registry 事实层惰性 accessor（core/ 已在上面注入 sys.path，零漂移）──
_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        import dep_registry as _mod
        _dr = _mod
    return _dr


def infos_to_seek(anchor: dict) -> Optional[dict]:
    """
    将 infos 锚点转换为 seek 意图卡片

    输入: {name, platform, type?, score, entry, entry_type}
    输出: {platform, type, quantity, tech, entry, entry_type}
    返回 None 表示过滤（噪声锚点 score < 40）
    """
    # 噪声过滤
    if anchor.get("score", 0) < 40:
        return None

    platform_lower = (anchor.get("platform") or "").lower()
    entry_type = anchor.get("entry_type", "URL")
    entry = anchor.get("entry", "")

    # ─── 规则 1: URL 类 ───
    if entry_type == "URL":
        if any(vp in platform_lower for vp in ["b站", "bilibili", "youtube", "哔哩哔哩"]):
            return {"platform": anchor["platform"], "type": "video", "quantity": "single",
                    "tech": "auto", "entry": entry, "entry_type": "URL"}
        if any(pp in platform_lower for pp in ["知乎", "zhihu"]):
            return {"platform": anchor["platform"], "type": "article", "quantity": "single",
                    "tech": "可能需要登录", "entry": entry, "entry_type": "URL"}
        return {"platform": "web", "type": "article", "quantity": "single",
                "tech": "auto", "entry": entry, "entry_type": "URL"}

    # ─── 规则 2: 名称类（需搜索发现）───
    if entry_type in ("名称", "频道名"):
        if any(bp in platform_lower for bp in ["b站", "bilibili", "哔哩哔哩"]):
            return {"platform": "B站", "type": "author_content", "quantity": "recent_10",
                    "tech": "bilibili-api", "entry": entry, "entry_type": "频道名"}
        if any(wp in platform_lower for wp in ["公众号", "wechat", "微信"]):
            return {"platform": "公众号", "type": "content", "quantity": "unknown",
                    "tech": "需用户提供分享链接", "entry": entry, "entry_type": "名称"}
        if "视频号" in platform_lower:
            return {"platform": "视频号", "type": "content", "quantity": "unknown",
                    "tech": "需用户提供分享链接", "entry": entry, "entry_type": "名称"}
        if any(zp in platform_lower for zp in ["知识星球", "zsxq", "星球"]):
            return {"platform": "知识星球", "type": "content", "quantity": "unknown",
                    "tech": "需Cookie", "entry": entry, "entry_type": "名称"}
        return {"platform": "综合", "type": "author_content", "quantity": "recent_10",
                "tech": "需搜索", "entry": entry, "entry_type": "名称"}

    # 兜底
    return {"platform": "web", "type": "unknown", "quantity": "single",
            "tech": "需确认", "entry": entry, "entry_type": "URL"}


# ═══════════════════════════════════════════════════════════════
# v1.7.0 新增: 第 8 维（语义相似度）
# ═══════════════════════════════════════════════════════════════

def compute_semantic_similarity(text: str, subject: str, method: str = "jaccard") -> int:
    """
    语义相似度评分 (v1.7.0 第 8 维)

    v1.7.4 默认算法: 关键词集合 Jaccard 相似度（三跑择优 summa+jieba+regex）
    v1.7.3 实验版: TF-IDF（公式退化，已废弃，不推荐使用）
    v1.7.2 baseline: TF-IDF 加权（中英混合友好但公式复杂）
    v1.7.1 baseline: summa 关键词 + Jaccard / 字符串包含

    参数:
        text: 待评估的源文本
        subject: 调研主题
        method: 算法 ("jaccard" / "tfidf" / "summa" / "string")
    返回: 0-100 分
    """
    if not text or not subject:
        return 0

    try:
        if method == "jaccard":
            return _jaccard_similarity(text, subject)

        elif method == "tfidf":
            # v1.7.4 兼容路径：仍可用，但内部已重定向到 jaccard
            # （v1.7.3 退化的 TF-IDF 已废弃，保留入口仅作向后兼容）
            import warnings
            warnings.warn(
                "method='tfidf' is deprecated since v1.7.4 due to v1.7.3 formula "
                "degradation; falling back to Jaccard similarity. "
                "Use method='jaccard' explicitly.",
                DeprecationWarning,
                stacklevel=2
            )
            return _jaccard_similarity(text, subject)

        elif method == "summa":
            if not _dep_reg().is_available("summa"):
                return _jaccard_similarity(text, subject)
            from summa.keywords import keywords as summa_keywords

            text_kw_text = summa_keywords(text, words=20)
            subject_kw_text = summa_keywords(subject, words=10)

            text_kw = set(k.strip() for k in text_kw_text.split('\n') if k.strip())
            subject_kw = set(k.strip() for k in subject_kw_text.split('\n') if k.strip())

            # summa 对中文支持差（subject 关键词为空）→ 降级到 jaccard
            if not text_kw or not subject_kw:
                return _jaccard_similarity(text, subject)

            # Jaccard 相似度 = 交集 / 并集
            intersection = text_kw & subject_kw
            union = text_kw | subject_kw
            return int(len(intersection) / len(union) * 100)

        else:
            return _string_containment_similarity(text, subject)

    except Exception:
        # summa/jaccard 不可用 → 最低级降级：字符串包含
        return _string_containment_similarity(text, subject)


def _tokenize_subject(subject: str) -> set:
    """subject 主体词提取（v1.7.8 P1#4 词级命中率口径 / v1.8.4 GA5 单源化委托）

    **实现已收敛至唯一真源 `text_tokenizer.tokenize_text()`**（GA5 闭合）——本函数退化为
    薄封装，仅为向后兼容既有调用点（`_string_containment_similarity`）与测试断言而保留名字。

    历史：v1.7.8 与 `infoseek_pipeline._tokenize_query` 各自独立实现同一套「jieba 优先 →
    缺失回退 findall 中英数分段」逻辑；v1.8.2 对齐回退算法但两份代码仍并存（审计 P1-1
    「同算法」声明曾被实测证伪：6 样本 3 分叉）；v1.8.4 抽公共 `tokenize_text` 彻底单源化，
    口径漂移风险归零。

    与 query 侧的唯一差异（有意设计，非漂移）：本函数**无中文前置门控**（服务通用词级命中率，
    需处理任意语言 subject）；`_tokenize_query` 传 `require_chinese=True`（服务
    `_filter_relevant` 的中文多字词硬门槛）。
    """
    return tokenize_text(subject)


def _string_containment_similarity(text: str, subject: str) -> int:
    """词级命中率（v1.7.8 P1#4：命中主体词数 / 主体词总数 × 100）

    替代 v1.7.1 字符片段口径（中文逐字）——中文改多字词级（_tokenize_subject，
    jieba 优先 → 缺失回退 2-gram），与 _filter_relevant 硬门槛同口径。
    接入 max(jaccard, containment×0.8) 融合（pipeline / core_v2 调用方不变）。

    返回: 0-100
    """
    if not text or not subject:
        return 0

    subject_words = _tokenize_subject(subject)
    if not subject_words:
        return 0

    text_lower = text.lower()
    matched = sum(1 for w in subject_words if w in text_lower)
    return int(matched / len(subject_words) * 100)


# v1.9.0 修补④ 特殊 subject 字典展开
SPECIAL_SUBJECTS = {
    'last30days': 'last30days recent community discussions hacker news reddit x.com emerging ai agent techniques trends',
    'arxiv': 'arxiv preprints academic papers research latest papers machine learning',
    'github-trending': 'github trending repositories popular projects recent activity',
    'wechat-mp': '微信公众号文章 公众号 微信文章 最新',
    'zhihu': '知乎 问答 讨论 热门话题 最新',
}


def _expand_special_subject(subject: str) -> str:
    """短 subject 字典后缀展开（v1.9.0 修补）

    针对专有名词 subject（Last30days/Arxiv 等）只有 1-2 个词，导致 Jaccard 永远 0 分的问题，
    在 Jaccard 计算前先用字典展开为长串查询词组。
    """
    subj_lower = subject.lower().strip()
    for canonical, expansion in SPECIAL_SUBJECTS.items():
        if subj_lower == canonical or subj_lower == expansion.lower():
            return expansion
    return subject


def _jaccard_similarity(text: str, subject: str) -> int:
    """关键词集合 Jaccard 相似度

    v1.7.4 替代 v1.7.3 退化的 TF-IDF（公式退化为常数 stub）。
    v1.9.0 修补特殊 subject（短专有名词字典展开）。

    公式:
      sim = |A ∩ B| / |A ∪ B| × 100（×自适应系数 1.2-1.8）

    思路:
      1. 字典展开 subject（v1.9.0）
      2. 三跑流水线提取 text 关键词（summa + jieba + regex fallback）
      3. 同样三跑流水线提取 subject 关键词
      4. 计算 Jaccard
      5. 按文本长度自适应加权（短 1.8 / 中 1.5 / 长 1.2）

    返回: 0-100 分
    """
    # v1.9.0 特殊 subject 字典展开
    subject = _expand_special_subject(subject)

    if not text or not subject:
        return 0

    try:
        # 1. 提取 text 关键词集合
        text_kw = _extract_keywords_three_run(text, max_keywords=20)
        # 2. 提取 subject 关键词集合
        subject_kw = _extract_keywords_three_run(subject, max_keywords=10)

        if not text_kw or not subject_kw:
            return _string_containment_similarity(text, subject)

        # 3. Jaccard 相似度
        intersection = text_kw & subject_kw
        union = text_kw | subject_kw
        if not union:
            return 0
        sim = int(len(intersection) / len(union) * 100)
        # v1.8.1 强化：自适应加权（短文本高系数，长文本低系数）
        # 短文本（<50 词）更容易匹配 → 系数 1.8（确保覆盖 15-30）
        # 中等文本（50-200 词）→ 系数 1.5（保持 15-35）
        # 长文本（>200 词）→ 系数 1.2（避免 100 分堆积）
        text_word_count = len(text.split()) if text else len(text_kw) * 3
        if text_word_count < 50:
            factor = 1.8
        elif text_word_count < 200:
            factor = 1.5
        else:
            factor = 1.2
        sim = min(int(sim * factor), 100)
        return min(max(sim, 0), 100)

    except Exception:
        return _string_containment_similarity(text, subject)


@functools.lru_cache(maxsize=2048)
def _extract_keywords_cached(text: str, max_keywords: int = 20) -> frozenset:
    """三跑提取关键词集合（v1.7.4 新增，独立于 summarize_adapter）

    summa + jieba + regex fallback，取关键词数量最多者获胜。
    用于 _jaccard_similarity() 计算语义相似度。

    v1.0.0 增强：新增第 4 跑「零依赖共识兜底」——仅当 summa/jieba/regex
    全部无结果时启用（零依赖分词为最终兜底，不参与与外部分词竞争）。

    返回: set of 关键词字符串（小写）
    """
    candidates = []

    # 1. summa 路径（英文友好）
    if _dep_reg().is_available("summa"):
        try:
            from summa.keywords import keywords as summa_keywords
            kw_text = summa_keywords(text, words=max_keywords)
            kw_set = set(
                k.strip().lower()
                for k in kw_text.split('\n')
                if k.strip() and len(k.strip()) >= 2
            )
            if kw_set:
                candidates.append(("summa", kw_set))
        except Exception:
            pass

    # 2. jieba 路径（中文友好）
    # 2026-09-29：探测/初始化统一经 jieba_bridge（原裸 import 每次调用）
    import sys as _sys
    import os as _os
    _core = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'core')
    if _core not in _sys.path:
        _sys.path.insert(0, _core)
    try:
        import jieba_bridge as _jb
        kw_set = {k for k in _jb.textrank(text, max_keywords) if len(k) >= 2}
        if kw_set:
            candidates.append(("jieba", kw_set))
    except Exception:
        pass

    # 3. regex fallback（零依赖，纯英文）
    try:
        kw_set = _regex_extract_keywords_en(text, top_n=max_keywords)
        if kw_set:
            candidates.append(("regex", kw_set))
    except Exception:
        pass

    # 4. 零依赖共识兜底（v1.0.0，最终防线，纯标准库，中英文皆可）
    if not candidates:
        try:
            from infoseek_zerodep_nlp import extract_keywords as zd_extract_keywords
            kw_set = set(
                w.lower()
                for w, _ in zd_extract_keywords(text, max_kw=max_keywords)
                if w.strip() and len(w.strip()) >= 2
            )
            if kw_set:
                candidates.append(("zerodep", kw_set))
        except Exception:
            pass

    if not candidates:
        return frozenset()

    # 取关键词数量最多的获胜
    chosen = max(candidates, key=lambda x: len(x[1]))
    return frozenset(chosen[1])


def _extract_keywords_three_run(text: str, max_keywords: int = 20) -> set:
    """三跑提取关键词集合（对外接口，v1.7.4 新增 / v1.8.2 P1 加 LRU 缓存）

    底层走 _extract_keywords_cached（LRU 缓存，返回 frozenset），本函数 copy
    为可变 set 返回 → 调用方可安全 mutate 而不污染缓存。签名与返回类型同
    缓存前完全一致（_jaccard_similarity / test_v174_jaccard 等调用方零改动）。

    返回: set of 关键词字符串（小写）
    """
    return set(_extract_keywords_cached(text, max_keywords))


def _regex_extract_keywords_en(text: str, top_n: int = 20) -> set:
    """纯正则+词频英文关键词提取（v1.7.4 独立版本）

    与 summarize_adapter._regex_summarize() 类似但只返回 set。
    用于 _extract_keywords_three_run() 的 fallback 路径。
    """
    import re as re_mod
    from collections import Counter

    # 1. token 提取
    tokens = re_mod.findall(r'[a-zA-Z][a-zA-Z0-9]{2,}', text)
    tokens_lower = [t.lower() for t in tokens]

    # 2. 停用词过滤
    stop_words = set([
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
        'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who',
        'boy', 'did', 'use', 'than', 'this', 'that', 'with', 'from',
        'have', 'will', 'they', 'been', 'more', 'what', 'when', 'make', 'like',
        'over', 'such', 'also', 'into', 'then', 'them', 'very', 'just',
        'about', 'where', 'would', 'there', 'their', 'these', 'which', 'should'
    ])

    filtered = [t for t in tokens_lower if t not in stop_words and len(t) >= 3]
    counter = Counter(filtered)
    # 只返回 set，不做摘要
    top_keywords = set(w for w, _ in counter.most_common(top_n))
    return top_keywords


# v1.7.4 向后兼容 alias
def _tfidf_similarity(text: str, subject: str) -> int:
    """v1.7.4 alias: 保留向后兼容，重定向到 _jaccard_similarity

    v1.7.3 退化的 TF-IDF 公式已废弃。函数名保留以便调用方代码无须修改。
    推荐使用 _jaccard_similarity() 或 method="jaccard"。
    """
    return _jaccard_similarity(text, subject)


def _compute_domain_bonus(source: dict, profile: dict, prefer_kb: bool = False) -> int:
    """计算领域 profile 的信任源加权（v1.8.1；v1.7.2 加 prefer_kb 分段）

    参数:
        source: 源 dict（含 url/platform，可带 _kb_domain/_kb_hit_count）
        profile: 领域 profile dict（含 raw YAML 文本）
        prefer_kb: 多域交集场景（detect_domain 产出），对带 KB 域标记的源加分

    返回:
        0-20 分的加分
    """
    if not profile:
        return 0

    # v1.7.2 单源委托（消除三份漂移）：信任源加权 + prefer_kb 分段
    try:
        from domain_router import trust_source_bonus, kb_intersect_bonus, domain_bonus_cap
    except ImportError:
        return 0  # 单源不可用 → 不加分（不再重复实现）
    bonus = trust_source_bonus(source, profile)
    if prefer_kb:
        bonus += kb_intersect_bonus(source, profile)
    # v1.8.3 §8.4：cap 委托 domain_router.domain_bonus_cap()（与 anchor_score_v2 同源）
    return min(bonus, domain_bonus_cap())


def _extract_concepts(text: str, top_k: int = 20) -> set:
    """v1.7.2 新增：提取文本的概念集（关键词）

    策略：jieba 关键词（中文友好）+ 英文 token（summa 词频）
    """
    import re as re_mod
    concepts = set()

    # 1. jieba 关键词（中文）
    # 2026-09-29：经 jieba_bridge 探测（原裸 import）
    import sys as _sys
    import os as _os
    _core = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'core')
    if _core not in _sys.path:
        _sys.path.insert(0, _core)
    try:
        import jieba_bridge as _jb
        for kw in _jb.textrank(text, top_k):
            if len(kw) >= 2:
                concepts.add(kw)
    except Exception:
        pass

    # 2. 英文 token（≥3 字符）
    for t in re_mod.findall(r'[a-zA-Z][a-zA-Z0-9]{2,}', text):
        concepts.add(t.lower())

    # 3. 中文 2-4 字组合（补充 jieba 未覆盖）
    for segment in re_mod.findall(r'[\u4e00-\u9fff]{2,4}', text):
        concepts.add(segment)

    return concepts


# v2.0.2 shim: 旧 calculate_score() → 新 v2 计算（带 DeprecationWarning）
def _deprecation_warning_v202():
    warnings.warn(
        "anchor_adapter.calculate_score() is deprecated since v2.0.2; "
        "use core.anchor_score_v2.compute_final_score_v2() instead.",
        DeprecationWarning,
        stacklevel=3,
    )


# v2.0.2 重构：calculate_score() 内部转调 v2（保持 v1 行为兼容）
def calculate_score(
    source: dict,
    subject: str = "",
    with_llm_readability: bool = False,
    days_since_published: int = 0,
    with_cross_platform: bool = False,
    platforms: int = 1,
    with_semantic: bool = False,
    semantic_text: str = None,
    with_domain: bool = False,
    domain_profile: dict = None,
    prefer_kb: bool = None,
) -> dict:
    """v1 calculate_score() — v2.0.2 起标记 DEPRECATED

    内部转调 core/anchor_score_v2.compute_final_score_v2()。
    旧调用方代码无须修改（行为兼容）。
    """
    _deprecation_warning_v202()

    # v2.0.2: 转调纯函数 v2 评分
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))
        from anchor_score_v2 import compute_final_score_v2
        return compute_final_score_v2(
            source, subject,
            with_llm_readability=with_llm_readability,
            with_cross_platform=with_cross_platform,
            platforms=platforms,
            with_semantic=with_semantic,
            semantic_text=semantic_text,
            days_since_published=days_since_published,
            with_domain=with_domain,
            domain_profile=domain_profile,
            prefer_kb=bool(prefer_kb),
        )
    except ImportError:
        # fallback：返回基础评分（不修改 source）
        return {
            'raw_score': source.get('score', 50),
            'after_whitelist': source.get('score', 50),
            'classification': '🟡潜力',
            'version': '2.0.2-fallback',
        }


def cross_subject_analysis(subjects: List[str], archives_dir: str = None,
                          with_concept_overlap: bool = True) -> dict:
    """
    跨主题关联分析 (v1.6.0 第 7 工具，v1.7.2 升级)

    v1.7.2 新增:
      - 概念级共享（jieba 关键词 jaccard）
      - 共享关键词列表（不只 URL）

    输入: 多个调研主题
    输出: 共享源/共同作者/共有概念等关联信息
    """
    if archives_dir is None:
        archives_dir = str(get_archives_dir())

    archives_path = Path(archives_dir)
    if not archives_path.exists():
        return {"error": f"归档目录不存在: {archives_dir}"}

    # 收集每个主题的元数据
    subject_data = {}
    for subject in subjects:
        subject_dir = archives_path / subject
        if not subject_dir.exists():
            subject_data[subject] = {"exists": False, "files": [],
                                     "shared_sources": set(), "concepts": set()}
            continue

        files = list(subject_dir.glob('*.md')) + list(subject_dir.glob('*.json'))
        # 提取共享源（去重 URL）
        shared_sources = set()
        # v1.7.2: 提取概念集
        all_text = ""
        for f in files:
            content = f.read_text(encoding='utf-8', errors='ignore')
            all_text += content + "\n"
            import re
            urls = re.findall(r'https?://[^\s\)]+', content)
            for url in urls:
                # 标准化（去除尾部斜杠）
                shared_sources.add(url.rstrip('/'))

        # v1.7.2: 概念集（关键词）
        concepts = _extract_concepts(all_text) if with_concept_overlap else set()

        subject_data[subject] = {
            "exists": True,
            "files": [f.name for f in files],
            "file_count": len(files),
            "shared_sources": shared_sources,
            "concepts": concepts
        }

    # 计算两两共享
    correlation_matrix = {}
    for i, s1 in enumerate(subjects):
        correlation_matrix[s1] = {}
        for s2 in subjects:
            if s1 == s2:
                correlation_matrix[s1][s2] = {
                    "shared_sources": 0,
                    "shared_urls": [],
                    "shared_concepts": [],
                    "concept_jaccard": 0
                }
            else:
                # 防御：主题不存在时 shared_sources 缺失
                sources2 = subject_data.get(s2, {}).get("shared_sources", set())
                sources1 = subject_data.get(s1, {}).get("shared_sources", set())
                shared_url = sources1 & sources2

                # v1.7.2: 概念级共享
                concepts1 = subject_data.get(s1, {}).get("concepts", set())
                concepts2 = subject_data.get(s2, {}).get("concepts", set())
                shared_concepts = concepts1 & concepts2
                concept_jaccard = (
                    len(shared_concepts) / len(concepts1 | concepts2)
                    if (concepts1 | concepts2) else 0
                )

                correlation_matrix[s1][s2] = {
                    "shared_sources": len(shared_url),
                    "shared_urls": list(shared_url)[:5],
                    "shared_concepts": list(shared_concepts)[:10],  # 最多 10 个
                    "concept_jaccard": round(concept_jaccard, 3)
                }

    return {
        "subjects": subjects,
        "subject_data": {k: {"file_count": v.get("file_count", 0),
                              "files": v.get("files", []),
                              "concept_count": len(v.get("concepts", set()))}
                          for k, v in subject_data.items()},
        "correlation_matrix": correlation_matrix,
        "insights": _generate_cross_subject_insights_v172(subject_data, correlation_matrix)
    }


def _generate_cross_subject_insights_v172(subject_data: dict, correlation_matrix: dict) -> List[str]:
    """v1.7.2 跨主题洞察生成（含概念级）"""
    insights = []

    # 找共享源最多的主题对
    pairs = []
    subjects = list(subject_data.keys())
    for i, s1 in enumerate(subjects):
        for s2 in subjects[i+1:]:
            shared = correlation_matrix[s1][s2]["shared_sources"]
            if shared > 0:
                pairs.append((s1, s2, shared))

    pairs.sort(key=lambda x: -x[2])

    if pairs:
        top = pairs[0]
        insights.append(
            f"主题 '{top[0]}' 与 '{top[1]}' 共享 {top[2]} 个来源，可能存在强关联"
        )

    # v1.7.2: 找概念级 jaccard 最高的（即使没有共享源）
    concept_pairs = []
    for i, s1 in enumerate(subjects):
        for s2 in subjects[i+1:]:
            jaccard = correlation_matrix[s1][s2].get("concept_jaccard", 0)
            if jaccard > 0.05:  # >5% 概念重叠
                shared_kw = correlation_matrix[s1][s2].get("shared_concepts", [])
                concept_pairs.append((s1, s2, jaccard, shared_kw))

    concept_pairs.sort(key=lambda x: -x[2])

    if concept_pairs:
        top = concept_pairs[0]
        kw_sample = top[3][:5] if top[3] else []
        insights.append(
            f"概念级关联: '{top[0]}' 与 '{top[1]}' 共享概念 jaccard={top[2]:.2f}（{kw_sample}）"
        )

    # 找文件数最少的主题（可能数据不完整）
    file_counts = [(s, subject_data[s]["file_count"]) for s in subjects if subject_data[s]["exists"]]
    if file_counts:
        min_subject = min(file_counts, key=lambda x: x[1])
        if min_subject[1] < 3:
            insights.append(
                f"主题 '{min_subject[0]}' 仅有 {min_subject[1]} 个文件，建议补充调研"
            )

    return insights
