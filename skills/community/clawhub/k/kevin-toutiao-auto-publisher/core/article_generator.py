#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章生成器 - 根据话题邀请生成头条文章
结合国学经典哲学思想 + 中年男人共鸣视角
支持自定义个人画像
"""

import random
from datetime import datetime


class ArticleGenerator:
    """文章生成器"""

    def __init__(self, personal_profile=None):
        """
        初始化文章生成器

        Args:
            personal_profile: 个人画像字典，包含 age/job/relationship/family/assets/dream/skills/current_action
                             如果不传，使用默认的通用画像
        """
        # 个人画像（可自定义）
        if personal_profile:
            self.personal_profile = personal_profile
        else:
            # 默认通用画像（示例，用户应根据自己情况修改）
            self.personal_profile = {
                "age": 36,
                "job": "企业员工",
                "relationship": "有对象（未婚）",
                "family": "丁克",
                "assets": "有车贷，房子还没买",
                "dream": "想有个属于自己的房子",
                "skills": ["编程", "视频剪辑", "AI"],
                "current_action": "正在用编程+AI做副业"
            }

        # 国学经典名句
        self.classics = {
            "道德经": [
                "上善若水。水善利万物而不争。",
                "企者不立，跨者不行。",
                "千里之行，始于足下。",
                "柔弱胜刚强。",
                "知人者智，自知者明。",
                "大巧若拙，大辩若讷。",
                "道常无为而无不为。"
            ],
            "易经": [
                "否极泰来。",
                "天行健，君子以自强不息。",
                "地势坤，君子以厚德载物。",
                "穷则变，变则通，通则久。",
                "君子藏器于身，待时而动。"
            ],
            "论语": [
                "学而不思则罔，思而不学则殆。",
                "己所不欲，勿施于人。",
                "三人行，必有我师焉。",
                "知之为知之，不知为不知，是知也。"
            ],
            "庄子": [
                "井蛙不可以语于海者，拘于虚也。",
                "吾生也有涯，而知也无涯。",
                "君子之交淡如水，小人之交甘若醴。"
            ]
        }

        # 自然时间表达
        self.time_expressions = [
            "今天晚上",
            "今天下班回家的路上",
            "躺到床上刷手机时",
            "靠在阳台抽烟时",
            "早上醒来刷头条时",
            "刚跟朋友喝完酒回家",
            "深夜加班到很晚时"
        ]

        # 故事类型（多元化）
        self.story_types = [
            "犹豫型",  # 想改变但犹豫
            "迷茫型",  # 不知方向
            "后悔型",  # 后悔过去选择
            "绝望型",  # 感到无助
            "觉醒型"   # 开始行动
        ]

    def generate_article(self, topic, view_count=0):
        """
        根据话题生成文章

        Args:
            topic: 话题标题
            view_count: 话题围观人数

        Returns:
            dict: 包含标题、内容的文章
        """
        # 1. 选择自然时间开头
        time_expr = random.choice(self.time_expressions)

        # 2. 选择经典名句
        classic_source = random.choice(list(self.classics.keys()))
        classic_quote = random.choice(self.classics[classic_source])

        # 3. 选择故事类型
        story_type = random.choice(self.story_types)

        # 4. 生成文章
        article = self._generate_article_content(
            topic=topic,
            time_expr=time_expr,
            classic_source=classic_source,
            classic_quote=classic_quote,
            story_type=story_type,
            view_count=view_count
        )

        # 5. 生成标题
        title = self._generate_title(topic, story_type)

        return {
            "title": title,
            "content": article,
            "topic": topic,
            "classic_source": classic_source,
            "classic_quote": classic_quote,
            "story_type": story_type,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _generate_article_content(self, topic, time_expr, classic_source, classic_quote, story_type, view_count):
        """生成文章内容"""
        # 根据不同话题类型生成不同内容
        content = f"{time_expr}，刷到一个热门话题：\"{topic}\"。\n\n"

        # 根据围观人数增加热度描述
        if view_count > 0:
            content += f"这个话题有{view_count}人围观，下面评论几万条。"

        # 生成正文
        content += self._generate_body_by_topic(topic, classic_source, classic_quote, story_type)

        return content

    def _generate_body_by_topic(self, topic, classic_source, classic_quote, story_type):
        """根据话题类型生成正文"""
        # 根据话题关键词匹配不同的内容模板
        if any(keyword in topic for keyword in ["35岁", "失业", "裁员", "辞职", "工作"]):
            return self._generate_career_content(classic_source, classic_quote, story_type)
        elif any(keyword in topic for keyword in ["缺钱", "买房", "车贷", "房贷", "钱"]):
            return self._generate_money_content(classic_source, classic_quote, story_type)
        elif any(keyword in topic for keyword in ["焦虑", "迷茫", "崩溃", "压力"]):
            return self._generate_anxiety_content(classic_source, classic_quote, story_type)
        else:
            return self._generate_general_content(classic_source, classic_quote, story_type)

    def _generate_career_content(self, classic_source, classic_quote, story_type):
        """生成职场相关内容"""
        content = ""

        # 个人经历
        content += f"我今年{self.personal_profile['age']}，在一家{self.personal_profile['job']}上班。这行什么情况大家心里有数，我现在还能干活，不代表明年还能。我知道这个年纪的人，一失业就是失业，再找工作太难。\n\n"

        # 认知转变
        content += "我以前总觉得，只要自己努力，就能撑下去。但我错了。\n\n"

        # 经典引用
        content += f"《{classic_source}》里说：\"{classic_quote}\"\n\n"

        # 经典解释
        content += self._explain_classic(classic_source, classic_quote, "career")

        # 转折和微光
        content += self._generate_hope()

        return content

    def _generate_money_content(self, classic_source, classic_quote, story_type):
        """生成金钱相关内容"""
        content = ""

        # 个人经历
        content += f"我和对象躺床上算账，{self.personal_profile['assets']}。{self.personal_profile['dream']}，我也想。但算来算去，存款差得远。\n\n"
        content += f"我们{self.personal_profile['relationship']}，是{self.personal_profile['family']}，压力好像比人家小。但我知道，这只是表面。房子没着落，心里总不踏实。\n\n"

        # 认知转变
        content += "我以前总觉得，只要努力工作，总能攒够钱买房。但我错了。\n\n"

        # 经典引用
        content += f"《{classic_source}》里说：\"{classic_quote}\"\n\n"

        # 经典解释
        content += self._explain_classic(classic_source, classic_quote, "money")

        # 转折和微光
        content += self._generate_hope()

        return content

    def _generate_anxiety_content(self, classic_source, classic_quote, story_type):
        """生成焦虑相关内容"""
        content = ""

        # 个人经历
        skills_str = "、".join(self.personal_profile['skills'])
        content += f"我也爱折腾，今年{self.personal_profile['age']}了。学{skills_str}，天天晚上忙到半夜。\n\n"
        content += f"我在一家{self.personal_profile['job']}上班，日子也过得去。但我心里知道，我不是不累，是不敢停下来。\n\n"

        # 认知转变
        content += "我以前总觉得，中年男人的焦虑是矫情。但我错了。\n\n"

        # 经典引用
        content += f"《{classic_source}》里说：\"{classic_quote}\"\n\n"

        # 经典解释
        content += self._explain_classic(classic_source, classic_quote, "anxiety")

        # 转折和微光
        content += self._generate_hope()

        return content

    def _generate_general_content(self, classic_source, classic_quote, story_type):
        """生成通用内容"""
        content = ""

        # 个人经历
        content += f"我今年{self.personal_profile['age']}，在一家{self.personal_profile['job']}上班。{self.personal_profile['assets']}。\n\n"
        content += f"我{self.personal_profile['relationship']}，{self.personal_profile['family']}。{self.personal_profile['dream']}，我想给对象更好的生活，但总感觉力不从心。\n\n"

        # 认知转变
        content += "我以前总觉得，只要坚持就能改变。但我错了。\n\n"

        # 经典引用
        content += f"《{classic_source}》里说：\"{classic_quote}\"\n\n"

        # 经典解释
        content += self._explain_classic(classic_source, classic_quote, "general")

        # 转折和微光
        content += self._generate_hope()

        return content

    def _explain_classic(self, source, quote, topic_type):
        """解释经典名句"""
        explanations = {
            "道德经": {
                "career": "我以前不懂这话什么意思，现在我明白了。水是最软的东西，但水能适应任何容器。水流到地上，就变成水沟；流到河里，就变成江河；流到海里，就变成大海。水不固执，水不争强，但水能活下去。\n\n中年男人最大的困境，不是不够努力，是太固执。我们习惯了按部就班，习惯了靠平台、靠公司，把自己变成了固定的形状。现在平台不要你了，你还是那个形状，但已经装不下了。\n\n水不是认命，是换个活法。",
                "money": "我以前总觉得，缺钱是因为我不够努力。但现在我才发现，不是这样的。房价越来越高，工资涨得远远跟不上。这不是我不努力，是这个世道变了。\n\n但我明白了这句话的意思：不是等好运来，是自己在困境中找到出路。",
                "anxiety": "意思是：踮着脚尖站不稳，跨大步走不远。想太高站不稳，想太快走不远。\n\n我以前总想着要稳定，要安稳，要一步步往上走。但我发现，中年男人最大的困境，不是不敢辞职，是没有别的路可走。\n\n我们习惯了靠公司、靠平台，把自己的路走窄了。现在公司不要你了，你连个出口都找不到。",
                "general": "这句话我以前听过很多次，但直到今天才真正理解。它不是让你躺平，是让你找到自己的节奏。\n\n我们这代人活得太累了，总想着要往上爬，要追上别人。但每个人都有自己的节奏，太快反而走不远。"
            },
            "易经": {
                "career": "古人说\"否极泰来\"，不是让你等好运，是让你在最困难的时候，看见希望的方向。困境不是终点，是转折点。",
                "money": "意思是阻碍、不通。后面跟着\"泰卦\"，意思是通泰、安宁。古人说\"否极泰来\"，不是让你等好运，是让你在最困难的时候，看见希望的方向。",
                "anxiety": "意思是：穷则变，变则通，通则久。走到尽头了就要改变，改变了才能通达，通达了才能长久。\n\n我以前总觉得，中年男人的焦虑是矫情。现在我明白了：焦虑是因为走到尽头了，需要改变。不是让你放弃，是让你换个方向。",
                "general": "这句话我以前听过很多次，但直到今天才真正理解。它不是让你躺平，是让你找到自己的节奏。困境不是终点，是转折点。"
            },
            "论语": {
                "career": "学习很重要，但思考更重要。光靠蛮力干活，不如停下来想想方向。\n\n中年男人最大的问题，不是不够努力，是太习惯于不思考。公司让干什么就干什么，领导说什么就听什么，从来没想过自己到底想要什么。\n\n到了35岁，才突然发现，自己除了干活什么都不会。",
                "money": "自己不想要的，不要强加给别人。反过来也是一样——别人觉得好的路，未必适合你。\n\n有人觉得攒钱买房就是幸福，有人觉得租房自由也挺好。没有标准答案，关键是搞清楚自己要什么。",
                "anxiety": "焦虑不是因为做得不够多，是因为想得不够清楚。\n\n该停下来想想了：我到底在追求什么？是别人的认可，还是自己的内心？",
                "general": "三个人一起走路，其中一定有我的老师。意思是，每个人都有值得学习的地方。\n\n不要觉得自己年纪大了就不用学了。学无止境，只要还在学习，就还有希望。"
            },
            "庄子": {
                "career": "井底的青蛙，你跟它说大海有多大，它听不懂。因为它只见过井口那么大的天。\n\n中年人也是一样，我们被困在自己的舒适圈里，以为自己看到的就是全世界。但其实外面的世界大得多。\n\n打破舒适圈，才能看到更大的世界。",
                "money": "人的生命是有限的，但知识是无限的。用有限的生命去追求无限的东西，太累了。\n\n钱也是一样，赚不完的。别让钱成为你人生唯一的目标。",
                "anxiety": "真正的朋友之间，关系是淡的，像白开水一样，不热烈，但长久。\n\n中年人之间的焦虑，很多是跟别人比较出来的。别比了，过好自己的日子。",
                "general": "这句话的意思是，不要被自己有限的认知束缚住了。\n\n我们每个人都是那只井底的青蛙，只是井口大小不同罢了。承认自己的无知，才是真正的智慧。"
            }
        }

        return explanations.get(source, {}).get(topic_type, f"这句话的意思很深，值得细细品味。")

    def _generate_hope(self):
        """生成转折和微光"""
        hope = f"但最近我明白了一个事：路不是等来的，是自己开出来的。\n\n"
        hope += f"我现在{self.personal_profile['current_action']}，虽然还没起色，但至少方向是对的。我知道这很难，也知道很慢，但至少这是我自己的路。\n\n"
        hope += "中年男人的安全感，从来都不是别人给的，是自己一步一步走出来的。"

        return hope

    def _generate_title(self, topic, story_type):
        """生成文章标题"""
        age = self.personal_profile.get('age', '')
        titles = [
            f"关于{topic[:10]}，我想了很久",
            f"今天刷到\"{topic[:15]}\"的话题，我想起了一句话",
            f"{age}岁，聊聊{topic[:8]}" if age else f"聊聊{topic[:8]}",
            f"中年男人的困境：{topic[:12]}",
            f"关于{topic[:10]}，我才发现自己错了"
        ]

        return random.choice(titles)


def main():
    """测试文章生成器"""
    generator = ArticleGenerator()

    # 测试生成文章
    topic = "35岁被裁员，该何去何从"
    article = generator.generate_article(topic, view_count=50000)

    print(f"标题：{article['title']}")
    print(f"话题：{article['topic']}")
    print(f"经典来源：{article['classic_source']}")
    print(f"经典名句：{article['classic_quote']}")
    print(f"故事类型：{article['story_type']}")
    print(f"生成时间：{article['generated_at']}")
    print("\n" + "="*50 + "\n")
    print(article['content'])


if __name__ == "__main__":
    main()
