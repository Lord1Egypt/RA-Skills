import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    exact = text_rules.count_matches(response, [r"80\.00", r"75\.00", r"67\.50", r"76\.28", r"74\.28"])
    explanation = text_rules.contains_any(response, [r"7\.2 折", r"先打 8 折再打 9 折"]) and text_rules.contains_any(response, [r"满减", r"不等价|等价"])
    rule_score = 0.75 * min(100, exact / 5 * 100) + 0.25 * (100 if explanation else 30)
    return {
        "scores": {"brain": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["brain"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score), "exact_hits": exact},
    }
