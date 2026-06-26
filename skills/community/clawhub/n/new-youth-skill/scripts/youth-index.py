#!/usr/bin/env python3
"""
新青年指数计算器 | Youth Index Calculator

输入用户在六个维度的自评分（每个维度1-5分）
输出总分、等级、改进建议
"""

# 新青年六条标准
STANDARDS = [
    ("自主", "autonomy", "独立思考，不盲从权威"),
    ("进步", "progress", "拥抱变化，持续进化"),
    ("进取", "enterprise", "主动出击，向前一步"),
    ("世界", "global", "开放视野，跨文化理解"),
    ("实利", "pragmatic", "行动导向，解决问题"),
    ("科学", "scientific", "事实优先，逻辑驱动"),
]

LEVELS = [
    (27, "🌱 新青年典范", "你是六条标准的践行者，继续保持！"),
    (24, "🌿 接近新青年", "大部分维度达标，有1-2个短板可以重点提升。"),
    (18, "🌾 尚需精进", "有明显短板，需要针对性提升。"),
    (0, "🌰 亟需觉醒", "需要系统性地反思和行动，从最低分的维度开始。"),
]

IMPROVEMENT_TIPS = {
    "autonomy": "每天问自己：'这是我自己的判断还是别人告诉我的？'",
    "progress": "每周尝试一件新事物，不管多小。",
    "enterprise": "不要等机会，主动创造机会。",
    "global": "每天花10分钟了解一个不同文化或观点。",
    "pragmatic": "把想法立刻转化为'今天可以做的第一件事'。",
    "scientific": "遇到观点先问'证据是什么？'",
}


def calculate_youth_index(scores: dict) -> dict:
    """
    计算新青年指数
    
    Args:
        scores: dict, keys are autonym/global/..., values are 1-5
        
    Returns:
        dict with total, level, level_name, improvement_tips
    """
    if not scores:
        return {"error": "请提供评分数据"}
    
    # 验证分数范围
    for key, value in scores.items():
        if not 1 <= value <= 5:
            return {"error": f"{key} 评分必须在 1-5 之间"}
    
    # 计算总分
    total = sum(scores.values())
    
    # 确定等级
    level_name = LEVELS[-1][1]
    level_desc = LEVELS[-1][2]
    for threshold, name, desc in LEVELS:
        if total >= threshold:
            level_name = name
            level_desc = desc
            break
    
    # 找出最低分维度
    sorted_scores = sorted(scores.items(), key=lambda x: x[1])
    lowest_dims = sorted_scores[:2]  # 取最低的2个
    
    # 生成改进建议
    tips = []
    for dim_key, dim_score in lowest_dims:
        for zh, en, meaning in STANDARDS:
            if en == dim_key:
                tips.append(f"- **{zh}**（{meaning}）：{IMPROVEMENT_TIPS[dim_key]}")
                break
    
    return {
        "total": total,
        "max": 30,
        "level": level_name,
        "description": level_desc,
        "scores": scores,
        "improvement_tips": tips,
    }


def format_output(result: dict) -> str:
    """格式化输出"""
    if "error" in result:
        return f"错误：{result['error']}"
    
    lines = [
        "=" * 40,
        "🌱 新青年指数报告",
        "=" * 40,
        f"总分：{result['total']} / {result['max']}",
        f"等级：{result['level']}",
        f"评价：{result['description']}",
        "",
        "各维度评分：",
    ]
    
    for zh, en, _ in STANDARDS:
        score = result["scores"].get(en, 0)
        bar = "█" * score + "░" * (5 - score)
        lines.append(f"  {zh}：{bar} {score}")
    
    if result["improvement_tips"]:
        lines.extend(["", "📈 改进建议："])
        lines.extend(result["improvement_tips"])
    
    lines.append("=" * 40)
    return "\n".join(lines)


if __name__ == "__main__":
    # 示例评分
    example_scores = {
        "autonomy": 4,
        "progress": 3,
        "enterprise": 3,
        "global": 4,
        "pragmatic": 3,
        "scientific": 4,
    }
    
    result = calculate_youth_index(example_scores)
    print(format_output(result))
