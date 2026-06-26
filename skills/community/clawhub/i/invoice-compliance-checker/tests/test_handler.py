"""
Tests for Invoice Compliance Checker handler.py
"""

import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from handler import handle

def test_handle_returns_json():
    """Test that handle() returns valid JSON."""
    result = handle("test input")
    parsed = json.loads(result)
    assert isinstance(parsed, dict)
    assert parsed["skill"] == "invoice-compliance-checker"
    print(f"✓ test_handle_returns_json passed for invoice-compliance-checker")

def test_handle_contains_disclaimer():
    """Test that output contains the descriptive disclaimer."""
    result = handle("test")
    assert "descriptive" in result.lower() or "informational" in result.lower()
    print(f"✓ test_handle_contains_disclaimer passed for invoice-compliance-checker")

def test_handle_has_recommendations():
    """Test that output contains recommendations."""
    result = handle("test")
    parsed = json.loads(result)
    assert "recommendations" in parsed
    assert len(parsed["recommendations"]) > 0
    print(f"✓ test_handle_has_recommendations passed for invoice-compliance-checker")

def test_handle_has_next_steps():
    """Test that output contains next steps."""
    result = handle("test")
    parsed = json.loads(result)
    assert "next_steps" in parsed
    assert len(parsed["next_steps"]) > 0
    print(f"✓ test_handle_has_next_steps passed for invoice-compliance-checker")

def test_input_differentiation():
    """Test that different inputs produce different outputs (DEF-FIN-001 fix)."""
    # Test case 1: Simple input
    input1 = "Help me with this"
    result1 = handle(input1)
    parsed1 = json.loads(result1)
    
    # Test case 2: Detailed input with amounts
    input2 = "I need help with budget. Monthly income $5000, expenses $3000, debt $10000, urgent situation"
    result2 = handle(input2)
    parsed2 = json.loads(result2)
    
    # Verify input analysis differs
    assert parsed1["input_analysis"] != parsed2["input_analysis"], "Input analysis should differ"
    
    # Verify at least one recommendation differs (not guaranteed but likely)
    recs1 = parsed1.get("recommendations", [])
    recs2 = parsed2.get("recommendations", [])
    
    # Check if recommendations differ or if input analysis shows difference
    diff_found = False
    if recs1 != recs2:
        diff_found = True
    
    # Also check input analysis fields
    if parsed1["input_analysis"].get("contains_amounts") != parsed2["input_analysis"].get("contains_amounts"):
        diff_found = True
    if parsed1["input_analysis"].get("priority") != parsed2["input_analysis"].get("priority"):
        diff_found = True
    
    assert diff_found, "Different inputs should produce differentiable outputs"
    print(f"✓ test_input_differentiation passed for invoice-compliance-checker")

def test_amount_parsing():
    """Test that amounts in input are properly parsed."""
    input_text = "I have $5000 income and $3000 expenses"
    result = handle(input_text)
    parsed = json.loads(result)
    
    assert parsed["input_analysis"].get("contains_amounts") == True
    assert "amounts_found" in parsed["input_analysis"]
    print(f"✓ test_amount_parsing passed for invoice-compliance-checker")

if __name__ == "__main__":
    test_handle_returns_json()
    test_handle_contains_disclaimer()
    test_handle_has_recommendations()
    test_handle_has_next_steps()
    test_input_differentiation()
    test_amount_parsing()
    print(f"All tests passed for invoice-compliance-checker")
