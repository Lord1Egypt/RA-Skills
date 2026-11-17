#!/usr/bin/env python3
"""Self-test for laundry_decoder.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from laundry_decoder import lookup_symbol, Garment, plan_loads, STAINS, compatible

def test_lookup():
    for desc in ("tub 40", "Tub 40", "tub hand", "triangle crossed", "iron 2 dots",
                 "circle p", "square circle 1 dot", "no bleach", "dry flat"):
        key, entry = lookup_symbol(desc)
        assert entry is not None, f"failed: {desc}"
    key, entry = lookup_symbol("tub hand")
    assert "hand" in entry[0].lower()
    key, entry = lookup_symbol("iron 2 dots")
    assert entry and "150" in entry[0] + entry[1], entry
    key, entry = lookup_symbol("garbage nonsense")
    assert entry is None
    print("ok symbol lookup + aliases")


def test_garment():
    g = Garment("white towels;white;90;cotton")
    assert g.temp == 90 and g.fclass == "heavy" and not g.bleeder
    g2 = Garment("red tee;new;40;cotton")
    assert g2.bleeder
    g3 = Garment("blouse;light;30;silk;delicate")
    assert g3.delicate and g3.fclass == "delicate_fiber"
    try:
        Garment("bad")
        assert False
    except ValueError:
        pass
    print("ok garment parsing")


def test_compatibility():
    towels = Garment("towels;white;90;cotton")
    sheets = Garment("sheets;white;60;cotton")
    jeans = Garment("jeans;dark;40;denim")
    red = Garment("red tee;new;40;cotton")
    silk = Garment("blouse;light;30;silk;delicate")
    wool = Garment("sweater;dark;30;wool;delicate")

    assert compatible(towels, sheets)[0]          # both white heavy cotton
    assert not compatible(towels, jeans)[0]       # whites never with darks
    assert not compatible(red, towels)[0]         # bleeder
    assert not compatible(silk, towels)[0]       # delicate + heavy
    assert not compatible(wool, towels)[0]       # wool + terry
    assert compatible(wool, silk)[0]             # both delicate fibers
    print("ok compatibility rules")


def test_plan():
    items = [
        Garment("white towels;white;90;cotton"),
        Garment("red tee;new;40;cotton"),
        Garment("jeans;dark;40;denim"),
        Garment("silk blouse;light;30;silk;delicate"),
    ]
    loads = plan_loads(items)
    assert len(loads) == 4, loads  # towels / red tee / jeans / silk each separate
    # verify temperature invariant: load temp <= every member's ceiling
    for load in loads:
        members = [g for g in items if g.name in load["items"]]
        assert load["temp_c"] <= min(g.temp for g in members)
    assert not any(g.bleeder for load in loads for g in items
                   if g.name in load["items"] and "," in load["items"])
    # second scenario: compatible items merge (no whites-with-darks here)
    items2 = [
        Garment("grey tee;light;40;cotton"),
        Garment("beige socks;light;60;cotton"),
        Garment("chinos;dark;40;polyester"),
    ]
    loads2 = plan_loads(items2)
    assert len(loads2) == 1, loads2  # no bleeders/delicates; lights+dark mix at cold
    assert loads2[0]["temp_c"] == 40
    # whites vs darks must split
    items3 = [Garment("white shirts;white;60;cotton"),
              Garment("black tee;dark;40;cotton")]
    assert len(plan_loads(items3)) == 2
    print(f"ok plan: 4 conflicting -> {len(loads)} loads; 3 compatible -> {len(loads2)} load")


def test_stains():
    assert len(STAINS) >= 20
    for name in ("red wine", "blood", "pet urine", "dye transfer"):
        e = STAINS[name]
        assert len(e["steps"]) >= 3 and e["never"]
    # protein stains must not start with heat
    for name in ("blood", "coffee cream liqueur"):
        assert not any("hot" in s.lower() for s in STAINS[name]["steps"][:1])
    print(f"ok stains ({len(STAINS)} protocols)")


if __name__ == "__main__":
    test_lookup()
    test_garment()
    test_compatibility()
    test_plan()
    test_stains()
    print("\nALL TESTS PASSED ✅")
