#!/usr/bin/env python3
"""
MLM Income Calculator
Projects potential earnings based on team size and activity.
"""

import sys
import json

def calculate_enagic_income(personal_sales_monthly, team_size, avg_team_sales):
    """Calculate projected Enagic income."""
    
    # Commission per point
    COMMISSION_PER_POINT = 285
    
    # Average points per sale (assuming mix of K8 and SD501)
    AVG_POINTS_PER_SALE = 6.5
    
    # Personal income
    personal_points = personal_sales_monthly * AVG_POINTS_PER_SALE
    personal_income = personal_points * COMMISSION_PER_POINT
    
    # Team override (simplified - actual comp plan is more complex)
    # Assume 1 point override per team sale at higher ranks
    team_override_per_sale = 285 if team_size >= 10 else 0
    team_income = team_size * avg_team_sales * team_override_per_sale
    
    total_monthly = personal_income + team_income
    total_annual = total_monthly * 12
    
    return {
        "personal_sales": personal_sales_monthly,
        "personal_income": personal_income,
        "team_size": team_size,
        "team_income": team_income,
        "total_monthly": total_monthly,
        "total_annual": total_annual,
        "disclaimer": "PROJECTED INCOME ONLY. Actual results vary significantly. See income disclosure."
    }


def calculate_generic_mlm_income(
    personal_volume,
    commission_rate,
    team_size,
    avg_team_volume,
    override_rate
):
    """Calculate projected income for any MLM."""
    
    personal_income = personal_volume * commission_rate
    team_income = team_size * avg_team_volume * override_rate
    total_monthly = personal_income + team_income
    
    return {
        "personal_volume": personal_volume,
        "personal_income": personal_income,
        "team_size": team_size,
        "team_income": team_income,
        "total_monthly": total_monthly,
        "total_annual": total_monthly * 12,
        "disclaimer": "PROJECTED INCOME ONLY. Actual results vary significantly. See income disclosure."
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: income-calculator.py <company> [args]")
        print("  enagic <personal_sales> <team_size> <avg_team_sales>")
        print("  generic <personal_vol> <commission_rate> <team_size> <avg_team_vol> <override_rate>")
        sys.exit(1)
    
    company = sys.argv[1].lower()
    
    if company == "enagic":
        personal = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        team = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        avg = float(sys.argv[4]) if len(sys.argv) > 4 else 1
        result = calculate_enagic_income(personal, team, avg)
    else:
        # Generic calculation
        pv = float(sys.argv[2]) if len(sys.argv) > 2 else 500
        cr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
        ts = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        atv = float(sys.argv[5]) if len(sys.argv) > 5 else 200
        ovr = float(sys.argv[6]) if len(sys.argv) > 6 else 0.05
        result = calculate_generic_mlm_income(pv, cr, ts, atv, ovr)
    
    print(json.dumps(result, indent=2))
