import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    chars = text_rules.zh_length(response)
    length_score = 100 if 180 <= chars <= 260 else max(0, 100 - min(abs(chars - 220), 140) * 0.8)
    stats = text_rules.count_matches(response, [r"p\s*=\s*0\.08", r"不显著|未显著", r"加载.*变慢|客服.*增加"])
    decision = text_rules.contains_any(response, [r"继续观察|不上线|继续实验|不建议全量|建议继续"])
    next_step = text_rules.contains_any(response, [r"下一步|建议|补样本|延长实验|分层"])
    return {
        "scores": {"brain": int(0.3 * length_score + 0.4 * min(100, stats / 3 * 100) + 0.15 * (100 if decision else 30) + 0.15 * (100 if next_step else 40))},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": response[:4000],
            "context": {},
            "dimensions_to_judge": ["brain", "soul"],
        },
        "details": {"response_length": len(response), "chars": chars},
    }
