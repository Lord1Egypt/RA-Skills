#!/usr/bin/env python3
"""
🦞 Auto Comment Script
自动点评帖子
"""
import random
from datetime import datetime

# 点评模板
COMMENT_TEMPLATES = {
    "praise": [
        "🌟 这篇帖子很有价值！{具体评价}",
        "👍 写得真好！特别认同{观点}",
        "💡 学到了！感谢分享！",
    ],
    "insight": [
        "🔥 这个角度很新颖！{补充观点}",
        "🤔 让我想到一个相关问题：{问题}",
        "💭 我觉得还可以考虑{另一个角度}",
    ],
    "question": [
        "❓ 请教一下：{问题}",
        "🙏 想知道更多关于{细节}的部分",
        "🔍 这个方法适用场景是{场景}吗？",
    ],
    "suggestion": [
        "💬 建议可以补充一下{补充内容}",
        "📝 个人经验：还可以{经验}",
        "🔧 试试看{另一个方法}",
    ],
    "fun": [
        "😂 哈哈，说得太对了！",
        "🤣 这个问题我也遇到过！",
        "🙌 社区需要更多这样的分享！",
    ]
}

# 不同帖子的点评策略
STRATEGIES = {
    "技巧分享": ["praise", "insight", "fun"],
    "技术讨论": ["insight", "question", "suggestion"],
    "经验分享": ["praise", "insight", "suggestion"],
    "求助提问": ["question", "suggestion", "praise"],
    "日常闲聊": ["fun", "praise", "insight"],
}

def generate_comment(post_type="经验分享", style="auto"):
    """生成点评"""
    
    if style == "auto":
        styles = STRATEGIES.get(post_type, ["praise", "insight"])
        style = random.choice(styles)
    
    templates = COMMENT_TEMPLATES.get(style, COMMENT_TEMPLATES["praise"])
    comment = random.choice(templates)
    
    # 填充占位符
    replacements = {
        "具体评价": random.choice([
            "内容详实，可操作性很强",
            "思路清晰，对我帮助很大",
            "角度独特，值得学习"
        ]),
        "观点": random.choice([
            "关于模块化的部分",
            "关于持续迭代的想法",
            "关于用户需求的分析"
        ]),
        "补充观点": random.choice([
            "这个思路可以延伸到其他场景",
            "换个角度看可能效果更好",
            "核心原理其实是相通的"
        ]),
        "问题": random.choice([
            "这个方案的成本如何控制？",
            "有没有考虑边缘情况？",
            "实际落地有哪些坑？"
        ]),
        "另一个角度": random.choice([
            "从运维角度看是否可行",
            "长期维护的角度考虑过吗",
            "用户体验如何保证"
        ]),
        "问题": random.choice([
            "具体是怎么实现的？",
            "能详细说说步骤吗？",
            "遇到坑是怎么解决的？"
        ]),
        "细节": random.choice([
            "实现细节",
            "具体参数",
            "关键步骤"
        ]),
        "场景": random.choice([
            "小规模场景",
            "生产环境",
            "快速迭代阶段"
        ]),
        "补充内容": random.choice([
            "实际案例",
            "效果对比数据",
            "注意事项"
        ]),
        "经验": random.choice([
            "先做小范围测试",
            "做好备份再动手",
            "记录过程方便回溯"
        ]),
        "另一个方法": random.choice([
            "先调研再动手",
            "参考社区最佳实践",
            "用现有工具组合"
        ]),
    }
    
    for key, value in replacements.items():
        comment = comment.replace(f"{{{key}}}", value)
    
    return comment

def generate_full_comment(post_title, post_type="经验分享", style="auto"):
    """生成完整点评格式"""
    
    comment = generate_comment(post_type, style)
    lobster_name = "某只活跃龙虾"
    
    full = f"""### ⭐ 🦞 {lobster_name} 点评：

{comment}

*对帖子「{post_title}」的点评* 📝
"""
    
    return full

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='🦞 生成点评')
    parser.add_argument('--title', '-t', type=str, required=True, help='帖子标题')
    parser.add_argument('--type', type=str, 
                       choices=['技巧分享', '技术讨论', '经验分享', '求助提问', '日常闲聊'],
                       default='经验分享', help='帖子类型')
    parser.add_argument('--style', '-s', type=str,
                       choices=['auto', 'praise', 'insight', 'question', 'suggestion', 'fun'],
                       default='auto', help='点评风格')
    
    args = parser.parse_args()
    
    print("🦞 Auto Comment Generator")
    print("=" * 40)
    print()
    
    comment = generate_full_comment(args.title, args.type, args.style)
    print("📝 生成的点评：\n")
    print(comment)
    print()
    print("-" * 40)
    print("💡 提示：将点评追加到知识库帖子的评论区")

if __name__ == "__main__":
    main()
