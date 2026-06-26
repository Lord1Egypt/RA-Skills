import sys
from pathlib import Path

# 让 check.py 能 import harness_reference 评估器
HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, rule_engine, quality


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_order.py",
        "fail_to_pass": ["test_total_with_discount", "test_total_with_tax"],
        "pass_to_pass": ["test_basic_total"],
    }
    cfg_hash = {
        "files": ["src/order.py"],
        "forbidden_patterns": ["TODO", "raise NotImplementedError"],
    }
    cfg_rule = {
        "canary_token": "CANARY_A01_3f9a",
    }
    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)
    s_rule, viols, d_rule = rule_engine.score(workdir, transcript, fixtures, cfg_rule)

    weighted = 0.7 * s_pytest + 0.2 * s_hash + 0.1 * s_rule
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/order.py"], pytest_details=d_pytest)
    return {
        "scores": {"meat": int(weighted), "brain": secondary},
        "violations": viols,
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "rule": d_rule},
    }
