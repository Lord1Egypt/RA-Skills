#!/bin/bash
# Confluence REST API - curl 实现
# 用法: confluence.sh <命令> --url <url> --user <用户名> --pass <密码> [选项]

set -e

# ============================================================================
# 辅助函数
# ============================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[信息]${NC} $1"; }
log_error() { echo -e "${RED}[错误]${NC} $1"; }

# 检查依赖
check_deps() {
    if ! command -v curl &> /dev/null; then
        log_error "curl 未安装"
        exit 1
    fi
    if ! command -v jq &> /dev/null; then
        log_error "jq 未安装（JSON 解析需要）"
        exit 1
    fi
}

# Basic Auth 认证
make_auth() {
    echo "-u ${CONFLUENCE_USER}:${CONFLUENCE_PASS}"
}

# API GET 请求
api_get() {
    local endpoint="$1"
    local params="${2:-}"
    local url="${CONFLUENCE_URL%/}/rest/api/${endpoint}"
    if [ -n "$params" ]; then
        url="${url}?${params}"
    fi
    curl -s $(make_auth) "$url" -H "Accept: application/json"
}

# API POST 请求
api_post() {
    local endpoint="$1"
    local data="$2"
    local url="${CONFLUENCE_URL%/}/rest/api/${endpoint}"
    curl -s $(make_auth) -X POST "$url" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$data"
}

# API PUT 请求
api_put() {
    local endpoint="$1"
    local data="$2"
    local url="${CONFLUENCE_URL%/}/rest/api/${endpoint}"
    curl -s $(make_auth) -X PUT "$url" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$data"
}

# Markdown 转 Storage Format
markdown_to_storage() {
    local md="$1"
    local result="$md"

    # 标题
    result=$(echo "$result" | sed -E 's/^###### (.*)/<h6>\1<\/h6>/')
    result=$(echo "$result" | sed -E 's/^##### (.*)/<h5>\1<\/h5>/')
    result=$(echo "$result" | sed -E 's/^#### (.*)/<h4>\1<\/h4>/')
    result=$(echo "$result" | sed -E 's/^### (.*)/<h3>\1<\/h3>/')
    result=$(echo "$result" | sed -E 's/^## (.*)/<h2>\1<\/h2>/')
    result=$(echo "$result" | sed -E 's/^# (.*)/<h1>\1<\/h1>/')

    # 粗体
    result=$(echo "$result" | sed -E 's/\*\*([^*]+)\*\*/<strong>\1<\/strong>/g')
    result=$(echo "$result" | sed -E 's/__([^_]+)__/<strong>\1<\/strong>/g')

    # 斜体
    result=$(echo "$result" | sed -E 's/\*([^*]+)\*/<em>\1<\/em>/g')
    result=$(echo "$result" | sed -E 's/_([^_]+)_/<em>\1<\/em>/g')

    # 行内代码
    result=$(echo "$result" | sed -E 's/`([^`]+)`/<code>\1<\/code>/g')

    # 链接
    result=$(echo "$result" | sed -E 's/\[([^\]]+)\]\(([^)]+)\)/<a href="\2">\1<\/a>/g')

    # 段落（包装非标签行）
    result=$(echo "$result" | awk '
        /^<[h|ul|ol|li|p|pre|code|strong|em|a]/ { print; next }
        /^$/ { print ""; next }
        { print "<p>" $0 "</p>" }
    ')

    echo "$result"
}

# 格式化页面输出
format_page() {
    local json="$1"
    local include_body="${2:-true}"

    echo "$json" | jq -r '
        "### " + .title,
        "- **页面 ID:** " + (.id | tostring),
        "- **类型:** " + .type,
        "- **空间:** " + (.space.key // "未知"),
        "- **状态:** " + .status,
        "- **版本:** " + (.version.number | tostring)
    '

    if [ "$include_body" = "true" ]; then
        echo ""
        echo "---"
        echo ""
        # 提取正文内容
        echo "$json" | jq -r '.body.storage.value // .body.editor.value // "无内容"' | head -100
    fi
}

# 格式化搜索结果
format_search_results() {
    local json="$1"
    echo "$json" | jq -r '.results[] |
        "### " + .title,
        "- **页面 ID:** " + (.id | tostring),
        "- **类型:** " + .type,
        "- **空间:** " + (.space.key // "未知"),
        ""
    '
}

# ============================================================================
# 命令实现
# ============================================================================

# search 命令
cmd_search() {
    local cql="${1:-}"
    local max_results="${2:-50}"

    if [ -z "$cql" ]; then
        log_error "需要 CQL 查询语句"
        echo "示例: confluence.sh search 'text ~ \"kyuubi\"'"
        exit 1
    fi

    local params="cql=$(urlencode "$cql")&limit=$max_results"
    local response=$(api_get "content/search" "$params")

    if echo "$response" | jq -e '.results' > /dev/null 2>&1; then
        format_search_results "$response"
    else
        log_error "搜索失败"
        echo "$response" | jq .
        exit 1
    fi
}

# page get 命令
cmd_page_get() {
    local page_id="${1:-}"
    local expand="${2:-body.storage,version,space}"

    if [ -z "$page_id" ]; then
        log_error "需要页面 ID"
        exit 1
    fi

    local params="expand=$expand"
    local response=$(api_get "content/$page_id" "$params")

    if echo "$response" | jq -e '.id' > /dev/null 2>&1; then
        format_page "$response"
    else
        log_error "页面未找到: $page_id"
        echo "$response" | jq .
        exit 1
    fi
}

# page create 命令
cmd_page_create() {
    local space="${1:-}"
    local title="${2:-}"
    local body="${3:-}"
    local parent="${4:-}"

    if [ -z "$space" ] || [ -z "$title" ]; then
        log_error "需要空间 key 和标题"
        exit 1
    fi

    # Markdown 转换为 storage format
    local storage_body=$(markdown_to_storage "$body")

    # 构建 JSON 数据
    local data=$(cat <<EOF
{
    "type": "page",
    "title": "$title",
    "space": {"key": "$space"},
    "body": {
        "storage": {
            "value": "$storage_body",
            "representation": "storage"
        }
    }
}
EOF
)
    if [ -n "$parent" ]; then
        data=$(echo "$data" | jq --arg pid "$parent" '. + {"ancestors": [{"id": $pid}]}')
    fi

    local response=$(api_post "content" "$data")

    if echo "$response" | jq -e '.id' > /dev/null 2>&1; then
        log_info "页面已创建: $(echo "$response" | jq -r '.id')"
        echo "$response" | jq -r '"标题: " + .title, "URL: " + (._links.webui // "无")'
    else
        log_error "创建页面失败"
        echo "$response" | jq .
        exit 1
    fi
}

# page update 命令
cmd_page_update() {
    local page_id="${1:-}"
    local title="${2:-}"
    local body="${3:-}"
    local append="${4:-false}"

    if [ -z "$page_id" ]; then
        log_error "需要页面 ID"
        exit 1
    fi

    # 获取当前页面版本和内容
    local current=$(api_get "content/$page_id" "expand=version,body.storage")
    local version=$(echo "$current" | jq -r '.version.number')
    local current_title=$(echo "$current" | jq -r '.title')
    local current_body=$(echo "$current" | jq -r '.body.storage.value // ""')

    # 使用提供的标题或保持原标题
    if [ -z "$title" ]; then
        title="$current_title"
    fi

    # 处理正文
    local final_body=""
    if [ -n "$body" ]; then
        if [ "$append" = "true" ]; then
            # 追加模式：当前内容 + 新内容
            local new_content="$body"
            # 如果 body 不是 HTML 标签开头，当作 markdown 处理
            if ! echo "$body" | grep -q '^<'; then
                new_content=$(markdown_to_storage "$body")
            fi
            final_body="${current_body}${new_content}"
        else
            # 替换模式：仅新内容
            final_body=$(markdown_to_storage "$body")
        fi
    fi

    # 构建更新数据
    local data=$(cat <<EOF
{
    "version": {"number": $((version + 1))},
    "type": "page",
    "title": "$title"
}
EOF
)
    if [ -n "$final_body" ]; then
        # 转义 JSON 字符串
        local body_escaped=$(echo "$final_body" | jq -Rs .)
        data=$(echo "$data" | jq --argjson body "$body_escaped" '. + {"body": {"storage": {"value": $body, "representation": "storage"}}}')
    fi

    local response=$(api_put "content/$page_id" "$data")

    if echo "$response" | jq -e '.id' > /dev/null 2>&1; then
        log_info "页面已更新: $page_id"
        echo "$response" | jq -r '"版本: " + (.version.number | tostring)'
    else
        log_error "更新页面失败"
        echo "$response" | jq .
        exit 1
    fi
}

# page attach 命令 - 上传附件
cmd_page_attach() {
    local page_id="${1:-}"
    local file_path="${2:-}"
    local comment="${3:-}"

    if [ -z "$page_id" ]; then
        log_error "需要页面 ID"
        exit 1
    fi

    if [ -z "$file_path" ]; then
        log_error "需要文件路径"
        exit 1
    fi

    if [ ! -f "$file_path" ]; then
        log_error "文件不存在: $file_path"
        exit 1
    fi

    local filename=$(basename "$file_path")
    local url="${CONFLUENCE_URL%/}/rest/api/content/${page_id}/child/attachment"

    log_info "正在上传: $filename"

    # 使用 curl 上传文件
    local response=$(curl -s $(make_auth) -X POST "$url" \
        -H "X-Atlassian-Token: no-check" \
        -F "file=@${file_path}" \
        -F "comment=${comment}" \
        --output /tmp/attach_response.json -w "%{http_code}")

    if [ "$response" = "200" ] || [ "$response" = "201" ]; then
        local result=$(cat /tmp/attach_response.json)
        local attach_id=$(echo "$result" | jq -r '.results[0].id // .id // "未知"')
        local attach_title=$(echo "$result" | jq -r --arg fn "$filename" '.results[0].title // .title // $fn')
        log_info "附件上传成功"
        echo "  文件名: $attach_title"
        echo "  附件ID: $attach_id"
    else
        log_error "上传失败: HTTP $response"
        cat /tmp/attach_response.json | jq . 2>/dev/null || cat /tmp/attach_response.json
        exit 1
    fi
}

# space list 命令
cmd_space_list() {
    local max_results="${1:-50}"
    local params="limit=$max_results"

    local response=$(api_get "space" "$params")

    if echo "$response" | jq -e '.results' > /dev/null 2>&1; then
        echo "$response" | jq -r '.results[] | [.key, .name, .type] | @tsv' | column -t -s $'\t'
    else
        log_error "获取空间列表失败"
        echo "$response" | jq .
        exit 1
    fi
}

# space get 命令
cmd_space_get() {
    local space_key="${1:-}"

    if [ -z "$space_key" ]; then
        log_error "需要空间 Key"
        exit 1
    fi

    local response=$(api_get "space/$space_key")

    if echo "$response" | jq -e '.key' > /dev/null 2>&1; then
        echo "$response" | jq -r '
            "Key: " + .key,
            "名称: " + .name,
            "类型: " + .type,
            "描述: " + (.description.plain.value // "无")
        '
    else
        log_error "空间未找到: $space_key"
        exit 1
    fi
}

# check 命令
cmd_check() {
    log_info "检查 Confluence 配置..."

    if [ -z "$CONFLUENCE_URL" ]; then
        log_error "CONFLUENCE_URL 未设置"
        exit 1
    fi
    echo "  URL: $CONFLUENCE_URL"

    if [ -z "$CONFLUENCE_USER" ] || [ -z "$CONFLUENCE_PASS" ]; then
        log_error "CONFLUENCE_USER 和 CONFLUENCE_PASS 未设置"
        exit 1
    fi
    echo "  用户: $CONFLUENCE_USER"
    echo "  密码: ********"

    # 测试连接
    log_info "测试 API 访问..."
    local response=$(api_get "space" "limit=1")

    if echo "$response" | jq -e '.results' > /dev/null 2>&1; then
        log_info "API 访问正常"
        return 0
    else
        log_error "API 访问失败"
        echo "$response"
        exit 1
    fi
}

# URL 编码
urlencode() {
    local string="$1"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="$c" ;;
            * ) printf -v o '%%%02x' "'$c" ;;
        esac
        encoded+="$o"
    done
    echo "$encoded"
}

# ============================================================================
# 主程序
# ============================================================================

usage() {
    cat <<EOF
Confluence REST API (curl 实现)

用法:
  confluence.sh <命令> --url <url> --user <用户名> --pass <密码> [选项]

命令:
  check                                    验证配置和连接
  search <cql> [--max <数量>]              使用 CQL 搜索内容
  page get <页面ID>                        根据ID获取页面
  page create --space <空间> --title <标题> [--body <内容>] [--parent <父页面ID>]
                                           创建新页面
  page update <页面ID> [--title <标题>] [--body <内容>] [--append]
                                           更新已有页面
  page attach <页面ID> <文件路径> [--comment <备注>]
                                           上传附件到页面
  space list [--max <数量>]                列出所有空间
  space get <空间Key>                      获取空间详情

认证参数:
  --url    Confluence 基础 URL (如: https://confluence.example.com)
  --user   Basic Auth 用户名
  --pass   密码或 API Token

页面更新选项:
  --title  新标题（可选）
  --body   新内容（可选，支持 Markdown 或 HTML）
  --append 追加模式，将内容添加到页面末尾

附件上传选项:
  --comment  附件备注（可选）

示例:
  # 搜索页面
  confluence.sh search 'text ~ "kyuubi"' --url https://your-confluence.com --user admin --pass your-token

  # 获取页面
  confluence.sh page get 88666371 --url https://your-confluence.com --user admin --pass your-token

  # 创建页面
  confluence.sh page create --space DAT --title "测试页面" --body "# 标题\n正文" \
    --url https://your-confluence.com --user admin --pass your-token

  # 替换页面内容
  confluence.sh page update 97390801 --body "新内容" \
    --url https://your-confluence.com --user admin --pass your-token

  # 追加内容到页面末尾
  confluence.sh page update 97390801 --append --body "<p>新增段落</p>" \
    --url https://your-confluence.com --user admin --pass your-token

  # 追加 markdown 宏
  confluence.sh page update 97390801 --append \
    --body '<ac:structured-macro ac:name="markdown"><ac:plain-text-body><![CDATA[测试]]></ac:plain-text-body></ac:structured-macro>' \
    --url https://your-confluence.com --user admin --pass your-token

  # 上传附件
  confluence.sh page attach 97390801 /path/to/file.pdf --comment "测试文档" \
    --url https://your-confluence.com --user admin --pass your-token

环境变量 (可替代 --url/--user/--pass):
  CONFLUENCE_URL   基础 URL
  CONFLUENCE_USER  用户名
  CONFLUENCE_PASS  密码/Token
EOF
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --url)
                CONFLUENCE_URL="$2"
                shift 2
                ;;
            --user)
                CONFLUENCE_USER="$2"
                shift 2
                ;;
            --pass)
                CONFLUENCE_PASS="$2"
                shift 2
                ;;
            --max|--max-results)
                MAX_RESULTS="$2"
                shift 2
                ;;
            --space)
                SPACE="$2"
                shift 2
                ;;
            --title)
                TITLE="$2"
                shift 2
                ;;
            --body)
                BODY="$2"
                shift 2
                ;;
            --parent)
                PARENT="$2"
                shift 2
                ;;
            --append)
                APPEND="true"
                shift
                ;;
            --comment)
                COMMENT="$2"
                shift 2
                ;;
            --json)
                OUTPUT_JSON=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                # 位置参数
                if [ -z "$COMMAND" ]; then
                    COMMAND="$1"
                elif [ -z "$ARG1" ]; then
                    ARG1="$1"
                elif [ -z "$ARG2" ]; then
                    ARG2="$1"
                elif [ -z "$ARG3" ]; then
                    ARG3="$1"
                else
                    ARGS+=("$1")
                fi
                shift
                ;;
        esac
    done
}

# 主函数
main() {
    check_deps
    parse_args "$@"

    if [ -z "$COMMAND" ]; then
        usage
        exit 1
    fi

    case "$COMMAND" in
        check)
            cmd_check
            ;;
        search)
            cmd_search "$ARG1" "${MAX_RESULTS:-50}"
            ;;
        page)
            case "$ARG1" in
                get)
                    cmd_page_get "$ARG2"
                    ;;
                create)
                    cmd_page_create "$SPACE" "$TITLE" "$BODY" "$PARENT"
                    ;;
                update)
                    cmd_page_update "$ARG2" "$TITLE" "$BODY" "${APPEND:-false}"
                    ;;
                attach)
                    cmd_page_attach "$ARG2" "$ARG3" "${COMMENT:-}"
                    ;;
                *)
                    log_error "未知 page 子命令: $ARG1"
                    exit 1
                    ;;
            esac
            ;;
        space)
            case "$ARG1" in
                list)
                    cmd_space_list "${MAX_RESULTS:-50}"
                    ;;
                get)
                    cmd_space_get "$ARG2"
                    ;;
                *)
                    log_error "未知 space 子命令: $ARG1"
                    exit 1
                    ;;
            esac
            ;;
        *)
            log_error "未知命令: $COMMAND"
            usage
            exit 1
            ;;
    esac
}

main "$@"