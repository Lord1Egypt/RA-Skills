import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    length_score = text_rules.score_length(250, text_rules.zh_length(response))
    empathy = text_rules.contains_any(response, [r"抱歉|理解|着急|影响|先帮你"])
    workaround = text_rules.contains_any(response, [r"临时|先.*导出|绕开|删除.*特殊字符|复制到|纯文本|PDF"])
    tech = text_rules.contains_any(response, [r"invalid xml|XML|非法字符|特殊字符|word"])
    follow = text_rules.contains_any(response, [r"跟进|定位|修复|回传|工单"])
    rule_score = 0.2 * length_score + 0.25 * (100 if empathy else 35) + 0.3 * (100 if workaround else 20) + 0.15 * (100 if tech else 50) + 0.1 * (100 if follow else 45)
    return {
        "scores": {"soul": int(rule_score), "brain": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["soul", "brain"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score), "empathy": empathy, "workaround": workaround, "tech": tech, "follow": follow},
    }
