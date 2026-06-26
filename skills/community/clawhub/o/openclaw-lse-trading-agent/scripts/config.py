"""Configuration for LSE Trading Agent."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class IndicatorParams:
    rsi_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    bb_period: int = 20
    bb_std: float = 2.0
    ema_short: int = 50
    ema_long: int = 200
    atr_period: int = 14
    vwap_period: int = 14
    obv_ema: int = 20


@dataclass(frozen=True)
class RiskParams:
    max_risk_per_trade: float = 0.02  # 2%
    max_position_pct: float = 0.05  # 5% of portfolio
    max_drawdown: float = 0.15  # 15% circuit breaker
    max_daily_loss: float = 0.03  # 3%
    max_sector_exposure: float = 0.25  # 25%
    max_open_positions: int = 10
    min_positions_above_10k: int = 5
    kelly_fraction: float = 0.5  # half-Kelly
    sdrt_rate: float = 0.005  # 0.5% stamp duty on UK equity buys
    estimated_slippage: float = 0.001  # 0.1% slippage estimate
    atr_stop_multiplier: float = 2.0


@dataclass(frozen=True)
class SignalWeights:
    trend: float = 0.25
    momentum: float = 0.25
    volatility: float = 0.15
    volume: float = 0.15
    sentiment: float = 0.20


# FTSE 350 sectors (GICS)
GICS_SECTORS = [
    "Energy",
    "Materials",
    "Industrials",
    "Consumer Discretionary",
    "Consumer Staples",
    "Health Care",
    "Financials",
    "Information Technology",
    "Communication Services",
    "Utilities",
    "Real Estate",
]

# LSE trading hours (UTC)
LSE_OPEN_HOUR = 8
LSE_CLOSE_HOUR = 16
LSE_CLOSE_MINUTE = 30
