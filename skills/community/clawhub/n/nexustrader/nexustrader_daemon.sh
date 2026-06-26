#!/usr/bin/env bash
# =============================================================================
# NexusTrader MCP Server — Daemon Helper（Linux/macOS）
# =============================================================================
# 注意：此脚本仅是对 `nexustrader-mcp` CLI 命令的薄封装，供 Linux/macOS 用户使用。
#   Windows 用户请直接使用：
#     uv run nexustrader-mcp start / stop / status / logs
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load .env to get PROJECT_DIR
ENV_FILE="${SCRIPT_DIR}/.env"
if [[ -f "${ENV_FILE}" ]]; then
    set -a; source "${ENV_FILE}"; set +a
fi

PROJECT_DIR="${NEXUSTRADER_PROJECT_DIR:-}"
if [[ -z "${PROJECT_DIR}" ]]; then
    echo "错误：NEXUSTRADER_PROJECT_DIR 未设置。请运行 uv run nexustrader-mcp setup 重新生成配置。" >&2
    exit 1
fi

CMD="${1:-help}"
shift || true

case "${CMD}" in
    start)   uv --directory "${PROJECT_DIR}" run nexustrader-mcp start  "$@" ;;
    stop)    uv --directory "${PROJECT_DIR}" run nexustrader-mcp stop   "$@" ;;
    restart) uv --directory "${PROJECT_DIR}" run nexustrader-mcp stop   \
          && uv --directory "${PROJECT_DIR}" run nexustrader-mcp start  "$@" ;;
    status)  uv --directory "${PROJECT_DIR}" run nexustrader-mcp status "$@" ;;
    logs)    uv --directory "${PROJECT_DIR}" run nexustrader-mcp logs   "$@" ;;
    follow)
        LOG="${NEXUSTRADER_LOG_DIR:-${SCRIPT_DIR}/logs}/server.log"
        [[ -f "${LOG}" ]] || { echo "日志文件不存在，请先启动服务器。"; exit 1; }
        tail -f "${LOG}"
        ;;
    help|--help|-h)
        cat <<'EOF'
NexusTrader MCP — Daemon Helper（本脚本委托给 nexustrader-mcp CLI）

用法:  nexustrader_daemon.sh <命令> [选项]

命令:
  start [--no-wait]   后台启动（--no-wait 不等待上线）
  stop                停止
  restart             重启
  status              查看状态
  logs [行数]         查看最后 N 行日志（默认 50）
  follow              实时跟踪日志（Ctrl+C 退出）

Windows 用户直接使用：
  uv run nexustrader-mcp start / stop / status / logs
EOF
        ;;
    *) echo "未知命令: ${CMD}。运行 nexustrader_daemon.sh help"; exit 1 ;;
esac
