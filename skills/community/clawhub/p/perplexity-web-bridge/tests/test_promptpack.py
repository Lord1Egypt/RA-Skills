# tests/test_promptpack.py
from jev_webbridge.promptpack import enhance


def test_wrapper_keeps_goal_verbatim_and_core_rules():
    goal = "compare database options for a startup at scale"
    out = enhance(goal)
    assert goal in out  # keyword-gate tokens must survive the wrapper
    assert "citation after every factual sentence" in out
    assert "unsupported" in out


def test_recipes_add_their_focus_extras():
    assert "SEC filings" in enhance("x", "finance")
    assert "official docs" in enhance("x", "tech")
    assert "list sources before writing" in enhance("x", "research")


def test_unknown_recipe_is_rejected():
    try:
        enhance("x", "nope")
    except ValueError:
        return
    raise AssertionError("expected ValueError")
