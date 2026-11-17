"""Tests for antidetect module."""
import sys; sys.path.insert(0, "src")

from unittest.mock import patch, MagicMock
from perplexity_toolkit.utils.antidetect import human_delay, micro_delay


class TestHumanDelay:
    @patch("perplexity_toolkit.utils.antidetect.time.sleep")
    def test_sleeps_in_range(self, mock_sleep):
        human_delay(0.5, 1.5)
        args = mock_sleep.call_args[0]
        assert 0.5 <= args[0] <= 1.5

    @patch("perplexity_toolkit.utils.antidetect.time.sleep")
    def test_custom_range(self, mock_sleep):
        human_delay(2.0, 4.0)
        args = mock_sleep.call_args[0]
        assert 2.0 <= args[0] <= 4.0


class TestMicroDelay:
    @patch("perplexity_toolkit.utils.antidetect.time.sleep")
    def test_sleeps_in_range(self, mock_sleep):
        micro_delay(0.05, 0.15)
        args = mock_sleep.call_args[0]
        assert 0.05 <= args[0] <= 0.15


class TestLognormalDelay:
    @patch("perplexity_toolkit.utils.antidetect.time.sleep")
    def test_lognormal_positive(self, mock_sleep):
        from perplexity_toolkit.utils.antidetect import lognormal_delay
        for _ in range(100):
            lognormal_delay()
        assert mock_sleep.call_count == 100
        # All delays should be positive
        for call in mock_sleep.call_args_list:
            assert call[0][0] > 0


class TestDistractionDelay:
    @patch("perplexity_toolkit.utils.antidetect.time.sleep")
    @patch("perplexity_toolkit.utils.antidetect.random.random", return_value=0.1)
    def test_no_distraction_when_random_high(self, mock_random, mock_sleep):
        from perplexity_toolkit.utils.antidetect import distraction_delay
        distraction_delay()
        # random()=0.1 > 0.05 so no distraction
        mock_sleep.assert_not_called()

    @patch("perplexity_toolkit.utils.antidetect.time.sleep")
    @patch("perplexity_toolkit.utils.antidetect.random.random", return_value=0.01)
    def test_distraction_when_random_low(self, mock_random, mock_sleep):
        from perplexity_toolkit.utils.antidetect import distraction_delay
        distraction_delay()
        mock_sleep.assert_called_once()
        delay = mock_sleep.call_args[0][0]
        assert 3.0 <= delay <= 5.0
