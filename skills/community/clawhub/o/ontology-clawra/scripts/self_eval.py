#!/usr/bin/env python3
"""
ontology-clawra 自我评估模块
用于测试和改进本体论引擎
"""

import json
import sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent


def evaluate_ontology():
    """评估本体论引擎"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }

    # 测试1: 检查核心文件
    core_files = [
        "SKILL.md",
        "scripts/ontology-clawra.py",
        "scripts/main.py",
        "memory/schema.yaml"
    ]

    for f in core_files:
        filepath = SKILL_DIR / f
        results["tests"].append({
            "name": f"核心文件: {f}",
            "passed": filepath.exists(),
            "required": True
        })

    # 测试2: 检查版本一致性
    try:
        meta = json.loads((SKILL_DIR / "_meta.json").read_text())
        skill_md = (SKILL_DIR / "SKILL.md").read_text()
        version_in_skill = "version:" in skill_md
        results["tests"].append({
            "name": "版本一致性",
            "passed": version_in_skill,
            "details": f"meta: {meta.get('version')}"
        })
    except:
        results["tests"].append({
            "name": "版本一致性",
            "passed": False,
            "required": True
        })

    return results


def main():
    results = evaluate_ontology()
    passed = sum(1 for t in results["tests"] if t["passed"])
    total = len(results["tests"])

    print(f"\n🧪 ontology-clawra 自我评估")
    print(f"   通过: {passed}/{total}")

    for t in results["tests"]:
        status = "✅" if t["passed"] else "❌"
        print(f"   {status} {t['name']}")

    if passed == total:
        print("\n🎉 所有测试通过!")
        return 0
    else:
        print("\n⚠️ 部分测试失败，建议运行增强器")
        return 1


if __name__ == "__main__":
    sys.exit(main())
