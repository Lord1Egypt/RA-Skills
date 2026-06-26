#!/usr/bin/env python3
"""Analyze portfolio risk from local CSV inputs."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from itertools import combinations
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from risk_metrics import (  # noqa: E402
    beta,
    concentration,
    correlation,
    max_drawdown,
    returns_from_prices,
    volatility,
    weighted_portfolio_returns,
)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        weights = read_holdings(args.holdings_file)
        price_data = read_prices(args.prices_file)
        aligned_dates, aligned_prices = align_holding_prices(price_data, weights)

        asset_returns = {
            ticker: returns_from_prices(prices)
            for ticker, prices in aligned_prices.items()
        }
        portfolio_returns = weighted_portfolio_returns(asset_returns, weights)

        benchmark_summary = None
        if args.benchmark_file:
            benchmark_dates, benchmark_prices = read_benchmark(args.benchmark_file)
            benchmark_returns = align_benchmark_returns(
                aligned_dates, benchmark_dates, benchmark_prices
            )
            benchmark_summary = {
                "returns": round_list(benchmark_returns),
                "beta": round_or_none(beta(portfolio_returns, benchmark_returns)),
                "correlation": round_or_none(
                    correlation(portfolio_returns, benchmark_returns)
                ),
            }

        summary = {
            "inputs": {
                "holdings_file": str(args.holdings_file),
                "prices_file": str(args.prices_file),
                "benchmark_file": str(args.benchmark_file) if args.benchmark_file else None,
                "periods_per_year": args.periods_per_year,
            },
            "dates": {
                "price_dates": aligned_dates,
                "return_dates": aligned_dates[1:],
            },
            "weights": weights,
            "asset_returns": {
                ticker: round_list(returns)
                for ticker, returns in sorted(asset_returns.items())
            },
            "portfolio_returns": round_list(portfolio_returns),
            "metrics": {
                "volatility": round_or_none(
                    volatility(portfolio_returns, args.periods_per_year)
                ),
                "max_drawdown": round(max_drawdown(portfolio_returns), 10),
                "concentration": round_mapping(concentration(weights)),
                "pairwise_correlations": compact_pairwise_correlations(asset_returns),
            },
            "benchmark": benchmark_summary,
        }

        args.outdir.mkdir(parents=True, exist_ok=True)
        output_file = args.outdir / "portfolio_analytics_summary.json"
        summary_json = json.dumps(summary, allow_nan=False, indent=2, sort_keys=True)
        output_file.write_text(summary_json + "\n")
        print(summary_json)
    except (OSError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute portfolio risk analytics from holdings and price CSVs."
    )
    parser.add_argument("--holdings-file", required=True, type=Path)
    parser.add_argument("--prices-file", required=True, type=Path)
    parser.add_argument("--benchmark-file", type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    parser.add_argument("--periods-per-year", type=parse_periods_per_year, default=12)
    return parser


def read_holdings(path: Path) -> dict[str, float]:
    rows = read_dict_rows(path, {"ticker", "weight"})
    weights: dict[str, float] = {}
    for row in rows:
        ticker = require_text(row, "ticker", path)
        if ticker in weights:
            raise ValueError(f"duplicate holding ticker: {ticker}")
        weight = parse_float(row.get("weight", ""), f"{path}: weight for {ticker}")
        if weight < 0:
            raise ValueError(f"holding weight must be nonnegative: {ticker}")
        weights[ticker] = weight

    if not weights:
        raise ValueError("holdings file has no rows")

    total_weight = sum(weights.values())
    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(f"holding weights must sum to 1.0; got {total_weight:.10f}")

    return weights


def read_prices(path: Path) -> dict[str, dict[str, float]]:
    rows = read_dict_rows(path, {"date", "ticker", "close"})
    prices: dict[str, dict[str, float]] = {}
    for row in rows:
        ticker = require_text(row, "ticker", path)
        date = require_text(row, "date", path)
        close = parse_float(row.get("close", ""), f"{path}: close for {ticker} on {date}")
        if close <= 0:
            raise ValueError(f"close price must be positive: {ticker} {date}")
        prices.setdefault(ticker, {})
        if date in prices[ticker]:
            raise ValueError(f"duplicate price row: {ticker} {date}")
        prices[ticker][date] = close

    if not prices:
        raise ValueError("prices file has no rows")
    return prices


def read_benchmark(path: Path) -> tuple[list[str], list[float]]:
    rows = read_dict_rows(path, {"date", "close"})
    values: dict[str, float] = {}
    for row in rows:
        date = require_text(row, "date", path)
        close = parse_float(row.get("close", ""), f"{path}: close on {date}")
        if close <= 0:
            raise ValueError(f"benchmark close must be positive: {date}")
        if date in values:
            raise ValueError(f"duplicate benchmark date: {date}")
        values[date] = close

    if not values:
        raise ValueError("benchmark file has no rows")

    dates = sorted(values)
    return dates, [values[date] for date in dates]


def align_holding_prices(
    price_data: dict[str, dict[str, float]], weights: dict[str, float]
) -> tuple[list[str], dict[str, list[float]]]:
    missing_tickers = sorted(ticker for ticker in weights if ticker not in price_data)
    if missing_tickers:
        raise ValueError(f"missing price data for holdings: {', '.join(missing_tickers)}")

    first_ticker = next(iter(weights))
    aligned_dates = sorted(price_data[first_ticker])
    if len(aligned_dates) < 2:
        raise ValueError("at least two aligned price dates are required")

    for ticker in weights:
        ticker_dates = sorted(price_data[ticker])
        if ticker_dates != aligned_dates:
            missing = sorted(set(aligned_dates) - set(ticker_dates))
            extra = sorted(set(ticker_dates) - set(aligned_dates))
            details = []
            if missing:
                details.append(f"missing dates: {', '.join(missing)}")
            if extra:
                details.append(f"extra dates: {', '.join(extra)}")
            suffix = f" ({'; '.join(details)})" if details else ""
            raise ValueError(f"price dates are not aligned for {ticker}{suffix}")

    return aligned_dates, {
        ticker: [price_data[ticker][date] for date in aligned_dates]
        for ticker in weights
    }


def align_benchmark_returns(
    portfolio_price_dates: list[str], benchmark_dates: list[str], benchmark_prices: list[float]
) -> list[float]:
    if benchmark_dates != portfolio_price_dates:
        missing = sorted(set(portfolio_price_dates) - set(benchmark_dates))
        extra = sorted(set(benchmark_dates) - set(portfolio_price_dates))
        details = []
        if missing:
            details.append(f"missing dates: {', '.join(missing)}")
        if extra:
            details.append(f"extra dates: {', '.join(extra)}")
        suffix = f" ({'; '.join(details)})" if details else ""
        raise ValueError(f"benchmark dates are not aligned with portfolio prices{suffix}")
    return returns_from_prices(benchmark_prices)


def compact_pairwise_correlations(
    asset_returns: dict[str, list[float]]
) -> dict[str, float | None]:
    pairs: dict[str, float | None] = {}
    for left, right in combinations(sorted(asset_returns), 2):
        pairs[f"{left}:{right}"] = round_or_none(
            correlation(asset_returns[left], asset_returns[right])
        )
    return pairs


def read_dict_rows(path: Path, required_columns: set[str]) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(required_columns - fieldnames)
        if missing:
            raise ValueError(f"{path} missing columns: {', '.join(missing)}")
        return list(reader)


def require_text(row: dict[str, str], column: str, path: Path) -> str:
    value = (row.get(column) or "").strip()
    if not value:
        raise ValueError(f"{path} has blank {column}")
    return value


def parse_float(raw_value: str, context: str) -> float:
    try:
        value = float(raw_value)
    except ValueError as error:
        raise ValueError(f"invalid number for {context}: {raw_value!r}") from error
    if not math.isfinite(value):
        raise ValueError(f"non-finite number for {context}: {raw_value!r}")
    return value


def parse_periods_per_year(raw_value: str) -> int:
    try:
        value = int(raw_value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"periods-per-year must be a positive integer: {raw_value!r}"
        ) from error
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(
            f"periods-per-year must be a positive integer: {raw_value!r}"
        )
    return value


def round_list(values: list[float]) -> list[float]:
    return [round(value, 10) for value in values]


def round_mapping(values: dict[str, float]) -> dict[str, float]:
    return {key: round(value, 10) for key, value in values.items()}


def round_or_none(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 10)


if __name__ == "__main__":
    raise SystemExit(main())
