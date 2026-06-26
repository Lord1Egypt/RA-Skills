import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    questions = text_rules.numbered_question_lines(response)
    count_score = 100 if len(questions) == 3 else max(0, 100 - 35 * abs(len(questions) - 3))
    short_score = min(100, sum(1 for line in questions if text_rules.zh_length(line) <= 30) / max(len(questions), 1) * 100)
    no_preface = 100 if not text_rules.contains_any(response, [r"先说明|以下是|我有几个问题"]) else 70
    rule_score = 0.45 * count_score + 0.35 * short_score + 0.2 * no_preface
    return {
        "scores": {"brain": int(rule_score), "soul": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["brain", "soul"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score), "question_count": len(questions)},
    }
