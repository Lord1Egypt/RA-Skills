#!/bin/bash
#
# Memory Indexer 更新脚本
# 用法: ./update.sh [--skip-config] [--skip-hooks]
#
# 选项:
#   --skip-config  跳过配置文件更新
#   --skip-hooks   跳过 Hook 更新
#

set -e

echo "🔄 Memory Indexer 更新程序"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 解析参数
SKIP_CONFIG=false
SKIP_HOOKS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-config)
            SKIP_CONFIG=true
            shift
            ;;
        --skip-hooks)
            SKIP_HOOKS=true
            shift
            ;;
        -h|--help)
            echo "用法: $0 [--skip-config] [--skip-hooks]"
            echo ""
            echo "选项:"
            echo "  --skip-config   跳过配置文件更新"
            echo "  --skip-hooks    跳过 Hook 更新"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

# 检查是否是 git 仓库
if [ ! -d ".git" ]; then
    echo -e "${RED}错误: 当前目录不是 Git 仓库${NC}"
    exit 1
fi

# 获取当前版本
CURRENT_VERSION=$(git describe --tags --always --dirty 2>/dev/null || echo "unknown")
echo "当前版本: $CURRENT_VERSION"

# 备份重要数据
echo ""
echo "💾 备份数据..."
BACKUP_DIR="$SCRIPT_DIR/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f "data/index.json" ]; then
    cp data/index.json "$BACKUP_DIR/"
    echo "✅ 索引已备份"
fi
if [ -f "data/sync-state.json" ]; then
    cp data/sync-state.json "$BACKUP_DIR/"
    echo "✅ 同步状态已备份"
fi
if [ -f "data/stars.json" ]; then
    cp data/stars.json "$BACKUP_DIR/"
    echo "✅ 星星标记已备份"
fi

echo "📁 备份目录: $BACKUP_DIR"

# 拉取最新代码
echo ""
echo "📥 拉取最新代码..."
git fetch origin
git pull origin main --rebase || git pull origin master --rebase

# 获取新版本
NEW_VERSION=$(git describe --tags --always --dirty 2>/dev/null || echo "unknown")
echo "新版本: $NEW_VERSION"

# 重新安装依赖
echo ""
echo "📦 检查依赖..."
if python3 -c "import jieba" 2>/dev/null; then
    echo "✅ jieba 已安装"
else
    uv pip install jieba
    echo "✅ jieba 安装完成"
fi

# 运行迁移脚本（如果需要）
if [ -f "migrate.sh" ]; then
    echo ""
    echo "🔧 运行迁移脚本..."
    chmod +x migrate.sh
    ./migrate.sh
fi

# 更新 OpenClaw 配置文件
if [ "$SKIP_CONFIG" = false ]; then
    echo ""
    echo "🔧 更新 OpenClaw 配置文件..."
    
    WORKSPACE="${HOME}/.openclaw/workspace"
    
    if [ -d "$WORKSPACE" ]; then
        # 更新软链接
        echo "🔗 更新软链接..."
        mkdir -p "$WORKSPACE/skills"
        if [ ! -L "$WORKSPACE/skills/memory-indexer" ]; then
            ln -sf "$SCRIPT_DIR" "$WORKSPACE/skills/memory-indexer"
            echo "✅ 软链接已创建"
        else
            echo "✅ 软链接已存在"
        fi
        
        # 重新运行 install.sh 进行配置更新
        echo ""
        echo "📝 运行安装脚本以更新配置..."
        chmod +x install.sh
        
        # 检查是否配置了 AGENTS.md
        if [ -f "$WORKSPACE/AGENTS.md" ]; then
            if grep -q "Memory Indexer" "$WORKSPACE/AGENTS.md" 2>/dev/null; then
                echo "⚠️  AGENTS.md 已包含 Memory Indexer 配置，将更新"
            fi
        fi
        
        # 执行 install.sh 的配置部分（不创建软链接）
        bash -c "
            source install.sh 2>/dev/null || true
        " || true
        
        echo "✅ 配置文件已更新"
    else
        echo -e "${YELLOW}⚠️  未找到 OpenClaw workspace，跳过配置更新${NC}"
        echo "   如需配置，请手动运行: ./install.sh"
    fi
else
    echo -e "${YELLOW}⏭️  跳过配置文件更新${NC}"
fi

# 更新 Hook
if [ "$SKIP_HOOKS" = false ]; then
    echo ""
    echo "🪝 更新 Hook..."
    
    HOOKS_DIR="${HOME}/.openclaw/hooks"
    
    if [ -d "hooks/memory-indexer-on-new" ]; then
        if [ -d "$HOOKS_DIR" ]; then
            cp -r hooks/memory-indexer-on-new "$HOOKS_DIR/"
            echo "✅ Hook 已更新"
            echo "   提示: 如需生效，请运行: openclaw gateway restart"
        else
            echo -e "${YELLOW}⚠️  未找到 Hooks 目录，跳过${NC}"
        fi
    else
        echo "ℹ️  未找到 Hook 目录"
    fi
else
    echo -e "${YELLOW}⏭️  跳过 Hook 更新${NC}"
fi

# 清理并重新同步
echo ""
echo "🔄 重新同步索引..."
python3 memory-indexer.py sync 2>/dev/null || python3 memory-indexer.py sync

# 完成
echo ""
echo "================================"
echo -e "${GREEN}🎉 更新完成！${NC}"
echo ""
echo "📋 更新日志:"
git log --oneline -5
echo ""

# 提示备份清理
echo "💡 提示:"
echo "   - 如果更新后一切正常，可以删除备份目录:"
echo "     rm -rf $BACKUP_DIR"
echo "   - 如果使用了 Hook，可能需要重启 Gateway:"
echo "     openclaw gateway restart"
