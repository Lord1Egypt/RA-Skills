#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weather High-Temp Sniper v1.0.0
================================
Automated trading bot for Polymarket weather event markets

核心功能：
- Pre-generate event slugs for 33 cities x 2 days (today & tomorrow)
- Asynchronously fetch Gamma Events + CLOB Orderbooks
- Monitor during local time 09:00-09:55, check every 5 minutes
- Trigger condition: CLOB best_ask >= 0.35
- Buy 1 share YES at best_ask price (with 15% slippage protection)
- 10:00 fallback: For unpositioned events, buy highest CLOB mid-price outcome
- Print positions/trades/PnL report every 4 minutes
- Disk caching + rate limiting + retries

用法：
  python sniper.py [--dry-run] [--once] [--status] [--live]

  --dry-run   Scan only, no real orders (default)
  --once      Run one scan cycle then exit (for debugging)
  --status    Show current positions and statistics
  --live      Real trading (requires API credentials configured)

实盘配置（--live 模式）：
  1. Install dependencies: pip install py-clob-client
  2. Set environment variables:
     export PRIVATE_KEY="0x..."           # EOA wallet private key
     export PROXY_WALLET="0x..."         # Polymarket proxy wallet address (export from website)
     export SIGNER_TYPE="2"              # 0=EOA, 2=Gnosis Safe (recommended)
  3. First run automatically derives L2 API credentials (API key/secret/passphrase)
  4. L2 credentials saved to memory, auto-used during session

认证机制：
  - L1: EIP-712 signature (private key) → Derive API credentials
  - L2: HMAC-SHA256 (API credentials) → Order/cancel/query
  Orders themselves need EIP-712 signature, request headers need HMAC signature
"""

import os
import sys
import json
import asyncio
import signal
import argparse
import math
import hashlib
import re
import base64
import hmac
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_UP

import aiohttp
import requests
from pytz import timezone as tz
from dotenv import load_dotenv
from eth_account import Account

# py-clob-client (required for live trading)
try:
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType
    from py_clob_client.order_builder.constants import BUY
    _HAS_PY_CLOB_CLIENT = True
except ImportError as e:
    ClobClient = ApiCreds = OrderArgs = OrderType = BUY = None
    _HAS_PY_CLOB_CLIENT = False
    print(f"[WARN] py-clob-client not available: {e}")
    print("[WARN] Install with: pip install py-clob-client")

# =============================================================================
# CONFIG
# =============================================================================

load_dotenv()

# =============================================================================
# SkillPay Billing Configuration (Developer Config - 开发者内置)
# =============================================================================
SKILL_BILLING_API_KEY = "sk_a9015b19df64f2248966c345e94dbc374a4482843e09c1cef83dd51306b7c6e9"
SKILL_ID = "e56f2a83-819c-4e43-a457-5442ebba0098"
BILLING_URL = "https://skillpay.me/api/v1/billing"

# =============================================================================
# Static Data (城市列表、时区映射 - 固定不变)
# =============================================================================

# City slug list (33 cities)
CITY_SLUGS = [
    "taipei", "seoul", "shanghai", "shenzhen", "wuhan", "beijing", "chongqing",
    "tokyo", "singapore", "hong-kong", "tel-aviv", "lucknow",
    "london", "warsaw", "paris", "milan", "madrid", "munich", "ankara",
    "atlanta", "nyc", "toronto", "miami", "chicago", "dallas", "seattle",
    "wellington", "buenos-aires", "sao-paulo",
    "denver", "houston", "austin", "san-francisco",
]

# Timezone mapping (city → IANA timezone name)
TIMEZONES = {
    "nyc": "America/New_York",
    "chicago": "America/Chicago",
    "miami": "America/New_York",
    "dallas": "America/Chicago",
    "seattle": "America/Los_Angeles",
    "atlanta": "America/New_York",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "munich": "Europe/Berlin",
    "ankara": "Europe/Istanbul",
    "seoul": "Asia/Seoul",
    "tokyo": "Asia/Tokyo",
    "shanghai": "Asia/Shanghai",
    "shenzhen": "Asia/Shanghai",
    "wuhan": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "chongqing": "Asia/Shanghai",
    "singapore": "Asia/Singapore",
    "tel-aviv": "Asia/Jerusalem",
    "toronto": "America/Toronto",
    "buenos-aires": "America/Argentina/Buenos_Aires",
    "wellington": "Pacific/Auckland",
    # 补充缺失的时区
    "taipei": "Asia/Taipei",
    "hong-kong": "Asia/Hong_Kong",
    "lucknow": "Asia/Kolkata",
    "warsaw": "Europe/Warsaw",
    "milan": "Europe/Rome",
    "madrid": "Europe/Madrid",
    "sao-paulo": "America/Sao_Paulo",
    # 新增美国城市
    "denver": "America/Denver",
    "houston": "America/Chicago",
    "austin": "America/Chicago",
    "san-francisco": "America/Los_Angeles",
}

# Month names (lowercase)
MONTHS = ["january","february","march","april","may","june",
          "july","august","september","october","november","december"]

# =============================================================================
# Static Constants (不依赖 .env 的固定常量)
# =============================================================================

# API endpoints (fixed)
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"

# =============================================================================
# User Configuration Loader (从 .env 加载用户配置)
# =============================================================================

def load_user_config():
    """Load all user-configurable parameters from environment variables"""
    config = {}

    # SkillPay Billing (required - for billing)
    config['SKILLPAY_USER_ID'] = os.getenv('SKILLPAY_USER_ID')

    # Polymarket API (required)
    config['PRIVATE_KEY'] = os.getenv('PRIVATE_KEY')
    config['PROXY_WALLET'] = os.getenv('PROXY_WALLET')
    config['POLY_API_KEY'] = os.getenv('POLY_API_KEY')
    config['POLY_API_SECRET'] = os.getenv('POLY_API_SECRET')
    config['POLY_API_PASSPHRASE'] = os.getenv('POLY_API_PASSPHRASE')
    config['SIGNER_TYPE'] = int(os.getenv('SIGNER_TYPE', '2'))

    # Trading Parameters
    config['TRADE_AMOUNT_USD'] = float(os.getenv('TRADE_AMOUNT_USD', '1.0'))
    config['MIN_ORDERBOOK_SIZE'] = float(os.getenv('MIN_ORDERBOOK_SIZE', '1.0'))
    config['SLIPPAGE_TOLERANCE'] = float(os.getenv('SLIPPAGE_TOLERANCE', '0.15'))
    config['ENTRY_THRESHOLD'] = float(os.getenv('ENTRY_THRESHOLD', '0.35'))
    config['MAX_COST_PER_TRADE'] = float(os.getenv('MAX_COST_PER_TRADE', '1.2'))

    # Time Windows (Local Time)
    config['MONITOR_START_HOUR'] = float(os.getenv('MONITOR_START_HOUR', '9'))
    config['MONITOR_END_HOUR'] = float(os.getenv('MONITOR_END_HOUR', '9.9167'))
    config['FALLBACK_START_HOUR'] = float(os.getenv('FALLBACK_START_HOUR', '10'))
    config['FALLBACK_WINDOW_MINUTES'] = int(os.getenv('FALLBACK_WINDOW_MINUTES', '5'))

    # Execution Intervals (Seconds)
    config['CHECK_INTERVAL'] = int(os.getenv('CHECK_INTERVAL', '300'))
    config['REPORT_INTERVAL'] = int(os.getenv('REPORT_INTERVAL', '240'))

    # Cache TTLs (Seconds)
    config['CACHE_TTL'] = int(os.getenv('CACHE_TTL', '3600'))
    config['GAMMA_CACHE_TTL'] = int(os.getenv('GAMMA_CACHE_TTL', '300'))
    config['CLOB_CACHE_TTL'] = int(os.getenv('CLOB_CACHE_TTL', '30'))

    # Rate Limiting
    config['MAX_CONCURRENT_REQUESTS'] = int(os.getenv('MAX_CONCURRENT_REQUESTS', '50'))
    config['REQUEST_DELAY'] = float(os.getenv('REQUEST_DELAY', '0.05'))
    config['RETRY_BACKOFF_BASE'] = float(os.getenv('RETRY_BACKOFF_BASE', '0.5'))
    config['MAX_RETRIES'] = int(os.getenv('MAX_RETRIES', '3'))
    config['RETRY_DELAY'] = float(os.getenv('RETRY_DELAY', '1.0'))

    # Paths
    config['STATE_FILE'] = Path(os.getenv('STATE_FILE', 'state.json'))
    config['CACHE_DIR'] = Path(os.getenv('CACHE_DIR', 'cache'))

    return config

# Load user configuration
user_config = load_user_config()

# Assign to module-level constants for backward compatibility
SKILLPAY_USER_ID = user_config.get('SKILLPAY_USER_ID')
PRIVATE_KEY = user_config['PRIVATE_KEY']
PROXY_WALLET = user_config['PROXY_WALLET']
POLY_API_KEY = user_config['POLY_API_KEY']
POLY_API_SECRET = user_config['POLY_API_SECRET']
POLY_API_PASSPHRASE = user_config['POLY_API_PASSPHRASE']
SIGNER_TYPE = user_config['SIGNER_TYPE']
TRADE_AMOUNT_USD = user_config['TRADE_AMOUNT_USD']
MIN_ORDERBOOK_SIZE = user_config['MIN_ORDERBOOK_SIZE']
SLIPPAGE_TOLERANCE = user_config['SLIPPAGE_TOLERANCE']
ENTRY_THRESHOLD = user_config['ENTRY_THRESHOLD']
MAX_COST_PER_TRADE = user_config['MAX_COST_PER_TRADE']
MONITOR_START_HOUR = user_config['MONITOR_START_HOUR']
MONITOR_END_HOUR = user_config['MONITOR_END_HOUR']
FALLBACK_START_HOUR = user_config['FALLBACK_START_HOUR']
FALLBACK_WINDOW_MINUTES = user_config['FALLBACK_WINDOW_MINUTES']
CHECK_INTERVAL = user_config['CHECK_INTERVAL']
REPORT_INTERVAL = user_config['REPORT_INTERVAL']
CACHE_TTL = user_config['CACHE_TTL']
GAMMA_CACHE_TTL = user_config['GAMMA_CACHE_TTL']
CLOB_CACHE_TTL = user_config['CLOB_CACHE_TTL']
MAX_CONCURRENT_REQUESTS = user_config['MAX_CONCURRENT_REQUESTS']
REQUEST_DELAY = user_config['REQUEST_DELAY']
RETRY_BACKOFF_BASE = user_config['RETRY_BACKOFF_BASE']
MAX_RETRIES = user_config['MAX_RETRIES']
RETRY_DELAY = user_config['RETRY_DELAY']
STATE_FILE = user_config['STATE_FILE']
CACHE_DIR = user_config['CACHE_DIR']

# Setup cache directories
CACHE_DIR.mkdir(exist_ok=True)
EVENTS_CACHE_DIR = CACHE_DIR / "events"
ORDERBOOKS_CACHE_DIR = CACHE_DIR / "orderbooks"
EVENTS_CACHE_DIR.mkdir(exist_ok=True)
ORDERBOOKS_CACHE_DIR.mkdir(exist_ok=True)

# =============================================================================
# SkillPay Billing Functions (per-order billing - 0.01 USDT deducted each successful order)
# =============================================================================
import requests

# Pre-check constant: keep at least one billing quota
MIN_CHARGE_AMOUNT = 0.01  # USDT

def billing_charge(user_id: str) -> dict:
    """
    Deduct fee: called after each successful order
    Uses skill preset rate (configured in SkillPay backend, currently 0.01 USDT/call)

    Args:
        user_id: SKILLPAY_USER_ID

    Returns:
        {'ok': True, 'balance': float} 或 {'ok': False, 'balance': float, 'payment_url': str}
    """
    try:
        resp = requests.post(
            f"{BILLING_URL}/charge",
            headers={
                'X-API-Key': SKILL_BILLING_API_KEY,
                'Content-Type': 'application/json'
            },
            json={
                'user_id': user_id,
                'skill_id': SKILL_ID,
                'amount': 0.01,  # 每次调用 0.01 USDT（硬编码费率）
            },
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get('success'):
            return {'ok': True, 'balance': data['balance']}
        return {
            'ok': False,
            'balance': data.get('balance', 0),
            'payment_url': data.get('payment_url')
        }
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Billing charge failed (network error): {e}")
        return {'ok': False, 'balance': 0.0}
    except Exception as e:
        print(f"[ERROR] Billing charge failed: {e}")
        return {'ok': False, 'balance': 0.0}

def billing_get_balance(user_id: str) -> float:
    """
    Query user balance

    Args:
        user_id: 用户钱包地址

    Returns:
        余额（USDT），失败返回 0.0
    """
    try:
        resp = requests.get(
            f"{BILLING_URL}/balance",
            params={'user_id': user_id},
            headers={'X-API-Key': SKILL_BILLING_API_KEY},
            timeout=10
        )
        resp.raise_for_status()
        return float(resp.json()['balance'])
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get balance (network error): {e}")
        return 0.0
    except Exception as e:
        print(f"[ERROR] Failed to get balance: {e}")
        return 0.0

def billing_get_payment_link(user_id: str, amount: float = 8) -> str:
    """
    Generate payment link (minimum 8 USDT)

    Args:
        user_id: 用户钱包地址
        amount: 充值金额（默认 8 USDT）

    Returns:
        payment_url 字符串
    """
    try:
        resp = requests.post(
            f"{BILLING_URL}/payment-link",
            headers={'X-API-Key': SKILL_BILLING_API_KEY},
            json={'user_id': user_id, 'amount': amount},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()['payment_url']
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get payment link (network error): {e}")
        return ""
    except Exception as e:
        print(f"[ERROR] Failed to get payment link: {e}")
        return ""


def load_state() -> dict:
    """加载机器人状态（支持旧格式迁移）"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)

        # 迁移：检测positions的key格式
        positions = state.get("positions", {})
        if positions:
            def is_city_date_key(key: str) -> bool:
                """检查key是否为 city_YYYY-MM-DD 格式"""
                if '_' not in key:
                    return False
                parts = key.split('_')
                if len(parts) != 2:
                    return False
                date_str = parts[1]
                # 验证日期格式
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False

            # 如果没有任何一个key符合city_date格式，认为是旧格式
            if not any(is_city_date_key(k) for k in positions.keys()):
                new_positions = {}
                for pos in positions.values():
                    city = pos.get('city')
                    date = pos.get('date')
                    if city and date:
                        key = f"{city}_{date}"
                        new_positions[key] = pos
                state["positions"] = new_positions
                print("[MIGRATE] State format migrated from market_id keys to city_date keys")

        # 确保fallback_executed存在
        if "fallback_executed" not in state:
            state["fallback_executed"] = []

        return state
    return {
        "balance": 10000.0,  # 虚拟余额（仅报告用）
        "positions": {},      # city_date → position dict
        "trades": [],         # 交易历史
        "stats": {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "total_pnl": 0.0,
        },
        "last_report": None,
        "last_full_scan": None,
        "fallback_executed": [],  # city_date list of executed fallbacks
    }

def save_state(state: dict):
    """保存状态（原子写入：先写临时文件再替换）"""
    tmp_file = STATE_FILE.with_suffix('.tmp')
    with open(tmp_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    tmp_file.replace(STATE_FILE)  # 原子替换（POSIX保证）

def load_private_key() -> str:
    """从环境变量加载私钥（返回纯 hex，无 0x 前缀）"""
    pk = os.getenv("PRIVATE_KEY")
    if not pk:
        raise ValueError("PRIVATE_KEY 未设置")
    # SDK 需要不带 0x 前缀的纯 hex 字符串
    if pk.startswith("0x") or pk.startswith("0X"):
        pk = pk[2:]
    return pk


async def init_auth_manager() -> PolymarketAuth:
    """
    初始化认证管理器。
    - .env 已有 POLY_API_KEY/SECRET/PASSPHRASE → 直接加载，continue running
    - 没有 → 派生并打印到控制台，程序退出，等待手动写入 .env
    """
    private_key = load_private_key()

    proxy_wallet = os.getenv("PROXY_WALLET") or None
    signer_type = int(os.getenv("SIGNER_TYPE", "2"))

    auth = PolymarketAuth(
        private_key=private_key,
        proxy_wallet=proxy_wallet,
        signer_type=signer_type,
    )

    api_key = os.getenv("POLY_API_KEY")
    api_secret = os.getenv("POLY_API_SECRET")
    api_passphrase = os.getenv("POLY_API_PASSPHRASE")

    if api_key and api_secret and api_passphrase:
        auth.api_key = api_key
        auth.api_secret = api_secret
        auth.api_passphrase = api_passphrase
        print(f"[AUTH] [OK] Loaded credentials from .env  (key: {api_key[:10]}...)")
        return auth

    # .env 里没有 → 派生，打印，退出
    auth.derive_l2_credentials()  # 同步方法，不要 await
    print("[INFO] Fill .env and rerun --live to continue.")
    sys.exit(0)

# =============================================================================
# API CLIENT
# =============================================================================

class ApiClient:
    def __init__(self):
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, url: str, params: dict = None, cache_dir: Path = None, ttl: int = CACHE_TTL) -> Optional[dict]:
        """通用HTTP GET（带缓存和限流）"""
        async with self.semaphore:
            # 缓存key = URL + params的hash
            cache_key = hashlib.md5(f"{url}{params}".encode()).hexdigest()[:16]

            if cache_dir:
                cache_file = cache_dir / f"{cache_key}.json"
                if cache_file.exists():
                    cache_age = datetime.now().timestamp() - cache_file.stat().st_mtime
                    if cache_age < ttl:
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            return json.load(f)

            try:
                await asyncio.sleep(REQUEST_DELAY)  # 限流
                async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status != 200:
                        print(f"[WARN]  HTTP {resp.status} for {url}")
                        return None
                    data = await resp.json()
                    if cache_dir:
                        with open(cache_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                    return data
            except Exception as e:
                print(f"[WARN]  Request failed: {type(e).__name__}: {e}")
                return None

    async def fetch_gamma_event(self, slug: str) -> Optional[dict]:
        """获取Gamma event"""
        url = f"{GAMMA_API_BASE}/events"
        params = {"slug": slug}
        return await self.fetch(url, params, EVENTS_CACHE_DIR, ttl=GAMMA_CACHE_TTL)

    async def fetch_clob_orderbook(self, token_id: str) -> Optional[dict]:
        """获取CLOB订单簿"""
        url = f"{CLOB_API_BASE}/book"
        params = {"token_id": token_id}
        # orderbook缓存时间短一点（实时性要求高）
        return await self.fetch(url, params, ORDERBOOKS_CACHE_DIR, ttl=CLOB_CACHE_TTL)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def parse_temp_range(question: str) -> Optional[Tuple[float, float]]:
    """从question解析温度范围"""
    import re
    if not question:
        return None
    num = r'(-?\d+(?:\.\d+)?)'
    if re.search(r'or below', question, re.IGNORECASE):
        m = re.search(num + r'[°]?[FC] or below', question, re.IGNORECASE)
        if m: return (-999.0, float(m.group(1)))
    if re.search(r'or higher', question, re.IGNORECASE):
        m = re.search(num + r'[°]?[FC] or higher', question, re.IGNORECASE)
        if m: return (float(m.group(1)), 999.0)
    m = re.search(r'between ' + num + r'-' + num + r'[°]?[FC]', question, re.IGNORECASE)
    if m: return (float(m.group(1)), float(m.group(2)))
    m = re.search(r'be ' + num + r'[°]?[FC] on', question, re.IGNORECASE)
    if m:
        v = float(m.group(1))
        return (v, v)
    return None

def generate_slug(city_slug: str, date_obj: datetime) -> str:
    """生成event slug"""
    month = MONTHS[date_obj.month - 1]
    day = date_obj.day
    year = date_obj.year
    return f"highest-temperature-in-{city_slug}-on-{month}-{day}-{year}"

def is_in_monitor_window(city_slug: str, event_date_str: str) -> bool:
    """检查当前是否在该event的本地时间监控窗口内"""
    tz_name = TIMEZONES.get(city_slug, "UTC")
    local_tz = tz(tz_name)

    now_utc = datetime.now(timezone.utc)
    now_local = now_utc.astimezone(local_tz)

    # 事件本地日期
    event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()

    return now_local.date() == event_date and \
           MONITOR_START_HOUR <= now_local.hour + now_local.minute/60 <= MONITOR_END_HOUR

def is_fallback_time(city_slug: str, event_date_str: str) -> bool:
    """检查是否在fallback时间窗口（本地时间10:00-10:04）"""
    tz_name = TIMEZONES.get(city_slug, "UTC")
    local_tz = tz(tz_name)

    now_utc = datetime.now(timezone.utc)
    now_local = now_utc.astimezone(local_tz)

    event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()

    # 窗口：10:00-10:04（严格5分钟窗口，防止重复触发）
    in_time_window = (now_local.hour == FALLBACK_START_HOUR and
                      now_local.minute < FALLBACK_WINDOW_MINUTES)

    return now_local.date() == event_date and in_time_window

def is_city_still_tradeable(city: str, date_str: str) -> bool:
    """检查城市今日市场是否仍可交易（10:05前）"""
    tz_name = TIMEZONES.get(city, "UTC")
    local_tz = tz(tz_name)
    now_local = datetime.now(timezone.utc).astimezone(local_tz)
    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # 如果不是今天，总是可查
    if now_local.date() != event_date:
        return True

    # 今天的市场：10:05 后不再查询
    cutoff_minutes = FALLBACK_START_HOUR * 60 + FALLBACK_WINDOW_MINUTES
    current_minutes = now_local.hour * 60 + now_local.minute
    return current_minutes < cutoff_minutes

def extract_city_date_from_slug(slug: str) -> Tuple[str, str]:
    """从slug提取city和date（YYYY-MM-DD）"""
    # slug格式: highest-temperature-in-{city}-on-{month}-{day}-{year}
    parts = slug.split("-on-")
    if len(parts) != 2:
        return None, None
    city = parts[0].replace("highest-temperature-in-", "")
    date_parts = parts[1].split("-")
    if len(date_parts) != 3:
        return None, None
    month_str, day_str, year_str = date_parts
    month = MONTHS.index(month_str) + 1
    date = f"{year_str}-{month:02d}-{int(day_str):02d}"
    return city, date

# =============================================================================
# TRADING LOGIC
# =============================================================================

async def scan_and_find_trades(api_client: ApiClient, date_range: List[datetime]) -> List[dict]:
    """Scan all markets, find tradeable candidates (select Yes outcome with highest best_ask per event)"""
    all_slugs = []
    for date_obj in date_range:
        for city in CITY_SLUGS:
            slug = generate_slug(city, date_obj)
            all_slugs.append((city, slug, date_obj.strftime("%Y-%m-%d")))

    print(f"[SCAN] Total {len(all_slugs)} slugs to check")

    # 第一步：并发收集所有markets（不筛选）
    raw_candidates = []  # 每个market一个entry

    async def fetch_gamma_and_extract(city, slug, date_str):
        """并发获取Gamma并提取candidate"""
        # Pre-filter: skip if today's market past 10:05
        if not is_city_still_tradeable(city, date_str):
            return []

        events = await api_client.fetch_gamma_event(slug)
        if not events or not isinstance(events, list) or len(events) == 0:
            return []

        event = events[0]
        candidates = []

        for market in event.get("markets", []):
            market_id = str(market.get("id"))
            clob_token_ids_str = market.get("clobTokenIds", "[]")
            token_ids = json.loads(clob_token_ids_str)
            if len(token_ids) < 1:
                continue

            # 使用 outcomes 字段确定 YES token 的正确索引
            outcomes_str = market.get("outcomes", '["Yes","No"]')
            outcomes = json.loads(outcomes_str)

            # 找到 "Yes" 在 outcomes 中的位置
            try:
                yes_idx = next(i for i, o in enumerate(outcomes)
                               if str(o).strip().lower() == "yes")
            except StopIteration:
                continue  # No Yes outcome, skipping

            if yes_idx >= len(token_ids):
                continue  # token 数量对不上，数据异常

            # 获取 YES 和 NO 的 token ID（二元市场）
            yes_token_id = token_ids[yes_idx]
            no_idx = 1 - yes_idx  # 另一个索引
            if no_idx >= len(token_ids):
                continue  # token 数量异常
            no_token_id = token_ids[no_idx]

            question = market.get("question", "")
            rng = parse_temp_range(question)
            if not rng:
                continue

            # 使用 YES 对应的价格
            outcome_prices_raw = json.loads(market.get("outcomePrices", "[0.5,0.5]"))
            if yes_idx >= len(outcome_prices_raw):
                continue  # 价格数组异常
            gamma_price = float(outcome_prices_raw[yes_idx])

            # 保存原始数据（不做任何筛选）
            candidates.append({
                "city": city,
                "date": date_str,
                "market_id": market_id,
                "token_id": yes_token_id,        # YES token（保留用于后续CLOB查询）
                "yes_token_id": yes_token_id,    # 显式命名
                "no_token_id": no_token_id,      # 互补验证用（实盘必需）
                "question": question,
                "range": rng,
                "gamma_price": gamma_price,  # 可能缺失，后续用 .get()
                "slug": slug,
            })

        return candidates

    # Execute all Gamma requests concurrently
    tasks = [fetch_gamma_and_extract(city, slug, date_str)
             for city, slug, date_str in all_slugs]
    results = await asyncio.gather(*tasks)

    # 合并所有候选
    for cand_list in results:
        raw_candidates.extend(cand_list)

    print(f"[SCAN] Raw outcomes collected: {len(raw_candidates)}")

    # 第二步：并发为每个candidate获取CLOB数据（批量）
    enriched = []

    async def fetch_clob_for_candidate(cand):
        """并发获取YES和NO token的订单簿"""
        yes_book = await api_client.fetch_clob_orderbook(cand['yes_token_id'])
        no_book = await api_client.fetch_clob_orderbook(cand['no_token_id'])
        return (cand, yes_book, no_book)

    tasks = [fetch_clob_for_candidate(cand) for cand in raw_candidates]
    results = await asyncio.gather(*tasks)

    for cand, yes_book, no_book in results:
        if not yes_book or not no_book:
            continue

        yes_asks = yes_book.get("asks", [])
        yes_bids = yes_book.get("bids", [])
        no_asks = no_book.get("asks", [])
        no_bids = no_book.get("bids", [])

        if not yes_asks or not no_asks:
            continue

        # asks 是降序（最高价在前），需要排序取第一个（最低价 = best ask）
        yes_asks_sorted = sorted(yes_asks, key=lambda x: float(x['price']))
        no_asks_sorted = sorted(no_asks, key=lambda x: float(x['price']))

        yes_ask = float(yes_asks_sorted[0]['price'])
        yes_ask_size = float(yes_asks_sorted[0]['size'])
        no_ask = float(no_asks_sorted[0]['price'])

        # 互补验证（YES + NO 应在 1.0 附近，允许 spread 误差 ±15%）
        complement = yes_ask + no_ask
        if not (0.90 <= complement <= 1.15):
            print(f"[WARN]  {cand['city']}/{cand['date']} YES+NO={complement:.3f}, skipping")
            continue

        # 验证通过，打印调试信息
        print(f"[DEBUG] {cand['city']}/{cand['date']} YES_ask={yes_ask:.3f} NO_ask={no_ask:.3f} sum={complement:.3f} size={yes_ask_size:.1f}")

        best_ask = yes_ask
        best_ask_size = yes_ask_size
        best_bid = float(yes_bids[-1]['price']) if yes_bids else None  # bids升序，取最后一个=best bid
        best_bid_size = float(yes_bids[-1]['size']) if yes_bids else 0.0

        if best_ask_size < MIN_ORDERBOOK_SIZE:
            continue

        cost_usd = TRADE_AMOUNT_USD  # 从配置读取交易金额
        if cost_usd > MAX_COST_PER_TRADE:
            continue

        clob_mid_price = (best_ask + best_bid) / 2 if best_bid else None

        enriched.append({
            **cand,
            "best_ask": best_ask,
            "best_ask_size": best_ask_size,
            "best_bid": best_bid,
            "best_bid_size": best_bid_size,
            "cost_usd": cost_usd,
            "clob_mid_price": clob_mid_price,
        })

    print(f"[SCAN] Outcomes with valid orderbook: {len(enriched)}")

    # 第三步：按event分组（city + date），每组内只选一个 outcome（纯概率策略）
    # 同一个城市同一天可能有多个temperature ranges，只选 mid_price 最高的
    event_groups = {}  # (city, date) -> list of outcomes

    for outcome in enriched:
        key = (outcome['city'], outcome['date'])
        event_groups.setdefault(key, []).append(outcome)

    # 每组选 mid_price 最高的（纯概率，不考虑流动性）
    selected = []
    for key, outcomes in event_groups.items():
        best = max(outcomes, key=lambda x: x.get('clob_mid_price') or 0.0)
        selected.append(best)

    print(f"[SCAN] Selected best outcome per event: {len(selected)}")

    # 第四步：应用 ENTRY_THRESHOLD（基于 best_ask）
    tradeable = []
    for outcome in selected:
        if outcome['best_ask'] >= ENTRY_THRESHOLD:
            tradeable.append(outcome)

    print(f"[SCAN] Tradeable events (best_ask >= {ENTRY_THRESHOLD}): {len(tradeable)}")
    return tradeable, selected, enriched  # 同时返回enriched（全量有效订单簿）供Fallback使用

class PolymarketAuth:
    """Polymarket CLOB 两级认证管理（手动凭证管理）"""

    def __init__(self, private_key: str, proxy_wallet: str = None, signer_type: int = 0):
        """
        初始化认证管理器

        Args:
            private_key: EOA 钱包私钥（0x开头）
            proxy_wallet: 代理钱包地址（用于 POLY_PROXY 或 GNOSIS_SAFE）
            signer_type: 签名类型: 0=EOA, 1=POLY_PROXY, 2=GNOSIS_SAFE
        """
        from eth_account import Account
        self.private_key = private_key
        self.account = Account.from_key(private_key)
        self.wallet_address = self.account.address
        self.proxy_wallet = proxy_wallet or self.wallet_address
        self.signer_type = signer_type

        # L2 凭证（运行时加载）
        self.api_key = None
        self.api_secret = None
        self.api_passphrase = None

    def derive_l2_credentials(self, base_url: str = "https://clob.polymarket.com", chain_id: int = 137) -> dict:
        """
        使用 L1 (EIP-712) 派生 L2 API 凭证，打印到控制台供手动写入 .env

        Returns:
            凭证字典
        """
        print(f"[AUTH] Deriving L2 API credentials for {self.wallet_address}...")

        try:
            from py_clob_client.client import ClobClient

            # 创建临时客户端（去掉私钥的 0x 前缀）
            pk = self.private_key
            if pk.startswith("0x"):
                pk = pk[2:]

            temp_client = ClobClient(
                host=base_url,
                chain_id=chain_id,
                key=pk,
                signature_type=self.signer_type,
                funder=self.proxy_wallet,
            )

            # 派生 API 凭证（直接使用返回值）
            api_creds = temp_client.create_or_derive_api_creds()
            temp_client.set_api_creds(api_creds)

            self.api_key = api_creds.api_key
            self.api_secret = api_creds.api_secret
            self.api_passphrase = api_creds.api_passphrase

            print()
            print("=" * 64)
            print("  [OK] Credentials derived successfully. Add the following to your .env file")
            print("=" * 64)
            print(f"POLY_API_KEY={self.api_key}")
            print(f"POLY_API_SECRET={self.api_secret}")
            print(f"POLY_API_PASSPHRASE={self.api_passphrase}")
            print("=" * 64)
            print()

            return {
                "api_key": self.api_key,
                "api_secret": self.api_secret,
                "api_passphrase": self.api_passphrase,
            }

        except Exception as e:
            print(f"[ERROR] Failed to derive L2 credentials: {e}")
            raise



async def execute_buy_order(token_id: str, price: float, max_price: float, dry_run: bool = True,
                           retries: int = MAX_RETRIES, no_token_id: str = None,
                           auth_manager: PolymarketAuth = None, user_id: str = None) -> Optional[dict]:
    """
    买入1 share YES，使用正确的两级认证

    Args:
        token_id: YES token ID
        price: 预期买入价（best_ask）
        max_price: 最高可接受价格（考虑滑点）
        dry_run: 模拟模式
        retries: 最大重试次数
        no_token_id: NO outcome token ID（必需）
        auth_manager: 认证管理器（包含 L2 凭证）
        user_id: 钱包地址（用于SkillPay计费，仅live模式需要）

    Returns:
        交易结果字典或 None
    """
    if dry_run:
        if price > max_price:
            print(f"  [DRY] Would SKIP: price ${price:.4f} exceeds max ${max_price:.4f} (slippage)")
            return None
        print(f"  [DRY] Would buy 1 share @ ${price:.4f} (max: ${max_price:.4f})")
        return {"dry_run": True, "token_id": token_id, "price": price, "max_price": max_price}

    # 依赖检查
    if not _HAS_PY_CLOB_CLIENT:
        print("[ERROR] py-clob-client is required for live trading")
        print("[ERROR] Install: pip install py-clob-client")
        return None

    # 实盘检查
    if price > max_price:
        print(f"  [ERROR] Price ${price:.4f} exceeds max allowed ${max_price:.4f} (slippage)")
        return None

    if not no_token_id:
        print(f"  [ERROR] no_token_id required for live trading")
        return None

    if not auth_manager or not auth_manager.api_key:
        print(f"  [ERROR] auth_manager required with derived L2 credentials")
        return None

    try:
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType
        from py_clob_client.order_builder.constants import BUY
        import time

        # 构建 L2 凭证对象
        creds = ApiCreds(
            api_key=auth_manager.api_key,
            api_secret=auth_manager.api_secret,
            api_passphrase=auth_manager.api_passphrase,
        )

        # 初始化 ClobClient（去掉私钥的 0x 前缀）
        raw_key = auth_manager.private_key
        if raw_key.startswith("0x"):
            raw_key = raw_key[2:]

        client = ClobClient(
            host="https://clob.polymarket.com",
            key=raw_key,  # 纯 hex 无 0x
            chain_id=137,
            signature_type=auth_manager.signer_type,
            funder=auth_manager.proxy_wallet,
            creds=creds,
        )

        # 限价单：按 best_ask 价格，size = TRADE_AMOUNT_USD / price
        size = float(
            Decimal(str(TRADE_AMOUNT_USD / price)).quantize(
                Decimal("0.01"), rounding=ROUND_UP
            )
        )
        order_args = OrderArgs(
            token_id=token_id,
            price=round(price, 4),
            size=size,
            side=BUY,
        )

        print(f"  [LIVE] Wallet: {auth_manager.wallet_address}")
        print(f"  [LIVE] Placing order: token={token_id[:16]}... price={price:.4f} size={size} cost≈${round(price*size,4)}")

        for attempt in range(retries):
            try:
                signed_order = client.create_order(order_args)            # 签名
                result = client.post_order(signed_order, OrderType.GTC)   # GTC 提交

                order_id = result.get("orderID") or result.get("order_id", "N/A")
                print(f"  [LIVE] Order submitted! ID: {order_id}")

                # SkillPay 计费：订单提交成功后扣费 0.01 USDT
                if not dry_run and user_id:
                    try:
                        bill = billing_charge(user_id)
                        if bill.get('ok'):
                            print(f"  [OK] Billing success - Balance: {bill['balance']:.4f} USDT")
                        else:
                            balance = bill.get('balance', 0)
                            payment_url = bill.get('payment_url') or billing_get_payment_link(user_id, 8)
                            # Order is on-chain. Cannot exit due to billing failure, only log warning
                            print(f"\n[WARNING] Billing failed (balance: {balance:.4f} USDT)")
                            print(f"   Order {order_id} was submitted successfully but NOT billed.")
                            if payment_url:
                                print(f"   Please top up: {payment_url}\n")
                    except Exception as e:
                        # 计费异常不应影响订单成功
                        print(f"[WARN] Billing error (ignored): {e}")

                return {
                    "type": "BUY",
                    "token_id": token_id,
                    "question": "",
                    "price": price,
                    "shares": size,
                    "cost_usd": round(price * size, 4),
                    "order_id": order_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "success": True,
                }

            except Exception as e:
                import traceback
                traceback.print_exc()
                error_msg = str(e)
                if "insufficient" in error_msg.lower() or "balance" in error_msg.lower():
                    print(f"  [ERROR] Insufficient balance")
                    return None
                elif "429" in error_msg or "rate limit" in error_msg.lower():
                    print(f"  [ERROR] Rate limit hit")
                else:
                    print(f"  [ERROR] Order failed (attempt {attempt+1}): {e}")

                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    print(f"  [RETRY] Waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    return None

    except Exception as e:
        print(f"  [ERROR] Live trading setup failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# =============================================================================
# REPORTING
# =============================================================================

def print_positions(state: dict):
    """Print current positions"""
    positions = state.get("positions", {})
    if not positions:
        print("\n[INFO] No positions")
        return

    print(f"\n{'='*80}")
    print(f"{'POSITIONS':^80}")
    print(f"{'='*80}")

    total_cost = 0
    total_unrealized = 0

    for pos_key, pos in positions.items():
        # pos_key 是 city_date (e.g., "nyc_2026-03-22")
        question = pos.get("question", "N/A")[:60]
        entry = pos.get("entry_price", 0)
        shares = pos.get("shares", 0)
        cost = pos.get("cost_usd", 0)
        best_ask = pos.get("best_ask", entry)
        best_bid = pos.get("best_bid", entry)

        # 用 mid price 作为当前价格估算（更真实）
        current_price = (best_ask + best_bid) / 2 if best_bid else best_ask
        unrealized = (current_price - entry) * shares

        total_cost += cost
        total_unrealized += unrealized

        print(f"\n[MARKET] {question}...")
        print(f"    Cost: ${cost:.4f} | Shares: {shares} | Entry: ${entry:.4f}")
        bid_str = f"${best_bid:.4f}" if best_bid is not None else "N/A"
        print(f"    Bid: {bid_str} | Ask: ${best_ask:.4f} | Mid: ${current_price:.4f}")
        print(f"    Unrealized P&L: {'+' if unrealized >=0 else ''}${unrealized:.4f}")

    print(f"\nTotal cost: ${total_cost:.4f}")
    print(f"Total unrealized: {'+' if total_unrealized >=0 else ''}${total_unrealized:.4f}")
    print(f"{'='*80}")

    # 更新 stats（PnL 追踪）
    state["stats"]["total_pnl"] = total_unrealized
    wins = 0
    losses = 0
    for pos in positions.values():
        entry = pos.get('entry_price', 0)
        shares = pos.get('shares', 0)
        best_ask = pos.get('best_ask')
        best_bid = pos.get('best_bid')
        # 计算当前价格（优先用 mid，或 best_bid/ask）
        if best_bid is not None and best_ask is not None:
            current = (best_ask + best_bid) / 2
        elif best_bid is not None:
            current = best_bid
        elif best_ask is not None:
            current = best_ask
        else:
            continue
        pnl = (current - entry) * shares
        if pnl > 0:
            wins += 1
        elif pnl < 0:
            losses += 1
    state["stats"]["wins"] = wins
    state["stats"]["losses"] = losses

def print_trades(trades: List[dict]):
    """Print recent trades"""
    if not trades:
        print("\n[INFO] No trades")
        return

    print(f"\n{'='*80}")
    print(f"{'RECENT TRADES':^80}")
    print(f"{'='*80}")

    for trade in trades[-10:][::-1]:  # Last 10 trades
        ts = trade.get("timestamp", "")[:19]
        type_ = trade.get("type", "?")
        question = trade.get("question", "N/A")[:50]
        price = trade.get("price", 0)
        cost = trade.get("cost_usd", 0)

        print(f"\n[TIME] {ts}")
        print(f"    Type: {type_.upper()}")
        print(f"    Market: {question}...")
        print(f"    Price: ${price:.4f} | Cost: ${cost:.4f}")

    print(f"{'='*80}")

def print_pnl(state: dict):
    """Print P&L statistics"""
    stats = state.get("stats", {})
    total_trades = stats.get("total_trades", 0)
    wins = stats.get("wins", 0)
    losses = stats.get("losses", 0)
    total_pnl = stats.get("total_pnl", 0.0)

    print(f"\n{'='*80}")
    print(f"{'STATS REPORT':^80}")
    print(f"{'='*80}")
    print(f"Total trades: {total_trades}")
    if total_trades > 0:
        print(f"Win rate: {wins}/{total_trades} ({wins/total_trades*100:.1f}%)")
    print(f"Total P&L: {'+' if total_pnl >= 0 else ''}${total_pnl:.4f}")
    balance = state.get("balance", 0)
    print(f"Virtual balance: ${balance:.2f}")
    print(f"{'='*80}")

def print_full_report(state: dict, tradeable: List[dict]):
    """Print full report every 4 minutes (don't clear screen, keep scan logs)"""

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'#'*80}")
    print(f"# Weather Sniper v1.0.0 - Status Report")
    print(f"# Time: {now}")
    print(f"{'#'*80}\n")

    print_positions(state)
    print_trades(state.get("trades", []))
    print_pnl(state)

    # Scan summary
    print(f"\n{'='*80}")
    print(f"{'SCAN SUMMARY':^80}")
    print(f"{'='*80}")
    print(f"Tradeable markets: {len(tradeable)}")
    print(f"Monitoring cities: {len(CITY_SLUGS)}")
    print(f"Date range: Today + tomorrow")
    print(f"Trade amount: ${TRADE_AMOUNT_USD} (max allowed: ${MAX_COST_PER_TRADE})")
    print(f"Fallback threshold: {ENTRY_THRESHOLD} (enforced via scan)")
    print(f"{'='*80}\n")

# =============================================================================
# MAIN LOOP
# =============================================================================

class SniperBot:
    def __init__(self, dry_run: bool = True, once: bool = False, auth_manager: PolymarketAuth = None):
        self.dry_run = dry_run
        self.once = once
        self.running = True
        self.state = load_state()
        self.last_report = datetime.now(timezone.utc)  # 启动时不欠报告
        self.last_scan = datetime.now(timezone.utc) - timedelta(seconds=600)
        self.auth_manager = auth_manager  # 认证管理器

        # 城市今日日期（本地时间）- 会在 scan 开始时动态更新
        self.today_dates = {}
        for city in CITY_SLUGS:
            tz_name = TIMEZONES.get(city, "UTC")
            local_tz = tz(tz_name)
            now_local = datetime.now(timezone.utc).astimezone(local_tz)
            self.today_dates[city] = now_local.date()

        # 缓存最近一次scan的tradeable列表（用于报告）
        self.last_tradeable = []

        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        print("\n\n[INFO] Received stop signal, exiting...")
        self.running = False

    async def run(self):
        """主循环"""
        print("\n" + "="*60)
        print("[START] Weather High-Temp Sniper v1.0.0")
        print("="*60)
        print(f"Mode: {'DRY RUN (simulation)' if self.dry_run else 'LIVE (real trading)'}")
        print(f"Monitoring cities: {len(CITY_SLUGS)}")
        print(f"Date range: 2 days (today + tomorrow)")
        end_h = int(MONITOR_END_HOUR)
        end_m = int((MONITOR_END_HOUR - end_h) * 60)
        print(f"Monitor window: Local {MONITOR_START_HOUR}:00-{end_h}:{end_m:02d}")
        print(f"Scan interval: {CHECK_INTERVAL//60} minutes")
        print(f"Report interval: {REPORT_INTERVAL//60} minutes")
        print("="*60 + "\n")

        # 实盘或 once 模式：确保 L2 凭证已加载（未加载则派生）
        # --once 用于快速获取凭证，不需要 --live
        if (self.once or not self.dry_run) and self.auth_manager:
            if not self.auth_manager.api_key:
                try:
                    await self.auth_manager.derive_l2_credentials()
                    # After deriving credentials successfully, exit and have user fill .env
                    print("[INFO] Fill .env with the credentials above and rerun.")
                    return
                except Exception as e:
                    print(f"[ERROR] Failed to initialize auth: {e}")
                    print("[ERROR] Please check your PRIVATE_KEY and PROXY_WALLET.")
                    return
            else:
                print("[AUTH] Credentials already loaded from .env")

        async with ApiClient() as api_client:
            while self.running:
                now = datetime.now(timezone.utc)

                # --once mode: enter loop, execute one scan immediately then exit
                if self.once:
                    await self.scan_cycle(api_client)
                    await self.print_report_cycle(api_client)
                    save_state(self.state)
                    print("\n[OK] Single run complete (--once mode)")
                    break

                # 时间点触发：每5分钟的00-02秒（9:00, 9:05, 9:10...）
                minute = now.minute
                second = now.second
                is_scan_time = (minute % 5 == 0 and second < 2)

                if is_scan_time and (now - self.last_scan).total_seconds() > 10:
                    # Update today_dates dynamically (handle day rollover)
                    for city in CITY_SLUGS:
                        tz_name = TIMEZONES.get(city, "UTC")
                        local_tz = tz(tz_name)
                        now_local = now.astimezone(local_tz)
                        self.today_dates[city] = now_local.date()

                    await self.scan_cycle(api_client)
                    self.last_scan = now

                # 报告间隔：每4分钟（在 REPORT_INTERVAL 基础上）
                if (now - self.last_report).total_seconds() >= REPORT_INTERVAL:
                    await self.print_report_cycle(api_client)
                    self.last_report = now

                await asyncio.sleep(0.5)  #  finer sleep to catch exact time

        # 退出前保存状态
        save_state(self.state)
        print("\n[OK] State saved, exiting.")

    async def scan_cycle(self, api_client: ApiClient):
        """Scan cycle: find tradable markets"""
        print(f"\n[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Starting scan...")

        # Dynamically recalc date_range (only scan today & tomorrow to reduce API calls)
        self.date_range = [
            datetime.now(timezone.utc) + timedelta(days=i) for i in range(2)
        ]

        # 清理 fallback_executed：只保留今日城市日期（跨天自动重置）
        fallback_executed = set(self.state.get("fallback_executed", []))
        current_city_dates = set()
        for city, date_obj in self.today_dates.items():
            current_city_dates.add(f"{city}_{date_obj.strftime('%Y-%m-%d')}")
        fallback_executed = {fe for fe in fallback_executed if fe in current_city_dates}
        self.state["fallback_executed"] = list(fallback_executed)
        # 保存到实例变量方便后续使用
        self.fallback_executed = fallback_executed

        # [Balance pre-check] Before scanning and ordering, check SkillPay balance is sufficient
        if not self.dry_run and SKILLPAY_USER_ID:
            try:
                balance = billing_get_balance(SKILLPAY_USER_ID)
                # Need at least one charge amount remaining
                if balance < MIN_CHARGE_AMOUNT:
                    print(f"\n[ERROR] SkillPay insufficient balance ({balance:.4f} USDT), skipping this scan")
                    payment_url = billing_get_payment_link(SKILLPAY_USER_ID, 8)
                    print(f"   Top up to continue: {payment_url}\n")
                    return  # Return early, no scan, no order
                # else: balance sufficient, continue
            except Exception as e:
                print(f"[WARN] Balance check failed (network error): {e}, continuing...")

        # 1. Find all tradable candidates
        tradeable, all_selected, all_enriched = await scan_and_find_trades(api_client, self.date_range)

        # 2. Check which are in monitor window
        window_candidates = []
        for cand in tradeable:
            if is_in_monitor_window(cand['city'], cand['date']):
                window_candidates.append(cand)

        print(f"[SCAN] Tradeable in monitor window: {len(window_candidates)}")

        # 3. Check for existing positions
        positions = self.state.get("positions", {})
        new_positions = 0

        for cand in window_candidates:
            # Check if already have position for this city_date (each city can only have one position per day)
            pos_key = f"{cand['city']}_{cand['date']}"
            if pos_key in positions:
                continue

            # 【每次下单前实时检查余额】防止多城市触发时中途耗尽
            if not self.dry_run and SKILLPAY_USER_ID:
                try:
                    balance = billing_get_balance(SKILLPAY_USER_ID)
                    if balance < MIN_CHARGE_AMOUNT:
                        print(f"\n[ERROR] Insufficient balance ({balance:.4f} < {MIN_CHARGE_AMOUNT} USDT), stopping remaining orders in this round\n")
                        break  # 退出循环，不再继续
                except Exception as e:
                    print(f"[WARN] Balance check failed ({e}), continuing...")

            # [OK] Execute buy (with slippage control)
            max_price = cand['best_ask'] * (1 + SLIPPAGE_TOLERANCE)
            # For dry-run we allow the price check but continue anyway
            # In live mode, the order might fail if price exceeds tolerance

            print(f"[BUY] Triggered: {cand['question'][:60]}...")
            print(f"    City: {cand['city']} Date: {cand['date']}")
            print(f"    Best Ask: ${cand['best_ask']:.4f} Max Allowed: ${max_price:.4f} Cost: ${cand['cost_usd']:.4f}")

            # 准备 user_id（用于 SkillPay 计费）
            # 使用用户配置的 SKILLPAY_USER_ID（必需），不是 PROXY_WALLET
            user_id = SKILLPAY_USER_ID

            order_result = await execute_buy_order(
                token_id=cand['token_id'],
                price=cand['best_ask'],
                max_price=max_price,
                dry_run=self.dry_run,
                retries=MAX_RETRIES,
                no_token_id=cand['no_token_id'],
                auth_manager=self.auth_manager,
                user_id=user_id if not self.dry_run else None  # dry-run 不传
            )

            if order_result:
                # 使用 city_date 作为 position key（确保每个城市每天一个仓位）
                pos_key = f"{cand['city']}_{cand['date']}"
                pos = {
                    "market_id": cand['market_id'],
                    "token_id": cand['token_id'],
                    "yes_token_id": cand['yes_token_id'],
                    "no_token_id": cand['no_token_id'],
                    "city": cand['city'],
                    "date": cand['date'],
                    "question": cand['question'],
                    "range": cand['range'],
                    "entry_price": cand['best_ask'],
                    "shares": float(Decimal(str(TRADE_AMOUNT_USD / cand['best_ask'])).quantize(Decimal("0.01"), rounding=ROUND_UP)),
                    "cost_usd": TRADE_AMOUNT_USD,
                    "gamma_price": cand.get('gamma_price'),  # 安全访问
                    "best_bid": cand['best_bid'],
                    "best_ask": cand['best_ask'],
                    "clob_mid_price": cand['clob_mid_price'],
                    "opened_at": datetime.now(timezone.utc).isoformat(),
                    "fallback": False,
                }
                positions[pos_key] = pos
                self.state["positions"] = positions

                # 合并基础信息和订单信息（order_id, signature, voucher_file）
                base_trade = {
                    "type": "BUY",
                    "market_id": cand['market_id'],
                    "question": cand['question'],
                    "price": cand['best_ask'],
                    "shares": float(Decimal(str(TRADE_AMOUNT_USD / cand['best_ask'])).quantize(Decimal("0.01"), rounding=ROUND_UP)),
                    "cost_usd": TRADE_AMOUNT_USD,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "dry_run": self.dry_run,
                    "fallback": False,
                }
                trade = {**base_trade, **order_result}
                self.state["trades"].append(trade)
                self.state["stats"]["total_trades"] += 1

                new_positions += 1
                print(f"  [OK] Buy success ({'simulation' if self.dry_run else 'real'})")

                # 立即持久化state，防止崩溃丢失持仓
                save_state(self.state)
            else:
                print(f"  [ERROR] Buy failed")

        print(f"[SCAN] New positions created: {new_positions}")

        # 4. Fallback check (strict 10:00-10:04 window per city)
        # 使用 self.fallback_executed (已在上面清理)
        fallback_executed = self.fallback_executed if hasattr(self, 'fallback_executed') else set(self.state.get("fallback_executed", []))

        # 检查是否有任何城市处于fallback窗口
        for city in CITY_SLUGS:
            if not is_fallback_time(city, self.today_dates[city].strftime("%Y-%m-%d")):
                continue

            today_str = self.today_dates[city].strftime("%Y-%m-%d")
            city_date_key = f"{city}_{today_str}"

            # Check if today's city already has position or fallback executed
            if city_date_key in positions or city_date_key in fallback_executed:
                print(f"[FALLBACK] Skipping {city} (already has position executed)")
                continue

            # 【每次下单前实时检查余额】防止多城市触发时中途耗尽
            if not self.dry_run and SKILLPAY_USER_ID:
                try:
                    balance = billing_get_balance(SKILLPAY_USER_ID)
                    if balance < MIN_CHARGE_AMOUNT:
                        print(f"\n[ERROR] Insufficient balance ({balance:.4f} < {MIN_CHARGE_AMOUNT} USDT), stopping fallback remaining orders\n")
                        break  # 退出fallback循环
                except Exception as e:
                    print(f"[WARN] Balance check failed ({e}), continuing...")

            # Fallback 使用 all_enriched（全量有效订单簿），按概率（mid_price）选最高
            city_candidates = [c for c in all_enriched if c['city'] == city and c['date'] == today_str]
            if not city_candidates:
                print(f"[FALLBACK] No candidates for {city} {today_str}")
                continue

            # 按 clob_mid_price 排序（最高的最可能发生），None 时回退到 gamma_price
            best = max(city_candidates, key=lambda c: c.get('clob_mid_price') or c.get('gamma_price') or 0)

            print(f"\n[FALLBACK] Triggered for {city} {today_str}")
            print(f"    Candidate: {best['question'][:60]}... (mid=${best.get('clob_mid_price', 0):.4f}, gamma={best.get('gamma_price', 0):.4f})")

            max_price = best['best_ask'] * (1 + SLIPPAGE_TOLERANCE)
            # 准备 user_id（用于 SkillPay 计费）
            # 使用用户配置的 SKILLPAY_USER_ID（必需），不是 PROXY_WALLET
            user_id = SKILLPAY_USER_ID

            order_result = await execute_buy_order(
                token_id=best['token_id'],
                price=best['best_ask'],
                max_price=max_price,
                dry_run=self.dry_run,
                retries=MAX_RETRIES,
                no_token_id=best['no_token_id'],
                auth_manager=self.auth_manager,
                user_id=user_id if not self.dry_run else None  # dry-run 不传
            )

            if order_result:
                # 保存仓位（city_date key）
                pos = {
                    "market_id": best['market_id'],
                    "token_id": best['token_id'],
                    "yes_token_id": best['yes_token_id'],
                    "no_token_id": best['no_token_id'],
                    "city": best['city'],
                    "date": best['date'],
                    "question": best['question'],
                    "range": best['range'],
                    "entry_price": best['best_ask'],
                    "shares": float(Decimal(str(1.0 / best['best_ask'])).quantize(Decimal("0.01"), rounding=ROUND_UP)),
                    "cost_usd": TRADE_AMOUNT_USD,
                    "gamma_price": best.get('gamma_price'),  # 安全访问
                    "best_bid": best['best_bid'],
                    "best_ask": best['best_ask'],
                    "clob_mid_price": best['clob_mid_price'],
                    "opened_at": datetime.now(timezone.utc).isoformat(),
                    "fallback": True,
                    "order_id": order_result.get("order_id"),  # 保存订单ID
                    "voucher_file": order_result.get("voucher_file"),  # 凭证文件路径
                }
                positions[city_date_key] = pos
                self.state["positions"] = positions

                # 合并基础信息和订单信息
                base_trade = {
                    "type": "BUY",
                    "market_id": best['market_id'],
                    "question": best['question'],
                    "price": best['best_ask'],
                    "shares": float(Decimal(str(1.0 / best['best_ask'])).quantize(Decimal("0.01"), rounding=ROUND_UP)),
                    "cost_usd": TRADE_AMOUNT_USD,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "dry_run": self.dry_run,
                    "fallback": True,
                }
                trade = {**base_trade, **order_result}
                self.state["trades"].append(trade)
                self.state["stats"]["total_trades"] += 1

                print(f"  [OK] Fallback buy success")

                # 立即持久化state，防止崩溃丢失持仓
                save_state(self.state)
            else:
                print(f"  [ERROR] Fallback buy failed")

            # 无论成功失败都标记，防止窗口内重试
            fallback_executed.add(city_date_key)
            self.state["fallback_executed"] = list(fallback_executed)

        # 保存 tradeable 供报告使用
        self.last_tradeable = tradeable

    async def print_report_cycle(self, api_client: ApiClient):
        """打印报告周期（实时更新持仓价格）"""
        positions = self.state.get("positions", {})

        if positions:
            print(f"[REPORT] Updating {len(positions)} position prices...")
            for pos_key, pos in positions.items():
                token_id = pos.get("yes_token_id") or pos.get("token_id")
                if not token_id:
                    continue
                try:
                    book = await api_client.fetch_clob_orderbook(token_id)
                    if not book:
                        continue

                    asks = sorted(book.get("asks", []), key=lambda x: float(x['price']))
                    bids = sorted(book.get("bids", []), key=lambda x: float(x['price']))

                    if asks:
                        pos["best_ask"] = float(asks[0]['price'])
                    if bids:
                        pos["best_bid"] = float(bids[-1]['price'])

                except Exception as e:
                    print(f"[WARN] Failed to update price for {pos_key}: {e}")
                    continue

            self.state["positions"] = positions

        print_full_report(self.state, self.last_tradeable)

    def run_sync(self):
        """同步入口"""
        asyncio.run(self.run())

# =============================================================================
# COMMANDS
# =============================================================================

def show_positions():
    """显示当前持仓"""
    state = load_state()
    print_positions(state)
    print_trades(state.get("trades", []))
    print_pnl(state)

def reset_state():
    """Reset state"""
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    print("[OK] State reset")

# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather High-Temp Sniper v1.0.0")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulation mode (no real orders)")
    parser.add_argument("--live", action="store_true",
                        help="Live trading (requires PRIVATE_KEY and PROXY_WALLET configured)")
    parser.add_argument("--once", action="store_true",
                        help="Run one scan cycle then exit (debugging)")
    parser.add_argument("--status", action="store_true",
                        help="Show current positions and stats")

    args = parser.parse_args()

    dry_run = not args.live
    auth_manager = None

    # --once 或 --live 模式都需要 auth_manager（用于派生 L2 凭证）
    if args.live or args.once:
        try:
            auth_manager = asyncio.run(init_auth_manager())
        except Exception as e:
            print(f"[ERROR] Failed to initialize: {e}")
            if not args.live:
                print("[INFO] This is needed to derive L2 API credentials.")
            sys.exit(1)

    if args.status:
        show_positions()
    elif args.once or args.dry_run or args.live:
        bot = SniperBot(dry_run=dry_run, once=args.once, auth_manager=auth_manager)
        bot.run_sync()
    else:
        parser.print_help()
