#!/usr/bin/env python3
"""
Auto Researcher v2.0 - 智能研究助手
用法：python3 auto-researcher.py "研究主题" [选项]

Copyright © 2026 anyafu. All rights reserved.
Licensed under MIT License.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path
import time

# 配置
CONFIG = {
    'timeout': 30,
    'max_results': 20,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'output_dir': '/tmp/auto-researcher',
    'jina_api': 'https://r.jina.ai/',
    'exa_api': None,  # 可配置
}

class Color:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log(msg, level='info'):
    """日志输出"""
    colors = {
        'info': Color.CYAN,
        'success': Color.GREEN,
        'warning': Color.YELLOW,
        'error': Color.RED,
    }
    color = colors.get(level, '')
    print(f"{color}{msg}{Color.ENDC}")

def fetch_json(url, headers=None, timeout=None):
    """获取 JSON 数据"""
    if headers is None:
        headers = {}
    if timeout is None:
        timeout = CONFIG['timeout']
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        log(f"  HTTP 错误 {e.code}: {e.reason}", 'error')
        return None
    except Exception as e:
        log(f"  请求失败：{str(e)[:80]}", 'error')
        return None

def fetch_text(url, headers=None, timeout=None):
    """获取文本数据"""
    if headers is None:
        headers = {'User-Agent': CONFIG['user_agent']}
    if timeout is None:
        timeout = CONFIG['timeout']
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode()
    except Exception as e:
        return ""

def search_hackernews(query, limit=20):
    """搜索 Hacker News"""
    log("📰 搜索 Hacker News...", 'info')
    encoded = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=story&limit={limit}"
    
    data = fetch_json(url)
    if data and 'hits' in data:
        log(f"   ✅ 找到 {len(data['hits'])} 条结果", 'success')
        return data['hits']
    return []

def search_github_via_jina(query):
    """通过 Jina AI 搜索 GitHub"""
    log("💻 搜索 GitHub...", 'info')
    encoded = urllib.parse.quote(query)
    url = f"{CONFIG['jina_api']}https://github.com/search?q={encoded}&type=repositories"
    
    text = fetch_text(url)
    if text:
        log(f"   ✅ 获取到 {len(text)} 字节数据", 'success')
        return parse_github_text(text)
    return []

def parse_github_text(text):
    """解析 GitHub 搜索结果"""
    repos = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if 'href=' in line and '/github.com/' in line:
            # 提取仓库名
            for part in line.split():
                if '/' in part and len(part.split('/')[0]) > 1:
                    repos.append({'raw': line.strip()})
                    if len(repos) >= 10:
                        break
        if len(repos) >= 10:
            break
    
    return repos

def search_producthunt_via_jina(query):
    """通过 Jina AI 搜索 Product Hunt"""
    log("🚀 搜索 Product Hunt...", 'info')
    encoded = urllib.parse.quote(query)
    url = f"{CONFIG['jina_api']}https://www.producthunt.com/search?q={encoded}"
    
    text = fetch_text(url)
    if text:
        log(f"   ✅ 获取到 {len(text)} 字节数据", 'success')
        return parse_ph_text(text)
    return []

def parse_ph_text(text):
    """解析 Product Hunt 搜索结果"""
    products = []
    lines = text.split('\n')
    
    for line in lines[:30]:
        line = line.strip()
        if line and len(line) > 20 and len(line) < 200:
            if not line.startswith('http') and not line.startswith('<'):
                products.append({'name': line})
    
    return products[:10]

def search_duckduckgo(query, limit=20):
    """DuckDuckGo 搜索"""
    log("🌐 网页搜索...", 'info')
    encoded = urllib.parse.quote(f"{query} 2025 2026")
    url = f"{CONFIG['jina_api']}https://duckduckgo.com/html/?q={encoded}"
    
    text = fetch_text(url)
    if text:
        log(f"   ✅ 获取到 {len(text)} 字节数据", 'success')
        return parse_ddg_text(text)
    return []

def parse_ddg_text(text):
    """解析 DuckDuckGo 搜索结果"""
    results = []
    lines = text.split('\n')
    
    for line in lines:
        if 'href=' in line and ('http' in line):
            results.append({'snippet': line.strip()[:200]})
            if len(results) >= 15:
                break
    
    return results

def search_twitter_via_jina(query):
    """通过 Jina AI 搜索 Twitter"""
    log("📱 搜索 Twitter/X...", 'info')
    encoded = urllib.parse.quote(query)
    url = f"{CONFIG['jina_api']}https://x.com/search?q={encoded}&f=live"
    
    text = fetch_text(url)
    if text:
        log(f"   ✅ 获取到 {len(text)} 字节数据", 'success')
        return parse_twitter_text(text)
    return []

def parse_twitter_text(text):
    """解析 Twitter 搜索结果"""
    tweets = []
    lines = text.split('\n')
    
    for line in lines[:50]:
        if len(line.strip()) > 30 and len(line.strip()) < 280:
            tweets.append({'text': line.strip()})
            if len(tweets) >= 10:
                break
    
    return tweets

def generate_report(topic, data, output_dir):
    """生成研究报告"""
    log("📊 生成研究报告...", 'info')
    
    hn_results = data.get('hackernews', [])
    github_results = data.get('github', [])
    ph_results = data.get('producthunt', [])
    web_results = data.get('web_search', [])
    twitter_results = data.get('twitter', [])
    
    # 热度评估
    total_score = len(hn_results) * 3 + len(github_results) + len(ph_results) * 2
    if total_score > 50:
        heatmap = "🔥 非常高"
    elif total_score > 20:
        heatmap = "⭐ 高"
    elif total_score > 5:
        heatmap = "📈 中等"
    else:
        heatmap = "📊 待观察"
    
    # 生成 Markdown 报告
    report = f"""# 📊 {topic} 深度研究报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**数据来源**: Hacker News, GitHub, Product Hunt, Twitter/X, DuckDuckGo  
**研究版本**: Auto Researcher v2.0

---

## 🎯 执行摘要

### 数据概览
| 平台 | 结果数量 | 状态 |
|------|----------|------|
| Hacker News | {len(hn_results)} | {'✅' if hn_results else '⚠️'} |
| GitHub | {len(github_results)} | {'✅' if github_results else '⚠️'} |
| Product Hunt | {len(ph_results)} | {'✅' if ph_results else '⚠️'} |
| Twitter/X | {len(twitter_results)} | {'✅' if twitter_results else '⚠️'} |
| 网页搜索 | {len(web_results)} | {'✅' if web_results else '⚠️'} |

### 热度评估
**综合热度**: {heatmap} (得分：{total_score})

### 关键发现
"""
    
    # 添加关键发现
    if hn_results:
        top_hn = hn_results[0] if hn_results else {}
        report += f"\n1. **Hacker News 热门**: {top_hn.get('title', 'N/A')[:80]}...\n"
    
    if ph_results:
        report += f"\n2. **Product Hunt 相关**: 找到 {len(ph_results)} 个相关产品\n"
    
    if github_results:
        report += f"\n3. **GitHub 项目**: 找到 {len(github_results)} 个相关仓库\n"
    
    report += f"""
---

## 📰 Hacker News 讨论

"""
    
    for i, story in enumerate(hn_results[:10], 1):
        title = story.get('title', 'N/A')
        author = story.get('author', 'unknown')
        points = story.get('points', 0)
        comments = story.get('num_comments', 0)
        url = story.get('url', '')
        created = story.get('created_at', '')[:10] if story.get('created_at') else ''
        
        report += f"""
### {i}. {title}

- **作者**: {author}
- **分数**: {points} | **评论**: {comments}
- **日期**: {created}
- **链接**: {url}

"""
    
    report += """
---

## 💻 GitHub 相关项目

"""
    
    if github_results:
        for i, repo in enumerate(github_results[:10], 1):
            report += f"{i}. {repo.get('raw', 'N/A')}\n\n"
    else:
        report += "*数据提取中，建议手动访问 GitHub 搜索*\n\n"
    
    report += """
---

## 🚀 Product Hunt 产品

"""
    
    if ph_results:
        for i, product in enumerate(ph_results[:10], 1):
            report += f"{i}. {product.get('name', 'N/A')}\n\n"
    else:
        report += "*数据提取中，建议手动访问 Product Hunt*\n\n"
    
    report += f"""
---

## 📱 Twitter/X 讨论

"""
    
    if twitter_results:
        for i, tweet in enumerate(twitter_results[:10], 1):
            report += f"{i}. {tweet.get('text', 'N/A')[:150]}...\n\n"
    else:
        report += "*数据提取中*\n\n"
    
    report += f"""
---

## 🌐 网页搜索结果

"""
    
    if web_results:
        for i, result in enumerate(web_results[:15], 1):
            report += f"{i}. {result.get('snippet', 'N/A')}\n\n"
    else:
        report += "*数据提取中*\n\n"
    
    report += f"""
---

## 📈 市场洞察

### 趋势分析

基于收集的数据，建议关注以下方向：

1. **技术趋势**: [根据 HN 和 GitHub 数据分析]
2. **产品趋势**: [根据 Product Hunt 数据分析]
3. **用户关注点**: [根据 Twitter 和网页搜索分析]

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
- `{output_dir}/github.json` - GitHub 数据
- `{output_dir}/producthunt.json` - PH 数据
- `{output_dir}/twitter.json` - Twitter 数据
- `{output_dir}/web_search.json` - 网页搜索数据

---

*报告由 Auto Researcher v2.0 自动生成 | 数据截止时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## 📜 License

Copyright © 2026 anyafu. All rights reserved.
Licensed under MIT License.
"""
    
    # 保存报告
    report_path = os.path.join(output_dir, "report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    log(f"✅ 报告已保存：{report_path}", 'success')
    return report_path

def save_json(data, filepath):
    """保存 JSON 数据"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(f"""
{Color.BOLD}🔍 Auto Researcher v2.0 - 智能研究助手{Color.ENDC}
{Color.CYAN}{'='*60}{Color.ENDC}

用法：python3 auto-researcher.py "研究主题" [选项]

示例:
  python3 auto-researcher.py "AI Agent 变现"
  python3 auto-researcher.py "SaaS pricing trends"
  python3 auto-researcher.py "Python web frameworks"

选项:
  --output <dir>  指定输出目录（默认：/tmp/auto-researcher_<时间戳>）
  --no-twitter    跳过 Twitter 搜索
  --no-web        跳过网页搜索
  --help          显示帮助信息

{Color.CYAN}{'='*60}{Color.ENDC}
        """)
        sys.exit(1)
    
    topic = sys.argv[1]
    output_dir = None
    skip_twitter = False
    skip_web = False
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--no-twitter':
            skip_twitter = True
            i += 1
        elif sys.argv[i] == '--no-web':
            skip_web = True
            i += 1
        elif sys.argv[i] == '--help':
            print("使用示例：python3 auto-researcher.py \"研究主题\"")
            sys.exit(0)
        else:
            i += 1
    
    if not output_dir:
        output_dir = f"/tmp/auto-researcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{Color.BOLD}🔍 开始研究：{topic}{Color.ENDC}")
    print(f"{Color.CYAN}📁 输出目录：{output_dir}{Color.ENDC}")
    print(f"{Color.CYAN}{'='*60}{Color.ENDC}\n")
    
    # 数据收集
    all_data = {}
    
    # 1. Hacker News
    hn_results = search_hackernews(topic)
    all_data['hackernews'] = hn_results
    save_json(hn_results, os.path.join(output_dir, 'hackernews.json'))
    
    time.sleep(0.5)
    
    # 2. GitHub
    github_results = search_github_via_jina(topic)
    all_data['github'] = github_results
    save_json(github_results, os.path.join(output_dir, 'github.json'))
    
    time.sleep(0.5)
    
    # 3. Product Hunt
    ph_results = search_producthunt_via_jina(topic)
    all_data['producthunt'] = ph_results
    save_json(ph_results, os.path.join(output_dir, 'producthunt.json'))
    
    time.sleep(0.5)
    
    # 4. Twitter
    if not skip_twitter:
        twitter_results = search_twitter_via_jina(topic)
        all_data['twitter'] = twitter_results
        save_json(twitter_results, os.path.join(output_dir, 'twitter.json'))
    
    time.sleep(0.5)
    
    # 5. 网页搜索
    if not skip_web:
        web_results = search_duckduckgo(topic)
        all_data['web_search'] = web_results
        save_json(web_results, os.path.join(output_dir, 'web_search.json'))
    
    print()
    
    # 生成报告
    report_path = generate_report(topic, all_data, output_dir)
    
    # 打印摘要
    print(f"\n{Color.GREEN}{'='*60}{Color.ENDC}")
    print(f"{Color.BOLD}✅ 研究完成！{Color.ENDC}")
    print(f"{Color.GREEN}{'='*60}{Color.ENDC}")
    print(f"📄 报告文件：{report_path}")
    print(f"📊 原始数据：{output_dir}/")
    print(f"{Color.GREEN}{'='*60}{Color.ENDC}\n")

if __name__ == '__main__':
    main()
