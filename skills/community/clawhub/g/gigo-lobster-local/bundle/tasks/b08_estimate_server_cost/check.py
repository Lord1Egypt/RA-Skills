import re
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import text_rules  # noqa: E402


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    excerpt = response[:4000]
    items = text_rules.count_matches(response, [r"ECS|云主机", r"OSS|存储", r"RDS|数据库", r"向量", r"LLM|API", r"CDN", r"日志", r"带宽"])
    formulas = len(re.findall(r"[×xX*].*[=＝].*(元|万|约)", response))
    total = text_rules.contains_any(response, [r"合计|总计|总额"])
    optimizations = len([line for line in response.splitlines() if re.search(r"(优化|压缩|降本)", line)])
    rule_score = 0.35 * min(100, items / 5 * 100) + 0.25 * min(100, formulas / 5 * 100) + 0.2 * (100 if total else 20) + 0.2 * min(100, optimizations / 3 * 100)
    return {
        "scores": {"brain": int(rule_score), "meat": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {},
            "dimensions_to_judge": ["brain", "meat"],
        },
        "details": {"response_length": len(response), "rule_score": int(rule_score), "items": items, "formulas": formulas, "optimizations": optimizations},
    }
