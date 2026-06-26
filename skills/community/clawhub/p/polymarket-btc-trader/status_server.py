#!/usr/bin/env python3
"""
Bot 状态监控网页 - 前后端分离版
后端：提供多个 API 端点和静态文件服务
前端：public/status.html + status.css + status.js
"""

import http.server
import json
import os
import socketserver
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from urllib.parse import urlparse

PORT = 18795

# 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(BASE_DIR, "bot_status.json")
PAPER_STATE_FILE = os.path.join(BASE_DIR, "paper_trade_state.json")
CONTROL_FILE = os.path.join(BASE_DIR, "trading_control.json")
DECISION_SIGNAL_FILE = os.path.join(BASE_DIR, "decision_signal.json")
NOTIFICATIONS_FILE = os.path.join(BASE_DIR, "notifications.json")
ENV_FILE = os.path.join(BASE_DIR, ".env")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

# Polymarket CLOB API
CLOB_BASE = "https://clob.polymarket.com"
# Polymarket Data API (公开读取，不需要认证)
DATA_API_BASE = "https://data-api.polymarket.com"
GAMMA_BASE = "https://gamma-api.polymarket.com"


def load_env():
    """从 .env 文件中提取配置"""
    env = {}
    try:
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        env[k.strip()] = v.strip()
    except Exception:
        pass
    override_keys = {
        "BET_AMOUNT",
        "MAX_BET_AMOUNT",
        "MIN_PROBABILITY_DIFF",
        "STOP_LOSS_ENABLED",
        "STOP_LOSS_PERCENT",
        "TAKE_PROFIT_PERCENT",
        "TRADING_MODE",
        "PAPER_START_BALANCE",
        "PAPER_BET_AMOUNT",
        "PAPER_MIN_ENTRY_PRICE",
        "PAPER_MAX_ENTRY_PRICE",
        "PAPER_TAKE_PROFIT_USD",
        "PAPER_POLL_INTERVAL_SECONDS",
        "PAPER_MAX_OPEN_POSITIONS",
        "PAPER_MAX_SPREAD",
        "PAPER_MIN_TOP_BOOK_SIZE",
        "PAPER_MIN_MINUTES_TO_EXPIRY",
        "PAPER_MAX_NEW_POSITIONS_PER_CYCLE",
        "PAPER_MARKET_INTERVAL_MINUTES",
        "PAPER_FORWARD_SLOT_COUNT",
        "PAPER_WALLET_LABEL",
        "BTC_UPDOWN_MARKET_ID",
        "POLYMARKET_WALLET_ADDRESS",
        "AI_UP_THRESHOLD",
        "AI_DOWN_THRESHOLD",
        "AI_ENABLED",
        "AI_MODEL",
        "AI_BASE_URL",
        "AI_PROVIDER",
        "AI_DECISION_INTERVAL_SECONDS",
        "MINIMAX_API_KEY",
        "AI_ENABLED",
    }
    for key in override_keys:
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def build_hmac_headers(api_key, api_secret, passphrase, method, path, body=""):
    """构建 Polymarket L2 HMAC-SHA256 认证头"""
    import base64, hashlib, hmac as hmac_mod, time as time_mod
    timestamp = str(int(time_mod.time()))
    message = timestamp + method.upper() + path + body
    secret_decoded = base64.urlsafe_b64decode(api_secret)
    signature = base64.urlsafe_b64encode(
        hmac_mod.new(secret_decoded, message.encode('utf-8'), hashlib.sha256).digest()
    ).decode('utf-8')
    return {
        "POLY-API-KEY": api_key,
        "POLY-SIGNATURE": signature,
        "POLY-TIMESTAMP": timestamp,
        "POLY-PASSPHRASE": passphrase,
    }


def clob_get(path, env=None, timeout=10):
    """向 Polymarket CLOB API 发起带 HMAC 签名的 GET 请求"""
    env = env or {}
    api_key = env.get("POLYMARKET_API_KEY", "")
    api_secret = env.get("POLYMARKET_API_SECRET", "")
    passphrase = env.get("POLYMARKET_API_PASSPHRASE", "")

    url = f"{CLOB_BASE}{path}"
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

    # 如果有完整的 L2 凭证，使用 HMAC 签名
    if api_key and api_secret and passphrase:
        headers = build_hmac_headers(api_key, api_secret, passphrase, "GET", path)
        for k, v in headers.items():
            req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        return {"error": f"HTTP {e.code}", "detail": body}
    except Exception as e:
        return {"error": str(e)}


def data_api_get(path, timeout=10):
    """向 Polymarket Data API 发起 GET 请求（公开端点，无需认证）"""
    url = f"{DATA_API_BASE}{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        return {"error": f"HTTP {e.code}", "detail": body}
    except Exception as e:
        return {"error": str(e)}


def http_json_get(url, timeout=10):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        return {"error": f"HTTP {e.code}", "detail": body}
    except Exception as e:
        return {"error": str(e)}


def load_status_from_file():
    """从 bot_status.json 加载 Bot 状态"""
    try:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None


def load_paper_state():
    try:
        if os.path.exists(PAPER_STATE_FILE):
            with open(PAPER_STATE_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return None


def load_decision_signal():
    try:
        if os.path.exists(DECISION_SIGNAL_FILE):
            with open(DECISION_SIGNAL_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return None


def load_notifications():
    try:
        if os.path.exists(NOTIFICATIONS_FILE):
            with open(NOTIFICATIONS_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {"notifications": []}


def append_notification(event_type, title, message, details=None):
    """追加一条通知到 notifications.json"""
    notifications = load_notifications().get("notifications", [])
    notification = {
        "id": len(notifications) + 1,
        "type": event_type,
        "title": title,
        "message": message,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    notifications.insert(0, notification)
    # 保留最近 50 条
    notifications = notifications[:50]
    with open(NOTIFICATIONS_FILE, "w") as f:
        json.dump({"notifications": notifications}, f, ensure_ascii=False, indent=2)
    return notification


def load_trading_control():
    state = {"trading_enabled": True}
    try:
        if os.path.exists(CONTROL_FILE):
            with open(CONTROL_FILE, "r") as f:
                raw = json.load(f)
            state["trading_enabled"] = bool(raw.get("trading_enabled", True))
            state["updated_at"] = raw.get("updated_at")
    except Exception:
        pass
    return state


def save_trading_control(trading_enabled):
    state = {
        "trading_enabled": bool(trading_enabled),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(CONTROL_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    return state


def is_paper_mode(env):
    return env.get("TRADING_MODE", "paper").strip().lower().startswith("paper")


def get_requested_account(parsed, env):
    params = urllib.parse.parse_qs(parsed.query)
    requested = (params.get("account", ["paper" if is_paper_mode(env) else "real"])[0] or "").strip().lower()
    return "real" if requested == "real" else "paper"


def extract_market_slug(value):
    if not value:
        return ""
    if "polymarket.com/event/" in value:
        return value.split("polymarket.com/event/")[-1].split("#")[0].split("?")[0]
    return value.strip()


def parse_json_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return []
    return []


def derive_complement_price(value):
    try:
        return round(max(0.0, min(1.0, 1 - float(value))), 4)
    except Exception:
        return None


def normalize_orderbook_levels(levels, descending=False):
    normalized = []
    for level in levels or []:
        try:
            normalized.append({
                "price": round(float(level.get("price", 0)), 4),
                "size": round(float(level.get("size", 0)), 4),
            })
        except Exception:
            continue
    return sorted(normalized, key=lambda item: item["price"], reverse=descending)


def derive_display_price(last_trade_price, best_bid, best_ask):
    spread = None
    if best_bid is not None and best_ask is not None:
        spread = round(best_ask - best_bid, 4)
    if spread is not None and spread <= 0.10:
        return round((best_bid + best_ask) / 2, 4), spread
    if last_trade_price is not None:
        return round(float(last_trade_price), 4), spread
    if best_bid is not None and best_ask is not None:
        return round((best_bid + best_ask) / 2, 4), spread
    return None, spread


def get_active_market_slug(env):
    status = load_status_from_file() or {}
    if status.get("market_slug"):
        return status["market_slug"]
    paper_state = load_paper_state() or {}
    market = paper_state.get("market", {})
    if market.get("slug"):
        return market["slug"]
    return extract_market_slug(env.get("BTC_UPDOWN_MARKET_ID", ""))


def fetch_market_snapshot(slug, timeout=10):
    return http_json_get(f"{GAMMA_BASE}/markets/slug/{slug}", timeout=timeout)


def build_synthetic_orderbook(snapshot):
    outcomes = parse_json_list(snapshot.get("outcomes")) or ["UP", "DOWN"]
    up_bid = snapshot.get("bestBid")
    up_ask = snapshot.get("bestAsk")
    outcome_prices = [float(item) for item in parse_json_list(snapshot.get("outcomePrices")) or [0.5, 0.5]]
    if len(outcome_prices) < 2:
        outcome_prices = [0.5, 0.5]

    if up_bid is None:
        up_bid = round(max(0.01, float(outcome_prices[0]) - 0.01), 4)
    if up_ask is None:
        up_ask = round(min(0.99, float(outcome_prices[0]) + 0.01), 4)

    up_mid, up_spread = derive_display_price(outcome_prices[0], float(up_bid), float(up_ask))
    if up_mid is None:
        up_mid = round(float(outcome_prices[0]), 4)
    down_bid = derive_complement_price(up_ask)
    down_ask = derive_complement_price(up_bid)
    down_mid, down_spread = derive_display_price(outcome_prices[1], down_bid or 0.5, down_ask or 0.5)
    if down_mid is None:
        down_mid = round(float(outcome_prices[1]), 4)

    return {
        "source": "snapshot_fallback",
        "market": snapshot.get("question"),
        "closed": snapshot.get("closed"),
        "updated_at": snapshot.get("updatedAt"),
        "outcomes": [
            {
                "label": str(outcomes[0]).upper(),
                "mid": round(up_mid, 4),
                "best_bid": round(float(up_bid), 4),
                "best_ask": round(float(up_ask), 4),
                "spread": round(up_spread or 0.0, 4),
                "bids": [{"price": round(float(up_bid), 4), "size": snapshot.get("liquidity", "--")}],
                "asks": [{"price": round(float(up_ask), 4), "size": snapshot.get("liquidity", "--")}],
            },
            {
                "label": str(outcomes[1]).upper() if len(outcomes) > 1 else "DOWN",
                "mid": round(down_mid, 4),
                "best_bid": round(float(down_bid or max(0.01, down_mid - 0.01)), 4),
                "best_ask": round(float(down_ask or min(0.99, down_mid + 0.01)), 4),
                "spread": round(down_spread or 0.0, 4),
                "bids": [{"price": round(float(down_bid or max(0.01, down_mid - 0.01)), 4), "size": snapshot.get("liquidity", "--")}],
                "asks": [{"price": round(float(down_ask or min(0.99, down_mid + 0.01)), 4), "size": snapshot.get("liquidity", "--")}],
            },
        ],
    }


def fetch_order_book(slug, timeout=10):
    snapshot = fetch_market_snapshot(slug, timeout=timeout)
    if snapshot.get("error"):
        return snapshot

    token_ids = parse_json_list(snapshot.get("clobTokenIds"))
    outcomes = parse_json_list(snapshot.get("outcomes"))
    outcome_prices = [float(item) for item in parse_json_list(snapshot.get("outcomePrices")) or []]
    books = []
    source = "clob"

    for idx, token_id in enumerate(token_ids[:2]):
        book = http_json_get(f"{CLOB_BASE}/book?token_id={token_id}", timeout=timeout)
        label = str(outcomes[idx]).upper() if idx < len(outcomes) else f"OUTCOME {idx+1}"

        if book.get("error"):
            source = "snapshot_fallback"
            return build_synthetic_orderbook(snapshot)

        bids = normalize_orderbook_levels(book.get("bids"), descending=True)
        asks = normalize_orderbook_levels(book.get("asks"), descending=False)
        best_bid = bids[0]["price"] if bids else None
        best_ask = asks[0]["price"] if asks else None
        last_trade = outcome_prices[idx] if idx < len(outcome_prices) else None
        mid, spread = derive_display_price(last_trade, best_bid, best_ask)
        books.append({
            "label": label,
            "mid": round(float(mid), 4) if mid is not None else 0.5,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": round(spread or 0.0, 4),
            "bids": bids[:3],
            "asks": asks[:3],
        })

    return {
        "source": source,
        "market": snapshot.get("question"),
        "closed": snapshot.get("closed"),
        "updated_at": snapshot.get("updatedAt"),
        "outcomes": books,
    }


def get_btc_price():
    """从 Binance 拉取 BTC 实时价格"""
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            return {
                "price": float(data["lastPrice"]),
                "change_24h": float(data["priceChangePercent"]),
                "high_24h": float(data["highPrice"]),
                "low_24h": float(data["lowPrice"]),
                "volume_24h": float(data["volume"]),
            }
    except Exception as e:
        return {"error": str(e)}


def fetch_usdc_balance_polygonscan(wallet, env, timeout=10):
    """优先使用 Etherscan/Polygonscan V2 查询 Polygon 上的 USDC 余额。"""
    api_key = env.get("POLYGONSCAN_API_KEY") or env.get("ETHERSCAN_API_KEY") or ""
    query = urllib.parse.urlencode({
        "chainid": "137",
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "address": wallet,
        "tag": "latest",
        "apikey": api_key,
    })
    req = urllib.request.Request(f"https://api.etherscan.io/v2/api?{query}")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read().decode())

    if result.get("status") == "1" and result.get("result") is not None:
        return int(result["result"]) / 1e6, "etherscan_v2"

    raise RuntimeError(result.get("result") or result.get("message") or "余额查询失败")


def fetch_usdc_balance_rpc(wallet, timeout=10):
    """公共 Polygon RPC 兜底，避免区块浏览器接口变更导致余额无法显示。"""
    wallet_hex = wallet.lower().replace("0x", "").rjust(64, "0")
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{
            "to": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            "data": "0x70a08231" + wallet_hex,
        }, "latest"],
        "id": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://gateway.tenderly.co/public/polygon",
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read().decode())

    value = result.get("result")
    if not value:
        raise RuntimeError(result.get("error", {}).get("message", "RPC 返回为空"))
    return int(value, 16) / 1e6, "polygon_rpc"


def get_real_wallet_balance(env):
    """无论当前是否为 paper 模式，都查询真实 Polymarket 资金钱包余额。"""
    wallet = env.get("POLYMARKET_WALLET_ADDRESS", "")
    if not wallet:
        raise RuntimeError("未配置钱包地址")

    try:
        balance, source = fetch_usdc_balance_polygonscan(wallet, env)
    except Exception:
        balance, source = fetch_usdc_balance_rpc(wallet)

    return {
        "balance": balance,
        "wallet": wallet,
        "source": source,
    }


def send_json(handler, data, status=200):
    handler.send_response(status)
    handler.send_header('Content-type', 'application/json; charset=utf-8')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
    handler.send_header('Pragma', 'no-cache')
    handler.send_header('Expires', '0')
    handler.end_headers()
    handler.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))


class StatusHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def log_message(self, format, *args):
        # 安静模式，减少终端刷屏
        pass

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def read_json_body(self):
        length = int(self.headers.get('Content-Length', '0') or '0')
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode('utf-8')
        if not raw.strip():
            return {}
        return json.loads(raw)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/control':
            try:
                payload = self.read_json_body()
            except Exception as e:
                send_json(self, {"error": f"无效 JSON: {e}"}, 400)
                return

            if "trading_enabled" not in payload:
                send_json(self, {"error": "缺少 trading_enabled"}, 400)
                return

            value = payload.get("trading_enabled")
            if isinstance(value, bool):
                trading_enabled = value
            else:
                trading_enabled = str(value).strip().lower() in {"1", "true", "yes", "on"}

            send_json(self, save_trading_control(trading_enabled))
            return

        if path == '/api/notifications' and self.command == 'POST':
            self.do_PUSHNotification()
            return

        if path == '/api/notifications/clear' and self.command == 'POST':
            with open(NOTIFICATIONS_FILE, "w") as f:
                json.dump({"notifications": []}, f)
            send_json(self, {"ok": True})
            return

        send_json(self, {"error": "未找到接口"}, 404)

    def do_PUSHNotification(self):
        """POST /api/notifications - 写入通知"""
        try:
            payload = self.read_json_body()
        except Exception as e:
            send_json(self, {"error": f"无效 JSON: {e}"}, 400)
            return
        event_type = payload.get("type", "info")
        title = payload.get("title", "")
        message = payload.get("message", "")
        details = payload.get("details")
        n = append_notification(event_type, title, message, details)
        send_json(self, n)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # === Bot 状态 (从 bot_status.json) ===
        if path == '/status-json':
            data = load_status_from_file()
            send_json(self, data or {})

        # === BTC 实时价格 ===
        elif path == '/api/btc':
            send_json(self, get_btc_price())

        # === Polymarket USDC 余额 ===
        elif path == '/api/balance':
            env = load_env()
            if is_paper_mode(env):
                state = load_paper_state() or {}
                summary = state.get("summary", {})
                send_json(self, {
                    "balance": summary.get("ending_balance", float(env.get("PAPER_START_BALANCE", "100"))),
                    "wallet": state.get("wallet") or env.get("PAPER_WALLET_LABEL", "LOCAL-SIM"),
                    "source": "paper_live",
                    "cash_balance": summary.get("cash_balance"),
                    "reserved_balance": summary.get("reserved_balance"),
                    "realized_pnl": summary.get("realized_pnl"),
                    "unrealized_pnl": summary.get("unrealized_pnl"),
                })
                return

        # === Bot 真实统计（从 paper_trade_state.json 计算）===
        elif path == '/api/bot-stats':
            state = load_paper_state() or {}
            trades = state.get("trades", [])
            # 只统计 COMPLETE 且有 realized_profit 的交易
            closed = [t for t in trades if t.get("operation") == "COMPLETE" and "realized_profit" in t]
            wins = sum(1 for t in closed if t.get("realized_profit", 0) > 0)
            losses = sum(1 for t in closed if t.get("realized_profit", 0) < 0)
            total = len(closed)
            wr = round(wins / total * 100, 1) if total > 0 else 0.0
            summary = state.get("summary", {})
            send_json(self, {
                "total_trades": total,
                "winning_trades": wins,
                "losing_trades": losses,
                "win_rate": wr,
                "realized_pnl": summary.get("realized_pnl"),
                "starting_balance": summary.get("starting_balance"),
                "cash_balance": summary.get("cash_balance"),
            })

        # === 真实钱包余额（即使处于 paper 模式也返回链上现金） ===
        elif path == '/api/real-balance':
            env = load_env()
            try:
                send_json(self, get_real_wallet_balance(env))
            except Exception as e:
                send_json(self, {"error": str(e)}, 400)

        # === 交易控制状态 ===
        elif path == '/api/control':
            send_json(self, load_trading_control())

        # === 当前持仓 (Data API，公开) ===
        elif path == '/api/positions':
            env = load_env()
            account = get_requested_account(parsed, env)
            if account == 'paper':
                state = load_paper_state() or {}
                send_json(self, state.get("positions", []))
            else:
                wallet = env.get("POLYMARKET_WALLET_ADDRESS", "")
                if not wallet:
                    send_json(self, {"error": "未配置钱包地址"}, 400)
                    return
                data = data_api_get(f"/positions?user={wallet}")
                send_json(self, data)

        # === Market Order Book ===
        elif path == '/api/orderbook':
            env = load_env()
            slug = get_active_market_slug(env)
            if not slug:
                send_json(self, {"error": "未配置 market slug"}, 400)
                return
            send_json(self, fetch_order_book(slug))

        # === 最近交易 (Data API，公开) ===
        elif path == '/api/trades':
            env = load_env()
            account = get_requested_account(parsed, env)
            if account == 'paper':
                state = load_paper_state() or {}
                send_json(self, state.get("trades", []))
            else:
                wallet = env.get("POLYMARKET_WALLET_ADDRESS", "")
                if not wallet:
                    send_json(self, {"error": "未配置钱包地址"}, 400)
                    return
                data = data_api_get(f"/trades?user={wallet}&limit=20")
                send_json(self, data)

        # === AI 决策历史 ===
        elif path == '/api/ai-decisions':
            state = load_paper_state() or {}
            send_json(self, state.get("ai_history", []))

        # === OpenClaw 决策信号 ===
        elif path == '/api/decision-signal':
            signal = load_decision_signal()
            if signal:
                send_json(self, signal)
            else:
                send_json(self, {"error": "暂无 decision_signal.json"}, 404)

        # === 交易通知 ===
        elif path == '/api/notifications':
            send_json(self, load_notifications())

        # === 清除通知 ===
        elif path == '/api/notifications/clear':
            with open(NOTIFICATIONS_FILE, "w") as f:
                json.dump({"notifications": []}, f)
            send_json(self, {"ok": True})

        # === 挂单 (Data API，公开) ===
        elif path == '/api/orders':
            env = load_env()
            account = get_requested_account(parsed, env)
            if account == 'paper':
                state = load_paper_state() or {}
                send_json(self, state.get("orders", []))
            else:
                wallet = env.get("POLYMARKET_WALLET_ADDRESS", "")
                if not wallet:
                    send_json(self, {"error": "未配置钱包地址"}, 400)
                    return
                data = data_api_get(f"/activity?user={wallet}&limit=10")
                send_json(self, data)

        # === Bot 配置 (脱敏) ===
        elif path == '/api/config':
            env = load_env()
            state = load_paper_state() or {}
            report = state.get("report", {})
            summary = state.get("summary", {})
            signal = state.get("last_signal", {})
            control = load_trading_control()
            decision_signal = load_decision_signal() or {}
            config = {
                "bet_amount": env.get("BET_AMOUNT", "1"),
                "max_bet_amount": env.get("MAX_BET_AMOUNT", "10"),
                "paper_bet_amount": env.get("PAPER_BET_AMOUNT", env.get("BET_AMOUNT", "1")),
                "min_probability_diff": env.get("MIN_PROBABILITY_DIFF", "0.05"),
                "trading_mode": env.get("TRADING_MODE", "paper"),
                "take_profit_percent": env.get("TAKE_PROFIT_PERCENT", "0.18"),
                "take_profit_usd": env.get("PAPER_TAKE_PROFIT_USD", "0.12"),
                "min_entry_price": env.get("PAPER_MIN_ENTRY_PRICE", "0.15"),
                "max_entry_price": env.get("PAPER_MAX_ENTRY_PRICE", "0.60"),
                "max_spread": env.get("PAPER_MAX_SPREAD", "0.06"),
                "min_top_book_size": env.get("PAPER_MIN_TOP_BOOK_SIZE", "25"),
                "min_minutes_to_expiry": env.get("PAPER_MIN_MINUTES_TO_EXPIRY", "3"),
                "max_new_positions_per_cycle": env.get("PAPER_MAX_NEW_POSITIONS_PER_CYCLE", "1"),
                "market_interval_minutes": env.get("PAPER_MARKET_INTERVAL_MINUTES", "15"),
                "forward_slot_count": env.get("PAPER_FORWARD_SLOT_COUNT", "8"),
                "paper_start_balance": env.get("PAPER_START_BALANCE", "100"),
                "paper_max_open_positions": env.get("PAPER_MAX_OPEN_POSITIONS", "1"),
                "stop_loss_enabled": env.get("STOP_LOSS_ENABLED", "true"),
                "stop_loss_percent": env.get("STOP_LOSS_PERCENT", "0.10"),
                "market_id": (state.get("market", {}).get("slug") or env.get("BTC_UPDOWN_MARKET_ID", ""))[:32] + "...",
                "wallet": state.get("wallet") or (env.get("POLYMARKET_WALLET_ADDRESS", "")[:10] + "..."),
                "ai_up_threshold": env.get("AI_UP_THRESHOLD", "0.02"),
                "ai_down_threshold": env.get("AI_DOWN_THRESHOLD", "-0.02"),
                "paper_result": report.get("result"),
                "paper_profit": report.get("profit"),
                "paper_roi_percent": report.get("roi_percent"),
                "paper_balance": summary.get("ending_balance"),
                "paper_session_started_at": state.get("session_started_at") or summary.get("session_started_at") or report.get("session_started_at"),
                "cash_balance": summary.get("cash_balance"),
                "reserved_balance": summary.get("reserved_balance"),
                "open_positions": summary.get("open_positions"),
                "daily_open": signal.get("daily_open"),
                "signal_price": signal.get("current_price"),
                "daily_change_percent": signal.get("change_percent"),
                "signal_reason": signal.get("reason"),
                "strategy_name": report.get("strategy"),
                "ai_enabled": env.get("AI_ENABLED", "true"),
                "ai_model": signal.get("ai_model") or env.get("AI_MODEL", "gpt-4o-mini"),
                "ai_source": signal.get("ai_source"),
                "ai_decision_id": signal.get("decision_id"),
                "ai_decision_interval_seconds": signal.get("decision_interval_seconds") or env.get("AI_DECISION_INTERVAL_SECONDS", "180"),
                "decision_signal_action": decision_signal.get("action"),
                "decision_signal_confidence": decision_signal.get("confidence"),
                "decision_signal_source": decision_signal.get("source"),
                "decision_signal_timestamp": decision_signal.get("timestamp") or decision_signal.get("generated_at"),
                "decision_signal_reason": decision_signal.get("reason") or decision_signal.get("reasoning"),
                "exit_rule": f"best bid 浮盈 > ${env.get('PAPER_TAKE_PROFIT_USD', '0.12')} 提前卖出，否则到期离场",
                "trading_enabled": control.get("trading_enabled", True),
            }
            send_json(self, config)

        # === 首页 → status.html ===
        elif path == '/':
            self.path = '/status.html'
            super().do_GET()

        # === 合并历史交易数据（永久修复 Mar31 历史丢失问题）===
        elif path == '/api/merge-history':
            history_file = "/home/billy/.openclaw/workspace/polymarket_web/paper_trade_state.json.bak4"
            state_file = "/home/billy/.openclaw/workspace/polymarket_web/paper_trade_state.json"
            try:
                with open(history_file) as f:
                    mar31 = json.load(f)
                with open(state_file) as f:
                    current = json.load(f)
                # Mar31 COMPLETE trades
                mar31_closed = [t for t in mar31.get("trades", [])
                                 if t.get("operation") == "COMPLETE" and t.get("realized_profit", 0) != 0]
                # 当前 COMPLETE trades
                current_closed = [t for t in current.get("trades", [])
                                   if t.get("operation") == "COMPLETE"]
                # 去重（用 closed_at）
                current_ats = set(t.get("closed_at", "") for t in current_closed)
                new_from_mar31 = [t for t in mar31_closed if t.get("closed_at", "") not in current_ats]
                # 合并
                all_trades = current.get("trades", []) + new_from_mar31
                all_closed = [t for t in all_trades if t.get("operation") == "COMPLETE"]
                wins = sum(1 for t in all_closed if t.get("realized_profit", 0) > 0)
                losses = sum(1 for t in all_closed if t.get("realized_profit", 0) < 0)
                total = len(all_closed)
                cash = current.get("cash_balance", 0)
                starting = 100.0
                computed_pnl = cash - starting
                # 更新 state
                current["trades"] = all_trades
                current["starting_balance"] = round(starting, 4)
                current["realized_pnl"] = round(computed_pnl, 4)
                current["stats"]["total_trades"] = total
                current["stats"]["winning_trades"] = wins
                current["stats"]["losing_trades"] = losses
                current["stats"]["total_profit"] = round(computed_pnl, 4)
                current["summary"]["starting_balance"] = round(starting, 4)
                current["summary"]["realized_pnl"] = round(computed_pnl, 4)
                current["summary"]["total_trades"] = total
                with open(state_file, "w") as f:
                    json.dump(current, f, indent=2)
                send_json(self, {
                    "ok": True,
                    "total_trades": total,
                    "mar31_added": len(new_from_mar31),
                    "win_rate": round(wins / total * 100, 1) if total > 0 else 0,
                })
            except Exception as e:
                send_json(self, {"error": str(e)}, 500)

        # === 其它静态文件 ===
        else:
            super().do_GET()


def run_server():
    """运行 HTTP 服务器"""
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    socketserver.ThreadingTCPServer.daemon_threads = True
    with socketserver.ThreadingTCPServer(("", PORT), StatusHandler) as httpd:
        print(f"🌐 状态监控页面: http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    print(f"🌐 启动状态监控页面: http://localhost:{PORT}")
    print("按 Ctrl+C 停止")
    run_server()
