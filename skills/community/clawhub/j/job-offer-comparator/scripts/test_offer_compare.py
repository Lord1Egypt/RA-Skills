#!/usr/bin/env python3
"""Test suite for offer_compare.py — plain asserts, no third-party deps.

Run:  python3 scripts/test_offer_compare.py
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "offer_compare.py")

spec = importlib.util.spec_from_file_location("offer_compare", SCRIPT)
oc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oc)

PASS = 0


def ok(name, cond, detail=""):
    global PASS
    if not cond:
        print(f"[FAIL] {name} {detail}")
        sys.exit(1)
    PASS += 1
    print(f"[PASS] {name}")


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol


# ---------------------------------------------------------------- offer fixture
BASE_OFFER = {
    "name": "Fixture",
    "base": 100_000,
    "bonus_pct": 0.10,
    "equity_annual_value": 10_000,
    "equity_risk": 0.5,
    "retirement_match_pct": 0.05,
    "retirement_match_cap": 10_000,
    "health_premium_monthly": 200,
    "other_benefits_monthly": 0,
    "pto_days": 20,
    "holidays": 10,
    "hours_per_week": 40,
    "overtime_hours_per_week": 0,
    "commute_km_each_way": 20,
    "commute_days_per_week": 3,
    "commute_cost_per_km": 0.30,
    "monthly_parking_or_transit": 100,
    "col_index": 100,
    "relocation_bonus": 0,
}


def variant(**over):
    o = dict(BASE_OFFER)
    o.update(over)
    return o


# ---------------------------------------------------------------- 1. match cap
def test_match_cap():
    # 5% of 100k = 5,000 < cap 10,000 -> uncapped
    c = oc.compute_offer(oc.normalize_offer(variant(), 0))
    ok("match below cap pays full 5%", near(c["retirement_match"], 5_000.0))
    ok("match_capped flag false below cap", c["match_capped"] is False)
    # cap 3,000 binds: 5,000 -> 3,000
    c2 = oc.compute_offer(oc.normalize_offer(variant(retirement_match_cap=3_000), 0))
    ok("match cap enforced at 3,000", near(c2["retirement_match"], 3_000.0))
    ok("match_capped flag true when cap binds", c2["match_capped"] is True)
    # cap None -> no cap
    c3 = oc.compute_offer(
        oc.normalize_offer(variant(retirement_match_cap=None), 0))
    ok("match uncapped when cap is null", near(c3["retirement_match"], 5_000.0))


# ------------------------------------------------------------- 2. equity risk
def test_equity_risk():
    c = oc.compute_offer(oc.normalize_offer(variant(), 0))
    ok("equity EV = value x (1-risk) 10k@50%", near(c["equity_ev"], 5_000.0))
    c2 = oc.compute_offer(
        oc.normalize_offer(variant(equity_risk=0.0), 0))
    ok("equity EV full value at risk 0", near(c2["equity_ev"], 10_000.0))
    c3 = oc.compute_offer(
        oc.normalize_offer(variant(equity_risk=1.0, equity_annual_value=10_000), 0))
    ok("equity EV zero at risk 1", near(c3["equity_ev"], 0.0))


# ------------------------------------------------------------- 3. commute math
def test_commute():
    # 20 km each way, 3 days/wk, 0.30/km, 52 wk:
    # annual km = 20*2*3*52 = 6,240 -> cost = 1,872; parking 100*12 = 1,200
    c = oc.compute_offer(oc.normalize_offer(variant(), 0))
    ok("commute annual km = 6,240", near(c["commute_km_annual"], 6_240.0))
    ok("commute transport = $1,872", near(c["commute_transport_annual"], 1_872.0))
    ok("commute parking = $1,200", near(c["commute_parking_annual"], 1_200.0))
    ok("commute cost total = $3,072", near(c["commute_cost_annual"], 3_072.0))
    # hours: 2 * 3 * (20/28) = 4.2857... h/week
    exp_h = 2.0 * 3.0 * (20.0 / 28.0)
    ok("commute hours = 2*d*(km/28)", near(c["commute_hours_week"], exp_h))


# --------------------------------------------------------------- 4. PTO value
def test_pto():
    # true_daily_rate = true_comp / 260; pto_value = days * rate
    c = oc.compute_offer(oc.normalize_offer(variant(), 0))
    exp_rate = c["true_comp"] / 260.0
    ok("true daily rate = true comp / 260", near(c["true_daily_rate"], exp_rate))
    ok("PTO value = days x daily rate", near(c["pto_value"], 20.0 * exp_rate))


# ----------------------------------------------------------- 5. COL adjustment
def test_col():
    same = variant(commute_km_each_way=0, commute_days_per_week=0,
                   monthly_parking_or_transit=0)
    c100 = oc.compute_offer(oc.normalize_offer(dict(same, col_index=100), 0))
    c115 = oc.compute_offer(oc.normalize_offer(dict(same, col_index=115), 0))
    ok("COL 115 divides comp by 1.15", near(c115["true_comp"],
                                            c100["true_comp"] / 1.15))
    # gross comp must be identical before COL
    ok("gross identical across COL", near(c100["gross"], c115["gross"]))


# ------------------------------------------------------- 6. effective hourly
def test_effective_hourly():
    remote = oc.compute_offer(oc.normalize_offer(variant(
        commute_km_each_way=0, commute_days_per_week=0), 0))
    # real hours = 40; hourly = true_comp / (52*40)
    ok("effective hourly = true comp / (52 x real h)",
       near(remote["effective_hourly"], remote["true_comp"] / (52.0 * 40.0)))
    commuter = oc.compute_offer(oc.normalize_offer(variant(), 0))
    ok("commuter real hours > work hours",
       commuter["real_hours_week"] > commuter["work_hours_week"])


# --------------------------------------------------------------- 7. breakeven
def test_breakeven():
    # Two identical offers except base: breakeven base of the loser == winner's base
    a = variant(name="A", base=100_000)
    b = variant(name="B", base=110_000)
    offers = [oc.normalize_offer(o, i) for i, o in enumerate([a, b])]
    comps = [oc.compute_offer(o) for o in offers]
    target = comps[1]["true_comp"]
    bb = oc.solve_breakeven_base(offers[0], target)
    ok("breakeven base for identical shape = winner base",
       near(bb, 110_000.0, tol=1.0))
    # verify: recompute true comp at breakeven base
    tc = oc.true_comp_at_base(offers[0], bb)
    ok("true comp at breakeven base hits target", near(tc, target, tol=0.01))


# ------------------------------------------------------------- 8. JSON output
def test_json_output():
    offers = [variant(name="J1"), variant(name="J2", base=90_000)]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(offers, f)
        path = f.name
    r = subprocess.run([sys.executable, SCRIPT, "compare", "--file", path,
                        "--json"], capture_output=True, text=True)
    ok("compare --json exits 0", r.returncode == 0, r.stderr[:200])
    try:
        data = json.loads(r.stdout)
        ok("compare --json parses", True)
    except json.JSONDecodeError as e:
        ok("compare --json parses", False, str(e))
        return
    rows = data.get("rows") or data.get("offers") or []
    ok("json has >=2 offer rows", len(rows) >= 2)
    first = rows[0]
    for key in ("name", "gross", "true_comp", "effective_hourly"):
        ok(f"json row has '{key}'", key in first)
    os.unlink(path)


# -------------------------------------------------------- 9. CLI validation
def test_cli_validation():
    # single offer rejected
    r = subprocess.run(
        [sys.executable, SCRIPT, "compare", "--offer", json.dumps(variant())],
        capture_output=True, text=True)
    ok("single offer rejected (exit 2)", r.returncode == 2,
       f"rc={r.returncode} err={r.stderr[:120]}")
    # bad JSON rejected
    r = subprocess.run(
        [sys.executable, SCRIPT, "compare", "--offer", "{not json",
         "--offer", json.dumps(variant())],
        capture_output=True, text=True)
    ok("malformed JSON rejected (exit 2)", r.returncode == 2,
       f"rc={r.returncode}")
    # missing required field
    bad = variant()
    del bad["base"]
    r = subprocess.run(
        [sys.executable, SCRIPT, "compare", "--offer", json.dumps(bad),
         "--offer", json.dumps(variant())],
        capture_output=True, text=True)
    ok("missing 'base' rejected (exit 2)", r.returncode == 2, f"rc={r.returncode}")
    # duplicate names rejected
    r = subprocess.run(
        [sys.executable, SCRIPT, "compare", "--offer", json.dumps(variant()),
         "--offer", json.dumps(variant())],
        capture_output=True, text=True)
    ok("duplicate offer names rejected (exit 2)", r.returncode == 2,
       f"rc={r.returncode}")
    # breakeven requires exactly 2
    three = [variant(name=f"T{i}") for i in range(3)]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(three, f)
        path = f.name
    r = subprocess.run([sys.executable, SCRIPT, "breakeven", "--file", path],
                       capture_output=True, text=True)
    ok("breakeven with 3 offers rejected (exit 2)", r.returncode == 2,
       f"rc={r.returncode}")
    os.unlink(path)


# ---------------------------------------------------------------- 10. verdict
def test_verdict():
    # A dominates on money and hours; verdict should name A
    a = variant(name="GoodCo", base=120_000, commute_km_each_way=0,
                commute_days_per_week=0, health_premium_monthly=0)
    b = variant(name="BadCo", base=70_000, commute_km_each_way=50,
                commute_days_per_week=5, health_premium_monthly=500)
    offers = [oc.normalize_offer(o, i) for i, o in enumerate([a, b])]
    comps = [oc.compute_offer(o) for o in offers]
    v = oc.build_verdict(offers, comps)
    ok("verdict money winner = higher true comp offer",
       v["money_winner"] == "GoodCo")
    ok("verdict hours winner = fewer real hours offer",
       v["hours_winner"] == "GoodCo")
    ok("dominant offer detected", v["trade"]["type"] == "dominates")


if __name__ == "__main__":
    test_match_cap()
    test_equity_risk()
    test_commute()
    test_pto()
    test_col()
    test_effective_hourly()
    test_breakeven()
    test_json_output()
    test_cli_validation()
    test_verdict()
    print(f"\nALL TESTS PASSED ({PASS} assertions)")
