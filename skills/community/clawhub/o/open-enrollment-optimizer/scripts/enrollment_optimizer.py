#!/usr/bin/env python3
"""open-enrollment-optimizer — true-annual-cost modeling for benefits elections.

Modes:
  --demo                 built-in PPO vs HDHP family comparison + crossover
  --plans plans.json     compare your plans (see plans.example.json)
  --fsa E SPEND TAX      FSA election math: forfeiture risk vs tax saved
  --hsa CONTRIB YEARS RET TAX   HSA vs taxable investing over a horizon

Stdlib only.
"""
from __future__ import annotations

import argparse
import json

# ------------------------------------------------------------- plan engine

def medical_spend(claims: float, deductible: float, coins: float, oop_max: float) -> float:
    """Patient share of deductible-eligible claims, capped at OOP max."""
    if claims <= 0:
        return 0.0
    if claims <= deductible:
        pay = claims
    else:
        pay = deductible + (claims - deductible) * coins
    return min(pay, oop_max)


def true_annual_cost(plan: dict, claims: float, months: int = 12,
                     pretax_premium: bool = False, marginal_tax: float = 0.30) -> float:
    prem = plan["monthly_premium"] * months
    if pretax_premium:
        prem *= (1 - marginal_tax)
    spend = medical_spend(claims, plan["deductible"], plan["coinsurance"],
                          plan["oop_max"])
    # copay-based add-ons: expected visits x copay
    for label, (copay, visits) in plan.get("copays", {}).items():
        spend += copay * visits.get("per_year", 0)
    spend = min(spend, plan["oop_max"])  # copays count toward the max on ACA plans
    seed = plan.get("hsa_seed", 0)
    return prem + spend - seed


SCENARIOS = {"healthy": 600.0, "typical": 3200.0, "bad-luck": 18000.0}


def compare(plans: list, scenarios=None, **kw) -> dict:
    scenarios = scenarios or SCENARIOS
    out = {}
    for name, claims in scenarios.items():
        costs = {p["name"]: round(true_annual_cost(p, claims, **kw), 2) for p in plans}
        winner = min(costs, key=costs.get)
        out[name] = {"claims": claims, "costs": costs, "winner": winner}
    return out


def crossover(plan_a: dict, plan_b: dict, lo: float = 0.0, hi: float = 150000.0,
              tol: float = 1.0) -> float | None:
    """Claims amount where TAC(A) == TAC(B); None if one dominates everywhere."""
    def diff(c):
        return true_annual_cost(plan_a, c) - true_annual_cost(plan_b, c)
    d_lo, d_hi = diff(lo), diff(hi)
    if d_lo * d_hi > 0:
        return None  # no crossing in range: one plan wins everywhere
    for _ in range(60):
        mid = (lo + hi) / 2
        d_mid = diff(mid)
        if abs(d_mid) < 0.01 or (hi - lo) < tol:
            return round(mid, 0)
        if d_lo * d_mid <= 0:
            hi = mid
        else:
            lo, d_lo = mid, d_mid
    return round((lo + hi) / 2, 0)


def robust_pick(results: dict) -> str:
    wins: dict[str, int] = {}
    for sc in results.values():
        wins[sc["winner"]] = wins.get(sc["winner"], 0) + 1
    return max(wins, key=wins.get)


# ------------------------------------------------------------ FSA election

def fsa_math(election: float, expected_spend: float, tax_rate: float,
             carryover: float = 0.0, p_underspend: float = 0.25):
    """Tax saved vs forfeiture exposure. tax_rate as percent (32 = 32%)."""
    tr = tax_rate / 100
    usable = min(election, expected_spend)
    tax_saved = usable * tr
    at_risk = max(0.0, election - max(expected_spend, carryover)) * p_underspend
    net = tax_saved - at_risk
    # break-even utilization: fraction of election you must spend to come out ahead
    beu = None
    if election > 0:
        # solve election*u*tr = (election - election*u)*p  ->  u = p/(tr+p)
        beu = round(p_underspend / (tr + p_underspend), 3)
    return {
        "election": election,
        "tax_saved_if_used": round(tax_saved, 2),
        "expected_forfeiture": round(at_risk, 2),
        "expected_net": round(net, 2),
        "verdict": "GOOD BET" if net > 0 else "SHRINK ELECTION",
        "break_even_utilization": beu,
        "note": f"You must spend >{beu*100:.0f}% of the election for FSA to beat paying cash."
                if beu else "",
    }


# --------------------------------------------------------------- HSA engine

def hsa_vs_taxable(contrib: float, years: int, ret_pct: float, tax_pct: float):
    """Balance after N years: HSA (never taxed) vs taxable (dividends+gains taxed)."""
    r = ret_pct / 100
    t = tax_pct / 100
    hsa = 0.0
    taxable = 0.0
    basis = 0.0
    for _ in range(years):
        hsa = (hsa + contrib) * (1 + r)
        taxable = (taxable + contrib) * (1 + r * (1 - t * 0.5))  # ~50% drag: annual div + LT cap at withdrawal
    return {
        "years": years,
        "annual_contribution": contrib,
        "hsa_balance": round(hsa, 2),
        "taxable_balance": round(taxable, 2),
        "advantage": round(hsa - taxable, 2),
    }


# ------------------------------------------------------------------ demo

DEMO_PLANS = [
    {
        "name": "PPO",
        "monthly_premium": 520, "deductible": 1500, "coinsurance": 0.20, "oop_max": 6000,
        "copays": {},
    },
    {
        "name": "HDHP+HSA",
        "monthly_premium": 360, "deductible": 3000, "coinsurance": 0.20, "oop_max": 8000,
        "copays": {}, "hsa_seed": 1000,
    },
]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--demo", action="store_true")
    p.add_argument("--plans", help="plans JSON file")
    p.add_argument("--fsa", nargs=3, metavar=("ELECTION", "SPEND", "TAX%"),
                   help="FSA math: e.g. 1600 1400 32")
    p.add_argument("--hsa", nargs=4, metavar=("CONTRIB", "YEARS", "RET%", "TAX%"),
                   help="HSA vs taxable: e.g. 4300 8 25 15")
    args = p.parse_args()

    if args.demo or args.plans:
        plans = DEMO_PLANS
        if args.plans:
            with open(args.plans) as f:
                plans = json.load(f)
        results = compare(plans)
        print(f"{'SCENARIO':<10}{'CLAIMS':>9}", end="")
        for pl in plans:
            print(f"{pl['name']:>14}", end="")
        print("   WINNER")
        print("-" * (29 + 14 * len(plans)))
        for sc, r in results.items():
            print(f"{sc:<10}{r['claims']:>9,.0f}", end="")
            for pl in plans:
                print(f"{r['costs'][pl['name']]:>14,.0f}", end="")
            print(f"   {r['winner']}")
        print()
        if len(plans) >= 2:
            for i in range(len(plans) - 1):
                x = crossover(plans[i], plans[i + 1])
                a, b = plans[i]["name"], plans[i + 1]["name"]
                if x is None:
                    d = true_annual_cost(plans[i], 8000) - true_annual_cost(plans[i+1], 8000)
                    dom = a if d < 0 else b
                    print(f"CROSSOVER {a} vs {b}: none — {dom} wins across the whole range")
                else:
                    print(f"CROSSOVER {a} vs {b}: ${x:,.0f}/yr in claims — "
                          f"below: cheaper plan flips at this point")
        print(f"\nROBUST PICK: {robust_pick(results)} (most scenario wins)")
        return

    if args.fsa:
        e, s, t = map(float, args.fsa)
        print(json.dumps(fsa_math(e, s, t), indent=2))
        return

    if args.hsa:
        c, y, r, t = map(float, args.hsa)
        print(json.dumps(hsa_vs_taxable(c, int(y), r, t), indent=2))
        return

    p.print_help()


if __name__ == "__main__":
    main()
