#!/bin/bash
# daemon.sh — market-watch 守护进程管理
#
# 管理两个后台进程：
#   price-monitor.py  — 价格盯盘（HTTP polling，每5s）
#   news-monitor.py   — 新闻盯盘（RSS/API polling，默认每5分钟）
#
# 用法:
#   daemon.sh start   [--agent laok]
#   daemon.sh stop    [--agent laok]
#   daemon.sh restart [--agent laok]
#   daemon.sh status  [--agent laok]
#   daemon.sh log     [--agent laok] [--lines N]
#   daemon.sh ensure  [--agent laok]

set -euo pipefail

AGENT="${PRICE_WATCH_AGENT:-laok}"
ACTION="${1:-status}"
shift || true
LOG_LINES=40

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent)  AGENT="$2";      shift 2 ;;
        --lines)  LOG_LINES="$2";  shift 2 ;;
        *)        shift ;;
    esac
done

# M-02: 校验 AGENT 名称，防止含空格或特殊字符时注入 Shell/Python 命令
if [[ ! "$AGENT" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: invalid --agent value: '$AGENT' (only alphanumeric, _ and - allowed)" >&2
    exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PRICE_MONITOR_PY="$SKILL_DIR/scripts/price-monitor.py"
NEWS_MONITOR_PY="$SKILL_DIR/scripts/news-monitor.py"
ALERTS_FILE="$HOME/.openclaw/agents/$AGENT/private/market-alerts.json"

# PID 文件（新命名带 -price / -news 后缀）
PRICE_PID_FILE="/tmp/market-watch-${AGENT}-price.pid"
NEWS_PID_FILE="/tmp/market-watch-${AGENT}-news.pid"
# 旧 PID 文件（迁移兼容）
OLD_PID_FILE="/tmp/market-watch-${AGENT}.pid"

# 日志文件（Python RotatingFileHandler 管理）
PRICE_LOG_FILE="/tmp/market-watch-${AGENT}.log"
NEWS_LOG_FILE="/tmp/market-watch-${AGENT}-news.log"

# ── 迁移兼容：旧 PID 文件 → 新 PRICE_PID_FILE ─────────────────────────────────

migrate_old_pid() {
    if [[ -f "$OLD_PID_FILE" ]] && [[ ! -f "$PRICE_PID_FILE" ]]; then
        cp "$OLD_PID_FILE" "$PRICE_PID_FILE"
        rm -f "$OLD_PID_FILE"
    fi
}

# ── Helpers ───────────────────────────────────────────────────────────────────

is_running() {
    local pid_file="$1"
    [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null
}

count_active_by_type() {
    local alert_type="$1"
    [[ -f "$ALERTS_FILE" ]] || { echo 0; return; }
    python3 -c "
import json, sys
try:
    data = json.load(open('$ALERTS_FILE'))
    t = '$alert_type'
    n = sum(1 for a in data.get('alerts',[])
            if a.get('status')=='active' and a.get('type','price')==t)
    print(n)
except Exception:
    print(0)
" 2>/dev/null || echo 0
}

show_alerts() {
    [[ -f "$ALERTS_FILE" ]] || return
    python3 - "$ALERTS_FILE" << 'EOF'
import json, sys
try:
    data = json.load(open(sys.argv[1]))
    active = [a for a in data.get("alerts", []) if a.get("status") == "active"]
    price  = [a for a in active if a.get("type", "price") == "price"]
    news   = [a for a in active if a.get("type") == "news"]
    print(f"  活跃警报: {len(active)} 个  (价格:{len(price)} 新闻:{len(news)})")
    for a in active[:10]:
        if a.get("type", "price") == "price":
            print(f"    · [价格] {a['asset']} {a['condition']} {a['target_price']}  [{a.get('context_summary','')[:40]}]")
        else:
            kw = ', '.join(a.get('keywords', [])[:4])
            srcs = ', '.join(a.get('sources', [])[:3])
            print(f"    · [新闻] {kw}  [{srcs}]  [{a.get('context_summary','')[:30]}]")
    if len(active) > 10:
        print(f"    ... 还有 {len(active)-10} 个")
except Exception as e:
    print(f"  (无法读取警报文件: {e})")
EOF
}

start_price_monitor() {
    migrate_old_pid
    if is_running "$PRICE_PID_FILE"; then
        echo "[price-monitor] 已在运行 PID=$(cat "$PRICE_PID_FILE")"
        return 0
    fi
    mkdir -p "$(dirname "$ALERTS_FILE")"
    # stdout/stderr 丢弃到 /dev/null；日志由 Python RotatingFileHandler 管理
    nohup python3 "$PRICE_MONITOR_PY" \
        --agent "$AGENT" \
        --alerts-file "$ALERTS_FILE" \
        > /dev/null 2>&1 &
    echo $! > "$PRICE_PID_FILE"
    sleep 1
    if is_running "$PRICE_PID_FILE"; then
        echo "[price-monitor] 已启动 agent=$AGENT PID=$(cat "$PRICE_PID_FILE")"
        echo "  日志: $PRICE_LOG_FILE"
    else
        echo "[price-monitor] ❌ 启动失败"
        echo "  最后 10 行日志:"
        tail -10 "$PRICE_LOG_FILE" 2>/dev/null || echo "  (日志文件不存在)"
        return 1
    fi
}

start_news_monitor() {
    if is_running "$NEWS_PID_FILE"; then
        echo "[news-monitor] 已在运行 PID=$(cat "$NEWS_PID_FILE")"
        return 0
    fi
    mkdir -p "$(dirname "$ALERTS_FILE")"
    nohup python3 "$NEWS_MONITOR_PY" \
        --agent "$AGENT" \
        --alerts-file "$ALERTS_FILE" \
        > /dev/null 2>&1 &
    echo $! > "$NEWS_PID_FILE"
    sleep 1
    if is_running "$NEWS_PID_FILE"; then
        echo "[news-monitor] 已启动 agent=$AGENT PID=$(cat "$NEWS_PID_FILE")"
        echo "  日志: $NEWS_LOG_FILE"
    else
        echo "[news-monitor] ❌ 启动失败"
        echo "  最后 10 行日志:"
        tail -10 "$NEWS_LOG_FILE" 2>/dev/null || echo "  (日志文件不存在)"
        return 1
    fi
}

stop_price_monitor() {
    migrate_old_pid
    # 兼容：同时检查旧 PID 文件
    for pf in "$PRICE_PID_FILE" "$OLD_PID_FILE"; do
        if [[ -f "$pf" ]]; then
            PID=$(cat "$pf")
            kill "$PID" 2>/dev/null && echo "[price-monitor] 已停止 PID=$PID" || true
            rm -f "$pf"
        fi
    done
}

stop_news_monitor() {
    if is_running "$NEWS_PID_FILE"; then
        PID=$(cat "$NEWS_PID_FILE")
        kill "$PID" 2>/dev/null && echo "[news-monitor] 已停止 PID=$PID" || true
        rm -f "$NEWS_PID_FILE"
    else
        rm -f "$NEWS_PID_FILE" 2>/dev/null || true
    fi
}

# ── Actions ───────────────────────────────────────────────────────────────────

case "$ACTION" in

    start)
        migrate_old_pid
        PRICE_ACTIVE=$(count_active_by_type "price")
        NEWS_ACTIVE=$(count_active_by_type "news")

        if [[ "$PRICE_ACTIVE" -gt 0 ]]; then
            start_price_monitor
        else
            if is_running "$PRICE_PID_FILE"; then
                echo "[price-monitor] 运行中（无活跃价格警报，将在下一个循环自动退出）"
            else
                echo "[price-monitor] 无活跃价格警报，跳过启动"
            fi
        fi

        if [[ "$NEWS_ACTIVE" -gt 0 ]]; then
            start_news_monitor
        else
            if is_running "$NEWS_PID_FILE"; then
                echo "[news-monitor] 运行中（无活跃新闻警报，将在下一个循环自动退出）"
            else
                echo "[news-monitor] 无活跃新闻警报，跳过启动"
            fi
        fi

        show_alerts
        ;;

    stop)
        stop_price_monitor
        stop_news_monitor
        echo "[market-watch] 全部已停止 agent=$AGENT"
        ;;

    restart)
        bash "$0" stop  --agent "$AGENT" || true
        sleep 1
        bash "$0" start --agent "$AGENT"
        ;;

    status)
        migrate_old_pid
        echo "=== market-watch status | agent=$AGENT ==="

        if is_running "$PRICE_PID_FILE"; then
            PID=$(cat "$PRICE_PID_FILE")
            START_TIME=$(ps -p "$PID" -o lstart= 2>/dev/null | xargs || echo "未知")
            echo "[price-monitor] ✅ 运行中  PID=$PID  启动: $START_TIME"
        else
            echo "[price-monitor] ⛔ 未运行"
        fi

        if is_running "$NEWS_PID_FILE"; then
            PID=$(cat "$NEWS_PID_FILE")
            START_TIME=$(ps -p "$PID" -o lstart= 2>/dev/null | xargs || echo "未知")
            echo "[news-monitor]  ✅ 运行中  PID=$PID  启动: $START_TIME"
        else
            echo "[news-monitor]  ⛔ 未运行"
        fi

        show_alerts
        echo ""
        echo "  价格日志: $PRICE_LOG_FILE"
        echo "  新闻日志: $NEWS_LOG_FILE"
        ;;

    log)
        echo "=== price-monitor 最近 $LOG_LINES 行 ($PRICE_LOG_FILE) ==="
        if [[ -f "$PRICE_LOG_FILE" ]]; then
            tail -"$LOG_LINES" "$PRICE_LOG_FILE"
        else
            echo "（日志不存在）"
        fi

        echo ""
        echo "=== news-monitor 最近 $LOG_LINES 行 ($NEWS_LOG_FILE) ==="
        if [[ -f "$NEWS_LOG_FILE" ]]; then
            tail -"$LOG_LINES" "$NEWS_LOG_FILE"
        else
            echo "（日志不存在）"
        fi
        ;;

    ensure)
        # 有活跃警报且对应进程未运行 → 拉起；无活跃警报 → 不动
        migrate_old_pid
        PRICE_ACTIVE=$(count_active_by_type "price")
        NEWS_ACTIVE=$(count_active_by_type "news")

        if [[ "$PRICE_ACTIVE" -gt 0 ]] && ! is_running "$PRICE_PID_FILE"; then
            echo "[market-watch] $PRICE_ACTIVE 个活跃价格警报，price-monitor 未运行，拉起..."
            start_price_monitor
        fi

        if [[ "$NEWS_ACTIVE" -gt 0 ]] && ! is_running "$NEWS_PID_FILE"; then
            echo "[market-watch] $NEWS_ACTIVE 个活跃新闻警报，news-monitor 未运行，拉起..."
            start_news_monitor
        fi
        ;;

    *)
        echo "用法: daemon.sh {start|stop|restart|status|log|ensure} [--agent AGENT] [--lines N]"
        echo ""
        echo "  start   — 按需启动 price-monitor / news-monitor（有活跃警报才拉起）"
        echo "  stop    — 停止两个进程"
        echo "  restart — 停止后重新启动"
        echo "  status  — 显示两个进程状态和活跃警报"
        echo "  log     — 显示两个进程的最近日志"
        echo "  ensure  — 检查并按需拉起（被 watchdog 调用）"
        exit 1
        ;;
esac
