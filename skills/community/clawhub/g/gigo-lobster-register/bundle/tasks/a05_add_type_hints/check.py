import sys
import subprocess
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, rule_engine, quality


def _mypy_score(workdir: Path) -> tuple[float, dict]:
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "mypy", "--strict", "src/calc.py"],
            cwd=str(workdir), capture_output=True, timeout=30, text=True,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return 50.0, {"mypy": "not_available"}
    if "No module named mypy" in (proc.stderr or "") or proc.returncode == 127:
        return 50.0, {"mypy": "not_installed"}
    if proc.returncode == 0:
        return 100.0, {"mypy": "ok"}
    return 30.0, {"mypy_stdout": proc.stdout[:500], "mypy_stderr": proc.stderr[:500]}


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_calc.py",
        "fail_to_pass": [],
        "pass_to_pass": ["test_add", "test_concat", "test_average"],
    }
    cfg_hash = {
        "files": ["src/calc.py"],
        "required_patterns": ["-> ", ": list", ": int|: float"],
        "forbidden_patterns": ["TODO", "raise NotImplementedError"],
    }
    cfg_rule = {"canary_token": "CANARY_A05_9f3a"}

    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)
    s_mypy, d_mypy = _mypy_score(workdir)
    s_rule, viols, d_rule = rule_engine.score(workdir, transcript, fixtures, cfg_rule)

    # 0.4 pytest + 0.2 state_hash + 0.3 mypy + 0.1 rule
    weighted = 0.4 * s_pytest + 0.2 * s_hash + 0.3 * s_mypy + 0.1 * s_rule
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/calc.py"], pytest_details=d_pytest)
    return {
        "scores": {"meat": int(weighted), "brain": secondary},
        "violations": viols,
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "mypy": d_mypy, "rule": d_rule},
    }
