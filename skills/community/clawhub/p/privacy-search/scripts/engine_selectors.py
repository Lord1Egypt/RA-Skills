"""
解析选择器配置（F1-2）
======================
V1.2 新增

问题背景：
    V1.1 中每个引擎适配器只有单套 CSS 选择器，例如百度写死 "div.result"。
    搜索引擎调整页面结构后该引擎立即返回 0 条结果，且调用方无法区分
    "本次搜索确实没有匹配内容" 与 "选择器已失效"，排查成本高。

解决方案：
    1. 每个引擎配置多套候选选择器，按顺序尝试，命中即用。
    2. 解析结果为空时结合页面特征判断原因，输出明确诊断。
    3. 配合 search.py 的 --selftest 命令批量体检各引擎解析健康度。
"""

import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

sys.dont_write_bytecode = True


# ============================================================
# 选择器组
# ============================================================

@dataclass
class SelectorSet:
    """
    单套选择器方案

    Attributes:
        container: 结果条目容器
        title:     标题元素（相对容器）
        link:      链接元素（相对容器），为空则复用 title
        snippet:   摘要元素（相对容器），支持逗号分隔的多个候选
    """
    container: str
    title: str
    link: str = ""
    snippet: str = ""

    def link_selector(self) -> str:
        """链接选择器，未单独配置时复用标题元素"""
        return self.link or self.title


@dataclass
class EngineSelectors:
    """
    某引擎的全部候选选择器方案

    variants 按可靠性从高到低排列，解析时逐个尝试。
    """
    engine: str
    variants: List[SelectorSet] = field(default_factory=list)
    # 页面出现以下关键词，判定为被反爬拦截而非无结果
    blocked_markers: List[str] = field(default_factory=list)
    # 页面出现以下关键词，判定为确实无匹配结果
    empty_markers: List[str] = field(default_factory=list)


# ============================================================
# 各引擎选择器注册（多套备选）
# ============================================================

SELECTORS: Dict[str, EngineSelectors] = {
    "baidu": EngineSelectors(
        engine="baidu",
        variants=[
            SelectorSet(
                container="div.result, div.result-op",
                title="h3 a",
                snippet="div.c-abstract, div.content-right_8Zs40, span.content-right_8Zs40",
            ),
            SelectorSet(
                container="div[class*='result']",
                title="h3 a, a.title",
                snippet="[class*='abstract'], [class*='content-right']",
            ),
            SelectorSet(
                container="div#content_left > div",
                title="h3 a",
                snippet="span, div.c-span-last",
            ),
        ],
        blocked_markers=["百度安全验证", "网络不给力", "请输入验证码", "wappass.baidu.com"],
        empty_markers=["抱歉，没有找到与", "没有找到该URL"],
    ),
    "bing": EngineSelectors(
        engine="bing",
        variants=[
            SelectorSet(container="li.b_algo", title="h2 a", snippet="div.b_caption p, p"),
            SelectorSet(container="ol#b_results > li", title="h2 a", snippet="p, div.b_caption"),
            SelectorSet(container="[class*='b_algo']", title="h2 a, a", snippet="p"),
        ],
        blocked_markers=["captcha", "unusual traffic"],
        empty_markers=["没有与此相关的结果", "There are no results for"],
    ),
    "sogou": EngineSelectors(
        engine="sogou",
        variants=[
            SelectorSet(container="div.vrwrap, div.rb", title="h3 a", snippet="div.str-text-info, div.ft, p.str-info"),
            SelectorSet(container="div.results > div", title="h3 a, a.pt", snippet="div[class*='info'], p"),
        ],
        blocked_markers=["请输入验证码", "antispider"],
        empty_markers=["抱歉，没有找到与"],
    ),
    "360": EngineSelectors(
        engine="360",
        variants=[
            SelectorSet(container="li.res-list", title="h3 a", snippet="p.res-desc, div.res-comm-con, p"),
            SelectorSet(container="ul.result > li", title="h3 a", snippet="p"),
        ],
        blocked_markers=["验证码", "安全验证"],
        empty_markers=["没有找到相关结果"],
    ),
    "duckduckgo": EngineSelectors(
        engine="duckduckgo",
        variants=[
            SelectorSet(container="div.result__body", title="a.result__a", snippet="a.result__snippet, div.result__snippet"),
            SelectorSet(container="div.web-result", title="a.result__a, h2 a", snippet="[class*='snippet']"),
            SelectorSet(container="div[class*='result']", title="a[class*='result__a'], h2 a", snippet="[class*='snippet']"),
        ],
        blocked_markers=["anomaly", "blocked"],
        empty_markers=["No results", "没有找到"],
    ),
    "yandex": EngineSelectors(
        engine="yandex",
        variants=[
            SelectorSet(container="li.serp-item", title="a.organic__url, h2 a", snippet="div.organic__content-wrapper, div.text-container"),
            SelectorSet(container="div.serp-item", title="h2 a, a[href^='http']", snippet="[class*='text']"),
        ],
        blocked_markers=["captcha", "подтвердите", "ddos"],
        empty_markers=["ничего не нашлось", "nothing found"],
    ),
    "startpage": EngineSelectors(
        engine="startpage",
        variants=[
            SelectorSet(container="div.w-gl__result", title="a.w-gl__result-title, h3 a", snippet="p.w-gl__description"),
            SelectorSet(container="div[class*='result']", title="h3 a, a[class*='title']", snippet="p, [class*='description']"),
        ],
        blocked_markers=["captcha", "suspicious activity"],
        empty_markers=["No results found"],
    ),
    "qwant": EngineSelectors(
        engine="qwant",
        variants=[
            SelectorSet(container="div[data-testid='webResult']", title="a", snippet="[class*='desc'], p"),
            SelectorSet(container="article, div[class*='result']", title="a[href^='http']", snippet="p"),
        ],
        blocked_markers=["captcha", "robot"],
        empty_markers=["No result", "Aucun résultat"],
    ),
    "brave": EngineSelectors(
        engine="brave",
        variants=[
            SelectorSet(container="div.snippet", title="a", snippet="div.snippet-description, p"),
            SelectorSet(container="div[data-type='web'], div[class*='result']", title="a[href^='http']", snippet="[class*='description'], p"),
        ],
        blocked_markers=["captcha", "verify you are human"],
        empty_markers=["No results found"],
    ),
}


# ============================================================
# 解析诊断
# ============================================================

class ParseDiagnosis:
    """解析结果诊断标识"""
    OK = "ok"                       # 正常解析出结果
    EMPTY_CONFIRMED = "empty"       # 确认无匹配结果
    BLOCKED = "blocked"             # 被反爬拦截
    PARTIAL = "partial"             # 有结果但数量远低于预期
    SELECTOR_STALE = "stale"        # 选择器可能失效
    UNKNOWN = "unknown"             # 无法判断


DIAGNOSIS_HINT: Dict[str, str] = {
    ParseDiagnosis.EMPTY_CONFIRMED: "该引擎确实没有匹配结果，可尝试更换关键词",
    ParseDiagnosis.BLOCKED: "请求被引擎拦截，建议降低搜索频率、更换网络或启用代理",
    ParseDiagnosis.PARTIAL: "该引擎返回结果偏少，可能触发了限流，可稍后重试或改用其他引擎",
    ParseDiagnosis.SELECTOR_STALE: "页面结构可能已变化，解析规则需要更新，可执行 --selftest 复查",
    ParseDiagnosis.UNKNOWN: "返回内容异常，建议加 --verbose 查看详情",
}


def get_selectors(engine: str) -> Optional[EngineSelectors]:
    """获取指定引擎的选择器配置"""
    return SELECTORS.get(engine)


# ============================================================
# 跳转链接识别
# ============================================================
# 部分引擎（尤其百度）返回自家跳转地址而非目标站点真实 URL，
# 形如 http://www.baidu.com/link?url=xxxx。
# 这类地址会导致：
#   1. 跨引擎去重失效（同一页面在不同引擎下 URL 完全不同）
#   2. 域名质量评分失准（识别成搜索引擎自身域名）
# 因此需要标记出来，由排序模块降权处理。

REDIRECT_PATTERNS = (
    "baidu.com/link?url=",
    "so.com/link?",
    "sogou.com/link?",
    "r.search.yahoo.com",
    "duckduckgo.com/l/?",
)


def is_redirect_url(url: str) -> bool:
    """判断是否为搜索引擎的跳转中转地址"""
    if not url:
        return False
    lowered = url.lower()
    return any(p in lowered for p in REDIRECT_PATTERNS)


def diagnose_empty(engine: str, html: str) -> str:
    """
    在解析结果为空时判断原因

    Args:
        engine: 引擎名
        html: 原始页面内容

    Returns:
        ParseDiagnosis 中的常量
    """
    cfg = SELECTORS.get(engine)
    if not cfg or not html:
        return ParseDiagnosis.UNKNOWN

    lowered = html.lower()

    for marker in cfg.blocked_markers:
        if marker.lower() in lowered:
            return ParseDiagnosis.BLOCKED

    for marker in cfg.empty_markers:
        if marker.lower() in lowered:
            return ParseDiagnosis.EMPTY_CONFIRMED

    # 页面内容过短通常意味着被拦截或跳转
    if len(html) < 2000:
        return ParseDiagnosis.BLOCKED

    # 页面正常返回却解析不出条目，判定为选择器失效
    return ParseDiagnosis.SELECTOR_STALE


def is_blocked_page(engine: str, html: str) -> bool:
    """
    判断页面是否带有反爬拦截特征

    与 diagnose_empty 的区别：本函数在「已解析出结果」时也会被调用。
    引擎限流时未必返回空页——百度会跳转验证页却仍夹带一两条结果，
    只在零结果时检查拦截，这种半拦截状态会被当成正常返回。
    """
    cfg = SELECTORS.get(engine)
    if not cfg or not html:
        return False
    lowered = html.lower()
    return any(m.lower() in lowered for m in cfg.blocked_markers)


# 实际结果数低于期望值的该比例时，判定为「偏少」。
# 取 1/3 是因为引擎本就不保证返回满额（去重、广告位、地域差异都会减少条目），
# 阈值过高会频繁误报；低于三分之一则通常意味着限流或解析漏抓。
PARTIAL_RATIO = 1.0 / 3


def diagnose_partial(engine: str, html: str, got: int, expected: int) -> str:
    """
    在已有结果时判断返回是否异常偏少

    Returns:
        ParseDiagnosis.OK / BLOCKED / PARTIAL
    """
    if is_blocked_page(engine, html):
        return ParseDiagnosis.BLOCKED
    if expected > 1 and got < max(1, int(expected * PARTIAL_RATIO)):
        return ParseDiagnosis.PARTIAL
    return ParseDiagnosis.OK


def diagnosis_hint(diagnosis: str) -> str:
    """获取诊断对应的处理建议"""
    return DIAGNOSIS_HINT.get(diagnosis, "")
