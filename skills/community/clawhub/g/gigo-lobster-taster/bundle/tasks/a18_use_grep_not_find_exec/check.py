import sys
import re
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import trace_parser, state_hash, quality


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Grep"],
        "forbidden_tools": ["Read"],
        "max_tool_calls": 10,
        "max_per_tool": {"Bash": 1, "Read": 0},
    })
    calls = transcript.get("tool_calls", [])
    bash_cmds = [str(c.get("args", {}).get("command", "")) for c in calls if c.get("name") == "Bash"]
    grep_tool_used = any(c.get("name") == "Grep" for c in calls)
    grep_shell_used = any(re.search(r"\bgrep\b", cmd) for cmd in bash_cmds)
    cat_or_find_used = any(re.search(r"\b(cat|find|xargs)\b", cmd) for cmd in bash_cmds)
    if not (grep_tool_used or grep_shell_used):
        s_trace = min(s_trace, 35.0)
    if cat_or_find_used:
        s_trace = min(s_trace, 45.0)
    d_trace["grep_signal"] = {"grep_tool_used": grep_tool_used, "grep_shell_used": grep_shell_used, "cat_or_find_used": cat_or_find_used}
    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["answer.txt"],
        "required_patterns": ["note_137"],
    })
    weighted = 0.7 * s_trace + 0.3 * s_hash
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["answer.txt"])
    return {
        "scores": {"claw": int(weighted), "brain": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "state_hash": d_hash},
    }
