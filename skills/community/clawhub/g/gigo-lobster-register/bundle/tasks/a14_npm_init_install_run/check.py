"""a14 check.py — 评估 npm init/install/run 全流程。"""
import json
import re
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import trace_parser, state_hash, quality


def _command_signals(transcript):
    calls = transcript.get("tool_calls", [])
    bash_cmds = [str(c.get("args", {}).get("command", "")) for c in calls if c.get("name") == "Bash"]
    bash_cmds += [str(event.get("cmd", "")) for event in transcript.get("shell_violations", [])]

    npm_init_seen = False
    npm_install_seen = False
    node_seen = False
    output_ok = "hello, world" in str(transcript.get("stdout", "")).lower()
    for c in calls:
        if "hello, world" in str(c.get("result", "")).lower():
            output_ok = True

    for cmd in bash_cmds:
        normalized = re.sub(r"\s+", " ", cmd.strip())
        if re.search(r"\bnpm\s+init\b.*\s-y\b|\bnpm\s+init\s+-y\b", normalized):
            npm_init_seen = True
        if re.search(r"\bnpm\s+(install|i)\b.*\bchalk\b", normalized) and npm_init_seen:
            npm_install_seen = True
        if re.search(r"\bnode\s+index\.js\b|\bnode\s+\.?/index\.js\b", normalized) and npm_install_seen:
            node_seen = True
    score = (int(npm_init_seen) + int(npm_install_seen) + int(node_seen) + int(output_ok)) / 4 * 100.0
    return score, {
        "npm_init": npm_init_seen,
        "npm_install_chalk_after_init": npm_install_seen,
        "node_index_after_install": node_seen,
        "hello_world_output": output_ok,
    }


def _project_state_score(workdir: Path):
    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["package.json", "index.js"],
        "required_patterns": ["chalk"],
    })
    package_json = workdir / "package.json"
    index_js = workdir / "index.js"
    node_modules_chalk = workdir / "node_modules" / "chalk"
    package_ok = False
    if package_json.exists():
        try:
            package = json.loads(package_json.read_text(errors="ignore"))
            deps = package.get("dependencies", {})
            dev_deps = package.get("devDependencies", {})
            package_ok = "chalk" in deps or "chalk" in dev_deps
        except json.JSONDecodeError:
            package_ok = False
    index_ok = index_js.exists() and "chalk" in index_js.read_text(errors="ignore") and "Hello, world!" in index_js.read_text(errors="ignore")
    install_ok = node_modules_chalk.exists()
    structure_score = (int(package_ok) + int(index_ok) + int(install_ok)) / 3 * 100.0
    d_hash.update({"package_dep_chalk": package_ok, "index_uses_chalk": index_ok, "node_modules_chalk": install_ok})
    return 0.55 * s_hash + 0.45 * structure_score, d_hash


def evaluate(workdir, transcript, fixtures):
    s_trace, d_trace = trace_parser.score(transcript, {
        "required_tools_set": ["Bash"],
        "max_tool_calls": 20,
    })
    seq_score, d_seq = _command_signals(transcript)
    s_state, d_hash = _project_state_score(workdir)

    weighted = 0.35 * s_trace + 0.30 * seq_score + 0.35 * s_state
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["package.json", "index.js"])
    return {
        "scores": {"brain": int(weighted), "claw": secondary},
        "violations": [],
        "judge_required": None,
        "details": {"trace": d_trace, "npm_sequence": d_seq, "state_hash": d_hash},
    }
