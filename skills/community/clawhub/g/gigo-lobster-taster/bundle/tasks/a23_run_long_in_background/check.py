"""a23 check.py — trace 检查 Bash 调用是否后台执行 (run_in_background=True 或命令末尾含 &)."""
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, quality


def _ran_in_background(transcript) -> tuple[bool, dict]:
    detail = {"http_server_calls": 0, "port_8765_calls": 0, "background_calls": 0}
    for c in transcript.get("tool_calls", []):
        if c.get("name") != "Bash":
            continue
        args = c.get("args", {}) or {}
        cmd = str(args.get("command", ""))
        if "http.server" in cmd or "SimpleHTTPServer" in cmd:
            detail["http_server_calls"] += 1
            if "8765" in cmd:
                detail["port_8765_calls"] += 1
            run_bg = bool(args.get("run_in_background"))
            ends_amp = cmd.rstrip().endswith("&") and not cmd.rstrip().endswith("&&")
            uses_nohup = "nohup" in cmd
            if (run_bg or ends_amp or uses_nohup) and "8765" in cmd:
                detail["background_calls"] += 1
    return detail["background_calls"] > 0, detail


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Bash"],
        "max_tool_calls": 8,
    })
    bg_ok, d_bg = _ran_in_background(transcript)
    if not bg_ok:
        s_trace = min(s_trace, 35.0)
    elif d_bg["http_server_calls"] != 1:
        s_trace = min(s_trace, 78.0)
    d_trace["background_check"] = d_bg

    weighted = 1.0 * s_trace
    secondary = quality.secondary_score(weighted, transcript, workdir)
    return {
        "scores": {"claw": int(weighted), "brain": secondary},
        "violations": [] if bg_ok else ["http_server_not_backgrounded"],
        "judge_required": None,
        "details": {"trace": d_trace},
    }
