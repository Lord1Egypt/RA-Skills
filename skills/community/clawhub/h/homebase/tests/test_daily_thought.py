"""
test_daily_thought.py — Unit tests for features/briefing/daily_thought.py

Covers:
  - get_daily_thought(): live ZenQuotes success path (formatted quote + author)
  - HTML entities in the quote are unescaped
  - Rate-limit placeholder response is rejected -> fallback
  - Network failure (URLError) -> fallback, never raises
  - Missing quote text -> fallback
  - Output always starts with the header and is non-empty
"""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).parent.parent))

import features.briefing.daily_thought as dt


def make_url_response(payload):
    """Mock context manager matching urllib.request.urlopen()."""
    encoded = json.dumps(payload).encode()
    mock_resp = MagicMock()
    mock_resp.read.return_value = encoded
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = lambda s, *a: False
    return mock_resp


def test_success_path_formats_quote_and_author():
    payload = [{"q": "The best way out is always through.", "a": "Robert Frost",
                "date": "2026-07-21"}]
    with patch("urllib.request.urlopen", return_value=make_url_response(payload)):
        out = dt.get_daily_thought()
    assert out.startswith(dt._HEADER)
    assert "The best way out is always through." in out
    assert "Robert Frost" in out


def test_html_entities_are_unescaped():
    payload = [{"q": "Don&#039;t quit &mdash; keep going.", "a": "Anon"}]
    with patch("urllib.request.urlopen", return_value=make_url_response(payload)):
        line = dt._fetch_zenquotes()
    assert "&#039;" not in line and "&mdash;" not in line
    assert "Don't quit" in line


def test_rate_limit_placeholder_rejected():
    payload = [{"q": "Too many requests. Obtaining quotes per day...", "a": "zenquotes.io"}]
    with patch("urllib.request.urlopen", return_value=make_url_response(payload)):
        assert dt._fetch_zenquotes() is None


def test_network_failure_falls_back_and_never_raises():
    with patch("urllib.request.urlopen", side_effect=URLError("down")):
        assert dt._fetch_zenquotes() is None
        out = dt.get_daily_thought()  # must not raise
    assert out.startswith(dt._HEADER)
    body = out.split("\n", 1)[1]
    assert body in dt._FALLBACK_POOL


def test_missing_quote_text_falls_back():
    with patch("urllib.request.urlopen", return_value=make_url_response([{"q": "", "a": "X"}])):
        assert dt._fetch_zenquotes() is None


def test_output_always_has_header_and_body():
    payload = [{"q": "Progress, not perfection.", "a": "Anon"}]
    with patch("urllib.request.urlopen", return_value=make_url_response(payload)):
        out = dt.get_daily_thought()
    assert out.startswith(dt._HEADER)
    assert len(out.split("\n", 1)[1].strip()) > 0
