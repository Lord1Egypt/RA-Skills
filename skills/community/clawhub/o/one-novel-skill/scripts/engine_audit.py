#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""engine_audit.py — 引擎调用审计工具
Phase 0.2: 识别所有未调用/死代码/重复引擎，生成清理清单。
用法: python scripts/engine_audit.py
"""

import os
import sys
import ast
from pathlib import Path
from collections import defaultdict

SKILL_DIR = Path(__file__).parent.parent
ENGINE_DIR = SKILL_DIR / "engine"

# 在 pipeline.py 中被显式 import 的引擎（已在管线中）
PIPELINE_IMPORTS = {
    "engines_algorithm", "engines_dialogue", "engines_literature",
    "engines_nlp", "engines_reasoning", "engines_screenplay",
    "engines_writing", "engines_analysis", "engines_architecture",
    "engines_development", "engines_inspiration", "simulation",
    "engines_utils",
}

# 在 pipeline.py 中通过动态 import 调用的引擎
PIPELINE_DYNAMIC = {
    "engines_psychology", "engines_logic", "engines_tension",
    "multi_line_engine", "foreshadow_engine", "character_state_engine",
    "global_memory_engine", "world_engine", "stability_checker",
    "engines_timeline", "reflection_engine", "fractal_engine",
}

# 核心基础设施（不是引擎，是基础设施）
CORE_INFRA = {
    "novel_state", "generator", "config", "contracts", "exceptions",
    "log", "pipeline", "orchestrator", "scheduler", "registry",
    "engine_base", "circuit_breaker", "chapter_transaction",
    "checkpoint_manager", "persistence", "arc_manager",
    "context_builder", "health_check", "detector_wrapper",
}

# DDD 层（不参与引擎统计）
DDD_LAYER = {
    "compat",
}


def find_python_files(directory: Path) -> list:
    """列出目录下所有 .py 文件"""
    return sorted([
        f for f in directory.glob("*.py")
        if f.name != "__init__.py" and not f.name.startswith("_")
    ])


def analyze_engine(filepath: Path) -> dict:
    """分析单个引擎文件的结构"""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except SyntaxError:
        return {"classes": [], "functions": [], "has_main_methods": False}

    classes = []
    functions = []
    has_analyze = False
    has_check = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [
                n.name for n in ast.walk(node)
                if isinstance(n, ast.FunctionDef)
            ]
            classes.append({"name": node.name, "methods": methods})
            if "analyze" in methods:
                has_analyze = True
            if "check" in methods:
                has_check = True
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    return {
        "classes": classes,
        "functions": functions,
        "has_analyze": has_analyze,
        "has_check": has_check,
    }


def search_references(module_name: str) -> set:
    """在项目代码中搜索对某个模块的引用"""
    import re
    refs = set()
    module_stem = module_name.replace(".py", "")

    for py_file in SKILL_DIR.rglob("*.py"):
        if py_file.name.startswith("_"):
            continue
        try:
            content = py_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        patterns = [
            f"from .{module_stem} import",
            f"from engine.{module_stem} import",
            f"import engine.{module_stem}",
            f"from .{module_stem}.",
            f"'{module_stem}'",
            f'"{module_stem}"',
        ]
        for pat in patterns:
            if pat in content:
                refs.add(str(py_file.relative_to(SKILL_DIR)))
                break

    return refs


def main():
    print("=" * 70)
    print("  one-novel-skill 引擎调用审计报告")
    print("=" * 70)

    engine_files = find_python_files(ENGINE_DIR)
    print(f"\n总引擎文件数: {len(engine_files)}")

    # 分类统计
    pipeline_engines = set()
    dynamic_engines = set()
    infra_engines = set()
    uncalled_engines = set()
    ddd_engines = set()
    unknown_engines = set()

    for ef in engine_files:
        stem = ef.stem
        if stem in CORE_INFRA:
            infra_engines.add(stem)
        elif stem in DDD_LAYER:
            ddd_engines.add(stem)
        elif stem in PIPELINE_IMPORTS:
            pipeline_engines.add(stem)
        elif stem in PIPELINE_DYNAMIC:
            dynamic_engines.add(stem)
        else:
            # 检查是否在其他地方被引用
            refs = search_references(stem)
            if refs:
                dynamic_engines.add(stem)
                print(f"  [外部引用] {stem} → {', '.join(sorted(refs)[:3])}")
            else:
                uncalled_engines.add(stem)

    print(f"\n📊 分类统计:")
    print(f"  ├─ 核心基础设施: {len(infra_engines)}")
    print(f"  ├─ Pipeline 显式导入: {len(pipeline_engines)}")
    print(f"  ├─ Pipeline 动态调用: {len(dynamic_engines)}")
    print(f"  ├─ DDD 兼容层: {len(ddd_engines)}")
    print(f"  └─ 🔴 未调用/死代码: {len(uncalled_engines)}")

    if uncalled_engines:
        print(f"\n🔴 未调用引擎清单 ({len(uncalled_engines)} 个):")
        print("  (以下引擎在任何代码路径中均未被引用)")
        for name in sorted(uncalled_engines):
            fpath = ENGINE_DIR / f"{name}.py"
            analysis = analyze_engine(fpath)
            cls_info = ", ".join(
                f"{c['name']}({','.join(c['methods'][:3])})"
                for c in analysis["classes"][:2]
            ) if analysis["classes"] else "无类定义"
            print(f"  - {name}.py  |  {cls_info}")

    print(f"\n✅ Pipeline 显式导入 ({len(pipeline_engines)} 个):")
    for name in sorted(pipeline_engines):
        print(f"  - {name}.py")

    print(f"\n🟡 Pipeline 动态调用 ({len(dynamic_engines)} 个):")
    for name in sorted(dynamic_engines):
        print(f"  - {name}.py")

    # Registry 注册状态
    print(f"\n📋 Registry 注册状态:")
    try:
        from engine.registry import summary
        s = summary()
        print(f"  总数: {s['total']} | 活跃: {s['active']} | 已调用: {s['called']} | 未调用: {s['uncalled']}")
        print(f"  ready: {s['ready']} | skeleton: {s['skeleton']} | dead: {s['dead']}")
    except Exception as e:
        print(f"  Registry 加载失败: {e}")

    # 建议
    print(f"\n💡 清理建议:")
    if uncalled_engines:
        print(f"  1. 确认以下 {len(uncalled_engines)} 个引擎是否需要保留:")
        for name in sorted(uncalled_engines):
            print(f"     - {name}.py")
        print(f"  2. 如不需要，在 registry.py 中标记 state='dead'")
        print(f"  3. 或在下一版本中直接删除文件")

    print(f"\n审计完成。")

    # 写入审计报告文件
    report = {
        "total": len(engine_files),
        "infrastructure": len(infra_engines),
        "pipeline_explicit": len(pipeline_engines),
        "pipeline_dynamic": len(dynamic_engines),
        "ddd_layer": len(ddd_engines),
        "uncalled": len(uncalled_engines),
        "uncalled_list": sorted(uncalled_engines),
    }
    report_path = SKILL_DIR / "_checkpoints" / "engine_audit.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    import json
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告已保存: {report_path}")


if __name__ == "__main__":
    main()
