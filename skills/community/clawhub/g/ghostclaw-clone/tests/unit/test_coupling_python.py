"""Tests for Python import coupling analysis."""

import sys
from pathlib import Path

# Add repo root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from ghostclaw.core.coupling import PythonImportAnalyzer


def create_python_repo(tmp_path: Path, structure: dict):
    """Helper to create a Python repo from a dict of {relpath: content}."""
    for relpath, content in structure.items():
        p = tmp_path / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)


def test_no_imports(tmp_path):
    create_python_repo(tmp_path, {
        "module.py": "def foo():\n    return 1\n"
    })
    analyzer = PythonImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    assert report["circular_dependencies"] == []
    assert len(report["issues"]) == 0
    # Should have one module with 0 afferent/efferent
    assert len(report["coupling_metrics"]) == 1


def test_simple_chain(tmp_path):
    create_python_repo(tmp_path, {
        "a.py": "from b import get\n",
        "b.py": "from c import value\n",
        "c.py": "CONST = 1\n"
    })
    analyzer = PythonImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    # No cycles
    assert len(report["circular_dependencies"]) == 0
    metrics = report["coupling_metrics"]
    # a imports b -> a efferent=1, b afferent=1
    assert metrics["a"]["efferent"] == 1
    assert metrics["b"]["afferent"] == 1
    assert metrics["b"]["efferent"] == 1
    assert metrics["c"]["afferent"] == 1


def test_circular_dependency(tmp_path):
    create_python_repo(tmp_path, {
        "a.py": "from b import x\n",
        "b.py": "from a import y\n"
    })
    analyzer = PythonImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    assert len(report["circular_dependencies"]) >= 1
    # Check that a cycle appears in issues/ghosts
    issues = " ".join(report["issues"])
    assert "Circular dependency" in issues

def test_entry_point_not_flagged_as_unstable(tmp_path):
    # Create a repo where a 'cli' module imports many others
    create_python_repo(tmp_path, {
        "cli.py": "import a; import b; import c; import d; import e; import f",
        "a.py": "pass",
        "b.py": "pass",
        "c.py": "pass",
        "d.py": "pass",
        "e.py": "pass",
        "f.py": "pass"
    })
    analyzer = PythonImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    # 'cli' module is stable (I=1.0 because ca=0, ce=6)
    # But it should be skipped from 'highly unstable' issues/ghosts
    issues = [i for i in report["issues"] if "highly unstable" in i]
    assert not any("cli" in i for i in issues)

def test_relative_imports(tmp_path):
    create_python_repo(tmp_path, {
        "pkg/__init__.py": "",
        "pkg/a.py": "from .b import x\n",
        "pkg/b.py": "from ..pkg import c\n",
        "pkg/c.py": "pass"
    })
    analyzer = PythonImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    edges = analyzer.graph.edges
    # pkg.a -> pkg.b (from .b)
    assert ("pkg.a", "pkg.b") in edges
    # pkg.b -> pkg.c (from ..pkg import c)
    # pkg.b parts: ['pkg', 'b']. level=2 -> base is [] -> base.c -> pkg.c?
    # Actually if current is pkg.b, level 2 means go up twice from 'pkg.b'
    # pkg.b -> pkg -> (root).
    # Wait, parts[:-2] for pkg.b is []. So base is "".
    # node.module is "pkg". so it returns "pkg".
    # And then we import 'c' from pkg.
    # Our analyzer should have pkg.c in its nodes.
    assert ("pkg.b", "pkg") in edges or any(dst == "pkg" for src, dst in edges if src == "pkg.b")
