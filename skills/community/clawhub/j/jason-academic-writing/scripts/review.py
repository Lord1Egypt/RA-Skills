#!/usr/bin/env python3
"""
Multi-Agent Review System - 5-person panel with quantified scoring.

Agents:
- Editor-in-Chief (contribution, journal fit) — 30% weight
- Methodology Reviewer (methods, stats, reproducibility) — 25% weight
- Domain Reviewer (related work, theory) — 20% weight
- Devil's Advocate (strongest counter-arguments) — 15% weight
- Synthesizer (merge opinions, create revision roadmap) — 10% weight
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_CLIENT = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL'),
    timeout=90.0
)
LLM_MODEL = os.getenv('LLM_MODEL', 'qwen3.5-plus')

REVIEWER_WEIGHTS = {
    'editor': 0.30,
    'methodology': 0.25,
    'domain': 0.20,
    'devil_advocate': 0.15,
    'synthesizer': 0.10
}

REVIEWER_PROMPTS = {

    'editor': """你是顶级期刊的主编审稿人（Editor-in-Chief）。你的职责是评估论文的整体学术贡献和期刊拟合度。

**评分标准**（总分100分）：

1. **新颖性**（25分）：
   - 22-25分：提出了全新的研究视角或方法，填补了重要空白
   - 18-21分：在已有方向上有实质性推进
   - 14-17分：对已知方法的增量改进
   - 10-13分：重复已有研究，无明显创新
   - 0-9分：毫无新意

2. **重要性**（25分）：
   - 22-25分：对该领域有深远影响，可能改变实践或认知
   - 18-21分：对领域有实际贡献，会被广泛引用
   - 14-17分：对特定子领域有用
   - 10-13分：影响有限
   - 0-9分：无实际意义

3. **期刊匹配度**（25分）：
   - 22-25分：完美匹配期刊定位，读者高度关注
   - 18-21分：符合期刊范围，读者感兴趣
   - 14-17分：勉强相关
   - 10-13分：不太适合本期刊
   - 0-9分：完全不匹配

4. **写作质量**（25分）：
   - 22-25分：结构清晰、逻辑严密、表达精练、无冗余
   - 18-21分：整体良好，有少量改进空间
   - 14-17分：基本清楚，但组织松散或表达不清
   - 10-13分：结构混乱，难以理解
   - 0-9分：无法理解

**评价要求**：
- 逐节评价，引用论文具体内容（如"Methods 第3段声称..."）
- 指出具体的优点和不足，不要笼统评价
- 给出具体的改进建议

输出严格JSON格式：
{
  "score": <总分0-100>,
  "novelty_score": <0-25>,
  "significance_score": <0-25>,
  "fit_score": <0-25>,
  "writing_score": <0-25>,
  "strengths": ["<优点1>", "<优点2>", ...],
  "weaknesses": ["<不足1>", "<不足2>", ...],
  "comments": "<详细审稿意见，逐节评价>",
  "decision": "<accept/minor_revision/major_revision/reject>"
}""",

    'methodology': """你是方法学专家审稿人。你专精于研究设计、统计分析和可复现性评估。

**评分标准**（总分100分）：

1. **研究设计**（30分）：
   - 26-30分：设计严谨，遵循公认标准（如PRISMA），有预注册
   - 21-25分：设计合理，基本遵循标准流程
   - 16-20分：设计可行但有明显缺陷
   - 10-15分：设计不当，存在严重偏差风险
   - 0-9分：设计不可接受

2. **数据质量**（25分）：
   - 22-25分：样本充足、来源可靠、纳入标准明确、有PICOS框架
   - 18-21分：数据质量良好
   - 14-17分：数据有局限但不影响核心结论
   - 10-13分：数据质量堪忧
   - 0-9分：数据不可靠

3. **统计分析**（25分）：
   - 22-25分：方法恰当、结果解读准确、报告了效应量和置信区间
   - 18-21分：分析方法正确，有少量问题
   - 14-17分：方法基本可行但不够严谨
   - 10-13分：分析方法有误或解读不当
   - 0-9分：统计分析完全不可接受

4. **可复现性**（20分）：
   - 18-20分：提供完整代码、数据、PRISMA流程图，完全可以复现
   - 15-17分：提供了大部分复现所需信息
   - 12-14分：方法描述基本可复现
   - 8-11分：关键信息缺失
   - 0-7分：完全不可复现

**特别关注**：
- 检索策略是否完整（数据库、检索式、时间范围）
- 筛选流程是否透明（PRISMA流程图、双人筛选）
- 质量评估是否使用了公认工具（Cochrane RoB, NOS, CASP）
- 统计方法的选择是否合理（固定/随机效应、异质性检验）
- 是否有敏感性分析或亚组分析

输出严格JSON格式：
{
  "score": <总分0-100>,
  "design_score": <0-30>,
  "data_score": <0-25>,
  "stats_score": <0-25>,
  "reproducibility_score": <0-20>,
  "strengths": ["<优点1>", "<优点2>", ...],
  "weaknesses": ["<不足1>", "<不足2>", ...],
  "comments": "<详细方法学意见>",
  "decision": "<accept/minor_revision/major_revision/reject>"
}""",

    'domain': """你是该领域的资深专家审稿人。你专精于相关工作的全面性和理论框架的严谨性。

**评分标准**（总分100分）：

1. **相关工作**（30分）：
   - 26-30分：覆盖了所有关键文献，引用准确，有DOI等完整信息
   - 21-25分：覆盖了主要文献，少量遗漏
   - 16-20分：覆盖面一般，有明显遗漏
   - 10-15分：文献覆盖不足，引用质量低
   - 0-9分：严重缺失关键文献

2. **理论框架**（30分）：
   - 26-30分：理论基础扎实，概念操作化定义清晰，框架指导了整个研究
   - 21-25分：理论框架良好，基本完整
   - 16-20分：有理论但不够深入
   - 10-15分：理论框架薄弱或缺失
   - 0-9分：完全没有理论支撑

3. **文献综述**（25分）：
   - 22-25分：全面且批判性的综述，不是简单罗列，而是分析了研究间的异同
   - 18-21分：良好的综述，有一定批判性分析
   - 14-17分：以罗列为主，缺乏批判性评价
   - 10-13分：综述不充分
   - 0-9分：几乎没有综述

4. **领域贡献**（15分）：
   - 13-15分：对领域知识有实质性推进
   - 10-12分：有意义的贡献
   - 7-9分：贡献有限
   - 4-6分：几乎没有新贡献
   - 0-3分：无贡献

**特别关注**：
- 是否引用了领域内最权威的文献（高引用、顶级期刊）
- 引用是否完整（期刊名、DOI、页码等）
- 是否讨论了理论争议和不同学术观点
- 综述是否有批判性分析（不只是"XXX研究了Y"）
- 是否建立了清晰的理论框架指导研究

输出严格JSON格式：
{
  "score": <总分0-100>,
  "related_work_score": <0-30>,
  "theory_score": <0-30>,
  "literature_score": <0-25>,
  "contribution_score": <0-15>,
  "strengths": ["<优点1>", "<优点2>", ...],
  "weaknesses": ["<不足1>", "<不足2>", ...],
  "comments": "<详细领域意见>",
  "decision": "<accept/minor_revision/major_revision/reject>"
}""",

    'devil_advocate': """你是魔鬼代言人审稿人（Devil's Advocate）。你的任务是找出论文最致命的弱点，提出最强有力的反驳论点。

你应当以最严格、最挑剔的标准审视论文。假设你是对该论文持最负面态度的审稿人。

**评分标准**（总分100分）：
注意：你评的是论文在反驳面前"站得住脚"的程度，不是"你找到了多少漏洞"。
如果论文在严厉质疑下仍然站得住脚，应给予高分。

1. **论证强度**（40分）：核心论点在严密审视下是否成立？
   - 36-40分：论证严密，几乎没有破绽
   - 30-35分：论证较强，小问题不影响结论
   - 24-29分：有明显的论证薄弱环节
   - 16-23分：核心论证有重大漏洞
   - 0-15分：论证完全站不住脚

2. **证据充分性**（30分）：证据是否足以支撑结论？
   - 27-30分：证据链完整，结论可靠
   - 22-26分：证据基本充分
   - 17-21分：证据不够充分
   - 10-16分：证据严重不足
   - 0-9分：几乎无有效证据

3. **过度声明检测**（20分）：论文是否诚实？
   - 18-20分：结论审慎，恰如其分
   - 15-17分：基本诚实，有少量夸大
   - 12-14分：有明显的过度声明
   - 8-11分：大量夸大结论
   - 0-7分：结论严重失实

4. **替代解释考量**（10分）：是否考虑了其他可能性？
   - 9-10分：全面讨论了替代解释
   - 7-8分：有所提及但不深入
   - 5-6分：简单带过
   - 3-4分：完全忽视
   - 0-2分：无视任何替代解释

**你必须**：
- 找出至少3个最强的反驳论点
- 为每个反驳论点提供具体的逻辑推理
- 指出论文中具体的薄弱段落（引用原文）
- 建议论文如何加强论证来抵御这些反驳

输出严格JSON格式：
{
  "score": <总分0-100>,
  "argument_strength_score": <0-40>,
  "evidence_sufficiency_score": <0-30>,
  "overclaim_score": <0-20>,
  "alternative_score": <0-10>,
  "counter_arguments": [
    {
      "argument": "<反驳论点>",
      "evidence": "<支撑这个反驳的证据或逻辑>",
      "severity": "<fatal/serious/moderate>",
      "suggestion": "<论文如何应对这个反驳>"
    }
  ],
  "comments": "<最严厉的批评>",
  "decision": "<accept/minor_revision/major_revision/reject>"
}"""
}

SYNTHESIZER_PROMPT = """你是意见合成器（Synthesizer）。你的职责是合并所有审稿人意见，创建清晰的修订路线图。

**你的任务**：

1. **计算加权分数**：
   - Editor-in-Chief: 30%
   - Methodology: 25%
   - Domain: 20%
   - Devil's Advocate: 15%
   - 注意：你的评分不算在内，只合并以上四位

2. **识别共识**：多位审稿人都提出的问题（高优先级）
3. **识别分歧**：审稿人意见不一致的地方（需要作者判断）
4. **制定修订路线图**：按优先级排序的具体修订任务

**决策阈值**：
- ≥80: accept（接受）
- 65-79: minor_revision（小修）
- 50-64: major_revision（大修）
- <50: reject（拒稿）

输出严格JSON格式：
{
  "final_score": <加权平均分数>,
  "final_decision": "<accept/minor_revision/major_revision/reject>",
  "consensus_points": ["<共识问题1>", "<共识问题2>", ...],
  "divergence_points": ["<分歧问题1>", ...],
  "revision_roadmap": [
    {
      "priority": "<high/medium/low>",
      "section": "<章节名>",
      "issue": "<问题描述>",
      "action": "<具体修订建议>",
      "reviewer": "<来源审稿人>"
    }
  ],
  "summary": "<给作者的总结建议（200字以内）>"
}"""


def call_reviewer(role: str, manuscript: str) -> Dict:
    """Call a single reviewer agent with full manuscript."""
    prompt = REVIEWER_PROMPTS[role]

    # Devil's Advocate needs more output tokens for detailed counter-arguments
    max_tokens = 3000 if role == 'devil_advocate' else 2000

    try:
        response = LLM_CLIENT.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"请评审以下论文全文：\n\n{manuscript}"}
            ],
            temperature=0.3,
            max_tokens=max_tokens
        )

        content = response.choices[0].message.content or ""

        # Extract JSON (handle nested braces)
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                fixed = match.group().replace('\n', '\\n').replace('\t', '\\t')
                return json.loads(fixed)
        else:
            return {"score": 50, "comments": content, "decision": "major_revision"}

    except Exception as e:
        print(f"  ⚠️ {role} reviewer failed: {e}")
        return {"score": 50, "comments": f"Error: {e}", "decision": "major_revision"}


def synthesize_reviews(reviews: Dict[str, Dict], manuscript: str) -> Dict:
    """Synthesize all reviewer opinions into final decision."""

    review_summary = json.dumps(reviews, indent=2, ensure_ascii=False)

    try:
        response = LLM_CLIENT.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYNTHESIZER_PROMPT},
                {"role": "user", "content": f"审稿人意见汇总：\n{review_summary}\n\n请合成意见并创建修订路线图。"}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        content = response.choices[0].message.content or ""

        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            try:
                result = json.loads(match.group())
            except json.JSONDecodeError:
                result = {}

            # Always recalculate weighted score (don't trust LLM math)
            weights = {'editor': 0.30, 'methodology': 0.25, 'domain': 0.20, 'devil_advocate': 0.15}
            total_weight = sum(weights[r] for r in weights if r in reviews)
            if total_weight > 0:
                result['final_score'] = round(
                    sum(reviews[r]['score'] * weights[r] for r in weights if r in reviews) / total_weight * (1/total_weight) * total_weight,
                    1
                )
                # Simpler calculation
                result['final_score'] = round(
                    sum(reviews[r].get('score', 50) * weights[r] for r in weights if r in reviews),
                    1
                )

            # Determine decision by score
            score = result.get('final_score', 50)
            if score >= 80:
                result['final_decision'] = 'accept'
            elif score >= 65:
                result['final_decision'] = 'minor_revision'
            elif score >= 50:
                result['final_decision'] = 'major_revision'
            else:
                result['final_decision'] = 'reject'

            return result
        else:
            return {"final_score": 50, "final_decision": "major_revision", "summary": content}

    except Exception as e:
        print(f"  ⚠️ Synthesizer failed: {e}")
        # Fallback: calculate weighted score ourselves
        weights = {'editor': 0.30, 'methodology': 0.25, 'domain': 0.20, 'devil_advocate': 0.15}
        score = round(sum(reviews[r].get('score', 50) * weights[r] for r in weights if r in reviews), 1)
        decision = 'accept' if score >= 80 else 'minor_revision' if score >= 65 else 'major_revision' if score >= 50 else 'reject'
        return {"final_score": score, "final_decision": decision, "summary": f"Synthesizer error: {e}"}


def run_review(manuscript_file: str) -> Dict:
    """Run full 5-person review panel."""
    manuscript = Path(manuscript_file).read_text()

    print("👥 Running Multi-Agent Review Panel")
    print(f"   Manuscript length: {len(manuscript)} chars")

    # Run each reviewer (sequentially to avoid rate limits)
    reviews = {}
    for role in ['editor', 'methodology', 'domain', 'devil_advocate']:
        print(f"  [{role}] Reviewing...")
        reviews[role] = call_reviewer(role, manuscript)
        score = reviews[role].get('score', 'N/A')
        decision = reviews[role].get('decision', 'unknown')
        print(f"       Score: {score} -> {decision}")

    # Synthesize
    print("  [synthesizer] Merging opinions...")
    synthesis = synthesize_reviews(reviews, manuscript)
    print(f"       Final score: {synthesis.get('final_score', 'N/A')}")
    print(f"       Decision: {synthesis.get('final_decision', 'N/A')}")

    return {
        "reviews": reviews,
        "synthesis": synthesis,
        "weights": REVIEWER_WEIGHTS,
        "manuscript_length": len(manuscript),
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python review.py <manuscript_file>")
        sys.exit(1)

    manuscript_file = sys.argv[1]
    report = run_review(manuscript_file)

    # Save report next to manuscript
    output_file = Path(manuscript_file).parent / "review_report.json"
    Path(output_file).write_text(json.dumps(report, indent=2, ensure_ascii=False))

    print(f"\n✅ Review report saved to {output_file}")

    decision = report['synthesis'].get('final_decision', 'unknown')
    score = report['synthesis'].get('final_score', 0)
    print(f"   Final: {score}/100 → {decision}")

    if decision in ['accept', 'minor_revision']:
        print(f"✅ Decision: {decision} - proceed to Finalize stage")
        return True
    else:
        print(f"❌ Decision: {decision} - proceed to Revise stage")
        return False


if __name__ == "__main__":
    main()
