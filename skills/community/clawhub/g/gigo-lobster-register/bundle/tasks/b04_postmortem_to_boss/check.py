import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    length_score = text_rules.score_length(200, text_rules.zh_length(response))
    sections = text_rules.count_matches(response, [r"是什么", r"为什么", r"怎么办"])
    improvements = text_rules.count_matches(response, [r"worker.*告警|告警.*worker", r"回滚|灰度|监控|测试|过滤器|模板"])
    blame = text_rules.contains_any(response, [r"小王.*责任|小王.*失误|甩锅"])
    empty_words = text_rules.contains_any(response, [r"加强意识|引以为戒|高度重视"])
    rule_score = 0.2 * length_score + 0.3 * min(100, sections / 3 * 100) + 0.35 * min(100, improvements / 2 * 100) + 0.15 * (100 - (45 if blame else 0) - (30 if empty_words else 0))
    return {
        "scores": {"soul": int(rule_score), "brain": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["soul", "brain"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score), "sections": sections, "improvements": improvements, "blame": blame, "empty_words": empty_words},
    }
