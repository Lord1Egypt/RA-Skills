#!/usr/bin/env python3
"""
memory-oracle: test_capture.py
Tests for rule-based pattern matching in both EN and RU.

Usage:
  python3 test_capture.py
  python3 test_capture.py -v    # Verbose
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from capture import extract_facts, load_patterns

PATTERNS = load_patterns()

# Test cases: (input_text, expected_type, expected_min_count, description)
TEST_CASES = [
    # English — preferences
    ("I prefer using Python over JavaScript for backend work",
     "preference", 1, "EN preference detected"),

    # English — decisions
    ("We decided to go with SQLite for the memory database",
     "decision", 1, "EN decision detected"),

    # English — identity
    ("I work at Anthropic as a research engineer",
     "identity", 1, "EN identity detected"),

    # English — tasks
    ("I need to finish the API integration by Friday",
     "task", 1, "EN task detected"),

    # English — guardrails
    ("Never execute trades without my explicit approval",
     "guardrail", 1, "EN guardrail detected"),

    # English — contacts (note: "by Monday" also matches task, which has higher importance)
    ("My boss John wants the report by Monday",
     "task", 1, "EN contact+task hybrid — task wins by importance"),

    # English — pure contact (no task keywords)
    ("I work with Sarah on the frontend team",
     "contact", 1, "EN pure contact detected"),

    # English — projects
    ("The project called memory-oracle is almost ready",
     "project", 1, "EN project detected"),

    # Russian — preferences
    ("Я предпочитаю использовать лёгкие архитектуры без бэкенда",
     "preference", 1, "RU preference detected"),

    # Russian — decisions
    ("Решили что будем использовать Bybit API для трейдинга",
     "decision", 1, "RU decision detected"),

    # Russian — identity
    ("Я работаю в области крипто и AI агентов",
     "identity", 1, "RU identity detected"),

    # Russian — tasks
    ("Нужно доделать систему рефлексии к понедельнику",
     "task", 1, "RU task detected"),

    # Russian — guardrails
    ("Никогда не забывай проверять API ключ перед деплоем",
     "guardrail", 1, "RU guardrail detected"),

    # Explicit remember
    ("Remember this: always use WAL mode for SQLite",
     "guardrail", 1, "EN explicit remember + guardrail"),

    # Russian explicit remember
    ("Запомни: деплой только через GitHub Actions",
     None, 1, "RU explicit remember triggers capture"),

    # Negative — should NOT extract
    ("Hello, how are you today?",
     None, 0, "EN small talk — no extraction"),

    ("Привет, как дела?",
     None, 0, "RU small talk — no extraction"),

    # Mixed language
    ("Я использую Python для бэкенда и React для фронта",
     "tech_stack", 1, "Mixed RU+tech terms detected"),
]


def run_tests(verbose=False):
    passed = 0
    failed = 0
    total = len(TEST_CASES)

    for text, expected_type, expected_min, description in TEST_CASES:
        facts = extract_facts(text, PATTERNS)

        if expected_min == 0:
            # Expect no extraction
            ok = len(facts) == 0
        else:
            ok = len(facts) >= expected_min
            if ok and expected_type:
                # Check that at least one fact has the expected type
                types_found = {f["type"] for f in facts}
                ok = expected_type in types_found

        if ok:
            passed += 1
            if verbose:
                print(f"  ✓ {description}")
                if facts:
                    for f in facts:
                        print(f"    → [{f['type']}] {f['content'][:60]}...")
        else:
            failed += 1
            types_found = {f["type"] for f in facts} if facts else set()
            print(f"  ✗ {description}")
            print(f"    Input: {text[:80]}...")
            print(f"    Expected: type={expected_type}, min={expected_min}")
            print(f"    Got: {len(facts)} facts, types={types_found}")

    print(f"\nResults: {passed}/{total} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    print("Memory Oracle — Capture Pattern Tests\n")
    success = run_tests(verbose)
    sys.exit(0 if success else 1)
