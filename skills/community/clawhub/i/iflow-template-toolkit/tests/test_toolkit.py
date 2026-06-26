#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for iFlow Template Toolkit"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.template_engine import TemplateEngine, render_template
from src.i18n.translator import Translator, init_translator, t


def test_variable_substitution():
    """Test simple variable substitution"""
    result = render_template("Hello {{name}}!", {"name": "World"})
    assert result == "Hello World!", f"Expected 'Hello World!', got '{result}'"
    print("✓ Variable substitution")


def test_conditionals():
    """Test conditional blocks"""
    template = "{% if status == 'active' %}Active{% else %}Inactive{% endif %}"
    
    result = render_template(template, {"status": "active"})
    assert result == "Active", f"Expected 'Active', got '{result}'"
    
    result = render_template(template, {"status": "inactive"})
    assert result == "Inactive", f"Expected 'Inactive', got '{result}'"
    print("✓ Conditionals")


def test_loops():
    """Test for loops"""
    template = "{% for item in items %}{{item}} {% endfor %}"
    result = render_template(template, {"items": ["A", "B", "C"]})
    assert "A" in result and "B" in result and "C" in result
    print("✓ Loops")


def test_combined():
    """Test combined template features"""
    template = """
{% for user in users %}
{{index1}}. {{user.name}} - {% if user.active %}Active{% else %}Inactive{% endif %}
{% endfor %}
"""
    context = {
        "users": [
            {"name": "Alice", "active": True},
            {"name": "Bob", "active": False}
        ]
    }
    result = render_template(template, context)
    assert "Alice" in result and "Bob" in result
    assert "Active" in result and "Inactive" in result
    print("✓ Combined features")


def test_translator():
    """Test translation functions"""
    init_translator({
        'en': {'hello': 'Hello', 'bye': 'Goodbye'},
        'zh': {'hello': '你好', 'bye': '再见'}
    }, default_lang='en')
    
    assert t('hello') == 'Hello'
    assert t('hello', lang='zh') == '你好'
    assert t('bye') == 'Goodbye'
    assert t('bye', lang='zh') == '再见'
    print("✓ Translator")


def test_missing_key():
    """Test missing translation key returns the key"""
    init_translator({'en': {}}, default_lang='en')
    assert t('missing_key') == 'missing_key'
    print("✓ Missing key fallback")


if __name__ == '__main__':
    print("\nRunning iFlow Template Toolkit Tests...\n")
    
    test_variable_substitution()
    test_conditionals()
    test_loops()
    test_combined()
    test_translator()
    test_missing_key()
    
    print("\n✅ All tests passed!\n")
