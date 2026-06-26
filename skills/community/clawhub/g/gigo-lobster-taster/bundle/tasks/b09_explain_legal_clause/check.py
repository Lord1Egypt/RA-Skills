import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    terms = text_rules.count_matches(response, [r"非独占", r"永久", r"商业化", r"不可撤销"])
    risks = text_rules.count_matches(response, [r"风险", r"训练", r"商业化", r"授权不能收回", r"数据"])
    redlines = text_rules.count_matches(response, [r"删除.*永久", r"限定.*匿名", r"去标识", r"仅用于", r"可撤回"])
    rule_score = 0.35 * min(100, terms / 4 * 100) + 0.3 * min(100, risks / 2 * 100) + 0.35 * min(100, redlines / 2 * 100)
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
