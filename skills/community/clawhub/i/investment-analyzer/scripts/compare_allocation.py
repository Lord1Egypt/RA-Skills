#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timedelta

MARGINAL_TAX_RATE = 0.46
CAPITAL_GAINS_INCLUSION = 0.50
APPRECIATION_RATE = 0.035
DOWN_PAYMENT_RATIO = 0.20
MORTGAGE_RATE = 0.0539
AMORT_YEARS = 25
VACANCY_RATE = 0.05
MAINTENANCE_RATIO = 0.01
INSURANCE_MONTHLY = 150
LOC_RATE = 0.0495
ETF_DEFAULT_RETURN = 0.10
ETF_TICKER = "TEC.TO"
CLOSE_THRESHOLD = 0.015


def calc_monthly_mortgage(principal, annual_rate, amort_years=AMORT_YEARS):
    r = annual_rate / 12
    n = amort_years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def model_property(capital, monthly_rent, property_tax_annual, years, mortgage_rate=MORTGAGE_RATE):
    price = capital / DOWN_PAYMENT_RATIO
    loan = price - capital
    monthly_mortgage = calc_monthly_mortgage(loan, mortgage_rate)
    effective_rent = monthly_rent * (1 - VACANCY_RATE)
    maintenance = price * MAINTENANCE_RATIO / 12
    tax_monthly = property_tax_annual / 12
    total_expenses = monthly_mortgage + maintenance + tax_monthly + INSURANCE_MONTHLY
    monthly_cf = effective_rent - total_expenses
    annual_cf = monthly_cf * 12
    after_tax_cf = annual_cf * (1 - MARGINAL_TAX_RATE) if annual_cf > 0 else annual_cf
    total_cf = after_tax_cf * years
    total_appreciation = price * ((1 + APPRECIATION_RATE) ** years - 1)
    cgt = total_appreciation * CAPITAL_GAINS_INCLUSION * MARGINAL_TAX_RATE
    net_appreciation = total_appreciation - cgt
    equity_end = capital + net_appreciation
    total_return = total_cf + net_appreciation
    annualized = (1 + total_return / capital) ** (1 / years) - 1 if capital > 0 else 0
    return {
        "strategy": "Real Estate",
        "capital_deployed": round(capital),
        "property_price_implied": round(price),
        "loan_amount": round(loan),
        "monthly_gross_rent": round(monthly_rent),
        "monthly_net_cash_flow": round(monthly_cf),
        "annual_after_tax_cash_flow": round(after_tax_cf),
        "total_cash_flow_over_period": round(total_cf),
        "total_appreciation_gross": round(total_appreciation),
        "capital_gains_tax": round(cgt),
        "net_appreciation_after_tax": round(net_appreciation),
        "equity_end_of_period": round(equity_end),
        "total_net_return": round(total_return),
        "annualized_after_tax_return_pct": round(annualized * 100, 2),
        "leverage_note": f"${round(price):,} property controlled with ${round(capital):,} down ({DOWN_PAYMENT_RATIO*100:.0f}%)",
    }


def get_etf_return(ticker):
    try:
        import yfinance as yf
        now = datetime.now()
        t = yf.Ticker(ticker)
        hist = t.history(start=(now - timedelta(days=365 * 5)).strftime("%Y-%m-%d"))
        if hist is not None and len(hist) >= 2:
            end = hist["Close"].iloc[-1]
            start = hist["Close"].iloc[0]
            cagr = (end / start) ** (1 / 5) - 1
            return cagr
    except Exception:
        pass
    return ETF_DEFAULT_RETURN


def model_etf(capital, years, annual_return=None, ticker=ETF_TICKER):
    if annual_return is None:
        annual_return = get_etf_return(ticker)
    end_value = capital * (1 + annual_return) ** years
    gross_gain = end_value - capital
    cgt = gross_gain * CAPITAL_GAINS_INCLUSION * MARGINAL_TAX_RATE
    net_gain = gross_gain - cgt
    net_end_value = capital + net_gain
    annualized_after_tax = (net_end_value / capital) ** (1 / years) - 1
    return {
        "strategy": f"ETF ({ticker})",
        "capital_deployed": round(capital),
        "assumed_annual_return_pct": round(annual_return * 100, 2),
        "end_portfolio_value_gross": round(end_value),
        "gross_gain": round(gross_gain),
        "capital_gains_tax": round(cgt),
        "net_gain_after_tax": round(net_gain),
        "net_end_value": round(net_end_value),
        "annualized_after_tax_return_pct": round(annualized_after_tax * 100, 2),
        "leverage_note": "No leverage — 1:1 capital deployment",
    }


def compare(capital, monthly_rent, property_tax_annual, years, mortgage_rate=MORTGAGE_RATE, etf_return=None, etf_ticker=ETF_TICKER):
    prop = model_property(capital, monthly_rent, property_tax_annual, years, mortgage_rate)
    etf = model_etf(capital, years, etf_return, etf_ticker)

    prop_ret = prop["annualized_after_tax_return_pct"]
    etf_ret = etf["annualized_after_tax_return_pct"]
    diff = prop_ret - etf_ret

    if diff > CLOSE_THRESHOLD * 100:
        verdict = "✅ REAL ESTATE WINS"
        reason = f"Property delivers {abs(diff):.1f}% higher after-tax annualized return with leverage boost."
    elif diff < -CLOSE_THRESHOLD * 100:
        verdict = "✅ ETF WINS"
        reason = f"ETF delivers {abs(diff):.1f}% higher after-tax annualized return with better liquidity and less time commitment."
    else:
        verdict = "⚠️ TOO CLOSE TO CALL"
        reason = f"Returns within {CLOSE_THRESHOLD*100:.1f}% of each other. Decide based on liquidity needs, risk tolerance, and time commitment."

    return {
        "comparison_period_years": years,
        "property_scenario": prop,
        "etf_scenario": etf,
        "conclusion": {
            "verdict": verdict,
            "reason": reason,
            "annualized_after_tax_property_pct": prop_ret,
            "annualized_after_tax_etf_pct": etf_ret,
            "difference_pct": round(diff, 2),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Compare ETF vs real estate investment.")
    parser.add_argument("--capital", type=float, required=True, help="Available capital to deploy (CAD)")
    parser.add_argument("--rent", type=float, default=2000, help="Expected monthly gross rent (default: 2000)")
    parser.add_argument("--tax", type=float, default=3600, help="Annual property tax (default: 3600)")
    parser.add_argument("--years", type=int, default=10, help="Investment horizon in years (default: 10)")
    parser.add_argument("--mortgage-rate", type=float, default=MORTGAGE_RATE, help="Mortgage annual rate")
    parser.add_argument("--etf-return", type=float, default=None, help="Override ETF annual return (e.g. 0.10 for 10%%)")
    parser.add_argument("--etf-ticker", type=str, default=ETF_TICKER, help="ETF ticker to fetch live return from")
    args = parser.parse_args()

    result = compare(args.capital, args.rent, args.tax, args.years, args.mortgage_rate, args.etf_return, args.etf_ticker)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

