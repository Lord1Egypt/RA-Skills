#!/usr/bin/env bash
# monitor-daemon.sh — 监控守护进程
# 依赖：bash + curl + jq + cron
# 用法：./scripts/monitor-daemon.sh [start|stop|status|reload]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SKILL_DIR}/config/monitor-config.yaml"
PID_FILE="/tmp/monitor-daemon.pid"
LOG_FILE="/tmp/monitor-daemon.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

start() {
  if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "监控守护进程已在运行 (PID: $(cat "$PID_FILE"))"
    exit 0
  fi

  if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "错误：配置文件不存在: $CONFIG_FILE"
    echo "请先创建 config/monitor-config.yaml"
    exit 1
  fi

  log "启动监控守护进程..."
  nohup bash "$0" _run >> "$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  log "守护进程已启动 (PID: $!)"
  echo "日志文件: $LOG_FILE"
}

stop() {
  if [[ ! -f "$PID_FILE" ]]; then
    echo "监控守护进程未运行"
    exit 0
  fi
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    rm -f "$PID_FILE"
    log "守护进程已停止 (PID: $PID)"
  else
    echo "进程 $PID 不存在，清理 PID 文件"
    rm -f "$PID_FILE"
  fi
}

status() {
  if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "✅ 监控守护进程运行中 (PID: $(cat "$PID_FILE"))"
    echo "日志文件: $LOG_FILE"
    echo ""
    echo "最近10条日志："
    tail -10 "$LOG_FILE" 2>/dev/null || echo "(暂无日志)"
  else
    echo "❌ 监控守护进程未运行"
    [[ -f "$PID_FILE" ]] && rm -f "$PID_FILE"
  fi
}

reload() {
  if [[ ! -f "$PID_FILE" ]] || ! kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "守护进程未运行，请先执行 start"
    exit 1
  fi
  kill -HUP "$(cat "$PID_FILE")"
  log "已发送 SIGHUP，配置重新加载中..."
}

_run() {
  # 读取检查间隔（默认300秒）
  INTERVAL=$(grep 'check_interval:' "$CONFIG_FILE" | awk '{print $2}' | head -1)
  INTERVAL=${INTERVAL:-300}

  log "监控循环启动，检查间隔: ${INTERVAL}s"

  # 捕获 SIGHUP 重新加载配置
  trap 'log "收到 SIGHUP，重新加载配置"; INTERVAL=$(grep "check_interval:" "$CONFIG_FILE" | awk "{print \$2}" | head -1); INTERVAL=${INTERVAL:-300}' HUP

  while true; do
    log "执行监控检查..."
    # 调用 alert-sender.sh 执行实际检查（由 AI 根据配置生成具体检查逻辑）
    if [[ -x "$SCRIPT_DIR/alert-sender.sh" ]]; then
      bash "$SCRIPT_DIR/alert-sender.sh" check-all "$CONFIG_FILE" || log "检查执行出错"
    else
      log "警告：alert-sender.sh 不存在或不可执行"
    fi
    sleep "$INTERVAL"
  done
}

case "${1:-}" in
  start)   start ;;
  stop)    stop ;;
  status)  status ;;
  reload)  reload ;;
  _run)    _run ;;
  *)
    echo "用法: $0 [start|stop|status|reload]"
    echo ""
    echo "  start   启动监控守护进程"
    echo "  stop    停止监控守护进程"
    echo "  status  查看运行状态"
    echo "  reload  重新加载配置文件"
    exit 1
    ;;
esac
