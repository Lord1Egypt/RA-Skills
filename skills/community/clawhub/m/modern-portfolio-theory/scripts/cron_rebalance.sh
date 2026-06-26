#!/bin/bash
# MPT Portfolio Rebalance Cron Script
#
# Usage:
#   ./cron_rebalance.sh <portfolio_name> [python_path]
#
# Example crontab entries:
#   # Monthly (1st trading day, 9am)
#   0 9 1-7 * 1-5 /path/to/cron_rebalance.sh my_portfolio
#
#   # Quarterly (1st of Jan/Apr/Jul/Oct, 9am)
#   0 9 1-7 1,4,7,10 1-5 /path/to/cron_rebalance.sh my_portfolio
#
#   # Weekly (Monday 9am)
#   0 9 * * 1 /path/to/cron_rebalance.sh my_portfolio
#
#   # Daily check (dynamic rebalancing, 9am on weekdays)
#   0 9 * * 1-5 /path/to/cron_rebalance.sh my_portfolio

set -euo pipefail

PORTFOLIO="${1:?Usage: $0 <portfolio_name> [python_path]}"
PYTHON="${2:-python3}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/portfolios/$PORTFOLIO/reports"
LOG_FILE="$LOG_DIR/cron_$(date +%Y%m%d_%H%M%S).log"

cd "$PROJECT_DIR"

# Activate venv if present
if [ -f "$PROJECT_DIR/.venv/bin/activate" ]; then
    source "$PROJECT_DIR/.venv/bin/activate"
fi

mkdir -p "$LOG_DIR"

{
    echo "=== MPT Portfolio Rebalance Check ==="
    echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "Portfolio: $PORTFOLIO"
    echo ""

    # Update data
    $PYTHON -m mpt_portfolio update-data -p "$PORTFOLIO" 2>&1 || true
    echo ""

    # Check rebalance (dry run)
    $PYTHON -m mpt_portfolio rebalance -p "$PORTFOLIO" 2>&1
    echo ""

    # Update status
    $PYTHON -m mpt_portfolio status -p "$PORTFOLIO" 2>&1
    echo ""

    echo "=== Complete ==="
} >> "$LOG_FILE" 2>&1

echo "Log saved: $LOG_FILE"
