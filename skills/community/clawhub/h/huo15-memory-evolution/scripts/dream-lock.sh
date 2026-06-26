#!/usr/bin/env bash
# dream-lock.sh - Dream Consolidation Lock

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE_DIR/memory"
LOCK_FILE="$MEMORY_DIR/.dream-lock"
LOCK_TIMEOUT_MINUTES=30

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[DREAM-LOCK]${NC} $*"; }
log_ok() { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

try_acquire() {
    if [ -f "$LOCK_FILE" ]; then
        local lock_time
        lock_time=$(cat "$LOCK_FILE" | python3 -c "
import json, time
try:
    data = json.load(sys.stdin)
    lt = data.get('lock_time', 0)
    if lt:
        age = (time.time() - lt) / 60
        print('locked' if age < $LOCK_TIMEOUT_MINUTES else 'expired')
    else:
        print('expired')
except:
    print('expired')
" 2>/dev/null || echo "expired")

        if [ "$lock_time" = "locked" ]; then
            log_warn "Dream 进程正在运行"
            return 1
        fi
    fi

    python3 - "$LOCK_FILE" << 'PYEOF' 2>/dev/null || true
import json, os, time
lock_file = sys.argv[1]
with open(lock_file, 'w') as f:
    json.dump({'lock_time': time.time(), 'pid': os.getpid()}, f)
print("OK")
PYEOF

    [ $? -eq 0 ] && log_ok "已获取 dream 锁" && return 0
    return 1
}

release() {
    [ -f "$LOCK_FILE" ] && rm -f "$LOCK_FILE" && log_ok "已释放 dream 锁"
}

status() {
    if [ -f "$LOCK_FILE" ]; then
        echo "锁状态: 已锁定"
    else
        echo "锁状态: 未锁定"
    fi
}

can_run() {
    if [ -f "$LOCK_FILE" ]; then
        local lt
        lt=$(cat "$LOCK_FILE" | python3 -c "
import json, time
try:
    data = json.load(sys.stdin)
    lt = data.get('lock_time', 0)
    if lt:
        age = (time.time() - lt) / 60
        print('locked' if age < $LOCK_TIMEOUT_MINUTES else 'expired')
    else:
        print('expired')
except:
    print('expired')
" 2>/dev/null)
        [ "$lt" = "locked" ] && echo "locked" && return 1
    fi
    echo "available"
    return 0
}

main() {
    case "${1:-}" in
        -h|--help|help|"") echo "dream-lock.sh: acquire|release|status|can-run" ;;
        acquire|lock) try_acquire ;;
        release|unlock) release ;;
        status) status ;;
        can-run|can) can_run ;;
        *) echo "未知命令: $1" ;;
    esac
}

main "$@"
