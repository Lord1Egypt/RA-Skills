#!/usr/bin/env python3
"""
Ondo Perps Points Estimator — Points 收益预估器
─────────────────────────────────────────────
跟踪你的交易量和 Points 发放，自动校准 pts/$1M ratio。
"""
import json, os, time, hashlib, hmac, logging
from datetime import datetime, timezone
from typing import Optional
import requests

log = logging.getLogger("pts-est")

# ═══════ 配置 ══════════════════════════════════════════════════════
# 和 farmer.py 使用相同的 API Key
ONDO_KEY_ID = os.environ.get("ONDO_KEY_ID", "ondoKeyId_YOUR_KEY_ID_HERE")
ONDO_API_SECRET = os.environ.get("ONDO_API_SECRET", "ondoApiSecret_YOUR_SECRET_HERE")
API_BASE = "https://api.ondoperps.xyz"
STATE_FILE = os.path.expanduser("~/.ondo_points_state.json")
# ═══════════════════════════════════════════════════════════════════

def _sign(method: str, path: str, body: str = "") -> dict:
    ts = str(int(time.time() * 1000))
    msg = ts + method.upper() + path + body
    return {
        "ONDO-KEY-ID": ONDO_KEY_ID,
        "ONDO-TIMESTAMP": ts,
        "ONDO-SIGN": hmac.new(ONDO_API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest(),
        "Content-Type": "application/json",
    }

def _get(path: str) -> dict:
    r = requests.get(API_BASE + path, headers=_sign("GET", path), timeout=15)
    r.raise_for_status()
    return r.json()

# ─── 状态管理 ──────────────────────────────────────────────────────

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except: pass
    return {
        "known_ratio": None,
        "ratio_history": [],
        "points_drops": [],
        "last_points": 0,
        "last_volume": 0,
        "last_check": None,
    }

def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_FILE) or ".", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

# ─── 数据采集 ──────────────────────────────────────────────────────

def fetch_current() -> dict:
    s = _get("/v1/portfolio/summary")["result"]
    return {
        "points": int(s.get("points", 0)),
        "volumeAllTime": float(s.get("volumeAllTime", 0)),
        "volume7d": float(s.get("volume7d", 0)),
    }

def check_update():
    """
    检查 Points 是否有更新。应每 5-10 分钟调用一次。
    检测到新 Points 发放时，自动计算 pts/$1M ratio。
    """
    state = load_state()
    cur = fetch_current()
    pts = cur["points"]
    vol = cur["volumeAllTime"]

    if state["last_points"] is None:
        state["last_points"] = pts
        state["last_volume"] = vol
        save_state(state)
        return {"updated": False}

    gain = pts - state["last_points"]
    vol_gain = vol - state["last_volume"]

    if gain > 0 and vol_gain > 0:
        ratio = gain / (vol_gain / 1_000_000)
        drop = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "points": gain,
            "volume": vol_gain,
            "ratio": round(ratio, 2),
        }
        state["points_drops"].append(drop)
        state["known_ratio"] = round(ratio, 2)
        state["ratio_history"].append(round(ratio, 2))
        state["last_points"] = pts
        state["last_volume"] = vol
        save_state(state)
        log.info(f"📈 Points! +{gain:,} | vol={vol_gain:,.0f} | ratio={ratio:.2f}/$1M")
        return {"updated": True, "new_points": gain, "ratio": round(ratio, 2)}
    else:
        state["last_points"] = pts
        state["last_volume"] = vol
        save_state(state)
        return {"updated": False}

def estimate(weekly_target: float = 500_000, confidence: str = "moderate") -> dict:
    """预估每周 Points"""
    state = load_state()

    if state["known_ratio"]:
        ratios = state["ratio_history"]
        mul = {"conservative": 0.8, "moderate": 1.0, "aggressive": 1.5}
        ratio = (sum(ratios) / len(ratios)) * mul.get(confidence, 1.0)
        pts = weekly_target / 1_000_000 * ratio
        return {"ratio": round(ratio, 2), "weekly": round(pts), "monthly": round(pts * 4.33),
                "method": "historical", "drops": len(state["points_drops"])}
    else:
        # 首次发放前：Leaderboard 粗估
        est_ratio = {"conservative": 500, "moderate": 2000, "aggressive": 5000}
        ratio = est_ratio.get(confidence, 2000)
        pts = weekly_target / 1_000_000 * ratio
        return {"ratio": ratio, "weekly": round(pts), "monthly": round(pts * 4.33),
                "method": "leaderboard_estimate", "drops": 0}

def print_report(weekly_target: float = 500_000, confidence: str = "moderate"):
    state = load_state()
    cur = fetch_current()
    est = estimate(weekly_target, confidence)

    print("=" * 58)
    print("  🪙  Ondo Points 收益预测")
    print("=" * 58)
    print(f"\n📊 当前")
    print(f"   Points:    {cur['points']:>8,}")
    print(f"   7天交易量: ${cur['volume7d']:>10,.0f}")
    print(f"   累计交易量: ${cur['volumeAllTime']:>10,.0f}")

    if state["known_ratio"]:
        print(f"\n📈 校准数据")
        print(f"   Ratio:     {state['known_ratio']:>8.2f} pts/$1M")
        print(f"   发放次数:  {len(state['points_drops'])}")
        for d in state["points_drops"][-3:]:
            print(f"   📅 +{d['points']:>6,} pts  (vol {d['volume']:>8,.0f})")

    print(f"\n🎯 {confidence}")
    print(f"   周目标:    ${weekly_target:>10,.0f}")
    print(f"   预计 pts:  {est['weekly']:>8,}/周 → {est['monthly']:>8,}/月")
    print(f"   Ratio:     {est['ratio']:>8,.0f} pts/$1M")

    print(f"\n📋 场景对比")
    for c in ["conservative", "moderate", "aggressive"]:
        e = estimate(weekly_target, c)
        print(f"   {c:12s}: {e['weekly']:>8,} pts/周")

    print(f"\n🎯 目标所需量")
    for goal in [10000, 50000, 100000]:
        r = state["known_ratio"] or est["ratio"]
        if r > 0:
            req = goal / r * 1_000_000
            print(f"   {goal:>6,} pts/月 → ${req*4.33:>10,.0f}/月")

    if not state["known_ratio"]:
        print(f"\n💡 首次 Points 发放后将自动校准，Ratio 会更准。")
        print(f"   运行 python3 -c 'from points_estimator import check_update; check_update()'")
    print("=" * 58)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--weekly-vol", type=float, default=500_000)
    parser.add_argument("--confidence", choices=["conservative", "moderate", "aggressive"], default="moderate")
    parser.add_argument("--watch", action="store_true", help="持续监控")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    if args.watch:
        print("🔄 监控 Points 发放中（每 60 秒检查）...")
        try:
            while True:
                r = check_update()
                if r["updated"]:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✅ +{r['new_points']:,} pts!")
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n停止监控")

    print_report(args.weekly_vol, args.confidence)
