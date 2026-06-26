"""a17 check.py — trace 检测失败后的重规划 + pytest 验证 marker 写入。

依赖 harness 注入第 1 次 Bash 失败；若 transcript 中没有任何 tool_result=='error' 或
带 "failed"/"exit_code>0" 的调用，则认为 failure injection 未启用，此时 trace 评估
给中性 65 分以避免卡死；pytest 仍然跑，验证最终状态。
"""
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, pytest_runner, quality


def _detect_injection(transcript) -> bool:
    for c in transcript.get("tool_calls", []):
        r = c.get("result")
        if isinstance(r, dict):
            if r.get("exit_code", 0) not in (0, None):
                return True
            if r.get("error") or r.get("failed"):
                return True
        elif isinstance(r, str):
            low = r.lower()
            if "error" in low or "failed" in low or "non-zero" in low:
                return True
    return False


def _replan_score(transcript) -> float:
    """如果失败后继续出现新的 tool 调用且最终成功达成目标，说明有重规划。"""
    calls = transcript.get("tool_calls", [])
    # 简化启发：失败注入生效 + 调用总数 >=2 + 最后一次不是失败
    if not calls:
        return 0.0
    last = calls[-1]
    r = last.get("result")
    last_ok = True
    if isinstance(r, dict):
        last_ok = r.get("exit_code", 0) == 0 and not r.get("error")
    return 100.0 if (len(calls) >= 2 and last_ok) else 40.0


def evaluate(workdir, transcript, fixtures):
    injected = _detect_injection(transcript)
    if injected:
        s_trace_base, d_trace = trace_parser.score(transcript, {
            "required_tools_set": ["Bash"],
            "max_tool_calls": 15,
        })
        s_replan = _replan_score(transcript)
        s_trace = 0.5 * s_trace_base + 0.5 * s_replan
        d_trace["injection_detected"] = True
        d_trace["replan_score"] = s_replan
    else:
        # 未启用失败注入 → 中性分
        s_trace = 65.0
        d_trace = {"injection_detected": False, "note": "failure_injection_not_enabled_neutral_score"}

    s_pytest, d_pytest = pytest_runner.score(workdir, {
        "target": "tests/test_marker.py",
        "fail_to_pass": ["test_marker_written"],
        "pass_to_pass": [],
    })

    weighted = 0.6 * s_trace + 0.4 * s_pytest
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["marker.txt"], pytest_details=d_pytest)
    return {
        "scores": {"brain": int(weighted), "claw": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "pytest": d_pytest},
    }
