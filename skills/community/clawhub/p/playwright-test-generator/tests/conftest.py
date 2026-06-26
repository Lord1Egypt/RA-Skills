"""Pytest configuration for Playwright test generator tests."""
import pytest

# Provide a minimal page fixture for sample generated tests
# In real usage, tests would use pytest-playwright's page fixture
@pytest.fixture
def mock_page():
    """Mock page fixture for testing."""
    from unittest.mock import MagicMock
    page = MagicMock()
    page.goto = MagicMock()
    page.fill = MagicMock()
    page.click = MagicMock()
    page.wait_for_selector = MagicMock()
    page.title = MagicMock(return_value="Test Page")
    page.url = "https://example.com"
    return page
