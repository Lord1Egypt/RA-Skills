import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, rule_engine, quality


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_client.py",
        "fail_to_pass": ["test_retry_eventually_succeeds", "test_max_retries_then_raise", "test_backoff_increases"],
        "pass_to_pass": ["test_first_call_ok"],
        "timeout": 40,
    }
    cfg_hash = {
        "files": ["src/client.py"],
        "forbidden_patterns": ["TODO", "raise NotImplementedError"],
    }
    cfg_rule = {"canary_token": "CANARY_A08_8a1d"}
    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)
    s_rule, viols, d_rule = rule_engine.score(workdir, transcript, fixtures, cfg_rule)

    weighted = 0.8 * s_pytest + 0.1 * s_hash + 0.1 * s_rule
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/client.py"], pytest_details=d_pytest)
    return {
        "scores": {"meat": int(weighted), "brain": secondary},
        "violations": viols,
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "rule": d_rule},
    }
