#!/usr/bin/env python3
"""Run a tiny failing-to-passing Proof Loop demo."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "examples" / "demo-repo" / "check_nav_labels.py"
GOOD = ROOT / "examples" / "demo-repo" / "nav_labels.json"


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.strip())
    print(f"exit={result.returncode}")
    return result


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        fixture = work / "nav_labels.json"
        shutil.copy(GOOD, fixture)
        data = json.loads(fixture.read_text(encoding="utf-8"))
        data["de"]["billing"] = "Billing"
        fixture.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        print("# Proof Loop demo: fail -> fix -> pass")
        first = run(["python3", str(CHECKER), str(fixture)], cwd=ROOT)
        if first.returncode == 0:
            print("expected initial failure")
            return 1

        print("# applying fix")
        fixture.write_text(GOOD.read_text(encoding="utf-8"), encoding="utf-8")
        second = run(["python3", str(CHECKER), str(fixture)], cwd=ROOT)
        if second.returncode != 0:
            return second.returncode

        report = run([str(ROOT / "bin" / "proof-loop"), "report", "examples/demo-repo/.agent/tasks/nav-labels-proof"], cwd=ROOT)
        return report.returncode


if __name__ == "__main__":
    raise SystemExit(main())
