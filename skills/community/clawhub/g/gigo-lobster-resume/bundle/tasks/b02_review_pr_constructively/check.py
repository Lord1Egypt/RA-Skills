import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    length_score = text_rules.score_length(300, text_rules.zh_length(response))
    bug = text_rules.contains_any(response, [r"expire_at.*None|None.*expire_at|永久券|TypeError"])
    style = text_rules.count_matches(response, [r"\bchk\b|函数名|命名", r"嵌套|提前 return|扁平"])
    gentle = text_rules.contains_any(response, [r"建议|可以|不错|辛苦|先说结论|必须改"])
    rule_score = 0.25 * length_score + 0.35 * (100 if bug else 20) + 0.25 * min(100, style * 50) + 0.15 * (100 if gentle else 45)
    return {
        "scores": {"soul": int(rule_score), "brain": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["soul", "brain"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score), "bug": bug, "style_points": style, "gentle": gentle},
    }
