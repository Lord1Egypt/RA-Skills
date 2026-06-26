#!/bin/bash
#############################################################################
# GLM 编码套餐使用统计查询脚本
# 从 GLM 编码套餐监控端点查询使用统计信息
#
# GLM Coding Plan Usage Statistics Query Script
# Query usage statistics from GLM coding plan monitoring endpoints
#############################################################################

set -uo pipefail

# 颜色定义 / Color definitions
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color
readonly BOLD='\033[1m'

# 配置路径 / Configuration paths
readonly OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
readonly API_BASE="https://open.bigmodel.cn"

# 全局变量 / Global variables
PROVIDER=""
API_KEY=""
LANG_CODE=""

#############################################################################
# 国际化函数 / Internationalization functions
#############################################################################

# 语言检测 / Language detection
get_language() {
    if [[ -n "${OPENCLAW_LANGUAGE:-}" ]]; then
        echo "$OPENCLAW_LANGUAGE"
    elif [[ "${LANG:-}" == zh* ]]; then
        echo "zh"
    else
        echo "en"
    fi
}

LANG_CODE=$(get_language)

# 翻译字典 / Translation dictionary
get_text() {
    local key="$1"
    local lang="${LANG_CODE:-zh}"

    case "$key:$lang" in
        "error_curl:zh") echo "缺少依赖工具，请安装: curl" ;;
        "error_curl:en") echo "Missing dependency, please install: curl" ;;
        "error_jq:zh") echo "缺少依赖工具，请安装: jq" ;;
        "error_jq:en") echo "Missing dependency, please install: jq" ;;
        "error_config:zh") echo "未找到 OpenClaw 配置文件 ~/.openclaw/openclaw.json" ;;
        "error_config:en") echo "OpenClaw config file not found: ~/.openclaw/openclaw.json" ;;
        "error_no_provider:zh") echo "未找到配置的提供商" ;;
        "error_no_provider:en") echo "No configured provider found" ;;
        "error_no_apikey:zh") echo "未找到提供商的 API 密钥" ;;
        "error_no_apikey:en") echo "API key not found for provider" ;;
        "error_not_coding:zh") echo "未找到配置 GLM 编码套餐的提供商" ;;
        "error_not_coding:en") echo "No GLM coding plan provider configured" ;;
        "error_timeout:zh") echo "API 请求超时" ;;
        "error_timeout:en") echo "API request timeout" ;;
        "error_auth:zh") echo "认证失败，请检查 API 密钥配置" ;;
        "error_auth:en") echo "Authentication failed, please check API key" ;;
        "warn_quota:zh") echo "无法获取配额限制" ;;
        "warn_quota:en") echo "Unable to get quota limits" ;;
        "warn_model:zh") echo "无法获取模型使用统计" ;;
        "warn_model:en") echo "Unable to get model usage statistics" ;;
        "warn_tool:zh") echo "无法获取工具使用统计" ;;
        "warn_tool:en") echo "Unable to get tool usage statistics" ;;
        "header_title:zh") echo "📊 GLM 编码套餐使用统计" ;;
        "header_title:en") echo "📊 GLM Coding Plan Usage Statistics" ;;
        "label_provider:zh") echo "提供商" ;;
        "label_provider:en") echo "Provider" ;;
        "label_time:zh") echo "统计时间" ;;
        "label_time:en") echo "Statistics Time" ;;
        "section_quota:zh") echo "配额限制" ;;
        "section_quota:en") echo "Quota Limits" ;;
        "section_model:zh") echo "模型使用 (24小时)" ;;
        "section_model:en") echo "Model Usage (24 hours)" ;;
        "section_tool:zh") echo "工具使用 (24小时)" ;;
        "section_tool:en") echo "Tool Usage (24 hours)" ;;
        "token_5h:zh") echo "Token 使用 (5小时)" ;;
        "token_5h:en") echo "Token Usage (5-hour)" ;;
        "mcp_1m:zh") echo "MCP 使用 (1个月)" ;;
        "mcp_1m:en") echo "MCP Usage (1-month)" ;;
        "total_tokens:zh") echo "总 Token 数" ;;
        "total_tokens:en") echo "Total Tokens" ;;
        "total_calls:zh") echo "总调用次数" ;;
        "total_calls:en") echo "Total Calls" ;;
        "no_data:zh") echo "暂无数据" ;;
        "no_data:en") echo "No data available" ;;
        "times_unit:zh") echo "次" ;;
        "times_unit:en") echo "times" ;;
        "sec_unit:zh") echo "秒" ;;
        "sec_unit:en") echo "sec" ;;
        "ensure_url:zh") echo "请确保 provider 的 baseUrl 包含 'api/coding/paas/v4'" ;;
        "ensure_url:en") echo "Please ensure provider's baseUrl contains 'api/coding/paas/v4'" ;;
        "sample_config:zh") echo "示例配置:" ;;
        "sample_config:en") echo "Sample configuration:" ;;
        "error_prefix:zh") echo "错误:" ;;
        "error_prefix:en") echo "Error:" ;;
        *) echo "$key" ;;
    esac
}

#############################################################################
# 辅助函数 / Helper functions
#############################################################################

print_error() {
    local key="$1"
    echo -e "${RED}❌ $(get_text 'error_prefix')${NC} $(get_text "$key")" >&2
}

print_success() {
    echo -e "${GREEN}✓${NC} $*"
}

print_warning() {
    local key="$1"
    echo -e "${YELLOW}⚠${NC} $(get_text "$key")"
}

print_info() {
    echo -e "${CYAN}ℹ${NC} $*"
}

# 检查依赖工具 / Check dependencies
check_dependencies() {
    if ! command -v curl &> /dev/null; then
        print_error "error_curl"
        exit 1
    fi

    if ! command -v jq &> /dev/null; then
        print_error "error_jq"
        exit 1
    fi
}

# 查找 GLM 编码套餐提供商 / Find GLM coding plan provider
find_coding_plan_provider() {
    local config="$1"

    # 检查配置文件是否存在 / Check if config file exists
    if [[ ! -f "$config" ]]; then
        print_error "error_config"
        exit 1
    fi

    # 获取所有提供商名称 / Get all provider names
    local providers
    providers=$(jq -r '.models.providers // {} | keys[]' "$config" 2>/dev/null || true)

    if [[ -z "$providers" ]]; then
        print_error "error_no_provider"
        exit 1
    fi

    # 查找第一个使用编码端点的提供商 / Find first provider using coding endpoint
    for provider in $providers; do
        local base_url
        base_url=$(jq -r ".models.providers.\"$provider\".baseUrl // empty" "$config" 2>/dev/null)

        if [[ "$base_url" == *"api/coding/paas/v4"* ]]; then
            local api_key
            api_key=$(jq -r ".models.providers.\"$provider\".apiKey // empty" "$config" 2>/dev/null)

            if [[ -z "$api_key" ]]; then
                print_error "error_no_apikey"
                exit 1
            fi

            PROVIDER="$provider"
            API_KEY="$api_key"
            return 0
        fi
    done

    # 未找到编码套餐提供商 / No coding plan provider found
    print_error "error_not_coding"
    echo ""
    echo "$(get_text 'ensure_url')"
    echo "$(get_text 'sample_config')"
    echo '  "models": {'
    echo '    "providers": {'
    echo '      "glm-coding": {'
    echo '        "baseUrl": "https://open.bigmodel.cn/api/coding/paas/v4",'
    echo '        "apiKey": "your-api-key"'
    echo '      }'
    echo '    }'
    echo '  }'
    exit 1
}

# 查询 API 端点 / Query API endpoint
query_api() {
    local endpoint="$1"
    local url="${API_BASE}${endpoint}"

    local response
    response=$(curl -sS \
        --connect-timeout 10 \
        --max-time 30 \
        -H "Authorization: $API_KEY" \
        -H "Content-Type: application/json" \
        "$url" 2>&1)

    local curl_exit=$?
    if [[ $curl_exit -ne 0 ]]; then
        print_error "error_timeout"
        exit 1
    fi

    # 检查 HTTP 错误 / Check HTTP errors
    local http_code
    http_code=$(echo "$response" | jq -r 'select(.code? // .error? // .status? != null) | .code // .error // .status // "200"' 2>/dev/null)

    if [[ "$http_code" =~ ^(401|403)$ ]]; then
        print_error "error_auth"
        exit 1
    fi

    echo "$response"
}

# 绘制进度条 / Draw progress bar
draw_progress_bar() {
    local percentage="$1"
    local width=30
    local filled=$(( width * percentage / 100 ))
    local empty=$(( width - filled ))

    echo -n "["
    printf '%0.s#' $(seq 1 $filled 2>/dev/null || echo "")
    printf '%0.s-' $(seq 1 $empty 2>/dev/null || echo "")
    echo -n "] "
    printf "%5.1f%%" "$percentage"
}

#############################################################################
# 输出格式化函数 / Output formatting functions
#############################################################################

# 打印头部框 / Print header box
print_header() {
    local title="$1"
    local title_len=${#title}
    local box_width=64

    echo ""
    echo "╔$(printf '═%.0s' $(seq 1 $box_width 2>/dev/null || echo "") 2>/dev/null || echo "══════════════════════════════════════════════════════════════")╗"
    # 居中标题 / Center title
    local padding=$(( (box_width - title_len - 2) / 2 ))
    printf "║%$((padding + 1))s%s%$((box_width - padding - title_len - 2))s║\n" "" "$title" ""
    echo "╠$(printf '═%.0s' $(seq 1 $box_width 2>/dev/null || echo "") 2>/dev/null || echo "══════════════════════════════════════════════════════════════")╣"
}

# 打印底部 / Print footer
print_footer() {
    local box_width=64
    echo "╚$(printf '═%.0s' $(seq 1 $box_width 2>/dev/null || echo "") 2>/dev/null || echo "══════════════════════════════════════════════════════════════")╝"
    echo ""
}

# 打印信息行 / Print info row
print_info_row() {
    local key="$1"
    local value="$2"
    local box_width=64
    local key_width=12

    printf "║  ${BOLD}%-${key_width}s${NC} %s%$((box_width - key_width - ${#value} - 6))s║\n" "$key" "$value" ""
}

# 打印分节标题 / Print section header
print_section_header() {
    local text="$1"
    local box_width=64

    echo "╠$(printf '═%.0s' $(seq 1 $box_width 2>/dev/null || echo "") 2>/dev/null || echo "══════════════════════════════════════════════════════════════")╣"
    printf "║  ${BOLD}%s${NC}%$((box_width - ${#text} - 4))s║\n" "$text" ""
    echo "╟$(printf '─%.0s' $(seq 1 $box_width 2>/dev/null || echo "") 2>/dev/null || echo "──────────────────────────────────────────────────────────────────────────────────")╢"
}

# 打印进度条行 / Print progress bar row
print_progress_row() {
    local label="$1"
    local percentage="$2"
    local box_width=64

    printf "║  %-26s  " "$label"
    draw_progress_bar "$percentage"
    printf "%13s║\n" ""
}

# 打印统计行 / Print stat row
print_stat_row() {
    local label="$1"
    local value="$2"
    local box_width=64

    printf "║  %-26s  %s%$((box_width - ${#label} - ${#value} - 8))s║\n" "$label" "$value" ""
}

#############################################################################
# 主查询函数 / Main query functions
#############################################################################

query_quota_limits() {
    local response
    response=$(query_api "/api/monitor/usage/quota/limit")

    local success
    success=$(echo "$response" | jq -r '.success // false' 2>/dev/null)

    if [[ "$success" != "true" ]]; then
        print_warning "warn_quota"
        return 1
    fi

    echo "$response"
}

query_model_usage() {
    local response
    response=$(query_api "/api/monitor/usage/model-usage")

    local success
    success=$(echo "$response" | jq -r '.success // false' 2>/dev/null)

    if [[ "$success" != "true" ]]; then
        print_warning "warn_model"
        return 1
    fi

    echo "$response"
}

query_tool_usage() {
    local response
    response=$(query_api "/api/monitor/usage/tool-usage")

    local success
    success=$(echo "$response" | jq -r '.success // false' 2>/dev/null)

    if [[ "$success" != "true" ]]; then
        print_warning "warn_tool"
        return 1
    fi

    echo "$response"
}

#############################################################################
# 显示结果 / Display results
#############################################################################

display_results() {
    local quota_response="$1"
    local model_response="$2"
    local tool_response="$3"

    # 计算时间周期 / Calculate time period
    local end_time
    local start_time
    end_time=$(date '+%Y-%m-%d %H:%M:%S')
    start_time=$(date -d '5 hours ago' '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -v-5H '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "$end_time")

    # 打印头部 / Print header
    echo ""
    echo -e "${BOLD}$(get_text 'header_title')${NC}"
    echo ""
    echo "$(get_text 'label_provider'): $PROVIDER"
    echo "$(get_text 'label_time'): $end_time"
    echo ""

    # 配额限制部分 / Quota limits section
    if [[ -n "$quota_response" ]]; then
        echo -e "${BOLD}$(get_text 'section_quota')${NC}"
        echo "---"

        local token_5h
        local mcp_1m
        local mcp_current
        local mcp_total
        local mcp_level

        token_5h=$(echo "$quota_response" | jq -r '.data.limits[]? | select(.type == "TOKENS_LIMIT") | .percentage // 0' 2>/dev/null || echo "0")
        mcp_1m=$(echo "$quota_response" | jq -r '.data.limits[]? | select(.type == "TIME_LIMIT") | .percentage // 0' 2>/dev/null || echo "0")
        mcp_current=$(echo "$quota_response" | jq -r '.data.limits[]? | select(.type == "TIME_LIMIT") | .currentValue // 0' 2>/dev/null || echo "0")
        mcp_total=$(echo "$quota_response" | jq -r '.data.limits[]? | select(.type == "TIME_LIMIT") | .usage // 0' 2>/dev/null || echo "0")
        mcp_level=$(echo "$quota_response" | jq -r '.data.level // "unknown"' 2>/dev/null || echo "unknown")

        echo "  $(get_text 'token_5h'): ${token_5h}%"
        echo "  $(get_text 'mcp_1m'):   ${mcp_1m}%  (${mcp_current}/${mcp_total} $(get_text 'times_unit')) [${mcp_level}]"
        echo ""
    fi

    # 模型使用部分 / Model usage section
    if [[ -n "$model_response" ]]; then
        echo -e "${BOLD}$(get_text 'section_model')${NC}"
        echo "---"

        local total_tokens
        local total_calls

        total_tokens=$(echo "$model_response" | jq -r '.data.totalTokens // 0' 2>/dev/null || echo "0")
        total_calls=$(echo "$model_response" | jq -r '.data.totalCalls // 0' 2>/dev/null || echo "0")

        # 格式化数字 / Format numbers
        formatted_tokens=$(echo "$total_tokens" | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta')
        formatted_calls=$(echo "$total_calls" | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta')

        echo "  $(get_text 'total_tokens'):  $formatted_tokens"
        echo "  $(get_text 'total_calls'):  $formatted_calls"
        echo ""
    fi

    # 工具使用部分 - 简化显示 / Tool usage section - simplified display
    if [[ -n "$tool_response" ]]; then
        echo -e "${BOLD}$(get_text 'section_tool')${NC}"
        echo "---"

        local tools
        tools=$(echo "$tool_response" | jq -r '.data.tools[]? // empty' 2>/dev/null)

        if [[ -n "$tools" ]]; then
            echo "$tools" | jq -r '"  \(.toolName // .name // "unknown"): \(.usageCount // 0) $(get_text 'times_unit')"' 2>/dev/null
        else
            echo "  $(get_text 'no_data')"
        fi
        echo ""
    fi
}

#############################################################################
# 主入口 / Main entry
#############################################################################

main() {
    # 检查依赖 / Check dependencies
    check_dependencies

    # 查找编码套餐提供商 / Find coding plan provider
    find_coding_plan_provider "$OPENCLAW_CONFIG"

    # 查询所有端点 / Query all endpoints
    local quota_response=""
    local model_response=""
    local tool_response=""

    quota_response=$(query_quota_limits)
    model_response=$(query_model_usage)
    tool_response=$(query_tool_usage)

    # 显示结果 / Display results
    display_results "$quota_response" "$model_response" "$tool_response"
}

# 运行主函数 / Run main function
main "$@"
