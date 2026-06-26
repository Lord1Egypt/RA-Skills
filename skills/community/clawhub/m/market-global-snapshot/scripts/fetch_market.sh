#!/bin/bash
# market-global-snapshot helper script
# Supported exchanges: yahoo, sina
# Usage: scripts/fetch_market.sh <ticker> [exchange]
# Example: scripts/fetch_market.sh ^GSPC

readonly USER_AGENT="Mozilla/5.0"
readonly SINA_REFERER="https://finance.sina.com.cn"

usage() {
    printf 'Usage: %s <ticker> [exchange]\n' "$0" >&2
}

print_error() {
    printf '%s\n' "$1" >&2
}

fetch_url() {
    local url=$1

    curl -s "$url" -H "User-Agent: ${USER_AGENT}"
}

fetch_sina_url() {
    local url=$1

    curl -s "$url" \
        -H "User-Agent: ${USER_AGENT}" \
        -H "Referer: ${SINA_REFERER}"
}

print_response_if_present() {
    local response=$1

    if [ -n "$response" ]; then
        echo "$response"
        return 0
    fi

    return 1
}

# Yahoo Finance (Primary)
fetch_yahoo() {
    local ticker=$1
    local response

    response=$(fetch_url "https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=5d")

    if [ -n "$response" ] && grep -q "close" <<<"$response"; then
        echo "$response"
        return 0
    fi

    return 1
}

decode_sina_response() {
    if command -v iconv >/dev/null 2>&1; then
        iconv -f GB2312 -t UTF-8
        return
    fi

    cat
}

sina_symbol_for_ticker() {
    local ticker=$1

    case "$ticker" in
        000001.SS) echo "sh000001" ;;
        399001.SZ) echo "sz399001" ;;
        000680.SS) echo "sh000680" ;;
        *) return 1 ;;
    esac
}

# Sina Finance fallback for supported China-market tickers.
fetch_sina() {
    local ticker=$1
    local sina_symbol
    local response

    sina_symbol=$(sina_symbol_for_ticker "$ticker") || return 1
    response=$(fetch_sina_url "https://hq.sinajs.cn/list=${sina_symbol}" | decode_sina_response)

    print_response_if_present "$response"
}

main() {
    local ticker=$1
    local exchange=${2:-"yahoo"}

    if [ -z "$ticker" ]; then
        usage
        exit 1
    fi

    case "$exchange" in
        yahoo)
            fetch_yahoo "$ticker" || {
                print_error "ERROR: Yahoo Finance failed"
                exit 1
            }
            ;;
        sina)
            fetch_sina "$ticker" || {
                print_error "ERROR: Sina Finance failed"
                exit 1
            }
            ;;
        *)
            print_error "ERROR: Unknown exchange: $exchange"
            exit 1
            ;;
    esac
}

main "$@"
