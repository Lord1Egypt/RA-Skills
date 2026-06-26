"""
Test suite for i18n_processor.
Run: python3 tests/test_processor.py

Tests are organized by language and cover:
- Diacritics fixes
- Stray character removal
- Common typos
- Edge cases (no-change scenarios)
"""

import sys
import os

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from i18n_processor import process


def run_tests():
    """Run all tests and report results."""
    results = []

    # ====================
    # ROMANIAN TESTS
    # ====================

    # Diacritics tests
    results.append(test(
        "RO: stiu → știu",
        lambda: process("eu stiu", "ro"),
        "eu știu"
    ))

    results.append(test(
        "RO: si conjunction → și",
        lambda: process("el si ea", "ro"),
        "el și ea"
    ))

    results.append(test(
        "RO: stii → știi",
        lambda: process("tu stii", "ro"),
        "tu știi"
    ))

    results.append(test(
        "RO: vrau → vreau",
        lambda: process("eu vrau sa plec", "ro"),
        "eu vreau să plec"
    ))

    results.append(test(
        "RO: invata → învăța",
        lambda: process("el invata", "ro"),
        "el învăța"
    ))

    results.append(test(
        "RO: trebuie să (subjunctive)",
        lambda: process("trebuie sa fac asta", "ro"),
        "trebuie să fac asta"
    ))

    results.append(test(
        "RO: in preposition → în",
        lambda: process("am fost in oras", "ro"),
        "am fost în oraș"
    ))

    results.append(test(
        "RO: ii pronoun",
        lambda: process("le spui ii adevarul", "ro"),
        "le spui îi adevărul"
    ))

    # Stray character removal
    results.append(test(
        "RO: stray Chinese chars removed",
        lambda: process("Bună理论 ziua", "ro"),
        "Bună ziua"
    ))

    results.append(test(
        "RO: stray Cyrillic removed",
        lambda: process("salutСчёт мир", "ro"),
        "salut мир"
    ))

    # No-change scenarios (should NOT modify)
    results.append(test_no_change(
        "RO: already correct text — no change",
        "Bună ziua! Cum ai dormit?",
        "ro"
    ))

    results.append(test_no_change(
        "RO: proper Romanian diacritics preserved",
        "țăran, șoarece, împreună, român",
        "ro"
    ))

    # ====================
    # GERMAN TESTS
    # ====================

    results.append(test(
        "DE: Mueller → Müller",
        lambda: process("Herr Mueller", "de"),
        "Herr Müller"
    ))

    results.append(test(
        "DE: Uber → Über",
        lambda: process("das ist uber", "de"),
        "das ist über"
    ))

    results.append(test(
        "DE: konnen → können",
        lambda: process("ich konnen das", "de"),
        "ich können das"
    ))

    results.append(test(
        "DE: fur → für",
        lambda: process("das ist fur dich", "de"),
        "das ist für dich"
    ))

    results.append(test(
        "DE: schon → schön (when pattern matches)",
        lambda: process("das ist schon", "de"),
        "das ist schön"
    ))

    results.append(test(
        "DE: Strasse → Straße",
        lambda: process("Hauptstrasse", "de"),
        "Hauptstraße"
    ))

    results.append(test(
        "DE: Munchen → München",
        lambda: process("Willkommen in Munchen", "de"),
        "Willkommen in München"
    ))

    # No-change scenarios for German
    results.append(test_no_change(
        "DE: already correct text — no change",
        "Guten Tag! Wie geht es Ihnen?",
        "de"
    ))

    results.append(test_no_change(
        "DE: proper German umlauts preserved",
        "Müller, Über, groß, Straße, München",
        "de"
    ))

    # ====================
    # ENGLISH TESTS
    # ====================

    results.append(test(
        "EN: passthrough — no changes",
        lambda: process("Hello world", "en"),
        "Hello world"
    ))

    results.append(test(
        "EN: whitespace normalization",
        lambda: process("Hello    world", "en"),
        "Hello world"
    ))

    # ====================
    # BASE RULES TESTS
    # ====================

    results.append(test(
        "BASE: double spaces normalized",
        lambda: process("Hello    world", "ro"),
        "Hello world"
    ))

    results.append(test(
        "BASE: trailing whitespace removed",
        lambda: process("Hello world   ", "ro"),
        "Hello world"
    ))

    results.append(test(
        "BASE: leading whitespace removed",
        lambda: process("   Hello world", "ro"),
        "Hello world"
    ))

    # ====================
    # REPORT
    # ====================

    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)

    passed = 0
    failed = 0

    for name, input_text, expected, actual, ok in results:
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"\n{'FAIL':5} {name}")
            print(f"       Input:    {input_text}")
            print(f"       Expected: {expected}")
            print(f"       Got:      {actual}")
        print(f"  {'PASS' if ok else 'FAIL':5} {name}")

    print("\n" + "=" * 50)
    print(f"Total: {passed}/{passed + failed} passed")
    print("=" * 50)

    return failed == 0


def test(name: str, fn, expected: str):
    """Run a single test with a lambda function."""
    actual = fn()
    ok = actual == expected
    return (name, None, expected, actual, ok)


def test_no_change(name: str, text: str, lang: str):
    """Test that text is not modified."""
    actual = process(text, lang)
    ok = actual == text
    return (name, text, text, actual, ok)


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
