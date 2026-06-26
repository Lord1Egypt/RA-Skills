#!/usr/bin/env python3
"""Imperial Orchestrator · 模型基准测试

同一道题丢给所有模型，打分排名，按类别（coding/writing/ops/reasoning等）输出排行榜。
测试结果持久化到 .imperial_benchmark.json，路由器会读取分数来优化模型选择。

用法:
  # 跑全部类别
  python3 scripts/benchmark.py \
    --openclaw-config ~/.openclaw/openclaw.json \
    --state-file .imperial_state.json

  # 只跑 coding 类别
  python3 scripts/benchmark.py --category coding

  # 只测指定模型
  python3 scripts/benchmark.py --only-model deepseek/deepseek-chat

  # 跑完后看排行榜
  python3 scripts/benchmark.py --leaderboard
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lib import (
    Registry,
    build_initial_state,
    load_json,
    load_yaml,
    now_ts,
    read_openclaw_config,
    refresh_group_summaries,
    save_json,
    HealthInfo,
)
from model_validator import resolve_api_base, resolve_api_key, is_local_provider
from executor import call_model_api


# ── 类别到角色映射 ────────────────────────────────────────────────────

CATEGORY_TO_ROLES = {
    "coding": ["ministry-coding"],
    "writing": ["ministry-writing"],
    "reasoning": ["cabinet-planner", "censor-review"],
    "ops": ["ministry-ops"],
    "security": ["ministry-security"],
    "finance": ["ministry-finance"],
}

# 角色到主要类别（用于路由加分）
ROLE_PRIMARY_CATEGORY = {
    "ministry-coding": "coding",
    "ministry-writing": "writing",
    "cabinet-planner": "reasoning",
    "censor-review": "reasoning",
    "ministry-ops": "ops",
    "ministry-security": "security",
    "ministry-finance": "finance",
    "ministry-legal": "reasoning",
    "router-chief": "reasoning",
    "emergency-scribe": "coding",
}


# ── 调用模型 ──────────────────────────────────────────────────────────

def call_model(
    base_url: str,
    model_id: str,
    api_key: Optional[str],
    api_type: str,
    prompt: str,
    timeout: int = 60,
    max_tokens: int = 2048,
) -> Tuple[Optional[str], float, Optional[str]]:
    """调用模型并返回 (response_text, latency_ms, error)。"""
    messages = [{"role": "user", "content": prompt}]
    result = call_model_api(base_url, model_id, api_key, api_type, messages, max_tokens, temperature=0.1, timeout=timeout)
    if result["success"]:
        return result.get("content"), result.get("latency_ms", 0), None
    return None, result.get("latency_ms", 0), result.get("error")


# ── 自动评分 ──────────────────────────────────────────────────────────

def score_by_signals(
    response: str,
    expected_signals: List[str],
    scoring_weights: Dict[str, float],
    category: str,
) -> Dict[str, Any]:
    """基于 signal 匹配的自动评分。返回各维度分数和总分。"""
    if not response:
        return {
            "correctness": 0, "completeness": 0, "efficiency": 0, "style": 0,
            "total": 0, "signals_hit": [], "signals_missed": [],
        }

    text = response.lower()
    hits = []
    misses = []

    for signal in expected_signals:
        # 将 signal 拆成关键词组，全部命中算匹配
        keywords = [k.strip().lower() for k in re.split(r"[/、或]", signal)]
        matched = any(kw in text for kw in keywords)
        if matched:
            hits.append(signal)
        else:
            misses.append(signal)

    n_signals = len(expected_signals) if expected_signals else 1
    signal_ratio = len(hits) / n_signals

    # 基础分数（基于 signal 命中率）
    correctness = round(signal_ratio * 10, 1)
    completeness = round(signal_ratio * 10, 1)

    # 效率：输出长度合理性（太短扣分，太长也扣分）
    length = len(response)
    if length < 50:
        efficiency = 3.0
    elif length < 200:
        efficiency = 7.0
    elif length < 3000:
        efficiency = 9.0
    elif length < 6000:
        efficiency = 7.0
    else:
        efficiency = 5.0

    # 风格：结构化输出加分
    style = 5.0
    if "```" in response:
        style += 1.5  # 有代码块
    if re.search(r"^#{1,3}\s", response, re.MULTILINE):
        style += 1.0  # 有标题结构
    if re.search(r"^\d+\.\s", response, re.MULTILINE):
        style += 0.5  # 有编号列表
    if re.search(r"^[-*]\s", response, re.MULTILINE):
        style += 0.5  # 有无序列表
    style = min(style, 10.0)

    # 特殊规则：coding/ops 有代码块额外加分
    if category in ("coding", "ops") and "```" in response:
        correctness = min(correctness + 1.0, 10.0)

    # 加权总分
    weights = scoring_weights
    total = round(
        correctness * weights.get("correctness", 0.4)
        + completeness * weights.get("completeness", 0.25)
        + efficiency * weights.get("efficiency", 0.2)
        + style * weights.get("style", 0.15),
        2,
    )

    return {
        "correctness": correctness,
        "completeness": completeness,
        "efficiency": efficiency,
        "style": round(style, 1),
        "total": total,
        "signals_hit": hits,
        "signals_missed": misses,
    }


# ── 排行榜 ────────────────────────────────────────────────────────────

def print_leaderboard(benchmark_file: Path) -> None:
    """打印排行榜。"""
    data = load_json(benchmark_file)
    if not data:
        print("❌ 没有基准测试数据。先运行 benchmark.py 跑测试。")
        return

    scores = data.get("model_scores", {})
    if not scores:
        print("❌ 没有评分数据。")
        return

    # 收集所有类别
    all_categories = set()
    for model_scores in scores.values():
        all_categories.update(model_scores.get("categories", {}).keys())
    all_categories = sorted(all_categories)

    # 按总分排序
    ranked = sorted(
        scores.items(),
        key=lambda x: x[1].get("overall", 0),
        reverse=True,
    )

    # 打印表头
    cat_header = "".join(f"{c:>10s}" for c in all_categories)
    print(f"\n{'🏆 Imperial Orchestrator 模型排行榜':^80}")
    print(f"{'═' * 80}")
    print(f"  {'排名':>4s}  {'模型':40s}  {'总分':>6s}{cat_header}")
    print(f"  {'─' * 4}  {'─' * 40}  {'─' * 6}{''.join(['─' * 10] * len(all_categories))}")

    for rank, (model_ref, model_data) in enumerate(ranked, 1):
        overall = model_data.get("overall", 0)
        cats = model_data.get("categories", {})
        cat_scores = ""
        for c in all_categories:
            s = cats.get(c, {}).get("avg_score", 0)
            cat_scores += f"{s:>10.1f}"

        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "  ")
        print(f"  {medal}{rank:>2d}  {model_ref:40s}  {overall:>6.2f}{cat_scores}")

    print(f"\n  共 {len(ranked)} 个模型 | 测试时间: {data.get('last_run', 'N/A')}")
    print()

    # 按类别打印冠军
    print(f"  {'📊 各类别冠军':^60}")
    print(f"  {'─' * 60}")
    for cat in all_categories:
        best_model = None
        best_score = 0
        for model_ref, model_data in scores.items():
            s = model_data.get("categories", {}).get(cat, {}).get("avg_score", 0)
            if s > best_score:
                best_score = s
                best_model = model_ref
        display = CATEGORY_TO_ROLES.get(cat, [cat])
        print(f"  {cat:>12s} 冠军: {best_model or 'N/A':35s} ({best_score:.1f}分)")

    print()


# ── 主逻辑 ────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="模型基准测试 - 按类别评分排名")
    p.add_argument("--openclaw-config", type=Path, default=None)
    p.add_argument("--state-file", type=Path, default=Path(".imperial_state.json"))
    p.add_argument("--benchmark-file", type=Path, default=Path(".imperial_benchmark.json"))
    p.add_argument("--category", type=str, default=None,
                   help="只跑指定类别 (coding/writing/reasoning/ops/security/finance)")
    p.add_argument("--only-model", type=str, default=None, help="只测指定模型")
    p.add_argument("--difficulty", type=str, default=None,
                   help="只跑指定难度 (easy/medium/hard)")
    p.add_argument("--timeout", type=int, default=60, help="每个请求超时(秒)")
    p.add_argument("--max-tokens", type=int, default=2048)
    p.add_argument("--leaderboard", action="store_true", help="只显示排行榜")
    p.add_argument("--json", action="store_true", help="JSON 输出")
    p.add_argument("--skip-unhealthy", action="store_true", default=True,
                   help="跳过不健康的模型")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]

    # 仅显示排行榜
    if args.leaderboard:
        print_leaderboard(args.benchmark_file)
        return 0

    reg = Registry(root)
    benchmark_cfg = load_yaml(root / "config" / "benchmark_tasks.yaml")
    categories = benchmark_cfg.get("categories", {})

    if not categories:
        print("❌ 没有找到 benchmark_tasks.yaml 或无测试类别", file=sys.stderr)
        return 1

    # 加载 openclaw config 和 state
    cfg = read_openclaw_config(args.openclaw_config)
    if not cfg:
        print("❌ 找不到 openclaw.json", file=sys.stderr)
        return 1

    if args.state_file.exists():
        state = load_json(args.state_file)
    else:
        state = build_initial_state(reg, cfg)
        refresh_group_summaries(state)

    providers_cfg = cfg.get("models", {}).get("providers", {})
    models_state = state.get("models", {})

    # 过滤要测试的模型
    test_models = {}
    for model_ref, model_data in models_state.items():
        if args.only_model and model_ref != args.only_model:
            continue
        if args.skip_unhealthy:
            health = HealthInfo(**model_data.get("health", {}))
            if not health.healthy():
                continue
        test_models[model_ref] = model_data

    if not test_models:
        print("❌ 没有可测试的模型（都不健康或被过滤）", file=sys.stderr)
        return 1

    # 过滤类别
    test_categories = {}
    for cat_name, cat_data in categories.items():
        if args.category and cat_name != args.category:
            continue
        test_categories[cat_name] = cat_data

    if not test_categories:
        print(f"❌ 未找到类别 '{args.category}'，可选: {', '.join(categories.keys())}", file=sys.stderr)
        return 1

    # 加载已有的 benchmark 数据（增量更新）
    benchmark_data = load_json(args.benchmark_file) if args.benchmark_file.exists() else {}
    raw_results = benchmark_data.get("raw_results", {})
    model_scores = benchmark_data.get("model_scores", {})

    total_tests = sum(
        len([t for t in cat.get("tasks", []) if not args.difficulty or t.get("difficulty") == args.difficulty])
        for cat in test_categories.values()
    ) * len(test_models)

    if not args.json:
        print(f"🧪 开始基准测试: {len(test_models)} 模型 × {len(test_categories)} 类别 = {total_tests} 项测试\n")

    done = 0
    for cat_name, cat_data in test_categories.items():
        tasks = cat_data.get("tasks", [])
        scoring_weights = cat_data.get("scoring_weights", {})

        if not args.json:
            print(f"━━━ {cat_data.get('display_name', cat_name)} ━━━")

        for task in tasks:
            if args.difficulty and task.get("difficulty") != args.difficulty:
                continue

            task_id = task["id"]
            prompt = task["prompt"].strip()
            expected_signals = task.get("expected_signals", [])

            if not args.json:
                print(f"\n  📝 {task_id} [{task.get('difficulty', '?')}]")

            for model_ref, model_data in test_models.items():
                done += 1
                provider_key = model_data.get("provider", "unknown")
                model_id = model_ref.split("/", 1)[1] if "/" in model_ref else model_ref
                provider_data = providers_cfg.get(provider_key, {})

                base_url = resolve_api_base(provider_key, provider_data)
                api_key = resolve_api_key(provider_key, provider_data)

                if not base_url:
                    if not args.json:
                        print(f"     ⏭️  {model_ref:40s} — 无 API 地址，跳过")
                    continue

                if not api_key and not is_local_provider(provider_key):
                    if not args.json:
                        print(f"     ⏭️  {model_ref:40s} — 无 API Key，跳过")
                    continue

                # Resolve api_type from model config
                api_type = "openai-completions"
                models_list = provider_data.get("models", [])
                if isinstance(models_list, list):
                    for m in models_list:
                        if m.get("id") == model_id:
                            api_type = (m.get("api") or provider_data.get("api") or "openai-completions").lower()
                            break

                # 调用模型
                response, latency, error = call_model(
                    base_url, model_id, api_key, api_type, prompt, args.timeout, args.max_tokens
                )

                if error:
                    if not args.json:
                        print(f"     ❌ {model_ref:40s} — {error}")
                    continue

                # 评分
                score = score_by_signals(response or "", expected_signals, scoring_weights, cat_name)

                # 存储原始结果
                result_key = f"{model_ref}|{task_id}"
                raw_results[result_key] = {
                    "model_ref": model_ref,
                    "task_id": task_id,
                    "category": cat_name,
                    "difficulty": task.get("difficulty"),
                    "latency_ms": round(latency, 1),
                    "response_length": len(response or ""),
                    "score": score,
                    "timestamp": now_ts(),
                }

                if not args.json:
                    hit_count = len(score["signals_hit"])
                    total_signals = len(expected_signals)
                    print(
                        f"     {'✅' if score['total'] >= 6 else '⚠️' if score['total'] >= 4 else '❌'} "
                        f"{model_ref:40s} "
                        f"总分:{score['total']:>5.2f}  "
                        f"信号:{hit_count}/{total_signals}  "
                        f"延迟:{latency:>6.0f}ms"
                    )

    # 汇总每个模型的类别得分
    for model_ref in test_models:
        model_scores.setdefault(model_ref, {"categories": {}, "overall": 0})
        category_totals: Dict[str, List[float]] = {}

        for key, result in raw_results.items():
            if result.get("model_ref") != model_ref:
                continue
            cat = result.get("category", "")
            total = result.get("score", {}).get("total", 0)
            category_totals.setdefault(cat, []).append(total)

        for cat, scores_list in category_totals.items():
            avg = round(sum(scores_list) / len(scores_list), 2) if scores_list else 0
            model_scores[model_ref]["categories"][cat] = {
                "avg_score": avg,
                "tests_run": len(scores_list),
                "min_score": round(min(scores_list), 2) if scores_list else 0,
                "max_score": round(max(scores_list), 2) if scores_list else 0,
            }

        # 总分 = 所有类别平均分的平均
        cat_avgs = [v["avg_score"] for v in model_scores[model_ref]["categories"].values()]
        model_scores[model_ref]["overall"] = round(sum(cat_avgs) / len(cat_avgs), 2) if cat_avgs else 0

    # 持久化
    benchmark_data = {
        "last_run": time.strftime("%Y-%m-%d %H:%M:%S"),
        "last_run_ts": now_ts(),
        "model_scores": model_scores,
        "raw_results": raw_results,
    }
    save_json(args.benchmark_file, benchmark_data)

    if args.json:
        print(json.dumps(benchmark_data, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'═' * 60}")
        print(f"📊 测试完成，结果已保存到 {args.benchmark_file}")
        print(f"   运行 --leaderboard 查看排行榜\n")
        print_leaderboard(args.benchmark_file)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
