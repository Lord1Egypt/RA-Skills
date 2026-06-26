"""Tests for scaffold chart-type auto-inference."""
from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    "fields,expected",
    [
        ([("count", "int")], "heatmap"),
        ([("weight", "float")], "heatmap"),
        ([("count", "int"), ("notes", "text")], "heatmap"),
        ([("mood", "text")], "calendar_grid"),
        ([("done", "bool")], "calendar_grid"),
        ([], "calendar_grid"),
    ],
)
def test_infer_chart_type(fields, expected):
    from glancely.skills.scaffold_component.scripts.scaffold import _infer_chart_type

    assert _infer_chart_type(fields) == expected
