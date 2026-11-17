#!/usr/bin/env python3
"""Self-test for party_planner.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from party_planner import (drinks_needed, split_drinks, ceil_to, plan,
                           WINE_GLASSES_PER_BOTTLE, SHOTS_PER_750)
import argparse


def test_drinks():
    # 4h party, 20 drinkers: 2+3 = 5 each = 100
    assert abs(drinks_needed(20, 4) - 100) < 1e-9
    # heat +20%: 120
    assert abs(drinks_needed(20, 4, heat=True) - 120) < 1e-9
    # light crowd -20%: 80
    assert abs(drinks_needed(20, 4, light=True) - 80) < 1e-9
    # 1h party: 2 each
    assert abs(drinks_needed(10, 1) - 20) < 1e-9
    # wine-only 3h: 4.5 glasses each
    assert abs(drinks_needed(10, 3, wine_only=True) - 45) < 1e-9
    print("ok drinks math")


def test_split():
    b, w, s = split_drinks(100, (40, 40, 20))
    assert abs(b - 40) < 1e-9 and abs(w - 40) < 1e-9 and abs(s - 20) < 1e-9
    b, w, s = split_drinks(90, (50, 50, 0))
    assert s == 0 and abs(b - 45) < 1e-9
    print("ok mix split")


def test_ceil():
    assert ceil_to(7.2, 6) == 12
    assert ceil_to(12, 6) == 12
    assert ceil_to(0.8) == 1
    assert ceil_to(13, 6) == 18
    print("ok round-up to purchasable units")


def test_plan_bbq():
    args = argparse.Namespace(
        guests=40, hours=5, drinkers=30, kids=10, style="bbq",
        mix=(40, 40, 20), heat=True, active=False, light=False,
        wine_only=False, toast=False, big_eaters=False,
        price_beer=None, price_wine=None, price_spirit=None)
    p = plan(args)
    # 30 drinkers × 5h: (2+4)=6 ×1.2 heat = 7.2 → 216 drinks
    assert abs(p["drinks_total"] - 216) < 1.0
    assert p["beer_bottles"] % 6 == 0
    assert p["wine_bottles"] >= 216 * 0.4 / 5 - 1
    assert p["spirit_750ml"] >= 1
    # food: adult_equiv = 30 + 5 = 35 → protein 17.5 lb
    assert abs(p["food"]["protein_lb"] - 17.5) < 0.01
    assert p["kids"] == 10
    print(f"ok bbq plan: {p['drinks_total']:.0f} drinks, {p['beer_bottles']} beer, "
          f"{p['wine_bottles']} wine, {p['ice_20lb_bags']} ice bags")


def test_plan_dinner():
    args = argparse.Namespace(
        guests=8, hours=3, drinkers=8, kids=0, style="dinner",
        mix=(20, 60, 20), heat=False, active=False, light=False,
        wine_only=False, toast=False, big_eaters=False,
        price_beer=None, price_wine=None, price_spirit=None)
    p = plan(args)
    # 8 drinkers × (2+2) = 32 drinks; wine 60% = 19.2 glasses → 4 bottles
    assert p["wine_bottles"] == 4, p["wine_bottles"]
    assert abs(p["food"]["total_lb"] - 9.6) < 0.01
    print(f"ok dinner: {p['drinks_total']} drinks → {p['wine_bottles']} wine bottles")


def test_plan_no_alcohol():
    args = argparse.Namespace(
        guests=20, hours=3, drinkers=0, kids=12, style="birthday",
        mix=(40, 40, 20), heat=False, active=False, light=False,
        wine_only=False, toast=False, big_eaters=False,
        price_beer=None, price_wine=None, price_spirit=None)
    p = plan(args)
    assert p["beer_bottles"] == 0 and p["wine_bottles"] == 0
    # 20 non-drinkers × 2/hr × 3h = 120 servings
    assert p["nonalc_servings"] >= 120
    assert p["food"]["cake_servings"] == 20
    print(f"ok birthday: {p['nonalc_servings']} non-alc servings")


def test_wedding_toast():
    args = argparse.Namespace(
        guests=80, hours=5, drinkers=60, kids=0, style="reception",
        mix=(50, 50, 0), heat=False, active=True, light=False,
        wine_only=False, toast=True, big_eaters=False,
        price_beer=1.5, price_wine=9.0, price_spirit=None)
    p = plan(args)
    assert p["toast_bottles"] == 80 // 8  # 10 bottles
    assert p["budget"] and p["budget"]["total"] > 0
    print(f"ok wedding: toast {p['toast_bottles']} btl, budget ${p['budget']['total']}")


if __name__ == "__main__":
    test_drinks()
    test_split()
    test_ceil()
    test_plan_bbq()
    test_plan_dinner()
    test_plan_no_alcohol()
    test_wedding_toast()
    print("\nALL TESTS PASSED ✅")
