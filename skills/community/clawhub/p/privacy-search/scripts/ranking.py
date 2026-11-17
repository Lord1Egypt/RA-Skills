"""
去重与排序（F1-5 / F1-6）
=========================
V1.2 新增

问题背景：
    1. V1.1 的 compute_simhash 将各 n-gram 的 MD5 直接异或合并，
       这不是 SimHash——异或缺少加权投票，两段仅个别词不同的文本
       可能得到差异极大的指纹，去重召回不稳定。
    2. n-gram 按字符切分，对中文短标题不友好；requirements 中已声明
       jieba 依赖却从未被引用。
    3. 汉明距离阈值硬编码为 3，无法按场景调整。
    4. 排序公式为 engine_count * 10 - best_rank，粒度过粗：
       单引擎排名第 1 的优质结果会低于两个引擎排名第 10 的结果，
       且未考虑查询相关度与站点质量。

解决方案：
    - 实现标准 SimHash（按位加权投票），阈值可配。
    - 中文使用 jieba 分词特征，英文使用词 + 字符 n-gram，jieba 缺失时自动降级。
    - 排序改为多因子加权：共识度 + 位次 + 相关度 + 权威度 + 域名质量。
"""

import hashlib
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

sys.dont_write_bytecode = True

try:
    from engines_registry import get_authority
except ImportError:
    from .engines_registry import get_authority

# jieba 为可选依赖，采用懒加载：
#   直接 import 会在模块加载时构建前缀词典（实测约 0.8 秒），
#   而多数搜索请求并不需要中文分词，故延迟到首次使用时再加载，
#   避免拖慢 CLI 启动（死规则 10：不影响用户设备日常使用）。
_jieba_mod = None
_jieba_state = None  # None 未尝试 / True 可用 / False 不可用


def _load_jieba():
    """
    首次需要时才导入 jieba，失败则永久降级

    同时关闭 jieba 的词典构建日志，避免污染 CLI 输出
    （默认会向 stderr 打印 "Building prefix dict..." 等信息）。
    """
    global _jieba_mod, _jieba_state
    if _jieba_state is not None:
        return _jieba_mod
    try:
        import logging
        import jieba as _j
        # 静默词典加载日志，保持命令行输出整洁
        _j.setLogLevel(logging.ERROR)
        _jieba_mod = _j
        _jieba_state = True
    except Exception:  # noqa: BLE001 - 任何导入异常都应降级而非中断
        _jieba_mod = None
        _jieba_state = False
    return _jieba_mod


# ============================================================
# 文本特征提取
# ============================================================

_CJK_PATTERN = re.compile(r"[\u4e00-\u9fff]")
_WORD_PATTERN = re.compile(r"[a-z0-9]+")


def has_cjk(text: str) -> bool:
    """判断文本是否含中日韩字符"""
    return bool(_CJK_PATTERN.search(text))


def extract_features(text: str, max_len: int = 256) -> List[str]:
    """
    提取文本特征词

    中文：优先 jieba 分词（过滤单字，保留信息量较高的词）
    英文：按单词切分
    兜底：字符 3-gram

    Args:
        text: 原始文本
        max_len: 参与计算的最大字符数

    Returns:
        特征词列表
    """
    text = (text or "").strip().lower()[:max_len]
    if not text:
        return []

    features: List[str] = []

    if has_cjk(text):
        jb = _load_jieba()
        if jb is not None:
            # 中文分词，单字信息量低予以过滤
            features = [w for w in jb.cut(text) if len(w.strip()) > 1]
        if len(features) < 3:
            # jieba 不可用或分词过少时，用字符 2-gram 保证指纹稳定
            features += [text[i:i + 2] for i in range(len(text) - 1)]
    else:
        features = _WORD_PATTERN.findall(text)

    if len(features) < 3:
        # 最终兜底：字符 3-gram
        features = [text[i:i + 3] for i in range(max(0, len(text) - 2))]

    return [f for f in features if f.strip()]


# ============================================================
# SimHash（F1-5）
# ============================================================

SIMHASH_BITS = 64


def compute_simhash(text: str, bits: int = SIMHASH_BITS) -> int:
    """
    计算标准 SimHash 指纹

    算法：
        1. 提取特征词并统计词频作为权重
        2. 每个特征取 MD5 作为哈希
        3. 按位投票：位为 1 则加权重，为 0 则减权重
        4. 投票结果大于 0 的位置 1

    与 V1.1 的异或合并相比，加权投票使得少量词变化只影响少数比特，
    汉明距离才能真实反映文本相似度。

    Args:
        text: 待计算文本
        bits: 指纹位数

    Returns:
        指纹整数
    """
    features = extract_features(text)
    if not features:
        return 0

    # 词频作为权重
    weights: Dict[str, int] = defaultdict(int)
    for f in features:
        weights[f] += 1

    vector = [0] * bits
    for feature, weight in weights.items():
        h = int(hashlib.md5(feature.encode("utf-8")).hexdigest(), 16)
        for i in range(bits):
            if (h >> i) & 1:
                vector[i] += weight
            else:
                vector[i] -= weight

    fingerprint = 0
    for i in range(bits):
        if vector[i] > 0:
            fingerprint |= (1 << i)
    return fingerprint


def hamming_distance(a: int, b: int) -> int:
    """计算两个指纹的汉明距离"""
    return bin(a ^ b).count("1")


def similarity(a: int, b: int, bits: int = SIMHASH_BITS) -> float:
    """由汉明距离换算相似度（0~1）"""
    return 1.0 - hamming_distance(a, b) / bits


# ============================================================
# 去重
# ============================================================

def normalize_url(url: str) -> str:
    """
    URL 归一化

    去除协议差异、www 前缀、追踪参数与尾部斜杠，
    使同一页面的不同写法能够正确合并。
    """
    if not url:
        return ""
    try:
        parsed = urlparse(url if "://" in url else f"http://{url}")
    except ValueError:
        return url.strip().lower()

    host = (parsed.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]

    path = (parsed.path or "/").rstrip("/") or "/"
    return f"{host}{path}"


def _is_redirect(url: str) -> bool:
    """
    判断是否为搜索引擎跳转中转地址

    engine_selectors 不可用时降级为不判定，
    此时跳转链接按普通 URL 处理，仅影响去重召回，不影响可用性。
    """
    if not url:
        return False
    try:
        from engine_selectors import is_redirect_url
    except ImportError:
        try:
            from .engine_selectors import is_redirect_url
        except ImportError:
            return False
    return is_redirect_url(url)


# 各引擎会给标题追加站点后缀或截断标记，归并前需剥离
_TITLE_TAIL = re.compile(
    r"(\s*[-_|—–]\s*[^-_|—–]{0,20}(网|站|社区|博客|知乎|简书|掘金|csdn|blog|com|cn)\s*)?"
    r"[.．。]{2,}\s*$"
)
# 仅保留中日韩、字母与数字，其余（含全半角标点）一律视为噪声
_TITLE_NOISE = re.compile(r"[^\u4e00-\u9fff\u3040-\u30ffa-z0-9]+")


def _title_key(item: Any) -> str:
    """
    标题归一化，作为跳转链接的归并键

    同一页面在不同引擎的标题常有细微差异：
    全角与半角标点混用、追加站点名后缀、超长时以省略号截断。
    仅做大小写与空白归一无法匹配，故一并剥离标点与噪声字符。
    """
    title = getattr(item, "title", "") or ""
    if not isinstance(title, str):
        return ""
    text = _TITLE_TAIL.sub("", title.strip().lower())
    return _TITLE_NOISE.sub("", text)


# 前缀匹配的最短长度：过短的公共前缀会把不同文章误判为同一篇
_TITLE_PREFIX_MIN = 12


def _match_direct_title(key: str, index: Dict[str, str]) -> str:
    """
    为跳转链接找到对应的直链分组

    先精确匹配；未命中时按前缀匹配，用于处理引擎把长标题截断的情况
    （如「A的原理、优化与实践」与「A的原理、优化与实践_算法详解」）。
    前缀长度不足 12 个字符时不做模糊匹配，避免「Python 教程」这类
    通用短标题把不同文章错误合并。

    Returns:
        命中的归并键，未命中返回空串
    """
    if not key:
        return ""
    hit = index.get(key)
    if hit:
        return hit
    if len(key) < _TITLE_PREFIX_MIN:
        return ""
    # 取最长匹配前缀，降低歧义
    best = ""
    best_len = 0
    for known, mapped in index.items():
        if len(known) < _TITLE_PREFIX_MIN:
            continue
        if key.startswith(known) or known.startswith(key):
            common = min(len(known), len(key))
            if common > best_len:
                best, best_len = mapped, common
    return best


def _prefer(candidate: Any, current: Any, url_getter, snippet_len_getter) -> bool:
    """
    判断合并同组结果时是否应改用 candidate 作为代表

    判据优先级：
        1. 直链优于跳转中转地址——跳转地址对用户不可读，
           且点击会经由搜索引擎记录一次访问，与隐私目标相悖
        2. 摘要更完整者优先

    Returns:
        True 表示应改用 candidate
    """
    cand_redirect = _is_redirect(url_getter(candidate))
    cur_redirect = _is_redirect(url_getter(current))
    if cand_redirect != cur_redirect:
        return cur_redirect      # 当前是跳转链接才替换
    return snippet_len_getter(candidate) > snippet_len_getter(current)


def _engines_of(item: Any) -> List[str]:
    """
    读取条目已知的引擎来源

    合并过的条目携带 engines 列表，未合并的退化为 engine 单值。
    """
    merged = getattr(item, "engines", None)
    if merged:
        return list(merged)
    single = getattr(item, "engine", "")
    return [single] if single else []


def _merge_into(winner: Any, loser: Any) -> None:
    """
    把被去重条目的信息并入保留条目

    去重会丢弃重复条目，但其携带的两项信息对排序至关重要：
        1. 引擎来源——共识度因子依赖「被几个引擎收录」
        2. 原始位次——同一页面在不同引擎的排名可能相差很大
    若不合并，排序阶段按 URL 分组时每组只剩一条，
    共识度恒为最小值，多引擎交叉验证形同虚设。
    """
    try:
        merged = list(dict.fromkeys(_engines_of(winner) + _engines_of(loser)))
        setattr(winner, "engines", merged)
    except AttributeError:
        # 不支持写属性的条目（如具名元组）跳过合并，不影响去重本身
        return

    # 位次取各引擎中的最优值，0 表示未知不参与比较
    try:
        w_rank = getattr(winner, "rank", 0) or 0
        l_rank = getattr(loser, "rank", 0) or 0
        candidates = [r for r in (w_rank, l_rank) if r > 0]
        if candidates:
            setattr(winner, "rank", min(candidates))
    except AttributeError:
        pass


def deduplicate(
    items: Sequence[Any],
    threshold: int = 3,
    text_getter=None,
    url_getter=None,
    snippet_len_getter=None,
) -> List[Any]:
    """
    近似去重

    先按归一化 URL 精确去重，再用 SimHash 消除不同 URL 的重复内容。
    同组结果保留摘要最完整的一条，并把被丢弃条目的引擎来源与
    最优位次合并进保留条目，供后续排序计算共识度。

    Args:
        items: 待去重条目
        threshold: 汉明距离阈值，小于等于该值视为重复
        text_getter: 取文本的函数，默认取 title + snippet
        url_getter: 取 URL 的函数
        snippet_len_getter: 取摘要长度的函数，用于挑选代表条目

    Returns:
        去重后的条目列表（保持输入顺序）
    """
    if not items:
        return []

    text_getter = text_getter or (lambda x: f"{getattr(x, 'title', '')} {getattr(x, 'snippet', '')}")
    url_getter = url_getter or (lambda x: getattr(x, "url", ""))
    snippet_len_getter = snippet_len_getter or (lambda x: len(getattr(x, "snippet", "") or ""))

    # 跳转中转地址（如 baidu.com/link?url=...）的真实目标无法从 URL 还原，
    # 与其他引擎给出的直链会被当作两个页面，导致同一结果重复占位。
    # 先扫描所有直链，建立「标题 -> 归一化 URL」索引，
    # 随后让同标题的跳转链接并入直链分组。
    # 预扫描而非边遍历边建索引，是为了不受结果先后顺序影响。
    direct_by_title: Dict[str, str] = {}
    for item in items:
        raw = url_getter(item)
        if _is_redirect(raw):
            continue
        t = _title_key(item)
        norm = normalize_url(raw)
        if t and norm:
            direct_by_title.setdefault(t, norm)

    # 第一轮：URL 归一化精确去重
    by_url: Dict[str, Any] = {}
    order: List[str] = []

    for item in items:
        raw_url = url_getter(item)
        if _is_redirect(raw_url):
            t = _title_key(item)
            # 有同标题直链则并入，否则同标题的跳转链接之间也相互合并
            key = _match_direct_title(t, direct_by_title) or (f"__title__{t}" if t else "")
        else:
            key = normalize_url(raw_url)
        if not key:
            key = f"__no_url__{len(order)}"

        if key not in by_url:
            by_url[key] = item
            order.append(key)
        else:
            current = by_url[key]
            if _prefer(item, current, url_getter, snippet_len_getter):
                _merge_into(item, current)
                by_url[key] = item
            else:
                _merge_into(current, item)

    stage1 = [by_url[k] for k in order]

    # 第二轮：SimHash 近似去重
    kept: List[Tuple[int, Any]] = []
    result: List[Any] = []
    for item in stage1:
        fp = compute_simhash(text_getter(item))
        duplicated = False
        for idx, (kept_fp, kept_item) in enumerate(kept):
            if hamming_distance(fp, kept_fp) <= threshold:
                duplicated = True
                if _prefer(item, kept_item, url_getter, snippet_len_getter):
                    _merge_into(item, kept_item)
                    pos = result.index(kept_item)
                    result[pos] = item
                    kept[idx] = (kept_fp, item)
                else:
                    _merge_into(kept_item, item)
                break
        if not duplicated:
            kept.append((fp, item))
            result.append(item)

    return result


# ============================================================
# 排序（F1-6）
# ============================================================

@dataclass
class RankWeights:
    """
    排序权重配置

    各因子含义：
        consensus  多引擎共识度，被越多引擎收录越可信
        position   引擎内原始位次
        relevance  查询词与标题摘要的匹配程度
        authority  引擎权威度（来自 engines_registry）
        domain     域名质量（可信站点加分、低质站点降权）
    """
    consensus: float = 6.0
    position: float = 3.0
    relevance: float = 4.0
    authority: float = 2.0
    domain: float = 1.5


def weights_from_config(config: Optional[Dict[str, Any]] = None) -> RankWeights:
    """
    依据配置构造排序权重

    配置示例：
        ranking:
          consensus: 6.0
          position: 3.0
          relevance: 4.0
          authority: 2.0
          domain: 1.5

    任一项缺失或非法时回落到该项默认值，保证配置写错不影响搜索可用性。
    """
    cfg = (config or {}).get("ranking", {}) or {}
    base = RankWeights()
    values = {}
    for field_name in ("consensus", "position", "relevance", "authority", "domain"):
        raw = cfg.get(field_name, None)
        if raw is None:
            values[field_name] = getattr(base, field_name)
            continue
        try:
            parsed = float(raw)
        except (TypeError, ValueError):
            values[field_name] = getattr(base, field_name)
            continue
        # 负权重会颠倒排序语义，按非法处理
        values[field_name] = parsed if parsed >= 0 else getattr(base, field_name)
    return RankWeights(**values)


# 低质量内容站点，命中则降权
LOW_QUALITY_DOMAINS = {
    # 百度系低质内容农场
    "baijiahao.baidu.com", "zhidao.baidu.com", "wenku.baidu.com",
    # 文档分享站（多为爬取内容）
    "docin.com", "doc88.com", "book118.com", "renrendoc.com",
    "csdn.net",  # 内容重复度较高，适度降权而非屏蔽
    # 采集站/SEO 站
    "www.toutiao.com", "www.360doc.com", "www.docin.com",
    "www.doc88.com", "www.book118.com", "www.renrendoc.com",
    "www.90so.net", "www.51wendang.com", "www.csdn.net",
    "www.pianshen.com", "www.fenxiangdashi.com",
}

# 优质站点，命中则加权
HIGH_QUALITY_DOMAINS = {
    # 国际技术社区
    "github.com", "stackoverflow.com", "wikipedia.org", "zhihu.com",
    "developer.mozilla.org", "docs.python.org", "arxiv.org",
    "gitee.com", "juejin.cn", "segmentfault.com",
    # 中文技术社区
    "www.cnblogs.com", "www.cnblogs.cn", "blog.csdn.net",
    "www.jianshu.com", "juejin.cn", "segmentfault.com",
    "www.oschina.net", "www.51cto.com", "www.infoq.cn",
    # 百科/知识
    "baike.baidu.com", "www.baike.com", "wiki.mbalib.com",
    # 官方文档
    "docs.oracle.com", "docs.microsoft.com", "learn.microsoft.com",
    "developers.google.com", "developer.apple.com",
    "kubernetes.io", "docker.com", "docs.docker.com",
    "www.elastic.co", "redis.io", "mongodb.com",
    "www.postgresql.org", "www.mysql.com",
    # 学术
    "scholar.google.com", "www.ncbi.nlm.nih.gov",
    "semanticscholar.org", "arxiv.org",
    # 主流媒体
    "www.people.com.cn", "www.xinhuanet.com", "www.chinanews.com.cn",
}


def domain_of(url: str) -> str:
    """提取主机名（去 www）"""
    try:
        host = urlparse(url if "://" in url else f"http://{url}").netloc.lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def domain_score(url: str) -> float:
    """
    域名质量评分

    跳转中转地址无法反映真实站点质量，且不利于跨引擎去重，
    统一给予轻微降权。

    Returns:
        1.0 优质 / 0.0 普通 / -0.5 跳转链接 / -1.0 低质
    """
    if not url:
        return 0.0

    try:
        from engine_selectors import is_redirect_url
    except ImportError:
        try:
            from .engine_selectors import is_redirect_url
        except ImportError:
            is_redirect_url = lambda _u: False  # noqa: E731 - 降级为不判定

    if is_redirect_url(url):
        return -0.5

    host = domain_of(url)
    if not host:
        return 0.0
    for good in HIGH_QUALITY_DOMAINS:
        if host == good or host.endswith("." + good):
            return 1.0
    for bad in LOW_QUALITY_DOMAINS:
        if host == bad or host.endswith("." + bad):
            return -1.0
    return 0.0


def _relevance_simple(query: str, title: str, snippet: str) -> float:
    """
    词项覆盖率相关度（轻量模式）

    采用轻量词项覆盖率而非完整 BM25：
    搜索结果摘要长度相近，文档长度归一化收益有限，
    覆盖率计算成本更低且效果稳定。

    标题命中权重高于摘要。
    """
    terms = [t for t in extract_features(query, max_len=64) if len(t) > 1]
    if not terms:
        return 0.0

    title_l = (title or "").lower()
    snippet_l = (snippet or "").lower()

    hit = 0.0
    for term in set(terms):
        in_title = term in title_l
        in_snippet = term in snippet_l
        if in_title:
            hit += 1.0
        elif in_snippet:
            hit += 0.5

    return min(1.0, hit / len(set(terms)))


def _relevance_tfidf(query: str, title: str, snippet: str) -> float:
    """
    TF-IDF 余弦相似度（精准模式）

    使用 jieba 分词将查询和文档转为词频向量，
    计算余弦相似度。对中文短文本，分词后的向量
    比词项覆盖率更能捕捉语义关联。

    jieba 不可用时返回 None，由调用方降级为 simple。
    """
    jb = _load_jieba()
    if jb is None:
        return None

    query_terms = [w for w in jb.cut((query or "").strip().lower()) if len(w.strip()) > 1]
    title_terms = [w for w in jb.cut((title or "").strip().lower()) if len(w.strip()) > 1]
    snippet_terms = [w for w in jb.cut((snippet or "").strip().lower()) if len(w.strip()) > 1]

    if not query_terms:
        return 0.0

    # 文档向量：标题词权重 2.0，摘要词权重 1.0
    doc_terms: Dict[str, int] = defaultdict(int)
    for w in title_terms:
        doc_terms[w] += 2
    for w in snippet_terms:
        doc_terms[w] += 1

    if not doc_terms:
        return 0.0

    # 计算点积和模长
    dot_product = 0.0
    query_norm = 0.0
    doc_norm = 0.0

    query_counts: Dict[str, int] = defaultdict(int)
    for w in query_terms:
        query_counts[w] += 1

    for w, qc in query_counts.items():
        query_norm += qc * qc
        dot_product += qc * doc_terms.get(w, 0)

    for w, dc in doc_terms.items():
        doc_norm += dc * dc

    if query_norm == 0.0 or doc_norm == 0.0:
        return 0.0

    return dot_product / (math.sqrt(query_norm) * math.sqrt(doc_norm))


def relevance_score(query: str, title: str, snippet: str) -> float:
    """
    查询相关度评分（0~1）

    主模式：jieba 分词 + TF-IDF 余弦相似度（中文准确度高）
    降级模式：jieba 不可用时回退到词项覆盖率（仍可用）
    """
    # 含中文时优先 TF-IDF
    if has_cjk(query) or has_cjk(title) or has_cjk(snippet):
        tfidf = _relevance_tfidf(query, title, snippet)
        if tfidf is not None:
            return min(1.0, max(0.0, tfidf))

    # 英文或无 jieba 时用轻量模式
    return _relevance_simple(query, title, snippet)


def rank_results(
    items: Sequence[Any],
    query: str = "",
    weights: Optional[RankWeights] = None,
    max_rank: int = 10,
    total_engines: Optional[int] = None,
) -> List[Any]:
    """
    多因子加权排序

    评分公式：
        score = consensus_w * 共识度
              + position_w  * 位次得分
              + relevance_w * 相关度
              + authority_w * 引擎权威度
              + domain_w    * 域名质量

    Args:
        items: 已去重的结果条目
        query: 原始查询词，用于计算相关度
        weights: 权重配置
        max_rank: 位次归一化基准
        total_engines: 本次实际参与搜索的引擎总数，用于归一化共识度。
            为空时从结果中推断；推断值可能偏小（某引擎全部结果被去重
            合并后仍会被计入，但完全无结果的引擎无法体现），
            调用方已知准确值时应显式传入。

    Returns:
        按得分降序排列的结果
    """
    if not items:
        return []

    w = weights or RankWeights()

    # 按归一化 URL 聚合，统计跨引擎共识
    groups: Dict[str, List[Any]] = defaultdict(list)
    for item in items:
        groups[normalize_url(getattr(item, "url", ""))].append(item)

    if total_engines and total_engines > 0:
        engine_total = total_engines
    else:
        # 去重已把引擎来源合并进保留条目，需展开统计而非只看 engine 单值
        seen_engines = set()
        for i in items:
            seen_engines.update(_engines_of(i))
        engine_total = len(seen_engines) or 1

    scored: List[Tuple[float, Any]] = []
    for _, group in groups.items():
        engines = set()
        for i in group:
            engines.update(_engines_of(i))
        best_rank = min((getattr(i, "rank", max_rank) or max_rank) for i in group)
        representative = max(group, key=lambda x: len(getattr(x, "snippet", "") or ""))

        # 共识度：被多少比例的引擎收录
        consensus = len(engines) / engine_total

        # 位次得分：排名越靠前越高，做对数衰减避免尾部差异被放大
        position = 1.0 / math.log2(max(1, best_rank) + 1)

        # 相关度
        relevance = relevance_score(
            query,
            getattr(representative, "title", ""),
            getattr(representative, "snippet", ""),
        )

        # 引擎权威度取组内最高
        authority = max(get_authority(e) for e in engines) if engines else 1.0
        authority_norm = (authority - 0.8) / 0.5  # 归一到约 0~1

        dom = domain_score(getattr(representative, "url", ""))

        score = (
            w.consensus * consensus
            + w.position * position
            + w.relevance * relevance
            + w.authority * authority_norm
            + w.domain * dom
        )

        # 记录得分便于调试与 JSON 输出
        try:
            setattr(representative, "score", round(score, 4))
        except AttributeError:
            pass

        scored.append((score, representative))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored]


def jieba_available() -> bool:
    """
    jieba 是否可用（供自检与文档提示）

    会触发一次懒加载，仅在自检场景调用。
    """
    return _load_jieba() is not None
