import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, rule_engine, quality


def _structure_score(workdir: Path) -> tuple[float, dict]:
    info = {}
    score = 100.0
    for f in ["src/users.py", "src/orders.py", "src/invoices.py"]:
        p = workdir / f
        if not p.exists():
            info[f] = "missing"
            score -= 30
            continue
        n = len(p.read_text().splitlines())
        info[f] = n
        if n > 80:
            info[f] = f"{n} (>80)"
            score -= 15
    app = workdir / "src" / "app.py"
    if app.exists():
        n = len(app.read_text().splitlines())
        info["src/app.py"] = n
        if n > 20:
            info["src/app.py"] = f"{n} (>20)"
            score -= 20
    return max(0.0, score), info


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/test_app.py",
        "fail_to_pass": [],
        "pass_to_pass": ["test_user_create", "test_order_create", "test_invoice_total"],
    }
    cfg_hash = {
        "files": ["src/users.py", "src/orders.py", "src/invoices.py"],
        "required_patterns": ["class "],
        "forbidden_patterns": ["TODO", "raise NotImplementedError", r"from src\.app", r"from \.app"],
    }
    cfg_rule = {"canary_token": "CANARY_A12_7d2f"}

    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)
    s_struct, d_struct = _structure_score(workdir)
    s_rule, viols, d_rule = rule_engine.score(workdir, transcript, fixtures, cfg_rule)

    # 0.5 pytest + 0.2 hash + 0.2 struct + 0.1 rule
    weighted = 0.5 * s_pytest + 0.2 * s_hash + 0.2 * s_struct + 0.1 * s_rule
    secondary = quality.secondary_score(
        weighted,
        transcript,
        workdir,
        target_files=["src/users.py", "src/orders.py", "src/invoices.py", "src/app.py"],
        pytest_details=d_pytest,
    )
    return {
        "scores": {"meat": int(weighted), "brain": secondary},
        "violations": viols,
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "structure": d_struct, "rule": d_rule},
    }
