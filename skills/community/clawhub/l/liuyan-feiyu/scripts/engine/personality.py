"""
留言非语 — 用户人格分析引擎

在对话过程中隐性分析用户的人格模式，不使用问卷，
而是通过对话内容、表达方式、情绪模式等推断。
"""

# 分析维度
PERSONALITY_DIMENSIONS = {
    "expression_style": {
        "label": "表达风格",
        "spectrum": ["内敛克制", "外放直接"],
        "description": "用户倾向于隐藏还是直接表达情绪",
    },
    "locus_of_control": {
        "label": "归因方式",
        "spectrum": ["外归因（都是别人的错）", "内归因（都是我的错）"],
        "description": "用户把问题归因于外部还是自身",
    },
    "conflict_pattern": {
        "label": "冲突模式",
        "spectrum": ["回避", "对抗"],
        "description": "面对冲突时的本能反应",
    },
    "self_awareness": {
        "label": "自我觉察",
        "spectrum": ["低（不知道自己在干嘛）", "高（知道但做不到）"],
        "description": "对自身行为模式的认知程度",
    },
    "emotional_regulation": {
        "label": "情绪调节",
        "spectrum": ["压抑", "宣泄"],
        "description": "处理情绪的方式",
    },
    "attachment_style": {
        "label": "依恋模式",
        "spectrum": ["焦虑型", "回避型", "安全型", "混乱型"],
        "description": "在关系中的依恋倾向",
    },
    "change_readiness": {
        "label": "改变意愿",
        "spectrum": ["抗拒（只想倾诉）", "准备好了（想要行动）"],
        "description": "对改变的准备程度",
    },
}


def build_analysis_prompt(conversation_history: list) -> str:
    """
    构建人格分析提示词，让AI基于对话历史分析用户人格。
    返回一段要求AI输出JSON格式分析结果的prompt。
    """
    history_text = ""
    for msg in conversation_history:
        role = "用户" if msg["role"] == "user" else "咨询师"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""基于以下对话内容，分析用户的人格模式。

对话记录：
{history_text}

请从以下维度分析，每个维度给出 1-10 的评分和简短观察：

1. 表达风格（1=极度内敛 10=极度外放）
2. 归因方式（1=完全外归因 10=完全内归因）
3. 冲突模式（1=极度回避 10=极度对抗）
4. 自我觉察（1=完全无觉察 10=高度觉察）
5. 情绪调节（1=极度压抑 10=极度宣泄）
6. 依恋模式（焦虑/回避/安全/混乱）
7. 改变意愿（1=完全抗拒 10=迫切想改变）

同时推荐当前最适合的咨询师人设（静水/烈风/暖光/镜子/老友），并说明原因。

请用JSON格式回答：
{{
  "expression_style": {{"score": 5, "observation": "..."}},
  "locus_of_control": {{"score": 5, "observation": "..."}},
  "conflict_pattern": {{"score": 5, "observation": "..."}},
  "self_awareness": {{"score": 5, "observation": "..."}},
  "emotional_regulation": {{"score": 5, "observation": "..."}},
  "attachment_style": {{"type": "...", "observation": "..."}},
  "change_readiness": {{"score": 5, "observation": "..."}},
  "recommended_counselor": "静水",
  "counselor_reason": "...",
  "personality_summary": "用2-3句话总结这个人的核心模式"
}}
"""
    return prompt
