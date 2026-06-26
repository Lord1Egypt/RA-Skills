#!/usr/bin/env python3
"""
沙盘推演脚本 - Sandbox Simulation Engine
功能：读取联网搜索结果 → 模拟多种应对方案 → 运算最优解 → 输出经验文档

用法：
  python3 sandbox_sim.py \\
    --scenario "AlfredLi表达了沮丧情绪" \\
    --search-results "找到以下策略：1.倾听 2.共情 3.重构问题..." \\
    --emotion-type "sadness" \\
    --context "AlfredLi今天工作中遇到了挫折..."
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PALACE_BASE = Path.home() / ".mempalace/palace/wing_shared/experience/sandbox"


def load_today_summary():
    """读取今日已有的沙盘记录，用于去重和参考"""
    today = datetime.now().strftime("%Y-%m-%d")
    summary_file = PALACE_BASE / today / "daily_summary.json"
    if summary_file.exists():
        with open(summary_file) as f:
            return json.load(f)
    return {"scenarios": [], "optimal_solutions": []}


def save_daily_summary(summary):
    """保存今日沙盘汇总"""
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = PALACE_BASE / today
    day_dir.mkdir(parents=True, exist_ok=True)
    summary_file = day_dir / "daily_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def parse_search_results(search_results: str) -> list:
    """解析联网搜索结果，提取关键策略"""
    # 提取所有策略（编号列表）
    strategies = []
    for line in search_results.split("\n"):
        line = line.strip()
        # 匹配 "1. xxx" 或 "- xxx" 或 "① xxx" 格式
        m = re.match(r"^\d+[.、)）]\s*(.+)", line)
        if m:
            strategies.append(m.group(1).strip())
        elif line.startswith("- ") and len(line) > 2:
            strategies.append(line[2:].strip())
    if not strategies:
        strategies = [search_results[:200]]  # fallback
    return strategies


def score_strategy(strategy: str, emotion_type: str) -> dict:
    """
    给单个策略打分
    维度：适用性 / 温度感 / 可执行性 / 创新性
    """
    scores = {"applicability": 0.5, "warmth": 0.5, "actionability": 0.5, "creativity": 0.5}
    strategy_lower = strategy.lower()

    # 通用正面词加分
    positive_words = ["倾听", "共情", "陪伴", "支持", "理解", "安慰", "温暖", "拥抱", "鼓励"]
    for w in positive_words:
        if w in strategy_lower:
            scores["warmth"] += 0.15

    # 负面词减分
    negative_words = ["否定", "指责", "忽视", "冷漠", "敷衍"]
    for w in negative_words:
        if w in strategy_lower:
            scores["warmth"] -= 0.3
            scores["applicability"] -= 0.2

    # 可执行性：具体动作 > 空泛描述
    action_words = ["一起", "具体", "执行", "计划", "步骤", "问问", "说说", "聊聊"]
    for w in action_words:
        if w in strategy_lower:
            scores["actionability"] += 0.15

    # 情绪类型适配
    if emotion_type in ("sadness", "loneliness"):
        if any(w in strategy_lower for w in ["倾听", "陪伴", "共情", "安慰"]):
            scores["applicability"] += 0.3
            scores["warmth"] += 0.2
    elif emotion_type in ("anger", "frustration"):
        if any(w in strategy_lower for w in ["重构", "冷静", "暂停", "转化"]):
            scores["applicability"] += 0.3
    elif emotion_type in ("joy", "excitement"):
        if any(w in strategy_lower for w in ["共振", "放大", "庆祝", "延伸"]):
            scores["applicability"] += 0.3
            scores["creativity"] += 0.2

    # clamp 到 0-1
    for k in scores:
        scores[k] = max(0.0, min(1.0, scores[k]))

    # 总分 = 加权平均
    total = (
        scores["applicability"] * 0.35
        + scores["warmth"] * 0.30
        + scores["actionability"] * 0.20
        + scores["creativity"] * 0.15
    )
    return {**scores, "total": round(total, 3)}


def simulate_sandbox(scenario: str, search_results: str, emotion_type: str, context: str) -> dict:
    """
    沙盘推演主逻辑：
    1. 解析搜索结果中的策略列表
    2. 对每个策略打分
    3. 选出最优解
    4. 生成推演过程记录
    5. 写入 MemPalace
    """
    strategies = parse_search_results(search_results)
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M:%S")
    run_id = f"{today}_{datetime.now().strftime('%H%M%S')}"

    # 加载今日汇总
    daily = load_today_summary()

    # 推演记录
    simulation = {
        "run_id": run_id,
        "timestamp": timestamp,
        "scenario": scenario,
        "emotion_type": emotion_type,
        "context": context,
        "strategies_count": len(strategies),
        "simulation": [],
        "optimal_solution": None,
        "learning": "",
    }

    # 对每个策略打分
    for i, strategy in enumerate(strategies):
        scores = score_strategy(strategy, emotion_type)
        simulation["simulation"].append(
            {
                "rank": i + 1,
                "strategy": strategy,
                "scores": scores,
                "reasoning": f"总分 {scores['total']:.2f}，"
                f"适用性 {scores['applicability']:.2f}，"
                f"温度感 {scores['warmth']:.2f}，"
                f"可执行性 {scores['actionability']:.2f}，"
                f"创新性 {scores['creativity']:.2f}",
            }
        )

    # 按总分排序，选最优
    simulation["simulation"].sort(key=lambda x: x["scores"]["total"], reverse=True)
    top = simulation["simulation"][0]
    top["is_optimal"] = True

    # 生成最优解描述
    optimal = {
        "strategy": top["strategy"],
        "total_score": top["scores"]["total"],
        "key_strengths": {
            "适用性": round(top["scores"]["applicability"], 2),
            "温度感": round(top["scores"]["warmth"], 2),
            "可执行性": round(top["scores"]["actionability"], 2),
            "创新性": round(top["scores"]["creativity"], 2),
        },
        "why_best": f"在 {len(strategies)} 个候选方案中，总分 {top['scores']['total']:.2f} 最高，"
        f"温度感 {top['scores']['warmth']:.2f}，"
        f"对 {emotion_type} 类型情绪最有针对性。",
    }
    simulation["optimal_solution"] = optimal

    # 生成学习要点
    simulation["learning"] = (
        f"场景「{scenario}」（情绪类型：{emotion_type}）→ "
        f"最优策略：{top['strategy']}（得分{top['scores']['total']:.2f}）"
    )

    # 写入 MemPalace
    day_dir = PALACE_BASE / today
    day_dir.mkdir(parents=True, exist_ok=True)
    out_file = day_dir / f"sandbox_{run_id}.json"
    with open(out_file, "w") as f:
        json.dump(simulation, f, ensure_ascii=False, indent=2)

    # 更新每日汇总
    daily.setdefault("scenarios", [])
    daily.setdefault("optimal_solutions", [])
    daily["scenarios"].append({"time": timestamp, "scenario": scenario, "emotion": emotion_type})
    daily["optimal_solutions"].append(
        {"time": timestamp, "strategy": top["strategy"], "score": top["scores"]["total"]}
    )
    daily["last_updated"] = f"{today} {timestamp}"
    save_daily_summary(daily)

    return simulation


def main():
    parser = argparse.ArgumentParser(description="Neuro-Agent 沙盘推演引擎")
    parser.add_argument("--scenario", required=True, help="场景描述")
    parser.add_argument("--search-results", required=True, help="联网搜索结果摘要")
    parser.add_argument("--emotion-type", required=True, help="情绪类型")
    parser.add_argument("--context", default="", help="当前对话上下文")
    args = parser.parse_args()

    print(f"[sandbox_sim] 开始沙盘推演...", flush=True)
    print(f"  场景: {args.scenario}", flush=True)
    print(f"  情绪: {args.emotion_type}", flush=True)

    result = simulate_sandbox(
        scenario=args.scenario,
        search_results=args.search_results,
        emotion_type=args.emotion_type,
        context=args.context,
    )

    top = result["optimal_solution"]
    print(f"\n[sandbox_sim] ✅ 推演完成", flush=True)
    print(f"  最优策略: {top['strategy']}", flush=True)
    print(f"  总分: {top['total_score']}", flush=True)
    print(f"  强度: 适用性={top['key_strengths']['适用性']} | "
          f"温度感={top['key_strengths']['温度感']} | "
          f"可执行={top['key_strengths']['可执行性']}", flush=True)
    print(f"  学习: {result['learning']}", flush=True)

    return result


if __name__ == "__main__":
    main()
