#!/bin/bash

# switch-java.sh - 使用 Homebrew 自动安装并切换 Java 版本
# 用法：./switch-java.sh <version>
# 示例：./switch-java.sh 17 或 ./switch-java.sh 11

set -e

VERSION="${1:-}"

if [ -z "$VERSION" ]; then
    echo "❌ 请指定 Java 版本，例如：./switch-java.sh 17"
    echo "   支持的版本：8, 11, 17, 21 等"
    exit 1
fi

echo "🔧 macOS Java 版本切换工具"
echo "=========================="
echo ""

# 步骤 1: 检查 Homebrew 是否已安装
echo "🔍 步骤 1: 检查 Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew 未安装，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "✅ Homebrew 安装完成"
else
    echo "✅ Homebrew 已安装：$(brew --version)"
fi
echo ""

# 步骤 2: 检查指定版本的 Java 是否已安装
echo "🔍 步骤 2: 检查 Java $VERSION 是否已安装..."
if /usr/libexec/java_home -v "$VERSION" &> /dev/null; then
    echo "✅ Java $VERSION 已安装"
    INSTALLED=true
else
    echo "⚠️  Java $VERSION 未安装"
    INSTALLED=false
fi
echo ""

# 步骤 3: 如果未安装，使用 Homebrew 安装
if [ "$INSTALLED" = false ]; then
    echo "📦 步骤 3: 使用 Homebrew 安装 OpenJDK $VERSION..."
    brew install "openjdk@$VERSION"
    echo "✅ OpenJDK $VERSION 安装完成"
fi
echo ""

# 步骤 4: 获取 Java 安装路径
echo "🔍 步骤 4: 获取 Java 安装路径..."
JAVA_HOME_PATH=$(/usr/libexec/java_home -v "$VERSION")
echo "✅ JAVA_HOME: $JAVA_HOME_PATH"
echo ""

# 步骤 5: 切换环境变量（当前会话）
echo "🔄 步骤 5: 切换环境变量（当前会话）..."
export JAVA_HOME="$JAVA_HOME_PATH"
export PATH="$JAVA_HOME/bin:$PATH"
echo "✅ 当前会话环境变量已设置"
echo ""

# 步骤 6: 持久化配置
echo "💾 步骤 6: 持久化配置到 ~/.zshrc..."
ZSHRC_ENTRY="# Java $VERSION configuration (added by java-switch on $(date '+%Y-%m-%d %H:%M:%S'))"

# 检查是否已存在 Java 配置
if grep -q "export JAVA_HOME=\$(/usr/libexec/java_home" ~/.zshrc 2>/dev/null; then
    echo "⚠️  检测到 ~/.zshrc 中已有 JAVA_HOME 配置"
    echo "   备份原配置并更新..."
    cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d%H%M%S)
    # 注释掉旧的 JAVA_HOME 配置
    sed -i '' 's/^export JAVA_HOME=\$(\/usr\/libexec\/java_home/# &/' ~/.zshrc 2>/dev/null || true
fi

# 添加新配置
echo "" >> ~/.zshrc
echo "$ZSHRC_ENTRY" >> ~/.zshrc
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v '"$VERSION"')' >> ~/.zshrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.zshrc
echo "✅ 配置已添加到 ~/.zshrc"
echo ""

# 使配置生效
echo "🔄 使配置生效..."
source ~/.zshrc
echo "✅ ~/.zshrc 已重新加载"
echo ""

# 步骤 7: 验证
echo "=========================="
echo "✅ 验证安装"
echo "=========================="
echo ""
echo "📌 Java 版本:"
java -version
echo ""
echo "📌 JAVA_HOME:"
echo $JAVA_HOME
echo ""
echo "=========================="
echo "🎉 切换完成!"
echo "=========================="
echo ""
echo "💡 提示:"
echo "   - 当前切换已永久生效（~/.zshrc 已更新）"
echo "   - 新打开的终端窗口将自动使用 Java $VERSION"
echo "   - 如需切换其他版本，运行：./switch-java.sh <version>"
echo ""
