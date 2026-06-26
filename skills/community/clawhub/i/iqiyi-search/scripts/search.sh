#!/bin/bash

# 爱奇艺影视搜索脚本
# 使用方法: bash search.sh "搜索关键词"

KEYWORD="$1"

if [ -z "$KEYWORD" ]; then
    echo "错误: 请提供搜索关键词"
    echo "用法: bash search.sh \"搜索关键词\""
    exit 1
fi

# URL编码搜索词
ENCODED_KEYWORD=$(printf '%s' "$KEYWORD" | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))")

# 爱奇艺搜索URL
SEARCH_URL="https://so.iqiyi.com/so/q_${ENCODED_KEYWORD}"

echo "正在搜索: $KEYWORD"
echo "搜索URL: $SEARCH_URL"
echo ""

# 使用agent-browser抓取页面
agent-browser open "$SEARCH_URL" --timeout 30000

# 获取页面HTML
HTML=$(agent-browser eval "document.body.innerHTML" --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',''))" 2>/dev/null)

# 如果没有结果，尝试另一种方式
if [ -z "$HTML" ]; then
    echo "尝试备用抓取方式..."
    # 保存页面源码到临时文件
    TEMP_FILE=$(mktemp)
    agent-browser eval "document.documentElement.outerHTML" > "$TEMP_FILE" 2>/dev/null
    HTML=$(cat "$TEMP_FILE")
    rm -f "$TEMP_FILE"
fi

if [ -z "$HTML" ]; then
    echo '{"error": "无法获取页面内容", "results": []}'
    agent-browser close 2>/dev/null
    exit 1
fi

# 使用Python解析HTML并提取影视信息
python3 << EOF
import re
import json
import sys

html = """$HTML"""

results = []

# 尝试多种模式匹配爱奇艺搜索结果
patterns = [
    # 模式1: 标准搜索结果卡片
    r'<a[^>]*href="(https://www\.iqiyi\.com/[^"]+)"[^>]*>.*?<img[^>]*alt="([^"]*)"[^>]*>.*?<div[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</div>',
    # 模式2: 搜索结果列表
    r'data-videoinfo=\'([^\']+)\'',
    # 模式3: 剧集信息
    r'<div[^>]*class="[^"]*qy-search-result-item[^"]*"[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>.*?<div[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</div>',
]

# 提取剧集名称和链接
for pattern in patterns:
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    if matches:
        break

# 尝试提取页面中的JSON数据
json_pattern = r'window\.__INITIAL_STATE__\s*=\s*({.+?});'
json_match = re.search(json_pattern, html, re.DOTALL)

if json_match:
    try:
        data = json.loads(json_match.group(1))
        if 'searchResult' in data and 'data' in data['searchResult']:
            for item in data['searchResult']['data'][:10]:
                title = item.get('title', '') or item.get('displayName', '')
                url = item.get('url', '') or item.get('pageUrl', '')
                desc = item.get('description', '') or item.get('shortTitle', '')
                type_name = item.get('categoryName', '') or item.get('typeName', '未知')
                
                if title and url:
                    results.append({
                        'title': title.replace('<em>', '').replace('</em>', ''),
                        'type': type_name,
                        'description': desc.replace('<em>', '').replace('</em>', '')[:100] + '...' if len(desc) > 100 else desc.replace('<em>', '').replace('</em>', ''),
                        'url': url if url.startswith('http') else 'https:' + url if url.startswith('//') else 'https://www.iqiyi.com' + url,
                        'rating': item.get('score', '')
                    })
    except Exception as e:
        pass

# 如果JSON解析失败，尝试从HTML中提取
if not results:
    # 提取所有链接和标题
    link_pattern = r'<a[^>]*href="(/v_[^"]+|https://www\.iqiyi\.com/[^"]+)"[^>]*[^>]*>\s*<[^>]*>\s*([^<]+)</[^>]*>\s*</a>'
    title_pattern = r'<h3[^>]*>\s*<a[^>]*>([^<]+)</a>'
    
    titles = re.findall(r'title="([^"]+)"[^>]*href="[^"]*iqiyi\.com', html)
    links = re.findall(r'href="(https?://www\.iqiyi\.com/[^"]+)"[^>]*title="', html)
    
    seen = set()
    for i, link in enumerate(links[:10]):
        if link not in seen:
            seen.add(link)
            title = titles[i] if i < len(titles) else '未知标题'
            results.append({
                'title': title,
                'type': '影视',
                'description': '',
                'url': link,
                'rating': ''
            })

# 返回JSON格式
output = {
    'keyword': '$KEYWORD',
    'count': len(results),
    'results': results
}

print(json.dumps(output, ensure_ascii=False, indent=2))
EOF

# 关闭浏览器
agent-browser close 2>/dev/null
