"""Pure portfolio risk metric helpers."""

from __future__ import annotations

import math


def returns_from_prices(prices: list[float]) -> list[float]:
    """Return simple period returns from an ordered price series."""
    returns: list[float] = []
    for previous, current in zip(prices, prices[1:]):
        if previous == 0:
            raise ValueError("price series contains zero base price")
        returns.append((current / previous) - 1.0)
    return returns


def weighted_portfolio_returns(
    asset_returns: dict[str, list[float]], weights: dict[str, float]
) -> list[float]:
    """Combine aligned asset return series using portfolio weights."""
    if not weights:
        return []

    missing_tickers = [ticker for ticker in weights if ticker not in asset_returns]
    if missing_tickers:
        raise ValueError(
            "missing asset returns for weights: " + ", ".join(sorted(missing_tickers))
        )

    lengths = {len(asset_returns[ticker]) for ticker in weights}
    if len(lengths) != 1:
        raise ValueError("asset return series are not aligned")

    period_count = lengths.pop()
    portfolio_returns: list[float] = []
    for index in range(period_count):
        portfolio_returns.append(
            sum(asset_returns[ticker][index] * weight for ticker, weight in weights.items())
        )
    return portfolio_returns


def volatility(returns: list[float], periods_per_year: int) -> float | None:
    """Return annualized sample volatility."""
    if len(returns) < 2 or periods_per_year <= 0:
        return None

    mean = sum(returns) / len(returns)
    variance = sum((value - mean) ** 2 for value in returns) / (len(returns) - 1)
    return math.sqrt(variance) * math.sqrt(periods_per_year)


def max_drawdown(returns: list[float]) -> float:
    """Return the worst peak-to-trough drawdown as a negative decimal."""
    wealth = 1.0
    peak = 1.0
    worst_drawdown = 0.0

    for value in returns:
        wealth *= 1.0 + value
        if wealth > peak:
            peak = wealth
        drawdown = (wealth / peak) - 1.0
        if drawdown < worst_drawdown:
            worst_drawdown = drawdown

    return worst_drawdown


def beta(portfolio_returns: list[float], benchmark_returns: list[float]) -> float | None:
    """Return beta versus benchmark returns."""
    if len(portfolio_returns) != len(benchmark_returns):
        return None

    paired = _paired_values(portfolio_returns, benchmark_returns)
    if len(paired) < 2:
        return None

    portfolio, benchmark = zip(*paired)
    benchmark_mean = sum(benchmark) / len(benchmark)
    portfolio_mean = sum(portfolio) / len(portfolio)
    benchmark_variance = sum((value - benchmark_mean) ** 2 for value in benchmark)
    if benchmark_variance == 0:
        return None

    covariance = sum(
        (portfolio_value - portfolio_mean) * (benchmark_value - benchmark_mean)
        for portfolio_value, benchmark_value in paired
    )
    return covariance / benchmark_variance


def correlation(x: list[float], y: list[float]) -> float | None:
    """Return Pearson correlation for aligned series."""
    if len(x) != len(y):
        return None

    paired = _paired_values(x, y)
    if len(paired) < 2:
        return None

    x_values, y_values = zip(*paired)
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    x_squares = sum((value - x_mean) ** 2 for value in x_values)
    y_squares = sum((value - y_mean) ** 2 for value in y_values)
    denominator = math.sqrt(x_squares * y_squares)
    if denominator == 0:
        return None

    numerator = sum(
        (x_value - x_mean) * (y_value - y_mean) for x_value, y_value in paired
    )
    return numerator / denominator


def concentration(weights: dict[str, float]) -> dict[str, float]:
    """Return largest holding weight and Herfindahl-Hirschman index."""
    if not weights:
        return {"largest_weight": 0.0, "herfindahl_index": 0.0}

    return {
        "largest_weight": max(weights.values()),
        "herfindahl_index": sum(weight**2 for weight in weights.values()),
    }


def _paired_values(x: list[float], y: list[float]) -> list[tuple[float, float]]:
    return list(zip(x, y))
