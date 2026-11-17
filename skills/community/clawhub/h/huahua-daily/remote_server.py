"""Authenticated Streamable HTTP wrapper for hosted HuahuaDaily MCP."""

import asyncio
import hashlib
import os
import re
import time
from pathlib import Path

import httpx
import uvicorn
from mcp.server.transport_security import TransportSecuritySettings

from huahua_mcp_runtime.client import (
    OFFICIAL_API,
    bind_request_token,
    get_client,
    reset_request_token,
)
from huahua_mcp_runtime.tool_registry import TOOL_SPEC_BY_NAME
from server import mcp


_ROOT = Path(__file__).resolve().parent
_REFERENCE_DIR = _ROOT / "references"
_SKILL_TOPICS = {
    "router": (_ROOT / "SKILL.md",),
    **{
        path.stem: (path,)
        for path in sorted(_REFERENCE_DIR.glob("*.md"))
    },
}
_AUTH_CACHE_TTL = 300
_AUTH_FAILURE_TTL = 30
_AUTH_CACHE_LIMIT = 1000
_AUTH_VALIDATE_CONCURRENCY = 8
_AUTH_VALIDATE_WAIT_SECONDS = 2
_auth_cache: dict[str, tuple[bool, float]] = {}
_auth_cache_lock = asyncio.Lock()
_auth_validation_semaphore = asyncio.Semaphore(_AUTH_VALIDATE_CONCURRENCY)


def _load_skill_context(topic: str = "router") -> str:
    normalized_topic = str(topic or "router").strip().lower()
    if normalized_topic == "full":
        files = [path for paths in _SKILL_TOPICS.values() for path in paths]
    else:
        files = list(_SKILL_TOPICS.get(normalized_topic, ()))
    if not files:
        available = ", ".join([*_SKILL_TOPICS, "full"])
        raise ValueError(f"未知 Skill 主题：{normalized_topic}；可选：{available}")
    available = ", ".join([*_SKILL_TOPICS, "full"])
    content = "\n\n".join(
        f"# {path.relative_to(_ROOT)}\n\n{path.read_text(encoding='utf-8')}"
        for path in files
    )
    return f"可按需加载的主题：{available}\n\n{content}"


@mcp.prompt(
    name="huahua_daily_expert",
    description="加载花花日记完整 Skill 与全部领域参考说明。",
)
def huahua_daily_expert() -> str:
    """Return the complete hosted Skill context for clients supporting MCP Prompts."""
    return _load_skill_context("full")


@mcp.tool(
    name="get_skill_context",
    description=(
        "按需读取一个花花日记 Skill 主题。普通查询直接使用业务工具，无需预加载；"
        "复杂任务仅加载相关主题：router、portfolio、fund-market、date-safety、"
        "quant、trade-import、community-reports、cli-artifacts。仅在用户明确要求时使用 full。"
    ),
)
def get_skill_context(topic: str = "router") -> str:
    """Return one requested Skill topic through the Tools capability."""
    return _load_skill_context(topic)


# Remote callers authenticate per request, so the local process-wide setter is
# intentionally unavailable on this surface.
mcp.remove_tool("set_token")

_REMOTE_TOOL_DESCRIPTIONS = {
    "get_summary": (
        "轻量查询总资产、今日收益、持有收益及完整度；只问组合汇总时使用。"
        "综合投资分析改用 get_quant_strategy_context(view='compact')。"
    ),
    "get_records": (
        "按需查询逐只持仓和观察列表，默认不返回交易明细。必须检查 freshness/complete；"
        "收益归属日只认 returnAttributionDate，缺失时不得回退到净值 D 日。"
        "综合投资分析优先使用 get_quant_strategy_context(view='compact')，避免再串行查询行情和量化工具。"
    ),
    "get_item_estimate": (
        "批量查询最多 50 只基金的当前估算。必须区分估算与官方净值，并检查 complete、"
        "evidenceComplete、staleCodes、timeoutCodes；收益 G 日只从 get_records 获取。"
    ),
    "get_fund_quant_metrics": (
        "按需查询单只基金 technical、momentum、risk 或 full 量化视图；不要无条件使用 full。"
        "必须检查 complete、historyFreshness 和 current.status；若 retryAfterMs 存在，按该间隔"
        "有界重取，最多 3 次，仍不完整则明确说明补数尚未完成。"
    ),
    "get_batch_fund_quant_metrics": (
        "批量查询基金量化视图；优先一次批量调用，不要逐只并发。technical/momentum/risk "
        "最多 50 只，full 最多 10 只。必须检查 complete、staleCodes、missingCodes、"
        "unverifiedCodes、refreshingCodes；若 retryAfterMs 存在，按该间隔有界重取，最多 3 次。"
    ),
    "get_batch_fund_nav_history": (
        "批量读取最多 20 只基金的官方 D 日净值数据库快照。freshnessMode="
        "unchecked_db_snapshot 表示未核验当前公布进度；complete 只代表所请求区间的边界覆盖，"
        "不得据此声称数据已更新到最新。当前量化分析应改用 get_batch_fund_quant_metrics。"
    ),
    "get_portfolio_nav_history": (
        "读取组合收益、净值与回撤。当前日期区间必须检查 complete 和 navFreshness；若其中"
        "retryAfterMs 存在，按该间隔有界重取，最多 3 次，仍不完整则禁止给出当前量化结论。"
    ),
    "get_night_estimate": (
        "查询最多 30 只 QDII 的物化夜盘估值；检查阶段、完整度、freshness 与 FX 状态，"
        "不得把夜盘日期或净值 D 日当作收益 G 日。"
    ),
    "get_quant_strategy_context": (
        "综合投资分析的首选单调用：一次返回持仓、市场、基金指标、执行窗口、数据质量与"
        "readyForAnalysis。默认 view='compact'；先检查 blockingReasons，只有缺少必要证据才用 full，"
        "不要再串行调用 get_records、get_overview 和逐基金量化工具重复取数。检查 dataQuality；"
        "若 fundOfficialNavFreshness.retryAfterMs 存在，按该间隔有界重取，最多 3 次。"
    ),
    "get_index_metrics": (
        "查询指数服务端量化指标。必须检查 historyFreshness、historyFreshnessBasis 与排名覆盖；"
        "新鲜度不可证明或历史过期时不得把指标描述为当前结论。"
    ),
    "get_sector_metrics": (
        "查询行业/主题 ETF 代理量化指标。必须检查报价与历史新鲜度及 historyFreshnessBasis；"
        "ETF 只代表板块代理，不代表底层指数或成分股完整覆盖。"
    ),
}


def _first_description_paragraph(description: str) -> str:
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", description or "")
        if paragraph.strip()
    ]
    return paragraphs[0] if paragraphs else ""


for tool_name, tool in mcp._tool_manager._tools.items():
    if tool_name in _REMOTE_TOOL_DESCRIPTIONS:
        tool.description = _REMOTE_TOOL_DESCRIPTIONS[tool_name]
        continue
    spec = TOOL_SPEC_BY_NAME.get(tool_name)
    if spec is not None and "state_change" not in spec.effects:
        tool.description = _first_description_paragraph(tool.description or "")

mcp._mcp_server.instructions = (
    "优先根据工具名称、描述和参数直接调用。综合投资分析首选 "
    "get_quant_strategy_context(view='compact') 一次取齐，不要重复串行取数。复杂任务才调用 "
    "get_skill_context 按需加载一个主题；不要预加载 full，也不要假设客户端自动注入 Prompt。"
    "凡用户问当前、最新、刚刷新、刚修改或是否已生效，必须在当前轮重新调用相应工具，"
    "不得复用更早轮次的结果。响应含 retryAfterMs 且仍 incomplete/stale/computing 时，"
    "按该间隔有界重取，最多 3 次；仍未完成则如实说明。"
)


def _bearer_token(headers: list[tuple[bytes, bytes]]) -> str | None:
    authorization = next(
        (value.decode("latin-1") for key, value in headers if key.lower() == b"authorization"),
        "",
    )
    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1].strip()
    if not token or len(token) > 4096:
        return None
    if any(ord(character) < 32 or ord(character) == 127 for character in token):
        return None
    return token


async def _validate_agent_token(token: str) -> bool | None:
    """Validate remotely while caching only a one-way token fingerprint."""
    fingerprint = hashlib.sha256(token.encode()).hexdigest()
    now = time.monotonic()
    async with _auth_cache_lock:
        cached = _auth_cache.get(fingerprint)
        if cached and now < cached[1]:
            return cached[0]
    try:
        await asyncio.wait_for(
            _auth_validation_semaphore.acquire(),
            timeout=_AUTH_VALIDATE_WAIT_SECONDS,
        )
    except TimeoutError:
        return None
    try:
        try:
            response = await get_client().get(
                f"{OFFICIAL_API}/api/auth/agent-token/validate",
                headers={"Authorization": f"AgentToken {token}"},
            )
        except httpx.RequestError:
            return None
    finally:
        _auth_validation_semaphore.release()
    if response.status_code not in {204, 401, 403}:
        return None
    valid = response.status_code == 204
    ttl = _AUTH_CACHE_TTL if valid else _AUTH_FAILURE_TTL
    async with _auth_cache_lock:
        if len(_auth_cache) >= _AUTH_CACHE_LIMIT:
            expired = [key for key, entry in _auth_cache.items() if now >= entry[1]]
            for key in expired:
                _auth_cache.pop(key, None)
            if len(_auth_cache) >= _AUTH_CACHE_LIMIT:
                _auth_cache.clear()
        _auth_cache[fingerprint] = (valid, now + ttl)
    return valid


class BearerAuthApp:
    """Protect the MCP endpoint while leaving a data-free health check public."""

    def __init__(self, inner_app):
        self.inner_app = inner_app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope.get("path") == "/healthz":
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b"ok"})
            return
        if scope["type"] == "http":
            token = _bearer_token(scope.get("headers", []))
            if token is None:
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [(b"www-authenticate", b"Bearer")],
                })
                await send({"type": "http.response.body", "body": b"Unauthorized"})
                return
            valid = await _validate_agent_token(token)
            if valid is not True:
                status = 401 if valid is False else 503
                body = b"Unauthorized" if valid is False else b"Authentication unavailable"
                await send({"type": "http.response.start", "status": status, "headers": []})
                await send({"type": "http.response.body", "body": body})
                return
            context_token = bind_request_token(token)
            try:
                await self.inner_app(scope, receive, send)
            finally:
                reset_request_token(context_token)
            return
        await self.inner_app(scope, receive, send)


public_hosts = [
    host.strip()
    for host in os.environ.get(
        "HUAHUA_MCP_PUBLIC_HOSTS",
        "huahua-mcp.preview.aliyun-zeabur.cn,mcp.huahuadaily.cn",
    ).split(",")
    if host.strip()
]
mcp.settings.stateless_http = True
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=public_hosts,
    allowed_origins=[f"https://{host}" for host in public_hosts],
)
app = BearerAuthApp(mcp.streamable_http_app())


if __name__ == "__main__":
    # Container ingress requires binding all interfaces.
    container_bind_host = "0.0.0.0"  # nosec B104
    uvicorn.run(app, host=container_bind_host, port=int(os.environ.get("PORT", "8000")))
