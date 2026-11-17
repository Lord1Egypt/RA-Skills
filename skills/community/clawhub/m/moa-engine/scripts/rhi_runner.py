#!/usr/bin/env python3
"""
MoA RHI (Recursive Harness Self-Improvement) 闭环运行器

递归式自我改进循环：执行 MoA → 采集 <signal> → 计算 fitness → 生成增强指令 → 下一轮

用法:
  # 计算适应度
  python scripts/rhi_runner.py fitness --signals signals.json

  # 生成下一轮增强 Prompt
  python scripts/rhi_runner.py enhance --task "..." --signals signals.json --round 2

  # 批量分析多轮结果
  python scripts/rhi_runner.py analyze --rounds round1.json round2.json round3.json
"""

import argparse
import json
import sys
import math
from typing import List, Dict, Optional, Any

# ============================================================
# 适应度函数
# ============================================================

FITNESS_WEIGHTS = {
    "synthesis_novelty": 0.30,
    "critique_specificity": 0.25,
    "revision_quality": 0.20,
    "token_efficiency": 0.15,
    "immutability_intact": 0.10,
}

DIMENSION_DESCRIPTIONS = {
    "synthesis_novelty": "熔铸创新度",
    "critique_specificity": "批判精准度",
    "revision_quality": "修正质量",
    "token_efficiency": "Token 效率",
    "immutability_intact": "IMMUTABLE 完整性",
}

ENHANCE_TEMPLATES = {
    "synthesis_novelty": (
        "\n## RHI 增强指令（第{round}轮）\n"
        "### 熔铸创新要求\n"
        "上一轮熔铸创新度不足（{score:.2f}）。本轮熔铸决策者必须：\n"
        "1. 在最终答案中，显式列出至少 3 条超越各专家原始方案的创新洞见\n"
        "2. 使用 `<creative_leap>` 标签标注每个创新点的来源\n"
        "3. 禁止直接复制专家观点，必须进行重新组织与再创造\n"
    ),
    "critique_specificity": (
        "\n## RHI 增强指令（第{round}轮）\n"
        "### 批判精度要求\n"
        "上一轮批判精准度不足（{score:.2f}）。本轮批判者必须：\n"
        "1. 每条批判必须包含具体行号、变量名或逻辑节点\n"
        "2. 必须提供可复现的边界测试用例或极端场景\n"
        "3. 禁止使用「可能有问题」「不够健壮」等模糊表述\n"
        "4. 每条批判的 severity 必须显式标注\n"
    ),
    "revision_quality": (
        "\n## RHI 增强指令（第{round}轮）\n"
        "### 修正质量要求\n"
        "上一轮修正质量不足（{score:.2f}）。本轮被批判专家必须：\n"
        "1. 逐条回应批判，不得跳过任何攻击点\n"
        "2. 修正方案必须包含完整的代码/文本 diff，而非仅描述思路\n"
        '3. 使用 `<revision type="修复|反驳|补充">` 标注修正类型\n'
        "4. 若反驳批判，必须提供充分论据和证据\n"
    ),
    "token_efficiency": (
        "\n## RHI 增强指令（第{round}轮）\n"
        "### 效率优化要求\n"
        "上一轮 Token 效率不足（{score:.2f}）。本轮所有参与者必须：\n"
        "1. 阶段 2 和阶段 3 仅输出核心逻辑和关键要点，详细展开保留至最终答案\n"
        '2. 重复内容使用引用标签 `<ref target="...">` 替代重写\n'
        "3. 批判者优先攻击高优先级问题，次要问题标注后移\n"
    ),
    "immutability_intact": (
        "\n## RHI 增强指令（第{round}轮）\n"
        "### IMMUTABLE 保护警告\n"
        "上一轮检测到 IMMUTABLE 区域被触碰（{score:.2f}）。本轮必须：\n"
        "1. 严格保护 I1-I6 不可变区域，不得移除、跳过或重排序\n"
        "2. 对抗阶段（phase 3）不可省略\n"
        '3. `<final_answer>` 必须显式「再创造」，禁止罗列\n'
    ),
}


def compute_fitness(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    计算适应度函数。

    fitness = sum(weight * score) for each metric
    未出现的 metric 使用默认值 0.5（中等水平）
    """
    if not signals:
        return {
            "fitness": 0.5,
            "breakdown": {},
            "weakest": None,
            "verdict": "no_data",
            "message": "无信号数据，无法评估。"
        }

    # 按 metric 分组，取平均值
    metric_scores: Dict[str, float] = {}
    for s in signals:
        metric = s.get("metric")
        score = s.get("score", 0.5)
        if not metric or metric not in FITNESS_WEIGHTS:
            continue
        if metric not in metric_scores:
            metric_scores[metric] = []
        metric_scores[metric].append(float(score))

    # 计算各维度平均值
    breakdown = {}
    for metric, scores in metric_scores.items():
        breakdown[metric] = sum(scores) / len(scores)

    # 未出现的 metric 使用默认值
    for metric in FITNESS_WEIGHTS:
        if metric not in breakdown:
            breakdown[metric] = 0.5  # 默认中等水平

    # 计算加权总分
    fitness = sum(
        breakdown.get(metric, 0.5) * weight
        for metric, weight in FITNESS_WEIGHTS.items()
    )

    # 找出最弱维度
    weakest = min(breakdown, key=breakdown.get) if breakdown else None

    # 判断是否需要继续进化
    if fitness >= 0.85:
        verdict = "converged"
        message = f"适应度 {fitness:.3f} >= 0.85，已达到收敛标准。"
    elif fitness >= 0.70:
        verdict = "improving"
        message = f"适应度 {fitness:.3f}，在 0.70-0.85 之间，建议继续优化。"
    else:
        verdict = "needs_improvement"
        message = f"适应度 {fitness:.3f} < 0.70，需要显著改进。"

    # 添加维度中文描述
    breakdown_cn = {}
    for metric, score in breakdown.items():
        cn_name = DIMENSION_DESCRIPTIONS.get(metric, metric)
        breakdown_cn[f"{metric}({cn_name})"] = round(score, 3)

    return {
        "fitness": round(fitness, 3),
        "breakdown": breakdown_cn,
        "weakest": weakest,
        "weakest_score": round(breakdown.get(weakest, 0), 3) if weakest else None,
        "verdict": verdict,
        "message": message,
    }


def generate_enhancement(
    task: str,
    signals: List[Dict[str, Any]],
    fitness_result: Dict[str, Any],
    round_num: int,
    base_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """
    生成增强指令，用于注入下一轮 MoA Prompt 的自由区。
    """
    enhancements = []
    weakest = fitness_result.get("weakest")

    if not weakest:
        return {
            "round": round_num,
            "enhancements": [],
            "enhanced_prompt": base_prompt or "",
            "message": "无明确需要增强的维度。"
        }

    # 生成最弱维度的增强指令
    weakest_score = fitness_result.get("weakest_score", 0.5)
    template = ENHANCE_TEMPLATES.get(weakest)
    if template and weakest_score < 0.7:
        instruction = template.format(round=round_num, score=weakest_score)
        enhancements.append({
            "target": weakest,
            "score": weakest_score,
            "instruction": instruction.strip(),
        })

    # 对 fitness < 0.5 的维度也生成增强指令
    for metric, score_str in fitness_result.get("breakdown", {}).items():
        # 提取 metric 名称（去掉中文描述）
        metric_name = metric.split("(")[0] if "(" in metric else metric
        if metric_name == weakest or metric_name not in ENHANCE_TEMPLATES:
            continue
        # 从 score_str 提取数值
        if isinstance(score_str, (int, float)):
            score_val = float(score_str)
        else:
            continue
        if score_val < 0.5:
            template = ENHANCE_TEMPLATES.get(metric_name)
            if template:
                instruction = template.format(round=round_num, score=score_val)
                enhancements.append({
                    "target": metric_name,
                    "score": score_val,
                    "instruction": instruction.strip(),
                })

    # 构建增强后的 Prompt
    enhanced_prompt = base_prompt or ""
    if enhancements:
        enhancement_section = "\n\n<!-- RHI 增强指令（自动生成，仅影响自由区） -->\n"
        enhancement_section += f"## 第 {round_num} 轮 RHI 调整\n\n"
        for e in enhancements:
            enhancement_section += e["instruction"] + "\n\n"
        enhancement_section += "<!-- RHI 增强指令结束 -->\n"

        if base_prompt:
            # 在 base_prompt 末尾追加（不修改 IMMUTABLE 区域）
            enhanced_prompt = base_prompt.rstrip() + "\n" + enhancement_section
        else:
            enhanced_prompt = enhancement_section

    return {
        "round": round_num,
        "fitness": fitness_result["fitness"],
        "weakest": weakest,
        "weakest_score": fitness_result.get("weakest_score"),
        "enhancements": enhancements,
        "enhanced_prompt": enhanced_prompt,
    }


def analyze_rounds(round_files: List[str]) -> Dict[str, Any]:
    """
    批量分析多轮执行结果，输出 fitness 曲线。
    """
    rounds_data = []
    for i, filepath in enumerate(round_files):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            rounds_data.append({
                "round": i + 1,
                "file": filepath,
                "error": str(e),
            })
            continue

        # 兼容多种格式
        if isinstance(data, list):
            signals = data  # 直接是信号数组
        elif isinstance(data, dict):
            signals = data.get("signals", [])  # 包含 signals 字段
            if not signals and "output_signal" in data:
                signals = [data["output_signal"]]
        else:
            signals = []

        fitness_result = compute_fitness(signals) if signals else {
            "fitness": None, "verdict": "no_data",
            "message": "无法解析信号数据。"
        }

        rounds_data.append({
            "round": i + 1,
            "file": filepath,
            "signals_count": len(signals),
            "fitness": fitness_result.get("fitness"),
            "verdict": fitness_result.get("verdict"),
            "weakest": fitness_result.get("weakest"),
            "breakdown": fitness_result.get("breakdown", {}),
        })

    # 找出最佳轮次
    valid_rounds = [r for r in rounds_data if r.get("fitness") is not None]
    best_round = None
    if valid_rounds:
        best_round = max(valid_rounds, key=lambda r: r["fitness"])

    # 计算 fitness 趋势
    trend = "unknown"
    if len(valid_rounds) >= 2:
        first = valid_rounds[0]["fitness"]
        last = valid_rounds[-1]["fitness"]
        if last > first + 0.05:
            trend = "improving"
        elif last < first - 0.05:
            trend = "declining"
        else:
            trend = "stable"

    return {
        "rounds": rounds_data,
        "total_rounds": len(round_files),
        "valid_rounds": len(valid_rounds),
        "best_round": best_round["round"] if best_round else None,
        "best_fitness": best_round["fitness"] if best_round else None,
        "trend": trend,
        "recommendation": (
            f"经过 {len(valid_rounds)} 轮有效评估，最佳轮次是第 {best_round['round']} 轮"
            f"（fitness={best_round['fitness']:.3f}），趋势为 {trend}。"
        ) if best_round else "无有效评估数据。"
    }


# ============================================================
# CLI 入口
# ============================================================

def cmd_fitness(args):
    """计算适应度"""
    try:
        with open(args.signals, "r") as f:
            signals = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"文件不存在: {args.signals}"}, ensure_ascii=False))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON 解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if isinstance(signals, dict):
        signals = [signals]
    elif not isinstance(signals, list):
        print(json.dumps({"error": "信号数据必须是 JSON 数组或对象"}, ensure_ascii=False))
        sys.exit(1)

    result = compute_fitness(signals)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_enhance(args):
    """生成增强 Prompt"""
    try:
        with open(args.signals, "r") as f:
            signals = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"文件不存在: {args.signals}"}, ensure_ascii=False))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON 解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if isinstance(signals, dict):
        signals = [signals]
    elif not isinstance(signals, list):
        print(json.dumps({"error": "信号数据必须是 JSON 数组或对象"}, ensure_ascii=False))
        sys.exit(1)

    # 读取 base prompt（可选）
    base_prompt = None
    if args.prompt:
        try:
            with open(args.prompt, "r") as f:
                base_prompt = f.read()
        except FileNotFoundError:
            print(json.dumps({"error": f"Prompt 文件不存在: {args.prompt}"}, ensure_ascii=False))
            sys.exit(1)

    fitness_result = compute_fitness(signals)
    result = generate_enhancement(
        task=args.task,
        signals=signals,
        fitness_result=fitness_result,
        round_num=args.round,
        base_prompt=base_prompt,
    )

    # 简化为纯文本输出（增强指令部分），便于直接复制使用
    if args.text and result.get("enhancements"):
        output_lines = []
        for e in result["enhancements"]:
            output_lines.append(e["instruction"])
            output_lines.append("")
        print("\n".join(output_lines))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_analyze(args):
    """批量分析多轮结果"""
    result = analyze_rounds(args.rounds)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="MoA RHI (Recursive Harness Self-Improvement) 闭环运行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # fitness 子命令
    fit_parser = subparsers.add_parser("fitness", help="计算适应度")
    fit_parser.add_argument("--signals", required=True, help="信号标签 JSON 文件路径")
    fit_parser.set_defaults(func=cmd_fitness)

    # enhance 子命令
    enh_parser = subparsers.add_parser("enhance", help="生成增强指令")
    enh_parser.add_argument("--task", required=True, help="原始任务描述")
    enh_parser.add_argument("--signals", required=True, help="信号标签 JSON 文件路径")
    enh_parser.add_argument("--round", type=int, required=True, help="当前轮次编号")
    enh_parser.add_argument("--prompt", help="base Prompt 文件路径（可选，用于生成增强版 Prompt）")
    enh_parser.add_argument("--text", action="store_true", help="以纯文本输出增强指令（便于复制）")
    enh_parser.set_defaults(func=cmd_enhance)

    # analyze 子命令
    ana_parser = subparsers.add_parser("analyze", help="批量分析多轮结果")
    ana_parser.add_argument("--rounds", nargs="+", required=True, help="多轮结果 JSON 文件路径列表")
    ana_parser.set_defaults(func=cmd_analyze)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()