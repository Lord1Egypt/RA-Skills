"""a21 check.py — trace 检查 parallel_group 非空."""
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, state_hash, quality


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Read"],
        "max_tool_calls": 12,
        "parallel_required": True,
    })
    # 额外：并行批次中 Read 的数量是否 ≥ 5
    groups = {}
    for c in transcript.get("tool_calls", []):
        g = c.get("parallel_group")
        if g and c.get("name") == "Read":
            groups.setdefault(g, 0)
            groups[g] += 1
    max_in_group = max(groups.values()) if groups else 0
    d_trace["max_parallel_reads"] = max_in_group
    if max_in_group < 5:
        s_trace = min(s_trace, 40.0 if max_in_group == 0 else 58.0)
        d_trace["parallel_under_5"] = True

    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["report.md"],
        "required_patterns": ["file_a", "file_b", "file_c", "file_d", "file_e"],
    })
    weighted = 0.7 * s_trace + 0.3 * s_hash
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["report.md"])
    return {
        "scores": {"claw": int(weighted), "brain": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "state_hash": d_hash},
    }
