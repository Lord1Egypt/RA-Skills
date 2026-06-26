#!/usr/bin/env bash
# OpenClaw Portable Package Export - Wrapper Script
# Usage: openclaw-export.sh [options]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMPL_SCRIPT="${SCRIPT_DIR}/openclaw-export.impl.sh"

# Source logging library
source "${SCRIPT_DIR}/../lib/logging.sh" 2>/dev/null || {
    log_info() { echo "[INFO] $*"; }
    log_warn() { echo "[WARN] $*" >&2; }
    log_error() { echo "[ERROR] $*" >&2; }
}

# Show help
show_help() {
    cat << 'EOF'
📦 OpenClaw 可移植包导出

Usage: openclaw-export.sh [options]

Options:
  --target <dir>          导出目标目录 (默认: ~/.openclaw/exports)
  --name <name>           包名称 (默认: openclaw-portable-<timestamp>)
  --with-templates        包含环境变量模板 (默认: 启用)
  --no-templates          不包含环境变量模板
  --sanitize-env          模板化环境相关配置 (默认: 启用)
  --no-sanitize           保留原始配置值
  --with-manifest         生成清单文件 (默认: 启用)
  --no-manifest           不生成清单
  --debug                 启用调试日志
  --help, -h              显示帮助

Examples:
  # 基本导出
  bash openclaw-export.sh

  # 导出到指定目录
  bash openclaw-export.sh --target ~/backups/

  # 不模板化配置（保留原始值）
  bash openclaw-export.sh --no-sanitize

  # 调试模式
  bash openclaw-export.sh --debug

Environment Variables:
  BACKUP_LOG_LEVEL        日志级别: DEBUG, INFO, WARN, ERROR (默认: INFO)
  BACKUP_LOG_FILE         日志文件路径
  OPENCLAW_HOME          OpenClaw 主目录 (默认: ~/.openclaw)

EOF
}

# Parse arguments
parse_args() {
    export EXPORT_DIR=""
    export PACKAGE_NAME=""
    export WITH_TEMPLATES="true"
    export SANITIZE_ENV="true"
    export GENERATE_MANIFEST="true"
    export DEBUG="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --target)
                EXPORT_DIR="$2"
                shift 2
                ;;
            --name)
                PACKAGE_NAME="$2"
                shift 2
                ;;
            --with-templates)
                WITH_TEMPLATES="true"
                shift
                ;;
            --no-templates)
                WITH_TEMPLATES="false"
                shift
                ;;
            --sanitize-env)
                SANITIZE_ENV="true"
                shift
                ;;
            --no-sanitize)
                SANITIZE_ENV="false"
                shift
                ;;
            --with-manifest)
                GENERATE_MANIFEST="true"
                shift
                ;;
            --no-manifest)
                GENERATE_MANIFEST="false"
                shift
                ;;
            --debug)
                DEBUG="true"
                BACKUP_LOG_LEVEL="DEBUG"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Set defaults
    if [[ -z "${EXPORT_DIR}" ]]; then
        EXPORT_DIR="${HOME}/.openclaw/exports"
    fi
    if [[ -z "${PACKAGE_NAME}" ]]; then
        PACKAGE_NAME="openclaw-portable-$(date +"%Y-%m-%d-%H%M%S")"
    fi
}

# Main
main() {
    parse_args "$@"
    
    # Check implementation script exists
    if [[ ! -f "${IMPL_SCRIPT}" ]]; then
        log_error "实现脚本不存在: ${IMPL_SCRIPT}"
        exit 1
    fi
    
    # Source and run
    source "${IMPL_SCRIPT}"
    export_portable
}

main "$@"
