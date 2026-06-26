from __future__ import annotations

from collections import defaultdict

from .ai_judge import AIJudge
from .utils import Scores, TaskResult, clamp, load_tier, normalize_score, now_iso, score_band_comment


def _rule_scores(result: TaskResult) -> tuple[int, int]:
    if result.status != "success":
        return 0, 0

    response_length = len(result.response.strip())
    sentence_count = sum(1 for chunk in result.response.replace("\r", "").splitlines() if chunk.strip())
    code_bonus = 6 if "```" in result.response else 0
    list_bonus = 5 if any(marker in result.response for marker in ("\n-", "\n*", "\n1.", "\n2.")) else 0
    verify_bonus = 6 if any(word in result.response for word in ["测试", "验证", "检查", "回归", "test", "verify", "check"]) else 0
    short_penalty = 14 if response_length < 70 else 6 if response_length < 120 else 0

    l1 = 52 + min(34, response_length // 9) + min(10, sentence_count * 2) + verify_bonus - short_penalty
    l2 = 46 + min(28, response_length // 12) + list_bonus + code_bonus + min(14, sentence_count * 2) - short_penalty
    return max(0, min(100, l1)), max(0, min(100, l2))


def score_results(raw_results: list[TaskResult], config: dict, soul) -> Scores:
    judge = AIJudge()
    dim_totals: dict[str, float] = defaultdict(float)
    dim_counts: dict[str, float] = defaultdict(float)
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_elapsed_ms = 0

    for result in raw_results:
        l1, l2 = _rule_scores(result)
        if result.status == "success":
            ai_payload = judge.judge(result.task_id, result.response, result.rubric or result.prompt)
        else:
            ai_payload = {"l3_score": 0, "l4_score": 0, "l5_score": 0, "reasoning": ""}
        result.rule_scores = {"L1": l1, "L2": l2}
        result.ai_scores = {
            "L3": ai_payload["l3_score"],
            "L4": ai_payload["l4_score"],
            "L5": ai_payload["l5_score"],
        }
        weighted = (
            l1 * config["scoring_layers"]["L1"]["weight"]
            + l2 * config["scoring_layers"]["L2"]["weight"]
            + ai_payload["l3_score"] * config["scoring_layers"]["L3"]["weight"]
            + ai_payload["l4_score"] * config["scoring_layers"]["L4"]["weight"]
            + ai_payload["l5_score"] * config["scoring_layers"]["L5"]["weight"]
        )
        result.total_score = normalize_score(weighted)
        result.reasoning = ai_payload["reasoning"]

        for key in result.primary_dimensions:
            dim_totals[key] += result.total_score
            dim_counts[key] += 1
        for key in result.secondary_dimensions:
            dim_totals[key] += result.total_score * 0.65
            dim_counts[key] += 0.65

        total_prompt_tokens += int(result.usage.get("prompt_tokens", 0))
        total_completion_tokens += int(result.usage.get("completion_tokens", 0))
        total_elapsed_ms += result.elapsed_ms

    dimensions: dict[str, int] = {}
    for key in config["dimensions"]:
        if key in {"cost", "speed"}:
            continue
        count = dim_counts.get(key, 0) or 1
        dimensions[key] = normalize_score(dim_totals.get(key, 0) / count)

    total_tokens = total_prompt_tokens + total_completion_tokens
    dimensions["cost"] = normalize_score(clamp(98 - total_tokens / 140, 10, 100))
    dimensions["speed"] = normalize_score(
        clamp(100 - (total_elapsed_ms / 1000) / max(1, config["task_timeout_seconds"] / 6), 10, 100)
    )

    total_score = normalize_score(
        sum(dimensions[key] * meta["weight"] for key, meta in config["dimensions"].items())
    )
    tier = load_tier(config, total_score)
    lang = config.get("lang", "zh")
    expected_task_count = int(config.get("expected_task_count") or len(raw_results) or 0)

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
        judge_model=judge.model_name,
        anonymous=bool(config.get("anonymous", False)),
    )
