import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    frameworks = text_rules.count_matches(response, [r"React", r"Vue", r"Svelte"], ignore_case=False)
    dims = text_rules.count_matches(response, [r"生态|富文本|协作", r"团队|学习成本|适配", r"维护|可维护|长期"])
    recommend = text_rules.contains_any(response, [r"推荐.*React|建议.*React|最终选.*React|推荐.*Vue|推荐.*Svelte"])
    reasons = text_rules.count_matches(response, [r"决定性|理由|因为"], ignore_case=False)
    rule_score = 0.35 * min(100, frameworks / 3 * 100) + 0.3 * min(100, dims / 3 * 100) + 0.2 * (100 if recommend else 35) + 0.15 * min(100, reasons * 40)
    return {
        "scores": {"brain": int(rule_score), "soul": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["brain", "soul"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score)},
    }
