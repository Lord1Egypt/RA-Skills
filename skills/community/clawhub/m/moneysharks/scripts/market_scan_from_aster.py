#!/usr/bin/env python3
"""
Full market scan using real Aster DEX data.
Fetches multi-timeframe klines, computes technical features, runs signal + confluence.

usage: market_scan_from_aster.py <config.json> <symbol> [--existing-position-side BUY|SELL]
"""
import json
import subprocess
import sys
from pathlib import Path


def run_json(args: list, stdin_obj=None, check: bool = True) -> dict:
    proc = subprocess.run(
        args,
        input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode not in (0, 1):
        raise RuntimeError(f"subprocess failed ({proc.returncode}): {proc.stderr.decode()[:400]}")
    return json.loads(proc.stdout.decode())


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: market_scan_from_aster.py <config.json> <symbol>", file=sys.stderr)
        return 2

    base = Path(__file__).resolve().parent
    config = json.loads(Path(sys.argv[1]).read_text())
    symbol = sys.argv[2]

    # ── 1. Fetch market bundle (multi-TF klines + ticker + mark price) ──
    try:
        market_bundle = run_json(
            [sys.executable, str(base / "aster_readonly_client.py"), "market_bundle", symbol]
        )
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"market_fetch_failed: {e}"}))
        return 1

    klines_1h = market_bundle.get("klines_1h", [])
    klines_4h = market_bundle.get("klines_4h", [])
    klines_5m = market_bundle.get("klines_5m", [])
    mark = market_bundle.get("mark_price", {})
    funding_rate = mark.get("lastFundingRate")
    last_price = float(market_bundle["ticker"].get("price", 0))

    # ── 2. Fetch account bundle ──
    try:
        account_bundle = run_json(
            [sys.executable, str(base / "aster_readonly_client.py"), "account", symbol]
        )
    except Exception as e:
        account_bundle = {"account": {}, "positions": [], "orders": []}

    account = account_bundle.get("account", {})
    positions = account_bundle.get("positions", [])
    orders = account_bundle.get("orders", [])

    # Equity and margins
    equity = float(account.get("totalWalletBalance") or account.get("equity") or 0)
    avail_margin = float(account.get("availableBalance") or account.get("available_margin") or equity)
    total_exposure = sum(
        abs(float(p.get("notional") or p.get("positionAmt", 0))) for p in positions
    )

    # Find existing position for this symbol
    existing_position = None
    for p in positions:
        if p.get("symbol") == symbol:
            amt = float(p.get("positionAmt", 0))
            if abs(amt) > 0:
                upnl = float(p.get("unRealizedProfit", 0))
                entry_price = float(p.get("entryPrice", 0))
                pnl_pct = (upnl / (entry_price * abs(amt))) if entry_price and amt else 0
                existing_position = {
                    "symbol": symbol,
                    "side": "BUY" if amt > 0 else "SELL",
                    "quantity": abs(amt),
                    "entry_price": entry_price,
                    "unrealised_pnl": upnl,
                    "unrealised_pnl_pct": pnl_pct,
                }
            break

    # ── 3. Compute features on each timeframe ──
    def features(klines: list, fr=None) -> dict:
        if not klines:
            return {}
        return run_json(
            [sys.executable, str(base / "compute_features.py")],
            {"klines": klines, "funding_rate": fr},
        )

    f1h = features(klines_1h, funding_rate)
    f4h = features(klines_4h)
    f5m = features(klines_5m)

    # ── 4. Compute signal ──
    signal_result = run_json(
        [sys.executable, str(base / "compute_signal.py")],
        {
            "features_1h": f1h,
            "features_4h": f4h,
            "features_5m": f5m,
            "allow_short": config.get("allow_short", True),
            "position": existing_position,
        },
    )
    signal = signal_result.get("signal", "wait")
    signal_confidence = float(signal_result.get("confidence", 0))

    # ── 5. Compute stop/target for confluence evaluation ──
    atr_val = f1h.get("atr14") or 0
    entry_price = last_price
    is_long = signal == "long"
    is_short = signal == "short"

    if atr_val:
        stop_loss = entry_price - (1.5 * atr_val) if is_long else entry_price + (1.5 * atr_val)
        take_profit = entry_price + (2.5 * atr_val) if is_long else entry_price - (2.5 * atr_val)
    else:
        stop_loss = entry_price * 0.985 if is_long else entry_price * 1.015
        take_profit = entry_price * 1.025 if is_long else entry_price * 0.975

    # ── 6. Compute confluence ──
    confluence_result = run_json(
        [sys.executable, str(base / "compute_confluence.py")],
        {
            "signal": signal,
            "features_1h": f1h,
            "features_4h": f4h,
            "entry": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "min_reward_risk": config.get("min_reward_risk", 1.5),
            "max_concurrent_positions": config.get("max_concurrent_positions", 3),
            "current_positions": len([p for p in positions if abs(float(p.get("positionAmt", 0))) > 0]),
            "max_total_exposure": config.get("max_total_exposure", 0),
            "current_exposure": total_exposure,
        },
    )
    confidence = float(confluence_result.get("confidence", 0))

    # ── 7. Compute recommended leverage ──
    leverage_result = run_json(
        [sys.executable, str(base / "recommend_leverage.py")],
        {
            "min_leverage": config.get("min_leverage", 1),
            "max_leverage": config.get("max_leverage", 3),
            "confidence": confidence,
            "high_volatility": f1h.get("high_volatility", False),
        },
    )
    leverage = int(leverage_result.get("recommended_leverage", config.get("min_leverage", 1)))

    # ── 8. Compute position size ──
    risk_pct = float(config.get("risk_pct_per_trade", 0.01))  # default 1% risk per trade
    size_result = run_json(
        [sys.executable, str(base / "size_position.py")],
        {
            "equity": equity,
            "risk_pct": risk_pct,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "leverage": leverage,
        },
    )
    quantity = float(size_result.get("quantity", 0))
    notional = float(size_result.get("notional", 0))

    # Cap at max notional per trade
    max_notional = float(config.get("max_notional_per_trade", 0))
    if max_notional and notional > max_notional:
        scale = max_notional / notional
        quantity *= scale
        notional *= scale

    # ── 9. Round quantity and prices to exchange precision ──
    try:
        sys.path.insert(0, str(base))
        from aster_readonly_client import round_quantity, round_price, get_symbol_filters
        quantity = round_quantity(symbol, quantity)
        stop_loss = round_price(symbol, stop_loss)
        take_profit = round_price(symbol, take_profit)
        # Verify minimum notional
        filters = get_symbol_filters(symbol)
        min_notional = filters.get("min_notional", 5)
        if quantity * entry_price < min_notional:
            signal = "wait"  # Position too small for exchange
    except Exception:
        pass  # If exchange info unavailable, proceed with unrounded (API will reject if wrong)

    # ── 10. Liquidity check from order book ──
    depth = market_bundle.get("depth", {})
    bids = depth.get("bids", [])
    asks = depth.get("asks", [])
    bid_liquidity = sum(float(b[1]) * float(b[0]) for b in bids[:5]) if bids else 0
    ask_liquidity = sum(float(a[1]) * float(a[0]) for a in asks[:5]) if asks else 0
    total_book_liquidity = bid_liquidity + ask_liquidity
    liquidity_ok = True
    if notional > 0 and total_book_liquidity > 0:
        # If our order is > 10% of visible top-5 book, flag low liquidity
        if notional > total_book_liquidity * 0.10:
            liquidity_ok = False

    output = {
        "symbol": symbol,
        "mode": config.get("mode", "paper"),
        "timestamp": market_bundle.get("fetched_at"),
        "market": {
            "last_price": last_price,
            "mark_price": float(mark.get("markPrice", last_price) or last_price),
            "funding_rate": float(funding_rate or 0),
        },
        "account": {
            "equity": equity,
            "available_margin": avail_margin,
            "total_exposure": total_exposure,
            "positions_count": len([p for p in positions if abs(float(p.get("positionAmt", 0))) > 0]),
        },
        "existing_position": existing_position,
        "features_1h": f1h,
        "features_4h": f4h,
        "signal": signal,
        "signal_reason": signal_result.get("reason", ""),
        "signal_confidence": signal_confidence,
        "confluence": confluence_result,
        "confidence": confidence,
        "order": {
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "leverage": leverage,
            "quantity": quantity,
            "notional": notional,
            "side": "BUY" if is_long else ("SELL" if is_short else None),
        } if signal in ("long", "short") else None,
        "liquidity": {
            "bid_liquidity_usd": bid_liquidity,
            "ask_liquidity_usd": ask_liquidity,
            "liquidity_ok": liquidity_ok,
        },
    }

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
