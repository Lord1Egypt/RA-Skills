#!/usr/bin/env python3
"""
Perspective Router — Nova 自动视角调度引擎
根据任务描述，自动匹配最合适的专家视角能力。
"""
import json, os, sys
from datetime import datetime

# ── 视角库 ─────────────────────────────────────────────────────────
PERSPECTIVES = {
    "naval": {
        "name": "Naval Ravikant",
        "skill": "naval-perspective",
        "emoji": "📈",
        "keywords": [
            "投资", "理财", "财富", "股票", "基金", "被动收入", "财务",
            "创业", "股权", "融资", "退休", "FIRE", "复利",
            "财富自由", "资产配置", "纳斯达克", "收益", "年化",
            "portfolio", "investment", "wealth", "rich", "money"
        ],
        "score_keywords": [
            "幸福", "快乐", "内心平静", "冥想", "焦虑", "欲望",
            "happiness", "peace", "meditation", "suffering", "meaning"
        ],
        "weight": 1.0,
        "description": "财富投资 · 幸福算法 · 长期复利"
    },
    "elon": {
        "name": "Elon Musk",
        "skill": "elon-musk-perspective",
        "emoji": "🚀",
        "keywords": [
            "战略", "火箭", "spacex", "tesla", "工程", "制造",
            "风险决策", "第一性原理", "颠覆", "激进", "创新",
            "技术突破", "极限制造", "可回收火箭", "电池", "AI",
            "strategy", "engineering", "risk", "first principle"
        ],
        "weight": 1.0,
        "description": "第一性原理 · 工程制造 · 颠覆式创新"
    },
    "munger": {
        "name": "Charlie Munger",
        "skill": "munger-perspective",
        "emoji": "📊",
        "keywords": [
            "多元思维模型", "逆向思考", "商业分析", "投资分析",
            "护城河", "风险评估", "概率", "决策模型", "心智模型",
            "聪明人犯错", "误判心理学", "逆向", "inversion"
        ],
        "weight": 1.0,
        "description": "多元思维模型 · 逆向分析 · 误判心理学"
    },
    "paul_graham": {
        "name": "Paul Graham",
        "skill": "paul-graham-perspective",
        "emoji": "💡",
        "keywords": [
            "创业", "产品", "idea", "创新", "写作", "nbsp",
            "y combinator", "初创公司", "创意", "startup", "product",
            "maker", "doing", "write", "essay", "founder"
        ],
        "weight": 1.0,
        "description": "创业智慧 · 写作思维 · YC经验"
    },
    "steve_jobs": {
        "name": "Steve Jobs",
        "skill": "steve-jobs-perspective",
        "emoji": "🍎",
        "keywords": [
            "产品设计", "用户体验", "品牌", "完美主义", "简约",
            "乔布斯", "产品直觉", "设计思维", "细节", "品味",
            "design", "UX", "brand", "minimal", "aesthetic", "apple"
        ],
        "weight": 1.0,
        "description": "产品设计 · 完美主义 · 品牌美学"
    },
    "zhang_yiming": {
        "name": "Zhang Yiming",
        "skill": "zhang-yiming-perspective",
        "emoji": "⚡",
        "keywords": [
            "字节跳动", "抖音", "tiktok", "推荐算法", "全球化",
            "信息流", "产品全球化", "算法推荐", "海外扩张",
            "bytedance", "algorithm", "feed", "globalization"
        ],
        "weight": 1.0,
        "description": "推荐算法 · 字节产品 · 全球化扩张"
    },
    "trump": {
        "name": "Donald Trump",
        "skill": "trump-perspective",
        "emoji": "🔥",
        "keywords": [
            "谈判", "说服", "交易", "房地产", "Deal", "谈判策略",
            "直觉", "直接感", "影响力", "nbsp",
            "negotiation", "deal", "real estate", "persuasion"
        ],
        "weight": 1.0,
        "description": "谈判策略 · 直接感 · 交易直觉"
    },
    "mrbeast": {
        "name": "MrBeast",
        "skill": "mrbeast-perspective",
        "emoji": "🎬",
        "keywords": [
            "内容创作", "youtube", "流量", "viral", "注意力经济",
            "视频", "传播", "点击率", "算法", "博主",
            "content creation", "viral", "subscriber", "views"
        ],
        "weight": 1.0,
        "description": "病毒传播 · 注意力工程 · YouTube"
    },
    "taleb": {
        "name": "Nassim Taleb",
        "skill": "taleb-perspective",
        "emoji": "🩸",
        "keywords": [
            "反脆弱", "黑天鹅", "尾部风险", "不确定性", "脆弱",
            "抗风险", "非线性", "极端斯坦", "杠铃策略",
            "antifragile", "black swan", "tail risk", "uncertainty"
        ],
        "weight": 1.0,
        "description": "反脆弱 · 黑天鹅思维 · 尾部风险"
    },
    "feynman": {
        "name": "Richard Feynman",
        "skill": "feynman-perspective",
        "emoji": "🔬",
        "keywords": [
            "科学思维", "怀疑精神", "物理学", "批判性思考",
            "第一性原理", "证伪", "科学方法",
            "science", "physics", "skepticism", "critical thinking"
        ],
        "weight": 1.0,
        "description": "科学怀疑精神 · 证伪思维 · 物理直觉"
    },
    "karpathy": {
        "name": "Andrej Karpathy",
        "skill": "andrej-karpathy-perspective",
        "emoji": "🧠",
        "keywords": [
            "深度学习", "神经网络", "AI", "机器学习", "计算机视觉",
            "NLP", "大模型", "LLM", "训练", "反向传播",
            "deep learning", "neural network", "AI", "ML", "LLM", "GPT"
        ],
        "weight": 1.0,
        "description": "深度学习 · 神经网络直觉 · AI教育"
    },
    "jobs": {
        "name": "Steve Jobs",
        "skill": "steve-jobs-perspective",
        "emoji": "🍎",
        "keywords": [
            "产品设计", "用户体验", "品牌", "完美主义", "简约",
            "乔布斯", "产品直觉", "设计思维", "细节", "品味",
            "design", "UX", "brand", "minimal", "aesthetic", "apple"
        ],
        "weight": 1.0,
        "description": "产品设计 · 完美主义 · 品牌美学"
    }
}

def score(text):
    """对一段文本打分，返回匹配的视角列表（按匹配度降序）"""
    text_lower = text.lower()
    scores = {}
    for pid, p in PERSPECTIVES.items():
        kws = p.get("keywords", [])
        score_kws = p.get("score_keywords", [])
        kw_count = sum(1 for kw in kws if kw.lower() in text_lower)
        score_count = sum(2 for kw in score_kws if kw.lower() in text_lower)  # 高权重关键词×2
        scores[pid] = (kw_count + score_count) * p.get("weight", 1.0)
    
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return ranked

def route(task_text, top_n=3):
    """
    主路由函数
    输入: 任务描述文本
    输出: [(perspective_id, score, perspective_info), ...]
    """
    if not task_text or len(task_text.strip()) < 5:
        return []
    
    ranked = score(task_text)
    results = []
    for pid, s in ranked[:top_n]:
        if s > 0:
            results.append((pid, s, PERSPECTIVES[pid]))
    return results

def build_prompt(task_text, matches):
    """根据匹配结果，构建给 Nova 的分析指令"""
    if not matches:
        return None
    
    lines = [
        f"【Perspective Router · 视角自动调度结果】",
        f"任务：「{task_text[:80]}{'...' if len(task_text)>80 else ''}」",
        f"",
        f"匹配到 {len(matches)} 个专家视角：",
    ]
    
    for i, (pid, score, p) in enumerate(matches, 1):
        skill_path = f"/workspace/skills/{p['skill']}/SKILL.md"
        skill_exists = os.path.exists(skill_path)
        lines.append(f"")
        lines.append(f"【{i}】{p['emoji']} {p['name']} — {p['description']}")
        lines.append(f"   匹配度：{score:.1f}分 | Skill：{p['skill']} {'✅' if skill_exists else '❌未安装'}")
        if skill_exists:
            lines.append(f"   📖 调用方式：读取 {skill_path}，以该专家身份分析任务")
        else:
            lines.append(f"   ⚠️ Skill 未安装，跳过此视角")
    
    if len(matches) < 1:
        return None
    
    primary = matches[0]
    lines.append(f"")
    lines.append(f"【主要视角】{primary[2]['emoji']} {primary[2]['name']}")
    lines.append(f"建议优先调用 {primary[2]['skill']}，以该专家身份分析后，")
    lines.append(f"整合进 Nova 的主回复中（作为参考视角，非主导）。")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"⚠️ 注意：Perspective 是工具，不是结论。Nova 最终判断优先。")
    
    return "\n".join(lines)

# ── CLI 接口 ───────────────────────────────────────────────────────
if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not task:
        # 无参数时输出使用说明
        print("Perspective Router — Nova 视角调度引擎")
        print("用法: python3 router.py <任务描述>")
        print(f"可用视角: {len(PERSPECTIVES)} 个")
        for pid, p in PERSPECTIVES.items():
            print(f"  {p['emoji']} {p['name']}: {p['description']}")
        sys.exit(0)
    
    matches = route(task, top_n=3)
    if not matches:
        print(f"[Perspective Router] 未匹配到任何视角，请手动选择。")
        sys.exit(0)
    
    result = build_prompt(task, matches)
    print(result)
    
    # 输出结构化 JSON（供 Nova 解析）
    output = {
        "task": task[:100],
        "matches": [
            {"id": pid, "score": s, "name": p["name"], "skill": p["skill"], "emoji": p["emoji"]}
            for pid, s, p in matches
        ],
        "primary": {"id": matches[0][0], "skill": matches[0][2]["skill"], "emoji": matches[0][2]["emoji"]}
    }
    print("\n__JSON__", json.dumps(output, ensure_ascii=False))
