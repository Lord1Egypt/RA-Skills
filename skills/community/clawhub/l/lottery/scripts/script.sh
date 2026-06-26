#!/usr/bin/env bash
set -euo pipefail

VERSION="3.0.0"
SCRIPT_NAME="lottery"
DATA_DIR="$HOME/.local/share/lottery"
mkdir -p "$DATA_DIR"

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com

_info()  { echo "[INFO]  $*"; }
_error() { echo "[ERROR] $*" >&2; }
die()    { _error "$@"; exit 1; }

cmd_pick() {
    local count="${2:-}"
    local max="${3:-}"
    [ -z "$count" ] && die "Usage: $SCRIPT_NAME pick <count max>"
    shuf -i 1-${3:-49} -n ${2:-6} | sort -n | tr '\n' ' '; echo
}

cmd_powerball() {
    echo 'Numbers: '$(shuf -i 1-69 -n 5 | sort -n | tr '\n' ' ')' PB: '$(shuf -i 1-26 -n 1)
}

cmd_mega() {
    echo 'Numbers: '$(shuf -i 1-70 -n 5 | sort -n | tr '\n' ' ')' MB: '$(shuf -i 1-25 -n 1)
}

cmd_check() {
    local numbers="${2:-}"
    local winning="${3:-}"
    [ -z "$numbers" ] && die "Usage: $SCRIPT_NAME check <numbers winning>"
    echo 'Your: $2  Winning: $3'
}

cmd_history() {
    cat $DATA_DIR/picks.log 2>/dev/null || echo 'No history'
}

cmd_stats() {
    echo 'Total picks: '$(wc -l < $DATA_DIR/picks.log 2>/dev/null || echo 0)
}

cmd_help() {
    echo "$SCRIPT_NAME v$VERSION"
    echo ""
    echo "Commands:"
    printf "  %-25s\n" "pick <count max>"
    printf "  %-25s\n" "powerball"
    printf "  %-25s\n" "mega"
    printf "  %-25s\n" "check <numbers winning>"
    printf "  %-25s\n" "history"
    printf "  %-25s\n" "stats"
    printf "  %%-25s\n" "help"
    echo ""
    echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
}

cmd_version() { echo "$SCRIPT_NAME v$VERSION"; }

main() {
    local cmd="${1:-help}"
    case "$cmd" in
        pick) shift; cmd_pick "$@" ;;
        powerball) shift; cmd_powerball "$@" ;;
        mega) shift; cmd_mega "$@" ;;
        check) shift; cmd_check "$@" ;;
        history) shift; cmd_history "$@" ;;
        stats) shift; cmd_stats "$@" ;;
        help) cmd_help ;;
        version) cmd_version ;;
        *) die "Unknown: $cmd" ;;
    esac
}

main "$@"
