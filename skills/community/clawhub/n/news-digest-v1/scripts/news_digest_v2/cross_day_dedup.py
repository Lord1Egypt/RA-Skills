# -*- coding: utf-8 -*-
"""
跨天重复新闻检测模块

在 stage 2.5 候选文章筛选后、LLM 调用前使用。
对比 digest_output 历史摘要，拦截跨天重复新闻。

核心规则：
1. 标题 Jaccard(0.5) + 数字匹配(0.25) + 内容词重叠(0.25)
2. 硬规则：双方都有显著数字但不共享 → 直接判定为非重复（返回 0.0）
   这自动覆盖周期性新闻（每月 PMI、CPI 等数字不同 → 自动放行）
3. 三档判定：
   - ≥ 0.75：拦截
   - 0.60 ~ 0.75：警告保留
   - < 0.60：正常通过
"""
import re
import sqlite3
from datetime import datetime, timedelta

try:
    from .config import DB_PATH, CROSS_DAY_HISTORY_DAYS, CROSS_DAY_THRESHOLD, CROSS_DAY_WARN_THRESHOLD
except ImportError:
    from config import DB_PATH, CROSS_DAY_HISTORY_DAYS, CROSS_DAY_THRESHOLD, CROSS_DAY_WARN_THRESHOLD


def _clean_title(title):
    """清洗标题：去标点、空格化，便于比较"""
    if not title:
        return ''
    # 去各种括号、引号
    title = re.sub(r'[【】\[\]（）()""""''\u201c\u201d\u2018\u2019]', '', title)
    # 标点转空格
    title = re.sub(r'[\u00b7\u3001\uff0c\u3002\uff1a\uff1b\s\u2014]+', ' ', title)
    return title.strip().lower()


def _extract_significant_numbers(text):
    """
    提取显著数字（用于判断是否为同一数据报道）
    返回：≥3 位数字或带小数点的数字集合
    """
    if not text:
        return set()
    nums = re.findall(r'\d+\.?\d*', text)
    return {n for n in nums if len(n) >= 3 or '.' in n}


def _extract_content_words(text):
    """提取中文内容词（2 字以上连续汉字）"""
    if not text:
        return set()
    return set(re.findall(r'[\u4e00-\u9fa5]{2,}', text))


def _compute_cross_day_similarity(candidate, history_item):
    """
    计算候选文章与历史摘要的跨天相似度

    硬规则 1（标题完全匹配）：
        候选标题 == 历史标题（清洗后） → 直接返回 1.0（拦截）
    硬规则 2（标题嵌入历史摘要）：
        候选标题（去标点）出现在历史摘要中 → 直接返回 1.0（拦截）
    硬规则 3（数字差异化）：
        双方都有显著数字但不共享 → 直接返回 0.0（非重复，放行）
        自动覆盖周期性新闻：每月 PMI/CPI 数字不同 → 放行

    综合评分 = 0.5 * 标题Jaccard + 0.25 * 数字匹配 + 0.25 * 内容词重叠
    """
    c_title_raw = candidate.get('title', '') or ''
    h_title_raw = history_item.get('title', '') or ''
    c_summary = candidate.get('summary', '') or ''
    h_summary = history_item.get('summary', '') or ''

    c_title_clean = _clean_title(c_title_raw)
    h_title_clean = _clean_title(h_title_raw)

    # === 硬规则 1：标题完全一致 ===
    if c_title_clean and c_title_clean == h_title_clean:
        return 1.0

    # === 硬规则 2：候选标题嵌入历史摘要 ===
    c_title_bare = re.sub(r'[\s\u00b7\u3001\uff0c\u3002\uff1a\uff1b\u2014\u201c\u201d\u2018\u2019【】\[\]（）()"\u201c\u201d]', '', c_title_raw)
    if c_title_bare and len(c_title_bare) >= 8 and c_title_bare in h_summary:
        return 1.0

    # === 硬规则 4：标题互相包含（同事件不同来源报道）===
    # 例："今年前4月，我国服务出口同比增长15%" vs "前4月 我国服务出口同比增长15%"
    # 较短标题几乎完整地出现在较长标题中 → 同一数据/事件的不同来源报道
    if c_title_clean and h_title_clean and len(c_title_clean) >= 8 and len(h_title_clean) >= 8:
        shorter, longer = (c_title_clean, h_title_clean) if len(c_title_clean) <= len(h_title_clean) else (h_title_clean, c_title_clean)
        # 较短标题的 ≥80% 字符序列连续出现在较长标题中
        match_len = len(shorter) * 0.8
        # 简化检查：较短标题去掉1-2个词后是否被包含
        short_words = shorter.split()
        for skip_count in range(0, min(2, len(short_words))):
            for start in range(len(short_words) - skip_count):
                sub = ' '.join(short_words[start:start + len(short_words) - skip_count])
                if len(sub) >= match_len and sub in longer:
                    # 计算包含度作为相似度
                    containment_ratio = len(sub) / len(longer)
                    return min(1.0, 0.85 + containment_ratio * 0.15)  # 0.85~1.0 区间，直接拦截

    # === 硬规则 3：数字差异化判断 ===
    c_text = c_title_raw + ' ' + c_summary
    h_text = h_title_raw + ' ' + h_summary
    c_nums = _extract_significant_numbers(c_text)
    h_nums = _extract_significant_numbers(h_text)
    shared_nums = c_nums & h_nums

    # 双方都有显著数字但不共享 → 直接判为非重复
    if c_nums and h_nums and not shared_nums:
        return 0.0

    # === 标题 Jaccard 相似度 ===
    if not c_title_clean or not h_title_clean:
        return 0.0

    c_words = set(c_title_clean.split())
    h_words = set(h_title_clean.split())
    union = c_words | h_words
    intersection = c_words & h_words
    title_sim = len(intersection) / len(union) if union else 0.0

    # === 数字匹配度 ===
    num_sim = 0.0
    if shared_nums:
        num_sim = len(shared_nums) / min(len(c_nums), len(h_nums))

    # === 内容词重叠 ===
    c_words_content = _extract_content_words(c_summary)
    h_words_content = _extract_content_words(h_summary)
    kw_sim = 0.0
    if c_words_content and h_words_content:
        union_kw = c_words_content | h_words_content
        inter_kw = c_words_content & h_words_content
        kw_sim = len(inter_kw) / len(union_kw) if union_kw else 0.0

    # === 综合评分 ===
    # 调整权重：标题相似度权重提高到 0.6（此前 0.5），因为内容词在候选尚未 LLM 时往往为空
    # 标题 Jaccard ≥ 0.8 且无数字差异 → 基本可判定为同一事件
    if not c_nums and not h_nums:
        score = 0.6 * title_sim + 0.4 * kw_sim
        # 补充：标题 Jaccard ≥ 0.8 且一方是另一方的超集 → 提权
        if title_sim >= 0.8 and max(len(c_words), len(h_words)) - min(len(c_words), len(h_words)) <= 1:
            score = max(score, 0.80)  # 至少提到警告区
    else:
        score = 0.6 * title_sim + 0.25 * num_sim + 0.15 * kw_sim

    return min(1.0, score)


def get_history_digests(days=None):
    """
    从 digest_output 获取最近 N 天的摘要记录

    Args:
        days: 历史窗口天数，默认使用配置值

    Returns:
        list[dict]: 历史摘要列表
    """
    if days is None:
        days = CROSS_DAY_HISTORY_DAYS

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    c.execute('''
        SELECT id, title, source, summary, digest_date
        FROM digest_output
        WHERE digest_date >= ?
        ORDER BY digest_date DESC, id DESC
    ''', (date_from,))

    rows = c.fetchall()
    conn.close()

    return [
        {
            'id': r[0], 'title': r[1], 'source': r[2],
            'summary': r[3], 'digest_date': r[4]
        }
        for r in rows
    ]


def filter_cross_day_duplicates(candidates, history=None, verbose=True):
    """
    过滤候选文章中的跨天重复新闻

    Args:
        candidates: 待筛选候选文章 list[dict]，每项需含 title, summary, source
        history: 历史摘要列表，None 则自动从数据库加载
        verbose: 是否打印拦截日志

    Returns:
        tuple(filtered, blocked)
        - filtered: 通过筛选的文章（含警告区保留的）
        - blocked: 被拦截的文章及匹配原因
    """
    if history is None:
        history = get_history_digests()

    if not history:
        if verbose:
            print(f"  [跨天去重] 无历史摘要，跳过")
        return candidates, []

    if verbose:
        print(f"  [跨天去重] 加载历史摘要 {len(history)} 条（最近 {CROSS_DAY_HISTORY_DAYS} 天）")

    filtered = []
    blocked = []

    for c in candidates:
        max_sim = 0.0
        best_match = None

        for h in history:
            sim = _compute_cross_day_similarity(c, h)
            if sim > max_sim:
                max_sim = sim
                best_match = h

        if max_sim >= CROSS_DAY_THRESHOLD:
            # 拦截
            blocked.append({
                'article': c,
                'similarity': max_sim,
                'matched': best_match
            })
            if verbose:
                print(f"    \u26d4 [跨天拦截] {c['title'][:60]}")
                print(f"       匹配 {best_match['digest_date']} [{best_match['source']}] "
                      f"{best_match['title'][:50]} (相似度: {max_sim:.2f})")
        elif max_sim >= CROSS_DAY_WARN_THRESHOLD:
            # 警告区：保留，但打印日志
            filtered.append(c)
            if verbose:
                print(f"    \u26a0\ufe0f [跨天警告] {c['title'][:60]}")
                print(f"       疑似匹配 {best_match['digest_date']} [{best_match['source']}] "
                      f"{best_match['title'][:50]} (相似度: {max_sim:.2f}) \u2014 保留")
        else:
            filtered.append(c)

    return filtered, blocked
