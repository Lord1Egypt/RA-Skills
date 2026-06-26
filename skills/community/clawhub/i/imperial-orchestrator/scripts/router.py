#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lib import (
    HealthInfo,
    Registry,
    count_healthy_models,
    infer_complexity,
    load_json,
    match_role_by_keywords,
    now_ts,
    read_openclaw_config,
    record_failure,
    record_success,
    refresh_group_summaries,
    save_json,
)

# 角色到基准测试类别映射
ROLE_TO_BENCHMARK_CATEGORY = {
    "ministry-coding": "coding",
    "ministry-writing": "writing",
    "ministry-ops": "ops",
    "ministry-security": "security",
    "ministry-finance": "finance",
    "ministry-legal": "reasoning",
    "cabinet-planner": "reasoning",
    "censor-review": "reasoning",
    "router-chief": "reasoning",
    "emergency-scribe": "coding",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Route a task to the best role and model chain.")
    p.add_argument("--task", required=True, help="User task text")
    p.add_argument("--openclaw-config", type=Path, default=None)
    p.add_argument("--state-file", type=Path, default=Path(".imperial_state.json"))
    p.add_argument("--benchmark-file", type=Path, default=Path(".imperial_benchmark.json"),
                   help="Benchmark scores file for routing boost")
    p.add_argument("--record-failure", nargs=2, metavar=("MODEL_REF", "ERROR_TYPE"))
    p.add_argument("--record-success", metavar="MODEL_REF")
    p.add_argument("--write-state", action="store_true", help="Persist updated state")
    return p.parse_args()


def load_benchmark_scores(benchmark_file: Path) -> Dict[str, Dict[str, Any]]:
    """加载基准测试评分，返回 {model_ref: {category: avg_score, ...}}。"""
    if not benchmark_file.exists():
        return {}
    data = load_json(benchmark_file)
    return data.get("model_scores", {})


def ensure_state(root: Path, state_file: Path, openclaw_config: Optional[Path]) -> Dict[str, Any]:
    from lib import build_initial_state

    reg = Registry(root)
    if state_file.exists():
        state = load_json(state_file)
        refresh_group_summaries(state)
        return state
    cfg = read_openclaw_config(openclaw_config)
    state = build_initial_state(reg, cfg)
    refresh_group_summaries(state)
    return state


def determine_role(reg: Registry, task: str) -> Tuple[str, List[str], str]:
    role = match_role_by_keywords(task)
    chosen_mode = "direct"
    reviews: List[str] = []

    # Build i18n-augmented keyword map: rule_name → extra keywords from i18n
    i18n_map = {
        "coding-debug": "coding", "ops-infra": "ops", "security": "security",
        "writing-translation": "writing", "legal": "legal", "finance": "finance",
    }

    for rule in reg.rules_cfg.get("rules", []):
        keywords = list(rule.get("any_keywords", []))
        # Inject multi-language routing keywords
        rule_name = rule.get("name", "")
        i18n_cat = i18n_map.get(rule_name)
        if i18n_cat:
            keywords.extend(reg.i18n.routing_keywords(i18n_cat))
        if any(k.lower() in task.lower() for k in keywords):
            role = rule.get("lead_role", role)
            reviews = list(rule.get("review_roles", []))
            chosen_mode = rule.get("mode", "direct")
            break

    if not role:
        default = reg.rules_cfg.get("default", {})
        role = default.get("lead_role", "cabinet-planner")
        reviews = list(default.get("review_roles", []))
        chosen_mode = default.get("mode", "direct")

    complexity = infer_complexity(task)
    if complexity == "high" and chosen_mode == "direct":
        chosen_mode = "plan_then_execute"
    return role, reviews, chosen_mode


def candidate_models_for_role(
    reg: Registry,
    state: Dict[str, Any],
    role: str,
    benchmark_scores: Optional[Dict[str, Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    models = []
    role_cfg = reg.roles_cfg.get("roles", {}).get(role, {})
    preferred_caps = set(role_cfg.get("preferred_capabilities", []))
    bench_category = ROLE_TO_BENCHMARK_CATEGORY.get(role)
    prefer_quality = role_cfg.get("prefer_quality", False)
    top_model_keywords = [kw.lower() for kw in role_cfg.get("top_model_keywords", [])]
    quality_keywords = [kw.lower() for kw in role_cfg.get("quality_keywords", [])]
    now = now_ts()

    for ref, data in state.get("models", {}).items():
        health = HealthInfo(**data.get("health", {}))
        if not health.healthy(now):
            continue
        score = 0

        # 基础分：角色匹配
        if role in data.get("roles", []):
            score += 30
        # 能力偏好
        caps = set(data.get("capabilities", []))
        score += 8 * len(preferred_caps.intersection(caps))

        if prefer_quality:
            # ★ 质量优先模式：强模型大幅加分，成本不再是优势
            # 模型名关键词匹配：top 级 > quality 级
            ref_lower = ref.lower()
            if any(kw in ref_lower for kw in top_model_keywords):
                score += 35  # 顶级模型（Opus 等）最高加分
            elif any(kw in ref_lower for kw in quality_keywords):
                score += 20  # 次级强模型
            # coding_strong + reasoning_high 的组合再加分
            if "coding_strong" in caps and "reasoning_high" in caps:
                score += 15
            elif "coding_strong" in caps or "reasoning_high" in caps:
                score += 8
            # 质量优先时成本不加分（避免免费弱模型挤掉强模型）
            # 本地加分也降低（除非也是强模型）
            if data.get("local"):
                score += 2
        else:
            # 常规模式：成本和延迟有权重
            if data.get("local"):
                score += 5
            cost_tier = data.get("cost_tier", "medium")
            latency_tier = data.get("latency_tier", "medium")
            score += {"low": 6, "medium": 3, "high": 0}.get(cost_tier, 3)
            score += {"fast": 5, "medium": 3, "slow": 0}.get(latency_tier, 3)

        # 健康惩罚
        if health.status == "degraded":
            score -= 6

        # ★ 基准测试实测加分（最高 +20 分，实测分 × 2）
        bench_boost = 0
        if benchmark_scores and ref in benchmark_scores and bench_category:
            model_bench = benchmark_scores[ref].get("categories", {})
            cat_score = model_bench.get(bench_category, {}).get("avg_score", 0)
            bench_boost = round(cat_score * 2, 1)  # 0-10 的实测分 → 0-20 的路由加分
            score += bench_boost

        entry = {"ref": ref, "score": score, **data}
        if bench_boost > 0:
            entry["bench_boost"] = bench_boost
        models.append(entry)

    models.sort(key=lambda x: x["score"], reverse=True)
    return models


def choose_with_cross_provider(candidates: List[Dict[str, Any]]) -> Tuple[Optional[str], List[str]]:
    if not candidates:
        return None, []
    primary = candidates[0]
    fallback_chain: List[str] = []
    used_providers = {primary.get("provider")}
    used_auth_groups = {primary.get("auth_group")}

    for item in candidates[1:]:
        if len(fallback_chain) >= 4:
            break
        provider = item.get("provider")
        auth_group = item.get("auth_group")
        if provider not in used_providers and auth_group not in used_auth_groups:
            fallback_chain.append(item["ref"])
            used_providers.add(provider)
            used_auth_groups.add(auth_group)

    for item in candidates[1:]:
        if len(fallback_chain) >= 4:
            break
        if item["ref"] not in fallback_chain:
            fallback_chain.append(item["ref"])

    return primary["ref"], fallback_chain


def survival_model(state: Dict[str, Any]) -> Optional[str]:
    viable = []
    for ref, data in state.get("models", {}).items():
        health = HealthInfo(**data.get("health", {}))
        if not health.healthy():
            continue
        score = 0
        caps = set(data.get("capabilities", []))
        if "survival_ready" in caps:
            score += 20
        if data.get("local"):
            score += 10
        if "cheap_fast" in caps:
            score += 6
        viable.append((score, ref))
    viable.sort(reverse=True)
    return viable[0][1] if viable else None


def maybe_degrade(reg: Registry, state: Dict[str, Any]) -> bool:
    p = reg.fail_cfg.get("policies", {}).get("degrade_mode", {})
    min_models = int(p.get("enter_if_healthy_models_below", 2))
    min_auth_groups = int(p.get("enter_if_auth_groups_healthy_below", 1))
    healthy_models = count_healthy_models(state)
    healthy_auth_groups = sum(1 for _, item in state.get("auth_groups", {}).items() if item.get("healthy_models", 0) > 0)
    return healthy_models < min_models or healthy_auth_groups < min_auth_groups


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    reg = Registry(root)
    state = ensure_state(root, args.state_file, args.openclaw_config)

    if args.record_failure:
        model_ref, error_type = args.record_failure
        cooldown = int(reg.fail_cfg.get("policies", {}).get("auth_errors", {}).get("cooldown_seconds", 1800))
        record_failure(state, model_ref, error_type, cooldown_seconds=cooldown)

    if args.record_success:
        record_success(state, args.record_success)

    # 加载基准测试评分
    bench_scores = load_benchmark_scores(args.benchmark_file)

    lead_role, review_roles, mode = determine_role(reg, args.task)
    degraded = maybe_degrade(reg, state)
    if degraded:
        mode = "degraded"
        review_roles = []
        lead_role = "emergency-scribe" if candidate_models_for_role(reg, state, "emergency-scribe", bench_scores) else "router-chief"

    lead_candidates = candidate_models_for_role(reg, state, lead_role, bench_scores)
    selected_model, fallback_chain = choose_with_cross_provider(lead_candidates)

    if not selected_model:
        role_cfg = reg.roles_cfg.get("roles", {}).get(lead_role, {})
        for fallback_role in role_cfg.get("fallback_roles", []):
            cands = candidate_models_for_role(reg, state, fallback_role, bench_scores)
            selected_model, fallback_chain = choose_with_cross_provider(cands)
            if selected_model:
                lead_role = fallback_role
                break

    survive = survival_model(state)
    if not selected_model and survive:
        selected_model = survive
        lead_role = "emergency-scribe"
        mode = "degraded"

    # Build system prompt for the lead role
    lead_prompt = reg.get_system_prompt(lead_role)
    role_meta = reg.get_role_metadata(lead_role)

    # Build review prompts
    review_prompts = {}
    for r in review_roles:
        rp = reg.get_system_prompt(r)
        if rp:
            review_prompts[r] = rp

    # i18n: provide titles in all available languages
    i18n = reg.i18n
    lead_titles_i18n = {lang: i18n.role_title(lead_role, lang) for lang in i18n.available_languages}
    mode_labels_i18n = {lang: i18n.mode_label(mode, lang) for lang in i18n.available_languages}

    result = {
        "mode": mode,
        "mode_labels": mode_labels_i18n,
        "complexity": infer_complexity(args.task),
        "lead_role": lead_role,
        "lead_title": i18n.role_title(lead_role),
        "lead_titles": lead_titles_i18n,
        "lead_system_prompt": lead_prompt,
        "review_roles": review_roles,
        "review_system_prompts": review_prompts if review_prompts else None,
        "selected_model": selected_model,
        "fallback_chain": fallback_chain,
        "survival_model": survive,
        "forbidden_actions": role_meta.get("forbidden_actions", []),
        "reasoning": {
            "degraded": degraded,
            "healthy_models": count_healthy_models(state),
            "healthy_auth_groups": sum(1 for _, item in state.get("auth_groups", {}).items() if item.get("healthy_models", 0) > 0),
            "benchmark_available": bool(bench_scores),
            "benchmark_category": ROLE_TO_BENCHMARK_CATEGORY.get(lead_role),
            "selected_model_bench_score": (
                bench_scores.get(selected_model, {}).get("categories", {})
                .get(ROLE_TO_BENCHMARK_CATEGORY.get(lead_role, ""), {})
                .get("avg_score")
            ) if selected_model and bench_scores else None,
            "task": args.task,
        },
    }

    if args.write_state:
        save_json(args.state_file, state)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
