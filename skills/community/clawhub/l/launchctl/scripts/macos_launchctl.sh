#!/bin/bash
# ============================================================
# macOS Launchctl Manager - 定时启停 macOS 应用
# 用法: macos_launchctl.sh <command> [options]
#
# 兼容性说明：macOS 默认 bash 为 3.2 版本，对中文 regex 支持不佳。
# 时间解析使用 sed/awk 替代 bash 内置正则，确保跨 shell 兼容。
#
# Commands:
#   create  <app_path> <schedule> [--label <label>] [--args "<args>"]
#           [--start-only|--stop-only] [--stop-at <stop_schedule>]
#           [--yes|--confirm|--dry-run]                         创建定时启停任务
#   list    [--type all|active|inactive]                       列出任务
#   start   <label>                                            启动指定任务
#   stop    <label>                                            停止指定任务
#   restart <label>                                            重启任务
#   remove  <label> [--yes|--dry-run]                          删除任务
#   info    <label>                                            查看任务详情
#   status  <label>                                           查看任务运行状态
#
# 安全参数说明：
#   --yes       跳过确认，直接执行（仅限非交互式自动化场景）
#   --confirm   执行前要求用户交互确认（默认行为，可省略）
#   --dry-run   仅展示将要执行的操作，不实际写入或加载
#
# Schedule 格式 (支持自然语言和 cron):
#   - "每天 9:00" / "每天上午9点" / "daily at 09:00"
#   - "每小时" / "每2小时" / "hourly" / "every 2h"
#   - "每周一 9:00" / "周一到周五 8:30"
#   - 标准 cron: "* * * * *" (分 时 日 月 周)
# ============================================================

set -euo pipefail

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_CYAN='\033[0;36m'
COLOR_RESET='\033[0m'

log_info()  { echo -e "${COLOR_GREEN}[✓]${COLOR_RESET} $*"; }
log_warn()  { echo -e "${COLOR_YELLOW}[!]${COLOR_RESET} $*"; }
log_error() { echo -e "${COLOR_RED}[×]${COLOR_RESET} $*"; }
log_step()  { echo -e "${COLOR_BLUE}[→]${COLOR_RESET} $*"; }

# 获取用户登录 UID（launchctl 需要）
get_user_uid() {
    id -u
}

# 解析应用路径：支持应用名、路径、bundle identifier
resolve_app_path() {
    local input="$1"

    # 如果已经是绝对路径，直接返回
    if [[ "$input" == /* ]]; then
        if [[ -f "$input" || -d "$input" ]]; then
            echo "$input"
            return 0
        fi
        log_error "文件路径不存在: $input"
        return 1
    fi

    # 尝试在 /Applications 和 ~/Applications 中查找
    local search_paths=(
        "/Applications/${input}.app"
        "/Applications/${input}"
        "$HOME/Applications/${input}.app"
        "$HOME/Applications/${input}"
    )

    for path in "${search_paths[@]}"; do
        if [[ -d "$path" ]]; then
            log_info "找到应用: $path"
            echo "$path"
            return 0
        fi
    done

    # 尝试 mdfind 搜索
    local found
    found=$(mdfind "kMDItemKind == 'Application' && kMDItemFSName == '${input}.app'" 2>/dev/null | head -1)
    if [[ -n "$found" && -d "$found" ]]; then
        log_info "通过搜索找到应用: $found"
        echo "$found"
        return 0
    fi

    # 可能是 bundle identifier
    if mdfind "kMDItemCFBundleIdentifier == '${input}'" >/dev/null 2>&1; then
        local bundle_path
        bundle_path=$(mdfind "kMDItemCFBundleIdentifier == '${input}'" 2>/dev/null | grep '\.app$' | head -1)
        if [[ -n "$bundle_path" ]]; then
            log_info "通过 Bundle ID 找到应用: $bundle_path"
            echo "$bundle_path"
            return 0
        fi
    fi

    log_error "无法找到应用: $input"
    log_warn "请使用完整路径或 .app 名称"
    return 1
}

# 将自然语言时间转换为 cron 表达式
# 使用 grep/sed 替代 bash 内置 regex，兼容 macOS bash 3.2 和 zsh
parse_schedule() {
    local schedule="$1"

    # 用 grep -oE 提取时间 HH:MM（macOS grep -E 完全支持 POSIX 扩展正则）
    local time_match
    time_match=$(echo "$schedule" | grep -oE '[0-9]{1,2}:[0-9]{2}' | tail -1)

    local hour=""
    local min="00"
    if [[ -n "$time_match" ]]; then
        hour="${time_match%:*}"
        min="${time_match#*:}"
    fi

    # 如果没有提取到时间，报错
    if [[ -z "$hour" ]]; then
        log_error "无法解析时间格式: $schedule"
        return 1
    fi

    # 判断星期范围（工作日 / 周末）
    local dow="*"
    if echo "$schedule" | grep -qE '(工作日|weekday|周一到周五|周一.*周五)'; then
        dow="1-5"
    elif echo "$schedule" | grep -qE '(周末|weekend|周六到周日|周六.*周日)'; then
        dow="0,6"
    elif echo "$schedule" | grep -qE '周日|星期日|\bsun\b'; then
        dow="0"
    elif echo "$schedule" | grep -qE '周一|星期一|\bmon\b'; then
        dow="1"
    elif echo "$schedule" | grep -qE '周二|星期二|\btue\b'; then
        dow="2"
    elif echo "$schedule" | grep -qE '周三|星期三|\bwed\b'; then
        dow="3"
    elif echo "$schedule" | grep -qE '周四|星期四|\bthu\b'; then
        dow="4"
    elif echo "$schedule" | grep -qE '周五|星期五|\bfri\b'; then
        dow="5"
    elif echo "$schedule" | grep -qE '周六|星期六|\bsat\b'; then
        dow="6"
    fi

    # ===== 每小时 / 每 N 小时 =====
    if echo "$schedule" | grep -qE '^(每[0-9]*小时?|hourly|every *[0-9]*h)$'; then
        local interval=1
        if [[ "$hour" =~ ^[0-9]+$ ]] && [[ "$hour" -gt 0 && "$hour" -lt 24 ]]; then
            interval="$hour"
        else
            local extracted_num
            extracted_num=$(echo "$schedule" | grep -oE '[0-9]+' | head -1)
            if [[ -n "$extracted_num" ]]; then
                interval="$extracted_num"
            fi
        fi
        echo "0 */${interval} * * *"
        return 0
    fi

    # 处理上午/下午/凌晨
    if echo "$schedule" | grep -qE '下午|pm'; then
        hour=$((hour + 12))
        if [[ "$hour" -ge 24 ]]; then hour=12; fi
    elif echo "$schedule" | grep -qE '(凌晨|上午|am)' && [[ "$hour" -eq 12 ]]; then
        hour=0
    fi

    printf "%02d %02d * * %s\n" "$min" "$hour" "$dow"
    return 0
}

# 生成 plist 文件内容
# cron_expr 格式：minute hour day month weekday
# weekday 支持 * / 0-6 / 0,6 / 1-5 等格式
generate_plist() {
    local label="$1"
    local app_path="$2"
    local cron_expr="$3"
    local extra_args="${4:-}"

    # 解析 cron 字段
    local minute hour day month weekday
    read -r minute hour day month weekday <<< "$cron_expr"

    # 生成 Weekday 片段列表（若 weekday 不是 *，则展开为多个 dict）
    local wd_dicts=""
    if [[ "$weekday" == "*" || -z "$weekday" ]]; then
        # 不限星期几：不加 Weekday key
        wd_dicts="        <dict>\n            <key>Minute</key>\n            <integer>${minute}</integer>\n            <key>Hour</key>\n            <integer>${hour}</integer>\n        </dict>"
    else
        # 展开 weekday：支持 1-5、0,6、单个数字
        local wd_list=""
        if [[ "$weekday" == *-* ]]; then
            # 范围：1-5
            local wd_start wd_end
            wd_start="${weekday%-*}"
            wd_end="${weekday#*-}"
            for ((wd=wd_start; wd<=wd_end; wd++)); do
                wd_list="$wd_list $wd"
            done
        elif [[ "$weekday" == *,* ]]; then
            # 逗号分隔：0,6
            wd_list=$(echo "$weekday" | tr ',' ' ')
        else
            wd_list="$weekday"
        fi
        for wd in $wd_list; do
            wd_dicts="${wd_dicts}        <dict>\n            <key>Minute</key>\n            <integer>${minute}</integer>\n            <key>Hour</key>\n            <integer>${hour}</integer>\n            <key>Weekday</key>\n            <integer>${wd}</integer>\n        </dict>\n"
        done
        # 去掉末尾多余的 \n
        wd_dicts=$(echo "$wd_dicts" | sed '/^$/d')
    fi

    cat <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${label}</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>-a</string>
        <string>${app_path}</string>
${extra_args:+        <string>${extra_args}</string>}
    </array>

    <key>StartCalendarInterval</key>
    <array>
$(echo -e "$wd_dicts")
    </array>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string>/tmp/${label}.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/${label}-error.log</string>
</dict>
</plist>
PLISTEOF
}

# 生成停止应用的 plist（用 osascript quit）
generate_stop_plist() {
    local label="$1"
    local app_name="$2"
    local cron_expr="$3"

    local minute hour day month weekday
    read -r minute hour day month weekday <<< "$cron_expr"

    local wd_dicts=""
    if [[ "$weekday" == "*" || -z "$weekday" ]]; then
        wd_dicts="        <dict>\n            <key>Minute</key>\n            <integer>${minute}</integer>\n            <key>Hour</key>\n            <integer>${hour}</integer>\n        </dict>"
    else
        local wd_list=""
        if [[ "$weekday" == *-* ]]; then
            local wd_start="${weekday%-*}"
            local wd_end="${weekday#*-}"
            for ((wd=wd_start; wd<=wd_end; wd++)); do
                wd_list="$wd_list $wd"
            done
        elif [[ "$weekday" == *,* ]]; then
            wd_list=$(echo "$weekday" | tr ',' ' ')
        else
            wd_list="$weekday"
        fi
        for wd in $wd_list; do
            wd_dicts="${wd_dicts}        <dict>\n            <key>Minute</key>\n            <integer>${minute}</integer>\n            <key>Hour</key>\n            <integer>${hour}</integer>\n            <key>Weekday</key>\n            <integer>${wd}</integer>\n        </dict>\n"
        done
        wd_dicts=$(echo "$wd_dicts" | sed '/^$/d')
    fi

    cat <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${label}</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/osascript</string>
        <string>-e</string>
        <string>tell application "${app_name}" to quit</string>
    </array>

    <key>StartCalendarInterval</key>
    <array>
$(echo -e "$wd_dicts")
    </array>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string>/tmp/${label}.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/${label}-error.log</string>
</dict>
</plist>
PLISTEOF
}

# ============================================================
# 安全交互函数
# ============================================================

# 展示操作计划（用于 create 命令的 dry-run/预览模式）
show_create_plan() {
    local app_name="$1"
    local app_path="$2"
    local start_label="$3"
    local stop_label="$4"
    local start_schedule_human="$5"
    local stop_schedule_human="$6"
    local start_cron="$7"
    local stop_cron="$8"
    local mode="$9"
    local agent_dir="$10"

    echo ""
    echo -e "${COLOR_CYAN}${COLOR_CYAN}========================================${COLOR_RESET}"
    echo -e "${COLOR_CYAN}  📋 定时任务执行计划（预览） ${COLOR_RESET}"
    echo -e "${COLOR_CYAN}========================================${COLOR_RESET}"
    echo ""
    echo -e "  应用:  ${COLOR_YELLOW}${app_name}${COLOR_RESET}"
    echo -e "  路径:  ${app_path}"
    echo ""
    if [[ "$mode" == "both" || "$mode" == "start_only" ]]; then
        echo -e "  ${COLOR_GREEN}▸ 启动任务${COLOR_RESET}"
        echo -e "    Label:     ${start_label}"
        echo -e "    调度时间:   ${start_schedule_human} (${start_cron})"
        echo -e "    Plist路径:  ${agent_dir}/${start_label}.plist"
        echo -e "    执行命令:   launchctl load '${agent_dir}/${start_label}.plist'"
        echo ""
    fi
    if [[ "$mode" == "both" || "$mode" == "stop_only" ]]; then
        echo -e "  ${COLOR_RED}▸ 停止任务${COLOR_RESET}"
        echo -e "    Label:     ${stop_label}"
        echo -e "    调度时间:   ${stop_schedule_human:-同上} (${stop_cron:-同上})"
        echo -e "    Plist路径:  ${agent_dir}/${stop_label}.plist"
        echo -e "    执行命令:   launchctl load '${agent_dir}/${stop_label}.plist'"
        echo ""
    fi
    echo -e "${COLOR_CYAN}========================================${COLOR_RESET}"
    echo ""
}

# 展示删除计划（用于 remove 的 dry-run/预览模式）
show_remove_plan() {
    local prefix="$1"
    local agent_dir="$2"

    echo ""
    echo -e "${COLOR_RED}${COLOR_RED}========================================${COLOR_RESET}"
    echo -e "${COLOR_RED}  ⚠️  定时任务删除计划（预览）${COLOR_RESET}"
    echo -e "${COLOR_RED}========================================${COLOR_RESET}"
    echo ""

    local found_any=false
    for plist in "$agent_dir"/${prefix}*.plist; do
        [[ -f "$plist" ]] || continue
        local label
        label=$(basename "$plist" .plist)
        found_any=true
        echo -e "  ${COLOR_RED}✗ 将删除: ${COLOR_RESET}${label}"
        echo -e "    文件:      ${plist}"
        echo -e "    备份至:    ${plist}.bak.$(date +%Y%m%d%H%M%S)"
        echo -e "    执行命令:  launchctl unload '${plist}' && rm '${plist}'"
        echo ""
    done

    if ! $found_any; then
        echo -e "  ${COLOR_YELLOW}未找到匹配 '${prefix}' 的任务${COLOR_RESET}"
        echo ""
    fi

    echo -e "${COLOR_RED}========================================${COLOR_RESET}"
    echo ""
}

# 交互式确认（默认行为）
ask_confirm() {
    local prompt="${1:-是否继续？}"
    echo -en "${COLOR_YELLOW}[?] ${prompt} (y/N): ${COLOR_RESET}"
    local answer
    read -r answer
    case "$answer" in
        y|Y|yes|YES|"是"|"确认"|confirm)
            return 0 ;;
        *)
            echo -e "${COLOR_CYAN}[i] 操作已取消。${COLOR_RESET}"
            return 1 ;;
    esac
}

# ============================================================
# 命令实现
# ============================================================

cmd_create() {
    if [[ $# -lt 2 ]]; then
        log_error "用法: $0 create <app_path_or_name> <schedule> [--label <label>] [--start-only|--stop-only] [--args \"arguments\"] [--stop-at <stop_schedule>] [--yes|--confirm|--dry-run]"
        exit 1
    fi

    local app_input="$1"
    local schedule="$2"
    shift 2

    local custom_label=""
    local mode="both"       # both | start_only | stop_only
    local extra_args=""
    local stop_schedule=""
    local flag_yes=false    # skip confirmation
    local flag_dry_run=false  # preview only, no actual execution

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --label)
                custom_label="$2"; shift 2 ;;
            --start-only)
                mode="start_only"; shift ;;
            --stop-only)
                mode="stop_only"; shift ;;
            --args)
                extra_args="$2"; shift 2 ;;
            --stop-at)
                stop_schedule="$2"; shift 2 ;;
            --yes|-y)
                flag_yes=true; shift ;;
            --confirm)
                shift ;;  # default behavior, no-op but accepted
            --dry-run)
                flag_dry_run=true; shift ;;
            *)
                log_error "未知参数: $1"; exit 1 ;;
        esac
    done

    log_step "解析应用路径..."
    local app_path
    app_path=$(resolve_app_path "$app_input") || exit 1

    # 提取应用名称
    local app_name
    app_name=$(basename "$app_path" .app)

    # 生成 label（使用 tr 转小写，兼容 bash 3.2）
    local app_name_lower
    app_name_lower=$(echo "$app_name" | tr '[:upper:]' '[:lower:]')
    local label="${custom_label:-com.user.launch.${app_name_lower}}"

    log_step "解析时间调度..."
    local cron_expr
    cron_expr=$(parse_schedule "$schedule") || exit 1
    log_info "Cron 表达式: $cron_expr"

    local uid
    uid=$(get_user_uid)
    local agent_dir="$HOME/Library/LaunchAgents"

    # 解析停止时间
    local stop_cron=""
    if [[ "$mode" == "both" || "$mode" == "stop_only" ]]; then
        if [[ -n "$stop_schedule" ]]; then
            stop_cron=$(parse_schedule "$stop_schedule") || exit 1
            log_info "停止时间 Cron: $stop_cron"
        else
            stop_cron="$cron_expr"
            log_warn "未指定 --stop-at，停止任务将使用与启动相同的时间调度（请手动修改或重新指定）"
        fi
    fi

    local start_label="${label}.start"
    local stop_label="${label}.stop"

    # ===== 展示执行计划 =====
    show_create_plan \
        "$app_name" "$app_path" \
        "$start_label" "$stop_label" \
        "$schedule" "${stop_schedule:-同上}" \
        "$cron_expr" "${stop_cron:-同上}" \
        "$mode" "$agent_dir"

    # dry-run: 仅预览，不执行
    if $flag_dry_run; then
        log_info "[DRY RUN] 预览完成，未执行任何写入操作。"
        log_info "去掉 --dry-run 参数后重新运行以实际创建任务。"
        return 0
    fi

    # 默认需要用户确认（除非传了 --yes）
    if ! $flag_yes; then
        ask_confirm "以上计划是否确认执行？" || return 0
    fi

    mkdir -p "$agent_dir"

    if [[ "$mode" == "both" || "$mode" == "start_only" ]]; then
        local plist_file="$agent_dir/${start_label}.plist"

        log_step "创建启动任务: ${start_label}..."
        generate_plist "$start_label" "$app_path" "$cron_expr" "$extra_args" > "$plist_file"

        # 加载 plist
        launchctl load "$plist_file" 2>/dev/null && \
            log_info "启动任务已创建并加载: $plist_file" || \
            log_warn "plist 已创建但加载失败，可能需要手动执行: launchctl load '$plist_file'"
    fi

    if [[ "$mode" == "both" || "$mode" == "stop_only" ]]; then
        local stop_plist_file="$agent_dir/${stop_label}.plist"

        log_step "创建停止任务: ${stop_label}..."
        generate_stop_plist "$stop_label" "$app_name" "$stop_cron" > "$stop_plist_file"

        launchctl load "$stop_plist_file" 2>/dev/null && \
            log_info "停止任务已创建并加载: $stop_plist_file" || \
            log_warn "plist 已创建但加载失败"
    fi

    echo ""
    log_info "========== 任务摘要 =========="
    log_info "应用: ${app_name} (${app_path})"
    log_info "启动 Label: ${label}.start"
    log_info "启动调度: $schedule ($cron_expr)"
    if [[ "$mode" != "start_only" ]]; then
        log_info "停止 Label: ${label}.stop"
        log_info "停止调度: ${stop_schedule:-同上} (${stop_cron:-同上})"
    fi
    log_info "Plist 目录: $agent_dir/"
    log_info "================================="
    echo ""
    log_tip "管理命令:"
    log_tip "  查看状态:  $0 status ${label}.start"
    log_tip "  手动启动:  $0 start ${label}.start"
    log_tip "  手动停止:  $0 stop ${label}.start"
    log_tip "  删除任务:  $0 remove ${label}"
}

cmd_list() {
    local filter_type="${1:-all}"
    local uid
    uid=$(get_user_uid)

    echo ""
    echo -e "${COLOR_CYAN}===== 用户 LaunchAgents 任务列表 =====${COLOR_RESET}"
    echo ""

    local count=0

    for plist in "$HOME"/Library/LaunchAgents/*.plist; do
        [[ -f "$plist" ]] || continue

        local label
        label=$(/usr/libexec/PlistBuddy -c "Print :Label" "$plist" 2>/dev/null || echo "")
        [[ -z "$label" ]] && continue

        # 过滤类型
        local is_loaded=false
        if launchctl list "$label" &>/dev/null; then
            is_loaded=true
        fi

        if [[ "$filter_type" == "active" && "$is_loaded" == false ]]; then
            continue
        fi
        if [[ "$filter_type" == "inactive" && "$is_loaded" == true ]]; then
            continue
        fi

        ((count++)) || true

        # 提取信息
        local program=""
        program=$(/usr/libexec/PlistBuddy -c "Print :ProgramArguments:0" "$plist" 2>/dev/null || echo "-")
        local program_arg=""
        program_arg=$(/usr/libexec/PlistBuddy -c "Print :ProgramArguments:2" "$plist" 2>/dev/null || echo "")

        local schedule="-"
        if /usr/libexec/PlistBuddy -c "Print :StartCalendarInterval:Hour" "$plist" &>/dev/null; then
            local sch_hour sch_min sch_wday
            sch_hour=$(/usr/libexec/PlistBuddy -c "Print :StartCalendarInterval:Hour" "$plist" 2>/dev/null || echo "?")
            sch_min=$(/usr/libexec/PlistBuddy -c "Print :StartCalendarInterval:Minute" "$plist" 2>/dev/null || echo "?")
            sch_wday=$(/usr/libexec/PlistBuddy -c "Print :StartCalendarInterval:Weekday" "$plist" 2>/dev/null || echo "*")
            schedule="${sch_hour}:${sch_min} (周${sch_wday})"
        fi

        local pid="-"
        local status_text=""
        if $is_loaded; then
            pid=$(launchctl list "$label" 2>/dev/null | tail -1 | awk '{print $1}')
            if [[ "$pid" != "-" && -n "$pid" ]]; then
                status_text="${COLOR_GREEN}运行中 (PID: ${pid})${COLOR_RESET}"
            else
                status_text="${COLOR_YELLOW}已加载(等待触发)${COLOR_RESET}"
            fi
        else
            status_text="${COLOR_GRAY:-}未加载${COLOR_RESET}"
        fi

        echo -e "  ${COLOR_BLUE}${count}.${COLOR_RESET} ${COLOR_CYAN}${label}${COLOR_RESET}"
        echo -e "     程序: ${program_arg:-$program}"
        echo -e "     调度: $schedule"
        echo -e "     状态: $status_text"
        echo -e "     Plist: $(basename "$plist")"
        echo ""
    done

    if [[ "$count" -eq 0 ]]; then
        log_warn "没有找到匹配的任务 (${filter_type})"
    else
        echo -e "共 ${count} 个任务"
    fi
}

cmd_start() {
    if [[ $# -lt 1 ]]; then
        log_error "用法: $0 start <label>"
        exit 1
    fi
    local label="$1"

    log_step "启动任务: ${label}..."
    launchctl kickstart -k "gui/$(get_user_uid)/${label}" 2>/dev/null || \
    launchctl start "$label" 2>/dev/null
    if [[ $? -eq 0 ]]; then
        log_info "任务已触发: $label"
    else
        log_warn "尝试直接运行任务..."
        local plist="$HOME/Library/LaunchAgents/${label}.plist"
        if [[ -f "$plist" ]]; then
            local program=$(/usr/libexec/PlistBuddy -c "Print :ProgramArguments:0" "$plist" 2>/dev/null)
            local arg1=$(/usr/libexec/PlistBuddy -c "Print :ProgramArguments:1" "$plist" 2>/dev/null)
            local arg2=$(/usr/libexec/PlistBuddy -c "Print :ProgramArguments:2" "$plist" 2>/dev/null)
            if [[ -n "$program" ]]; then
                "$program" "${arg1:-}" "${arg2:-}" &
                log_info "已手动执行: $program $arg1 $arg2"
            fi
        else
            log_error "无法找到 plist: $plist"
        fi
    fi
}

cmd_stop() {
    if [[ $# -lt 1 ]]; then
        log_error "用法: $0 stop <label>"
        exit 1
    fi
    local label="$1"

    log_step "停止任务: ${label}..."
    # 先尝试 stop，再尝试 kill
    launchctl stop "$label" 2>/dev/null || true
    sleep 0.5

    # 获取 PID 并终止进程
    local pid
    pid=$(launchctl list "$label" 2>/dev/null | tail -1 | awk '{print $1}')
    if [[ -n "$pid" && "$pid" != "-" ]]; then
        kill "$pid" 2>/dev/null && log_info "已终止 PID: $pid" || log_warn "进程可能已退出"
    else
        log_info "任务已停止: $label"
    fi
}

cmd_restart() {
    if [[ $# -lt 1 ]]; then
        log_error "用法: $0 restart <label>"
        exit 1
    fi
    local label="$1"
    cmd_stop "$label"
    sleep 1
    cmd_start "$label"
}

cmd_remove() {
    if [[ $# -lt 1 ]]; then
        log_error "用法: $0 remove <label_prefix> [--yes|--dry-run]"
        exit 1
    fi
    local prefix="$1"
    shift
    local uid
    uid=$(get_user_uid)
    local agent_dir="$HOME/Library/LaunchAgents"

    local flag_yes=false
    local flag_dry_run=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --yes|-y)
                flag_yes=true; shift ;;
            --dry-run)
                flag_dry_run=true; shift ;;
            *)
                log_error "未知参数: $1"; exit 1 ;;
        esac
    done

    # ===== 展示删除计划 =====
    show_remove_plan "$prefix" "$agent_dir"

    # dry-run: 仅预览
    if $flag_dry_run; then
        log_info "[DRY RUN] 预览完成，未执行任何删除操作。"
        log_info "去掉 --dry-run 参数后重新运行以实际删除。"
        return 0
    fi

    # 确认
    if ! $flag_yes; then
        ask_confirm "确认删除以上任务？（原文件将被备份）" || return 0
    fi

    local removed=0

    log_step "删除匹配 '${prefix}' 的任务..."

    for plist in "$agent_dir"/${prefix}*.plist; do
        [[ -f "$plist" ]] || continue
        local label
        label=$(basename "$plist" .plist)

        # 卸载
        launchctl unload "$plist" 2>/dev/null && log_info "已卸载: $label" || log_warn "卸载失败: $label"

        # 备份再删除
        cp "$plist" "$plist.bak.$(date +%Y%m%d%H%M%S)" 2>/dev/null
        rm "$plist" && log_info "已删除: $(basename "$plist")" || log_warn "删除失败: $plist"

        ((removed++)) || true
    done

    if [[ "$removed" -gt 0 ]]; then
        log_info "共移除 $removed 个任务（原文件已备份）"
    else
        log_warn "没有找到匹配 '${prefix}' 的任务"
    fi
}

cmd_info() {
    if [[ $# -lt 1 ]]; then
        log_error "用法: $0 info <label>"
        exit 1
    fi
    local label="$1"
    local plist="$HOME/Library/LaunchAgents/${label}.plist"

    if [[ ! -f "$plist" ]]; then
        log_error "找不到任务: $label"
        exit 1
    fi

    echo ""
    echo -e "${COLOR_CYAN}===== 任务详情: ${label} =====${COLOR_RESET}"
    echo ""

    # 显示完整 plist 信息
    /usr/libexec/PlistBuddy -c "Print" "$plist" 2>/dev/null || cat "$plist"

    echo ""
    echo "--- 运行日志 ---"
    local logfile="/tmp/${label}.log"
    local errfile="/tmp/${label}-error.log"
    if [[ -f "$logfile" ]] && [[ -s "$logfile" ]]; then
        echo "stdout (最后 20 行):"
        tail -20 "$logfile"
    else
        echo "(无 stdout 日志)"
    fi
    echo ""
    if [[ -f "$errfile" ]] && [[ -s "$errfile" ]]; then
        echo "stderr (最后 20 行):"
        tail -20 "$errfile"
    else
        echo "(无 stderr 日志)"
    fi
    echo ""
}

cmd_status() {
    if [[ $# -lt 1 ]]; then
        log_error "用法: $0 status <label>"
        exit 1
    fi
    local label="$1"
    local plist="$HOME/Library/LaunchAgents/${label}.plist"

    echo -e "${COLOR_CYAN}--- 状态: ${label} ---${COLOR_RESET}"

    # Plist 存在性
    if [[ -f "$plist" ]]; then
        log_info "Plist: ✓ 存在于 $(dirname "$plist")/"
    else
        log_error "Plist: ✗ 不存在"
        return 1
    fi

    # 是否已加载
    local output
    output=$(launchctl list "$label" 2>&1)
    if [[ $? -eq 0 ]]; then
        local pid exit_code rest
        read -r pid exit_code rest <<< "$output"
        if [[ "$pid" != "-" && -n "$pid" ]]; then
            log_info "状态: ✓ 运行中 (PID: $pid, ExitCode: $exit_code)"
        else
            log_info "状态: ○ 已加载，等待下次触发"
        fi
        log_info "上次运行: $rest"
    else
        log_warn "状态: ✗ 未加载 (可执行: launchctl load '$plist')"
    fi
}

# 输出提示（兼容 log_tip 函数调用）
log_tip() { echo -e "  ${COLOR_CYAN}$*${COLOR_RESET}"; }

# ============================================================
# 主入口
# ============================================================

main() {
    local command="${1:-help}"
    shift 2>/dev/null || true

    case "$command" in
        create|c)
            cmd_create "$@"
            ;;
        list|ls|l)
            cmd_list "$@"
            ;;
        start|run)
            cmd_start "$@"
            ;;
        stop)
            cmd_stop "$@"
            ;;
        restart|r)
            cmd_restart "$@"
            ;;
        remove|rm|delete)
            cmd_remove "$@"
            ;;
        info|i|detail)
            cmd_info "$@"
            ;;
        status|st)
            cmd_status "$@"
            ;;
        help|h|*)
            echo -e "${COLOR_CYAN}"
            echo "============================================================"
            echo "  macOS Launchctl Manager - 定时启停应用工具"
            echo "============================================================"
            echo "${COLOR_RESET}"
            echo "用法: $0 <command> [options]"
            echo ""
            echo -e "${COLOR_BLUE}命令:${COLOR_RESET}"
            echo "  create <app> <schedule>  创建定时启停任务"
            echo "  list                     列出所有定时任务"
            echo "  start <label>            触发启动任务"
            echo "  stop <label>             停止正在运行的任务"
            echo "  restart <label>          重启任务"
            echo "  remove <label>           删除任务"
            echo "  info <label>             查看任务详情和日志"
            echo "  status <label>           查看任务运行状态"
            echo ""
            echo -e "${COLOR_BLUE}安全参数:${COLOR_RESET}"
            echo "  --yes / -y               跳过确认，直接执行"
            echo "  --confirm                要求交互确认（默认行为）"
            echo "  --dry-run                仅预览，不实际执行"
            echo ""
            echo -e "${COLOR_BLUE}示例:${COLOR_RESET}"
            echo "  $0 create Safari '每天 9:00' --stop-at '每天 18:00' --dry-run"
            echo "  $0 create WeChat '工作日 9:00'"
            echo "  $0 create Slack '每2小时' --start-only"
            echo "  $0 list"
            echo "  $0 status com.user.launch.safari.start"
            echo "  $0 remove com.user.launch.safari --dry-run"
            echo "  $0 remove com.user.launch.safari --yes"
            echo ""
            echo -e "${COLOR_BLUE}时间格式:${COLOR_RESET}"
            echo "  '每天 9:00' / '每天 18:30'      每天固定时间"
            echo "  '每小时' / '每2小时'              按间隔重复"
            echo "  '每周一 9:00' / '工作日 8:30'     特定日期"
            echo "  '* 9 * * 1-5'                    标准 cron 表达式"
            ;;
    esac
}

main "$@"
