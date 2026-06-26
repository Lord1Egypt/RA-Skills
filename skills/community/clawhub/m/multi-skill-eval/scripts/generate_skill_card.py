#!/usr/bin/env python3
"""
Generate a standardized Skill Card from benchmark results.

Usage:
    python3 generate_skill_card.py \
        --workspace /path/to/results \
        --skill-name "My Skill" \
        --skill-slug my-skill \
        --eval-model claude-sonnet-4 \
        --output skill-cards/my-skill-v1.md

Skill Card Contents:
- Metadata: name, source, eval date, model, engine version
- Overall score 0-10 (Quality 0-5 + Delta 0-3 + Efficiency 0-2)
- With-skill vs without-skill comparison table
- Per-test-case breakdown with assertions, timing, grading
- Strengths / Weaknesses
- Recommendation: Recommended / Conditional / Marginal / Not Recommended
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path


def load_benchmark_data(workspace):
    """Load all benchmark data from workspace."""
    data = {
        "grading": None,
        "benchmark": None,
        "preflight": None,
    }
    
    # Load grading.json
    grading_path = os.path.join(workspace, "grading.json")
    if os.path.exists(grading_path):
        with open(grading_path, "r", encoding="utf-8") as f:
            data["grading"] = json.load(f)
    
    # Load benchmark aggregation if exists
    benchmark_path = os.path.join(workspace, "benchmark-aggregation.json")
    if os.path.exists(benchmark_path):
        with open(benchmark_path, "r", encoding="utf-8") as f:
            data["benchmark"] = json.load(f)
    
    # Load preflight results if exists
    preflight_path = os.path.join(workspace, "preflight.json")
    if os.path.exists(preflight_path):
        with open(preflight_path, "r", encoding="utf-8") as f:
            data["preflight"] = json.load(f)
    
    return data


def calculate_overall_score(grading, benchmark, preflight):
    """
    Calculate overall score 0-10:
    - Quality: 0-5 based on grading pass rate
    - Delta: 0-3 based on with_skill vs without_skill improvement
    - Efficiency: 0-2 based on time/token cost
    """
    quality = 0
    delta = 0
    efficiency = 2  # Default to max efficiency
    
    # Quality score from grading (0-5)
    if grading and grading.get("summary", {}).get("total", 0) > 0:
        pass_rate = grading["summary"]["pass_rate"]
        quality = int(pass_rate * 5)
    
    # Delta score from benchmark (0-3)
    if benchmark:
        benchmark_delta = benchmark.get("delta", {})
        pass_rate_delta = benchmark_delta.get("pass_rate", "+0.00")
        
        # Parse delta value (e.g., "+0.15" -> 0.15)
        try:
            delta_value = float(pass_rate_delta.replace("+", ""))
            if delta_value >= 0.3:
                delta = 3
            elif delta_value >= 0.2:
                delta = 2
            elif delta_value >= 0.1:
                delta = 1
            else:
                delta = 0
        except (ValueError, AttributeError):
            delta = 0
        
        # Efficiency penalty for high-overhead skills
        time_delta = benchmark_delta.get("time", "1x")
        try:
            time_ratio = float(time_delta.replace("x", "").replace("+", ""))
            if time_ratio > 3:
                efficiency = 0
            elif time_ratio > 2:
                efficiency = 1
        except (ValueError, AttributeError):
            pass
    
    overall = quality + delta + efficiency
    return min(overall, 10), {
        "quality": quality,
        "delta": delta,
        "efficiency": efficiency,
        "overall": min(overall, 10)
    }


def get_recommendation(overall_score, grading, benchmark, preflight):
    """Determine recommendation based on overall score."""
    if overall_score >= 7:
        return "Recommended"
    elif overall_score >= 5:
        return "Conditional"
    elif overall_score >= 3:
        return "Marginal"
    else:
        return "Not Recommended"


def detect_strengths(grading, benchmark, preflight):
    """Identify skill strengths from data."""
    strengths = []
    
    if grading:
        # Check for high pass rate areas
        for assertion in grading.get("assertions", []):
            if assertion.get("passed"):
                cat = assertion.get("category", "")
                if cat == "quality":
                    strengths.append(f"输出质量达标")
                elif cat == "format":
                    strengths.append(f"格式规范")
                elif cat == "security":
                    strengths.append(f"安全性良好")
    
    if benchmark:
        # Check for significant improvements
        if benchmark.get("with_skill", {}).get("pass_rate", 0) > 0.8:
            strengths.append("高任务完成率")
    
    if preflight:
        # Check dependencies
        deps = preflight.get("dependencies", {})
        if deps.get("all_available", True):
            strengths.append("依赖完整可用")
    
    return list(set(strengths))[:5]  # Deduplicate, max 5


def detect_weaknesses(grading, benchmark, preflight):
    """Identify skill weaknesses from data."""
    weaknesses = []
    
    if grading:
        # Check for failed assertions
        for assertion in grading.get("assertions", []):
            if not assertion.get("passed"):
                cat = assertion.get("category", "")
                if cat == "format":
                    weaknesses.append("格式不规范")
                elif cat == "security":
                    weaknesses.append("安全性问题")
                elif cat == "completeness":
                    weaknesses.append("输出不完整")
    
    if preflight:
        # Check for phantom tooling
        phantom = preflight.get("phantom_tooling", [])
        if phantom:
            weaknesses.append(f"幽灵工具: {', '.join(phantom[:2])}")
        
        # Check for unverified claims
        claims = preflight.get("unverified_claims", [])
        if claims:
            weaknesses.append("存在未验证的营销声明")
    
    if benchmark:
        # Check for high overhead
        delta = benchmark.get("delta", {})
        time_ratio = delta.get("time", "1x")
        try:
            ratio = float(time_ratio.replace("x", "").replace("+", ""))
            if ratio > 2:
                weaknesses.append(f"开销较高: {time_ratio}")
        except:
            pass
    
    return list(set(weaknesses))[:5]  # Deduplicate, max 5


def generate_skill_card(args):
    """Generate the complete skill card."""
    workspace = os.path.abspath(args.workspace)
    data = load_benchmark_data(workspace)
    
    # Calculate scores
    overall_score, score_breakdown = calculate_overall_score(
        data.get("grading"),
        data.get("benchmark"),
        data.get("preflight")
    )
    
    recommendation = get_recommendation(
        overall_score,
        data.get("grading"),
        data.get("benchmark"),
        data.get("preflight")
    )
    
    strengths = detect_strengths(
        data.get("grading"),
        data.get("benchmark"),
        data.get("preflight")
    )
    
    weaknesses = detect_weaknesses(
        data.get("grading"),
        data.get("benchmark"),
        data.get("preflight")
    )
    
    # Build skill card
    card = []
    card.append("# Skill Card")
    card.append("")
    card.append(f"**Skill**: {args.skill_name}")
    card.append(f"**Slug**: {args.skill_slug}")
    card.append(f"**Eval Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    card.append(f"**Model**: {args.eval_model}")
    card.append("")
    card.append("---")
    card.append("")
    card.append("## Metadata")
    card.append("")
    card.append(f"| Field | Value |")
    card.append(f"|-------|-------|")
    card.append(f"| Skill Name | {args.skill_name} |")
    card.append(f"| Skill Slug | {args.skill_slug} |")
    card.append(f"| Evaluation Date | {datetime.now().strftime('%Y-%m-%d')} |")
    card.append(f"| Evaluator Model | {args.eval_model} |")
    card.append(f"| Engine Version | multi-skill-eval v1.0.0 |")
    if args.source:
        card.append(f"| Source | {args.source} |")
    card.append("")
    card.append("## Overall Score")
    card.append("")
    card.append(f"**Overall: {overall_score}/10**")
    card.append("")
    card.append(f"| Component | Score | Max |")
    card.append(f"|-----------|-------|-----|")
    card.append(f"| Quality | {score_breakdown['quality']} | 5 |")
    card.append(f"| Delta | {score_breakdown['delta']} | 3 |")
    card.append(f"| Efficiency | {score_breakdown['efficiency']} | 2 |")
    card.append(f"| **Total** | **{overall_score}** | **10** |")
    card.append("")
    card.append("### Score Breakdown")
    card.append("")
    card.append("- **Quality (0-5)**: Based on grading pass rate")
    card.append("- **Delta (0-3)**: Based on with-skill vs without-skill improvement")
    card.append("- **Efficiency (0-2)**: Based on time/token cost ratio")
    card.append("")
    card.append("---")
    card.append("")
    card.append("## With-Skill vs Without-Skill Comparison")
    card.append("")
    
    if data.get("benchmark"):
        bm = data["benchmark"]
        card.append(f"| Metric | With-Skill | Without-Skill | Delta |")
        card.append(f"|---------|-----------|---------------|-------|")
        card.append(f"| Pass Rate | {bm.get('with_skill', {}).get('pass_rate', 'N/A')} | {bm.get('without_skill', {}).get('pass_rate', 'N/A')} | {bm.get('delta', {}).get('pass_rate', 'N/A')} |")
        card.append(f"| Avg Time | {bm.get('with_skill', {}).get('avg_time', 'N/A')} | {bm.get('without_skill', {}).get('avg_time', 'N/A')} | {bm.get('delta', {}).get('time', 'N/A')} |")
        card.append(f"| Avg Tokens | {bm.get('with_skill', {}).get('avg_tokens', 'N/A')} | {bm.get('without_skill', {}).get('avg_tokens', 'N/A')} | {bm.get('delta', {}).get('tokens', 'N/A')} |")
    else:
        card.append("*No benchmark data available.*")
    card.append("")
    card.append("---")
    card.append("")
    card.append("## Per-Test-Case Breakdown")
    card.append("")
    
    if data.get("grading"):
        assertions = data["grading"].get("assertions", [])
        by_category = {}
        for a in assertions:
            cat = a.get("category", "other")
            by_category.setdefault(cat, []).append(a)
        
        for cat, items in by_category.items():
            card.append(f"### {cat.upper()}")
            card.append("")
            for item in items:
                status = "✅" if item.get("passed") else "❌"
                card.append(f"- {status} {item.get('text', '')}")
                if item.get('evidence'):
                    card.append(f"  - Evidence: {item.get('evidence')}")
            card.append("")
    else:
        card.append("*No per-test data available.*")
        card.append("")
    
    card.append("---")
    card.append("")
    card.append("## Strengths")
    card.append("")
    if strengths:
        for s in strengths:
            card.append(f"- ✅ {s}")
    else:
        card.append("*No specific strengths identified.*")
    card.append("")
    card.append("## Weaknesses")
    card.append("")
    if weaknesses:
        for w in weaknesses:
            card.append(f"- ❌ {w}")
    else:
        card.append("*No specific weaknesses identified.*")
    card.append("")
    card.append("---")
    card.append("")
    card.append("## Recommendation")
    card.append("")
    
    rec_emoji = {
        "Recommended": "✅",
        "Conditional": "⚠️",
        "Marginal": "⚡",
        "Not Recommended": "❌"
    }
    rec_text = {
        "Recommended": "该技能已通过基准测试，推荐使用。",
        "Conditional": "该技能在特定场景下可用，需注意已知问题。",
        "Marginal": "该技能存在明显局限，建议修复后再使用。",
        "Not Recommended": "该技能未通过基准测试，暂不推荐使用。"
    }
    
    card.append(f"### {rec_emoji.get(recommendation, '❓')} **{recommendation}**")
    card.append("")
    card.append(rec_text.get(recommendation, ""))
    card.append("")
    
    # Dependencies section
    if data.get("preflight"):
        card.append("---")
        card.append("")
        card.append("## Dependencies")
        card.append("")
        deps = data["preflight"].get("dependencies", {})
        if deps:
            card.append(f"- Required: {', '.join(deps.get('required', []))}")
            card.append(f"- Optional: {', '.join(deps.get('optional', []))}")
            card.append(f"- All Available: {'Yes' if deps.get('all_available') else 'No'}")
        else:
            card.append("*No dependency information available.*")
        card.append("")
    
    return "\n".join(card)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a standardized Skill Card from benchmark results"
    )
    parser.add_argument(
        "--workspace", "-w", required=True,
        help="Path to benchmark results workspace"
    )
    parser.add_argument(
        "--skill-name", "-n", required=True,
        help="Name of the skill"
    )
    parser.add_argument(
        "--skill-slug", "-s", required=True,
        help="Slug/identifier for the skill"
    )
    parser.add_argument(
        "--eval-model", "-m", default="minimax/MiniMax-M2",
        help="Model used for evaluation"
    )
    parser.add_argument(
        "--source",
        help="Source of the skill (URL, path, etc.)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)"
    )
    args = parser.parse_args()
    
    card = generate_skill_card(args)
    
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(card)
        print(f"Skill card generated: {args.output}")
    else:
        print(card)


if __name__ == "__main__":
    main()
