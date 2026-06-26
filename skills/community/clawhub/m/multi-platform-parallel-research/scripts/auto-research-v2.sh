# Auto Researcher - 增强版研究脚本

#!/bin/bash
# 用法：./auto-research-v2.sh "研究主题"
# 支持：web_fetch + jina.ai 作为备用数据源

set -e

TOPIC="$1"
if [ -z "$TOPIC" ]; then
    echo "❌ 用法：./auto-research-v2.sh \"研究主题\""
    exit 1
fi

OUTPUT_DIR="/tmp/research_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "🔍 开始研究：$TOPIC"
echo "📁 输出目录：$OUTPUT_DIR"
echo ""

# 使用 Python 进行数据收集（更可靠）
python3 << PYTHON_SCRIPT
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime

topic = "$TOPIC"
output_dir = "$OUTPUT_DIR"

def fetch_json(url, headers={}):
    """获取 JSON 数据"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"   ⚠️  {url}: {str(e)[:50]}")
        return {}

def fetch_text(url, headers={}):
    """获取文本数据"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode()
    except Exception as e:
        return ""

def search_hackernews(query):
    """搜索 Hacker News"""
    url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(query)}&tags=story&limit=20"
    return fetch_json(url)

def search_github(query):
    """搜索 GitHub (使用 Jina AI 代理)"""
    url = f"https://r.jina.ai/https://github.com/search?q={urllib.parse.quote(query)}&type=repositories"
    return fetch_text(url)

def search_producthunt(query):
    """搜索 Product Hunt (使用 Jina AI 代理)"""
    url = f"https://r.jina.ai/https://www.producthunt.com/search?q={urllib.parse.quote(query)}"
    return fetch_text(url)

def search_twitter_jina(query):
    """通过 Jina AI 搜索 Twitter"""
    url = f"https://r.jina.ai/https://x.com/search?q={urllib.parse.quote(query)}"
    return fetch_text(url)

def search_web(query):
    """通用网页搜索 (DuckDuckGo via Jina)"""
    url = f"https://r.jina.ai/https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    return fetch_text(url)

print("📊 开始多平台数据收集...")
print("")

# 1. Hacker News
print("📰 搜索 Hacker News...")
hn_data = search_hackernews(topic)
with open(f"{output_dir}/hackernews.json", 'w') as f:
    json.dump(hn_data, f, indent=2)
hn_hits = hn_data.get('hits', [])
print(f"   ✅ 找到 {len(hn_hits)} 条结果")

# 2. GitHub
print("💻 搜索 GitHub...")
github_data = search_github(topic)
with open(f"{output_dir}/github_raw.txt", 'w') as f:
    f.write(github_data)
print(f"   ✅ 获取到 {len(github_data)} 字节数据")

# 3. Product Hunt
print("🚀 搜索 Product Hunt...")
ph_data = search_producthunt(topic)
with open(f"{output_dir}/producthunt_raw.txt", 'w') as f:
    f.write(ph_data)
print(f"   ✅ 获取到 {len(ph_data)} 字节数据")

# 4. Twitter/X
print("📱 搜索 Twitter/X...")
twitter_data = search_twitter_jina(topic)
with open(f"{output_dir}/twitter_raw.txt", 'w') as f:
    f.write(twitter_data)
print(f"   ✅ 获取到 {len(twitter_data)} 字节数据")

# 5. 通用网页搜索
print("🌐 网页搜索...")
web_data = search_web(f"{topic} 2025 2026")
with open(f"{output_dir}/web_search_raw.txt", 'w') as f:
    f.write(web_data)
print(f"   ✅ 获取到 {len(web_data)} 字节数据")

print("")
print("✅ 数据收集完成！")
PYTHON_SCRIPT

# 生成增强版报告
echo ""
echo "📊 生成增强版研究报告..."

python3 << PYTHON_SCRIPT
import json
import os
import re
from datetime import datetime
import sys

output_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/research"
topic = sys.argv[2] if len(sys.argv) > 2 else "research"
PYTHON_SCRIPT

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

def load_text(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return ""

def extract_hn_stories(data, limit=10):
    """提取 HN 故事"""
    stories = []
    for hit in data.get('hits', [])[:limit]:
        stories.append({
            'title': hit.get('title', ''),
            'author': hit.get('author', ''),
            'points': hit.get('points', 0),
            'comments': hit.get('num_comments', 0),
            'url': hit.get('url', ''),
            'created': hit.get('created_at', '')[:10] if hit.get('created_at') else ''
        })
    return stories

def extract_github_repos(text):
    """从 GitHub 原始文本提取仓库信息"""
    repos = []
    # 简单提取包含 star 信息的行
    lines = text.split('\n')
    for line in lines[:20]:
        if 'star' in line.lower() or 'fork' in line.lower():
            repos.append(line.strip())
    return repos[:10]

def extract_ph_products(text):
    """从 Product Hunt 文本提取产品"""
    products = []
    lines = text.split('\n')
    for line in lines[:20]:
        if len(line.strip()) > 20 and len(line.strip()) < 200:
            products.append(line.strip())
    return products[:10]

# 加载数据
hn_data = load_json(f"{output_dir}/hackernews.json")
github_text = load_text(f"{output_dir}/github_raw.txt")
ph_text = load_text(f"{output_dir}/producthunt_raw.txt")
twitter_text = load_text(f"{output_dir}/twitter_raw.txt")
web_text = load_text(f"{output_dir}/web_search_raw.txt")

# 提取信息
hn_stories = extract_hn_stories(hn_data)
github_repos = extract_github_repos(github_text)
ph_products = extract_ph_products(ph_text)

# 生成报告
report = f"""# 📊 {topic} 深度研究报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**数据来源**: Hacker News, GitHub, Product Hunt, Twitter/X, 网页搜索

---

## 🎯 执行摘要

### 数据概览
- **Hacker News**: {len(hn_stories)} 条讨论
- **GitHub**: {len(github_repos)} 个相关仓库
- **Product Hunt**: {len(ph_products)} 个相关产品
- **Twitter/X**: 已收集原始数据
- **网页搜索**: 已收集原始数据

### 热度评估
"""

# 热度评估
total_score = len(hn_stories) * 2 + len(github_repos) + len(ph_products) * 3
if total_score > 30:
   热度 = "🔥 非常高"
elif total_score > 15:
   热度 = "⭐ 高"
elif total_score > 5:
   热度 = "📈 中等"
else:
   热度 = "📊 待观察"

report += f"""
**综合热度**: {热度} (得分：{total_score})

**关键发现**:
1. [根据数据填写 - 主要趋势]
2. [根据数据填写 - 市场机会]
3. [根据数据填写 - 竞争格局]

---

## 📰 Hacker News 讨论

"""

for i, story in enumerate(hn_stories[:5], 1):
    report += f"""
### {i}. {story['title']}

- **作者**: {story['author']}
- **分数**: {story['points']} | **评论**: {story['comments']}
- **日期**: {story['created']}
- **链接**: {story['url']}

"""

report += """
---

## 💻 GitHub 相关项目

"""

if github_repos:
    for i, repo in enumerate(github_repos[:5], 1):
        report += f"{i}. {repo}\n\n"
else:
    report += "*数据提取中，建议手动访问 GitHub 搜索*\n\n"

report += """
---

## 🚀 Product Hunt 产品

"""

if ph_products:
    for i, product in enumerate(ph_products[:5], 1):
        report += f"{i}. {product}\n\n"
else:
    report += "*数据提取中，建议手动访问 Product Hunt*\n\n"

report += f"""
---

## 📈 市场洞察

### 趋势分析

1. **技术趋势**: [基于 HN 和 GitHub 数据分析]
2. **产品趋势**: [基于 Product Hunt 数据分析]
3. **用户关注点**: [基于讨论内容分析]

### 竞争格局

**主要玩家**:
- [从数据中识别]

**差异化机会**:
- [基于竞争分析]

### 市场机会

**高潜力方向**:
1. [机会点 1]
2. [机会点 2]
3. [机会点 3]

---

## 💡 行动建议

### 短期（1-2 周）
- [ ] 深入研究 Top 3 竞争对手
- [ ] 联系潜在用户获取反馈
- [ ] 验证 MVP 想法

### 中期（1-2 月）
- [ ] 开发最小可行产品
- [ ] 建立早期用户群
- [ ] 收集产品反馈

### 长期（3-6 月）
- [ ] 产品迭代优化
- [ ] 扩大用户规模
- [ ] 探索变现模式

---

## 📎 原始数据

所有原始数据已保存到：
- `{output_dir}/hackernews.json` - HN 数据
- `{output_dir}/github_raw.txt` - GitHub 搜索结果
- `{output_dir}/producthunt_raw.txt` - PH 搜索结果
- `{output_dir}/twitter_raw.txt` - Twitter 搜索结果
- `{output_dir}/web_search_raw.txt` - 网页搜索结果

---

*报告由 Auto Researcher v2 自动生成 | 数据截止时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

# 保存报告
with open(f"{output_dir}/report_enhanced.md", 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ 增强版报告已生成：{output_dir}/report_enhanced.md")

# 生成摘要
print("")
print("=" * 50)
print("📋 研究摘要")
print("=" * 50)
print(f"主题：{topic}")
print(f"HN 讨论：{len(hn_stories)} 条")
print(f"GitHub 项目：{len(github_repos)} 个")
print(f"PH 产品：{len(ph_products)} 个")
print(f"综合热度：{热度} ({total_score}分)")
print("=" * 50)
PYTHON_SCRIPT

echo ""
echo "================================"
echo "✅ 研究完成！"
echo "================================"
echo ""
echo "📄 增强版报告：$OUTPUT_DIR/report_enhanced.md"
echo "📊 原始数据目录：$OUTPUT_DIR/"
echo ""
