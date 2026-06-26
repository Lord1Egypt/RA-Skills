import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, quality


def evaluate(workdir, transcript, fixtures):
    s_pytest, d_pytest = pytest_runner.score(workdir, {
        "target": "tests/test_app.py",
        "fail_to_pass": ["test_perf_optimized", "test_logging_added"],
        "pass_to_pass": [],
    })
    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["PRIORITY.md"],
        "required_patterns": ["性能优化", "日志"],
    })

    # 准备 llm_judge payload
    priority_md = ""
    p = workdir / "PRIORITY.md"
    if p.exists():
        priority_md = p.read_text(errors="ignore")
    implemented = {
        "perf_optimized": d_pytest.get("fail_to_pass", {}).get("test_perf_optimized") == "passed",
        "logging_added": d_pytest.get("fail_to_pass", {}).get("test_logging_added") == "passed",
    }
    judge_required = {
        "rubric_file": "judge_rubric.md",
        "agent_output_excerpt": priority_md[:4000],
        "context": {
            "implemented": implemented,
        },
        "dimensions_to_judge": ["brain", "claw"],
    }

    priority_text = priority_md.lower()
    mentions_perf = ("性能" in priority_md) or ("performance" in priority_text)
    mentions_log = ("日志" in priority_md) or ("log" in priority_text)
    mentions_tradeoff = any(token in priority_md for token in ["优先", "取舍", "原因", "冲突", "风险"])
    priority_score = (int(mentions_perf) + int(mentions_log) + int(mentions_tradeoff)) / 3 * 100.0

    weighted = 0.55 * s_pytest + 0.25 * s_hash + 0.20 * priority_score
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/app.py", "PRIORITY.md"], pytest_details=d_pytest)
    claw_local = int(0.60 * priority_score + 0.40 * secondary)
    return {
        "scores": {
            "brain": int(weighted),
            "meat": secondary,
            "claw": claw_local,
        },
        "violations": [],
        "judge_required": judge_required,
        "details": {
            "pytest": d_pytest,
            "state_hash": d_hash,
            "priority_score": int(priority_score),
            "priority_signals": {
                "mentions_perf": mentions_perf,
                "mentions_log": mentions_log,
                "mentions_tradeoff": mentions_tradeoff,
            },
        },
    }
