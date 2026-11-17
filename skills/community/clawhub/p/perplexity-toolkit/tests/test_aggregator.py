"""Tests for perplexity_toolkit.aggregator."""

from perplexity_toolkit.aggregator import (
    aggregate,
    _dedup_sources,
    _extract_key_facts,
    to_markdown,
)


def _result(query="q", answer="", sources=None, follow_ups=None, mode="search", error=None):
    r = {
        "query": query,
        "answer": answer,
        "sources": sources or [],
        "url": "https://www.perplexity.ai/search/x",
        "title": "title",
        "follow_ups": follow_ups or [],
        "mode": mode,
    }
    if error:
        r["error"] = error
    return r


SRC = [
    {"text": "Example source one", "href": "https://example.com/a"},
    {"text": "Example source two", "href": "https://example.com/b?x=1"},
    {"text": "Example source one again", "href": "https://example.com/a/"},
    {"text": "No href", "href": ""},
]


class TestAggregate:
    def test_counts_modes_and_errors(self):
        results = [
            _result(
                query="q1",
                answer="Answer one for q1 that is fairly long indeed.",
                sources=SRC[:2],
                follow_ups=["f1", "f2"],
                mode="search",
            ),
            _result(
                query="q2",
                answer="Answer two for q2 that is fairly long indeed.",
                sources=SRC[2:4],
                follow_ups=["f2", "f3"],
                mode="deep_research",
            ),
            _result(query="q3", error="network boom"),
        ]
        report = aggregate(results)

        assert report["total_searches"] == 3
        assert report["successful"] == 2
        assert report["errors"] == 1
        # /a and /a/ normalize to the same URL → 2 unique sources, one cited twice
        assert report["unique_sources"] == 2
        assert report["modes_used"] == {"search": 2, "deep_research": 1}
        assert report["top_sources"][0]["cited_count"] == 2
        # follow-ups deduped across results, order preserved
        assert report["follow_up_questions"] == ["f1", "f2", "f3"]
        assert len(report["queries"]) == 3
        assert report["queries"][2]["answer_len"] == 0
        assert report["queries"][2]["sources_count"] == 0

    def test_empty_results(self):
        report = aggregate([])
        assert report["total_searches"] == 0
        assert report["successful"] == 0
        assert report["errors"] == 0
        assert report["modes_used"] == {}
        assert report["unique_sources"] == 0
        assert report["queries"] == []


class TestDedupSources:
    def test_normalizes_urls_and_merges_variants(self):
        results = [
            _result(sources=[
                {"text": "A", "href": "https://example.com/a"},
                {"text": "B", "href": "https://example.com/b?utm_source=x"},
                {"text": "Empty", "href": ""},
            ]),
            _result(sources=[{"text": "A2", "href": "https://example.com/a/"}]),
        ]
        out = _dedup_sources(results)
        assert len(out) == 2
        by_url = {s["url"]: s for s in out}
        assert by_url["https://example.com/a"]["cited_count"] == 2
        assert by_url["https://example.com/b?utm_source=x"]["cited_count"] == 1

    def test_sorts_by_citation_count_desc(self):
        results = [
            _result(sources=[{"text": "A", "href": "https://example.com/a"}]),
            _result(sources=[
                {"text": "B", "href": "https://example.com/b"},
                {"text": "B2", "href": "https://example.com/b/"},
            ]),
        ]
        out = _dedup_sources(results)
        assert out[0]["url"] == "https://example.com/b"
        assert out[0]["cited_count"] == 2
        assert out[1]["cited_count"] == 1

    def test_truncates_text_to_150_chars(self):
        results = [_result(sources=[{"text": "x" * 200, "href": "https://example.com/a"}])]
        out = _dedup_sources(results)
        assert len(out[0]["text"]) == 150

    def test_ignores_empty_hrefs_and_empty_sources(self):
        assert _dedup_sources([_result()]) == []
        assert _dedup_sources([_result(sources=[{"text": "no", "href": ""}])]) == []


class TestExtractKeyFacts:
    def test_filters_skip_lines_and_takes_first_hit(self):
        results = [_result(
            query="What is X",
            answer="答案详细如下\n"
                    "This is the first substantial fact about the topic under discussion here.\n"
                    "Second line should be ignored because we break after the first hit.",
        )]
        assert _extract_key_facts(results) == [
            "This is the first substantial fact about the topic under discussion here."
        ]

    def test_skips_query_prefix_short_lines_and_urls(self):
        answer = (
            "What is X — here is a full explanation that starts with the query and is long.\n"
            "Short.\n"
            "https://example.com/plain link text that is long enough but starts with http\n"
            "A valid fact that is definitely longer than forty characters total.\n"
        )
        assert _extract_key_facts([_result(query="What is X", answer=answer)]) == [
            "A valid fact that is definitely longer than forty characters total."
        ]

    def test_skips_lines_starting_with_skip_terms(self):
        answer = (
            "链接如下\n"
            "视频内容很长但其实这是第一段足够长的文字超过四十个字符了\n"
            "A real fact that is definitely longer than forty characters in length.\n"
        )
        assert _extract_key_facts([_result(answer=answer)]) == [
            "A real fact that is definitely longer than forty characters in length."
        ]

    def test_truncates_to_300_chars(self):
        facts = _extract_key_facts([_result(answer="A" * 400)])
        assert len(facts) == 1 and len(facts[0]) == 300

    def test_empty_or_skip_only_answer_yields_nothing(self):
        assert _extract_key_facts([_result(answer="")]) == []
        assert _extract_key_facts([_result(answer="答案")]) == []


class TestToMarkdown:
    def test_output_format(self):
        report = {
            "total_searches": 3,
            "successful": 2,
            "errors": 1,
            "modes_used": {"search": 2, "deep_research": 1},
            "unique_sources": 2,
            "top_sources": [
                {"url": "https://example.com/a", "text": "Example text",
                 "domain": "example.com", "cited_count": 3},
            ],
            "key_facts": ["fact one", "fact two"],
            "follow_up_questions": ["f1", "f2"],
            "queries": [
                {"query": "q1", "mode": "search", "url": "",
                 "answer_len": 5, "sources_count": 2},
            ],
        }
        md = to_markdown(report)

        assert md.startswith("# Perplexity Search Report")
        assert "**Total searches:** 3" in md
        assert "**Successful:** 2" in md
        assert "**Errors:** 1" in md
        assert "**Unique sources:** 2" in md
        assert "**Modes used:** search(2), deep_research(1)" in md
        assert "## Top Sources (by citation frequency)" in md
        assert "1. **[example.com](https://example.com/a)** (3x cited) — Example text" in md
        assert "## Key Findings" in md
        assert "1. fact one" in md
        assert "## Suggested Follow-ups" in md
        assert "- f1" in md
        assert "## Query Details" in md
        assert "| q1 | search | 2 | 5 |" in md

    def test_empty_report(self):
        md = to_markdown(aggregate([]))
        assert "# Perplexity Search Report" in md
        assert "**Total searches:** 0" in md