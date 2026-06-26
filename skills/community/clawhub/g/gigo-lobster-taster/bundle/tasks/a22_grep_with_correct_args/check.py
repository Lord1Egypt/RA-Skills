"""a22 check.py — trace 检查 Grep 调用的 args.path / args.pattern."""
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, state_hash, quality


def _grep_args_ok(transcript) -> tuple[bool, dict]:
    grep_calls = [c for c in transcript.get("tool_calls", []) if c.get("name") == "Grep"]
    detail = {"grep_calls": len(grep_calls)}
    if not grep_calls:
        detail["reason"] = "no_grep_call"
        return False, detail
    for c in grep_calls:
        args = c.get("args", {}) or {}
        pat = str(args.get("pattern", ""))
        path = str(args.get("path", ""))
        if "def main" in pat and ("src" in path or path.startswith("src")):
            detail["matched_call"] = {"pattern": pat, "path": path}
            return True, detail
    detail["reason"] = "no_grep_call_with_correct_args"
    return False, detail


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Grep"],
        "max_tool_calls": 6,
    })
    ok, d_args = _grep_args_ok(transcript)
    if not ok:
        s_trace = max(0.0, s_trace - 40)
    d_trace["args_check"] = d_args

    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["answer.txt"],
        "required_patterns": ["main\\.py", "app\\.py"],
    })
    weighted = 0.7 * s_trace + 0.3 * s_hash
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["answer.txt"])
    return {
        "scores": {"claw": int(weighted), "brain": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "state_hash": d_hash},
    }
