---
name: auto-researcher
description: |
  AI 研究助手 - 自动跨平台研究任何主题并生成结构化报告。
  支持平台：X/Twitter、Reddit、YouTube、GitHub、Hacker News、Product Hunt、新闻网站。
  触发词："研究"、"调研"、"分析"、"收集信息"、"auto research"、"research this"。
  自动输出：市场趋势、竞争分析、技术调研、用户反馈汇总。
author: anyafu
license: MIT
copyright: Copyright © 2026 anyafu. All rights reserved.
---

# Auto Researcher - AI 研究助手

自动跨平台研究任何主题，生成结构化洞察报告。

## 核心能力

### 支持平台

| 平台 | 用途 | 工具 |
|------|------|------|
| X/Twitter | 实时讨论、行业趋势 | xreach CLI |
| Reddit | 深度讨论、用户反馈 | Reddit API |
| YouTube | 视频教程、产品演示 | yt-dlp |
| GitHub | 技术实现、开源项目 | gh CLI |
| Hacker News | 技术趋势、创业动态 | web_fetch |
| Product Hunt | 新产品、市场验证 | web_fetch |
| 新闻网站 | 行业动态、媒体报道 | web_fetch |

## 使用方法

### 基础用法

```bash
# 研究任何主题
auto-research search "主题名称"

# 指定平台
auto-research search "主题" --platforms twitter,reddit,github

# 输出报告
auto-research report "主题" --format markdown
```

### 详细命令

#### 1. 快速研究（5 分钟）

```bash
# 搜索 X/Twitter 讨论
xreach search "关键词" --json -n 20 > /tmp/twitter_results.json

# 搜索 Reddit 讨论
curl -s "https://www.reddit.com/search.json?q=关键词&limit=20" > /tmp/reddit_results.json

# 搜索 GitHub 项目
gh search repos "关键词" --sort stars --limit 20 > /tmp/github_results.json

# 搜索 Hacker News
curl -s "https://hn.algolia.com/api/v1/search?query=关键词" > /tmp/hn_results.json
```

#### 2. 深度研究（30 分钟）

```bash
# 多平台并行研究
auto-research deep "主题" --platforms all --timeout 1800

# 生成竞争分析报告
auto-research competitors "产品名称" --output competitors.md

# 生成市场趋势报告
auto-research trends "行业名称" --output trends.md
```

#### 3. 输出报告

```bash
# 生成 Markdown 报告
auto-research report --input /tmp/research_results.json --output report.md

# 生成 JSON 数据
auto-research report --input /tmp/research_results.json --output data.json --format json

# 生成演示文稿大纲
auto-research report --input /tmp/research_results.json --output presentation.md --template slides
```

## 报告模板

### 标准研究报告结构

```markdown
# [主题] 研究报告

## 执行摘要
- 核心发现（3-5 点）
- 关键数据
- 行动建议

## 市场概况
- 市场规模
- 增长趋势
- 主要参与者

## 用户反馈
- 正面评价
- 负面评价
- 常见需求

## 竞争分析
- 主要竞争对手
- 差异化机会
- 市场空白

## 技术趋势
- 主流技术方案
- 新兴技术
- 技术难点

## 结论与建议
- 进入策略
- 风险点
- 下一步行动
```

## 脚本示例

### research.sh - 快速研究脚本

```bash
#!/bin/bash
# 用法：./research.sh "关键词"

TOPIC="$1"
OUTPUT_DIR="/tmp/research_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "🔍 开始研究：$TOPIC"
echo "📁 输出目录：$OUTPUT_DIR"

# 1. X/Twitter 搜索
echo "📱 搜索 X/Twitter..."
xreach search "$TOPIC" --json -n 20 > "$OUTPUT_DIR/twitter.json"

# 2. Reddit 搜索
echo "💬 搜索 Reddit..."
curl -s "https://www.reddit.com/search.json?q=$TOPIC&limit=20" \
  -H "User-Agent: auto-researcher/1.0" > "$OUTPUT_DIR/reddit.json"

# 3. GitHub 搜索
echo "💻 搜索 GitHub..."
gh search repos "$TOPIC" --sort stars --limit 20 > "$OUTPUT_DIR/github.json"

# 4. Hacker News 搜索
echo "📰 搜索 Hacker News..."
curl -s "https://hn.algolia.com/api/v1/search?query=$TOPIC" > "$OUTPUT_DIR/hn.json"

# 5. 生成报告
echo "📊 生成报告..."
python3 scripts/generate_report.py "$OUTPUT_DIR" "$TOPIC"

echo "✅ 研究完成！报告：$OUTPUT_DIR/report.md"
```

### generate_report.py - 报告生成脚本

```python
#!/usr/bin/env python3
"""
从研究数据生成结构化报告
"""
import json
import sys
from datetime import datetime

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return []

def extract_twitter(data):
    """提取 Twitter 关键信息"""
    results = []
    for item in data.get('results', [])[:10]:
        results.append({
            'text': item.get('text', ''),
            'user': item.get('user', {}).get('screen_name', ''),
            'likes': item.get('favorite_count', 0),
            'retweets': item.get('retweet_count', 0)
        })
    return results

def extract_reddit(data):
    """提取 Reddit 关键信息"""
    results = []
    posts = data.get('data', {}).get('children', [])
    for post in posts[:10]:
        d = post.get('data', {})
        results.append({
            'title': d.get('title', ''),
            'author': d.get('author', ''),
            'score': d.get('score', 0),
            'comments': d.get('num_comments', 0),
            'url': d.get('url', '')
        })
    return results

def extract_github(data):
    """提取 GitHub 关键信息"""
    results = []
    for item in data[:10]:
        results.append({
            'name': item.get('full_name', ''),
            'description': item.get('description', ''),
            'stars': item.get('stargazers_count', 0),
            'language': item.get('language', ''),
            'url': item.get('html_url', '')
        })
    return results

def generate_report(output_dir, topic):
    """生成 Markdown 报告"""
    # 加载数据
    twitter = load_json(f"{output_dir}/twitter.json")
    reddit = load_json(f"{output_dir}/reddit.json")
    github = load_json(f"{output_dir}/github.json")
    hn = load_json(f"{output_dir}/hn.json")
    
    # 提取信息
    tw_data = extract_twitter(twitter)
    rd_data = extract_reddit(reddit)
    gh_data = extract_github(github)
    
    # 生成报告
    report = f"""# {topic} 研究报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 执行摘要

基于 X/Twitter、Reddit、GitHub、Hacker News 等平台的实时数据分析。

## X/Twitter 讨论热点

"""
    
    for i, item in enumerate(tw_data[:5], 1):
        report += f"{i}. **@{item['user']}** ({item['likes']} likes): {item['text'][:100]}...\n\n"
    
    report += """## Reddit 讨论

"""
    
    for i, item in enumerate(rd_data[:5], 1):
        report += f"{i}. **{item['title']}** (Score: {item['score']}, Comments: {item['comments']})\n\n"
    
    report += """## GitHub 相关项目

| 项目 | Stars | 语言 |
|------|-------|------|
"""
    
    for item in gh_data[:5]:
        report += f"| [{item['name']}]({item['url']}) | {item['stars']} | {item['language']} |\n"
    
    report += f"""
## 结论与建议

基于以上数据，建议关注以下方向：
1. [根据数据填写]
2. [根据数据填写]
3. [根据数据填写]

---
*报告由 Auto Researcher 自动生成*
"""
    
    with open(f"{output_dir}/report.md", 'w') as f:
        f.write(report)
    
    print(f"报告已生成：{output_dir}/report.md")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 generate_report.py <output_dir> <topic>")
        sys.exit(1)
    
    generate_report(sys.argv[1], sys.argv[2])
```

## 使用场景

### 1. 市场调研

```bash
# 研究某个市场/行业
auto-research search "AI 写作工具 市场" --platforms all
```

### 2. 竞品分析

```bash
# 研究竞争对手
auto-research competitors "Notion AI" --output notion-ai-analysis.md
```

### 3. 技术选型

```bash
# 研究技术方案
auto-research search "Python 向量数据库 对比" --platforms github,reddit,hn
```

### 4. 用户反馈收集

```bash
# 收集用户对某产品的评价
auto-research feedback "产品名" --platforms twitter,reddit
```

### 5. 趋势分析

```bash
# 分析行业趋势
auto-research trends "AI Agent" --timeframe 30d
```

## 定价策略

### 免费层
- 每日 3 次快速研究
- 基础报告模板
- 支持 3 个平台

### 付费层（¥99/月）
- 无限次研究
- 高级报告模板
- 支持所有平台
- 导出 PDF/PPT
- API 访问

### 企业层（¥999/月）
- 定制报告模板
- 私有化部署
- 专属支持
- SLA 保障

## 变现路径

1. **ClawHub 技能销售** - 一次性购买或订阅
2. **SaaS 服务** - 网页版 + API
3. **定制报告** - 人工深度研究服务
4. **培训课程** - 教别人做市场研究

## 下一步

1. [ ] 完成脚本开发
2. [ ] 测试各平台搜索
3. [ ] 优化报告模板
4. [ ] 发布到 ClawHub
5. [ ] 制作演示视频
6. [ ] 上线 Product Hunt

---

## 📜 License

**Copyright © 2026 anyafu. All rights reserved.**

Licensed under the MIT License.

### MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### 商业使用

- ✅ 允许个人和商业使用
- ✅ 允许修改和分发
- ✅ 允许私有化部署
- ⚠️ 如需闭源商业授权，请联系作者 anyafu
