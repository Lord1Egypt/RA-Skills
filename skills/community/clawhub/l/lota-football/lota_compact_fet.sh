#!/bin/bash
# Lota Football 特征报告工具 (compact-fet)
# 用法: ./lota_compact_fet.sh <lota_id> [--plain]
# 跨平台兼容，仅依赖curl

set -e

BASE_URL="${LOTA_API_BASE_URL:-http://deepdata.lota.tv/predictions/api/v2}"
API_KEY="${LOTA_API_KEY}"
VERSION="1.0.0"

show_usage() {
    cat <<EOF
Lota Compact Fet CLI v${VERSION}

用法: $0 <lota_id> [选项]

选项:
  --plain     仅输出特征文本 (默认输出完整JSON)
  --help      显示帮助

环境变量:
  LOTA_API_KEY         API密钥
  LOTA_API_BASE_URL    API基础URL
EOF
}

# 发送请求获取特征报告
fetch_compact() {
    local lota_id="$1"
    local plain_mode="$2"

    local url="${BASE_URL}/compact-fet/?lota_id=${lota_id}"
    local curl_cmd=("curl" "-s" "--connect-timeout" "30" "--max-time" "60")

    if [[ -n "${API_KEY}" ]]; then
        curl_cmd+=("-H" "X-API-Key: ${API_KEY}")
    fi
    curl_cmd+=("${url}")

    if [[ "${plain_mode}" == "true" ]]; then
        # 提取 data.compact_fet 字段，若jq不可用则输出原始响应
        if command -v jq &>/dev/null; then
            "${curl_cmd[@]}" | jq -r '.data.compact_fet // empty'
        else
            "${curl_cmd[@]}"
        fi
    else
        # 完整JSON输出，若jq可用则格式化
        if command -v jq &>/dev/null; then
            "${curl_cmd[@]}" | jq .
        else
            "${curl_cmd[@]}"
        fi
    fi
}

main() {
    command -v curl &>/dev/null || { echo "错误: curl未安装"; exit 1; }

    local lota_id=""
    local plain_mode="false"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --plain)
                plain_mode="true"
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            --version|-v)
                echo "v${VERSION}"
                exit 0
                ;;
            -*)
                echo "未知选项: $1"
                show_usage
                exit 1
                ;;
            *)
                if [[ -z "$lota_id" ]]; then
                    lota_id="$1"
                else
                    echo "错误: 多余的参数 $1"
                    show_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$lota_id" ]]; then
        echo "错误: 缺少lota_id参数"
        show_usage
        exit 1
    fi

    fetch_compact "$lota_id" "$plain_mode"
}

main "$@"