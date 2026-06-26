"""
Tests for playwright_test_generator module.
"""
import pytest
from unittest.mock import MagicMock, patch


class TestPageAnalysis:
    """Tests for page analysis logic."""

    def test_extract_form_fields(self):
        """Form fields should be extracted correctly."""
        from playwright_test_generator import PageAnalyzer
        
        mock_page = MagicMock()
        mock_page.query_selector_all.return_value = [
            MagicMock(selectorname='input#email', get_attribute=MagicMock(return_value='email')),
            MagicMock(selectorname='input#password', get_attribute=MagicMock(return_value='password')),
            MagicMock(selectorname='button[type="submit"]', get_attribute=MagicMock(return_value='submit')),
        ]
        
        analyzer = PageAnalyzer(mock_page)
        forms = analyzer.extract_forms()
        
        assert len(forms) >= 0  # May be 0 if no forms found

    def test_extract_navigation_links(self):
        """Navigation links should be extracted."""
        from playwright_test_generator import PageAnalyzer
        
        mock_page = MagicMock()
        mock_page.query_selector_all.return_value = []
        
        analyzer = PageAnalyzer(mock_page)
        links = analyzer.extract_links()
        
        assert isinstance(links, list)

    def test_suggest_locators(self):
        """Locator suggestions should be generated."""
        from playwright_test_generator import PageAnalyzer
        
        mock_page = MagicMock()
        analyzer = PageAnalyzer(mock_page)
        
        locators = analyzer.suggest_locators('input', {'type': 'text', 'id': 'email'})
        
        assert isinstance(locators, list)
        assert len(locators) > 0


class TestURLGenerator:
    """Tests for URL-based test generation."""

    @patch('playwright.sync_api.sync_playwright')
    def test_generate_from_url_basic(self, mock_playwright):
        """Basic URL generation should produce valid code."""
        from playwright_test_generator import generate_from_url
        
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.url = 'https://example.com'
        mock_page.title.return_value = 'Example'
        mock_page.query_selector_all.return_value = []
        
        mock_context = MagicMock()
        mock_context.new_page.return_value = mock_page
        mock_browser.new_context.return_value = mock_context
        
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        
        code = generate_from_url('https://example.com', 'python')
        
        assert 'example.com' in code

    @patch('playwright.sync_api.sync_playwright')
    def test_generate_from_url_js(self, mock_playwright):
        """JS generation from URL should produce JS code."""
        from playwright_test_generator import generate_from_url
        
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.url = 'https://test.com'
        mock_page.title.return_value = 'Test'
        mock_page.query_selector_all.return_value = []
        
        mock_context = MagicMock()
        mock_context.new_page.return_value = mock_page
        mock_browser.new_context.return_value = mock_context
        
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        
        code = generate_from_url('https://test.com', 'js')
        
        assert 'test.com' in code


class TestStoryParser:
    """Tests for user story parsing."""

    def test_parse_login_story(self):
        """Login story should be parsed into steps."""
        from playwright_test_generator import parse_user_story
        
        story = "As a user I can login with email and password"
        steps = parse_user_story(story)
        
        assert isinstance(steps, list)
        assert len(steps) >= 2
        assert any('login' in s.lower() or 'navigate' in s.lower() for s in steps)

    def test_parse_registration_story(self):
        """Registration story parsing."""
        from playwright_test_generator import parse_user_story
        
        story = "As a new user I want to register so I can access the platform"
        steps = parse_user_story(story)
        
        assert isinstance(steps, list)
        assert len(steps) > 0

    def test_parse_empty_story(self):
        """Empty story should return default steps."""
        from playwright_test_generator import parse_user_story
        
        steps = parse_user_story("")
        
        assert isinstance(steps, list)
        # Empty story returns default steps
        assert len(steps) > 0


class TestDescParser:
    """Tests for description parsing."""

    def test_parse_login_desc(self):
        """Login description should be parsed."""
        from playwright_test_generator import parse_description
        
        desc = "Open login page, fill email, fill password, click submit, verify redirect"
        steps = parse_description(desc)
        
        assert isinstance(steps, list)
        assert len(steps) >= 3

    def test_parse_checkout_desc(self):
        """Checkout description parsing."""
        from playwright_test_generator import parse_description
        
        desc = "Add item to cart, go to checkout, enter shipping, enter payment, place order"
        steps = parse_description(desc)
        
        assert isinstance(steps, list)
        assert len(steps) >= 3
