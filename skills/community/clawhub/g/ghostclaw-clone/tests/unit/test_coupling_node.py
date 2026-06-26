"""Tests for Node.js import coupling analysis."""

import sys
from pathlib import Path

# Add repo root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from ghostclaw.core.node_coupling import NodeImportAnalyzer


def create_node_repo(tmp_path: Path, structure: dict):
    for relpath, content in structure.items():
        p = tmp_path / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)


def test_simple_imports(tmp_path):
    create_node_repo(tmp_path, {
        "a.js": "const b = require('./b');\n",
        "b.js": "const c = require('./c');\n",
        "c.js": "module.exports = 1;\n"
    })
    analyzer = NodeImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    metrics = report["coupling_metrics"]
    assert "a" in metrics
    assert metrics["a"]["efferent"] == 1
    assert metrics["b"]["afferent"] == 1


def test_circular_dependency(tmp_path):
    create_node_repo(tmp_path, {
        "a.js": "const b = require('./b');\n",
        "b.js": "const a = require('./a');\n"
    })
    analyzer = NodeImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    assert len(report["circular_dependencies"]) >= 1

def test_entry_point_not_flagged_as_unstable(tmp_path):
    # Create a repo where a 'cli' module imports many others
    create_node_repo(tmp_path, {
        "cli.js": "require('./a'); require('./b'); require('./c'); require('./d'); require('./e'); require('./f')",
        "a.js": "pass",
        "b.js": "pass",
        "c.js": "pass",
        "d.js": "pass",
        "e.js": "pass",
        "f.js": "pass"
    })
    analyzer = NodeImportAnalyzer(str(tmp_path))
    report = analyzer.analyze()
    # 'cli' module is stable (I=1.0 because ca=0, ce=6)
    # But it should be skipped from 'highly unstable' issues/ghosts
    issues = [i for i in report["issues"] if "highly unstable" in i]
    assert not any("cli" in i for i in issues)
