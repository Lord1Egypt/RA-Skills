#!/usr/bin/bash
# GitHub 稳定克隆脚本 v2.1
# 用法: github-clone.sh <url> [target-dir] [options]
#
# 选项：
#   --full        完整克隆（默认浅克隆 --depth 1）
#   --oref <ref>  指定 tag/commit（如 --oref v1.0.0 或 --oref abc123）
#   --probe       只探测可用镜像，不实际克隆
#   --timeout <s> 自定义超时秒数（默认 30）
#   --branch <b>  指定分支（默认自动探测 main/master）
#
# 示例：
#   github-clone.sh https://github.com/d9g/page-build.git
#   github-clone.sh https://github.com/d9g/page-build.git ~/proj --oref v2.0.0
#   github-clone.sh https://github.com/d9g/page-build.git ~/proj --timeout 60
#   github-clone.sh https://github.com/d9g/page-build.git --probe

set -e

# 默认值
DEPTH="--depth=1"
CLONE_TIMEOUT=30
BRANCH=""
OREF=""
PROBE_ONLY=false
FULL_CLONE=false

# 解析参数
URL=""
TARGET=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --full)
            FULL_CLONE=true
            DEPTH=""
            shift
            ;;
        --oref)
            OREF="$2"
            shift 2
            ;;
        --probe)
            PROBE_ONLY=true
            shift
            ;;
        --timeout)
            CLONE_TIMEOUT="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        -*)
            echo "❌ 未知参数: $1"
            exit 1
            ;;
        *)
            if [ -z "$URL" ]; then
                URL="$1"
            elif [ -z "$TARGET" ]; then
                TARGET="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$URL" ]; then
    echo "用法: github-clone.sh <url> [target-dir] [options]"
    echo ""
    echo "选项："
    echo "  --full        完整克隆（默认浅克隆）"
    echo "  --oref <ref>  指定 tag/commit（如 v1.0.0 或 abc123）"
    echo "  --probe       只探测可用镜像，不实际克隆"
    echo "  --timeout <s> 自定义超时秒数（默认 30）"
    echo "  --branch <b>  指定分支（默认自动探测）"
    echo ""
    echo "示例："
    echo "  github-clone.sh https://github.com/d9g/page-build.git"
    echo "  github-clone.sh https://github.com/d9g/page-build.git ~/proj --oref v2.0.0"
    echo "  github-clone.sh https://github.com/d9g/page-build.git --probe"
    exit 1
fi

# ========== 工具函数 ==========

parse_repo_info() {
    local url="$1"
    if [[ "$url" =~ ^https://github\.com/([^/]+)/([^/]+)(\.git)?$ ]]; then
        USER="${BASH_REMATCH[1]}"
        REPO="${BASH_REMATCH[2]}"
        REPO="${REPO%.git}"
    elif [[ "$url" =~ ^git@github\.com:([^/]+)/([^/]+)(\.git)?$ ]]; then
        USER="${BASH_REMATCH[1]}"
        REPO="${BASH_REMATCH[2]}"
        REPO="${REPO%.git}"
    else
        echo "❌ 无法解析仓库 URL: $url"
        exit 1
    fi
}

ssh_precheck() {
    echo "🔑 检测 SSH key..."
    
    if ! ls ~/.ssh/id_*.pub >/dev/null 2>&1; then
        echo "   ❌ 无 SSH key 文件"
        return 1
    fi
    
    echo "   检测 key 有效性..."
    local ssh_output
    ssh_output=$(timeout 10 ssh -T git@github.com -o StrictHostKeyChecking=no -o BatchMode=yes 2>&1 || true)
    
    if [[ "$ssh_output" =~ "successfully authenticated" ]]; then
        echo "   ✅ SSH key 已绑定 GitHub"
        return 0
    elif [[ "$ssh_output" =~ "Permission denied" ]]; then
        echo "   ❌ SSH key 未绑定 GitHub"
        return 2
    else
        echo "   ⚠️ SSH 连接异常"
        return 1
    fi
}

probe_mirrors() {
    echo ""
    echo "🔍 探测可用镜像..."
    echo ""
    
    local available=()
    
    # SSH
    if ssh_precheck; then
        echo "   ✅ SSH 方式可用"
        available+=("ssh")
    fi
    
    # ghproxy 镜像
    local HTTPS_URL="https://github.com/$USER/$REPO.git"
    for MIRROR in "ghproxy.com" "mirror.ghproxy.com" "gh-proxy.com"; do
        local PROXY_URL="https://$MIRROR/$HTTPS_URL"
        echo "   探测: $MIRROR..."
        
        local http_code
        http_code=$(timeout 5 curl -s -o /dev/null -w "%{http_code}" "$PROXY_URL" 2>/dev/null || echo "000")
        
        if [ "$http_code" = "200" ] || [ "$http_code" = "301" ] || [ "$http_code" = "302" ]; then
            echo "   ✅ $MIRROR 可用"
            available+=("$MIRROR")
        else
            echo "   ❌ $MIRROR 不可用 (HTTP $http_code)"
        fi
    done
    
    # 原 HTTPS
    echo "   探测: github.com (HTTPS)..."
    local github_code
    github_code=$(timeout 5 curl -s -o /dev/null -w "%{http_code}" "$HTTPS_URL" 2>/dev/null || echo "000")
    if [ "$github_code" = "200" ] || [ "$github_code" = "301" ]; then
        echo "   ✅ 原 HTTPS 可用"
        available+=("github-https")
    else
        echo "   ❌ 原 HTTPS 不可用"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 探测结果汇总"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ ${#available[@]} -eq 0 ]; then
        echo "❌ 无可用镜像"
        return 1
    else
        echo "✅ 可用镜像："
        for mirror in "${available[@]}"; do
            echo "   - $mirror"
        done
        echo ""
        echo "💡 推荐顺序："
        echo "   1. SSH（最稳定）"
        echo "   2. ghproxy.com"
        echo "   3. 原 HTTPS"
        return 0
    fi
}

# ========== 主流程 ==========

parse_repo_info "$URL"
echo "📦 仓库: $USER/$REPO"

# 探测模式
if [ "$PROBE_ONLY" = true ]; then
    probe_mirrors
    exit $?
fi

echo "📝 克隆深度: $([ "$FULL_CLONE" = true ] && echo "完整" || echo "浅克隆 (--depth 1)")"
echo "⏱️ 超时设置: $CLONE_TIMEOUT 秒"

# 指定 ref
if [ -n "$OREF" ]; then
    echo "📌 指定 ref: $OREF"
fi

# 指定分支
if [ -n "$BRANCH" ]; then
    echo "📌 指定分支: $BRANCH"
fi

# 目标目录检查
if [ -d "$TARGET" ]; then
    if [ -d "$TARGET/.git" ]; then
        echo "⚠️ 目标已是 git 仓库: $TARGET"
        echo "   建议: 删除后重新克隆"
        exit 1
    else
        new_target="${TARGET}-$(date +%Y%m%d-%H%M%S)"
        echo "⚠️ 目标已存在，自动切换: $new_target"
        TARGET="$new_target"
    fi
fi

# SSH 预检测
SSH_URL="git@github.com:$USER/$REPO.git"

if ssh_precheck; then
    echo ""
    echo "🚀 方案 1: SSH clone"
    echo "   URL: $SSH_URL"
    
    # 构建 clone 命令
    clone_cmd="git clone $DEPTH $SSH_URL $TARGET"
    if [ -n "$OREF" ]; then
        clone_cmd="$clone_cmd && cd $TARGET && git checkout $OREF"
    fi
    
    if timeout $CLONE_TIMEOUT bash -c "$clone_cmd" 2>&1; then
        echo ""
        echo "✅ SSH clone 成功！"
        
        # LFS 检测
        if [ -f "$TARGET/.gitattributes" ] && grep -q "lfs" "$TARGET/.gitattributes"; then
            echo ""
            echo "⚠️ 检测到 Git LFS"
            echo "   完整克隆后执行: cd $TARGET && git lfs pull"
        fi
        
        exit 0
    else
        echo "   ❌ SSH clone 失败"
    fi
fi

# ghproxy 镜像
echo ""
echo "🌐 方案 2: ghproxy 镜像"

HTTPS_URL="https://github.com/$USER/$REPO.git"
for MIRROR in "ghproxy.com" "mirror.ghproxy.com" "gh-proxy.com"; do
    PROXY_URL="https://$MIRROR/$HTTPS_URL"
    echo "   尝试: $MIRROR..."
    
    clone_cmd="git clone $DEPTH"
if [ -n "$BRANCH" ]; then
    clone_cmd="$clone_cmd --branch $BRANCH"
fi
clone_cmd="$clone_cmd $PROXY_URL $TARGET"

if timeout $CLONE_TIMEOUT bash -c "$clone_cmd" 2>&1; then
        echo ""
        echo "✅ ghproxy clone 成功！（$MIRROR）"
        
        if [ -n "$OREF" ]; then
            cd "$TARGET" && git checkout "$OREF"
            echo "   已 checkout 到: $OREF"
        fi
        
        exit 0
    fi
done

echo "   ⚠️ ghproxy 均失败"

# 原 HTTPS
echo ""
echo "🌐 方案 3: 原 HTTPS"
echo "   URL: $HTTPS_URL"

clone_cmd="git clone $DEPTH"
if [ -n "$BRANCH" ]; then
    clone_cmd="$clone_cmd --branch $BRANCH"
fi
clone_cmd="$clone_cmd $HTTPS_URL $TARGET"

if timeout $CLONE_TIMEOUT bash -c "$clone_cmd" 2>&1; then
    echo ""
    echo "✅ HTTPS clone 成功！"
    
    if [ -n "$OREF" ]; then
        cd "$TARGET" && git checkout "$OREF"
        echo "   已 checkout 到: $OREF"
    fi
    
    exit 0
fi

echo "   ❌ HTTPS clone 失败"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "❌ 所有克隆方案均失败"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 建议："
echo "   1. 使用 --probe 先探测可用镜像"
echo "   2. 增加 --timeout 60 等待更长时间"
echo "   3. 使用 github-fetch-file.sh 获取关键文件"
exit 1