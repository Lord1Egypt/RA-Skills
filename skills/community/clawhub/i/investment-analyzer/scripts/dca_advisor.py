#!/usr/bin/env python3
import json
import argparse

BIWEEKLY = 1940
TFSA_ANNUAL = 7000
RRSP_ANNUAL_EST = 16200
EMERGENCY_TARGET = 9000
SHERBROOKE_DOWN = 90000
MORTGAGE_RATE = 0.0539
ETF_EXPECTED = 0.15
LOC_RATE = 0.0495


def advise(
    emergency_fund=0,
    tfsa_room=TFSA_ANNUAL,
    rrsp_room=RRSP_ANNUAL_EST,
    loc_balance=0,
    saving_for_property=False,
    down_payment_saved=0,
):
    remaining = BIWEEKLY
    allocations = []
    flags = []

    tfsa_biweekly = round(TFSA_ANNUAL / 26)
    rrsp_biweekly = round(RRSP_ANNUAL_EST / 26)

    if emergency_fund < EMERGENCY_TARGET:
        needed = EMERGENCY_TARGET - emergency_fund
        per_period = min(remaining, round(needed / 6))
        allocations.append({
            "bucket": "🛡️ Emergency Fund",
            "amount": per_period,
            "reason": f"Build to ${EMERGENCY_TARGET:,} (3 months expenses). Currently ${emergency_fund:,}. Priority #1."
        })
        remaining -= per_period
        flags.append("⚠️ Emergency fund not complete — do this before anything else.")

    if tfsa_room > 0 and remaining > 0:
        amount = min(remaining, tfsa_biweekly)
        allocations.append({
            "bucket": "🏦 TFSA (HXQ)",
            "amount": amount,
            "reason": f"Max TFSA first — gains are 100% tax-free. ~${tfsa_biweekly}/bi-weekly to hit ${TFSA_ANNUAL:,}/yr limit."
        })
        remaining -= amount

    if rrsp_room > 0 and remaining > 0:
        if remaining >= 200:
            amount = min(remaining, rrsp_biweekly)
            allocations.append({
                "bucket": "📋 RRSP (HXQ)",
                "amount": amount,
                "reason": f"RRSP contribution = immediate ~46% tax refund on contribution. Est. room ~${RRSP_ANNUAL_EST:,}/yr."
            })
            remaining -= amount

    if loc_balance > 0 and remaining > 0:
        loc_roi = LOC_RATE
        if loc_roi >= ETF_EXPECTED * 0.5:
            amount = min(remaining, round(loc_balance / 12))
            allocations.append({
                "bucket": "💳 LOC Paydown",
                "amount": amount,
                "reason": f"LOC at {LOC_RATE*100:.2f}% — lower priority than ETF (~15% expected), but reduce balance if large."
            })
            remaining -= amount

    if saving_for_property and remaining > 0:
        still_needed = max(0, SHERBROOKE_DOWN - down_payment_saved)
        if still_needed > 0:
            amount = min(remaining, round(still_needed / 12))
            allocations.append({
                "bucket": "🏠 Down Payment Reserve (Sherbrooke)",
                "amount": amount,
                "reason": f"Targeting Sherbrooke triplex — need ${SHERBROOKE_DOWN:,} down. Saved: ${down_payment_saved:,}."
            })
            remaining -= amount

    if remaining > 0:
        allocations.append({
            "bucket": "📈 HXQ (Taxable)",
            "amount": remaining,
            "reason": "Remaining capital — DCA into HXQ in taxable account."
        })

    total_to_invest = sum(a["amount"] for a in allocations if "HXQ" in a["bucket"] or "TFSA" in a["bucket"] or "RRSP" in a["bucket"])
    invest_pct = round(total_to_invest / BIWEEKLY * 100)

    return {
        "biweekly_income": BIWEEKLY,
        "allocations": allocations,
        "summary": {
            "total_to_invest_etf": total_to_invest,
            "invest_pct": invest_pct,
            "verdict": f"Invest {invest_pct}% of each paycheck (${total_to_invest}) into HXQ across TFSA/RRSP/taxable."
        },
        "flags": flags,
        "key_unknowns": [k for k, v in {
            "TFSA room": tfsa_room == TFSA_ANNUAL,
            "RRSP room": rrsp_room == RRSP_ANNUAL_EST,
            "Emergency fund": emergency_fund == 0,
            "LOC balance": loc_balance == 0,
        }.items() if v],
        "note": "Update references/criteria.md with actual TFSA/RRSP/emergency fund values for precise advice."
    }


def main():
    parser = argparse.ArgumentParser(description="DCA allocation advisor.")
    parser.add_argument("--emergency-fund", type=float, default=0, help="Current emergency fund balance")
    parser.add_argument("--tfsa-room", type=float, default=TFSA_ANNUAL, help="Remaining TFSA contribution room")
    parser.add_argument("--rrsp-room", type=float, default=RRSP_ANNUAL_EST, help="Remaining RRSP contribution room")
    parser.add_argument("--loc-balance", type=float, default=0, help="Current LOC outstanding balance")
    parser.add_argument("--saving-for-property", action="store_true", help="Flag: actively saving for Sherbrooke down payment")
    parser.add_argument("--down-payment-saved", type=float, default=0, help="Down payment already saved")
    args = parser.parse_args()

    result = advise(
        emergency_fund=args.emergency_fund,
        tfsa_room=args.tfsa_room,
        rrsp_room=args.rrsp_room,
        loc_balance=args.loc_balance,
        saving_for_property=args.saving_for_property,
        down_payment_saved=args.down_payment_saved,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

