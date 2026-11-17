#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
identity_provider.py v1.6 — 多智能体系统身份提供器

v1.6 变更:
  - 精简身份预设: 30+个"世界第一"身份 → 7个核心智能体 + 3个精确角色
  - 按 phase 注入: 生成阶段用作家身份，评审阶段用编辑身份，修正阶段用去AI身份
  - 身份从 YAML 加载（回退硬编码），避免过度夸张导致AI浮夸输出
"""

# ========== 7 大核心智能体 System Identity（v1.6: 精简过激描述） ==========

SYSTEM_IDENTITIES = {
    "story_architect": {
        "name": "故事架构专家",
        "identity": (
            "你是故事架构专家，关注因果逻辑和情绪曲线的咬合。"
            "对逻辑漏洞有本能的敏感。"
        ),
        "function": "架构/因果/情绪曲线审查",
    },
    "style_master": {
        "name": "文体大师",
        "identity": (
            "你对语言的质感有要求。对'AI味'的表达有一套具体的审美排斥清单。"
            "追求简洁有力的语言，避免空洞修饰。"
        ),
        "function": "语言质地/去AI味",
    },
    "critic": {
        "name": "评论家",
        "identity": (
            "你是一个严格的文学书评人。"
            "对陈词滥调、逻辑不清、情感虚假的内容零容忍。"
            "批评一针见血。"
        ),
        "function": "逻辑/陈词滥调审查",
    },
    "reader_agent": {
        "name": "读者代理",
        "identity": (
            "你是一个普通的、热爱此类型的资深读者。不分析技巧，只报告即时感受。"
            "有时不耐烦，有时会心一笑，有时会被感动。"
        ),
        "function": "直觉反馈/读者视角",
    },
    "detail_agent": {
        "name": "细节真实性代理",
        "identity": (
            "你关注世界真实性的细节。对模糊的通用描写不满，"
            "用具体的、有生活痕迹的细节替换空洞描述。"
        ),
        "function": "具体细节注入/真实性校验",
    },
    "reader_comments": {
        "name": "读者本章说代理",
        "identity": (
            "你是一个资深网文读者群体。会即时吐槽、猜测后续、玩梗、指出逻辑问题。"
            "反应多元真实。"
        ),
        "function": "模拟本章说/读者反馈",
    },
    "cross_platform": {
        "name": "跨平台分发专家",
        "identity": (
            "你深刻理解各主流内容平台的读者心理和流量规则。"
            "能将同一故事内核根据平台要求进行精准改写。"
        ),
        "function": "平台适配/多平台改写",
    },
}

# ========== v1.6: 按 Phase 注入的精确角色（替代 30+ 个世界第一身份） ==========

PHASE_ROLES = {
    "generate": {
        "name": "平台作家",
        "identity": (
            "你是一名经验丰富的网文作家，熟悉本平台的读者偏好和写作规范。"
            "写正文时保持自然流畅，避免模板化表达。"
        ),
        "note": "由 generator.py PLATFORM_IDENTITIES 覆盖具体平台身份",
    },
    "review": {
        "name": "资深编辑",
        "identity": (
            "你是资深网文编辑，有10年审稿经验。"
            "评审标准：逻辑自洽 > 节奏把控 > 语言质感 > AI痕迹。"
        ),
    },
    "rewrite": {
        "name": "去AI改写专家",
        "identity": (
            "你擅长消除AI痕迹。改写原则：用具体动作替代抽象情绪，"
            "用短句交替替代均匀节奏，用口语化表达替代书面语。"
        ),
    },
}

# ========== 开篇前校验 Prompt（概念解析.md 原文提取） ==========

PRE_WRITING_PROMPTS = {
    "premortem": (
        "[开篇前-事前验尸]\\n"
        "假设我们今天基于这个核心设定和总纲创作的小说，在发布后彻底失败了——"
        "读者寥寥，口碑崩坏。请作为最严厉的批评家，从以下维度为我列出所有可能的、"
        "最致命的失败原因：\\n"
        "1. 核心爽点是否已经被过度消费、令读者极度疲惫？\\n"
        "2. 主角人设是否存在致命的、会引发大规模读者反感的缺陷？\\n"
        "3. 核心冲突是否是读者毫不关心的'茶杯里的风波'？\\n"
        "4. 故事终点是否令人感到空虚、徒劳或毫无满足感？"
    ),
    "emotion_curve": (
        "[开篇前-总纲情绪曲线审计]\\n"
        "请基于我的总纲，为我绘制一条全书的'预期读者情绪曲线图'。"
        "标注出四大阶段的情绪高点、低点和转折点。然后请诊断：是否存在连续过长的、"
        "没有明显情绪起伏的'平缓地带'？情绪的高峰是否来的太晚或太早？"
        "整体的情绪节奏是否过于单一，缺乏'紧张-舒缓'的呼吸感？"
    ),
    "hook_strength": (
        "[开篇前-细纲钩子强度扫描]\\n"
        "请对我前三章的细纲进行一次逐章的'钩子强度扫描'。"
        "为每一章的章末钩子进行A（极强，不可抗拒）、B（较强，有效）、C（一般）三级评级。"
        "要求：至少两章的钩子达到A级。"
    ),
    "info_pacing": (
        "[开篇前-细纲信息释放节奏审查]\\n"
        "审查我的细纲，诊断是否存在'信息倾泻'或'信息饥渴'的问题。"
        "在前三章中，是否一次性塞给了读者过多他们目前尚不关心、也记不住的世界观设定？"
        "或者，是否让读者在极度缺乏必要信息的情况下感到困惑和挫败？"
        "请精确标出每一处信息释放过多或过少的节点，并提出调整建议。"
    ),
}

# ========== 7 维度拆书模型（全维研究报告 2.5） ==========

HIT_DIMENSIONS = {
    "core_hook": {
        "name": "核心梗/强设定",
        "standard": "30字内完成'主角身份+核心场景+独特金手指'信息压缩",
        "weight": 20,
    },
    "golden_three": {
        "name": "黄金三章节奏",
        "standard": "第一章冲突/悬念，第二章能力/人设展示，第三章目标抛出",
        "weight": 20,
    },
    "satisfaction_logic": {
        "name": "核心爽点逻辑",
        "standard": "受众分层+3-5-10波浪节奏+定向情绪痛点",
        "weight": 15,
    },
    "character_support": {
        "name": "人设支撑体系",
        "standard": "身份×反差×执念公式化设计+行为逻辑自洽",
        "weight": 15,
    },
    "hook_layout": {
        "name": "长短线钩子布局",
        "standard": "3-5章短线钩子+10章长线钩子+悬念链",
        "weight": 10,
    },
    "narrative_density": {
        "name": "叙事视角与密度",
        "standard": "有限第三人称+控制场景切换频率+防信息过载",
        "weight": 10,
    },
    "commercial_potential": {
        "name": "商业变现潜力",
        "standard": "适配平台算法逻辑+匹配付费/广告/IP变现路径",
        "weight": 10,
    },
}

# ========== 平台深度偏好表（概念解析.md 提取） ==========

PLATFORM_PREFERENCES = {
    "\u8d77\u70b9": {
        "name": "起点中文网",
        "hot_types": ["\u4e1c\u65b9\u7384\u5e7b", "\u4ed9\u4fa0\u4fee\u771f", "\u90fd\u5e02\u5f02\u80fd", "\u5386\u53f2\u67b6\u7a7a"],
        "pacing": "\u4e2d\u6162\u901f\u85c4\u529b\uff0c\u9ad8\u6f6e\u91ca\u653e\u5145\u5206",
        "opening": "\u524d50\u7ae0\u5efa\u7acb\u5b8c\u6574\u529b\u91cf\u4f53\u7cfb\u548c\u4e3b\u7ebf\u76ee\u6807\uff0c\u53ef\u94fa\u57ab\u8f83\u957f",
        "reader": "\u91cd\u5ea6\u9605\u8bfb\u8005\uff0c\u5bf9\u8bbe\u5b9a\u4e25\u8c28\u6027\u8981\u6c42\u9ad8",
        "taboo": "\u8fc7\u5ea6\u73a9\u689f/\u6c99\u96d5\u98ce\u3001\u903b\u8f91\u5d29\u574f",
    },
    "\u7ffc\u8304": {
        "name": "\u7ffc\u8304/\u756a\u8304\u5c0f\u8bf4",
        "hot_types": ["\u8d58\u5a7f/\u9690\u85cf\u8eab\u4efd", "\u90fd\u5e02\u5f02\u80fd", "\u5f3a\u8005\u91cd\u751f", "\u7cfb\u7edf\u723d\u6587"],
        "pacing": "\u5feb\u8282\u594f\uff0c\u6bcf\u7ae0\u6709\u5c0f\u51b2\u7a81\uff0c\u5f00\u7bc7\u5373\u77db\u76fe",
        "opening": "\u9ec4\u91d1\u4e00\u7ae0\u5b9a\u751f\u6b7b\uff0c3\u7ae0\u5185\u5fc5\u987b\u5b8c\u6210\u91d1\u624b\u6307+\u7b2c\u4e00\u6b21\u723d\u70b9",
        "reader": "\u788e\u7247\u5316\u9605\u8bfb\uff0c\u8010\u5fc3\u7a97\u53e3\u6781\u77ed",
        "taboo": "\u6162\u70ed\u6587\u3001\u8bbe\u5b9a\u8fc7\u4e8e\u590d\u6742\u3001\u94fa\u57ab\u8fc7\u957f\u3001\u6587\u827a\u98ce",
    },
    "\u664b\u6c5f": {
        "name": "\u664b\u6c5f\u6587\u5b66\u57ce",
        "hot_types": ["\u53e4\u4ee3\u8a00\u60c5", "\u73b0\u4ee3\u90fd\u5e02", "\u7eaf\u7231", "\u7a7f\u8d8a\u91cd\u751f", "\u7cfb\u7edf\u7a7f\u4e66"],
        "pacing": "\u60c5\u611f\u8fdb\u5c55\u4e3a\u4e3b\u7ebf\uff0c\u60c5\u8282\u51b2\u7a81\u4e3a\u8f85",
        "opening": "\u5feb\u901f\u5efa\u7acb\u4eba\u7269\u5173\u7cfb\u7684\u5f20\u529b",
        "reader": "\u6807\u7b7e\u7cbe\u51c6\u5339\u914d+\u60c5\u611f\u5171\u9e23\u9a71\u52a8\u6536\u85cf",
        "taboo": "\u60c5\u611f\u63a8\u8fdb\u8fc7\u5feb\u5bfc\u81f4\u5de5\u4e1a\u7cd6\u7cbe",
    },
    "\u77e5\u4e4e": {
        "name": "\u77e5\u4e4e\u76d0\u9009",
        "hot_types": ["\u8eab\u4efd\u53cd\u8f6c\uff08\u77ed\u7bc7\u7248\uff09", "\u60ac\u7591\u63ed\u79d8"],
        "pacing": "\u5f00\u7bc7\u5373\u60ac\u5ff5\uff0c3000\u5b57\u5185\u5b8c\u6210\u53cd\u8f6c",
        "opening": "\u5f00\u7bc7\u63d0\u95ee\u4f53\uff0c\u5bc6\u96c6\u53cd\u8f6c",
        "reader": "\u4f1a\u5458\u5236\u77ed\u7bc7\uff0c\u671f\u5f85\u5373\u65f6\u60c5\u7eea\u51b2\u51fb",
        "taboo": "\u85c4\u529b\u8d85\u8fc7\u5168\u6587\u4e00\u534a\u3001\u7ed3\u5c3e\u89e3\u91ca\u8fc7\u591a",
    },
}


def get_identity(name: str) -> str:
    """获取指定智能体的 System Identity 文本"""
    agent = SYSTEM_IDENTITIES.get(name)
    if agent:
        return f"[{agent['name']}] {agent['identity']}"
    return ""


def get_prompt(name: str) -> str:
    """获取指定开篇前 Prompt"""
    return PRE_WRITING_PROMPTS.get(name, "")


def get_platform_prefs(platform: str) -> dict:
    """获取指定平台的深度偏好"""
    return PLATFORM_PREFERENCES.get(platform, {})


def score_hit_dimensions(setting: dict) -> dict:
    """基于7维度拆书模型打分（概念验证用）"""
    scores = {}
    total = 0
    max_total = sum(d["weight"] for d in HIT_DIMENSIONS.values())
    for key, dim in HIT_DIMENSIONS.items():
        base = setting.get(key, 50)  # 外部传入评分
        weighted = base * dim["weight"] / 100
        scores[key] = {
            "dimension": dim["name"],
            "raw_score": base,
            "weighted": round(weighted, 1),
            "standard": dim["standard"],
        }
        total += weighted
    return {
        "dimensions": scores,
        "total_score": round(total / max_total * 100, 1),
        "max_possible": 100,
    }
