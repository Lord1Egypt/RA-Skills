#!/bin/bash
set -e

# IndexNow URL 提交工具
# 通过 IndexNow 协议向搜索引擎提交 URL，加速收录

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC} $1"; }

INDEXNOW_API="https://api.indexnow.org/indexnow"
KEY_FILE=".indexnow-key"

# ---- generate-key ----
cmd_generate_key() {
    if [ -f "$KEY_FILE" ]; then
        local existing_key
        existing_key=$(cat "$KEY_FILE" | tr -d '[:space:]')
        log_warn "Key 已存在: $existing_key"
        echo -n "是否重新生成? (y/N) "
        read -r reply
        case "$reply" in
            [Yy]*) ;;
            *) log_info "保留现有 key"; return 0 ;;
        esac
    fi

    # 生成 32 位十六进制 key
    local key
    key=$(openssl rand -hex 16)

    echo "$key" > "$KEY_FILE"
    log_info "API Key 已生成: $key"
    log_info "Key 已保存到: $KEY_FILE"

    # 创建验证文件
    local public_dir="public"
    if [ ! -d "$public_dir" ]; then
        log_warn "未找到 public/ 目录，在当前目录创建验证文件"
        public_dir="."
    fi

    echo "$key" > "${public_dir}/${key}.txt"
    log_info "验证文件已创建: ${public_dir}/${key}.txt"
    echo ""
    log_info "下一步:"
    log_info "  1. 部署项目，使验证文件可在线访问"
    log_info "  2. 确认可访问: https://你的域名/${key}.txt"
    log_info "  3. 然后即可提交 URL"
}

# ---- 加载 key ----
load_key() {
    if [ ! -f "$KEY_FILE" ]; then
        log_error "API Key 不存在，请先运行: $0 generate-key"
        exit 1
    fi
    API_KEY=$(cat "$KEY_FILE" | tr -d '[:space:]')
    if [ -z "$API_KEY" ]; then
        log_error "Key 文件为空"
        exit 1
    fi
}

# ---- 从 URL 提取 host ----
extract_host() {
    echo "$1" | sed -E 's|https?://([^/]+).*|\1|'
}

# ---- URL 编码 ----
url_encode() {
    python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"
}

# ---- 解析响应码 ----
format_response() {
    local code=$1
    local url=$2
    case $code in
        200) echo -e "  ${GREEN}200 OK${NC}        $url" ;;
        202) echo -e "  ${YELLOW}202 Accepted${NC}  $url (key 待验证)" ;;
        400) echo -e "  ${RED}400 Bad${NC}       $url (格式错误)" ;;
        403) echo -e "  ${RED}403 Forbidden${NC} $url (key 无效)" ;;
        422) echo -e "  ${RED}422 Invalid${NC}   $url (URL 不匹配)" ;;
        429) echo -e "  ${RED}429 TooMany${NC}   $url (请求过多)" ;;
        *)   echo -e "  ${RED}${code} Error${NC}     $url" ;;
    esac
}

# ---- 提交单个 URL (GET) ----
submit_single() {
    local url=$1
    local encoded_url
    encoded_url=$(url_encode "$url")
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" \
        "${INDEXNOW_API}?url=${encoded_url}&key=${API_KEY}")
    format_response "$code" "$url"
}

# ---- 批量提交 URL (POST) ----
submit_batch() {
    local host=$1
    shift
    local urls=("$@")

    # 构建 JSON URL 数组
    local url_json=""
    for url in "${urls[@]}"; do
        [ -n "$url_json" ] && url_json+=","
        url_json+="\"$url\""
    done

    local body="{\"host\":\"${host}\",\"key\":\"${API_KEY}\",\"keyLocation\":\"https://${host}/${API_KEY}.txt\",\"urlList\":[${url_json}]}"

    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "${INDEXNOW_API}" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "$body")

    echo "$code"
}

# ---- 从 XML 提取 URL（macOS 兼容） ----
extract_urls_from_xml() {
    grep -o '<loc>[^<]*</loc>' | sed 's/<loc>//g;s/<\/loc>//g'
}

# ---- submit 命令 ----
cmd_submit() {
    if [ $# -eq 0 ]; then
        log_error "请提供至少一个 URL"
        echo "用法: $0 submit <url1> [url2] [url3] ..."
        exit 1
    fi

    load_key

    local urls=("$@")
    local count=${#urls[@]}

    log_info "准备提交 $count 个 URL (Key: ${API_KEY:0:8}...)"
    echo ""

    if [ $count -eq 1 ]; then
        log_step "提交 URL..."
        submit_single "${urls[0]}"
    else
        local host
        host=$(extract_host "${urls[0]}")
        log_step "批量提交到 host: $host"

        local code
        code=$(submit_batch "$host" "${urls[@]}")

        echo ""
        if [ "$code" = "200" ] || [ "$code" = "202" ]; then
            log_info "批量提交成功 ($code)"
            for url in "${urls[@]}"; do
                echo -e "  ${GREEN}OK${NC} $url"
            done
        else
            format_response "$code" "(批量 $count 个 URL)"
        fi
    fi

    echo ""
    log_info "提交完成"
}

# ---- submit-sitemap 命令 ----
cmd_submit_sitemap() {
    local sitemap_path="${1:-public/sitemap.xml}"

    if [ ! -f "$sitemap_path" ]; then
        log_error "Sitemap 文件不存在: $sitemap_path"
        exit 1
    fi

    load_key

    # 从 sitemap 提取 URL
    local urls=()
    while IFS= read -r url; do
        [ -n "$url" ] && urls+=("$url")
    done < <(cat "$sitemap_path" | extract_urls_from_xml)

    if [ ${#urls[@]} -eq 0 ]; then
        log_error "未从 sitemap 中提取到 URL"
        exit 1
    fi

    local host
    host=$(extract_host "${urls[0]}")

    log_info "从 $sitemap_path 提取到 ${#urls[@]} 个 URL"
    log_info "Host: $host"
    echo ""

    # 按 10000 个一批提交
    local total=${#urls[@]}
    local batch_size=10000
    local offset=0

    while [ $offset -lt $total ]; do
        local end=$((offset + batch_size))
        [ $end -gt $total ] && end=$total
        local batch=("${urls[@]:$offset:$batch_size}")

        if [ $total -gt $batch_size ]; then
            log_step "提交第 $((offset/batch_size + 1)) 批 (${#batch[@]} 个 URL)..."
        else
            log_step "提交 ${#batch[@]} 个 URL..."
        fi

        local code
        code=$(submit_batch "$host" "${batch[@]}")

        if [ "$code" = "200" ] || [ "$code" = "202" ]; then
            log_info "提交成功 ($code) - ${#batch[@]} 个 URL"
        else
            format_response "$code" "(批量 ${#batch[@]} 个 URL)"
        fi

        offset=$end
    done

    echo ""
    log_info "全部提交完成 ($total 个 URL)"
    echo ""
    echo "已提交的 URL:"
    for url in "${urls[@]}"; do
        echo "  $url"
    done
}

# ---- submit-sitemap-url 命令 ----
cmd_submit_sitemap_url() {
    local sitemap_url="$1"

    if [ -z "$sitemap_url" ]; then
        log_error "请提供 sitemap URL"
        echo "用法: $0 submit-sitemap-url https://example.com/sitemap.xml"
        exit 1
    fi

    load_key

    log_step "下载 sitemap: $sitemap_url"
    local content
    content=$(curl -sL "$sitemap_url")

    if [ -z "$content" ]; then
        log_error "无法下载 sitemap"
        exit 1
    fi

    # 提取 URL
    local urls=()
    while IFS= read -r url; do
        [ -n "$url" ] && urls+=("$url")
    done < <(echo "$content" | extract_urls_from_xml)

    if [ ${#urls[@]} -eq 0 ]; then
        log_error "未从 sitemap 中提取到 URL"
        exit 1
    fi

    local host
    host=$(extract_host "${urls[0]}")

    log_info "提取到 ${#urls[@]} 个 URL"
    log_info "Host: $host"
    echo ""

    local code
    code=$(submit_batch "$host" "${urls[@]}")

    if [ "$code" = "200" ] || [ "$code" = "202" ]; then
        log_info "批量提交成功 ($code) - ${#urls[@]} 个 URL"
        for url in "${urls[@]}"; do
            echo -e "  ${GREEN}OK${NC} $url"
        done
    else
        format_response "$code" "(批量 ${#urls[@]} 个 URL)"
    fi

    echo ""
    log_info "提交完成"
}

# ---- status 命令 ----
cmd_status() {
    echo "IndexNow 状态"
    echo "=============="

    if [ -f "$KEY_FILE" ]; then
        local key
        key=$(cat "$KEY_FILE" | tr -d '[:space:]')
        echo -e "API Key:     ${GREEN}${key}${NC}"

        local verify_file="public/${key}.txt"
        if [ -f "$verify_file" ]; then
            local content
            content=$(cat "$verify_file" | tr -d '[:space:]')
            if [ "$content" = "$key" ]; then
                echo -e "验证文件:    ${GREEN}${verify_file} ✓${NC}"
            else
                echo -e "验证文件:    ${RED}${verify_file} (内容不匹配)${NC}"
            fi
        else
            echo -e "验证文件:    ${RED}未找到 ${verify_file}${NC}"
        fi
    else
        echo -e "API Key:     ${RED}未生成${NC}"
        echo -e "             运行: indexnow.sh generate-key"
    fi

    if [ -f "public/sitemap.xml" ]; then
        local url_count
        url_count=$(grep -c '<loc>' "public/sitemap.xml" 2>/dev/null || echo "0")
        echo -e "Sitemap:     ${GREEN}public/sitemap.xml ($url_count 个 URL)${NC}"
    else
        echo -e "Sitemap:     ${YELLOW}未找到 public/sitemap.xml${NC}"
    fi

    echo ""
}

# ---- 主入口 ----
case "${1:-}" in
    generate-key)
        shift
        cmd_generate_key "$@"
        ;;
    submit)
        shift
        cmd_submit "$@"
        ;;
    submit-sitemap)
        shift
        cmd_submit_sitemap "$@"
        ;;
    submit-sitemap-url)
        shift
        cmd_submit_sitemap_url "$@"
        ;;
    status)
        cmd_status
        ;;
    *)
        echo "IndexNow URL 提交工具"
        echo ""
        echo "用法: $0 <command> [args]"
        echo ""
        echo "命令:"
        echo "  generate-key              生成 API key 和验证文件"
        echo "  submit <url1> [url2...]    提交一个或多个 URL"
        echo "  submit-sitemap [path]      从本地 sitemap 提取并提交 (默认 public/sitemap.xml)"
        echo "  submit-sitemap-url <url>   从远程 sitemap 提取并提交"
        echo "  status                     显示当前配置状态"
        ;;
esac
