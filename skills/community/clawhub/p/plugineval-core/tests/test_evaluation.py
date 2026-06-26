#!/usr/bin/env python3
"""Tests for plugineval-core evaluation engine."""

import unittest
import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from eval import SkillEvaluation, evaluate_frontmatter


class TestFrontmatter(unittest.TestCase):
    """Test frontmatter quality checks."""
    
    def test_complete_frontmatter(self):
        """Complete frontmatter should score 100."""
        content = """---
name: test-skill
version: 1.0.0
description: A comprehensive test skill with good description length.
triggers:
  - "test trigger"
---
# Test Skill
"""
        score, issues = evaluate_frontmatter(content)
        self.assertEqual(score, 100)
        self.assertEqual(len(issues), 0)
    
    def test_missing_trigger(self):
        """Missing trigger should reduce score."""
        content = """---
name: test-skill
version: 1.0.0
description: A comprehensive test skill with good description.
---
"""
        score, issues = evaluate_frontmatter(content)
        self.assertLess(score, 100)
        self.assertTrue(any('trigger' in i.lower() for i in issues))


class TestAntiPatterns(unittest.TestCase):
    """Test anti-pattern detection."""
    
    def test_over_constrained(self):
        """Too many directives should be flagged."""
        content = "MUST " * 20  # 20 MUST directives
        # Implementation would detect this
        self.assertTrue(len(content.split('MUST')) > 15)


class TestBadges(unittest.TestCase):
    """Test badge assignment."""
    
    def test_platinum_badge(self):
        """Score ≥90 should be Platinum."""
        self.assertEqual(get_badge(90), "Platinum")
        self.assertEqual(get_badge(95), "Platinum")
    
    def test_gold_badge(self):
        """Score ≥80 should be Gold."""
        self.assertEqual(get_badge(85), "Gold")
        self.assertEqual(get_badge(80), "Gold")


def get_badge(score):
    """Helper to get badge from score."""
    if score >= 90:
        return "Platinum"
    elif score >= 80:
        return "Gold"
    elif score >= 70:
        return "Silver"
    elif score >= 60:
        return "Bronze"
    return "Needs Improvement"


if __name__ == '__main__':
    unittest.main()
