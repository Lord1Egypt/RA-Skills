#!/bin/bash
#
# Smart Search CLI 脚本
# 统一智能搜索命令行入口
#
# 用法:
#   ./scripts/search.sh "查询内容" [options]
#   npm run search "查询内容" [options]
#
# 选项:
#   --count=<n>         结果数量 (默认: 10)
#   --language=<lang>   语言 (zh|en|auto, 默认: auto)
#   --intent=<type>     意图 (general|academic|technical|news)
#   --timeout=<ms>      超时毫秒 (默认: 5000)
#   --json              JSON 格式输出
#   --quiet             安静模式（仅输出错误）
#
# 示例:
#   ./scripts/search.sh "OpenClaw 新功能"
#   ./scripts/search.sh "LLM Agent 论文" --intent=academic --count=5
#   ./scripts/search.sh "MCP 配置教程" --intent=technical --language=zh
#
# 安全说明:
#   - 使用 set -euo pipefail 严格模式
#   - 所有变量使用双引号包裹防止词分割
#   - 避免使用 eval，使用数组构建参数
#   - 使用 exec 替换进程减少资源占用
#

# 严格模式：出错即退出、未定义变量报错、管道失败传播
set -euo pipefail

# 自动加载 .env 文件（如果存在）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
ENV_FILE="${PROJECT_DIR}/.env"

if [[ -f "$ENV_FILE" ]]; then
    set -a  # 自动导出所有变量
    source "$ENV_FILE"
    set +a  # 停止自动导出
fi

# 获取脚本所在目录（安全方式）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

# 默认参数
QUERY=""
COUNT=10
LANGUAGE="auto"
INTENT="general"
TIMEOUT=5000
OUTPUT_FORMAT="default"
QUIET=false

# 颜色定义
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# 显示帮助
show_help() {
    cat << 'EOF'
🔍 Smart Search - 统一智能搜索

用法:
  ./scripts/search.sh "<查询>" [选项]
  npm run search "<查询>" [选项]

选项:
  --count=<n>         返回结果数量 (默认: 10)
  --language=<lang>   语言偏好 (zh|en|auto, 默认: auto)
  --intent=<type>     搜索意图 (general|academic|technical|news)
  --timeout=<ms>      超时时间毫秒 (默认: 5000)
  --json              JSON 格式输出
  --quiet             安静模式（仅输出错误）
  --help              显示帮助

示例:
  ./scripts/search.sh "OpenClaw 新功能"
  ./scripts/search.sh "LLM Agent 论文" --intent=academic --count=5
  ./scripts/search.sh "MCP 配置" --intent=technical --language=zh --json

支持的搜索引擎:
  • 百炼 MCP (中文优化, 2000 次/月)
  • Tavily (高级搜索, 1000 次/月)
  • Serper (Google 结果, 2500 次/月)
  • Exa (学术搜索, 1000 次/月)
  • Firecrawl (网页抓取, 500 页/月)
EOF
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                show_help
                exit 0
                ;;
            --count=*)
                COUNT="${1#*=}"
                shift
                ;;
            --language=*)
                LANGUAGE="${1#*=}"
                shift
                ;;
            --intent=*)
                INTENT="${1#*=}"
                shift
                ;;
            --timeout=*)
                TIMEOUT="${1#*=}"
                shift
                ;;
            --json)
                OUTPUT_FORMAT="json"
                shift
                ;;
            --quiet|-q)
                QUIET=true
                shift
                ;;
            -*)
                echo -e "${RED}错误: 未知选项 $1${NC}" >&2
                show_help
                exit 1
                ;;
            *)
                if [[ -z "${QUERY:-}" ]]; then
                    QUERY="$1"
                fi
                shift
                ;;
        esac
    done
}

# 验证参数
validate_args() {
    if [[ -z "${QUERY:-}" ]]; then
        echo -e "${RED}错误: 请提供搜索查询${NC}" >&2
        echo ""
        show_help
        exit 1
    fi

    # 验证语言
    if [[ ! "$LANGUAGE" =~ ^(zh|en|auto)$ ]]; then
        echo -e "${YELLOW}警告: 无效语言 '$LANGUAGE'，使用 'auto'${NC}" >&2
        LANGUAGE="auto"
    fi

    # 验证意图
    if [[ ! "$INTENT" =~ ^(general|academic|technical|news)$ ]]; then
        echo -e "${YELLOW}警告: 无效意图 '$INTENT'，使用 'general'${NC}" >&2
        INTENT="general"
    fi

    # 验证数量 - 使用正则匹配确保是数字
    if [[ ! "$COUNT" =~ ^[0-9]+$ ]] || [[ "$COUNT" -lt 1 ]] || [[ "$COUNT" -gt 50 ]]; then
        echo -e "${YELLOW}警告: 无效数量 '$COUNT'，使用默认值 10${NC}" >&2
        COUNT=10
    fi
}

# 格式化输出（使用 node 处理 JSON）
format_output() {
    local json_output="$1"
    
    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        echo "$json_output"
        return
    fi
    
    # 解析 JSON 并格式化输出 - 使用 printf 和管道安全处理
    printf '%s' "$json_output" | node -e "
        const input = require('fs').readFileSync(0, 'utf-8');
        try {
            const data = JSON.parse(input);
            
            if (!data.success) {
                console.log('\\x1b[31m❌ 搜索失败\\x1b[0m');
                console.log('错误:', data.error || '未知错误');
                process.exit(1);
            }
            
            console.log('\\x1b[32m✅ 搜索成功\\x1b[0m');
            console.log('引擎:', data.enginesUsed.join(', '));
            console.log('结果:', data.results.length, '条');
            if (data.fallback) {
                console.log('\\x1b[33m⚠️  部分引擎失败，已降级\\x1b[0m');
            }
            console.log('');
            
            data.results.forEach((r, i) => {
                console.log(\`\${i + 1}. \${r.title || '无标题'}\`);
                console.log(\`   \\x1b[36m\${r.url}\\x1b[0m\`);
                if (r.snippet) {
                    const snippet = r.snippet.length > 150 ? r.snippet.substring(0, 150) + '...' : r.snippet;
                    console.log(\`   \${snippet}\`);
                }
                console.log(\`   引擎: \${r.engine} | 分数: \${(r.finalScore || 0).toFixed(2)}\`);
                console.log('');
            });
        } catch (e) {
            console.error('\\x1b[31m解析错误:\\x1b[0m', e.message);
            console.log('原始输出:', input.substring(0, 500));
            process.exit(1);
        }
    "
}

# 主函数
main() {
    parse_args "$@"
    validate_args
    
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${CYAN}🔍 搜索: ${QUERY}${NC}" >&2
        echo -e "${BLUE}   语言: ${LANGUAGE} | 意图: ${INTENT} | 数量: ${COUNT}${NC}" >&2
    fi
    
    # 安全构建参数数组 - 避免使用 eval
    local -a args=()
    args+=("${PROJECT_DIR}/dist/index.js")
    args+=("${QUERY}")
    args+=("--count=${COUNT}")
    
    if [[ "$LANGUAGE" != "auto" ]]; then
        args+=("--language=${LANGUAGE}")
    fi
    
    if [[ "$INTENT" != "general" ]]; then
        args+=("--intent=${INTENT}")
    fi
    
    args+=("--timeout=${TIMEOUT}")
    
    # 使用 exec 替换进程，安全传递参数
    # 注意：这里需要先检查 dist 目录是否存在
    if [[ ! -f "${PROJECT_DIR}/dist/src/index.js" ]]; then
        echo -e "${RED}错误: 未找到编译后的文件，请先运行 npm run build${NC}" >&2
        exit 1
    fi
    
    # 修正路径
    args[0]="${PROJECT_DIR}/dist/src/index.js"
    
    # 执行搜索并捕获输出
    local output
    if [[ "$QUIET" == "true" ]]; then
        output=$(node "${args[@]}" 2>/dev/null) || {
            echo -e "${RED}❌ 搜索失败${NC}" >&2
            exit 1
        }
    else
        output=$(node "${args[@]}" 2>&1) || true
        # 提取 JSON 输出（最后一行以 { 开头）
        local json_line
        json_line=$(echo "$output" | grep -E '^\{' | tail -1) || true
        if [[ -n "$json_line" ]]; then
            output="$json_line"
        fi
    fi
    
    # 格式化输出
    if [[ -n "${output:-}" ]]; then
        format_output "$output"
    else
        echo -e "${RED}❌ 搜索失败: 无输出${NC}" >&2
        exit 1
    fi
}

# 运行
main "$@"