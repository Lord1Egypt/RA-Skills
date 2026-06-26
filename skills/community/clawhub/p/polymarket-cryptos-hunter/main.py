"""
HUNTER ULTIMATE v4 — PURE LIVE TRADING & ON-CHAIN TRUTH
══════════════════════════════════════════════════════════════════════
Ce script est prêt pour la production sur OpenClaw.
La balance est lue directement sur la blockchain Polygon (Phantom).
Les Fills proviennent de l'API live de Polymarket.
══════════════════════════════════════════════════════════════════════
"""

import json
import time
import sqlite3
import logging
import requests
import threading
import os
from datetime import datetime
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import argparse
from web3 import Web3

try:
    import websocket

    WS_AVAILABLE = True
except ImportError:
    WS_AVAILABLE = False
    print("  ⚠️ websocket-client non installé — fallback REST actif")

# ══════════════════════════════════════════════════════════════
#  CONFIG (Variables d'environnement)
# ══════════════════════════════════════════════════════════════
load_dotenv()

WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
POLYMARKET_API_KEY = os.getenv("POLYMARKET_API_KEY")
POLYMARKET_API_SECRET = os.getenv("POLYMARKET_API_SECRET")
POLYMARKET_API_PASSPHRASE = os.getenv("POLYMARKET_API_PASSPHRASE")

if not WALLET_PRIVATE_KEY:
    print("❌ FATAL: WALLET_PRIVATE_KEY manquant dans le fichier .env")
    exit(1)

# --- STRATEGY PARAMS ---
BASE_RISK_PCT = 0.02  # Le bot trade avec 2% de la vraie balance
MAX_RISK_PCT = 0.06
MIN_SHARES = 10
MAX_OPEN_MARKETS = 10
DAILY_STOP_PCT = 0.15  # Stop-Loss si le portefeuille chute de 15%

SPREAD_MIN = 0.51
SPREAD_DEFAULT = 0.52
SPREAD_MAX = 0.57

BID_SWEET_MIN = 0.43
BID_SWEET_MAX = 0.54
MAX_BID_IMBALANCE = 0.040
MIN_DEPTH_SHARES = 20

TREND_LOOKBACK = 600
TREND_TRIGGER = 3
TREND_HALT_SECS = 300

ATOMIC_CLOSE_SECS = 5  # Kill Switch (Protection Legging)
ORDER_CANCEL_SECS = 12
ENTRY_START_5M = 15
ENTRY_END_5M = 120
ENTRY_START_15M = 45
ENTRY_END_15M = 210

MAX_VOLATILITY_PCT = 0.004
FEES_RATE = 0.0156
ARB_THRESHOLD = 0.97

ASSETS = {
    "btc": {
        "ticker": "BTCUSDT",
        "slug_5m": "btc-updown-5m",
        "slug_15m": "btc-updown-15m",
    },
    "eth": {
        "ticker": "ETHUSDT",
        "slug_5m": "eth-updown-5m",
        "slug_15m": "eth-updown-15m",
    },
    "sol": {
        "ticker": "SOLUSDT",
        "slug_5m": "sol-updown-5m",
        "slug_15m": "sol-updown-15m",
    },
    "xrp": {
        "ticker": "XRPUSDT",
        "slug_5m": "xrp-updown-5m",
        "slug_15m": "xrp-updown-15m",
    },
}

logging.basicConfig(
    filename="hunter_errors.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# ══════════════════════════════════════════════════════════════
#  BOOK CACHE (Haute Fréquence)
# ══════════════════════════════════════════════════════════════


class BookCache:
    def __init__(self):
        self._lock = threading.RLock()
        self._books = {}
        self._subs = set()
        self._ws = None
        self._ws_ok = False
        self._sess = requests.Session()
        self._sess.headers["User-Agent"] = "HunterUltimate/Live"
        self._stop = threading.Event()

        self._rest_thread = threading.Thread(target=self._rest_poller, daemon=True)
        self._rest_thread.start()

        if WS_AVAILABLE:
            self._ws_thread = threading.Thread(target=self._ws_runner, daemon=True)
            self._ws_thread.start()

    def subscribe(self, token_ids):
        with self._lock:
            new = [t for t in token_ids if t not in self._subs]
            self._subs.update(token_ids)
        if new and self._ws and self._ws_ok:
            try:
                self._ws.send(
                    json.dumps(
                        {"type": "subscribe", "channel": "book", "asset_ids": new}
                    )
                )
            except Exception:
                pass

    def get(self, token_id):
        with self._lock:
            return self._books.get(token_id, {}).copy()

    def _parse_book(self, token_id, data):
        asks = data.get("asks", [])
        bids = data.get("bids", [])
        with self._lock:
            self._books[token_id] = {
                "ask": min(float(a["price"]) for a in asks) if asks else None,
                "bid": max(float(b["price"]) for b in bids) if bids else None,
                "asks": asks,
                "bids": bids,
                "ts": time.time(),
            }

    def _rest_fetch(self, token_id):
        try:
            r = self._sess.get(
                f"https://clob.polymarket.com/book?token_id={token_id}", timeout=1.2
            )
            self._parse_book(token_id, r.json())
        except Exception:
            pass

    def _rest_poller(self):
        while not self._stop.is_set():
            with self._lock:
                subs = list(self._subs)
            if not self._ws_ok and subs:
                with ThreadPoolExecutor(max_workers=8) as ex:
                    list(ex.map(self._rest_fetch, subs))
            time.sleep(0.5)

    def _ws_runner(self):
        ws_url = "wss://clob.polymarket.com/"

        def on_open(ws):
            self._ws_ok = True
            with self._lock:
                subs = list(self._subs)
            if subs:
                ws.send(
                    json.dumps(
                        {"type": "subscribe", "channel": "book", "asset_ids": subs}
                    )
                )

        def on_message(ws, message):
            try:
                data = json.loads(message)
                if isinstance(data, list):
                    for item in data:
                        tid = item.get("asset_id") or item.get("market")
                        if tid:
                            self._parse_book(tid, item)
                elif isinstance(data, dict):
                    tid = data.get("asset_id") or data.get("market")
                    if tid:
                        self._parse_book(tid, data)
            except Exception:
                pass

        def on_error(ws, err):
            self._ws_ok = False

        def on_close(ws, *args):
            self._ws_ok = False

        while not self._stop.is_set():
            try:
                self._ws = websocket.WebSocketApp(
                    ws_url,
                    on_open=on_open,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close,
                )
                self._ws.run_forever(ping_interval=30, ping_timeout=10)
            except Exception:
                pass
            time.sleep(5)

    def stop(self):
        self._stop.set()
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════
#  DATABASE (Journal d'audit uniquement)
# ══════════════════════════════════════════════════════════════


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("hunter_live_audit.db", check_same_thread=False)
        self._lock = threading.Lock()
        self.c = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.c.executescript("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                asset TEXT, slug TEXT, timeframe TEXT, strategy TEXT, up_fill REAL, dn_fill REAL,
                shares INTEGER, spread_used REAL, collected REAL, payout REAL, profit REAL,
                real_balance REAL, close_reason TEXT
            );
        """)
        self.conn.commit()

    def log_trade(
        self,
        asset,
        slug,
        tf,
        strategy,
        up_fill,
        dn_fill,
        shares,
        spread,
        collected,
        payout,
        profit,
        real_balance,
        reason,
    ):
        with self._lock:
            self.c.execute(
                """
                INSERT INTO trades (asset,slug,timeframe,strategy,up_fill,dn_fill, shares,spread_used,collected,payout,profit,real_balance,close_reason)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    asset,
                    slug,
                    tf,
                    strategy,
                    up_fill,
                    dn_fill,
                    shares,
                    spread,
                    collected,
                    payout,
                    profit,
                    real_balance,
                    reason,
                ),
            )
            self.conn.commit()


# ══════════════════════════════════════════════════════════════
#  ASSET TRACKER / TREND / CORRELATION / FILL ADAPTOR
# ══════════════════════════════════════════════════════════════


class AssetTracker:
    def __init__(self):
        self.fills = defaultdict(list)

    def record(self, asset, filled):
        self.fills[asset].append((time.time(), filled))
        if len(self.fills[asset]) > 100:
            self.fills[asset] = self.fills[asset][-100:]

    def fill_rate(self, asset, secs=3600):
        now = time.time()
        r = [f for t, f in self.fills[asset] if now - t < secs]
        return sum(r) / len(r) if len(r) >= 3 else 0.5

    def should_skip(self, asset):
        return len(self.fills[asset]) >= 5 and self.fill_rate(asset) < 0.25


class TrendDetector:
    def __init__(self):
        self.fills = deque()
        self.halted_until = 0.0

    def record_onesided(self, direction):
        now = time.time()
        self.fills.append((now, direction))
        while self.fills and now - self.fills[0][0] > TREND_LOOKBACK:
            self.fills.popleft()
        up = sum(1 for _, d in self.fills if d == "UP")
        dn = sum(1 for _, d in self.fills if d == "DN")
        if max(up, dn) >= TREND_TRIGGER:
            self.halted_until = now + TREND_HALT_SECS
            print(f"\n  📈 TENDANCE ({max(up, dn)} fills) → Pause {TREND_HALT_SECS}s")

    def is_trending(self):
        return time.time() < self.halted_until

    def remaining(self):
        return max(0, int(self.halted_until - time.time()))


class CorrelationGuard:
    def __init__(self):
        self.risky = {}

    def mark(self, asset, cycle_ts):
        self.risky.setdefault(cycle_ts, set()).add(asset)
        if len(self.risky) > 12:
            del self.risky[min(self.risky)]

    def is_risky(self, cycle_ts):
        return len(self.risky.get(cycle_ts, set())) >= 2


class FillAdaptor:
    def __init__(self):
        self.history = []

    def record(self, filled):
        self.history.append(filled)
        if len(self.history) > 40:
            self.history = self.history[-40:]

    @property
    def fill_rate(self):
        return min(0.70, sum(self.history) / len(self.history)) if self.history else 0.5

    def adjusted_spread(self, base):
        if len(self.history) < 10:
            return base
        r = self.fill_rate
        if r > 0.85:
            return min(SPREAD_MAX, round(base + 0.003, 3))
        if r > 0.70:
            return min(SPREAD_MAX, round(base + 0.001, 3))
        if r < 0.30:
            return max(SPREAD_MIN, round(base - 0.003, 3))
        if r < 0.45:
            return max(SPREAD_MIN, round(base - 0.001, 3))
        return base

    def size_mult(self):
        r = self.fill_rate
        if r < 0.25:
            return 0.5
        if r < 0.40:
            return 0.75
        if r > 0.80:
            return 1.25
        return 1.0


# ══════════════════════════════════════════════════════════════
#  MARKET DATA
# ══════════════════════════════════════════════════════════════


class DataFeed:
    def __init__(self, book_cache: BookCache):
        self.cache = book_cache
        self.s = requests.Session()
        self._price = {}
        self._vol = {}
        self._mkt = {}
        self._bg = threading.Thread(target=self._bg_refresh, daemon=True)
        self._bg.start()

    def _bg_refresh(self):
        while True:
            for cfg in ASSETS.values():
                try:
                    r = self.s.get(
                        f"https://api.binance.com/api/v3/ticker/price?symbol={cfg['ticker']}",
                        timeout=1.2,
                    ).json()
                    self._price[cfg["ticker"]] = {
                        "t": time.time(),
                        "v": float(r["price"]),
                    }

                    r2 = self.s.get(
                        f"https://api.binance.com/api/v3/klines?symbol={cfg['ticker']}&interval=1m&limit=3",
                        timeout=1.2,
                    ).json()
                    if len(r2) >= 2:
                        vol = abs(float(r2[-1][4]) - float(r2[-2][4])) / float(
                            r2[-2][4]
                        )
                        self._vol[cfg["ticker"]] = {"t": time.time(), "v": vol}
                except Exception:
                    pass
            time.sleep(3)

    def get_spot(self, ticker):
        return self._price.get(ticker, {}).get("v")

    def get_volatility(self, ticker):
        return self._vol.get(ticker, {}).get("v", 0)

    def find_market(self, slug_pfx, interval):
        now_ts = int(time.time())
        cycle_ts = (now_ts // interval) * interval
        slug = f"{slug_pfx}-{cycle_ts}"
        if slug in self._mkt:
            return self._mkt[slug]
        try:
            r = self.s.get(
                f"https://gamma-api.polymarket.com/markets?slug={slug}", timeout=2
            ).json()
            if not r or r[0].get("closed"):
                return None
            ids = json.loads(r[0].get("clobTokenIds", "[]"))
            if len(ids) < 2:
                return None
            m = {
                "slug": slug,
                "cycle_ts": cycle_ts,
                "end_ts": cycle_ts + interval,
                "up_id": ids[0],
                "dn_id": ids[1],
            }
            self._mkt[slug] = m
            self.cache.subscribe([ids[0], ids[1]])
            return m
        except Exception:
            return None

    def purge_cache(self):
        cutoff = int(time.time()) - 700
        stale = [k for k, v in self._mkt.items() if v and v.get("cycle_ts", 0) < cutoff]
        for k in stale:
            del self._mkt[k]


# ══════════════════════════════════════════════════════════════
#  POLYMARKET CLIENT (Web3 + CLOB API)
# ══════════════════════════════════════════════════════════════


class PolyClient:
    def __init__(self):
        self._lock = threading.Lock()
        request_kwargs = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        }
        # 1. Configuration Web3 (Polygon) pour la vraie balance
        self.w3 = Web3(
            Web3.HTTPProvider("https://polygon.drpc.org", request_kwargs=request_kwargs)
        )
        self.usdc_address = self.w3.to_checksum_address(
            "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        )
        self.usdc_abi = json.loads(
            '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]'
        )
        self.usdc_contract = self.w3.eth.contract(
            address=self.usdc_address, abi=self.usdc_abi
        )

        self.wallet_address = self.w3.eth.account.from_key(WALLET_PRIVATE_KEY).address

        # 2. Configuration CLOB (Exécution)
        try:
            from py_clob_client.client import ClobClient
            from py_clob_client.clob_types import ApiCreds

            self._live = ClobClient(
                host="https://clob.polymarket.com",
                chain_id=137,
                key=WALLET_PRIVATE_KEY,
                creds=ApiCreds(
                    POLYMARKET_API_KEY, POLYMARKET_API_SECRET, POLYMARKET_API_PASSPHRASE
                ),
            )
            creds = self._live.derive_api_key()
            self._live.set_api_creds(creds)
            print(
                f"  ✅ Polymarket API Live Prête | Wallet: {self.wallet_address[:6]}...{self.wallet_address[-4:]}"
            )
        except ImportError:
            print("  ❌ pip install py-clob-client web3")
            exit(1)
        except Exception as e:
            print(f"  ❌ Erreur Init CLOB: {e}")
            exit(1)

    def get_real_balance(self):
        """Lit la vraie balance USDC.e sur Polygon."""
        try:
            bal_wei = self.usdc_contract.functions.balanceOf(self.wallet_address).call()
            return bal_wei / 1e6
        except Exception as e:
            logging.error(f"Erreur Web3 Balance: {e}")
            return -1.0

    def post_sell(self, tid, price, size):
        try:
            from py_clob_client.clob_types import OrderArgs, OrderType

            o = self._live.create_order(
                OrderArgs(
                    token_id=tid,
                    price=price,
                    size=size,
                    side="SELL",
                    order_type=OrderType.LIMIT,
                )
            )
            r = self._live.post_order(o)
            return {"success": True, "order_id": r.get("orderID", "")}
        except Exception as e:
            logging.error(f"API post_sell error: {e}")
            return {"success": False}

    def post_both_parallel(self, up_id, dn_id, price, shares):
        results = {}

        def _post(side, tid):
            results[side] = self.post_sell(tid, price, shares)

        t_up = threading.Thread(target=_post, args=("up", up_id))
        t_dn = threading.Thread(target=_post, args=("dn", dn_id))
        t_up.start()
        t_dn.start()
        t_up.join(timeout=3)
        t_dn.join(timeout=3)
        return results.get("up", {"success": False}), results.get(
            "dn", {"success": False}
        )

    def cancel(self, oid):
        try:
            self._live.cancel_order(oid)
        except Exception:
            pass

    def get_status(self, oid):
        try:
            o = self._live.get_order(oid)
            sf = int(float(o.get("size_matched", 0)))
            return o.get("status", "unknown").lower(), o.get("avg_price"), sf
        except Exception:
            return "unknown", None, 0


# ══════════════════════════════════════════════════════════════
#  MAIN BOT
# ══════════════════════════════════════════════════════════════


class Hunter:
    def __init__(self):
        self.book_cache = BookCache()
        self.feed = DataFeed(self.book_cache)
        self.poly = PolyClient()
        self.db = DB()

        print("  🔄 Lecture de la vraie balance depuis Polygon...")
        self.real_bal = self.poly.get_real_balance()
        if self.real_bal < 0:
            print("❌ Impossible de lire la balance (RPC Polygon Error).")
            exit(1)

        self.peak = self.real_bal
        self.halted = False
        self.day = str(datetime.now().date())
        self.open = {}

        self.corr = CorrelationGuard()
        self.fadapt = FillAdaptor()
        self.trend = TrendDetector()
        self.tracker = AssetTracker()

        self.trades = 0
        self.wins = 0
        self.last_stat = 0

    def calc_shares(self):
        risk = min(MAX_RISK_PCT, BASE_RISK_PCT)
        shares = int(
            self.real_bal * risk * self.fadapt.size_mult() / (SPREAD_DEFAULT * 2)
        )
        return max(MIN_SHARES, shares)

    def check_day_reset(self):
        today = str(datetime.now().date())
        if today != self.day:
            self.day = today
            self.peak = self.real_bal
            self.halted = False
            self.feed.purge_cache()

    def check_stop(self):
        if self.halted:
            return True
        if self.real_bal > self.peak:
            self.peak = self.real_bal
        dd = (self.peak - self.real_bal) / self.peak if self.peak else 0
        if dd >= DAILY_STOP_PCT:
            self.halted = True
            print(
                f"\n🛑 STOP LOSS DECLENCHE — Drawdown de {dd:.1%} (Balance actuelle: ${self.real_bal:,.2f})"
            )
            return True
        return False

    def post_maker(self, asset, market, tf):
        key = f"{market['slug']}_{tf}"
        if key in self.open or len(self.open) >= MAX_OPEN_MARKETS:
            return

        up_book = self.feed.cache.get(market["up_id"])
        dn_book = self.feed.cache.get(market["dn_id"])
        up_ask, up_bid = up_book.get("ask"), up_book.get("bid")
        dn_ask, dn_bid = dn_book.get("ask"), dn_book.get("bid")
        if None in (up_ask, up_bid, dn_ask, dn_bid):
            return

        if self.trend.is_trending() or self.corr.is_risky(market["cycle_ts"]):
            return
        if self.tracker.should_skip(asset):
            return
        if self.feed.get_volatility(ASSETS[asset]["ticker"]) > MAX_VOLATILITY_PCT:
            return
        if up_bid < BID_SWEET_MIN or dn_bid < BID_SWEET_MIN:
            return
        if up_bid > BID_SWEET_MAX or dn_bid > BID_SWEET_MAX:
            return

        spread = self.fadapt.adjusted_spread(SPREAD_DEFAULT)
        shares = self.calc_shares()

        up_r, dn_r = self.poly.post_both_parallel(
            market["up_id"], market["dn_id"], spread, shares
        )

        up_oid = up_r.get("order_id") if up_r.get("success") else None
        dn_oid = dn_r.get("order_id") if dn_r.get("success") else None
        if not up_oid and not dn_oid:
            return

        self.open[key] = {
            "strategy": "MAKER",
            "asset": asset,
            "slug": market["slug"],
            "tf": tf,
            "end_ts": market["end_ts"],
            "ticker": ASSETS[asset]["ticker"],
            "shares": shares,
            "spread": spread,
            "up_id": market["up_id"],
            "dn_id": market["dn_id"],
            "up_oid": up_oid,
            "dn_oid": dn_oid,
            "up_shares": 0,
            "dn_shares": 0,
            "posted_at": time.time(),
            "atomic_done": False,
        }
        print(
            f"\n  📤 [{asset.upper()} {tf}] UP/DN posés @ {spread:.3f} | {shares} parts"
        )

    def manage(self):
        now = int(time.time())
        to_close = []

        for key, pos in list(self.open.items()):
            age = time.time() - pos["posted_at"]
            expired = now >= pos["end_ts"]

            up_s, up_fp, up_sf = (
                self.poly.get_status(pos["up_oid"])
                if pos.get("up_oid")
                else ("none", None, 0)
            )
            dn_s, dn_fp, dn_sf = (
                self.poly.get_status(pos["dn_oid"])
                if pos.get("dn_oid")
                else ("none", None, 0)
            )

            if up_sf > 0:
                pos["up_shares"] = up_sf
            if dn_sf > 0:
                pos["dn_shares"] = dn_sf

            up_f = pos["up_shares"] == pos["shares"] or up_s == "filled"
            dn_f = pos["dn_shares"] == pos["shares"] or dn_s == "filled"

            if not pos["atomic_done"] and age >= ATOMIC_CLOSE_SECS:
                if up_f and not dn_f:
                    if pos.get("dn_oid"):
                        self.poly.cancel(pos["dn_oid"])
                    self.trend.record_onesided("UP")
                    print(
                        f"\n  ⚡ KILL SWITCH [{pos['asset'].upper()}] - Annulation DN"
                    )
                elif dn_f and not up_f:
                    if pos.get("up_oid"):
                        self.poly.cancel(pos["up_oid"])
                    self.trend.record_onesided("DN")
                    print(
                        f"\n  ⚡ KILL SWITCH [{pos['asset'].upper()}] - Annulation UP"
                    )
                pos["atomic_done"] = True

            if age > ORDER_CANCEL_SECS and not expired:
                if not up_f and pos.get("up_oid"):
                    self.poly.cancel(pos["up_oid"])
                if not dn_f and pos.get("dn_oid"):
                    self.poly.cancel(pos["dn_oid"])
                if not up_f and not dn_f:
                    to_close.append(key)
                    continue

            if expired:
                self._settle_maker(
                    key,
                    pos,
                    pos["up_shares"] > 0,
                    pos["dn_shares"] > 0,
                    up_fp or pos["spread"],
                    dn_fp or pos["spread"],
                )
                to_close.append(key)

        for k in to_close:
            self.open.pop(k, None)

    def _settle_maker(self, key, pos, up_f, dn_f, up_fp, dn_fp):
        final = self.feed.get_spot(pos["ticker"]) or 0
        strike = self.feed.get_spot(pos["ticker"]) or final
        up_wins = final >= strike

        up_shares = pos.get("up_shares", 0)
        dn_shares = pos.get("dn_shares", 0)

        collected = payout = 0
        if up_f:
            collected += up_fp * up_shares
            if up_wins:
                payout += up_shares
        if dn_f:
            collected += dn_fp * dn_shares
            if not up_wins:
                payout += dn_shares

        profit = collected - (payout * (1 - FEES_RATE))

        if up_f or dn_f:
            current_bal = self.poly.get_real_balance()
            if current_bal > 0:
                self.real_bal = current_bal

            self.trades += 1
            if profit > 0:
                self.wins += 1
            self.fadapt.record(profit > 0)
            self.tracker.record(pos["asset"], profit > 0)

            self.db.log_trade(
                pos["asset"],
                pos["slug"],
                pos["tf"],
                pos["strategy"],
                up_fp if up_f else 0,
                dn_fp if dn_f else 0,
                max(up_shares, dn_shares),
                pos.get("spread", 0),
                collected,
                payout,
                profit,
                self.real_bal,
                "EXPIRED",
            )

            icon = "✅" if profit > 0 else "❌"
            print(
                f"\n  🏁 [{pos['asset'].upper()} {pos['tf']}] {icon} | Balance Phantom: ${self.real_bal:,.2f}"
            )

    def scan(self):
        now = int(time.time())
        for asset, cfg in ASSETS.items():
            for tf, interval, start, end in [
                ("5m", 300, ENTRY_START_5M, ENTRY_END_5M),
                ("15m", 900, ENTRY_START_15M, ENTRY_END_15M),
            ]:
                if not (start <= now % interval <= end):
                    continue
                mkt = self.feed.find_market(cfg[f"slug_{tf}"], interval)
                if mkt:
                    self.post_maker(asset, mkt, tf)

    def print_stats(self, force=False):
        now = time.time()
        if not force and now - self.last_stat < 180:
            return
        self.last_stat = now
        wr = self.wins / self.trades if self.trades else 0
        dd = (self.peak - self.real_bal) / self.peak if self.peak else 0
        ws_status = (
            "🔌 WS live"
            if (
                WS_AVAILABLE
                and hasattr(self.book_cache, "_ws_ok")
                and self.book_cache._ws_ok
            )
            else "📡 REST"
        )
        print(f"\n{'═' * 62}")
        print(f"  🏆 HUNTER ULTIMATE | 🟢 ON-CHAIN PRODUCTION | {ws_status}")
        print(f"  Vraie Balance: ${self.real_bal:,.2f} USDC.e (Phantom)")
        print(f"  Trades: {self.trades} | WinRate: {wr:.0%} | DD: {dd:.1%}")
        print(f"{'═' * 62}")

    def run(self):
        print("═" * 62)
        print("  🏆 HUNTER ULTIMATE - OPENCLAW ON-CHAIN SKILL")
        print(f"  Balance LUE: ${self.real_bal:,.2f} USDC.e")
        print("═" * 62)
        time.sleep(3)

        while True:
            try:
                bal_check = self.poly.get_real_balance()
                if bal_check > 0:
                    self.real_bal = bal_check

                self.check_day_reset()
                if self.check_stop():
                    time.sleep(30)
                    continue

                self.manage()
                self.scan()
                self.print_stats()

                wr = self.wins / self.trades if self.trades else 0
                next5 = 300 - (int(time.time()) % 300)
                print(
                    f"\r  ⏳{next5:3d}s | Phantom: ${self.real_bal:,.2f} | T:{self.trades} WR:{wr:.0%} | Pos:{len(self.open)}    ",
                    end="",
                    flush=True,
                )
            except KeyboardInterrupt:
                self.book_cache.stop()
                break
            except Exception as e:
                logging.error(f"Erreur Boucle: {e}")
            time.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hunter Ultimate - Production Skill")
    parser.add_argument("action", choices=["start"], help="Start the continuous bot")
    args = parser.parse_args()

    if args.action == "start":
        bot = Hunter()
        bot.run()
