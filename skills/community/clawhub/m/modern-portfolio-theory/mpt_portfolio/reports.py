"""Report generation — HTML (string formatting) and terminal (rich)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from mpt_portfolio.charts import export_chart_base64
from mpt_portfolio.metrics import PerformanceMetrics
from mpt_portfolio.tracker import PortfolioState
from mpt_portfolio.utils import get_portfolio_reports_dir, timestamp_str

console = Console()

_REPORT_CSS = """\
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         color: #333; background: #f8f9fa; line-height: 1.6; }
  .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
  header { background: #1a1a2e; color: white; padding: 30px 0; margin-bottom: 30px; }
  header .container { display: flex; justify-content: space-between; align-items: center; }
  h1 { font-size: 1.8em; font-weight: 600; }
  .meta { color: #a0aec0; font-size: 0.9em; }
  h2 { font-size: 1.3em; margin: 30px 0 15px; color: #1a1a2e;
       border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }
  .card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
          padding: 20px; margin-bottom: 20px; }
  table { width: 100%; border-collapse: collapse; }
  th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #e2e8f0; }
  th { background: #f7fafc; font-weight: 600; color: #4a5568; font-size: 0.85em;
       text-transform: uppercase; letter-spacing: 0.5px; }
  td { font-size: 0.95em; }
  tr:hover td { background: #f7fafc; }
  .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
  .metric-box { background: white; border-radius: 8px; padding: 18px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }
  .metric-value { font-size: 1.6em; font-weight: 700; color: #1a1a2e; }
  .metric-label { font-size: 0.8em; color: #718096; text-transform: uppercase;
                  letter-spacing: 0.5px; margin-top: 4px; }
  .chart-container { margin: 20px 0; }
  .recommendation { background: #ebf8ff; border-left: 4px solid #3182ce;
                     padding: 15px 20px; border-radius: 0 8px 8px 0; margin: 20px 0; }
  .recommendation strong { color: #2c5282; }
  .positive { color: #38a169; }
  .negative { color: #e53e3e; }
  .residual { margin-top: 10px; font-size: 0.95em; color: #4a5568; }
  footer { text-align: center; color: #a0aec0; font-size: 0.8em;
           padding: 30px 0; border-top: 1px solid #e2e8f0; margin-top: 40px; }
"""


def _build_metrics_html(metrics: PerformanceMetrics) -> str:
    boxes = [
        (f"{metrics.cagr * 100:.2f}%", "CAGR"),
        (f"{metrics.sharpe_ratio:.3f}", "Sharpe Ratio"),
        (f"{metrics.annualized_volatility * 100:.2f}%", "Volatility"),
        (f"{metrics.max_drawdown * 100:.2f}%", "Max Drawdown"),
        (f"{metrics.sortino_ratio:.3f}", "Sortino Ratio"),
        (f"{metrics.calmar_ratio:.3f}", "Calmar Ratio"),
    ]
    items = "\n".join(
        f'    <div class="metric-box"><div class="metric-value">{val}</div>'
        f'<div class="metric-label">{label}</div></div>'
        for val, label in boxes
    )
    return f'<h2>Key Metrics</h2>\n<div class="metric-grid">\n{items}\n</div>'


def _build_weights_html(
    weights_table: list[dict],
    latest_prices: pd.Series | None,
    investment_amount: float | None,
) -> str:
    show_qty = latest_prices is not None and investment_amount is not None

    headers = "<th>Asset</th><th>Weight</th><th>Expected Return</th><th>Volatility</th>"
    if show_qty:
        headers += "<th>Price</th><th>Exact Shares</th><th>Whole Shares</th>"

    rows = ""
    total_whole_cost = 0.0
    for row in weights_table:
        ticker = row["asset"]
        cells = (
            f"<td>{ticker}</td>"
            f"<td>{row['weight'] * 100:.2f}%</td>"
            f"<td>{row['expected_return'] * 100:.2f}%</td>"
            f"<td>{row['volatility'] * 100:.2f}%</td>"
        )
        if show_qty:
            price = latest_prices.get(ticker, 0)
            if price > 0:
                alloc = investment_amount * row["weight"]
                exact = alloc / price
                whole = int(exact)
                total_whole_cost += whole * price
                cells += (
                    f"<td>${price:,.2f}</td>"
                    f"<td>{exact:,.2f}</td>"
                    f"<td>{whole:,}</td>"
                )
            else:
                cells += "<td>-</td><td>-</td><td>-</td>"
        rows += f"<tr>{cells}</tr>\n"

    residual_html = ""
    if show_qty:
        residual = investment_amount - total_whole_cost
        residual_html = (
            f'<p class="residual"><strong>Investment:</strong> ${investment_amount:,.2f} &nbsp;|&nbsp; '
            f'<strong>Residual cash (whole shares):</strong> ${residual:,.2f}</p>'
        )

    return (
        f'<h2>Portfolio Weights</h2>\n<div class="card">\n'
        f"<table>\n<thead><tr>{headers}</tr></thead>\n<tbody>\n{rows}</tbody>\n</table>\n"
        f"{residual_html}</div>"
    )


def _build_rebalance_history_html(rebalance_events: list) -> str:
    """Build HTML table showing how holdings changed at each rebalance."""
    if not rebalance_events:
        return ""

    all_tickers = sorted({
        t for ev in rebalance_events
        for t, w in ev.new_weights.items() if abs(w) > 0.001
    })

    headers = "<th>Date</th>"
    for t in all_tickers:
        headers += f"<th>{t}</th>"
    headers += "<th>Turnover</th>"

    rows = ""
    for ev in rebalance_events:
        cells = f"<td><strong>{ev.date.strftime('%Y-%m-%d')}</strong></td>"
        for t in all_tickers:
            w = ev.new_weights.get(t, 0.0)
            if abs(w) > 0.001:
                cells += f"<td>{w * 100:.1f}%</td>"
            else:
                cells += "<td style='color:#ccc;'>-</td>"
        cells += f"<td>{ev.turnover:.2%}</td>"
        rows += f"<tr>{cells}</tr>\n"

    return (
        '<h2>Rebalance History</h2>\n<div class="card">\n'
        f"<table>\n<thead><tr>{headers}</tr></thead>\n<tbody>\n{rows}</tbody>\n</table>\n"
        "<p class='residual'>Shows how the optimizer re-selected assets at each rebalance. "
        "Different stocks may enter or exit the portfolio as market conditions change.</p></div>"
    )


def _build_backtest_html(backtest_table: list[dict]) -> str:
    headers = (
        "<th>Strategy</th><th>Total Return</th><th>CAGR</th><th>Volatility</th>"
        "<th>Sharpe</th><th>Sortino</th><th>Max DD</th><th>Calmar</th>"
        "<th>Turnover</th><th>Costs</th>"
    )
    rows = ""
    for row in backtest_table:
        rows += (
            f"<tr><td><strong>{row['strategy']}</strong></td>"
            f"<td>{row['total_return']}</td><td>{row['cagr']}</td>"
            f"<td>{row['volatility']}</td><td>{row['sharpe']}</td>"
            f"<td>{row['sortino']}</td><td>{row['max_dd']}</td>"
            f"<td>{row['calmar']}</td><td>{row['turnover']}</td>"
            f"<td>{row['costs']}</td></tr>\n"
        )
    return (
        f'<h2>Backtest Comparison</h2>\n<div class="card">\n'
        f"<table>\n<thead><tr>{headers}</tr></thead>\n<tbody>\n{rows}</tbody>\n</table>\n</div>"
    )


def generate_html_report(
    portfolio_name: str,
    optimization_method: str,
    weights: pd.Series,
    expected_returns: pd.Series,
    volatilities: pd.Series,
    metrics: PerformanceMetrics | None = None,
    charts: dict | None = None,
    backtest_comparison: pd.DataFrame | None = None,
    recommendation: dict | None = None,
    latest_prices: pd.Series | None = None,
    investment_amount: float | None = None,
    rebalance_events: list | None = None,
) -> Path:
    """Generate full HTML report."""
    gen_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    weights_table = []
    for ticker in weights.index:
        if abs(weights[ticker]) > 0.001:
            weights_table.append({
                "asset": ticker,
                "weight": weights[ticker],
                "expected_return": expected_returns.get(ticker, 0),
                "volatility": volatilities.get(ticker, 0),
            })
    weights_table.sort(key=lambda x: x["weight"], reverse=True)

    # Build HTML sections
    sections = []

    if metrics:
        sections.append(_build_metrics_html(metrics))

    if weights_table:
        sections.append(_build_weights_html(weights_table, latest_prices, investment_amount))

    if charts:
        for name, fig in charts.items():
            if fig is not None:
                title = name.replace("_", " ").title()
                img_html = export_chart_base64(fig)
                sections.append(
                    f'<h2>{title}</h2>\n<div class="card chart-container">{img_html}</div>'
                )

    if backtest_comparison is not None:
        bt_rows = []
        for strategy, row in backtest_comparison.iterrows():
            bt_rows.append({
                "strategy": strategy,
                "total_return": row.get("Total Return", ""),
                "cagr": row.get("CAGR", ""),
                "volatility": row.get("Volatility", ""),
                "sharpe": row.get("Sharpe", ""),
                "sortino": row.get("Sortino", ""),
                "max_dd": row.get("Max Drawdown", ""),
                "calmar": row.get("Calmar", ""),
                "turnover": row.get("Turnover", ""),
                "costs": row.get("Costs", ""),
            })
        sections.append(_build_backtest_html(bt_rows))

    if rebalance_events:
        sections.append(_build_rebalance_history_html(rebalance_events))

    if recommendation:
        sections.append(
            f'<h2>Recommendation</h2>\n'
            f'<div class="recommendation"><strong>{recommendation["strategy"]}</strong>'
            f' &mdash; {recommendation["reason"]}</div>'
        )

    body = "\n\n".join(sections)

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{portfolio_name} — MPT Portfolio Report</title>
<style>
{_REPORT_CSS}
</style>
</head>
<body>
<header>
  <div class="container">
    <div><h1>{portfolio_name}</h1><div class="meta">Modern Portfolio Theory Report</div></div>
    <div class="meta">Generated: {gen_date}<br>Method: {optimization_method}</div>
  </div>
</header>
<div class="container">
{body}
</div>
<footer>
  <div class="container">
    Generated by MPT Portfolio Optimizer v0.1.0.
    This is not financial advice. Past performance does not guarantee future results.
  </div>
</footer>
</body>
</html>
"""
    reports_dir = get_portfolio_reports_dir(portfolio_name)
    path = reports_dir / f"report_{timestamp_str()}.html"
    path.write_text(html)
    return path


def generate_terminal_report(
    portfolio_name: str,
    optimization_method: str,
    weights: pd.Series,
    expected_returns: pd.Series,
    volatilities: pd.Series,
    sharpe_ratio: float,
    expected_return: float,
    portfolio_volatility: float,
    risk_free_rate: float,
    backtest_comparison: pd.DataFrame | None = None,
    recommendation: dict | None = None,
    latest_prices: pd.Series | None = None,
    investment_amount: float | None = None,
    rebalance_events: list | None = None,
) -> None:
    """Print rich-formatted terminal report."""
    show_qty = latest_prices is not None and investment_amount is not None

    console.print()
    console.print(Panel(
        f"[bold]{portfolio_name}[/bold]  |  Method: {optimization_method}  |  "
        f"Return: [green]{expected_return:.2%}[/green]  |  "
        f"Vol: [yellow]{portfolio_volatility:.2%}[/yellow]  |  "
        f"Sharpe: [cyan]{sharpe_ratio:.3f}[/cyan]  |  "
        f"Rf: {risk_free_rate:.2%}",
        title="Portfolio Summary",
    ))

    table = Table(title="Asset Weights", show_lines=False)
    table.add_column("Asset", style="bold")
    table.add_column("Weight", justify="right")
    table.add_column("Exp Return", justify="right")
    table.add_column("Volatility", justify="right")
    if show_qty:
        table.add_column("Price", justify="right")
        table.add_column("Exact Shares", justify="right")
        table.add_column("Whole Shares", justify="right")

    total_whole_cost = 0.0
    for ticker in weights.sort_values(ascending=False).index:
        w = weights[ticker]
        if abs(w) < 0.001:
            continue
        row_data = [
            ticker,
            f"{w:.2%}",
            f"{expected_returns.get(ticker, 0):.2%}",
            f"{volatilities.get(ticker, 0):.2%}",
        ]
        if show_qty:
            price = latest_prices.get(ticker, 0)
            if price > 0:
                alloc = investment_amount * w
                exact = alloc / price
                whole = int(exact)
                total_whole_cost += whole * price
                row_data += [f"${price:,.2f}", f"{exact:,.2f}", f"{whole:,}"]
            else:
                row_data += ["-", "-", "-"]
        table.add_row(*row_data)
    console.print(table)

    if show_qty:
        residual = investment_amount - total_whole_cost
        console.print(
            f"  Investment: ${investment_amount:,.2f}  |  "
            f"Residual cash (whole shares): ${residual:,.2f}"
        )

    if backtest_comparison is not None:
        console.print()
        bt_table = Table(title="Backtest Comparison", show_lines=True)
        bt_table.add_column("Strategy", style="bold")
        for col in backtest_comparison.columns:
            bt_table.add_column(col, justify="right")
        for strategy, row in backtest_comparison.iterrows():
            bt_table.add_row(str(strategy), *[str(row[c]) for c in backtest_comparison.columns])
        console.print(bt_table)

    if rebalance_events:
        all_tickers = sorted({
            t for ev in rebalance_events
            for t, w in ev.new_weights.items() if abs(w) > 0.001
        })
        rb_table = Table(title="Rebalance History", show_lines=True)
        rb_table.add_column("Date", style="bold")
        for t in all_tickers:
            rb_table.add_column(t, justify="right")
        rb_table.add_column("Turnover", justify="right")
        for ev in rebalance_events:
            row_data = [ev.date.strftime("%Y-%m-%d")]
            for t in all_tickers:
                w = ev.new_weights.get(t, 0.0)
                row_data.append(f"{w * 100:.1f}%" if abs(w) > 0.001 else "[dim]-[/dim]")
            row_data.append(f"{ev.turnover:.2%}")
            rb_table.add_row(*row_data)
        console.print()
        console.print(rb_table)

    if recommendation:
        console.print()
        console.print(Panel(
            f"[bold]{recommendation['strategy']}[/bold]\n{recommendation['reason']}",
            title="Recommended Rebalancing Strategy",
            border_style="blue",
        ))
    console.print()


def generate_status_report(
    portfolio_name: str,
    holdings: dict,
    current_values: dict[str, float],
    total_value: float,
    current_weights: pd.Series,
    target_weights: pd.Series,
    benchmark_return: float,
    portfolio_return: float,
) -> None:
    """Terminal report for portfolio status."""
    console.print()
    pnl_style = "green" if portfolio_return >= 0 else "red"
    console.print(Panel(
        f"[bold]{portfolio_name}[/bold]  |  "
        f"Value: [bold]${total_value:,.2f}[/bold]  |  "
        f"Return: [{pnl_style}]{portfolio_return:.2%}[/{pnl_style}]  |  "
        f"Benchmark: {benchmark_return:.2%}",
        title="Portfolio Status",
    ))

    table = Table(title="Holdings", show_lines=False)
    table.add_column("Asset", style="bold")
    table.add_column("Shares", justify="right")
    table.add_column("Value", justify="right")
    table.add_column("Current Wt", justify="right")
    table.add_column("Target Wt", justify="right")
    table.add_column("Drift", justify="right")

    for ticker in current_weights.sort_values(ascending=False).index:
        cw = current_weights[ticker]
        tw = target_weights.get(ticker, 0)
        drift = cw - tw
        h = holdings.get(ticker, {})
        drift_str = f"{drift:+.2%}"
        if abs(drift) > 0.05:
            drift_str = f"[red]{drift_str}[/red]"
        table.add_row(
            ticker,
            f"{h.get('shares', 0):.2f}",
            f"${current_values.get(ticker, 0):,.2f}",
            f"{cw:.2%}",
            f"{tw:.2%}",
            drift_str,
        )
    console.print(table)
    console.print()


def generate_rebalance_report(
    needs_rebalance: bool,
    reason: str,
    max_drift: float,
    max_drift_asset: str,
    orders: list,
    estimated_cost: float,
) -> None:
    """Terminal report for rebalance check."""
    console.print()
    if needs_rebalance:
        console.print(Panel(
            f"[bold red]Rebalance Recommended[/bold red]\n"
            f"Reason: {reason}\n"
            f"Max drift: {max_drift:.2%} ({max_drift_asset})\n"
            f"Estimated cost: ${estimated_cost:.2f}",
            title="Rebalance Check",
            border_style="red",
        ))

        table = Table(title="Recommended Orders", show_lines=True)
        table.add_column("Action", style="bold")
        table.add_column("Asset")
        table.add_column("Shares", justify="right")
        table.add_column("Amount", justify="right")
        table.add_column("Current Wt", justify="right")
        table.add_column("Target Wt", justify="right")

        for order in orders:
            action_style = "green" if order.action == "BUY" else "red"
            table.add_row(
                f"[{action_style}]{order.action}[/{action_style}]",
                order.ticker,
                f"{order.shares_rounded}",
                f"${abs(order.dollar_amount):,.2f}",
                f"{order.current_weight:.2%}",
                f"{order.target_weight:.2%}",
            )
        console.print(table)
    else:
        console.print(Panel(
            f"[bold green]No Rebalance Needed[/bold green]\n"
            f"Max drift: {max_drift:.2%} ({max_drift_asset})",
            title="Rebalance Check",
            border_style="green",
        ))
    console.print()


def generate_performance_terminal_report(
    portfolio_name: str,
    metrics: PerformanceMetrics,
    total_value: float,
    portfolio_return: float,
    benchmark_return: float | None,
    live_days: int,
    rebalance_count: int,
    holdings: dict,
    current_values: dict[str, float],
) -> None:
    """Terminal report for live portfolio performance."""
    console.print()
    ret_style = "green" if portfolio_return >= 0 else "red"
    bm_str = f"Benchmark Return: {benchmark_return:.2%}" if benchmark_return is not None else ""

    console.print(Panel(
        f"[bold]{portfolio_name}[/bold]  |  "
        f"Value: [bold]${total_value:,.2f}[/bold]  |  "
        f"Return: [{ret_style}]{portfolio_return:.2%}[/{ret_style}]  |  "
        f"{bm_str}\n"
        f"Sharpe: {metrics.sharpe_ratio:.3f}  |  "
        f"Max DD: {metrics.max_drawdown:.2%}  |  "
        f"CAGR: {metrics.cagr:.2%}  |  "
        f"Vol: {metrics.annualized_volatility:.2%}\n"
        f"Live days: {live_days}  |  Rebalances: {rebalance_count}",
        title="Performance Report",
    ))

    if holdings:
        table = Table(title="Current Holdings", show_lines=False)
        table.add_column("Asset", style="bold")
        table.add_column("Shares", justify="right")
        table.add_column("Value", justify="right")

        for ticker in sorted(current_values, key=lambda t: current_values[t], reverse=True):
            h = holdings.get(ticker, {})
            table.add_row(
                ticker,
                f"{h.get('shares', 0):.2f}",
                f"${current_values.get(ticker, 0):,.2f}",
            )
        console.print(table)
    console.print()


def _build_holdings_html(holdings: dict, current_values: dict[str, float]) -> str:
    headers = "<th>Asset</th><th>Shares</th><th>Value</th>"
    rows = ""
    for ticker in sorted(current_values, key=lambda t: current_values[t], reverse=True):
        h = holdings.get(ticker, {})
        rows += (
            f"<tr><td>{ticker}</td>"
            f"<td>{h.get('shares', 0):.2f}</td>"
            f"<td>${current_values.get(ticker, 0):,.2f}</td></tr>\n"
        )
    return (
        f'<h2>Current Holdings</h2>\n<div class="card">\n'
        f"<table>\n<thead><tr>{headers}</tr></thead>\n<tbody>\n{rows}</tbody>\n</table>\n</div>"
    )


def _build_rebalance_log_html(rebalance_history: list[dict]) -> str:
    if not rebalance_history:
        return ""
    headers = "<th>Date</th><th>Strategy</th><th>Turnover</th><th>Cost</th>"
    rows = ""
    for ev in rebalance_history:
        rows += (
            f"<tr><td>{ev.get('date', '')[:10]}</td>"
            f"<td>{ev.get('strategy', '-')}</td>"
            f"<td>{ev.get('turnover', 0):.2%}</td>"
            f"<td>${ev.get('transaction_cost', 0):,.2f}</td></tr>\n"
        )
    return (
        '<h2>Rebalance Log</h2>\n<div class="card">\n'
        f"<table>\n<thead><tr>{headers}</tr></thead>\n<tbody>\n{rows}</tbody>\n</table>\n</div>"
    )


def generate_performance_html_report(
    portfolio_name: str,
    metrics: PerformanceMetrics,
    state: PortfolioState,
    benchmark_ticker: str,
    charts: dict | None = None,
    current_values: dict[str, float] | None = None,
    total_value: float = 0.0,
    portfolio_return: float = 0.0,
    benchmark_return: float | None = None,
) -> Path:
    """Generate HTML performance report from live data."""
    gen_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    live_start = state.optimization_date[:10] if state.optimization_date else "N/A"

    sections = []

    sections.append(_build_metrics_html(metrics))

    if current_values and state.holdings:
        sections.append(_build_holdings_html(state.holdings, current_values))

    if charts:
        for name, fig in charts.items():
            if fig is not None:
                title = name.replace("_", " ").title()
                img_html = export_chart_base64(fig)
                sections.append(
                    f'<h2>{title}</h2>\n<div class="card chart-container">{img_html}</div>'
                )

    if state.rebalance_history:
        sections.append(_build_rebalance_log_html(state.rebalance_history))

    bm_str = f"Benchmark ({benchmark_ticker}): {benchmark_return:.2%}" if benchmark_return is not None else ""
    ret_class = "positive" if portfolio_return >= 0 else "negative"

    summary_html = (
        '<div class="recommendation">'
        f'<strong>Portfolio Return: <span class="{ret_class}">{portfolio_return:.2%}</span></strong>'
        f' &nbsp;|&nbsp; {bm_str}'
        f' &nbsp;|&nbsp; Total Value: ${total_value:,.2f}'
        f' &nbsp;|&nbsp; Live Since: {live_start}'
        '</div>'
    )
    sections.insert(0, summary_html)

    body = "\n\n".join(sections)

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{portfolio_name} — Performance Report</title>
<style>
{_REPORT_CSS}
</style>
</head>
<body>
<header>
  <div class="container">
    <div><h1>{portfolio_name}</h1><div class="meta">Performance Report</div></div>
    <div class="meta">Generated: {gen_date}<br>Live since: {live_start}</div>
  </div>
</header>
<div class="container">
{body}
</div>
<footer>
  <div class="container">
    Generated by MPT Portfolio Optimizer v0.1.0.
    This is not financial advice. Past performance does not guarantee future results.
  </div>
</footer>
</body>
</html>
"""
    reports_dir = get_portfolio_reports_dir(portfolio_name)
    path = reports_dir / f"performance_{timestamp_str()}.html"
    path.write_text(html)
    return path
