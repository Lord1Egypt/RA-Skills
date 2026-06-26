#!/bin/bash
#===============================================================================
# profind-cli.sh — ProFind 命令行封装工具
#
# 功能：提供便捷的 profind 命令行接口
# 用法：
#   profind search <关键词> [--kind PDF] [--size larger:1MB]
#   profind window "搜索词"
#   profind api <SOAP-ACTION>
#   profind check
#
# 安装：将此脚本路径加入 PATH，或 source 此文件
#===============================================================================

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

# 默认参数
KIND=""
SIZE=""
DATE=""
PATH=""
SCOPE=""
LABEL=""
META=""
EXCLUDE=""

#-----------------------------------------------------------------------------
# 构建 URL
#-----------------------------------------------------------------------------
build_url() {
    local name="$1"
    local url="profind:search?name=${name}"
    [ -n "$KIND" ]  && url="${url}&kind=${KIND}"
    [ -n "$SIZE" ]  && url="${url}&size=${SIZE}"
    [ -n "$DATE" ]  && url="${url}&date=${DATE}"
    [ -n "$PATH" ]  && url="${url}&path=${PATH}"
    [ -n "$SCOPE" ] && url="${url}&scope=${SCOPE}"
    [ -n "$LABEL" ] && url="${url}&label=${LABEL}"
    [ -n "$META" ]  && url="${url}&meta=${META}"
    [ -n "$EXCLUDE" ] && url="${url}&exclude=${EXCLUDE}"
    echo "$url"
}

#-----------------------------------------------------------------------------
# 执行搜索
#-----------------------------------------------------------------------------
cmd_search() {
    local name="${1:-}"
    if [ -z "$name" ]; then
        echo -e "${RED}用法: profind search <关键词> [选项]${NC}"
        echo "选项:"
        echo "  --kind PDF|image|movie|document|archive|folder"
        echo "  --size larger:1MB|smaller:100KB|equal:5GB"
        echo "  --date modified:~week|created:~month"
        echo "  --path ~/Documents"
        echo "  --scope all|home|hidden"
        echo "  --label red|orange|yellow|green|blue|purple|gray"
        exit 1
    fi

    local url
    url=$(build_url "$name")
    echo -e "${GREEN}[ProFind]${NC} 搜索: $name"
    osascript -e "tell application \"ProFind\" to open location \"$url\"" &
}

#-----------------------------------------------------------------------------
# 打开搜索窗口
#-----------------------------------------------------------------------------
cmd_window() {
    local query="${1:-}"
    if [ -z "$query" ]; then
        echo -e "${GREEN}[ProFind]${NC} 打开搜索窗口..."
    else
        echo -e "${GREEN}[ProFind]${NC} 打开搜索窗口，关键词: $query"
    fi
    if [ -n "$query" ]; then
        osascript -e "tell application \"ProFind\" to open location \"profind:search?name=${query}\"" &
    else
        osascript -e "tell application \"ProFind\" to activate" &
    fi
}

#-----------------------------------------------------------------------------
# Media Server API
#-----------------------------------------------------------------------------
cmd_api() {
    local action="${1:-capabilities}"
    local port=54812

    echo -e "${GREEN}[ProFind API]${NC} action: $action"

    case "$action" in
        capabilities)
            curl -s --max-time 10 -X POST "http://localhost:$port/ContentDirectory/control" \
              -H "Content-Type: text/xml; charset=utf-8" \
              -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#GetSearchCapabilities"' \
              -d '<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body><u:GetSearchCapabilities xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"/></s:Body>
</s:Envelope>'
            ;;
        browse)
            curl -s --max-time 10 -X POST "http://localhost:$port/ContentDirectory/control" \
              -H "Content-Type: text/xml; charset=utf-8" \
              -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#Browse"' \
              -d '<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
      <ObjectID>0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag>
      <Filter>*</Filter><StartingIndex>0</StartingIndex><RequestedCount>20</RequestedCount>
      <SortCriteria></SortCriteria>
    </u:Browse>
  </s:Body>
</s:Envelope>'
            ;;
        search)
            local keyword="${2:-pdf}"
            curl -s --max-time 15 -X POST "http://localhost:$port/ContentDirectory/control" \
              -H "Content-Type: text/xml; charset=utf-8" \
              -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#Search"' \
              -d "<?xml version=\"1.0\" encoding=\"utf-8\"?>
<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">
  <s:Body>
    <u:Search xmlns:u=\"urn:schemas-upnp-org:service:ContentDirectory:1\">
      <ContainerID>0</ContainerID>
      <SearchCriteria>(dc:title contains \"$keyword\")</SearchCriteria>
      <SortCriteria></SortCriteria>
    </u:Search>
  </s:Body>
</s:Envelope>"
            ;;
        *)
            echo -e "${RED}未知 action: $action${NC}"
            echo "可用: capabilities | browse | search [keyword]"
            ;;
    esac
}

#-----------------------------------------------------------------------------
# 健康检查
#-----------------------------------------------------------------------------
cmd_check() {
    echo -e "${GREEN}[ProFind]${NC} 健康检查"
    echo ""

    # ProFind 安装
    if [ -d "/Applications/ProFind.app" ]; then
        VERSION=$(defaults read /Applications/ProFind.app/Contents/Info.plist CFBundleShortVersionString 2>/dev/null)
        echo -e "  ✓ ProFind: v${VERSION}"
    else
        echo -e "  ${RED}✗ ProFind: 未安装${NC}"
    fi

    # ProFind 运行
    if pgrep -x "ProFind" > /dev/null; then
        echo -e "  ✓ ProFind: 运行中"
    else
        echo -e "  ${YELLOW}△ ProFind: 未运行（将自动启动）${NC}"
        open -a ProFind
        sleep 2
    fi

    # URL Scheme
    if osascript -e 'tell application "ProFind" to open location "profind:search?name=check"' 2>/dev/null; then
        echo -e "  ✓ URL Scheme: 正常"
    else
        echo -e "  ${RED}✗ URL Scheme: 失败${NC}"
    fi

    # Media Server
    HTTP_STATUS=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" "http://localhost:54812/" 2>/dev/null)
    if [ "$HTTP_STATUS" = "200" ]; then
        echo -e "  ✓ Media Server: HTTP 200 (端口 54812)"
    else
        echo -e "  ${YELLOW}△ Media Server: 未启动（可选，需在偏好设置中开启）${NC}"
    fi
}

#-----------------------------------------------------------------------------
# 帮助
#-----------------------------------------------------------------------------
cmd_help() {
    echo "ProFind CLI — macOS 文件搜索工具"
    echo ""
    echo "用法: profind <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  search <关键词> [选项]    搜索文件"
    echo "  window [关键词]           打开搜索窗口"
    echo "  api <action> [args]      调用 Media Server API"
    echo "  check                    健康检查"
    echo "  help                     显示帮助"
    echo ""
    echo "示例:"
    echo "  profind search report --kind PDF --date modified:~month"
    echo "  profind window \"*.swift\""
    echo "  profind api browse"
    echo "  profind api search pdf"
}

#-----------------------------------------------------------------------------
# 主入口
#-----------------------------------------------------------------------------
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --kind)  KIND="$2";  shift 2 ;;
            --size)  SIZE="$2";   shift 2 ;;
            --date)  DATE="$2";   shift 2 ;;
            --path)  PATH="$2";   shift 2 ;;
            --scope) SCOPE="$2";  shift 2 ;;
            --label) LABEL="$2";  shift 2 ;;
            --meta)  META="$2";   shift 2 ;;
            --exclude) EXCLUDE="$2"; shift 2 ;;
            *) break ;;
        esac
    done
    echo "$@"
}

main() {
    local cmd="${1:-help}"
    shift 2>/dev/null || true

    case "$cmd" in
        search)  parse_args "$@"; cmd_search  "$1" ;;
        window)  cmd_window "$1" ;;
        api)     cmd_api "$1" "$2" ;;
        check)   cmd_check ;;
        help|--help|-h) cmd_help ;;
        *)       echo -e "${RED}未知命令: $cmd${NC}"; cmd_help; exit 1 ;;
    esac
}

main "$@"
