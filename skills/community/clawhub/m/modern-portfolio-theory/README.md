# Modern Portfolio Theory Portfolio Optimizer

A Python CLI tool for building, optimizing, backtesting, and managing investment
portfolios using Markowitz mean-variance optimization. Supports multiple
optimization strategies, walk-forward backtesting with configurable rebalancing,
benchmark comparison, and automated reporting with interactive charts.

## Overview

This tool implements core Modern Portfolio Theory techniques:

- **Optimization**: Maximum Sharpe ratio, minimum variance, risk parity, and
  full efficient frontier construction.
- **Robust estimation**: Ledoit-Wolf covariance shrinkage to reduce estimation
  error in the covariance matrix.
- **Walk-forward backtesting**: Compare monthly, quarterly, yearly, and
  dynamic (drift-threshold) rebalancing strategies against a benchmark.
- **Transaction cost modeling**: Configurable per-trade cost (default 0.1%)
  applied during backtesting and rebalance calculations.
- **Reporting**: HTML reports with embedded charts (efficient frontier,
  equity curves, drawdown, rolling Sharpe, correlation heatmap, weight
  allocation) and Rich-formatted terminal output.
- **Multi-portfolio management**: Each portfolio has its own config, state, and
  report directory under `portfolios/`.
- **Automated rebalancing**: Cron-compatible rebalance checks with file or
  email notifications.

Default universe: XLC, XLY, XLP, XLE, XLF, XLV, XLI, XLB, XLRE, XLK, XLU,
GLD, DBC, TLT. Default benchmark: SPY. Both are user-configurable.

## Quick Start

### Requirements

- Python 3.10 or later
- pip

### Install

```bash
git clone <repo-url> && cd modern-portfolio-theory
pip install -r requirements.txt
```

Or install as a package (provides the `mpt-portfolio` entry point):

```bash
pip install .
```

### Create your first portfolio

There are two ways to set up a portfolio:

**Option A: LLM-guided setup (via OpenClaw / Claude Code)**

If using this project as an OpenClaw skill, the LLM walks you through each
decision step by step, explains options in plain language, and writes the
config for you. Just invoke the skill and say "create a new portfolio".

**Option B: Edit config file directly (Python CLI)**

When running the CLI directly, create the portfolio with defaults, then edit
the YAML config file:

```bash
# 1. Create portfolio structure with defaults
python -m mpt_portfolio setup -p my-portfolio --no-interactive

# 2. Edit the config to customize assets, method, constraints, etc.
#    See config/default.yaml for all options with comments.
nano portfolios/my-portfolio/config.yaml

# 3. Run optimization (automatically runs backtest + generates full report)
python -m mpt_portfolio opt -p my-portfolio
```

You can also create from a pre-written config file:
```bash
python -m mpt_portfolio setup -p my-portfolio --config-file my-config.yaml --no-interactive
```

### Day-to-day usage

```bash
# View current portfolio status (value, return, drift)
python -m mpt_portfolio status -p my-portfolio

# Add or remove assets (takes effect at next rebalance)
python -m mpt_portfolio modify-assets -p my-portfolio --add NVDA,AAPL --remove XLB

# Check if rebalancing is needed (dry-run)
python -m mpt_portfolio rebalance -p my-portfolio

# Compare multiple portfolios side by side
python -m mpt_portfolio compare -p portfolio-a -p portfolio-b

# List all portfolios
python -m mpt_portfolio list
```

Reports are written to `portfolios/my-portfolio/reports/`.

## CLI Commands

All commands are invoked via `python -m mpt_portfolio <command>`.

| Command         | Description                                              | Key Options                                                     |
|-----------------|----------------------------------------------------------|-----------------------------------------------------------------|
| `setup`         | Create a new portfolio with configuration                | `-p NAME`, `--config-file PATH`, `--no-interactive`             |
| `opt`           | Run optimization + backtest + report                     | `-p NAME`, `--method {max_sharpe,min_variance,efficient_frontier,risk_parity}`, `--no-auto-report` |
| `backtest`      | Walk-forward backtest across rebalancing strategies      | `-p NAME`                                                       |
| `modify-assets` | Add or remove assets for next rebalance                  | `-p NAME`, `--add TICKERS`, `--remove TICKERS`                  |
| `status`        | Show current value, return, and weight drift             | `-p NAME`                                                       |
| `rebalance`     | Check drift and generate rebalance orders                | `-p NAME`, `--execute` (default is dry-run)                     |
| `report`        | Generate full performance report                         | `-p NAME`, `--format {html,terminal,both}`                      |
| `update-data`   | Refresh cached price data from yfinance                  | `-p NAME`                                                       |
| `compare`       | Compare multiple portfolios side by side                 | `-p NAME1 -p NAME2 [-p NAME3 ...]`                              |
| `delete`        | Delete a portfolio and all its data                      | `-p NAME`, `--force`                                            |
| `list`          | List all configured portfolios                           | --                                                              |

Global options: `--verbose` / `-v` for debug logging, `--version`.

## Configuration

Each portfolio is configured via a YAML file at `portfolios/<name>/config.yaml`.
A commented default template lives at `config/default.yaml`.

Key sections:

```yaml
portfolio:
  name: "my-portfolio"
  initial_investment: 100000
  assets: [XLC, XLY, XLP, XLE, XLF, XLV, XLI, XLB, XLRE, XLK, XLU, GLD, DBC, TLT]
  benchmark: SPY

data:
  lookback_years: 5
  price_type: adjusted          # adjusted | unadjusted

optimization:
  method: max_sharpe            # max_sharpe | min_variance | efficient_frontier | risk_parity
  risk_free_rate: auto          # "auto" fetches 3-month Treasury yield, or a float
  covariance: ledoit_wolf       # sample | ledoit_wolf
  constraints:
    long_only: true
    max_weight: 0.40

backtest:
  rebalancing_strategies: [monthly, quarterly, yearly, dynamic]
  dynamic_threshold: 0.05       # 5% weight drift triggers rebalance
  transaction_cost: 0.001       # 0.1% per trade

rebalancing:
  strategy: recommended         # recommended | monthly | quarterly | yearly | dynamic
```

Email notifications are opt-in. Add an `email` section to your portfolio
config to enable:

```yaml
email:
  enabled: true
  smtp_host: smtp.gmail.com
  smtp_port: 587
  smtp_use_tls: true
  smtp_user: ${SMTP_USER}
  smtp_password: ${SMTP_PASSWORD}
  sender: ${SMTP_SENDER}
  recipients:
    - you@example.com

notifications:
  method: both                  # file | email | both
  portfolio_created: true
  backtest_complete: true
  rebalance_reminder: true
  performance_report: true
```

Environment variable substitution is supported for secrets via `${VAR}`
syntax.

See `config/default.yaml` for the full reference with comments.

## Cron-Based Rebalancing

To automate rebalance checks, add a cron entry that runs the rebalance
script:

```bash
crontab -e

# Example: check every Monday at 9:00 AM
0 9 * * 1 /path/to/modern-portfolio-theory/scripts/cron_rebalance.sh my-portfolio
```

Notifications are delivered via file, email, or both, as configured in
the `notifications` and `email` sections of your portfolio `config.yaml`.

## OpenClaw Skill

This project also works as an OpenClaw skill. When loaded as a skill, an LLM
agent can invoke the CLI commands and parse the structured `---JSON---` output
blocks. See `SKILL.md` for the full skill specification.

## Project Structure

```
modern-portfolio-theory/
  config/default.yaml       Default configuration template
  mpt_portfolio/            Core Python package
    cli.py                  Click-based CLI entry point
    optimization.py         Mean-variance optimization solvers
    backtest.py             Walk-forward backtesting engine
    data.py                 yfinance data fetching and caching
    risk.py                 Covariance estimation (sample, Ledoit-Wolf)
    returns.py              Return computation (log, expected)
    metrics.py              Performance metrics (Sharpe, Sortino, drawdown, etc.)
    reports.py              HTML and terminal report generation
    charts.py               Matplotlib chart builders
    rebalance.py            Drift detection and order generation
    tracker.py              Portfolio state persistence
    config.py               YAML config loading and validation
    notifications.py        Email / file notification dispatch
  portfolios/               Per-portfolio config, state, and reports
  scripts/                  Cron and utility scripts
  tests/                    Test suite (pytest)
```

## Dependencies

yfinance, numpy, pandas, scipy, matplotlib, pyyaml, rich, click

Dev: pytest, pytest-cov

## Further Reading

Detailed documentation is available in the `docs/` directory.

## License

MIT
