"""
AST-based cost-risk auditor.

Replaces the regex `analyze_code_for_costs` that flagged every medium class
as "recursion" and matched `while True` across hundreds of unrelated lines.

Checks performed:

  CRITICAL
    - LLM API call inside `while True:` or `while 1:` with no break guarded
      by an iteration counter.
    - Self-recursive function (calls itself by name) with an LLM API call
      and no visible depth parameter.

  HIGH
    - retry / while loops that call an API but never reference a counter
      like max_retries / max_attempts.

  MEDIUM
    - LLM API call with no `max_tokens` / `max_completion_tokens` kwarg.
    - Function with > N LLM API calls back-to-back (batching candidate).

All risks carry a file line number so users can jump to the problem.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import List, Optional, Set


# Method-name suffixes that indicate an LLM / chat-completion API call.
# We match on the final attribute because SDKs nest them differently
# (client.chat.completions.create, client.messages.create, client.responses.create,
# anthropic.messages.create, model.generate_content, ...).
_LLM_CALL_ATTRS = {
    "create",              # OpenAI chat.completions / responses, Anthropic messages
    "complete",
    "generate",
    "generate_content",    # Google Gemini
    "chat",                # Cohere
    "invoke_model",        # AWS Bedrock
    "completion",          # LiteLLM
}

# kwargs that bound output size. Any of these satisfies the max_tokens check.
_MAX_TOKEN_KWARGS = {
    "max_tokens", "max_completion_tokens", "max_output_tokens",
    "maxTokens", "max_new_tokens",
}

# Names that act as iteration / retry / recursion bounds.
_BOUND_NAMES = {
    "max_iterations", "max_iter", "max_retries", "max_attempts",
    "max_steps", "max_tries", "max_loops", "retries_left",
    "iterations", "attempts",
    "max_depth", "depth", "max_recursion_depth", "depth_limit",
    "budget", "remaining_budget",
}


@dataclass
class Risk:
    severity: str   # "CRITICAL" | "HIGH" | "MEDIUM"
    line: int
    kind: str       # short machine-readable tag
    message: str
    recommendation: str


def _is_llm_call(node: ast.AST) -> bool:
    """True if `node` is a Call whose attribute chain ends in an LLM verb."""
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if isinstance(f, ast.Attribute):
        return f.attr in _LLM_CALL_ATTRS
    return False


def _has_max_tokens(call: ast.Call) -> bool:
    for kw in call.keywords:
        if kw.arg in _MAX_TOKEN_KWARGS:
            return True
    return False


def _names_referenced(node: ast.AST) -> Set[str]:
    """All bare Name references under `node`. Used to detect bound variables."""
    seen: Set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            seen.add(child.id)
    return seen


def _is_while_true(node: ast.While) -> bool:
    t = node.test
    if isinstance(t, ast.Constant) and t.value is True:
        return True
    if isinstance(t, ast.NameConstant) and t.value is True:  # pragma: no cover  (pre-3.8)
        return True
    if isinstance(t, ast.Name) and t.id == "True":
        return True
    if isinstance(t, ast.Constant) and t.value == 1:
        return True
    return False


class _Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.risks: List[Risk] = []
        self._loop_stack: List[ast.AST] = []
        self._func_stack: List[ast.FunctionDef] = []

    # --- loops ----------------------------------------------------------
    def visit_While(self, node: ast.While) -> None:
        self._loop_stack.append(node)
        try:
            self._check_loop(node, infinite=_is_while_true(node))
            self.generic_visit(node)
        finally:
            self._loop_stack.pop()

    def visit_For(self, node: ast.For) -> None:
        self._loop_stack.append(node)
        try:
            self.generic_visit(node)
        finally:
            self._loop_stack.pop()

    def _check_loop(self, node: ast.While, infinite: bool) -> None:
        # Does the loop body contain an LLM call?
        has_llm = any(_is_llm_call(c) for c in ast.walk(node))
        if not has_llm:
            return
        refs = _names_referenced(node)
        bound = refs & _BOUND_NAMES
        if infinite and not bound:
            self.risks.append(Risk(
                severity="CRITICAL",
                line=node.lineno,
                kind="unbounded_while_true_api",
                message="while True loop calls an LLM API with no iteration bound",
                recommendation="Add max_iterations and break when it hits 0.",
            ))
        elif not infinite and not bound:
            # A regular while-loop calling the API without a visible bound.
            self.risks.append(Risk(
                severity="HIGH",
                line=node.lineno,
                kind="unbounded_while_api",
                message="while loop calls an LLM API with no retry/iteration counter",
                recommendation="Reference max_retries / max_attempts / max_iterations.",
            ))

    # --- functions ------------------------------------------------------
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._func_stack.append(node)
        try:
            self._check_recursion(node)
            self._check_batching_candidate(node)
            self.generic_visit(node)
        finally:
            self._func_stack.pop()

    def visit_AsyncFunctionDef(self, node) -> None:  # type: ignore[override]
        # Same logic as sync functions.
        self._func_stack.append(node)
        try:
            self._check_recursion(node)
            self._check_batching_candidate(node)
            self.generic_visit(node)
        finally:
            self._func_stack.pop()

    def _check_recursion(self, func: ast.FunctionDef) -> None:
        has_llm = False
        calls_self = False
        for child in ast.walk(func):
            if isinstance(child, ast.Call):
                if _is_llm_call(child):
                    has_llm = True
                f = child.func
                if isinstance(f, ast.Name) and f.id == func.name:
                    calls_self = True
                elif isinstance(f, ast.Attribute) and f.attr == func.name:
                    # e.g. self.<func.name>(...)
                    calls_self = True
        if has_llm and calls_self:
            arg_names = {a.arg for a in func.args.args}
            if not (arg_names & _BOUND_NAMES):
                self.risks.append(Risk(
                    severity="CRITICAL",
                    line=func.lineno,
                    kind="unbounded_recursion_api",
                    message=f"function {func.name!r} recurses and calls an LLM API without a depth parameter",
                    recommendation="Add a depth/max_depth argument and short-circuit when it hits 0.",
                ))

    def _check_batching_candidate(self, func: ast.FunctionDef) -> None:
        calls_in_func = sum(1 for n in ast.walk(func) if _is_llm_call(n))
        if calls_in_func >= 5:
            self.risks.append(Risk(
                severity="MEDIUM",
                line=func.lineno,
                kind="many_sequential_calls",
                message=f"{calls_in_func} LLM API calls inside {func.name!r}",
                recommendation="Consider batching, prompt caching, or parallelism.",
            ))

    # --- bare calls -----------------------------------------------------
    def visit_Call(self, node: ast.Call) -> None:
        if _is_llm_call(node) and not _has_max_tokens(node):
            self.risks.append(Risk(
                severity="MEDIUM",
                line=node.lineno,
                kind="missing_max_tokens",
                message="LLM API call without max_tokens / max_completion_tokens",
                recommendation="Pass max_tokens to bound worst-case output size.",
            ))
        self.generic_visit(node)


def audit_source(code: str) -> List[Risk]:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [Risk(
            severity="HIGH",
            line=e.lineno or 0,
            kind="syntax_error",
            message=f"Could not parse file: {e.msg}",
            recommendation="Fix syntax; auditor needs valid Python.",
        )]
    v = _Visitor()
    v.visit(tree)
    return v.risks


def audit_file(path) -> List[Risk]:
    from pathlib import Path
    return audit_source(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}


def format_report(path: str, risks: List[Risk]) -> str:
    if not risks:
        return f"{path}: no cost risks detected."
    risks = sorted(risks, key=lambda r: (_SEVERITY_ORDER.get(r.severity, 9), r.line))
    lines = [f"{path}: {len(risks)} risk(s)"]
    for r in risks:
        lines.append(f"  [{r.severity:<8}] line {r.line:>4}: {r.message}")
        lines.append(f"    → {r.recommendation}")
    return "\n".join(lines)


def main() -> int:
    import sys
    if len(sys.argv) < 2:
        print("usage: python3 scripts/code_audit.py <file.py> [<file.py> ...]")
        return 2
    any_risks = False
    for path in sys.argv[1:]:
        risks = audit_file(path)
        if risks:
            any_risks = True
        print(format_report(path, risks))
    return 1 if any_risks else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
