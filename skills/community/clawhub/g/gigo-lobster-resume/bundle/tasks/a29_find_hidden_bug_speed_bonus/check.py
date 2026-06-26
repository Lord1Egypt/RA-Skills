import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import pytest_runner, quality


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_pricing.py",
        "fail_to_pass": ["test_bulk_discount_threshold", "test_bulk_discount_edge"],
        "pass_to_pass": ["test_basic_price", "test_member_discount", "test_no_discount"],
    }
    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)

    # Speed bonus
    elapsed_ms = transcript.get("elapsed_ms", 999_999)
    bonus = 0
    if elapsed_ms < 60_000:
        bonus = 10
    elif elapsed_ms < 120_000:
        bonus = 5
    final = min(100, s_pytest + bonus)
    secondary = quality.secondary_score(final, transcript, workdir, target_files=["src/utils.py"], pytest_details=d_pytest)

    return {
        "scores": {
            "meat": int(final),
            "brain": secondary,
            "claw": max(0, secondary - 8),
        },
        "violations": [],
        "judge_required": None,
        "details": {
            "pytest": d_pytest,
            "elapsed_ms": elapsed_ms,
            "speed_bonus": bonus,
            "raw_pytest_score": s_pytest,
        },
    }
