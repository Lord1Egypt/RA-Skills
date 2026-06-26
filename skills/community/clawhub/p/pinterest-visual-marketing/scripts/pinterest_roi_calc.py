#!/usr/bin/env python3
"""
Pinterest Organic ROI Calculator.

Estimates monthly revenue from Pinterest organic traffic based on
impressions, click-through rate, conversion rate, and AOV.

Usage:
    python3 pinterest_roi_calc.py --monthly-impressions 50000 --ctr 1.0 --cvr 2.5 --aov 65
    python3 pinterest_roi_calc.py --monthly-impressions 100000 --ctr 1.5 --cvr 3.0 --aov 45 --months 12
"""

import argparse


def calculate_roi(
    monthly_impressions: int,
    ctr_pct: float,
    cvr_pct: float,
    aov: float,
    months: int = 12,
) -> dict:
    ctr = ctr_pct / 100.0
    cvr = cvr_pct / 100.0

    monthly_clicks = monthly_impressions * ctr
    monthly_orders = monthly_clicks * cvr
    monthly_revenue = monthly_orders * aov

    annual_clicks = monthly_clicks * months
    annual_orders = monthly_orders * months
    annual_revenue = monthly_revenue * months

    return {
        "monthly_impressions": monthly_impressions,
        "ctr_pct": ctr_pct,
        "cvr_pct": cvr_pct,
        "aov": aov,
        "months": months,
        "monthly_clicks": round(monthly_clicks, 1),
        "monthly_orders": round(monthly_orders, 1),
        "monthly_revenue": round(monthly_revenue, 2),
        "annual_clicks": round(annual_clicks, 1),
        "annual_orders": round(annual_orders, 1),
        "annual_revenue": round(annual_revenue, 2),
    }


def format_report(r: dict) -> str:
    lines = [
        "",
        "=" * 55,
        "  PINTEREST ORGANIC ROI ESTIMATE",
        "=" * 55,
        "",
        f"  Monthly impressions:    {r['monthly_impressions']:>12,}",
        f"  Click-through rate:     {r['ctr_pct']:>11.1f}%",
        f"  Conversion rate:        {r['cvr_pct']:>11.1f}%",
        f"  Average order value:    ${r['aov']:>10.2f}",
        "",
        "-" * 55,
        "  MONTHLY ESTIMATES",
        "-" * 55,
        f"  Clicks to store:        {r['monthly_clicks']:>12,.0f}",
        f"  Orders:                 {r['monthly_orders']:>12,.1f}",
        f"  Revenue:                ${r['monthly_revenue']:>11,.2f}",
        "",
        "-" * 55,
        f"  {r['months']}-MONTH PROJECTION",
        "-" * 55,
        f"  Total clicks:           {r['annual_clicks']:>12,.0f}",
        f"  Total orders:           {r['annual_orders']:>12,.1f}",
        f"  Total revenue:          ${r['annual_revenue']:>11,.2f}",
        "",
        "-" * 55,
        "  NOTES",
        "-" * 55,
        "  - Pinterest traffic compounds: older Pins continue",
        "    driving clicks for months/years (unlike social posts).",
        "  - Add Rijoy loyalty to convert Pinterest visitors into",
        "    repeat buyers — even a 10% repeat rate doubles LTV.",
        "  - Use UTM parameters on all Pin links for attribution.",
        "",
        "=" * 55,
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Estimate revenue from Pinterest organic traffic"
    )
    parser.add_argument(
        "--monthly-impressions", type=int, required=True,
        help="Monthly Pin impressions",
    )
    parser.add_argument(
        "--ctr", type=float, required=True,
        help="Click-through rate (percentage, e.g. 1.0 for 1%%)",
    )
    parser.add_argument(
        "--cvr", type=float, required=True,
        help="Conversion rate (percentage, e.g. 2.5 for 2.5%%)",
    )
    parser.add_argument(
        "--aov", type=float, required=True,
        help="Average order value (USD)",
    )
    parser.add_argument(
        "--months", type=int, default=12,
        help="Projection period in months (default: 12)",
    )
    args = parser.parse_args()

    result = calculate_roi(
        monthly_impressions=args.monthly_impressions,
        ctr_pct=args.ctr,
        cvr_pct=args.cvr,
        aov=args.aov,
        months=args.months,
    )
    print(format_report(result))


if __name__ == "__main__":
    main()
