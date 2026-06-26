#!/bin/bash
# Ollama Web Search API 实现脚本 v1.0.0

set -euo pipefail

readonly VERSION="1.0.1"
readonly TIMEOUT_SECONDS=30
readonly MAX_QUERY_LENGTH=1000
readonly MAX_URL_LENGTH=2048

# ==================== 帮助和版本 ====================
show_help() {
  cat << 'EOF'
Ollama Web Search CLI v1.0.1

使用 Ollama Web Search API 进行网络搜索和网页抓取。

用法:
  ollama-web-search.sh search "查询主题" [结果数量]   # 执行网络搜索
  ollama-web-search.sh fetch "URL"                   # 抓取网页内容
  ollama-web-search.sh --help                         # 显示此帮助
  ollama-web-search.sh --version                      # 显示版本

参数:
  search    搜索模式
    - 参数1: 搜索查询字符串 (必需)
    - 参数2: 最大结果数量 (可选, 默认5, 范围1-10)

  fetch     抓取模式
    - 参数1: 网页URL (必需, 必须以 http:// 或 https:// 开头)

环境变量:
  OLLAMA_API_KEY    必需。从 https://ollama.com/settings/keys 获取

示例:
  export OLLAMA_API_KEY='your_key_here'
  ./ollama-web-search.sh search "AI最新进展" 5
  ./ollama-web-search.sh fetch "https://ollama.com"

EOF
}

show_version() {
  echo "Ollama Web Search CLI v${VERSION}"
  echo "Author: sunnydou"
  echo "License: MIT"
}

# ==================== 参数处理 ====================
MODE="${1:-}"
ARG1="${2:-}"
ARG2="${3:-}"

# 帮助和版本检查
if [ "$MODE" = "--help" ] || [ "$MODE" = "-h" ]; then
  show_help
  exit 0
fi

if [ "$MODE" = "--version" ] || [ "$MODE" = "-v" ]; then
  show_version
  exit 0
fi

if [ -z "$MODE" ] || [ -z "$ARG1" ]; then
  show_help
  exit 1
fi

# ==================== API Key 检查 ====================
if [ -z "${OLLAMA_API_KEY:-}" ]; then
  echo "❌ 错误：OLLAMA_API_KEY 环境变量未设置" >&2
  echo "" >&2
  echo "请设置环境变量：" >&2
  echo "  export OLLAMA_API_KEY='your_key_here'" >&2
  echo "" >&2
  echo "获取 API Key: https://ollama.com/settings/keys" >&2
  exit 1
fi

# ==================== 临时目录 ====================
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# ==================== 工具函数 ====================
# 安全地打印错误（脱敏 API Key）
safe_error() {
  local msg="$1"
  # 如果消息中包含 API Key，用 **** 替换
  if [[ -n "${OLLAMA_API_KEY:-}" ]]; then
    msg="${msg//${OLLAMA_API_KEY}/****REDACTED****}"
  fi
  echo "❌ $msg" >&2
}

# 验证 HTTP 状态码
check_http_status() {
  local http_code="$1"
  if [ "$http_code" != "200" ]; then
    safe_error "HTTP 错误: $http_code"
    return 1
  fi
  return 0
}

# ==================== Web Search ====================
if [ "$MODE" = "search" ]; then
  QUERY="$ARG1"
  MAX_RESULTS="${ARG2:-5}"
  
  # 输入验证：查询长度
  if [ "${#QUERY}" -gt "$MAX_QUERY_LENGTH" ]; then
    safe_error "查询过长 (最大 ${MAX_QUERY_LENGTH} 字符, 当前 ${#QUERY})"
    exit 1
  fi
  
  # 输入验证：限制结果数量
  if ! [[ "$MAX_RESULTS" =~ ^[0-9]+$ ]] || [ "$MAX_RESULTS" -lt 1 ] || [ "$MAX_RESULTS" -gt 10 ]; then
    MAX_RESULTS=5
  fi
  
  # 安全构建 JSON
  printf '%s' "$QUERY" > "$TEMP_DIR/query.txt"
  
  JSON_PAYLOAD=$(python3 << 'PYEOF'
import json
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    query = f.read()

max_results = int(sys.argv[2])
print(json.dumps({'query': query, 'max_results': max_results}))
PYEOF
  "$TEMP_DIR/query.txt" "$MAX_RESULTS" 2>/dev/null) || {
    safe_error "查询参数处理失败"
    exit 1
  }
  
  if [ -z "$JSON_PAYLOAD" ]; then
    safe_error "JSON 构建失败"
    exit 1
  fi
  
  echo "🔍 搜索：(最多 $MAX_RESULTS 个结果)"
  echo ""
  
  # 执行请求并检查状态码
  HTTP_CODE=$(curl -s -o "$TEMP_DIR/response.txt" -w "%{http_code}" \
    --max-time "$TIMEOUT_SECONDS" \
    -X POST "https://ollama.com/api/web_search" \
    --header "Authorization: Bearer $OLLAMA_API_KEY" \
    --header "Content-Type: application/json" \
    -d "$JSON_PAYLOAD" 2>/dev/null || echo "000")
  
  if [ "$HTTP_CODE" = "000" ]; then
    safe_error "请求失败 (网络错误或超时)"
    exit 1
  fi
  
  check_http_status "$HTTP_CODE" || exit 1
  
  RESPONSE=$(cat "$TEMP_DIR/response.txt")
  
  # 检查 API 错误
  if echo "$RESPONSE" | grep -q '"error"'; then
    ERROR_MSG=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('error', 'Unknown error'))
except:
    print('Unknown error')
" 2>/dev/null || echo "Unknown error")
    safe_error "API 错误: $ERROR_MSG"
    exit 1
  fi
  
  # 解析并输出结果
  echo "$RESPONSE" | python3 << 'PYEOF'
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    if not results:
        print("未找到结果")
        sys.exit(0)
    
    for i, r in enumerate(results, 1):
        print(f"📄 {r.get('title', 'N/A')}")
        print(f"🔗 {r.get('url', 'N/A')}")
        content = r.get('content', '')[:500]
        print(f"📝 {content}...")
        print()
except json.JSONDecodeError as e:
    print(f'解析错误：无效的 JSON 响应')
    sys.exit(1)
except Exception as e:
    print(f'解析错误：{e}')
    sys.exit(1)
PYEOF
  
  echo "✅ 搜索完成"

# ==================== Web Fetch ====================
elif [ "$MODE" = "fetch" ]; then
  URL="$ARG1"
  
  # 输入验证：URL 长度
  if [ "${#URL}" -gt "$MAX_URL_LENGTH" ]; then
    safe_error "URL 过长 (最大 ${MAX_URL_LENGTH} 字符)"
    exit 1
  fi
  
  # 输入验证：检查 URL 格式
  if ! [[ "$URL" =~ ^https?:// ]]; then
    safe_error "无效的 URL 格式。URL 必须以 http:// 或 https:// 开头"
    exit 1
  fi
  
  # 安全构建 JSON
  printf '%s' "$URL" > "$TEMP_DIR/url.txt"
  
  JSON_PAYLOAD=$(python3 << 'PYEOF'
import json
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    url = f.read()

print(json.dumps({'url': url}))
PYEOF
  "$TEMP_DIR/url.txt" 2>/dev/null) || {
    safe_error "URL 参数处理失败"
    exit 1
  }
  
  if [ -z "$JSON_PAYLOAD" ]; then
    safe_error "JSON 构建失败"
    exit 1
  fi
  
  echo "📡 抓取中..."
  echo ""
  
  # 执行请求并检查状态码
  HTTP_CODE=$(curl -s -o "$TEMP_DIR/response.txt" -w "%{http_code}" \
    --max-time "$TIMEOUT_SECONDS" \
    -X POST "https://ollama.com/api/web_fetch" \
    --header "Authorization: Bearer $OLLAMA_API_KEY" \
    --header "Content-Type: application/json" \
    -d "$JSON_PAYLOAD" 2>/dev/null || echo "000")
  
  if [ "$HTTP_CODE" = "000" ]; then
    safe_error "请求失败 (网络错误或超时)"
    exit 1
  fi
  
  check_http_status "$HTTP_CODE" || exit 1
  
  RESPONSE=$(cat "$TEMP_DIR/response.txt")
  
  # 检查 API 错误
  if echo "$RESPONSE" | grep -q '"error"'; then
    ERROR_MSG=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('error', 'Unknown error'))
except:
    print('Unknown error')
" 2>/dev/null || echo "Unknown error")
    safe_error "API 错误: $ERROR_MSG"
    exit 1
  fi
  
  # 解析并输出结果
  echo "$RESPONSE" | python3 << 'PYEOF'
import sys, json
try:
    data = json.load(sys.stdin)
    
    title = data.get('title', 'N/A')
    if title == 'N/A' or not title:
        title = '无标题'
    
    print(f"📄 标题：{title}")
    print()
    
    content = data.get('content', '')
    if content:
        print(f"📝 内容:")
        print(content[:2000])
        if len(content) > 2000:
            print("\n... (内容已截断)")
    else:
        print("📝 内容: (空)")
    
    print()
    links = data.get('links', [])
    if links:
        print(f"🔗 页面链接 (前 10 个):")
        for link in links[:10]:
            print(f"  - {link}")
        if len(links) > 10:
            print(f"  ... 还有 {len(links) - 10} 个链接")
except json.JSONDecodeError as e:
    print(f'解析错误：无效的 JSON 响应')
    sys.exit(1)
except Exception as e:
    print(f'解析错误：{e}')
    sys.exit(1)
PYEOF

else
  safe_error "未知模式: $MODE。请使用 'search' 或 'fetch'"
  show_help
  exit 1
fi
