#!/usr/bin/env python3
"""Critic for the generic-skill lane.

Phase 1 adds an optional skill-evaluator evidence mode so ranking can use
rubric/category/boundary evidence in addition to the original heuristic.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

# LLM Judge — import from sibling interfaces/ package
_INTERFACES_DIR = str(Path(__file__).resolve().parents[1] / "interfaces")
if _INTERFACES_DIR not in sys.path:
    sys.path.insert(0, _INTERFACES_DIR)

from rubric_evidence import build_evaluator_evidence
from lib.common import (
    KEEP_CATEGORIES,
    SCHEMA_VERSION,
    protected_target,
    read_json,
    utc_now_iso,
    write_json,
)
from lib.state_machine import (
    DEFAULT_STATE_ROOT,
    ensure_tree,
    update_state,
)
from llm_judge import LLMJudge, JudgeConfig, JudgeVerdict

logger = logging.getLogger(__name__)

DEFAULT_CATEGORY_WEIGHTS = {
    "docs": 4.0,
    "reference": 3.5,
    "guardrail": 3.5,
    "workflow": 1.5,
    "prompt": 1.0,
    "tests": 1.5,
}
CATEGORY_BONUS = DEFAULT_CATEGORY_WEIGHTS  # backward compat alias
RISK_PENALTY = {"low": 0.0, "medium": 1.5, "high": 3.0}  # ranking signal only; high-risk is hard-rejected by build_recommendation
HEURISTIC_WEIGHT = 0.5
EVALUATOR_WEIGHT = 0.5

# Blended weight schemes when LLM judge is enabled
# heuristic + llm only
HEURISTIC_WEIGHT_WITH_LLM = 0.3
LLM_WEIGHT_WITHOUT_EVALUATOR = 0.7
# heuristic + llm + evaluator (all three)
HEURISTIC_WEIGHT_ALL_THREE = 0.2
LLM_WEIGHT_ALL_THREE = 0.5
EVALUATOR_WEIGHT_ALL_THREE = 0.3


# ---------------------------------------------------------------------------
# Multi-reviewer panel (Phase 2A)
# ---------------------------------------------------------------------------


class ReviewerConfig:
    """Configuration for a single reviewer in the panel."""

    def __init__(
        self,
        name: str,
        category_weights: dict | None = None,
        risk_sensitivity: float = 1.0,
        use_evaluator: bool = False,
    ):
        self.name = name
        self.category_weights = category_weights or dict(DEFAULT_CATEGORY_WEIGHTS)
        self.risk_sensitivity = risk_sensitivity
        self.use_evaluator = use_evaluator


DEFAULT_REVIEWERS = [
    ReviewerConfig(
        "structural",
        category_weights={
            "docs": 5.0, "reference": 4.0, "guardrail": 4.0,
            "workflow": 2.0, "prompt": 1.5, "tests": 2.0,
        },
    ),
    ReviewerConfig(
        "conservative",
        risk_sensitivity=1.5,
        category_weights={
            "docs": 3.0, "reference": 3.0, "guardrail": 5.0,
            "workflow": 1.0, "prompt": 0.5, "tests": 1.0,
        },
    ),
    ReviewerConfig(
        "user_advocate",
        risk_sensitivity=0.8,
        category_weights={
            "docs": 4.0, "reference": 2.0, "guardrail": 2.0,
            "workflow": 4.0, "prompt": 3.0, "tests": 1.0,
        },
    ),
    ReviewerConfig(
        "security_auditor",
        risk_sensitivity=2.0,
        category_weights={
            "docs": 2.0, "reference": 2.0, "guardrail": 5.0,
            "workflow": 0.5, "prompt": 0.5, "tests": 3.0,
        },
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score and rank generic-skill candidates")
    parser.add_argument("--input", required=True, help="Candidate artifact JSON")
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--output", default=None)
    parser.add_argument(
        "--use-evaluator-evidence",
        action="store_true",
        help="Blend Phase 1 skill-evaluator rubric/category/boundary evidence into scoring.",
    )
    parser.add_argument(
        "--panel",
        action="store_true",
        help="Enable multi-reviewer blind panel scoring (Phase 2A).",
    )
    parser.add_argument(
        "--llm-judge",
        choices=["claude", "openai", "mock"],
        default=None,
        dest="llm_judge",
        help="Enable LLM-as-Judge evaluation. Backend: claude, openai, or mock.",
    )
    return parser.parse_args()


def heuristic_score(candidate: dict) -> tuple[float, float]:
    category = candidate.get("category", "unknown")
    risk_level = candidate.get("risk_level", "medium")
    source_refs = candidate.get("source_refs", []) or []
    executor_support = bool(candidate.get("executor_support"))
    base = 2.0
    category_bonus = 0.0  # category gating handled by build_recommendation
    source_signal = min(len(source_refs), 3) * 0.5
    support_bonus = 0.5 if executor_support else 0.0
    protected_penalty = 2.5 if protected_target(candidate.get("target_path", "")) else 0.0
    risk_penalty = RISK_PENALTY.get(risk_level, 2.0) + protected_penalty
    score = max(0.0, min(10.0, round(base + category_bonus + source_signal + support_bonus - risk_penalty, 2)))
    return score, round(risk_penalty, 2)


def build_blockers(
    candidate: dict,
    *,
    evidence: dict | None = None,
    llm_verdict: JudgeVerdict | None = None,
) -> list[str]:
    blockers: list[str] = []
    category = candidate.get("category", "unknown")
    risk_level = candidate.get("risk_level", "medium")

    if protected_target(candidate.get("target_path", "")):
        blockers.append("protected_target")
    if not candidate.get("executor_support"):
        blockers.append("executor_not_supported")
    if category not in KEEP_CATEGORIES:
        blockers.append("not_auto_keep_category")
    if risk_level != "low":
        blockers.append(f"risk_{risk_level}")

    if evidence:
        skill_level = evidence.get("skill_profile", {}).get("skill_level")
        evaluator_verdict = evidence.get("verdict")
        if skill_level == "Level 1" and category in {"workflow", "prompt", "tests"}:
            blockers.append("skill_level_insufficient_for_structural_change")
        if evaluator_verdict == "reject":
            blockers.append("evaluator_reject")

    if llm_verdict and llm_verdict.decision == "reject":
        blockers.append("llm_judge_reject")
    return blockers


def build_recommendation(candidate: dict, score: float, blockers: list[str], evidence: dict | None = None) -> str:
    is_low_risk_keep = (
        candidate.get("category") in KEEP_CATEGORIES
        and candidate.get("risk_level") == "low"
        and bool(candidate.get("executor_support"))
        and not protected_target(candidate.get("target_path", ""))
    )
    if evidence:
        boundary = evidence.get("boundary", {})
        if is_low_risk_keep and boundary.get("auto_promote_eligible") and evidence.get("verdict") != "reject":
            return "accept_for_execution"
        if evidence.get("verdict") == "reject" or score < 2.0:
            return "reject"
        return "hold"

    if is_low_risk_keep:
        return "accept_for_execution"
    if candidate.get("risk_level") == "high" or score < 2.0:
        return "reject"
    return "hold"


def build_judge_notes(candidate: dict, recommendation: str, blockers: list[str], evidence: dict | None = None) -> list[str]:
    judge_notes: list[str] = []
    if recommendation == "accept_for_execution":
        judge_notes.append("低风险 + 文档/引用类候选，可交给第一版 executor。")
    if "executor_not_supported" in blockers:
        judge_notes.append("当前 executor 只支持 docs/reference/guardrail 的简单文案追加。")
    if "protected_target" in blockers:
        judge_notes.append("目标路径属于保护区域，需要人工 gate。")
    if "skill_level_insufficient_for_structural_change" in blockers:
        judge_notes.append("skill-evaluator rubric 认为当前目标 skill 级别过低，不宜直接推进结构性改动。")
    if recommendation == "hold":
        judge_notes.append("先进入 pending_promote / human review，等待后续 richer judge。")
    if recommendation == "reject":
        judge_notes.append("当前判断认为收益不足、证据不足或风险过高。")
    if evidence:
        rubric = evidence.get("rubric", {})
        judge_notes.append(
            f"Phase 1 evaluator evidence: {rubric.get('evaluator_category', 'process-type')} rubric, verdict={evidence.get('verdict')}, overall={evidence.get('overall_score_10', 0):.2f}/10。"
        )
        for limitation in evidence.get("limitations", [])[:2]:
            judge_notes.append(limitation)
    return judge_notes


def score_candidate(
    candidate: dict,
    *,
    use_evaluator_evidence: bool = False,
    llm_judge: LLMJudge | None = None,
    target_content: str = "",
) -> dict:
    heuristic, risk_penalty = heuristic_score(candidate)

    # Semantic relevance check
    relevance_penalty = 0.0
    if target_content:
        content_lines = candidate.get("execution_plan", {}).get("content_lines", [])
        if content_lines:
            candidate_words = set()
            for line in content_lines:
                candidate_words.update(w.lower() for w in line.split() if len(w) > 3)
            target_words = set(w.lower() for w in target_content.split() if len(w) > 3)
            overlap = candidate_words & target_words
            if len(candidate_words) > 0 and len(overlap) == 0:
                relevance_penalty = 2.0
    heuristic = max(0.0, heuristic - relevance_penalty)

    # Diff size factor: larger changes get slightly lower scores (more scrutiny needed)
    content_lines = candidate.get("execution_plan", {}).get("content_lines", [])
    total_lines = sum(len(line) for line in content_lines) if content_lines else 0
    if total_lines > 500:
        heuristic = max(0.0, heuristic - 1.0)

    evidence = build_evaluator_evidence(candidate) if use_evaluator_evidence else None
    evaluator_score = evidence.get("overall_score_10") if evidence else None

    # --- LLM Judge evaluation ---
    llm_verdict: JudgeVerdict | None = None
    if llm_judge is not None:
        try:
            llm_verdict = llm_judge.evaluate(candidate, target_content=target_content)
        except Exception as exc:
            logger.warning("LLM judge evaluation failed: %s", exc)

    # --- Blended scoring ---
    llm_score_10 = llm_verdict.score * 10.0 if llm_verdict else None

    if evaluator_score is not None and llm_score_10 is not None:
        # All three sources
        final_score = round(
            heuristic * HEURISTIC_WEIGHT_ALL_THREE
            + llm_score_10 * LLM_WEIGHT_ALL_THREE
            + evaluator_score * EVALUATOR_WEIGHT_ALL_THREE,
            2,
        )
    elif llm_score_10 is not None:
        # Heuristic + LLM only
        final_score = round(
            heuristic * HEURISTIC_WEIGHT_WITH_LLM
            + llm_score_10 * LLM_WEIGHT_WITHOUT_EVALUATOR,
            2,
        )
    elif evaluator_score is not None:
        # Heuristic + evaluator only (original path)
        final_score = round(
            heuristic * HEURISTIC_WEIGHT
            + evaluator_score * EVALUATOR_WEIGHT,
            2,
        )
    else:
        final_score = heuristic

    blockers = build_blockers(candidate, evidence=evidence, llm_verdict=llm_verdict)
    recommendation = build_recommendation(candidate, final_score, blockers, evidence=evidence)
    judge_notes = build_judge_notes(candidate, recommendation, blockers, evidence=evidence)

    # Determine adapter name
    if llm_judge and use_evaluator_evidence:
        adapter_name = "heuristic+evaluator+llm-judge"
    elif llm_judge:
        adapter_name = "heuristic+llm-judge"
    elif use_evaluator_evidence:
        adapter_name = "heuristic+evaluator-phase1"
    else:
        adapter_name = "rule-based-heuristic-v1"

    payload = {
        **candidate,
        "score": final_score,
        "heuristic_score": heuristic,
        "risk_penalty": risk_penalty,
        "recommendation": recommendation,
        "blockers": blockers,
        "judge_notes": judge_notes,
        "judge_adapter": {
            "name": adapter_name,
            "future_replacement": "full-skill-evaluator-adapter",
            "evaluated_at": utc_now_iso(),
            "evaluator_evidence_enabled": use_evaluator_evidence,
            "llm_judge_enabled": llm_judge is not None,
        },
    }
    if evidence:
        payload["score_components"] = {
            "heuristic_weight": HEURISTIC_WEIGHT if llm_judge is None else HEURISTIC_WEIGHT_ALL_THREE,
            "evaluator_weight": EVALUATOR_WEIGHT if llm_judge is None else EVALUATOR_WEIGHT_ALL_THREE,
            "heuristic_score": heuristic,
            "evaluator_score": evaluator_score,
        }
        if llm_score_10 is not None:
            payload["score_components"]["llm_weight"] = LLM_WEIGHT_ALL_THREE
            payload["score_components"]["llm_score"] = llm_score_10
        payload["evaluator_score"] = evaluator_score
        payload["evaluator_evidence"] = evidence
    elif llm_score_10 is not None:
        payload["score_components"] = {
            "heuristic_weight": HEURISTIC_WEIGHT_WITH_LLM,
            "llm_weight": LLM_WEIGHT_WITHOUT_EVALUATOR,
            "heuristic_score": heuristic,
            "llm_score": llm_score_10,
        }

    if llm_verdict is not None:
        payload["llm_verdict"] = {
            "score": llm_verdict.score,
            "decision": llm_verdict.decision,
            "reasoning": llm_verdict.reasoning,
            "dimensions": llm_verdict.dimensions,
            "confidence": llm_verdict.confidence,
            "suggestions": llm_verdict.suggestions,
        }
    return payload


def _heuristic_score_with_config(candidate: dict, config: ReviewerConfig) -> tuple[float, float]:
    """Compute heuristic score using reviewer-specific category weights and risk sensitivity."""
    category = candidate.get("category", "unknown")
    risk_level = candidate.get("risk_level", "medium")
    source_refs = candidate.get("source_refs", []) or []
    executor_support = bool(candidate.get("executor_support"))
    base = 2.0
    category_bonus = config.category_weights.get(category, 0.0)
    source_signal = min(len(source_refs), 3) * 0.5
    support_bonus = 0.5 if executor_support else 0.0
    protected_penalty = 2.5 if protected_target(candidate.get("target_path", "")) else 0.0
    raw_risk = RISK_PENALTY.get(risk_level, 2.0) + protected_penalty
    risk_penalty = round(raw_risk * config.risk_sensitivity, 2)
    score = max(0.0, min(10.0, round(base + category_bonus + source_signal + support_bonus - risk_penalty, 2)))
    return score, risk_penalty


def _user_impact_bonus(candidate: dict) -> float:
    """user_advocate reviewer: bonus for user-facing improvements."""
    rationale = candidate.get("rationale", "").lower()
    summary = candidate.get("proposed_change_summary", "").lower()
    text = rationale + " " + summary
    user_keywords = ["user", "用户", "读者", "体验", "experience", "usability", "误用", "misuse"]
    return 0.5 if any(k in text for k in user_keywords) else 0.0


def _security_penalty(candidate: dict) -> float:
    """security_auditor reviewer: penalty for security-sensitive changes."""
    content_lines = candidate.get("execution_plan", {}).get("content_lines", [])
    text = " ".join(content_lines).lower() if content_lines else ""
    risk_keywords = ["password", "token", "secret", "api_key", "credential", "auth", "exec(", "eval(", "os.system"]
    return 2.0 if any(k in text for k in risk_keywords) else 0.0


def score_candidate_with_config(
    candidate: dict,
    config: ReviewerConfig,
    *,
    llm_judge: LLMJudge | None = None,
    target_content: str = "",
) -> dict:
    """Score a candidate using a specific ReviewerConfig.

    Mirrors score_candidate() but substitutes the reviewer's category_weights
    and risk_sensitivity.  Evaluator evidence is blended only when
    config.use_evaluator is True.  LLM judge is blended when provided.
    """
    heuristic, risk_penalty = _heuristic_score_with_config(candidate, config)
    if config.name == "user_advocate":
        heuristic = min(10.0, heuristic + _user_impact_bonus(candidate))
    elif config.name == "security_auditor":
        heuristic = max(0.0, heuristic - _security_penalty(candidate))
    evidence = build_evaluator_evidence(candidate) if config.use_evaluator else None
    evaluator_score = evidence.get("overall_score_10") if evidence else None

    # --- LLM Judge evaluation ---
    llm_verdict: JudgeVerdict | None = None
    if llm_judge is not None:
        try:
            llm_verdict = llm_judge.evaluate(candidate, target_content=target_content)
        except Exception as exc:
            logger.warning("LLM judge evaluation failed for reviewer %s: %s", config.name, exc)

    llm_score_10 = llm_verdict.score * 10.0 if llm_verdict else None

    # --- Blended scoring (same logic as score_candidate) ---
    if evaluator_score is not None and llm_score_10 is not None:
        final_score = round(
            heuristic * HEURISTIC_WEIGHT_ALL_THREE
            + llm_score_10 * LLM_WEIGHT_ALL_THREE
            + evaluator_score * EVALUATOR_WEIGHT_ALL_THREE, 2)
    elif llm_score_10 is not None:
        final_score = round(
            heuristic * HEURISTIC_WEIGHT_WITH_LLM
            + llm_score_10 * LLM_WEIGHT_WITHOUT_EVALUATOR, 2)
    elif evaluator_score is not None:
        final_score = round(
            heuristic * HEURISTIC_WEIGHT
            + evaluator_score * EVALUATOR_WEIGHT, 2)
    else:
        final_score = heuristic

    blockers = build_blockers(candidate, evidence=evidence, llm_verdict=llm_verdict)
    recommendation = build_recommendation(candidate, final_score, blockers, evidence=evidence)
    judge_notes = build_judge_notes(candidate, recommendation, blockers, evidence=evidence)

    payload = {
        **candidate,
        "score": final_score,
        "heuristic_score": heuristic,
        "risk_penalty": risk_penalty,
        "recommendation": recommendation,
        "blockers": blockers,
        "judge_notes": judge_notes,
        "reviewer": config.name,
        "judge_adapter": {
            "name": f"multi-reviewer-{config.name}",
            "future_replacement": "full-skill-evaluator-adapter",
            "evaluated_at": utc_now_iso(),
            "evaluator_evidence_enabled": config.use_evaluator,
            "llm_judge_enabled": llm_judge is not None,
        },
    }
    if evidence:
        payload["score_components"] = {
            "heuristic_weight": HEURISTIC_WEIGHT if llm_judge is None else HEURISTIC_WEIGHT_ALL_THREE,
            "evaluator_weight": EVALUATOR_WEIGHT if llm_judge is None else EVALUATOR_WEIGHT_ALL_THREE,
            "heuristic_score": heuristic,
            "evaluator_score": evaluator_score,
        }
        if llm_score_10 is not None:
            payload["score_components"]["llm_weight"] = LLM_WEIGHT_ALL_THREE
            payload["score_components"]["llm_score"] = llm_score_10
        payload["evaluator_score"] = evaluator_score
        payload["evaluator_evidence"] = evidence
    elif llm_score_10 is not None:
        payload["score_components"] = {
            "heuristic_weight": HEURISTIC_WEIGHT_WITH_LLM,
            "llm_weight": LLM_WEIGHT_WITHOUT_EVALUATOR,
            "heuristic_score": heuristic,
            "llm_score": llm_score_10,
        }
    if llm_verdict is not None:
        payload["llm_verdict"] = {
            "score": llm_verdict.score,
            "decision": llm_verdict.decision,
            "reasoning": llm_verdict.reasoning,
            "dimensions": llm_verdict.dimensions,
            "confidence": llm_verdict.confidence,
            "suggestions": llm_verdict.suggestions,
        }
    return payload


def run_multi_reviewer_panel(
    candidate: dict,
    reviewers: list[ReviewerConfig] | None = None,
    *,
    llm_judge: LLMJudge | None = None,
    target_content: str = "",
) -> dict:
    """Run blind multi-reviewer panel on a candidate.

    Each reviewer scores independently (no visibility into other scores).
    The panel then determines consensus via cognitive labels:
      - CONSENSUS: all reviewers agree on the recommendation
      - VERIFIED:  2+ reviewers agree (majority)
      - DISPUTED:  no majority; default recommendation becomes "hold"
    """
    reviewers = reviewers or DEFAULT_REVIEWERS
    reviews: list[dict] = []
    for reviewer in reviewers:
        scored = score_candidate_with_config(
            candidate, reviewer,
            llm_judge=llm_judge, target_content=target_content,
        )
        review_entry = {
            "reviewer": reviewer.name,
            "score": scored["score"],
            "recommendation": scored["recommendation"],
        }
        if "llm_verdict" in scored:
            review_entry["llm_score"] = scored["llm_verdict"]["score"]
        reviews.append(review_entry)

    # --- Determine consensus ---
    recommendations = [r["recommendation"] for r in reviews]
    unique_recs = set(recommendations)

    if len(unique_recs) == 1:
        label = "CONSENSUS"
        final_rec = recommendations[0]
    else:
        from collections import Counter
        counts = Counter(recommendations)
        most_common = counts.most_common()
        top_count = most_common[0][1]
        # Check for tie: if top two have equal count, treat as split
        if len(most_common) >= 2 and most_common[0][1] == most_common[1][1]:
            label = "SPLIT"
            final_rec = "hold"  # Conservative default on tie
        elif top_count >= 2:
            label = "VERIFIED"
            final_rec = most_common[0][0]
        else:
            label = "DISPUTED"
            final_rec = "hold"

    avg_score = sum(r["score"] for r in reviews) / len(reviews)
    return {
        "panel_reviews": reviews,
        "cognitive_label": label,
        "final_recommendation": final_rec,
        "aggregated_score": round(avg_score, 2),
    }


def main() -> int:
    args = parse_args()
    state_root = Path(args.state_root).expanduser().resolve()
    ensure_tree(state_root)

    candidate_artifact = read_json(Path(args.input).expanduser().resolve())
    run_id = candidate_artifact["run_id"]
    target_path = candidate_artifact["target"]["path"]
    raw_candidates = candidate_artifact.get("candidates", [])

    # --- LLM Judge setup ---
    llm_judge_instance: LLMJudge | None = None
    if args.llm_judge:
        llm_judge_instance = LLMJudge(JudgeConfig(backend=args.llm_judge))

    # --- Read target skill content for LLM context ---
    target_content = ""
    if llm_judge_instance:
        tp = Path(target_path)
        skill_md = tp / "SKILL.md" if tp.is_dir() else tp.parent / "SKILL.md"
        if skill_md.exists():
            try:
                target_content = skill_md.read_text(encoding="utf-8")
            except Exception as exc:
                logger.warning("Could not read target SKILL.md: %s", exc)

    if args.panel:
        # Multi-reviewer panel mode (Phase 2A) — now integrates LLM judge
        panel_results = []
        for candidate in raw_candidates:
            panel = run_multi_reviewer_panel(
                candidate,
                llm_judge=llm_judge_instance,
                target_content=target_content,
            )
            panel_results.append({
                **candidate,
                "score": panel["aggregated_score"],
                "recommendation": panel["final_recommendation"],
                "panel": panel,
            })
        ranked_candidates = sorted(panel_results, key=lambda item: item["score"], reverse=True)
    else:
        ranked_candidates = sorted(
            [
                score_candidate(
                    candidate,
                    use_evaluator_evidence=args.use_evaluator_evidence,
                    llm_judge=llm_judge_instance,
                    target_content=target_content,
                )
                for candidate in raw_candidates
            ],
            key=lambda item: item["score"],
            reverse=True,
        )

    output_path = Path(args.output).expanduser().resolve() if args.output else state_root / "rankings" / f"{run_id}.json"
    ranking_artifact = {
        "schema_version": SCHEMA_VERSION,
        "lane": candidate_artifact.get("lane", "generic-skill"),
        "run_id": run_id,
        "stage": "ranked",
        "status": "success",
        "created_at": utc_now_iso(),
        "source_candidate_artifact": args.input,
        "target": candidate_artifact["target"],
        "critic_mode": (
            "multi-reviewer-panel" if args.panel
            else "heuristic+evaluator+llm-judge" if args.use_evaluator_evidence and args.llm_judge
            else "heuristic+llm-judge" if args.llm_judge
            else "heuristic+evaluator-phase1" if args.use_evaluator_evidence
            else "heuristic-only"
        ),
        "scored_candidates": ranked_candidates,
        "summary": {
            "accept_for_execution": sum(1 for item in ranked_candidates if item["recommendation"] == "accept_for_execution"),
            "hold": sum(1 for item in ranked_candidates if item["recommendation"] == "hold"),
            "reject": sum(1 for item in ranked_candidates if item["recommendation"] == "reject"),
            "evaluator_evidence_enabled": args.use_evaluator_evidence,
            "llm_judge_enabled": args.llm_judge is not None,
            "llm_judge_backend": args.llm_judge,
        },
        "next_step": "execute_candidate",
        "next_owner": "executor",
        "truth_anchor": str(output_path),
    }
    write_json(output_path, ranking_artifact)
    update_state(
        state_root,
        run_id=run_id,
        stage="ranked",
        status="success",
        target_path=target_path,
        truth_anchor=str(output_path),
        extra={
            "ranked_candidate_count": len(ranked_candidates),
            "top_candidate_id": ranked_candidates[0]["id"] if ranked_candidates else None,
            "critic_mode": ranking_artifact["critic_mode"],
        },
    )
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
