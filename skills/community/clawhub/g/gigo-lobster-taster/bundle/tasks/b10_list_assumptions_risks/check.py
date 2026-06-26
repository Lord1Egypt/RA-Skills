import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    bullets = text_rules.bullet_like_lines(response)
    assumptions = text_rules.count_matches(response, [r"假设"], ignore_case=False) + sum(1 for line in bullets if "假设" in line)
    risks = text_rules.count_matches(response, [r"影响.*高|影响.*中|影响.*低"]) + text_rules.count_matches(response, [r"概率.*高|概率.*中|概率.*低"])
    open_questions = text_rules.count_matches(response, [r"开放问题|拍板|需要老板"], ignore_case=False)
    coverage = text_rules.count_matches(response, [r"业务", r"技术", r"合规", r"运营"])
    rule_score = 0.3 * min(100, assumptions / 8 * 100) + 0.3 * min(100, risks / 12 * 100) + 0.2 * min(100, coverage / 4 * 100) + 0.2 * (100 if open_questions else 50)
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
