from governed_agents.profiles import TASK_PROFILES, get_profile
from governed_agents.structural_gate import run_structural_gate
from governed_agents.grounding_gate import run_grounding_gate, _check_url
from governed_agents.verification import run_non_coding_verification
from governed_agents.contract import TaskContract


# ── Profiles ──────────────────────────────────────────────────────────

def test_all_task_types_present():
    for t in ["research", "analysis", "strategy", "writing", "planning", "custom"]:
        p = get_profile(t)
        assert "structural_checks" in p
        assert "grounding_checks" in p


def test_unknown_type_falls_back_to_custom():
    p = get_profile("totally_unknown")
    assert p == TASK_PROFILES["custom"]


def test_research_profile_has_url_check():
    p = get_profile("research")
    assert "url_reachable" in p["grounding_checks"]
    assert "sources_list" in p["structural_checks"]


# ── Structural Gate ───────────────────────────────────────────────────

def test_structural_word_count_fail():
    profile = {"structural_checks": ["word_count"], "min_word_count": 100, "required_sections": []}
    result = run_structural_gate("too short", profile)
    assert result.passed is False
    assert any("word_count" in f for f in result.failures)


def test_structural_word_count_pass():
    profile = {"structural_checks": ["word_count"], "min_word_count": 5, "required_sections": []}
    result = run_structural_gate("one two three four five six", profile)
    assert result.passed is True


def test_structural_required_sections_fail():
    profile = {"structural_checks": ["required_sections"], "min_word_count": 0, "required_sections": ["summary", "conclusion"]}
    result = run_structural_gate("just some text", profile)
    assert result.passed is False
    assert any("summary" in f or "conclusion" in f for f in result.failures)


def test_structural_required_sections_pass():
    profile = {"structural_checks": ["required_sections"], "min_word_count": 0, "required_sections": ["summary"]}
    result = run_structural_gate("Summary: blah blah blah conclusion here", profile)
    assert result.passed is True


def test_structural_sources_list_fail():
    profile = {"structural_checks": ["sources_list"], "min_word_count": 0, "required_sections": []}
    result = run_structural_gate("No URLs or references anywhere", profile)
    assert result.passed is False


def test_structural_sources_list_pass():
    profile = {"structural_checks": ["sources_list"], "min_word_count": 0, "required_sections": []}
    result = run_structural_gate("References:\n- https://example.com\n- https://arxiv.org", profile)
    assert result.passed is True


def test_structural_has_steps_pass():
    profile = {"structural_checks": ["has_steps"], "min_word_count": 0, "required_sections": []}
    result = run_structural_gate("Plan:\n1. First step\n2. Second step", profile)
    assert result.passed is True


# ── Grounding Gate ────────────────────────────────────────────────────

def test_grounding_citations_fail():
    profile = {"grounding_checks": ["citations_present"]}
    result = run_grounding_gate("No citations in this text at all.", profile)
    assert result.passed is False


def test_grounding_citations_pass_et_al():
    profile = {"grounding_checks": ["citations_present"]}
    result = run_grounding_gate("According to Smith et al. (2024) this is proven.", profile)
    assert result.passed is True


def test_grounding_unknown_check_skipped():
    profile = {"grounding_checks": ["completely_unknown_check"]}
    result = run_grounding_gate("anything", profile)
    assert result.passed is True


def test_grounding_warnings_dont_fail():
    profile = {"grounding_checks": ["dates_valid"]}
    result = run_grounding_gate("This happened on 2010-01-01 long ago.", profile)
    assert result.passed is True  # warning only, not failure
    assert len(result.warnings) > 0


def test_ssrf_internal_ip_rejected():
    payload = "169.254.169.254/metadata"
    assert _check_url(payload) is False


# ── Verification Pipeline ─────────────────────────────────────────────

def test_pipeline_structural_short_circuit():
    contract = TaskContract(task_type="research", verification_mode="council")
    result = run_non_coding_verification("short", contract)
    assert result.passed is False
    assert result.layer_failed == "structural"
    assert result.needs_council is False


def test_pipeline_custom_skips_gates():
    contract = TaskContract(task_type="custom", verification_mode="council")
    result = run_non_coding_verification("anything at all", contract)
    assert result.passed is True
    assert result.needs_council is True


def test_pipeline_writing_good_output_passes():
    contract = TaskContract(task_type="writing", verification_mode="council")
    output = " ".join(["word"] * 100)
    result = run_non_coding_verification(output, contract)
    assert result.passed is True
    assert result.needs_council is True
