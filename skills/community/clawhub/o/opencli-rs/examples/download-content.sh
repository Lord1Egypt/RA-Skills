#!/bin/bash
# 内容下载示例脚本
# 演示如何使用 OpenCLI 下载各种内容

set -e

echo "🚀 内容下载示例"
echo "📥 演示图片、视频、文章下载功能"

# 配置
OUTPUT_BASE="./downloads"
DATE=$(date +%Y%m%d)
OUTPUT_DIR="$OUTPUT_BASE/$DATE"

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

echo "📂 下载目录: $(pwd)"

# 检查 yt-dlp（视频下载需要）
echo "🔍 检查依赖..."
if command -v yt-dlp &> /dev/null; then
    YTDLP_VERSION=$(yt-dlp --version)
    echo "✅ yt-dlp 已安装: $YTDLP_VERSION"
else
    echo "⚠️  yt-dlp 未安装，视频下载功能受限"
    echo "   安装命令: pip install yt-dlp"
    echo "   或 brew install yt-dlp"
fi

echo ""
echo "📋 下载选项:"
echo "1. 小红书笔记下载（图片/视频）"
echo "2. B站视频下载（需要 yt-dlp）"
echo "3. 知乎文章导出（Markdown）"
echo "4. Twitter 媒体下载"
echo "5. 微信公众号文章导出"
echo ""
read -p "🔢 请选择下载类型 (1-5，按回车跳过): " choice

case $choice in
    1)
        echo ""
        echo "📸 小红书笔记下载"
        echo "需要: 小红书登录 + 笔记ID"
        read -p "📝 输入小红书笔记ID (如 abc123): " note_id
        if [ -n "$note_id" ]; then
            mkdir -p xiaohongshu
            echo "⏬ 下载小红书笔记: $note_id"
            opencli xiaohongshu download "$note_id" --output "./xiaohongshu/$note_id" || {
                echo "❌ 下载失败，请检查:"
                echo "   1. Chrome 是否登录小红书"
                echo "   2. 笔记ID是否正确"
                echo "   3. 网络连接"
            }
        fi
        ;;
    
    2)
        echo ""
        echo "🎬 B站视频下载"
        if ! command -v yt-dlp &> /dev/null; then
            echo "❌ 需要先安装 yt-dlp"
            echo "   运行: pip install yt-dlp"
            exit 1
        fi
        
        read -p "📺 输入B站视频BV号 (如 BV1xxx): " bv_id
        if [ -n "$bv_id" ]; then
            mkdir -p bilibili
            echo "⏬ 下载B站视频: $bv_id"
            opencli bilibili download "$bv_id" --quality 1080p --output "./bilibili/$bv_id" || {
                echo "❌ 下载失败，可能原因:"
                echo "   1. 需要大会员的高清视频"
                echo "   2. 视频不可用"
                echo "   3. yt-dlp 配置问题"
            }
        fi
        ;;
    
    3)
        echo ""
        echo "📝 知乎文章导出"
        read -p "🔗 输入知乎文章URL: " zhihu_url
        if [ -n "$zhihu_url" ]; then
            mkdir -p zhihu
            echo "⏬ 导出知乎文章..."
            opencli zhihu download "$zhihu_url" --download-images --output "./zhihu" || {
                echo "❌ 导出失败，请检查:"
                echo "   1. URL 是否正确"
                echo "   2. 文章是否公开"
                echo "   3. 网络连接"
            }
        fi
        ;;
    
    4)
        echo ""
        echo "🐦 Twitter 媒体下载"
        read -p "👤 输入 Twitter 用户名 (如 elonmusk): " twitter_user
        if [ -n "$twitter_user" ]; then
            mkdir -p twitter
            read -p "📊 下载数量 (默认10): " limit
            limit=${limit:-10}
            echo "⏬ 下载 Twitter 用户媒体: @$twitter_user"
            opencli twitter download "$twitter_user" --limit "$limit" --output "./twitter/$twitter_user" || {
                echo "❌ 下载失败，请检查:"
                echo "   1. Chrome 是否登录 Twitter"
                echo "   2. 用户名是否正确"
                echo "   3. 用户是否有公开媒体"
            }
        fi
        ;;
    
    5)
        echo ""
        echo "📱 微信公众号文章导出"
        read -p "🔗 输入微信公众号文章URL: " weixin_url
        if [ -n "$weixin_url" ]; then
            mkdir -p weixin
            echo "⏬ 导出微信公众号文章..."
            opencli weixin download --url "$weixin_url" --output "./weixin" || {
                echo "❌ 导出失败，请检查:"
                echo "   1. URL 是否正确"
                echo "   2. 文章是否可访问"
                echo "   3. 需要微信登录"
            }
        fi
        ;;
    
    *)
        echo ""
        echo "📋 显示下载功能示例"
        ;;
esac

echo ""
echo "📁 当前下载目录内容:"
find . -type f -name "*.jpg" -o -name "*.png" -o -name "*.mp4" -o -name "*.md" 2>/dev/null | head -10

echo ""
echo "🔧 常用下载命令参考:"

cat > download_commands.txt << 'EOF'
# 小红书笔记下载
opencli xiaohongshu download <note_id> --output ./xhs

# B站视频下载 (需要 yt-dlp)
opencli bilibili download <BV号> --quality 1080p --output ./bilibili

# 知乎文章导出
opencli zhihu download <文章URL> --download-images --output ./zhihu

# Twitter 媒体下载
opencli twitter download <用户名> --limit 20 --output ./twitter

# 单条推文媒体下载
opencli twitter download --tweet-url "https://x.com/user/status/123" --output ./twitter

# 微信公众号文章导出
opencli weixin download --url <文章URL> --output ./weixin

# 批量下载示例
for note_id in abc123 def456 ghi789; do
    opencli xiaohongshu download "$note_id" --output "./batch_downloads/$note_id"
done
EOF

echo "📄 完整命令参考已保存到: download_commands.txt"

echo ""
echo "💡 使用提示:"
echo "1. 确保 Chrome 已登录目标网站"
echo "2. 视频下载需要安装 yt-dlp"
echo "3. 大量下载时注意频率限制"
echo "4. 尊重版权和平台规则"

echo ""
echo "🛠️  故障排除:"
echo "❌ 下载失败？尝试:"
echo "   1. 运行 opencli doctor 检查连接"
echo "   2. 手动在 Chrome 中访问目标网站"
echo "   3. 检查网络代理设置"
echo "   4. 查看扩展日志: curl localhost:19825/logs"

echo ""
echo "🎉 下载功能演示完成！"
echo "📂 文件保存在: $(pwd)"
echo ""
echo "🚀 进阶用法:"
echo "   1. 结合 cron 定时下载"
echo "   2. 批量处理下载队列"
echo "   3. 自动重命名和组织文件"
echo "   4. 与 AI 处理管道结合"