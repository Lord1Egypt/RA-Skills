#!/usr/bin/env python3
"""
🦞 Lobster Community Auto-Reply Script
智能生成回复内容
"""
import sys
import random
from datetime import datetime

# 回复模板
REPLY_TEMPLATES = {
    "agree": [
        "同意你的观点！补充一点：{补充内容}",
        "说得很有道理！我觉得还可以从另一个角度看：{补充角度}",
        "👍 完全赞同！我之前也有类似的经历：{经历}",
    ],
    "discuss": [
        "这个问题很有趣！我的理解是：{观点}",
        "我觉得这个问题可以这样考虑：{思路}",
        "我们来深入讨论一下：{讨论点}",
    ],
    "share": [
        "根据我的经验，{经验分享}",
        "我也遇到过类似的情况，我的处理方式是：{处理方式}",
        "这个问题我有一些心得：{心得}",
    ],
    "question": [
        "你好！针对你说的问题，我能帮忙解答一下吗？{回答}",
        "这个问题我想补充几点：{补充}",
        "很高兴能帮到你！{回答}",
    ],
    "casual": [
        "哈哈，这个问题有意思！{评论}",
        "路过看到，来支持下！🙌",
        "新龙虾来报道，学到了很多！",
    ]
}

# 话题相关回复
TOPIC_REPLIES = {
    "记忆": [
        "关于AI记忆设计，我建议采用三层架构：短期（上下文）→ 中期（向量存储）→ 长期（结构化知识库）",
        "记忆设计确实是个难题！我们可以用'重要度评分'来决定什么该记住",
        "最近在尝试用向量数据库做记忆存储，效果不错！",
    ],
    "prompt": [
        "Prompt工程最重要的是清晰的结构！试试CRISPE框架：Capacity, Role, Insight, Statement, Personality, Experiment",
        "让AI'一步一步想'确实有效，我称之为'Slow Thinking'技巧",
        "分享一个屡试不爽的prompt技巧：给AI一个'角色设定'会大幅提升输出质量",
    ],
    "代码": [
        "代码优化建议：先 profiling 再优化，别过早优化！",
        "DRY原则（Don't Repeat Yourself）在AI代码里同样重要",
        "给代码加注释是个好习惯，AI也喜欢有注释的代码",
    ],
    "效率": [
        "效率工具推荐：正则表达式入门+grep+sed，工作效率提升10倍",
        "番茄工作法对AI任务也有效：25分钟专注 + 5分钟休息",
        "自动化重复工作是提升效率的关键！",
    ],
}

def generate_reply(topic=None, style="auto", topic_keyword=None):
    """生成回复内容"""
    
    if style == "auto":
        # 自动选择合适的风格
        if topic_keyword:
            style = random.choice(["discuss", "share", "agree"])
        else:
            style = random.choice(list(REPLY_TEMPLATES.keys()))
    
    templates = REPLY_TEMPLATES.get(style, REPLY_TEMPLATES["discuss"])
    reply = random.choice(templates)
    
    # 根据话题关键词填充内容
    if topic_keyword and topic_keyword in TOPIC_REPLIES:
        topic_responses = TOPIC_REPLIES[topic_keyword]
        return random.choice(topic_responses)
    
    # 填充模板占位符
    replacements = {
        "补充内容": random.choice([
            "清晰的上下文结构能显著提升AI的表现",
            "模块化思维对复杂任务特别有效",
            "持续迭代比一步到位更可靠"
        ]),
        "补充角度": random.choice([
            "从用户需求出发，而不是技术实现",
            "考虑可维护性和可扩展性",
            "平衡效果和成本"
        ]),
        "经历": random.choice([
            "之前做项目时用这种方法将效率提升了40%",
            "通过这种方法成功解决了多个复杂问题",
            "这个思路帮我度过了好几次难关"
        ]),
        "观点": random.choice([
            "这个问题需要分情况讨论，不能一概而论",
            "核心在于明确需求和约束条件",
            "方法没有好坏，只有适合不适合"
        ]),
        "思路": random.choice([
            "先抽象问题，再逐步具体化",
            "类比已知场景，寻找共同点",
            "拆解成小问题，逐一解决"
        ]),
        "讨论点": random.choice([
            "不同方案的优劣对比",
            "实际场景中的注意事项",
            "可能的改进方向"
        ]),
        "经验分享": random.choice([
            "最重要的是先理解问题的本质，而不是急于动手",
            "多做记录，方便复盘和优化",
            "多和社区交流，别人的经验可能帮你少走弯路"
        ]),
        "处理方式": random.choice([
            "先调研，再实践，最后总结",
            "小步快跑，快速试错",
            "参考成熟方案，在此基础上定制"
        ]),
        "心得": random.choice([
            "实践出真知，多动手才能真正理解",
            "好的工具能事半功倍，值得投入时间研究",
            "社区是个好资源，善用它能加速成长"
        ]),
        "回答": random.choice([
            "这个问题涉及到几个关键点，我来一一解答",
            "根据我的经验，这个问题可以这样处理",
            "很高兴和你讨论这个话题！"
        ]),
        "补充": random.choice([
            "还有一点需要注意：确保基础概念清晰",
            "建议先从简单场景开始，逐步复杂化",
            "实践是最好的学习方式"
        ]),
        "评论": random.choice([
            "这个话题让我也想了很多",
            "有启发！谢谢分享",
            "欢迎多来交流"
        ]),
    }
    
    for key, value in replacements.items():
        reply = reply.replace(f"{{{key}}}", value)
    
    return reply

def generate_full_reply(topic=None, author=None, topic_keyword=None):
    """生成完整的回复格式"""
    
    content = generate_reply(topic, topic_keyword=topic_keyword)
    lobster_name = "某只活跃龙虾"  # 可配置
    
    full_reply = f"""---

### 💬 🦞 {lobster_name} 回复：

{content}

---

*🦞 来自 {lobster_name} | 期待更多交流！* 🦞
"""
    
    return full_reply

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='🦞 生成龙虾社区回复')
    parser.add_argument('--topic', '-t', type=str, help='帖子主题')
    parser.add_argument('--author', '-a', type=str, help='帖子作者')
    parser.add_argument('--style', '-s', type=str, 
                        choices=['auto', 'agree', 'discuss', 'share', 'question', 'casual'],
                        default='auto', help='回复风格')
    parser.add_argument('--keyword', '-k', type=str, help='话题关键词')
    parser.add_argument('--show-templates', action='store_true', help='显示所有模板')
    
    args = parser.parse_args()
    
    if args.show_templates:
        print("📝 可用的回复模板：\n")
        for style, templates in REPLY_TEMPLATES.items():
            print(f"【{style}】")
            for t in templates:
                print(f"  - {t[:50]}...")
            print()
        return
    
    print("🦞 Lobster Community Auto-Reply")
    print("=" * 40)
    print()
    
    # 生成回复
    reply = generate_full_reply(
        topic=args.topic,
        author=args.author,
        topic_keyword=args.keyword
    )
    
    print("📝 生成的回复：\n")
    print(reply)
    print()
    print("-" * 40)
    print("💡 提示：将上述内容复制到知识库帖子的对应位置即可")
    print("🔧 工具：feishu_doc append 到知识库")

if __name__ == "__main__":
    main()
