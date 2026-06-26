"""CLI entry point — thin layer that orchestrates domain modules."""

from __future__ import annotations

import json
import logging
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import click
import numpy as np
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from mpt_portfolio import __version__
from mpt_portfolio.backtest import run_all_backtests
from mpt_portfolio.charts import (
    chart_correlation_heatmap,
    chart_drawdown,
    chart_efficient_frontier,
    chart_equity_curves,
    chart_rolling_sharpe,
    chart_weights_pie,
    export_chart_png,
)
from mpt_portfolio.config import (
    Config,
    ConfigValidationError,
    create_portfolio_from_config,
    load_portfolio_config,
    save_portfolio_config,
    validate_config,
)
from mpt_portfolio.data import (
    DataFetchError,
    DataSufficiencyReport,
    DataValidationError,
    _fetch_raw_prices,
    cache_prices,
    check_data_sufficiency,
    fetch_prices,
    get_risk_free_rate,
    load_cached_prices,
    validate_price_data,
)
from mpt_portfolio.metrics import (
    compare_metrics,
    compute_drawdown_series,
    compute_metrics,
    compute_rolling_sharpe,
)
from mpt_portfolio.optimization import (
    EfficientFrontierResult,
    OptimizationError,
    efficient_frontier,
    optimize,
)
from mpt_portfolio.rebalance import apply_rebalance, check_rebalance
from mpt_portfolio.reports import (
    generate_html_report,
    generate_rebalance_report,
    generate_status_report,
    generate_terminal_report,
)
from mpt_portfolio.notifications import (
    notify_backtest_complete,
    notify_performance_report,
    notify_portfolio_created,
    notify_rebalance_reminder,
)
from mpt_portfolio.returns import compute_log_returns, get_expected_returns
from mpt_portfolio.risk import correlation_matrix, get_covariance
from mpt_portfolio.tracker import (
    compute_current_value,
    initialize_state,
    load_state,
    update_performance_history,
)
from mpt_portfolio.utils import (
    DEFAULT_ASSETS,
    get_portfolio_reports_dir,
    get_portfolios_dir,
    validate_portfolio_name,
)

console = Console()
logger = logging.getLogger("mpt_portfolio")


def _emit_json(data: dict) -> None:
    """Emit machine-parseable JSON block for LLM consumption."""
    print("\n---JSON---")
    print(json.dumps(data, indent=2, default=str))
    print("---JSON---")


def _fetch_data(config: Config) -> pd.DataFrame:
    """Fetch or load cached price data for a portfolio's assets + benchmark.

    Fetches lookback_years + backtest_years of history so the backtest has
    a full lookback window available from day one of the backtest period.
    """
    cached = load_cached_prices(config.portfolio.name)
    if cached is not None:
        console.print("[dim]Using cached price data[/dim]")
        return cached

    end_date = datetime.now(timezone.utc)
    total_years = config.data.lookback_years + config.backtest.backtest_years
    start_date = end_date - timedelta(days=int(total_years * 365.25) + 30)

    all_tickers = list(config.portfolio.assets) + [config.portfolio.benchmark]
    all_tickers = list(dict.fromkeys(all_tickers))

    console.print(f"[dim]Fetching price data for {len(all_tickers)} tickers...[/dim]")
    raw_prices = _fetch_raw_prices(all_tickers, start_date, end_date, config.data.price_type)

    report = check_data_sufficiency(
        raw_prices, config.data.lookback_years, config.backtest.backtest_years,
    )
    if not report.all_sufficient:
        _print_data_sufficiency_warning(report, config)
        _emit_json({
            "status": "warning",
            "type": "data_sufficiency",
            "insufficient_assets": report.insufficient_assets,
            "effective_common_days": report.effective_common_days,
            "required_days": report.required_days,
            "suggested_max_years": report.suggested_max_years,
            "assets": [
                {"ticker": a.ticker, "available_days": a.available_days,
                 "required_days": a.required_days, "sufficient": a.sufficient,
                 "first_date": a.first_date}
                for a in report.assets
            ],
        })

    prices = raw_prices[all_tickers].dropna()
    prices.index = pd.DatetimeIndex(prices.index)
    cache_prices(prices, config.portfolio.name)
    return prices


def _print_data_sufficiency_warning(
    report: DataSufficiencyReport, config: Config,
) -> None:
    """Print a warning table for assets with insufficient history."""
    from rich.table import Table as RichTable

    console.print()
    console.print(Panel(
        f"[bold yellow]Data Sufficiency Warning[/bold yellow]\n"
        f"Requested: {config.data.lookback_years}yr lookback + "
        f"{config.backtest.backtest_years}yr backtest = "
        f"{report.required_days} trading days needed\n"
        f"Effective common data: {report.effective_common_days} days "
        f"({report.suggested_max_years:.1f} years)",
        title="Data Check",
        border_style="yellow",
    ))

    table = RichTable(show_lines=False)
    table.add_column("Asset", style="bold")
    table.add_column("Available", justify="right")
    table.add_column("Required", justify="right")
    table.add_column("First Date", justify="right")
    table.add_column("Status")

    for a in report.assets:
        status = "[green]OK[/green]" if a.sufficient else "[red]Insufficient[/red]"
        table.add_row(
            a.ticker,
            str(a.available_days),
            str(a.required_days),
            a.first_date or "-",
            status,
        )
    console.print(table)

    if report.insufficient_assets:
        console.print(
            f"\n[yellow]Suggestion:[/yellow] Remove {', '.join(report.insufficient_assets)} "
            f"or reduce lookback+backtest to ~{report.suggested_max_years:.0f} years total.\n"
            f"The backtest will proceed with the overlapping data window "
            f"({report.effective_common_days} days)."
        )
    console.print()


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(verbose: bool) -> None:
    """Modern Portfolio Theory Portfolio Optimizer."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


@main.command()
@click.option("--portfolio", "-p", required=True, help="Portfolio name")
@click.option("--config-file", type=click.Path(exists=True), help="Path to config YAML")
@click.option("--interactive/--no-interactive", default=True)
def setup(portfolio: str, config_file: str | None, interactive: bool) -> None:
    """Create a new portfolio with configuration."""
    try:
        validate_portfolio_name(portfolio)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    portfolio_dir = get_portfolios_dir() / portfolio
    if portfolio_dir.exists():
        console.print(f"[red]Error:[/red] Portfolio '{portfolio}' already exists.")
        sys.exit(1)

    if config_file:
        import yaml
        with open(config_file) as f:
            raw = yaml.safe_load(f)
        raw.setdefault("portfolio", {})["name"] = portfolio
        try:
            config = validate_config(raw)
        except ConfigValidationError as e:
            console.print(f"[red]Config error:[/red] {e}")
            sys.exit(1)
    elif interactive:
        console.print(f"\n[bold]Setting up portfolio: {portfolio}[/bold]\n")

        investment = float(Prompt.ask("Initial investment amount", default="100000"))
        asset_input = Prompt.ask(
            "Assets (comma-separated tickers, or 'default' for sector ETFs)",
            default="default",
        )
        if asset_input.lower() == "default":
            assets = list(DEFAULT_ASSETS)
        else:
            assets = [t.strip().upper() for t in asset_input.split(",") if t.strip()]

        benchmark = Prompt.ask("Benchmark ticker", default="SPY")
        lookback = int(Prompt.ask("Lookback years (for estimating returns/covariance)", default="5"))
        backtest_years = int(Prompt.ask(
            "Backtest simulation years (how many years to test strategies)",
            default="5",
        ))

        price_type = Prompt.ask(
            "Price type: 'adjusted' (total return, recommended) or 'unadjusted' (price only)",
            default="adjusted",
        )

        method = Prompt.ask(
            "Optimization method (max_sharpe / min_variance / risk_parity)",
            default="max_sharpe",
        )

        long_only = Confirm.ask("Long-only (no short selling)?", default=True)
        max_weight = float(Prompt.ask("Maximum weight per asset (0-1)", default="0.40"))

        monitoring_freq = Prompt.ask(
            "Performance monitoring frequency (weekly / monthly / none)",
            default="none",
        )

        console.print(
            "\n[bold blue]Email Notifications (optional)[/bold blue]\n"
            "To receive portfolio reports by email, edit the [bold]email[/bold] section\n"
            f"in [bold]portfolios/{portfolio}/config.yaml[/bold] after setup.\n"
            "Fill in your SMTP details and set [bold]notifications.method[/bold] to "
            '"email" or "both".\n'
        )

        from mpt_portfolio.config import load_default_config
        raw = load_default_config()
        raw["portfolio"] = {
            "name": portfolio,
            "initial_investment": investment,
            "assets": assets,
            "benchmark": benchmark,
        }
        raw["data"]["lookback_years"] = lookback
        raw["data"]["price_type"] = price_type
        raw["backtest"]["backtest_years"] = backtest_years
        raw["optimization"]["method"] = method
        raw["optimization"]["constraints"]["long_only"] = long_only
        raw["optimization"]["constraints"]["max_weight"] = max_weight
        raw.setdefault("monitoring", {})["frequency"] = monitoring_freq
        config = validate_config(raw)
    else:
        from mpt_portfolio.config import load_default_config
        raw = load_default_config()
        raw.setdefault("portfolio", {})["name"] = portfolio
        config = validate_config(raw)

    create_portfolio_from_config(config)
    console.print(f"\n[green]Portfolio '{portfolio}' created successfully![/green]")
    console.print(f"Config: {portfolio_dir / 'config.yaml'}")
    console.print(f"Next: run [bold]python -m mpt_portfolio optimize -p {portfolio}[/bold]")
    _print_schedule_recommendation(portfolio, config.rebalancing.strategy, config.monitoring.frequency)

    _emit_json({
        "status": "success", "command": "setup", "portfolio": portfolio,
        "assets": config.portfolio.assets, "benchmark": config.portfolio.benchmark,
        "method": config.optimization.method,
        "backtest_years": config.backtest.backtest_years,
        "monitoring_frequency": config.monitoring.frequency,
    })


@main.command()
@click.option("--portfolio", "-p", required=True)
@click.option("--method", type=click.Choice(["max_sharpe", "min_variance", "efficient_frontier", "risk_parity"]))
@click.option("--save-state/--no-save-state", default=True)
@click.option("--auto-report/--no-auto-report", default=True, help="Automatically run backtest and generate full report")
def opt(portfolio: str, method: str | None, save_state: bool, auto_report: bool) -> None:
    """Run portfolio optimization and display results."""
    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if method:
        config.optimization.method = method

    try:
        prices = _fetch_data(config)
    except DataFetchError as e:
        console.print(f"[red]Data error:[/red] {e}")
        sys.exit(1)

    asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
    if not asset_tickers:
        console.print("[red]Error:[/red] None of the configured assets found in price data.")
        sys.exit(1)

    asset_prices = prices[asset_tickers]
    try:
        validate_price_data(asset_prices)
    except DataValidationError as e:
        console.print(f"[red]Data error:[/red] {e}")
        sys.exit(1)

    log_returns = compute_log_returns(asset_prices)
    mu = get_expected_returns(log_returns, config.optimization.expected_returns)
    cov = get_covariance(log_returns, config.optimization.covariance)
    rf = get_risk_free_rate(config.optimization.risk_free_rate)

    try:
        result = optimize(mu, cov, rf, config.optimization.method, config.optimization.constraints)
    except OptimizationError as e:
        console.print(f"[red]Optimization error:[/red] {e}")
        sys.exit(1)

    # Determine main result for display
    if isinstance(result, EfficientFrontierResult):
        main_result = result.max_sharpe_portfolio
        ef_result = result
    else:
        main_result = result
        ef_result = efficient_frontier(mu, cov, rf, config.optimization.constraints, n_points=100)

    asset_vols = pd.Series(np.sqrt(np.diag(cov.values)), index=cov.index)
    corr = correlation_matrix(cov)
    latest_prices = prices[asset_tickers].iloc[-1]
    investment = config.portfolio.initial_investment

    # Generate charts
    charts = {}
    individual_assets = {t: (asset_vols[t], mu[t]) for t in asset_tickers}
    charts["efficient_frontier"] = chart_efficient_frontier(
        ef_result.frontier_returns, ef_result.frontier_volatilities,
        min_var={"return": ef_result.min_variance_portfolio.expected_return,
                 "volatility": ef_result.min_variance_portfolio.volatility},
        max_sharpe={"return": ef_result.max_sharpe_portfolio.expected_return,
                    "volatility": ef_result.max_sharpe_portfolio.volatility},
        individual_assets=individual_assets,
        risk_free_rate=rf,
    )
    charts["correlation_heatmap"] = chart_correlation_heatmap(corr)
    charts["weights"] = chart_weights_pie(main_result.weights)

    # Terminal report
    generate_terminal_report(
        portfolio, config.optimization.method,
        main_result.weights, mu, asset_vols,
        main_result.sharpe_ratio, main_result.expected_return,
        main_result.volatility, rf,
        latest_prices=latest_prices,
        investment_amount=investment,
    )

    # HTML report
    html_report_path = None
    if "html" in config.reports.formats:
        metrics = compute_metrics(
            prices[asset_tickers].iloc[-252:].mean(axis=1),  # proxy
            rf,
        )
        html_report_path = generate_html_report(
            portfolio, config.optimization.method,
            main_result.weights, mu, asset_vols,
            charts=charts,
            latest_prices=latest_prices,
            investment_amount=investment,
        )
        console.print(f"[dim]HTML report: {html_report_path}[/dim]")

    # Save PNG charts
    reports_dir = get_portfolio_reports_dir(portfolio)
    for name, fig in charts.items():
        if fig is not None:
            export_chart_png(fig, reports_dir / f"{name}.png")

    # Initialize portfolio state
    if save_state:
        initialize_state(
            portfolio, investment,
            main_result.weights, latest_prices,
            config.optimization.method,
        )
        console.print("[dim]Portfolio state initialized.[/dim]")

    # Build quantity data for JSON
    qty_data = {}
    for ticker, weight in main_result.weights.items():
        if abs(weight) < 0.001:
            continue
        price = latest_prices.get(ticker, 0)
        if price > 0:
            alloc = investment * float(weight)
            exact = alloc / price
            qty_data[ticker] = {
                "weight": round(float(weight), 6),
                "price": round(float(price), 2),
                "exact_shares": round(exact, 4),
                "whole_shares": int(exact),
            }
    residual = investment - sum(
        v["whole_shares"] * latest_prices.get(k, 0)
        for k, v in qty_data.items()
    )

    _emit_json({
        "status": "success", "command": "optimize", "portfolio": portfolio,
        "method": config.optimization.method,
        "expected_return": round(main_result.expected_return, 6),
        "volatility": round(main_result.volatility, 6),
        "sharpe_ratio": round(main_result.sharpe_ratio, 4),
        "risk_free_rate": round(rf, 4),
        "investment_amount": investment,
        "weights": {k: round(float(v), 6) for k, v in main_result.weights.items() if abs(v) > 0.001},
        "quantities": qty_data,
        "residual_cash_whole_shares": round(float(residual), 2),
    })

    try:
        notify_portfolio_created(
            portfolio, config, config.optimization.method,
            {k: round(float(v), 6) for k, v in main_result.weights.items() if abs(v) > 0.001},
            main_result.expected_return, main_result.volatility,
            main_result.sharpe_ratio, rf, investment, qty_data, html_report_path,
        )
    except Exception as e:
        logger.warning(f"Portfolio created notification failed: {e}")

    if auto_report:
        try:
            comparison, best_result = _run_backtest_and_report(portfolio, config, prices)
            _emit_json({
                "status": "success", "command": "backtest", "portfolio": portfolio,
                "recommended_strategy": comparison.recommended_strategy,
                "recommendation_reason": comparison.recommendation_reason,
                "strategies": {
                    name: {
                        "total_return": round(r.metrics.total_return, 4),
                        "cagr": round(r.metrics.cagr, 4),
                        "sharpe": round(r.metrics.sharpe_ratio, 4),
                        "max_drawdown": round(r.metrics.max_drawdown, 4),
                        "turnover": round(r.total_turnover, 4),
                        "costs": round(r.total_transaction_costs, 2),
                    }
                    for name, r in comparison.results.items()
                },
                "rebalance_history": [
                    {
                        "date": ev.date.strftime("%Y-%m-%d"),
                        "weights": {t: round(w, 4) for t, w in ev.new_weights.items() if abs(w) > 0.001},
                        "turnover": round(ev.turnover, 4),
                    }
                    for ev in best_result.rebalance_events
                ],
            })
        except Exception as e:
            console.print(f"[yellow]Warning: Auto-report failed: {e}[/yellow]")


def _run_backtest_and_report(portfolio: str, config: Config, prices: pd.DataFrame):
    """Run all backtests, generate charts/reports. Returns (comparison, best_result)."""
    console.print("[bold]Running backtests...[/bold]")
    comparison = run_all_backtests(prices, config)

    all_metrics = {name: r.metrics for name, r in comparison.results.items()}
    all_metrics[f"Benchmark ({config.portfolio.benchmark})"] = comparison.benchmark_result.metrics
    bt_table = compare_metrics(all_metrics)

    recommendation = {
        "strategy": comparison.recommended_strategy,
        "reason": comparison.recommendation_reason,
    }

    rf = get_risk_free_rate(config.optimization.risk_free_rate)
    equity_curves = {name: r.portfolio_values for name, r in comparison.results.items()}
    benchmark_values = comparison.benchmark_result.portfolio_values
    drawdowns = {name: compute_drawdown_series(r.portfolio_values) for name, r in comparison.results.items()}
    rolling_sharpes = {}
    for name, r in comparison.results.items():
        if len(r.daily_returns) > 63:
            rolling_sharpes[name] = compute_rolling_sharpe(r.daily_returns, rf)

    charts = {
        "equity_curves": chart_equity_curves(equity_curves, benchmark_values, config.portfolio.benchmark),
        "drawdown": chart_drawdown(drawdowns),
        "rolling_sharpe": chart_rolling_sharpe(rolling_sharpes) if rolling_sharpes else None,
    }

    asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
    log_returns = compute_log_returns(prices[asset_tickers])
    mu = get_expected_returns(log_returns, config.optimization.expected_returns)
    cov = get_covariance(log_returns, config.optimization.covariance)
    asset_vols = pd.Series(np.sqrt(np.diag(cov.values)), index=cov.index)

    best_result = comparison.results[comparison.recommended_strategy]
    generate_terminal_report(
        portfolio, f"Backtest ({comparison.recommended_strategy})",
        best_result.weights_over_time.iloc[-1] if len(best_result.weights_over_time) > 0 else pd.Series(dtype=float),
        mu, asset_vols,
        best_result.metrics.sharpe_ratio, best_result.metrics.cagr,
        best_result.metrics.annualized_volatility, rf,
        backtest_comparison=bt_table,
        recommendation=recommendation,
        rebalance_events=best_result.rebalance_events,
    )

    if "html" in config.reports.formats:
        weights = best_result.weights_over_time.iloc[-1] if len(best_result.weights_over_time) > 0 else pd.Series(dtype=float)
        path = generate_html_report(
            portfolio, "Backtest",
            weights, mu, asset_vols,
            metrics=best_result.metrics,
            charts=charts,
            backtest_comparison=bt_table,
            recommendation=recommendation,
            rebalance_events=best_result.rebalance_events,
        )
        console.print(f"[dim]HTML report: {path}[/dim]")

    reports_dir = get_portfolio_reports_dir(portfolio)
    for name, fig in charts.items():
        if fig is not None:
            export_chart_png(fig, reports_dir / f"backtest_{name}.png")

    if config.rebalancing.strategy == "recommended":
        config.rebalancing.strategy = comparison.recommended_strategy
        save_portfolio_config(portfolio, config)
        console.print(f"[dim]Rebalancing strategy set to: {comparison.recommended_strategy}[/dim]")
        _print_schedule_recommendation(portfolio, comparison.recommended_strategy, config.monitoring.frequency)

    bt_html_path = None
    if "html" in config.reports.formats:
        html_files = sorted(reports_dir.glob("report_*.html"), reverse=True)
        if html_files:
            bt_html_path = html_files[0]
    try:
        notify_backtest_complete(
            portfolio, config,
            comparison.recommended_strategy,
            comparison.recommendation_reason,
            {
                name: {
                    "total_return": r.metrics.total_return,
                    "cagr": r.metrics.cagr,
                    "sharpe": r.metrics.sharpe_ratio,
                    "max_drawdown": r.metrics.max_drawdown,
                    "turnover": r.total_turnover,
                    "costs": r.total_transaction_costs,
                }
                for name, r in comparison.results.items()
            },
            bt_html_path,
        )
    except Exception as e:
        logger.warning(f"Backtest notification failed: {e}")

    return comparison, best_result


@main.command()
@click.option("--portfolio", "-p", required=True)
def backtest(portfolio: str) -> None:
    """Run backtesting comparison across rebalancing strategies."""
    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    try:
        prices = _fetch_data(config)
    except DataFetchError as e:
        console.print(f"[red]Data error:[/red] {e}")
        sys.exit(1)

    comparison, best_result = _run_backtest_and_report(portfolio, config, prices)

    _emit_json({
        "status": "success", "command": "backtest", "portfolio": portfolio,
        "recommended_strategy": comparison.recommended_strategy,
        "recommendation_reason": comparison.recommendation_reason,
        "strategies": {
            name: {
                "total_return": round(r.metrics.total_return, 4),
                "cagr": round(r.metrics.cagr, 4),
                "sharpe": round(r.metrics.sharpe_ratio, 4),
                "max_drawdown": round(r.metrics.max_drawdown, 4),
                "turnover": round(r.total_turnover, 4),
                "costs": round(r.total_transaction_costs, 2),
            }
            for name, r in comparison.results.items()
        },
        "rebalance_history": [
            {
                "date": ev.date.strftime("%Y-%m-%d"),
                "weights": {t: round(w, 4) for t, w in ev.new_weights.items() if abs(w) > 0.001},
                "turnover": round(ev.turnover, 4),
            }
            for ev in best_result.rebalance_events
        ],
    })


@main.command()
@click.option("--portfolio", "-p", required=True)
def status(portfolio: str) -> None:
    """Show current portfolio status."""
    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    state = load_state(portfolio)
    if state is None:
        console.print(f"[yellow]No state found for '{portfolio}'. Run optimize first.[/yellow]")
        sys.exit(1)

    try:
        prices = _fetch_data(config)
    except DataFetchError as e:
        console.print(f"[red]Data error:[/red] {e}")
        sys.exit(1)

    asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
    latest_prices = prices[asset_tickers].iloc[-1]
    total_value, current_weights = compute_current_value(state, latest_prices)
    target_weights = pd.Series(state.target_weights)
    portfolio_return = (total_value / state.initial_investment) - 1.0

    bm_ticker = config.portfolio.benchmark
    if bm_ticker in prices.columns:
        bm_prices = prices[bm_ticker]
        bm_return = (bm_prices.iloc[-1] / bm_prices.iloc[-252]) - 1.0 if len(bm_prices) > 252 else 0.0
    else:
        bm_return = 0.0

    current_values = {}
    for ticker, holding in state.holdings.items():
        price = latest_prices.get(ticker, 0)
        current_values[ticker] = holding["shares"] * price

    generate_status_report(
        portfolio, state.holdings, current_values,
        total_value, current_weights, target_weights,
        bm_return, portfolio_return,
    )

    update_performance_history(
        portfolio, latest_prices,
        prices[bm_ticker].iloc[-1] if bm_ticker in prices.columns else None,
    )

    _emit_json({
        "status": "success", "command": "status", "portfolio": portfolio,
        "total_value": round(total_value, 2),
        "portfolio_return": round(portfolio_return, 4),
        "benchmark_return": round(bm_return, 4),
        "cash": round(state.cash, 2),
        "max_drift": round(float((current_weights.reindex(target_weights.index, fill_value=0) - target_weights).abs().max()), 4) if len(target_weights) > 0 else 0,
    })


@main.command("rebalance")
@click.option("--portfolio", "-p", required=True)
@click.option("--execute/--dry-run", default=False)
def rebalance_cmd(portfolio: str, execute: bool) -> None:
    """Check if rebalancing is needed and generate orders."""
    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    try:
        prices = _fetch_data(config)
    except DataFetchError as e:
        console.print(f"[red]Data error:[/red] {e}")
        sys.exit(1)

    result = check_rebalance(portfolio, config, prices)

    generate_rebalance_report(
        result.needs_rebalance, result.reason,
        result.max_drift, result.max_drift_asset,
        result.orders, result.estimated_cost,
    )

    if execute and result.needs_rebalance:
        asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
        latest_prices = prices[asset_tickers].iloc[-1]
        apply_rebalance(
            portfolio, result.orders, result.target_weights,
            latest_prices, config.optimization.method,
            result.estimated_cost,
        )
        console.print("[green]Rebalance applied to portfolio state.[/green]")

    _emit_json({
        "status": "success", "command": "rebalance", "portfolio": portfolio,
        "needs_rebalance": result.needs_rebalance,
        "reason": result.reason,
        "max_drift": round(result.max_drift, 4),
        "max_drift_asset": result.max_drift_asset,
        "estimated_cost": round(result.estimated_cost, 2),
        "orders": [
            {"ticker": o.ticker, "action": o.action, "shares": o.shares_rounded,
             "amount": round(o.dollar_amount, 2)}
            for o in result.orders
        ],
    })

    try:
        notify_rebalance_reminder(
            portfolio, config, result.needs_rebalance, result.reason,
            result.max_drift, result.max_drift_asset,
            result.orders, result.estimated_cost,
        )
    except Exception as e:
        logger.warning(f"Rebalance notification failed: {e}")


@main.command()
@click.option("--portfolio", "-p", required=True)
@click.option("--format", "fmt", type=click.Choice(["html", "terminal", "both"]), default="both")
def report(portfolio: str, fmt: str) -> None:
    """Generate full performance report."""
    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    try:
        prices = _fetch_data(config)
    except DataFetchError as e:
        console.print(f"[red]Data error:[/red] {e}")
        sys.exit(1)

    asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
    log_returns = compute_log_returns(prices[asset_tickers])
    mu = get_expected_returns(log_returns, config.optimization.expected_returns)
    cov = get_covariance(log_returns, config.optimization.covariance)
    rf = get_risk_free_rate(config.optimization.risk_free_rate)
    asset_vols = pd.Series(np.sqrt(np.diag(cov.values)), index=cov.index)
    latest_prices = prices[asset_tickers].iloc[-1]
    investment = config.portfolio.initial_investment

    opt_method = config.optimization.method
    if opt_method == "efficient_frontier":
        opt_method = "max_sharpe"

    result = optimize(mu, cov, rf, opt_method, config.optimization.constraints)
    if hasattr(result, "max_sharpe_portfolio"):
        result = result.max_sharpe_portfolio

    if fmt in ("terminal", "both"):
        generate_terminal_report(
            portfolio, config.optimization.method,
            result.weights, mu, asset_vols,
            result.sharpe_ratio, result.expected_return,
            result.volatility, rf,
            latest_prices=latest_prices,
            investment_amount=investment,
        )

    if fmt in ("html", "both"):
        corr = correlation_matrix(cov)
        ef = efficient_frontier(mu, cov, rf, config.optimization.constraints)
        individual_assets = {t: (asset_vols[t], mu[t]) for t in asset_tickers}
        charts = {
            "efficient_frontier": chart_efficient_frontier(
                ef.frontier_returns, ef.frontier_volatilities,
                min_var={"return": ef.min_variance_portfolio.expected_return,
                         "volatility": ef.min_variance_portfolio.volatility},
                max_sharpe={"return": ef.max_sharpe_portfolio.expected_return,
                            "volatility": ef.max_sharpe_portfolio.volatility},
                individual_assets=individual_assets, risk_free_rate=rf,
            ),
            "correlation_heatmap": chart_correlation_heatmap(corr),
            "weights": chart_weights_pie(result.weights),
        }
        path = generate_html_report(
            portfolio, config.optimization.method,
            result.weights, mu, asset_vols, charts=charts,
            latest_prices=latest_prices,
            investment_amount=investment,
        )
        console.print(f"[dim]HTML report: {path}[/dim]")

    _emit_json({"status": "success", "command": "report", "portfolio": portfolio})


@main.command()
@click.option("--portfolio", "-p", required=True)
@click.option("--format", "fmt", type=click.Choice(["html", "terminal", "both"]), default="both")
def performance(portfolio: str, fmt: str) -> None:
    """Generate on-demand performance report from live portfolio data."""
    from mpt_portfolio.reports import (
        generate_performance_html_report,
        generate_performance_terminal_report,
    )

    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    state = load_state(portfolio)
    if state is None:
        console.print(f"[yellow]No state found for '{portfolio}'. Run optimize first.[/yellow]")
        sys.exit(1)

    if len(state.performance_history) < 2:
        console.print(
            f"[yellow]Only {len(state.performance_history)} data point(s) in performance history.[/yellow]\n"
            f"Run [bold]python -m mpt_portfolio status -p {portfolio}[/bold] to record snapshots, "
            f"or set up the cron job for automated monitoring."
        )
        sys.exit(1)

    try:
        prices = _fetch_data(config)
    except DataFetchError as e:
        console.print(f"[red]Data error:[/red] {e}")
        sys.exit(1)

    portfolio_values = pd.Series(
        {pd.Timestamp(e["date"]): e["portfolio_value"] for e in state.performance_history},
    ).sort_index()

    benchmark_values = None
    if any("benchmark_price" in e for e in state.performance_history):
        bm_entries = {
            pd.Timestamp(e["date"]): e["benchmark_price"]
            for e in state.performance_history if "benchmark_price" in e
        }
        if bm_entries:
            benchmark_values = pd.Series(bm_entries).sort_index()

    rf = get_risk_free_rate(config.optimization.risk_free_rate)
    metrics = compute_metrics(portfolio_values, rf)

    portfolio_return = (portfolio_values.iloc[-1] / portfolio_values.iloc[0]) - 1.0
    benchmark_return = None
    if benchmark_values is not None and len(benchmark_values) >= 2:
        benchmark_return = (benchmark_values.iloc[-1] / benchmark_values.iloc[0]) - 1.0

    # Compute current holdings values
    asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
    latest_prices = prices[asset_tickers].iloc[-1]
    total_value, _ = compute_current_value(state, latest_prices)
    current_values = {}
    for ticker, holding in state.holdings.items():
        price = latest_prices.get(ticker, 0)
        current_values[ticker] = holding["shares"] * price

    live_start_date = None
    if state.optimization_date:
        live_start_date = pd.Timestamp(state.optimization_date[:10])

    live_days = (portfolio_values.index[-1] - portfolio_values.index[0]).days

    # Generate charts
    equity_curves = {"Portfolio": portfolio_values}
    charts = {}
    charts["equity_curves"] = chart_equity_curves(
        equity_curves,
        benchmark=benchmark_values,
        benchmark_ticker=config.portfolio.benchmark,
        live_start_date=live_start_date,
    )

    dd_series = compute_drawdown_series(portfolio_values)
    charts["drawdown"] = chart_drawdown({"Portfolio": dd_series})

    if len(portfolio_values) > 63:
        daily_returns = portfolio_values.pct_change().dropna()
        rs = compute_rolling_sharpe(daily_returns, rf)
        charts["rolling_sharpe"] = chart_rolling_sharpe({"Portfolio": rs})

    if fmt in ("terminal", "both"):
        generate_performance_terminal_report(
            portfolio, metrics, total_value, portfolio_return,
            benchmark_return, live_days, len(state.rebalance_history),
            state.holdings, current_values,
        )

    if fmt in ("html", "both"):
        path = generate_performance_html_report(
            portfolio, metrics, state, config.portfolio.benchmark,
            charts=charts, current_values=current_values,
            total_value=total_value, portfolio_return=portfolio_return,
            benchmark_return=benchmark_return,
        )
        console.print(f"[dim]Performance report: {path}[/dim]")

    reports_dir = get_portfolio_reports_dir(portfolio)
    for name, fig in charts.items():
        if fig is not None:
            export_chart_png(fig, reports_dir / f"performance_{name}.png")

    _emit_json({
        "status": "success", "command": "performance", "portfolio": portfolio,
        "total_value": round(total_value, 2),
        "portfolio_return": round(portfolio_return, 4),
        "benchmark_return": round(benchmark_return, 4) if benchmark_return is not None else None,
        "live_days": live_days,
        "rebalance_count": len(state.rebalance_history),
        "sharpe": round(metrics.sharpe_ratio, 4),
        "cagr": round(metrics.cagr, 4),
        "max_drawdown": round(metrics.max_drawdown, 4),
        "volatility": round(metrics.annualized_volatility, 4),
    })

    perf_html_path = None
    if fmt in ("html", "both"):
        html_files = sorted(reports_dir.glob("performance_*.html"), reverse=True)
        if html_files:
            perf_html_path = html_files[0]
    try:
        notify_performance_report(
            portfolio, config, total_value, portfolio_return, benchmark_return,
            metrics.sharpe_ratio, metrics.cagr, metrics.max_drawdown,
            metrics.annualized_volatility, live_days,
            len(state.rebalance_history), perf_html_path,
        )
    except Exception as e:
        logger.warning(f"Performance notification failed: {e}")


@main.command("update-data")
@click.option("--portfolio", "-p", required=True)
def update_data(portfolio: str) -> None:
    """Refresh cached price data."""
    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    # Force fresh fetch by not using cache
    end_date = datetime.now(timezone.utc)
    total_years = config.data.lookback_years + config.backtest.backtest_years
    start_date = end_date - timedelta(days=int(total_years * 365.25) + 30)
    all_tickers = list(config.portfolio.assets) + [config.portfolio.benchmark]
    all_tickers = list(dict.fromkeys(all_tickers))

    console.print(f"Fetching fresh data for {len(all_tickers)} tickers...")
    try:
        prices = fetch_prices(all_tickers, start_date, end_date, config.data.price_type)
        cache_prices(prices, portfolio)
        console.print(f"[green]Data updated: {len(prices)} trading days, {len(prices.columns)} tickers[/green]")
    except DataFetchError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    _emit_json({
        "status": "success", "command": "update-data", "portfolio": portfolio,
        "rows": len(prices), "tickers": list(prices.columns),
    })


@main.command()
@click.option("--portfolio", "-p", required=True)
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
def delete(portfolio: str, force: bool) -> None:
    """Delete a portfolio and all its data."""
    portfolio_dir = get_portfolios_dir() / portfolio
    if not portfolio_dir.exists():
        console.print(f"[red]Error:[/red] Portfolio '{portfolio}' does not exist.")
        sys.exit(1)

    if not force:
        confirmed = Confirm.ask(
            f"Delete portfolio '{portfolio}' and all its data (config, state, reports)?",
            default=False,
        )
        if not confirmed:
            console.print("[dim]Cancelled.[/dim]")
            return

    shutil.rmtree(portfolio_dir)
    console.print(f"[green]Portfolio '{portfolio}' deleted.[/green]")

    _emit_json({"status": "success", "command": "delete", "portfolio": portfolio})


@main.command("modify-assets")
@click.option("--portfolio", "-p", required=True, help="Portfolio name")
@click.option("--add", "add_tickers", default="", help="Comma-separated tickers to add")
@click.option("--remove", "remove_tickers", default="", help="Comma-separated tickers to remove")
def modify_assets(portfolio: str, add_tickers: str, remove_tickers: str) -> None:
    """Add or remove assets from a portfolio for subsequent rebalancing."""
    try:
        config = load_portfolio_config(portfolio)
    except (FileNotFoundError, ConfigValidationError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    to_add = [t.strip().upper() for t in add_tickers.split(",") if t.strip()]
    to_remove = [t.strip().upper() for t in remove_tickers.split(",") if t.strip()]

    if not to_add and not to_remove:
        console.print("[red]Error:[/red] Provide --add and/or --remove tickers.")
        sys.exit(1)

    current = list(config.portfolio.assets)

    not_found = [t for t in to_remove if t not in current]
    if not_found:
        console.print(f"[red]Error:[/red] Tickers not in portfolio: {', '.join(not_found)}")
        sys.exit(1)

    already = [t for t in to_add if t in current]
    if already:
        console.print(f"[yellow]Warning:[/yellow] Already in portfolio (skipping): {', '.join(already)}")
        to_add = [t for t in to_add if t not in current]

    for t in to_remove:
        current.remove(t)
    current.extend(to_add)

    if not current:
        console.print("[red]Error:[/red] Cannot remove all assets.")
        sys.exit(1)

    config.portfolio.assets = current
    save_portfolio_config(portfolio, config)

    portfolio_dir = get_portfolios_dir() / portfolio
    (portfolio_dir / "price_cache.parquet").unlink(missing_ok=True)
    (portfolio_dir / "price_cache.csv").unlink(missing_ok=True)

    console.print(f"[green]Assets updated for '{portfolio}'[/green]")
    console.print(f"  Added: {', '.join(to_add) if to_add else 'none'}")
    console.print(f"  Removed: {', '.join(to_remove) if to_remove else 'none'}")
    console.print(f"  Current assets ({len(current)}): {', '.join(current)}")
    console.print("[dim]Price cache cleared. Next rebalance will use updated assets.[/dim]")

    _emit_json({
        "status": "success", "command": "modify-assets", "portfolio": portfolio,
        "added": to_add, "removed": to_remove, "current_assets": current,
    })


@main.command()
@click.option("--portfolio", "-p", multiple=True, required=True, help="Portfolio names to compare (use -p multiple times)")
def compare(portfolio: tuple[str, ...]) -> None:
    """Compare multiple portfolios side by side."""
    if len(portfolio) < 2:
        console.print("[red]Error:[/red] Provide at least 2 portfolios to compare (e.g. -p port1 -p port2).")
        sys.exit(1)

    from rich.table import Table
    table = Table(title="Portfolio Comparison")
    table.add_column("Metric", style="bold")
    for name in portfolio:
        table.add_column(name, justify="right")

    json_data = {}
    rows = {
        "Total Value": [], "Return": [], "# Holdings": [],
        "Max Drift": [], "Method": [], "Rebalance Strategy": [],
        "Last Rebalanced": [], "Cash": [],
    }

    for name in portfolio:
        try:
            config = load_portfolio_config(name)
        except (FileNotFoundError, ConfigValidationError):
            for key in rows:
                rows[key].append("[dim]Not found[/dim]")
            json_data[name] = {"error": "not found"}
            continue

        state = load_state(name)
        if state is None:
            rows["Total Value"].append("[dim]N/A[/dim]")
            rows["Return"].append("[dim]N/A[/dim]")
            rows["# Holdings"].append("[dim]N/A[/dim]")
            rows["Max Drift"].append("[dim]N/A[/dim]")
            rows["Method"].append(config.optimization.method)
            rows["Rebalance Strategy"].append(config.rebalancing.strategy)
            rows["Last Rebalanced"].append("[dim]N/A[/dim]")
            rows["Cash"].append("[dim]N/A[/dim]")
            json_data[name] = {"status": "not initialized", "method": config.optimization.method}
            continue

        try:
            prices = _fetch_data(config)
            asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
            current_prices = prices[asset_tickers].iloc[-1]
            total_value, current_weights = compute_current_value(state, current_prices)

            ret = (total_value / state.initial_investment - 1) if state.initial_investment > 0 else 0
            n_holdings = sum(1 for h in state.holdings.values() if h.get("shares", 0) > 0.001)

            target_w = pd.Series(state.target_weights)
            aligned = current_weights.reindex(target_w.index, fill_value=0.0)
            max_drift = float((aligned - target_w).abs().max()) if len(target_w) > 0 else 0.0

            last_rb = state.rebalance_history[-1]["date"][:10] if state.rebalance_history else state.optimization_date[:10]

            ret_style = "green" if ret >= 0 else "red"
            rows["Total Value"].append(f"${total_value:,.0f}")
            rows["Return"].append(f"[{ret_style}]{ret:+.2%}[/{ret_style}]")
            rows["# Holdings"].append(str(n_holdings))
            rows["Max Drift"].append(f"{max_drift:.2%}")
            rows["Method"].append(config.optimization.method)
            rows["Rebalance Strategy"].append(config.rebalancing.strategy)
            rows["Last Rebalanced"].append(last_rb)
            rows["Cash"].append(f"${state.cash:,.2f}")

            json_data[name] = {
                "total_value": round(total_value, 2),
                "return": round(ret, 4),
                "holdings": n_holdings,
                "max_drift": round(max_drift, 4),
                "method": config.optimization.method,
                "rebalance_strategy": config.rebalancing.strategy,
                "cash": round(state.cash, 2),
            }
        except Exception as e:
            for key in rows:
                rows[key].append(f"[red]Error[/red]")
            json_data[name] = {"error": str(e)}

    for metric, values in rows.items():
        table.add_row(metric, *values)

    console.print()
    console.print(table)
    console.print()

    _emit_json({"status": "success", "command": "compare", "portfolios": json_data})


def _print_schedule_recommendation(
    portfolio_name: str, strategy: str, monitoring_freq: str = "none",
) -> None:
    """Print cron scheduling guidance based on rebalancing strategy."""
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "cron_rebalance.sh"

    cron_lines = {
        "monthly": f"0 9 1-7 * 1-5 {script_path} {portfolio_name}",
        "quarterly": f"0 9 1-7 1,4,7,10 1-5 {script_path} {portfolio_name}",
        "yearly": f"0 9 1-7 1 1-5 {script_path} {portfolio_name}",
        "dynamic": f"0 9 * * 1-5 {script_path} {portfolio_name}",
    }

    descriptions = {
        "monthly": "Runs on the first trading day of each month at 9am.",
        "quarterly": "Runs at the start of each quarter (Jan/Apr/Jul/Oct) at 9am.",
        "yearly": "Runs at the start of each year at 9am.",
        "dynamic": "Runs every weekday at 9am to check portfolio drift.",
    }

    if strategy == "recommended":
        console.print(Panel(
            "Run [bold]backtest[/bold] first to determine the best rebalancing strategy,\n"
            "then scheduling recommendations will be provided.",
            title="Scheduling",
            border_style="dim",
        ))
        return

    cron = cron_lines.get(strategy)
    desc = descriptions.get(strategy)
    if not cron:
        return

    console.print(Panel(
        f"Rebalancing strategy: [bold]{strategy}[/bold]\n\n"
        f"Recommended cron schedule:\n"
        f"  [cyan]{cron}[/cyan]\n\n"
        f"{desc}\n"
        f"To install: run [bold]crontab -e[/bold] and add the line above.\n"
        f"Notifications will be sent via your configured method.",
        title="Scheduling Recommendation",
        border_style="blue",
    ))

    if monitoring_freq != "none":
        perf_script = Path(__file__).resolve().parent.parent / "scripts" / "cron_performance.sh"
        perf_crons = {
            "weekly": f"0 9 * * 1 {perf_script} {portfolio_name}",
            "monthly": f"0 9 1-7 * 1-5 {perf_script} {portfolio_name}",
        }
        perf_descs = {
            "weekly": "Generates a performance report every Monday at 9am.",
            "monthly": "Generates a performance report on the first trading day of each month at 9am.",
        }
        perf_cron = perf_crons.get(monitoring_freq)
        if perf_cron:
            console.print(Panel(
                f"Performance monitoring: [bold]{monitoring_freq}[/bold]\n\n"
                f"Recommended cron schedule:\n"
                f"  [cyan]{perf_cron}[/cyan]\n\n"
                f"{perf_descs[monitoring_freq]}\n"
                f"Add this line to your crontab alongside the rebalancing schedule.",
                title="Performance Monitoring Schedule",
                border_style="green",
            ))


@main.command("list")
def list_portfolios() -> None:
    """List all portfolios."""
    portfolios_dir = get_portfolios_dir()
    portfolios = [d.name for d in portfolios_dir.iterdir() if d.is_dir() and (d / "config.yaml").exists()]

    if not portfolios:
        console.print("[yellow]No portfolios found. Run setup to create one.[/yellow]")
        return

    from rich.table import Table
    table = Table(title="Portfolios")
    table.add_column("Name", style="bold")
    table.add_column("Assets")
    table.add_column("Method")
    table.add_column("Benchmark")
    table.add_column("Has State")

    for p in sorted(portfolios):
        try:
            config = load_portfolio_config(p)
            has_state = (portfolios_dir / p / "state.json").exists()
            table.add_row(
                p,
                str(len(config.portfolio.assets)),
                config.optimization.method,
                config.portfolio.benchmark,
                "[green]Yes[/green]" if has_state else "[dim]No[/dim]",
            )
        except Exception:
            table.add_row(p, "?", "?", "?", "?")

    console.print(table)

    _emit_json({
        "status": "success", "command": "list",
        "portfolios": sorted(portfolios),
    })


if __name__ == "__main__":
    main()
