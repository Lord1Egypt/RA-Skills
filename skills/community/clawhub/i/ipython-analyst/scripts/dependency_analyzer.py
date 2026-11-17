"""
dependency_analyzer.py — Analyze code dependencies and call graphs via AST.

Use to find: which functions call which, what's an entry point (called by
nobody internally), what imports a script pulls in. Output as DOT graph
for visualization.
"""
from __future__ import annotations

import ast
from collections import defaultdict
from typing import Any


class DependencyAnalyzer:
    """Build a call graph and import map from Python source.

    Limitations:
    - Method calls (obj.method()) are tracked as `method`, not `Class.method`.
    - Calls via computed names (callables in variables) are tracked only
      when the variable is a direct Name reference.
    - Dynamic imports (importlib.import_module) are not followed.
    """

    def __init__(self, source: str):
        self.tree = ast.parse(source)
        self.imports: dict[str, str] = {}  # alias → full module path
        self.classes: dict[str, list[str]] = {}  # class name → method names
        self.call_graph: dict[str, set[str]] = defaultdict(set)
        self._analyze()

    def _analyze(self) -> None:
        # First pass: imports and class definitions
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports[alias.asname or alias.name] = alias.name
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    full_name = f"{module}.{alias.name}" if module else alias.name
                    self.imports[alias.asname or alias.name] = full_name
            elif isinstance(node, ast.ClassDef):
                self.classes[node.name] = [
                    n.name for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]

        # Second pass: build call graph with a NodeVisitor that tracks current function
        analyzer = self

        class CallVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current: str | None = None
                self.func_stack: list[str] = []

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                self.func_stack.append(node.name)
                self.current = ".".join(self.func_stack)
                self.generic_visit(node)
                self.func_stack.pop()
                self.current = ".".join(self.func_stack) if self.func_stack else None

            visit_AsyncFunctionDef = visit_FunctionDef

            def visit_Call(self, node: ast.Call) -> None:
                if self.current:
                    # Direct name call: foo()
                    if isinstance(node.func, ast.Name):
                        analyzer.call_graph[self.current].add(node.func.id)
                    # Method call: obj.method() — track as just method name
                    elif isinstance(node.func, ast.Attribute):
                        analyzer.call_graph[self.current].add(node.func.attr)
                self.generic_visit(node)

        CallVisitor().visit(self.tree)

    def get_entry_points(self) -> list[str]:
        """Functions that are defined but never called internally —
        likely entry points (called from outside or by main())."""
        called = set()
        for callees in self.call_graph.values():
            called.update(callees)
        defined = set(self.call_graph.keys())
        return sorted(defined - called)

    def get_orphans(self) -> list[str]:
        """Functions that are called but not defined internally —
        likely external imports or builtins."""
        defined = set(self.call_graph.keys())
        called = set()
        for callees in self.call_graph.values():
            called.update(callees)
        return sorted(called - defined)

    def export_dot(self, path: str) -> None:
        """Export call graph as Graphviz DOT format."""
        lines = ["digraph calls {", "  rankdir=LR;"]
        for caller, callees in self.call_graph.items():
            for callee in callees:
                # Escape quotes in names
                c = caller.replace('"', '\\"')
                ce = callee.replace('"', '\\"')
                lines.append(f'  "{c}" -> "{ce}";')
        lines.append("}")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def analyze_dependencies(source_or_path: str) -> dict[str, Any]:
    """Analyze imports, classes, and call graph from source or .py file."""
    if source_or_path.endswith(".py") and "\n" not in source_or_path[:50]:
        with open(source_or_path, encoding="utf-8") as f:
            source = f.read()
    else:
        source = source_or_path
    d = DependencyAnalyzer(source)
    return {
        "imports": d.imports,
        "classes": d.classes,
        "call_graph": {k: sorted(v) for k, v in d.call_graph.items()},
        "entry_points": d.get_entry_points(),
        "orphans": d.get_orphans(),
    }


__all__ = ["DependencyAnalyzer", "analyze_dependencies"]
