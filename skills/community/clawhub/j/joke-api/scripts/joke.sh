#!/usr/bin/env bash

# JokeAPI CLI Tool
# 用法：joke <command> [options]

set -e

BASE_URL="https://v2.jokeapi.dev"

# 默认参数
CATEGORY="Any"
TYPE=""
FORMAT="json"
LANG="en"
BLACKLIST=""
AMOUNT="1"
CONTAINS=""
SAFE_MODE=""

# 显示帮助信息
show_help() {
    cat << EOF
JokeAPI CLI - 获取幽默笑话

用法：joke <command> [options]

命令:
  random      获取随机笑话 (默认命令)
  categories  列出所有可用分类
  langs       列出所有支持的语言
  info        获取 API 信息

选项:
  -c, --category CAT    指定分类 (默认：Any, 多个用逗号分隔)
  -t, --type TYPE       指定类型：single 或 twopart
  -f, --format FORMAT   指定格式：json, xml, yaml, txt (默认：json)
  -l, --lang CODE       指定语言代码 (默认：en)
  -b, --blacklist FLAGS 过滤标志 (nsfw,religious,racist,sexist,explicit)
  -a, --amount N        获取笑话数量 (1-10, 默认：1)
  -s, --contains TEXT   搜索包含特定文本的笑话
  --safe-mode          仅获取安全内容
  -h, --help           显示帮助信息

示例:
  joke random                    # 获取随机笑话
  joke random -c Programming     # 获取编程笑话
  joke random -c Misc,Pun -t twopart
  joke random --safe-mode        # 仅获取安全内容
  joke random -a 5               # 获取 5 个笑话
  joke categories                # 列出所有分类
  joke langs                     # 列出所有语言
EOF
}

# 获取笑话
get_joke() {
    local url="${BASE_URL}/joke/${CATEGORY}"
    local params=""
    
    [[ -n "$TYPE" ]] && params+="type=${TYPE}&"
    [[ "$FORMAT" != "json" ]] && params+="format=${FORMAT}&"
    [[ "$LANG" != "en" ]] && params+="lang=${LANG}&"
    [[ -n "$BLACKLIST" ]] && params+="blacklistFlags=${BLACKLIST}&"
    [[ "$AMOUNT" != "1" ]] && params+="amount=${AMOUNT}&"
    [[ -n "$CONTAINS" ]] && params+="contains=$(urlencode "$CONTAINS")&"
    [[ -n "$SAFE_MODE" ]] && params+="safe-mode&"
    
    # 移除末尾的 &
    params="${params%&}"
    
    if [[ -n "$params" ]]; then
        url+="?${params}"
    fi
    
    # 获取笑话
    local response
    response=$(curl -s "$url")
    
    # 根据格式输出
    if [[ "$FORMAT" == "txt" ]]; then
        if [[ "$AMOUNT" == "1" ]]; then
            echo "$response"
        else
            # 多笑话的 txt 格式处理
            echo "$response"
        fi
    elif [[ "$FORMAT" == "json" ]]; then
        if [[ "$AMOUNT" -gt 1 ]]; then
            # 多笑话 JSON 格式
            echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for i, joke in enumerate(data['jokes'], 1):
    print(f'--- 笑话 {i} ---')
    if joke['type'] == 'single':
        print(joke['joke'])
    else:
        print(joke['setup'])
        print()
        print(joke['delivery'])
    print()
"
        else
            # 单笑话 JSON 格式
            if echo "$response" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('error', False))" | grep -q "True"; then
                echo "错误："
                echo "$response" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Message: {d.get(\"message\", \"Unknown error\")}')
if d.get('additionalInfo'):
    print(f'详情：{d[\"additionalInfo\"]}')
"
                exit 1
            else
                if echo "$response" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('type', 'single'))" | grep -q "single"; then
                    echo "$response" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['joke'])"
                else
                    echo "$response" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d['setup'])
print()
print(d['delivery'])
"
                fi
            fi
        fi
    else
        echo "$response"
    fi
}

# URL 编码
urlencode() {
    python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$1"
}

# 列出分类
list_categories() {
    curl -s "${BASE_URL}/categories" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('可用分类:')
for cat in data.get('categories', []):
    print(f'  - {cat}')
"
}

# 列出语言
list_languages() {
    curl -s "${BASE_URL}/languages" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('支持的编程语言:')
for lang in data.get('jokeLanguages', []):
    print(f'  - {lang}')
"
}

# 获取 API 信息
get_info() {
    curl -s "${BASE_URL}/info" | python3 -m json.tool
}

# 解析命令行参数
COMMAND="random"

while [[ $# -gt 0 ]]; do
    case $1 in
        random|categories|langs|info)
            COMMAND="$1"
            shift
            ;;
        -c|--category)
            CATEGORY="$2"
            shift 2
            ;;
        -t|--type)
            TYPE="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -l|--lang)
            LANG="$2"
            shift 2
            ;;
        -b|--blacklist)
            BLACKLIST="$2"
            shift 2
            ;;
        -a|--amount)
            AMOUNT="$2"
            shift 2
            ;;
        -s|--contains)
            CONTAINS="$2"
            shift 2
            ;;
        --safe-mode)
            SAFE_MODE="1"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项：$1"
            show_help
            exit 1
            ;;
    esac
done

# 执行命令
case $COMMAND in
    random)
        get_joke
        ;;
    categories)
        list_categories
        ;;
    langs)
        list_languages
        ;;
    info)
        get_info
        ;;
esac
