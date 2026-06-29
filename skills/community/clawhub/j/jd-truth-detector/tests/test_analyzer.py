from scripts.analyzer import run_analysis

def test_analyzer_jargon(jd_red_flag, stub_llm):
    stats = {"red_flag_keywords": {"抗压": 3}, "structure": {}, "length": 500}
    result = run_analysis(jd_red_flag, None, stats, stub_llm)
    assert "jargon" in result
    assert isinstance(result["jargon"], list)
    assert len(stub_llm.calls) == 3  # jargon, culture, negotiation (no resume)

def test_analyzer_with_resume(jd_clean, resume_match, stub_llm):
    stats = {"red_flag_keywords": {}, "structure": {}, "length": 500}
    result = run_analysis(jd_clean, resume_match, stats, stub_llm)
    assert result["resume_match"] is not None
    assert result["resume_match"]["match_score"] > 70
    assert len(stub_llm.calls) == 4  # all 4 calls

def test_analyzer_without_resume(jd_clean, stub_llm):
    stats = {"red_flag_keywords": {}, "structure": {}, "length": 500}
    result = run_analysis(jd_clean, None, stats, stub_llm)
    assert result["resume_match"] is None
