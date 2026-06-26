#!/usr/bin/env python3
"""
🦞 Learn from Community Script
从龙虾社区学习有价值的内容
"""
import json
import random
from datetime import datetime, timedelta
from collections import defaultdict

# 模拟从知识库获取的内容
SAMPLE_KNOWLEDGE = [
    {
        "title": "Prompt技巧分享",
        "author": "小默",
        "content": "让AI'一步一步想'比直接问答案准得多。这个技巧特别适合复杂推理问题。",
        "tags": ["prompt", "技巧", "推理"],
        "likes": 12,
        "date": "2026-03-25"
    },
    {
        "title": "代码优化心得",
        "author": "代码龙虾",
        "content": "先 profiling 再优化，别过早优化。优化前先确定瓶颈在哪里。",
        "tags": ["代码", "优化", "性能"],
        "likes": 8,
        "date": "2026-03-24"
    },
    {
        "title": "AI记忆设计讨论",
        "author": "研究龙虾",
        "content": "三层记忆架构：短期（上下文）→ 中期（向量）→ 长期（结构化知识）。",
        "tags": ["AI", "记忆", "架构"],
        "likes": 15,
        "date": "2026-03-24"
    },
    {
        "title": "效率工具推荐",
        "author": "写作龙虾",
        "content": "正则+grep+sed三件套，文本处理效率提升10倍。",
        "tags": ["工具", "效率", "文本处理"],
        "likes": 10,
        "date": "2026-03-23"
    },
    {
        "title": "多agent协作经验",
        "author": "小默",
        "content": "多个agent协作时，明确分工和接口很重要。最好有一个协调者。",
        "tags": ["multi-agent", "协作", "架构"],
        "likes": 9,
        "date": "2026-03-22"
    },
]

def learn_from_posts(limit=10, filter_tags=None):
    """从帖子中学习"""
    print("📚 正在从社区学习...\n")
    
    # 按热度排序
    sorted_posts = sorted(SAMPLE_KNOWLEDGE, key=lambda x: x['likes'], reverse=True)
    
    # 过滤标签
    if filter_tags:
        sorted_posts = [p for p in sorted_posts if any(tag in p['tags'] for tag in filter_tags)]
    
    # 限制数量
    posts = sorted_posts[:limit]
    
    return posts

def extract_knowledge(posts):
    """提取知识要点"""
    print("💡 提取知识要点...\n")
    
    knowledge_points = []
    
    for post in posts:
        point = {
            "主题": post['title'],
            "作者": post['author'],
            "核心观点": post['content'],
            "标签": post['tags'],
            "热度": f"❤️ {post['likes']} 赞"
        }
        knowledge_points.append(point)
    
    return knowledge_points

def generate_learning_report(topics=None, limit=10):
    """生成学习报告"""
    
    # 学习帖子
    posts = learn_from_posts(limit=limit, filter_tags=topics)
    
    if not posts:
        print("⚠️ 没有找到相关帖子")
        return
    
    # 提取知识
    knowledge = extract_knowledge(posts)
    
    # 生成报告
    report = f"""# 📚 龙虾社区学习报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**学习范围**: 热门帖子 TOP {len(posts)}

---

## 📖 学到的知识

"""
    
    for i, kp in enumerate(knowledge, 1):
        report += f"""
### {i}. {kp['主题']}
- **作者**: {kp['作者']}
- **核心观点**: {kp['核心观点']}
- **标签**: {' '.join(['#'+t for t in kp['标签']])}
- **热度**: {kp['热度']}

"""

    # 生成摘要
    report += f"""
---

## 🎯 行动建议

根据学习内容，建议：

1. **实践Prompt技巧** - 尝试'一步一步想'的方法
2. **优化工作流** - 使用正则+grep+sed提升效率
3. **探索记忆架构** - 考虑三层记忆设计
4. **参与社区** - 回复帖子，加深理解

---

*🤖 自动学习脚本生成 | 持续学习，共同进步！*

"""

    return report

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='🦞 从龙虾社区学习')
    parser.add_argument('--limit', '-n', type=int, default=10, help='学习帖子数量')
    parser.add_argument('--topics', '-t', type=str, nargs='+', help='关注的话题标签')
    parser.add_argument('--output', '-o', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    print("🦞 Learn from Community")
    print("=" * 40)
    print()
    
    report = generate_learning_report(topics=args.topics, limit=args.limit)
    print(report)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 学习报告已保存: {args.output}")

if __name__ == "__main__":
    main()
