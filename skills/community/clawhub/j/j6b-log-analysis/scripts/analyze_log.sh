#!/bin/sh
# J6B泊车日志错误分析脚本 v1.0
#
# 用法:
#   ./analyze_log.sh                        # 分析板端所有模块日志
#   ./analyze_log.sh planning               # 分析planning模块日志
#   ./analyze_log.sh planning od rd         # 分析多个模块
#   ./analyze_log.sh -l planning            # 分析本地日志
#   ./analyze_log.sh -r                     # 生成分析报告
#   ./analyze_log.sh -h                     # 显示帮助

#
# ============================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 默认配置
LOG_DIR="/app/apa/log"
LOCAL_MODE=false
GENERATE_REPORT=false
REPORT_FILE=""

# 模块列表
ALL_MODULES="dr loc sensorcenter image_preprocess od rd psd gridmap planning ui_control perception_fusion"

# 统计变量
TOTAL_FATAL=0
TOTAL_ERRORS=0
TOTAL_WARNINGS=0

# ============================================================
# 帮助信息
# ============================================================
show_help() {
    echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}        J6B泊车日志错误分析脚本 v1.0${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "用法: $0 [选项] [模块名...]"
    echo ""
    echo "选项:"
    echo "  -l          本地模式（分析本地下载的日志）"
    echo "  -r          生成分析报告（保存到文件）"
    echo "  -h          显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                              # 分析板端所有模块日志"
    echo "  $0 planning                     # 分析planning模块日志"
    echo "  $0 -l planning od               # 分析本地指定模块日志"
    echo "  $0 -r                           # 生成分析报告"
    echo ""
}

# ============================================================
# 解析参数
# ============================================================
while getopts "lrh" opt; do
    case $opt in
        l) LOCAL_MODE=true ;;
        r) GENERATE_REPORT=true ;;
        h) show_help; exit 0 ;;
    esac
done
shift $((OPTIND - 1))

# 指定模块
if [ -n "$*" ]; then
    MODULES="$*"
else
    MODULES="$ALL_MODULES"
fi

# 本地模式切换日志目录
if [ "$LOCAL_MODE" = true ]; then
    LOG_DIR="./j6b_logs"
 || grep -c "^$" 2>/dev/null)
    if [ "$MODULES" = "$ALL_MODULES" ]; then
        # 查找本地日志目录下的所有子目录作为模块
        MODULES=$(ls -d "$LOG_DIR"/*/ 2>/dev/null | xargs -n 1 -basename 2>/dev/null)
    fi
fi

# 报告文件
if [ "$GENERATE_REPORT" = true ]; then
    REPORT_FILE="./analysis_report_$(date '+%Y%m%d_%H%M%S').txt"
fi

# 输出函数
output() {
    echo -e "$1"
    if [ "$GENERATE_REPORT" = true ] && [ -n "$REPORT_FILE" ]; then
        echo -e "$1" >> "$REPORT_FILE"
    fi
}

# ============================================================
# 分析函数
# ============================================================
analyze_module() {
    local module="$1"
    local module_dir="${LOG_DIR}/${module}"

    # 检查目录
    if [ ! -d "$module_dir" ]; then
        output "${YELLOW}  ⚠ 目录不存在: ${module_dir}${NC}"
        return
    fi

    # 日志文件数量
    local log_files=$(find "$module_dir" -name "*.log" -type f 2>/dev/null)
 | tail -1)
    local log_count=$(find "$module_dir" -name "*.log" -type f 2>/dev/null | wc -l)

    if [ "$log_count" -eq 0 ] || [ -z "$log_files" ]; then
        output "${YELLOW}  ⚠ 无日志文件${NC}"
        return
    fi

    # 日志大小
    local log_size=$(du -sh "$module_dir" 2>/dev/null | cut -f1)
    output "${BLUE}  日志文件: ${log_count} 个, 总大小: ${log_size}${NC}"

    # ---- FATAL 级别 ----
    local fatal_count=0
    local fatal_file=""
    for f in "$module_dir"/*.log; do
        if [ -f "$f" ]; then
            local c=$(grep -ciE "FATAL|CRITICAL|ABORT|SEGFAULT|SEGMENTATION|Bus error" "$f" 2>/dev/null || echo 0)
            if [ "$c" -gt 0 ] 2>/dev/null; then
                fatal_count=$((fatal_count + c))
                fatal_file="$f"
            fi
        fi
    done

    if [ "$fatal_count" -gt 0 ]; then
        output "${RED}  🔴 致命错误: ${fatal_count} 条${NC}"
        grep -inE "FATAL|CRITICAL|ABORT|SEGFAULT|SEGMENTATION|Bus error" "$module_dir"/*.log 2>/dev/null | tail -5 | while read line; do
            output "${RED}     ${line}${NC}"
        done
        TOTAL_FATAL=$((TOTAL_FATAL + fatal_count))
    fi

    # ---- ERROR 级别 ----
    local error_count=0
    for f in "$module_dir"/*.log; do
        if [ -f "$f" ]; then
            local c=$(grep -ciE "ERROR|FAILED|FAILURE|TIMEOUT" "$f" 2>/dev/null || echo 0)
            if [ "$c" -gt 0 ] 2>/dev/null; then
                error_count=$((error_count + c))
            fi
        fi
    done
    if [ "$error_count" -gt 0 ]; then
        output "${YELLOW}  🟡 错误: ${error_count} 条${NC}"

        # 错误分类
        local timeout_c=0
        local fail_c=0
        for f in "$module_dir"/*.log; do
            if [ -f "$f" ]; then
                local tc=$(grep -ci "TIMEOUT" "$f" 2>/dev/null || echo 0)
)
                local fc=$(grep -ciE "FAILED|FAILURE" "$f" 2>/dev/null || echo 0)
)
                timeout_c=$((timeout_c + tc))
                fail_c=$((fail_c + fc))
            fi
        done
        [ "$timeout_c" -gt 0 ] 2>/dev/null && output "     超时: ${timeout_c} 条"
        [ "$fail_c" -gt 0 ] 2>/dev/null && output "     失败: ${fail_c} 条"
        local other_c=$((error_count - timeout_c - fail_c))
        [ "$other_c" -gt 0 ] 2>/dev/null && output "     其他: ${other_c} 条"

        # 最近5条错误
        grep -inE "ERROR|FAILED|FAILURE|TIMEOUT" "$module_dir"/*.log 2>/dev/null | tail -5 | while read line; do
            output "${YELLOW}     ${line}${NC}"
        done
        TOTAL_ERRORS=$((TOTAL_ERRORS + error_count))
    else
        output "${GREEN}  ✅ 无错误${NC}"
    fi

    # ---- WARN 级别 ----
    local warn_count=0
    for f in "$module_dir"/*.log; do
        if [ -f "$f" ]; then
            local c=$(grep -ciE "WARN|WARNING|DEPRECATED" "$f" 2>/dev/null || echo 0)
            if [ "$c" -gt 0 ] 2>/dev/null; then
                warn_count=$((warn_count + c))
            fi
        fi
    done
    if [ "$warn_count" -gt 0 ]; then
        output "${BLUE}  ⚡ 警告: ${warn_count} 条${NC}"
        TOTAL_WARNINGS=$((TOTAL_WARNINGS + warn_count))
    fi

    # ---- 模式检测 ----
    output "${PURPLE}  【模式检测】${NC}"
    # 感知丢失目标
    local p1=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p1=$((p1 + $(grep -ci "Found 0 obstacles\|No object detected\|Detection failed" "$f" 2>/dev/null || echo 0)))
    done
    [ "$p1" -gt 0 ] 2>/dev/null && output "${RED}    🔍 感知丢失目标: ${p1} 次${NC}"

    # 规划失败
    local p2=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p2=$((p2 + $(grep -ci "Path planning failed\|No valid path\|Planning timeout" "$f" 2>/dev/null || echo 0)))
    done
    [ "$p2" -gt 0 ] 2>/dev/null && output "${RED}    🗺️ 规划失败: ${p2} 次${NC}"

    # 定位漂移
    local p3=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p3=$((p3 + $(grep -ci "Pose drift\|Localization error\|Pose jump" "$f" 2>/dev/null || echo 0))
    done
    [ "$p3" -gt 0 ] 2>/dev/null && output "${RED}    📍 定位漂移: ${p3} 次${NC}"
    # CAN通信异常
    local p4=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p4=$((p4 + $(grep -ci "CAN timeout\|CAN frame lost\|Communication error" "$f" 2>/dev/null || echo 0))
    done
    [ "$p4" -gt 0 ] 2>/dev/null && output "${RED}    🔌 CAN通信异常: ${p4} 次${NC}"
    # 进程崩溃
    local p5=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p5=$((p5 + $(grep -ci "Segmentation fault\|Bus error\|Process crashed\|core dumped" "$f" 2>/dev/null || echo 0))
    done
    [ "$p5" -gt 0 ] 2>/dev/null && output "${RED}    💥 进程崩溃: ${p5} 次${NC}"

    # 内存问题
    local p6=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p6=$((p6 + $(grep -ci "OOM\|out of memory\|alloc.*fail\|lowmem" "$f" 2>/dev/null || echo 0))
    done
    [ "$p6" -gt 0 ] 2>/dev/null && output "${RED}    💾 内存问题: ${p6} 次${NC}"
    # 锁竞争/死锁
    local p7=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p7=$((p7 + $(grep -ci "Mtx\|Sem\|mutex\|lock timeout\|deadlock" "$f" 2>/dev/null || echo 0))
    done
    [ "$p7" -gt 0 ] 2>/dev/null && output "${RED}    🔒 锁竞争/死锁: ${p7} 次${NC}"
    # 时序异常
    local p8=0
    for f in "$module_dir"/*.log; do
        [ -f "$f" ] && p8=$((p8 + $(grep -ci "timestamp\|clock drift\|time sync" "$f" 2>/dev/null || echo 0))
    done
    [ "$p8" -gt 0 ] 2>/dev/null && output "${RED}    ⏱️ 时序异常: ${p8} 次${NC}"
}

# ============================================================
# 主程序
# ============================================================
output "${CYAN}══════════════════════════════════════════════════════════${NC}"
output "${CYAN}        J6B泊车日志错误分析${NC}  $(date '+%Y-%m-%d %H:%M:%S')"
output "${CYAN}══════════════════════════════════════════════════════════${NC}"
output "${BLUE}【分析模块】${NC} ${MODULES}"
output ""

# 逐模块分析
for module in $MODULES; do
    output ""
    output "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    output "${YELLOW}  分析模块: ${module}${NC}"
    output "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    analyze_module "$module"
done

# ============================================================
# 分析摘要
# ============================================================
output ""
output "${CYAN}══════════════════════════════════════════════════════════${NC}"
output "${CYAN}                     分析摘要${NC}"
output "${CYAN}══════════════════════════════════════════════════════════${NC}"
output ""

# 总体状态
TOTAL_ISSUES=$((TOTAL_FATAL + TOTAL_ERRORS + TOTAL_WARNINGS))
if [ "$TOTAL_FATAL" -gt 0 ]; then
    output "${RED}【严重程度】🔴 存在致命错误${NC}"
elif [ "$TOTAL_ERRORS" -gt 0 ]; then
    output "${YELLOW}【严重程度】🟡 存在错误${NC}"
elif [ "$TOTAL_WARNINGS" -gt 0 ]; then
    output "${GREEN}【严重程度】🟢 仅有警告${NC}"
else
    output "${GREEN}【严重程度】✅ 未发现问题${NC}"
fi

 output ""
output "${PURPLE}【统计信息】${NC}"
output "  致命错误: ${TOTAL_FATAL} 条"
output "  普通错误: ${TOTAL_ERRORS} 条"
output "  警告信息: ${TOTAL_WARNINGS} 条"
output "  总计:     ${TOTAL_ISSUES} 条"

# 建议操作
output ""
output "${YELLOW}【建议操作】${NC}"
if [ "$TOTAL_FATAL" -gt 0 ]; then
    output "${RED}  1. 存在致命错误，请立即排查！${NC}"
    output "     - 检查 coredump: ls -la /log/coredump/"
    output "     - 查看重启原因: cat /log/reset_reason.txt"
    output "     - 查看系统日志: slog2info | grep -i 'crash'"
fi
if [ "$TOTAL_ERRORS" -gt 0 ]; then
    output "${YELLOW}  2. 存在 ${TOTAL_ERRORS} 条错误，建议重点关注${NC}"
    output "     - 查看详细错误: grep -i 'error' /app/apa/log/*/*.log"
fi
if [ "$TOTAL_WARNINGS" -gt 0 ]; then
    output "${BLUE}  3. 存在 ${TOTAL_WARNINGS} 条警告，可选择性关注${NC}"
fi
if [ "$TOTAL_ISSUES" -eq 0 ]; then
    output "${GREEN}  ✅ 系统日志正常，无异常${NC}"
fi
output ""

# 报告提示
if [ "$GENERATE_REPORT" = true ] && [ -n "$REPORT_FILE" ]; then
    output "${GREEN}分析报告已保存至: ${REPORT_FILE}${NC}"
fi
