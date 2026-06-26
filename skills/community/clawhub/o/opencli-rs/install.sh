#!/bin/bash
# OpenCLI 安装脚本

set -e

echo "🔧 开始安装 OpenCLI..."

# 检查 Node.js 版本
echo "📦 检查 Node.js 版本..."
NODE_VERSION=$(node --version | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

if [ $NODE_MAJOR -lt 20 ]; then
    echo "❌ Node.js 版本需要 >= 20.0.0，当前版本: $NODE_VERSION"
    echo "请先升级 Node.js: https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js 版本: $NODE_VERSION"

# 安装 OpenCLI
echo "📦 安装 OpenCLI..."
npm install -g @jackwener/opencli@latest

# 检查安装是否成功
if command -v opencli &> /dev/null; then
    OPENCLI_VERSION=$(opencli --version 2>/dev/null || echo "unknown")
    echo "✅ OpenCLI 安装成功，版本: $OPENCLI_VERSION"
else
    echo "❌ OpenCLI 安装失败"
    exit 1
fi

# 创建配置文件目录
echo "📁 创建配置文件目录..."
mkdir -p ~/.opencli

# 创建示例配置文件
echo "📄 创建示例配置文件..."
cat > ~/.opencli/config.yaml << 'EOF'
# OpenCLI 配置文件
# 参考: https://github.com/jackwener/opencli

# 浏览器配置
browser:
  # Chrome 数据目录（可选）
  # userDataDir: ~/Library/Application Support/Google/Chrome
  
  # 扩展已安装时保持连接
  keepAlive: true

# 输出配置
output:
  defaultFormat: json  # table, json, yaml, md, csv
  prettyPrint: true
  
# 下载配置
download:
  defaultOutputDir: ./downloads
  maxConcurrent: 3

# 插件配置
plugins:
  autoUpdate: true
  installDir: ~/.opencli/plugins
EOF

echo "✅ 配置文件创建完成: ~/.opencli/config.yaml"

# 安装 yt-dlp（用于视频下载）
echo "📥 检查 yt-dlp..."
if ! command -v yt-dlp &> /dev/null; then
    echo "⚠️  yt-dlp 未安装，视频下载功能将受限"
    echo "   可以通过以下方式安装:"
    echo "   pip install yt-dlp"
    echo "   或 brew install yt-dlp"
else
    YTDLP_VERSION=$(yt-dlp --version)
    echo "✅ yt-dlp 已安装，版本: $YTDLP_VERSION"
fi

# 创建示例脚本目录
echo "📁 创建示例脚本目录..."
mkdir -p ~/.opencli/examples

# 创建基本使用示例
cat > ~/.opencli/examples/basic-usage.sh << 'EOF'
#!/bin/bash
# OpenCLI 基本使用示例

echo "🚀 OpenCLI 基本使用示例"

# 1. 查看所有命令
echo "📋 查看所有可用命令:"
opencli list | head -20

# 2. 查看特定平台命令
echo "🔍 查看 B站命令:"
opencli list | grep bilibili

# 3. 获取热门内容（无需登录）
echo "🔥 获取 HackerNews 头条:"
opencli hackernews top --limit 5 -f table

# 4. 检查连接状态
echo "🔌 检查连接状态:"
opencli doctor || true

echo "✅ 示例完成！"
EOF

chmod +x ~/.opencli/examples/basic-usage.sh

# 创建数据收集示例
cat > ~/.opencli/examples/collect-data.sh << 'EOF'
#!/bin/bash
# 数据收集示例脚本

DATE=$(date +%Y%m%d)
OUTPUT_DIR="./data/$DATE"
mkdir -p "$OUTPUT_DIR"

echo "📊 开始收集数据到: $OUTPUT_DIR"

# 收集公开数据（无需登录）
echo "📰 收集 HackerNews 头条..."
opencli hackernews top --limit 30 -f json > "$OUTPUT_DIR/hackernews.json"

echo "📰 收集 GitHub Trending..."
opencli github trending --limit 20 -f json > "$OUTPUT_DIR/github-trending.json"

echo "📰 收集 arXiv 最新论文..."
opencli arxiv search --query "artificial intelligence" --limit 10 -f json > "$OUTPUT_DIR/arxiv-ai.json"

# 如果需要浏览器登录，可以取消注释以下行
# echo "📺 收集 B站热门..."
# opencli bilibili hot --limit 20 -f json > "$OUTPUT_DIR/bilibili.json"

# echo "📝 收集知乎热榜..."
# opencli zhihu hot -f json > "$OUTPUT_DIR/zhihu.json"

echo "✅ 数据收集完成！"
echo "数据保存在: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR"/*.json
EOF

chmod +x ~/.opencli/examples/collect-data.sh

echo ""
echo "🎉 OpenCLI 安装完成！"
echo ""
echo "📖 下一步:"
echo "1. 安装 Chrome 扩展:"
echo "   访问 https://github.com/jackwener/opencli/releases"
echo "   下载 opencli-extension.zip 并加载到 Chrome"
echo ""
echo "2. 测试安装:"
echo "   opencli doctor"
echo "   opencli list"
echo ""
echo "3. 运行示例:"
echo "   bash ~/.opencli/examples/basic-usage.sh"
echo "   bash ~/.opencli/examples/collect-data.sh"
echo ""
echo "4. 查看完整文档:"
echo "   opencli --help"
echo "   或访问 https://github.com/jackwener/opencli"
echo ""
echo "📂 配置文件: ~/.opencli/config.yaml"
echo "📁 示例脚本: ~/.opencli/examples/"