"""Tests for dataflow_report — memory dataflow analysis."""

import json
import pytest


class TestDataflowReport:
    def test_main_runs(self):
        """dataflow_report only has main(), verify it's callable."""
        from dataflow_report import main
        assert callable(main)
