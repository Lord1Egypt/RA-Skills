"""
code_analyzer.py — Static code analysis with complexity & smell detection.

Bug fix vs v6:
- `_analyze_function` now correctly counts `elif`/`else` branches, `except`
  handlers, `with` blocks, comprehensions, and conditional expressions.
  v6 only walked top-level `If`/`For`/`While` nodes via ast.walk, which
  missed `orelse` chains entirely — a 10-branch if/elif/elif/... was
  reported as complexity 2.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any


@dataclass
class FunctionMetrics:
    name: str
    lineno: int
    complexity: int
    max_nesting: int
    params: list[str]
    docstring: str


@dataclass
class ClassMetrics:
    name: str
    bases: list[str]
    methods: list[str]
    is_dataclass: bool


# Node types that each add 1 to cyclomatic complexity.
BRANCH_NODES: tuple[type[ast.AST], ...] = (
    ast.If, ast.For, ast.AsyncFor, ast.While,
    ast.ExceptHandler,  # each except clause is a branch
    ast.With, ast.AsyncWith,
    ast.Assert,
    ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
    ast.IfExp,  # ternary
    ast.BoolOp,  # `and` / `or` — each adds a path
    ast.Match,  # match/case (3.10+)
)


class CodeAnalyzer:
    """Comprehensive static analyzer with code smell detection.

    Use to find hotspots in a script before optimizing, or to flag functions
    that need refactoring before they grow further.
    """

    COMPLEXITY_THRESHOLD = 10
    NESTING_THRESHOLD = 4
    PARAM_THRESHOLD = 5

    def __init__(self, source_code: str):
        self.source = source_code
        self.lines = source_code.split("\n")
        self.tree = ast.parse(source_code)
        self.functions: dict[str, FunctionMetrics] = {}
        self.classes: dict[str, ClassMetrics] = {}
        self.regex_patterns: list[dict] = []
        self.imports: list[str] = []
        self.issues: list[dict] = []
        self._analyze()

    def _analyze(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class(node)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._analyze_function(node)
            elif isinstance(node, ast.Call):
                self._analyze_call(node)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                self.imports.append(ast.unparse(node))
        self._detect_issues()

    def _analyze_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        complexity = 1  # base path
        max_nesting = 0

        def walk(n: ast.AST, depth: int = 0) -> None:
            nonlocal complexity, max_nesting
            for child in ast.iter_child_nodes(n):
                # Track nesting depth at branch points
                if isinstance(child, BRANCH_NODES):
                    complexity += 1
                    # For BoolOp, each additional operand is another path
                    if isinstance(child, ast.BoolOp):
                        complexity += max(0, len(child.values) - 1)
                    # For Match, each case is a branch
                    if isinstance(child, ast.Match):
                        complexity += len(child.cases)
                    max_nesting = max(max_nesting, depth + 1)
                    walk(child, depth + 1)
                elif isinstance(child, ast.Try):
                    # try itself isn't a branch, but each except is
                    walk(child, depth + 1)
                else:
                    walk(child, depth)

        walk(node)

        self.functions[node.name] = FunctionMetrics(
            name=node.name,
            lineno=node.lineno,
            complexity=complexity,
            max_nesting=max_nesting,
            params=[a.arg for a in node.args.args],
            docstring=ast.get_docstring(node) or "",
        )

    def _analyze_class(self, node: ast.ClassDef) -> None:
        self.classes[node.name] = ClassMetrics(
            name=node.name,
            bases=[ast.unparse(b) for b in node.bases],
            methods=[n.name for n in node.body if isinstance(n, ast.FunctionDef)],
            is_dataclass=any(
                isinstance(d, ast.Name) and d.id == "dataclass"
                or isinstance(d, ast.Attribute) and d.attr == "dataclass"
                for d in node.decorator_list
            ),
        )

    def _analyze_call(self, node: ast.Call) -> None:
        """Find re.compile() calls with literal patterns — useful for regex debugging."""
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "compile"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "re"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        ):
            self.regex_patterns.append({
                "pattern": node.args[0].value,
                "lineno": node.lineno,
            })

    def _detect_issues(self) -> None:
        for name, f in self.functions.items():
            if f.complexity > self.COMPLEXITY_THRESHOLD:
                self.issues.append({
                    "type": "high_complexity", "severity": "warning",
                    "location": f"{name}:{f.lineno}",
                    "message": f"Complexity {f.complexity} (threshold {self.COMPLEXITY_THRESHOLD})",
                })
            if f.max_nesting > self.NESTING_THRESHOLD:
                self.issues.append({
                    "type": "deep_nesting", "severity": "warning",
                    "location": f"{name}:{f.lineno}",
                    "message": f"Nesting depth {f.max_nesting} (threshold {self.NESTING_THRESHOLD})",
                })
            if len(f.params) > self.PARAM_THRESHOLD:
                self.issues.append({
                    "type": "too_many_params", "severity": "info",
                    "location": f"{name}:{f.lineno}",
                    "message": f"{len(f.params)} params (threshold {self.PARAM_THRESHOLD})",
                })
            if not f.docstring:
                self.issues.append({
                    "type": "missing_docstring", "severity": "info",
                    "location": f"{name}:{f.lineno}",
                    "message": "No docstring",
                })

    def get_summary(self) -> dict[str, Any]:
        return {
            "loc": len(self.lines),
            "classes": len(self.classes),
            "functions": len(self.functions),
            "regex_patterns": len(self.regex_patterns),
            "avg_complexity": (
                sum(f.complexity for f in self.functions.values()) / len(self.functions)
                if self.functions else 0
            ),
            "issues": len(self.issues),
            "top_complex": sorted(
                [(f.name, f.complexity) for f in self.functions.values()],
                key=lambda x: -x[1],
            )[:5],
        }


def analyze_script(source_or_path: str) -> dict[str, Any]:
    """Quick script analysis. Accepts a path (ends in .py, no newline in first 100 chars) or source string."""
    if source_or_path.endswith(".py") and "\n" not in source_or_path[:100]:
        with open(source_or_path, encoding="utf-8") as f:
            source = f.read()
    else:
        source = source_or_path
    analyzer = CodeAnalyzer(source)
    return {"summary": analyzer.get_summary(), "issues": analyzer.issues}


__all__ = ["CodeAnalyzer", "FunctionMetrics", "ClassMetrics", "analyze_script"]
