#!/usr/bin/env python3
"""
Ondo Perps Points Farmer — 自动化交易工具
───────────────────────────────────────────
适合新手开箱即用。只需设置 API Key 和存入 USDC。
"""
import hashlib, hmac, time, json, os, sys, logging, random
from datetime import datetime, timezone, timedelta
from typing import Optional
import requests

# 注册邀请链接（可选）
REFERRAL_LINK = "https://app.ondoperps.xyz/?ref=8RU3VB"

# ═══════ 配置（新手从这里改）═══════════════════════════════════════
# 方法1：设置环境变量（推荐）
#   export ONDO_KEY_ID="ondoKeyId_你的key_id"
#   export ONDO_API_SECRET="ondoApiSecret_你的secret"
# 方法2：直接修改下面两行的字符串

ONDO_KEY_ID = os.environ.get("ONDO_KEY_ID", "ondoKeyId_YOUR_KEY_ID_HERE")
ONDO_API_SECRET = os.environ.get("ONDO_API_SECRET", "ondoApiSecret_YOUR_SECRET_HERE")
API_BASE = "https://api.ondoperps.xyz"

# 交易参数
LIQUID_MKTS = ["BTC-USD.P", "ETH-USD.P", "SPY-USD.P", "HOOD-USD.P", "AAPL-USD.P",
               "NVDA-USD.P", "TSLA-USD.P", "QQQ-USD.P", "AMZN-USD.P", "MSFT-USD.P"]
SZ_USD = float(os.environ.get("ONDO_POSITION_SIZE", "50"))      # 每轮名义仓位（$）
MAX_CYCLES = int(os.environ.get("ONDO_MAX_CYCLES", "200"))       # 最大轮次
MIN_WITHDRAW = float(os.environ.get("ONDO_MIN_WITHDRAW", "5"))   # 自动提现阈值

# 执行参数（随机化，不用改）
MIN_DELAY, MAX_DELAY = 5, 30      # 交易间隔（秒）
SZ_JITTER = 0.30                  # 仓位调节比例
HOLD_PROB = 0.10                  # 持仓延迟概率
HOLD_MIN, HOLD_MAX = 60, 300     # 延迟范围（秒）
NOISE_PROB = 0.05                 # 分散交易概率
REV_PROB = 0.50                   # 方向随机概率

# ═══════ 结束配置 ═══════════════════════════════════════════════════

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger("ondo")

# 自动检测市场状态
_et = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-4)))
_is_mh = (_et.weekday() < 5 and 9.5 <= _et.hour + _et.minute / 60 < 16)
ACTIVE = LIQUID_MKTS if _is_mh else ["BTC-USD.P", "ETH-USD.P"]

# ─── API 签名 ──────────────────────────────────────────────────────

def _sign(method: str, path: str, body: str = "") -> dict:
    ts = str(int(time.time() * 1000))
    msg = ts + method.upper() + path + body
    return {"ONDO-KEY-ID": ONDO_KEY_ID, "ONDO-TIMESTAMP": ts,
            "ONDO-SIGN": hmac.new(ONDO_API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest(),
            "Content-Type": "application/json"}

def _get(path: str) -> dict:
    r = requests.get(API_BASE + path, headers=_sign("GET", path), timeout=15)
    r.raise_for_status(); return r.json()

def _post(path: str, data: dict) -> dict:
    body = json.dumps(data)
    r = requests.post(API_BASE + path, headers=_sign("POST", path, body), data=body, timeout=15)
    if r.status_code != 200:
        log.warning(f"POST {path}: {r.status_code} {r.text[:150]}")
    r.raise_for_status(); return r.json()

def _delete(path: str):
    try:
        requests.delete(API_BASE + path, headers=_sign("DELETE", path), timeout=15)
    except:
        pass

# ─── 工具函数 ──────────────────────────────────────────────────────

def balance() -> dict: return _get("/v1/perps/balance")["result"]
def summary() -> dict: return _get("/v1/portfolio/summary")["result"]
def mark_price(market: str) -> float:
    return float(_get(f"/v1/perps/mark_prices?markets={market}")["result"][market]["markPrice"])

def pick_market() -> str:
    """加权随机选市场，盘后自动限制 BTC/ETH"""
    weights = [len(ACTIVE) - i for i in range(len(ACTIVE))]
    return random.choices(ACTIVE, weights=weights, k=1)[0]

def calc_size(base_usd: float, price: float) -> float:
    """计算仓位大小，带 ±30% 随机调节"""
    raw = (base_usd * random.uniform(1 - SZ_JITTER, 1 + SZ_JITTER)) / price
    return round(max(raw, 0.001), 3)

def market_order(market: str, side: str, size: float) -> Optional[dict]:
    """市价单，保证成交"""
    r = _post("/v1/perps/orders", {"market": market, "side": side, "type": "market", "size": str(size)})
    res = r["result"]
    if res.get("status") in ("filled", "fullyfilled"):
        cost = float(res.get("filledCost", 0))
        fee = float(res.get("fee", 0))
        log.info(f"  ✓ {side:4s} {market} ${cost:.2f} 费=${fee:.4f}")
        return res
    log.warning(f"  ✗ {side} failed: {res.get('status')}")
    return None

def do_flip(market: str, size: float, buy_first: bool) -> dict:
    """一轮 flip：先买后卖 或 先卖后买"""
    result = {"vol": 0.0, "fee": 0.0}
    side1, side2 = ("buy", "sell") if buy_first else ("sell", "buy")

    f1 = market_order(market, side1, size)
    if not f1: return result
    result["vol"] += float(f1.get("filledCost", 0))
    result["fee"] += float(f1.get("fee", 0))

    # 持仓延迟（随机化用）
    if random.random() < HOLD_PROB:
        hold = random.uniform(HOLD_MIN, HOLD_MAX)
        log.info(f"  💤 {hold:.0f}s hold (随机化)")
        time.sleep(hold)

    f2 = market_order(market, side2, size)
    if not f2: return result
    result["vol"] += float(f2.get("filledCost", 0))
    result["fee"] += float(f2.get("fee", 0))

    return result

# ─── Points 预估集成 ──────────────────────────────────────────────

try:
    from points_estimator import check_update as check_points_update, estimate as estimate_weekly_points
    HAS_EST = True
except ImportError:
    HAS_EST = False

PTS_CHECK_INTERVAL = 20

def log_estimate(vol: float, elapsed_min: float):
    if not HAS_EST or vol <= 0 or elapsed_min <= 0: return
    proj = vol / elapsed_min * 60 * 24 * 7
    est = estimate_weekly_points(proj)
    note = " [粗估]" if est.get("method", "") == "leaderboard_estimate" else ""
    log.info(f"  🔮 预估: {est['weekly']:,} pts/周 | {est['monthly']:,} pts/月{note}")

# ═══════ 主程序 ═══════════════════════════════════════════════════

def main():
    n = int(MAX_CYCLES * random.uniform(0.8, 1.0))
    bal = balance()
    summ = summary()
    pts0 = summ["points"]
    start = time.time()
    check_ctr = 0

    log.info("=" * 60)
    log.info("Ondo Points Farmer  🪙")
    log.info("=" * 60)
    log.info(f"🔗 注册链接: {REFERRAL_LINK}")
    log.info(f"余额: ${float(bal['walletBalance']):.2f} | Points: {pts0}")
    log.info(f"计划: {n} 轮 | 市场: {len(ACTIVE)} 个{' (盘后模式)' if not _is_mh else ''}")
    log.info(f"仓位: ~${SZ_USD}/轮 | 每轮成本: ~${SZ_USD * 0.001:.4f}")
    if HAS_EST:
        est = estimate_weekly_points(500_000)
        log.info(f"🔮 预估(周$500K): {est['est_weekly_points']:,} pts/周")
    log.info("=" * 60)

    stats = {"n": 0, "vol": 0.0, "fee": 0.0}

    try:
        for i in range(1, n + 1):
            log.info(f"\n{'─'*40}\n#{i}/{n}")

            market = pick_market()
            px = mark_price(market)
            size = calc_size(SZ_USD, px)
            bf = random.random() >= REV_PROB
            log.info(f"  {market} {'📈 先买' if bf else '📉 先卖'} sz={size:.4f} (~${size*px:.1f})")

            # 分散交易（5%概率）
            if random.random() < NOISE_PROB:
                nm = random.choice(ACTIVE)
                ns = calc_size(5, mark_price(nm))
                ns_side = random.choice(["buy", "sell"])
                r = _post("/v1/perps/orders", {"market": nm, "side": ns_side, "type": "market", "size": str(ns)})
                oid = r["result"].get("orderId", "")
                log.info(f"  ~ 🎲 分散 {nm} {ns_side} {ns:.4f}")
                if oid:
                    time.sleep(1)
                    _post("/v1/perps/orders", {"market": nm,
                        "side": ("sell" if ns_side == "buy" else "buy"),
                        "type": "market", "size": str(ns)})

            r = do_flip(market, size, bf)
            stats["n"] += 1
            stats["vol"] += r["vol"]
            stats["fee"] += r["fee"]

            if i % 5 == 0 or r["vol"] == 0:
                sp = summary()
                elapsed = (time.time() - start) / 60
                log.info(f"  📊 量=${stats['vol']:.0f} | 费=${stats['fee']:.4f} | Pts: +{sp['points'] - pts0}")
                if stats["vol"]:
                    log.info(f"  💰 每百万成本: ${(stats['fee']/stats['vol'])*1_000_000:.2f}")
                if i % 10 == 0:
                    log_estimate(stats["vol"], elapsed)

            # 定时检查 Points 发放
            check_ctr += 1
            if HAS_EST and check_ctr >= PTS_CHECK_INTERVAL:
                check_ctr = 0
                try:
                    upd = check_points_update()
                    if upd["updated"]:
                        log.info(f"  🎉 Points 发放! +{upd['new_points']:,} pts (ratio: {upd['ratio']} pts/$1M)")
                except:
                    pass

            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

    except KeyboardInterrupt:
        log.info("🛑 手动中断")
    except Exception as e:
        log.error(f"❌ 错误: {e}")
        import traceback; traceback.print_exc()
    finally:
        # 清仓
        for m in ACTIVE:
            _delete(f"/v1/perps/orders?market={m}")
        sp = summary()
        bp = balance()
        elapsed = (time.time() - start) / 60
        log.info("\n" + "=" * 60)
        log.info(f"✅ 完成 {stats['n']} 轮 | 量=${stats['vol']:.0f} | 费=${stats['fee']:.4f}")
        log.info(f"⏱️  {elapsed:.1f} 分钟 | 速度: ${stats['vol']/elapsed:,.0f}/分钟")
        log.info(f"🪙 Points: +{sp['points'] - pts0} (共{sp['points']})")
        log.info(f"💰 余额: ${float(bp['walletBalance']):.2f}")
        if stats['vol']:
            cpm = (stats['fee']/stats['vol'])*1_000_000
            log.info(f"💳 每百万成本: ${cpm:.2f}")
        log.info("=" * 60)

if __name__ == "__main__":
    main()
