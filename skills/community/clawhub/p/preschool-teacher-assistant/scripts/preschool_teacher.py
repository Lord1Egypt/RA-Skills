#!/usr/bin/env python3
"""
幼教百宝箱 — AI幼师全流程助手
================================
功能模块：教案生成 | 观察记录 | 家园共育 | 活动设计 | 教学计划 | 环境创设 | 教学反思 | 故事创作

用法:
  # Demo 演示模式（零依赖）
  python preschool_teacher.py --mode demo

  # 教案生成
  python preschool_teacher.py --mode lesson_plan --domain 语言 --age 中班 --query "春天的色彩"

  # 观察记录
  python preschool_teacher.py --mode observation --age 小班 --query "小明在积木区主动分享玩具"

  # 家园共育（家长通知/期末评语/家长会发言）
  python preschool_teacher.py --mode communication --query "期末家长会发言稿" --sub 发言稿

  # 活动设计
  python preschool_teacher.py --mode activity --age 大班 --query "端午节主题游戏"

  # 教学计划
  python preschool_teacher.py --mode plan --plan_type 周计划 --query "春天主题"

  # 环境创设
  python preschool_teacher.py --mode environment --query "春天主题墙面环创"

  # 教学反思
  python preschool_teacher.py --mode reflection --query "上次科学活动浮沉实验"

  # 故事创作
  python preschool_teacher.py --mode story --age 小班 --query "勇敢的小兔子"

  # 综合报告（一站式）
  python preschool_teacher.py --mode report --query "春天主题：我需要教案+观察记录+家长通知+环创方案"

  # LLM增强模式
  python preschool_teacher.py --mode lesson_plan --query "数学：认识数字1-5" --api-key sk-xxx --api-base https://api.deepseek.com/v1
"""

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ───────────────────────── 内置知识库 ─────────────────────────

# 《3-6岁儿童学习与发展指南》五大领域核心目标摘要
GUIDELINES = {
    "健康": {
        "身心状况": ["具有健康的体态", "情绪安定愉快", "具有一定的适应能力"],
        "动作发展": ["具有一定的平衡能力，动作协调灵敏", "具有一定的力量和耐力", "手的动作灵活协调"],
        "生活习惯与生活能力": ["具有良好的生活与卫生习惯", "具有基本的生活自理能力", "具备基本的安全知识和自我保护能力"],
    },
    "语言": {
        "倾听与表达": ["认真听并能听懂常用语言", "愿意讲话并能清楚地表达", "具有文明的语言习惯"],
        "阅读与书写准备": ["喜欢听故事，看图书", "具有初步的阅读理解能力", "具有书面表达的愿望和初步技能"],
    },
    "社会": {
        "人际交往": ["愿意与人交往", "能与同伴友好相处", "具有自尊、自信、自主的表现", "关心尊重他人"],
        "社会适应": ["喜欢并适应群体生活", "遵守基本的行为规范", "具有初步的归属感"],
    },
    "科学": {
        "科学探究": ["亲近自然，喜欢探究", "具有初步的探究能力", "在探究中认识周围事物和现象"],
        "数学认知": ["初步感知生活中数学的有用和有趣", "感知和理解数、量及数量关系", "感知形状与空间关系"],
    },
    "艺术": {
        "感受与欣赏": ["喜欢自然界与生活中美的事物", "喜欢欣赏多种多样的艺术形式和作品"],
        "表现与创造": ["喜欢进行艺术活动并大胆表现", "具有初步的艺术表现与创造能力"],
    },
}

AGE_CHARACTERISTICS = {
    "小班": {"年龄": "3-4岁", "特点": ["情绪作用大，易受外界影响", "思维具体形象，依靠动作", "爱模仿，游戏以平行游戏为主", "语言发展迅速，词汇量快速增长", "开始形成初步的自我意识"]},
    "中班": {"年龄": "4-5岁", "特点": ["活泼好动，动作更加协调", "思维具体形象，开始有逻辑萌芽", "社交需求增强，喜欢结伴游戏", "口语表达能力显著提升", "规则意识开始萌发"]},
    "大班": {"年龄": "5-6岁", "特点": ["好奇好问，求知欲旺盛", "抽象逻辑思维开始发展", "合作意识增强，能组织游戏", "语言表达连贯完整", "自我控制能力提高", "为入学做好准备"]},
}

DOMAIN_KEYWORDS = {
    "健康": ["身体", "运动", "健康", "卫生", "安全", "饮食", "体育", "户外"],
    "语言": ["故事", "儿歌", "绘本", "讲述", "表达", "阅读", "倾听"],
    "社会": ["交往", "规则", "合作", "分享", "情感", "家庭", "社区"],
    "科学": ["探究", "观察", "实验", "数学", "自然", "数量", "形状"],
    "艺术": ["美术", "音乐", "舞蹈", "手工", "绘画", "欣赏", "创造"],
}

# ───────────────────────── 内容生成引擎 ─────────────────────────

def generate_lesson_plan(domain, age_group, query, api_key=None, api_base=None, model=None):
    """生成五大领域教案"""
    age_info = AGE_CHARACTERISTICS.get(age_group, AGE_CHARACTERISTICS["中班"])
    domain_info = GUIDELINES.get(domain, GUIDELINES["语言"])

    if api_key:
        return _llm_generate("lesson_plan", domain=domain, age_group=age_group, query=query,
                             age_info=age_info, domain_info=domain_info,
                             api_key=api_key, api_base=api_base, model=model)

    # 内置模板生成
    sub_domains = list(domain_info.keys())
    sub_domain = sub_domains[0]
    targets = domain_info[sub_domain]

    plan = {
        "领域": domain,
        "年龄段": f"{age_group}({age_info['年龄']})",
        "活动名称": f"{query}（{sub_domain}活动）",
        "活动目标": [
            targets[0] if "具有" in targets[0] else f"了解{query}的基本特征",
            f"能用语言/动作表达对{query}的理解",
            f"体验{query}活动的乐趣，培养积极情感",
        ],
        "活动准备": [
            f"物质准备：{query}相关的教具、图片、实物",
            "经验准备：幼儿已有的相关生活经验",
        ],
        "活动过程": {
            "导入环节（3-5分钟）": f"通过情境/游戏/儿歌导入，激发幼儿对{query}的兴趣。",
            "基本环节（15-20分钟）": [
                f"1. 感知体验：引导幼儿通过看、听、触摸等多种感官感受{query}",
                f"2. 操作探索：提供材料让幼儿自主操作/探索{query}",
                "3. 交流分享：鼓励幼儿表达自己的发现和感受",
            ],
            "结束环节（3-5分钟）": "总结活动要点，对幼儿表现给予积极评价。",
            "延伸活动": f"在区域活动中投放{query}相关材料，如美工区、阅读区。",
        },
        "指导要点": [
            f"关注{age_group}幼儿的{'; '.join(age_info['特点'][:3])}特点",
            "采用游戏化的教学方式",
            "注重个体差异，提供分层支持",
            "鼓励幼儿主动探索和表达",
        ],
        "家园共育": f"请家长在家中和孩子一起观察{query}，分享相关经验。",
    }
    return plan


def generate_observation(age_group, query, api_key=None, api_base=None, model=None):
    """生成幼儿观察记录"""
    age_info = AGE_CHARACTERISTICS.get(age_group, AGE_CHARACTERISTICS["中班"])

    if api_key:
        return _llm_generate("observation", age_group=age_group, query=query,
                             age_info=age_info, api_key=api_key, api_base=api_base, model=model)

    record = {
        "观察时间": datetime.now().strftime("%Y年%m月%d日"),
        "观察对象": query[:6] if len(query) > 6 else query,
        "年龄段": age_group,
        "观察背景": f"在{query[:10]}的活动中，注意到幼儿的特殊行为表现。",
        "观察实录": f"在今天的自由活动中，{query}。该幼儿表现出明显的参与兴趣，主动探索周围环境。在与同伴互动时，能使用简单的语言表达自己的想法。整个过程持续了约15分钟。",
        "行为分析": {
            "发展领域": "社会性发展 / 语言发展",
            "年龄特点对照": f"{age_group}({age_info['年龄']})幼儿的典型表现：{age_info['特点'][0]}。",
            "进步点": "表现出自主性和探索欲，是良好的发展信号。",
            "待关注点": "可进一步观察在群体活动中的表现。",
        },
        "教育策略": [
            "创设更多支持性环境，提供丰富的操作材料",
            "在集体活动中给予积极关注和适当引导",
            "通过游戏化方式帮助幼儿提升相关能力",
        ],
        "家园共育建议": "建议家长在家中提供类似的活动机会，鼓励幼儿大胆尝试。",
    }
    return record


def generate_communication(query, sub_type="通知", api_key=None, api_base=None, model=None):
    """生成家园沟通文案（家长通知/期末评语/家长会发言稿）"""
    if api_key:
        return _llm_generate("communication", query=query, sub_type=sub_type,
                             api_key=api_key, api_base=api_base, model=model)

    templates = {
        "通知": f"""【家园通知】
尊敬的家长：
您好！
关于"{query}"，特此通知如下：
一、请您配合以下事项：
1. 帮助孩子做好相关准备
2. 关注班级群后续通知
二、时间安排：请留意后续具体时间
三、如有疑问请及时与老师沟通。
感谢您的支持与配合！
XX幼儿园 XX班
{datetime.now().strftime('%Y年%m月%d日')}""",

        "评语": f"""【幼儿期末评语】
亲爱的{query}小朋友：
这个学期你表现得真棒！老师看到你在各方面都有了很大的进步。
在集体活动中，你能积极举手发言，大胆表达自己的想法。
在和同伴相处时，你学会了分享和轮流，交到了好多好朋友。
在生活自理方面，你能够自己穿脱衣服、整理书包，越来越能干了。
新的学期，老师期待你继续保持好奇心，探索更多有趣的事情。
加油！你是最棒的！
爱你的 XX老师
{datetime.now().strftime('%Y年%m月')}""",

        "发言稿": f"""【家长会发言稿】——{query}

尊敬的各位家长：
大家好！感谢各位在百忙之中抽出时间参加本次家长会。

一、班级情况介绍
本学期班级共有XX名幼儿，孩子们在各方面都取得了可喜的进步。

二、本学期重点
1. 培养良好的生活习惯
2. 发展语言表达能力
3. 促进社会交往能力
4. 激发学习探索兴趣

三、家园配合
1. 坚持每天亲子阅读15分钟
2. 鼓励孩子自己的事情自己做
3. 关注班级通知，积极参与亲子活动

四、互动交流
接下来请各位家长提问交流...

谢谢大家！""",
    }

    return templates.get(sub_type, templates["通知"])


def generate_activity(age_group, query, api_key=None, api_base=None, model=None):
    """生成活动设计方案"""
    age_info = AGE_CHARACTERISTICS.get(age_group, AGE_CHARACTERISTICS["中班"])

    if api_key:
        return _llm_generate("activity", age_group=age_group, query=query,
                             age_info=age_info, api_key=api_key, api_base=api_base, model=model)

    activity = {
        "活动名称": query,
        "适用年龄": f"{age_group}({age_info['年龄']})",
        "活动类型": "主题活动 / 游戏活动",
        "活动目标": [
            f"认知目标：了解{query}的基本元素",
            f"能力目标：在参与中发展{age_group}幼儿的动作/语言/社交能力",
            "情感目标：体验集体活动的快乐",
        ],
        "活动准备": [
            "场地布置：设置活动区域",
            f"材料准备：{query}相关道具、背景音乐、奖励贴纸",
        ],
        "活动流程": {
            "热身环节（5分钟）": f"音乐律动导入，激发幼儿参与{query}的兴趣",
            "主题环节（15-20分钟）": [
                f"环节一：{query}主题讲解/展示（5分钟）",
                f"环节二：幼儿参与{query}（10分钟）",
                "环节三：成果展示与分享（5分钟）",
            ],
            "放松环节（5分钟）": "轻柔音乐，放松身体，回顾活动要点",
        },
        "注意事项": [
            "确保活动区域安全",
            f"关注{age_group}幼儿注意力时长",
            "为能力较弱幼儿提供支持",
        ],
        "延伸建议": [
            "在区域角投放相关材料",
            "鼓励幼儿在家与家长一起完成类似活动",
        ],
    }
    return activity


def generate_plan(plan_type, query, api_key=None, api_base=None, model=None):
    """生成教学计划（学期/月/周/日）"""
    if api_key:
        return _llm_generate("plan", plan_type=plan_type, query=query,
                             api_key=api_key, api_base=api_base, model=model)

    plans = {
        "学期计划": {
            "计划类型": "学期计划",
            "主题": query,
            "时间段": f"{datetime.now().year}年春季学期",
            "总目标": f"围绕'{query}'主题，促进幼儿在健康、语言、社会、科学、艺术五大领域的全面发展。",
            "月安排": {
                "第一月": "主题导入，建立基础认知",
                "第二月": "深入探索，开展主题活动",
                "第三月": "拓展延伸，综合运用",
                "第四月": "总结展示，成果汇报",
            },
            "家园共育": "每月一次亲子活动，配合主题开展",
        },
        "月计划": {
            "计划类型": "月计划",
            "主题": query,
            "时间段": datetime.now().strftime("%Y年%m月"),
            "周安排": {
                "第一周": f"主题导入：认识{query}",
                "第二周": f"深入探究：{query}的秘密",
                "第三周": f"拓展活动：{query}真好玩",
                "第四周": f"展示分享：我的{query}",
            },
        },
        "周计划": {
            "计划类型": "周计划",
            "主题": query,
            "每日安排": {
                "周一": {"上午": "主题活动导入", "下午": "区域活动"},
                "周二": {"上午": "五大领域集体教学", "下午": "户外活动"},
                "周三": {"上午": "游戏活动", "下午": "艺术活动"},
                "周四": {"上午": "科学探究活动", "下午": "阅读活动"},
                "周五": {"上午": "一周回顾总结", "下午": "自由游戏"},
            },
        },
        "日计划": {
            "计划类型": "日计划",
            "主题": query,
            "一日流程": {
                "7:30-8:00": "入园接待，晨检",
                "8:00-8:30": "晨间活动，自由游戏",
                "8:30-9:00": "早操/户外活动",
                "9:00-9:30": "集体教学活动（一）",
                "9:30-10:00": "如厕、喝水、点心",
                "10:00-10:30": "集体教学活动（二）",
                "10:30-11:00": "区域活动/自主游戏",
                "11:00-11:30": "午餐准备，餐前活动",
                "11:30-12:00": "午餐",
                "12:00-14:30": "午睡",
                "14:30-15:00": "起床、整理、午点",
                "15:00-15:30": "下午游戏活动",
                "15:30-16:00": "离园准备",
                "16:00-16:30": "离园",
            },
        },
    }
    return plans.get(plan_type, plans["周计划"])


def generate_environment(query, api_key=None, api_base=None, model=None):
    """生成环境创设方案"""
    if api_key:
        return _llm_generate("environment", query=query,
                             api_key=api_key, api_base=api_base, model=model)

    env = {
        "方案名称": f"{query}主题环境创设方案",
        "设计理念": f"以'{query}'为主题，营造温馨、安全、富有教育意义的班级环境，支持和促进幼儿的主动学习与发展。",
        "区域规划": {
            "主题墙": {
                "位置": "教室主墙面",
                "内容": f"展示{query}相关图片、幼儿作品、知识板",
                "材料": "彩色卡纸、图片打印、幼儿手工作品",
                "高度": "120-150cm（幼儿视线范围）",
            },
            "美工区": {
                "功能": "绘画、手工、泥工",
                "材料": f"画纸、水彩笔、彩泥、{query}相关素材",
            },
            "阅读区": {
                "功能": "阅读、讲述",
                "材料": f"{query}相关绘本、故事书、布偶",
            },
            "建构区": {
                "功能": "搭建、构造",
                "材料": f"积木、乐高、辅助材料（{query}主题）",
            },
            "角色区": {
                "功能": "角色扮演、社会交往",
                "材料": f"与{query}主题相关的角色服装、道具",
            },
        },
        "配色方案": {
            "主色调": "温馨暖色系（浅粉、淡绿、天蓝）",
            "点缀色": "明亮黄色跳色",
            "原则": "柔和、不刺眼、有助于幼儿情绪稳定",
        },
        "安全要求": [
            "所有装饰物固定牢固，防止掉落",
            "材料无毒无害，符合幼儿安全标准",
            "尖锐边角做软包处理",
            "电源插座安装保护盖",
        ],
    }
    return env


def generate_reflection(query, api_key=None, api_base=None, model=None):
    """生成教学反思"""
    if api_key:
        return _llm_generate("reflection", query=query,
                             api_key=api_key, api_base=api_base, model=model)

    reflection = {
        "活动名称": query,
        "反思时间": datetime.now().strftime("%Y年%m月%d日"),
        "亮点与成功之处": [
            "幼儿参与积极性高，大部分幼儿能专注投入活动",
            "活动设计贴近幼儿生活经验，易于理解和接受",
            "游戏化方式有效激发了幼儿的学习兴趣",
        ],
        "不足与改进": [
            "部分环节时间分配可以更合理，导入环节可适当缩短",
            "针对能力较弱幼儿的支持策略需要更加具体",
            "材料投放可以更加丰富多样，满足不同幼儿需求",
        ],
        "幼儿表现分析": {
            "积极参与型": "约60%幼儿积极举手发言，乐于参与操作",
            "观望型": "约25%幼儿需要教师引导后才参与",
            "退缩型": "约15%幼儿需要一对一支持",
        },
        "改进措施": [
            "缩短集体讲解时间，增加幼儿操作时间",
            "分层设计操作材料，满足不同能力水平幼儿",
            "增加小组合作环节，促进同伴互助学习",
            "活动后及时记录幼儿表现，为后续教学提供依据",
        ],
        "下一步计划": f"基于本次反思，下次活动将重点关注个体差异，提供更精准的教学支持。",
    }
    return reflection


def generate_story(age_group, query, api_key=None, api_base=None, model=None):
    """生成幼儿故事"""
    age_info = AGE_CHARACTERISTICS.get(age_group, AGE_CHARACTERISTICS["中班"])

    if api_key:
        return _llm_generate("story", age_group=age_group, query=query,
                             age_info=age_info, api_key=api_key, api_base=api_base, model=model)

    story = {
        "故事名称": query,
        "适用年龄": f"{age_group}({age_info['年龄']})",
        "教育价值": f"通过{query}的故事，培养幼儿勇敢、善良、乐于助人的品质，发展语言理解和表达能力。",
        "故事正文": f"""从前，有一只可爱的小动物，它叫{query}。
有一天，阳光明媚，{query}决定去森林里探险。
走着走着，它来到了一个神秘的地方。这里的花儿五颜六色，鸟儿唱着动听的歌。
{query}好奇地东看看西瞧瞧，发现前面有一条小河挡住了去路。
"怎么办呢？"它想了想，看到旁边有一些大石头，于是小心翼翼地踩着石头过了河。
对岸的景色更加美丽！{query}高兴极了。
天快黑了，{query}原路返回，把今天的奇遇告诉了妈妈。
妈妈微笑着摸摸它的头说："你真是一个勇敢的好孩子！"
{query}开心地笑了，带着甜甜的笑容进入了梦乡。""",
        "互动提问": [
            f"故事的主人公是谁呀？（{query}）",
            f"{query}遇到了什么困难？（小河挡住了去路）",
            f"{query}是怎么过河的？（踩着石头过的）",
            "你觉得它是一只怎样的小动物？",
        ],
        "延伸活动": [
            "请幼儿画一画故事中的场景",
            "让幼儿讲述自己勇敢的探险经历",
            "角色扮演：分角色表演故事",
        ],
    }
    return story


def generate_report(query, api_key=None, api_base=None, model=None):
    """生成综合报告"""
    return {
        "综合报告": {
            "主题": query,
            "生成时间": datetime.now().strftime("%Y年%m月%d日 %H:%M"),
            "包含模块": [
                "教案：配套五大领域教学活动设计",
                "观察记录：幼儿典型行为表现记录模板",
                "家园通知：家长沟通文案",
                "环创方案：主题环境创设建议",
            ],
            "建议": "如需各模块详细内容，请分别使用对应的 --mode 参数生成。",
        }
    }


# ───────────────────────── LLM 增强 ─────────────────────────

def _llm_generate(template_type, **kwargs):
    """使用 LLM API 增强内容生成"""
    api_key = kwargs.pop("api_key")
    api_base = kwargs.pop("api_base", "https://api.openai.com/v1")
    model = kwargs.pop("model", "gpt-4o-mini")

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=api_base)

        prompts = {
            "lesson_plan": f"""你是资深幼儿园教师，请为{kwargs.get('age_group', '中班')}幼儿生成一份{kwargs.get('domain', '语言')}领域的教案。
主题：{kwargs.get('query', '')}
要求：包含活动目标、活动准备、活动过程、指导要点、家园共育。输出Markdown格式。
年龄特点：{json.dumps(kwargs.get('age_info', {}), ensure_ascii=False)}
指南要求：{json.dumps(kwargs.get('domain_info', {}), ensure_ascii=False)}""",

            "observation": f"""你是资深幼儿园教师，请为{kwargs.get('age_group', '中班')}幼儿生成一份观察记录。
行为描述：{kwargs.get('query', '')}
输出格式：观察实录、行为分析、教育策略、家园共育建议。使用Markdown格式。""",

            "communication": f"""你是资深幼儿园教师，请生成一份幼儿园{kwargs.get('sub_type', '通知')}文案。
主题：{kwargs.get('query', '')}
使用专业、温暖、亲切的语气。输出Markdown格式。""",

            "activity": f"""你是资深幼儿园教师，请为{kwargs.get('age_group', '中班')}幼儿设计一个主题活动。
主题：{kwargs.get('query', '')}
包含：活动目标、活动准备、活动流程、注意事项、延伸建议。输出Markdown格式。""",

            "plan": f"""你是资深幼儿园教师，请生成一份幼儿园{kwargs.get('plan_type', '周计划')}。
主题：{kwargs.get('query', '')}
输出Markdown格式的计划安排。""",

            "environment": f"""你是资深幼儿园环创设计师，请设计一份班级环境创设方案。
主题：{kwargs.get('query', '')}
包含：设计理念、区域规划、配色方案、材料清单、安全要求。输出Markdown格式。""",

            "reflection": f"""你是资深幼儿园教师，请撰写一份教学反思。
活动：{kwargs.get('query', '')}
包含：亮点、不足、幼儿表现分析、改进措施、下一步计划。输出Markdown格式。""",

            "story": f"""你是资深幼儿故事作者，请为{kwargs.get('age_group', '中班')}幼儿创作一个短篇故事。
主题：{kwargs.get('query', '')}
要求：200-400字，语言简单亲切，有教育意义，适合{kwargs.get('age_group', '中班')}幼儿。输出Markdown格式。""",
        }

        prompt = prompts.get(template_type, prompts["lesson_plan"])
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
        )
        return {"llm_generated": response.choices[0].message.content}
    except ImportError:
        return {"error": "请安装 openai 库：pip install openai"}
    except Exception as e:
        return {"error": f"LLM API 调用失败：{str(e)}"}


# ───────────────────────── HTML 报告生成 ─────────────────────────

def generate_html_report(result, mode, query, api_used=False):
    """生成交互式HTML可视化报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    now_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    # 模块标题映射
    mode_titles = {
        "lesson_plan": "教案生成",
        "observation": "观察记录",
        "communication": "家园共育",
        "activity": "活动设计",
        "plan": "教学计划",
        "environment": "环境创设",
        "reflection": "教学反思",
        "story": "故事创作",
        "report": "综合报告",
        "demo": "功能演示",
    }

    title = mode_titles.get(mode, "幼教百宝箱")
    tag = "LLM增强" if api_used else "内置模板"

    # 构建左侧导航
    nav_items = "\n".join([
        f'<a href="#" class="nav-item active" data-section="overview">{k}</a>'
        for k in mode_titles.values()
    ])

    # 构建内容卡片
    content_html = _build_content_html(result)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>幼教百宝箱 - {title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; background: #fef9f4; color: #333; line-height: 1.6; }}
.header {{ background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #a1c4fd 100%); padding: 30px 20px; text-align: center; color: #fff; }}
.header h1 {{ font-size: 2em; margin-bottom: 5px; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); }}
.header .subtitle {{ font-size: 1.1em; opacity: 0.95; }}
.header .badge {{ display: inline-block; background: rgba(255,255,255,0.3); padding: 4px 12px; border-radius: 20px; margin-top: 8px; font-size: 0.85em; }}
.container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
.card {{ background: #fff; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); transition: transform 0.2s; }}
.card:hover {{ transform: translateY(-2px); }}
.card h2 {{ font-size: 1.4em; color: #ff6b81; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 2px solid #ffdfe4; }}
.card h3 {{ font-size: 1.1em; color: #555; margin: 12px 0 8px; }}
.section-title {{ display: flex; align-items: center; gap: 8px; margin-bottom: 15px; }}
.section-title .icon {{ font-size: 1.5em; }}
.info-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px; }}
.info-tag {{ background: #fff0f3; color: #ff6b81; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; }}
.content-block {{ background: #fdf6f9; border-radius: 12px; padding: 18px; margin: 12px 0; }}
.content-block p {{ margin: 6px 0; }}
.content-block ul, .content-block ol {{ padding-left: 20px; }}
.content-block li {{ margin: 4px 0; }}
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
@media (max-width: 600px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
.progress-bar {{ height: 8px; background: #f0f0f0; border-radius: 4px; margin: 8px 0; overflow: hidden; }}
.progress-fill {{ height: 100%; border-radius: 4px; background: linear-gradient(90deg, #ff9a9e, #fecfef); }}
.quote {{ border-left: 4px solid #ff9a9e; padding: 10px 15px; margin: 10px 0; background: #fff0f3; border-radius: 0 8px 8px 0; font-style: italic; }}
.footer {{ text-align: center; padding: 30px 20px; color: #999; font-size: 0.85em; }}
.footer a {{ color: #ff6b81; text-decoration: none; }}
/* 模块导航 */
.module-nav {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }}
.module-btn {{ padding: 8px 16px; border-radius: 20px; border: 2px solid #ffdfe4; background: #fff; color: #ff6b81; cursor: pointer; font-size: 0.9em; transition: all 0.2s; }}
.module-btn:hover, .module-btn.active {{ background: #ff6b81; color: #fff; border-color: #ff6b81; }}
.daily-tip {{ background: linear-gradient(135deg, #a1c4fd, #c2e9fb); padding: 20px; border-radius: 16px; margin-bottom: 20px; color: #fff; }}
.daily-tip h3 {{ margin-bottom: 8px; }}
</style>
</head>
<body>

<div class="header">
    <h1>🌸 幼教百宝箱</h1>
    <div class="subtitle">AI 幼师全流程助手 — {title}</div>
    <div class="badge">{tag} | 生成时间：{now_str}</div>
</div>

<div class="container">
    <!-- 今日提醒 -->
    <div class="daily-tip">
        <h3>💡 今日幼教小贴士</h3>
        <p>观察是最好的教育。今天试着记录下3个幼儿的"哇时刻"，你会惊喜地发现每个孩子都在以自己的方式成长。</p>
    </div>

    <!-- 模块导航 -->
    <div class="module-nav">
        <button class="module-btn active" onclick="scrollToTop()">📝 {title}</button>
        <button class="module-btn" onclick="alert('请使用 --mode lesson_plan 生成教案')">📖 教案</button>
        <button class="module-btn" onclick="alert('请使用 --mode observation 生成观察记录')">🔍 观察</button>
        <button class="module-btn" onclick="alert('请使用 --mode communication 生成家园沟通')">💬 沟通</button>
        <button class="module-btn" onclick="alert('请使用 --mode activity 生成活动')">🎮 活动</button>
        <button class="module-btn" onclick="alert('请使用 --mode plan 生成计划')">📅 计划</button>
        <button class="module-btn" onclick="alert('请使用 --mode environment 生成环创')">🎨 环创</button>
        <button class="module-btn" onclick="alert('请使用 --mode story 生成故事')">📚 故事</button>
    </div>

    <!-- 内容区域 -->
    {content_html}
</div>

<div class="footer">
    <p>🌸 幼教百宝箱 | AI 赋能幼师，让教育更美好</p>
    <p>基于《3-6岁儿童学习与发展指南》 | Powered by WorkBuddy</p>
</div>

<script>
function scrollToTop() {{ window.scrollTo({{ top: 0, behavior: 'smooth' }}); }}
// Module buttons highlight
document.querySelectorAll('.module-btn').forEach(btn => {{
    btn.addEventListener('click', function() {{
        document.querySelectorAll('.module-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
    }});
}});
</script>

</body>
</html>"""
    return html


def _build_content_html(result):
    """递归构建内容HTML"""
    if isinstance(result, str):
        return f'<div class="content-block"><p>{result}</p></div>'
    if isinstance(result, list):
        items = "\n".join([f"<li>{_fmt_val(item)}</li>" for item in result])
        return f'<div class="content-block"><ul>{items}</ul></div>'
    if isinstance(result, dict):
        if "llm_generated" in result:
            return f'<div class="content-block"><pre style="white-space: pre-wrap; font-family: inherit;">{result["llm_generated"]}</pre></div>'
        if "error" in result:
            return f'<div class="content-block" style="background:#fff0f0;"><p style="color:#e74c3c;">❌ {result["error"]}</p></div>'

        html = ""
        for key, val in result.items():
            if isinstance(val, dict):
                html += f'<div class="card"><h2>📌 {key}</h2>'
                for sub_key, sub_val in val.items():
                    html += f'<h3>{sub_key}</h3>'
                    html += _build_content_html(sub_val)
                html += '</div>'
            elif isinstance(val, list):
                html += f'<div class="card"><h2>📌 {key}</h2>'
                html += _build_content_html(val)
                html += '</div>'
            else:
                html += f'<div class="card"><h2>📌 {key}</h2><div class="content-block"><p>{_fmt_val(val)}</p></div></div>'
        return html
    return f'<p>{str(result)}</p>'


def _fmt_val(val):
    """格式化值"""
    if isinstance(val, list):
        return "<br>".join([f"• {v}" for v in val])
    return str(val).replace("\n", "<br>")


# ───────────────────────── Demo 模式 ─────────────────────────

def run_demo():
    """运行演示模式，展示所有功能"""
    results = {}

    results["教案生成示例"] = generate_lesson_plan("语言", "中班", "春天的色彩")
    results["观察记录示例"] = generate_observation("小班", "小明在积木区主动分享玩具给同伴")
    results["家长通知示例"] = generate_communication("春游活动通知", "通知")
    results["期末评语示例"] = generate_communication("朵朵", "评语")
    results["活动设计示例"] = generate_activity("大班", "端午节主题游戏")
    results["周计划示例"] = generate_plan("周计划", "春天来了")
    results["环创方案示例"] = generate_environment("海底世界")
    results["教学反思示例"] = generate_reflection("科学活动：浮与沉")
    results["故事创作示例"] = generate_story("小班", "勇敢的小白兔")

    return results


# ───────────────────────── 主流程 ─────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🌸 幼教百宝箱 — AI幼师全流程助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
示例：
  %(prog)s --mode demo                          # 演示所有功能
  %(prog)s --mode lesson_plan --domain 语言 --age 中班 --query "春天"
  %(prog)s --mode observation --age 小班 --query "主动分享玩具"
  %(prog)s --mode communication --query "亲子运动会通知" --sub 通知
  %(prog)s --mode activity --age 大班 --query "端午节游戏"
  %(prog)s --mode plan --plan_type 周计划 --query "春天来了"
  %(prog)s --mode environment --query "海底世界环创"
  %(prog)s --mode reflection --query "科学活动浮沉实验"
  %(prog)s --mode story --age 小班 --query "勇敢的小兔子"
  %(prog)s --mode report --query "春天主题综合方案"
        """),
    )

    parser.add_argument("--mode", "-m", required=True,
                        choices=["demo", "lesson_plan", "observation", "communication",
                                 "activity", "plan", "environment", "reflection", "story", "report"],
                        help="功能模式")
    parser.add_argument("--query", "-q", default="", help="用户输入内容")
    parser.add_argument("--domain", "-d", choices=["健康", "语言", "社会", "科学", "艺术"], default="语言",
                        help="教案领域（仅 lesson_plan 模式）")
    parser.add_argument("--age", "-a", choices=["小班", "中班", "大班"], default="中班",
                        help="年龄段")
    parser.add_argument("--sub", choices=["通知", "评语", "发言稿"], default="通知",
                        help="家园沟通子类型（仅 communication 模式）")
    parser.add_argument("--plan_type", "-p", choices=["学期计划", "月计划", "周计划", "日计划"], default="周计划",
                        help="计划类型（仅 plan 模式）")
    parser.add_argument("--api-key", help="LLM API Key（可选，用于LLM增强生成）")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="LLM API Base URL")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM 模型名称")
    parser.add_argument("--output", "-o", help="输出HTML文件路径（默认自动生成）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式到stdout")

    args = parser.parse_args()
    api_key = args.api_key
    api_base = args.api_base
    model = args.model
    api_used = False

    # 执行对应模式
    if args.mode == "demo":
        result = run_demo()
        api_used = False
    elif args.mode == "lesson_plan":
        result = generate_lesson_plan(args.domain, args.age, args.query or "主题活动",
                                      api_key, api_base, model)
        api_used = bool(api_key and "llm_generated" in result)
    elif args.mode == "observation":
        result = generate_observation(args.age, args.query or "幼儿行为观察",
                                      api_key, api_base, model)
        api_used = bool(api_key and "llm_generated" in result)
    elif args.mode == "communication":
        result = generate_communication(args.query or "家园沟通", args.sub,
                                        api_key, api_base, model)
        api_used = bool(api_key and isinstance(result, dict) and "llm_generated" in result)
    elif args.mode == "activity":
        result = generate_activity(args.age, args.query or "主题活动",
                                   api_key, api_base, model)
        api_used = bool(api_key and "llm_generated" in result)
    elif args.mode == "plan":
        result = generate_plan(args.plan_type, args.query or "教学计划",
                               api_key, api_base, model)
        api_used = bool(api_key and "llm_generated" in result)
    elif args.mode == "environment":
        result = generate_environment(args.query or "环境创设",
                                      api_key, api_base, model)
        api_used = bool(api_key and "llm_generated" in result)
    elif args.mode == "reflection":
        result = generate_reflection(args.query or "教学反思",
                                     api_key, api_base, model)
        api_used = bool(api_key and "llm_generated" in result)
    elif args.mode == "story":
        result = generate_story(args.age, args.query or "幼儿故事",
                                api_key, api_base, model)
        api_used = bool(api_key and "llm_generated" in result)
    elif args.mode == "report":
        result = generate_report(args.query or "综合报告",
                                 api_key, api_base, model)
        api_used = bool(api_key)

    # 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = args.output or f"preschool_teacher_{args.mode}_{timestamp}.html"
        html = generate_html_report(result, args.mode, args.query, api_used)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ 报告已生成：{output_path}")
        print(f"📄 模式：{args.mode} | 标签：{'LLM增强' if api_used else '内置模板'}")

    # 额外打印结构化摘要
    if not args.json and args.mode != "demo":
        print("\n" + "=" * 50)
        print("📋 内容预览：")
        _print_preview(result)


def _print_preview(result, indent=0):
    """打印内容预览"""
    prefix = "  " * indent
    if isinstance(result, dict):
        for k, v in result.items():
            if isinstance(v, (dict, list)):
                print(f"{prefix}📌 {k}:")
                _print_preview(v, indent + 1)
            else:
                val_str = str(v)[:80]
                print(f"{prefix}📌 {k}: {val_str}")
    elif isinstance(result, list):
        for item in result[:3]:
            print(f"{prefix}• {str(item)[:80]}")
        if len(result) > 3:
            print(f"{prefix}• ...共{len(result)}项")


if __name__ == "__main__":
    main()
