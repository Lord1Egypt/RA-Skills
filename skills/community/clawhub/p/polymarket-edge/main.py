"""
Polymarket Edge — Skill entrypoint
════════════════════════════════════════
Monetised via SkillPay.me (1 token = 0.001 USDT per call)

Routes
──────
GET  /                         health check (free)
GET  /balance?user_id=         check SkillPay token balance (free)
GET  /topup?user_id=           get USDC top-up link (free)

GET  /markets/search?q=        search any Polymarket market   [1 token]
GET  /markets/btc              list active BTC markets         [1 token]
GET  /market/{id}              get a single market by ID       [1 token]
GET  /market/{id}/book         full order book                 [1 token]
GET  /market/{id}/price        mid-price + spread              [1 token]
GET  /market/{id}/history      5-min price history             [1 token]

POST /signal                   run strategy signal on BTC mkts [1 token]
GET  /autotrader/status        is auto-trader running?         [1 token]
POST /autotrader/start         start 5-min BTC auto-trader     [1 token]
POST /autotrader/stop          stop auto-trader                [1 token]
GET  /autotrader/log           last 50 trade log entries       [1 token]

POST /portfolio?wallet=        view open positions             [1 token]
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Query, Path, BackgroundTasks
from fastapi.responses import JSONResponse

import billing
import polymarket_client as pm
import strategy as strat
from strategy import StrategyConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
log = logging.getLogger("main")


# ── App lifecycle ─────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Polymarket Edge skill started.")
    yield
    strat.stop_auto_trader()
    log.info("Skill shut down.")


app = FastAPI(
    title="Polymarket Edge",
    description=(
        "AI skill for Polymarket prediction market trading. "
        "Powered by SkillPay.me — each API call costs 1 token (0.001 USDT)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _charge_or_reject(user_id: str) -> Optional[JSONResponse]:
    """Charge 1 token. Return 402 response if balance is zero."""
    result = await billing.charge_user(user_id)
    if not result.ok:
        return JSONResponse(
            status_code=402,
            content={
                "error": "Insufficient SkillPay tokens",
                "balance": result.balance,
                "top_up_url": result.payment_url,
                "message": "Top up with USDT on BNB Chain. 8 USDT = 8000 calls.",
            },
        )
    return None


# ── Free routes ───────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def health():
    return {
        "skill": "Polymarket Edge",
        "status": "ok",
        "billing": "SkillPay.me — 1 token per call",
        "auto_trader_running": strat.is_running(),
    }


@app.get("/balance", tags=["Billing"])
async def get_balance(user_id: str = Query(..., description="Your SkillPay user ID")):
    balance = await billing.get_balance(user_id)
    return {"user_id": user_id, "balance": balance, "unit": "tokens", "usdt_equivalent": balance / 1000}


@app.get("/topup", tags=["Billing"])
async def get_topup_link(
    user_id: str = Query(...),
    amount: float = Query(8.0, description="USDT amount to top up (min 8)"),
):
    url = await billing.get_payment_link(user_id, amount)
    return {"payment_url": url, "amount_usdt": amount, "tokens_received": int(amount * 1000)}


# ── Market data (billed) ──────────────────────────────────────────────────────

@app.get("/markets/search", tags=["Markets"])
async def search_markets(
    q: str = Query(..., description="Search keyword"),
    limit: int = Query(10, ge=1, le=50),
    user_id: str = Query(...),
):
    if err := await _charge_or_reject(user_id):
        return err
    markets = await pm.search_markets(q, limit)
    return {
        "query": q,
        "count": len(markets),
        "markets": [
            {
                "id": m.id,
                "question": m.question,
                "slug": m.slug,
                "yes_price": m.outcome_prices[0] if m.outcome_prices else None,
                "no_price": m.outcome_prices[1] if len(m.outcome_prices) > 1 else None,
                "volume": m.volume,
                "liquidity": m.liquidity,
                "active": m.active,
                "end_date": m.end_date,
            }
            for m in markets
        ],
    }


@app.get("/markets/btc", tags=["Markets"])
async def btc_markets(
    limit: int = Query(10, ge=1, le=20),
    user_id: str = Query(...),
):
    if err := await _charge_or_reject(user_id):
        return err
    markets = await pm.get_active_btc_markets(limit)
    return {
        "count": len(markets),
        "markets": [
            {
                "id": m.id,
                "question": m.question,
                "yes_token_id": m.clob_token_ids[0] if m.clob_token_ids else None,
                "no_token_id": m.clob_token_ids[1] if len(m.clob_token_ids) > 1 else None,
                "yes_price": m.outcome_prices[0] if m.outcome_prices else None,
                "no_price": m.outcome_prices[1] if len(m.outcome_prices) > 1 else None,
                "volume": m.volume,
                "liquidity": m.liquidity,
                "end_date": m.end_date,
            }
            for m in markets
        ],
    }


@app.get("/market/{market_id}", tags=["Markets"])
async def get_market(
    market_id: str = Path(...),
    user_id: str = Query(...),
):
    if err := await _charge_or_reject(user_id):
        return err
    m = await pm.get_market_by_id(market_id)
    return {
        "id": m.id,
        "question": m.question,
        "slug": m.slug,
        "condition_id": m.condition_id,
        "outcomes": m.outcomes,
        "prices": m.outcome_prices,
        "yes_token_id": m.clob_token_ids[0] if m.clob_token_ids else None,
        "no_token_id": m.clob_token_ids[1] if len(m.clob_token_ids) > 1 else None,
        "volume": m.volume,
        "liquidity": m.liquidity,
        "active": m.active,
        "closed": m.closed,
        "end_date": m.end_date,
    }


@app.get("/market/{token_id}/book", tags=["Order Book"])
async def order_book(
    token_id: str = Path(..., description="YES or NO token ID"),
    user_id: str = Query(...),
):
    if err := await _charge_or_reject(user_id):
        return err
    book = await pm.get_order_book(token_id)
    return {
        "token_id": book.token_id,
        "last_trade_price": book.last_trade_price,
        "best_bid": book.bids[0].price if book.bids else None,
        "best_ask": book.asks[0].price if book.asks else None,
        "bid_depth": len(book.bids),
        "ask_depth": len(book.asks),
        "bids": [{"price": b.price, "size": b.size} for b in book.bids[:10]],
        "asks": [{"price": a.price, "size": a.size} for a in book.asks[:10]],
        "timestamp": book.timestamp,
    }


@app.get("/market/{token_id}/price", tags=["Order Book"])
async def market_price(
    token_id: str = Path(..., description="YES or NO token ID"),
    user_id: str = Query(...),
):
    if err := await _charge_or_reject(user_id):
        return err
    mid, spread = await asyncio.gather(
        pm.get_midpoint(token_id),
        pm.get_spread(token_id),
    )
    return {
        "token_id": token_id,
        "mid_price": mid,
        "spread": spread,
        "implied_probability_pct": round(float(mid) * 100, 2) if mid else None,
    }


@app.get("/market/{token_id}/history", tags=["Order Book"])
async def price_history(
    token_id: str = Path(..., description="YES or NO token ID"),
    interval: str = Query("5m", description="1m | 5m | 1h | 6h | 1d"),
    fidelity: int = Query(60, ge=5, le=200),
    user_id: str = Query(...),
):
    if err := await _charge_or_reject(user_id):
        return err
    history = await pm.get_price_history(token_id, interval, fidelity)
    return {"token_id": token_id, "interval": interval, "candles": len(history), "history": history}


# ── Strategy (billed) ─────────────────────────────────────────────────────────

@app.post("/signal", tags=["Strategy"])
async def run_signal(
    user_id: str = Query(...),
    ema_fast: int = Query(5),
    ema_slow: int = Query(20),
    auto_trade: bool = Query(False, description="Place real orders (requires POLYMARKET_PRIVATE_KEY)"),
):
    """
    Run EMA crossover strategy across top BTC markets.
    Returns trade signals: BUY_YES / BUY_NO / HOLD / SKIP per market.
    """
    if err := await _charge_or_reject(user_id):
        return err
    cfg = StrategyConfig(ema_fast=ema_fast, ema_slow=ema_slow, auto_trade=auto_trade)
    signals = await strat.run_once(cfg)
    return {
        "signal_count": len(signals),
        "actionable": len([s for s in signals if s.action in ("BUY_YES", "BUY_NO")]),
        "signals": [
            {
                "market": sig.question[:80],
                "action": sig.action,
                "yes_price": sig.yes_price,
                "no_price": sig.no_price,
                "spread": sig.spread,
                "ema_fast": sig.ema_fast_last,
                "ema_slow": sig.ema_slow_last,
                "reason": sig.reason,
                "timestamp": sig.timestamp,
            }
            for sig in signals
        ],
    }


# ── Auto-trader (billed) ──────────────────────────────────────────────────────

@app.get("/autotrader/status", tags=["Auto Trader"])
async def autotrader_status(user_id: str = Query(...)):
    if err := await _charge_or_reject(user_id):
        return err
    return {"running": strat.is_running(), "log_entries": len(strat.get_trade_log())}


@app.post("/autotrader/start", tags=["Auto Trader"])
async def autotrader_start(
    background_tasks: BackgroundTasks,
    user_id: str = Query(...),
    interval_seconds: int = Query(300, ge=60, description="Check interval in seconds (min 60)"),
    auto_trade: bool = Query(False, description="Enable live order placement"),
):
    """Start the 5-minute BTC auto-trader in the background."""
    if err := await _charge_or_reject(user_id):
        return err
    if strat.is_running():
        return JSONResponse(status_code=409, content={"error": "Auto-trader is already running."})

    cfg = StrategyConfig(auto_trade=auto_trade)
    background_tasks.add_task(strat.auto_trade_loop, interval_seconds, cfg)
    return {
        "status": "started",
        "interval_seconds": interval_seconds,
        "live_trading": auto_trade,
        "message": (
            "Auto-trader is scanning BTC markets every "
            f"{interval_seconds}s using EMA({cfg.ema_fast}/{cfg.ema_slow}) crossover strategy."
        ),
    }


@app.post("/autotrader/stop", tags=["Auto Trader"])
async def autotrader_stop(user_id: str = Query(...)):
    if err := await _charge_or_reject(user_id):
        return err
    strat.stop_auto_trader()
    return {"status": "stopped"}


@app.get("/autotrader/log", tags=["Auto Trader"])
async def autotrader_log(
    user_id: str = Query(...),
    limit: int = Query(50, ge=1, le=200),
):
    if err := await _charge_or_reject(user_id):
        return err
    entries = strat.get_trade_log()[:limit]
    return {"count": len(entries), "entries": entries}


# ── Portfolio (billed) ────────────────────────────────────────────────────────

@app.get("/portfolio", tags=["Portfolio"])
async def portfolio(
    wallet: str = Query(..., description="Your Polymarket proxy wallet address (0x...)"),
    user_id: str = Query(...),
):
    if err := await _charge_or_reject(user_id):
        return err
    positions, value = await asyncio.gather(
        pm.get_positions(wallet),
        pm.get_portfolio_value(wallet),
    )
    return {"wallet": wallet, "positions": positions, "value": value}


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
