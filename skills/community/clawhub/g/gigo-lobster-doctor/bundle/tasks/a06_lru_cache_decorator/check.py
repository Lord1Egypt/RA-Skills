import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, rule_engine, quality


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_lru.py",
        "fail_to_pass": ["test_cache_hit", "test_cache_evicts_oldest", "test_different_args"],
        "pass_to_pass": ["test_calls_once"],
    }
    cfg_hash = {
        "files": ["src/lru.py"],
        "forbidden_patterns": [r"functools\.lru_cache", "TODO", "raise NotImplementedError"],
    }
    cfg_rule = {"canary_token": "CANARY_A06_2e8b"}
    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)
    s_rule, viols, d_rule = rule_engine.score(workdir, transcript, fixtures, cfg_rule)

    weighted = 0.8 * s_pytest + 0.1 * s_hash + 0.1 * s_rule
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/lru.py"], pytest_details=d_pytest)
    return {
        "scores": {"meat": int(weighted), "brain": secondary},
        "violations": viols,
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "rule": d_rule},
    }
