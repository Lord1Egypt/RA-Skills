"""Tests for memo-based cross-day dedup logic."""
import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest


# --- helper copied from pipeline (to test in isolation before refactor) ---

def extract_urls_from_memo(path: Path) -> set[str]:
    """Extract all markdown link URLs from a memo file."""
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r'\[.*?\]\((https?://[^\)]+)\)', text))


def get_shown_urls(memo_dir: Path, lookback_days: int) -> set[str]:
    """Collect URLs from the last N days of memo files."""
    shown: set[str] = set()
    today = datetime.now().date()
    for i in range(1, lookback_days + 1):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        memo_path = memo_dir / f"{date_str}.md"
        shown |= extract_urls_from_memo(memo_path)
    return shown


# --- tests ---

def test_extract_urls_from_memo_basic():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("· **[Some Article](https://example.com/a)** — great post [Blog]\n")
        f.write("· **[@handle](https://x.com/handle/123)** — opinion [X]\n")
        path = Path(f.name)
    result = extract_urls_from_memo(path)
    assert "https://example.com/a" in result
    assert "https://x.com/handle/123" in result
    path.unlink()


def test_extract_urls_from_memo_missing_file():
    result = extract_urls_from_memo(Path("/nonexistent/path/2099-01-01.md"))
    assert result == set()


def test_extract_urls_no_links():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("# Daily Brief\nNo links here, just plain text.\n")
        path = Path(f.name)
    result = extract_urls_from_memo(path)
    assert result == set()
    path.unlink()


def test_get_shown_urls_empty_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        shown = get_shown_urls(Path(tmpdir), lookback_days=7)
    assert shown == set()


def test_get_shown_urls_collects_from_multiple_days():
    with tempfile.TemporaryDirectory() as tmpdir:
        memo_dir = Path(tmpdir)
        today = datetime.now().date()
        # Write memo for yesterday and 2 days ago
        for i in [1, 2]:
            date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            (memo_dir / f"{date_str}.md").write_text(
                f"· **[Article {i}](https://example.com/{i})** — blah [Blog]\n"
            )
        shown = get_shown_urls(memo_dir, lookback_days=7)
    assert "https://example.com/1" in shown
    assert "https://example.com/2" in shown
    assert "https://example.com/3" not in shown


# ---------------------------------------------------------------------------
# AnthropicNewsSource tests (offline, uses mocked HTML)
# ---------------------------------------------------------------------------

from unittest.mock import patch, MagicMock


ANTHROPIC_HTML_FIXTURE = """
<html><body>
  <div>
    <a href="/news/claude-sonnet-4-6">
      <p>Feb 17, 2026</p>
      <p>Product</p>
      <h3>Introducing Claude Sonnet 4.6</h3>
    </a>
    <a href="/news/alignment-faking">
      <p>Dec 20, 2025</p>
      <p>Research</p>
      <h3>Alignment faking in large language models</h3>
    </a>
    <a href="/news/claude-is-a-space-to-think">
      <p>Feb 4, 2026</p>
      <p>Announcements</p>
      <h3>Claude is a space to think</h3>
    </a>
    <a href="/about">Not a news article</a>
  </div>
</body></html>
"""


def test_anthropic_returns_feed_items():
    """fetch() returns FeedItem objects for /news/ links."""
    from src.sources.anthropic_news import AnthropicNewsSource
    mock_resp = MagicMock()
    mock_resp.text = ANTHROPIC_HTML_FIXTURE
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        source = AnthropicNewsSource(name="anthropic-news", config={"max_items": 10, "tags": ["ai", "anthropic"]})
        items = source.fetch()

    assert len(items) >= 1
    urls = [item.url for item in items]
    assert "https://www.anthropic.com/news/claude-sonnet-4-6" in urls


def test_anthropic_filters_non_news_links():
    """Links not starting with /news/ are excluded."""
    from src.sources.anthropic_news import AnthropicNewsSource
    mock_resp = MagicMock()
    mock_resp.text = ANTHROPIC_HTML_FIXTURE
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        source = AnthropicNewsSource(name="anthropic-news", config={"max_items": 10, "tags": []})
        items = source.fetch()

    urls = [item.url for item in items]
    assert "https://www.anthropic.com/about" not in urls


def test_anthropic_filters_research_keeps_product_and_announcements():
    """Research articles are filtered out; Product and Announcements are kept."""
    from src.sources.anthropic_news import AnthropicNewsSource
    mock_resp = MagicMock()
    mock_resp.text = ANTHROPIC_HTML_FIXTURE
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        source = AnthropicNewsSource(name="anthropic-news", config={"max_items": 10, "tags": []})
        items = source.fetch()

    urls = [item.url for item in items]
    assert "https://www.anthropic.com/news/claude-sonnet-4-6" in urls
    assert "https://www.anthropic.com/news/claude-is-a-space-to-think" in urls
    assert "https://www.anthropic.com/news/alignment-faking" not in urls


def test_anthropic_respects_max_items():
    """max_items config caps the number of returned items."""
    from src.sources.anthropic_news import AnthropicNewsSource
    mock_resp = MagicMock()
    mock_resp.text = ANTHROPIC_HTML_FIXTURE
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        source = AnthropicNewsSource(name="anthropic-news", config={"max_items": 1, "tags": []})
        items = source.fetch()

    assert len(items) <= 1


def test_anthropic_network_error_returns_empty():
    """On network failure, fetch() returns [] instead of raising."""
    from src.sources.anthropic_news import AnthropicNewsSource
    with patch("requests.get", side_effect=Exception("network error")):
        source = AnthropicNewsSource(name="anthropic-news", config={"max_items": 10, "tags": []})
        items = source.fetch()

    assert items == []
