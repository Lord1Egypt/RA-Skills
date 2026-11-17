#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级检索语法解析器（V1.8 新增）

功能：解析时间限定、站点限定、文件类型限定，映射为各引擎等价参数。
     与现有 bangs 语法统一为查询语法表。

支持的语法：
  after:2024    时间下限（仅保留该年份之后的内容）
  before:2025   时间上限
  site:example.com  站点限定
  filetype:pdf  文件类型

遵循死规则 9：纯本地字符串处理，无外部依赖。
遵循死规则 10：解析只做字符串匹配，无性能问题。
遵循死规则 13：不生成 __pycache__。
"""

import re
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.dont_write_bytecode = True

# 语法规则（有序，优先级从高到晚）
# 每个规则: (名, 正则, 是否可重复)
_SYNTAX_RULES: List[Tuple[str, re.Pattern, bool]] = [
    ("site", re.compile(r"site:([^\s]+)", re.IGNORECASE), False),
    ("filetype", re.compile(r"filetype:([a-z0-9]+)", re.IGNORECASE), False),
    ("after", re.compile(r"after:(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", re.IGNORECASE), False),
    ("before", re.compile(r"before:(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", re.IGNORECASE), False),
]

# bangs 语法（V1.1 已有）
_BANG_PATTERN = re.compile(r"(^|\s)![a-z0-9]+", re.IGNORECASE)

# 引擎对语法的支持能力
_ENGINE_CAPABILITIES: Dict[str, set] = {
    "baidu": {"site"},
    "bing": {"site", "filetype"},
    "duckduckgo": {"site"},
    "yandex": {"site"},
    "startpage": set(),
    "qwant": set(),
    "brave": {"site"},
    "sogou": set(),
    "360": {"site"},
    "searxng": {"site", "after", "before"},
}

# 时间限定参数映射（各引擎的 URL 参数格式）
_TIME_PARAM_FORMAT = {
    "baidu": "&gpc=stf={after},stf",  # 简化：仅年份
    "bing": "&filters=ex1%3A%22ez5_{after}%22",
    "duckduckgo": "&df={after}",
    "yandex": "&within={after}",
    "searxng": "&time_range={after}",
}


class SyntaxFilter:
    """解析后的语法限定条件"""

    def __init__(self):
        self.site: Optional[str] = None
        self.filetype: Optional[str] = None
        self.after: Optional[str] = None      # YYYY or YYYY-MM or YYYY-MM-DD
        self.before: Optional[str] = None
        self.bang: Optional[str] = None      # 如 "!w"

    @property
    def has_filters(self) -> bool:
        return any([self.site, self.filetype, self.after, self.before, self.bang])

    def to_dict(self) -> Dict[str, Any]:
        d = {}
        if self.site:
            d["site"] = self.site
        if self.filetype:
            d["filetype"] = self.filetype
        if self.after:
            d["after"] = self.after
        if self.before:
            d["before"] = self.before
        if self.bang:
            d["dang"] = self.bang
        return d


def parse_query(query: str) -> Tuple[str, SyntaxFilter]:
    """
    解析查询中的高级语法

    Returns:
        (clean_query, SyntaxFilter)
        clean_query: 移除语法限定词后的纯查询词
    """
    if not query:
        return ("", SyntaxFilter())

    clean = query.strip()
    sf = SyntaxFilter()

    # 先检查 bangs 语法（最先处理，避免被其它规则干扰）
    bang_match = _BANG_PATTERN.search(clean)
    if bang_match:
        sf.bang = bang_match.group(0).strip()
        clean = clean[:bang_match.start()] + clean[bang_match.end():]
        clean = clean.strip()

    # 依次解析各语法规则
    for name, pattern, _repeat in _SYNTAX_RULES:
        matches = list(pattern.finditer(clean))
        if not matches:
            continue
        # 取最后一个匹配（前面的如果是查询词的一部分，会被误匹配，
        # 这里取最后一个，通常语法限定在查询末尾）
        m = matches[-1]
        value = m.group(1)
        if name == "after":
            sf.after = _normalize_date(value, m)
        elif name == "before":
            sf.before = _normalize_date(value, m)
        elif name == "site":
            sf.site = value.rstrip("/")
        elif name == "filetype":
            sf.filetype = value.lower()
        # 从 clean 中移除该语法
        clean = clean[:m.start()] + clean[m.end():]
        clean = clean.strip()

    # 清理多余的空格
    clean = re.sub(r"\s+", " ", clean).strip()

    return (clean, sf)


def _normalize_date(year_str: str, m: re.Match) -> str:
    """标准化日期格式为 YYYY 或 YYYY-MM 或 YYYY-MM-DD"""
    year = int(year_str)
    if year < 1900 or year > 2100:
        return year_str  # 非法年份不处理
    groups = m.groups()
    if len(groups) >= 2 and groups[1]:
        month = int(groups[1])
        if 1 <= month <= 12:
            if len(groups) >= 3 and groups[2]:
                day = int(groups[2])
                if 1 <= day <= 31:
                    return f"{year:04d}-{month:02d}-{day:02d}"
            return f"{year:04d}-{month:02d}"
    return f"{year:04d}"


def engine_supports_syntax(engine: str, syntax_name: str) -> bool:
    """检查引擎是否支持某种语法"""
    caps = _ENGINE_CAPABILITIES.get(engine, set())
    return syntax_name in caps


def get_unsupported_syntax(engine: str, sf: SyntaxFilter) -> List[str]:
    """获取引擎不支持的语法列表"""
    unsupported = []
    for name in ["site", "filetype", "after", "before"]:
        val = getattr(sf, name, None)
        if val and not engine_supports_syntax(engine, name):
            unsupported.append(name)
    return unsupported


def apply_time_filter_to_url(engine: str, url: str, sf: SyntaxFilter) -> str:
    """
    将时间限定应用到引擎 URL

    注意：各引擎的时间参数格式差异很大，
    不支持的引擎由调用方做本地过滤。
    """
    if not sf.after and not sf.before:
        return url

    fmt = _TIME_PARAM_FORMAT.get(engine)
    if not fmt:
        return url

    # 简化处理：仅 after 优先
    time_val = sf.after or sf.before
    # 仅取年份部分
    year = time_val[:4] if len(time_val) >= 4 else time_val
    param = fmt.replace("{after}", year)

    # 拼接到 URL
    if "&" in url:
        return url + param
    else:
        return url + "?" + param.lstrip("&")


def apply_site_filter_to_query(engine: str, query: str, sf: SyntaxFilter) -> str:
    """
    将站点限定拼接到查询词

    部分引擎（如 bing）支持 site: 语法直接拼入查询词。
    """
    if not sf.site:
        return query
    if not engine_supports_syntax(engine, "site"):
        return query

    # bing / yandex 等支持 site: 操作符
    if engine in ("bing", "yandex", "brave", "baidu"):
        return f"{query} site:{sf.site}"

    return query


def filter_results_locally(
    results: List[Any],
    sf: SyntaxFilter,
    engine: str = "",
) -> Tuple[List[Any], List[str]]:
    """
    本地过滤（引擎不支持语法时的兜底）

    Returns:
        (过滤后的结果, 提示信息列表)
    """
    if not sf.has_filters or not results:
        return (results, [])

    notices: List[str] = []
    filtered = list(results)

    # 站点过滤
    if sf.site:
        before = len(filtered)
        filtered = [
            r for r in filtered
            if sf.site in getattr(r, "url", "")
        ]
        removed = before - len(filtered)
        if removed > 0 and engine:
            notices.append(
                f"{engine} 不支持 site: 语法，已本地过滤 {removed} 条"
            )

    # 文件类型过滤
    if sf.filetype:
        before = len(filtered)
        filtered = [
            r for r in filtered
            if getattr(r, "url", "").lower().endswith(f".{sf.filetype}")
        ]
        removed = before - len(filtered)
        if removed > 0 and engine:
            notices.append(
                f"{engine} 不支持 filetype: 语法，已本地过滤 {removed} 条"
            )

    # 时间过滤（基于 publish_date 或 snippet 中的年份）
    if sf.after or sf.before:
        time_before = sf.before or "9999"
        time_after = sf.after or "0000"
        before = len(filtered)
        time_filtered = []
        for r in filtered:
            # 尝试从结果中提取日期
            date_str = _extract_date_from_result(r)
            if not date_str:
                # 无法判断日期时保留（宁可多不可少）
                time_filtered.append(r)
                continue
            if time_after <= date_str[:10] <= time_before:
                time_filtered.append(r)
        removed = before - len(filtered)
        if removed > 0 and engine:
            notices.append(
                f"{engine} 不支持时间限定，已本地过滤 {removed} 条"
            )
        filtered = time_filtered

    return (filtered, notices)


def _extract_date_from_result(result: Any) -> Optional[str]:
    """尝试从结果中提取日期（用于本地时间过滤）"""
    # 优先看 publish_date 属性
    pub_date = getattr(result, "publish_date", None)
    if pub_date:
        # 尝试提取 YYYY-MM-DD
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", pub_date)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        m = re.search(r"(\d{4})", pub_date)
        if m:
            return f"{m.group(1)}-01-01"

    # 尝试从 snippet 提取年份
    snippet = getattr(result, "snippet", "") or ""
    m = re.search(r"(20\d{2})", snippet)
    if m:
        return f"{m.group(1)}-01-01"

    # 尝试从 title 提取
    title = getattr(result, "title", "") or ""
    m = re.search(r"(20\d{2})", title)
    if m:
        return f"{m.group(1)}-01-01"

    return None


def get_query_syntax_table() -> str:
    """
    生成统一查询语法表（供 CLI --help 和文档使用）
    """
    lines = [
        "统一查询语法：",
        "",
        "  [高级检索]",
        "    after:2024          时间下限（2024年及之后）",
        "    after:2024-06       时间下限（2024年6月及之后）",
        "    before:2025         时间上限（2025年及之前）",
        "    site:example.com    站点限定",
        "    filetype:pdf        文件类型限定",
        "",
        "  [快捷跳转 - bangs]",
        "    !w 关键词           维基百科",
        "    !gh 关键词           GitHub",
        "    !yt 关键词           YouTube",
        "",
        "  [引擎兼容性]",
    ]
    engines = sorted(_ENGINE_CAPABILITIES.keys())
    for eng in engines:
        caps = _ENGINE_CAPABILITIES[eng]
        cap_str = ", ".join(sorted(caps)) if caps else "仅本地过滤"
        lines.append(f"    {eng:12} {cap_str}")

    return "\n".join(lines)


if __name__ == "__main__":
    test_queries = [
        "量子计算 site:mit.edu after:2024",
        "python教程 filetype:pdf before:2023",
        "人工智能发展 after:2024-06 site:tsinghua.edu.cn",
        "!w 量子力学",
        "普通搜索词",
    ]
    for q in test_queries:
        clean, sf = parse_query(q)
        print(f"查询: {q}")
        print(f"  清洗后: {clean}")
        print(f"  语法: {sf.to_dict()}")
        print()

    print(get_query_syntax_table())
