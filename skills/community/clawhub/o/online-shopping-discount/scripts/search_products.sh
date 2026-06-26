#!/bin/bash

# 商品查询脚本 - 根据关键词查询商品信息
# 用途：使用凭证查询优惠商品

set -e

# 配置
API_ENDPOINT="${SHOPPING_API_ENDPOINT:-https://online-shopping-discount.io.mlj130.com}"
TIMEOUT="${SHOPPING_API_TIMEOUT:-30}"

# 默认值
CREDENTIAL=""
KEYWORD=""
USER_ID=""
PLATFORM="${SHOPPING_DEFAULT_PLATFORM:-taobao}"
START_PRICE=""
END_PRICE=""

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

# 工具函数
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
  --credential CREDENTIAL    API 凭证
  --keyword KEYWORD          搜索关键词

可选参数:
  --platform PLATFORM        平台偏好（默认 taobao）
  --user_id USER_ID          指定 user_id（默认与 credential 相同）
  --start_price PRICE        最低成交价（仅在需要限制下限时传入）
  --end_price PRICE          最高成交价（仅在需要限制上限时传入）
  -h, --help                 显示此帮助信息

示例:
  $0 --credential "token_xxx" --keyword "无线耳机"
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
            --keyword)
                KEYWORD="$2"
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
            --start_price)
                START_PRICE="$2"
                shift 2
                ;;
            --end_price)
                END_PRICE="$2"
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
    
    if [ -z "$KEYWORD" ]; then
        error_exit "缺少必需参数: --keyword" "INVALID_PARAMS"
    fi
}

# 主函数
main() {
    parse_args "$@"
    ensure_dep curl
    ensure_dep jq
    
    log "开始查询商品: $KEYWORD"
    log "目标平台: $PLATFORM"
    
    local endpoint
    endpoint="$(normalized_endpoint "$API_ENDPOINT")/coupon/search"
    local user_value="${USER_ID:-$CREDENTIAL}"
    local curl_cmd=(curl -s -G --max-time "$TIMEOUT")
    curl_cmd+=(--data-urlencode "keyword=$KEYWORD")
    if [ -n "$PLATFORM" ]; then
        curl_cmd+=(--data-urlencode "platform=$PLATFORM")
    fi
    if [ -n "$user_value" ]; then
        curl_cmd+=(--data-urlencode "user_id=$user_value")
    fi
    if [ -n "$START_PRICE" ]; then
        curl_cmd+=(--data-urlencode "start_price=$START_PRICE")
    fi
    if [ -n "$END_PRICE" ]; then
        curl_cmd+=(--data-urlencode "end_price=$END_PRICE")
    fi
    curl_cmd+=("$endpoint")
    
    local response
    if ! response=$("${curl_cmd[@]}"); then
        error_exit "查询接口请求失败，请检查服务是否已在 $API_ENDPOINT 运行" "NETWORK_ERROR"
    fi

    if ! echo "$response" | jq . >/dev/null 2>&1; then
        error_exit "查询接口返回了无效的 JSON 数据" "API_ERROR"
    fi

    local result
    result=$(echo "$response" | jq -r '.result // empty')
    if [ "$result" != "success" ]; then
        local message
        message=$(echo "$response" | jq -r '.message // "查询失败"')
        error_exit "查询失败: $message" "API_ERROR"
    fi

    local payload
    payload=$(echo "$response" | jq --arg keyword "$KEYWORD" --arg user "$user_value" --arg platform "$PLATFORM" '
        def parse_discount_value($promo):
            (
                [
                    $promo.promotion_fee,
                    $promo.promotion_amount,
                    $promo.coupon_amount,
                    $promo.promotion_discount,
                    $promo.discount
                ]
                | map(select(. != null and . != ""))
                | map(try (if type == "number" then . else tonumber end) catch 0)
            ) as $values
            | (if ($values | length) > 0 then ($values | max) else 0 end);

        def pick_best_promo($list):
            if ($list | length) == 0 then null
            else
                ($list
                    | map(
                        . + {
                            __discount_value: parse_discount_value(.),
                            __end_value: (try (.promotion_end_time | tonumber) catch 0),
                            __start_value: (try (.promotion_start_time | tonumber) catch 0)
                        }
                    )
                    | sort_by(-.__discount_value, .__end_value)
                    | .[0]
                )
            end;

        def enrich_product:
            . as $product
            | (
                $product.final_promotion_list
                // $product.final_promotion
                // $product.promotions
                // $product.promotion_list
                // []
            ) as $promos
            | (pick_best_promo($promos)) as $best
            | if $best == null or ($best.promotion_id // "") == "" then
                $product
            else
                $product + {
                    best_promotion_id: $best.promotion_id,
                    best_promotion: ($best | del(.__discount_value, .__end_value, .__start_value))
                }
            end;

        {
            status: "success",
            keyword: $keyword,
            platform: $platform,
            total: (.data.total // (.data.products | length // 0)),
            products: ((.data.products // []) | map(enrich_product))
        } + (if $user != "" then {user_id: $user} else {} end)
    ')

    log "查询成功，返回 $(
        echo "$payload" | jq -r '.products | length'
    ) 条商品"
    echo "$payload"
}

# 执行主函数
main "$@"
