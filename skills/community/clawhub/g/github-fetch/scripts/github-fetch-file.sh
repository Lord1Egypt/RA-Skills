#!/bin/bash
# GitHub 单文件获取脚本 v2.0（优化版）
# 用法: github-fetch-file.sh <user/repo> <path> [branch] [output]
#
# 优化点：
# 1. 分支自动探测 - main/master
# 2. 多 CDN fallback - jsdelivr → ghproxy → raw.githubusercontent
# 3. 细化错误信息 - 区分 404/503/超时
# 4. 50MB 文件警告

set -e

REPO="$1"
FILE="$2"
BRANCH="${3:-}"  # 空则自动探测
OUTPUT="${4:-$FILE}"

if [ -z "$REPO" ] || [ -z "$FILE" ]; then
    echo "用法: github-fetch-file.sh <user/repo> <path> [branch] [output]"
    echo ""
    echo "示例:"
    echo "  github-fetch-file.sh d9g/page-build README.md"
    echo "  github-fetch-file.sh d9g/page-build src/main.py main main.py"
    echo "  github-fetch-file.sh d9g/page-build config.yml master"
    echo ""
    echo "优化："
    echo "  • 分支自动探测（main → master）"
    echo "  • 多 CDN fallback（jsdelivr → ghproxy → raw）"
    echo "  • 细化错误信息"
    exit 1
fi

# ========== 工具函数 ==========

# 探测默认分支
detect_branch() {
    local repo="$1"
    
    if [ -n "$BRANCH" ]; then
        echo "📌 使用指定分支: $BRANCH"
        return 0
    fi
    
    echo "🔍 探测默认分支..."
    
    # 尝试 GitHub API
    local api_url="https://api.github.com/repos/$repo"
    local response
    
    response=$(timeout 5 curl -fsSL "$api_url" 2>/dev/null || echo "")
    
    if [ -n "$response" ]; then
        if echo "$response" | grep -q '"default_branch": "main"'; then
            BRANCH="main"
            echo "   ✅ 默认分支: main"
        elif echo "$response" | grep -q '"default_branch": "master"'; then
            BRANCH="master"
            echo "   ✅ 默认分支: master"
        else
            BRANCH="main"
            echo "   ⚠️ 无法探测，使用: main"
        fi
    else
        BRANCH="main"
        echo "   ⚠️ API 不可用，使用: main（如失败请尝试 master）"
    fi
}

# 获取文件大小（通过 HTTP 头）
get_file_size() {
    local url="$1"
    local size
    
    size=$(timeout 5 curl -fsSLI "$url" 2>/dev/null | grep -i "content-length" | awk '{print $2}' | tr -d '\r' || echo "0")
    
    if [ -n "$size" ] && [ "$size" -gt 52428800 ]; then  # 50MB
        echo "⚠️ 文件超过 50MB（$((size/1048576))MB），jsdelivr CDN 可能失败"
        echo "   建议使用 ghproxy 或 raw.githubusercontent.com"
        return 1
    fi
    return 0
}

# 尝试下载
try_download() {
    local url="$1"
    local output="$2"
    local source_name="$3"
    
    echo "   尝试: $source_name"
    
    local http_code
    http_code=$(timeout 15 curl -fsSL -w "%{http_code}" -o "$output" "$url" 2>/dev/null || echo "000")
    
    case $http_code in
        200)
            echo "   ✅ 成功！来源: $source_name"
            return 0
            ;;
        404)
            echo "   ❌ 文件不存在（404）"
            return 2
            ;;
        503)
            echo "   ❌ CDN 服务不可用（503）"
            return 3
            ;;
        000|"")
            echo "   ❌ 连接超时"
            return 1
            ;;
        *)
            echo "   ❌ HTTP $http_code"
            return 1
            ;;
    esac
}

# ========== 主流程 ==========

echo "📥 获取文件: $REPO/$FILE"

# 探测分支
detect_branch "$REPO"

# 创建输出目录
OUTPUT_DIR=$(dirname "$OUTPUT")
if [ "$OUTPUT_DIR" != "." ] && [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

# ========== CDN 1: jsdelivr ==========
JSDELIVR_URL="https://cdn.jsdelivr.net/gh/$REPO@$BRANCH/$FILE"
echo ""
echo "🌐 CDN 1: jsdelivr"
echo "   URL: $JSDELIVR_URL"

# 检查文件大小
get_file_size "$JSDELIVR_URL" || true

try_download "$JSDELIVR_URL" "$OUTPUT" "jsdelivr" && {
    echo ""
    echo "✅ 保存到: $OUTPUT"
    echo "   文件大小: $(wc -c < "$OUTPUT") bytes"
    exit 0
}

# ========== CDN 2: ghproxy ==========
GHPROXY_URL="https://ghproxy.com/https://raw.githubusercontent.com/$REPO/$BRANCH/$FILE"
echo ""
echo "🌐 CDN 2: ghproxy"
echo "   URL: $GHPROXY_URL"

try_download "$GHPROXY_URL" "$OUTPUT" "ghproxy" && {
    echo ""
    echo "✅ 保存到: $OUTPUT"
    echo "   文件大小: $(wc -c < "$OUTPUT") bytes"
    exit 0
}

# ========== CDN 3: raw.githubusercontent ==========
RAW_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/$FILE"
echo ""
echo "🌐 CDN 3: raw.githubusercontent"
echo "   URL: $RAW_URL"

try_download "$RAW_URL" "$OUTPUT" "raw.githubusercontent" && {
    echo ""
    echo "✅ 保存到: $OUTPUT"
    echo "   文件大小: $(wc -c < "$OUTPUT") bytes"
    exit 0
}

# ========== 尝试 master 分支 ==========
if [ "$BRANCH" == "main" ]; then
    echo ""
    echo "🔄 尝试 master 分支..."
    
    MASTER_URL="https://raw.githubusercontent.com/$REPO/master/$FILE"
    try_download "$MASTER_URL" "$OUTPUT" "raw.githubusercontent (master)" && {
        echo ""
        echo "✅ 保存到: $OUTPUT"
        echo "   文件大小: $(wc -c < "$OUTPUT") bytes"
        echo "   提示: 文件在 master 分支，非 main"
        exit 0
    }
fi

# ========== 全部失败 ==========
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "❌ 所有 CDN 均失败"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 可能的原因："
echo "   1. 文件路径错误"
echo "   2. 分支名称错误（请指定 main 或 master）"
echo "   3. 仓库不存在或为私有仓库"
echo "   4. 文件超过 50MB（jsdelivr 限制）"
echo ""
echo "   jsdelivr 不支持私有仓库，单文件最大 50MB"
echo ""
echo "   建议："
echo "   github-fetch-file.sh $REPO $FILE master  # 尝试 master 分支"
echo "   或使用 SSH clone 获取完整仓库"
exit 1