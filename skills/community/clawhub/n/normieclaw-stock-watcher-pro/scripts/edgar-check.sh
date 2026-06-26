#!/usr/bin/env bash
# edgar-check.sh — Manual SEC EDGAR Filing Checker
#
# Queries SEC EDGAR for recent filings for all portfolio tickers.
# Outputs a summary of new filings found since the last check.
#
# Usage:
#   bash scripts/edgar-check.sh                — Check all portfolio tickers
#   bash scripts/edgar-check.sh AAPL           — Check a specific ticker
#   bash scripts/edgar-check.sh --days 7       — Check last 7 days (default: 3)
#
# Requirements:
#   - curl
#   - python3
#   - data/portfolio.json must exist
#   - config/watchlist-config.json for rate limit settings

set -euo pipefail

# --- Path Resolution ---
# Workspace root is passed as $1, or detected from script location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # Skill directory detection (stay within skill boundary)
  WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    # Skill directory detection (stay within skill boundary)
  # Inside skill package: skills/stock-watcher-pro/scripts/
  WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
else
  WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
fi
CONFIG_FILE="$WORKSPACE_DIR/config/watchlist-config.json"
PORTFOLIO_FILE="$WORKSPACE_DIR/data/portfolio.json"
WATCHLIST_FILE="$WORKSPACE_DIR/data/watchlist.json"
FILINGS_DIR="$WORKSPACE_DIR/data/filings"

# --- Defaults ---
LOOKBACK_DAYS=3
SPECIFIC_TICKER=""
RATE_LIMIT_MS=500
USER_AGENT_EMAIL=""

# --- Color Output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_filing(){ echo -e "${CYAN}[FILING]${NC} $1"; }

is_valid_ticker() {
    [[ "$1" =~ ^[A-Z][A-Z0-9.-]{0,9}$ ]]
}

# --- Parse Arguments ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --days)
            if [[ -z "${2:-}" ]]; then
                log_error "Missing value for --days"
                exit 1
            fi
            LOOKBACK_DAYS="$2"
            shift 2
            ;;
        --help|-h)
            echo "EDGAR Filing Checker — Stock Watcher Pro"
            echo ""
            echo "Usage:"
            echo "  bash scripts/edgar-check.sh              — Check all tickers"
            echo "  bash scripts/edgar-check.sh AAPL          — Check specific ticker"
            echo "  bash scripts/edgar-check.sh --days 7      — Set lookback window"
            echo ""
            echo "Options:"
            echo "  --days N    Days to look back (default: 3)"
            echo "  --help      Show this help"
            exit 0
            ;;
        *)
            SPECIFIC_TICKER="$1"
            shift
            ;;
    esac
done

if ! [[ "$LOOKBACK_DAYS" =~ ^[0-9]+$ ]] || [ "$LOOKBACK_DAYS" -lt 1 ] || [ "$LOOKBACK_DAYS" -gt 365 ]; then
    log_error "--days must be an integer between 1 and 365"
    exit 1
fi

if [ -n "$SPECIFIC_TICKER" ]; then
    SPECIFIC_TICKER="$(echo "$SPECIFIC_TICKER" | tr '[:lower:]' '[:upper:]')"
    if ! is_valid_ticker "$SPECIFIC_TICKER"; then
        log_error "Invalid ticker format: $SPECIFIC_TICKER"
        exit 1
    fi
fi

# --- Validation ---
if [ ! -f "$PORTFOLIO_FILE" ]; then
    log_error "Portfolio file not found: $PORTFOLIO_FILE"
    log_error "Run SETUP-PROMPT.md first, then add holdings."
    exit 1
fi

# Read rate limit from config
if [ -f "$CONFIG_FILE" ]; then
    RATE_LIMIT_MS=$(CONFIG_FILE="$CONFIG_FILE" python3 -c "
import json, os
try:
    with open(os.environ['CONFIG_FILE']) as f:
        data = json.load(f)
    v = data.get('edgar_settings', {}).get('rate_limit_delay_ms', 500)
    print(int(v))
except Exception:
    print(500)
" 2>/dev/null || echo "500")

    USER_AGENT_EMAIL=$(CONFIG_FILE="$CONFIG_FILE" python3 -c "
import json, os
try:
    with open(os.environ['CONFIG_FILE']) as f:
        data = json.load(f)
    print(str(data.get('edgar_settings', {}).get('user_agent_email', '')).strip())
except Exception:
    print('')
" 2>/dev/null || echo "")
fi

if ! [[ "$RATE_LIMIT_MS" =~ ^[0-9]+$ ]]; then
    RATE_LIMIT_MS=500
fi
if [ "$RATE_LIMIT_MS" -lt 100 ]; then
    RATE_LIMIT_MS=100
fi

# Prevent header injection and malformed values.
USER_AGENT_EMAIL="$(echo "$USER_AGENT_EMAIL" | tr -d '\r\n')"
if [ -n "$USER_AGENT_EMAIL" ] && ! [[ "$USER_AGENT_EMAIL" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
    log_warn "Configured user_agent_email is not a valid email. Using fallback contact."
    USER_AGENT_EMAIL=""
fi

if [ -z "$USER_AGENT_EMAIL" ]; then
    log_warn "No user_agent_email set in config. SEC recommends setting a contact email."
    log_warn "Edit config/watchlist-config.json → edgar_settings → user_agent_email"
    USER_AGENT_EMAIL="stock-watcher-pro@example.com"
fi

# --- Collect Tickers ---
get_tickers() {
    PORTFOLIO_FILE="$PORTFOLIO_FILE" WATCHLIST_FILE="$WATCHLIST_FILE" python3 -c "
import json
import os
import re

ticker_re = re.compile(r'^[A-Z][A-Z0-9.-]{0,9}$')
tickers = set()

def add_ticker(raw):
    if not isinstance(raw, str):
        return
    t = raw.strip().upper()
    if ticker_re.match(t):
        tickers.add(t)

try:
    with open(os.environ['PORTFOLIO_FILE']) as f:
        data = json.load(f)
    for h in data.get('holdings', []):
        add_ticker(h.get('ticker'))
except Exception:
    pass

try:
    with open(os.environ['WATCHLIST_FILE']) as f:
        data = json.load(f)
    for w in data.get('watchlist', []):
        add_ticker(w.get('ticker'))
except Exception:
    pass

print('\n'.join(sorted(tickers)))
" 2>/dev/null
}

# --- Date Calculation ---
START_DATE=$(LOOKBACK_DAYS_ENV="$LOOKBACK_DAYS" python3 -c "
import os
from datetime import datetime, timedelta

days = int(os.environ['LOOKBACK_DAYS_ENV'])
d = datetime.now() - timedelta(days=days)
print(d.strftime('%Y-%m-%d'))
")
END_DATE=$(python3 -c "from datetime import datetime; print(datetime.now().strftime('%Y-%m-%d'))")

# --- EDGAR Query ---
check_ticker_filings() {
    local ticker="$1"
    if ! is_valid_ticker "$ticker"; then
        log_warn "Skipping invalid ticker: $ticker"
        return 0
    fi

    # Get CIK from source file if available
    local source_file="$WORKSPACE_DIR/data/sources/${ticker}.json"
    local cik=""

    if [ -f "$source_file" ]; then
        cik=$(SOURCE_FILE="$source_file" python3 -c "
import json, os
try:
    with open(os.environ['SOURCE_FILE']) as f:
        data = json.load(f)
    cik = str(data.get('cik', '')).strip()
    print(cik if cik.isdigit() else '')
except Exception:
    print('')
" 2>/dev/null || echo "")
    fi

    # Query EDGAR full-text search
    local search_term
    if [ -n "$cik" ]; then
        search_term="$cik"
    else
        search_term="$ticker"
    fi

    log_info "Checking EDGAR for $ticker (search: $search_term, last $LOOKBACK_DAYS days)..."

    local encoded_term
    encoded_term=$(SEARCH_TERM="$search_term" python3 -c "import os, urllib.parse; print(urllib.parse.quote(os.environ['SEARCH_TERM']))")

    local url="https://efts.sec.gov/LATEST/search-index?q=%22${encoded_term}%22&dateRange=custom&startdt=${START_DATE}&enddt=${END_DATE}&forms=8-K,10-K,10-Q,4"

    local response
    response=$(curl -s -f \
        -H "User-Agent: Stock-Watcher-Pro/1.0 ($USER_AGENT_EMAIL)" \
        -H "Accept: application/json" \
        "$url" 2>/dev/null) || {
        log_warn "EDGAR query failed for $ticker. API may be temporarily unavailable."
        return 0
    }

    # Parse results
    TICKER="$ticker" LOOKBACK_DAYS="$LOOKBACK_DAYS" python3 -c "
import json
import os
import sys

raw = sys.stdin.read()
try:
    data = json.loads(raw)
    hits = data.get('hits', {}).get('hits', [])
    ticker = os.environ['TICKER']
    lookback = os.environ['LOOKBACK_DAYS']

    if not hits:
        print(f'  No new filings for {ticker} in the last {lookback} days.')
        sys.exit(0)

    print(f'  Found {len(hits)} filing(s) for {ticker}:')
    for hit in hits[:10]:
        source = hit.get('_source', {})
        form = source.get('forms', 'Unknown')
        date = source.get('file_date', 'Unknown')
        names = source.get('display_names') or []
        desc = names[0] if names else ''
        print(f'    [{form}] {date} — {desc}')
except Exception as e:
    print(f'  Could not parse EDGAR response for {os.environ.get(\"TICKER\", \"UNKNOWN\")}: {e}', file=sys.stderr)
" <<< "$response" 2>/dev/null || log_warn "  Could not parse response for $ticker"

    # Respect rate limits
    sleep "$(echo "scale=3; $RATE_LIMIT_MS / 1000" | bc 2>/dev/null || echo "0.5")"
}

# --- Main ---
echo "========================================="
echo "  EDGAR Filing Check"
echo "  Period: $START_DATE to $END_DATE"
echo "========================================="
echo ""

if [ -n "$SPECIFIC_TICKER" ]; then
    check_ticker_filings "$SPECIFIC_TICKER"
else
    TICKERS=$(get_tickers)
    if [ -z "$TICKERS" ]; then
        log_warn "No tickers found in portfolio or watchlist."
        log_warn "Add holdings first, then run this script."
        exit 0
    fi

    log_info "Checking filings for: $(echo "$TICKERS" | tr '\n' ' ')"
    echo ""

    while IFS= read -r ticker; do
        [ -z "$ticker" ] && continue
        check_ticker_filings "$ticker"
        echo ""
    done <<< "$TICKERS"
fi

# Create filings directory if needed
mkdir -p "$FILINGS_DIR"
chmod 700 "$FILINGS_DIR"

echo "========================================="
log_info "EDGAR check complete."
log_info "For detailed filing analysis, ask your agent:"
log_info "  'Analyze the latest [TICKER] filing in detail.'"
echo "========================================="
