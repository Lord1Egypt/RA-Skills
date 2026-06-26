#!/usr/bin/env python3
"""
MEXC contract funding-rate arbitrage (core-only version).

Behavior:
- Scans all API-enabled active USDT perpetual contracts.
- Runs only when U.S. regular stock session is closed.
- Opens market position a few seconds before funding settlement.
- Closes market position immediately after settlement.
- Direction follows funding sign:
  fundingRate > 0 -> open short (receive funding)
  fundingRate < 0 -> open long  (receive funding)

Important:
- Uses MEXC contract_v1 API: https://contract.mexc.com
- Order endpoint in docs is marked "Under maintenance"; availability depends on account/exchange status.

中文说明：
- 仅实现核心策略：美股常规盘停盘时运行，结算前几秒开仓，结算后立即平仓。
- 资金费率 > 0 时优先开空，资金费率 < 0 时优先开多。
- 触发时序采用“分段休眠 + 最后几毫秒忙等待”提升精度。
"""

import hashlib
import hmac
import json
import math
import os
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, time as dtime
from zoneinfo import ZoneInfo


# ===== 基础配置 =====
BASE_URL = os.getenv("MEXC_CONTRACT_BASE_URL", "https://contract.mexc.com")
API_KEY = os.getenv("MEXC_API_KEY", "").strip()
API_SECRET = os.getenv("MEXC_API_SECRET", "").strip()

TZ_NAME = os.getenv("BOT_TIMEZONE", "Asia/Shanghai")
LOOP_INTERVAL_SEC = float(os.getenv("LOOP_INTERVAL_SEC", "1.0"))

# 开仓提前秒数 / 平仓滞后秒数
OPEN_LEAD_SEC = float(os.getenv("OPEN_LEAD_SEC", "3"))
CLOSE_LAG_SEC = float(os.getenv("CLOSE_LAG_SEC", "2"))

ORDER_VOL = float(os.getenv("ORDER_VOL", "1"))
LEVERAGE = int(os.getenv("LEVERAGE", "100"))
# 每个仓位使用本金的保证金比例（默认 10%）
POSITION_MARGIN_RATIO = float(os.getenv("POSITION_MARGIN_RATIO", "0.10"))
# 本金（USDT）。>0 使用固定本金；<=0 自动读取账户 USDT 可用余额。
PRINCIPAL_USDT = float(os.getenv("PRINCIPAL_USDT", "0"))
PRINCIPAL_REFRESH_SEC = int(os.getenv("PRINCIPAL_REFRESH_SEC", "60"))
OPEN_TYPE = int(os.getenv("OPEN_TYPE", "2"))  # 1逐仓, 2全仓
POSITION_MODE = int(os.getenv("POSITION_MODE", "2"))  # 1双向, 2单向

RECV_WINDOW_MS = int(os.getenv("RECV_WINDOW_MS", "10000"))
HTTP_TIMEOUT_SEC = float(os.getenv("HTTP_TIMEOUT_SEC", "10"))

# 控制请求节奏，降低触发限频风险（funding 接口文档示例：20次/2秒）
FUNDING_REQ_GAP_SEC = float(os.getenv("FUNDING_REQ_GAP_SEC", "0.12"))
DETAIL_REFRESH_SEC = int(os.getenv("DETAIL_REFRESH_SEC", "600"))
FUNDING_REFRESH_SEC = int(os.getenv("FUNDING_REFRESH_SEC", "30"))
# 与交易所时钟偏移（毫秒），本地时钟慢可设正值，快可设负值
TIME_OFFSET_MS = int(os.getenv("TIME_OFFSET_MS", "0"))
OPEN_ARM_MS = int(os.getenv("OPEN_ARM_MS", "7000"))
CLOSE_ARM_MS = int(os.getenv("CLOSE_ARM_MS", "5000"))
# 进入忙等待阈值（最后 N 毫秒）
SPIN_THRESHOLD_MS = int(os.getenv("SPIN_THRESHOLD_MS", "5"))
MAX_PARALLEL_ORDERS = int(os.getenv("MAX_PARALLEL_ORDERS", "8"))
# 目标触发前预取 fair price（毫秒），用于减少触发瞬间额外 RTT
PRICE_PREFETCH_LEAD_MS = int(os.getenv("PRICE_PREFETCH_LEAD_MS", "300"))
# 预取/即时取价失败时，是否用 0 作为市价单 price 兜底
MARKET_PRICE_FALLBACK_ZERO = os.getenv("MARKET_PRICE_FALLBACK_ZERO", "1").strip() in (
    "1", "true", "TRUE", "yes", "YES"
)
# 开仓风险保护：最大开仓张数（<=0 表示不限制）
MAX_OPEN_VOL = float(os.getenv("MAX_OPEN_VOL", "0"))
# 开仓风险保护：最大名义金额 USDT（<=0 表示不限制）
MAX_NOTIONAL_USDT = float(os.getenv("MAX_NOTIONAL_USDT", "0"))
# 最小绝对资金费率阈值（默认 0.12% = 0.0012），低于该值不交易
MIN_ABS_FUNDING_RATE = float(os.getenv("MIN_ABS_FUNDING_RATE", "0.0012"))

# 是否仅运行股票合约（默认开启）
STOCK_ONLY = os.getenv("STOCK_ONLY", "1").strip() in ("1", "true", "TRUE", "yes", "YES")
# 默认股票合约白名单（可被环境变量 STOCK_SYMBOLS 覆盖）
DEFAULT_STOCK_SYMBOLS_CSV = (
    "SP500USDT,MRVLUSDT,NAS100USDT,NVDAUSDT,CRCLUSDT,TSLAUSDT,PAYPUSDT,MUUSDT,"
    "ACNUSDT,MSTRUSDT,MSFTUSDT,GOOGLUSDT,US30USDT,PEPUSDT,NBISUSDT,AAPLUSDT,"
    "METAUSDT,IRENUSDT,RDDTUSDT,PGUSDT,AMZNUSDT,KLACUSDT,RKLBUSDT,PLTRUSDT,"
    "CVNAUSDT,SNOWUSDT,COINUSDT,LINUSDT,HOODUSDT,QQQUSDT,ORCLUSDT,SNDKUSDT,"
    "CRWVUSDT,STXSTOCKUSDT,INTCUSDT,XOMUSDT,FUTUUSDT,GEUSDT,AMDUSDT,AMATUSDT,"
    "TSMUSDT,COHRUSDT,SPOTUSDT,SHOPUSDT,CSCOUSDT,IBMUSDT,PANWUSDT,OXYUSDT,"
    "WDCUSDT,MCDUSDT,NFLXUSDT,AVGOUSDT,SMCIUSDT,INTUUSDT,ARMUSDT,COPUSDT,"
    "LMTUSDT,COSTUSDT,CVXSTOCKUSDT,ONDSUSDT,BBAIUSDT,HIMSUSDT,GEVUSDT,MAUSDT,"
    "BABAUSDT,UBERUSDT,JDUSDT,ACHRUSDT,PDDUSDT,ASMLUSDT,LLYUSDT,NOWUSDT,"
    "ABBVUSDT,FIGUSDT,EWJUSDT,HK50,KOUSDT,LRCXUSDT,MELIUSDT,RTXSTOCKUSDT,"
    "CRWDUSDT,JPMUSDT,GSUSDT,QCOMUSDT,WMTUSDT,NKEUSDT,CRMUSDT,VUSDT,UNHUSDT,"
    "PYPLUSDT,VRTUSDT,ADBEUSDT,VZUSDT,BACUSDT,BAUSDT"
)
# 显式指定股票合约白名单，逗号分隔，例如: AAPLSTOCK_USDT,TSLASTOCK_USDT
STOCK_SYMBOLS_RAW = os.getenv("STOCK_SYMBOLS", DEFAULT_STOCK_SYMBOLS_CSV).strip()
STOCK_SYMBOLS = {x.strip().upper() for x in STOCK_SYMBOLS_RAW.split(",") if x.strip()}
# 兜底关键词（用于自动识别）
STOCK_KEYWORDS = tuple(
    x.strip().lower()
    for x in os.getenv(
        "STOCK_KEYWORDS",
        "stock,xstock,us stock,nasdaq,nyse,spy,qqq",
    ).split(",")
    if x.strip()
)
# 常见美股标的 ticker（用于自动识别，避免仅靠“stock”关键词漏检）
DEFAULT_STOCK_TICKERS = {
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA",
    "AMD", "INTC", "ORCL", "AVGO", "NFLX", "COIN", "PLTR", "MSTR",
    "HOOD", "UBER", "DIS", "NKE", "WMT", "COST", "JPM", "BAC",
    "SPY", "QQQ",
}

# NYSE 官方节假日/提前收盘（来源：https://www.nyse.com/trade/hours-calendars）
# 维护范围：2026-2028，可通过环境变量追加覆盖。
NYSE_HOLIDAYS_CSV = (
    "2026-01-01,2026-01-19,2026-02-16,2026-04-03,2026-05-25,2026-06-19,"
    "2026-07-03,2026-09-07,2026-11-26,2026-12-25,"
    "2027-01-01,2027-01-18,2027-02-15,2027-03-26,2027-05-31,2027-06-18,"
    "2027-07-05,2027-09-06,2027-11-25,2027-12-24,"
    "2028-01-17,2028-02-21,2028-04-14,2028-05-29,2028-06-19,2028-07-04,"
    "2028-09-04,2028-11-23,2028-12-25"
)
NYSE_EARLY_CLOSE_CSV = "2026-11-27,2026-12-24,2027-11-26,2028-07-03,2028-11-24"
EXTRA_NYSE_HOLIDAYS = os.getenv("EXTRA_NYSE_HOLIDAYS", "").strip()
EXTRA_NYSE_EARLY_CLOSES = os.getenv("EXTRA_NYSE_EARLY_CLOSES", "").strip()


def parse_date_set(csv_text: str) -> set[date]:
    out = set()
    for raw in csv_text.split(","):
        s = raw.strip()
        if not s:
            continue
        try:
            out.add(date.fromisoformat(s))
        except Exception:
            continue
    return out


NYSE_HOLIDAY_DATES = parse_date_set(NYSE_HOLIDAYS_CSV) | parse_date_set(EXTRA_NYSE_HOLIDAYS)
NYSE_EARLY_CLOSE_DATES = parse_date_set(NYSE_EARLY_CLOSE_CSV) | parse_date_set(EXTRA_NYSE_EARLY_CLOSES)
STATE_FILE = os.getenv(
    "STATE_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "funding_arb_state.json"),
)


def cycle_key(symbol: str, settle_ms: int) -> str:
    return f"{symbol}|{int(settle_ms)}"


def load_opened_state() -> dict:
    """
    从本地状态文件恢复未平仓记录，避免重启后漏平仓。
    """
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        opened = {}
        for item in raw.get("opened", []):
            try:
                key = str(item["key"])
                opened[key] = {
                    "key": key,
                    "symbol": str(item["symbol"]),
                    "settle_ms": int(item["settle_ms"]),
                    "close_at_ms": int(item["close_at_ms"]),
                    "vol": float(item["vol"]),
                    "close_side": int(item["close_side"]),
                    "open_order_id": int(item.get("open_order_id", 0)),
                    "open_side": int(item.get("open_side", 0)),
                    "fr": float(item.get("fr", 0)),
                }
            except Exception:
                continue
        return opened
    except Exception as e:
        log(f"STATE_LOAD_FAIL file={STATE_FILE} err={e}")
        return {}


def save_opened_state(opened: dict) -> None:
    """
    原子写入状态文件，记录当前未平仓记录。
    """
    payload = {"version": 1, "opened": list(opened.values())}
    tmp = f"{STATE_FILE}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=True, separators=(",", ":"))
        os.replace(tmp, STATE_FILE)
    except Exception as e:
        log(f"STATE_SAVE_FAIL file={STATE_FILE} err={e}")


def log(msg: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", flush=True)


def now_ms() -> int:
    # 使用纳秒时钟换算毫秒，触发精度比 time.time() 更稳定
    return int(time.time_ns() // 1_000_000) + TIME_OFFSET_MS


def sleep_until_ms(target_ms: int) -> None:
    """
    Sleep in stages, then spin very briefly for high-precision trigger timing.
    中文：先粗粒度 sleep，再在最后几毫秒忙等待，尽量贴近目标时刻。
    """
    while True:
        diff = target_ms - now_ms()
        if diff <= 0:
            return
        if diff > 2000:
            time.sleep((diff - 500) / 1000.0)
            continue
        if diff > 200:
            time.sleep((diff - 50) / 1000.0)
            continue
        if diff > SPIN_THRESHOLD_MS:
            time.sleep((diff - SPIN_THRESHOLD_MS) / 1000.0)
            continue
        # 仅在最后几毫秒忙等待，避免 CPU 长时间空转。
        while now_ms() < target_ms:
            pass
        return


def is_us_regular_open_now() -> bool:
    """
    判断美股常规盘是否开盘（不含盘前盘后）：
    - 普通交易日：周一至周五 09:30-16:00 (America/New_York)
    - 提前收盘日：周一至周五 09:30-13:00 (America/New_York)
    - 全日休市：返回 False
    """
    ny_now = datetime.now(ZoneInfo("America/New_York"))
    ny_date = ny_now.date()

    # 节假日全日休市
    if ny_date in NYSE_HOLIDAY_DATES:
        return False

    if ny_now.weekday() >= 5:
        return False

    t = ny_now.time()
    close_t = dtime(13, 0) if ny_date in NYSE_EARLY_CLOSE_DATES else dtime(16, 0)
    return dtime(9, 30) <= t < close_t


def is_in_run_window() -> bool:
    """
    整周停盘窗口：仅在美股“常规盘关闭”时运行。
    已接入 NYSE 节假日和提前收盘日历（内置 2026-2028，可用环境变量追加）。
    """
    return not is_us_regular_open_now()


def http_request(method: str, path: str, params=None, body=None, private: bool = False):
    params = params or {}
    query = urllib.parse.urlencode(params, doseq=True)
    url = f"{BASE_URL}{path}" + (f"?{query}" if query else "")

    body_bytes = None
    headers = {}

    if body is not None:
        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=True)
        body_bytes = body_str.encode("utf-8")
        headers["Content-Type"] = "application/json"
    else:
        body_str = ""

    if private:
        if not API_KEY or not API_SECRET:
            raise RuntimeError("Missing MEXC_API_KEY or MEXC_API_SECRET")
        ts = str(now_ms())

        if method.upper() in ("GET", "DELETE"):
            sorted_items = sorted((k, v) for k, v in params.items() if v is not None)
            request_param = urllib.parse.urlencode(sorted_items)
        else:
            request_param = body_str

        # 合约签名串：ApiKey + Request-Time + 请求参数串
        sign_target = f"{API_KEY}{ts}{request_param}"
        signature = hmac.new(
            API_SECRET.encode("utf-8"),
            sign_target.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        headers["ApiKey"] = API_KEY
        headers["Request-Time"] = ts
        headers["Signature"] = signature
        headers["Recv-Window"] = str(RECV_WINDOW_MS)

    req = urllib.request.Request(url=url, data=body_bytes, headers=headers, method=method.upper())

    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTPError {e.code} {path}: {err_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"URLError {path}: {e}")


def api_get(path: str, params=None):
    return http_request("GET", path, params=params, private=False)


def api_post_private(path: str, body: dict):
    return http_request("POST", path, body=body, private=True)


def api_get_private(path: str, params=None):
    return http_request("GET", path, params=params, private=True)


def pick_symbols(contract_details):
    symbols = []
    for c in contract_details:
        try:
            if c.get("state") != 0:
                continue
            if not c.get("apiAllowed", False):
                continue
            # 仅筛选 USDT 结算合约，减少不必要品种
            if c.get("settleCoin") != "USDT":
                continue
            if STOCK_ONLY and not is_stock_contract(c):
                continue
            symbol = c.get("symbol")
            if not symbol:
                continue
            symbols.append(
                {
                    "symbol": symbol,
                    "minVol": float(c.get("minVol", 1)),
                    "volScale": int(c.get("volScale", 0)),
                    "contractSize": float(c.get("contractSize", 1) or 1),
                }
            )
        except Exception:
            continue
    return symbols


def is_stock_contract(contract: dict) -> bool:
    """
    股票合约识别逻辑（按优先级）：
    1) 如果设置了 STOCK_SYMBOLS，仅匹配白名单；
    2) 否则先用 ticker 判断，再用文本关键词兜底。
    """
    symbol = str(contract.get("symbol", "")).upper()
    if not symbol:
        return False

    if STOCK_SYMBOLS:
        return symbol in STOCK_SYMBOLS

    # 去掉下划线后统一判断，例如 BTC_USDT -> BTCUSDT
    flat_symbol = symbol.replace("_", "")
    if flat_symbol.endswith("USDT"):
        root = flat_symbol[:-4]
        if root in DEFAULT_STOCK_TICKERS:
            return True

    text = " ".join(
        str(contract.get(k, ""))
        for k in ("symbol", "displayName", "displayNameEn", "baseCoin", "underlyingSymbol", "indexCoin")
    ).lower()
    return any(k in text for k in STOCK_KEYWORDS)


def normalize_vol(vol: float, min_vol: float, vol_scale: int) -> float:
    v = max(vol, min_vol)
    scale = 10 ** max(vol_scale, 0)
    v = math.floor(v * scale) / scale
    if v < min_vol:
        v = min_vol
    return float(f"{v:.{max(vol_scale,0)}f}")


def get_contracts():
    r = api_get("/api/v1/contract/detail")
    if not r.get("success"):
        raise RuntimeError(f"contract/detail failed: {r}")
    data = r.get("data") or []
    return pick_symbols(data)


def get_funding(symbol: str):
    r = api_get(f"/api/v1/contract/funding_rate/{symbol}")
    if not r.get("success"):
        raise RuntimeError(f"funding_rate failed {symbol}: {r}")
    return r.get("data") or {}


def get_fair_price(symbol: str) -> float:
    r = api_get(f"/api/v1/contract/fair_price/{symbol}")
    if not r.get("success"):
        raise RuntimeError(f"fair_price failed {symbol}: {r}")
    return float((r.get("data") or {}).get("fairPrice", 0))


def get_principal_usdt_from_account() -> float:
    """
    读取合约账户 USDT 资产（优先可用余额）。
    """
    r = api_get_private("/api/v1/private/account/assets")
    if not r.get("success") or r.get("code") != 0:
        raise RuntimeError(f"account/assets failed: {r}")

    data = r.get("data")
    rows = []
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("list") or data.get("assets") or []

    for it in rows:
        cur = str(it.get("currency") or it.get("coin") or it.get("asset") or "").upper()
        if cur != "USDT":
            continue
        for k in ("availableBalance", "available", "balance", "equity"):
            if k in it:
                try:
                    return float(it[k])
                except Exception:
                    continue

    raise RuntimeError("USDT asset not found in account/assets response")


def submit_market_order(
    symbol: str,
    side: int,
    vol: float,
    reduce_only: bool = False,
    price: float | None = None,
) -> int:
    # type=5 为市价单；优先使用预取 price，未提供时再实时请求 fairPrice
    fair_price = float(price) if price is not None else get_fair_price(symbol)
    payload = {
        "symbol": symbol,
        "price": fair_price if fair_price > 0 else 0,
        "vol": vol,
        "side": side,
        "type": 5,  # market order
        "openType": OPEN_TYPE,
        "positionMode": POSITION_MODE,
    }
    if not reduce_only:
        payload["leverage"] = LEVERAGE
    if reduce_only:
        payload["reduceOnly"] = True

    r = api_post_private("/api/v1/private/order/submit", payload)
    if not r.get("success") or r.get("code") != 0:
        raise RuntimeError(f"order submit failed: {r}")

    order_id = int(r.get("data")) if r.get("data") is not None else 0
    return order_id


def open_close_sides_by_funding(funding_rate: float):
    # MEXC side: 1开多, 2平空, 3开空, 4平多
    # 策略方向：费率正开空，费率负开多
    if funding_rate > 0:
        return 3, 2  # open short before settle, close short after settle
    if funding_rate < 0:
        return 1, 4  # open long before settle, close long after settle
    return None, None


def prefetch_prices_for_actions(actions):
    """
    为动作批次并发预取 fair price，减少触发瞬间 RTT。
    返回: {symbol: price}
    """
    if not actions:
        return {}

    symbols = sorted({a["symbol"] for a in actions})
    max_workers = max(1, min(MAX_PARALLEL_ORDERS, len(symbols)))
    out = {}

    def worker(symbol):
        try:
            return symbol, get_fair_price(symbol), None
        except Exception as e:
            return symbol, None, str(e)

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        fut_map = {ex.submit(worker, s): s for s in symbols}
        for fut in as_completed(fut_map):
            symbol, price, err = fut.result()
            if price is not None:
                out[symbol] = price
            else:
                log(f"PREFETCH_FAIL {symbol} err={err}")
    return out


def execute_order_batch(batch_actions):
    """
    并发执行同一触发时刻的动作，减少串行等待导致的时序偏差。
    batch_actions item:
      - kind: "open" | "close"
      - symbol, side, vol, key, target_ms, settle_ms(optional for open), fr(optional for open)
      - reduce_only(bool)
      - close_side(optional for open)
    """

    def worker(action):
        kind = action["kind"]
        send_ms = now_ms()

        if kind == "open" and send_ms >= action["settle_ms"]:
            return {
                "ok": False,
                "action": action,
                "reason": "miss_open",
                "delay_ms": send_ms - action["settle_ms"],
            }

        price = action.get("prefetched_price")
        if price is None:
            try:
                price = get_fair_price(action["symbol"])
            except Exception as e:
                if MARKET_PRICE_FALLBACK_ZERO:
                    price = 0.0
                    log(f"PRICE_FALLBACK_ZERO {action['symbol']} reason={e}")
                else:
                    raise
        try:
            price = float(price)
        except Exception:
            price = 0.0

        # 开仓前二次校验，避免“取价期间跨过结算”仍继续下单
        pre_submit_ms = now_ms()
        if kind == "open" and pre_submit_ms >= action["settle_ms"]:
            return {
                "ok": False,
                "action": action,
                "reason": "miss_open",
                "delay_ms": pre_submit_ms - action["settle_ms"],
            }

        # 开仓量按“本金 * 保证金比例”计算（默认 10%）
        if kind == "open":
            if price <= 0:
                return {
                    "ok": False,
                    "action": action,
                    "reason": "invalid_price",
                    "error": "open price <= 0",
                }
            principal = float(action.get("principal_usdt") or 0)
            if principal <= 0:
                return {
                    "ok": False,
                    "action": action,
                    "reason": "no_principal",
                    "error": "principal_usdt unavailable",
                }
            margin_usdt = principal * float(action.get("position_margin_ratio", POSITION_MARGIN_RATIO))
            if margin_usdt <= 0:
                return {
                    "ok": False,
                    "action": action,
                    "reason": "invalid_margin_ratio",
                    "error": "position_margin_ratio <= 0",
                }
            contract_size = max(1e-12, float(action.get("contractSize", 1) or 1))
            denom = max(1e-12, float(price) * contract_size)
            raw_vol = (margin_usdt * LEVERAGE) / denom
            action["vol"] = normalize_vol(
                raw_vol,
                float(action.get("minVol", 1)),
                int(action.get("volScale", 0)),
            )
            if MAX_OPEN_VOL > 0 and float(action["vol"]) > MAX_OPEN_VOL:
                return {
                    "ok": False,
                    "action": action,
                    "reason": "risk_guard",
                    "error": f"vol {action['vol']} > MAX_OPEN_VOL {MAX_OPEN_VOL}",
                }
            notional_usdt = float(action["vol"]) * float(price) * contract_size
            if MAX_NOTIONAL_USDT > 0 and notional_usdt > MAX_NOTIONAL_USDT:
                return {
                    "ok": False,
                    "action": action,
                    "reason": "risk_guard",
                    "error": (
                        f"notional {notional_usdt:.6f} > MAX_NOTIONAL_USDT {MAX_NOTIONAL_USDT}"
                    ),
                }

        oid = submit_market_order(
            action["symbol"],
            action["side"],
            action["vol"],
            reduce_only=action["reduce_only"],
            price=price,
        )
        ack_ms = now_ms()
        return {
            "ok": True,
            "action": action,
            "order_id": oid,
            "send_ms": pre_submit_ms,
            "ack_ms": ack_ms,
        }

    results = []
    if not batch_actions:
        return results

    max_workers = max(1, min(MAX_PARALLEL_ORDERS, len(batch_actions)))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        fut_map = {ex.submit(worker, a): a for a in batch_actions}
        for fut in as_completed(fut_map):
            action = fut_map[fut]
            try:
                results.append(fut.result())
            except Exception as e:
                results.append(
                    {
                        "ok": False,
                        "action": action,
                        "reason": "exception",
                        "error": str(e),
                    }
                )
    return results


def main():
    if not API_KEY or not API_SECRET:
        log("Please set MEXC_API_KEY and MEXC_API_SECRET first.")
        sys.exit(1)

    log(
        "Starting bot. "
        f"timezone={TZ_NAME}, run_when_us_regular_closed=True"
    )
    log(
        "Config: "
        f"open_lead={OPEN_LEAD_SEC}s, close_lag={CLOSE_LAG_SEC}s, "
        f"order_vol={ORDER_VOL}, leverage={LEVERAGE}, openType={OPEN_TYPE}, positionMode={POSITION_MODE}, "
        f"stock_only={STOCK_ONLY}, min_abs_funding_rate={MIN_ABS_FUNDING_RATE}"
    )
    log(
        f"Sizing: position_margin_ratio={POSITION_MARGIN_RATIO}, "
        f"principal_usdt={'AUTO' if PRINCIPAL_USDT <= 0 else PRINCIPAL_USDT}"
    )
    if STOCK_SYMBOLS:
        log(f"Stock whitelist enabled: {len(STOCK_SYMBOLS)} symbols")
    log(
        "Precision: "
        f"time_offset_ms={TIME_OFFSET_MS}, open_arm_ms={OPEN_ARM_MS}, "
        f"close_arm_ms={CLOSE_ARM_MS}, spin_threshold_ms={SPIN_THRESHOLD_MS}, "
        f"price_prefetch_lead_ms={PRICE_PREFETCH_LEAD_MS}, "
        f"price_fallback_zero={MARKET_PRICE_FALLBACK_ZERO}"
    )
    log(
        f"Risk guards: max_open_vol={MAX_OPEN_VOL}, max_notional_usdt={MAX_NOTIONAL_USDT}"
    )
    log(
        f"NYSE calendar loaded: holidays={len(NYSE_HOLIDAY_DATES)}, "
        f"early_closes={len(NYSE_EARLY_CLOSE_DATES)}"
    )
    log(f"State file: {STATE_FILE}")

    contracts = []
    last_detail_refresh = 0

    funding_cache = {}
    last_funding_refresh = 0
    principal_usdt = PRINCIPAL_USDT
    last_principal_refresh = 0.0

    # 未平仓状态（持久化），key = f"{symbol}|{settle_ms}"
    opened = load_opened_state()
    if opened:
        log(f"Recovered opened state: {len(opened)} positions from {STATE_FILE}")

    while True:
        try:
            in_window = is_in_run_window()
            if (not in_window) and (not opened):
                if int(time.time()) % 60 == 0:
                    log("Out of run window, strategy is idle. Waiting for next window...")
                time.sleep(1)
                continue
            if (not in_window) and opened and int(time.time()) % 60 == 0:
                log("Out of run window, close-only mode for recovered/open positions.")

            now = time.time()

            if PRINCIPAL_USDT <= 0 and (
                principal_usdt <= 0 or (now - last_principal_refresh) >= PRINCIPAL_REFRESH_SEC
            ):
                try:
                    principal_usdt = get_principal_usdt_from_account()
                    last_principal_refresh = now
                    log(f"Principal refreshed from account: {principal_usdt:.6f} USDT")
                except Exception as e:
                    log(f"PRINCIPAL_FETCH_FAIL err={e}")

            if in_window:
                if (now - last_detail_refresh) >= DETAIL_REFRESH_SEC or not contracts:
                    contracts = get_contracts()
                    last_detail_refresh = now
                    log(f"Loaded symbols: {len(contracts)}")

                if (now - last_funding_refresh) >= FUNDING_REFRESH_SEC or not funding_cache:
                    tmp = {}
                    for c in contracts:
                        s = c["symbol"]
                        try:
                            tmp[s] = get_funding(s)
                        except Exception as e:
                            log(f"funding fetch failed for {s}: {e}")
                        time.sleep(FUNDING_REQ_GAP_SEC)
                    funding_cache = tmp
                    last_funding_refresh = now
                    log(f"Funding refreshed: {len(funding_cache)} symbols")

            open_actions = []
            close_actions = []
            opened_symbols = {v["symbol"] for v in opened.values()}

            if in_window:
                for c in contracts:
                    now_ms_val = now_ms()
                    symbol = c["symbol"]
                    fd = funding_cache.get(symbol)
                    if not fd:
                        continue

                    try:
                        fr = float(fd.get("fundingRate", 0))
                        settle_ms = int(fd.get("nextSettleTime", 0))
                    except Exception:
                        continue

                    if settle_ms <= 0:
                        continue
                    if abs(fr) < MIN_ABS_FUNDING_RATE:
                        continue

                    key = cycle_key(symbol, settle_ms)
                    open_side, close_side = open_close_sides_by_funding(fr)
                    if open_side is None:
                        continue

                    open_at = settle_ms - int(OPEN_LEAD_SEC * 1000)
                    close_at = settle_ms + int(CLOSE_LAG_SEC * 1000)

                    # 开仓动作收集（稍后按目标时刻并发执行）
                    if key not in opened and now_ms_val < settle_ms:
                        # 单向模式下，同一 symbol 仅允许一个未平仓周期，避免重叠仓位
                        if symbol in opened_symbols:
                            continue
                        if POSITION_MARGIN_RATIO <= 0:
                            continue
                        until_open_ms = open_at - now_ms_val
                        if until_open_ms <= OPEN_ARM_MS:
                            open_actions.append(
                                {
                                    "kind": "open",
                                    "key": key,
                                    "symbol": symbol,
                                    "side": open_side,
                                    "close_side": close_side,
                                    "vol": None,
                                    "reduce_only": False,
                                    "target_ms": open_at,
                                    "settle_ms": settle_ms,
                                    "close_at_ms": close_at,
                                    "fr": fr,
                                    "principal_usdt": None,  # 运行时动态注入
                                    "position_margin_ratio": float(POSITION_MARGIN_RATIO),
                                    "minVol": float(c["minVol"]),
                                    "volScale": int(c["volScale"]),
                                    "contractSize": float(c.get("contractSize", 1) or 1),
                                }
                            )

            # 平仓动作由已开仓状态驱动，不依赖最新 funding 的 nextSettleTime
            now_ms_val = now_ms()
            for key, st in list(opened.items()):
                until_close_ms = int(st["close_at_ms"]) - now_ms_val
                if until_close_ms <= CLOSE_ARM_MS:
                    close_actions.append(
                        {
                            "kind": "close",
                            "key": key,
                            "symbol": st["symbol"],
                            "side": int(st["close_side"]),
                            "vol": float(st["vol"]),
                            "reduce_only": True,
                            "target_ms": int(st["close_at_ms"]),
                            "settle_ms": int(st["settle_ms"]),
                        }
                    )

            all_actions = open_actions + close_actions
            if all_actions:
                actions_by_target = {}
                for a in all_actions:
                    actions_by_target.setdefault(a["target_ms"], []).append(a)

                for target_ms in sorted(actions_by_target.keys()):
                    batch = actions_by_target[target_ms]
                    for a in batch:
                        if a["kind"] == "open":
                            a["principal_usdt"] = principal_usdt
                    prefetch_at = target_ms - max(0, PRICE_PREFETCH_LEAD_MS)
                    if prefetch_at > now_ms():
                        sleep_until_ms(prefetch_at)

                    prefetched = prefetch_prices_for_actions(batch)
                    for a in batch:
                        a["prefetched_price"] = prefetched.get(a["symbol"])

                    if target_ms > now_ms():
                        sleep_until_ms(target_ms)

                    results = execute_order_batch(batch)
                    for r in results:
                        action = r["action"]
                        key = action["key"]
                        kind = action["kind"]

                        if not r.get("ok"):
                            if r.get("reason") == "miss_open":
                                log(
                                    f"MISS_OPEN {action['symbol']} settle={action['settle_ms']} "
                                    f"delay_ms={r.get('delay_ms', -1)}"
                                )
                            elif r.get("reason") in ("no_principal", "invalid_margin_ratio"):
                                log(
                                    f"OPEN_SKIP {action['symbol']} reason={r.get('reason')} "
                                    f"err={r.get('error', '')}"
                                )
                            elif r.get("reason") in ("invalid_price", "risk_guard"):
                                log(
                                    f"OPEN_BLOCK {action['symbol']} reason={r.get('reason')} "
                                    f"err={r.get('error', '')}"
                                )
                            else:
                                log(
                                    f"{kind.upper()}_FAIL {action['symbol']} "
                                    f"target={action['target_ms']} err={r.get('error', r.get('reason'))}"
                                )
                            continue

                        send_ms = int(r.get("send_ms", now_ms()))
                        ack_ms = int(r.get("ack_ms", send_ms))
                        oid = int(r["order_id"])
                        trigger_ms = send_ms - int(action["target_ms"])
                        rtt_ms = ack_ms - send_ms

                        if kind == "open":
                            opened[key] = {
                                "key": key,
                                "symbol": action["symbol"],
                                "settle_ms": int(action["settle_ms"]),
                                "close_at_ms": int(action["close_at_ms"]),
                                "vol": action["vol"],
                                "close_side": action["close_side"],
                                "open_order_id": oid,
                                "open_side": int(action["side"]),
                                "fr": float(action["fr"]),
                            }
                            save_opened_state(opened)
                            log(
                                f"OPEN {action['symbol']} fr={action['fr']:+.6f} settle={action['settle_ms']} "
                                f"side={action['side']} vol={action['vol']} order_id={oid} "
                                f"trigger_ms={trigger_ms} rtt_ms={rtt_ms}"
                            )
                        else:
                            if key in opened:
                                del opened[key]
                                save_opened_state(opened)
                            log(
                                f"CLOSE {action['symbol']} settle={action['settle_ms']} "
                                f"side={action['side']} vol={action['vol']} order_id={oid} "
                                f"trigger_ms={trigger_ms} rtt_ms={rtt_ms}"
                            )

            if all_actions:
                # 临近触发窗口时提高轮询频率，减少跨窗口延迟
                time.sleep(min(0.05, LOOP_INTERVAL_SEC))
            else:
                time.sleep(LOOP_INTERVAL_SEC)

        except KeyboardInterrupt:
            log("Stopped by user")
            return
        except Exception as e:
            log(f"Loop error: {e}")
            traceback.print_exc()
            time.sleep(2)


if __name__ == "__main__":
    main()
