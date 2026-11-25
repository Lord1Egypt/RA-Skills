#!/usr/bin/env python3
"""Regression tests for the min_len=4 defect in name_tokens.

Root cause: name tokens shorter than 4 chars were silently dropped, so
"Rhea Ott" vs "Rhea Ott" — two identical strings — scored 1 shared token
instead of 2 and fell below the corroboration threshold. Measured at 14.4%
of the live contact store, skewed heavily toward East Asian surnames
(Lee, Liu, Kim, Wu, Ng, Xu, Li, Ngo, Ho, Oh, Das).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _normalize import name_tokens, token_overlap_ratio


def _shared(a, b):
    return token_overlap_ratio(a, b)[1]


# ── the reported defect ───────────────────────────────────────────────────

def test_identical_short_surname_scores_full_match():
    assert _shared("Rhea Ott", "Rhea Ott") == 2, "identical names must fully agree"
    assert _shared("Rhea Ott", "RHEA OTT") == 2, "matching is case-insensitive"


def test_common_short_surnames_participate():
    for full in ["Milo Ng", "Nora Li", "Felix Wu", "Paula Ho",
                 "Sabine Lee", "Otto Liu", "Hugo Kim", "Tao Xu",
                 "Bruno Ngo", "Ravi Das", "Yuna Oh"]:
        assert _shared(full, full) == 2, f"{full!r} should score 2, got {_shared(full, full)}"


def test_short_given_names_participate():
    assert _shared("Ada Quill", "Ada Quill") == 2
    assert _shared("Ray Bexley", "Ray Bexley") == 2
    assert _shared("Ivy Tran", "Ivy Tran") == 2


def test_middle_name_still_matches():
    assert _shared("Wren Keeley", "Wren Jane Keeley") == 2


# ── guards: the fix must not manufacture agreement ────────────────────────

def test_particles_never_corroborate():
    # Two unrelated Dutch names share only "VAN" — must not count.
    assert _shared("Jan van Dijk", "Piet van Gogh") == 0
    assert _shared("Ana de Silva", "Maria de Souza") == 0
    assert "VAN" not in name_tokens("Jan van Dijk")
    assert "DE" not in name_tokens("Ana de Silva")


def test_single_initials_excluded():
    assert "J" not in name_tokens("J Smith")
    assert _shared("J Smith", "J Brown") == 0, "initials must not corroborate"


def test_different_people_do_not_match():
    assert _shared("Rhea Ott", "Marcus Doyle") == 0
    assert _shared("Nora Li", "Nora Wu") == 1, "given name only"
    assert _shared("Milo Ng", "Iris Ng") == 1, "surname only"


def test_surname_only_is_not_full_agreement():
    # This is what the >=2 corroboration gate depends on staying true.
    assert _shared("Sabine Lee", "Rafael Lee") == 1


def test_suffixes_still_stripped():
    assert _shared("Jane Roe PhD", "Jane Roe") == 2
    assert "PHD" not in name_tokens("Jane Roe PhD")


def test_empty_and_none_safe():
    assert name_tokens(None) == set()
    assert name_tokens("") == set()
    assert _shared(None, "Rhea Ott") == 0


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for n, f in tests:
        try:
            f()
            print(f"PASS {n}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {n}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR {n}: {type(e).__name__}: {e}")
    print(f"\n{len(tests)-failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
