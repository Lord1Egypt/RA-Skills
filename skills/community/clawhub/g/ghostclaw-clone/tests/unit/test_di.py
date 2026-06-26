"""Tests for Dependency Injection in CodebaseAnalyzer."""

import pytest
from unittest.mock import MagicMock
from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.validator import RuleValidator

def test_analyzer_injected_validator():
    # Create a mock validator
    mock_validator = MagicMock(spec=RuleValidator)
    mock_validator.validate.return_value = {
        "issues": ["Injected Issue"],
        "architectural_ghosts": [],
        "red_flags": []
    }

    # Inject it
    analyzer = CodebaseAnalyzer(validator=mock_validator)

    # We need a minimal repo to analyze
    # For simplicity, we just check if it was called during analyze
    # but analyze() does a lot of other things that might fail if repo doesn't exist.

    assert analyzer.validator == mock_validator

def test_analyzer_default_validator():
    analyzer = CodebaseAnalyzer()
    assert isinstance(analyzer.validator, RuleValidator)
