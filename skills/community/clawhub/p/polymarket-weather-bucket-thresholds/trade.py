import os
import argparse
import requests
import time

SKILL_SLUG = "polymarket-weather-bucket-thresholds"  # must match ClawHub slug exactly
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"

BASE_URL = "https://api.simmer.markets"

ENTRY_THRESHOLD = 0.15
EXIT_THRESHOLD = 0.45

DEFAULT_ENTRY_AMOUNT = 1.80  # keep under $2 cap after LMSR movement
MAX_TRADES_PER_SCAN = 5
STRICT_WARNINGS = True


def headers():
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        raise SystemExit("Missing SIMMER_API_KEY in environment.")
    return {"Authorization": f"Bearer {api_key}"}


def get_markets(q: str, limit: int = 200):
    url = f"{BASE_URL}/api/sdk/markets"
    r = requests.get(
        url,
        headers=headers(),
        params={"status": "active", "q": q, "limit": limit},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("markets", [])


def get_context(market_id: str, retries: int = 3, backoff_s: float = 2.0):
    url = f"{BASE_URL}/api/sdk/context/{market_id}"
    for attempt in range(retries):
        r = requests.get(url, headers=headers(), timeout=30)
        if r.status_code == 429:
            time.sleep(backoff_s * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()
    return {"warnings": ["Rate limited on context (429) — skipping market this scan."]}


def get_positions_sim():
    url = f"{BASE_URL}/api/sdk/positions"
    r = requests.get(url, headers=headers(), params={"venue": "sim"}, timeout=30)
    r.raise_for_status()
    return r.json()


def trade(
    market_id: str,
    side: str,
    *,
    action: str,
    venue: str,
    amount: float = 0.0,
    shares: float = 0.0,
    reasoning: str,
    live: bool,
):
    payload = {
        "market_id": market_id,
        "side": side,
        "action": action,
        "venue": venue,
        "source": TRADE_SOURCE,
        "skill_slug": SKILL_SLUG,
        "reasoning": reasoning,
    }
    if shares and shares > 0:
        payload["shares"] = float(shares)
    else:
        payload["amount"] = float(amount)

    if not live:
        print(f"DRY_RUN trade payload: {payload}")
        return {"dry_run": True, "payload": payload}

    url = f"{BASE_URL}/api/sdk/trade"
    r = requests.post(
        url,
        headers={**headers(), "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def has_blocking_warnings(ctx: dict) -> bool:
    w = ctx.get("warnings") or []
    if isinstance(w, dict):
        w = list(w.values())
    if not w:
        return False
    text = " | ".join(map(str, w)).lower()
    blocking = ["high urgency", "wide spread", "elevated risk"]
    return any(b in text for b in blocking)


def market_prob(m: dict):
    p = m.get("current_probability")
    try:
        return float(p) if p is not None else None
    except Exception:
        return None


def is_weatherish(question: str) -> bool:
    q = (question or "").lower()
    return any(
        k in q
        for k in [
            "temperature",
            "temp",
            "highest temperature",
            "high temp",
            "°",
            "precip",
            "precipitation",
            "rain",
            "snow",
        ]
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="Place real trades (default: dry-run)")
    ap.add_argument("--max-trades", type=int, default=MAX_TRADES_PER_SCAN)
    ap.add_argument("--entry-amount", type=float, default=DEFAULT_ENTRY_AMOUNT)
    ap.add_argument("--query", default="temperature", help="Market search query (default: temperature)")
    ap.add_argument("--strict-warnings", action="store_true", default=STRICT_WARNINGS)
    args = ap.parse_args()

    live = args.live

    # Exit pass
    pos = get_positions_sim()
    positions = pos.get("positions", [])
    exits_done = 0

    for p in positions:
        mid = p.get("market_id")
        prob = p.get("current_probability")
        shares_yes = p.get("shares_yes", 0.0)
        try:
            prob = float(prob) if prob is not None else None
            shares_yes = float(shares_yes) if shares_yes is not None else 0.0
        except Exception:
            continue

        if mid and shares_yes > 0 and prob is not None and prob >= EXIT_THRESHOLD:
            ctx = get_context(mid)
            if args.strict_warnings and has_blocking_warnings(ctx):
                print(f"Skip EXIT due to warnings: {mid} warnings={ctx.get('warnings')}")
                continue
            reasoning = f"Exit: prob {prob:.0%} >= {EXIT_THRESHOLD:.0%}. Selling entire YES position."
            res = trade(
                mid,
                "yes",
                action="sell",
                venue="sim",
                shares=shares_yes,
                reasoning=reasoning,
                live=live,
            )
            print("EXIT result:", res)
            exits_done += 1

    # Entry pass
    trades_done = 0
    markets = get_markets(args.query, limit=200)

    scored = []
    for m in markets:
        p = market_prob(m)
        if p is None:
            continue
        if p < ENTRY_THRESHOLD:
            scored.append((p, m))

    scored.sort(key=lambda x: x[0])
    candidates = [m for _, m in scored[:75]]

    for m in candidates:
        if trades_done >= args.max_trades:
            break

        mid = m.get("id")
        prob = market_prob(m)
        if not mid or prob is None:
            continue

        question = m.get("question", "")
        if not is_weatherish(question):
            continue

        ctx = get_context(mid)
        if args.strict_warnings and has_blocking_warnings(ctx):
            continue

        reasoning = f"Entry: prob {prob:.0%} < {ENTRY_THRESHOLD:.0%}. Small YES buy with explicit reasoning."
        res = trade(
            mid,
            "yes",
            action="buy",
            venue="sim",
            amount=args.entry_amount,
            reasoning=reasoning,
            live=live,
        )
        print(f"ENTRY {mid} prob={prob:.0%} :: {question}")
        print("ENTRY result:", res)
        trades_done += 1

    print(f"Done. exits_done={exits_done} entries_done={trades_done} live={live}")


if __name__ == "__main__":
    main()
