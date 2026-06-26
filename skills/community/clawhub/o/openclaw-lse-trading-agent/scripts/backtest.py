"""Pandas-based strategy backtester for LSE stocks.

Tests the composite signal strategy on historical data with UK-specific costs
(SDRT stamp duty on buys, slippage on all trades).

Usage:
    uv run scripts/backtest.py HSBA.L --years 5 --initial-capital 10000
    uv run scripts/backtest.py VOD --years 2 --initial-capital 50000
"""

import argparse
import json
import sys

import numpy as np
import pandas as pd
import pandas_ta as ta

from config import IndicatorParams, RiskParams, SignalWeights
from indicators import fetch_ohlcv


def compute_indicator_series(df: pd.DataFrame, params: IndicatorParams) -> pd.DataFrame:
    """Compute all indicator series across the full dataframe.

    Unlike compute_indicators() which returns only the latest values,
    this returns full series so we can walk through day by day.
    """
    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    result = pd.DataFrame(index=df.index)
    result["close"] = close
    result["high"] = high
    result["low"] = low

    # RSI
    rsi = ta.rsi(close, length=params.rsi_period)
    result["rsi"] = rsi

    # MACD
    macd_df = ta.macd(close, fast=params.macd_fast, slow=params.macd_slow, signal=params.macd_signal)
    if macd_df is not None:
        result["macd_line"] = macd_df.iloc[:, 0]
        result["macd_hist"] = macd_df.iloc[:, 1]
        result["macd_signal"] = macd_df.iloc[:, 2]

    # Bollinger Bands
    bb = ta.bbands(close, length=params.bb_period, std=params.bb_std)
    if bb is not None:
        result["bb_lower"] = bb.iloc[:, 0]
        result["bb_mid"] = bb.iloc[:, 1]
        result["bb_upper"] = bb.iloc[:, 2]
        bb_width = (result["bb_upper"] - result["bb_lower"]) / result["bb_mid"]
        result["bb_width"] = bb_width
        result["bb_pct_b"] = (close - result["bb_lower"]) / (result["bb_upper"] - result["bb_lower"])

    # EMAs
    ema_short = ta.ema(close, length=params.ema_short)
    ema_long = ta.ema(close, length=params.ema_long)
    result["ema_short"] = ema_short
    result["ema_long"] = ema_long

    # ATR
    atr = ta.atr(high, low, close, length=params.atr_period)
    result["atr"] = atr
    result["atr_pct"] = (atr / close) * 100

    # OBV
    obv = ta.obv(close, volume)
    result["obv"] = obv
    result["obv_ema"] = ta.ema(obv, length=params.obv_ema) if obv is not None else None

    # VWAP (cumulative)
    typical_price = (high + low + close) / 3
    cumulative_tp_vol = (typical_price * volume).cumsum()
    cumulative_vol = volume.cumsum()
    result["vwap"] = cumulative_tp_vol / cumulative_vol

    return result


def compute_composite_score(row: pd.Series, weights: SignalWeights) -> float:
    """Compute composite signal score for a single day from indicator values.

    Returns a score in [-1, 1] range. Uses trend, momentum, volatility, volume
    components (no sentiment for backtesting). Weights are re-normalised to
    exclude the sentiment weight.
    """
    scores = {}

    # --- Trend score [-1, 1] ---
    trend = 0.0
    ema_s = row.get("ema_short")
    ema_l = row.get("ema_long")
    if pd.notna(ema_s) and pd.notna(ema_l) and ema_l != 0:
        # EMA alignment: +1 if short > long, -1 otherwise
        ema_diff = (ema_s - ema_l) / ema_l
        trend = np.clip(ema_diff * 20, -1, 1)  # scale so 5% diff = full signal
    close = row.get("close")
    vwap = row.get("vwap")
    if pd.notna(close) and pd.notna(vwap) and vwap != 0:
        vwap_diff = (close - vwap) / vwap
        vwap_score = np.clip(vwap_diff * 10, -1, 1)
        trend = 0.7 * trend + 0.3 * vwap_score
    scores["trend"] = trend

    # --- Momentum score [-1, 1] ---
    momentum = 0.0
    rsi = row.get("rsi")
    macd_hist = row.get("macd_hist")
    if pd.notna(rsi):
        # RSI: 50 is neutral, <30 oversold (bullish), >70 overbought (bearish)
        rsi_score = np.clip((50 - rsi) / 30, -1, 1)
        momentum += 0.5 * rsi_score
    if pd.notna(macd_hist):
        # Positive histogram = bullish momentum
        atr = row.get("atr")
        if pd.notna(atr) and atr > 0:
            macd_norm = np.clip(macd_hist / atr, -1, 1)
        else:
            macd_norm = np.clip(macd_hist * 10, -1, 1)
        momentum += 0.5 * macd_norm
    scores["momentum"] = np.clip(momentum, -1, 1)

    # --- Volatility score [-1, 1] ---
    volatility = 0.0
    bb_pct_b = row.get("bb_pct_b")
    bb_width = row.get("bb_width")
    if pd.notna(bb_pct_b):
        # %B < 0.2 = near lower band (bullish), > 0.8 = near upper (bearish)
        volatility = np.clip((0.5 - bb_pct_b) * 2, -1, 1)
    if pd.notna(bb_width) and bb_width < 0.04:
        # Bollinger squeeze — amplify signal slightly
        volatility *= 1.3
        volatility = np.clip(volatility, -1, 1)
    scores["volatility"] = volatility

    # --- Volume score [-1, 1] ---
    vol_score = 0.0
    obv = row.get("obv")
    obv_ema = row.get("obv_ema")
    if pd.notna(obv) and pd.notna(obv_ema) and obv_ema != 0:
        obv_diff = (obv - obv_ema) / abs(obv_ema) if obv_ema != 0 else 0
        vol_score = np.clip(obv_diff * 5, -1, 1)
    scores["volume"] = vol_score

    # Re-normalise weights excluding sentiment
    w_total = weights.trend + weights.momentum + weights.volatility + weights.volume
    if w_total == 0:
        return 0.0

    composite = (
        scores["trend"] * weights.trend
        + scores["momentum"] * weights.momentum
        + scores["volatility"] * weights.volatility
        + scores["volume"] * weights.volume
    ) / w_total

    return float(np.clip(composite, -1, 1))


def run_backtest(
    ticker: str,
    years: int = 5,
    initial_capital: float = 10000.0,
) -> dict:
    """Run backtest on a single ticker and return performance metrics."""
    params = IndicatorParams()
    risk = RiskParams()
    weights = SignalWeights()

    # Fetch extra history for 200-day EMA warmup
    fetch_years = max(years + 1, 2)
    period = f"{fetch_years}y"
    df = fetch_ohlcv(ticker, period=period, interval="1d")

    # Compute indicator series over the full history
    indicators = compute_indicator_series(df, params)

    # Determine the trading window — skip first 200 rows for warmup
    warmup = max(params.ema_long, 200)
    if len(indicators) <= warmup:
        return {
            "ticker": ticker,
            "error": f"Not enough data ({len(indicators)} bars, need > {warmup})",
        }

    trading_data = indicators.iloc[warmup:].copy()

    # Limit to requested number of years (approx 252 trading days per year)
    max_bars = years * 252
    if len(trading_data) > max_bars:
        trading_data = trading_data.iloc[-max_bars:]

    # --- Simulate trades ---
    capital = initial_capital
    position = None  # dict with entry_price, shares, entry_date, trailing_stop
    trades = []  # completed trades
    daily_equity = []

    for i, (date, row) in enumerate(trading_data.iterrows()):
        price = row["close"]
        atr = row["atr"] if pd.notna(row["atr"]) else 0
        score = compute_composite_score(row, weights)

        # Update trailing stop if in position
        if position is not None:
            new_stop = price - (atr * risk.atr_stop_multiplier) if atr > 0 else position["trailing_stop"]
            position["trailing_stop"] = max(position["trailing_stop"], new_stop)

            # Check sell conditions
            sell = False
            if score < -0.4:
                sell = True
            elif price <= position["trailing_stop"]:
                sell = True

            if sell:
                slippage_cost = price * risk.estimated_slippage
                sell_price = price - slippage_cost
                proceeds = sell_price * position["shares"]
                pnl = proceeds - position["cost_basis"]
                capital = proceeds
                trades.append({
                    "entry_date": str(position["entry_date"]),
                    "exit_date": str(date.date()) if hasattr(date, "date") else str(date),
                    "entry_price": position["entry_price"],
                    "exit_price": round(sell_price, 4),
                    "shares": position["shares"],
                    "pnl": round(pnl, 2),
                    "days_held": (date - position["entry_date_dt"]).days,
                })
                position = None

        # Check buy conditions (only if not in position)
        if position is None and score > 0.4:
            # Apply SDRT (stamp duty) and slippage on buy
            sdrt_cost = price * risk.sdrt_rate
            slippage_cost = price * risk.estimated_slippage
            buy_price = price + slippage_cost + sdrt_cost
            shares = capital / buy_price
            cost_basis = shares * buy_price
            trailing_stop = price - (atr * risk.atr_stop_multiplier) if atr > 0 else price * 0.95

            position = {
                "entry_price": round(buy_price, 4),
                "shares": shares,
                "cost_basis": cost_basis,
                "entry_date": str(date.date()) if hasattr(date, "date") else str(date),
                "entry_date_dt": date,
                "trailing_stop": trailing_stop,
            }
            capital = 0.0  # fully invested

        # Track daily equity
        if position is not None:
            equity = position["shares"] * price
        else:
            equity = capital
        daily_equity.append({"date": date, "equity": equity})

    # Close any open position at last price
    if position is not None:
        last_row = trading_data.iloc[-1]
        last_date = trading_data.index[-1]
        last_price = last_row["close"]
        slippage_cost = last_price * risk.estimated_slippage
        sell_price = last_price - slippage_cost
        proceeds = sell_price * position["shares"]
        pnl = proceeds - position["cost_basis"]
        capital = proceeds
        trades.append({
            "entry_date": position["entry_date"],
            "exit_date": str(last_date.date()) if hasattr(last_date, "date") else str(last_date),
            "entry_price": position["entry_price"],
            "exit_price": round(sell_price, 4),
            "shares": position["shares"],
            "pnl": round(pnl, 2),
            "days_held": (last_date - position["entry_date_dt"]).days,
        })
        position = None

    # --- Compute metrics ---
    equity_series = pd.Series(
        [d["equity"] for d in daily_equity],
        index=[d["date"] for d in daily_equity],
    )

    final_capital = capital if capital > 0 else equity_series.iloc[-1]
    total_return_pct = ((final_capital - initial_capital) / initial_capital) * 100

    # Benchmark: buy and hold (with SDRT + slippage on initial buy, slippage on final sell)
    first_price = trading_data.iloc[0]["close"]
    last_price = trading_data.iloc[-1]["close"]
    bh_buy_price = first_price * (1 + risk.sdrt_rate + risk.estimated_slippage)
    bh_sell_price = last_price * (1 - risk.estimated_slippage)
    benchmark_return_pct = ((bh_sell_price / bh_buy_price) - 1) * 100

    # Daily returns for Sharpe/Sortino
    daily_returns = equity_series.pct_change().dropna()

    # Sharpe ratio (annualised, rf=0)
    if len(daily_returns) > 1 and daily_returns.std() > 0:
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0

    # Sortino ratio (annualised, downside deviation only)
    downside = daily_returns[daily_returns < 0]
    if len(downside) > 1 and downside.std() > 0:
        sortino_ratio = (daily_returns.mean() / downside.std()) * np.sqrt(252)
    else:
        sortino_ratio = 0.0

    # Max drawdown
    cummax = equity_series.cummax()
    drawdown = (equity_series - cummax) / cummax
    max_drawdown_pct = float(drawdown.min()) * 100 if len(drawdown) > 0 else 0.0

    # Trade stats
    total_trades = len(trades)
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]
    win_rate_pct = (len(wins) / total_trades * 100) if total_trades > 0 else 0.0
    avg_trade_days = (sum(t["days_held"] for t in trades) / total_trades) if total_trades > 0 else 0.0

    gross_profit = sum(t["pnl"] for t in wins) if wins else 0.0
    gross_loss = abs(sum(t["pnl"] for t in losses)) if losses else 0.0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float("inf") if gross_profit > 0 else 0.0

    return {
        "ticker": ticker,
        "backtest_years": years,
        "initial_capital": initial_capital,
        "final_capital": round(final_capital, 2),
        "trading_days": len(trading_data),
        "data_start": str(trading_data.index[0].date()),
        "data_end": str(trading_data.index[-1].date()),
        "metrics": {
            "total_return_pct": round(total_return_pct, 2),
            "benchmark_return_pct": round(benchmark_return_pct, 2),
            "sharpe_ratio": round(sharpe_ratio, 4),
            "sortino_ratio": round(sortino_ratio, 4),
            "max_drawdown_pct": round(max_drawdown_pct, 2),
            "win_rate_pct": round(win_rate_pct, 2),
            "total_trades": total_trades,
            "avg_trade_days": round(avg_trade_days, 1),
            "profit_factor": round(profit_factor, 4) if profit_factor != float("inf") else "inf",
        },
        "trades": trades,
    }


def main():
    parser = argparse.ArgumentParser(description="Backtest composite signal strategy on LSE stocks")
    parser.add_argument("ticker", help="Yahoo Finance ticker (e.g., HSBA.L)")
    parser.add_argument("--years", type=int, default=5, help="Number of years to backtest (default: 5)")
    parser.add_argument("--initial-capital", type=float, default=10000, help="Initial capital in GBP (default: 10000)")
    args = parser.parse_args()

    ticker = args.ticker if "." in args.ticker else f"{args.ticker}.L"
    result = run_backtest(ticker, years=args.years, initial_capital=args.initial_capital)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
