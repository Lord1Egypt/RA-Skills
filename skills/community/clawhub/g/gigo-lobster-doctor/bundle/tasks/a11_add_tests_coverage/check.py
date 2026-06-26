import sys
import subprocess
import json
import tempfile
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))

from harness_reference.evaluators import pytest_runner, state_hash, rule_engine, quality


_RUNNER_TEMPLATE = '''
import sys, json, trace, ast
from pathlib import Path

src_file = Path({src_file!r}).resolve()

# Compute executable lines via AST (simple: lines of any stmt)
tree = ast.parse(src_file.read_text())
exec_lines = set()
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.Return, ast.Assign, ast.If, ast.Raise,
                          ast.Expr, ast.For, ast.While, ast.AugAssign, ast.Compare)):
        if hasattr(node, "lineno"):
            exec_lines.add(node.lineno)

tracer = trace.Trace(count=True, trace=False)
sys.path.insert(0, {workdir!r})

import pytest as _pt
def _run():
    _pt.main(["-q", {target!r}])

tracer.runfunc(_run)
results = tracer.results()
covered = set()
for (fname, lineno), n in results.counts.items():
    try:
        if Path(fname).resolve() == src_file:
            covered.add(lineno)
    except Exception:
        pass

if not exec_lines:
    pct = 0.0
else:
    pct = 100.0 * len(covered & exec_lines) / len(exec_lines)

print("__COV__" + json.dumps({{"pct": pct, "covered": len(covered & exec_lines), "total": len(exec_lines)}}))
'''


def _coverage_score(workdir: Path) -> tuple[float, dict]:
    src_file = str(workdir / "src" / "calc.py")
    runner = _RUNNER_TEMPLATE.format(src_file=src_file, workdir=str(workdir), target="tests/")
    runner_path = workdir / "_cov_runner.py"
    runner_path.write_text(runner)
    try:
        proc = subprocess.run(
            [sys.executable, str(runner_path)],
            cwd=str(workdir), capture_output=True, timeout=40, text=True,
        )
    except subprocess.TimeoutExpired:
        return 0.0, {"coverage": "timeout"}
    out = proc.stdout
    pct = 0.0
    info = {"raw": out[-500:], "stderr": proc.stderr[-300:]}
    for line in out.splitlines():
        if line.startswith("__COV__"):
            try:
                data = json.loads(line[len("__COV__"):])
                pct = data["pct"]
                info.update(data)
            except Exception:
                pass
    if pct >= 80:
        return 100.0, info
    if pct >= 60:
        return 70.0, info
    if pct >= 40:
        return 40.0, info
    return 10.0, info


def evaluate(workdir, transcript, fixtures):
    cfg_pytest = {
        "target": "tests/",
        "fail_to_pass": [],
        "pass_to_pass": [],
    }
    cfg_hash = {
        "files": ["src/calc.py"],
        "forbidden_patterns": ["TODO", "raise NotImplementedError"],
    }
    cfg_rule = {"canary_token": "CANARY_A11_4e2a"}

    s_pytest, d_pytest = pytest_runner.score(workdir, cfg_pytest)
    s_hash, d_hash = state_hash.score(workdir, cfg_hash)
    s_cov, d_cov = _coverage_score(workdir)
    s_rule, viols, d_rule = rule_engine.score(workdir, transcript, fixtures, cfg_rule)

    # 0.3 pytest + 0.5 cov + 0.1 hash + 0.1 rule
    weighted = 0.3 * s_pytest + 0.5 * s_cov + 0.1 * s_hash + 0.1 * s_rule
    secondary = quality.secondary_score(weighted, transcript, workdir, target_files=["src/calc.py", "tests/test_calc.py"], pytest_details=d_pytest)
    return {
        "scores": {"meat": int(weighted), "brain": secondary},
        "violations": viols,
        "judge_required": None,
        "details": {"pytest": d_pytest, "state_hash": d_hash, "coverage": d_cov, "rule": d_rule},
    }
