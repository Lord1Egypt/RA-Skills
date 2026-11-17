#!/usr/bin/env python3
"""new-car-otd-decoder — audit a new-car out-the-door quote line by line.

Modes:
  --demo                 run built-in demo quotes (padded purchase + marked-up lease)
  --quote quote.json     audit your quote (see quote.example.json for the shape)
  --lease ...            decode a lease: money factor -> effective APR + payment check
  --finance ...          amortize and compare two loan offers

Classifies each line FAIR / STATE-CAPPED / OVER-CAP / PADDED / REFUSE, computes
corrected OTD, and prices the padding. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------- known fees
# NOTE: keywords are distinctive two-word forms so add-on lines like
# "nitrogen tire fill" never collide with gov fees.
GOV_FEE_KEYWORDS = {
    "title": (5, 150, "state title fee"),
    "registration": (30, 400, "state registration (value/weight based)"),
    "plate transfer": (5, 60, "plate/transfer fee"),
    "plate fee": (5, 60, "plate/transfer fee"),
    "tire fee": (1, 20, "tire disposal fee"),
    "tire disposal": (1, 20, "tire disposal fee"),
    "battery fee": (1, 20, "battery fee"),
    "emissions": (10, 60, "emissions program fee"),
    "ev registration": (50, 300, "EV registration surcharge"),
}

# state doc-fee regimes: cap in USD (None = uncapped), typical market range
DOC_FEE_RULES = {
    # hard caps
    "CA": 85, "ND": 99, "NH": 100, "MN": 75, "AR": 90, "MD": 0,
    # mid caps
    "FL": 300, "WA": 200, "OR": 150, "CO": 300, "NE": 300, "KS": 300,
    "IA": 250, "MO": 250, "OK": 250, "WV": 250, "NY": 175, "MA": 175,
    # uncapped / market (typical band used for banding)
    "TX": None, "GA": None, "PA": None, "NJ": None, "MI": None, "OH": None, "IL": None,
}

# rebates taxed as income (tax computed on pre-rebate price)
REBATE_TAXED = {"TX", "NM"}

# trade-in does NOT reduce taxable base
NO_TRADE_CREDIT = {"CA", "DC", "HI", "MI", "VA"}

# classic add-ons: (typical charge low, high, fair value, verdict)
ADDONS = {
    "vin etch":              (195, 1995, 0,   "REFUSE"),
    "vin etching":           (195, 1995, 0,   "REFUSE"),
    "surface protection":    (295, 995,  20,  "REFUSE"),
    "paint sealant":         (295, 995,  25,  "REFUSE"),
    "fabric protection":     (195, 495,  0,   "REFUSE"),
    "nitrogen":              (29,  210,  0,   "REFUSE"),
    "nitrogen fill":         (29,  210,  0,   "REFUSE"),
    "appearance package":    (995, 4995, 0,   "AUDIT-UNBUNDLE"),
    "pro pack":              (995, 4995, 0,   "AUDIT-UNBUNDLE"),
    "market adjustment":     (1000, 50000, 0, "REFUSE"),
    "adm":                   (1000, 50000, 0, "REFUSE"),
    "dealer prep":           (99,  999,  0,   "REFUSE"),
    "dealer services":       (99,  999,  0,   "REFUSE"),
    "anti-theft":            (395, 895,  150, "PADDED"),
    "wheel locks":           (95,  295,  60,  "PADDED"),
    "floor mats":            (295, 695,  200, "PADDED"),
    "all-weather mats":      (295, 695,  200, "PADDED"),
    "mud flaps":             (150, 400,  100, "PADDED"),
    "splash guards":         (150, 400,  100, "PADDED"),
    "ceramic coating":       (495, 2495, 150, "PADDED"),
    "gap insurance":         (495, 1295, 60,  "PADDED"),  # ~$20-30/yr via auto insurer
    "gap":                   (495, 1295, 60,  "PADDED"),
    "key fob plan":          (295, 795,  150, "PADDED"),
    "tire and wheel":        (495, 1495, 400, "PADDED"),
    "tire & wheel":          (495, 1495, 400, "PADDED"),
    "maintenance plan":      (695, 1995, 400, "PADDED"),
    "extended warranty":     (1500, 4500, 1000, "PADDED"),
    "vsc":                   (1500, 4500, 1000, "PADDED"),
    "paint protection film": (995, 3995, 1200, "PADDED"),
    "ppf":                   (995, 3995, 1200, "PADDED"),
}

# lease lender fees that are real but must be disclosed
LEASE_FEES = {"acquisition fee": (395, 1195), "disposition fee": (295, 495)}


@dataclass
class Line:
    label: str
    amount: float
    verdict: str = ""
    reason: str = ""
    fair: float | None = None


@dataclass
class Audit:
    state: str = ""
    lines: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def add(self, label: str, amount: float, verdict: str, reason: str, fair=None):
        self.lines.append(Line(label, amount, verdict, reason, fair))

    @property
    def quoted_total(self) -> float:
        return sum(l.amount for l in self.lines if l.verdict != "INFO")

    @property
    def corrected_total(self) -> float:
        t = 0.0
        for l in self.lines:
            if l.verdict == "INFO":
                continue
            if l.verdict in ("REFUSE", "OVER-CAP"):
                t += 0 if l.verdict == "REFUSE" else (l.fair or 0)
            elif l.verdict == "PADDED":
                t += l.fair if l.fair is not None else l.amount
            else:
                t += l.amount
        return t

    @property
    def padding_found(self) -> float:
        return self.quoted_total - self.corrected_total

    def report(self) -> str:
        out = ["=" * 78, "OUT-THE-DOOR AUDIT", "=" * 78]
        if self.state:
            out.append(f"State: {self.state}  "
                       f"(doc-cap={DOC_FEE_RULES.get(self.state.upper(), '?')}, "
                       f"rebate-taxed={self.state.upper() in REBATE_TAXED}, "
                       f"trade-credit={'NO' if self.state.upper() in NO_TRADE_CREDIT else 'yes'})")
        out += ["", f"{'LINE':<38}{'CHARGED':>10}{'FAIR':>10}  VERDICT", "-" * 78]
        for l in self.lines:
            fair = f"{l.fair:,.0f}" if l.fair is not None else "—"
            out.append(f"{l.label[:37]:<38}{l.amount:>10,.0f}{fair:>10}  {l.verdict}")
            if l.reason:
                out.append(f"    ↳ {l.reason}")
        out += ["-" * 78]
        out.append(f"Quoted OTD:    ${self.quoted_total:>12,.2f}")
        out.append(f"Corrected OTD: ${self.corrected_total:>12,.2f}")
        out.append(f"PADDING FOUND: ${self.padding_found:>12,.2f}")
        for n in self.notes:
            out.append(f"• {n}")
        return "\n".join(out)


def classify_doc_fee(a: Audit, amount: float):
    st = (a.state or "??").upper()
    cap = DOC_FEE_RULES.get(st)
    if cap == 0:
        a.add("Documentation fee", amount, "REFUSE",
              "doc fees banned in MD — title charges only are legal")
    elif cap is None:
        if amount <= 450:
            a.add("Documentation fee", amount, "FAIR",
                  f"{st} uncapped — ${amount:.0f} is inside the $250-450 market band")
        else:
            a.add("Documentation fee", amount, "PADDED",
                  f"{st} uncapped — above the $250-450 market band; counter down",
                  fair=350.0)
    elif amount <= cap:
        a.add("Documentation fee", amount, "STATE-CAPPED",
              f"at/below {st} cap ${cap} — legitimate, absorb in negotiated price")
    else:
        a.add("Documentation fee", amount, "OVER-CAP",
              f"above {st} cap ${cap} — demand reduction to cap", fair=float(cap))


def classify_line(a: Audit, label: str, amount: float):
    low = label.lower().strip()
    # government fees
    for kw, (lo, hi, what) in GOV_FEE_KEYWORDS.items():
        if kw in low:
            if amount <= hi * 1.5:
                a.add(label, amount, "FAIR", what)
            else:
                a.add(label, amount, "PADDED",
                      f"{what} normally ${lo}-{hi} — challenge this", fair=float(hi))
            return
    if "doc" in low or "documentation" in low or "doc fee" in low:
        classify_doc_fee(a, amount)
        return
    if "sales tax" in low or "tax" == low:
        a.add(label, amount, "FAIR",
              "tax base check: should be (price − rebates − trade) in net-tax states")
        a.notes.append("Verify tax base vs your state's rebate/trade rules (references/state-rules.md).")
        return
    if any(k in low for k in ("rebate", "discount", "incentive", "credit", "trade")):
        a.add(label, -abs(amount), "FAIR", "reduces the price — verify it matches OEM program")
        return
    if "destination" in low or "delivery" in low and "charge" in low:
        a.add(label, amount, "FAIR", "fixed by manufacturer — not negotiable")
        return
    if "acquisition fee" in low or "disposition fee" in low:
        lo, hi = LEASE_FEES.get(low.split()[0] + " fee", (395, 995)) if False else (395, 1195)
        for k, v in LEASE_FEES.items():
            if k in low:
                lo, hi = v
        if amount <= hi:
            a.add(label, amount, "FAIR", f"lender fee within ${lo}-{hi} band — must be disclosed")
        else:
            a.add(label, amount, "PADDED", "above lender band — refuse the markup",
                  fair=float(hi))
        return
    # add-on catalog
    for kw, (lo, hi, fair, verdict) in ADDONS.items():
        if kw in low:
            if verdict == "REFUSE":
                a.add(label, amount, "REFUSE",
                      f"real value ≈ ${fair} — charged ${amount:,.0f}; refuse outright",
                      fair=0.0)
            elif verdict == "PADDED":
                a.add(label, amount, "PADDED",
                      f"real product, fair ≈ ${fair}; counter at fair value", fair=float(fair))
            else:
                a.add(label, amount, "AUDIT-UNBUNDLE",
                      "bundle — demand itemization, then audit each component", fair=0.0)
            return
    # price-ish lines (reference lines are INFO — excluded from totals)
    if "msrp" in low:
        a.add(label, amount, "INFO", "reference only — not part of what you pay")
        return
    if any(k in low for k in ("selling price", "vehicle price", "base price", "cap cost",
                              "capitalized cost", "negotiated price")):
        a.add(label, amount, "FAIR", "negotiated price line — the number you actually negotiated")
        return
    a.add(label, amount, "UNKNOWN",
          "not in catalog — ask what it is and whether it's state-mandated; default to refusing")


def audit_quote(q: dict) -> Audit:
    a = Audit(state=q.get("state", ""))
    for item in q["lines"]:
        classify_line(a, item["label"], float(item["amount"]))
    if q.get("deal_type") == "lease":
        a.notes.append("LEASE: demand residual, money factor, acquisition/disposition fees, "
                       "mileage cap + overage rate in writing before signing.")
    if (q.get("state", "").upper()) in NO_TRADE_CREDIT and q.get("has_trade"):
        a.notes.append(f"{q['state'].upper()}: trade-ins do NOT reduce sales tax — consider "
                       "selling privately (no tax penalty either way).")
    return a


# ------------------------------------------------------------------- lease
def lease_decode(mf: float, cap_cost: float, residual_pct: float, term: int,
                 tax_rate: float = 0.0, drive_off_cap_reduction: float = 0.0):
    """tax_rate is a fraction: 7.5% -> 0.075 (the CLI divides percent by 100)."""
    apr = mf * 24  # MF x 2400 = APR in %; /100 for fraction -> x 24
    residual = cap_cost * residual_pct / 100
    dep = (cap_cost - drive_off_cap_reduction - residual) / term
    rent = (cap_cost - drive_off_cap_reduction + residual) * mf
    base = dep + rent
    monthly = base * (1 + tax_rate)
    return {
        "effective_apr_pct": round(apr * 100, 3),
        "residual": round(residual, 2),
        "monthly_no_tax": round(base, 2),
        "monthly_with_tax": round(monthly, 2),
        "dep_component": round(dep, 2),
        "rent_component": round(rent, 2),
        "total_rent_charged": round(rent * term, 2),
    }


def lease_markup_cost(mf_bump: float, cap_cost: float, residual_pct: float, term: int):
    """$ cost of a dealer MF markup over the term."""
    r = residual_pct / 100
    bump_monthly = (cap_cost + cap_cost * r) * mf_bump
    return round(bump_monthly * term, 2)


# ---------------------------------------------------------------- finance
def amortize(principal: float, annual_rate: float, months: int):
    r = annual_rate / 100 / 12
    if r == 0:
        pay = principal / months
    else:
        pay = principal * r / (1 - (1 + r) ** -months)
    return round(pay, 2), round(pay * months - principal, 2)  # payment, total interest


DEMO_PURCHASE = {
    "state": "TX",
    "deal_type": "purchase",
    "has_trade": False,
    "lines": [
        {"label": "MSRP", "amount": 39995},
        {"label": "Selling price", "amount": 37500},
        {"label": "Manufacturer rebate", "amount": -3000},
        {"label": "Sales tax @ 8.25%", "amount": 2856},
        {"label": "Title, registration, plates", "amount": 218},
        {"label": "Documentation fee", "amount": 350},
        {"label": "VIN etching", "amount": 1495},
        {"label": "Surface protection package", "amount": 495},
        {"label": "Nitrogen tire fill", "amount": 210},
        {"label": "All-weather floor mats", "amount": 495},
        {"label": "Gap insurance", "amount": 795},
    ],
}

DEMO_LEASE = {
    "state": "OH",
    "deal_type": "lease",
    "lines": [
        {"label": "MSRP", "amount": 44000},
        {"label": "Cap cost", "amount": 41500},
        {"label": "Acquisition fee", "amount": 995},
        {"label": "Disposition fee", "amount": 395},
    ],
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--demo", action="store_true", help="run built-in demo quotes")
    p.add_argument("--quote", help="path to quote.json (see quote.example.json)")
    p.add_argument("--lease", nargs=5, metavar=("MF", "CAP", "RES%", "TERM", "TAX%"),
                   help="decode lease: e.g. 0.00145 41500 58 36 7.5")
    p.add_argument("--lease-markup", nargs=4, metavar=("MF_BUMP", "CAP", "RES%", "TERM"),
                   help="cost of dealer MF markup: e.g. 0.0004 41500 58 36")
    p.add_argument("--finance", nargs=4, metavar=("PRINCIPAL", "RATE%", "MONTHS", "ALT_RATE%"),
                   help="compare two loans: principal, rate1, months, rate2")
    args = p.parse_args()

    if args.demo:
        print(AuditReport := audit_quote(DEMO_PURCHASE).report())
        print()
        print(audit_quote(DEMO_LEASE).report())
        print()
        print("LEASE DEMO: MF 0.00145, cap $41,500, residual 58%, 36mo, tax 7.5%")
        for k, v in lease_decode(0.00145, 41500, 58, 36, 0.075).items():
            print(f"  {k:<24}{v}")
        print("\nMARKUP COST: bump 0.00040 over the term:")
        print(f"  ${lease_markup_cost(0.0004, 41500, 58, 36):,.2f} extra rent charge")
        print("\nFINANCE DEMO: $32,356 @ 5.5% vs 7.9%, 60 mo")
        p1, i1 = amortize(32356, 5.5, 60)
        p2, i2 = amortize(32356, 7.9, 60)
        print(f"  5.5%: ${p1}/mo, interest ${i1:,}")
        print(f"  7.9%: ${p2}/mo, interest ${i2:,}   <- dealer bump costs ${i2 - i1:,}")
        return

    if args.quote:
        with open(args.quote) as f:
            q = json.load(f)
        print(audit_quote(q).report())
        return

    if args.lease:
        mf, cap, res, term, tax = map(float, args.lease)
        print(json.dumps(lease_decode(mf, cap, res, int(term), tax / 100.0), indent=2))
        return

    if args.lease_markup:
        bump, cap, res, term = map(float, args.lease_markup)
        print(f"MF markup of {bump:.5f} costs ${lease_markup_cost(bump, cap, res, int(term)):,.2f} "
              f"over {int(term)} months")
        return

    if args.finance:
        principal, r1, months, r2 = map(float, args.finance)
        p1, i1 = amortize(principal, r1, int(months))
        p2, i2 = amortize(principal, r2, int(months))
        print(f"Loan A {r1}%: ${p1}/mo | interest ${i1:,.2f}")
        print(f"Loan B {r2}%: ${p2}/mo | interest ${i2:,.2f}")
        print(f"Difference: ${abs(i2 - i1):,.2f} total interest")
        return

    p.print_help()


if __name__ == "__main__":
    main()
