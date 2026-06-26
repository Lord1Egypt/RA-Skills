# Setup: Modern Portfolio Theory Optimizer

This skill helps you build and manage investment portfolios using Markowitz's Modern Portfolio Theory.

## Prerequisites

- **Python 3.10+**
- `uv` (recommended) or `pip` for package management.

## Installation

1. Install the required Python packages:
   ```bash
   pip install yfinance>=0.2.36 numpy>=1.24 pandas>=2.0 scipy>=1.11 matplotlib>=3.7 pyyaml>=6.0 rich>=13.0 click>=8.1
   ```
   (Alternatively, use `uv pip install -r requirements.txt`)

2. Verify that `python3` is in your PATH.

## Initial Configuration

The skill will guide you through creating your first portfolio `config.yaml`. No manual file editing is required for first-time setup.

## Cron Scheduling

For automated monitoring and rebalancing:
1. Ensure the `scripts/` directory has execute permissions:
   ```bash
   chmod +x scripts/*.sh
   ```
2. Schedule performance tracking (e.g., daily at market close).
3. Schedule rebalancing checks (e.g., weekly or monthly).
