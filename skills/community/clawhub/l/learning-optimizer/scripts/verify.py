#!/usr/bin/env python3
"""End-to-end verification for Learning Optimizer."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "main.py"


def run(args, env):
    result = subprocess.run(
        [sys.executable, str(MAIN), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def main():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["LEARNING_OPTIMIZER_HOME"] = str(Path(tmp) / "learning-data")

        print("[verify] analyze")
        out = run(["analyze", "--schedule", "每天2小时", "--subjects", "数学,英语"], env)
        assert "学习模式分析" in out

        print("[verify] optimize")
        out = run(["optimize", "--problem", "容易分心", "--current", "长时间连续学习"], env)
        assert "学习优化建议" in out

        print("[verify] allocate")
        out = run(["allocate", "--total", "120", "--priorities", "数学高,英语中"], env)
        assert "时间分配方案" in out

        print("[verify] data")
        data = json.loads(run(["data"], env))
        root = Path(data["storage_root"])
        assert root == Path(env["LEARNING_OPTIMIZER_HOME"])
        assert count_jsonl(root / "analysis_log.jsonl") == 1
        assert count_jsonl(root / "optimization_log.jsonl") == 1
        assert count_jsonl(root / "allocation_log.jsonl") == 1

    print("[verify] ok")


if __name__ == "__main__":
    main()
