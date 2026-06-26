import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    length_score = text_rules.score_length(300, text_rules.zh_length(response))
    analogy = text_rules.contains_any(response, [r"像", r"好比", r"类似", r"目录", r"索引页", r"字典"])
    forbidden = text_rules.count_matches(response, [r"B-?Tree", r"哈希", r"hash", r"复杂度", r"O\("])
    advice = text_rules.contains_any(response.splitlines()[-1] if response.splitlines() else response, [r"适合|建议|当.*查询|经常.*查|频繁"])
    rule_score = 0.35 * length_score + 0.25 * (100 if analogy else 40) + 0.25 * (100 - min(100, forbidden * 45)) + 0.15 * (100 if advice else 45)
    return {
        "scores": {"soul": int(rule_score), "brain": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["soul", "brain"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score), "analogy": analogy, "forbidden_terms": forbidden, "advice": advice},
    }
