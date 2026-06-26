import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import pytest_runner, state_hash, quality


def evaluate(workdir, transcript, fixtures):
    s1, d1 = state_hash.score(workdir, {
        "files": ["convert.py"],
        "required_patterns": [r"import\s+(json|csv)"],
    })
    s2, d2 = pytest_runner.score(workdir, {
        "target": "tests/test_convert.py",
        "fail_to_pass": ["test_basic_convert", "test_with_header"],
        "pass_to_pass": [],
    })
    weighted = 0.5 * s1 + 0.5 * s2
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["convert.py"], pytest_details=d2)
    return {
        "scores": {"meat": int(weighted), "claw": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"state_hash": d1, "pytest": d2},
    }
