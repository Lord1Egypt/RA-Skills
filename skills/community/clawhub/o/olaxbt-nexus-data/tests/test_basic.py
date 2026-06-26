"""
Basic tests for olaxbt-nexus-data package.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))


def test_imports():
    """Test that all major modules can be imported."""
    # Test core imports
    from olaxbt_nexus_data.core.exceptions import (
        NexusError, APIError, AuthenticationError, RateLimitError, ValidationError
    )
    
    # Test security imports
    from olaxbt_nexus_data.core.security import SecurityConfig
    
    # Test API modules imports
    from olaxbt_nexus_data.api.news import NewsClient
    from olaxbt_nexus_data.api.market import MarketClient
    
    assert True  # If we get here, imports worked


def test_security_config():
    """Test SecurityConfig initialization."""
    from olaxbt_nexus_data.core.security import SecurityConfig
    
    # Test default config
    config = SecurityConfig()
    assert config.encrypt_jwt is True
    assert config.rate_limit == 1000
    assert config.timeout == 30
    assert config.max_retries == 3


def test_exceptions():
    """Test exception hierarchy."""
    from olaxbt_nexus_data.core.exceptions import (
        NexusError, APIError, AuthenticationError, RateLimitError, ValidationError
    )
    
    # Test exception instantiation
    nexus_error = NexusError("Test error")
    assert str(nexus_error) == "Test error"
    
    api_error = APIError("API failed", status_code=500)
    assert "API failed" in str(api_error)
    assert api_error.status_code == 500
    
    auth_error = AuthenticationError("Auth failed")
    assert "Auth failed" in str(auth_error)
    
    rate_error = RateLimitError("Rate limited", reset_in=60)
    assert "Rate limited" in str(rate_error)
    assert rate_error.reset_in == 60
    
    validation_error = ValidationError("Invalid input")
    assert "Invalid input" in str(validation_error)


if __name__ == "__main__":
    # Run tests
    test_imports()
    test_security_config()
    test_exceptions()
    print("✅ All basic tests passed!")