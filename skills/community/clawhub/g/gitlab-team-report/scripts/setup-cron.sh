#!/bin/bash
#
# 设置定时自动生成周报
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" \u0026\u0026 pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

CRON_COMMENT="# GitLab Weekly Report Generator"
DEFAULT_CRON="0 18 * * 5"  # 每周五 18:00

show_help() {
    cat \u003c\u003c EOF
设置定时自动生成周报

用法:
    \$0 -c <config_file> [选项]

选项:
    -c, --config FILE    配置文件路径（必需）
    --cron CRON          Cron 表达式（默认: \"$DEFAULT_CRON\"）
    --list               列出已设置的定时任务
    --remove             移除定时任务
    -h, --help           显示帮助

示例:
    # 设置每周五 18:00 自动生成
    \$0 -c config/config.json
    
    # 设置每周一 09:00 自动生成
    \$0 -c config/config.json --cron "0 9 * * 1"
    
    # 查看已设置的任务
    \$0 --list
    
    # 移除定时任务
    \$0 --remove

Cron 格式说明:
    分 时 日 月 周
    0 18 * * 5    # 每周五 18:00
    0 9 * * 1     # 每周一 09:00
    0 10 * * 0    # 每周日 10:00
EOF
}

parse_args() {
    while [[ \$# -gt 0 ]]; do
        case \$1 in
            -c|--config) CONFIG_FILE="\$2"; shift 2 ;;
            --cron) CRON_EXPR="\$2"; shift 2 ;;
            --list) LIST_MODE=true; shift ;;
            --remove) REMOVE_MODE=true; shift ;;
            -h|--help) show_help; exit 0 ;;
            *) echo "未知选项: \$1"; show_help; exit 1 ;;
        esac
    done
}

list_cron() {
    echo "📋 当前定时任务:"
    crontab -l 2>/dev/null | grep -A2 -B2 "$CRON_COMMENT" || echo "  未找到 GitLab 周报定时任务"
}

remove_cron() {
    echo "🗑️  正在移除定时任务..."
    (crontab -l 2>/dev/null | grep -v "$CRON_COMMENT") | crontab -
    echo "✅ 定时任务已移除"
}

setup_cron() {
    local config_file="\$1"
    local cron_expr="\${2:-$DEFAULT_CRON}"
    
    [[ ! -f "\$config_file" ]] \u0026\u0026 { echo "❌ 配置文件不存在: \$config_file"; exit 1; }
    
    # 获取绝对路径
    CONFIG_ABS_PATH="$(cd "$(dirname "\$config_file")" \u0026\u0026 pwd)/$(basename "\$config_file")"
    
    # 构建命令
    CMD="\$cron_expr cd \"$SKILL_DIR\" \u0026\u0026 ./scripts/generate-report.sh -c \"\$CONFIG_ABS_PATH\" \u0026\u0026 ./scripts/upload-to-feishu.sh -d \"\$SKILL_DIR/reports/latest\" \u003e\u003e \"\$SKILL_DIR/logs/cron.log\" 2\u003e\u00261 # $CRON_COMMENT"
    
    echo "⏰ 设置定时任务:"
    echo "  时间: \$cron_expr"
    echo "  命令: 生成周报并上传到飞书"
    echo ""
    
    # 移除旧的同类任务
    (crontab -l 2>/dev/null | grep -v "$CRON_COMMENT") | crontab -
    
    # 添加新任务
    (crontab -l 2>/dev/null; echo "$CMD") | crontab -
    
    echo "✅ 定时任务设置成功!"
    echo ""
    echo "📋 当前 crontab:"
    crontab -l | grep -A1 -B1 "$CRON_COMMENT"
}

main() {
    parse_args "$@"
    
    [[ "$LIST_MODE" == true ]] \u0026\u0026 { list_cron; exit 0; }
    [[ "$REMOVE_MODE" == true ]] \u0026\u0026 { remove_cron; exit 0; }
    
    [[ -z "$CONFIG_FILE" ]] \u0026\u0026 { echo "❌ 请指定配置文件 (-c)"; show_help; exit 1; }
    
    setup_cron "$CONFIG_FILE" "${CRON_EXPR:-$DEFAULT_CRON}"
}

main "$@"
