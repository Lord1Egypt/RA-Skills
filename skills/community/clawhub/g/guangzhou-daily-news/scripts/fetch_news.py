#!/usr/bin/env python3
"""
广州日报新花城新闻获取脚本 v2.1
自动获取20-30条新闻，包含：标题、摘要、分类、发布时间、编辑、记者
输出美观 Markdown 格式 + 微信消息
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# 配置
OUTPUT_DIR = Path.home() / "News"
NEWS_COUNT = 20  # 默认获取条数


def extract_author_editor(text):
    """从新闻详情文本中提取记者和编辑"""
    author = "—"
    editor = "—"
    
    # 提取编辑 - 多种模式
    editor_patterns = [
        r'广州日报新花城编辑[：:]\s*(\S+)',
        r'编辑[：:]\s*(\S+)',
    ]
    for pattern in editor_patterns:
        match = re.search(pattern, text)
        if match:
            editor = match.group(1).strip()
            break
    
    # 提取记者 - 多种模式
    author_patterns = [
        r'文/广州日报新花城记者[：:]\s*([^\n]+)',
        r'广州日报新花城记者[：:]\s*([^\n]+)',
        r'记者[：:]\s*([^\n]+)',
        r'统筹[：:]\s*(\S+)',  # 统筹也算负责人
    ]
    for pattern in author_patterns:
        match = re.search(pattern, text)
        if match:
            author = match.group(1).strip()
            # 清理多余的空格和斜杠
            author = author.split('/')[-1].strip()
            if author and author != editor:
                break
    
    # 如果没找到记者但有统筹，可以用统筹
    if author == "—":
        match = re.search(r'统筹[：:]\s*(\S+)', text)
        if match:
            author = match.group(1).strip()
    
    return author, editor


def parse_article_detail(html_text):
    """从文章详情页提取信息"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_text, 'html.parser')
    result = {}
    
    # 获取正文内容作为摘要
    article = soup.select_one('.article-content, .content, article, .text, .main-content, #textcontent')
    if article:
        text = article.get_text(strip=True)
        # 截取前200字作为摘要
        result['abstract'] = text[:200] + "..." if len(text) > 200 else text
    else:
        result['abstract'] = "点击链接查看详情"
    
    # 获取页面所有文本用于提取记者/编辑
    page_text = soup.get_text()
    author, editor = extract_author_editor(page_text)
    result['author'] = author
    result['editor'] = editor
    
    # 尝试获取发布时间
    time_elem = soup.select_one('.time, .date, .publish-time, time')
    if time_elem:
        result['publish_time'] = time_elem.get_text(strip=True)[:16]
    else:
        result['publish_time'] = "今天"
    
    return result


def generate_markdown(news_list):
    """生成美观 Markdown 格式"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 分类 emoji 映射
    category_emoji = {
        "要闻": "🔴", "科技": "🚀", "文化": "🎭", "国际": "🌍",
        "经济": "💰", "教育": "📚", "健康": "🏥", "体育": "⚽",
        "湾区": "🌊", "城事": "🏙️", "汽车": "🚗", "时政": "📰"
    }
    
    md = f"""<div align="center">

# 📰 广州日报新闻简报

**📅 {today}** · **来源：新花城** · **共 {len(news_list)} 条**

---

</div>

"""
    
    for i, news in enumerate(news_list, 1):
        emoji = category_emoji.get(news.get('category', ''), '📌')
        category = news.get('category', '综合')
        
        md += f"""> ## {i}. {news['title']}
> 
> **{emoji} {category}** · ⏰ {news.get('time', '')}
> 
> {news.get('abstract', '暂无摘要')}
> 
> ✍️ 记者：**{news.get('author', '—')}** · 📝 编辑：**{news.get('editor', '—')}** · 🔗 [阅读原文]({news['url']})
> 
> ---
> 
"""
    
    return md, today


def generate_wechat_msg(news_list):
    """生成微信推送消息"""
    today = datetime.now().strftime("%m月%d日")
    msg = f"📰 广州日报 {today} ({len(news_list)}条)\n\n"
    
    for i, news in enumerate(news_list[:10], 1):
        title = news['title'][:22] + ".." if len(news['title']) > 22 else news['title']
        msg += f"{i}. {title}\n"
    
    if len(news_list) > 10:
        msg += f"\n...还有 {len(news_list) - 10} 条"
    
    return msg


def process_news(news_with_details):
    """处理带有详情的新闻列表，生成输出"""
    if not news_with_details:
        print("❌ 没有新闻数据")
        return None
    
    # 生成 Markdown
    md_content, today = generate_markdown(news_with_details)
    
    # 保存文件
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"广州日报_{today}.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 生成微信消息
    wechat_msg = generate_wechat_msg(news_with_details)
    
    result = {
        "success": True,
        "count": len(news_with_details),
        "date": today,
        "markdown_path": str(output_path),
        "wechat_message": wechat_msg
    }
    
    print(f"✅ 已保存: {output_path}")
    print(f"\n📱 微信消息：\n{wechat_msg}")
    
    return result


if __name__ == "__main__":
    # 测试用
    print("请通过 AI 配合 web_fetch 使用本脚本")
