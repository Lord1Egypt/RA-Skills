from __future__ import annotations

from collections import defaultdict

from .utils import Scores, TaskResult, calculate_v2_speed_score, clamp, load_tier, normalize_score, now_iso, score_band_comment


def _reliability_adjusted_dimension_average(raw_average: float, sample_count: int, core_average: float, task_count: int) -> float:
    if task_count < 20 or sample_count >= 12:
        return raw_average
    if raw_average <= core_average:
        return raw_average
    prior_weight = max(0, 12 - sample_count)
    return (raw_average * sample_count + core_average * prior_weight) / max(sample_count + prior_weight, 1)


def score_results_v2(raw_results: list[TaskResult], config: dict, soul) -> Scores:
    dim_totals: dict[str, float] = defaultdict(float)
    dim_counts: dict[str, float] = defaultdict(float)
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_elapsed_ms = 0
    judge_models: list[str] = []

    for result in raw_results:
        task_success = result.status == "success" and not result.error
        for receipt in result.judge_receipts:
            model = str(receipt.get("judge_model") or "")
            if model:
                judge_models.append(model)

        for key in result.primary_dimensions:
            task_score = int(result.task_scores.get(key, result.total_score)) if task_success else 0
            dim_totals[key] += task_score
            dim_counts[key] += 1.0
        for key in result.secondary_dimensions:
            task_score = int(result.task_scores.get(key, round(result.total_score * 0.65))) if task_success else 0
            dim_totals[key] += task_score
            dim_counts[key] += 1.0

        total_prompt_tokens += int(result.usage.get("prompt_tokens", 0))
        total_completion_tokens += int(result.usage.get("completion_tokens", 0))
        total_elapsed_ms += int(result.elapsed_ms)

    dimensions: dict[str, int] = {}
    core_total = sum(dim_totals[key] for key in dim_totals if key not in {"cost", "speed"})
    core_count = sum(dim_counts[key] for key in dim_counts if key not in {"cost", "speed"})
    core_average = core_total / core_count if core_count else 0.0
    for key in config["dimensions"]:
        if key in {"cost", "speed"}:
            continue
        if not dim_counts.get(key):
            continue
        dimensions[key] = normalize_score(
            _reliability_adjusted_dimension_average(
                dim_totals[key] / dim_counts[key],
                int(dim_counts[key]),
                core_average,
                len(raw_results),
            )
        )

    total_tokens = total_prompt_tokens + total_completion_tokens
    task_count = max(1, len(raw_results))
    baseline_tokens = max(int(config.get("v2_cost_baseline_tokens", 50000)), task_count * 3500)
    scale_tokens = max(int(config.get("v2_cost_scale_tokens", 120000)), task_count * 5000)
    dimensions["cost"] = normalize_score(clamp(100 - ((total_tokens - baseline_tokens) / max(scale_tokens, 1)) * 100, 0, 100))
    dimensions["speed"] = calculate_v2_speed_score(total_elapsed_ms, len(raw_results), config)

    total_score = normalize_score(
        sum(dimensions.get(key, 0) * meta["weight"] for key, meta in config["dimensions"].items())
    )
    tier = load_tier(config, total_score)
    lang = config.get("lang", "zh")
    expected_task_count = int(config.get("expected_task_count") or len(raw_results) or 0)
    judge_model = judge_models[0] if judge_models else "local-v2"

    return Scores(
        lobster_name=soul.name,
        total_score=total_score,
        tier=tier["key"],
        tier_name=f"{tier['emoji']} {tier[lang]}",
        tier_emoji=tier["emoji"],
        dimensions=dimensions,
        task_breakdowns=raw_results,
        summary_comment=score_band_comment(total_score, lang),
        lang=lang,
        timestamp=now_iso(),
        partial=bool(expected_task_count and len(raw_results) < expected_task_count),
        judge_model=judge_model,
        anonymous=bool(config.get("anonymous", False)),
        bundle_version=str(config.get("task_bundle_version", "unknown")),
        bundle_hash=str(config.get("task_bundle_hash", "")),
    )
