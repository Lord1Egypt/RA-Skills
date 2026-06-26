"""
Basic tests for HTML to PPTX Converter
"""

import unittest
import tempfile
import os
from pathlib import Path
from src.converter import HTMLToPPTXConverter, parse_html_slides


class TestHTMLToPPTXConverter(unittest.TestCase):

    def setUp(self):
        self.converter = HTMLToPPTXConverter()

    def test_parse_html_slides(self):
        """Test parsing HTML slides from a sample file."""
        # Create a temporary HTML file with sample slides
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body>
            <div class="slide slide-cover" id="slide-1">
                <h1>Test Title</h1>
                <p>Test subtitle</p>
            </div>
            <div class="slide slide-overview" id="slide-2">
                <h2>Overview</h2>
                <div class="overview-grid">
                    <div class="overview-card">
                        <div class="number">100</div>
                        <div class="label">Total Items</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_html_path = f.name

        try:
            slides = parse_html_slides(temp_html_path)
            self.assertEqual(len(slides), 2)
            self.assertEqual(slides[0]['type'], 'cover')
            self.assertEqual(slides[1]['type'], 'overview')
        finally:
            os.unlink(temp_html_path)


if __name__ == '__main__':
    unittest.main()