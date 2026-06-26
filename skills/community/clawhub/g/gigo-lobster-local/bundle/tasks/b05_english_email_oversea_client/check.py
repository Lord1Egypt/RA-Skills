import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    words = text_rules.en_word_count(response)
    subject = text_rules.contains_any(response, [r"(?m)^subject\s*:", r"(?m)^re:"])
    banned = text_rules.contains_any(response, [r"hope this email finds you well"])
    differentiator = text_rules.contains_any(response, [r"80\+\s*评分项|80\+\s*evaluation|response sections|extract .* scoring"])
    boundary = text_rules.contains_any(response, [r"mainland|china|legal corpus|人工|manual review"])
    next_step = text_rules.contains_any(response, [r"30-minute demo|30 minute demo|sample rfp|next week|meeting"])
    rule_score = 0.2 * text_rules.score_length(220, words) + 0.2 * (100 if subject else 30) + 0.2 * (0 if banned else 100) + 0.2 * (100 if differentiator else 30) + 0.1 * (100 if boundary else 40) + 0.1 * (100 if next_step else 40)
    return {
        "scores": {"soul": int(rule_score), "brain": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["soul", "brain"],
        },
        "details": {"response_length": len(response), "words": words, "rule_score": int(rule_score)},
    }
