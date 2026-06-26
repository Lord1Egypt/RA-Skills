#!/usr/bin/env python3
"""
 Polymarket BTC Up.Down 自动交易 Bot
 
 流程:
   BTC数据 → AI预测 → 概率判断 → Polymarket下单
   
 每{MARKET_INTERVAL_MINUTES}分钟运行一次
"""

import asyncio
import calendar
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

import aiohttp
import requests
from dotenv import load_dotenv

# 状态文件路径
STATUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_status.json")
CONTROL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trading_control.json")
DECISION_SIGNAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decision_signal.json")

def load_json_file(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return default


def save_json_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_trading_control():
    state = load_json_file(CONTROL_FILE, {})
    return {
        "trading_enabled": bool(state.get("trading_enabled", True)),
        "updated_at": state.get("updated_at"),
    }


def extract_market_slug(market_input: str) -> str:
    if not market_input:
        return ""
    if "polymarket.com/event/" in market_input:
        return market_input.split("polymarket.com/event/")[-1].split("#")[0].split("?")[0]
    return market_input.strip()


def parse_json_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return []
    return []


def safe_float(value, default=None):
    try:
        return float(value)
    except Exception:
        return default


def load_openclaw_signal():
    signal = load_json_file(DECISION_SIGNAL_FILE, {})
    if not isinstance(signal, dict):
        return None

    action = str(signal.get("action", "")).upper().strip()
    if action not in {"BUY", "SELL", "HOLD"}:
        return None

    prediction = str(signal.get("prediction") or signal.get("direction") or action).upper().strip()
    if prediction not in {"UP", "DOWN", "HOLD"}:
        prediction = "UP" if action == "BUY" else "DOWN" if action == "SELL" else "HOLD"

    return {
        "decision_id": signal.get("decision_id") or signal.get("id") or f"OPENCLAW-{int(time.time())}",
        "generated_at": signal.get("timestamp") or signal.get("generated_at") or datetime.now(timezone.utc).isoformat(),
        "prediction": prediction,
        "action": action,
        "reason": str(signal.get("reason") or signal.get("reasoning") or signal.get("summary") or "OpenClaw 外部决策信号").strip(),
        "ai_confidence": round(safe_float(signal.get("confidence"), 0.5) or 0.5, 4),
        "ai_model": str(signal.get("model") or signal.get("agent") or "OpenClaw Decision"),
        "ai_source": str(signal.get("source") or "openclaw-cron"),
        "ai_key_factors": [str(x)[:220] for x in (signal.get("key_factors") or [])[:6]],
        "ai_risk_flags": [str(x)[:220] for x in (signal.get("risk_flags") or [])[:6]],
        "ai_thought_markdown": str(signal.get("thought_markdown") or signal.get("reason") or signal.get("reasoning") or "OpenClaw 外部决策信号"),
        "close_positions": bool(signal.get("close_positions", action == "SELL")),
        "decision_interval_seconds": int(safe_float(signal.get("decision_interval_seconds"), AI_DECISION_INTERVAL_SECONDS) or AI_DECISION_INTERVAL_SECONDS),
        "external_signal": True,
        "raw_signal": signal,
    }


def iso_to_utc_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def iso_to_ts(value: str) -> int:
    return calendar.timegm(iso_to_utc_dt(value).utctimetuple())


def ts_to_iso(ts_value: int) -> str:
    return datetime.fromtimestamp(ts_value, tz=timezone.utc).isoformat()


def short_wallet(address: str) -> str:
    if not address or len(address) < 10:
        return "--"
    return f"{address[:6]}...{address[-4:]}"


def write_status(bot=None, market_info=None, btc_data=None, prediction=None, probabilities=None, decision=None, error=None, extra=None):
    """写入状态到文件"""
    try:
        status = {
            "running": True,
            "last_update": datetime.now().isoformat(),
            "btc_price": btc_data.get("price") if btc_data else None,
            "btc_change_24h": btc_data.get("change_24h") if btc_data else None,
            "ai_prediction": prediction,
            "yes_price": probabilities.get("yes_price") if probabilities else None,
            "no_price": probabilities.get("no_price") if probabilities else None,
            "outcomes": probabilities.get("outcomes") if probabilities else None,
            "decision_reason": probabilities.get("reason") if probabilities else None,
            "decision": decision,
            "total_trades": bot.stats.get("total_trades", 0) if bot else 0,
            "market": (market_info or {}).get("question") or (market_info or {}).get("title"),
            "error": error,
        }
        if extra:
            status.update(extra)
        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"写入状态失败: {e}")

# ==================== 配置 ====================

load_dotenv()  # 加载 .env 文件

# Polymarket API 配置
POLYMARKET_API_KEY = os.getenv("POLYMARKET_API_KEY", "")
POLYMARKET_API_SECRET = os.getenv("POLYMARKET_API_SECRET", "")
POLYMARKET_API_PASSPHRASE = os.getenv("POLYMARKET_API_PASSPHRASE", "")
RELAYER_API_KEY = os.getenv("RELAYER_API_KEY", "")
POLYMARKET_PRIVATE_KEY = os.getenv("POLYMARKET_PRIVATE_KEY", "")
POLYMARKET_WALLET_ADDRESS = os.getenv("POLYMARKET_WALLET_ADDRESS", "")

# 交易配置
BET_AMOUNT = float(os.getenv("BET_AMOUNT", "5"))        # 每次下注金额 (USDC)
# 交易参数
MIN_ENTRY_PRICE = float(os.getenv("MIN_ENTRY_PRICE", "0.15"))
MAX_ENTRY_PRICE = float(os.getenv("MAX_ENTRY_PRICE", "0.60"))
TAKE_PROFIT_USD = float(os.getenv("TAKE_PROFIT_USD", "0.12"))
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", "1"))
MAX_SPREAD = float(os.getenv("MAX_SPREAD", "0.06"))
MIN_TOP_BOOK_SIZE = float(os.getenv("MIN_TOP_BOOK_SIZE", "25"))
MIN_MINUTES_TO_EXPIRY = int(os.getenv("MIN_MINUTES_TO_EXPIRY", "3"))
MAX_NEW_POSITIONS_PER_CYCLE = int(os.getenv("MAX_NEW_POSITIONS_PER_CYCLE", "1"))
MARKET_INTERVAL_MINUTES = int(os.getenv("MARKET_INTERVAL_MINUTES", "5"))
MAX_BET_AMOUNT = float(os.getenv("MAX_BET_AMOUNT", "50"))  # 单笔最大
MIN_PROBABILITY_DIFF = float(os.getenv("MIN_PROBABILITY_DIFF", "0.1"))  # 最小概率差才下单
STOP_LOSS_ENABLED = bool(os.getenv("STOP_LOSS_ENABLED", "true").lower() == "true")
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", "0.10"))  # 止损比例
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", "0.18"))
TIME_EXIT_SECONDS = int(os.getenv("TIME_EXIT_SECONDS", "45"))
AI_EXIT_ENABLED = os.getenv("AI_EXIT_ENABLED", "false").strip().lower() == "true"
TIME_EXIT_ENABLED = os.getenv("TIME_EXIT_ENABLED", "true").strip().lower() == "true"
TAKE_PROFIT_ENABLED = os.getenv("TAKE_PROFIT_ENABLED", "false").strip().lower() == "true"

# BTC 配置
BTC_PRICE_SOURCE = os.getenv("BTC_PRICE_SOURCE", "binance")  # binance 或 coingecko
NY_TZ = ZoneInfo("America/New_York")

# AI 交易配置（OpenAI 兼容接口）
AI_ENABLED = os.getenv("AI_ENABLED", "true").lower() == "true"
AI_DECISION_INTERVAL_SECONDS = int(os.getenv("AI_DECISION_INTERVAL_SECONDS", "30"))  # 激进模式：每30秒重新决策
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai_compatible")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
AI_API_KEY = os.getenv("AI_API_KEY", "") or os.getenv("MINIMAX_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.2"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "700"))

# ====== Debug Mode ======
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# ====== High-Frequency Trading Params (5min markets) ======
HF_ENABLED = os.getenv("HF_ENABLED", "true").lower() == "true"
HF_ENTRY_THRESHOLD = float(os.getenv("HF_ENTRY_THRESHOLD", "0.003"))  #偏离 0.50 多少开始交易（±0.3%，激进模式）
HF_TAKE_PROFIT_USD = float(os.getenv("HF_TAKE_PROFIT_USD", "0.20"))   #浮盈 >N USD 立即止盈（$0.20合理）
HF_STOP_LOSS_USD = float(os.getenv("HF_STOP_LOSS_USD", "0.20"))       #浮亏 >N USD 止损（$0.20合理）
HF_MIN_PROB_THRESHOLD = float(os.getenv("HF_MIN_PROB_THRESHOLD", "0.50"))  #最低概率

# ====== Mean Reversion Long-term Strategy Params ======
MARKET_FAIR_PROB = float(os.getenv("MARKET_FAIR_PROB", "0.50"))
MEAN_REVERSION_ENTRY_THRESHOLD = float(os.getenv("MEAN_REVERSION_ENTRY_THRESHOLD", "0.12"))
MEAN_REVERSION_TAKE_PROFIT_THRESHOLD = float(os.getenv("MEAN_REVERSION_TAKE_PROFIT_THRESHOLD", "0.05"))
MEAN_REVERSION_STOP_LOSS_THRESHOLD = float(os.getenv("MEAN_REVERSION_STOP_LOSS_THRESHOLD", "0.08"))
BTC_TARGET_PRICE = float(os.getenv("BTC_TARGET_PRICE", "150000"))
MARKET_END_DATE = os.getenv("MARKET_END_DATE", "2026-03-31")

# Market ID (需要你自己填)
# 可以填: 
#   - 市场 slug (如 "btc-updown-5m-1773289200")
#   - 完整 URL (如 "https://polymarket.com/event/btc-updown-5m-1773289200")
#   - Condition ID (如 "0xabc123...")
BTC_UPDOWN_MARKET_ID = os.getenv("BTC_UPDOWN_MARKET_ID", "")


async def get_condition_id_from_market(client, market_input: str) -> Optional[dict]:
    """从市场 URL/slug 获取 Condition ID"""
    try:
        # 优先检查: 如果输入的是 condition_id (0x开头，66位)，直接使用
        if market_input.startswith("0x") and len(market_input) == 66:
            print(f"🔍 使用 Condition ID: {market_input}")
            return {'condition_id': market_input, 'question': 'Manual Condition ID'}
        
        # 提取 slug
        slug = market_input
        if "polymarket.com/event/" in market_input:
            # 从 URL 提取 slug
            slug = market_input.split("polymarket.com/event/")[-1].split("#")[0].split("?")[0]
        
        print(f"🔍 查找市场: {slug}")
        
        # 尝试通过 API 获取市场信息
        async with aiohttp.ClientSession() as session:
            # 方法1: 通过 eventSlug 查询
            url = f"{client.BASE_URL}/markets"
            params = {"eventSlug": slug}
            
            async with session.get(url, params=params, headers=client.headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    markets = data.get('data', []) if isinstance(data, dict) else data
                    
                    # 优先找 accepting_orders 的市场
                    for m in markets:
                        if m.get('accepting_orders') or m.get('active'):
                            return {
                                'condition_id': m.get('condition_id'),
                                'question': m.get('question'),
                                'market_slug': m.get('market_slug'),
                            }
                    
                    # 返回第一个
                    if markets:
                        return {
                            'condition_id': markets[0].get('condition_id'),
                            'question': markets[0].get('question'),
                            'market_slug': markets[0].get('market_slug'),
                        }
            
            # 方法2: 通过 event 查询
            url2 = f"{client.BASE_URL}/markets"
            params2 = {"event": slug}
            
            async with session.get(url2, params=params2, headers=client.headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    markets = data.get('data', []) if isinstance(data, dict) else data
                    
                    for m in markets:
                        if m.get('accepting_orders') or m.get('active'):
                            return {
                                'condition_id': m.get('condition_id'),
                                'question': m.get('question'),
                                'market_slug': m.get('market_slug'),
                            }
                    
                    if markets:
                        return {
                            'condition_id': markets[0].get('condition_id'),
                            'question': markets[0].get('question'),
                            'market_slug': markets[0].get('market_slug'),
                        }
            
            # 方法3: 搜索包含 slug 关键词的市场
            url3 = f"{client.BASE_URL}/markets"
            params3 = {"limit": "500", "closed": "false"}
            
            async with session.get(url3, params=params3, headers=client.headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    markets = data.get('data', []) if isinstance(data, dict) else data
                    
                    # 模糊匹配 slug
                    for m in markets:
                        market_slug = m.get('market_slug', '').lower()
                        question = m.get('question', '').lower()
                        if slug.lower() in market_slug or slug.lower() in question:
                            return {
                                'condition_id': m.get('condition_id'),
                                'question': m.get('question'),
                                'market_slug': m.get('market_slug'),
                            }
            
            # 方法4: 如果输入的是 condition_id，直接返回
            if market_input.startswith("0x") and len(market_input) == 66:
                return {'condition_id': market_input, 'question': 'Unknown'}
                
        print(f"⚠️ 未找到市场: {slug}")
        return None
    except Exception as e:
        print(f"获取 Condition ID 失败: {e}")
        return None

# ==================== 辅助函数 ====================

async def find_active_btc_market_by_interval(client, interval_minutes: int = MARKET_INTERVAL_MINUTES) -> Optional[dict]:
    """查找当前活跃的 BTC {interval_minutes}m 市场（动态 interval）"""
    try:
        interval_str = f"{interval_minutes}m"
        # 尝试多个 API 端点来查找
        endpoints = [
            f"{client.BASE_URL}/markets?closed=false&limit=1000",
            f"{client.BASE_URL}/markets?limit=1000",
        ]
        
        for url in endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=client.headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                        if resp.status != 200:
                            continue
                        data = await resp.json()
                        markets = data.get('data', []) if isinstance(data, dict) else data
                        
                        # 先找接受订单的市场
                        for m in markets:
                            if not m.get('accepting_orders'):
                                continue
                            q = m.get('question', '').lower()
                            slug = m.get('market_slug', '').lower()
                            
                            # 动态匹配 interval 市场
                            if (('btc' in q or 'bitcoin' in q) and 
                                (interval_str in q or f'{interval_minutes}min' in q or f'{interval_minutes} min' in q or 'up' in q or 'down' in q)):
                                return {
                                    'condition_id': m.get('condition_id'),
                                    'question': m.get('question'),
                                    'market_slug': m.get('market_slug'),
                                    'active': m.get('active'),
                                    'accepting_orders': m.get('accepting_orders')
                                }
                            
                            if 'btc' in slug and interval_str in slug:
                                return {
                                    'condition_id': m.get('condition_id'),
                                    'question': m.get('question'),
                                    'market_slug': m.get('market_slug'),
                                    'active': m.get('active'),
                                    'accepting_orders': m.get('accepting_orders')
                                }
                        
                        # 如果没找到接受的，找活跃的
                        for m in markets:
                            if not m.get('active'):
                                continue
                            q = m.get('question', '').lower()
                            slug = m.get('market_slug', '').lower()
                            
                            if (('btc' in q or 'bitcoin' in q) and 
                                (interval_str in q or f'{interval_minutes}min' in q or f'{interval_minutes} min' in q or 'up' in q or 'down' in q)):
                                return {
                                    'condition_id': m.get('condition_id'),
                                    'question': m.get('question'),
                                    'market_slug': m.get('market_slug'),
                                    'active': m.get('active'),
                                    'accepting_orders': m.get('accepting_orders')
                                }
            except Exception as e:
                print(f"  尝试端点失败: {e}")
                continue
                
        return None
    except Exception as e:
        print(f"查找 BTC {interval_minutes}m 市场失败: {e}")
        return None


# 向后兼容别名
async def find_active_btc_5m_market(client) -> Optional[dict]:
    return await find_active_btc_market_by_interval(client, MARKET_INTERVAL_MINUTES)

# ==================== API 客户端 ====================

async def get_current_btc_5m_market(client) -> Optional[dict]:
    """自动检测当前活跃的 BTC 5分钟 Up/Down 市场。
    市场slug格式: btc-updown-{interval}m-{unix_timestamp}

    优先尝试当前窗口，如果找不到则尝试上一个窗口（市场可能还未创建）。
    Returns None 如果没有活跃市场（下单前先检查返回值）。
    """
    try:
        import time as _time
        now = int(_time.time())
        interval = MARKET_INTERVAL_MINUTES
        interval_sec = interval * 60
        window = (now // interval_sec) * interval_sec
        # 尝试当前窗口和上一个窗口（Polymarket 市场可能尚未创建当前窗口）
        slugs_to_try = [
            (window, f"当前窗口 {interval}m"),
            (window - interval_sec, f"上一窗口 {interval}m"),
        ]

        async with aiohttp.ClientSession() as session:
            for win, win_label in slugs_to_try:
                slug = f"btc-updown-{interval}m-{win}"
                try:
                    url = f"https://gamma-api.polymarket.com/markets/slug/{slug}"
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                        if resp.status == 200:
                            m = await resp.json()
                            cond_id = m.get('conditionId') or m.get('condition_id')
                            is_closed = m.get('closed', False)
                            end_date = m.get('end_date')
                            if cond_id and not is_closed:
                                if win != window:
                                    print(f"ℹ️ 当前窗口市场未上线，使用上一窗口: {slug}")
                                return {
                                    'condition_id': cond_id,
                                    'question': m.get('question'),
                                    'market_slug': slug,
                                    'end_date': end_date,
                                    'clob_token_ids': json.loads(m.get('clobTokenIds') or '[]'),
                                }
                            elif is_closed:
                                print(f"⚠️ 市场已关闭: {slug}")
                            else:
                                print(f"⚠️ 未找到 condition_id: {slug}")
                        elif resp.status == 404:
                            print(f"  [{win_label}] 市场不存在: {slug}")
                        else:
                            print(f"  [{win_label}] HTTP {resp.status}: {slug}")
                except Exception as e:
                    print(f"  [{win_label}] 查询失败: {e}")
                    continue
    except Exception as e:
        print(f"⚠️ 自动检测 BTC 5m 市场失败: {e}")
    return None



class PolymarketClient:
    """Polymarket CLOB 客户端（使用 py_clob_client）"""

    def __init__(self, api_key: str, private_key: str, wallet_address: str,
                 api_secret: str = "", api_passphrase: str = "", relayer_key: str = ""):
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import ApiCreds
        from py_builder_signing_sdk.config import BuilderConfig
        from py_builder_signing_sdk.sdk_types import BuilderApiKeyCreds
        import os

        self.wallet_address = wallet_address
        self.BASE_URL = "https://clob.polymarket.com"
        self.GAMMA_BASE = "https://gamma-api.polymarket.com"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        # EOA wallet + API credentials
        # 注意：api_passphrase 就是签名私钥，不是 passphrase
        from py_clob_client.clob_types import ApiCreds
        api_creds = ApiCreds(
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=api_passphrase,
        ) if api_key else None

        # 优先用 api_passphrase 作为签名私钥（如果是有效的私钥格式）
        signing_key = api_passphrase if api_passphrase and len(api_passphrase) == 64 else private_key

        self._clob = ClobClient(
            host="https://clob.polymarket.com",
            chain_id=137,
            key=signing_key,
            creds=api_creds,
            signature_type=0,  # EOA wallet
            funder=wallet_address,
        )
        self._market_cache = {}  # condition_id -> market_data

    def _run_sync(self, fn, *args, **kwargs):
        """在线程池中执行同步 ClobClient 方法"""
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, lambda: fn(*args, **kwargs))

    async def get_markets(self, event_id: str = None):
        """获取市场列表"""
        try:
            result = await self._run_sync(self._clob.get_markets, {"closed": False, "limit": 100})
            return {"markets": result} if isinstance(result, list) else result
        except Exception as e:
            print(f"❌ get_markets 失败: {e}")
            return {"markets": []}

    async def get_order_book(self, condition_id: str):
        """获取订单簿（内部用 token_id）"""
        try:
            token_id = self._get_token_id(condition_id, "Buy_Up")
            if not token_id:
                return {}
            return await self._run_sync(self._clob.get_order_book, token_id)
        except Exception as e:
            print(f"❌ get_order_book 失败: {e}")
            return {}

    async def get_fills(self, condition_id: str):
        """获取成交记录"""
        try:
            return await self._run_sync(self._clob.get_fills, condition_id)
        except Exception as e:
            print(f"❌ get_fills 失败: {e}")
            return {}

    async def place_order(self, condition_id: str, side: str, amount: float, price: float = None, position: dict = None):
        """下单（使用 ClobClient 签名）。下单前会验证市场可交易性。
        position: 当前持仓 dict (from PolyMain.position)，SELL 时用于确定 token
        """
        from py_clob_client.clob_types import OrderArgs

        # ── 市场可交易性验证 ──
        is_valid, err_msg = await self._validate_market_tradeable(condition_id)
        if not is_valid:
            print(f"❌ 市场不可交易: {err_msg}")
            return {"error": err_msg}

        try:
            # SELL（平仓）时根据持仓方向获取正确的 token
            # position["outcome"] 包含 "UP"/"DOWN" 或 "YES"/"NO"，需要映射到 Buy_Up/Buy_Down
            if side == "Sell" and position:
                outcome = position.get("outcome", "")
                if "UP" in outcome.upper() or "YES" in outcome.upper():
                    token_side = "Buy_Up"
                else:
                    token_side = "Buy_Down"
                token_id = self._get_token_id(condition_id, token_side)
            else:
                # Buy → Buy_Up, Sell → Sell (Sell with no position = Sell Down token)
                token_side = "Buy_Up" if side == "Buy" else side
                token_id = self._get_token_id(condition_id, token_side)
            if not token_id:
                return {"error": f"找不到 condition_id {condition_id} 对应的 token_id"}

            order_args = OrderArgs(
                token_id=token_id,
                side="BUY" if side == "Buy" else "SELL",
                size=amount,
                price=price if price else 0.5,
            )
            if DEBUG_MODE: print(f"   [DEBUG] token_id={token_id[:30]}..., side={order_args.side}, size={amount}, price={order_args.price}")
            try:
                result = self._clob.create_and_post_order(order_args)
                # 注意：create_and_post_order 是同步的，不需要 thread pool
            except Exception as order_err:
                print(f"❌ create_and_post_order 直接异常: {type(order_err).__name__}: {order_err}")
                return {"error": f"{type(order_err).__name__}: {order_err}"}

            # 写通知
            self._write_notification(
                event_type="order_placed",
                title="🟢 开仓成功",
                message=f"{side.upper()} {amount} shares @ {price or 0.5}",
                details={
                    "side": side,
                    "size": amount,
                    "price": price or 0.5,
                    "token_id": token_id[:20] + "...",
                    "result": str(result)[:100],
                }
            )
            return result
        except Exception as e:
            print(f"❌ place_order 失败: {e}")
            return {"error": str(e)}

    def _get_token_id(self, condition_id: str, side: str = "Buy_Up") -> str:
        """从缓存获取 token_id。如果缓存没有，直接同步获取市场数据。

        Buy_Up/Buy_Yes → clob_ids[0] (Yes/Up token)
        Buy_Down/Buy_No → clob_ids[1] (No/Down token)
        """
        if DEBUG_MODE: print(f"   [DEBUG _get_token_id] cid={condition_id[:20]}..., side={side}, cache_keys={list(self._market_cache.keys())[:3]}")
        # 优先从缓存取
        info = self._market_cache.get(condition_id, {})
        tokens = info.get("tokens", [])
        # clobTokenIds 从 Gamma API 返回时可能是 JSON 字符串
        clob_ids_raw = info.get("clob_token_ids", [])
        if isinstance(clob_ids_raw, str):
            import json
            clob_ids = json.loads(clob_ids_raw) if clob_ids_raw else []
        else:
            clob_ids = clob_ids_raw or []
        if DEBUG_MODE: print(f"   [DEBUG _get_token_id] tokens={bool(tokens)}, clob_ids={bool(clob_ids)}")

        if tokens:
            idx = 0 if side in ("Buy_Up", "Buy_Yes") else 1
            result = tokens[idx].get("token_id", "") if len(tokens) > idx else ""
            if DEBUG_MODE: print(f"   [DEBUG _get_token_id] from tokens[{idx}] = {result[:20]}...")
            return result
        elif clob_ids:
            idx = 0 if side in ("Buy_Up", "Buy_Yes") else 1
            result = clob_ids[idx] if len(clob_ids) > idx else ""
            if DEBUG_MODE: print(f"   [DEBUG _get_token_id] from clob_ids[{idx}] = {result[:20]}...")
            return result

        # 缓存没有，直接同步查询（避免竞态）
        try:
            m = self._clob.get_market(condition_id)
            if DEBUG_MODE: print(f"   [DEBUG _get_token_id] get_market returned: {bool(m)}, keys={list(m.keys()) if m else []}")
            if m and m.get("condition_id"):
                self._market_cache[m["condition_id"]] = m
                tokens = m.get("tokens", [])
                if tokens:
                    idx = 0 if side in ("Buy_Up", "Buy_Yes") else 1
                    result = tokens[idx].get("token_id", "") if len(tokens) > idx else ""
                    if DEBUG_MODE: print(f"   [DEBUG _get_token_id] from market tokens[{idx}] = {result[:20]}...")
                    return result
                clobs = m.get("clobTokenIds") or []
                if clobs:
                    idx = 0 if side in ("Buy_Up", "Buy_Yes") else 1
                    result = clobs[idx] if len(clobs) > idx else ""
                    if DEBUG_MODE: print(f"   [DEBUG _get_token_id] from market clobTokenIds[{idx}] = {result[:20]}...")
                    return result
        except Exception as e:
            if DEBUG_MODE: print(f"   [DEBUG _get_token_id] get_market exception: {type(e).__name__}: {e}")
        if DEBUG_MODE: print(f"   [DEBUG _get_token_id] RETURNING EMPTY STRING")
        return ""

    def set_clob_token_ids(self, condition_id: str, clob_token_ids: list):
        """直接从 Gamma API 获取的 clobTokenIds 设置市场 token 信息"""
        self._market_cache[condition_id] = {
            "tokens": [],
            "clob_token_ids": clob_token_ids,
            "condition_id": condition_id,
        }

    def _ensure_market_cached_sync(self, condition_id: str):
        """同步确保市场信息已缓存（在线程池执行）"""
        if condition_id in self._market_cache:
            return
        try:
            result = self._clob.get_market(condition_id)
            if result and result.get("condition_id"):
                self._market_cache[result["condition_id"]] = result
        except Exception as e:
            print(f"⚠️ 缓存市场信息失败: {e}")

    async def _validate_market_tradeable(self, condition_id: str) -> tuple:
        """验证市场是否可以交易。Returns (is_valid, error_msg)"""
        from datetime import datetime, timezone
        try:
            result = await self._run_sync(self._clob.get_market, condition_id)
            if not result:
                return False, f"市场不存在: {condition_id}"
            if result.get("closed"):
                return False, f"市场已关闭: {result.get('question', condition_id)}"
            end_date = result.get("end_date") or result.get("endDate")
            if end_date:
                try:
                    end_dt = datetime.fromisoformat(str(end_date).replace("Z", "+00:00"))
                    if end_dt.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
                        return False, f"市场已过期: {end_date}"
                except Exception:
                    pass
            return True, ""
        except Exception as e:
            return False, f"验证市场失败: {e}"

    async def _refresh_markets(self):
        """刷新市场缓存"""
        try:
            result = await self._run_sync(self._clob.get_markets, {"closed": False, "limit": 1000})
            markets = result if isinstance(result, list) else result.get("data", [])
            for m in markets:
                cid = m.get("condition_id", "")
                if cid:
                    self._market_cache[cid] = m
        except Exception as e:
            print(f"⚠️ 刷新市场缓存失败: {e}")

    def _write_notification(self, event_type: str, title: str, message: str, details: dict = None):
        """写入通知到 notifications.json，供状态面板展示"""
        import json, os
        from datetime import datetime, timezone
        base_dir = os.path.dirname(os.path.abspath(__file__))
        notif_file = os.path.join(base_dir, "notifications.json")
        notifications = []
        if os.path.exists(notif_file):
            try:
                with open(notif_file, "r") as f:
                    notifications = json.load(f).get("notifications", [])
            except Exception:
                pass
        notification = {
            "id": len(notifications) + 1,
            "type": event_type,
            "title": title,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        notifications.insert(0, notification)
        notifications = notifications[:50]
        try:
            with open(notif_file, "w") as f:
                json.dump({"notifications": notifications}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 写入通知失败: {e}")

    async def cancel_orders(self, order_ids: list):
        """取消订单"""
        try:
            return await self._run_sync(self._clob.cancel_orders, order_ids)
        except Exception as e:
            print(f"❌ cancel_orders 失败: {e}")
            return {"error": str(e)}


class BTCDataprovider:
    """BTC 价格数据源"""
    
    @staticmethod
    def get_price_binance() -> Optional[dict]:
        """从 Binance 获取 BTC 价格"""
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            return {
                "price": float(data["price"]),
                "source": "binance",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ 获取 Binance BTC 价格失败: {e}")
            return None
    
    @staticmethod
    def get_price_coingecko() -> Optional[dict]:
        """从 CoinGecko 获取 BTC 价格"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            return {
                "price": data["bitcoin"]["usd"],
                "source": "coingecko",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ 获取 CoinGecko BTC 价格失败: {e}")
            return None
    
    @staticmethod
    def get_price_with_change() -> Optional[dict]:
        """获取价格 + 24h 变化"""
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            return {
                "price": float(data["lastPrice"]),
                "change_24h": float(data["priceChangePercent"]),
                "high_24h": float(data["highPrice"]),
                "low_24h": float(data["lowPrice"]),
                "volume_24h": float(data["volume"]),
                "source": "binance",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ 获取 BTC 24h 数据失败: {e}")
            return None


class AIDecisionEngine:
    """使用 OpenAI 兼容接口做结构化交易判断；无密钥时自动回退到规则策略。"""

    def __init__(self):
        self.enabled = AI_ENABLED
        self.base_url = AI_BASE_URL.rstrip("/")
        self.api_key = AI_API_KEY
        self.model = AI_MODEL
        self.temperature = AI_TEMPERATURE
        self.max_tokens = AI_MAX_TOKENS


    def parse_json_content(self, content: str) -> dict:
        """从模型输出提取 JSON，兼容 MiniMax think 标签格式。"""
        raw = str(content).strip()
        if not raw:
            return {}
        
        # 找最后一个 </think> 之后的内容
        idx = raw.rfind('</think>')
        text = raw[idx + 7:].strip() if idx != -1 else raw
        text = text.strip('`').strip()
        
        # 尝试直接解析
        for s in [text, raw]:
            s = s.strip()
            if s:
                try:
                    return json.loads(s)
                except Exception:
                    pass
        
        # 找第一个 {...} JSON 块
        start = text.find('{')
        if start != -1:
            depth = 0
            end = -1
            for i in range(start, len(text)):
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
            if end != -1:
                try:
                    return json.loads(text[start:end + 1])
                except Exception:
                    pass
        
        raise ValueError("JSON解析失败: " + raw[:100])
    def build_rule_fallback(self, payload: dict, fallback_reason: str) -> dict:
        btc = payload.get("btc", {})
        daily_open = safe_float(payload.get("daily_open"), 0.0) or 0.0
        current_price = safe_float(btc.get("price"), 0.0) or 0.0
        prediction = "HOLD"
        action = "HOLD"
        if current_price > daily_open:
            prediction = "UP"
            action = "BUY"
        elif current_price < daily_open:
            prediction = "DOWN"
            action = "BUY"

        return {
            "prediction": prediction,
            "action": action,
            "confidence": 0.35,
            "reasoning": f"AI 不可用，回退为规则策略：现价 {current_price:,.2f} 与今开 {daily_open:,.2f} 比较。{fallback_reason}",
            "key_factors": [
                f"BTC 现价 {current_price:,.2f}",
                f"今开 {daily_open:,.2f}",
                f"24h 涨跌 {safe_float(btc.get('change_24h'), 0.0) or 0.0:+.2f}%",
            ],
            "risk_flags": ["当前为规则回退，不是真实 LLM 输出"],
            "close_positions": False,
            "source": "fallback",
        }

    def build_prompt(self, payload: dict) -> tuple[str, str]:
        system = (
            "你是一个谨慎的 Polymarket BTC 短线纸上交易分析器。"
            "你只能输出严格 JSON，不要输出 markdown。"
            "目标：每 3 分钟评估一次是否 BUY / SELL / HOLD。"
            "BUY 表示允许按目标方向寻找可交易盘口开仓；SELL 表示建议把当前持仓平掉；HOLD 表示观望。"
            "prediction 只能是 UP、DOWN、HOLD。action 只能是 BUY、SELL、HOLD。"
            "必须提供 reasoning、key_factors、risk_flags、confidence。"
            "如果信号不够强，宁可 HOLD。"
        )
        user = json.dumps(payload, ensure_ascii=False)
        return system, user

    def call_model(self, payload: dict) -> dict:
        if not self.enabled:
            return self.build_rule_fallback(payload, "AI_ENABLED=false")
        if not self.api_key:
            return self.build_rule_fallback(payload, "未配置 AI_API_KEY")

        system, user = self.build_prompt(payload)

        # MiniMax 原生 API
        if AI_PROVIDER == "minimax":
            return self._call_minimax_native(system, user, payload)

        # OpenAI 兼容格式（默认）
        return self._call_openai_compatible(system, user, payload)

    def _call_minimax_native(self, system: str, user: str, payload: dict) -> dict:
        """MiniMax 原生 API 调用"""
        body = {
            "model": self.model,
            "tokens_to_generate": self.max_tokens,
            "temperature": self.temperature,
            "messages": [
                {"sender_type": "USER", "sender_name": "User", "text": f"{system}\n\n{user}"}
            ],
            "bot_setting": [
                {
                    "bot_name": "TraderBot",
                    "content": "You are a helpful trading assistant. Always respond with valid JSON only, no explanations."
                }
            ],
            "reply_constraints": {
                "sender_type": "BOT",
                "sender_name": "TraderBot"
            },
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            resp = requests.post(
                f"{self.base_url}/text/chatcompletion_pro",
                headers=headers,
                json=body,
                timeout=45
            )
            data = resp.json()

            # 检查 API 错误
            base_resp = data.get("base_resp", {})
            if base_resp.get("status_code") != 0:
                return self.build_rule_fallback(payload, f"MiniMax API 错误: {base_resp.get('status_msg', 'unknown')}")

            # MiniMax 返回格式：{"reply": "text or json..."}
            content = data.get("reply", "").strip()
            if not content:
                return self.build_rule_fallback(payload, "MiniMax API 返回空 reply")

            # 尝试把 reply 解析为 JSON
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                # reply 是纯文本，尝试从中提取 JSON
                parsed = self._parse_text_as_json(content, payload)
                if parsed is None:
                    return self.build_rule_fallback(payload, f"MiniMax 返回非JSON: {content[:100]}")

            return self._parse_llm_response(parsed, payload)
        except Exception as e:
            return self.build_rule_fallback(payload, f"MiniMax API 调用异常: {e}")

    def _parse_text_as_json(self, text: str, payload: dict) -> dict | None:
        """从纯文本中提取 JSON，或构建简化响应"""
        # 尝试找 {...} 块
        start = text.find('{')
        if start != -1:
            depth = 0
            end = -1
            for i in range(start, len(text)):
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
            if end != -1:
                try:
                    return json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    pass

        # 如果文本包含 UP/DOWN/HOLD 关键词，构建简化响应
        text_upper = text.upper()
        if "UP" in text_upper and "DOWN" not in text_upper:
            return {"prediction": "UP", "action": "BUY", "confidence": 0.5, "reasoning": text[:200]}
        elif "DOWN" in text_upper:
            return {"prediction": "DOWN", "action": "BUY", "confidence": 0.5, "reasoning": text[:200]}
        elif "HOLD" in text_upper or "WAIT" in text_upper:
            return {"prediction": "HOLD", "action": "HOLD", "confidence": 0.5, "reasoning": text[:200]}

        return None

    def _call_openai_compatible(self, system: str, user: str, payload: dict) -> dict:
        """OpenAI 兼容格式调用"""
        body = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=body, timeout=45)
            resp.raise_for_status()
            data = resp.json()
            if data is None:
                return self.build_rule_fallback(payload, "API 返回空响应 (None)")
            content = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "{}").strip()
            if not content or content == "{}":
                return self.build_rule_fallback(payload, "API 返回空 content")
            parsed = self.parse_json_content(content)
            if parsed is None:
                return self.build_rule_fallback(payload, "JSON 解析返回 None")
            return self._parse_llm_response(parsed, payload)
        except Exception as e:
            return self.build_rule_fallback(payload, f"API 调用异常: {e}")

    def _parse_llm_response(self, parsed: dict, payload: dict) -> dict:
        """解析 LLM 返回的 JSON，映射为标准响应格式"""
        if parsed is None:
            return self.build_rule_fallback(payload, "JSON 解析返回 None")

        # 安全解析 confidence（可能是 "中等"、0.5、"0.7" 等）
        conf_raw = parsed.get("confidence", 0.0)
        try:
            if isinstance(conf_raw, (int, float)):
                confidence = round(float(conf_raw), 4)
            elif isinstance(conf_raw, str):
                # 处理中文：低=0.3, 中=0.5, 高=0.7
                conf_map = {"低": 0.3, "中": 0.5, "高": 0.7, "低信心": 0.3, "中信心": 0.5, "高信心": 0.7}
                confidence = conf_map.get(conf_raw, round(float(conf_raw), 4))
            else:
                confidence = 0.5
        except (ValueError, TypeError):
            confidence = 0.5

        return {
            "prediction": str(parsed.get("prediction", "HOLD")).upper(),
            "action": str(parsed.get("action", "HOLD")).upper(),
            "confidence": confidence,
            "reasoning": str(parsed.get("reasoning", ""))[:1200],
            "key_factors": [str(x)[:220] for x in (parsed.get("key_factors") or [])[:6]],
            "risk_flags": [str(x)[:220] for x in (parsed.get("risk_flags") or [])[:6]],
            "close_positions": bool(parsed.get("close_positions", str(parsed.get("action", "")).upper() == "SELL")),
            "source": "llm",
        }
        try:
            resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=body, timeout=45)
            resp.raise_for_status()
            data = resp.json()
            if data is None:
                return self.build_rule_fallback(payload, "API 返回空响应 (None)")
            content = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "{}").strip()
            if not content or content == "{}":
                return self.build_rule_fallback(payload, "API 返回空 content")
            parsed = self.parse_json_content(content)
            if parsed is None:
                return self.build_rule_fallback(payload, "JSON 解析返回 None")
            return {
                "prediction": str(parsed.get("prediction", "HOLD")).upper(),
                "action": str(parsed.get("action", "HOLD")).upper(),
                "confidence": round(float(parsed.get("confidence", 0.0)), 4),
                "reasoning": str(parsed.get("reasoning", ""))[:1200],
                "key_factors": [str(x)[:220] for x in (parsed.get("key_factors") or [])[:6]],
                "risk_flags": [str(x)[:220] for x in (parsed.get("risk_flags") or [])[:6]],
                "close_positions": bool(parsed.get("close_positions", str(parsed.get("action", "")).upper() == "SELL")),
                "source": "llm",
            }
        except Exception as e:
            return self.build_rule_fallback(payload, f"API 调用异常: {e}")


class AIPredictor:
    """AIDecisionEngine 的异步包装器，提供 predict() 协程。

    TradingBot 调用:
        prediction = await self.ai_predictor.predict(btc_data, self.price_history)

    predict() 在线程池中执行 AIDecisionEngine.call_model()，
    完成后返回 "UP" / "DOWN" / "HOLD" 字符串，与 should_trade() 接口兼容。
    """

    def __init__(self):
        self.engine = AIDecisionEngine()

    def _build_payload(self, btc_data: Optional[dict], price_history: list) -> dict:
        """组装 AIDecisionEngine.call_model() 所需的 payload。"""
        btc = btc_data or {}
        current_price = safe_float(btc.get("price"), 0.0) or 0.0

        # 日线开盘价：优先用 btc_data.daily_open，否则估算
        daily_open = safe_float(btc.get("daily_open"), None)
        if not daily_open and price_history:
            daily_open = safe_float(price_history[0].get("price"), None)

        return {
            "btc": {
                "price": current_price,
                "change_24h": safe_float(btc.get("change_24h"), 0.0) or 0.0,
                "high_24h": safe_float(btc.get("high_24h"), 0.0) or 0.0,
                "low_24h": safe_float(btc.get("low_24h"), 0.0) or 0.0,
                "volume_24h": safe_float(btc.get("volume_24h"), 0.0) or 0.0,
            },
            "daily_open": daily_open or 0.0,
            "price_history": price_history[-20:] if price_history else [],
        }

    async def predict(self, btc_data: Optional[dict], price_history: list) -> str:
        """异步预测入口。返回 "UP" / "DOWN" / "HOLD"。"""
        payload = self._build_payload(btc_data, price_history)
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None, self.engine.call_model, payload
            )
            if result is None:
                return "HOLD"
            return str(result.get("prediction", "HOLD")).upper()
        except Exception:
            return "HOLD"


class TradingBot:
    """交易 Bot 主类"""
    
    def __init__(self):
        self.poly_client = PolymarketClient(
            api_key=POLYMARKET_API_KEY,
            private_key=POLYMARKET_PRIVATE_KEY,
            wallet_address=POLYMARKET_WALLET_ADDRESS,
            api_secret=POLYMARKET_API_SECRET,
            api_passphrase=POLYMARKET_API_PASSPHRASE,
            relayer_key=RELAYER_API_KEY,
        )
        self.btc_provider = BTCDataprovider()
        self.ai_engine = AIDecisionEngine()  # 与Paper Bot同步：使用AIDecisionEngine而非AIPredictor
        self.last_ai_signal = {}  # 信号缓存（与Paper Bot同步）
        
        # 历史数据
        self.price_history = []

        # 当前持仓（均值回归策略用）
        # {"side": "Buy_Yes" | "Buy_No", "entry_price": float, "entry_time": datetime}
        self.position = None

        # 交易统计
        self.stats = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_profit": 0.0
        }

    def _load_external_signal(self) -> dict:
        """加载 Simmer Bridge 外部信号（与Paper Bot同步）"""
        return load_openclaw_signal()

    def _get_daily_open(self) -> float:
        """获取BTC今日开盘价（与Paper Bot同步）"""
        try:
            import requests
            url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=2"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if len(data) >= 2:
                    return float(data[-2][4])  # 前一根日K收盘价
        except Exception:
            pass
        return 0.0

    def _notify(self, event_type: str, title: str, message: str, details: dict = None):
        """写入通知到 notifications.json"""
        import json, os
        from datetime import datetime, timezone
        base_dir = os.path.dirname(os.path.abspath(__file__))
        notif_file = os.path.join(base_dir, "notifications.json")
        notifications = []
        if os.path.exists(notif_file):
            try:
                with open(notif_file, "r") as f:
                    notifications = json.load(f).get("notifications", [])
            except Exception:
                pass
        notification = {
            "id": len(notifications) + 1,
            "type": event_type,
            "title": title,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        notifications.insert(0, notification)
        notifications = notifications[:50]
        try:
            with open(notif_file, "w") as f:
                json.dump({"notifications": notifications}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 写入通知失败: {e}")

    async def get_market_info(self, market_id: str) -> Optional[dict]:
        """获取市场详情和当前概率"""
        try:
            # 这里需要根据实际 API 调整
            # Polymarket 的 market ID 格式通常是 uuid
            url = f"https://clob.polymarket.com/markets/{market_id}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except Exception as e:
            print(f"❌ 获取市场信息失败: {e}")
            return None
    
    async def get_current_probabilities(self, condition_id: str) -> Optional[dict]:
        """获取当前 Yes/No 概率"""
        try:
            # 先尝试用 market API 获取价格
            async with aiohttp.ClientSession() as session:
                url = f"{self.poly_client.BASE_URL}/markets/{condition_id}"
                async with session.get(url, headers=self.poly_client.headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        market = await resp.json()
                        tokens = market.get('tokens', [])
                        
                        yes_price = None
                        no_price = None
                        
                        for t in tokens:
                            outcome = t.get('outcome', '').lower()
                            price = float(t.get('price', 0))
                            if 'yes' in outcome or 'up' in outcome:
                                yes_price = price
                            elif 'no' in outcome or 'down' in outcome:
                                no_price = price
                        
                        if yes_price is not None and no_price is not None:
                            return {
                                "yes_price": yes_price,
                                "no_price": no_price,
                            }
            
            # 如果 CLOB market API 失败，尝试从 Gamma API 获取 bestBid/bestAsk（盘口不存在时）
            try:
                gamma_url = f"{self.poly_client.GAMMA_BASE}/markets?condition_id={condition_id}&limit=1"
                async with aiohttp.ClientSession() as gs:
                    async with gs.get(gamma_url, timeout=aiohttp.ClientTimeout(total=10)) as gr:
                        if gr.status == 200:
                            gdata = await gr.json()
                            gmarkets = gdata.get('data', []) if isinstance(gdata, dict) else gdata
                            if gmarkets and isinstance(gmarkets, list) and len(gmarkets) > 0:
                                gm = gmarkets[0]
                                best_bid = safe_float(gm.get('bestBid'))
                                best_ask = safe_float(gm.get('bestAsk'))
                                if best_bid is not None and best_ask is not None:
                                    mid_price = (best_bid + best_ask) / 2
                                    outcome_prices = parse_json_list(gm.get('outcomePrices'))
                                    if len(outcome_prices) >= 2:
                                        yes_price = safe_float(outcome_prices[0], mid_price)
                                        no_price = safe_float(outcome_prices[1], 1 - mid_price)
                                    else:
                                        yes_price = mid_price
                                        no_price = 1 - mid_price
                                    print(f"   [Gamma API fallback] best_bid={best_bid}, best_ask={best_ask}, mid={mid_price:.4f}")
                                    return {
                                        "yes_price": yes_price,
                                        "no_price": no_price,
                                        "best_bid": best_bid,
                                        "best_ask": best_ask,
                                    }
            except Exception as gf_e:
                print(f"   [Gamma fallback] 获取概率失败: {gf_e}")

            # 最后尝试 orderbook（需要 token_id，不是 condition_id）
            token_id = self.poly_client._get_token_id(condition_id, "Buy_Up")
            if not token_id:
                token_id = self.poly_client._get_token_id(condition_id, "Buy_Up")
            if token_id:
                orderbook = await self.poly_client._run_sync(
                    self.poly_client._clob.get_order_book, token_id
                )
                # OrderBookSummary 是 dataclass，用 .bids/.asks
                bids = getattr(orderbook, 'bids', []) or []
                asks = getattr(orderbook, 'asks', []) or []
                if bids and asks:
                    best_bid = float(bids[0].price)
                    best_ask = float(asks[0].price)
                    mid_price = (best_bid + best_ask) / 2
                    return {
                        "yes_price": mid_price,
                        "no_price": 1 - mid_price,
                        "best_bid": best_bid,
                        "best_ask": best_ask,
                    }
        except Exception as e:
            print(f"❌ 获取概率失败: {e}")
        return None
    
    def _calc_pnl_usd(self, entry_px: float, current_px: float, side: str, stake: float = None) -> float:
        """计算持仓浮盈亏 (USD)。多仓(Buy_Up/Buy_Yes)价格涨则盈，空仓(Buy_Down/Buy_No)价格跌则盈。"""
        if stake is None:
            stake = BET_AMOUNT
        shares = stake / entry_px
        if side in ("Buy_Up", "Buy_Yes"):
            return shares * (current_px - entry_px)
        else:
            # 空仓方向相反：价格下跌则盈利
            return shares * (entry_px - current_px)

    async def should_trade(self, prediction: str, probabilities: dict) -> tuple:
        """
        BTC 5分钟方向策略 — 高频交易版本。
        逻辑:
        - |yes_price - 0.50| > HF_ENTRY_THRESHOLD → 开仓
        - 浮盈 > HF_TAKE_PROFIT_USD (默认 $1) → 立即止盈
        - 浮亏 > HF_STOP_LOSS_USD (默认 $1) → 止损
        - 否则等到时间结束
        """
        if not probabilities:
            return "HOLD", "", "无概率数据"
        if not isinstance(probabilities, dict):
            print(f"⚠️ probabilities 不是 dict: type={type(probabilities)}, val={probabilities}")
            return "HOLD", "", "概率数据格式错误"

        yes_price = probabilities.get("yes_price", 0.5)
        no_price = probabilities.get("no_price", 0.5)

        # 检查现有持仓
        if self.position:
            entry_px = self.position.get("entry_price") or 0
            entry_side = self.position.get("side", "")
            stake = self.position.get("stake", BET_AMOUNT)

            if entry_side in ("Buy_Up", "Buy_Yes"):
                pnl = self._calc_pnl_usd(entry_px, yes_price, entry_side, stake)
                # 盈利 > 2U，直接平仓
                if TAKE_PROFIT_ENABLED and pnl >= 2.0:
                    return "SELL", "Sell", f"✅ 止盈: Up {yes_price:.2%} (入场 {entry_px:.2%}, 浮盈 ${pnl:.2f})"
                # 亏损 > 30% 且 剩余时间 > 3分钟，直接平仓
                if STOP_LOSS_ENABLED and pnl <= -0.30 * stake and minutes_left > 3:
                    return "SELL", "Sell", f"🔴 止损: Up {yes_price:.2%} (入场 {entry_px:.2%}, 浮亏 ${pnl:.2f}, 剩余{minutes_left:.1f}分钟)"
                return "HOLD", "", f"持仓中: Up {yes_price:.2%} (入场 {entry_px:.2%}, 浮盈 ${pnl:.2f})"

            elif entry_side in ("Buy_Down", "Buy_No"):
                pnl = self._calc_pnl_usd(entry_px, no_price, entry_side, stake)
                # 盈利 > 2U，直接平仓
                if TAKE_PROFIT_ENABLED and pnl >= 2.0:
                    return "SELL", "Sell", f"✅ 止盈: Down {no_price:.2%} (入场 {entry_px:.2%}, 浮盈 ${pnl:.2f})"
                # 亏损 > 30% 且 剩余时间 > 3分钟，直接平仓
                if STOP_LOSS_ENABLED and pnl <= -0.30 * stake and minutes_left > 3:
                    return "SELL", "Sell", f"🔴 止损: Down {no_price:.2%} (入场 {entry_px:.2%}, 浮亏 ${pnl:.2f}, 剩余{minutes_left:.1f}分钟)"
                return "HOLD", "", f"持仓中: Down {no_price:.2%} (入场 {entry_px:.2%}, 浮盈 ${pnl:.2f})"

        # 无持仓 — 决定是否开仓
        upper = 0.50 + HF_ENTRY_THRESHOLD
        lower = 0.50 - HF_ENTRY_THRESHOLD

        if yes_price > upper and yes_price >= HF_MIN_PROB_THRESHOLD:
            return "BUY", "Buy_Up", f"🚀 信号 UP: Yes {yes_price:.2%} > {upper:.2%} → 买 Up"
        elif yes_price < lower and (1 - yes_price) >= HF_MIN_PROB_THRESHOLD:
            return "BUY", "Buy_Down", f"🚀 信号 DOWN: Yes {yes_price:.2%} < {lower:.2%} → 买 Down (No {no_price:.2%})"
        else:
            return "HOLD", "", f"中性区间: Yes {yes_price:.2%} / No {no_price:.2%} (偏离 >{HF_ENTRY_THRESHOLD:.2%} 才交易)"


    async def execute_trade(self, side: str, amount: float, condition_id: str):
        """执行交易

        side: "Buy_Up" / "Buy_Down" / "Sell"
        - Buy_Up → place_order(side="Buy") 买 Up
        - Buy_Down → place_order(side="Sell") 卖 Up (= 买 Down)
        - Sell → place_order(side="Sell") 平仓
        """
        try:
            probs = await self.get_current_probabilities(condition_id)
            if not probs:
                print("❌ 无法获取价格，跳过下单")
                return False

            # 决定是买还是卖
            if side == "Buy_Up":
                trade_side = "Buy"
                display_name = "Up"
                price = probs.get("best_ask", 0.5)
            elif side == "Buy_Down":
                trade_side = "Sell"
                display_name = "Down"
                price = probs.get("best_bid", 0.5)
            else:  # Sell
                trade_side = "Sell"
                display_name = "Up"
                price = probs.get("best_bid", 0.5)

            print(f"📝 下单: {display_name}, 金额: ${amount}, 价格: {price:.2%}, 方向: {trade_side}")

            # 真实下单（SELL 时传入 position 用于确定正确的 token）
            result = await self.poly_client.place_order(
                condition_id=condition_id,
                side=trade_side,
                amount=amount,
                price=price,
                position=self.position if trade_side == "Sell" else None
            )

            if result and "error" in result:
                print(f"❌ 下单失败: {result['error']}")
                return False
            # 确认订单成功（有 orderID 或类似成功标识）才计入
            is_success = result and (result.get("orderID") or result.get("order_id") or result.get("status") == "success")
            if is_success:
                self.stats["total_trades"] += 1
                print(f"✅ 下单结果: {result}")
            else:
                print(f"⚠️ 下单结果未知: {result}")
            return bool(is_success)

        except Exception as e:
            print(f"❌ 下单失败: {e}")
            return False
    
    async def run_cycle(self, market_id: str, condition_id: str):
        """运行一次交易循环"""
        print(f"\n{'='*50}")
        print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始交易循环")
        print(f"{'='*50}")
        
        # 1. 获取 BTC 数据
        print("\n📊 Step 1: 获取 BTC 数据...")
        btc_data = self.btc_provider.get_price_with_change()
        if btc_data:
            print(f"   BTC 价格: ${btc_data['price']:,.2f}")
            print(f"   24h 变化: {btc_data['change_24h']:+.2f}%")
            
            # 记录历史
            self.price_history.append(btc_data)
            if len(self.price_history) > 100:
                self.price_history.pop(0)
        
        # 2. 获取 Polymarket 市场快照（用于AI + 策略 + OrderBook过滤）
        print("\n📈 Step 2: 获取 Polymarket 市场快照...")
        snapshot = await self.get_current_probabilities(condition_id)
        if not snapshot:
            print("⚠️ 无法获取市场快照，跳过本轮")
            return
        yes_price = snapshot.get("yes_price", 0.5)
        no_price = snapshot.get("no_price", 0.5)
        best_ask = snapshot.get("best_ask", 0.5)
        best_bid = snapshot.get("best_bid", 0.5)
        spread = best_ask - best_bid if best_ask and best_bid else 0.0
        book_size = snapshot.get("best_ask_size", 0) or snapshot.get("bid_size", 0) or 0
        print(f"   Yes={yes_price:.2%} / No={no_price:.2%} | 价差={spread:.2%} | 深度={book_size:.0f}")

        # OrderBook 过滤（已禁用 - 不限制价差和深度）
        # if MAX_SPREAD and spread > MAX_SPREAD:
        #     print(f"   ⛔ 价差过宽({spread:.2%} > {MAX_SPREAD:.2%})，跳过")
        #     return
        # if MIN_TOP_BOOK_SIZE and book_size < MIN_TOP_BOOK_SIZE:
        #     print(f"   ⛔ 卖盘不足({book_size:.0f} < {MIN_TOP_BOOK_SIZE:.0f})，跳过")
        #     return

        # 3. AI 决策（AIDecisionEngine — 与Paper Bot同步）
        print("\n🔮 Step 3: AI 决策 (AIDecisionEngine)...")
        daily_open = self._get_daily_open() if hasattr(self, '_get_daily_open') else btc_data.get('price', 0)
        payload = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "strategy_constraints": {
                "bet_amount": BET_AMOUNT,
                "min_entry_price": MIN_ENTRY_PRICE,
                "max_entry_price": MAX_ENTRY_PRICE,
                "max_spread": MAX_SPREAD,
                "min_top_book_size": MIN_TOP_BOOK_SIZE,
            },
            "btc": btc_data,
            "daily_open": daily_open,
            "current_price": btc_data.get('price', 0),
            "yes_price": yes_price,
            "no_price": no_price,
        }
        ai_result = self.ai_engine.call_model(payload)
        ai_action = ai_result.get("action", "HOLD")
        ai_prediction = ai_result.get("prediction", "HOLD")
        ai_confidence = float(ai_result.get("confidence", 0.0))
        ai_reason = ai_result.get("reasoning", "AI未提供理由")
        print(f"   AI动作: {ai_action} | 方向: {ai_prediction} | 置信度: {ai_confidence:.0%}")
        print(f"   AI理由: {ai_reason[:80]}")

        # 4. 策略信号（BTC 5m价差套利 — 与Paper Bot同步）
        print("\n📐 Step 4: 策略信号...")
        try:
            from strategies import generate_signals as get_strategy_signals
            strategy_result = get_strategy_signals(yes_price, no_price, btc_data)
            strategy_signal = strategy_result.get("signal", "HOLD")
            strategy_confidence = strategy_result.get("confidence", 0.0)
            print(f"   策略信号: {strategy_signal} | 置信度: {strategy_confidence:.0%}")
        except Exception as e:
            strategy_signal = "HOLD"
            strategy_confidence = 0.0
            print(f"   策略异常: {e}，回退HOLD")

        # 5. Simmer Bridge 外部信号覆盖（与Paper Bot同步）
        external = self._load_external_signal()
        if external and external.get("signal") not in (None, "HOLD"):
            ext_signal = external.get("signal")
            ext_conf = external.get("confidence", 0.0)
            ext_reason = external.get("reason", "")
            # 外部信号置信度 > 70% 时覆盖AI
            if ext_conf > 0.70:
                ai_action = "BUY"
                ai_prediction = ext_signal
                print(f"   🔁 Simmer覆盖: {ext_signal} (置信度{ext_conf:.0%}) → AI动作强制BUY {ext_signal}")
            elif ai_action == "HOLD" and ext_conf > 0.50:
                ai_action = "BUY"
                ai_prediction = ext_signal
                print(f"   🔁 Simmer引导: {ext_signal} (置信度{ext_conf:.0%}) → AI动作覆盖为BUY {ext_signal}")

        # 6. 策略覆盖AI HOLD（置信度≥50%）
        combined_signal = ai_prediction
        combined_action = ai_action
        override_reason = ""
        if combined_action == "HOLD" and strategy_signal != "HOLD" and strategy_confidence >= 0.50:
            combined_signal = strategy_signal
            combined_action = "BUY"
            override_reason = f"[策略覆盖] 置信度{strategy_confidence:.0%} ≥ 50%"
            print(f"   ✅ 策略覆盖AI HOLD: {strategy_signal} (策略置信度{strategy_confidence:.0%})")
        # 策略反向AI时，策略置信度≥75%才覆盖
        elif combined_signal != strategy_signal and strategy_signal != "HOLD" and strategy_confidence >= 0.75:
            combined_signal = strategy_signal
            combined_action = "BUY"
            override_reason = f"[策略反向覆盖] 置信度{strategy_confidence:.0%} ≥ 75%"
            print(f"   ✅ 策略反向覆盖: AI={combined_signal} → {strategy_signal}")

        # 7. 均值回归 + 止盈止损 决策
        print("\n🎯 Step 5: 均值回归决策...")
        probabilities = snapshot
        action, side, reason = await self.should_trade(combined_signal, probabilities)
        # 注入AI/策略覆盖原因
        if override_reason:
            reason = f"{override_reason} | {reason}"
        trading_enabled = load_trading_control().get("trading_enabled", True)
        if action == "BUY" and not trading_enabled:
            action = "HOLD"
            reason = "交易已关闭，新开仓暂停"
        print(f"   决策: [{action}] {reason}")

        # 5. Execute trade / close position
        if action == "BUY":
            print(f"\n💰 Step 5: 开仓...")
            success = await self.execute_trade(side, BET_AMOUNT, condition_id)
            if success:
                entry_price = probabilities.get("yes_price" if side == "Buy_Up" else "no_price", 0.5)
                self.position = {
                    "side": side,  # "Buy_Up" or "Buy_Down"
                    "outcome": "UP" if "Up" in side else "DOWN",
                    "entry_price": entry_price,
                    "entry_time": datetime.now(),
                }
                print(f"   📌 已记录持仓: {self.position['side']} @ {entry_price:.2%}")
        elif action == "SELL":
            print(f"\n💰 Step 5: 平仓...")
            close_side = "Sell"
            success = await self.execute_trade(close_side, BET_AMOUNT, condition_id)
            if success and self.position:
                entry_side = self.position.get("side", "")
                entry_price = self.position.get("entry_price", 0)
                current_price = probabilities.get("yes_price" if "Up" in entry_side else "no_price", 0)
                shares = BET_AMOUNT / entry_price
                pnl = shares * (current_price - entry_price)  # 转换为单位盈亏 × 股数 = 美元盈亏
                self.stats["total_trades"] += 1
                if pnl >= 0:
                    self.stats["winning_trades"] += 1
                    self.stats["total_profit"] += pnl
                else:
                    self.stats["losing_trades"] += 1
                    self.stats["total_profit"] += pnl
                print(f"   📤 平仓完成: PnL {pnl:+.2%} (入场 {entry_price:.2%} -> 出场 {current_price:.2%})")
                self.position = None
        else:
            print(f"\n⏭️ 跳过交易: {reason}")
        # 6. 显示统计
        print(f"\n📊 统计: 总交易 {self.stats['total_trades']} 笔 | 胜率 {self.stats['winning_trades']}/{self.stats['total_trades']}")
        if self.position:
            print(f"📌 当前持仓: {self.position['side']} @ {self.position['entry_price']:.2%}")
        
        # 7. 写入状态文件
        decision = action  # "BUY" / "SELL" / "HOLD"
        write_status(
            self,
            None,
            btc_data,
            combined_signal,
            probabilities,
            decision,
            extra={
                "decision_reason": reason,
                "trading_enabled": trading_enabled,
            },
        )
    
    async def run_forever(self, interval_seconds: int = 300):
        """持续运行"""
        market_input = BTC_UPDOWN_MARKET_ID
        
        print(f"""
🤖 Polymarket BTC 5m 交易 Bot 启动!
        
配置:
  - 下注金额: ${BET_AMOUNT}
  - 最大单笔: ${MAX_BET_AMOUNT}
  - 最小概率差: {MIN_PROBABILITY_DIFF:.1%}
  - 止损: {'开启' if STOP_LOSS_ENABLED else '关闭'}
  - 运行间隔: {interval_seconds} 秒
  - 市场: {market_input}
        
按 Ctrl+C 停止
        """)
        
        if not market_input:
            print("❌ 未配置市场 ID!")
            print("   在 .env 中设置 BTC_UPDOWN_MARKET_ID")
            print("   可以是: URL、slug 或 Condition ID")
            return
        
        current_condition_id = None
        
        while True:
            try:
                # 获取/刷新 Condition ID
                market_info = await get_current_btc_5m_market(self.poly_client)
                
                if market_info:
                    condition_id = market_info['condition_id']
                    
                    if condition_id != current_condition_id:
                        old_condition_id = current_condition_id
                        # 市场窗口切换，先平掉旧窗口的持仓
                        if self.position and old_condition_id:
                            print(f"\n🔄 市场窗口切换，平掉旧仓...")
                            close_ok = await self.execute_trade("Sell", BET_AMOUNT, old_condition_id)
                            if close_ok:
                                self.position = None
                                print("✅ 旧仓已平，等待新窗口信号")
                        current_condition_id = condition_id
                        print(f"\n🆕 市场已连接: {market_info.get('question', 'Unknown')}")
                        print(f"   Condition ID: {condition_id}")
                        # 设置 CLOB token IDs（从 Gamma API 直接获取，避免重复查询）
                        clob_ids_raw = market_info.get('clob_token_ids', [])
                        if isinstance(clob_ids_raw, str):
                            clob_ids = json.loads(clob_ids_raw) if clob_ids_raw else []
                        else:
                            clob_ids = clob_ids_raw or []
                        if clob_ids:
                            self.poly_client.set_clob_token_ids(condition_id, clob_ids)
                            print(f"   CLOB Token IDs: Up={clob_ids[0][:20]}... Down={clob_ids[1][:20]}...")
                    
                    await self.run_cycle(None, condition_id)
                else:
                    print(f"\n⚠️ 无法获取 BTC 5m 市场，等待...")
                    
            except Exception as e:
                print(f"❌ 循环出错: {e}")
            
            print(f"\n😴 等待 {interval_seconds} 秒...")
            await asyncio.sleep(interval_seconds)




async def main():
    """主入口 - 真实交易模式"""
    if not POLYMARKET_WALLET_ADDRESS:
        print("❌ 请在 .env 文件中设置 POLYMARKET_WALLET_ADDRESS")
        return

    if not POLYMARKET_API_KEY:
        print("❌ 需要在 .env 文件中设置 POLYMARKET_API_KEY")
        print("   参考 .env.example")
        return

    bot = TradingBot()
    await bot.run_forever(interval_seconds=30)  # 30秒间隔


if __name__ == "__main__":
    asyncio.run(main())
