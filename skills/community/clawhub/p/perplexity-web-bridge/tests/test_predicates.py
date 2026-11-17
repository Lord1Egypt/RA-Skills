# tests/test_predicates.py
from jev_webbridge.predicates import get_predicate


def test_generic_is_default_for_unknown_site():
    p = get_predicate("some-random-site")
    assert p["name"] == "generic" and p["why_override"] is None
    assert p["cap_ms"] == 2000 and p["poll_ms"] == 100

def test_github_uses_generic_with_navigation_cap_only():
    p = get_predicate("github")
    assert p["name"] == "generic"
    assert p["cap_ms"] == 500

def test_perplexity_override_documents_why_generic_fails():
    p = get_predicate("perplexity")
    assert p["why_override"] and len(p["why_override"]) < 200
    assert "icon" in p["probe_js"]

def test_stability_needs_500ms_gap_not_consecutive_polls():
    from jev_webbridge.predicates.generic import is_stable
    # samples: (value, age_ms)
    assert is_stable([(10, 900), (10, 400)]) is True     # same value, older sample ≥500ms ago
    assert is_stable([(10, 100), (10, 50)]) is False     # too close together
    assert is_stable([(10, 900), (12, 400)]) is False    # value changed

def test_new_answer_seen_is_required_conjunct():
    from jev_webbridge.predicates.generic import settled
    # baseline 100; equal lengths but never grew -> not settled even if quiet
    assert settled(baseline_len=100, samples=[(100, 900), (100, 400)], quiet_ms=800) is False
    assert settled(baseline_len=100, samples=[(250, 900), (250, 400)], quiet_ms=800) is True

def test_every_override_file_carries_why_comment_constant():
    from jev_webbridge.predicates import perplexity
    assert perplexity.WHY_OVERRIDE


def test_perplexity_post_extract_probe_present_and_file_thin():
    import inspect
    import pathlib

    from jev_webbridge.predicates import perplexity
    p = get_predicate("perplexity")
    assert p.get("post_extract_js"), "post-extract verification probe missing"
    src = pathlib.Path(inspect.getfile(perplexity)).read_text()
    assert len(src.splitlines()) <= 30
