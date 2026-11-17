"""Session state, shared caches, and HTTP transport for the MCP facade."""

import asyncio
import hashlib
import os
import threading
from contextvars import ContextVar, Token
from typing import Optional

import httpx

OFFICIAL_API = os.environ.get("HUAHUA_API_BASE", "https://api.huahuadaily.cn").strip().rstrip("/")

session: dict = {
    "token": os.environ.get("HUAHUA_AGENT_TOKEN", "").strip(),
    "base_url": OFFICIAL_API,
    "generation": 0,
}
request_token: ContextVar[Optional[str]] = ContextVar(
    "huahua_mcp_request_token",
    default=None,
)

http_client: Optional[httpx.AsyncClient] = None
http_client_lock = threading.Lock()

portfolio_cache: dict = {"data": None, "ts": 0.0, "generation": -1}
PORTFOLIO_TTL = 30
download_lock: Optional[asyncio.Lock] = None
download_lock_loop: Optional[asyncio.AbstractEventLoop] = None


def get_client() -> httpx.AsyncClient:
    global http_client
    with http_client_lock:
        is_closed = bool(getattr(http_client, "is_closed", False)) if http_client is not None else True
        if http_client is None or is_closed:
            http_client = httpx.AsyncClient(
                timeout=30,
                limits=httpx.Limits(
                    max_connections=20,
                    max_keepalive_connections=10,
                    keepalive_expiry=30,
                ),
            )
    return http_client


def get_download_lock() -> asyncio.Lock:
    global download_lock, download_lock_loop
    loop = asyncio.get_running_loop()
    if download_lock is None or download_lock_loop is not loop:
        download_lock = asyncio.Lock()
        download_lock_loop = loop
    return download_lock


def clear_session_caches() -> None:
    """Clear data tied to the current token/base URL."""
    session["generation"] = int(session.get("generation") or 0) + 1
    portfolio_cache["data"] = None
    portfolio_cache["ts"] = 0.0
    portfolio_cache["generation"] = -1


def bind_request_token(token: str) -> Token:
    """Bind one remote Bearer token to the current async request context."""
    return request_token.set(token)


def reset_request_token(context_token: Token) -> None:
    request_token.reset(context_token)


def active_token() -> str:
    return (request_token.get() or session["token"]).strip()


def request_generation() -> int:
    """Return an opaque cache generation without retaining the remote token."""
    remote_token = request_token.get()
    if remote_token:
        digest = hashlib.sha256(remote_token.encode()).digest()
        return int.from_bytes(digest, "big")
    return int(session.get("generation") or 0)


def require_token() -> None:
    if not active_token():
        raise ValueError(
            "未配置 Agent Token。请在 MCP server env 中设置 HUAHUA_AGENT_TOKEN"
            "，或调用 set_token 工具。"
            "Agent Token 需在 App 设置页 →「Agent 访问令牌」中生成（PRO 会员专属）。"
        )


def headers() -> dict:
    token = active_token()
    return {"Authorization": f"AgentToken {token}"} if token else {}


def request_context() -> tuple[dict, int]:
    """Capture auth headers and the session generation as one request context."""
    return headers(), request_generation()


def assert_session_generation(generation: int) -> None:
    if request_generation() != generation:
        raise RuntimeError("Agent Token 已在请求期间变更，请重试")


def url(path: str) -> str:
    return f"{session['base_url']}{path}"


def _raise_auth_error(response: httpx.Response) -> None:
    if response.status_code == 401:
        raise ValueError("Agent Token 无效或已过期，请在 App 重新生成并更新配置。")
    if response.status_code == 403:
        if response.request.url.path == "/api/quant/strategy-context":
            raise ValueError(
                "无权读取量化策略上下文：请确认账号为 PRO 会员，"
                "且 Agent Token 包含 quant:read scope。"
            )
        if response.request.url.path == "/api/agent/messages":
            raise ValueError(
                "无权写入个人报告：请确认账号为 PRO 会员，且 Agent Token 有效。"
            )
        raise ValueError("无访问权限，请确认 Agent Token 正确，且账号为 PRO 会员。")


def _safe_response_detail(response: httpx.Response) -> str:
    """Return an intentional API validation message without leaking arbitrary bodies."""
    try:
        payload = response.json()
    except ValueError:
        return ""
    detail = payload.get("detail") if isinstance(payload, dict) else None
    if isinstance(detail, str):
        return " ".join(detail.split())[:500]
    if isinstance(detail, list):
        messages = []
        for item in detail[:5]:
            if not isinstance(item, dict) or not isinstance(item.get("msg"), str):
                continue
            location = item.get("loc")
            prefix = ".".join(str(part) for part in location) if isinstance(location, list) else ""
            message = " ".join(item["msg"].split())
            messages.append(f"{prefix}: {message}" if prefix else message)
        return "；".join(messages)[:500]
    return ""


def _translate_transport_error(error: Exception) -> None:
    if isinstance(error, httpx.TimeoutException):
        raise RuntimeError("请求超时，请稍后重试。") from error
    if isinstance(error, httpx.HTTPStatusError):
        status_code = error.response.status_code
        request = error.response.request
        safe_validation_routes = {
            ("POST", "/api/agent/request"),
            ("POST", "/api/agent/import-reviews"),
            ("POST", "/api/quant/snapshots"),
            ("GET", "/api/quant/strategy-context"),
            ("GET", "/api/market/index-metrics"),
            ("GET", "/api/market/indices/latest"),
            ("GET", "/api/market/indices/timeline"),
            ("GET", "/api/market/indices/history"),
            ("POST", "/api/fund/profile/batch"),
        }
        detail = _safe_response_detail(error.response) if (
            (request.method, request.url.path) in safe_validation_routes
            and status_code in {400, 409, 413, 422}
        ) else ""
        if detail:
            raise RuntimeError(f"服务器返回错误 {status_code}：{detail}") from error
        raise RuntimeError(f"服务器返回错误 {status_code}，请稍后重试。") from error
    if isinstance(error, httpx.RequestError):
        raise RuntimeError("无法连接花花日记后端，请检查网络和 API 地址。") from error
    raise error


def _decode_json(response: httpx.Response) -> dict | list:
    try:
        return response.json()
    except ValueError:
        raise RuntimeError("服务器返回了无法解析的响应，请稍后重试。") from None


async def get(path: str, params: dict = None) -> dict:
    request_headers, generation = request_context()
    try:
        response = await get_client().get(url(path), params=params, headers=request_headers)
        assert_session_generation(generation)
        _raise_auth_error(response)
        response.raise_for_status()
    except ValueError:
        raise
    except (httpx.RequestError, httpx.HTTPStatusError) as error:
        _translate_transport_error(error)
    return _decode_json(response)


async def get_optional(path: str, params: dict = None) -> Optional[dict]:
    request_headers, generation = request_context()
    try:
        response = await get_client().get(url(path), params=params, headers=request_headers)
        assert_session_generation(generation)
        _raise_auth_error(response)
        if response.status_code == 404:
            return None
        response.raise_for_status()
    except ValueError:
        raise
    except (httpx.RequestError, httpx.HTTPStatusError) as error:
        _translate_transport_error(error)
    return _decode_json(response)


async def post(path: str, body: dict = None, params: dict = None) -> dict:
    request_headers, generation = request_context()
    try:
        response = await get_client().post(url(path), params=params, json=body or {}, headers=request_headers)
        assert_session_generation(generation)
        _raise_auth_error(response)
        response.raise_for_status()
    except ValueError:
        raise
    except (httpx.RequestError, httpx.HTTPStatusError) as error:
        _translate_transport_error(error)
    return _decode_json(response)


async def post_files(
    path: str,
    files: list[tuple[str, bytes, str]],
    form_data: Optional[dict] = None,
) -> dict | list:
    request_headers, generation = request_context()
    try:
        multipart = [("files", (filename, content, mime)) for filename, content, mime in files]
        response = await get_client().post(
            url(path),
            files=multipart,
            data=form_data or None,
            headers=request_headers,
            timeout=httpx.Timeout(120, connect=30),
        )
        assert_session_generation(generation)
        _raise_auth_error(response)
        response.raise_for_status()
    except ValueError:
        raise
    except (httpx.RequestError, httpx.HTTPStatusError) as error:
        _translate_transport_error(error)
    return _decode_json(response)


async def put(path: str, body: dict = None) -> dict:
    request_headers, generation = request_context()
    try:
        response = await get_client().put(url(path), json=body or {}, headers=request_headers)
        assert_session_generation(generation)
        _raise_auth_error(response)
        response.raise_for_status()
    except ValueError:
        raise
    except (httpx.RequestError, httpx.HTTPStatusError) as error:
        _translate_transport_error(error)
    return _decode_json(response)


async def delete(path: str) -> dict:
    request_headers, generation = request_context()
    try:
        response = await get_client().delete(url(path), headers=request_headers)
        assert_session_generation(generation)
        _raise_auth_error(response)
        response.raise_for_status()
    except ValueError:
        raise
    except (httpx.RequestError, httpx.HTTPStatusError) as error:
        _translate_transport_error(error)
    return _decode_json(response)
