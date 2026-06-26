#!/bin/bash

# 链接生成脚本 - 为商品生成优惠推广链接
# 用途：调用实际的 /coupon/getLink 接口返回优惠链接或口令

set -e

# 配置
API_ENDPOINT="${SHOPPING_API_ENDPOINT:-https://online-shopping-discount.io.mlj130.com}"
TIMEOUT="${SHOPPING_API_TIMEOUT:-30}"

# 参数
CREDENTIAL=""
PRODUCT_ID=""
LINK_TYPE="url"
PROMOTION_ID=""
USER_ID=""
PLATFORM="${SHOPPING_DEFAULT_PLATFORM:-taobao}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 错误处理函数
error_exit() {
    echo -e "${RED}错误: $1${NC}" >&2
    echo "{\"status\":\"error\",\"error_code\":\"$2\",\"message\":\"$1\"}"
    exit 1
}

# 日志函数
log() {
    echo -e "${GREEN}[INFO]${NC} $1" >&2
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
}

ensure_dep() {
    if ! command -v "$1" >/dev/null 2>&1; then
        error_exit "缺少依赖: $1，请先安装后再试" "MISSING_DEP"
    fi
}

normalized_endpoint() {
    local endpoint="$1"
    endpoint="${endpoint%%/}"
    echo "$endpoint"
}

# 显示使用说明
usage() {
    cat >&2 <<EOF
使用方法: $0 [选项]

必需参数:
  --credential CREDENTIAL    API 凭证（注册接口返回的 uuid）
  --product_id PRODUCT_ID    商品ID

可选参数:
  --link_type TYPE           链接类型 (url|code|both)，默认 both
  --promotion_id ID          优惠活动ID（推荐使用）
  --activity_id ID           兼容旧参数，等价于 --promotion_id
  --platform PLATFORM        平台（默认 taobao）
  --user_id USER_ID          自定义 user_id（默认与 credential 相同）
  -h, --help                 显示此帮助信息

示例:
  $0 --credential "uuid_xxx" --product_id "12345678" --link_type "both"
EOF
    exit 1
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --credential)
                CREDENTIAL="$2"
                shift 2
                ;;
            --product_id)
                PRODUCT_ID="$2"
                shift 2
                ;;
            --link_type)
                LINK_TYPE="$2"
                shift 2
                ;;
            --promotion_id)
                PROMOTION_ID="$2"
                shift 2
                ;;
            --activity_id)
                PROMOTION_ID="$2"
                warn "--activity_id 参数已废弃，请改用 --promotion_id"
                shift 2
                ;;
            --user_id)
                USER_ID="$2"
                shift 2
                ;;
            --platform)
                PLATFORM="$2"
                shift 2
                ;;
            -h|--help)
                usage
                ;;
            *)
                error_exit "未知参数: $1" "INVALID_PARAMS"
                ;;
        esac
    done
    
    # 验证必需参数
    if [ -z "$CREDENTIAL" ]; then
        error_exit "缺少必需参数: --credential" "INVALID_PARAMS"
    fi
    
    if [ -z "$PRODUCT_ID" ]; then
        error_exit "缺少必需参数: --product_id" "INVALID_PARAMS"
    fi
    
    if [ -z "$LINK_TYPE" ]; then
        LINK_TYPE="both"
    fi
    
    case $LINK_TYPE in
        url|code|both)
            ;;
        *)
            error_exit "链接类型无效: $LINK_TYPE (必须是 url、code 或 both)" "INVALID_PARAMS"
            ;;
    esac
}

# 主函数
main() {
    parse_args "$@"
    ensure_dep curl
    ensure_dep jq
    
    log "开始生成推广链接..."
    log "商品ID: $PRODUCT_ID"
    log "链接类型: $LINK_TYPE"
    log "平台: $PLATFORM"
    
    local endpoint
    endpoint="$(normalized_endpoint "$API_ENDPOINT")/coupon/getLink"
    local user_value="${USER_ID:-$CREDENTIAL}"
    
    local curl_cmd=(curl -s -X POST --max-time "$TIMEOUT" -H "Content-Type: application/x-www-form-urlencoded")
    curl_cmd+=(--data-urlencode "product_id=$PRODUCT_ID")
    curl_cmd+=(--data-urlencode "link_type=$LINK_TYPE")
    if [ -n "$PLATFORM" ]; then
        curl_cmd+=(--data-urlencode "platform=$PLATFORM")
    fi
    if [ -n "$PROMOTION_ID" ]; then
        log "使用优惠活动ID: $PROMOTION_ID"
        curl_cmd+=(--data-urlencode "promotion_id=$PROMOTION_ID")
        curl_cmd+=(--data-urlencode "activity_id=$PROMOTION_ID")
    fi
    if [ -n "$user_value" ]; then
        curl_cmd+=(--data-urlencode "user_id=$user_value")
    fi
    curl_cmd+=("$endpoint")

    local response
    if ! response=$("${curl_cmd[@]}"); then
        error_exit "链接生成接口请求失败，请检查服务是否已在 $API_ENDPOINT 运行" "NETWORK_ERROR"
    fi

    if ! echo "$response" | jq . >/dev/null 2>&1; then
        error_exit "链接生成接口返回了无效的 JSON 数据" "API_ERROR"
    fi

    local result
    result=$(echo "$response" | jq -r '.result // empty')
    if [ "$result" != "success" ]; then
        local message
        message=$(echo "$response" | jq -r '.message // "生成链接失败"')
        error_exit "生成链接失败: $message" "API_ERROR"
    fi

    local payload
    payload=$(echo "$response" | jq --arg pid "$PRODUCT_ID" --arg lt "$LINK_TYPE" --arg user "$user_value" --arg platform "$PLATFORM" '
        {
            status: "success",
            product_id: $pid,
            link_type: (.data.link_type // $lt),
            platform: (.data.platform // $platform),
            url: (.data.url // ""),
            code: (.data.code // ""),
            expire_time: (.data.expire_time // "")
        } + (if $user != "" then {user_id: $user} else {} end)
    ')

    log "链接生成成功"
    echo "$payload"
}

# 执行主函数
main "$@"
