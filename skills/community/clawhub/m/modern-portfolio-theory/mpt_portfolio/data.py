from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf

from mpt_portfolio.utils import TRADING_DAYS_PER_YEAR, get_portfolios_dir

logger = logging.getLogger(__name__)


class DataFetchError(Exception):
    pass


class DataValidationError(Exception):
    pass


@dataclass
class AssetDataInfo:
    ticker: str
    available_days: int
    required_days: int
    sufficient: bool
    first_date: str | None = None
    last_date: str | None = None


@dataclass
class DataSufficiencyReport:
    assets: list[AssetDataInfo] = field(default_factory=list)
    all_sufficient: bool = True
    effective_common_days: int = 0
    required_days: int = 0
    insufficient_assets: list[str] = field(default_factory=list)
    suggested_max_years: float = 0.0


def _fetch_raw_prices(
    tickers: list[str],
    start_date: str | datetime,
    end_date: str | datetime | None = None,
    price_type: str = "adjusted",
) -> pd.DataFrame:
    """Fetch daily close prices via yfinance without dropping NaN rows."""
    auto_adjust = price_type == "adjusted"

    try:
        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            auto_adjust=auto_adjust,
            progress=False,
        )
    except Exception as e:
        raise DataFetchError(f"Failed to download data from yfinance: {e}") from e

    if data.empty:
        raise DataFetchError(
            f"No data returned for tickers: {tickers}. "
            "Check that tickers are valid and yfinance is up to date."
        )

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]] if len(tickers) == 1 else data
        if len(tickers) == 1:
            prices.columns = tickers

    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    missing = [t for t in tickers if t not in prices.columns or prices[t].isna().all()]
    if missing:
        raise DataFetchError(
            f"No data for tickers: {missing}. "
            "Verify they are valid symbols. Run 'pip install --upgrade yfinance' "
            "if this persists."
        )

    prices.index = pd.DatetimeIndex(prices.index)
    return prices


def fetch_prices(
    tickers: list[str],
    start_date: str | datetime,
    end_date: str | datetime | None = None,
    price_type: str = "adjusted",
) -> pd.DataFrame:
    """Fetch daily close prices via yfinance.

    Args:
        tickers: List of ticker symbols.
        start_date: Start date for historical data.
        end_date: End date (default: today).
        price_type: "adjusted" (auto_adjust=True, total return) or
                    "unadjusted" (auto_adjust=False, price return only).

    Returns:
        DataFrame with DatetimeIndex and columns = tickers (daily close prices).
    """
    prices = _fetch_raw_prices(tickers, start_date, end_date, price_type)
    return prices[tickers].dropna()


def check_data_sufficiency(
    raw_prices: pd.DataFrame,
    lookback_years: int,
    backtest_years: int,
) -> DataSufficiencyReport:
    """Check per-asset data availability against required lookback + backtest period."""
    required_days = int((lookback_years + backtest_years) * TRADING_DAYS_PER_YEAR)
    assets: list[AssetDataInfo] = []
    insufficient: list[str] = []

    for ticker in raw_prices.columns:
        col = raw_prices[ticker].dropna()
        available = len(col)
        first = col.index[0].strftime("%Y-%m-%d") if available > 0 else None
        last = col.index[-1].strftime("%Y-%m-%d") if available > 0 else None
        ok = available >= required_days
        assets.append(AssetDataInfo(
            ticker=ticker,
            available_days=available,
            required_days=required_days,
            sufficient=ok,
            first_date=first,
            last_date=last,
        ))
        if not ok:
            insufficient.append(ticker)

    common = len(raw_prices.dropna())
    suggested = round(common / TRADING_DAYS_PER_YEAR, 1) if common > 0 else 0.0

    return DataSufficiencyReport(
        assets=assets,
        all_sufficient=len(insufficient) == 0,
        effective_common_days=common,
        required_days=required_days,
        insufficient_assets=insufficient,
        suggested_max_years=suggested,
    )


def fetch_risk_free_rate() -> float:
    """Fetch current 3-month US Treasury yield (^IRX) as annualized decimal."""
    try:
        irx = yf.Ticker("^IRX")
        hist = irx.history(period="5d")
        if hist.empty:
            logger.warning("Could not fetch ^IRX; using default risk-free rate 0.05")
            return 0.05
        rate = float(hist["Close"].iloc[-1]) / 100.0
        return rate
    except Exception:
        logger.warning("Failed to fetch risk-free rate; using default 0.05")
        return 0.05


def get_risk_free_rate(config_value: float | str) -> float:
    """Resolve risk-free rate from config: 'auto' fetches ^IRX, otherwise returns float."""
    if isinstance(config_value, str) and config_value.lower() == "auto":
        return fetch_risk_free_rate()
    return float(config_value)


def validate_price_data(prices: pd.DataFrame, min_observations: int = 252) -> None:
    """Validate that price data has sufficient observations."""
    if len(prices) < min_observations:
        raise DataValidationError(
            f"Only {len(prices)} observations available, need at least {min_observations}. "
            f"Increase lookback period or reduce asset count."
        )


def cache_prices(prices: pd.DataFrame, portfolio_name: str) -> Path:
    """Save prices to cache in portfolio directory (parquet preferred, CSV fallback)."""
    cache_dir = get_portfolios_dir() / portfolio_name
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        path = cache_dir / "price_cache.parquet"
        prices.to_parquet(path)
        return path
    except ImportError:
        path = cache_dir / "price_cache.csv"
        prices.to_csv(path)
        return path


def load_cached_prices(portfolio_name: str, max_age_hours: int = 24) -> pd.DataFrame | None:
    """Load cached prices if fresh enough. Return None if stale or missing."""
    cache_dir = get_portfolios_dir() / portfolio_name
    for ext, reader in [("parquet", pd.read_parquet), ("csv", pd.read_csv)]:
        path = cache_dir / f"price_cache.{ext}"
        if not path.exists():
            continue
        age = time.time() - path.stat().st_mtime
        if age > max_age_hours * 3600:
            return None
        try:
            df = reader(path)
            if ext == "csv":
                df.index = pd.DatetimeIndex(df.iloc[:, 0])
                df = df.iloc[:, 1:]
            return df
        except Exception:
            continue
    return None
