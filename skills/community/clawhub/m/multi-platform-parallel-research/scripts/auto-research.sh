#!/bin/bash
# Auto Researcher - 快速研究脚本
# 用法：./auto-research.sh "研究主题"

set -e

TOPIC="$1"
if [ -z "$TOPIC" ]; then
    echo "❌ 用法：./auto-research.sh \"研究主题\""
    echo "示例：./auto-research.sh \"AI 写作工具\""
    exit 1
fi

OUTPUT_DIR="/tmp/research_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "🔍 开始研究：$TOPIC"
echo "📁 输出目录：$OUTPUT_DIR"
echo ""

# 1. X/Twitter 搜索
echo "📱 搜索 X/Twitter..."
if command -v xreach &> /dev/null; then
    xreach search "$TOPIC" --json -n 20 > "$OUTPUT_DIR/twitter.json" 2>/dev/null || echo "⚠️  Twitter 搜索失败"
    echo "   ✅ Twitter 数据已保存"
else
    echo "   ⚠️  xreach 未安装，跳过 Twitter"
fi

# 2. Reddit 搜索
echo "💬 搜索 Reddit..."
curl -s "https://www.reddit.com/search.json?q=$TOPIC&limit=20" \
  -H "User-Agent: auto-researcher/1.0" > "$OUTPUT_DIR/reddit.json" 2>/dev/null || echo "⚠️  Reddit 搜索失败"
echo "   ✅ Reddit 数据已保存"

# 3. GitHub 搜索
echo "💻 搜索 GitHub..."
if command -v gh &> /dev/null; then
    gh search repos "$TOPIC" --sort stars --limit 20 > "$OUTPUT_DIR/github.json" 2>/dev/null || echo "⚠️  GitHub 搜索失败"
    echo "   ✅ GitHub 数据已保存"
else
    echo "   ⚠️  gh CLI 未安装，跳过 GitHub"
fi

# 4. Hacker News 搜索
echo "📰 搜索 Hacker News..."
curl -s "https://hn.algolia.com/api/v1/search?query=$TOPIC" > "$OUTPUT_DIR/hn.json" 2>/dev/null || echo "⚠️  HN 搜索失败"
echo "   ✅ Hacker News 数据已保存"

# 5. Product Hunt 搜索
echo "🚀 搜索 Product Hunt..."
curl -s "https://www.producthunt.com/search?q=$TOPIC" \
  -H "Accept: text/html" > "$OUTPUT_DIR/producthunt.html" 2>/dev/null || echo "⚠️  PH 搜索失败"
echo "   ✅ Product Hunt 数据已保存"

# 6. 生成报告
echo ""
echo "📊 生成研究报告..."

python3 << PYTHON_SCRIPT
import json
import os
from datetime import datetime

output_dir = "$OUTPUT_DIR"
topic = "$TOPIC"

def load_json(path, default=[]):
    try:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    except:
        pass
    return default

def extract_twitter(data):
    results = []
    if not isinstance(data, dict):
        return results
    for item in data.get('results', [])[:10]:
        if isinstance(item, dict):
            results.append({
                'text': item.get('text', '')[:200],
                'user': item.get('user', {}).get('screen_name', 'unknown'),
                'likes': item.get('favorite_count', 0),
                'retweets': item.get('retweet_count', 0)
            })
    return results

def extract_reddit(data):
    results = []
    if not isinstance(data, dict):
        return results
    posts = data.get('data', {}).get('children', [])
    for post in posts[:10]:
        if isinstance(post, dict):
            d = post.get('data', {})
            results.append({
                'title': d.get('title', ''),
                'author': d.get('author', 'deleted'),
                'score': d.get('score', 0),
                'comments': d.get('num_comments', 0),
                'url': d.get('url', '')
            })
    return results

def extract_github(data):
    results = []
    if isinstance(data, list):
        for item in data[:10]:
            results.append({
                'name': item.get('full_name', ''),
                'description': (item.get('description') or '')[:100],
                'stars': item.get('stargazers_count', 0),
                'language': item.get('language', ''),
                'url': item.get('html_url', '')
            })
    return results

def extract_hn(data):
    results = []
    if not isinstance(data, dict):
        return results
    for item in data.get('hits', [])[:10]:
        if isinstance(item, dict):
            results.append({
                'title': item.get('title', ''),
                'author': item.get('author', ''),
                'points': item.get('points', 0),
                'comments': item.get('num_comments', 0),
                'url': item.get('url', '')
            })
    return results

# 加载数据
twitter_data = load_json(f"{output_dir}/twitter.json")
reddit_data = load_json(f"{output_dir}/reddit.json")
github_data = load_json(f"{output_dir}/github.json")
hn_data = load_json(f"{output_dir}/hn.json")

# 提取信息
tw_items = extract_twitter(twitter_data)
rd_items = extract_reddit(reddit_data)
gh_items = extract_github(github_data)
hn_items = extract_hn(hn_data)

# 生成报告
report = f"""# 📊 {topic} 研究报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**研究范围**: X/Twitter, Reddit, GitHub, Hacker News

---

## 🎯 执行摘要

基于多个平台的实时数据，共收集：
- **X/Twitter**: {len(tw_items)} 条讨论
- **Reddit**: {len(rd_items)} 个帖子
- **GitHub**: {len(gh_items)} 个项目
- **Hacker News**: {len(hn_items)} 条新闻

### 核心发现

1. **热度趋势**: {'高' if len(tw_items) + len(rd_items) > 15 else '中' if len(tw_items) + len(rd_items) > 5 else '低'}
2. **主要讨论点**: [需要人工分析]
3. **市场机会**: [需要人工分析]

---

## 📱 X/Twitter 讨论热点

"""

for i, item in enumerate(tw_items[:5], 1):
    report += f"""
**{i}. @{item['user']}** ({item['likes']} ❤️, {item['retweets']} 🔄)

> {item['text']}

"""

report += """
---

## 💬 Reddit 讨论

"""

for i, item in enumerate(rd_items[:5], 1):
    report += f"""
**{i}. {item['title']}**

- 作者：u/{item['author']}
- 评分：{item['score']} | 评论：{item['comments']}
- 链接：{item['url']}

"""

report += """
---

## 💻 GitHub 相关项目

| # | 项目 | Stars | 语言 |
|---|------|-------|------|
"""

for i, item in enumerate(gh_items[:5], 1):
    report += f"| {i} | [{item['name']}]({item['url']}) | ⭐ {item['stars']} | {item['language']} |\n"

report += """
---

## 📰 Hacker News 讨论

"""

for i, item in enumerate(hn_items[:5], 1):
    report += f"""
**{i}. {item['title']}**

- 作者：{item['author']}
- 分数：{item['points']} | 评论：{item['comments']}
- 链接：{item['url']}

"""

report += f"""
---

## 📈 结论与建议

### 市场机会

基于以上数据，以下方向值得关注：

1. **[机会点 1]** - [说明]
2. **[机会点 2]** - [说明]
3. **[机会点 3]** - [说明]

### 风险提示

- [风险点 1]
- [风险点 2]

### 下一步行动

- [ ] 深入分析 [具体方向]
- [ ] 联系 [相关人群] 获取反馈
- [ ] 研究 [竞争对手] 的策略

---

*报告由 Auto Researcher 自动生成 | 数据截止时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

# 保存报告
with open(f"{output_dir}/report.md", 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ 报告已生成：{output_dir}/report.md")
PYTHON_SCRIPT

echo ""
echo "================================"
echo "✅ 研究完成！"
echo "================================"
echo ""
echo "📄 报告文件：$OUTPUT_DIR/report.md"
echo "📊 原始数据：$OUTPUT_DIR/"
echo ""
echo "查看报告：cat $OUTPUT_DIR/report.md"
echo ""
