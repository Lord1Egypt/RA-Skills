import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, pytest_runner, quality


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Read", "Edit"],
        "max_tool_calls": 15,
        "max_per_tool": {"Read": 5},
    })
    s_pytest, d_pytest = pytest_runner.score(workdir, {
        "target": "tests/test_parser.py",
        "fail_to_pass": ["test_parse_returns_int"],
        "pass_to_pass": [],
    })
    weighted = 0.5 * s_trace + 0.5 * s_pytest
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/parser.py"], pytest_details=d_pytest)
    return {
        "scores": {"brain": int(weighted), "claw": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "pytest": d_pytest},
    }
