#!/usr/bin/env python3
"""Release verification for Ming."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_json(args):
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)


def main():
    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    clawhub = json.loads((ROOT / "clawhub.json").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    meta = json.loads((ROOT / "_meta.json").read_text(encoding="utf-8"))
    expected_version = "1.1.0"
    for label, version in {
        "SKILL.md": f"version: {expected_version}" in skill_md,
        "clawhub.json": clawhub["version"] == expected_version,
        "package.json": package["version"] == expected_version,
        "_meta.json": meta["version"] == expected_version,
    }.items():
        if not version:
            raise SystemExit(f"{label} version is not {expected_version}")

    print("[verify] bazi")
    bazi = run_json(["scripts/bazi_calculator.py", "1990", "3", "15", "15"])
    pillars = bazi["八字排盘"]["八字"]
    assert pillars == {"年柱": "庚午", "月柱": "庚辰", "日柱": "己亥", "时柱": "壬申"}
    assert bazi["八字排盘"]["日主"] == "己"
    assert bazi["八字排盘"]["五行分布"] == {"金": 3, "木": 0, "水": 2, "火": 1, "土": 2}

    print("[verify] name analyzer")
    name = run_json(["scripts/name_analyzer.py", "张", "伟"])
    assert name["五格"]["人格"]["数理"] == 22
    assert name["三才"]["三才配置"] == "木木木"

    print("[verify] zodiac")
    zodiac = run_json(["scripts/zodiac_match.py", "龙", "鸡"])
    assert zodiac["score"] == 95
    assert zodiac["配对类型"] == "六合"

    print("[verify] ok")


if __name__ == "__main__":
    main()
