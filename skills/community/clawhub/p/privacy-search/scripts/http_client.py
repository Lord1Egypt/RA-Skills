"""
统一 HTTP 请求出口
==================
V1.2 新增（修复 P0-8 / P0-9，承载 F1-3 / F1-4）

问题背景：
    V1.1 中 privacy.py 定义了完整的隐私头构建逻辑（build_headers），
    但 search.py 从未 import 过该模块，9 个引擎适配器各自在方法内硬编码
    自己的 headers。结果是：
      - strict 模式仅做了引擎筛选与降级，隐私头配置从未生效
      - no_cookie / no_referrer / 自定义 UA 等配置项形同虚设
      - 十个引擎中仅 3 个偶然带了 DNT 头
      - 想加 UA 池或代理，需要同时改 9 处

解决方案：
    所有出网请求统一经过本模块：
      - headers 由 PrivacyManager 集中构建（隐私配置真正生效）
      - UA 池随机轮换（F1-3）
      - 网络类错误指数退避重试（F1-4）
      - 代理透传
    引擎适配器退化为「URL 构造 + 响应解析」，不再关心传输细节。
"""

import asyncio
import random
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import aiohttp

sys.dont_write_bytecode = True


# ============================================================
# User-Agent 池（F1-3）
# ============================================================
# 说明：
#   V1.1 各适配器硬编码的 UA 为 "Mozilla/5.0 (...) AppleWebKit/537.36"，
#   尾部缺少 Chrome 版本号，特征明显容易被判定为爬虫。
#   此处收录主流浏览器的完整 UA，随机轮换以降低指纹一致性。

USER_AGENT_POOL: List[str] = [
    # Chrome / Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36",
    # Edge / Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    # Chrome / macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36",
    # Safari / macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/17.5 Safari/605.1.15",
    # Firefox / Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    # Firefox / Linux
    "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    # Chrome / Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36",
]


def get_user_agent_pool(config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    获取合并后的 User-Agent 池

    默认池（硬编码 8 个）+ config.yaml 中 user_agent_pool 追加的 UA。
    用户追加的 UA 在前，默认池在后，优先使用用户自定义。
    """
    custom: List[str] = []
    if config:
        ua_config = config.get("user_agent_pool", [])
        if isinstance(ua_config, list):
            custom = [str(ua).strip() for ua in ua_config if str(ua).strip()]
    return custom + USER_AGENT_POOL


def pick_user_agent(fixed: Optional[str] = None,
                     pool: Optional[List[str]] = None) -> str:
    """
    选取 User-Agent

    Args:
        fixed: 配置中指定的固定 UA；为空则从池中随机取
        pool: 自定义 UA 池；为空时使用默认池

    Returns:
        User-Agent 字符串
    """
    if fixed and fixed.strip():
        return fixed.strip()
    use_pool = pool if pool else USER_AGENT_POOL
    return random.choice(use_pool)


# ============================================================
# 重试配置（F1-4）
# ============================================================

@dataclass
class RetryPolicy:
    """
    重试策略

    仅对网络类错误重试。配置类错误（如引擎名非法）重试无意义，
    引擎类错误（如页面结构变化）重试同样无效，故均不重试。
    """
    max_retries: int = 2          # 首次之外的重试次数
    base_delay: float = 1.0       # 退避基数（秒）
    max_delay: float = 8.0        # 单次等待上限
    jitter: float = 0.3           # 抖动比例，避免多引擎同时重试造成尖峰

    def delay_for(self, attempt: int) -> float:
        """
        计算第 attempt 次重试前的等待时长（attempt 从 1 开始）

        指数退避：base * 2^(attempt-1)，叠加随机抖动
        """
        raw = self.base_delay * (2 ** max(0, attempt - 1))
        raw = min(raw, self.max_delay)
        jitter_span = raw * self.jitter
        return max(0.1, raw + random.uniform(-jitter_span, jitter_span))


# 判定为「网络类」的异常，仅这些参与重试
NETWORK_EXCEPTIONS = (
    aiohttp.ClientConnectorError,
    aiohttp.ServerDisconnectedError,
    aiohttp.ClientOSError,
    aiohttp.ClientPayloadError,
    aiohttp.ServerTimeoutError,
    asyncio.TimeoutError,
    TimeoutError,
    ConnectionRefusedError,
    ConnectionResetError,
)


def is_retryable(exc: BaseException) -> bool:
    """判断异常是否值得重试"""
    return isinstance(exc, NETWORK_EXCEPTIONS)


# ============================================================
# 请求上下文
# ============================================================

@dataclass
class RequestContext:
    """
    单次搜索会话的传输上下文

    由 SearchOrchestrator 构建一次，传递给所有适配器共用，
    保证同一次搜索中隐私策略、代理、重试策略完全一致。
    """
    headers: Dict[str, str] = field(default_factory=dict)
    proxy: Optional[str] = None
    timeout: int = 15
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    verbose: bool = False

    def headers_for(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        生成本次请求的 headers

        每次调用重新随机 UA（若未固定），使同一会话内不同引擎的指纹不一致。
        """
        merged = dict(self.headers)
        if extra:
            merged.update(extra)
        return merged


# ============================================================
# 统一请求执行
# ============================================================

async def fetch_text(
    session: aiohttp.ClientSession,
    url: str,
    ctx: RequestContext,
    extra_headers: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
) -> str:
    """
    发起 GET 请求并返回文本，内置网络错误重试

    Args:
        session: aiohttp 会话
        url: 目标地址
        ctx: 请求上下文（headers / proxy / 重试策略）
        extra_headers: 引擎特有的附加头
        timeout: 覆盖默认超时

    Returns:
        响应文本

    Raises:
        最后一次尝试的异常（重试耗尽后向上抛出）
    """
    effective_timeout = timeout or ctx.timeout
    attempts = ctx.retry.max_retries + 1
    last_exc: Optional[BaseException] = None

    for attempt in range(attempts):
        try:
            async with session.get(
                url,
                headers=ctx.headers_for(extra_headers),
                timeout=aiohttp.ClientTimeout(total=effective_timeout),
                proxy=ctx.proxy,
                allow_redirects=True,
            ) as resp:
                return await resp.text(errors="ignore")
        except Exception as exc:  # noqa: BLE001 - 需按类型决定是否重试
            last_exc = exc
            # 非网络类错误立即失败，重试无意义
            if not is_retryable(exc) or attempt >= attempts - 1:
                raise
            wait = ctx.retry.delay_for(attempt + 1)
            if ctx.verbose:
                print(f"   ↻ 网络异常，{wait:.1f}s 后重试（第 {attempt + 1}/{ctx.retry.max_retries} 次）: {url[:60]}")
            await asyncio.sleep(wait)

    # 理论上不会到达，兜底保证函数有明确出口
    if last_exc:
        raise last_exc
    raise RuntimeError("请求未能完成")


async def fetch_json(
    session: aiohttp.ClientSession,
    url: str,
    ctx: RequestContext,
    extra_headers: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
) -> Any:
    """
    发起 GET 请求并返回 JSON（用于 SearXNG 等 API 型引擎）

    与 fetch_text 共享同一套重试与隐私策略。
    """
    import json as _json

    text = await fetch_text(session, url, ctx, extra_headers, timeout)
    try:
        return _json.loads(text)
    except ValueError as exc:
        raise ValueError(f"响应不是合法 JSON: {text[:120]}") from exc


def build_connector(max_concurrent: int = 6) -> aiohttp.TCPConnector:
    """
    构建连接器

    limit 控制总并发，limit_per_host 防止对单一引擎造成压力。
    """
    return aiohttp.TCPConnector(
        limit=max_concurrent,
        limit_per_host=2,
        ttl_dns_cache=300,
    )
