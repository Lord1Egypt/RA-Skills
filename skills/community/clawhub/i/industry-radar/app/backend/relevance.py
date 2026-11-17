"""
M4-b 相关性过滤：基于关键词的规则打分。

打分维度（0~100）：
  * 命中「行业词」个数
  * 命中「技术词」个数
  * 命中「扩展词」个数
  * 标题命中加权（标题权重更高）
  * 多词共现奖励、时效性小奖励
未命中任何关键词的文章将被过滤。
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Dict, List

_SPLIT = re.compile(r"[,\s，、;；/|]+")

# 日报/快讯类标题特征：内容为多条新闻拼盘，正文顺带提及关键词的
# 噪声很大，不应进入「编辑精选」榜单（对总分也做降权）。
_DIGEST_RE = re.compile(
    r"(早报|晚报|晨报|日报|快讯|热点导览|要闻汇总|新闻汇总|今日要闻|"
    r"盘点|一图看懂|\d+点\d+氪|News\s*Roundup)"
)


def is_digest(art: Dict) -> bool:
    """判断是否为日报/快讯/新闻拼盘类文章（按标题识别）。"""
    title = art.get("title", "") or ""
    return bool(_DIGEST_RE.search(title))


def parse_keywords(raw: str) -> List[str]:
    if not raw:
        return []
    return [k.strip() for k in _SPLIT.split(raw) if k.strip()]


def _count_hits(text: str, kws: List[str]) -> int:
    return sum(text.count(k) for k in kws) if kws else 0


def score_article(art: Dict, industry: List[str], tech: List[str], extra: List[str]) -> float:
    title = art.get("title", "") or ""
    body = art.get("content", "") or ""
    text = f"{title}\n{body}"
    if not industry and not tech and not extra:
        return 50.0

    t_ind = _count_hits(title, industry)
    t_tech = _count_hits(title, tech)
    b_ind = _count_hits(text, industry)
    b_tech = _count_hits(text, tech)
    b_ext = _count_hits(text, extra)

    score = 0.0
    score += min(t_ind, 2) * 18         # 标题命中行业词
    score += min(t_tech, 2) * 18        # 标题命中技术词
    score += min(b_ind, 4) * 6          # 正文命中行业词
    score += min(b_tech, 4) * 6         # 正文命中技术词
    score += min(b_ext, 3) * 3          # 扩展词

    # 行业 × 技术 共现奖励（核心信号）：要求实质性命中——标题命中，
    # 或正文命中 ≥2 次；长文里被顺带提及 1 次不构成共现信号。
    raw_b_ind = _count_hits(body, industry)
    raw_b_tech = _count_hits(body, tech)
    if (t_ind or raw_b_ind >= 2) and (t_tech or raw_b_tech >= 2):
        score += 15

    # 时效性：越新略有加分
    pub = art.get("published_at", "")
    if pub:
        try:
            dt = datetime.strptime(pub[:19], "%Y-%m-%d %H:%M:%S")
            if datetime.utcnow() - dt < timedelta(days=14):
                score += 5
        except Exception:  # noqa: BLE001
            pass

    # 行业信号门控：标题命中行业词 / 正文命中行业词 / 标题命中扩展词。
    # 扩展词多为品牌名（Meta、Rokid…），正文顺带提及不构成行业信号，
    # 否则「谈大模型顺带提一句 Meta」的软文会挤掉真正的行业文章。
    # 本产品是「行业 × 技术」交叉筛选：完全无行业信号、只命中技术词的
    # 文章减半并封顶 22 分——可作尾部补位，但不得占据精选榜头部。
    # 注意：须在时效加分之后执行，保证 22 为含时效的硬顶。
    t_ext = _count_hits(title, extra)
    if not (t_ind or raw_b_ind or t_ext):
        score = min(score * 0.5, 22.0)

    # 行业信号门控：标题命中行业词 / 正文命中行业词 / 标题命中扩展词。
    # 扩展词多为品牌名（Meta、Rokid…），正文顺带提及不构成行业信号，
    # 否则「谈大模型顺带提一句 Meta」的软文会挤掉真正的行业文章。
    # 本产品是「行业 × 技术」交叉筛选：完全无行业信号、只命中技术词的
    # 文章减半并封顶 22 分——可作尾部补位，但不得占据精选榜头部。
    # 注意：须在时效加分之后执行，保证 22 为含时效的硬顶。
    t_ext = _count_hits(title, extra)
    if not (t_ind or raw_b_ind or t_ext):
        score = min(score * 0.5, 22.0)

    # 日报/快讯拼盘降权：正文长且杂，关键词命中多为顺带提及
    if is_digest(art):
        score *= 0.5

    return round(min(score, 100.0), 2)


def matched_keywords(art: Dict, industry: List[str], tech: List[str],
                     extra: List[str]) -> List[str]:
    """返回该文章命中的关键词列表（按 行业 → 技术 → 扩展 顺序）。"""
    hits: Dict[str, int] = keyword_hits(art, industry, tech, extra)
    return list(hits.keys())


def keyword_hits(art: Dict, industry: List[str], tech: List[str],
                 extra: List[str]) -> Dict[str, int]:
    """统计每个关键词在文中的加权命中次数（标题权重 ×2），用于挑选「主关键词」。

    聚类阶段据此把文章归入「命中次数最多的那个关键词」对应的板块，
    既避免长文本 Jaccard 导致的碎片化，也避免「关键词集合求并」造成的传递式大合并。
    """
    title = art.get("title", "") or ""
    body = art.get("content", "") or ""
    hits: Dict[str, int] = {}
    for k in industry + tech + extra:
        if not k or k in hits:
            continue
        c = title.count(k) * 2 + body.count(k)
        if c:
            hits[k] = c
    return hits


def filter_relevant(articles: List[Dict], industry: List[str], tech: List[str],
                    extra: List[str], min_score: float = 6.0) -> List[Dict]:
    scored = []
    for art in articles:
        s = score_article(art, industry, tech, extra)
        if s >= min_score:
            art["score"] = s
            hits = keyword_hits(art, industry, tech, extra)
            art["keyword_hits"] = hits
            art["matched_keywords"] = list(hits.keys())
            scored.append(art)
    scored.sort(key=lambda a: a["score"], reverse=True)
    return scored