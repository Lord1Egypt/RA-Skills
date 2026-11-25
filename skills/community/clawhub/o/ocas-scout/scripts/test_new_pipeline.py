#!/usr/bin/env python3
"""Regression tests for the Aliens Eye integration scripts.

Run: python3 test_new_pipeline.py
"""
import csv
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── profile_extract: botwall → name_from_profile false ──────────

def test_botwall_no_structured_name():
    from profile_extract import extract_profile
    bad = ("<!doctype html><html><head>"
           "<title>Just a moment...</title>"
           "<meta name='description' content='Checking your browser'>"
           "</head><body></body></html>")
    p = extract_profile(bad, "generic", "https://example.com/x")
    assert p["name_from_profile"] is False, "botwall title must not be a structured name"

# ── profile_extract: OpenGraph yields structured name ───────────

def test_extract_og_profile():
    from profile_extract import extract_profile
    html = ("<!doctype html><html><head>"
            "<title>Someone Smith · GitHub</title>"
            "<meta property='og:title' content='Someone Smith'>"
            "<meta property='og:description' content='Builder of things'>"
            "<meta property='og:image' content='https://example.com/av.png'>"
            "</head><body>Hi</body></html>")
    p = extract_profile(html, "github", "https://github.com/s")
    assert p["name"] == "Someone Smith"
    assert p["name_from_profile"] is True
    assert p["bio"] == "Builder of things"
    assert p["avatar"] == "https://example.com/av.png"
    assert p["sources"]["name"] == "og"

# ── correlation: two same-person profiles cluster ────────────────

def test_correlation_clusters_same_person():
    from correlate_profiles import correlate
    profiles = [
        {"site": "a", "url": "https://a.example", "avatar": "", "name": "Someone",
         "raw_name": "Someone",
         "bio": "Builder. https://example.org/mylink @mirrorhandle",
         "links": {"https://example.org/mylink"},
         "handles": {"mirrorhandle"}, "status": "Found", "avatar_hash": None},
        {"site": "b", "url": "https://b.example", "avatar": "", "name": "Someone",
         "raw_name": "Someone",
         "bio": "Builder. https://example.org/mylink @mirrorhandle",
         "links": {"https://example.org/mylink"},
         "handles": {"mirrorhandle"}, "status": "Found", "avatar_hash": None},
        {"site": "c", "url": "https://c.example", "avatar": "", "name": "Other",
         "raw_name": "Other",
         "bio": "Totally different person writing about databases.",
         "links": set(), "handles": set(), "status": "Found",
         "avatar_hash": None},
    ]
    res = correlate(profiles, fetch_avatars=False)
    assert len(res["clusters"]) == 1, "expected one cluster"
    cluster = res["clusters"][0]
    assert cluster["size"] == 2
    assert cluster["strength"] in ("high", "medium")
    assert "link" in cluster["signals"] or "name" in cluster["signals"]

# ── expansion: handles mined from bios ───────────────────────────

def test_expansion_mines_handles():
    from recurse_expand import expand
    data = {
        "profiles": [
            {"site": "github", "bio": "Builder @oldhandle also "
             "https://twitter.com/onetw and https://github.com/secondhandle"},
            {"site": "twitter", "bio": "Builder @oldhandle and "
             "https://github.com/secondhandle"},
        ]
    }
    res = expand(data, current_pass=1, known={"oldhandle"})
    handles = {c["handle"] for c in res["candidates"]}
    assert "secondhandle" in handles
    second = [c for c in res["candidates"] if c["handle"] == "secondhandle"][0]
    assert second["corroborated"] is True
    assert second["pass"] == 2

# ── expansion: cap at two passes ─────────────────────────────────

def test_expansion_cap_enforced():
    from recurse_expand import expand
    res = expand({}, current_pass=2)
    assert res["refused"] is True
    assert "recursion cap" in res.get("reason", "").lower()

# ── expansion: bio-less profiles yield nothing ──────────────────

def test_expansion_no_bios():
    from recurse_expand import expand
    res = expand({"profiles": [{"site": "x", "bio": ""},
                               {"site": "y", "bio": ""}]},
                  current_pass=1)
    assert not res["candidates"]

# ── domain check: label reduction ────────────────────────────────

def test_domain_label_reduces():
    from domain_check import domain_label
    # Underscore becomes a hyphen (both are valid DNS label chars);
    # underscores are not legal in DNS labels so the hyphen form is the safe choice.
    assert domain_label("someone_name") == "someone-name"
    assert domain_label("Someone") == "someone"
    assert domain_label("a" * 100) == "a" * 63  # capped at 63

# ── reliability: real metrics from a tiny corpus ─────────────────

def test_reliability_metrics():
    from source_reliability import score
    rows = [
        {"tool": "t", "site": "s", "predicted": True, "actual": True},
        {"tool": "t", "site": "s", "predicted": True, "actual": True},
        {"tool": "t", "site": "s", "predicted": True, "actual": False},
        {"tool": "t", "site": "s", "predicted": False, "actual": True},
    ]
    res = score(rows, min_n=1)
    m = res["tools"]["t"]
    assert m["tp"] == 2
    assert m["fp"] == 1
    assert m["fn"] == 1
    assert m["tn"] == 0
    assert abs(m["precision"] - 0.667) < 0.01
    assert abs(m["recall"] - 0.667) < 0.01

# ── reliability: empty corpus rejected ───────────────────────────

def test_reliability_empty():
    from source_reliability import score
    res = score([], min_n=1)
    assert res["labeled_observations"] == 0
    assert not res["tools"]

# ── entity resolution: exact, fuzzy, and token_overlap match ─────

def test_entity_resolution_matching():
    from entity_resolution import resolve

    left_rows = [
        {"name": "John Alexander Smith"},   # Exact & token_overlap match with right_rows[0]
        {"name": "Alice Williams"},         # Fuzzy match with right_rows[1] ("Williams Alice")
        {"name": "Robert James Johnson"},   # Token overlap with right_rows[2] ("Robert Johnson")
        {"name": "Unique Name Person"},     # No match
    ]
    right_rows = [
        {"fullname": "John Alexander Smith"},
        {"fullname": "Williams Alice"},
        {"fullname": "Robert Johnson"},
        {"fullname": "Unrelated Stranger"},
    ]

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="") as f_left, \
         tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="") as f_right, \
         tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="") as f_out:

        writer_left = csv.DictWriter(f_left, fieldnames=["name"])
        writer_left.writeheader()
        writer_left.writerows(left_rows)
        f_left.close()

        writer_right = csv.DictWriter(f_right, fieldnames=["fullname"])
        writer_right.writeheader()
        writer_right.writerows(right_rows)
        f_right.close()

        out_path = f_out.name
        f_out.close()

        try:
            count = resolve(
                left_path=f_left.name,
                left_col="name",
                right_path=f_right.name,
                right_col="fullname",
                out_path=out_path,
                overlap_threshold=0.5,
                min_shared=2,
            )
            assert count >= 3

            with open(out_path, newline="", encoding="utf-8") as fh:
                matches = list(csv.DictReader(fh))

            types = [m["match_type"] for m in matches]
            assert "exact" in types
            assert "fuzzy" in types
            assert "token_overlap" in types
        finally:
            os.unlink(f_left.name)
            os.unlink(f_right.name)
            os.unlink(out_path)

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
