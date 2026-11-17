"""
safe_execution.py — Resource limits, timeouts, and safe expression evaluation.

Bug fixes vs v6:
- `OperationTimeout` replaces the v6 `class TimeoutError(Exception)` that shadowed
  the builtin TimeoutError and broke `except TimeoutError:` callers.
- `resource_limits` saves and restores the original soft limit (was resetting to
  RLIM_INFINITY, which silently fails when the hard limit is lower).
"""
from __future__ import annotations

import math
import resource
import signal
from contextlib import contextmanager
from typing import Iterator


class OperationTimeout(Exception):
    """Raised by timeout_context when the operation exceeds the deadline.

    Distinct from the builtin TimeoutError so we don't shadow it — code that
    catches the builtin (e.g. socket operations) keeps working.
    """


@contextmanager
def timeout_context(seconds: float, error_message: str = "Operation timed out") -> Iterator[None]:
    """Context manager that raises OperationTimeout after `seconds` elapsed.

    Uses SIGALRM so it can interrupt blocking C calls (regex backtracking,
    socket reads, sleep). Unix-only; on Windows it's a no-op.
    """
    if not hasattr(signal, "SIGALRM"):
        # Windows fallback — no interruption, just yield.
        yield
        return

    def handler(signum: int, frame) -> None:
        raise OperationTimeout(error_message)

    seconds_int = max(1, int(math.ceil(seconds)))
    original_handler = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds_int)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)


@contextmanager
def resource_limits(max_memory_mb: int = 2048, max_cpu_seconds: int = 300) -> Iterator[None]:
    """Context manager to enforce memory and CPU limits on the current process.

    Note: setting RLIMIT_AS too low can crash Python itself (the interpreter needs
    address space for imports, JIT buffers, etc.). Use generous limits and prefer
    timeout_context for stopping specific operations rather than killing the process.
    """
    originals: dict[int, tuple[int, int]] = {}
    try:
        for limit, value in [
            (resource.RLIMIT_AS, max_memory_mb * 1024 * 1024),
            (resource.RLIMIT_CPU, max_cpu_seconds),
        ]:
            try:
                soft, hard = resource.getrlimit(limit)
                # Don't raise above the hard limit — silently cap instead.
                new_soft = min(value, hard) if hard != resource.RLIM_INFINITY else value
                resource.setrlimit(limit, (new_soft, hard))
                originals[limit] = (soft, hard)
            except (ValueError, OSError):
                pass  # resource module Unix-only or limit not supported
        yield
    finally:
        for limit, (soft, hard) in originals.items():
            try:
                resource.setrlimit(limit, (soft, hard))
            except (ValueError, OSError):
                pass


def safe_eval(expression: str, allowed_names: dict | None = None):
    """Evaluate a Python math expression with an AST-walking evaluator.

    Only literal nodes, arithmetic/comparison/boolean operators, and calls
    to whitelisted builtins + ``math`` functions are permitted. Attribute
    access, subscripting, comprehensions, lambdas, and arbitrary calls are
    rejected — so there is no path to ``__class__``, ``__subclasses__``, or
    any other dunder-based escape.

    This is safer than ``eval`` because the AST is walked before any code
    runs: disallowed node types raise ``ValueError`` during parsing, not at
    evaluation time. For truly untrusted code, still run in a subprocess
    with :func:`resource_limits` — defense in depth.

    Args:
        expression: The expression to evaluate (e.g. ``"sin(pi/2) + 2**10"``).
        allowed_names: Optional mapping of additional names the expression
            may reference. **Only callables and scalars are safe to inject
            here** — never pass user-controlled objects or objects with
            privileged methods, because the evaluator will call them.
    """
    import ast as _ast
    import math as _math

    # Build the whitelist of callable names.
    safe_funcs = {
        "abs": abs, "min": min, "max": max, "sum": sum,
        "len": len, "round": round,
    }
    for name in dir(_math):
        if not name.startswith("_"):
            safe_funcs[name] = getattr(_math, name)

    # Constants available by name.
    safe_constants = {
        "True": True, "False": False, "None": None,
        "pi": _math.pi, "e": _math.e, "tau": _math.tau, "inf": _math.inf, "nan": _math.nan,
    }

    # Caller-supplied names. Only scalars and callables are accepted —
    # reject modules, classes, and objects with dunder methods that could
    # be exploited if the evaluator were ever extended to attribute access.
    if allowed_names:
        for key, value in allowed_names.items():
            if key.startswith("_"):
                raise ValueError(f"Refusing to inject reserved name: {key!r}")
            if not (callable(value) or isinstance(value, (int, float, str, bool, type(None)))):
                raise ValueError(
                    f"Refusing to inject non-scalar name {key!r}: "
                    f"only callables and scalars are permitted in allowed_names"
                )
            safe_funcs[key] = value

    # AST node types we permit during the walk. Note: operator nodes (Add,
    # Sub, Mult, etc.) and operator-context nodes (Load, Mod, etc.) are
    # listed here so the pre-evaluation walk doesn't reject them — the
    # _eval dispatcher handles them via the _BINOPS/_UNARYOPS/_CMPOPS maps.
    _ALLOWED_NODES = (
        _ast.Expression,          # top-level wrapper
        _ast.BinOp,               # a + b, a ** b, etc.
        _ast.UnaryOp,             # -a, not a, ~a
        _ast.BoolOp,              # a and b, a or b
        _ast.Compare,             # a == b, a < b, etc.
        _ast.IfExp,               # a if cond else b
        _ast.Constant,            # 1, "str", True, None
        _ast.Name,                # variable references (checked against whitelist)
        _ast.Load,                # name-load context
        _ast.Call,                # function calls (checked against whitelist)
        _ast.keyword,             # keyword arguments in calls
        # List/tuple/dict/set literals — useful for min/max/sum arguments.
        _ast.List, _ast.Tuple, _ast.Dict, _ast.Set,
        # Binary operator types — permitted on the BinOp.op field.
        _ast.Add, _ast.Sub, _ast.Mult, _ast.Div, _ast.FloorDiv, _ast.Mod,
        _ast.Pow, _ast.LShift, _ast.RShift, _ast.BitOr, _ast.BitAnd, _ast.BitXor,
        # Unary operator types — permitted on the UnaryOp.op field.
        _ast.USub, _ast.UAdd, _ast.Not, _ast.Invert,
        # Comparison operator types — permitted on the Compare.ops field.
        _ast.Eq, _ast.NotEq, _ast.Lt, _ast.LtE, _ast.Gt, _ast.GtE,
        # Boolean operator types — permitted on the BoolOp.op field.
        _ast.And, _ast.Or,
    )

    def _eval(node):
        """Recursively evaluate an AST node against the whitelist."""
        if isinstance(node, _ast.Expression):
            return _eval(node.body)
        if isinstance(node, _ast.Constant):
            return node.value
        if isinstance(node, _ast.Name):
            if node.id in safe_constants:
                return safe_constants[node.id]
            if node.id in safe_funcs:
                return safe_funcs[node.id]
            raise ValueError(f"Undefined or unsafe name: {node.id!r}")
        if isinstance(node, _ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            return _BINOPS[type(node.op)](left, right)
        if isinstance(node, _ast.UnaryOp):
            operand = _eval(node.operand)
            return _UNARYOPS[type(node.op)](operand)
        if isinstance(node, _ast.BoolOp):
            values = [_eval(v) for v in node.values]
            if isinstance(node.op, _ast.And):
                result = True
                for v in values:
                    result = v
                    if not v:
                        break
                return result
            else:  # Or
                for v in values:
                    if v:
                        return v
                return values[-1] if values else False
        if isinstance(node, _ast.Compare):
            left = _eval(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = _eval(comparator)
                if not _CMPOPS[type(op)](left, right):
                    return False
                left = right
            return True
        if isinstance(node, _ast.IfExp):
            return _eval(node.body) if _eval(node.test) else _eval(node.orelse)
        if isinstance(node, _ast.Call):
            func = _eval(node.func)
            if not callable(func):
                raise ValueError("Attempted to call a non-callable")
            args = [_eval(a) for a in node.args]
            kwargs = {kw.arg: _eval(kw.value) for kw in node.keywords if kw.arg is not None}
            # Only allow calling whitelisted callables, not arbitrary injected objects.
            if func not in safe_funcs.values():
                raise ValueError("Call to non-whitelisted function")
            return func(*args, **kwargs)
        if isinstance(node, (_ast.List, _ast.Tuple, _ast.Set)):
            return [_eval(elt) for elt in node.elts] if isinstance(node, _ast.List) else \
                   tuple(_eval(elt) for elt in node.elts) if isinstance(node, _ast.Tuple) else \
                   {_eval(elt) for elt in node.elts}
        if isinstance(node, _ast.Dict):
            return {_eval(k): _eval(v) for k, v in zip(node.keys, node.values)}
        raise ValueError(f"Disallowed AST node: {type(node).__name__}")

    import operator as _op
    _BINOPS = {
        _ast.Add: _op.add, _ast.Sub: _op.sub, _ast.Mult: _op.mul,
        _ast.Div: _op.truediv, _ast.FloorDiv: _op.floordiv, _ast.Mod: _op.mod,
        _ast.Pow: _op.pow, _ast.LShift: _op.lshift, _ast.RShift: _op.rshift,
        _ast.BitOr: _op.or_, _ast.BitAnd: _op.and_, _ast.BitXor: _op.xor,
    }
    _UNARYOPS = {
        _ast.USub: _op.neg, _ast.UAdd: _op.pos,
        _ast.Not: _op.not_, _ast.Invert: _op.invert,
    }
    _CMPOPS = {
        _ast.Eq: _op.eq, _ast.NotEq: _op.ne,
        _ast.Lt: _op.lt, _ast.LtE: _op.le,
        _ast.Gt: _op.gt, _ast.GtE: _op.ge,
    }

    try:
        tree = _ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from e

    # Walk the tree once to reject disallowed node types before evaluating.
    for node in _ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(
                f"Disallowed AST node {type(node).__name__!r} in expression — "
                f"safe_eval only permits literals, operators, and whitelisted calls"
            )

    return _eval(tree.body)


__all__ = [
    "OperationTimeout",
    "timeout_context",
    "resource_limits",
    "safe_eval",
]
