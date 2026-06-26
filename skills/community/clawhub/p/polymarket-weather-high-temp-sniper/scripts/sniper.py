#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weather High-Temp Sniper v1.0.4
閫氳繃 Simmer API 鐩存帴鍦?Polymarket 澶╂皵甯傚満杩涜鑷姩浜ゆ槗銆?
鍏ㄦ柊鐨勪笁灞傛灦鏋勶細鍙戠幇锛坕mportable锛夆啋 鏌ヨ锛坱ags=weather锛夆啋 浜ゆ槗銆?
"""

import os
import sys
import json
import time
import logging
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

# ============================================================================
# Early .env loading
# ============================================================================
ROOT = Path(__file__).parent.parent.resolve()
env_path = ROOT / ".env"
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path, override=True)
    except ImportError:
        pass

sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

# ============================================================================
# Logging configuration
# ============================================================================
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("sniper")

# ============================================================================
# Simmer SDK + Config Management
# ============================================================================
try:
    from simmer_sdk import SimmerClient
    from simmer_sdk.skill import load_config, update_config
    SKILL_FRAMEWORK = True
except ImportError:
    SKILL_FRAMEWORK = False
    try:
        from simmer_sdk import SimmerClient
    except ImportError:
        print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
        sys.exit(1)

import pytz

# 閰嶇疆 schema
CONFIG_SCHEMA = {
    "entry_price_threshold": {"env": "SIMMER_SNIPER2_ENTRY_PRICE_THRESHOLD", "type": float, "default": 0.35},
    "max_position_usd": {"env": "SIMMER_SNIPER2_MAX_POSITION_USD", "type": float, "default": 2.50},
    "shares_per_order": {"env": "SIMMER_SNIPER2_SHARES", "type": int, "default": 5},
    "slippage_tolerance": {"env": "SIMMER_SNIPER2_SLIPPAGE", "type": float, "default": 0.15},
    "scan_interval_seconds": {"env": "SIMMER_SNIPER2_SCAN_INTERVAL", "type": int, "default": 300},
    "fallback_at_local_10": {"env": "SIMMER_SNIPER2_FALLBACK_10AM", "type": bool, "default": True},
    "max_retry": {"env": "SIMMER_SNIPER2_MAX_RETRY", "type": int, "default": 1},
    "allow_sim_paper": {"env": "SIMMER_SNIPER2_ALLOW_SIM_PAPER", "type": bool, "default": False},
    "enable_tp_sl": {"env": "SIMMER_SNIPER2_ENABLE_TP_SL", "type": bool, "default": False},
    "take_profit_pct": {"env": "SIMMER_SNIPER2_TP", "type": float, "default": 0.50},
    "stop_loss_pct": {"env": "SIMMER_SNIPER2_SL", "type": float, "default": 0.25},
    "report_interval_seconds": {"env": "SIMMER_SNIPER2_REPORT_INTERVAL", "type": int, "default": 240},
    "telegram_enabled": {"env": "SIMMER_SNIPER2_TELEGRAM_ENABLED", "type": bool, "default": False},
    "telegram_chat_id": {"env": "SIMMER_SNIPER2_TELEGRAM_CHAT_ID", "type": str, "default": ""},
    "telegram_bot_token": {"env": "SIMMER_SNIPER2_TELEGRAM_BOT_TOKEN", "type": str, "default": ""},
    # Redeem daemon settings
    "enable_redeem": {"env": "SIMMER_SNIPER2_ENABLE_REDEEM", "type": bool, "default": True},
    "redeem_interval_seconds": {"env": "SIMMER_SNIPER2_REDEEM_INTERVAL", "type": int, "default": 3600},
    # Redeem daemon settings
}

_LEGACY_ENV_ALIASES = {
    "PRICE_THRESHOLD": "SIMMER_SNIPER2_ENTRY_PRICE_THRESHOLD",
    "MAX_USD": "SIMMER_SNIPER2_MAX_POSITION_USD",
    "MAX_SHARES": "SIMMER_SNIPER2_SHARES",
    "SLIPPAGE": "SIMMER_SNIPER2_SLIPPAGE",
    "SCAN_INTERVAL": "SIMMER_SNIPER2_SCAN_INTERVAL",
    "ENABLE_TP_SL": "SIMMER_SNIPER2_ENABLE_TP_SL",
    "TAKE_PROFIT": "SIMMER_SNIPER2_TP",
    "STOP_LOSS": "SIMMER_SNIPER2_SL",
    "REPORT_INTERVAL": "SIMMER_SNIPER2_REPORT_INTERVAL",
    "TELEGRAM_ENABLED": "SIMMER_SNIPER2_TELEGRAM_ENABLED",
    "TELEGRAM_CHAT_ID": "SIMMER_SNIPER2_TELEGRAM_CHAT_ID",
}
for _old, _new in _LEGACY_ENV_ALIASES.items():
    if _old in os.environ and _new not in os.environ:
        os.environ[_new] = os.environ[_old]

if SKILL_FRAMEWORK:
    _config = load_config(CONFIG_SCHEMA, __file__, slug="polymarket-weather-high-temp-sniper")
    def get_cfg(key: str):
        return _config[key]
else:
    def get_cfg(key: str):
        env_name = CONFIG_SCHEMA[key]["env"]
        val = os.environ.get(env_name)
        if val is None:
            return CONFIG_SCHEMA[key]["default"]
        typ = CONFIG_SCHEMA[key]["type"]
        if typ is bool:
            return val.lower() in ("true", "1", "yes")
        elif typ is int:
            return int(val)
        elif typ is float:
            return float(val)
        return val

# 鍏ㄥ眬閰嶇疆
ENTRY_THRESHOLD = get_cfg("entry_price_threshold")
MAX_POSITION_USD = get_cfg("max_position_usd")
SHARES_PER_ORDER = get_cfg("shares_per_order")
SLIPPAGE = get_cfg("slippage_tolerance")
SCAN_INTERVAL = get_cfg("scan_interval_seconds")
FALLBACK_AT_10 = get_cfg("fallback_at_local_10")
MAX_RETRY = get_cfg("max_retry")
ALLOW_SIM_PAPER = get_cfg("allow_sim_paper")
ENABLE_TP_SL = get_cfg("enable_tp_sl")
TP_PCT = get_cfg("take_profit_pct")
SL_PCT = get_cfg("stop_loss_pct")
REPORT_INTERVAL = get_cfg("report_interval_seconds")
TELEGRAM_ENABLED = get_cfg("telegram_enabled")
TELEGRAM_CHAT_ID = get_cfg("telegram_chat_id")

# ================================================
# Market Cache Configuration
# ================================================
# Free tier: ~10 get_markets() calls per day.
# To ensure fresh data for time window catches, refresh hourly.
MARKET_CACHE_TTL = 3600  # seconds (1 hour)
# SCAN_INTERVAL is configured via get_cfg above

# ============================================================================
# Client management
# ============================================================================
_client = None
_market_cache = []          # list of market objects
_market_cache_ts = 0       # last refresh timestamp

def get_client(live: bool = False):
    global _client
    if _client is not None:
        return _client
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        log.error("SIMMER_API_KEY not set.")
        sys.exit(1)

    # Check for external wallet mode
    wallet_key = os.environ.get("WALLET_PRIVATE_KEY")
    if wallet_key:
        kwargs = {"api_key": api_key, "venue": "polymarket", "live": live, "private_key": wallet_key}
    else:
        kwargs = {"api_key": api_key, "venue": "polymarket", "live": live}
        log.info("Using managed wallet mode (server-side signing). Set WALLET_PRIVATE_KEY for external wallet.")

    _client = SimmerClient(**kwargs)

    # If external wallet, perform one-time link and approvals
    if wallet_key and live:
        try:
            log.info("External wallet mode: checking wallet link...")
            # link_wallet() will register the wallet with Simmer if not already linked
            _link_wallet_if_needed(_client)
            # Set approvals for USDC.e and POL (optional but recommended)
            # _set_approvals_if_needed(_client)  # TODO: implement when needed
        except Exception as e:
            log.warning(f"Wallet setup failed: {e}")

    return _client

def _link_wallet_if_needed(client):
    """Link external wallet to Simmer if not already linked."""
    try:
        # Check current wallet status via agent info
        agent_info = client._request("GET", "/api/sdk/agents/me")
        if agent_info.get("polymarket", {}).get("wallet_linked"):
            log.info("Wallet already linked.")
            return
        # Perform link
        link_result = client.link_wallet()
        log.info(f"Wallet linked: {link_result}")
    except Exception as e:
        log.error(f"Failed to link wallet: {e}")
        raise

# ============================================================================
# City -> Timezone mapping
# ============================================================================
CITY_TZ_MAP = {
    # 鈹€鈹€ 鍖楃編 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
    "new york": "America/New_York", "nyc": "America/New_York",
    "new york city": "America/New_York", "laguardia": "America/New_York",
    "la guardia": "America/New_York", "boston": "America/New_York",
    "miami": "America/New_York", "atlanta": "America/New_York",
    "washington": "America/New_York", "philadelphia": "America/New_York",
    "chicago": "America/Chicago", "houston": "America/Chicago",
    "dallas": "America/Chicago", "austin": "America/Chicago",
    "minneapolis": "America/Chicago", "o'hare": "America/Chicago",
    "ohare": "America/Chicago", "dfw": "America/Chicago",
    "denver": "America/Denver", "salt lake city": "America/Denver",
    "phoenix": "America/Phoenix", "las vegas": "America/Los_Angeles",
    "los angeles": "America/Los_Angeles", "san francisco": "America/Los_Angeles",
    "seattle": "America/Los_Angeles", "sea-tac": "America/Los_Angeles",
    "portland": "America/Los_Angeles", "toronto": "America/Toronto",
    "vancouver": "America/Vancouver", "montreal": "America/Toronto",
    "calgary": "America/Edmonton",
    # 鍖楃編琛ュ厖鍩庡競
    "los angeles international": "America/Los_Angeles", "lax": "America/Los_Angeles",
    "san diego": "America/Los_Angeles", "sacramento": "America/Los_Angeles",
    "san jose": "America/Los_Angeles", "denver international": "America/Denver",
    "dallas fort worth": "America/Chicago", "orlando": "America/New_York",
    "tampa": "America/New_York", "detroit": "America/Detroit",
    "cleveland": "America/New_York", "pittsburgh": "America/New_York",
    "st. louis": "America/Chicago", "st louis": "America/Chicago",
    "nashville": "America/Chicago", "memphis": "America/Chicago",
    "new orleans": "America/Chicago", "houston hobby": "America/Chicago",
    "baltimore": "America/New_York", "chicago midway": "America/Chicago",
    "salt lake city international": "America/Denver",

    # 鈹€鈹€ 娆ф床 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
    "london": "Europe/London", "paris": "Europe/Paris", "berlin": "Europe/Berlin",
    "madrid": "Europe/Madrid", "rome": "Europe/Rome",
    "amsterdam": "Europe/Amsterdam", "brussels": "Europe/Brussels",
    "vienna": "Europe/Vienna", "stockholm": "Europe/Stockholm",
    "oslo": "Europe/Oslo", "copenhagen": "Europe/Copenhagen",
    "helsinki": "Europe/Helsinki", "warsaw": "Europe/Warsaw",
    "prague": "Europe/Prague", "budapest": "Europe/Budapest",
    "athens": "Europe/Athens", "istanbul": "Europe/Istanbul",
    "ankara": "Europe/Istanbul", "moscow": "Europe/Moscow",
    # 娆ф床琛ュ厖鍩庡競
    "zurich": "Europe/Zurich", "geneva": "Europe/Zurich",
    "frankfurt": "Europe/Berlin", "munich": "Europe/Berlin",
    "cologne": "Europe/Berlin", "dusseldorf": "Europe/Berlin",
    "hamburg": "Europe/Berlin", "stuttgart": "Europe/Berlin",
    "lyon": "Europe/Paris", "marseille": "Europe/Paris",
    "barcelona": "Europe/Madrid", "valencia": "Europe/Madrid",
    "seville": "Europe/Madrid", "lisbon": "Europe/Lisbon",
    "porto": "Europe/Lisbon", "dublin": "Europe/Dublin",
    "manchester": "Europe/London", "birmingham": "Europe/London",
    "edinburgh": "Europe/London", "glasgow": "Europe/London",
    "leeds": "Europe/London", "bristol": "Europe/London",
    "belfast": "Europe/London", "stockholm arlanda": "Europe/Stockholm",
    "gothenburg": "Europe/Stockholm", "malmo": "Europe/Stockholm",
    "copenhagen airport": "Europe/Copenhagen", "aarhus": "Europe/Copenhagen",
    "odense": "Europe/Copenhagen", "bratislava": "Europe/Bratislava",
    "lithuania": "Europe/Vilnius", "riga": "Europe/Riga",
    "tallinn": "Europe/Tallinn", "sofia": "Europe/Sofia",
    "bucharest": "Europe/Bucharest", "belgrade": "Europe/Belgrade",
    "zagreb": "Europe/Zagreb", "ljubljana": "Europe/Ljubljana",
    "sarajevo": "Europe/Sarajevo", "skopje": "Europe/Skopje",
    "tirana": "Europe/Tirana", "podgorica": "Europe/Podgorica",

    # 鈹€鈹€ 浜氭床 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
    "tokyo": "Asia/Tokyo", "seoul": "Asia/Seoul",
    "beijing": "Asia/Shanghai", "shanghai": "Asia/Shanghai",
    "hong kong": "Asia/Hong_Kong", "taipei": "Asia/Taipei",
    "singapore": "Asia/Singapore", "bangkok": "Asia/Bangkok",
    "jakarta": "Asia/Jakarta", "kuala lumpur": "Asia/Kuala_Lumpur",
    "manila": "Asia/Manila", "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata", "bangalore": "Asia/Kolkata",
    # 浜氭床琛ュ厖鍩庡競
    "guangzhou": "Asia/Shanghai", "shenzhen": "Asia/Shanghai",
    "chengdu": "Asia/Shanghai", "wuhan": "Asia/Shanghai",
    "xian": "Asia/Shanghai", "hangzhou": "Asia/Shanghai",
    "nanjing": "Asia/Shanghai", "tianjin": "Asia/Shanghai",
    "chongqing": "Asia/Shanghai", "shenyang": "Asia/Shanghai",
    "qingdao": "Asia/Shanghai", "dalian": "Asia/Shanghai",
    "xiamen": "Asia/Shanghai", "fuzhou": "Asia/Shanghai",
    "hongqiao": "Asia/Shanghai", "pudong": "Asia/Shanghai",
    "osaka": "Asia/Tokyo", "kyoto": "Asia/Tokyo",
    "yokohama": "Asia/Tokyo", "nagoya": "Asia/Tokyo",
    "sapporo": "Asia/Tokyo", "fukuoka": "Asia/Tokyo",
    "seoul gimpo": "Asia/Seoul", "seoul incheon": "Asia/Seoul",
    "busan": "Asia/Seoul", "incheon": "Asia/Seoul",
    "ho chi minh": "Asia/Ho_Chi_Minh", "hanoi": "Asia/Ho_Chi_Minh",
    "phnom penh": "Asia/Phnom_Penh", "vientiane": "Asia/Vientiane",
    "yangon": "Asia/Rangoon", "naypyidaw": "Asia/Rangoon",
    "kuala lumpur international": "Asia/Kuala_Lumpur", "penang": "Asia/Kuala_Lumpur",
    "johor bahru": "Asia/Kuala_Lumpur", "bangkok don mueang": "Asia/Bangkok",
    "bangkok suvarnabhumi": "Asia/Bangkok", "phuket": "Asia/Bangkok",
    "chiang mai": "Asia/Bangkok", "pattaya": "Asia/Bangkok",
    "batam": "Asia/Jakarta", "surabaya": "Asia/Jakarta",
    "bandung": "Asia/Jakarta", "medan": "Asia/Jakarta",
    "makassar": "Asia/Jakarta", "denpasar": "Asia/Jakarta",
    "chennai": "Asia/Kolkata", "kolkata": "Asia/Kolkata",
    "hyderabad": "Asia/Kolkata", "pune": "Asia/Kolkata",
    "ahmedabad": "Asia/Kolkata", "jaipur": "Asia/Kolkata",
    "kashmir": "Asia/Kolkata", "goa": "Asia/Kolkata",
    "colombo": "Asia/Colombo", "male": "Asia/Mal茅",
    "kathmandu": "Asia/Kathmandu", "dhaka": "Asia/Dhaka",
    "karachi": "Asia/Karachi", "lahore": "Asia/Karachi",
    "islamabad": "Asia/Karachi", "peshawar": "Asia/Karachi",
    "quetta": "Asia/Karachi", "rawalpindi": "Asia/Karachi",
    "tashkent": "Asia/Tashkent", "astana": "Asia/Almaty",
    "almaty": "Asia/Almaty", "bishkek": "Asia/Bishkek",
    "dushanbe": "Asia/Dushanbe", "ashgabat": "Asia/Ashgabat",
    "tehran": "Asia/Tehran", "baghdad": "Asia/Baghdad",
    "riyadh": "Asia/Riyadh", "jeddah": "Asia/Riyadh",
    "dammam": "Asia/Riyadh", "medina": "Asia/Riyadh",
    "kuwait city": "Asia/Kuwait", "doha": "Asia/Qatar",
    "dubai": "Asia/Dubai", "abu dhabi": "Asia/Dubai",
    "sharjah": "Asia/Dubai", "muscat": "Asia/Muscat",
    "manama": "Asia/Bahrain", "doha international": "Asia/Qatar",
    "beirut": "Asia/Beirut", "aleppo": "Asia/Damascus",
    "damascus": "Asia/Damascus", "amman": "Asia/Amman",
    "jerusalem": "Asia/Jerusalem", "tel aviv": "Asia/Jerusalem",
    "haifa": "Asia/Jerusalem", "beersheba": "Asia/Jerusalem",

    # 鈹€鈹€ 澶ф磱娲?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
    "sydney": "Australia/Sydney", "melbourne": "Australia/Melbourne",
    "brisbane": "Australia/Brisbane", "adelaide": "Australia/Adelaide",
    "perth": "Australia/Perth", "hobart": "Australia/Hobart",
    "darwin": "Australia/Darwin", "canberra": "Australia/Sydney",
    "auckland": "Pacific/Auckland", "wellington": "Pacific/Auckland",
    "christchurch": "Pacific/Auckland", "dunedin": "Pacific/Auckland",
    "hamilton": "Pacific/Auckland", "suva": "Pacific/Fiji",
    "nadi": "Pacific/Fiji", "port moresby": "Pacific/Port_Moresby",

    # 鈹€鈹€ 闈炴床 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
    "cairo": "Africa/Cairo", "johannesburg": "Africa/Johannesburg",
    "cape town": "Africa/Johannesburg", "durban": "Africa/Johannesburg",
    "pretoria": "Africa/Johannesburg", "lagos": "Africa/Lagos",
    "abuja": "Africa/Lagos", "kano": "Africa/Lagos",
    "nairobi": "Africa/Nairobi", "kampala": "Africa/Kampala",
    "addis ababa": "Africa/Addis_Ababa", "casablanca": "Africa/Casablanca",
    "rabat": "Africa/Casablanca", "tunis": "Africa/Tunis",
    "algiers": "Africa/Algiers", "dakar": "Africa/Dakar",
    "accra": "Africa/Accra", "abidjan": "Africa/Abidjan",
    "luanda": "Africa/Luanda", "kinshasa": "Africa/Kinshasa",
    "johannesburg": "Africa/Johannesburg", "harare": "Africa/Harare",
    "lusaka": "Africa/Lusaka", "blantyre": "Africa/Blantyre",

    # 鈹€鈹€ 鍗楃編 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
    "buenos aires": "America/Argentina/Buenos_Aires",
    "sao paulo": "America/Sao_Paulo", "rio de janeiro": "America/Sao_Paulo",
    "lima": "America/Lima", "bogota": "America/Bogota",
    "medellin": "America/Bogota", "cali": "America/Bogota",
    "santiago": "America/Santiago", "valparaiso": "America/Santiago",
    "montevideo": "America/Montevideo", "asuncion": "America/Asuncion",
    "caracas": "America/Caracas", "quito": "America/Guayaquil",
    "guayaquil": "America/Guayaquil", "la paz": "America/La_Paz",
    "sucre": "America/La_Paz", "cordoba": "America/Argentina/Cordoba",
    "rosario": "America/Argentina/Buenos_Aires", "recife": "America/Recife",
    "brasilia": "America/Sao_Paulo", "belo horizonte": "America/Sao_Paulo",
    "salvador": "America/Sao_Paulo", "fortaleza": "America/Sao_Paulo",
    "manaus": "America/Manaus",

    # 鈹€鈹€ 澧ㄨタ鍝?涓編娲?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
    "mexico city": "America/Mexico_City", "guadalajara": "America/Mexico_City",
    "monterrey": "America/Mexico_City", "tijuana": "America/Tijuana",
    "juarez": "America/Denver", "leon": "America/Mexico_City",
    "puebla": "America/Mexico_City", "cancun": "America/Cancun",
    "merida": "America/Mexico_City", "hermosillo": "America/Hermosillo",
}

# ================================================
# Market Cache (to respect rate limits)
# ================================================
_market_cache = []
_market_cache_ts = 0

def is_market_expired(market) -> bool:
    """Check if market resolves before today (expired)."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    resolves_at = getattr(market, 'resolves_at', None)
    if resolves_at:
        try:
            end_str = str(resolves_at).split("T")[0]
            return end_str < today_str
        except Exception:
            return False
    return False

def refresh_market_cache():
    """Fetch all markets from Simmer, filter weather + non-expired, update cache."""
    global _market_cache, _market_cache_ts
    client = get_client(live=False)
    try:
        # Use tags=weather to fetch all weather markets (all cities)
        all_markets = client._request(
            "GET", "/api/sdk/markets",
            params={"tags": "weather", "status": "active", "limit": 500}
        ).get("markets", [])
        log.info(f"[CACHE] get_markets(tags='weather') returned {len(all_markets)} markets")
        
        weather_markets = []
        for m in all_markets:
            q = m.get("question", "") if isinstance(m, dict) else getattr(m, "question", "")
            if is_weather_market_question(q) and not is_market_expired(m):
                weather_markets.append(m)
        _market_cache = weather_markets
        _market_cache_ts = time.time()
        log.info(f"[CACHE] Refreshed {len(weather_markets)} weather markets (TTL={MARKET_CACHE_TTL}s)")
    except Exception as e:
        log.warning(f"[CACHE] Refresh failed: {e}")
        # On failure, keep old cache if exists, but do not update timestamp
        # (so next call will try again soon)

def get_cached_weather_markets() -> list:
    """Return weather markets, using cache if still fresh."""
    global _market_cache, _market_cache_ts
    now = time.time()
    if now - _market_cache_ts > MARKET_CACHE_TTL:
        log.info("[CACHE] Cache expired, refreshing...")
        refresh_market_cache()
    else:
        age_min = (now - _market_cache_ts) / 60
        log.debug(f"[CACHE] Cache hit (age {age_min:.1f}min, {len(_market_cache)} markets)")
    return _market_cache or []

def detect_timezone(question: str) -> Optional[pytz.BaseTzInfo]:
    q_low = question.lower()
    for city, tz_name in CITY_TZ_MAP.items():
        if city in q_low:
            try:
                return pytz.timezone(tz_name)
            except Exception:
                return None
    return None

def local_hhmm(tz):
    n = datetime.now(tz)
    return n.hour, n.minute

def is_scan_window(tz):
    h, _ = local_hhmm(tz)
    return 9 <= h < 10

def is_fallback_moment(tz):
    h, m = local_hhmm(tz)
    return h == 10 and m < 5

def get_market_price(m) -> float:
    if isinstance(m, dict):
        for key in ("current_probability", "external_price_yes", "price_yes", "probability"):
            val = m.get(key)
            if val is not None:
                try:
                    return float(val)
                except (TypeError, ValueError):
                    pass
    else:
        for attr in ("current_probability", "external_price_yes", "price_yes", "probability"):
            val = getattr(m, attr, None)
            if val is not None:
                try:
                    return float(val)
                except (TypeError, ValueError):
                    pass
    return 0.0

def already_holds(market_id: str, open_positions: dict, traded_today: list) -> bool:
    return market_id in open_positions or market_id in traded_today

# ============================================================================
# Market discovery / import (NEW ARCHITECTURE)
# ============================================================================

def get_import_quota(state: dict) -> int:
    """
    杩斿洖浠婃棩鍓╀綑瀵煎叆閰嶉銆?
    鐢变簬 Simmer briefing 涓嶇洿鎺ヨ繑鍥為厤棰濓紝鎴戜滑浣跨敤鏈湴鐘舵€佽窡韪細
    - 鐘舵€佷腑璁板綍 `imports_today` 鍜?`last_import_date`
    - 姣忔棩 UTC 鏃ユ湡鍙樻洿鏃惰嚜鍔ㄩ噸缃鏁板櫒
    Free 璐︽埛榛樿涓婇檺 10 娆?澶╋紝Pro 璐︽埛鍙涓?50
    """
    DAILY_IMPORT_LIMIT = 10  # TODO: Make configurable via env SIMMER_SNIPER2_DAILY_IMPORT_LIMIT
    
    today_utc = datetime.utcnow().strftime("%Y-%m-%d")
    last_date = state.get("last_import_date", "")
    
    # 濡傛灉鏃ユ湡鍙樹簡锛岄噸缃鏁板櫒
    if today_utc != last_date:
        state["imports_today"] = 0
        state["last_import_date"] = today_utc
        log.info(f"[QUOTA] New day ({today_utc}), reset import counter")
    
    imported_today = state.get("imports_today", 0)
    remaining = DAILY_IMPORT_LIMIT - imported_today
    log.info(f"[QUOTA] Today: {imported_today}/{DAILY_IMPORT_LIMIT} imported, {remaining} remaining")
    return remaining

def is_weather_market_question(q: str) -> bool:
    """Check if market is specifically about 'highest temperature' prediction."""
    q_low = q.lower()
    
    # Exclude noise categories
    noise = ["crypto", "bitcoin", "ethereum", "solana", "token", "defi",
             "president", "election", "vote", "senate", "house", "parliament",
             "football", "soccer", "basketball", "nba", "nfl", "mlb", "hockey",
             "stock", "nasdaq", "dow", "s&p", "index", "oil", "gold", "silver",
             "war", "military", "conflict", "attack", "missile",
             "covid", "pandemic", "virus", "disease"]
    if any(n in q_low for n in noise):
        return False
    
    # Must contain "highest temperature" or "highest temp"
    return ("highest temperature" in q_low) or ("highest temp" in q_low)



def discover_and_import(state: dict) -> int:
    """
    鏂版灦鏋勶細浣跨敤 /importable + /check + /import
    1. 鑾峰彇浠婃棩鍓╀綑閰嶉锛堝熀浜庢湰鍦扮姸鎬侊級
    2. 杞澶氫釜鍩庡競鍏抽敭璇嶆悳绱㈠彲瀵煎叆甯傚満
    3. 瀵规瘡涓€欓€夛紝鍏?/check 鏄惁宸插瓨鍦?
    4. 瀵规柊甯傚満鎵ц /import锛岀洿鍒伴厤棰濊€楀敖
    """
    client = get_client(live=False)
    
    # 1. 閰嶉
    remaining = get_import_quota(state)
    if remaining <= 0:
        log.warning("[DISCOVER] Daily import quota exhausted (0). Skipping.")
        return 0
    
    # 2. 鑾峰彇鎵€鏈夊彲瀵煎叆鐨?"highest temperature" 甯傚満锛堜笉闄愬煄甯傦級
    importable = []
    log.info("[DISCOVER] Fetching importable markets (q='highest temperature')")
    try:
        importable = client.list_importable_markets(
            min_volume=0,
            limit=50,
            venue="polymarket",
            q="highest temperature"
        )
        log.info(f"[DISCOVER] Found {len(importable)} importable markets")
    except Exception as e:
        log.warning(f"[DISCOVER] list_importable_markets failed: {e}")
        return 0
    
    # 3. 杩囨护澶╂皵甯傚満锛堜娇鐢ㄥ鏉剧殑 is_weather_market_question锛?
    weather_candidates = []
    for m in importable:
        q = m.get("question", "")
        if is_weather_market_question(q):
            weather_candidates.append(m)
    log.info(f"[DISCOVER] {len(weather_candidates)} weather markets after filter")
    
    # 4. 妫€鏌ュ凡瀛樺湪骞跺鍏?
    imported = 0
    for market in weather_candidates:
        if imported >= remaining:
            log.info("[DISCOVER] Reached daily quota limit")
            break
        url = market.get("url")
        if not url:
            continue
        # 妫€鏌ユ槸鍚﹀凡瀛樺湪
        try:
            exists = client.check_market_exists(polymarket_url=url)
            if exists.get("exists"):
                continue
        except Exception:
            continue
        
        # 鎵ц瀵煎叆
        try:
            resp = client.import_market(polymarket_url=url)
            if resp.get("status") == "imported":
                imported += 1
                state["imports_today"] = state.get("imports_today", 0) + 1
                save_state(state)
                log.info(f"[DISCOVER] Imported: {market.get('question', '')[:60]}... (total today: {state['imports_today']})")
            else:
                log.debug(f"[DISCOVER] Import not successful: {resp}")
        except Exception as e:
            if "rate limit" in str(e).lower() or "429" in str(e):
                log.warning("[DISCOVER] Rate limited, pausing")
                break
            log.debug(f"[DISCOVER] Import error: {e}")
    
    log.warning(f"[DISCOVER] Imported {imported} new markets today")
    return imported



def fetch_weather_markets() -> list:
    """
    杩斿洖缂撳瓨鐨勫ぉ姘斿競鍦哄垪琛紙宸茶繃婊よ繃鏈燂級
    缂撳瓨鐢?get_cached_weather_markets() 绠＄悊锛屾瘡 MARKET_CACHE_TTL 绉掑埛鏂颁竴娆?
    """
    return get_cached_weather_markets()

def ensure_weather_markets_imported() -> list:
    """
    纭繚澶╂皵甯傚満宸茬紦瀛樺苟杩斿洖銆?
    鐩存帴浣跨敤 get_cached_weather_markets()锛堝熀浜?tags=weather 鏌ヨ锛?
    """
    return get_cached_weather_markets()

def run_redeem_cycle(client, dry_run: bool = False) -> dict:
    """Run one redeem cycle. Returns stats dict."""
    stats = {"checked": 0, "redeemed": 0, "failed": 0, "errors": []}
    try:
        positions = client.get_positions(venue="polymarket")
        redeemable = [p for p in positions if getattr(p, 'redeemable', False)]
        stats["checked"] = len(redeemable)
        log.info(f"[REDEEM] Found {len(redeemable)} redeemable positions")
        for pos in redeemable:
            market_id = getattr(pos, 'market_id', None) or (pos.get('market_id') if isinstance(pos, dict) else None)
            side = getattr(pos, 'side', None) or (pos.get('side') if isinstance(pos, dict) else None)
            if not market_id or not side:
                continue
            q = getattr(pos, 'question', '') or (pos.get('question', 'N/A'))
            log.info(f"[REDEEM] Redeeming: {q[:50]}... ({market_id}, side={side})")
            try:
                if dry_run:
                    log.info(f"[REDEEM] Dry-run: would redeem {market_id}")
                    continue
                result = client.redeem(market_id=market_id, side=side)
                if result.get('success'):
                    stats["redeemed"] += 1
                    log.info(f"[REDEEM] Success: tx_hash={result.get('tx_hash')}")
                else:
                    stats["failed"] += 1
                    err = result.get('error', 'unknown')
                    stats["errors"].append(f"{market_id}: {err}")
                    log.warning(f"[REDEEM] Failed: {err}")
            except Exception as e:
                stats["failed"] += 1
                stats["errors"].append(str(e))
                log.warning(f"[REDEEM] Exception: {e}")
    except Exception as e:
        log.error(f"[REDEEM] Cycle error: {e}", exc_info=True)
    return stats


# ============================================================================
# Trading logic (unchanged from original, using new market list)
# ============================================================================

def check_context_safeguards(market_id: str, price: float, now_dt: datetime, tz, skip_threshold: bool=False) -> tuple[bool, str]:
    ENFORCE_9AM_4PM = True
    if ENFORCE_9AM_4PM:
        h = now_dt.astimezone(tz).hour
        if not (9 <= h < 16):
            return False, "outside 9am-4pm local"
    if price < 0.05 or price > 0.95:
        return False, "price out of bounds [0.05, 0.95]"
    if not skip_threshold and price < ENTRY_THRESHOLD:
        return False, f"price < entry ({ENTRY_THRESHOLD:.0%})"
    return True, "OK"

def maybe_buy(market, open_positions: dict, traded_today: list, now_dt: datetime, is_fallback: bool=False, dry_run: bool=False) -> tuple[bool, str]:
    market_id = getattr(market, "id", None)
    if not market_id:
        return False, "no market id"
    if already_holds(market_id, open_positions, traded_today):
        return False, "already hold/open"
    price = get_market_price(market)
    if price <= 0:
        return False, "price 0"
    q = getattr(market, "question", "")
    tz = detect_timezone(q)
    if tz is None:
        return False, "no timezone"
    ok, reason = check_context_safeguards(market_id, price, now_dt, tz, skip_threshold=is_fallback)
    if not ok:
        return False, reason
    # 鎵ц涔板叆
    try:
        client = get_client(live=True)
        shares = SHARES_PER_ORDER
        cost_usd = round(shares * price, 4)
        if cost_usd > MAX_POSITION_USD:
            return False, f"cost ${cost_usd:.2f} > max ${MAX_POSITION_USD:.2f}"
        # Simmer SDK trade (correct method)
        try:
            order = client.trade(
                market_id=market_id,
                side="yes",
                shares=shares,
                price=price,
                dry_run=dry_run
            )
        except AttributeError:
            # Fallback to older place_order API
            order = client.place_order(
                market_id=market_id,
                side="yes",
                shares=shares,
                price=price
            )
        log.info(f"[BUY] {q[:50]}... price={price:.2%} shares={shares} cost=${cost_usd:.2f}")
        return True, f"bought {shares} shares @ {price:.2%}"
    except Exception as e:
        log.warning(f"[BUY] failed: {e}")
        return False, str(e)

def maybe_sell_tp_sl(market, position, now_dt: datetime) -> tuple[bool, str]:
    # 绠€鍖栧疄鐜帮細鏆備笉灞曞紑
    return False, "tp/sl not implemented"

def load_state() -> dict:
    state_file = ROOT / "sniper.state.json"
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except:
            pass
    return {"traded_today": [], "last_report_ts": 0, "date": "", "last_discovery_ts": 0, "imports_today": 0, "last_import_date": "", "last_redeem_ts": 0, "redeem_stats": {"checked": 0, "redeemed": 0, "failed": 0}}

def save_state(state: dict):
    state_file = ROOT / "sniper.state.json"
    try:
        state_file.write_text(json.dumps(state, indent=2))
    except Exception as e:
        log.warning(f"[STATE] save failed: {e}")

def find_upcoming_windows(weather_markets: list, hours_ahead: int = 6) -> list:
    """Find markets whose event date (resolves-1) will enter 9-10 AM window within next N hours."""
    now_dt = datetime.utcnow()
    upcoming = []
    
    for m in weather_markets:
        q = m.get('question', '') if isinstance(m, dict) else getattr(m, 'question', '')
        tz = detect_timezone(q)
        if tz is None:
            continue
        
        resolves = m.get('resolves_at') if isinstance(m, dict) else getattr(m, 'resolves_at', None)
        if not resolves:
            continue
        if isinstance(resolves, str):
            try:
                date_part = resolves.split('T')[0].split(' ')[0]
                resolves_dt = datetime.strptime(date_part, "%Y-%m-%d")
            except:
                continue
        else:
            resolves_dt = resolves
        
        # Event date is one day BEFORE resolves (since resolves at midnight UTC)
        event_date = resolves_dt - timedelta(days=1)
        
        try:
            window_start = event_date.replace(hour=9, minute=0, second=0, microsecond=0)
            if window_start.tzinfo is None:
                window_start = tz.localize(window_start) if hasattr(tz, 'localize') else tz.fromutc(window_start.replace(tzinfo=pytz.utc))
            else:
                window_start = window_start.astimezone(tz)
        except Exception:
            continue
        
        now_city = datetime.now(tz)
        if now_city >= window_start:
            continue
        hours_until = (window_start - now_city).total_seconds() / 3600
        # Also check that event_date is today or tomorrow relative to now_city
        days_diff = (event_date.date() - now_city.date()).days
        if 0 < hours_until <= hours_ahead and days_diff <= 1:
            upcoming.append((m, window_start, hours_until))
    
    upcoming.sort(key=lambda x: x[2])
    return upcoming


def print_cycle_summary(summary: dict, weather_markets: list):
    print("\n=== Cycle Summary ===")
    print(f"Weather markets available: {len(weather_markets)}")
    print(f"Signals: {summary['signals']}")
    print(f"Attempted: {summary['attempted']}")
    print(f"Executed: {summary['executed']}")

    upcoming = find_upcoming_windows(weather_markets, hours_ahead=6)
    if upcoming:
        from collections import defaultdict
        print("\n--- Upcoming Windows (next 6h) ---")
        # Group by city+date to avoid clutter
        grouped = defaultdict(list)
        for m, window_start, hours_until in upcoming:
            q = m.get('question', '') if isinstance(m, dict) else getattr(m, 'question', '')
            price = get_market_price(m)
            # Get city name from question
            q_low = q.lower()
            city = "Unknown"
            for c in CITY_TZ_MAP.keys():
                if c in q_low:
                    city = c.title()
                    break
            # Event date from window_start
            date_str = window_start.strftime("%m-%d")
            grouped[(city, date_str)].append((m, window_start, hours_until, price))

            # For each city+date, show the option with highest price (consensus)
        for (city, date_str), items in sorted(grouped.items(), key=lambda x: x[0]):
            # Pick item with max price
            best = max(items, key=lambda it: it[3])
            m, window_start, hours_until, price = best
            q = m.get('question', '') if isinstance(m, dict) else getattr(m, 'question', '')
            market_id = m.get('id', '')
            # Prefer the 'url' field from API (usually simmer.markets)
            market_url = m.get('url', '')
            if not market_url and market_id:
                market_url = f"https://simmer.markets/{market_id}"
            url_display = f"\n    {market_url}" if market_url else ""
            print(f"  [{hours_until:.1f}h] {city} ({date_str}) Price: {price:.1%} | {q[:50]}...{url_display}")
    if summary.get('errors'):
        print("Errors:")
        for err in summary['errors'][:5]:
            print(f"  - {err}")

def print_report(open_positions: dict, weather_markets: list, state: dict, summary: dict):
    print("\n=== Daily Report ===")
    print(f"Date: {state.get('date')}")
    print(f"Total weather markets: {len(weather_markets)}")
    print(f"Open positions: {len(open_positions)}")
    print(f"Traded today: {len(state.get('traded_today', []))}")
    print(f"Cycle summary: {summary}")

    # Redeem stats
    redeem_stats = state.get("redeem_stats", {})
    if redeem_stats:
        print(f"Redeemed (total): {redeem_stats.get('redeemed', 0)} positions")

    # Detailed market list with city and date (grouped by city+date, showing best option)
    print("\n--- Markets Overview ---")
    from collections import defaultdict
    grouped = defaultdict(list)
    for m in weather_markets[:50]:
        q = m.get('question', '') if isinstance(m, dict) else getattr(m, 'question', '')
        price = get_market_price(m)
        # Get city name from question
        q_low = q.lower()
        city = "Unknown"
        for c in CITY_TZ_MAP.keys():
            if c in q_low:
                city = c.title()
                break
        # Resolves date
        resolves = m.get('resolves_at') if isinstance(m, dict) else getattr(m, 'resolves_at', None)
        if resolves:
            if isinstance(resolves, str):
                try:
                    date_part = resolves.split('T')[0].split(' ')[0]
                    resolves_dt = datetime.strptime(date_part, "%Y-%m-%d")
                    date_str = resolves_dt.strftime("%m-%d")
                except:
                    date_str = str(resolves)[:5]
            else:
                date_str = resolves.strftime("%m-%d")
        else:
            date_str = "N/A"
        grouped[(city, date_str)].append((m, price))

    # Show best option per city+date
    displayed = 0
    for (city, date_str), items in sorted(grouped.items(), key=lambda x: x[0]):
        # Pick item with max price
        best_m, best_price = max(items, key=lambda it: it[1] if it[1] else 0)
        q = best_m.get('question', '') if isinstance(best_m, dict) else getattr(best_m, 'question', '')
        price_str = f"{best_price:.1%}" if best_price else "N/A"
        q_short = q[:70] if q else ""
        market_id = best_m.get('id', '')
        market_url = best_m.get('url', '')
        if not market_url and market_id:
            market_url = f"https://simmer.markets/{market_id}"
        url_display = f"\n    {market_url}" if market_url else ""
        print(f"  {city} ({date_str}) Price: {price_str} | {q_short}...{url_display}")
        displayed += 1
        if displayed >= 20:
            break

def run_once(dry_run: bool = False) -> dict:
    now_ts = time.time()
    now_dt = datetime.utcnow()
    state = load_state()
    
    # 鏃ユ湡婊氬姩
    today_str = now_dt.strftime("%Y-%m-%d")
    if state.get("date") != today_str:
        state["date"] = today_str
        state["traded_today"] = []
        # 鏂扮殑涓€澶╋紝鍙兘闇€瑕侀噸鏂板彂鐜板競鍦?
        state["last_discovery_ts"] = 0    
    # Redeem phase (if enabled)
    if get_cfg("enable_redeem"):
        redeem_interval = get_cfg("redeem_interval_seconds")
        if now_ts - state.get("last_redeem_ts", 0) >= redeem_interval:
            log.info("[REDEEM] Starting redeem cycle")
            client = get_client(live=not dry_run)
            redeem_stats = run_redeem_cycle(client, dry_run=dry_run)
            # Update state
            state["last_redeem_ts"] = now_ts
            # Accumulate stats
            prev = state.get("redeem_stats", {"checked": 0, "redeemed": 0, "failed": 0})
            prev["checked"] += redeem_stats["checked"]
            prev["redeemed"] += redeem_stats["redeemed"]
            prev["failed"] += redeem_stats["failed"]
            state["redeem_stats"] = prev
            save_state(state)
            log.info(f"[REDEEM] Cycle done: {redeem_stats}")
    
    # 1. 鍙戠幇闃舵锛堝鏋滀粖澶╄繕娌″彂鐜拌繃锛屾垨璺濈涓婃瓒呰繃 12 灏忔椂锛?
    if now_ts - state.get("last_discovery_ts", 0) >= 12 * 3600:
        log.info("[RUN] Discovery phase")
        if not dry_run:
            count = discover_and_import(state)
        else:
            log.info("[DRY-RUN] Skipping import")
            count = 0
        state["last_discovery_ts"] = now_ts
        save_state(state)
    
    # 2. 鎵弿闃舵
    log.info("[RUN] Scanning phase")
    weather_markets = ensure_weather_markets_imported()
    
    # 3. 鑾峰彇褰撳墠鎸佷粨
    try:
        client = get_client(live=not dry_run)
        venue = "polymarket" if not dry_run else "sim"
        positions_data = client.get_positions(venue=venue)
        open_positions = {p.market_id: p for p in positions_data if getattr(p, 'shares_yes', 0) > 0}
    except Exception as e:
        log.warning(f"[POS] error: {e}")
        open_positions = {}
    
    summary = {"signals": 0, "attempted": 0, "executed": 0, "errors": [], "blocked": []}
    amount_usd = 0.0
    # 4. 按城市分组扫描
    from collections import defaultdict
    grouped = defaultdict(list)
    for m in weather_markets:
        q = getattr(m, 'question', '')
        tz = detect_timezone(q)
        if not tz:
            continue
        city = tz.zone
        resolves = getattr(m, 'resolves_at', None)
        if not resolves:
            continue
        # Extract date string
        if isinstance(resolves, str):
            try:
                date_part = resolves.split('T')[0].split(' ')[0]
                date_str = datetime.strptime(date_part, "%Y-%m-%d").strftime("%m-%d")
            except:
                date_str = str(resolves)[:5]
        else:
            try:
                date_str = resolves.strftime("%m-%d")
            except:
                date_str = str(resolves)[:5]
        grouped[(city, date_str)].append(m)

    # Process each group
    for (city, date_str), markets in grouped.items():
        # Pick the option with highest yes% (price)
        best_market = max(markets, key=lambda m: get_market_price(m))
        price = get_market_price(best_market)
        if price <= 0:
            continue

        # Check time window
        if city in CITY_TZ_MAP:
            tz = pytz.timezone(CITY_TZ_MAP[city])
        else:
            try:
                tz = pytz.timezone(city)
            except:
                tz = None
        if tz is None:
            continue
        is_window = is_scan_window(tz)
        is_fallback = FALLBACK_AT_10 and is_fallback_moment(tz)
        if not (is_window or is_fallback):
            continue

        # Threshold: fallback mode has no price threshold
        threshold = 0 if is_fallback else ENTRY_THRESHOLD
        if price < threshold:
            continue

        # Check already holds (by market_id of best option)
        market_id = getattr(best_market, 'id', None)
        if not market_id:
            continue
        if already_holds(market_id, open_positions, state.get('traded_today', [])):
            continue

        summary['signals'] += 1
        if dry_run:
            log.info(f"[SIGNAL] {city} {date_str} price={price:.2%} (dry-run skip)")
            continue

        # maybe_buy needs to know if this is fallback
        success, reason = maybe_buy(best_market, open_positions, state.get('traded_today', []), now_dt, is_fallback=is_fallback, dry_run=dry_run)
        if success:
            summary['executed'] += 1
            amount_usd += round(SHARES_PER_ORDER * price, 4)
            state['traded_today'].append(market_id)
            save_state(state)
        else:
            summary['attempted'] += 1
            summary['blocked'].append((f"{city} {date_str}", reason))

    log.warning(f"Cycle done | signals={summary['signals']} attempted={summary['attempted']} executed={summary['executed']}")
    log.warning(f"Cycle done | signals={summary['signals']} attempted={summary['attempted']} executed={summary['executed']}")
    
    print_cycle_summary(summary, weather_markets)
    
    # Send Telegram summary if enabled
    if get_cfg("telegram_enabled"):
        upcoming_count = len(find_upcoming_windows(weather_markets, hours_ahead=6))
        tel_msg = (
            f"Weather Sniper Cycle\n"
            f"Markets: {len(weather_markets)}\n"
            f"Signals: {summary['signals']}\n"
            f"Executed: {summary['executed']}\n"
            f"Upcoming (6h): {upcoming_count}"
        )
        send_telegram(tel_msg, silent=True)
    
    # 5. 瀹氭湡鎶ュ憡
    need_report = now_ts - state.get("last_report_ts", 0) >= REPORT_INTERVAL
    if need_report:
        print_report(open_positions, weather_markets, state, summary)
        state["last_report_ts"] = now_ts
        save_state(state)
    
    if os.environ.get("AUTOMATON_MANAGED"):
        report = {"signals": summary["signals"], "trades_attempted": summary["attempted"], "trades_executed": summary["executed"], "amount_usd": round(amount_usd, 2)}
        print(json.dumps({"automaton": report}))
    
    # Prepare market details for agent response
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    market_details = []
    date_breakdown = {"expired": 0, "today": 0, "future": 0}
    for m in weather_markets:
        resolves_at = getattr(m, 'resolves_at', None)
        if resolves_at:
            try:
                end_str = str(resolves_at).split("T")[0]
                if end_str < today_str:
                    date_breakdown["expired"] += 1
                elif end_str == today_str:
                    date_breakdown["today"] += 1
                else:
                    date_breakdown["future"] += 1
            except Exception:
                date_breakdown["future"] += 1
        else:
            date_breakdown["future"] += 1
        market_details.append({
            "id": getattr(m, 'id', None),
            "question": getattr(m, 'question', '')[:80],
            "resolves_at": str(resolves_at) if resolves_at else None,
            "volume": getattr(m, 'volume', None),
            "yes_bid": getattr(m, 'yes_bid', None),
        })
    
    return {
        "signals": summary["signals"],
        "attempted": summary["attempted"],
        "executed": summary["executed"],
        "amount_usd": round(amount_usd, 2),
        "markets_count": len(weather_markets),
        "date_breakdown": date_breakdown,
        "markets": market_details[:20],  # limit to first 20 for brevity
    }

def agent_tool_main():
    input_data = {}
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        pass
    dry_run = input_data.get("dry_run", False)
    try:
        stats = run_once(dry_run=dry_run)
        result = {"status": "success", "message": "Sniper cycle completed", "live": not dry_run, "timestamp": datetime.utcnow().isoformat() + "Z", "stats": stats}
    except Exception as e:
        result = {"status": "error", "message": str(e), "live": not dry_run, "timestamp": datetime.utcnow().isoformat() + "Z"}
        send_telegram(f"馃毃 Sniper cycle ERROR\n{str(e)[:200]}")

    return result

# ============================================================================
# Telegram utilities
# ============================================================================
def _tg_token() -> Optional[str]:
    """Get Telegram bot token from config or env."""
    # First try config (which may have default empty string)
    token = get_cfg("telegram_bot_token")
    if not token:
        # Fallback to env
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
    return token or None

def send_telegram(text: str, silent: bool = False) -> bool:
    """Send a message to the configured Telegram chat."""
    token = _tg_token()
    if not token:
        return False
    chat_id = get_cfg("telegram_chat_id") or os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "disable_notification": silent}
    try:
        resp = requests.post(url, data=payload, timeout=10)
        if resp.status_code != 200:
            log.warning(f"[TG] send failed: {resp.status_code} {resp.text}")
            return False
        return True
    except Exception as e:
        log.warning(f"[TG] exception: {e}")
        return False

def telegram_probe() -> bool:
    """Test Telegram connectivity by calling getMe."""
    token = _tg_token()
    if not token:
        return False
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        resp = requests.get(url, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Weather High-Temp Sniper v1.0.4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sniper.py --live              Live daemon: trades + Telegram reports
  python sniper.py                     Dry-run daemon (no real trades)
  python sniper.py --positions         Show current positions and exit
  python sniper.py --config            Show active configuration and exit
  python sniper.py --test-telegram     Verify Telegram config and exit
  python sniper.py --set entry_price_threshold=0.40
        """,
    )
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions and exit")
    parser.add_argument("--config", action="store_true", help="Show config and exit")
    parser.add_argument("--test-telegram", action="store_true", help="Test Telegram and exit")
    parser.add_argument("--set", type=str, metavar="KEY=VALUE", help="Persist config value")
    parser.add_argument("--quiet", action="store_true", help="Suppress info/warning logs")
    args = parser.parse_args()

    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)

    if args.test_telegram:
        print("Testing Telegram connection...")
        if not telegram_probe():
            print("Bot token invalid or network unreachable. Check TELEGRAM_BOT_TOKEN.")
            sys.exit(1)
        sent = send_telegram(
            f"🌡️ Weather High-Temp Sniper\n"
            f"Telegram test successful.\n"
            f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )
        if sent:
            print("Test message sent.")
        else:
            print("Failed to send test message.")
    if args.config:
        print("Current configuration:")
        for k in CONFIG_SCHEMA:
            val = get_cfg(k)
            display = "***" if ("key" in k or "token" in k) and val else val
            print(f"  {k}: {display}")
        return
    if args.set:
        try:
            key, val_str = args.set.split("=", 1)
            if key in CONFIG_SCHEMA:
                typ = CONFIG_SCHEMA[key]["type"]
                if typ is bool:
                    val = val_str.lower() in ("true", "1", "yes")
                elif typ is int:
                    val = int(val_str)
                elif typ is float:
                    val = float(val_str)
                else:
                    val = val_str
                if SKILL_FRAMEWORK:
                    update_config({key: val}, __file__, slug="polymarket-weather-high-temp-sniper")
                else:
                    os.environ[CONFIG_SCHEMA[key]["env"]] = str(val)
                print(f"Updated {key} = {val}")
            else:
                print(f"Unknown config key: {key}")
                print(f"Available: {', '.join(CONFIG_SCHEMA.keys())}")
        except ValueError:
            print("Usage: --set KEY=VALUE")
            return

    live = args.live or bool(os.environ.get("AUTOMATON_MANAGED"))
    dry_run = not live

    if TELEGRAM_ENABLED:
        if telegram_probe():
            print("Telegram: connected")
        else:
            print("Bot token invalid or network unreachable. Check TELEGRAM_BOT_TOKEN.")
            sys.exit(1)
    startup_msg = (
        f"馃尅锔?Weather High-Temp Sniper {'LIVE' if live else 'DRY-RUN'}\n"
        f"Entry: >= {ENTRY_THRESHOLD:.0%} | max=${MAX_POSITION_USD:.2f} | "
        f"scan={SCAN_INTERVAL}s | report={REPORT_INTERVAL}s\n"
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC  |  Press Ctrl+C to stop."
    )

    print(startup_msg)
    send_telegram(startup_msg)

    try:
        while True:
            run_once(dry_run=dry_run)
            time.sleep(SCAN_INTERVAL)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        log.exception("Fatal error")
        send_telegram(f"馃毃 Sniper FATAL ERROR\n{str(e)[:200]}")
        raise

if __name__ == "__main__":
    if not sys.stdin.isatty():
        agent_tool_main()
    else:
        main()

