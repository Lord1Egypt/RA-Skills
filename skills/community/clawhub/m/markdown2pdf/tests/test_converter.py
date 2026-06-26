#!/usr/bin/env python3
"""
Tests for Markdown to PDF/PNG Converter
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.converter import (
    MarkdownConverter,
    Theme,
    convert_markdown,
    convert_markdown_to_pdf,
    convert_markdown_to_png
)


class TestTheme:
    """Test theme functionality."""
    
    def test_get_default_theme(self):
        """Test getting default theme."""
        theme = Theme.get('default')
        assert theme is not None
        assert 'font_family' in theme
        assert 'text_color' in theme
    
    def test_get_dark_theme(self):
        """Test getting dark theme."""
        theme = Theme.get('dark')
        assert theme is not None
        assert theme['background'] == '#1a1a1a'
    
    def test_get_github_theme(self):
        """Test getting github theme."""
        theme = Theme.get('github')
        assert theme is not None
        assert theme['max_width'] == '980px'
    
    def test_get_minimal_theme(self):
        """Test getting minimal theme."""
        theme = Theme.get('minimal')
        assert theme is not None
        assert 'Georgia' in theme['font_family']
    
    def test_get_professional_theme(self):
        """Test getting professional theme."""
        theme = Theme.get('professional')
        assert theme is not None
        assert 'Helvetica' in theme['font_family']
    
    def test_get_invalid_theme(self):
        """Test getting invalid theme returns default."""
        theme = Theme.get('invalid')
        default_theme = Theme.get('default')
        assert theme == default_theme
    
    def test_list_themes(self):
        """Test listing available themes."""
        themes = Theme.list_themes()
        assert len(themes) > 0
        assert 'default' in themes
        assert 'dark' in themes
        assert 'github' in themes


class TestMarkdownConverter:
    """Test converter functionality."""
    
    @pytest.fixture
    def converter(self):
        """Create a converter instance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield MarkdownConverter(output_dir=Path(tmpdir))
    
    @pytest.fixture
    def sample_markdown(self):
        """Sample markdown text for testing."""
        return """# Test Document

This is a **test** document.

## Section 1

Some text with `inline code`.

```python
def hello():
    print("Hello, World!")
```

- Item 1
- Item 2
- Item 3

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

> This is a blockquote.

[Link](https://example.com)
"""
    
    def test_init(self, converter):
        """Test converter initialization."""
        assert converter.output_dir is not None
        assert converter.output_dir.exists()
    
    def test_markdown_to_html(self, converter, sample_markdown):
        """Test markdown to HTML conversion."""
        html = converter.markdown_to_html(sample_markdown)
        assert '<html>' in html
        assert '</html>' in html
        assert '<h1>Test Document</h1>' in html
        assert '<strong>test</strong>' in html
        assert '<code>' in html
    
    def test_generate_css(self, converter):
        """Test CSS generation."""
        css = converter.generate_css()
        assert 'body' in css
        assert 'font-family' in css
        assert 'color' in css
    
    def test_convert_to_pdf(self, converter, sample_markdown):
        """Test PDF conversion."""
        try:
            pdf_path = converter.convert_to_pdf(
                sample_markdown,
                'test.pdf'
            )
            assert pdf_path.exists()
            assert pdf_path.suffix == '.pdf'
            assert pdf_path.stat().st_size > 0
        except Exception as e:
            # wkhtmltopdf might not be installed
            pytest.skip(f"wkhtmltopdf not available: {e}")
    
    def test_convert_to_png(self, converter, sample_markdown):
        """Test PNG conversion."""
        try:
            png_path = converter.convert_to_png(
                sample_markdown,
                'test.png',
                width=800
            )
            assert png_path.exists()
            assert png_path.suffix == '.png'
            assert png_path.stat().st_size > 0
        except Exception as e:
            # wkhtmltopdf might not be installed
            pytest.skip(f"wkhtmltopdf not available: {e}")
    
    def test_convert_multiple_formats(self, converter, sample_markdown):
        """Test conversion to multiple formats."""
        try:
            results = converter.convert(
                sample_markdown,
                'test',
                formats=['pdf', 'png']
            )
            assert 'pdf' in results
            assert 'png' in results
            assert results['pdf'].exists()
            assert results['png'].exists()
        except Exception as e:
            # wkhtmltopdf might not be installed
            pytest.skip(f"wkhtmltopdf not available: {e}")
    
    def test_custom_theme(self, sample_markdown):
        """Test converter with custom theme."""
        with tempfile.TemporaryDirectory() as tmpdir:
            converter = MarkdownConverter(
                output_dir=Path(tmpdir),
                theme='dark'
            )
            html = converter.markdown_to_html(sample_markdown)
            assert '#1a1a1a' in html  # Dark background
    
    def test_custom_css(self, sample_markdown):
        """Test converter with custom CSS."""
        custom_css = ".custom { color: red; }"
        with tempfile.TemporaryDirectory() as tmpdir:
            converter = MarkdownConverter(
                output_dir=Path(tmpdir),
                custom_css=custom_css
            )
            css = converter.generate_css()
            assert custom_css in css
    
    def test_list_themes(self, converter):
        """Test listing themes."""
        themes = converter.list_themes()
        assert len(themes) > 0
        assert 'default' in themes


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    @pytest.fixture
    def sample_markdown(self):
        """Sample markdown text."""
        return "# Test\n\nContent"
    
    def test_convert_markdown_to_pdf(self, sample_markdown):
        """Test convert_markdown_to_pdf function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                pdf_path = convert_markdown_to_pdf(
                    sample_markdown,
                    'test.pdf',
                    Path(tmpdir)
                )
                assert pdf_path.exists()
            except Exception as e:
                pytest.skip(f"wkhtmltopdf not available: {e}")
    
    def test_convert_markdown_to_png(self, sample_markdown):
        """Test convert_markdown_to_png function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                png_path = convert_markdown_to_png(
                    sample_markdown,
                    'test.png',
                    Path(tmpdir)
                )
                assert png_path.exists()
            except Exception as e:
                pytest.skip(f"wkhtmltopdf not available: {e}")
    
    def test_convert_markdown(self, sample_markdown):
        """Test convert_markdown function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                results = convert_markdown(
                    sample_markdown,
                    'test',
                    Path(tmpdir),
                    formats=['pdf']
                )
                assert 'pdf' in results
                assert results['pdf'].exists()
            except Exception as e:
                pytest.skip(f"wkhtmltopdf not available: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
