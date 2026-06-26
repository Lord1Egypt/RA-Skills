#!/bin/bash
# Lota Football 比赛查询工具 (纯列表，无特征报告)
# 跨平台兼容，仅依赖curl，所有日期需显式传入 YYYY-MM-DD

set -e

VERSION="2.2.0"
BASE_URL="${LOTA_API_BASE_URL:-http://deepdata.lota.tv/predictions/api/v2}"
API_KEY="${LOTA_API_KEY}"
DEFAULT_OUTPUT="json"

show_usage() {
    cat <<EOF
Lota Football Matches CLI v${VERSION}

命令:
  today <date>             指定日期比赛 (例: today 2026-04-18)
  match <lota_id>          根据lota_id获取单场
  jingcai <date>           指定日期竞彩比赛 (例: jingcai 2026-04-18)
  beidan <date>            指定日期北单比赛
  range <start> <end>      日期范围查询 (YYYY-MM-DD)
  leagues <date>           指定日期联赛列表

选项:
  --pretty                 格式化JSON输出 (需jq)
  --raw                    原始JSON输出
  --output=<file>          保存到文件

环境变量:
  LOTA_API_KEY             API密钥
  LOTA_API_BASE_URL        API基础URL
EOF
}

send_request() {
    local endpoint="$1"
    shift
    local params=()
    while [[ $# -gt 0 ]]; do
        params+=("$1")
        shift
    done

    local url="${BASE_URL}/${endpoint}"
    if [[ ${#params[@]} -gt 0 ]]; then
        url="${url}?$(IFS='&'; echo "${params[*]}")"
    fi

    local curl_cmd=("curl" "-s" "--connect-timeout" "30" "--max-time" "60")
    [[ -n "${API_KEY}" ]] && curl_cmd+=("-H" "X-API-Key: ${API_KEY}")
    curl_cmd+=("${url}")

    if [[ "${DEFAULT_OUTPUT}" == "raw" ]]; then
        "${curl_cmd[@]}"
    elif command -v jq &>/dev/null && [[ "${DEFAULT_OUTPUT}" != "text" ]]; then
        "${curl_cmd[@]}" | jq .
    else
        "${curl_cmd[@]}"
    fi
}

# 命令实现 - 所有日期参数必须显式传入
cmd_today() {
    local date_param="$1"
    if [[ -z "$date_param" ]]; then
        echo "错误: 缺少日期参数，格式 YYYY-MM-DD" >&2
        exit 1
    fi
    send_request "matches/" "date=$date_param"
}

cmd_match() {
    local lota_id="$1"
    if [[ -z "$lota_id" ]]; then
        echo "错误: 缺少lota_id参数" >&2
        exit 1
    fi
    send_request "matches/" "lota_id=$lota_id"
}

cmd_jingcai() {
    local date_param="$1"
    if [[ -z "$date_param" ]]; then
        echo "错误: 缺少日期参数，格式 YYYY-MM-DD" >&2
        exit 1
    fi
    send_request "matches/" "date=$date_param" "is_jingcai=true"
}

cmd_beidan() {
    local date_param="$1"
    if [[ -z "$date_param" ]]; then
        echo "错误: 缺少日期参数，格式 YYYY-MM-DD" >&2
        exit 1
    fi
    send_request "matches/" "date=$date_param" "is_beidan=true"
}

cmd_range() {
    local start_date="$1"
    local end_date="$2"
    if [[ -z "$start_date" ]] || [[ -z "$end_date" ]]; then
        echo "错误: 需要开始和结束日期 (YYYY-MM-DD)" >&2
        exit 1
    fi
    send_request "matches/" "start_date=$start_date" "end_date=$end_date"
}

cmd_leagues() {
    local date_param="$1"
    if [[ -z "$date_param" ]]; then
        echo "错误: 缺少日期参数，格式 YYYY-MM-DD" >&2
        exit 1
    fi
    if command -v jq &>/dev/null; then
        send_request "matches/" "date=$date_param" | jq '[.data.matches[] | .league_name] | unique'
    else
        send_request "matches/" "date=$date_param"
    fi
}

main() {
    command -v curl &>/dev/null || { echo "错误: curl未安装"; exit 1; }

    local output_file=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --raw) DEFAULT_OUTPUT="raw"; shift ;;
            --pretty) DEFAULT_OUTPUT="json"; shift ;;
            --output=*) output_file="${1#*=}"; shift ;;
            --help|-h) show_usage; exit 0 ;;
            --version|-v) echo "v${VERSION}"; exit 0 ;;
            *) break ;;
        esac
    done

    if [[ -n "$output_file" ]]; then
        exec > "$output_file"
    fi

    case "$1" in
        today) shift; cmd_today "$1" ;;
        match) shift; cmd_match "$1" ;;
        jingcai) shift; cmd_jingcai "$1" ;;
        beidan) shift; cmd_beidan "$1" ;;
        range) shift; cmd_range "$1" "$2" ;;
        leagues) shift; cmd_leagues "$1" ;;
        help|--help|-h) show_usage ;;
        version|--version|-v) echo "v${VERSION}" ;;
        "") show_usage ;;
        *) echo "未知命令: $1"; show_usage; exit 1 ;;
    esac
}

main "$@"