#!/usr/bin/env python3
"""
F1: 多引擎并行搜索模块
- asyncio + aiohttp 并发请求多个搜索引擎
- BeautifulSoup 解析 HTML 结果
- SimHash 去重与多引擎交叉验证排序
- 超时控制 + 请求频率限制
- 错误分类：网络错误、配置错误、引擎错误
- 国内可用备选引擎：Yandex / Startpage / Qwant / Brave

V1.2 变更：
    1. 传输层统一收归 http_client，隐私头配置真正作用于每次请求
       （此前各适配器自行硬编码 headers，privacy 模块未被引用）
    2. 引擎清单统一取自 engines_registry
    3. 接入结果缓存与搜索历史（cache）
    4. 接入多套备选选择器与解析诊断（selectors）
    5. 去重排序迁移至 ranking，支持相关度与权威度加权
    6. 网络错误自动重试、User-Agent 池轮换
    7. num_results 支持从配置文件读取
"""

import asyncio
import hashlib
import os
import random
import re
import sys
import time
import traceback
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote, urlparse

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True


# 依赖检查须早于第三方 import，否则用户只会看到裸 ModuleNotFoundError。
# version_util 仅依赖标准库，可安全提前导入。
try:
    from version_util import require_dependencies
except ImportError:
    from .version_util import require_dependencies

require_dependencies()

import aiohttp
import yaml
from bs4 import BeautifulSoup

try:
    from engines_registry import (
        all_engine_names, default_engines, get_authority,
        is_valid_engine, strict_fallback_engines, validate_engines,
        format_engine_table,
    )
    from http_client import RequestContext, RetryPolicy, build_connector, fetch_text, fetch_json
    from privacy import PrivacyManager
    from engine_selectors import (
        ParseDiagnosis, diagnose_empty, diagnose_partial, diagnosis_hint, get_selectors,
    )
    from ranking import (
        deduplicate, rank_results, RankWeights, jieba_available, weights_from_config,
        relevance_score,
    )
    from cache import SearchCache, build_cache_from_config, make_cache_key
    from logging_util import build_logger_from_config
    from version_util import get_current_version
except ImportError:  # 以包方式导入时
    from .engines_registry import (
        all_engine_names, default_engines, get_authority,
        is_valid_engine, strict_fallback_engines, validate_engines,
        format_engine_table,
    )
    from .http_client import RequestContext, RetryPolicy, build_connector, fetch_text, fetch_json
    from .privacy import PrivacyManager
    from .engine_selectors import (
        ParseDiagnosis, diagnose_empty, diagnose_partial, diagnosis_hint, get_selectors,
    )
    from .ranking import (
        deduplicate, rank_results, RankWeights, jieba_available, weights_from_config,
        relevance_score,
    )
    from .cache import SearchCache, build_cache_from_config, make_cache_key
    from .logging_util import build_logger_from_config
    from .version_util import get_current_version


# ============================================================
# 错误分类
# ============================================================

class ErrorCategory(str, Enum):
    """错误分类"""
    NETWORK = "network"
    CONFIG = "config"
    ENGINE = "engine"


@dataclass
class ClassifiedError:
    """分类错误信息"""
    category: ErrorCategory
    engine: str
    message: str
    troubleshooting: List[str]
    exception: Optional[Exception] = None


def classify_error(engine: str, exception: Exception) -> ClassifiedError:
    """
    将统一的 Exception 分类为 network/config/engine

    Error categorization principles:
    - NetworkError → network (timeout, connection refused, DNS failure, SSL error, proxy error)
    - ConfigError → config (missing/invalid config key, invalid engine name)
    - ParserError → engine (HTML parsing failure, response format changed)
    """
    # Network errors
    network_exceptions = (
        aiohttp.ClientConnectorError,
        aiohttp.ServerDisconnectedError,
        aiohttp.ClientOSError,
        TimeoutError,
        ConnectionRefusedError,
    )

    # Config errors
    config_exceptions = (
        KeyError,
        ValueError,
    )

    # Check network errors first
    if isinstance(exception, network_exceptions):
        msg = str(exception).lower()
        if "timeout" in msg or "timed out" in msg:
            troubleshooting = [
                f"  1. 检查网络连接是否正常（ping www.baidu.com）",
                f"  2. 确认网络环境不受限制（特定网络可能阻止访问某些引擎）",
                f"  3. 增加超时时间：修改 config.yaml 中 search.timeout",
                f"  4. 检查代理/VPN 设置是否正确",
            ]
        elif "dns" in msg or "resolve" in msg:
            troubleshooting = [
                f"  1. DNS 解析失败，尝试更换 DNS 服务器",
                f"  2. 检查网络连接是否正常",
            ]
        else:
            troubleshooting = [
                f"  1. 检查网络连接是否正常",
                f"  2. 确认目标引擎网站可访问",
                f"  3. 如使用代理，检查代理配置",
            ]
        return ClassifiedError(
            category=ErrorCategory.NETWORK,
            engine=engine,
            message=f"网络连接失败: {exception}",
            troubleshooting=troubleshooting,
            exception=exception,
        )

    # Config errors
    if isinstance(exception, config_exceptions):
        troubleshooting = [
            f"  1. 确认 config.yaml 文件格式正确（冒号后有空格）",
            f"  2. 复制 references/config.yaml.example 重新配置",
            f"  3. 检查引用的引擎名称是否正确",
        ]
        return ClassifiedError(
            category=ErrorCategory.CONFIG,
            engine=engine,
            message=f"配置错误: {exception}",
            troubleshooting=troubleshooting,
            exception=exception,
        )

    # Engine parser errors (default)
    troubleshooting = [
        f"  1. {engine} 可能已更新页面结构",
        f"  2. 尝试更新本 skill 到最新版本",
        f"  3. 暂不使用该引擎：--engines 参数排除",
    ]
    return ClassifiedError(
        category=ErrorCategory.ENGINE,
        engine=engine,
        message=f"引擎解析或请求失败: {exception}",
        troubleshooting=troubleshooting,
        exception=exception,
    )


# ============================================================
# 数据结构
# ============================================================

@dataclass
class SearchResult:
    """单条搜索结果"""
    title: str
    url: str
    snippet: str
    engine: str
    rank: int = 0
    simhash: Optional[int] = None
    score: float = 0.0
    # 去重合并后，收录同一 URL 的全部引擎名。
    # 为空表示尚未参与合并，此时以 engine 单值为准。
    engines: List[str] = field(default_factory=list)

    @property
    def engine_set(self) -> List[str]:
        """收录该结果的引擎列表，未合并时退化为单元素"""
        return list(self.engines) if self.engines else ([self.engine] if self.engine else [])

    def compute_simhash(self) -> int:
        """
        计算 SimHash 指纹

        V1.2 起委托 ranking 模块的标准实现（按位加权投票），
        此前的异或合并方式无法稳定反映文本相似度。
        """
        from ranking import compute_simhash as _cs
        self.simhash = _cs(f"{self.title} {self.snippet}")
        return self.simhash

    def to_dict(self) -> Dict[str, Any]:
        """转为可序列化字典（用于缓存与 JSON 输出）"""
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "engine": self.engine,
            "engines": self.engine_set,
            "engine_count": len(self.engine_set) if self.engines else 1,
            "rank": self.rank,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """从字典还原（用于读取缓存）"""
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            snippet=data.get("snippet", ""),
            engine=data.get("engine", ""),
            rank=int(data.get("rank", 0) or 0),
            score=float(data.get("score", 0) or 0),
            engines=list(data.get("engines", []) or []),
        )


@dataclass
class SearchResponse:
    """搜索响应"""
    engine: str
    results: List[SearchResult] = field(default_factory=list)
    error: Optional[str] = None
    elapsed: float = 0.0
    diagnosis: Optional[str] = None      # 解析诊断结果（selectors.ParseDiagnosis）
    selector_variant: int = -1           # 命中的选择器方案序号，-1 表示未命中


# ============================================================
# 搜索引擎适配器
# ============================================================
# V1.2 架构调整：
#   适配器只负责「构造 URL」与「解析响应」，
#   请求发送、隐私头、UA 轮换、代理、重试统一由 http_client 处理。
#   这样新增传输层能力时无需逐个修改适配器。


class EngineAdapter:
    """
    搜索引擎适配器基类

    子类需实现 build_url()；HTML 型引擎默认复用 selectors 中的
    多套备选选择器解析，无需各自重写 parse()。
    """

    def __init__(self, name: str, timeout: int = 10):
        self.name = name
        self.timeout = timeout

    # ---------- 需子类实现 ----------

    def build_url(self, query: str, num: int) -> str:
        """构造搜索请求地址"""
        raise NotImplementedError

    def extra_headers(self) -> Dict[str, str]:
        """引擎特有的附加请求头（可选）"""
        return {}

    # ---------- 通用实现 ----------

    async def search(
        self,
        session: aiohttp.ClientSession,
        query: str,
        num: int = 10,
        ctx: Optional[RequestContext] = None,
    ) -> SearchResponse:
        """
        执行搜索

        Args:
            session: aiohttp 会话
            query: 查询词
            num: 期望结果数
            ctx: 统一请求上下文；为空时构造一个默认上下文（兼容单元测试）
        """
        ctx = ctx or RequestContext(timeout=self.timeout)
        start = time.time()
        try:
            html = await fetch_text(
                session,
                self.build_url(query, num),
                ctx,
                extra_headers=self.extra_headers(),
                timeout=self.timeout,
            )
            results = self.parse(html, num)
            elapsed = time.time() - start

            if results:
                # 有结果不等于正常：引擎限流时可能只吐出一两条，
                # 若一律记为 OK，用户要 10 条只拿到 1 条却得不到任何解释，
                # 无从判断是「确实只有这些」还是「被限流了」。
                diag = diagnose_partial(self.name, html, len(results), num)
                return SearchResponse(
                    engine=self.name, results=results, elapsed=elapsed,
                    diagnosis=diag,
                    error=None if diag == ParseDiagnosis.OK else diagnosis_hint(diag),
                )

            # 无结果时给出明确诊断，便于区分「真没有」与「解析失效」
            diag = diagnose_empty(self.name, html)
            return SearchResponse(
                engine=self.name, results=[], elapsed=elapsed, diagnosis=diag,
                error=None if diag == ParseDiagnosis.EMPTY_CONFIRMED else diagnosis_hint(diag),
            )
        except Exception as e:  # noqa: BLE001 - 统一转为响应对象向上传递
            return SearchResponse(
                engine=self.name, error=str(e), elapsed=time.time() - start,
                diagnosis=ParseDiagnosis.UNKNOWN,
            )

    def parse(self, html: str, num: int) -> List[SearchResult]:
        """
        使用多套备选选择器解析页面

        按 selectors 中登记的顺序依次尝试，命中即返回，
        任一方案失效时自动回退到下一套。
        """
        cfg = get_selectors(self.name)
        if not cfg or not html:
            return []

        soup = BeautifulSoup(html, "lxml")

        for variant_idx, sel in enumerate(cfg.variants):
            results = self._parse_with(soup, sel, num)
            if results:
                self._last_variant = variant_idx
                return results
        return []

    def _parse_with(self, soup: "BeautifulSoup", sel, num: int) -> List[SearchResult]:
        """按单套选择器方案解析"""
        results: List[SearchResult] = []
        try:
            containers = soup.select(sel.container)
        except Exception:  # noqa: BLE001 - 选择器语法异常不应中断整体流程
            return []

        for item in containers:
            if len(results) >= num:
                break
            try:
                link_el = item.select_one(sel.link_selector())
                if not link_el:
                    continue
                url = (link_el.get("href") or "").strip()
                if not url or url.startswith("javascript:"):
                    continue

                title_el = item.select_one(sel.title) or link_el
                title = title_el.get_text(strip=True)
                if not title:
                    continue

                snippet = ""
                if sel.snippet:
                    snip_el = item.select_one(sel.snippet)
                    if snip_el:
                        snippet = snip_el.get_text(strip=True)

                results.append(SearchResult(
                    title=title,
                    url=url,
                    snippet=snippet,
                    engine=self.name,
                    rank=len(results) + 1,
                ))
            except Exception:  # noqa: BLE001 - 单条解析失败跳过即可
                continue

        return results


# ---------- 国内引擎 ----------

class BaiduAdapter(EngineAdapter):
    """百度搜索"""

    def __init__(self):
        super().__init__("baidu", timeout=10)

    def build_url(self, query: str, num: int) -> str:
        return f"https://www.baidu.com/s?wd={quote(query)}&rn={num}"


class BingAdapter(EngineAdapter):
    """必应搜索"""

    def __init__(self):
        super().__init__("bing", timeout=10)

    def build_url(self, query: str, num: int) -> str:
        return f"https://www.bing.com/search?q={quote(query)}&count={num}"


class SogouAdapter(EngineAdapter):
    """搜狗搜索"""

    def __init__(self):
        super().__init__("sogou", timeout=10)

    def build_url(self, query: str, num: int) -> str:
        return f"https://www.sogou.com/web?query={quote(query)}"


class So360Adapter(EngineAdapter):
    """360 搜索"""

    def __init__(self):
        super().__init__("360", timeout=10)

    def build_url(self, query: str, num: int) -> str:
        return f"https://www.so.com/s?q={quote(query)}"


# ---------- 隐私优先引擎 ----------

class DuckDuckGoAdapter(EngineAdapter):
    """DuckDuckGo（使用 HTML 轻量版，避免 JS 渲染）"""

    def __init__(self):
        super().__init__("duckduckgo", timeout=15)

    def build_url(self, query: str, num: int) -> str:
        return f"https://html.duckduckgo.com/html/?q={quote(query)}"


class YandexAdapter(EngineAdapter):
    """Yandex 搜索"""

    def __init__(self):
        super().__init__("yandex", timeout=15)

    def build_url(self, query: str, num: int) -> str:
        return f"https://yandex.com/search/?text={quote(query)}"


class StartpageAdapter(EngineAdapter):
    """Startpage（Google 结果代理）"""

    def __init__(self):
        super().__init__("startpage", timeout=15)

    def build_url(self, query: str, num: int) -> str:
        return f"https://www.startpage.com/sp/search?query={quote(query)}"


class QwantAdapter(EngineAdapter):
    """Qwant 搜索"""

    def __init__(self):
        super().__init__("qwant", timeout=15)

    def build_url(self, query: str, num: int) -> str:
        return f"https://lite.qwant.com/?q={quote(query)}&t=web"


class BraveAdapter(EngineAdapter):
    """Brave Search"""

    def __init__(self):
        super().__init__("brave", timeout=15)

    def build_url(self, query: str, num: int) -> str:
        return f"https://search.brave.com/search?q={quote(query)}"


# ---------- 本地实例 ----------

class SearXNGAdapter(EngineAdapter):
    """
    本地 SearXNG 实例

    走 JSON 接口而非 HTML 解析，稳定性更高。
    V1.2 增加 bangs 语法与搜索类目透传（SearXNG 原生能力）。
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8888"):
        super().__init__("searxng", timeout=20)
        self.base_url = base_url.rstrip("/")
        self.category = "general"

    def build_url(self, query: str, num: int) -> str:
        url = f"{self.base_url}/search?q={quote(query)}&format=json"
        if self.category and self.category != "general":
            url += f"&categories={quote(self.category)}"
        return url

    async def search(
        self,
        session: aiohttp.ClientSession,
        query: str,
        num: int = 10,
        ctx: Optional[RequestContext] = None,
    ) -> SearchResponse:
        """SearXNG 返回 JSON，单独实现"""
        ctx = ctx or RequestContext(timeout=self.timeout)
        start = time.time()
        try:
            data = await fetch_json(
                session, self.build_url(query, num), ctx, timeout=self.timeout
            )
            results = self.parse_json(data, num)
            return SearchResponse(
                engine=self.name, results=results, elapsed=time.time() - start,
                diagnosis=ParseDiagnosis.OK if results else ParseDiagnosis.EMPTY_CONFIRMED,
            )
        except Exception as e:  # noqa: BLE001
            return SearchResponse(
                engine=self.name, error=str(e), elapsed=time.time() - start,
                diagnosis=ParseDiagnosis.UNKNOWN,
            )

    def parse_json(self, data: Any, num: int) -> List[SearchResult]:
        """解析 SearXNG JSON 响应"""
        results: List[SearchResult] = []
        if not isinstance(data, dict):
            return results
        for idx, item in enumerate(data.get("results", [])[:num]):
            if not isinstance(item, dict):
                continue
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("content", ""),
                engine=self.name,
                rank=idx + 1,
            ))
        return results

    # 兼容旧接口命名
    def parse(self, data: Any, num: int) -> List[SearchResult]:  # type: ignore[override]
        return self.parse_json(data, num)


# ============================================================
# 引擎管理
# ============================================================

# strict 模式降级链，取自引擎注册表（单一真相源）
STRICT_FALLBACK_ENGINES = strict_fallback_engines()

# bangs 语法前缀，形如 !w !yt !gh，由 SearXNG 原生支持
_BANG_PATTERN = re.compile(r"(^|\s)![a-z0-9]+", re.IGNORECASE)


def has_bang(query: str) -> bool:
    """判断查询是否使用了 bangs 语法"""
    return bool(_BANG_PATTERN.search(query or ""))


class EngineManager:
    """引擎实例管理"""

    def __init__(self, searxng_url: str = "http://127.0.0.1:8888"):
        self.searxng_url = searxng_url
        self._registry = {
            "baidu": BaiduAdapter,
            "bing": BingAdapter,
            "sogou": SogouAdapter,
            "360": So360Adapter,
            "duckduckgo": DuckDuckGoAdapter,
            "yandex": YandexAdapter,
            "startpage": StartpageAdapter,
            "qwant": QwantAdapter,
            "brave": BraveAdapter,
        }

    def get_adapter(self, name: str) -> Optional[EngineAdapter]:
        """按引擎名创建适配器实例"""
        if name == "searxng":
            return SearXNGAdapter(self.searxng_url)
        cls = self._registry.get(name)
        return cls() if cls else None

    def get_adapters(self, names: List[str]) -> List[EngineAdapter]:
        """批量创建适配器，忽略未知引擎"""
        adapters = []
        for n in names:
            ad = self.get_adapter(n)
            if ad:
                adapters.append(ad)
        return adapters

    def available_engines(self) -> List[str]:
        """全部可用引擎名"""
        return all_engine_names()


# ============================================================
# 去重与排序（实现位于 ranking 模块）
# ============================================================

def hamming_distance(a: int, b: int) -> int:
    """计算汉明距离（转发至 ranking）"""
    from ranking import hamming_distance as _hd
    return _hd(a, b)


def deduplicate_results(results: List[SearchResult], threshold: int = 3) -> List[SearchResult]:
    """
    结果去重

    先按归一化 URL 精确去重，再用 SimHash 消除近似重复。
    """
    return deduplicate(results, threshold=threshold)


def cross_engine_rank(
    results: List[SearchResult],
    query: str = "",
    weights: Optional["RankWeights"] = None,
    total_engines: Optional[int] = None,
) -> List[SearchResult]:
    """
    多引擎交叉验证排序

    V1.2 起改为多因子加权：共识度、位次、查询相关度、引擎权威度、域名质量。
    weights 为空时使用默认权重。

    total_engines 传入本次实际发起搜索的引擎数，使共识度分母稳定；
    若不传，则由结果反推，某些引擎无结果时分母会偏小。
    """
    return rank_results(results, query=query, weights=weights,
                        total_engines=total_engines)


async def try_engine_with_fallback(
    adapter: EngineAdapter,
    session: aiohttp.ClientSession,
    query: str,
    num: int,
    ctx: Optional[RequestContext] = None,
) -> Tuple[Optional[SearchResponse], Optional[ClassifiedError]]:
    """
    尝试单个引擎，失败时返回分类错误

    用于 strict 模式下按降级链依次切换引擎。
    """
    try:
        result = await adapter.search(session, query, num, ctx)
        if result.error and result.error.strip():
            err = classify_error(adapter.name, Exception(result.error))
            return None, err
        return result, None
    except Exception as e:  # noqa: BLE001
        return None, classify_error(adapter.name, e)


# ============================================================
# 搜索编排器
# ============================================================

class SearchOrchestrator:
    """
    搜索编排器

    职责：引擎选择 → 并发调度 → 缓存 → 去重 → 排序 → 错误汇总。
    传输细节（隐私头 / UA / 代理 / 重试）由 http_client 承担。
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        search_cfg = self.config.get("search", {}) or {}
        searxng_cfg = self.config.get("searxng", {}) or {}

        base_url = f"http://{searxng_cfg.get('host', '127.0.0.1')}:{searxng_cfg.get('port', 8888)}"
        self.engine_manager = EngineManager(base_url)

        # searxng.enabled 此前未被消费，V1.2 起真正生效
        self.searxng_enabled = bool(searxng_cfg.get("enabled", True))

        self.privacy_manager = PrivacyManager(self.config)
        self.cache = build_cache_from_config(self.config)
        # 排序权重可在配置中调整，缺省或非法时回落默认值
        self.rank_weights = weights_from_config(self.config)
        # logging 段此前未被消费，V1.2 起真正写入日志文件
        self.logger = build_logger_from_config(self.config)

        # 判定「整体跑题」的相关度上限。
        # 实测（TF-IDF 模式）：命中主题的标题相关度 0.75~1.0，完全跑题的
        # 泛化结果约 0.29~0.47，取 0.5 可稳妥区分而不误伤部分匹配。
        self._LOW_RELEVANCE_MAX = 0.5
        # 样本过少时波动大，不足此数不做判定
        self._LOW_RELEVANCE_MIN_SAMPLES = 3

        self._request_counts: Dict[str, int] = defaultdict(int)
        self._last_reset = datetime.now()
        self._classified_errors: List[ClassifiedError] = []
        self._cache_hit = False
        self._notices: List[str] = []
        # V1.9 新增：记录本次搜索使用的引擎列表（用于可信度标记）
        self._last_engines_used: List[str] = []
        # 配置层面的告警独立保存：_notices 每次搜索会被清空，
        # 而配置问题在整个进程生命周期内都应可见
        self._config_warnings: List[str] = list(
            getattr(self.privacy_manager, "config_warnings", []) or []
        )
        # strict 引擎全部失败时是否允许降级到国内引擎，默认关闭（隐私优先）
        self.allow_fallback = False

    # ---------- 状态 ----------

    @property
    def classified_errors(self) -> List[ClassifiedError]:
        """本次搜索收集到的分类错误"""
        return self._classified_errors

    @property
    def cache_hit(self) -> bool:
        """本次结果是否来自缓存"""
        return self._cache_hit

    @property
    def notices(self) -> List[str]:
        """本次搜索产生的提示信息"""
        return self._notices

    @property
    def last_engines_used(self) -> List[str]:
        """本次搜索使用的引擎列表（V1.9 新增，用于可信度标记）"""
        return self._last_engines_used

    def _check_rate_limit(self, engine_name: str) -> bool:
        """检查是否超过单引擎日请求上限"""
        if datetime.now() - self._last_reset > timedelta(days=1):
            self._request_counts.clear()
            self._last_reset = datetime.now()
        limit = self.config.get("search", {}).get("daily_request_limit", 200)
        return self._request_counts[engine_name] < limit

    # ---------- 引擎选择 ----------

    def resolve_engines(
        self,
        engines: Optional[List[str]],
        privacy_mode: str,
        query: str = "",
    ) -> List[str]:
        """
        确定本次使用的引擎列表

        规则：
          - 显式指定则校验后使用
          - strict 模式下过滤掉不满足隐私要求的引擎，避免隐私承诺被绕过
          - strict 模式未指定引擎时取隐私友好引擎（含 SearXNG 优先）
          - normal 模式取配置的默认引擎
          - 使用 bangs 语法时仅保留 SearXNG（其它引擎不支持该语法）
        """
        if engines:
            valid, invalid = validate_engines(engines)
            if invalid:
                self._notices.append(
                    f"已忽略无法识别的引擎：{', '.join(invalid)}；"
                    f"可用引擎见 --list-engines"
                )
            # strict 模式下显式指定也不得绕过白名单：
            # 否则隐私报告会声称「已屏蔽 bing」而实际仍在向 bing 发起请求
            if privacy_mode == "strict":
                allowed = set(self.privacy_manager.get_allowed_engines())
                blocked = [e for e in valid if e not in allowed]
                valid = [e for e in valid if e in allowed]
                if blocked:
                    self._notices.append(
                        f"strict 模式已拒绝隐私保护不足的引擎：{', '.join(blocked)}；"
                        f"如需使用请改用 --privacy normal"
                    )
                if not valid:
                    self._notices.append(
                        "指定的引擎在 strict 模式下均不可用，已回退到隐私友好引擎"
                    )
                    valid = self.privacy_manager.get_allowed_engines()
            selected = valid
        elif privacy_mode == "strict":
            selected = self.privacy_manager.get_allowed_engines()
        else:
            selected = self.config.get("search", {}).get("default_engines") or default_engines()

        selected = list(dict.fromkeys(selected))  # 去重保序

        # bangs 语法仅 SearXNG 支持
        if has_bang(query):
            if "searxng" in selected and self.searxng_enabled:
                self._notices.append("检测到 bangs 语法，本次仅使用本地 SearXNG")
                return ["searxng"]
            self._notices.append(
                "检测到 bangs 语法，但本地 SearXNG 未启用；"
                "该语法需要 SearXNG 支持，已按普通关键词搜索"
            )

        # searxng 未启用则剔除
        if not self.searxng_enabled and "searxng" in selected:
            selected = [e for e in selected if e != "searxng"]

        return selected

    # ---------- 主流程 ----------

    async def search(
        self,
        query: str,
        engines: Optional[List[str]] = None,
        num: Optional[int] = None,
        privacy_mode: str = "normal",
        use_cache: bool = True,
        verbose: bool = False,
    ) -> List[SearchResult]:
        """
        执行多引擎并行搜索

        Args:
            query: 查询词
            engines: 指定引擎；为空时按隐私模式自动选择
            num: 每引擎结果数；为空时读取配置
            privacy_mode: normal | strict
            use_cache: 是否使用缓存
            verbose: 输出重试等过程信息

        Returns:
            去重排序后的结果列表
        """
        self._classified_errors = []
        # 配置告警在每轮搜索都需重新提示，故作为初始内容而非清空
        self._notices = list(self._config_warnings)
        self._cache_hit = False
        entered = time.time()

        search_cfg = self.config.get("search", {}) or {}
        # num_results 此前未被读取，V1.2 起生效；CLI 显式传参优先
        if num is None:
            num = int(search_cfg.get("num_results", 10))

        self.privacy_manager.set_mode_silent(privacy_mode)
        active = self.resolve_engines(engines, privacy_mode, query)
        active = [e for e in active if self._check_rate_limit(e)]
        # V1.9 新增：记录本次使用的引擎列表（用于可信度标记）
        self._last_engines_used = active

        if not active:
            self._notices.append("没有可用引擎，请检查配置或引擎名是否正确")
            self.logger.warning(
                f"no_engine_available mode={privacy_mode} requested={engines or 'auto'}"
            )
            return []

        # 缓存查询
        cache_key = make_cache_key(query, active, privacy_mode, num)
        if use_cache and self.cache.available:
            cached = self.cache.get(cache_key)
            if cached is not None:
                self._cache_hit = True
                hit_results = [SearchResult.from_dict(d) for d in cached]
                self.logger.log_search(
                    query, active, privacy_mode, len(hit_results),
                    time.time() - entered, cache_hit=True,
                )
                return hit_results

        started = time.time()
        timeout = int(search_cfg.get("timeout", 15))
        retry_max = int(search_cfg.get("retry_max", 2))
        max_concurrent = int(search_cfg.get("max_concurrent", 6))

        # 隐私配置在此处真正接入请求链路
        ctx = self.privacy_manager.build_request_context(
            timeout=timeout, retry_max=retry_max, verbose=verbose
        )

        all_results = await self._run_engines(active, query, num, ctx, search_cfg)

        # strict 模式全部失败时的兜底
        if privacy_mode == "strict" and not all_results:
            all_results = await self._strict_fallback(query, num, ctx, search_cfg)

        threshold = int(search_cfg.get("dedup_threshold", 3))
        unique = deduplicate_results(all_results, threshold=threshold)
        # 共识度分母取实际发起搜索的引擎数，而非有结果的引擎数，
        # 否则部分引擎失败时共识度会被虚高
        ranked = cross_engine_rank(unique, query=query, weights=self.rank_weights,
                                   total_engines=len(active))

        elapsed = time.time() - started

        self._warn_low_relevance(query, all_results)

        # 写入缓存与历史
        if self.cache.available:
            if ranked and use_cache:
                self.cache.set(cache_key, query, active, privacy_mode,
                               [r.to_dict() for r in ranked])
            self.cache.add_history(query, active, privacy_mode, len(ranked), elapsed)

        self.logger.log_search(
            query, active, privacy_mode, len(ranked), elapsed,
            cache_hit=False, errors=self._classified_errors,
        )

        return ranked

    def _warn_low_relevance(self, query: str, results: List[SearchResult]) -> None:
        """
        某引擎全部结果都与查询词无关时提示用户

        搜索引擎对无 cookie 的裸请求可能返回一份泛化的缓存兜底页——
        查「python 装饰器 原理」却回一堆 Python 官网下载页。
        这类响应状态码正常、条目数量充足，仅凭 HTTP 层无从察觉，
        用户会误以为「网上就这些资料」。
        """
        if not results:
            return

        by_engine: Dict[str, List[SearchResult]] = {}
        for r in results:
            by_engine.setdefault(r.engine, []).append(r)

        for engine, items in by_engine.items():
            if len(items) < self._LOW_RELEVANCE_MIN_SAMPLES:
                continue
            try:
                top = max(
                    relevance_score(query, it.title or "", it.snippet or "")
                    for it in items
                )
            except Exception:  # noqa: BLE001 - 提示功能不得影响主流程
                continue
            if top <= self._LOW_RELEVANCE_MAX:
                self._notices.append(
                    "%s 返回的结果与查询词关联较弱，可能是该引擎的兜底响应；"
                    "建议核对其他引擎的结果" % engine
                )

    async def _run_engines(
        self,
        engine_names: List[str],
        query: str,
        num: int,
        ctx: RequestContext,
        search_cfg: Dict[str, Any],
    ) -> List[SearchResult]:
        """并发执行指定引擎的搜索"""
        adapters = self.engine_manager.get_adapters(engine_names)
        if not adapters:
            return []

        connector = build_connector(int(search_cfg.get("max_concurrent", 6)))
        # 默认 1.0-5.0 与 config.yaml.example 一致：防封是合理默认值。
        # 0.0-1.0 偏快，未配置时易触发限流
        delay_min = float(search_cfg.get("request_delay_min", 1.0))
        delay_max = float(search_cfg.get("request_delay_max", 5.0))

        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [
                self._search_one(
                    adapter, session, query, num, ctx,
                    random.uniform(delay_min, delay_max),
                )
                for adapter in adapters
            ]
            responses = await asyncio.gather(*tasks, return_exceptions=True)

        results: List[SearchResult] = []
        for resp in responses:
            if isinstance(resp, BaseException) or resp is None:
                continue
            items, err = resp
            if err:
                self._classified_errors.append(err)
            if items:
                results.extend(items)
                self._request_counts[items[0].engine] += 1
                # 记录引擎成功率，供动态降级使用
                self.cache.record_engine_result(items[0].engine, success=True)
            elif err and err.category.value == "engine":
                # 解析失败：记录为失败
                engine_name = getattr(err, "engine", None)
                if engine_name:
                    self.cache.record_engine_result(engine_name, success=False)
        return results

    async def _strict_fallback(
        self,
        query: str,
        num: int,
        ctx: RequestContext,
        search_cfg: Dict[str, Any],
    ) -> List[SearchResult]:
        """
        strict 模式兜底

        默认不启用。strict 用户的核心预期是「宁可没有结果，也不把查询词
        发给隐私保护不足的引擎」，因此静默降级属于违背预期的危险默认值。
        仅当用户在配置中显式打开 privacy.strict.allow_fallback，
        或使用 --allow-fallback 参数时，才允许降级到国内引擎。
        """
        strict_cfg = (self.config.get("privacy", {}) or {}).get("strict", {}) or {}
        allowed = self.allow_fallback or bool(strict_cfg.get("allow_fallback", False))
        if not allowed:
            self._notices.append(
                "strict 模式下隐私引擎均不可用，已停止搜索以避免查询词外泄；"
                "如确需降级到国内引擎，请加 --allow-fallback 或在配置中开启 "
                "privacy.strict.allow_fallback"
            )
            self.logger.warning("strict_fallback_refused reason=privacy_first")
            return []

        # 动态降级：按成功率排序候选引擎（排除已失败的隐私引擎），
        # 不再写死 bing→baidu，而是优先选历史成功率最高的
        fallback_names = strict_cfg.get("fallback_engines", ["bing", "baidu"])
        # 按成功率排序，但跳过已知被限流的引擎
        candidates = [
            name for name in self.cache.rank_engines_by_success(fallback_names)
            if self._check_rate_limit(name)
        ]

        for name in candidates:
            adapter = self.engine_manager.get_adapter(name)
            if not adapter:
                continue
            try:
                connector = build_connector(1)
                async with aiohttp.ClientSession(connector=connector) as session:
                    resp = await adapter.search(session, query, num, ctx)
                    if resp.results:
                        self._notices.append(
                            f"隐私引擎均不可用，已改用 {name} 返回结果；"
                            f"该引擎隐私保护较弱，建议检查网络或配置代理后重试"
                        )
                        self._request_counts[name] += 1
                        self.cache.record_engine_result(name, success=True)
                        return resp.results
                    else:
                        self.cache.record_engine_result(name, success=False)
            except Exception:  # noqa: BLE001 - 兜底失败不应影响主流程
                self.cache.record_engine_result(name, success=False)
                continue
        return []

    async def _search_one(
        self,
        adapter: EngineAdapter,
        session: aiohttp.ClientSession,
        query: str,
        num: int,
        ctx: RequestContext,
        delay: float,
    ) -> Tuple[List[SearchResult], Optional[ClassifiedError]]:
        """执行单引擎搜索并归类错误"""
        if delay > 0:
            await asyncio.sleep(delay)
        try:
            resp = await asyncio.wait_for(
                adapter.search(session, query, num, ctx),
                timeout=adapter.timeout + ctx.timeout,
            )
            if resp.results:
                # 结果偏少或页面带拦截特征时给出提示。
                # 这里不作为错误上报——结果毕竟拿到了，
                # 当作错误会让整体搜索显得失败，与事实不符。
                if resp.diagnosis in (ParseDiagnosis.PARTIAL, ParseDiagnosis.BLOCKED):
                    self._notices.append(
                        "%s 返回 %d 条（期望 %d 条）：%s"
                        % (adapter.name, len(resp.results), num,
                           diagnosis_hint(resp.diagnosis))
                    )
                return (resp.results, None)

            # 无结果：确认为空则不算错误，其余按引擎问题上报
            if resp.diagnosis == ParseDiagnosis.EMPTY_CONFIRMED:
                return ([], None)

            message = resp.error or diagnosis_hint(resp.diagnosis or "")
            err = classify_error(adapter.name, Exception(message or "未返回结果"))
            return ([], err)
        except asyncio.TimeoutError:
            return ([], classify_error(
                adapter.name, TimeoutError(f"请求超过 {adapter.timeout}s 未完成")
            ))
        except Exception as e:  # noqa: BLE001
            return ([], classify_error(adapter.name, e))

    # ---------- 引擎自检（F1-2） ----------

    async def selftest(self, query: str = "test", num: int = 3) -> List[Dict[str, Any]]:
        """
        逐个引擎体检，报告连通性与解析健康度

        用于在引擎改版导致解析失效时快速定位问题引擎。
        """
        ctx = self.privacy_manager.build_request_context(timeout=15, retry_max=0)
        report: List[Dict[str, Any]] = []

        names = [e for e in all_engine_names() if e != "searxng" or self.searxng_enabled]
        connector = build_connector(3)

        async with aiohttp.ClientSession(connector=connector) as session:
            for name in names:
                adapter = self.engine_manager.get_adapter(name)
                if not adapter:
                    continue
                start = time.time()
                try:
                    resp = await adapter.search(session, query, num, ctx)
                    report.append({
                        "engine": name,
                        "ok": bool(resp.results),
                        "count": len(resp.results),
                        "elapsed": round(time.time() - start, 2),
                        "diagnosis": resp.diagnosis or "unknown",
                        "hint": "" if resp.results else diagnosis_hint(resp.diagnosis or ""),
                    })
                except Exception as e:  # noqa: BLE001
                    report.append({
                        "engine": name,
                        "ok": False,
                        "count": 0,
                        "elapsed": round(time.time() - start, 2),
                        "diagnosis": "unknown",
                        "hint": str(e)[:80],
                    })
        return report


# ============================================================
# 输出格式化
# ============================================================

def format_error_report(errors: List[ClassifiedError]) -> str:
    """格式化错误诊断报告，按类别归组"""
    if not errors:
        return ""

    report: List[str] = []
    by_category: Dict[str, List[ClassifiedError]] = defaultdict(list)
    for e in errors:
        by_category[e.category.value].append(e)

    titles = {
        "network": "网络问题：",
        "config": "配置问题：",
        "engine": "引擎问题：",
    }

    for category, errs in by_category.items():
        report.append(titles.get(category, "其它问题："))
        for e in errs:
            report.append(f"  - {e.engine}: {e.message}")
            for ts in e.troubleshooting[:2]:
                report.append(f"    {ts}")

    return "\n".join(report)


def format_privacy_summary(manager: PrivacyManager) -> str:
    """
    格式化隐私保护摘要

    此前 PrivacyReport 已定义但未在搜索流程中输出，用户无法感知实际生效的保护措施。
    """
    report = manager.generate_report()
    lines = [f"隐私模式: {report.mode}"]
    if report.blocked_engines:
        lines.append(f"已屏蔽引擎: {', '.join(report.blocked_engines)}")
    if report.http_headers_cleaned:
        lines.append(f"已清理请求头: {', '.join(report.http_headers_cleaned)}")
    for rec in report.recommendations:
        lines.append(f"  · {rec}")
    return "\n".join(lines)


# ============================================================
# CLI 入口
# ============================================================

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    加载配置文件

    查找顺序：显式路径 → skill 根目录 config.yaml → 模板文件
    """
    import os as _os

    candidates: List[str] = []
    if config_path:
        candidates.append(config_path)
    else:
        here = _os.path.dirname(_os.path.abspath(__file__))
        root = _os.path.dirname(here)
        candidates.append(_os.path.join(root, "config.yaml"))
        candidates.append(_os.path.join(root, "references", "config.yaml.example"))

    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return yaml.safe_load(f) or {}
        except (FileNotFoundError, IsADirectoryError):
            continue
        except yaml.YAMLError as e:
            print(f"配置文件解析失败（{path}）：{e}")
            return {}
    return {}


def _print_results(results: List[SearchResult], args, orchestrator: SearchOrchestrator) -> None:
    """打印搜索结果"""
    source = "缓存" if orchestrator.cache_hit else "实时"
    print(f"\n搜索: {args.query} | 模式: {args.privacy} | 来源: {source} | 结果: {len(results)} 条\n")
    for idx, r in enumerate(results, 1):
        print(f"[{idx}] {r.title}")
        print(f"    {r.url}")
        if r.snippet:
            print(f"    {r.snippet[:100]}")
        # V1.9 新增：引擎数可信度标记（多引擎交叉即可信度信号）
        sources = r.engine_set
        label = ", ".join(sources) if sources else r.engine
        engine_count = len(sources) if sources else 1
        total_engines = len(orchestrator.last_engines_used) if hasattr(orchestrator, 'last_engines_used') else 10
        trust_badge = f"🔍 {engine_count}/{total_engines} 引擎返回"
        if engine_count >= 3:
            trust_badge += " ✅ 高可信"
        elif engine_count >= 2:
            trust_badge += " ⚡ 较可信"
        print(f"    — {label} | {trust_badge}" + (f" | 得分 {r.score}" if args.verbose else ""))
        print()


def main():
    """CLI 入口"""
    import argparse
    import json as _json

    parser = argparse.ArgumentParser(
        description=f"隐私搜索 v{get_current_version()} - 多引擎并行搜索",
    )
    parser.add_argument("query", nargs="?", default="", help="搜索关键词")
    parser.add_argument("--engines", help="指定引擎，逗号分隔；留空按隐私模式自动选择")
    parser.add_argument("--num", type=int, default=None, help="每个引擎返回结果数，默认读取配置")
    parser.add_argument("--privacy", choices=["normal", "strict"], default="normal", help="隐私模式")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细过程与错误信息")
    parser.add_argument("--no-cache", action="store_true", help="跳过缓存，强制重新搜索")
    parser.add_argument("--clear-cache", action="store_true", help="清空搜索结果缓存")
    parser.add_argument("--history", type=int, nargs="?", const=20, help="查看最近搜索历史")
    parser.add_argument("--clear-history", action="store_true", help="清空搜索历史")
    parser.add_argument("--cache-stats", action="store_true", help="查看缓存占用情况")
    parser.add_argument("--selftest", action="store_true", help="体检各引擎连通性与解析健康度")
    parser.add_argument("--list-engines", action="store_true", help="列出全部可用引擎")
    parser.add_argument("--privacy-report", action="store_true",
                        help="显示隐私保护摘要，可单独使用或与搜索同时使用")
    parser.add_argument(
        "--allow-fallback", action="store_true",
        help="strict 引擎全部失败时，允许降级到国内引擎（默认拒绝以保护隐私）",
    )
    parser.add_argument(
        "--fetch", type=int, metavar="N", default=0,
        help="抓取 Top-N 结果的网页正文（V1.5 新增）",
    )
    parser.add_argument(
        "--export", metavar="PATH",
        help="导出搜索结果到文件（支持 .md / .html / .pdf，V1.5 新增）",
    )
    parser.add_argument(
        "--summarize", action="store_true",
        help="对搜索结果生成摘要（V1.5 新增，需配置 llm_summary.api_key）",
    )
    parser.add_argument(
        "--vertical", choices=["news", "realtime", "academic", "image"],
        help="垂直搜索模式（V1.8 新增）：news=新闻, realtime=实时, academic=学术, image=图片",
    )
    parser.add_argument(
        "--fact-check", action="store_true",
        help="合成答案事实核查（V1.8 新增，逐论断回链原文做相似度比对）",
    )
    parser.add_argument(
        "--selftest-schedule", choices=["run", "status"],
        help="定时 selftest 调度（V1.6 新增）：run=执行一次, status=查看上次结果",
    )

    args = parser.parse_args()
    config = load_config(args.config)

    # ---- 不需要查询词的管理型命令 ----

    if args.list_engines:
        print(format_engine_table())
        return

    orchestrator = SearchOrchestrator(config)
    orchestrator.allow_fallback = bool(args.allow_fallback)

    # 启动时检查更新（24h 缓存期内瞬间返回，不阻塞搜索）
    _run_startup_update_check(config)

    if args.clear_cache:
        ok = orchestrator.cache.clear()
        print("缓存已清空" if ok else "缓存不可用或清空失败")
        return

    if args.clear_history:
        ok = orchestrator.cache.clear_history()
        print("搜索历史已清空" if ok else "历史不可用或清空失败")
        return

    if args.cache_stats:
        st = orchestrator.cache.stats()
        print(f"缓存条目: {st.entries}")
        print(f"占用空间: {st.size_mb} MB / 上限 {orchestrator.cache.max_size_mb} MB")
        print(f"历史记录: {st.history_count} 条")
        return

    if args.history is not None:
        rows = orchestrator.cache.get_history(args.history)
        if not rows:
            print("暂无搜索历史")
            return
        print(f"最近 {len(rows)} 条搜索记录：\n")
        for r in rows:
            print(f"  {r['time']}  [{r['privacy']}]  {r['query']}")
            print(f"      引擎: {r['engines']} | 结果 {r['result_count']} 条 | 耗时 {r['elapsed']}s")
        return

    if args.selftest:
        print("正在体检各引擎，请稍候...\n")
        report = asyncio.run(orchestrator.selftest())
        ok_count = sum(1 for r in report if r["ok"])
        print(f"{'引擎':<12}{'状态':<8}{'条数':<6}{'耗时':<8}诊断")
        print("-" * 62)
        for r in report:
            status = "正常" if r["ok"] else "异常"
            print(f"{r['engine']:<12}{status:<8}{r['count']:<6}{r['elapsed']:<8}{r['diagnosis']}")
            if r["hint"]:
                print(f"{'':<12}{r['hint']}")
        print(f"\n可用引擎 {ok_count}/{len(report)}")
        print(f"中文分词(jieba): {'可用' if jieba_available() else '不可用，已降级为字符切分'}")
        return

    # --- V1.6 新增：定时 selftest 调度 ---
    if args.selftest_schedule:
        try:
            from selftest_scheduler import SelftestScheduler
        except ImportError:
            from .selftest_scheduler import SelftestScheduler
        scheduler = SelftestScheduler(config)
        if args.selftest_schedule == "run":
            result = scheduler.run_once()
            if not result.get("enabled"):
                print("selftest 调度已禁用")
                return
            print(f"selftest 完成: {result['ok_count']}/{result['total']} 引擎正常")
            if result["failed"]:
                print(f"失效引擎: {', '.join(result['failed'])}")
            else:
                print("所有引擎正常")
        else:  # status
            log_path = os.path.expanduser("~/.workbuddy/output/privacy-search-selftest.log")
            if not os.path.exists(log_path):
                print("尚未执行过 selftest")
                return
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[-20:]:
                print(line.rstrip())
        return

    if not args.query:
        # 隐私报告属于信息查询，不带关键词时单独展示即可，
        # 强制要求先搜索一次才能查看隐私配置并不合理
        if args.privacy_report:
            print(format_privacy_summary(orchestrator.privacy_manager))
            return
        parser.error(
            "需要提供搜索关键词，或使用 "
            "--history / --selftest / --list-engines / --privacy-report 等命令")

    # ---- 执行搜索 ----

    # V1.8 新增：解析高级检索语法
    try:
        from query_parser import parse_query, get_unsupported_syntax, filter_results_locally
    except ImportError:
        from .query_parser import parse_query, get_unsupported_syntax, filter_results_locally

    clean_query, syntax_filter = parse_query(args.query)
    if syntax_filter.has_filters:
        # 提示不支持的语法
        engines_hint = [e.strip() for e in (args.engines or "").split(",")] if args.engines else None
        if engines_hint:
            for eng in engines_hint:
                unsupported = get_unsupported_syntax(eng, syntax_filter)
                if unsupported:
                    print(f"提示: {eng} 不支持 {','.join(unsupported)}，将本地过滤")

    search_query = clean_query if clean_query else args.query

    # V1.8 新增：垂直搜索模式
    if args.vertical:
        from vertical_search import run_vertical_search, format_vertical_results, get_vertical_config
        vcfg = get_vertical_config(args.vertical)
        print(f"\n{'='*60}")
        print(f"{vcfg['display_name'] if vcfg else args.vertical} 搜索: {search_query}")
        print(f"{'='*60}")
        results = run_vertical_search(
            query=search_query,
            vertical_type=args.vertical,
            config=config,
            num=args.num,
            privacy_mode=args.privacy,
        )
        # 应用本地过滤
        if syntax_filter.has_filters:
            results, extra_notices = filter_results_locally(results, syntax_filter)
            for n in extra_notices:
                print(f"提示: {n}")
        print(format_vertical_results(results, args.vertical, search_query))
        for notice in orchestrator.notices:
            print(f"提示: {notice}")
        return

    engines = [e.strip() for e in args.engines.split(",")] if args.engines else None

    results = asyncio.run(orchestrator.search(
        query=search_query,
        engines=engines,
        num=args.num,
        privacy_mode=args.privacy,
        use_cache=not args.no_cache,
        verbose=args.verbose,
    ))

    # V1.8 新增：高级语法本地过滤
    if syntax_filter.has_filters:
        results, extra_notices = filter_results_locally(results, syntax_filter)
        for n in extra_notices:
            orchestrator._notices.append(n)

    for notice in orchestrator.notices:
        print(f"提示: {notice}")

    errors = orchestrator.classified_errors
    if errors and args.verbose:
        print("\n" + "=" * 60)
        print("错误诊断报告：")
        print(format_error_report(errors))
        print()

    if args.json:
        payload = {
            "query": args.query,
            "privacy_mode": args.privacy,
            "from_cache": orchestrator.cache_hit,
            "count": len(results),
            "total_engines": len(orchestrator.last_engines_used) if hasattr(orchestrator, 'last_engines_used') else 10,
            "results": [r.to_dict() for r in results],
            "notices": orchestrator.notices,
            "errors": [
                {"engine": e.engine, "category": e.category.value, "message": e.message}
                for e in errors
            ],
        }
        print(_json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        _print_results(results, args, orchestrator)

    # --- V1.5 新增：网页正文抓取 ---
    if args.fetch and results:
        print("\n正在抓取正文...")
        try:
            from page_fetcher import extract_text, fetch_page
            for i, r in enumerate(results[: args.fetch]):
                url = getattr(r, "url", "")
                if not url:
                    continue
                html = fetch_page(url)
                if html:
                    text = extract_text(html)
                    if text:
                        # 把正文附加到结果对象
                        setattr(r, "content", text[:2000])
                        print(f"  ✓ [{i+1}] {getattr(r, 'title', '')[:40]} ({len(text)} 字)")
                    else:
                        print(f"  ✗ [{i+1}] 无法提取正文")
                else:
                    print(f"  ✗ [{i+1}] 抓取失败")
        except Exception as e:
            print(f"  抓取过程出错: {e}")

    # --- V1.5 新增：结果导出 ---
    if args.export:
        try:
            from exporters import auto_export
            ok = auto_export(results, args.export, args.query)
            if ok:
                print(f"\n已导出到: {args.export}")
            else:
                print(f"\n导出失败: {args.export}")
        except Exception as e:
            print(f"\n导出过程出错: {e}")

    # --- V1.5 新增：摘要生成 ---
    if args.summarize:
        try:
            from summarizer import summarize
            print("\n正在生成摘要...")
            summary = summarize(args.query, results, config)
            print("\n" + "=" * 60)
            print("摘要:")
            print(summary)
            print("=" * 60)
        except Exception as e:
            print(f"\n摘要生成出错: {e}")

    # --- V1.6 新增：Perplexity 式答案合成 ---
    if args.synthesize_pro:
        try:
            from synthesiser import synthesize_pro
            print("\n正在抓取正文并生成答案（Pro 模式）...")
            answer = synthesize_pro(search_query, results, config)
            print("\n" + "=" * 60)
            print("答案（Pro 模式）:")
            print(answer)
            print("=" * 60)
        except Exception as e:
            print(f"\nPro 合成出错: {e}")

    if args.privacy_report:
        print("=" * 60)
        print(format_privacy_summary(orchestrator.privacy_manager))
        print()

    # V1.9 优化：口语化错误建议（非堆栈、可操作）
    if not results and errors and not args.verbose:
        categories = {e.category.value for e in errors}
        if "network" in categories:
            print("\n💡 网络连接失败，看起来是网络问题。")
            print("   试试这些：")
            print("   • 检查网络：ping www.baidu.com")
            print("   • 确认代理设置：config.yaml 中 search.proxy")
            print("   • 加 --verbose 查看具体错误")
        elif "config" in categories:
            print("\n💡 配置有问题，config.yaml 没读对。")
            print("   试试这些：")
            print("   • 确认 YAML 格式（冒号后面要有空格）")
            print("   • 复制 references/config.yaml.example 重新配置")
            print("   • 加 --verbose 查看具体错误")
        else:
            print("\n💡 搜索引擎解析失败，引擎可能改版了。")
            print("   试试这些：")
            print("   • 运行 --selftest 体检各引擎状态")
            print("   • 更新到最新版本")
            print("   • 用 --engines 排除问题引擎")


def _run_startup_update_check(config: Dict[str, Any]) -> None:
    """
    启动时检查更新（异步、非阻塞主流程）

    config.yaml 中 update_check 段控制是否启用。
    24h 缓存期内从缓存读取，瞬间返回；仅首次真查，最多慢 5 秒。
    """
    update_cfg = config.get("update_check", {}) or {}
    if not update_cfg.get("enabled", True) or not update_cfg.get("check_on_startup", True):
        return
    try:
        from update_checker import UpdateChecker, display_update_notification
        checker = UpdateChecker(config)
        update_info = asyncio.run(checker.check())
        if update_info and update_info.has_update:
            display_update_notification(update_info)
    except Exception:  # noqa: BLE001 - 更新检查失败不干扰搜索
        pass


if __name__ == "__main__":
    main()
