"""
Tests for scorer.py - TDD approach (RED phase first)
"""

import pytest
from scripts.scorer import gini, participation_score, compute_total


class TestGini:
    """Test Gini coefficient calculation"""

    def test_gini_equal(self):
        """Equal distribution should have Gini = 0"""
        assert gini([10, 10, 10]) == 0.0

    def test_gini_unequal(self):
        """Highly unequal distribution should have high Gini"""
        result = gini([0, 0, 100])
        assert abs(result - 0.667) < 0.01

    def test_gini_single(self):
        """Single element should have Gini = 0"""
        assert gini([100]) == 0.0


class TestParticipationScore:
    """Test participation score calculation"""

    def test_participation_balanced(self):
        """Balanced participation should score 100"""
        result = participation_score({"A": 100, "B": 100})
        assert result == 100.0

    def test_participation_dominant(self):
        """Dominant speaker should lower the score"""
        result = participation_score({"A": 900, "B": 100})
        assert result <= 40.0

    def test_participation_single_speaker(self):
        """Single speaker should return None"""
        result = participation_score({"A": 500})
        assert result is None

    def test_participation_empty(self):
        """Empty speaker dict should return None"""
        result = participation_score({})
        assert result is None


class TestComputeTotal:
    """Test total score computation with weighted average"""

    def test_compute_total_full(self):
        """All three scores present should use standard weights"""
        result = compute_total(80.0, 70.0, 60.0)

        # Expected: 80*0.4 + 70*0.3 + 60*0.3 = 32 + 21 + 18 = 71.0
        assert result["total"] == 71.0
        assert result["weights_used"] == {"decision": 0.4, "time": 0.3, "participation": 0.3}
        assert result["degraded"] is False

    def test_compute_total_degraded(self):
        """Missing participation should use degraded weights"""
        result = compute_total(80.0, 60.0, None)

        # Expected: 80*0.6 + 60*0.4 = 48 + 24 = 72.0
        assert result["total"] == 72.0
        assert result["weights_used"] == {"decision": 0.6, "time": 0.4}
        assert result["degraded"] is True

    def test_compute_total_both_none(self):
        """Both decision and time None should return None total"""
        result = compute_total(None, None, 50.0)
        assert result["total"] is None
