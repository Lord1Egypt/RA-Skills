#!/bin/bash
# OpenCode 灵芯派记忆技能包 - 安装脚本

set -e

echo "🧠 OpenCode 记忆技能包安装..."

# 记忆库目标路径
MEMORY_DIR="$HOME/.opencode-memory"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. 创建记忆库目录
echo "📁 创建记忆库目录..."
mkdir -p "$MEMORY_DIR"

# 2. 复制记忆文件
echo "📋 复制记忆文件..."
cp "$SKILL_DIR/"*.md "$MEMORY_DIR/" 2>/dev/null || true
cp "$SKILL_DIR/"*.json "$MEMORY_DIR/" 2>/dev/null || true
cp "$SKILL_DIR/"*.sh "$MEMORY_DIR/" 2>/dev/null || true
chmod +x "$MEMORY_DIR/sync.sh"

# 3. 初始化git仓库（如果没有）
if [ ! -d "$MEMORY_DIR/.git" ]; then
    echo "📦 初始化Git仓库..."
    cd "$MEMORY_DIR"
    git init

    # 创建.gitignore
    cat > "$MEMORY_DIR/.gitignore" << 'EOF'
.DS_Store
*.log
EOF

    git add .
    git commit -m "init: OpenCode记忆库初始化"
fi

# 4. 检查远程仓库
echo "🔗 检查远程仓库..."
cd "$MEMORY_DIR"
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$REMOTE" ]; then
    echo "⚠️  未配置远程仓库，需要手动添加:"
    echo "   cd $MEMORY_DIR"
    echo "   git remote add origin <你的Gitee仓库URL>"
    echo "   git push -u origin master"
else
    echo "✅ 远程仓库已配置: $REMOTE"
fi

# 5. 完成
echo ""
echo "🎉 安装完成!"
echo ""
echo "📍 记忆库位置: $MEMORY_DIR"
echo ""
echo "📖 使用方法:"
echo "   # 查看README"
echo "   cat $MEMORY_DIR/README.md"
echo ""
echo "   # 同步记忆"
echo "   $MEMORY_DIR/sync.sh"
echo ""
echo "   # 恢复记忆(新对话开始时)"
echo "   cat $MEMORY_DIR/MEMORY.md"
echo ""