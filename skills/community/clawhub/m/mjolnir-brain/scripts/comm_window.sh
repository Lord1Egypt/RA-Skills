#!/usr/bin/env bash
# ============================================================================
# comm_window.sh — 雷神之脑 v3.0 通信窗口管理器
# ============================================================================
# 管理节点间通信窗口的完整生命周期：申请→批准→执行→关闭→归档
#
# 用法:
#   comm_window.sh request <from> <to> <duration_min> <purpose>
#   comm_window.sh approve <window_id>
#   comm_window.sh reject <window_id> [reason]
#   comm_window.sh status [window_id]
#   comm_window.sh close <window_id> [reason]
#   comm_window.sh list [--active|--all]
#   comm_window.sh report [YYYY-MM]
#   comm_window.sh check-expired
#
# 数据存储:
#   活跃窗口: memory/node-comms/active-windows.json
#   通信日志: memory/node-comms/YYYY-MM-DD/
#   月度报表: memory/node-comms/reports/
# ============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

# 项目根目录 (相对于脚本位置)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 数据目录
COMMS_DIR="${PROJECT_ROOT}/memory/node-comms"
ACTIVE_WINDOWS="${COMMS_DIR}/active-windows.json"
REPORTS_DIR="${COMMS_DIR}/reports"

# 节点注册表
REGISTRY="${PROJECT_ROOT}/templates/memory/node-registry.json"

# 通信模板目录
TEMPLATES_DIR="${PROJECT_ROOT}/templates/node-comms"

# 默认配置 (从注册表读取，若不存在则使用默认值)
DEFAULT_WINDOW_MIN=30
MAX_WINDOW_MIN=60
MONTHLY_TOKEN_BUDGET=1000000

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

# 生成窗口ID
# 格式: win-YYYYMMDD-HHMMss-随机4位
generate_window_id() {
    local date_part
    date_part="$(date +%Y%m%d-%H%M%S)"
    local rand_part
    rand_part="$(head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n' | head -c 4)"
    echo "win-${date_part}-${rand_part}"
}

# 获取当前ISO-8601时间戳
now_iso() {
    date -Iseconds
}

# 获取今日日期 YYYY-MM-DD
today() {
    date +%Y-%m-%d
}

# 获取当前月份 YYYY-MM
this_month() {
    date +%Y-%m
}

# 确保目录存在
ensure_dirs() {
    mkdir -p "${COMMS_DIR}"
    mkdir -p "${COMMS_DIR}/$(today)"
    mkdir -p "${REPORTS_DIR}"
}

# 初始化 active-windows.json (如果不存在)
init_active_windows() {
    if [[ ! -f "${ACTIVE_WINDOWS}" ]]; then
        echo '{"windows": []}' > "${ACTIVE_WINDOWS}"
    fi
}

# 从注册表读取配置
load_settings() {
    if [[ -f "${REGISTRY}" ]]; then
        DEFAULT_WINDOW_MIN=$(jq -r '.settings.default_window_min // 30' "${REGISTRY}" 2>/dev/null || echo 30)
        MAX_WINDOW_MIN=$(jq -r '.settings.max_window_min // 60' "${REGISTRY}" 2>/dev/null || echo 60)
        MONTHLY_TOKEN_BUDGET=$(jq -r '.settings.monthly_token_budget // 1000000' "${REGISTRY}" 2>/dev/null || echo 1000000)
    fi
}

# 检查 jq 是否可用
check_deps() {
    if ! command -v jq &>/dev/null; then
        echo "❌ 错误: 需要 jq 工具。请安装: sudo apt install jq" >&2
        exit 1
    fi
}

# 彩色输出
info()  { echo -e "\033[36m[INFO]\033[0m $*"; }
ok()    { echo -e "\033[32m[OK]\033[0m $*"; }
warn()  { echo -e "\033[33m[WARN]\033[0m $*"; }
error() { echo -e "\033[31m[ERROR]\033[0m $*" >&2; }

# ---------------------------------------------------------------------------
# 核心功能
# ---------------------------------------------------------------------------

# request — 申请通信窗口
# 用法: request <from> <to> <duration_min> <purpose>
# 生成待审批窗口记录，并输出审批提示
cmd_request() {
    local from="${1:?用法: request <from> <to> <duration_min> <purpose>}"
    local to="${2:?缺少参数: to (目标节点ID)}"
    local duration="${3:?缺少参数: duration_min (窗口时长/分钟)}"
    local purpose="${4:?缺少参数: purpose (通信目的)}"

    # 校验时长
    if (( duration > MAX_WINDOW_MIN )); then
        error "请求时长 ${duration}分钟 超过上限 ${MAX_WINDOW_MIN}分钟"
        exit 1
    fi

    local window_id
    window_id="$(generate_window_id)"
    local now
    now="$(now_iso)"

    # 创建窗口记录
    local window_json
    window_json=$(jq -n \
        --arg wid "${window_id}" \
        --arg from "${from}" \
        --arg to "${to}" \
        --arg purpose "${purpose}" \
        --arg requested_at "${now}" \
        --argjson duration "${duration}" \
        --argjson token_budget 50000 \
        '{
            window_id: $wid,
            from: $from,
            to: $to,
            purpose: $purpose,
            status: "pending",
            requested_at: $requested_at,
            approved_at: null,
            started_at: null,
            expires_at: null,
            closed_at: null,
            duration_min: $duration,
            token_budget: $token_budget,
            tokens_used: 0,
            message_count: 0,
            close_reason: null
        }')

    # 写入活跃窗口列表
    local updated
    updated=$(jq --argjson win "${window_json}" '.windows += [$win]' "${ACTIVE_WINDOWS}")
    echo "${updated}" > "${ACTIVE_WINDOWS}"

    # 生成审批请求文件 (基于模板)
    local request_file="${COMMS_DIR}/$(today)/request-${window_id}.md"
    if [[ -f "${TEMPLATES_DIR}/window-request.md" ]]; then
        sed -e "s/{{WINDOW_ID}}/${window_id}/g" \
            -e "s/{{FROM}}/${from}/g" \
            -e "s/{{TO}}/${to}/g" \
            -e "s/{{DURATION}}/${duration}/g" \
            -e "s/{{PURPOSE}}/${purpose}/g" \
            -e "s/{{REQUESTED_AT}}/${now}/g" \
            "${TEMPLATES_DIR}/window-request.md" > "${request_file}"
    else
        # 无模板时直接生成
        cat > "${request_file}" <<EOF
# 📋 通信窗口申请

| 项目 | 内容 |
|------|------|
| **窗口ID** | ${window_id} |
| **发起节点** | ${from} |
| **目标节点** | ${to} |
| **申请时长** | ${duration} 分钟 |
| **通信目的** | ${purpose} |
| **申请时间** | ${now} |

## 审批

请回复:
- \`comm_window.sh approve ${window_id}\` — 批准
- \`comm_window.sh reject ${window_id} "原因"\` — 拒绝
EOF
    fi

    ok "通信窗口已申请"
    info "窗口ID: ${window_id}"
    info "从 ${from} → ${to}, 时长 ${duration} 分钟"
    info "目的: ${purpose}"
    info "审批文件: ${request_file}"
    info ""
    info "等待老板审批..."
    info "批准命令: $0 approve ${window_id}"

    echo "${window_id}"
}

# approve — 批准通信窗口
# 用法: approve <window_id>
# 将窗口状态从 pending 改为 active，开始计时
cmd_approve() {
    local window_id="${1:?用法: approve <window_id>}"
    local now
    now="$(now_iso)"

    # 检查窗口是否存在且为 pending 状态
    local status
    status=$(jq -r --arg wid "${window_id}" \
        '.windows[] | select(.window_id == $wid) | .status' \
        "${ACTIVE_WINDOWS}")

    if [[ -z "${status}" ]]; then
        error "窗口 ${window_id} 不存在"
        exit 1
    fi
    if [[ "${status}" != "pending" ]]; then
        error "窗口 ${window_id} 状态为 '${status}'，只有 'pending' 可以批准"
        exit 1
    fi

    # 计算到期时间
    local duration
    duration=$(jq -r --arg wid "${window_id}" \
        '.windows[] | select(.window_id == $wid) | .duration_min' \
        "${ACTIVE_WINDOWS}")
    local expires_at
    expires_at=$(date -Iseconds -d "+${duration} minutes")

    # 更新状态
    local updated
    updated=$(jq --arg wid "${window_id}" \
        --arg now "${now}" \
        --arg exp "${expires_at}" \
        '(.windows[] | select(.window_id == $wid)) |=
            (.status = "active" | .approved_at = $now | .started_at = $now | .expires_at = $exp)' \
        "${ACTIVE_WINDOWS}")
    echo "${updated}" > "${ACTIVE_WINDOWS}"

    ok "窗口 ${window_id} 已批准 ✅"
    info "开始时间: ${now}"
    info "到期时间: ${expires_at}"
    info "时长: ${duration} 分钟"
}

# reject — 拒绝通信窗口
# 用法: reject <window_id> [reason]
cmd_reject() {
    local window_id="${1:?用法: reject <window_id> [reason]}"
    local reason="${2:-无}"
    local now
    now="$(now_iso)"

    local updated
    updated=$(jq --arg wid "${window_id}" \
        --arg now "${now}" \
        --arg reason "${reason}" \
        '(.windows[] | select(.window_id == $wid)) |=
            (.status = "rejected" | .closed_at = $now | .close_reason = $reason)' \
        "${ACTIVE_WINDOWS}")
    echo "${updated}" > "${ACTIVE_WINDOWS}"

    ok "窗口 ${window_id} 已拒绝"
    info "原因: ${reason}"
}

# status — 查看窗口状态
# 用法: status [window_id]
# 无参数时显示所有活跃窗口
cmd_status() {
    local window_id="${1:-}"

    if [[ -z "${window_id}" ]]; then
        # 显示所有活跃窗口
        info "活跃通信窗口:"
        jq -r '.windows[] | select(.status == "active" or .status == "pending") |
            "  [\(.status)] \(.window_id) | \(.from)→\(.to) | \(.purpose) | 到期: \(.expires_at // "待批准")"' \
            "${ACTIVE_WINDOWS}" 2>/dev/null || echo "  (无)"
    else
        # 显示指定窗口详情
        jq --arg wid "${window_id}" \
            '.windows[] | select(.window_id == $wid)' \
            "${ACTIVE_WINDOWS}" 2>/dev/null || error "窗口 ${window_id} 不存在"
    fi
}

# close — 手动关闭窗口
# 用法: close <window_id> [reason]
cmd_close() {
    local window_id="${1:?用法: close <window_id> [reason]}"
    local reason="${2:-手动关闭}"
    local now
    now="$(now_iso)"

    # 获取窗口信息
    local win_data
    win_data=$(jq --arg wid "${window_id}" \
        '.windows[] | select(.window_id == $wid)' \
        "${ACTIVE_WINDOWS}" 2>/dev/null)

    if [[ -z "${win_data}" ]]; then
        error "窗口 ${window_id} 不存在"
        exit 1
    fi

    # 更新状态为 closed
    local updated
    updated=$(jq --arg wid "${window_id}" \
        --arg now "${now}" \
        --arg reason "${reason}" \
        '(.windows[] | select(.window_id == $wid)) |=
            (.status = "closed" | .closed_at = $now | .close_reason = $reason)' \
        "${ACTIVE_WINDOWS}")
    echo "${updated}" > "${ACTIVE_WINDOWS}"

    # 生成摘要
    _generate_summary "${window_id}"

    ok "窗口 ${window_id} 已关闭"
    info "原因: ${reason}"
}

# list — 列出所有窗口
# 用法: list [--active|--all]
cmd_list() {
    local filter="${1:---all}"

    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              雷神之脑 — 通信窗口列表                       ║"
    echo "╠════════════════════════════════════════════════════════════╣"

    case "${filter}" in
        --active)
            jq -r '.windows[] | select(.status == "active" or .status == "pending") |
                "║ [\(.status|ascii_upcase)] \(.window_id)\n║   \(.from) → \(.to) | \(.purpose)\n║   Token: \(.tokens_used)/\(.token_budget) | 消息: \(.message_count)\n╟────────────────────────────────────────────────────────────"' \
                "${ACTIVE_WINDOWS}" 2>/dev/null || echo "║ (无活跃窗口)"
            ;;
        --all|*)
            jq -r '.windows[] |
                "║ [\(.status|ascii_upcase)] \(.window_id)\n║   \(.from) → \(.to) | \(.purpose)\n║   Token: \(.tokens_used)/\(.token_budget) | 消息: \(.message_count)\n╟────────────────────────────────────────────────────────────"' \
                "${ACTIVE_WINDOWS}" 2>/dev/null || echo "║ (无窗口记录)"
            ;;
    esac

    echo "╚════════════════════════════════════════════════════════════╝"
}

# check-expired — 检查并关闭已到期的窗口
# 用法: check-expired (建议由 cron 定期调用)
cmd_check_expired() {
    local now_epoch
    now_epoch=$(date +%s)

    # 获取所有活跃窗口
    local active_windows
    active_windows=$(jq -r '.windows[] | select(.status == "active") | .window_id + " " + .expires_at' \
        "${ACTIVE_WINDOWS}" 2>/dev/null)

    if [[ -z "${active_windows}" ]]; then
        return 0
    fi

    while IFS=' ' read -r wid exp; do
        local exp_epoch
        exp_epoch=$(date -d "${exp}" +%s 2>/dev/null || echo 0)
        if (( now_epoch >= exp_epoch )); then
            warn "窗口 ${wid} 已到期，自动关闭"
            cmd_close "${wid}" "到期自动关闭"
        fi
    done <<< "${active_windows}"
}

# report — 月度通信报表
# 用法: report [YYYY-MM]
cmd_report() {
    local month="${1:-$(this_month)}"
    local report_file="${REPORTS_DIR}/${month}.md"

    ensure_dirs

    # 统计数据
    local total_windows
    total_windows=$(jq --arg m "${month}" \
        '[.windows[] | select(.requested_at | startswith($m))] | length' \
        "${ACTIVE_WINDOWS}" 2>/dev/null || echo 0)

    local total_tokens
    total_tokens=$(jq --arg m "${month}" \
        '[.windows[] | select(.requested_at | startswith($m))] | map(.tokens_used) | add // 0' \
        "${ACTIVE_WINDOWS}" 2>/dev/null || echo 0)

    local total_messages
    total_messages=$(jq --arg m "${month}" \
        '[.windows[] | select(.requested_at | startswith($m))] | map(.message_count) | add // 0' \
        "${ACTIVE_WINDOWS}" 2>/dev/null || echo 0)

    # 生成报表
    cat > "${report_file}" <<EOF
# 📊 月度通信报表 — ${month}

> 生成时间: $(now_iso)

## 概览

| 指标 | 数值 |
|------|------|
| 通信窗口总数 | ${total_windows} |
| 消息总数 | ${total_messages} |
| Token 总消耗 | ${total_tokens} |
| 月度预算 | ${MONTHLY_TOKEN_BUDGET} |
| 预算使用率 | $(( total_tokens * 100 / (MONTHLY_TOKEN_BUDGET > 0 ? MONTHLY_TOKEN_BUDGET : 1) ))% |

## 窗口明细

$(jq -r --arg m "${month}" '
    .windows[] | select(.requested_at | startswith($m)) |
    "| \(.window_id) | \(.from)→\(.to) | \(.status) | \(.tokens_used) | \(.message_count) | \(.purpose) |"' \
    "${ACTIVE_WINDOWS}" 2>/dev/null || echo "| (无记录) | | | | | |")

## 节点使用排行

$(jq -r --arg m "${month}" '
    [.windows[] | select(.requested_at | startswith($m))] |
    group_by(.from) | map({node: .[0].from, tokens: (map(.tokens_used) | add // 0), windows: length}) |
    sort_by(-.tokens) | .[] |
    "| \(.node) | \(.tokens) | \(.windows) |"' \
    "${ACTIVE_WINDOWS}" 2>/dev/null || echo "| (无记录) | | |")

---

*报表由 comm_window.sh 自动生成*
EOF

    ok "月度报表已生成: ${report_file}"
}

# ---------------------------------------------------------------------------
# 内部辅助函数
# ---------------------------------------------------------------------------

# 生成窗口通信摘要
_generate_summary() {
    local window_id="${1}"
    local summary_file="${COMMS_DIR}/$(today)/summary-${window_id}.md"

    # 获取窗口数据
    local win_data
    win_data=$(jq --arg wid "${window_id}" \
        '.windows[] | select(.window_id == $wid)' \
        "${ACTIVE_WINDOWS}" 2>/dev/null)

    local from to purpose tokens messages started closed
    from=$(echo "${win_data}" | jq -r '.from')
    to=$(echo "${win_data}" | jq -r '.to')
    purpose=$(echo "${win_data}" | jq -r '.purpose')
    tokens=$(echo "${win_data}" | jq -r '.tokens_used')
    messages=$(echo "${win_data}" | jq -r '.message_count')
    started=$(echo "${win_data}" | jq -r '.started_at // "N/A"')
    closed=$(echo "${win_data}" | jq -r '.closed_at // "N/A"')

    # 生成摘要文件
    if [[ -f "${TEMPLATES_DIR}/window-summary.md" ]]; then
        sed -e "s/{{WINDOW_ID}}/${window_id}/g" \
            -e "s/{{FROM}}/${from}/g" \
            -e "s/{{TO}}/${to}/g" \
            -e "s/{{PURPOSE}}/${purpose}/g" \
            -e "s/{{TOKENS_USED}}/${tokens}/g" \
            -e "s/{{MESSAGE_COUNT}}/${messages}/g" \
            -e "s/{{STARTED_AT}}/${started}/g" \
            -e "s/{{CLOSED_AT}}/${closed}/g" \
            "${TEMPLATES_DIR}/window-summary.md" > "${summary_file}"
    else
        cat > "${summary_file}" <<EOF
# 📝 通信窗口摘要 — ${window_id}

| 项目 | 内容 |
|------|------|
| **窗口ID** | ${window_id} |
| **通信方** | ${from} → ${to} |
| **目的** | ${purpose} |
| **开始** | ${started} |
| **结束** | ${closed} |
| **Token** | ${tokens} |
| **消息数** | ${messages} |

## 通信内容摘要

(由 comm_logger.sh summary 生成)
EOF
    fi

    info "摘要已生成: ${summary_file}"
}

# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

main() {
    check_deps
    ensure_dirs
    init_active_windows
    load_settings

    local cmd="${1:-help}"
    shift || true

    case "${cmd}" in
        request)        cmd_request "$@" ;;
        approve)        cmd_approve "$@" ;;
        reject)         cmd_reject "$@" ;;
        status)         cmd_status "$@" ;;
        close)          cmd_close "$@" ;;
        list)           cmd_list "$@" ;;
        check-expired)  cmd_check_expired ;;
        report)         cmd_report "$@" ;;
        help|--help|-h)
            echo "雷神之脑 v3.0 — 通信窗口管理器"
            echo ""
            echo "用法:"
            echo "  $0 request <from> <to> <duration_min> <purpose>  申请通信窗口"
            echo "  $0 approve <window_id>                           批准窗口"
            echo "  $0 reject <window_id> [reason]                   拒绝窗口"
            echo "  $0 status [window_id]                            查看窗口状态"
            echo "  $0 close <window_id> [reason]                    关闭窗口"
            echo "  $0 list [--active|--all]                         列出窗口"
            echo "  $0 check-expired                                 检查到期窗口"
            echo "  $0 report [YYYY-MM]                              月度报表"
            ;;
        *)
            error "未知命令: ${cmd}"
            echo "运行 '$0 help' 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"
