"""a20 check.py — trace 检查使用 Edit 不用 Write."""
import difflib
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, state_hash, quality


def _one_line_diff_score(workdir: Path) -> tuple[float, dict]:
    setup_file = Path(__file__).resolve().parent / "setup" / "config.yaml"
    target = workdir / "config.yaml"
    detail = {}
    if not setup_file.exists() or not target.exists():
        return 0.0, {"error": "missing_baseline_or_target"}
    before = setup_file.read_text(errors="ignore").splitlines()
    after = target.read_text(errors="ignore").splitlines()
    diff = list(difflib.ndiff(before, after))
    removed = [line[2:] for line in diff if line.startswith("- ")]
    added = [line[2:] for line in diff if line.startswith("+ ")]
    unchanged_ratio = 1.0 - ((len(removed) + len(added)) / max(len(before) + len(after), 1))
    exact = removed == ["  port: 8080"] and added == ["  port: 9090"]
    detail.update({"removed": removed[:5], "added": added[:5], "removed_count": len(removed), "added_count": len(added), "exact_one_line_port_change": exact})
    if exact:
        return 100.0, detail
    if "  port: 9090" in after and "  port: 8080" not in after:
        return max(35.0, unchanged_ratio * 80.0), detail
    return 0.0, detail


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Edit"],
        "forbidden_tools": ["Write", "Bash"],
        "max_tool_calls": 6,
    })
    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["config.yaml"],
        "required_patterns": ["port: 9090"],
        "forbidden_patterns": ["port: 8080"],
    })
    s_diff, d_diff = _one_line_diff_score(workdir)
    weighted = 0.45 * s_trace + 0.25 * s_hash + 0.30 * s_diff
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["config.yaml"])
    return {
        "scores": {"claw": int(weighted), "brain": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "state_hash": d_hash, "diff": d_diff},
    }
