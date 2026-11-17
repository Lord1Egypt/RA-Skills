"""
output_differ.py — Compare two outputs to detect semantic regressions.

Use when refactoring a function: capture the old output as a baseline,
make your changes, then diff the new output to verify only intended
changes occurred. Numeric tolerance avoids noise from floating-point drift.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class OutputDiff:
    path: str
    diff_type: str  # 'added', 'removed', 'changed', 'type_change', 'length_change'
    old_value: Any
    new_value: Any
    semantic_change: bool


class OutputDiffer:
    """Recursively compare two values (dict/list/scalar) and produce a diff list.

    Supports:
    - Dicts: added/removed keys, recursive value comparison
    - Lists: length change + per-index comparison
    - Numbers: tolerance-based comparison (default 1e-9)
    - Strings: exact match
    - Other: equality check
    """

    def __init__(
        self,
        ignore_order: bool = False,  # if True, sort lists before comparing
        numeric_tolerance: float = 1e-9,
        ignore_keys: set[str] | None = None,  # keys to skip in dict comparison
    ):
        self.ignore_order = ignore_order
        self.numeric_tolerance = numeric_tolerance
        self.ignore_keys = ignore_keys or set()
        self.diffs: list[OutputDiff] = []

    def compare(self, old: Any, new: Any, path: str = "") -> list[OutputDiff]:
        """Compare two values. Returns the list of diffs found."""
        self.diffs = []
        self._compare(old, new, path)
        return self.diffs

    def _compare(self, old: Any, new: Any, path: str) -> None:
        # Both None — no diff
        if old is None and new is None:
            return

        # One None — changed
        if old is None or new is None:
            self.diffs.append(OutputDiff(path, "changed", old, new, True))
            return

        # Type mismatch (and not bool/int subtlety)
        if type(old) != type(new):
            # Special case: bool vs int — Python treats True == 1, but they're different semantically
            self.diffs.append(OutputDiff(path, "type_change", old, new, True))
            return

        # Dict comparison
        if isinstance(old, dict):
            self._compare_dicts(old, new, path)
        # List comparison
        elif isinstance(old, list):
            self._compare_lists(old, new, path)
        # Numeric comparison with tolerance
        elif isinstance(old, (int, float)) and not isinstance(old, bool):
            if abs(old - new) > self.numeric_tolerance:
                self.diffs.append(OutputDiff(path, "changed", old, new, True))
        # String and other — exact match
        elif old != new:
            self.diffs.append(OutputDiff(path, "changed", old, new, True))

    def _compare_dicts(self, old: dict, new: dict, path: str) -> None:
        old_keys = set(old.keys()) - self.ignore_keys
        new_keys = set(new.keys()) - self.ignore_keys

        for key in old_keys - new_keys:
            current_path = f"{path}.{key}" if path else key
            self.diffs.append(OutputDiff(current_path, "removed", old[key], None, True))

        for key in new_keys - old_keys:
            current_path = f"{path}.{key}" if path else key
            self.diffs.append(OutputDiff(current_path, "added", None, new[key], True))

        for key in old_keys & new_keys:
            current_path = f"{path}.{key}" if path else key
            self._compare(old[key], new[key], current_path)

    def _compare_lists(self, old: list, new: list, path: str) -> None:
        if self.ignore_order:
            # Try to match elements by hash; sort both sides
            try:
                old_sorted = sorted(old, key=lambda x: json.dumps(x, sort_keys=True, default=str))
                new_sorted = sorted(new, key=lambda x: json.dumps(x, sort_keys=True, default=str))
            except (TypeError, ValueError):
                old_sorted, new_sorted = old, new
            old, new = old_sorted, new_sorted

        if len(old) != len(new):
            self.diffs.append(OutputDiff(path, "length_change", len(old), len(new), True))

        for i, (o, n) in enumerate(zip(old, new)):
            self._compare(o, n, f"{path}[{i}]")

    def get_summary(self) -> dict[str, Any]:
        return {
            "total_diffs": len(self.diffs),
            "semantic_diffs": sum(1 for d in self.diffs if d.semantic_change),
            "by_type": {
                t: sum(1 for d in self.diffs if d.diff_type == t)
                for t in {d.diff_type for d in self.diffs}
            },
        }


class BaselineManager:
    """Persist baseline outputs for regression testing across runs.

    Save once before a change, then compare after. Baselines live in
    /home/z/my-project/download/.baselines/ by default — kept with outputs
    so they're easy to inspect.
    """

    def __init__(self, baseline_dir: str = "/home/z/my-project/download/.baselines"):
        self.baseline_dir = baseline_dir
        os.makedirs(baseline_dir, exist_ok=True)

    def save_baseline(self, name: str, output: Any) -> str:
        """Persist `output` as baseline `name`. Returns the file path."""
        data = {
            "output": output,
            "timestamp": datetime.now().isoformat(),
            "hash": hashlib.sha256(
                json.dumps(output, sort_keys=True, default=str).encode()
            ).hexdigest()[:16],
        }
        path = os.path.join(self.baseline_dir, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return path

    def load_baseline(self, name: str) -> dict | None:
        """Load a saved baseline, or None if not found."""
        path = os.path.join(self.baseline_dir, f"{name}.json")
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def compare_with_baseline(self, name: str, new_output: Any) -> dict[str, Any]:
        """Diff `new_output` against the saved baseline `name`."""
        baseline = self.load_baseline(name)
        if baseline is None:
            return {"status": "no_baseline", "message": f"No baseline named '{name}'"}

        differ = OutputDiffer()
        differ.compare(baseline["output"], new_output)
        return {
            "status": "match" if not differ.diffs else "diff",
            "summary": differ.get_summary(),
            "diffs": [
                {"path": d.path, "type": d.diff_type,
                 "old": d.old_value, "new": d.new_value}
                for d in differ.diffs[:50]  # cap to avoid huge responses
            ],
        }


def compare_outputs(old: Any, new: Any, **kwargs) -> dict[str, Any]:
    """One-shot comparison of two values. Returns summary dict."""
    differ = OutputDiffer(**kwargs)
    differ.compare(old, new)
    return {"summary": differ.get_summary(), "diffs": differ.diffs}


__all__ = ["OutputDiffer", "BaselineManager", "compare_outputs", "OutputDiff"]
