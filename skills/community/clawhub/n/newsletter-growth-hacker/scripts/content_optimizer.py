#!/usr/bin/env python3
"""
Newsletter Content Optimizer
提供基于数据的内容优化建议和 A/B 测试主题行生成
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime


class ContentOptimizer:
    """内容优化建议引擎"""
    
    def __init__(self):
        self.content_principles = [
            {
                "principle": "价值先行",
                "description": "开篇即展示核心价值，避免冗长铺垫",
                "tips": [
                    "第一段就告诉读者能获得什么",
                    "使用具体数字和案例",
                    "避免空洞的自我介绍"
                ]
            },
            {
                "principle": "可扫描性",
                "description": "让读者能快速浏览抓住重点",
                "tips": [
                    "使用小标题分隔内容块",
                    "每段不超过 3-4 行",
                    "重要内容加粗或高亮",
                    "使用项目符号列表"
                ]
            },
            {
                "principle": "个性化",
                "description": "让每个读者感到被理解",
                "tips": [
                    "使用读者姓名（如果可能）",
                    "细分受众发送不同版本",
                    "引用读者反馈和问题",
                    "分享个人故事和见解"
                ]
            },
            {
                "principle": "行动导向",
                "description": "每封邮件都有明确的下一步",
                "tips": [
                    "单一清晰的 CTA",
                    "CTA 按钮要醒目",
                    "说明行动的好处",
                    "降低行动门槛"
                ]
            },
            {
                "principle": "移动优先",
                "description": "确保在手机上阅读体验良好",
                "tips": [
                    "单栏布局",
                    "字体至少 14px",
                    "按钮足够大易点击",
                    "图片优化加载速度"
                ]
            }
        ]
        
        self.open_rate_benchmarks = {
            "technology": {"avg": 21.5, "good": 25, "excellent": 30},
            "finance": {"avg": 23.0, "good": 27, "excellent": 32},
            "health": {"avg": 19.0, "good": 23, "excellent": 28},
            "marketing": {"avg": 22.0, "good": 26, "excellent": 31},
            "education": {"avg": 24.0, "good": 28, "excellent": 33},
            "ecommerce": {"avg": 18.0, "good": 22, "excellent": 27},
            "general": {"avg": 21.0, "good": 25, "excellent": 30}
        }
    
    def analyze_content(self, content: str) -> Dict:
        """
        分析邮件内容并给出优化建议
        
        Args:
            content: 邮件内容
        
        Returns:
            分析报告
        """
        analysis = {
            "length": len(content),
            "word_count": len(content.split()),
            "paragraph_count": content.count('\n\n') + 1,
            "has_subject_line": False,
            "has_cta": False,
            "readability_score": 0,
            "suggestions": []
        }
        
        # 检查主题行
        if ':' in content[:100] or '【' in content[:100]:
            analysis["has_subject_line"] = True
        
        # 检查 CTA
        cta_keywords = ['点击', '立即', '注册', '订阅', '查看', '了解', 'CTA', 'button']
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in cta_keywords):
            analysis["has_cta"] = True
        
        # 可读性评分（简化版）
        avg_para_length = analysis["word_count"] / max(analysis["paragraph_count"], 1)
        if 50 <= avg_para_length <= 150:
            analysis["readability_score"] = 90
        elif 30 <= avg_para_length <= 200:
            analysis["readability_score"] = 70
        else:
            analysis["readability_score"] = 50
        
        # 生成建议
        if not analysis["has_subject_line"]:
            analysis["suggestions"].append("添加吸引人的主题行，使用【】或数字增加点击率")
        
        if not analysis["has_cta"]:
            analysis["suggestions"].append("添加明确的行动号召（CTA），告诉读者下一步做什么")
        
        if analysis["word_count"] < 200:
            analysis["suggestions"].append("内容可能过短，考虑增加更多价值")
        elif analysis["word_count"] > 1500:
            analysis["suggestions"].append("内容可能过长，考虑精简或分段发送")
        
        if analysis["paragraph_count"] < 3:
            analysis["suggestions"].append("增加段落分隔，提高可读性")
        
        return analysis
    
    def get_benchmarks(self, industry: str = "general") -> Dict:
        """获取行业打开率基准"""
        return self.open_rate_benchmarks.get(industry, self.open_rate_benchmarks["general"])


class SubjectLineGenerator:
    """A/B 测试主题行生成器"""
    
    def __init__(self):
        self.templates = {
            "curiosity": [
                "你可能不知道{topic}的这个秘密",
                "为什么{number}%的人{action}都失败了",
                "{topic}：大多数人忽略的关键",
                "我从未告诉过任何人的{topic}技巧",
                "这个{topic}错误正在毁掉你的{goal}"
            ],
            "urgency": [
                "最后{hours}小时：{offer}即将结束",
                "仅剩{number}个名额：{event}",
                "今晚 12 点截止：{benefit}",
                "错过再等一年：{opportunity}",
                "紧急：{important_update}"
            ],
            "benefit": [
                "如何在{time}内实现{goal}",
                "{number}个步骤让你{benefit}",
                "从零到{goal}：完整指南",
                "每天{time}分钟，{benefit}",
                "不用{pain}也能{benefit}的方法"
            ],
            "social_proof": [
                "{number}人已经{action}，你呢？",
                "为什么{authority}都选择{topic}",
                "{testimonial_snippet}",
                "加入{number}位{audience}的选择",
                "行业领袖都在用的{topic}策略"
            ],
            "question": [
                "你真的了解{topic}吗？",
                "{goal}，你做到了吗？",
                "为什么你的{topic}总是失败？",
                "{question}？答案可能让你惊讶",
                "如果{scenario}，你会怎么做？"
            ],
            "list": [
                "{number}个{topic}技巧让你{benefit}",
                "{number}位专家分享的{topic}秘密",
                "Top {number}: {topic}排行榜",
                "{number}个工具帮你{goal}",
                "{number}年经验总结的{topic}法则"
            ],
            "story": [
                "我是从{starting_point}到{ending_point}的",
                "{person}的{topic}故事",
                "那一天，我学会了{lesson}",
                "一个{adjective}的{topic}教训",
                "关于{topic}，没人告诉你的真相"
            ]
        }
        
        self.power_words = [
            "免费", "独家", "限时", "秘密", "惊人", "终极", "完整",
            " proven", "科学", "快速", "简单", "保证", "立即", "全新",
            "重磅", "重磅发布", "内部", "罕见", "必学", "必备"
        ]
    
    def generate(self, topic: str, goal: str = None, 
                 styles: List[str] = None, count: int = 5) -> List[Dict]:
        """
        生成 A/B 测试主题行
        
        Args:
            topic: 主题/话题
            goal: 目标/好处
            styles: 风格列表（curiosity/urgency/benefit/social_proof/question/list/story）
            count: 生成数量
        
        Returns:
            主题行列表
        """
        if not styles:
            styles = list(self.templates.keys())
        
        if not goal:
            goal = "提升效果"
        
        generated = []
        
        for style in styles:
            if style not in self.templates:
                continue
            
            for template in self.templates[style]:
                subject = template.format(
                    topic=topic,
                    goal=goal,
                    number=random.randint(3, 10),
                    time=random.choice(["7 天", "30 天", "1 小时", "每天 10 分钟"]),
                    hours=random.randint(2, 24),
                    benefit=goal,
                    action="成功",
                    offer="特别优惠",
                    event="活动",
                    important_update="重要更新",
                    opportunity="难得机会",
                    pain="痛苦努力",
                    authority="行业领袖",
                    testimonial_snippet="效果提升了 300%",
                    audience="专业人士",
                    question="你的目标实现了吗",
                    scenario="时间不够用",
                    starting_point="零基础",
                    ending_point="行业专家",
                    person="成功人士",
                    lesson="重要一课",
                    adjective="意想不到"
                )
                
                # 随机添加 power word
                if random.random() > 0.5:
                    power_word = random.choice(self.power_words)
                    subject = f"{power_word}！{subject}"
                
                generated.append({
                    "subject": subject,
                    "style": style,
                    "predicted_performance": self._predict_performance(style)
                })
                
                if len(generated) >= count:
                    return generated
        
        return generated
    
    def _predict_performance(self, style: str) -> Dict:
        """预测主题行表现（基于行业数据）"""
        predictions = {
            "curiosity": {"open_rate": "22-28%", "click_rate": "3-5%"},
            "urgency": {"open_rate": "25-35%", "click_rate": "4-7%"},
            "benefit": {"open_rate": "20-26%", "click_rate": "5-8%"},
            "social_proof": {"open_rate": "23-29%", "click_rate": "4-6%"},
            "question": {"open_rate": "21-27%", "click_rate": "3-5%"},
            "list": {"open_rate": "24-30%", "click_rate": "4-7%"},
            "story": {"open_rate": "22-28%", "click_rate": "5-9%"}
        }
        return predictions.get(style, {"open_rate": "20-25%", "click_rate": "3-5%"})
    
    def create_ab_test(self, topic: str, goal: str = None, 
                       variants: int = 3) -> Dict:
        """
        创建 A/B 测试方案
        
        Args:
            topic: 主题
            goal: 目标
            variants: 变体数量
        
        Returns:
            A/B 测试方案
        """
        subjects = self.generate(topic, goal, count=variants * 2)
        
        # 选择差异最大的变体
        selected = []
        used_styles = set()
        
        for subj in subjects:
            if subj["style"] not in used_styles:
                selected.append(subj)
                used_styles.add(subj["style"])
            if len(selected) >= variants:
                break
        
        test_plan = {
            "topic": topic,
            "goal": goal or "提升效果",
            "variants": selected,
            "test_setup": {
                "sample_size": "至少 1000 订阅者/变体",
                "duration": "24-48 小时",
                "success_metric": "打开率",
                "secondary_metric": "点击率"
            },
            "implementation": [
                "将订阅者随机分为平等组",
                "每组发送不同主题行",
                "保持内容完全一致",
                "追踪打开率和点击率",
                "统计显著性后宣布获胜者"
            ]
        }
        
        return test_plan


def main():
    """CLI 入口"""
    print("=== Newsletter 内容优化与 A/B 测试工具 ===\n")
    
    # 内容优化
    optimizer = ContentOptimizer()
    
    sample_content = """
【如何提升邮件打开率】

亲爱的读者，

很多人问我如何写出高打开率的邮件主题行。

今天分享 5 个实战技巧：

1. 使用数字：具体数字比模糊描述更吸引人
2. 制造好奇：留下信息缺口让人想点击
3. 强调好处：告诉读者能获得什么
4. 创造紧迫感：限时限量的力量
5. 个性化：让读者感到被理解

立即试用这些技巧，你的打开率会提升 30%+！

点击这里获取完整指南 →
"""
    
    analysis = optimizer.analyze_content(sample_content)
    print("内容分析结果:")
    print(f"字数：{analysis['word_count']}")
    print(f"段落数：{analysis['paragraph_count']}")
    print(f"可读性评分：{analysis['readability_score']}")
    print(f"有主题行：{'是' if analysis['has_subject_line'] else '否'}")
    print(f"有 CTA: {'是' if analysis['has_cta'] else '否'}")
    print("\n优化建议:")
    for sug in analysis["suggestions"]:
        print(f"  - {sug}")
    
    # A/B 测试主题行生成
    print("\n\n=== A/B 测试主题行生成 ===")
    generator = SubjectLineGenerator()
    
    ab_test = generator.create_ab_test(
        topic="邮件营销",
        goal="提升打开率",
        variants=3
    )
    
    print(f"\n主题：{ab_test['topic']}")
    print(f"目标：{ab_test['goal']}")
    print("\n测试变体:")
    for i, variant in enumerate(ab_test["variants"], 1):
        print(f"\n变体{i} ({variant['style']}):")
        print(f"  主题行：{variant['subject']}")
        print(f"  预测打开率：{variant['predicted_performance']['open_rate']}")
    
    print("\n测试设置:")
    for key, value in ab_test["test_setup"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
