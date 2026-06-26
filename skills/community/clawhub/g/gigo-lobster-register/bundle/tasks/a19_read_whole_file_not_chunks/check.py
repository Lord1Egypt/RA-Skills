"""a19 check.py — trace 检查 Read 次数 ≤2 且不分块."""
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, state_hash, quality


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Read"],
        "max_tool_calls": 6,
        "max_per_tool": {"Read": 2},
    })
    # 额外：分块惩罚 —— 同一文件的 Read 调用中带 offset 或 limit 的次数
    chunk_reads = 0
    for c in transcript.get("tool_calls", []):
        if c.get("name") == "Read":
            args = c.get("args", {}) or {}
            if args.get("offset") or args.get("limit"):
                chunk_reads += 1
    if chunk_reads > 0:
        penalty = min(40, 20 * chunk_reads)
        s_trace = max(0.0, s_trace - penalty)
        d_trace["chunk_read_penalty"] = penalty

    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["summary.txt"],
        "required_patterns": ["README"],
    })
    weighted = 0.7 * s_trace + 0.3 * s_hash
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["summary.txt"])
    return {
        "scores": {"claw": int(weighted), "brain": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "state_hash": d_hash},
    }
