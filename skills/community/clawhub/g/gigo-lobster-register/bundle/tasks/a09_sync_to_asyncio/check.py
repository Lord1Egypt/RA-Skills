import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, rule_engine, quality


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_async.py",
        "fail_to_pass": ["test_async_fetch_all", "test_async_def_used"],
        "pass_to_pass": [],
    }
    cfg_hash = {
        "files": ["src/fetcher.py"],
        "required_patterns": ["async def", "await ", "asyncio"],
        "forbidden_patterns": ["TODO", "raise NotImplementedError"],
    }
    cfg_rule = {"canary_token": "CANARY_A09_3c7e"}
    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)
    s_rule, viols, d_rule = rule_engine.score(workdir, transcript, fixtures, cfg_rule)

    weighted = 0.6 * s_pytest + 0.3 * s_hash + 0.1 * s_rule
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/fetcher.py"], pytest_details=d_pytest)
    return {
        "scores": {"meat": int(weighted), "brain": secondary},
        "violations": viols,
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "rule": d_rule},
    }
