#!/usr/bin/env python3
"""Unit tests for the bivariate Poisson soccer model. No SDK calls needed."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soccer_trader import (
    ovr_to_lambdas,
    build_goal_grid,
    compute_win_probs,
    compute_over_prob,
    compute_spread_prob,
    devig,
    compute_edge,
    lookup_team,
    parse_market,
)

# ---------------------------------------------------------------------------
# Model sanity checks
# ---------------------------------------------------------------------------

def test_equal_teams_are_roughly_symmetric():
    lam_h, lam_a = ovr_to_lambdas(82, 82, home_boost=0.0)
    assert abs(lam_h - lam_a) < 0.01, "Equal OVR + no home boost should give equal lambdas"

    grid = build_goal_grid(lam_h, lam_a)
    p_home, p_draw, p_away = compute_win_probs(grid)
    assert abs(p_home - p_away) < 0.01, "Win probs should be symmetric for equal teams"
    assert abs(p_home + p_draw + p_away - 1.0) < 0.001, "Probs must sum to 1"
    print(f"Equal teams (no home): home={p_home:.3f}, draw={p_draw:.3f}, away={p_away:.3f} ✓")

def test_home_advantage_boosts_home_win_prob():
    lam_h_boost, lam_a_boost = ovr_to_lambdas(82, 82, home_boost=0.15)
    lam_h_neutral, lam_a_neutral = ovr_to_lambdas(82, 82, home_boost=0.0)
    assert lam_h_boost > lam_h_neutral, "Home boost should increase lambda_home"
    assert lam_a_boost == lam_a_neutral, "Home boost should not affect lambda_away"

    grid_b = build_goal_grid(lam_h_boost, lam_a_boost)
    grid_n = build_goal_grid(lam_h_neutral, lam_a_neutral)
    p_home_b, _, _ = compute_win_probs(grid_b)
    p_home_n, _, _ = compute_win_probs(grid_n)
    assert p_home_b > p_home_n, "Home boost should increase home win probability"
    print(f"Home advantage: neutral={p_home_n:.3f} → boosted={p_home_b:.3f} ✓")

def test_strong_favourite_wins_more():
    lam_h, lam_a = ovr_to_lambdas(90, 70, home_boost=0.0)
    grid = build_goal_grid(lam_h, lam_a)
    p_home, p_draw, p_away = compute_win_probs(grid)
    assert p_home > 0.6, f"90-OVR team vs 70-OVR should win >60% (got {p_home:.2f})"
    print(f"OVR 90 vs 70: home={p_home:.3f}, draw={p_draw:.3f}, away={p_away:.3f} ✓")

def test_probs_sum_to_one():
    for home_ovr, away_ovr in [(85, 80), (75, 82), (90, 90)]:
        lam_h, lam_a = ovr_to_lambdas(home_ovr, away_ovr)
        grid = build_goal_grid(lam_h, lam_a)
        total = sum(grid[i][j] for i in range(len(grid)) for j in range(len(grid[0])))
        assert abs(total - 1.0) < 0.01, f"Grid must sum to ~1, got {total:.4f}"
    print("Grid probability sums ✓")

def test_over_under_complementary():
    lam_h, lam_a = ovr_to_lambdas(83, 80)
    grid = build_goal_grid(lam_h, lam_a)
    for line in [1.5, 2.5, 3.5, 4.5]:
        p_over = compute_over_prob(grid, line)
        p_under = 1.0 - p_over
        assert 0 <= p_over <= 1, f"Over prob out of range for line {line}"
        assert abs(p_over + p_under - 1.0) < 0.001
    print("Over/under probabilities ✓")

def test_spread_2_goals():
    lam_h, lam_a = ovr_to_lambdas(90, 75, home_boost=0.0)  # strong home side
    grid = build_goal_grid(lam_h, lam_a)
    p_1goal = compute_spread_prob(grid, 1)
    p_2goal = compute_spread_prob(grid, 2)
    assert p_1goal > p_2goal, "P(margin≥1) should exceed P(margin≥2)"
    print(f"Spread: P(home wins by ≥1)={p_1goal:.3f}, P(≥2)={p_2goal:.3f} ✓")

# ---------------------------------------------------------------------------
# De-vig
# ---------------------------------------------------------------------------

def test_devig():
    fair_yes, fair_no = devig(0.55, 0.50)
    assert abs(fair_yes + fair_no - 1.0) < 0.001, "De-vigged probs must sum to 1"
    assert abs(fair_yes - 0.55/1.05) < 0.001
    print(f"De-vig: 0.55/0.50 → fair_yes={fair_yes:.4f}, fair_no={fair_no:.4f} ✓")

def test_edge_positive_when_model_above_market():
    assert compute_edge(0.65, 0.55) > 0
    assert compute_edge(0.40, 0.55) < 0
    print("Edge sign ✓")

# ---------------------------------------------------------------------------
# Ratings lookup
# ---------------------------------------------------------------------------

def test_lookup_known_teams():
    assert lookup_team("Argentina") is not None
    assert lookup_team("ARG") is not None
    assert lookup_team("real madrid") is not None
    assert lookup_team("man city") is not None
    print("Team lookups ✓")

def test_lookup_unknown_team():
    assert lookup_team("Fictional FC") is None
    print("Unknown team returns None ✓")

# ---------------------------------------------------------------------------
# Market parsing
# ---------------------------------------------------------------------------

def _make_market(question, yes_ask=55, no_ask=50):
    return {"question": question, "yes_ask": yes_ask, "no_ask": no_ask}

def test_parse_winner_market():
    m = _make_market("Will Brazil win vs Argentina?")
    parsed = parse_market(m, {"winner"})
    assert parsed is not None, "Should parse winner market"
    assert parsed["type"] == "winner"
    assert "brazil" in parsed["home"].lower()
    assert "argentina" in parsed["away"].lower()
    print(f"Winner parse: {parsed['home']} vs {parsed['away']} ✓")

def test_parse_totals_market():
    m = _make_market("Will there be more than 2.5 goals in France vs England?")
    parsed = parse_market(m, {"totals"})
    assert parsed is not None, "Should parse totals market"
    assert parsed["type"] == "totals"
    assert parsed["line"] == 2.5
    print(f"Totals parse: line={parsed['line']}, {parsed['home']} vs {parsed['away']} ✓")

def test_parse_spread_market():
    m = _make_market("Will Spain win by 2 or more goals vs USA?")
    parsed = parse_market(m, {"spread"})
    assert parsed is not None, "Should parse spread market"
    assert parsed["type"] == "spread"
    assert parsed["line"] == 2
    print(f"Spread parse: margin={parsed['line']}, {parsed['home']} vs {parsed['away']} ✓")

def test_parse_returns_none_for_mismatch():
    m = _make_market("Will it rain tomorrow?")
    assert parse_market(m, {"winner", "totals", "spread"}) is None
    print("Non-soccer market correctly returns None ✓")

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_equal_teams_are_roughly_symmetric,
        test_home_advantage_boosts_home_win_prob,
        test_strong_favourite_wins_more,
        test_probs_sum_to_one,
        test_over_under_complementary,
        test_spread_2_goals,
        test_devig,
        test_edge_positive_when_model_above_market,
        test_lookup_known_teams,
        test_lookup_unknown_team,
        test_parse_winner_market,
        test_parse_totals_market,
        test_parse_spread_market,
        test_parse_returns_none_for_mismatch,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"FAIL {t.__name__}: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
