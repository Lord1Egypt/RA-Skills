"""
trader.py — Main entry point for the IBKR Autonomous Trader.

Orchestrates: connection → data → signals → risk → execution → monitoring → logging → eval.
"""

import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml
from ib_insync import IB, util
from loguru import logger

from strategy_engine import StrategyEngine
from risk_manager import RiskManager
from execution_engine import ExecutionEngine
from performance import PerformanceTracker
from news_engine import NewsEngine
from decision_engine import DecisionEngine

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config" / "settings.yaml"
LOG_PATH = ROOT / "logs" / "trader.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def configure_logging(cfg: dict) -> None:
    logger.remove()
    logger.add(
        LOG_PATH,
        level=cfg["logging"]["level"],
        rotation=cfg["logging"]["rotation"],
        retention=cfg["logging"]["retention"],
        enqueue=True,
    )
    logger.add(lambda msg: print(msg, end=""), level="INFO", colorize=True)


def is_market_hours(cfg: dict) -> bool:
    tz = ZoneInfo(cfg["loop"]["timezone"])
    now = datetime.now(tz)
    if now.weekday() >= 5:  # Saturday / Sunday
        return False
    open_t = datetime.strptime(cfg["loop"]["market_open"], "%H:%M").time()
    close_t = datetime.strptime(cfg["loop"]["market_close"], "%H:%M").time()
    return open_t <= now.time() <= close_t


def connect_ibkr(ib: IB, cfg: dict) -> bool:
    """Attempt to connect to TWS / IB Gateway."""
    safety = cfg["safety"]
    live = safety["enable_live_trading"]
    port = cfg["ibkr"]["live_trading_port"] if live else cfg["ibkr"]["paper_trading_port"]
    host = cfg["ibkr"]["host"]
    client_id = cfg["ibkr"]["client_id"]

    if live:
        logger.warning("⚠️  LIVE TRADING ENABLED — connecting to live account")
        if safety.get("require_confirmation"):
            confirm = input("Type CONFIRM to proceed with live trading: ").strip()
            if confirm != "CONFIRM":
                logger.error("Live trading aborted by user.")
                return False

    try:
        ib.connect(host, port, clientId=client_id, timeout=cfg["ibkr"]["timeout"])
        logger.info(f"Connected to IBKR {'LIVE' if live else 'PAPER'} on {host}:{port}")
        return True
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False


def main() -> None:
    cfg = load_config()
    configure_logging(cfg)
    logger.info("=" * 60)
    logger.info("IBKR Autonomous Trader starting")
    logger.info("=" * 60)

    ib = IB()
    if not connect_ibkr(ib, cfg):
        return

    strategy_engine = StrategyEngine(cfg)
    risk_manager = RiskManager(cfg, ib)
    execution_engine = ExecutionEngine(cfg, ib)
    perf_tracker = PerformanceTracker(cfg)
    news_engine = NewsEngine(cfg)
    decision_engine = DecisionEngine(cfg)

    loop_count = 0
    eval_every = cfg["loop"]["eval_every_n_loops"]
    interval = cfg["loop"]["interval_sec"]
    news_enabled = cfg.get("news", {}).get("enabled", True)

    logger.info("Trading loop started.")

    try:
        while True:
            loop_count += 1
            logger.info(f"── Loop {loop_count} ──────────────────────────────────────")

            # ── Gate: market hours ──────────────────────────────────
            if not is_market_hours(cfg):
                logger.info("Outside market hours. Sleeping 60s.")
                time.sleep(60)
                continue

            # ── Kill switch check ───────────────────────────────────
            if risk_manager.kill_switch_active():
                logger.warning("🛑 Kill switch active — halting trading for today.")
                time.sleep(300)
                continue

            # ── 1. Fetch market data ────────────────────────────────
            bars_dict = {}
            for symbol in cfg["watchlist"]:
                bars = execution_engine.fetch_bars(symbol)
                if bars is not None:
                    bars_dict[symbol] = bars

            if not bars_dict:
                logger.warning("No market data received. Retrying next loop.")
                time.sleep(interval)
                continue

            # ── 2. Fetch and analyze news ───────────────────────────
            news_items = []
            market_sentiment = {"aggregate_score": 0.0, "risk_event": False, "high_impact": False}
            if news_enabled:
                news_items = news_engine.fetch_all()
                market_sentiment = news_engine.get_market_sentiment(news_items)
                news_engine.log_news(news_items)
                logger.info(
                    f"Market sentiment: score={market_sentiment['aggregate_score']:.3f} "
                    f"risk_event={market_sentiment['risk_event']}"
                )

            # ── 3. Generate technical signals ───────────────────────
            signals = strategy_engine.generate_signals(bars_dict)
            logger.info(f"Generated {len(signals)} technical signal(s).")

            # ── 4. Open positions snapshot ──────────────────────────
            positions = execution_engine.get_positions()

            # ── 5. Multi-factor decision + risk validate + execute ──
            account_value = risk_manager.get_account_value()
            daily_pnl_pct = risk_manager.get_daily_pnl_pct(account_value)
            portfolio_state = {
                "positions": len(positions),
                "daily_pnl_pct": daily_pnl_pct,
            }

            for signal in signals:
                # Skip if already have a position in this symbol
                if any(p.contract.symbol == signal.symbol for p in positions):
                    logger.debug(f"Skipping {signal.symbol} — position already open.")
                    continue

                # Risk pre-check
                approved, reason = risk_manager.validate_signal(signal, positions)
                if not approved:
                    logger.info(f"Signal for {signal.symbol} rejected by risk_manager: {reason}")
                    continue

                # News sentiment for this symbol
                symbol_sentiment = (
                    news_engine.get_symbol_sentiment(signal.symbol, news_items)
                    if news_enabled else 0.0
                )

                # Volatility classification
                atr = signal.indicators.get("atr", 0.0)
                vol_regime = DecisionEngine.classify_volatility(atr, signal.entry_price)

                # Multi-factor decision
                decision = decision_engine.decide(
                    signal=signal,
                    market_sentiment=market_sentiment,
                    symbol_sentiment=symbol_sentiment,
                    volatility_regime=vol_regime,
                    portfolio_state=portfolio_state,
                )

                logger.info(
                    f"Decision: {decision.action} {signal.symbol} "
                    f"conf={decision.confidence:.2f} | {decision.reason}"
                )

                if decision.action in ("NO_TRADE", "REDUCE_RISK", "HOLD"):
                    continue

                # Apply decision modifiers to position size
                quantity = risk_manager.size_position(signal, account_value)
                quantity = int(quantity * decision.position_size_modifier)
                if quantity <= 0:
                    logger.info(f"Adjusted position size 0 for {signal.symbol} — skipping.")
                    continue

                # Apply stop modifier
                if decision.stop_modifier != 1.0:
                    if signal.direction == "LONG":
                        signal.stop_price = signal.entry_price - (
                            (signal.entry_price - signal.stop_price) * decision.stop_modifier
                        )
                    else:
                        signal.stop_price = signal.entry_price + (
                            (signal.stop_price - signal.entry_price) * decision.stop_modifier
                        )

                signal.quantity = quantity
                trade = execution_engine.execute_trade(signal)
                if trade:
                    perf_tracker.log_trade_open(trade, signal)

            # ── 6. Monitor open positions ───────────────────────────
            execution_engine.monitor_positions(positions, perf_tracker)

            # ── 7. Periodic performance evaluation ─────────────────
            if loop_count % eval_every == 0:
                logger.info("Running performance evaluation...")
                stats = perf_tracker.evaluate_performance()
                logger.info(f"Performance: {stats}")
                recommendations = perf_tracker.suggest_improvements(stats)
                if recommendations:
                    perf_tracker.apply_improvements(recommendations, strategy_engine)

                # News utility learning
                if news_enabled:
                    utility = news_engine.evaluate_news_utility()
                    if utility:
                        logger.info(f"News utility by type: {utility}")

            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Trader stopped by user.")
    except Exception as e:
        logger.exception(f"Unhandled exception in main loop: {e}")
    finally:
        execution_engine.close_all_positions()
        ib.disconnect()
        logger.info("Disconnected from IBKR.")


if __name__ == "__main__":
    util.startLoop()
    main()
