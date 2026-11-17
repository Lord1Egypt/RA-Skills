"""
parse_tree.py — Visualize Python ASTs as DOT/SVG/PNG graphs.

Use when explaining how Python parses a piece of code, or when teaching
AST-based static analysis. Falls back to DOT if graphviz isn't installed.
"""
from __future__ import annotations

import ast
import os
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    id: str
    label: str
    node_type: str  # 'function', 'class', 'variable', 'literal', 'default'
    children: list["TreeNode"]


class ParseTreeVisualizer:
    """Build a TreeNode tree from Python source, render as DOT/SVG/PNG.

    The visual style is color-coded by node kind — functions blue, classes
    green, variables orange, literals cyan. Useful for educational diagrams.
    """

    STYLES: dict[str, dict[str, str]] = {
        "function": {"shape": "box", "color": "#4A90D9", "style": "filled"},
        "class": {"shape": "box", "color": "#5CB85C", "style": "filled"},
        "variable": {"shape": "ellipse", "color": "#F0AD4E", "style": "filled"},
        "literal": {"shape": "plaintext", "color": "#5BC0DE"},
        "control": {"shape": "diamond", "color": "#D9534F", "style": "filled"},
        "default": {"shape": "ellipse", "color": "#BDC3C7"},
    }

    def __init__(self):
        self._counter = 0

    def _new_id(self) -> str:
        self._counter += 1
        return f"n{self._counter}"

    def from_ast(self, source: str, max_depth: int = 10) -> TreeNode:
        """Parse `source` and return the root TreeNode."""
        tree = ast.parse(source)
        return self._ast_to_tree(tree, 0, max_depth)

    def _ast_to_tree(
        self, node: ast.AST, depth: int, max_depth: int
    ) -> Optional[TreeNode]:
        if depth > max_depth:
            return None

        node_id = self._new_id()
        node_type = type(node).__name__

        # Classify the node for styling
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            label, style_type = f"def {node.name}()", "function"
        elif isinstance(node, ast.ClassDef):
            label, style_type = f"class {node.name}", "class"
        elif isinstance(node, ast.Name):
            label, style_type = node.id, "variable"
        elif isinstance(node, ast.Constant):
            label, style_type = repr(node.value)[:30], "literal"
        elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match)):
            label, style_type = node_type, "control"
        else:
            label, style_type = node_type, "default"

        children: list[TreeNode] = []
        for child in ast.iter_child_nodes(node):
            child_tree = self._ast_to_tree(child, depth + 1, max_depth)
            if child_tree is not None:
                children.append(child_tree)

        return TreeNode(node_id, label, style_type, children)

    def to_dot(self, root: TreeNode, title: str = "Parse Tree") -> str:
        """Render the tree as a Graphviz DOT string."""
        lines = [
            f'digraph "{title}" {{',
            "  rankdir=TB;",
            '  node [fontname="Helvetica"];',
        ]
        self._add_node_dot(root, lines)
        self._add_edge_dot(root, lines)
        lines.append("}")
        return "\n".join(lines)

    def _add_node_dot(self, node: TreeNode, lines: list[str]) -> None:
        style = self.STYLES.get(node.node_type, self.STYLES["default"])
        style_str = ", ".join(f'{k}="{v}"' for k, v in style.items())
        label = node.label.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'  "{node.id}" [label="{label}", {style_str}];')
        for child in node.children:
            self._add_node_dot(child, lines)

    def _add_edge_dot(self, node: TreeNode, lines: list[str]) -> None:
        for child in node.children:
            lines.append(f'  "{node.id}" -> "{child.id}";')
            self._add_edge_dot(child, lines)

    def export_dot(self, root: TreeNode, path: str, title: str = "Parse Tree") -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_dot(root, title))

    def export_svg(self, root: TreeNode, path: str, title: str = "Parse Tree") -> bool:
        """Render to SVG via graphviz `dot`. Returns False if graphviz missing."""
        dot_content = self.to_dot(root, title)
        try:
            result = subprocess.run(
                ["dot", "-Tsvg"],
                input=dot_content.encode(),
                capture_output=True,
                timeout=30,
            )
            if result.returncode == 0:
                with open(path, "wb") as f:
                    f.write(result.stdout)
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return False

    def export_png(self, root: TreeNode, path: str, title: str = "Parse Tree", dpi: int = 150) -> bool:
        """Render to PNG via graphviz `dot`. Returns False if graphviz missing."""
        dot_content = self.to_dot(root, title)
        try:
            result = subprocess.run(
                ["dot", "-Tpng", f"-Gdpi={dpi}"],
                input=dot_content.encode(),
                capture_output=True,
                timeout=30,
            )
            if result.returncode == 0:
                with open(path, "wb") as f:
                    f.write(result.stdout)
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return False


def visualize_ast(
    source: str,
    output_path: str | None = None,
    format: str = "dot",
    title: str = "AST",
) -> str:
    """Visualize Python source as an AST graph.

    Args:
        source: Python source code
        output_path: Where to save (extension determines format if format='auto')
        format: 'dot', 'svg', 'png', or 'auto' (use output_path extension)
        title: Graph title

    Returns the DOT content string regardless of output format.
    """
    viz = ParseTreeVisualizer()
    tree = viz.from_ast(source)
    dot = viz.to_dot(tree, title)

    if output_path:
        ext = os.path.splitext(output_path)[1].lower().lstrip(".")
        actual_format = ext if format == "auto" and ext in ("svg", "png", "dot") else format

        if actual_format == "svg":
            if not viz.export_svg(tree, output_path, title):
                # Fallback to DOT if graphviz not available
                fallback = output_path.replace(".svg", ".dot")
                viz.export_dot(tree, fallback, title)
                print(f"graphviz not available — wrote DOT to {fallback}")
        elif actual_format == "png":
            if not viz.export_png(tree, output_path, title):
                fallback = output_path.replace(".png", ".dot")
                viz.export_dot(tree, fallback, title)
                print(f"graphviz not available — wrote DOT to {fallback}")
        else:
            viz.export_dot(tree, output_path, title)

    return dot


__all__ = ["ParseTreeVisualizer", "visualize_ast", "TreeNode"]
