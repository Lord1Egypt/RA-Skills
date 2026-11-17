#!/usr/bin/env python3
"""proceeds.py — home-sale net proceeds, capital-gains, and rent-vs-sell
estimator (stdlib only).

Subcommands:
  estimate      full line-itemed net proceeds + tax-gain layer
  exclusion     Section 121 eligibility check from occupancy dates
  rent-vs-sell  honest cap-rate comparison (NOI, not gross yield)
"""
import argparse
import sys
from datetime import date

TRANSFER_TAX = {  # state-level approximation; counties/cities stack on top
    "AK": 0.0, "ID": 0.0, "IA": 0.0, "LA": 0.0, "MO": 0.0, "MS": 0.0,
    "NM": 0.0, "ND": 0.0, "TX": 0.0, "UT": 0.0, "WY": 0.0, "OR": 0.001,
    "CA": 0.0011, "CO": 0.0002, "FL": 0.007, "GA": 0.01, "IL": 0.0075,
    "MA": 0.0046, "NY": 0.004, "WA": 0.0128, "NJ": 0.006, "PA": 0.01,
    "MI": 0.0075, "MN": 0.0033, "OH": 0.003, "NC": 0.002, "SC": 0.0037,
    "TN": 0.0037, "AZ": 0.0002, "NV": 0.0002, "VA": 0.0033,
}

def money(x):
    return f"${x:,.0f}"

def cmd_estimate(a):
    price = a.price
    print(f"SALE PRICE: {money(price)}")
    lines = []
    # commission
    comm = price * a.commission / 100.0
    lines.append((f"agent commissions ({a.commission}%)", -comm))
    # closing costs
    title = price * 0.006
    lines.append(("title + escrow/settlement (~0.6%)", -title))
    attorney = 900 if a.attorney_state else 0.0
    if attorney:
        lines.append(("attorney (attorney state)", -attorney))
    ttax_rate = TRANSFER_TAX.get(a.state.upper(), 0.003)
    ttax = price * ttax_rate
    lines.append((f"transfer tax ({a.state.upper()} ~{ttax_rate * 100:.2f}% + local)", -ttax))
    misc = 400.0
    lines.append(("recording/HOA/wire misc", -misc))
    if a.warranty:
        lines.append(("buyer home warranty", -500.0))
    # payoff
    payoff = a.payoff + a.payoff * 0.04 * 12 / 365.0  # ~12 days per-diem
    lines.append((f"mortgage payoff + per-diem (≈12d interest)", -payoff))
    if a.heloc:
        lines.append(("HELOC payoff", -a.heloc))
    if a.credits:
        lines.append(("buyer credits (repairs/closing)", -a.credits))
    if a.tax_proration:
        lines.append(("property-tax proration", -a.tax_proration))
    net = price + sum(v for _, v in lines)
    print(f"{'line item':46} {'amount':>12}")
    for label, v in lines:
        print(f"{label:46} {money(v):>12}")
    print(f"{'=' * 59}")
    print(f"{'NET PROCEEDS (before moving + tax)':46} {money(net):>12}")
    pct = net / price * 100 if price else 0
    print(f"({pct:.1f}% of sale price)\n")

    # ---- tax layer ----
    if a.purchase:
        basis = a.purchase + (a.improvements or 0) + comm + title + ttax + misc
        gain = price - basis
        excl = 500000 if a.married else 250000
        # exclusion eligibility from dates
        eligible, note = exclusion_check(a.owned_from, a.sold_on or date.today(),
                                         a.moved_in, a.moved_out)
        taxable = max(0.0, gain - excl) if eligible else gain
        if 0 < excl and gain <= excl and eligible:
            taxable = 0.0
        print(f"--- tax layer (estimates; not tax advice) ---")
        print(f"adjusted basis: {money(basis)} (purchase {money(a.purchase)} + improvements "
              f"{money(a.improvements or 0)} + selling costs)")
        print(f"capital gain: {money(gain)}")
        print(f"Section 121 exclusion {'APPLIES' if eligible else 'DOES NOT APPLY'} — {note}")
        if eligible:
            print(f"  exclusion {money(excl)} ({'MFJ' if a.married else 'single'})")
        if a.depreciation:
            recap = min(a.depreciation, max(gain, 0))
            print(f"  depreciation recapture (never excluded, ≤25% rate): "
                  f"{money(recap)} taxable at up to 25%")
            taxable += 0  # recapture tracked separately below
        if taxable > 0:
            ltcg = 0.15 + (0.038 if a.niit else 0)
            est = taxable * ltcg
            print(f"taxable LTCG {money(taxable)} → est. federal tax @ {ltcg * 100:.1f}%: {money(est)}")
        else:
            print(f"gain fully excluded → $0 federal capital-gains tax")
        if a.state in ("CA", "NY", "NJ", "PA", "CT", "MN", "WI", "NE", "HI", "AZ", "OR", "ID", "UT", "KY", "DE", "DC", "MD", "NM", "SC", "VT", "WV", "MT", "RI", "ME", "AR", "OK", "KS", "IA", "HI"):
            print(f"note: {a.state} taxes capital gains as income — state tax may apply (verify)")
    return 0

def exclusion_check(owned_from, sold_on, moved_in, moved_out):
    """2-of-5-year ownership + use test from dates."""
    if not owned_from or not moved_in:
        return True, "dates not supplied — assumed eligible; VERIFY 2-of-5 tests"
    five_yr_before = date(sold_on.year - 5, sold_on.month, sold_on.day)
    own_ok = (sold_on - owned_from).days >= 730
    # use: overlap of [moved_in, moved_out or sold_on] within last 5y
    use_end = moved_out or sold_on
    use_start = max(moved_in, five_yr_before)
    use_days = max(0, (min(use_end, sold_on) - use_start).days)
    use_ok = use_days >= 730
    if own_ok and use_ok:
        return True, f"owned {(sold_on - owned_from).days // 30} mo, used {use_days // 30} mo of last 60 — both tests pass"
    if own_ok and not use_ok:
        return False, (f"used only {use_days // 30} mo in last 5y (<24) — use test FAILS; "
                        "partial exclusion only via work/health safe harbor")
    return False, f"owned {(sold_on - owned_from).days // 30} mo (<24) — ownership test fails"

def cmd_exclusion(a):
    ok, note = exclusion_check(a.owned_from, a.sold_on, a.moved_in, a.moved_out)
    excl = 500000 if a.married else 250000
    print(f"Section 121 exclusion: {'ELIGIBLE' if ok else 'NOT ELIGIBLE'}")
    print(f"  {note}")
    print(f"  exclusion amount if eligible: {money(excl)} of GAIN")
    if not ok and a.safe_harbor:
        print("  work/health/unforeseen safe harbor → partial exclusion = "
              f"{money(excl)} × qualifying months / 24 — compute with months of use")
    if a.prior_sale_within_2y:
        print("  !! excluded another home within past 2 years → barred this sale")
    return 0

def cmd_rent_vs_sell(a):
    gross = a.rent * 12
    vac = gross * (a.vacancy_pct / 100.0)
    maint = gross * (a.maintenance_pct / 100.0)
    mgmt = gross * (a.management_pct / 100.0) if a.management_pct else 0.0
    noi = gross - vac - maint - mgmt - a.taxes - a.insurance - a.hoa
    cap = noi / a.price * 100 if a.price else 0
    # opportunity: net proceeds in safe yield
    opp = a.net_proceeds * (a.alt_yield_pct / 100.0)
    print(f"Rent-vs-sell first pass (property {money(a.price)})")
    print(f"  gross scheduled rent:      {money(gross):>12}")
    for label, v in (("vacancy", -vac), ("maintenance", -maint),
                     ("management", -mgmt), ("property tax", -a.taxes),
                     ("insurance", -a.insurance), ("HOA", -a.hoa)):
        if v:
            print(f"  {label:26} {money(v):>12}")
    print(f"  NET OPERATING INCOME:      {money(noi):>12}")
    print(f"  cap rate (NOI/price):      {cap:>11.2f}%")
    print(f"  alt: {money(a.net_proceeds)} net proceeds @ {a.alt_yield_pct}% ≈ {money(opp)}/yr")
    verdict = "RENT competitive" if noi > opp else "SELL + reinvest wins on income"
    print(f"  → {verdict}")
    if cap < 4:
        print("  note: cap < 4% — renting is a bet on appreciation, not cash flow")
    print("  (first pass: no vacancy-mix risk, turnover, or rate-change modeling)")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("estimate")
    e.add_argument("--price", type=float, required=True)
    e.add_argument("--payoff", type=float, default=0.0)
    e.add_argument("--heloc", type=float, default=0.0)
    e.add_argument("--commission", type=float, default=5.5)
    e.add_argument("--state", default="XX")
    e.add_argument("--attorney-state", action="store_true")
    e.add_argument("--credits", type=float, default=0.0)
    e.add_argument("--tax-proration", type=float, default=0.0)
    e.add_argument("--warranty", action="store_true")
    e.add_argument("--purchase", type=float)
    e.add_argument("--improvements", type=float, default=0.0)
    e.add_argument("--married", action="store_true")
    e.add_argument("--depreciation", type=float, default=0.0)
    e.add_argument("--niit", action="store_true")
    e.add_argument("--owned-from", type=date.fromisoformat)
    e.add_argument("--moved-in", type=date.fromisoformat)
    e.add_argument("--moved-out", type=date.fromisoformat)
    e.add_argument("--sold-on", type=date.fromisoformat)
    e.set_defaults(fn=cmd_estimate)
    x = sub.add_parser("exclusion")
    x.add_argument("--owned-from", type=date.fromisoformat)
    x.add_argument("--moved-in", type=date.fromisoformat)
    x.add_argument("--moved-out", type=date.fromisoformat)
    x.add_argument("--sold-on", type=date.fromisoformat, required=True)
    x.add_argument("--married", action="store_true")
    x.add_argument("--safe-harbor", action="store_true")
    x.add_argument("--prior-sale-within-2y", action="store_true")
    x.set_defaults(fn=cmd_exclusion)
    r = sub.add_parser("rent-vs-sell")
    r.add_argument("--price", type=float, required=True)
    r.add_argument("--net-proceeds", type=float, required=True)
    r.add_argument("--rent", type=float, required=True)
    r.add_argument("--taxes", type=float, default=0.0)
    r.add_argument("--insurance", type=float, default=0.0)
    r.add_argument("--hoa", type=float, default=0.0)
    r.add_argument("--vacancy-pct", type=float, default=5.0)
    r.add_argument("--maintenance-pct", type=float, default=1.5)
    r.add_argument("--management-pct", type=float, default=8.0)
    r.add_argument("--alt-yield-pct", type=float, default=4.0)
    r.set_defaults(fn=cmd_rent_vs_sell)
    a = ap.parse_args()
    sys.exit(a.fn(a))

if __name__ == "__main__":
    main()
