from query_utils import build_intent, clean_natural_query, parse_search_query, parse_tab_query


def test_parse_queries_match_upstream_policy():
    assert parse_search_query("인공지능 AI -광고 -코인") == ("인공지능 AI", ["광고", "코인"])
    assert parse_tab_query("인공지능 AI -광고 -코인") == ("인공지능", ["광고", "코인"])


def test_build_intent_detects_recent_days_and_strips_briefing_words():
    intent = build_intent("최근 3일 반도체 뉴스 브리핑 -광고", limit=7)
    assert intent.search_query == "반도체"
    assert intent.exclude_words == ["광고"]
    assert intent.days == 3
    assert intent.limit == 7


def test_clean_natural_query_handles_sentence_style_korean():
    cleaned = clean_natural_query("삼성전자 관련해서 최근 일주일 핵심 뉴스만 브리핑해줘")
    assert cleaned == "삼성전자"


def test_build_intent_converts_korean_exclude_phrases():
    intent = build_intent("삼성전자 관련해서 증권사 리포트 말고 최근 일주일 핵심만 알려줘")
    assert intent.search_query == "삼성전자"
    assert intent.exclude_words == ["증권사", "리포트"]
    assert intent.days == 7


def test_build_intent_strips_particles_and_dedupes_tokens():
    intent = build_intent("반도체를 반도체 관련 뉴스 찾아줘")
    assert intent.search_query == "반도체"
    assert intent.exclude_words == []
