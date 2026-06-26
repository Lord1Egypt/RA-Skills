"""Tests for utils module formatting and parsing utilities."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
import utils


class TestFormatDatetime:
    """Tests for format_datetime function."""

    def test_format_datetime_with_valid_iso_string(self):
        """Test formatting valid ISO datetime string."""
        result = utils.format_datetime("2026-03-10T14:30:00.000Z")
        assert "2026" in result
        assert "14:30" in result or "2:30" in result  # May vary by locale

    def test_format_datetime_with_none(self):
        """Test formatting None returns '?'."""
        assert utils.format_datetime(None) == "?"

    def test_format_datetime_with_empty_string(self):
        """Test formatting empty string returns '?'."""
        assert utils.format_datetime("") == "?"

    def test_format_datetime_with_invalid_string(self):
        """Test invalid datetime returns input string."""
        invalid = "not-a-date"
        assert utils.format_datetime(invalid) == invalid

    def test_format_datetime_with_z_timezone(self):
        """Test datetime with Z timezone indicator."""
        result = utils.format_datetime("2026-03-03T10:30:00Z")
        assert "10:30" in result or "10:30" in result

    def test_format_datetime_without_milliseconds(self):
        """Test ISO datetime without milliseconds."""
        result = utils.format_datetime("2026-03-03T10:30:00+00:00")
        assert "10:30" in result


class TestParseLocalDatetime:
    """Tests for parse_local_datetime function."""

    def test_parse_iso_format_with_time(self):
        """Test parsing YYYY-MM-DDTHH:MM format."""
        result = utils.parse_local_datetime("2026-03-10T14:30")
        assert result["dateTime"] == "2026-03-10T14:30:00"
        assert result["timeZone"] == "America/New_York"

    def test_parse_with_custom_timezone(self):
        """Test parsing with custom timezone."""
        result = utils.parse_local_datetime("2026-03-10T14:30", "Europe/London")
        assert result["timeZone"] == "Europe/London"

    def test_parse_space_separator(self):
        """Test parsing with space separator instead of T."""
        result = utils.parse_local_datetime("2026-03-10 14:30")
        assert result["dateTime"] == "2026-03-10T14:30:00"

    def test_parse_date_only(self):
        """Test parsing date only defaults to 00:00."""
        result = utils.parse_local_datetime("2026-03-10")
        assert result["dateTime"] == "2026-03-10T00:00:00"

    def test_parse_returns_dict_structure(self):
        """Test that parse returns proper Graph API structure."""
        result = utils.parse_local_datetime("2026-03-10T14:30")
        assert "dateTime" in result
        assert "timeZone" in result
        assert isinstance(result, dict)


class TestStripHtml:
    """Tests for strip_html function."""

    def test_strip_html_simple_tags(self):
        """Test removing simple HTML tags."""
        html = "<p>Hello <b>World</b></p>"
        result = utils.strip_html(html)
        assert result == "Hello World"

    def test_strip_html_with_style_block(self):
        """Test removing style blocks."""
        html = "<style>body { color: red; }</style><p>Content</p>"
        result = utils.strip_html(html)
        assert "color: red" not in result
        assert "Content" in result

    def test_strip_html_preserves_content(self):
        """Test that content is preserved."""
        html = "<div class='container'><span>Test Content</span></div>"
        result = utils.strip_html(html)
        assert "Test Content" in result

    def test_strip_html_cleans_excessive_newlines(self):
        """Test that excessive newlines are cleaned."""
        html = "Line 1\n\n\n\nLine 2"
        result = utils.strip_html(html)
        # Should reduce 4+ newlines to max 2 (double newline)
        assert result.count("\n") <= 2

    def test_strip_html_with_complex_example(self):
        """Test with complex HTML email."""
        html = """
        <style>
            .header { background: blue; }
        </style>
        <div class="header">
            <p>Hello World</p>
        </div>
        <p>Email body</p>
        """
        result = utils.strip_html(html)
        assert "Hello World" in result
        assert "Email body" in result
        assert "<" not in result
        assert ">" not in result

    def test_strip_html_empty_string(self):
        """Test stripping empty string."""
        result = utils.strip_html("")
        assert result == ""

    def test_strip_html_whitespace_cleanup(self):
        """Test that leading/trailing whitespace is cleaned."""
        html = "   <p>Content</p>   "
        result = utils.strip_html(html)
        assert result == "Content"


class TestUtilsIntegration:
    """Integration tests for utils functions."""

    def test_datetime_parse_and_format_roundtrip(self):
        """Test that we can parse and work with dates."""
        # Parse a local datetime
        parsed = utils.parse_local_datetime("2026-03-10T14:30")
        assert parsed["dateTime"] == "2026-03-10T14:30:00"
        
        # Verify it has the right structure for Graph API
        assert "timeZone" in parsed

    def test_format_datetime_various_formats(self):
        """Test format_datetime handles various input formats."""
        test_cases = [
            ("2026-03-03T10:30:00Z", True),  # Should have content
            ("2026-03-03T10:30:00+00:00", True),
            (None, False),  # Should be "?"
            ("", False),  # Should be "?"
        ]
        
        for input_val, should_have_content in test_cases:
            result = utils.format_datetime(input_val)
            if should_have_content:
                assert result != "?"
            else:
                assert result == "?"

    def test_strip_html_email_signature(self):
        """Test stripping HTML from email with signature."""
        html = """
        <p>Hi,</p>
        <p>Here's the update:</p>
        <ul><li>Item 1</li><li>Item 2</li></ul>
        <p>--</p>
        <p>John Doe<br/>john@example.com</p>
        """
        result = utils.strip_html(html)
        assert "Hi" in result
        assert "Item 1" in result
        assert "John Doe" in result
        assert "<" not in result
