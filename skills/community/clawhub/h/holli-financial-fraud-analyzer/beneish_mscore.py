#!/usr/bin/env python3
"""
Beneish M-Score calculator
Input: JSON file with t and t_1 period fields
Output: JSON with component ratios and M-score

Usage:
  python scripts/beneish_mscore.py --input sample.json
"""

import argparse
import json
from typing import Dict, Any


def safe_div(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b


def getv(d: Dict[str, Any], key: str) -> float:
    if key not in d:
        raise KeyError(f"Missing field: {key}")
    return float(d[key])


def calc(data: Dict[str, Any]) -> Dict[str, Any]:
    t = data["t"]
    p = data["t_1"]

    dsri = safe_div(safe_div(getv(t, "receivables"), getv(t, "sales")), safe_div(getv(p, "receivables"), getv(p, "sales")))

    gm_t = safe_div((getv(t, "sales") - getv(t, "cogs")), getv(t, "sales"))
    gm_p = safe_div((getv(p, "sales") - getv(p, "cogs")), getv(p, "sales"))
    gmi = safe_div(gm_p, gm_t)

    aq_t = 1 - safe_div((getv(t, "current_assets") + getv(t, "ppe_net") + getv(t, "long_term_investments")), getv(t, "total_assets"))
    aq_p = 1 - safe_div((getv(p, "current_assets") + getv(p, "ppe_net") + getv(p, "long_term_investments")), getv(p, "total_assets"))
    aqi = safe_div(aq_t, aq_p)

    sgi = safe_div(getv(t, "sales"), getv(p, "sales"))

    dep_t = safe_div(getv(t, "depreciation"), (getv(t, "ppe_net") + getv(t, "depreciation")))
    dep_p = safe_div(getv(p, "depreciation"), (getv(p, "ppe_net") + getv(p, "depreciation")))
    depi = safe_div(dep_p, dep_t)

    sgai = safe_div(safe_div(getv(t, "sga"), getv(t, "sales")), safe_div(getv(p, "sga"), getv(p, "sales")))

    lv_t = safe_div((getv(t, "current_liabilities") + getv(t, "long_term_debt")), getv(t, "total_assets"))
    lv_p = safe_div((getv(p, "current_liabilities") + getv(p, "long_term_debt")), getv(p, "total_assets"))
    lvgi = safe_div(lv_t, lv_p)

    tata = safe_div((getv(t, "income_cont_ops") - getv(t, "cfo")), getv(t, "total_assets"))

    m_score = (
        -4.84
        + 0.920 * dsri
        + 0.528 * gmi
        + 0.404 * aqi
        + 0.892 * sgi
        + 0.115 * depi
        - 0.172 * sgai
        + 4.679 * tata
        - 0.327 * lvgi
    )

    return {
        "components": {
            "DSRI": dsri,
            "GMI": gmi,
            "AQI": aqi,
            "SGI": sgi,
            "DEPI": depi,
            "SGAI": sgai,
            "LVGI": lvgi,
            "TATA": tata,
        },
        "M_SCORE": m_score,
        "threshold": -2.22,
        "risk_signal": m_score > -2.22,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input JSON")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = calc(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
