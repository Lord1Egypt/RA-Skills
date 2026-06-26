#!/usr/bin/env python3
"""
Test script for Phase 5: Module Split - Verify structural correctness.

Tests module structure, class/method existence, and import paths
without requiring Ollama server connection.

Uses AST parsing for structure verification and importlib.util
for direct module loading (bypasses eager OllamaEngine import chain).
"""

import ast
import sys
import importlib.util
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATOR_DIR = PROJECT_ROOT / "kb" / "biblio" / "generator"
AGGREGATORS_DIR = GENERATOR_DIR / "aggregators"


def load_module_directly(name: str, filepath: Path):
    """Load a module directly from file, bypassing package __init__.py chain."""
    spec = importlib.util.spec_from_file_location(name, str(filepath))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        # If exec fails due to missing parent packages, still register it
        print(f"    (exec warning: {e})")
    return mod


def get_class_methods(filepath: Path, class_name: str) -> set:
    """Extract method names from a class using AST parsing."""
    tree = ast.parse(filepath.read_text(encoding="utf-8"))
    methods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.add(item.name)
    return methods


def test_file_structure():
    """Verify all expected files exist."""
    print("\n--- File Structure ---")
    expected_files = [
        GENERATOR_DIR / "__init__.py",
        GENERATOR_DIR / "report_generator.py",
        GENERATOR_DIR / "report_models.py",
        GENERATOR_DIR / "report_prompts.py",
        GENERATOR_DIR / "report_parallel.py",
        GENERATOR_DIR / "parallel_mixin.py",
        GENERATOR_DIR / "diff_merger.py",
        GENERATOR_DIR / "base.py",
        GENERATOR_DIR / "essence_generator.py",
        AGGREGATORS_DIR / "__init__.py",
        AGGREGATORS_DIR / "data_aggregator.py",
        AGGREGATORS_DIR / "stats_calculator.py",
    ]

    all_exist = True
    for f in expected_files:
        exists = f.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {f.relative_to(PROJECT_ROOT)}")
        if not exists:
            all_exist = False
    return all_exist


def test_ast_structure():
    """Verify all classes have expected methods via AST parsing."""
    print("\n--- AST Structure Verification ---")

    all_ok = True

    # ReportGenerator
    filepath = GENERATOR_DIR / "report_generator.py"
    methods = get_class_methods(filepath, "ReportGenerator")
    expected = {
        "generate_daily_report", "generate_weekly_report", "generate_monthly_report",
        "generate_report",
        "_collect_essences_for_period", "_collect_reports_for_period",
        "_read_essence_content", "_read_report_content", "_collect_sub_reports",
        "_compute_hotspots", "_generate_graph_data", "_save_graph_data",
        "_build_daily_prompt", "_build_weekly_prompt", "_build_monthly_prompt",
        "_build_prompt_for_type", "_generate_with_retry",
        "_extract_sections", "_build_report_title",
        "get_generation_stats", "__init__",
    }
    for m in sorted(expected):
        ok = m in methods
        print(f"  {'✅' if ok else '❌'} ReportGenerator.{m}")
        if not ok:
            all_ok = False

    # ReportDataAggregator
    filepath = AGGREGATORS_DIR / "data_aggregator.py"
    methods = get_class_methods(filepath, "ReportDataAggregator")
    expected = {
        "__init__", "collect_essences_for_period", "collect_reports_for_period",
        "read_essence_content", "read_report_content", "collect_sub_reports",
    }
    for m in sorted(expected):
        ok = m in methods
        print(f"  {'✅' if ok else '❌'} ReportDataAggregator.{m}")
        if not ok:
            all_ok = False

    # StatsCalculator
    filepath = AGGREGATORS_DIR / "stats_calculator.py"
    methods = get_class_methods(filepath, "StatsCalculator")
    expected = {
        "__init__", "compute_hotspots", "generate_graph_data",
        "save_graph_data", "get_generation_stats",
    }
    for m in sorted(expected):
        ok = m in methods
        print(f"  {'✅' if ok else '❌'} StatsCalculator.{m}")
        if not ok:
            all_ok = False

    return all_ok


def test_syntax():
    """Verify all Python files are syntactically valid."""
    print("\n--- Syntax Verification ---")
    all_ok = True

    files = [
        GENERATOR_DIR / "report_generator.py",
        GENERATOR_DIR / "__init__.py",
        AGGREGATORS_DIR / "__init__.py",
        AGGREGATORS_DIR / "data_aggregator.py",
        AGGREGATORS_DIR / "stats_calculator.py",
    ]

    for f in files:
        try:
            ast.parse(f.read_text(encoding="utf-8"))
            print(f"  ✅ {f.relative_to(PROJECT_ROOT)}")
        except SyntaxError as e:
            print(f"  ❌ {f.relative_to(PROJECT_ROOT)}: {e}")
            all_ok = False

    return all_ok


def test_isolated_imports():
    """
    Test that leaf modules can be imported in isolation.
    
    Uses importlib.util to load files directly, bypassing the
    eager import chain in generator/__init__.py (which triggers
    OllamaEngine initialization and hangs without a server).
    """
    print("\n--- Isolated Module Loading ---")
    all_ok = True

    # report_models.py has no external deps (only pathlib, typing)
    try:
        mod = load_module_directly(
            "kb.biblio.generator.report_models",
            GENERATOR_DIR / "report_models.py",
        )
        assert hasattr(mod, "ReportGeneratorError")
        assert hasattr(mod, "ReportGenerationResult")
        print("  ✅ report_models.py (direct load)")
    except Exception as e:
        print(f"  ❌ report_models.py: {e}")
        all_ok = False

    # stats_calculator.py imports from report_prompts
    # We can verify it parses correctly even if we can't exec it
    try:
        ast.parse((AGGREGATORS_DIR / "stats_calculator.py").read_text(encoding="utf-8"))
        print("  ✅ stats_calculator.py (AST valid)")
    except SyntaxError as e:
        print(f"  ❌ stats_calculator.py: {e}")
        all_ok = False

    try:
        ast.parse((AGGREGATORS_DIR / "data_aggregator.py").read_text(encoding="utf-8"))
        print("  ✅ data_aggregator.py (AST valid)")
    except SyntaxError as e:
        print(f"  ❌ data_aggregator.py: {e}")
        all_ok = False

    return all_ok


def test_delegation_integrity():
    """Verify delegation signatures match between ReportGenerator and target classes."""
    print("\n--- Delegation Signature Integrity ---")
    all_ok = True

    def get_method_params(filepath, class_name, method_name):
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                        return [a.arg for a in item.args.args]
        return None

    comparisons = [
        # (gen_file, gen_class, gen_method, target_file, target_class, target_method)
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_collect_essences_for_period",
         AGGREGATORS_DIR / "data_aggregator.py", "ReportDataAggregator", "collect_essences_for_period"),
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_collect_reports_for_period",
         AGGREGATORS_DIR / "data_aggregator.py", "ReportDataAggregator", "collect_reports_for_period"),
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_read_essence_content",
         AGGREGATORS_DIR / "data_aggregator.py", "ReportDataAggregator", "read_essence_content"),
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_read_report_content",
         AGGREGATORS_DIR / "data_aggregator.py", "ReportDataAggregator", "read_report_content"),
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_collect_sub_reports",
         AGGREGATORS_DIR / "data_aggregator.py", "ReportDataAggregator", "collect_sub_reports"),
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_compute_hotspots",
         AGGREGATORS_DIR / "stats_calculator.py", "StatsCalculator", "compute_hotspots"),
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_generate_graph_data",
         AGGREGATORS_DIR / "stats_calculator.py", "StatsCalculator", "generate_graph_data"),
        (GENERATOR_DIR / "report_generator.py", "ReportGenerator", "_save_graph_data",
         AGGREGATORS_DIR / "stats_calculator.py", "StatsCalculator", "save_graph_data"),
    ]

    for gf, gc, gm, tf, tc, tm in comparisons:
        g_params = get_method_params(gf, gc, gm)
        t_params = get_method_params(tf, tc, tm)
        # Delegation has 'self' + same params as target has 'self' + same params
        match = g_params is not None and t_params is not None and g_params == t_params
        print(f"  {'✅' if match else '❌'} {gc}.{gm} → {tc}.{tm}")
        if not match:
            print(f"    Generator: {g_params}")
            print(f"    Target:    {t_params}")
            all_ok = False

    return all_ok


def test_line_counts():
    """Report line counts to verify the split achieved its goal."""
    print("\n--- Line Counts ---")
    files = {
        "report_generator.py": GENERATOR_DIR / "report_generator.py",
        "data_aggregator.py (NEW)": AGGREGATORS_DIR / "data_aggregator.py",
        "stats_calculator.py (NEW)": AGGREGATORS_DIR / "stats_calculator.py",
        "report_models.py": GENERATOR_DIR / "report_models.py",
        "report_prompts.py": GENERATOR_DIR / "report_prompts.py",
        "report_parallel.py": GENERATOR_DIR / "report_parallel.py",
        "parallel_mixin.py": GENERATOR_DIR / "parallel_mixin.py",
    }

    for name, path in sorted(files.items()):
        if path.exists():
            lines = len(path.read_text(encoding="utf-8").splitlines())
            print(f"  {name}: {lines} lines")

    return True


def main():
    print("=" * 60)
    print("Phase 5 Module Split - Structural Verification")
    print("=" * 60)

    results = {
        "File Structure": test_file_structure(),
        "Syntax Validation": test_syntax(),
        "AST Structure": test_ast_structure(),
        "Isolated Imports": test_isolated_imports(),
        "Delegation Integrity": test_delegation_integrity(),
        "Line Counts": test_line_counts(),
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")

    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n  Result: {passed_count}/{total_count} tests passed")

    return 0 if passed_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())