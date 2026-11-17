"""
regex_debugger.py — Regex pattern analysis with catastrophic backtracking detection.

Bug fix vs v6:
- Uses OperationTimeout from safe_execution instead of the v6 shadowed
  TimeoutError class. Importers don't need to know about our local exception.
"""
from __future__ import annotations

import re
from typing import Any

# Import OperationTimeout from safe_execution. If that import fails (script run
# standalone), define a fallback so the module is still usable.
try:
    from safe_execution import timeout_context, OperationTimeout
except ImportError:
    import signal
    import math
    class OperationTimeout(Exception):
        pass
    from contextlib import contextmanager
    @contextmanager
    def timeout_context(seconds: float, error_message: str = "Operation timed out"):
        def handler(signum, frame): raise OperationTimeout(error_message)
        seconds_int = max(1, int(math.ceil(seconds)))
        original = signal.signal(signal.SIGALRM, handler)
        signal.alarm(seconds_int)
        try: yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, original)


class RegexDebugger:
    """Analyze a regex pattern for risks and stress-test it for backtracking.

    Use when a regex is hanging on certain inputs or you want to assess
    whether a pattern is safe for untrusted input.
    """

    # Patterns that commonly cause exponential backtracking
    RISK_PATTERNS = [
        (r"\([^)]*[+*][^)]*\)[+*]", "nested_quantifier", "high",
         "Nested quantifiers like (a+)+ cause exponential backtracking"),
        (r"\([^)]*\)\{[^}]+\}", "quantified_group", "high",
         "Quantified group like (a){2,10} can backtrack heavily"),
        (r"\.\*[+*]", "double_quantifier", "medium",
         "Multiple greedy wildcards .*.* may cause issues"),
    ]

    def __init__(self, pattern: str, flags: int = 0):
        self.pattern = pattern
        self.flags = flags
        self.compiled: re.Pattern | None = None
        self.error: str | None = None
        try:
            self.compiled = re.compile(pattern, flags)
        except re.error as e:
            self.error = str(e)

    def is_valid(self) -> bool:
        return self.compiled is not None

    def detect_risks(self) -> list[dict]:
        """Static analysis of the pattern for known catastrophic-backtracking shapes."""
        risks = []
        for pat, risk_type, severity, message in self.RISK_PATTERNS:
            if re.search(pat, self.pattern):
                risks.append({
                    "type": risk_type,
                    "severity": severity,
                    "message": message,
                    "pattern_match": pat,
                })

        # Count greedy wildcards as a softer signal
        greedy_count = self.pattern.count(".*") + self.pattern.count(".+") + self.pattern.count(".?")
        if greedy_count > 2:
            risks.append({
                "type": "multiple_greedy",
                "severity": "medium",
                "message": f"{greedy_count} greedy wildcards — consider possessive quantifiers or atomic groups",
            })

        # Check for unbounded quantifiers on alternations
        if re.search(r"\([^|]+\|[^|]+\)[+*]", self.pattern):
            risks.append({
                "type": "quantified_alternation",
                "severity": "medium",
                "message": "Quantified alternation can backtrack on partial matches",
            })

        return risks

    def stress_test(self, timeout: float = 0.5) -> dict[str, Any]:
        """Run the regex against adversarial inputs with a per-input timeout.

        Adversarial inputs target common backtracking failure modes:
        - Long strings that almost match (force full exploration)
        - Strings with the right structure but wrong terminator
        - Unicode and control characters
        """
        if not self.compiled:
            return {"error": self.error or "Pattern did not compile"}

        # Build adversarial test cases targeted at the pattern
        cases = [
            ("empty", ""),
            ("space", " "),
            ("long_a", "a" * 100),
            ("long_a_1000", "a" * 1000),
            ("unbalanced_parens", "(" * 50 + "x" + ")" * 50),
            ("almost_match", "a" * 50 + "b"),  # forces backtrack if pattern wants all a's
            ("unicode", "中文" * 20),
            ("control", "".join(chr(i) for i in range(0, 32))),
            ("mixed", "a1b2c3" * 30),
        ]

        results: dict[str, Any] = {"passed": 0, "timeouts": 0, "errors": 0, "details": []}

        for case_name, s in cases:
            try:
                with timeout_context(timeout):
                    self.compiled.search(s)
                results["passed"] += 1
                results["details"].append({"case": case_name, "status": "passed"})
            except OperationTimeout:
                results["timeouts"] += 1
                results["details"].append({
                    "case": case_name, "status": "timeout",
                    "message": f"Exceeded {timeout}s — likely catastrophic backtracking",
                })
            except Exception as e:
                results["errors"] += 1
                results["details"].append({
                    "case": case_name, "status": "error", "message": str(e),
                })

        results["pass_rate"] = results["passed"] / len(cases) if cases else 0
        return results

    def explain(self) -> dict[str, Any]:
        """Full diagnostic: validity, risks, stress test results."""
        return {
            "pattern": self.pattern,
            "valid": self.is_valid(),
            "error": self.error,
            "risks": self.detect_risks(),
            "stress_test": self.stress_test() if self.is_valid() else None,
        }


def debug_regex(pattern: str, flags: int = 0) -> dict[str, Any]:
    """One-shot regex debug: returns validity + risks (no stress test)."""
    debugger = RegexDebugger(pattern, flags)
    return {
        "pattern": pattern,
        "valid": debugger.is_valid(),
        "error": debugger.error,
        "risks": debugger.detect_risks(),
    }


__all__ = ["RegexDebugger", "debug_regex"]
