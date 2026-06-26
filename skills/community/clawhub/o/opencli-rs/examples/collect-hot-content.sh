#!/bin/bash
# 收集热门内容示例脚本
# 从多个平台收集热门内容并保存为结构化数据

set -e

# 配置
DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./collected_data/$DATE"
FORMAT="json"  # 可选: json, yaml, csv, md

echo "🚀 开始收集热门内容..."
echo "📅 时间: $(date)"
echo "📂 输出目录: $OUTPUT_DIR"
echo "📊 输出格式: $FORMAT"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 函数：收集数据并保存
collect_data() {
    local platform=$1
    local command=$2
    local filename=$3
    local options=$4
    
    echo "📡 收集 $platform 数据..."
    
    if opencli $command $options -f $FORMAT > "$OUTPUT_DIR/$filename" 2>/dev/null; then
        local size=$(wc -c < "$OUTPUT_DIR/$filename")
        if [ $size -gt 10 ]; then
            echo "✅ $platform 数据收集成功 ($size bytes)"
        else
            echo "⚠️  $platform 返回数据过小，可能未登录或连接问题"
            rm -f "$OUTPUT_DIR/$filename"
        fi
    else
        echo "❌ $platform 数据收集失败"
    fi
}

# 收集公开数据（无需登录）
collect_data "HackerNews" "hackernews top --limit 20" "hackernews_top.json" "--limit 20"
collect_data "GitHub Trending" "github trending --limit 15" "github_trending.json" "--limit 15"
collect_data "arXiv AI论文" "arxiv search --query 'artificial intelligence' --limit 10" "arxiv_ai.json" "--query 'artificial intelligence' --limit 10"

# 收集需要浏览器登录的数据（根据实际情况启用）
echo ""
echo "🔐 以下功能需要 Chrome 登录对应网站"
echo "   请确保已安装 Chrome 扩展并登录相应网站"

# 取消注释以下行以启用需要登录的功能
# collect_data "B站热门" "bilibili hot --limit 15" "bilibili_hot.json" "--limit 15"
# collect_data "知乎热榜" "zhihu hot" "zhihu_hot.json" ""
# collect_data "微博热搜" "weibo hot" "weibo_hot.json" ""
# collect_data "小红书推荐" "xiaohongshu feed --limit 10" "xiaohongshu_feed.json" "--limit 10"

# 生成汇总报告
echo ""
echo "📈 生成数据汇总报告..."

cat > "$OUTPUT_DIR/SUMMARY.md" << EOF
# 热门内容收集报告

**收集时间**: $(date)  
**数据目录**: $OUTPUT_DIR  
**输出格式**: $FORMAT  

## 收集的平台数据

EOF

# 列出收集的文件
for file in "$OUTPUT_DIR"/*.json; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        platform=$(echo "$filename" | cut -d'_' -f1)
        size=$(wc -c < "$file")
        count=$(jq length "$file" 2>/dev/null || echo "?")
        echo "- **$platform**: $filename (大小: ${size} bytes, 条目数: $count)" >> "$OUTPUT_DIR/SUMMARY.md"
    fi
done

# 添加使用说明
cat >> "$OUTPUT_DIR/SUMMARY.md" << 'EOF'

## 数据使用示例

### 使用 jq 处理 JSON 数据
```bash
# 查看 HackerNews 标题
jq -r '.[].title' hackernews_top.json

# 查看 GitHub Trending 仓库
jq -r '.[] | "\(.full_name): \(.star_count) stars"' github_trending.json
```

### 转换为其他格式
```bash
# JSON 转 CSV
opencli hackernews top --limit 10 -f csv > hackernews.csv

# JSON 转 YAML
opencli github trending --limit 5 -f yaml > github.yaml
```

## 故障排除

1. **空数据或错误**：确保 Chrome 扩展已安装且目标网站已登录
2. **连接问题**：运行 `opencli doctor` 诊断
3. **权限问题**：检查 Chrome 扩展权限设置

## 定时收集

可以设置定时任务自动收集：
```bash
# 每天上午9点收集
0 9 * * * /path/to/this/script.sh
```

---

*数据收集脚本由 OpenCLI 技能包提供*
EOF

echo "📊 数据收集完成！"
echo ""
echo "📁 输出文件:"
ls -la "$OUTPUT_DIR"/*.json 2>/dev/null || echo "   (暂无数据文件)"
echo ""
echo "📄 汇总报告: $OUTPUT_DIR/SUMMARY.md"
echo ""
echo "🔧 调试信息:"
opencli --version 2>/dev/null || echo "   OpenCLI 未安装"
echo ""
echo "💡 提示:"
echo "- 启用需要登录的功能请取消脚本中相应的注释"
echo "- 安装 yt-dlp 以支持视频下载: pip install yt-dlp"
echo "- 查看完整文档: opencli --help"