"""跑 workdir 下的 pytest，按 fail_to_pass / pass_to_pass 计分。"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


def run_pytest(workdir: Path, target: str, timeout: int = 25) -> dict:
    """返回 {<test_name>: 'passed'|'failed'|'error'|'skipped'}"""
    report_path = Path(tempfile.mktemp(suffix=".json"))
    try:
        subprocess.run(
            ["pytest", target, "-q",
             "--json-report", f"--json-report-file={report_path}"],
            cwd=str(workdir), capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return {}
    if not report_path.exists():
        return {}
    data = json.loads(report_path.read_text())
    out = {}
    for t in data.get("tests", []):
        name = t["nodeid"].split("::")[-1]
        out[name] = t["outcome"]
    return out


def score(workdir: Path, ev_cfg: dict) -> tuple[float, dict]:
    """返回 (0..100, details)"""
    target = ev_cfg["target"]
    ftp = ev_cfg.get("fail_to_pass", [])
    ptp = ev_cfg.get("pass_to_pass", [])
    timeout = ev_cfg.get("timeout", 25)
    results = run_pytest(workdir, target, timeout)

    if not results:
        return 0.0, {"error": "pytest_did_not_run"}

    if not ftp and not ptp:
        passed = sum(1 for outcome in results.values() if outcome == "passed")
        total = 100 * passed / max(len(results), 1)
    elif ftp and ptp:
        ftp_pass = sum(1 for n in ftp if results.get(n) == "passed")
        ptp_pass = sum(1 for n in ptp if results.get(n) == "passed")
        ftp_score = ftp_pass / len(ftp)
        ptp_score = ptp_pass / len(ptp)
        total = 100 * (0.75 * ftp_score + 0.25 * ptp_score)
    elif ftp:
        ftp_pass = sum(1 for n in ftp if results.get(n) == "passed")
        total = 100 * ftp_pass / len(ftp)
    else:
        ptp_pass = sum(1 for n in ptp if results.get(n) == "passed")
        total = 100 * ptp_pass / len(ptp)
    details = {
        "fail_to_pass": {n: results.get(n, "missing") for n in ftp},
        "pass_to_pass": {n: results.get(n, "missing") for n in ptp},
    }
    return total, details
