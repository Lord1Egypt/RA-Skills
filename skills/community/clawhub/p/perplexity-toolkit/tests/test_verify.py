"""Tests for verify module — source verification and answer quality."""
import sys; sys.path.insert(0, "src")

from unittest.mock import patch, MagicMock
from perplexity_toolkit.verify import (
    verify_sources, check_answer_quality, verify_result,
    generate_verification_prompt, generate_cross_check_queries,
)


class TestVerifySources:
    def test_empty_list(self):
        result = verify_sources([])
        assert result == {"total": 0, "valid": 0, "broken": 0, "broken_urls": []}

    @patch("perplexity_toolkit.verify.urllib.request.urlopen")
    def test_all_valid(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        sources = [{"text": "A", "href": "https://example.com"}, {"text": "B", "href": "https://test.com"}]
        result = verify_sources(sources)
        assert result["total"] == 2
        assert result["valid"] == 2
        assert result["broken"] == 0

    @patch("perplexity_toolkit.verify.urllib.request.urlopen")
    def test_some_broken(self, mock_urlopen):
        def side_effect(req, **kwargs):
            if "broken" in req.full_url:
                raise Exception("404")
            resp = MagicMock()
            resp.status = 200
            resp.__enter__ = MagicMock(return_value=resp)
            resp.__exit__ = MagicMock(return_value=False)
            return resp
        mock_urlopen.side_effect = side_effect

        sources = [
            {"text": "Good", "href": "https://good.com"},
            {"text": "Bad", "href": "https://broken.com"},
        ]
        result = verify_sources(sources)
        assert result["total"] == 2
        assert result["valid"] == 1
        assert result["broken"] == 1
        assert len(result["broken_urls"]) == 1


class TestCheckAnswerQuality:
    def test_empty_answer(self):
        result = check_answer_quality("", [])
        assert result["score"] == 0
        assert "Empty answer" in result["issues"]
        assert result["needs_verification"] is True

    def test_short_answer(self):
        result = check_answer_quality("Short.", [{"text": "s", "href": "https://x.com"}])
        assert result["score"] < 100
        assert any("short" in i.lower() for i in result["issues"])

    def test_good_answer(self):
        answer = "Python is a programming language. " * 10
        sources = [{"text": "s", "href": "https://x.com"}]
        result = check_answer_quality(answer, sources)
        assert result["score"] == 100
        assert result["issues"] == []
        assert result["needs_verification"] is False

    def test_hedging_language(self):
        answer = "I could not find specific data. I'm not sure about this. I apologize for the limited information. The answer may not be accurate."
        result = check_answer_quality(answer, [{"text": "s", "href": "https://x.com"}])
        assert result["score"] < 100
        assert any("hedging" in i.lower() for i in result["issues"])

    def test_no_sources(self):
        answer = "A good answer without sources. " * 5
        result = check_answer_quality(answer, [])
        assert result["score"] < 100
        assert any("no sources" in i.lower() for i in result["issues"])


class TestVerifyResult:
    def test_adds_quality_field(self):
        result = {"answer": "Test " * 20, "sources": [{"text": "s", "href": "https://x.com"}]}
        verified = verify_result(result, verify_urls=False)
        assert "quality" in verified
        assert "answer_check" in verified["quality"]
        assert "verdict" in verified["quality"]


class TestGeneratePrompts:
    def test_verification_prompt(self):
        prompt = generate_verification_prompt("test answer", "test query")
        assert "验证" in prompt
        assert "test query" in prompt

    def test_cross_check_queries(self):
        queries = generate_cross_check_queries("query", "answer with 2024 data.")
        assert len(queries) >= 1
        assert any("验证" in q or "错误" in q for q in queries)
