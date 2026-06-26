import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import pytest_runner, state_hash, quality


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_todo.py",
        "fail_to_pass": [
            "test_add",
            "test_list",
            "test_done",
            "test_delete",
            "test_persist_across_runs",
        ],
        "pass_to_pass": [],
    }
    cfg_hash = {
        "files": ["todo.py"],
        "forbidden_patterns": ["raise NotImplementedError"],
    }
    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)

    weighted = 0.9 * s_pytest + 0.1 * s_hash
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["todo.py"], pytest_details=d_pytest)
    return {
        "scores": {
            "meat": int(weighted),
            "brain": secondary,
            "claw": max(0, secondary - 10),
        },
        "violations": [],
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash},
    }
