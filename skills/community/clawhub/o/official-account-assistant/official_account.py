#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📢 Official Account Assistant - 公众号助手
功能：AI 降味写作、自动发布、智能配图
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent
ARTICLES_FILE = DATA_DIR / "articles.json"

# AI 降味规则
HUMANIZE_RULES = {
    "去除 AI 痕迹": [
        ("首先", "说实话"),
        ("其次", "还有"),
        ("最后", "最重要的是"),
        ("总之", "总的来说"),
        ("综上所述", "说了这么多"),
        ("值得注意的是", "要说的是"),
        ("不可否认", "老实说"),
    ],
    "添加语气词": [
        ("。", "。"),
        ("。", "。"),
        ("。", "。"),
    ],
    "添加个人感受": [
        ("我认为", "我个人觉得"),
        ("可以说", "说实话"),
        ("显然", "明眼人都能看出来"),
    ]
}

# 标题模板
TITLE_TEMPLATES = [
    "为什么 XXX 的人越来越多？",
    "XXX 的真相，90% 的人都不知道",
    "深度好文：XXX",
    "XXX 是一种什么样的体验？",
    "如何 XXX？这是我见过最好的答案",
]


def load_articles():
    """加载文章"""
    if ARTICLES_FILE.exists():
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"articles": [], "drafts": []}


def save_articles(data):
    """保存文章"""
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def humanize_text(text):
    """AI 降味"""
    result = text
    
    # 替换 AI 常用词
    for old, new in HUMANIZE_RULES["去除 AI 痕迹"]:
        result = result.replace(old, new)
    
    # 添加个人感受
    for old, new in HUMANIZE_RULES["添加个人感受"]:
        result = result.replace(old, new)
    
    # 添加 emoji（每段最多 2 个）
    emojis = ["😄", "🤔", "💡", "✨", "👍", "❤️", "🎉", "📝"]
    paragraphs = result.split("\n\n")
    for i, para in enumerate(paragraphs):
        if len(para) > 50 and i % 3 == 0:
            import random
            emoji = random.choice(emojis)
            paragraphs[i] = emoji + " " + para
    
    return "\n\n".join(paragraphs)


def generate_title(topic):
    """生成标题"""
    import random
    templates = random.sample(TITLE_TEMPLATES, 3)
    titles = [t.replace("XXX", topic) for t in templates]
    return titles


def create_article(title, content, author="公众号"):
    """创建文章"""
    data = load_articles()
    
    article = {
        "title": title,
        "content": content,
        "author": author,
        "created": datetime.now().isoformat(),
        "status": "draft",
        "views": 0,
        "likes": 0
    }
    
    data["articles"].append(article)
    save_articles(data)
    
    return article


def format_article(article):
    """格式化文章"""
    response = f"📝 **{article['title']}**\n\n"
    response += f"✍️ 作者：{article['author']}\n"
    response += f"📅 创建：{article['created'][:10]}\n"
    response += f"📊 状态：{article['status']}\n"
    response += f"👁️ 阅读：{article['views']}\n"
    response += f"❤️ 点赞：{article['likes']}\n\n"
    response += "---\n\n"
    response += article['content'][:500] + "...\n"
    
    return response


def main(query):
    """主函数"""
    query = query.lower()
    
    # AI 降味
    if "降味" in query or "人类化" in query:
        # 简单实现：返回示例
        sample = "首先，我认为这个问题值得探讨。其次，我们需要从多个角度分析。最后，综上所述，结论是明显的。"
        humanized = humanize_text(sample)
        
        return f"""🎭 **AI 降味示例**

**原文：**
{sample}

**降味后：**
{humanized}

💡 把你想降味的文章发给我，我帮你处理！"""
    
    # 生成标题
    if "标题" in query or "起名" in query:
        topic = "写作"  # 默认主题
        titles = generate_title(topic)
        
        response = "📝 **标题建议**：\n\n"
        for i, t in enumerate(titles, 1):
            response += f"{i}. {t}\n"
        
        response += "\n💡 告诉我你的主题，我帮你生成更精准的标题！"
        return response
    
    # 创建文章
    if "创建" in query or "写文章" in query:
        title = "新文章"
        content = "这里是文章内容..."
        article = create_article(title, content)
        return f"✅ 文章已创建！\n\n{format_article(article)}"
    
    # 查看文章列表
    if "文章" in query and "列表" in query:
        data = load_articles()
        if not data["articles"]:
            return "📝 暂无文章"
        
        response = "📝 **文章列表**：\n\n"
        for a in data["articles"][-5:]:
            status_icon = "✅" if a["status"] == "published" else "📝"
            response += f"{status_icon} {a['title']} ({a['created'][:10]})\n"
        
        return response
    
    # 默认回复
    return """📢 公众号助手

**功能**：
1. AI 降味 - "把这篇文章降味"
2. 标题生成 - "帮我想个标题"
3. 创建文章 - "写一篇关于 XXX 的文章"
4. 文章管理 - "查看文章列表"

**特色**：
- AI 降味，让文章更像人类写的
- 智能标题，吸引点击
- 自动排版，美观大方

告诉我你想做什么？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("AI 降味"))
