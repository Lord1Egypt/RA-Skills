"""Tests for rule validator."""

import sys
from pathlib import Path

# Add repo root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from ghostclaw.core.validator import RuleValidator


def test_node_average_file_size_rule():
    validator = RuleValidator()
    report = {
        "stack": "node",
        "average_lines": 500,
        "large_file_count": 2,
        "coupling_metrics": {}
    }
    result = validator.validate("node", report)
    # Should add issues for average_lines > 200
    issues = result["issues"]
    assert any("Average file size" in i for i in issues)
    # Should add issue for large files
    assert any("files >400 lines" in i for i in issues)


def test_python_average_file_size_rule():
    validator = RuleValidator()
    report = {
        "stack": "python",
        "average_lines": 250,
        "large_file_count": 1,
        "coupling_metrics": {}
    }
    result = validator.validate("python", report)
    issues = result["issues"]
    assert any("Average file size" in i for i in issues)
    assert any("files >300 lines" in i for i in issues)


def test_instability_rule():
    validator = RuleValidator()
    report = {
        "stack": "node",
        "average_lines": 100,
        "large_file_count": 0,
        "coupling_metrics": {
            "unstableModule": {
                "instability": 0.95,
                "efferent": 10
            }
        }
    }
    result = validator.validate("node", report)
    issues = result["issues"]
    assert any("unstableModule" in i and "highly unstable" in i for i in issues)


def test_unknown_stack_passes_through():
    validator = RuleValidator()
    report = {
        "stack": "unknown",
        "files_analyzed": 10,
        "average_lines": 100,
        "large_file_count": 0,
        "coupling_metrics": {},
        "issues": [],
        "architectural_ghosts": [],
        "red_flags": []
    }
    result = validator.validate("unknown", report)
    # Should not modify the report (no additional issues)
    assert result["issues"] == []
    assert result["architectural_ghosts"] == []

def test_import_dependency_rule():
    validator = RuleValidator()
    # Mock report for Node.js stack which has forbidden "repositories -> controllers"
    report = {
        "stack": "node",
        "import_edges": [
            ("src.repositories.UserRepo", "src.controllers.UserController")
        ],
        "issues": [],
        "architectural_ghosts": [],
        "red_flags": []
    }
    result = validator.validate("node", report)
    issues = result["issues"]
    assert any("Forbidden dependency" in i for i in issues)
    assert any("UserRepo" in i and "UserController" in i for i in issues)


def test_global_empty_codebase_rule():
    validator = RuleValidator()
    # Mock report with 0 files analyzed
    report = {
        "stack": "unknown",
        "files_analyzed": 0,
        "average_lines": 0,
        "large_file_count": 0,
        "issues": [],
        "architectural_ghosts": [],
        "red_flags": []
    }
    result = validator.validate("unknown", report)
    issues = result["issues"]
    assert any("Empty codebase detected" in i for i in issues)
    assert any("empty_codebase" in g for g in result["architectural_ghosts"])
