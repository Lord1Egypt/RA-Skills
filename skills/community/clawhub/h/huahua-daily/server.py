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
from decimal import Decimal
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
# ── Validation helpers ────────────────────────────────────────────────────────

# 图片文件大小限制（10MB）
_MAX_IMAGE_SIZE = 10 * 1024 * 1024

# 允许的图片 MIME 类型
_ALLOWED_IMAGE_MIMES = {
    "image/jpeg", "image/png", "image/webp", "image/gif", "image/bmp",
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

async def _post(path: str, body: dict = None) -> dict:
    try:
        r = await _get_client().post(_url(path), json=body or {}, headers=_headers())
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


def _unwrap_sync_payload(raw: dict) -> dict:
    json_data = raw.get("json_data") or "{}"
    updated_at = raw.get("updated_at", "")
    etag = raw.get("etag", "")
    try:
        parsed = json.loads(json_data)
        if isinstance(parsed, str):
            parsed = json.loads(parsed)
        if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict):
            parsed = parsed["data"]
        if not isinstance(parsed, dict):
            parsed = {}
    except Exception:
        parsed = {}
    parsed["_meta_updated_at"] = updated_at
    parsed["_meta_etag"] = etag
    parsed["_meta_size_bytes"] = len(json_data.encode("utf-8"))
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


# ── 精度工具（严格对齐前端 _round，消除 IEEE 754 差异）───────────────────────────
#
# 前端 _round(v, d)：Number(`${Math.round(Number(`${v}e+${d}`))}e-${d}`)
#   1. `${v}` 先转字符串，再拼成指数形式后 Number() 解析，避免 IEEE 754 乘法漂移
#      （如 1.005*100 在 float 中实为 100.4999...，导致 round 结果偏低）
#   2. Math.round 向 +∞ 舍入（正数同四舍五入，负数 -.5 → 0）
#
# Python 对齐实现：
#   - Decimal(repr(v)) 利用 Python repr 给出精确字符串（同 JS `${v}`）
#   - * Decimal(10**d) 精确乘法，等效 Number(`${v}e+${d}`)
#   - math.floor(x + 0.5) 完全等同 JS Math.round

def _js_round(v: float, d: int) -> float:
    """精确对齐前端 _round(v, d)。"""
    if not math.isfinite(v):
        return 0.0
    try:
        shifted = float(Decimal(repr(v)) * Decimal(10 ** d))
        return math.floor(shifted + 0.5) / (10 ** d)
    except Exception:
        return round(v, d)

def _r2(v: float) -> float: return _js_round(v, 2)
def _r4(v: float) -> float: return _js_round(v, 4)
def _r6(v: float) -> float: return _js_round(v, 6)

def _r2_pct(holding_profit: float, cost_total: float) -> float:
    """
    对齐前端 returnRate：Math.round((holdingProfit / costTotal) * 10000) / 100。
    使用 math.floor(v + 0.5) 而非 int(v + 0.5)：
    - int() 向零截断，对负值行为与 JS Math.round 不同（负半数向 +∞ 舍入）
    - math.floor(x + 0.5) 精确复现 JS Math.round 的 round-half-toward-+∞ 语义
    示例：returnRate = -0.6% 时，int(-0.1)=0 给出 0%，floor(-0.1)=-1 给出 -0.01%（正确）
    """
    if cost_total <= 0:
        return 0.0
    try:
        v = holding_profit / cost_total
        return math.floor(v * 10000 + 0.5) / 100
    except Exception:
        return 0.0


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


def _calc_correction_delta_total(txs: list[dict]) -> float:
    """对齐前端 getCorrectionDeltas：重放交易序列，计算每笔 CORRECTION 的成本变化量之和。"""
    current_shares = 0.0
    current_cost_total = 0.0
    delta_total = 0.0
    for tx in _sort_txs([t for t in txs if t.get("status") == "CONFIRMED"]):
        tx_type = tx.get("type", "")
        if tx_type == "BUY":
            buy_shares = tx.get("shares") or 0
            buy_amount = tx.get("amount") or 0
            if buy_shares <= 0 and (tx.get("nav") or 0) > 0 and buy_amount > 0:
                buy_shares = buy_amount / tx["nav"]
            if buy_amount <= 0 and buy_shares > 0 and (tx.get("nav") or 0) > 0:
                buy_amount = _r2(buy_shares * tx["nav"])
            current_shares = _r6(current_shares + buy_shares)
            current_cost_total = _r2(current_cost_total + buy_amount)
        elif tx_type == "SELL":
            sell_shares = tx.get("shares") or 0
            if sell_shares <= 0 and (tx.get("nav") or 0) > 0 and (tx.get("amount") or 0) > 0:
                sell_shares = tx["amount"] / tx["nav"]
            sold_cost = _r2(current_cost_total * min(sell_shares, current_shares) / current_shares) if current_shares > 0 else 0
            current_shares = _r6(current_shares - sell_shares)
            current_cost_total = _r2(current_cost_total - sold_cost)
            if current_shares <= 0.001:
                current_shares = 0.0
                current_cost_total = 0.0
        elif tx_type == "DIVIDEND_REINVEST":
            reinvest_shares = tx.get("shares") or 0
            if reinvest_shares <= 0 and (tx.get("nav") or 0) > 0 and (tx.get("amount") or 0) > 0:
                reinvest_shares = tx["amount"] / tx["nav"]
            current_shares = _r6(current_shares + reinvest_shares)
        elif tx_type == "CORRECTION":
            if (tx.get("nav") or 0) <= 0:
                continue
            new_cost_total = _r2(tx.get("shares", 0) * tx["nav"])
            delta_amount = _r2(new_cost_total - current_cost_total)
            delta_total = _r2(delta_total + delta_amount)
            current_shares = _r6(tx.get("shares", 0))
            current_cost_total = new_cost_total
    return delta_total


def _calc_fund_stats(fund: dict, est: Optional[dict] = None) -> dict:
    """
    计算单条记录的统计字段，逻辑对齐前端 calculateFundStats。

    关键对齐点：
    1. marketValue / holdingProfit / returnRate 均基于官方净值（lastNav），
       不受盘中估算影响（前端 getFundOfficialNav 的语义）。
    2. todayProfit = shares × (estimatedNav - prevNav)，用 prevNav（估算基准净值）
       而非 lastNav，避免 QDII / 新建仓场景下的偏差。
    3. 若 source == 'reset'（盘前重置）或 source == 'timeout'，忽略 estimatedNav，todayProfit = 0。
    4. returnRate 使用 _r2_pct 对齐前端 Math.round(v*10000)/100 语义。
    """
    shares: float = fund.get("holdingShares", 0) or 0
    cost_per_share: float = fund.get("holdingCost", 0) or 0
    last_nav: float = 0
    # 云快照只提供最后一次官方净值基线；优先采用本次估值接口返回的官方净值，
    # 兼容旧云快照没有 lastNav 的用户，避免错误退化为 1.0。
    for raw_nav in (
        est.get("dwjz"), est.get("lastNav"), est.get("last_nav"), fund.get("lastNav"),
    ):
        try:
            candidate = float(raw_nav or 0)
        except (TypeError, ValueError):
            continue
        if candidate > 0:
            last_nav = candidate
            break
    realized: float = fund.get("realizedProfit", 0) or 0

    # 估算信息（timeout 帧视同无估算，对齐前端拒收逻辑）
    est = est or {}
    source: str = est.get("source") or fund.get("source") or ""
    _ignore_est = source in ("reset", "timeout")
    estimated_nav_raw: float = est.get("estimatedNav") or est.get("nav") or 0
    estimated_nav: float = estimated_nav_raw if (estimated_nav_raw > 0 and not _ignore_est) else 0

    # prevNav：当日涨跌比较基准（前一交易日官方净值）
    # 估算接口返回字段名为 prev_dwjz（字符串），优先取实时值；
    # 降级顺序：est.prev_dwjz → est.prevNav(兼容) → fund.prevNav(云同步存储) → last_nav
    _prev_raw = est.get("prev_dwjz") or est.get("prevNav") or fund.get("prevNav") or 0
    try:
        prev_nav = float(_prev_raw) or last_nav
    except (TypeError, ValueError):
        prev_nav = last_nav

    official_nav: float = last_nav if last_nav > 0 else 0
    # 旧云快照且行情源只返回盘中估值时，用本次估值作为临时计价基线；
    # 两者都缺失则保持 0 并显式标记不可计价，绝不再伪造净值 1.0。
    valuation_nav: float = official_nav or estimated_nav
    valuation_available = valuation_nav > 0

    # ── 基于官方净值的稳定字段（对齐前端 currentMarketValue / holdingProfit）──
    _stored_cost_total = fund.get("holdingCostTotal")
    cost_total = _r2(_stored_cost_total) if _stored_cost_total is not None else _r2(shares * cost_per_share)
    market_value = _r2(shares * valuation_nav) if valuation_available else 0.0
    holding_profit = _r2(market_value - cost_total) if valuation_available else 0.0
    total_profit = _r2(holding_profit + realized) if valuation_available else realized
    return_rate = _r2_pct(holding_profit, cost_total) if valuation_available else 0.0

    # ── 今日盈亏：estimatedNav vs prevNav（对齐前端 calculateFundDayProfit）──────
    if estimated_nav > 0 and prev_nav > 0 and shares > 0:
        today_profit = _r2((estimated_nav - prev_nav) * shares)
    else:
        today_profit = 0.0

    _effective_date = fund.get("displayDate") or time.strftime("%Y-%m-%d")
    _cash_dividend_today = 0.0
    _buy_total = 0.0
    for tx in fund.get("transactions") or []:
        tx_status = tx.get("status", "")
        if tx_status != "CONFIRMED":
            continue
        tx_type = tx.get("type", "")
        if tx_type == "BUY":
            _buy_total += tx.get("amount") or 0
        elif (tx_type == "DIVIDEND_CASH"
              and (tx.get("confirmDate") or tx.get("date")) == _effective_date):
            _cash_dividend_today += tx.get("amount") or 0
    _correction_delta = _calc_correction_delta_total(fund.get("transactions") or [])
    today_profit = _r2(today_profit + _cash_dividend_today)
    total_invested = _r2(_buy_total + _correction_delta)

    display_nav = estimated_nav if estimated_nav > 0 else official_nav

    return {
        "marketValue": market_value,
        "costPerShare": _r4(cost_per_share),
        "costTotal": cost_total,
        "holdingShares": _r6(shares),
        "holdingProfit": holding_profit,
        "realizedProfit": _r2(realized),
        "totalProfit": total_profit,
        "totalInvested": total_invested,
        "returnRate": return_rate,
        "todayProfit": today_profit,
        "currentNav": display_nav,
        "lastNav": official_nav if official_nav > 0 else None,
        "valuationAvailable": valuation_available,
        "estimatedNav": estimated_nav if estimated_nav > 0 else None,
        "estimatedChangePercent": est.get("estimatedChangePercent"),
    }


# ── Estimates 带缓存拉取（60s TTL，多工具共享，避免重复网络请求）──────────────────────

# 并发控制：限制同时请求后端的批次数量，避免触发速率限制
_estimate_semaphore = asyncio.Semaphore(3)

async def _fetch_estimates(codes: list) -> dict:
    """
    批量获取今日估算数据，60s 内存缓存。
    get_records() 和 get_item_estimate() 共用此函数，同 session 内不重复请求。
    缓存超过 500 条时自动清空，防止长时间运行内存膨胀。
    source='timeout' 的结果不写入缓存，避免后端瞬时超时污染后续请求。
    """
    now = time.monotonic()

    # 分离缓存命中 vs 需要请求
    result: dict = {}
    miss_codes: list = []
    for code in codes:
        entry = _estimate_cache.get(code)
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
            return await _post("/api/estimate/batch", {"codes": batch})

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
                    _estimate_cache[code_key] = {"data": item, "ts": now}
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
            ],
            "market": [
                "search_item",
                "get_item_estimate",
                "get_item_detail",
                "get_item_history",
                "get_item_dividends",
                "get_fund_timeline",
                "get_fund_fees",
                "get_fund_period_rank",
                "get_batch_fund_period_ranks",
                "get_fund_profile",
                "get_batch_fund_profiles",
                "get_night_estimate",
                "get_daily_rank",
                "get_status",
                "get_overview",
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
                "sync_community_returns",
                "follow_community_user",
            ],
            "trade": ["request_transaction", "get_agent_requests", "update_agent_request"],
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
async def get_item_estimate(codes: list[str]) -> dict:
    """
    批量获取项目今日实时估算净值（最多 50 个）。
    适合查询"现在涨了多少""今天净值多少"等日常行情问题，比 get_item_detail 轻量得多。
    结果在同一 session 内缓存 60 秒，与 get_records 共享缓存，无重复网络请求。

    Args:
        codes: 项目编号列表，如 ["000001", "110022"]，最多 50 个
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
    estimate_map = await _fetch_estimates(validated_codes)
    return {"data": list(estimate_map.values())}


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
async def get_fund_timeline(code: str) -> list:
    """
    获取指定项目今日分时估值走势（每隔几分钟一个数据点，盘中更新）。
    适合了解今日净值走势曲线，判断入场时机。
    非交易日或盘前返回空列表。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    data = await _get(f"/api/fund/today-timeline/{validated_code}")
    return data if isinstance(data, list) else []


@mcp.tool()
async def get_fund_fees(code: str) -> dict:
    """
    获取项目费率信息，包括申购费率、赎回费率、管理费率、托管费率等。
    在制定买卖决策时可参考手续费成本。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/fees/{validated_code}")


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
    return await _get("/api/market/overview")


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
    data = await _get("/api/market/indices")
    return data if isinstance(data, list) else []


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
async def get_night_estimate(codes: list[str], force: bool = False) -> dict:
    """
    获取QDII基金的夜间实时估值（美股/港股盘后/盘前交易时段）。
    返回每只基金的盘后涨跌幅、持仓穿透明细、汇率变动等数据。
    仅在美股交易时段（北京时间夜间）数据有效，需要会员权限。

    Args:
        codes: 基金代码列表，如 ["016665", "018147"]，最多 50 个
        force: 是否强制刷新（跳过服务端缓存），默认 false
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
    return await _get("/api/market/night-est", params=params)


@mcp.tool()
async def get_night_watchlist() -> dict:
    """
    获取用户在 App「夜盘估值」页面手动添加的基金代码列表。

    数据来自最近一次云同步快照的 nightWatchCodes 字段；典型用法是把
    返回的 codes 作为参数传给 get_night_estimate，实现 "拉取用户自选
    夜盘基金的最新估值" 的端到端调用，无需用户在对话中手动报代码。

    Returns:
        dict 包含：
        - codes: 用户添加的 6 位基金代码列表（list[str]）
        - count: 代码数量
        - has_customized: 用户是否自定义过（False 表示用户从未修改，
          App 端会回退到内置默认列表；此时返回的 codes 为空，Agent
          可以提示用户先去 App 添加夜盘自选）
        - dataUpdatedAt: 云同步快照时间
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
    下载云同步数据并解析 JSON。
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

        raw = await _get("/api/sync/download")
        parsed = _unwrap_sync_payload(raw if isinstance(raw, dict) else {})
        _portfolio_cache["data"] = parsed
        _portfolio_cache["ts"] = now
        return parsed


@mcp.tool()
async def get_sync_meta() -> dict:
    """
    获取云端同步快照元信息，不下载完整数据。
    返回 updated_at、etag、size_bytes，用于判断 App 数据是否已经同步到云端。
    """
    _require_token()
    return await _get("/api/sync/meta")


@mcp.tool()
async def get_raw_sync_data(include_json_text: bool = False) -> dict:
    """
    获取完整云同步快照。默认返回解析后的 JSON，不返回原始 JSON 字符串以节省上下文。

    云同步快照包含 funds、groups、watchlistGroups、globalTags、字段显示配置等。
    profit ledger 是 App 可由交易记录和历史净值重建的派生数据；当前云同步快照通常不包含 ledger。

    Args:
        include_json_text: 是否同时返回服务端原始 json_data 字符串；只有做备份/迁移时才建议开启。
    """
    _require_token()
    raw = await _get("/api/sync/download")
    parsed = _unwrap_sync_payload(raw if isinstance(raw, dict) else {})
    result = {
        "data": {k: v for k, v in parsed.items() if not k.startswith("_meta_")},
        "meta": {
            "updated_at": parsed.get("_meta_updated_at", ""),
            "etag": parsed.get("_meta_etag", ""),
            "size_bytes": parsed.get("_meta_size_bytes", 0),
            "contains_ledger": "ledger" in parsed,
        },
    }
    if include_json_text:
        result["json_data"] = raw.get("json_data", "") if isinstance(raw, dict) else ""
    return result


@mcp.tool()
async def get_transactions(code: str = "", include_pending: bool = True) -> dict:
    """
    获取云同步快照中的交易流水。默认返回全部基金；传入 code 时只返回该基金。

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
    获取用户持仓记录，并自动计算今日收益、累计收益、市值、收益率等字段。
    需要 Agent Token 且账号需开通会员才能使用云同步功能。

    数据来自最近一次云同步（dataUpdatedAt 字段）。若刚在 App 中刷新了净值或新增了交易，
    请先在 App 设置页手动触发"立即同步"后再查询，以获取最新数据。

    返回结构：
    - holdings: 有持仓的记录列表（含实时收益计算）
    - watchlist: 观察列记录（无持仓，仅供参考）
    - summary: 持仓汇总（总市值/今日收益/持有收益/持有收益率/累计收益/收益率/在途金额）
      - totalHoldingProfit: 持有收益总额（市值 - 成本，不含落袋/已实现收益）
      - totalHoldingReturnRate: 持有收益率（totalHoldingProfit / totalCost × 100%，仅反映浮动亏盈）
      - cumulativeProfit: 累计收益（持有收益 + 已实现收益，含落袋）
      - totalReturnRate: 累计收益率（cumulativeProfit / totalCost × 100%，含落袋，综合回报率）
      注意：totalReturnRate ≠ totalHoldingReturnRate，前者含已实现收益，后者仅持仓浮动
    - dataUpdatedAt: 云同步数据的最后更新时间（UTC），展示给用户让其知晓数据新鲜度

    Args:
        include_transactions: 是否在每条记录中附带原始 transactions。默认 false 以节省上下文。
            需要审计交易流水、重算收益或排查数据时设为 true。
    """
    _require_token()
    # 1. 下载记录（有缓存时直接复用）
    portfolio = await _download_portfolio()
    funds: list = portfolio.get("funds", [])
    data_updated_at: str = portfolio.get("_meta_updated_at", "")

    # 2. 找出有持仓的项目编号
    held_codes = [f["code"] for f in funds if (f.get("holdingShares") or 0) > 0]

    # 3. 并行批量获取今日估算数值（共享 60s 缓存）
    estimate_map: dict = {}
    if held_codes:
        estimate_map = await _fetch_estimates(held_codes)

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
        in_transit_amount = _r2(sum((tx.get("amount") or 0) for tx in pending_buy_txs))
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
    for f in holdings:
        total_market_value = _r2(total_market_value + f.get("marketValue", 0))
        total_cost = _r2(total_cost + f.get("costTotal", 0))
        total_today_profit = _r2(total_today_profit + f.get("todayProfit", 0))
        total_holding_profit = _r2(total_holding_profit + f.get("holdingProfit", 0))
        total_cumulative_profit = _r2(total_cumulative_profit + f.get("totalProfit", 0))
        total_in_transit = _r2(total_in_transit + f.get("inTransitAmount", 0))
        total_invested = _r2(total_invested + f.get("totalInvested", 0))
    total_return_rate = _r2_pct(total_cumulative_profit, total_invested) if total_invested > 0 else 0.0
    total_holding_return_rate = _r2_pct(total_holding_profit, total_cost)

    return {
        "holdings": holdings,
        "watchlist": watchlist,
        "groups": portfolio.get("groups", []),
        "summary": {
            "totalMarketValue": total_market_value,
            "totalCost": total_cost,
            "todayProfit": total_today_profit,
            "totalHoldingProfit": total_holding_profit,
            "totalHoldingReturnRate": total_holding_return_rate,
            "cumulativeProfit": total_cumulative_profit,
            "totalInvested": total_invested,
            "totalReturnRate": total_return_rate,
            "heldItemCount": len(holdings),
            "totalInTransitAmount": total_in_transit,
        },
        "dataUpdatedAt": data_updated_at,
    }


@mcp.tool()
async def get_summary() -> dict:
    """
    获取持仓总览摘要（总市值、今日收益、累计收益、收益率）。
    输出比 get_records 更精简（不含每只基金明细），适合快速查询资产概况。

    返回的 dataUpdatedAt 字段表示云同步数据的更新时间，请将此时间告知用户，
    让其了解数据是否为最新（若时间较旧，提示用户在 App 触发同步）。
    """
    _require_token()
    result = await get_records()
    summary = result.get("summary", {})
    summary["dataUpdatedAt"] = result.get("dataUpdatedAt", "")
    return summary


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
async def sync_community_returns(
    weekly_return: float,
    monthly_return: float,
    total_return: float,
    fund_count: int,
    top_fund_code: str = "",
    top_fund_name: str = "",
) -> dict:
    """
    将用户收益率数据同步到喵舍社区，用于排行榜排名。
    通常由 App 自动调用；Agent 可在用户明确要求刷新排名时手动触发。

    Args:
        weekly_return: 近一周收益率（百分比数值，如 5.2 表示 +5.2%）
        monthly_return: 近一月收益率
        total_return: 累计总收益率
        fund_count: 持仓基金数量
        top_fund_code: 第一重仓基金代码（可选）
        top_fund_name: 第一重仓基金名称（可选）
    """
    _require_token()
    return await _post("/api/community/sync-returns", {
        "weekly_return": weekly_return,
        "monthly_return": monthly_return,
        "total_return": total_return,
        "fund_count": fund_count,
        "top_fund_code": top_fund_code,
        "top_fund_name": top_fund_name,
    })


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
