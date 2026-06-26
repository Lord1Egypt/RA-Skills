import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    both = text_rules.count_matches(response, [r"令牌桶|Token Bucket", r"漏桶|Leaky Bucket"])
    dims = text_rules.count_matches(response, [r"突发|burst", r"平均速率|匀速", r"削峰", r"复杂度", r"分布式"])
    scenes = text_rules.count_matches(response, [r"场景 A.*令牌桶|免费用户.*令牌桶", r"场景 B.*漏桶|后台批量.*漏桶"])
    pit = text_rules.contains_any(response, [r"时钟漂移|一致性|冷启动|Redis|Lua"])
    rule_score = 0.25 * min(100, both / 2 * 100) + 0.3 * min(100, dims / 4 * 100) + 0.3 * min(100, scenes / 2 * 100) + 0.15 * (100 if pit else 45)
    return {
        "scores": {"brain": int(rule_score), "meat": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["brain", "meat"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score)},
    }
