"""
session_manager.py — Track session memory, compress dormant variables.

Bug fix vs v6:
- `_get_object_size` returns 0 on error (was -1), so `list_variables` totals
  aren't dragged down by failures. Sorting by size now puts unknowns at the
  bottom instead of artificially at the top.
"""
from __future__ import annotations

import gc
import pickle
import sys
import zlib
from dataclasses import dataclass
from typing import Any


@dataclass
class VariableInfo:
    name: str
    type_name: str
    size_bytes: int
    is_operational: bool
    is_compressed: bool


class SessionManager:
    """Track and manage variables in the IPython user namespace.

    Use this when working with large datasets across multiple cells —
    identify what's eating memory, compress dormant DataFrames, restore
    them later.
    """

    PROTECTED_PREFIXES = {"_", "np", "pd", "plt", "sns", "sklearn", "torch", "nx"}
    OPERATIONAL_TYPES = {"Figure", "Axes", "Connection", "Session"}

    def __init__(self):
        self._operational_vars: set[str] = set()
        self._compression_cache: dict[str, bytes] = {}
        self._summaries: dict[str, str] = {}

    def get_namespace(self) -> dict[str, Any]:
        try:
            from IPython import get_ipython
            ip = get_ipython()
            if ip is not None:
                return ip.user_global_ns
        except Exception:
            pass
        return globals()

    def list_variables(self) -> list[VariableInfo]:
        ns = self.get_namespace()
        variables = []
        for name, obj in ns.items():
            if any(name.startswith(p) for p in self.PROTECTED_PREFIXES):
                continue
            is_operational = name in self._operational_vars or type(obj).__name__ in self.OPERATIONAL_TYPES
            size = self._get_object_size(obj)
            variables.append(
                VariableInfo(name, type(obj).__name__, size, is_operational, name in self._compression_cache)
            )
        return sorted(variables, key=lambda v: v.size_bytes, reverse=True)

    def _get_object_size(self, obj: Any) -> int:
        """Get accurate memory size for an object. Returns 0 on failure."""
        try:
            type_name = type(obj).__name__
            # Pandas DataFrame/Series — use deep memory usage (accounts for object dtype)
            if hasattr(obj, "memory_usage") and callable(obj.memory_usage):
                usage = obj.memory_usage(deep=True)
                return int(usage.sum() if hasattr(usage, "sum") else usage)
            # NumPy array — use nbytes
            if hasattr(obj, "nbytes"):
                return int(obj.nbytes)
            # Default — shallow size
            return sys.getsizeof(obj)
        except Exception:
            return 0

    def mark_operational(self, *var_names: str) -> None:
        """Mark variables as operational (won't be compressed)."""
        self._operational_vars.update(var_names)

    def get_memory_usage(self) -> dict[str, float]:
        variables = self.list_variables()
        total = sum(v.size_bytes for v in variables if v.size_bytes > 0)
        operational = sum(v.size_bytes for v in variables if v.is_operational and v.size_bytes > 0)
        return {"total_mb": total / 1024 / 1024, "operational_mb": operational / 1024 / 1024}

    def compress_variable(self, name: str) -> bool:
        """Pickle+zlib-compress a variable, then delete it from the namespace.

        Use when you have a big intermediate you might need again but don't
        need right now. Restore with decompress_variable.
        """
        ns = self.get_namespace()
        if name not in ns or name in self._operational_vars:
            return False
        try:
            obj = ns[name]
            pickled = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
            compressed = zlib.compress(pickled, level=9)
            self._compression_cache[name] = compressed
            self._summaries[name] = type(obj).__name__
            del ns[name]
            gc.collect()
            return True
        except Exception:
            return False

    def decompress_variable(self, name: str) -> Any:
        """Restore a previously compressed variable."""
        if name not in self._compression_cache:
            raise KeyError(f"No compressed data for '{name}'")
        obj = pickle.loads(zlib.decompress(self._compression_cache[name]))
        self.get_namespace()[name] = obj
        del self._compression_cache[name]
        return obj

    def list_compressed(self) -> dict[str, str]:
        """Return {name: type_name} for compressed variables."""
        return dict(self._summaries)


def memory_report() -> None:
    """Print a one-line summary of current session memory usage."""
    sm = SessionManager()
    mem = sm.get_memory_usage()
    print(f"Total: {mem['total_mb']:.1f}MB | Operational: {mem['operational_mb']:.1f}MB")


__all__ = ["SessionManager", "VariableInfo", "memory_report"]
