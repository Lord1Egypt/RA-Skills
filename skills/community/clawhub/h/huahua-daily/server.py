"""
HuahuaDaily MCP Server (OpenClaw Skills)
=========================================
让 Codex、Claude Code、Claude Desktop、Cursor、Windsurf、OpenClaw 等
AI agent 通过 MCP 协议直接访问花花日记的数据与功能。

配置方式：
  在 Agent 的 MCP 配置中添加：
  {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_AGENT_TOKEN": "从 App 设置页生成并复制的 Agent 令牌"
      }
    }
  }

认证说明：
  所有工具均需 Agent Token（PRO 会员专属功能）。
  通过环境变量 HUAHUA_AGENT_TOKEN 配置（推荐），或运行时调用 set_token 工具。
  Agent Token 需在 App 设置页 → "Agent 访问令牌" 中生成（需邮箱验证，仅 PRO 会员可用）。
"""

import os
import json
import math
import asyncio
import time
import base64
import mimetypes
import re
import threading
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

# ── Session state ─────────────────────────────────────────────────────────────
_OFFICIAL_API = os.environ.get("HUAHUA_API_BASE", "https://api.huahuadaily.cn").strip().rstrip("/")

_session: dict = {
    "token": os.environ.get("HUAHUA_AGENT_TOKEN", "").strip(),
    "base_url": _OFFICIAL_API,
}

mcp = FastMCP("huahua-daily")

# ── 连接池（模块级，整个 MCP session 复用同一个 client，避免每次请求重建 TCP 连接）─────
_http_client: Optional[httpx.AsyncClient] = None
_http_client_lock = threading.Lock()

def _get_client() -> httpx.AsyncClient:
    global _http_client
    with _http_client_lock:
        is_closed = bool(getattr(_http_client, "is_closed", False)) if _http_client is not None else True
        if _http_client is None or is_closed:
            _http_client = httpx.AsyncClient(
                timeout=30,
                limits=httpx.Limits(
                    max_connections=20,
                    max_keepalive_connections=10,
                    keepalive_expiry=30,
                ),
            )
    return _http_client

# ── Portfolio 内存缓存（TTL=30s，避免 get_summary 重复下载）─────────────────────
_portfolio_cache: dict = {"data": None, "ts": 0.0}
_PORTFOLIO_TTL = 30  # seconds
_download_lock: Optional[asyncio.Lock] = None

def _get_download_lock() -> asyncio.Lock:
    global _download_lock
    if _download_lock is None:
        _download_lock = asyncio.Lock()
    return _download_lock

# ── Estimates 内存缓存（TTL=60s，避免同 session 内多工具调用重复拉取相同基金估算）──────
_estimate_cache: dict = {}  # {code: {"data": {...}, "ts": float}}
_ESTIMATE_TTL = 60  # seconds
_DATA_SOURCE_MODES = {"huahua", "a", "b", "c"}
# ── Validation helpers ────────────────────────────────────────────────────────

# 图片文件大小限制（10MB）
_MAX_IMAGE_SIZE = 10 * 1024 * 1024

# 允许的图片 MIME 类型
_ALLOWED_IMAGE_MIMES = {
    "image/jpeg", "image/png", "image/webp", "image/gif", "image/bmp",
}

_CONFIRMED_EMPTY_PORTFOLIO_KEYS = {
    "funds",
    "archivedLedger",
    "deletedFundsMeta",
    "dismissedDividendKeys",
    "userPreferences",
    "groups",
    "watchlistGroups",
    "globalTags",
    "tagDisplayCount",
    "fieldConfigs",
    "watchlistFieldConfigs",
    "nightWatchCodes",
    "purchaseLimitWatchItems",
    "purchaseLimitWatchNightDefaultsMigrated",
    "marketIndexSelection",
    "emptyPortfolioConfirmed",
    "clearedAt",
    "timestamp",
    "version",
}

def _clear_session_caches() -> None:
    """清理和当前 token/base_url 绑定的内存缓存，避免运行时切账号串数据。"""
    _portfolio_cache["data"] = None
    _portfolio_cache["ts"] = 0.0
    _estimate_cache.clear()


def _detect_image_mime(content: bytes) -> Optional[str]:
    if content[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    if content[:2] == b'\xff\xd8':
        return "image/jpeg"
    if content[:4] == b'RIFF' and content[8:12] == b'WEBP':
        return "image/webp"
    if content[:6] in (b'GIF87a', b'GIF89a'):
        return "image/gif"
    if content[:2] == b'BM':
        return "image/bmp"
    return None


def _validate_image_file(filepath: str, content: bytes, mime: str) -> str:
    """验证图片文件大小和格式。"""
    if len(content) > _MAX_IMAGE_SIZE:
        raise ValueError(f"图片文件过大：{len(content) / 1024 / 1024:.1f}MB，最大允许 10MB")
    detected_mime = _detect_image_mime(content)
    if not detected_mime:
        raise ValueError(f"不支持的图片格式：{mime or 'unknown'}，仅支持 JPEG/PNG/WebP/GIF/BMP")
    return detected_mime

def _validate_fund_code(code: str) -> str:
    """验证并规范化基金代码（6位数字）。"""
    normalized = str(code or "").strip()
    if not re.fullmatch(r'\d{6}', normalized):
        raise ValueError(f"基金代码必须是 6 位数字，收到：{code}")
    return normalized


def _normalize_data_source_mode(value) -> str:
    normalized = str(value or "huahua").strip().lower()
    return normalized if normalized in _DATA_SOURCE_MODES else "huahua"

def _validate_amount(amount: float) -> float:
    """验证交易金额。"""
    if not isinstance(amount, (int, float)):
        raise ValueError(f"金额必须是数字，收到：{amount}")
    if amount <= 0:
        raise ValueError(f"金额必须大于 0，收到：{amount}")
    if amount > 100_000_000:  # 1亿
        raise ValueError(f"金额过大：{amount}，请确认是否正确")
    # 使用 _r2 对齐前端精度（四舍五入），而非 Python round()（四舍五入到偶数）
    return _r2(amount)

def _validate_date(date_str: str) -> str:
    """验证日期格式（YYYY-MM-DD）。"""
    if not date_str:
        return ""
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date_str):
        raise ValueError(f"日期格式必须是 YYYY-MM-DD，收到：{date_str}")
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"无效的日期：{date_str}")
    return date_str


def _beijing_date_string() -> str:
    from datetime import datetime
    from zoneinfo import ZoneInfo
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")

# ── Helpers ───────────────────────────────────────────────────────────────────

def _require_token() -> None:
    """所有工具（除 set_token）均须调用此函数，确保 Agent Token 已配置。"""
    if not _session["token"]:
        raise ValueError(
            "未配置 Agent Token。请在 MCP server env 中设置 HUAHUA_AGENT_TOKEN"
            "，或调用 set_token 工具。"
            "Agent Token 需在 App 设置页 →「Agent 访问令牌」中生成（PRO 会员专属）。"
        )

def _headers() -> dict:
    """构建 Agent Token HTTP 请求头。"""
    tok = _session["token"]
    if not tok:
        return {}
    return {"Authorization": f"AgentToken {tok}"}

def _url(path: str) -> str:
    return f"{_session['base_url']}{path}"

async def _get(path: str, params: dict = None) -> dict:
    try:
        r = await _get_client().get(_url(path), params=params, headers=_headers())
        if r.status_code == 401:
            raise ValueError("Agent Token 无效或已过期，请在 App 重新生成并更新配置。")
        if r.status_code == 403:
            raise ValueError("无访问权限，请确认 Agent Token 正确，且账号为 PRO 会员。")
        r.raise_for_status()
        return r.json()
    except ValueError:
        raise
    except httpx.TimeoutException:
        raise RuntimeError("请求超时，请稍后重试。")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"服务器返回错误 {e.response.status_code}，请稍后重试。")

async def _get_optional(path: str, params: dict = None) -> Optional[dict]:
    """GET helper that returns None for 404 while preserving auth errors."""
    try:
        r = await _get_client().get(_url(path), params=params, headers=_headers())
        if r.status_code == 401:
            raise ValueError("Agent Token 无效或已过期，请在 App 重新生成并更新配置。")
        if r.status_code == 403:
            raise ValueError("无访问权限，请确认 Agent Token 正确，且账号为 PRO 会员。")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except ValueError:
        raise
    except httpx.TimeoutException:
        raise RuntimeError("请求超时，请稍后重试。")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"服务器返回错误 {e.response.status_code}，请稍后重试。")

async def _post(path: str, body: dict = None, params: dict = None) -> dict:
    try:
        r = await _get_client().post(_url(path), params=params, json=body or {}, headers=_headers())
        if r.status_code == 401:
            raise ValueError("Agent Token 无效或已过期，请在 App 重新生成并更新配置。")
        if r.status_code == 403:
            raise ValueError("无访问权限，请确认 Agent Token 正确，且账号为 PRO 会员。")
        r.raise_for_status()
        return r.json()
    except ValueError:
        raise
    except httpx.TimeoutException:
        raise RuntimeError("请求超时，请稍后重试。")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"服务器返回错误 {e.response.status_code}，请稍后重试。")


async def _post_files(
    path: str,
    files: list[tuple[str, bytes, str]],
    form_data: Optional[dict] = None,
) -> dict | list:
    try:
        multipart = [
            ("files", (filename, content, mime))
            for filename, content, mime in files
        ]
        upload_client = httpx.AsyncClient(timeout=httpx.Timeout(120, connect=30))
        async with upload_client:
            r = await upload_client.post(
                _url(path),
                files=multipart,
                data=form_data or None,
                headers=_headers(),
            )
        if r.status_code == 401:
            raise ValueError("Agent Token 无效或已过期，请在 App 重新生成并更新配置。")
        if r.status_code == 403:
            raise ValueError("无访问权限，请确认 Agent Token 正确，且账号为 PRO 会员。")
        r.raise_for_status()
        return r.json()
    except ValueError:
        raise
    except httpx.TimeoutException:
        raise RuntimeError("请求超时，请稍后重试。")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"服务器返回错误 {e.response.status_code}，请稍后重试。")

async def _put(path: str, body: dict = None) -> dict:
    try:
        r = await _get_client().put(_url(path), json=body or {}, headers=_headers())
        if r.status_code == 401:
            raise ValueError("Agent Token 无效或已过期，请在 App 重新生成并更新配置。")
        if r.status_code == 403:
            raise ValueError("无访问权限，请确认 Agent Token 正确，且账号为 PRO 会员。")
        r.raise_for_status()
        return r.json()
    except ValueError:
        raise
    except httpx.TimeoutException:
        raise RuntimeError("请求超时，请稍后重试。")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"服务器返回错误 {e.response.status_code}，请稍后重试。")


async def _delete(path: str) -> dict:
    try:
        r = await _get_client().delete(_url(path), headers=_headers())
        if r.status_code == 401:
            raise ValueError("Agent Token 无效或已过期，请在 App 重新生成并更新配置。")
        if r.status_code == 403:
            raise ValueError("无访问权限，请确认 Agent Token 正确，且账号为 PRO 会员。")
        r.raise_for_status()
        return r.json()
    except ValueError:
        raise
    except httpx.TimeoutException:
        raise RuntimeError("请求超时，请稍后重试。")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"服务器返回错误 {e.response.status_code}，请稍后重试。")


def _parse_sync_payload(data) -> dict:
    parsed = data
    try:
        for _ in range(4):
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
                continue
            if isinstance(parsed, dict) and isinstance(parsed.get("data"), (dict, str)):
                parsed = parsed["data"]
                continue
            break
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        return {}
    return {}


def _is_valid_fund_code_value(value) -> bool:
    return bool(re.fullmatch(r"\d{6}", str(value or "").strip()))


def _is_restorable_fund(fund) -> bool:
    return isinstance(fund, dict) and _is_valid_fund_code_value(fund.get("code"))


def _is_empty_plain_object(value) -> bool:
    return isinstance(value, dict) and len(value) == 0


def _summarize_sync_payload(parsed: dict) -> dict:
    funds = parsed.get("funds")
    has_funds_array = isinstance(funds, list)
    fund_items = funds if has_funds_array else []
    restorable = [fund for fund in fund_items if _is_restorable_fund(fund)]
    empty_portfolio_confirmed = parsed.get("emptyPortfolioConfirmed") is True
    is_confirmed_empty = (
        bool(parsed)
        and not any(key not in _CONFIRMED_EMPTY_PORTFOLIO_KEYS for key in parsed.keys())
        and has_funds_array
        and len(fund_items) == 0
        and empty_portfolio_confirmed
        and (
            "archivedLedger" not in parsed
            or _is_empty_plain_object(parsed.get("archivedLedger"))
        )
        and (
            "deletedFundsMeta" not in parsed
            or _is_empty_plain_object(parsed.get("deletedFundsMeta"))
        )
    )
    return {
        "has_payload": bool(parsed),
        "has_funds_array": has_funds_array,
        "fund_count": len(fund_items),
        "restorable_fund_count": len(restorable),
        "portfolio_fund_count": sum(1 for fund in restorable if fund.get("isWatchlist") is not True),
        "watchlist_fund_count": sum(1 for fund in restorable if fund.get("isWatchlist") is True),
        "empty_portfolio_confirmed": empty_portfolio_confirmed,
        "is_confirmed_empty_portfolio_snapshot": is_confirmed_empty,
        "has_restorable_sync_payload": len(restorable) > 0 or is_confirmed_empty,
    }


def _portfolio_payload_source(raw: dict, fallback: str = "") -> str:
    if raw.get("version") == "portfolio-v1":
        return "structured_portfolio"
    return fallback or "structured_portfolio"


def _unwrap_sync_payload(raw: dict, source: str = "") -> dict:
    json_data = raw.get("json_data") or "{}"
    updated_at = raw.get("updated_at", "")
    etag = raw.get("etag", "")
    parsed = _parse_sync_payload(json_data)
    if not isinstance(parsed, dict):
        parsed = {}
    summary = _summarize_sync_payload(parsed)
    parsed["_meta_summary"] = summary
    parsed["_meta_updated_at"] = updated_at
    parsed["_meta_etag"] = etag
    parsed["_meta_data_source"] = _portfolio_payload_source(raw, source)
    json_text = json_data if isinstance(json_data, str) else json.dumps(json_data, ensure_ascii=False)
    parsed["_meta_size_bytes"] = raw.get("size_bytes") or len(json_text.encode("utf-8"))
    for key, value in summary.items():
        parsed[f"_meta_{key}"] = value
    return parsed


def _normalize_upload_files(
    image_paths: Optional[list[str]] = None,
    images_base64: Optional[list[dict]] = None,
) -> list[tuple[str, bytes, str]]:
    files: list[tuple[str, bytes, str]] = []
    for path in image_paths or []:
        clean_path = os.path.expanduser(str(path))
        if not os.path.isfile(clean_path):
            raise ValueError(f"图片文件不存在：{path}")
        with open(clean_path, "rb") as f:
            content = f.read()
        mime = mimetypes.guess_type(clean_path)[0] or "application/octet-stream"
        mime = _validate_image_file(clean_path, content, mime)
        files.append((os.path.basename(clean_path), content, mime))
    for idx, item in enumerate(images_base64 or []):
        if not isinstance(item, dict):
            raise ValueError("images_base64 每项必须是对象")
        filename = str(item.get("filename") or f"image_{idx + 1}.png")
        mime = str(item.get("mime") or mimetypes.guess_type(filename)[0] or "image/png")
        raw_b64 = str(item.get("base64") or "")
        if "," in raw_b64 and raw_b64.strip().lower().startswith("data:"):
            raw_b64 = raw_b64.split(",", 1)[1]
        try:
            content = base64.b64decode(raw_b64, validate=True)
        except Exception:
            raise ValueError(f"{filename} 的 base64 内容无效")
        mime = _validate_image_file(filename, content, mime)
        files.append((filename, content, mime))
    if not files:
        raise ValueError("请提供 image_paths 或 images_base64")
    if len(files) > 10:
        raise ValueError("单次最多上传 10 张截图")
    return files


def _summarize_import_items(items: list[dict]) -> dict:
    total = len(items)
    exact = fuzzy = ambiguous = unmatched = skipped = 0
    for item in items:
        if item.get("skip"):
            skipped += 1
            continue
        status = item.get("match_status") or item.get("match_quality")
        matched = item.get("matched")
        code = item.get("code") or item.get("fund_code")
        if status == "exact" or (matched is True and status not in {"fuzzy", "ambiguous"}):
            exact += 1
        elif status in {"fuzzy", "manual"}:
            fuzzy += 1
        elif status == "ambiguous":
            ambiguous += 1
        elif matched is False or code in {None, "", "000000"}:
            unmatched += 1
    return {
        "total": total,
        "exact": exact,
        "fuzzy": fuzzy,
        "ambiguous": ambiguous,
        "unmatched": unmatched,
        "skipped": skipped,
    }


# ── 精度工具（严格对齐前端 roundMetricValue，消除 IEEE 754 差异）──────────────────
#
# 前端 roundMetricValue 使用十进制字符串 + BigInt 缩放，按 half-up 规则保留小数。
# 负数也按绝对值 half-up 后恢复符号（即 ties away from zero）。

def _js_round(v: float, d: int) -> float:
    """精确对齐前端 roundMetricValue(v, d)：十进制 half-up，负数远离 0。"""
    if not math.isfinite(v):
        return 0.0
    try:
        sign = -1 if v < 0 else 1
        shifted = float(abs(Decimal(repr(v))) * Decimal(10 ** d))
        return sign * (math.floor(shifted + 0.5) / (10 ** d))
    except Exception:
        return round(v, d)

def _r2(v: float) -> float: return _js_round(v, 2)
def _r4(v: float) -> float: return _js_round(v, 4)
def _r6(v: float) -> float: return _js_round(v, 6)

def _ratio_pct(numerator: float, denominator: float) -> Optional[float]:
    """
    对齐前端 calcRatioPercent(numerator, denominator)：
    分母无效返回 null；有效时按 half-up 保留 2 位百分比。
    """
    if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator <= 0:
        return None
    try:
        value = (Decimal(repr(numerator)) / Decimal(repr(denominator)) * Decimal("100")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        return float(value)
    except Exception:
        return None


def _to_float(value, default: float = 0.0) -> float:
    try:
        candidate = float(value)
        return candidate if math.isfinite(candidate) else default
    except (TypeError, ValueError):
        return default


# ── 收益计算（严格对齐前端 calculateFundStats 逻辑）──────────────────────────────

_TYPE_ORDER = {"CORRECTION": 0, "SELL": 1, "BUY": 2, "DIVIDEND_CASH": 3, "DIVIDEND_REINVEST": 3}


def _tx_effective_date(tx: dict) -> str:
    return tx.get("confirmDate") or tx.get("date") or ""


def _sort_txs(txs: list[dict]) -> list[dict]:
    """对齐前端 sortTransactionsByEffectiveOrder：按日期 → DIVIDEND_CASH 置后 → dayOrder → typeOrder → 原序。"""
    indexed = list(enumerate(txs))
    indexed.sort(key=lambda pair: (
        _tx_effective_date(pair[1]),
        1 if pair[1].get("type") == "DIVIDEND_CASH" else 0,
        pair[1].get("dayOrder") if pair[1].get("dayOrder") is not None else 999999,
        _TYPE_ORDER.get(pair[1].get("type", ""), 9),
        pair[0],
    ))
    return [item for _, item in indexed]


def _resolve_amount(tx: dict) -> float:
    amount = _to_float(tx.get("amount"))
    if amount > 0:
        return amount
    shares = _to_float(tx.get("shares"))
    nav = _to_float(tx.get("nav"))
    return _r2(shares * nav) if shares > 0 and nav > 0 else 0.0


def _resolve_buy_shares(tx: dict) -> float:
    shares = _to_float(tx.get("shares"))
    if shares > 0:
        return _r6(shares)
    amount = _to_float(tx.get("amount"))
    fee = _to_float(tx.get("fee"))
    net_amount = _r2(max(0.0, amount - fee))
    nav = _to_float(tx.get("nav"))
    return _r6(net_amount / nav) if nav > 0 and net_amount > 0 else 0.0


def _resolve_sell_shares(tx: dict) -> float:
    shares = _to_float(tx.get("shares"))
    if shares > 0:
        return _r6(shares)
    amount = _to_float(tx.get("amount"))
    nav = _to_float(tx.get("nav"))
    return _r6(amount / nav) if nav > 0 and amount > 0 else 0.0


def _is_valid_correction_tx(tx: dict) -> bool:
    shares = _to_float(tx.get("shares"), float("nan"))
    nav = _to_float(tx.get("nav"), float("nan"))
    return math.isfinite(shares) and math.isfinite(nav) and shares >= 0 and nav > 0


def _calc_correction_delta_total(txs: list[dict]) -> float:
    """对齐前端 getCorrectionDeltas：重放交易序列，计算每笔 CORRECTION 的成本变化量之和。"""
    current_shares = 0.0
    current_cost_total = 0.0
    delta_total = 0.0
    for tx in _sort_txs([t for t in txs if t.get("status") == "CONFIRMED"]):
        tx_type = tx.get("type", "")
        if tx_type == "BUY":
            buy_shares = _resolve_buy_shares(tx)
            buy_amount = _resolve_amount(tx)
            current_shares = _r6(current_shares + buy_shares)
            current_cost_total = _r2(current_cost_total + buy_amount)
        elif tx_type == "SELL":
            sell_shares = _resolve_sell_shares(tx)
            sold_cost = _r2(current_cost_total * min(sell_shares, current_shares) / current_shares) if current_shares > 0 else 0
            current_shares = _r6(current_shares - sell_shares)
            current_cost_total = _r2(current_cost_total - sold_cost)
            if current_shares <= 0.001:
                current_shares = 0.0
                current_cost_total = 0.0
        elif tx_type == "DIVIDEND_REINVEST":
            reinvest_shares = _to_float(tx.get("shares"))
            if reinvest_shares <= 0 and _to_float(tx.get("nav")) > 0 and _to_float(tx.get("amount")) > 0:
                reinvest_shares = _to_float(tx.get("amount")) / _to_float(tx.get("nav"))
            current_shares = _r6(current_shares + reinvest_shares)
        elif tx_type == "CORRECTION":
            if not _is_valid_correction_tx(tx):
                continue
            new_cost_total = _r2(_to_float(tx.get("shares")) * _to_float(tx.get("nav")))
            delta_amount = _r2(new_cost_total - current_cost_total)
            delta_total = _r2(delta_total + delta_amount)
            current_shares = _r6(_to_float(tx.get("shares")))
            current_cost_total = new_cost_total
    return delta_total


def _calc_change_profit(shares: float, base_nav: float, change_percent, current_nav) -> float:
    if not math.isfinite(shares) or shares <= 0:
        return 0.0
    if not math.isfinite(base_nav) or base_nav <= 0:
        return 0.0
    pct = _to_float(str(change_percent).replace("%", ""), float("nan")) if change_percent is not None else float("nan")
    nav = _to_float(current_nav, float("nan"))
    if math.isfinite(nav) and nav > 0:
        diff = nav - base_nav
        diff_growth_rate = (diff / base_nav) * 100
        if not math.isfinite(pct) or abs(diff_growth_rate - pct) <= 0.05:
            return _r2(shares * diff)
    if not math.isfinite(pct):
        return 0.0
    return _r2(shares * base_nav * pct / 100)


def _calc_fund_stats(fund: dict, est: Optional[dict] = None) -> dict:
    """
    计算单条记录的统计字段，逻辑对齐前端 calculateFundStats。

    关键对齐点：
    1. currentMarketValue / holdingProfit 只基于 fund.lastNav（官方净值），
       不用估值接口返回的 dwjz 回填，完全对齐 getFundOfficialNav。
    2. dayProfit 使用 estimatedNav 与 estimatedChangePercent 双路径兜底，
       对齐 calculateFundChangeProfit / calculateDisplayedDayProfit。
    3. source == 'reset' 时今日市场收益为 0；现金分红仍按 displayDate 计入。
    4. 收益率分母无效时返回 None，对齐 calcRatioPercent。
    """
    est = est or {}
    shares = _to_float(fund.get("holdingShares"))
    safe_shares = shares if shares > 0 else 0.0
    cost_per_share = _to_float(fund.get("holdingCost"))
    official_nav = _to_float(fund.get("lastNav"))
    if official_nav <= 0:
        official_nav = 0.0
    valuation_available = official_nav > 0

    # ── 基于官方净值的稳定字段（对齐前端 currentMarketValue / holdingProfit）──
    _stored_cost_total = fund.get("holdingCostTotal")
    fallback_cost_total = _r2(safe_shares * cost_per_share) if safe_shares > 0 and cost_per_share > 0 else 0.0
    stored_cost_total = _to_float(_stored_cost_total, float("nan"))
    cost_total = stored_cost_total if safe_shares > 0 and math.isfinite(stored_cost_total) and stored_cost_total >= 0 else fallback_cost_total

    txs = fund.get("transactions") or []
    _buy_total = 0.0
    _total_sold = 0.0
    for tx in txs:
        if tx.get("status", "") != "CONFIRMED":
            continue
        tx_type = tx.get("type", "")
        if tx_type == "BUY":
            _buy_total = _r2(_buy_total + _resolve_amount(tx))
        elif tx_type == "SELL":
            _total_sold = _r2(_total_sold + _resolve_amount(tx))
    _correction_delta = _calc_correction_delta_total(txs)
    total_invested = _r2(_buy_total + _correction_delta)

    market_value = _r2(safe_shares * official_nav) if valuation_available else 0.0
    holding_profit = _r2(market_value - cost_total) if valuation_available else 0.0
    sold_cost = _r2(max(0.0, total_invested - cost_total)) if total_invested > 0 else 0.0
    realized_fallback = _r2(_total_sold - sold_cost) if total_invested > 0 else 0.0
    raw_realized = _to_float(fund.get("realizedProfit"), float("nan"))
    realized = raw_realized if math.isfinite(raw_realized) else realized_fallback
    total_profit = _r2(holding_profit + realized)
    holding_return_rate = _ratio_pct(holding_profit, cost_total) if valuation_available else None

    source = str(est.get("source") or fund.get("source") or "")
    estimated_nav = _to_float(
        est.get("estimatedNav")
        or est.get("nav")
        or fund.get("estimatedNav")
    )
    if estimated_nav <= 0:
        estimated_nav = 0.0
    prev_nav = _to_float(est.get("prev_dwjz") or est.get("prevNav") or fund.get("prevNav"))
    estimated_change_percent = est.get("estimatedChangePercent")
    if estimated_change_percent is None:
        estimated_change_percent = est.get("gszzl")
    if estimated_change_percent is None:
        estimated_change_percent = fund.get("estimatedChangePercent")
    if source == "reset":
        today_profit = 0.0
    else:
        today_profit = _calc_change_profit(safe_shares, prev_nav, estimated_change_percent, estimated_nav)
    day_base_market_value = _r2(safe_shares * prev_nav) if source != "reset" and safe_shares > 0 and prev_nav > 0 else 0.0

    _effective_date = est.get("display_date") or fund.get("displayDate") or _beijing_date_string()
    _cash_dividend_today = 0.0
    for tx in txs:
        tx_status = tx.get("status", "")
        if tx_status != "CONFIRMED":
            continue
        tx_type = tx.get("type", "")
        if (tx_type == "DIVIDEND_CASH"
              and (tx.get("confirmDate") or tx.get("date")) == _effective_date):
            _cash_dividend_today = _r2(_cash_dividend_today + _to_float(tx.get("amount")))
    today_profit = _r2(today_profit + _cash_dividend_today)
    return {
        "marketValue": market_value,
        "currentMarketValue": market_value,
        "costPerShare": _r4(cost_per_share),
        "costTotal": cost_total,
        "holdingShares": _r6(safe_shares),
        "holdingProfit": holding_profit,
        "realizedProfit": _r2(realized),
        "totalProfit": total_profit,
        "totalInvested": total_invested,
        "returnRate": holding_return_rate,
        "holdingReturnRate": holding_return_rate,
        "todayProfit": today_profit,
        "dayProfit": today_profit,
        "dayBaseMarketValue": day_base_market_value,
        "currentNav": official_nav,
        "lastNav": official_nav if official_nav > 0 else None,
        "valuationAvailable": valuation_available,
        "estimatedNav": estimated_nav if estimated_nav > 0 else None,
        "estimatedChangePercent": estimated_change_percent,
    }


# ── Estimates 带缓存拉取（60s TTL，多工具共享，避免重复网络请求）──────────────────────

# 并发控制：限制同时请求后端的批次数量，避免触发速率限制
_estimate_semaphore = asyncio.Semaphore(3)

async def _fetch_estimates(
    codes: list,
    default_data_source_mode: str = "huahua",
    data_source_mode_by_code: Optional[dict] = None,
) -> dict:
    """
    批量获取今日估算数据，60s 内存缓存。
    get_records() 和 get_item_estimate() 共用此函数，同 session 内不重复请求。
    缓存超过 500 条时自动清空，防止长时间运行内存膨胀。
    source='timeout' 的结果不写入缓存，避免后端瞬时超时污染后续请求。
    """
    now = time.monotonic()
    default_mode = _normalize_data_source_mode(default_data_source_mode)
    mode_by_code = {
        _validate_fund_code(str(code)): _normalize_data_source_mode(mode)
        for code, mode in (data_source_mode_by_code or {}).items()
        if re.fullmatch(r"\d{6}", str(code or "").strip())
    }

    def mode_for(code: str) -> str:
        return mode_by_code.get(code, default_mode)

    def cache_key(code: str) -> str:
        return f"{code}:{mode_for(code)}"

    # 分离缓存命中 vs 需要请求
    result: dict = {}
    miss_codes: list = []
    for code in codes:
        entry = _estimate_cache.get(cache_key(code))
        if entry and now - entry["ts"] < _ESTIMATE_TTL:
            result[code] = entry["data"]
        else:
            miss_codes.append(code)

    if not miss_codes:
        return result

    # 资源控制：条目过多时清空
    if len(_estimate_cache) > 500:
        _estimate_cache.clear()

    # 并行批量请求未命中的（每批 50 个）
    # return_exceptions=True 保证 gather 本身不会抛出，各批次异常通过 isinstance 判断处理
    # 使用信号量限制并发，避免同时发起过多请求
    batches = [miss_codes[i:i+50] for i in range(0, len(miss_codes), 50)]

    async def _fetch_batch(batch: list) -> dict:
        async with _estimate_semaphore:
            return await _post("/api/estimate/batch", {
                "codes": batch,
                "defaultDataSourceMode": default_mode,
                "dataSourceModeByCode": {
                    code: mode_for(code)
                    for code in batch
                    if mode_for(code) != default_mode or code in mode_by_code
                },
            })

    responses = await asyncio.gather(
        *[_fetch_batch(batch) for batch in batches],
        return_exceptions=True,
    )
    for resp in responses:
        if isinstance(resp, Exception):
            continue
        batch_data = resp.get("data", resp) if isinstance(resp, dict) else resp
        if isinstance(batch_data, list):
            for item in batch_data:
                code_key = item.get("fundcode") or item.get("code")
                if not code_key:
                    continue
                # timeout 帧不缓存，避免污染后续 60s 内的查询
                if item.get("source") == "timeout":
                    result[code_key] = item
                else:
                    mode = _normalize_data_source_mode(item.get("dataSourceMode") or mode_for(code_key))
                    _estimate_cache[f"{code_key}:{mode}"] = {"data": item, "ts": now}
                    result[code_key] = item

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Tools: 认证类
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def set_token(token: str) -> str:
    """
    手动设置 Agent Token（运行时配置）。
    推荐通过环境变量 HUAHUA_AGENT_TOKEN 配置，无需调用此工具。

    Args:
        token: 从 App 设置页「Agent 访问令牌」中生成的令牌（PRO 会员专属）
    """
    _session["token"] = token.strip()
    _clear_session_caches()
    return f"✅ Token 已设置，将连接官方后端：{_session['base_url']}"


@mcp.tool()
async def get_tool_manifest() -> dict:
    """
    返回本 MCP 服务的能力边界、认证方式和建议调用顺序。
    不访问后端，可用于 Agent 在会话开始时自检。
    """
    return {
        "name": "huahua-daily",
        "transport": "stdio",
        "auth": {
            "primary_env": "HUAHUA_AGENT_TOKEN",
            "header": "Authorization: AgentToken <token>",
        },
        "api_base": _OFFICIAL_API,
        "capabilities": {
            "profile": ["get_current_user"],
            "portfolio": [
                "get_sync_meta",
                "get_raw_sync_data",
                "get_records",
                "get_summary",
                "get_transactions",
                "get_groups",
                "get_tags",
                "get_night_watchlist",
                "get_purchase_limit_watchlist",
            ],
            "market": [
                "search_item",
                "get_item_estimate",
                "get_fund_source_previews",
                "get_item_detail",
                "get_item_history",
                "get_item_dividends",
                "get_fund_timeline",
                "get_fund_fees",
                "get_batch_fund_fees",
                "get_fund_period_rank",
                "get_batch_fund_period_ranks",
                "get_fund_profile",
                "get_batch_fund_profiles",
                "get_night_estimate",
                "get_daily_rank",
                "get_status",
                "get_overview",
                "get_sector_wind",
                "get_yesterday_rank",
                "get_fund_flow",
                "get_indices",
                "get_holder_ranking",
                "get_benchmark_history",
                "get_instrument_catalog",
                "get_instrument_quotes",
                "get_instrument_timeline",
                "get_instrument_history",
                "calculate_trading_dates",
                "get_next_trading_day",
            ],
            "community": [
                "get_danmaku",
                "send_danmaku",
                "get_notices",
                "get_community_ranking",
                "get_community_my_rank",
                "get_community_user",
                "get_community_stats",
                "get_community_following",
                "search_community_users",
                "get_community_notices",
                "get_community_authorization",
                "authorize_community",
                "revoke_community_authorization",
                "follow_community_user",
            ],
            "trade": ["request_transaction", "get_agent_requests", "update_agent_request"],
            "personal_reports": [
                "submit_personal_strategy_report",
            ],
            "imports": [
                "import_holding_screenshots",
                "import_transaction_screenshots",
                "request_import_review",
            ],
            "misc": [
                "analyze_jcti",
                "get_app_version",
                "get_app_versions",
            ],
        },
        "safety": {
            "direct_trading": False,
            "trade_flow": "request_transaction 只创建待确认信号，必须由用户在 App 内确认。",
            "personal_report_write": True,
            "personal_report_flow": "submit_personal_strategy_report 只投递到当前 Agent Token 所属用户的报告中心；不能广播，不能指定 user_id。",
            "personal_report_required_scope": "messages:write",
            "public_report_write": False,
            "cloud_sync_read": "get_records/get_summary/get_raw_sync_data 读取云端实时同步主数据；固定使用结构化组合接口，不读取云端历史备份快照。",
            "cloud_sync_write": False,
            "cloud_history_snapshot_write": False,
            "empty_portfolio_restore": "已确认的空组合主数据会被识别为合法可恢复状态，但 MCP 不提供恢复或覆盖写入工具。",
            "destructive_tools": [],
        },
    }


@mcp.tool()
async def get_current_user() -> dict:
    """
    获取当前登录用户的账号信息（昵称、UID、会员状态等）。
    需要有效的 Agent Token（PRO 会员专属）。
    """
    _require_token()
    return await _get("/api/auth/me")


# ═══════════════════════════════════════════════════════════════════════════════
# Tools: 数据查询（需 Agent Token）
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def search_item(query: str) -> list:
    """
    按编号或名称搜索项目，返回最多 20 条结果。
    仅在不知道基金代码时使用；若已知代码（如用户直接提供），可跳过此步骤直接查询。

    Args:
        query: 搜索关键词，如 "000001"、"华夏"
    """
    _require_token()
    normalized = str(query or "").strip()
    if not normalized:
        raise ValueError("搜索关键词不能为空")
    if len(normalized) > 100:
        raise ValueError("搜索关键词过长，最多 100 字符")
    data = await _get("/api/search", params={"key": normalized})
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_item_detail(code: str) -> dict:
    """
    获取项目深度信息，包括历史收益率、胜率分析、完整净值序列、费率等。
    适合用户需要详细分析某只基金时调用；仅查询当前净值/涨跌请用 get_item_estimate，更轻量快速。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/{validated_code}")


@mcp.tool()
async def get_item_estimate(
    codes: list[str],
    default_data_source_mode: str = "huahua",
    data_source_mode_by_code: Optional[dict] = None,
) -> dict:
    """
    批量获取项目今日实时估算净值（最多 50 个）。
    适合查询"现在涨了多少""今天净值多少"等日常行情问题，比 get_item_detail 轻量得多。
    结果在同一 session 内缓存 60 秒，与 get_records 共享缓存，无重复网络请求。
    支持新版后端多行情源：default_data_source_mode / data_source_mode_by_code。

    Args:
        codes: 项目编号列表，如 ["000001", "110022"]，最多 50 个
        default_data_source_mode: 默认行情源模式：huahua/a/b/c。
        data_source_mode_by_code: 可选，每只基金单独指定行情源模式。
    """
    _require_token()
    # 验证并去重基金代码
    validated_codes = []
    seen = set()
    for code in codes[:50]:
        try:
            normalized = _validate_fund_code(code)
            if normalized not in seen:
                validated_codes.append(normalized)
                seen.add(normalized)
        except ValueError:
            continue  # 跳过无效代码
    if not validated_codes:
        return {"data": []}
    estimate_map = await _fetch_estimates(
        validated_codes,
        default_data_source_mode=default_data_source_mode,
        data_source_mode_by_code=data_source_mode_by_code,
    )
    return {"data": list(estimate_map.values())}


@mcp.tool()
async def get_fund_source_previews(code: str) -> dict:
    """
    获取单只基金在多个行情源下的实时估算预览。
    适合用户询问"不同数据源现在差多少"或需要选择基金级 dataSourceMode 时调用。

    Args:
        code: 项目编号，如 "000001"

    Returns:
        dict 包含 code 和 data，其中 data 通常是 huahua/a/b/c 到估算帧的映射。
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/estimate/source-previews/{validated_code}")


@mcp.tool()
async def get_daily_rank() -> dict:
    """
    获取今日涨幅榜和跌幅榜。
    返回涨幅最大和跌幅最大的项目列表，以及板块概览。
    """
    _require_token()
    return await _get("/api/fund/today-rank")


@mcp.tool()
async def get_item_history(code: str) -> list:
    """
    获取项目历史净值数据（用于查看过去走势）。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    data = await _get(f"/api/history/{validated_code}")
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_item_dividends(code: str) -> list:
    """
    获取项目历史派息记录。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    data = await _get(f"/api/fund/dividends/{validated_code}")
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_fund_timeline(code: str, source_mode: str = "huahua") -> list:
    """
    获取指定项目今日分时估值走势（每隔几分钟一个数据点，盘中更新）。
    适合了解今日净值走势曲线，判断入场时机。
    非交易日或盘前返回空列表。

    Args:
        code: 项目编号，如 "000001"
        source_mode: 行情源模式：huahua/a/b/c。
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    data = await _get(
        f"/api/fund/today-timeline/{validated_code}",
        params={"sourceMode": _normalize_data_source_mode(source_mode)},
    )
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_fund_fees(code: str) -> dict:
    """
    获取项目交易规则，包括确认天数、申购状态、QDII/限大额日累计限购金额等。
    在制定买卖决策时可参考确认周期、限购状态和手续费成本。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/fees/{validated_code}")


@mcp.tool()
async def get_batch_fund_fees(codes: list[str]) -> dict:
    """
    批量获取基金费率、申购状态、限购规则。最多 50 个代码。
    适合配合 get_purchase_limit_watchlist 一次性检查限购观察列表。

    Args:
        codes: 6 位基金代码列表。
    """
    _require_token()
    validated_codes = []
    seen = set()
    for code in codes[:50]:
        try:
            normalized = _validate_fund_code(code)
            if normalized not in seen:
                validated_codes.append(normalized)
                seen.add(normalized)
        except ValueError:
            continue
    if not validated_codes:
        return {"data": {}, "truncated": False, "limit": 50}
    return await _post("/api/fund/fees/batch", {"codes": validated_codes})


@mcp.tool()
async def get_fund_period_rank(code: str) -> dict:
    """
    获取项目近期业绩排名，包含近 1 个月、3 个月、6 个月、1 年的收益率及同类排名百分位。
    适合评估基金经理和产品的中长期表现。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/period-rank/{validated_code}")


@mcp.tool()
async def get_fund_profile(code: str) -> dict:
    """
    获取基金画像，包含基本信息、费率、业绩排名、持仓、行业分布、分红、风险指标等综合数据。
    比 get_item_detail 更聚焦于基金本身的静态属性，适合深度分析和对比。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/profile/{validated_code}")


@mcp.tool()
async def get_batch_fund_profiles(codes: list[str]) -> dict:
    """
    批量获取多只基金的画像数据，返回 code → 画像的映射。
    适合同时对比多只基金的基本面，一次最多 20 只。

    Args:
        codes: 项目编号列表，如 ["000001", "161725"]，最多 20 个
    """
    _require_token()
    validated_codes = []
    seen = set()
    for code in codes[:20]:
        try:
            normalized = _validate_fund_code(code)
            if normalized not in seen:
                validated_codes.append(normalized)
                seen.add(normalized)
        except ValueError:
            continue
    if not validated_codes:
        return {"data": {}}
    payload = await _post("/api/fund/profile/batch", {"codes": validated_codes})
    return payload.get("data", {}) if isinstance(payload, dict) else {}


@mcp.tool()
async def get_batch_fund_period_ranks(codes: list[str]) -> dict:
    """
    批量获取多个项目的近期业绩排名，返回 code → 排名数据的映射。
    一次请求处理最多 50 个项目，适合同时查看多个项目的表现对比。

    Args:
        codes: 项目编号列表，如 ["000001", "161725"]，最多 50 个
    """
    _require_token()
    # 验证并去重基金代码
    validated_codes = []
    seen = set()
    for code in codes[:50]:
        try:
            normalized = _validate_fund_code(code)
            if normalized not in seen:
                validated_codes.append(normalized)
                seen.add(normalized)
        except ValueError:
            continue
    if not validated_codes:
        return {"data": {}}
    payload = await _post("/api/fund/period-rank/batch", {"codes": validated_codes})
    return payload.get("data", {}) if isinstance(payload, dict) else {}


# ═══════════════════════════════════════════════════════════════════════════════
# Tools: 概览数据（需 Agent Token）
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def get_status() -> dict:
    """
    查询今日状态。
    返回 is_trading_day: true/false。
    """
    _require_token()
    return await _get("/api/market/status")


@mcp.tool()
async def get_overview() -> dict:
    """
    获取整体概览数据，包括主要指数涨跌、热门板块、涨跌排行。
    适合快速了解今日整体情况。
    """
    _require_token()
    async def safe_get(name: str, path: str, params: dict = None):
        try:
            return name, await _get(path, params=params)
        except Exception as exc:
            return name, {"error": str(exc)}

    catalog = await _get("/api/market/indices/catalog")
    default_codes = catalog.get("defaultCodes", []) if isinstance(catalog, dict) else []
    default_codes = [str(code) for code in default_codes if code][:10]
    results = await asyncio.gather(
        safe_get("status", "/api/market/status"),
        safe_get("todayRank", "/api/fund/today-rank"),
        safe_get("sectorWind", "/api/market/sector-wind"),
        safe_get("yesterdayRank", "/api/market/yesterday-rank"),
        safe_get("indices", "/api/market/indices/latest", params={"codes": ",".join(default_codes)}) if default_codes else asyncio.sleep(0, result=("indices", {"quotes": []})),
    )
    overview = {name: value for name, value in results}
    overview["instrumentCatalog"] = catalog
    return overview


@mcp.tool()
async def get_sector_wind() -> dict:
    """
    获取市场板块风向数据，包含领涨/领跌板块和数据时间。
    适合单独回答"今天哪些板块强/弱"。
    """
    _require_token()
    return await _get("/api/market/sector-wind")


@mcp.tool()
async def get_yesterday_rank() -> dict:
    """
    获取上一交易日基金涨跌榜。
    适合回答"昨天哪些基金涨得多/跌得多"，或和今日榜做对比。
    """
    _require_token()
    return await _get("/api/market/yesterday-rank")


@mcp.tool()
async def get_fund_flow() -> dict:
    """
    获取资金流向数据，包括主力资金流向和板块资金流向。
    需要 PRO 会员权限。适合回答"资金在流向哪里""哪些板块受追捧"等问题。

    Returns:
        dict 包含 fundFlow（基金资金流）、sectorFlow（板块资金流）、polledAt（数据时间）
    """
    _require_token()
    return await _get("/api/market/fund-flow")


@mcp.tool()
async def get_indices() -> list:
    """
    获取主要指数实时数据（上证、深证、创业板、沪深300、纳斯达克等）。
    """
    _require_token()
    catalog = await _get("/api/market/indices/catalog")
    default_codes = catalog.get("defaultCodes", []) if isinstance(catalog, dict) else []
    code_str = ",".join(str(code) for code in default_codes if code)
    if not code_str:
        return []
    data = await _get("/api/market/indices/latest", params={"codes": code_str})
    return data.get("quotes", []) if isinstance(data, dict) else []


@mcp.tool()
async def get_holder_ranking() -> dict:
    """
    获取 App 内持有人数排行榜（持有用户最多的 30 只基金）。
    返回每只基金的持有人数、最新涨跌幅，按涨幅排序。
    适合了解"大家都在买什么"的社区热度。
    """
    _require_token()
    return await _get("/api/market/holder-ranking")


@mcp.tool()
async def get_night_estimate(codes: list[str], force: bool = False, view: str = "forecast") -> dict:
    """
    获取QDII基金的夜间实时估值（美股/港股盘后/盘前交易时段）。
    返回每只基金的盘后涨跌幅、持仓穿透明细、汇率变动等数据。
    仅在美股交易时段（北京时间夜间）数据有效，需要会员权限。

    Args:
        codes: 基金代码列表，如 ["016665", "018147"]，最多 50 个
        force: 是否强制刷新（跳过服务端缓存），默认 false
        view: forecast（预测口径）或 last_close（上一收盘快照口径）
    """
    _require_token()
    validated_codes = []
    seen = set()
    for code in codes[:50]:
        try:
            normalized = _validate_fund_code(code)
            if normalized not in seen:
                validated_codes.append(normalized)
                seen.add(normalized)
        except ValueError:
            continue
    if not validated_codes:
        return {"status": "empty", "items": []}
    code_str = ",".join(validated_codes)
    params = {"codes": code_str}
    if force:
        params["force"] = "true"
    if view in {"forecast", "last_close"}:
        params["view"] = view
    return await _get("/api/market/night-est", params=params)


@mcp.tool()
async def get_night_watchlist() -> dict:
    """
    获取用户在 App「夜盘估值」页面手动添加的基金代码列表。

    数据来自云端实时同步主数据的 nightWatchCodes 字段；典型用法是把
    返回的 codes 作为参数传给 get_night_estimate，实现 "拉取用户自选
    夜盘基金的最新估值" 的端到端调用，无需用户在对话中手动报代码。

    Returns:
        dict 包含：
        - codes: 用户添加的 6 位基金代码列表（list[str]）
        - count: 代码数量
        - has_customized: 用户是否自定义过（False 表示用户从未修改，
          App 端会回退到内置默认列表；此时返回的 codes 为空，Agent
          可以提示用户先去 App 添加夜盘自选）
        - dataUpdatedAt: 云端实时同步主数据时间
    """
    _require_token()
    portfolio = await _download_portfolio()
    raw = portfolio.get("nightWatchCodes")
    has_customized = isinstance(raw, list)
    codes = [str(c) for c in raw if c] if has_customized else []
    return {
        "codes": codes,
        "count": len(codes),
        "has_customized": has_customized,
        "dataUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


@mcp.tool()
async def get_purchase_limit_watchlist() -> dict:
    """
    获取用户在 App「限购观察」中保存的基金列表。

    数据来自云端实时同步主数据的 purchaseLimitWatchItems 字段。新版 App 会把
    夜盘默认基金并入限购观察列表；旧版本或尚未同步过该功能的主数据可能没有此字段。

    Returns:
        dict 包含：
        - items: 观察项列表，含 code/name/type/addedAt/snapshot
        - codes: 6 位基金代码列表，可传给 get_fund_fees 批量检查申购状态
        - count: 观察项数量
        - has_customized: 云端主数据是否包含该字段
        - dataUpdatedAt: 云端实时同步主数据时间
    """
    _require_token()
    portfolio = await _download_portfolio()
    raw = portfolio.get("purchaseLimitWatchItems")
    has_customized = isinstance(raw, list)
    items = []
    seen = set()
    if has_customized:
        for item in raw:
            if not isinstance(item, dict):
                continue
            code = str(item.get("code") or "").strip()
            if not _is_valid_fund_code_value(code) or code in seen:
                continue
            seen.add(code)
            items.append({
                "code": code,
                "name": str(item.get("name") or "").strip(),
                "type": str(item.get("type") or "").strip(),
                "addedAt": item.get("addedAt") or "",
                "snapshot": item.get("snapshot") if isinstance(item.get("snapshot"), dict) else None,
            })
    return {
        "items": items,
        "codes": [item["code"] for item in items],
        "count": len(items),
        "has_customized": has_customized,
        "dataUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


@mcp.tool()
async def get_benchmark_history(code: str = "sh000300") -> list:
    """
    获取指数或 ETF 的历史走势数据，用于与持仓基金进行基准对比。
    默认返回沪深300（sh000300）的历史数据。

    支持两类代码：
    - 指数代码：如 "sh000300"（沪深300）、"sh000001"（上证指数）、"sz399001"（深证成指）
    - ETF 代码（纯数字）：如 "510300"（沪深300ETF）

    适合回答"我的基金跑赢大盘了吗"、"与沪深300比较"等问题。

    Args:
        code: 指数或 ETF 代码，默认 "sh000300"（沪深300）
    """
    _require_token()
    normalized = str(code or "").strip().lower()
    # 验证格式：指数代码（sh/sz开头+6位数字）或 ETF 代码（6位数字）
    if not re.fullmatch(r'(sh|sz)\d{6}|\d{6}', normalized):
        raise ValueError(f"基准代码格式无效：{code}，应为 sh000300 或 510300 格式")
    data = await _get(f"/api/market/benchmark-history/{normalized}")
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_instrument_catalog() -> dict:
    """
    获取市场行情仪表盘的可选指数/ETF 目录。
    返回完整的标的分类列表和默认展示代码，用于了解可查询的指数/ETF 范围。
    """
    _require_token()
    return await _get("/api/market/indices/catalog")


@mcp.tool()
async def get_instrument_quotes(codes: list[str]) -> dict:
    """
    批量获取指数/ETF 实时行情报价。
    适合同时查看多个指数的最新价格、涨跌幅。

    Args:
        codes: 标的代码列表，如 ["sh000300", "sh000001", "sz399001"]，最多 20 个
    """
    _require_token()
    validated = [str(c).strip() for c in (codes or [])[:20] if str(c).strip()]
    if not validated:
        return {"quotes": [], "polledAt": None}
    code_str = ",".join(validated)
    return await _get("/api/market/indices/latest", params={"codes": code_str})


@mcp.tool()
async def get_instrument_timeline(code: str, range: str = "1d") -> dict:
    """
    获取单个指数/ETF 的分时走势（5 分钟 K 线）。
    适合了解今日盘中走势。

    Args:
        code: 标的代码，如 "sh000300"
        range: 时间范围，默认 "1d"（当日）
    """
    _require_token()
    normalized = str(code or "").strip()
    if not normalized:
        raise ValueError("标的代码不能为空")
    return await _get("/api/market/indices/timeline", params={"code": normalized, "range": range})


@mcp.tool()
async def get_instrument_history(code: str, period: str = "1m") -> dict:
    """
    获取单个指数/ETF 的日线历史数据。
    适合分析中长期走势。

    Args:
        code: 标的代码，如 "sh000300"
        period: 时间周期，可选 "1m"（1个月）、"3m"（3个月）、"6m"（6个月）、"1y"（1年）
    """
    _require_token()
    normalized = str(code or "").strip()
    if not normalized:
        raise ValueError("标的代码不能为空")
    if period not in ("1m", "3m", "6m", "1y"):
        period = "1m"
    return await _get("/api/market/indices/history", params={"code": normalized, "period": period})


@mcp.tool()
async def calculate_trading_dates(
    date: str,
    time_mode: str = "PRE_MARKET",
    confirm_days: int = 1,
) -> dict:
    """
    计算基金申赎的净值日、数据日、确认到账日（T+N 日期推算）。
    跳过周末和法定节假日，适合辅助用户规划买卖时机。

    Args:
        date: 操作日期，格式 "YYYY-MM-DD"
        time_mode: 操作时间段。
            "PRE_MARKET"（默认）= 当日收盘前买入，T 日起算；
            "POST_MARKET" = 收盘后买入，T+1 日起算
        confirm_days: 确认天数（即 T+N 的 N），常见值：
            1 = T+1（货币基金、部分债基）
            2 = T+2（多数股票型/混合型基金）
            3 = T+3（部分 QDII、特殊基金）

    Returns:
        dict 包含：
            nav_date: 净值日（基金以哪天净值计算）
            data_date: 数据日（净值数据公布日）
            confirm_date: 确认到账日（份额/资金到账日）
    """
    _require_token()
    validated_date = _validate_date(date)
    if time_mode not in ("PRE_MARKET", "POST_MARKET"):
        raise ValueError(f"time_mode 必须是 PRE_MARKET 或 POST_MARKET，收到：{time_mode}")
    if not (1 <= confirm_days <= 30):
        raise ValueError(f"confirm_days 必须在 1-30 之间，收到：{confirm_days}")
    return await _post("/api/market/calculate-dates", {
        "date": validated_date,
        "time_mode": time_mode,
        "confirm_days": confirm_days,
    })


@mcp.tool()
async def get_next_trading_day(date: str) -> dict:
    """
    获取指定日期起（含当日）的下一个交易日，自动跳过周末和法定节假日。
    适合回答"元旦后第一个交易日是哪天"、"这个日期能买基金吗"等问题。

    Args:
        date: 起始日期，格式 "YYYY-MM-DD"

    Returns:
        dict 包含 date 字段，值为下一个交易日日期（"YYYY-MM-DD"）
    """
    _require_token()
    validated_date = _validate_date(date)
    return await _get("/api/market/next-trading-day", params={"date": validated_date})


# ═══════════════════════════════════════════════════════════════════════════════
# Tools: 记录管理（需 Agent Token + 会员）
# ═══════════════════════════════════════════════════════════════════════════════

async def _download_portfolio() -> dict:
    """
    下载云端实时同步主数据并解析 JSON。
    固定读取结构化组合接口，不读取旧同步大包或云端历史备份快照。
    使用 30s 内存缓存 + asyncio.Lock 双检锁，避免并发调用时发出重复下载请求。
    """
    now = time.monotonic()
    # 快速路径：缓存命中，无需加锁
    if _portfolio_cache["data"] is not None and now - _portfolio_cache["ts"] < _PORTFOLIO_TTL:
        return _portfolio_cache["data"]

    # 慢速路径：加锁后二次检查，确保只有一个协程执行下载和写入
    async with _get_download_lock():
        now = time.monotonic()
        if _portfolio_cache["data"] is not None and now - _portfolio_cache["ts"] < _PORTFOLIO_TTL:
            return _portfolio_cache["data"]

        raw, source = await _download_portfolio_raw()
        parsed = _unwrap_sync_payload(raw if isinstance(raw, dict) else {}, source=source)
        _portfolio_cache["data"] = parsed
        _portfolio_cache["ts"] = now
        return parsed


async def _download_portfolio_raw() -> tuple[dict, str]:
    """
    Return raw portfolio payload from the canonical structured source.

    `/api/portfolio/snapshot` is the current realtime-sync master data source.
    """
    structured = await _get("/api/portfolio/snapshot")
    return structured if isinstance(structured, dict) else {}, "structured_portfolio"


@mcp.tool()
async def get_sync_meta() -> dict:
    """
    获取云端实时同步主数据元信息，不下载完整数据。
    返回 updated_at、etag、size_bytes 和历史快照摘要，用于判断 App 数据是否已经同步到云端。
    """
    _require_token()
    meta = await _get("/api/sync/meta")
    if isinstance(meta, dict):
        restorable_count = int(meta.get("restorable_fund_count") or 0)
        empty_confirmed = meta.get("empty_portfolio_confirmed") is True
        has_empty_tombstone = (
            empty_confirmed
            and meta.get("has_funds_array") is True
            and int(meta.get("fund_count") or 0) == 0
        )
        meta["has_restorable_sync_payload"] = restorable_count > 0 or has_empty_tombstone
        meta["data_source"] = _portfolio_payload_source(meta)
        meta["history_snapshot"] = {
            "latest_snapshot_created_at": meta.get("latest_snapshot_created_at"),
            "latest_snapshot_etag": meta.get("latest_snapshot_etag"),
            "latest_snapshot_source": meta.get("latest_snapshot_source"),
        }
    return meta


@mcp.tool()
async def get_raw_sync_data(include_json_text: bool = False) -> dict:
    """
    获取完整云端实时同步主数据。默认返回解析后的 JSON，不返回原始 JSON 字符串以节省上下文。

    实时同步主数据包含 funds、groups、watchlistGroups、globalTags、字段显示配置、
    nightWatchCodes、purchaseLimitWatchItems、marketIndexSelection 等。
    profit ledger 是 App 可由交易记录和历史净值重建的派生数据；当前主数据通常不包含 ledger。

    Args:
        include_json_text: 是否同时返回服务端原始 json_data 字符串；只有做导出/迁移审计时才建议开启。
    """
    _require_token()
    raw, source = await _download_portfolio_raw()
    parsed = _unwrap_sync_payload(raw if isinstance(raw, dict) else {}, source=source)
    result = {
        "data": {k: v for k, v in parsed.items() if not k.startswith("_meta_")},
        "meta": {
            "updated_at": parsed.get("_meta_updated_at", ""),
            "etag": parsed.get("_meta_etag", ""),
            "data_source": parsed.get("_meta_data_source", source),
            "size_bytes": parsed.get("_meta_size_bytes", 0),
            "contains_ledger": "ledger" in parsed,
            "contains_archived_ledger": "archivedLedger" in parsed,
            **parsed.get("_meta_summary", {}),
        },
    }
    if include_json_text:
        result["json_data"] = raw.get("json_data", "") if isinstance(raw, dict) else ""
    return result


@mcp.tool()
async def get_transactions(code: str = "", include_pending: bool = True) -> dict:
    """
    获取云端实时同步主数据中的交易流水。默认返回全部基金；传入 code 时只返回该基金。

    Args:
        code: 可选，6 位基金代码。
        include_pending: 是否包含待确认交易。
    """
    _require_token()
    # 验证基金代码（如果提供）
    validated_code = ""
    if code:
        validated_code = _validate_fund_code(code)
    portfolio = await _download_portfolio()
    funds = portfolio.get("funds", [])
    items = []
    for fund in funds:
        if validated_code and str(fund.get("code", "")) != validated_code:
            continue
        txs = fund.get("transactions") or []
        if not include_pending:
            txs = [tx for tx in txs if tx.get("status") == "CONFIRMED"]
        items.append({
            "code": fund.get("code", ""),
            "name": fund.get("name", ""),
            "groupId": fund.get("groupId", ""),
            "transactions": txs,
        })
    return {
        "items": items,
        "dataUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


@mcp.tool()
async def get_groups() -> dict:
    """
    获取持仓分组和自选分组。
    """
    _require_token()
    portfolio = await _download_portfolio()
    return {
        "groups": portfolio.get("groups", []),
        "watchlistGroups": portfolio.get("watchlistGroups", []),
        "dataUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


@mcp.tool()
async def get_tags() -> dict:
    """
    获取全局标签注册表，以及每只基金绑定的标签。
    """
    _require_token()
    portfolio = await _download_portfolio()
    funds = portfolio.get("funds", [])
    return {
        "globalTags": portfolio.get("globalTags", []),
        "fundTags": [
            {
                "code": fund.get("code", ""),
                "name": fund.get("name", ""),
                "tags": fund.get("tags", []),
                "visibleTags": fund.get("visibleTags", []),
            }
            for fund in funds
        ],
        "dataUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


@mcp.tool()
async def get_records(include_transactions: bool = False) -> dict:
    """
    获取用户持仓记录，并自动计算今日收益、持有收益、累计收益、市值、持有收益率等字段。
    需要 Agent Token 且账号需开通会员才能使用云端实时同步数据。

    数据来自云端实时同步主数据（dataUpdatedAt 字段）。若刚在 App 中刷新了净值或新增了交易，
    请先确认 App 实时同步已完成后再查询，以获取最新数据。

    返回结构：
    - holdings: 有持仓的记录列表（含实时收益计算）
    - watchlist: 观察列记录（无持仓，仅供参考）
    - summary: 持仓汇总（总市值/今日收益/持有收益/持有收益率/累计收益/在途金额）
      - todayProfitRate: 今日/昨日收益率（todayProfit / totalDayBaseMarketValue × 100%，分母为归属日组合期初市值）
      - totalDayBaseMarketValue: 今日/昨日收益率使用的组合期初市值
      - totalHoldingProfit: 持有收益总额（市值 - 成本，不含落袋/已实现收益）
      - totalHoldingReturnRate: 持有收益率（totalHoldingProfit / totalCost × 100%，仅反映浮动亏盈）
      - cumulativeProfit: 累计收益（持有收益 + 已实现收益，含落袋；不代表用户所有平台/历史交易的完整累计）
    - dataUpdatedAt: 云端实时同步主数据的最后更新时间（UTC），展示给用户让其知晓数据新鲜度

    Args:
        include_transactions: 是否在每条记录中附带原始 transactions。默认 false 以节省上下文。
            需要审计交易流水、重算收益或排查数据时设为 true。
    """
    _require_token()
    # 1. 下载记录（有缓存时直接复用）
    portfolio = await _download_portfolio()
    funds: list = portfolio.get("funds", [])
    data_updated_at: str = portfolio.get("_meta_updated_at", "")
    data_source: str = portfolio.get("_meta_data_source", "")
    snapshot_summary: dict = portfolio.get("_meta_summary", {})

    # 2. 找出有持仓的项目编号
    held_codes = [f["code"] for f in funds if (f.get("holdingShares") or 0) > 0]

    # 3. 并行批量获取今日估算数值（共享 60s 缓存）
    estimate_map: dict = {}
    if held_codes:
        user_preferences = portfolio.get("userPreferences") if isinstance(portfolio.get("userPreferences"), dict) else {}
        default_mode = _normalize_data_source_mode(user_preferences.get("fundDataSourceMode"))
        mode_by_code = {}
        for fund in funds:
            code = str(fund.get("code") or "").strip()
            if not _is_valid_fund_code_value(code):
                continue
            fund_mode = fund.get("dataSourceMode")
            if fund_mode or code not in mode_by_code:
                mode_by_code[code] = _normalize_data_source_mode(fund_mode or default_mode)
        estimate_map = await _fetch_estimates(
            held_codes,
            default_data_source_mode=default_mode,
            data_source_mode_by_code=mode_by_code,
        )

    # 4. 计算每条记录的收益字段，剥离原始 transactions（减少 token 消耗）
    holdings = []
    watchlist = []

    for fund in funds:
        code = fund.get("code", "")
        est = estimate_map.get(code, {})
        stats = _calc_fund_stats(fund, est)
        txs = fund.get("transactions") or []

        # 只保留对 AI 有用的字段，剥离原始交易记录（可能数百条）
        enriched = {
            "code": code,
            "name": fund.get("name", ""),
            "type": fund.get("type", ""),
            "groupId": fund.get("groupId", ""),
            "tags": fund.get("tags", []),
            **stats,
        }
        if include_transactions:
            enriched["transactions"] = txs

        # 估算时间（来自后端 gztime 字段）
        if est:
            enriched["estimateTime"] = est.get("gztime", "")
            enriched["estimateSource"] = est.get("source", "")

        # 在途资产（PENDING 买入交易）
        pending_buy_txs = [
            {"date": tx.get("date"), "amount": tx.get("amount"), "note": tx.get("note")}
            for tx in txs if tx.get("status") == "PENDING" and tx.get("type") == "BUY"
        ]
        in_transit_amount = _r2(sum(_to_float(tx.get("amount")) for tx in pending_buy_txs))
        enriched["inTransitAmount"] = in_transit_amount
        if pending_buy_txs:
            enriched["pendingBuyTransactions"] = pending_buy_txs

        if (fund.get("holdingShares") or 0) > 0:
            holdings.append(enriched)
        else:
            # 观察列只保留基础信息和行情，不需要收益字段
            watchlist.append({
                "code": code,
                "name": fund.get("name", ""),
                "type": fund.get("type", ""),
                "lastNav": stats.get("lastNav"),
                "estimatedNav": stats.get("estimatedNav"),
                "estimatedChangePercent": stats.get("estimatedChangePercent"),
                **({"transactions": txs} if include_transactions else {}),
            })

    # 5. 汇总统计（只统计持仓项目）
    # 使用迭代累加而非 sum-then-round，精确对齐前端 analytics.ts 的逐步 r2 模式：
    #   totalMarketValue = r2(totalMarketValue + r2(stats.currentMarketValue))
    # 各个 item 字段已是 _r2 值，累加时每步再 _r2 可消除多只基金累计的浮点漂移。
    total_market_value = 0.0
    total_cost = 0.0
    total_today_profit = 0.0
    total_holding_profit = 0.0
    total_cumulative_profit = 0.0
    total_in_transit = 0.0
    total_invested = 0.0
    total_day_base_market_value = 0.0
    for f in holdings:
        total_market_value = _r2(total_market_value + f.get("marketValue", 0))
        total_cost = _r2(total_cost + f.get("costTotal", 0))
        total_today_profit = _r2(total_today_profit + f.get("todayProfit", 0))
        total_day_base_market_value = _r2(total_day_base_market_value + f.get("dayBaseMarketValue", 0))
        total_holding_profit = _r2(total_holding_profit + f.get("holdingProfit", 0))
        total_cumulative_profit = _r2(total_cumulative_profit + f.get("totalProfit", 0))
        total_in_transit = _r2(total_in_transit + f.get("inTransitAmount", 0))
        total_invested = _r2(total_invested + f.get("totalInvested", 0))
    total_holding_return_rate = _ratio_pct(total_holding_profit, total_cost)
    today_profit_rate = _ratio_pct(total_today_profit, total_day_base_market_value)

    return {
        "holdings": holdings,
        "watchlist": watchlist,
        "groups": portfolio.get("groups", []),
        "summary": {
            "totalMarketValue": total_market_value,
            "totalCost": total_cost,
            "todayProfit": total_today_profit,
            "todayProfitRate": today_profit_rate,
            "totalDayBaseMarketValue": total_day_base_market_value,
            "totalHoldingProfit": total_holding_profit,
            "totalHoldingReturnRate": total_holding_return_rate,
            "cumulativeProfit": total_cumulative_profit,
            "totalInvested": total_invested,
            "heldItemCount": len(holdings),
            "totalInTransitAmount": total_in_transit,
            "emptyPortfolioConfirmed": snapshot_summary.get("empty_portfolio_confirmed", False),
            "isConfirmedEmptyPortfolioSnapshot": snapshot_summary.get("is_confirmed_empty_portfolio_snapshot", False),
            "hasRestorableSyncPayload": snapshot_summary.get("has_restorable_sync_payload", False),
            "dataSource": data_source,
        },
        "snapshotSummary": snapshot_summary,
        "dataUpdatedAt": data_updated_at,
        "dataSource": data_source,
    }


@mcp.tool()
async def get_summary() -> dict:
    """
    获取持仓总览摘要（总市值、今日收益、今日收益率、持有收益、持有收益率、累计收益）。
    输出比 get_records 更精简（不含每只基金明细），适合快速查询资产概况。
    今日收益率 todayProfitRate 使用 todayProfit / totalDayBaseMarketValue，
    即归属日组合期初市值口径，不使用当前总市值。

    返回的 dataUpdatedAt 字段表示云端实时同步主数据的更新时间，请将此时间告知用户，
    让其了解数据是否为最新（若时间较旧，提示用户在 App 确认实时同步已完成）。
    """
    _require_token()
    result = await get_records()
    summary = result.get("summary", {})
    summary["dataUpdatedAt"] = result.get("dataUpdatedAt", "")
    return summary


@mcp.tool()
async def submit_personal_strategy_report(
    title: str,
    summary: str,
    payload: dict,
    client_message_id: str = "",
) -> dict:
    """
    将用户自己的 Agent 生成的个人策略报告投递到当前用户报告中心。

    认证要求：
    - 需要当前用户自己的 Agent Token。
    - Token 需要显式包含 messages:write scope；不要使用 hermes:write。

    安全边界：
    - 只写当前 Agent Token 所属用户的报告中心。
    - 不能广播，不能指定 user_id，不能调用 /api/hermes/reports。
    - 可基于用户明确授权读取的持仓、交易和行情数据生成个人报告。

    Args:
        title: 报告标题，如 "7月1日 个人组合复盘"。
        summary: 报告列表摘要，最多 500 字。
        payload: 策略报告 JSON，建议包含 kind/date/body/sections/themes/riskNotes。
        client_message_id: 当前用户内幂等 ID，如 personal:2026-07-01:evening。
    """
    _require_token()
    clean_title = str(title or "").strip()
    clean_summary = str(summary or "").strip()
    if not clean_title:
        raise ValueError("title 不能为空")
    if not clean_summary:
        raise ValueError("summary 不能为空")
    if not isinstance(payload, dict) or not payload:
        raise ValueError("payload 必须是非空对象")

    body = {
        "type": "STRATEGY_REPORT",
        "title": clean_title,
        "summary": clean_summary,
        "payload": payload,
    }
    if client_message_id:
        body["clientMessageId"] = str(client_message_id).strip()
    return await _post("/api/agent/messages", body)


@mcp.tool()
async def request_transaction(
    item_code: str,
    item_name: str,
    record_type: str,
    amount: float,
    date: str = "",
    note: str = "",
    group_name: str = "",
) -> str:
    """
    向用户的 App 发送一条交易请求信号。
    用户会在 App 中收到提示，点击后打开预填好的交易表单，确认后执行。
    交易逻辑（净值日计算、手续费、PENDING/CONFIRMED 状态）由 App 处理，不会产生数据冲突。

    重要：调用前须向用户确认基金名称和代码无误，尤其是通过搜索推断出来的代码。
    发送后须告知用户"需在 App 中确认才会生效"，不要让用户误以为已执行。

    如用户说"XX分组的XX基金买入XX元"，请从 get_records 获取分组信息后填入 group_name。
    App 会按分组名精确匹配，匹配失败时降级为弹出分组选择器。

    Args:
        item_code: 项目编号，如 "110022"
        item_name: 项目名称，如 "易方达消费行业"
        record_type: "BUY"（买入）或 "SELL"（卖出）
        amount: 金额（元），如 10000.00
        date: 操作日期 YYYY-MM-DD，留空则由 App 使用今日
        note: 备注说明（可选）
        group_name: 目标分组名称（可选），如 "沪深宽基"；有值时 App 直接路由到该分组

    Returns:
        str: 发送结果提示
    """
    _require_token()
    tx_type = record_type.upper()
    if tx_type not in ("BUY", "SELL"):
        return "❌ record_type 必须是 'BUY' 或 'SELL'"

    validated_code = _validate_fund_code(item_code)
    normalized_name = str(item_name or "").strip()
    if not normalized_name:
        raise ValueError("item_name 不能为空")
    validated_amount = _validate_amount(amount)
    validated_date = _validate_date(date)

    payload_dict: dict = {
        "code": validated_code,
        "name": normalized_name,
        "amount": validated_amount,
        "date": validated_date,
        "note": note,
    }
    if group_name:
        payload_dict["group_name"] = group_name

    payload = json.dumps(payload_dict, ensure_ascii=False)

    await _post("/api/agent/request", {"action_type": tx_type, "payload": payload})
    action = "买入" if tx_type == "BUY" else "卖出"
    group_hint = f"（分组：{group_name}）" if group_name else ""
    return f"✅ {action}请求已发送：{item_name}（{validated_code}）¥{validated_amount:,.2f}{group_hint}，请打开 App 确认后生效。"


@mcp.tool()
async def get_agent_requests() -> list:
    """
    获取当前账号仍待处理的 Agent 交易请求。
    主要用于 Agent 自检是否已经重复发送请求；App 端仍是最终确认入口。
    """
    _require_token()
    data = await _get("/api/agent/request")
    return data if isinstance(data, list) else []


@mcp.tool()
async def update_agent_request(request_id: str, status: str) -> dict:
    """
    更新 Agent 交易请求状态。通常由 App 调用；Agent 只应在用户明确要求撤销/忽略时使用。

    Args:
        request_id: get_agent_requests 返回的 id。
        status: "DISMISSED" 或 "PROCESSED"。Agent 常用 "DISMISSED"。
    """
    _require_token()
    normalized_request_id = str(request_id or "").strip()
    if not normalized_request_id:
        raise ValueError("request_id 不能为空")
    normalized = (status or "").strip().upper()
    if normalized not in ("PROCESSED", "DISMISSED"):
        raise ValueError("status 必须是 PROCESSED 或 DISMISSED")
    return await _put(f"/api/agent/request/{normalized_request_id}", {"status": normalized})


@mcp.tool()
async def import_holding_screenshots(
    image_paths: Optional[list[str]] = None,
    images_base64: Optional[list[dict]] = None,
    import_type: str = "HOLDINGS",
) -> dict:
    """
    识别持仓/自选截图，只返回结构化结果，不写入 App。

    Agent 可先对 unmatched / ambiguous 条目做轻确认，然后调用 request_import_review
    把结果发送到 App 现有导入确认页。

    Args:
        image_paths: 本地图片路径列表，适合 Codex、Claude Code 等本地 CLI/桌面 Agent。
        images_base64: 图片对象列表，格式 {filename, mime, base64}。
        import_type: "HOLDINGS"（持仓，默认）或 "WATCHLIST"（自选）。
            自选截图通常显示 6 位基金代码，传 "WATCHLIST" 后端会用专门 prompt
            提取代码并精确匹配，避免名称模糊匹配的误配。
    """
    _require_token()
    files = _normalize_upload_files(image_paths, images_base64)
    mode = "watchlist" if (import_type or "").strip().upper() == "WATCHLIST" else "holdings"
    raw = await _post_files("/api/import_screenshot", files, form_data={"mode": mode})
    items = raw if isinstance(raw, list) else []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        code = item.get("code") or "000000"
        match_quality = item.get("match_quality") or ("exact" if code != "000000" else "none")
        normalized.append({
            **item,
            "match_status": "unmatched" if code == "000000" else match_quality,
            "resolution_required": code == "000000" or match_quality in {"none", "ambiguous"},
            "resolution_reason": "未匹配到基金代码" if code == "000000" else "",
        })
    return {
        "items": normalized,
        "summary": _summarize_import_items(normalized),
        "next_step": "如有未匹配或歧义项，先在对话中轻确认；确认后调用 request_import_review 发送到 App。",
    }


@mcp.tool()
async def import_transaction_screenshots(
    image_paths: Optional[list[str]] = None,
    images_base64: Optional[list[dict]] = None,
) -> dict:
    """
    识别交易记录截图，只返回结构化结果，不写入 App。

    Args:
        image_paths: 本地图片路径列表，适合 Codex、Claude Code 等本地 CLI/桌面 Agent。
        images_base64: 图片对象列表，格式 {filename, mime, base64}。
    """
    _require_token()
    files = _normalize_upload_files(image_paths, images_base64)
    raw = await _post_files("/api/import_transactions", files)
    items = raw if isinstance(raw, list) else []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        matched = bool(item.get("matched"))
        reason = ""
        if not matched:
            reason = "未匹配到基金代码"
        elif not item.get("date"):
            reason = "交易日期缺失"
        elif item.get("type") == "BUY" and item.get("amount") is None:
            reason = "买入金额缺失"
        elif item.get("type") == "SELL" and item.get("shares") is None:
            reason = "卖出份额缺失"
        normalized.append({
            **item,
            "match_status": "exact" if matched else "unmatched",
            "resolution_required": bool(reason),
            "resolution_reason": reason,
        })
    return {
        "items": normalized,
        "summary": _summarize_import_items(normalized),
        "next_step": "如有未匹配或日期/金额歧义，先在对话中轻确认；确认后调用 request_import_review 发送到 App。",
    }


@mcp.tool()
async def request_import_review(
    import_type: str,
    items: list[dict],
    source_note: str = "Agent screenshot import",
) -> str:
    """
    将 Agent 识别和轻确认后的导入结果发送到 App，复用 App 现有批量导入确认页。

    Args:
        import_type: "HOLDINGS"、"WATCHLIST" 或 "TRANSACTIONS"。
        items: 识别结果数组，最多 300 条。
        source_note: 展示给用户的来源说明。
    """
    _require_token()
    normalized_type = (import_type or "").strip().upper()
    action_map = {
        "HOLDINGS": "IMPORT_HOLDINGS",
        "WATCHLIST": "IMPORT_WATCHLIST",
        "TRANSACTIONS": "IMPORT_TRANSACTIONS",
    }
    action_type = action_map.get(normalized_type)
    if not action_type:
        raise ValueError("import_type 必须是 HOLDINGS、WATCHLIST 或 TRANSACTIONS")
    if not isinstance(items, list) or not items:
        raise ValueError("items 不能为空")
    if len(items) > 300:
        raise ValueError("单次导入请求最多 300 条")
    payload_dict = {
        "importType": normalized_type,
        "source": "agent_screenshot",
        "sourceNote": source_note,
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": _summarize_import_items(items),
        "items": items,
    }
    payload = json.dumps(payload_dict, ensure_ascii=False)
    if len(payload.encode("utf-8")) > 1024 * 1024:
        raise ValueError("导入请求体不能超过 1MB，请拆分后发送")
    await _post("/api/agent/request", {"action_type": action_type, "payload": payload})
    return f"✅ 已发送 {payload_dict['summary']['total']} 条导入结果到 App，请打开花花日记批量确认后导入。"


@mcp.tool()
async def get_danmaku(code: str) -> list:
    """
    获取某只基金今日弹幕/社区短消息。

    Args:
        code: 6 位基金代码。
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    data = await _get(f"/api/danmaku/{validated_code}")
    return data if isinstance(data, list) else []


@mcp.tool()
async def send_danmaku(fund_code: str, text: str) -> dict:
    """
    发送某只基金的社区短消息。只有用户明确要求发言时才调用。
    弹幕颜色由 App 根据基金涨跌情况自动设置，无需手动指定。

    Args:
        fund_code: 6 位基金代码。
        text: 1-30 字。
    """
    _require_token()
    validated_code = _validate_fund_code(fund_code)
    normalized_text = str(text or "").strip()
    if not normalized_text:
        raise ValueError("弹幕内容不能为空")
    if len(normalized_text) > 30:
        raise ValueError(f"弹幕内容过长：{len(normalized_text)} 字，最多 30 字")
    return await _post("/api/danmaku/send", {
        "fund_code": validated_code,
        "text": normalized_text,
    })


@mcp.tool()
async def get_notices(since: float = 0) -> list:
    """
    获取系统公告。

    Args:
        since: Unix 秒时间戳，只返回该时间之后的公告；默认返回最近公告。
    """
    data = await _get("/api/notices", params={"since": since})
    return data if isinstance(data, list) else []


# ═══════════════════════════════════════════════════════════════════════════════
# Tools: 喵舍社区（需 Agent Token + PRO 会员）
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def get_community_ranking(tab: str = "weekly", page: int = 1, page_size: int = 50) -> dict:
    """
    获取喵舍收益率排行榜。

    Args:
        tab: 排行榜类型，可选 "weekly"（周收益）、"monthly"（月收益）、"total"（总收益）
        page: 页码，从 1 开始
        page_size: 每页条数，1-100，默认 50
    """
    _require_token()
    if tab not in ("weekly", "monthly", "total"):
        tab = "weekly"
    return await _get("/api/community/ranking", params={
        "tab": tab,
        "page": max(1, page),
        "page_size": min(100, max(1, page_size)),
    })


@mcp.tool()
async def get_community_my_rank() -> dict:
    """
    获取当前用户在各排行榜的排名。
    适合回答"我排第几"类问题。
    """
    _require_token()
    return await _get("/api/community/my-rank")


@mcp.tool()
async def get_community_user(uid: str) -> dict:
    """
    获取喵舍用户详情，包含收益率和十大重仓（前5）。
    适合查看其他用户的投资组合。

    Args:
        uid: 用户的 8 位 UID
    """
    _require_token()
    normalized = str(uid or "").strip()
    if not normalized:
        raise ValueError("UID 不能为空")
    return await _get(f"/api/community/user/{normalized}")


@mcp.tool()
async def get_community_stats() -> dict:
    """
    获取当前用户的关注数和粉丝数。
    """
    _require_token()
    return await _get("/api/community/stats")


@mcp.tool()
async def get_community_following() -> list:
    """
    获取当前用户的关注列表。
    """
    _require_token()
    data = await _get("/api/community/following")
    return data if isinstance(data, list) else []


@mcp.tool()
async def search_community_users(query: str) -> list:
    """
    搜索喵舍用户，支持 UID 精确匹配和昵称模糊匹配。

    Args:
        query: 搜索关键词（UID 或昵称）
    """
    _require_token()
    normalized = str(query or "").strip()
    if not normalized:
        raise ValueError("搜索关键词不能为空")
    data = await _get("/api/community/search", params={"q": normalized})
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_community_notices(since: float = 0) -> list:
    """
    获取当前用户的社区定向通知（如排名变化、被关注等）。
    与 get_notices（系统公告）不同，这是用户个人的社区通知。

    Args:
        since: Unix 秒时间戳，只返回该时间之后的通知；默认返回最近通知。
    """
    _require_token()
    data = await _get("/api/community/notices", params={"since": since})
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_community_authorization() -> dict:
    """
    查询当前用户的喵舍社区授权状态。
    返回是否已授权、是否展示金额、是否匿名等信息。
    适合在首次使用社区功能前检查授权状态。
    """
    _require_token()
    return await _get("/api/community/authorization")


@mcp.tool()
async def authorize_community(
    show_amount: bool = False,
    anonymous: bool = False,
) -> dict:
    """
    授权参与喵舍社区排行榜。调用前须向用户确认是否愿意公开持仓数据。
    授权后用户的收益率将出现在社区排行榜中。

    Args:
        show_amount: 是否公开展示持仓金额（默认 false，仅展示收益率）
        anonymous: 是否匿名参与（默认 false）
    """
    _require_token()
    return await _post("/api/community/authorize", {
        "authorized": True,
        "show_amount": show_amount,
        "anonymous": anonymous,
        "disclaimer_accepted": True,
    })


@mcp.tool()
async def revoke_community_authorization() -> dict:
    """
    取消喵舍社区授权，退出排行榜。
    取消后用户的收益率数据将从排行榜中移除。
    """
    _require_token()
    return await _delete("/api/community/authorize")


@mcp.tool()
async def follow_community_user(target_uid: str) -> dict:
    """
    关注/取消关注喵舍社区用户（取反操作）。
    若已关注则取消关注，若未关注则添加关注。

    Args:
        target_uid: 目标用户的 8 位 UID
    """
    _require_token()
    normalized = str(target_uid or "").strip()
    if not normalized:
        raise ValueError("target_uid 不能为空")
    return await _post("/api/community/follow", {"target_uid": normalized})


# ═══════════════════════════════════════════════════════════════════════════════
# Tools: JCTI 投资人格测试（需 Agent Token）
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def analyze_jcti(
    personality_id: str,
    ye: float = 0,
    wen: float = 0,
    sui: float = 0,
    duan: float = 0,
) -> dict:
    """
    提交 JCTI（韭彩测试指标）四维分数，获取 AI 个性化投资人格分析。
    需要 VIP 或 PRO 会员权限。

    人格 ID 对照：
    - tepulang: 特普朗（高野高稳）
    - jiuhuang: 韭黄（高野高随）
    - faguo-dushen: 法国赌神（高野高短）
    - ji-wuli: 姬无力（低野低稳）
    - yingshengchong: 应声虫（低野高随）
    - shanmu: 山姆（低野高稳）
    - taozhongren: 套中人（低野高短）
    - tuoluowang: 陀螺王（高野低短）

    Args:
        personality_id: 人格 ID，如 "tepulang"
        ye: 野维度分数（0-100）
        wen: 稳维度分数（0-100）
        sui: 随维度分数（0-100）
        duan: 短维度分数（0-100）

    Returns:
        dict 包含 analysis 字段（AI 生成的个性化分析文本）
    """
    _require_token()
    valid_ids = {
        "tepulang", "jiuhuang", "faguo-dushen", "ji-wuli",
        "yingshengchong", "shanmu", "taozhongren", "tuoluowang",
    }
    normalized = str(personality_id or "").strip().lower()
    if normalized not in valid_ids:
        raise ValueError(f"无效的 personality_id：{personality_id}，有效值：{', '.join(sorted(valid_ids))}")
    for name, val in [("ye", ye), ("wen", wen), ("sui", sui), ("duan", duan)]:
        if not (0 <= val <= 100):
            raise ValueError(f"{name} 分数必须在 0-100 之间，收到：{val}")
    return await _post("/api/jcti/analyze", {
        "scores": {"ye": ye, "wen": wen, "sui": sui, "duan": duan},
        "personality_id": normalized,
    })


# ═══════════════════════════════════════════════════════════════════════════════
# Tools: 版本信息（需 Agent Token）
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def get_app_version() -> dict:
    """
    获取最新 App 版本信息，包括版本号、更新日志、下载地址、是否强制更新。
    适合回答"最新版本是多少""有什么新功能"等问题。
    """
    _require_token()
    return await _get("/api/version")


@mcp.tool()
async def get_app_versions(page: int = 1, page_size: int = 5) -> dict:
    """
    获取 App 版本历史列表（分页，从新到旧）。
    适合查看历史更新记录。

    Args:
        page: 页码，从 1 开始
        page_size: 每页条数，1-20，默认 5
    """
    _require_token()
    return await _get("/api/versions", params={
        "page": max(1, page),
        "page_size": min(20, max(1, page_size)),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """uvx / console_scripts 入口点。"""
    mcp.run()


if __name__ == "__main__":
    main()
