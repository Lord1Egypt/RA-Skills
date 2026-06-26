import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, quality


def count_diff_lines(workdir: Path, target: str, baseline: str) -> int:
    """统计 target vs baseline 改动的行数（增加+删除）。"""
    p_t = workdir / target
    p_b = workdir / baseline
    if not p_t.exists() or not p_b.exists():
        return 0
    import difflib
    a = p_b.read_text(errors="ignore").splitlines()
    b = p_t.read_text(errors="ignore").splitlines()
    diff = list(difflib.unified_diff(a, b, n=0))
    changed = 0
    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            changed += 1
        elif line.startswith("-") and not line.startswith("---"):
            changed += 1
    return changed


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_calc.py",
        "fail_to_pass": [
            "test_add_positive",
            "test_add_negative",
            "test_add_zero",
            "test_add_floats",
            "test_add_large",
        ],
        "pass_to_pass": [],
    }
    cfg_hash = {
        "files": ["src/calc.py"],
        "forbidden_patterns": ["TODO", "raise NotImplementedError"],
    }
    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)

    changed = count_diff_lines(workdir, "src/calc.py", "src/calc.py.baseline")
    line_penalty = 0
    if changed > 3:
        line_penalty = 50
    d_lines = {"changed_lines": changed, "max_allowed": 3, "penalty": line_penalty}

    weighted = 0.6 * s_pytest + 0.4 * s_hash - line_penalty
    weighted = max(0.0, min(100.0, weighted))
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/calc.py"], pytest_details=d_pytest)
    return {
        "scores": {"brain": int(weighted), "meat": secondary},
        "violations": [f"too_many_changed_lines:{changed}"] if line_penalty else [],
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "line_diff": d_lines},
    }
