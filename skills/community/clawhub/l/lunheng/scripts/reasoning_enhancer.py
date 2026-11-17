#!/usr/bin/env python3
"""
reasoning_enhancer.py — 说理深度自动增强器

当 reasoning_scorer 评分低于阈值时，自动触发增强流程：
补充构成要件分析 → 强化事实-法律联结 → 添加类案引用
最多 3 轮迭代，每轮重新评分。

用法：
    from reasoning_enhancer import enhance_judgment
    result = enhance_judgment(judgment_text, cause="民间借贷纠纷", elements=elements)
    print(result.final_text)
    print(result.final_score)
"""

import json
import sys
import os
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# ─── 路径 ───────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
SKILL_DIR = SCRIPTS_DIR.parent
REFS_DIR = SKILL_DIR / "refs"

sys.path.insert(0, str(SCRIPTS_DIR))
from reasoning_scorer import score_judgment, format_report, QualityReport
from style_retriever import retrieve_style_examples, format_for_prompt

# ─── LLM 配置（从统一配置模块导入）───────────────
from config import LLM_API_KEY as _LLM_KEY, LLM_BASE_URL as _LLM_URL, LLM_MODEL as _LLM_MODEL

# ─── 增强策略 ──────────────────────────────────────────
ENHANCEMENT_STRATEGIES = [
    {
        "name": "补充构成要件分析",
        "trigger_dims": ["构成要件分析"],
        "prompt_instruction": (
            "请在\"本院认为\"部分，对每个争议焦点补充构成要件分析：\n"
            "1. 列出该法律关系的构成要件（如借贷关系：借贷合意+款项交付）\n"
            "2. 逐一对应本案事实进行分析\n"
            "3. 明确哪些要件已满足、哪些有争议"
        ),
    },
    {
        "name": "强化事实-法律联结",
        "trigger_dims": ["事实认定与证据", "逻辑连贯性"],
        "prompt_instruction": (
            "请强化事实与法律之间的联结：\n"
            "1. 在事实认定部分，明确引用支持每项事实的具体证据\n"
            "2. 在说理部分，用\"经审理查明...根据...规定...因此...\"的结构串联\n"
            "3. 确保每个法律结论都有对应的事实支撑"
        ),
    },
    {
        "name": "添加类案引用",
        "trigger_dims": ["争议焦点归纳", "法条引用准确度"],
        "prompt_instruction": (
            "请在说理部分增加类案引用和法条论证：\n"
            "1. 引用相关司法解释的具体条款\n"
            "2. 如有指导性案例或典型案例，简要引用其裁判要点\n"
            "3. 用\"类似案件中，法院通常认为...\"的方式增强说服力"
        ),
    },
]


@dataclass
class EnhancementRound:
    """单轮增强记录"""
    round_num: int              # 轮次
    strategy: str               # 使用的策略
    score_before: float         # 增强前分数
    score_after: float          # 增强后分数
    improvement: float          # 提升幅度
    text_preview: str           # 增强后文本预览（前 500 字）


@dataclass
class EnhancementResult:
    """增强结果"""
    original_score: float           # 原始分数
    final_score: float              # 最终分数
    total_improvement: float        # 总提升
    rounds: list                    # 各轮记录（EnhancementRound dict）
    final_text: str                 # 最终文本
    final_report: dict              # 最终质量报告
    reached_threshold: bool         # 是否达到阈值
    max_rounds: int                 # 最大轮次
    score_threshold: float          # 目标阈值


def _select_strategy(report: QualityReport) -> Optional[dict]:
    """根据评分报告选择最佳增强策略"""
    # 找出最薄弱的维度
    weak_dims = []
    for d in report.dimensions:
        ratio = d["score"] / d["max_score"] if d["max_score"] > 0 else 0
        if ratio < 0.5:
            weak_dims.append(d["name"])
    
    # 匹配最佳策略
    best_strategy = None
    best_match = 0
    
    for strategy in ENHANCEMENT_STRATEGIES:
        match_count = sum(1 for dim in weak_dims if dim in strategy["trigger_dims"])
        if match_count > best_match:
            best_match = match_count
            best_strategy = strategy
    
    # 如果没有匹配，使用第一个策略
    if best_strategy is None and ENHANCEMENT_STRATEGIES:
        best_strategy = ENHANCEMENT_STRATEGIES[0]
    
    return best_strategy


def _call_llm(prompt: str, max_tokens: int = 4000) -> str:
    """调用 LLM 生成增强文本"""
    if not _LLM_KEY:
        return ""
    
    body = json.dumps({
        "model": _LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    
    req = urllib.request.Request(
        f"{_LLM_URL}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_LLM_KEY}",
        },
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"⚠️ LLM 调用失败: {e}", file=sys.stderr)
        return ""


def _build_enhancement_prompt(
    judgment_text: str,
    cause: str,
    strategy: dict,
    style_context: str = "",
) -> str:
    """构建增强 prompt"""
    prompt_parts = [
        "你是一位资深法官，擅长优化裁判文书的说理深度。",
        "请根据以下要求，对给定的判决书进行说理增强。",
        "只修改\"本院认为\"及相关说理部分，保持其他部分不变。",
        "",
        f"## 案由：{cause}",
        "",
        "## 增强要求",
        strategy["prompt_instruction"],
        "",
    ]
    
    if style_context:
        prompt_parts += [
            "## 优秀文书范式参考",
            style_context,
            "",
        ]
    
    prompt_parts += [
        "## 原始判决书",
        judgment_text,
        "",
        "## 输出要求",
        "输出完整的增强后判决书，只输出正文，不要说明。",
    ]
    
    return "\n".join(prompt_parts)


def enhance_judgment(
    judgment_text: str,
    cause: str = "",
    elements=None,
    score_threshold: float = 36.0,
    max_rounds: int = 3,
) -> EnhancementResult:
    """
    自动增强裁判文书的说理深度。
    
    Args:
        judgment_text: 原始判决书文本
        cause: 案由
        elements: CaseElements（可选，用于检索范式）
        score_threshold: 目标分数（默认 36/60 = 60%）
        max_rounds: 最大增强轮次
    
    Returns:
        EnhancementResult 包含增强过程和最终结果
    """
    # 初始评分
    original_report = score_judgment(judgment_text, cause)
    original_score = original_report.total_score
    
    # 如果已经达标，直接返回
    if original_score >= score_threshold:
        return EnhancementResult(
            original_score=original_score,
            final_score=original_score,
            total_improvement=0,
            rounds=[],
            final_text=judgment_text,
            final_report=asdict(original_report),
            reached_threshold=True,
            max_rounds=max_rounds,
            score_threshold=score_threshold,
        )
    
    # 检索优秀文书范式
    style_context = ""
    if elements:
        keywords = getattr(elements, 'legal_issues', [])[:3]
        style_result = retrieve_style_examples(cause, keywords, top_k=2)
        style_context = format_for_prompt(style_result, max_chars=1500)
    
    # 迭代增强
    current_text = judgment_text
    current_score = original_score
    rounds = []
    
    for round_num in range(1, max_rounds + 1):
        # 选择策略
        strategy = _select_strategy(original_report)
        if not strategy:
            break
        
        print(f"🔄 第 {round_num} 轮增强：{strategy['name']}（当前分数：{current_score:.1f}）",
              file=sys.stderr)
        
        # 构建 prompt 并调用 LLM
        prompt = _build_enhancement_prompt(current_text, cause, strategy, style_context)
        enhanced_text = _call_llm(prompt)
        
        if not enhanced_text or len(enhanced_text) < 200:
            print(f"⚠️ 第 {round_num} 轮增强失败（LLM 输出过短）", file=sys.stderr)
            break
        
        # 重新评分
        new_report = score_judgment(enhanced_text, cause)
        new_score = new_report.total_score
        improvement = new_score - current_score
        
        rounds.append(EnhancementRound(
            round_num=round_num,
            strategy=strategy["name"],
            score_before=current_score,
            score_after=new_score,
            improvement=round(improvement, 1),
            text_preview=enhanced_text[:500],
        ))
        
        # 更新状态
        current_text = enhanced_text
        current_score = new_score
        
        # 检查是否达标
        if current_score >= score_threshold:
            print(f"✅ 第 {round_num} 轮后达标：{current_score:.1f}/{score_threshold}",
                  file=sys.stderr)
            break
        
        # 检查是否有提升（如果连续无提升，停止）
        if improvement <= 0 and round_num > 1:
            print(f"⚠️ 第 {round_num} 轮无提升，停止增强", file=sys.stderr)
            break
    
    # 最终报告
    final_report = score_judgment(current_text, cause)
    
    return EnhancementResult(
        original_score=original_score,
        final_score=current_score,
        total_improvement=round(current_score - original_score, 1),
        rounds=[asdict(r) for r in rounds],
        final_text=current_text,
        final_report=asdict(final_report),
        reached_threshold=current_score >= score_threshold,
        max_rounds=max_rounds,
        score_threshold=score_threshold,
    )


def format_enhancement_report(result: EnhancementResult) -> str:
    """格式化增强报告"""
    lines = []
    lines.append("## 说理深度自动增强报告")
    lines.append("")
    lines.append(f"**原始分数**：{result.original_score:.1f}/60")
    lines.append(f"**最终分数**：{result.final_score:.1f}/60")
    lines.append(f"**总提升**：+{result.total_improvement:.1f}")
    lines.append(f"**达标状态**：{'✅ 已达标' if result.reached_threshold else '⚠️ 未达标'}")
    lines.append(f"**目标阈值**：{result.score_threshold}/60")
    lines.append("")
    
    if result.rounds:
        lines.append("### 增强过程")
        for r in result.rounds:
            lines.append(f"- 第 {r['round_num']} 轮 [{r['strategy']}]："
                        f"{r['score_before']:.1f} → {r['score_after']:.1f}（+{r['improvement']:.1f}）")
        lines.append("")
    
    # 最终各维度评分
    if result.final_report and result.final_report.get("dimensions"):
        lines.append("### 最终各维度评分")
        for d in result.final_report["dimensions"]:
            bar = "█" * int(d["score"]) + "░" * int(d["max_score"] - d["score"])
            lines.append(f"- {d['name']}: {d['score']}/{d['max_score']} {bar}")
        lines.append("")
    
    # 改进建议
    if result.final_report and result.final_report.get("improvement_suggestions"):
        lines.append("### 剩余改进建议")
        for s in result.final_report["improvement_suggestions"]:
            lines.append(f"- {s}")
    
    return "\n".join(lines)


# ─── CLI 入口 ─────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 reasoning_enhancer.py <判决书文件路径> [案由]")
        print("示例: python3 reasoning_enhancer.py judgment.md 民间借贷纠纷")
        sys.exit(1)
    
    file_path = sys.argv[1]
    cause = sys.argv[2] if len(sys.argv) > 2 else ""
    
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    
    result = enhance_judgment(text, cause)
    print(format_enhancement_report(result))
    print("\n" + "=" * 60 + "\n")
    print("### 增强后判决书")
    print(result.final_text)
