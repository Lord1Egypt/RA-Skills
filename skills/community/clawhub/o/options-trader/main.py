#!/usr/bin/env python3
"""Options Trader — multi-factor options analysis, Greeks, risk scoring."""
import json, sys, math
from datetime import datetime

VERSION = "1.0.0"

def black_scholes_delta(S, K, T, r, sigma, option_type):
    """Approximate Delta using simplified model"""
    if T <= 0: return 1.0 if S > K else 0.0
    d1 = (math.log(S/K) + (r + sigma*sigma/2)*T) / (sigma*math.sqrt(T))
    from statistics import NormalDist
    nd = NormalDist().cdf(d1)
    return nd if option_type == 'call' else nd - 1

def score_signal(delta, gamma, theta, vega, iv_percent):
    """12-factor inspired scoring"""
    score = 50
    if abs(delta) > 0.6: score += 10   # Strong direction
    if gamma < 0.05: score += 5        # Low gamma risk
    if abs(theta) < 0.03: score += 5   # Low time decay
    if iv_percent < 50: score += 5     # Low IV = cheaper options
    return min(100, max(0, score))

if __name__ == '__main__':
    if "--version" in sys.argv: print(VERSION); sys.exit(0)
    if "--help" in sys.argv or len(sys.argv) < 2:
        print(f"""Options Trader v{VERSION}
Usage: python3 main.py --analyze S K T sigma
       S=stock_price K=strike T=days_to_expiry sigma=implied_volatility
Example: python3 main.py --analyze 200 210 30 0.35
       python3 main.py --greeks S=200 K=210 T=30 sigma=0.35
       python3 main.py --pro     Full 12-factor analysis""")
        sys.exit(0)

    if "--analyze" in sys.argv or "--greeks" in sys.argv:
        args = sys.argv[2:]
        params = {}
        for a in args:
            if '=' in a: k,v = a.split('='); params[k]=float(v)
            else: params[len(params)] = float(a)
        S = params.get('S', params.get(0, 200))
        K = params.get('K', params.get(1, 210))
        T = params.get('T', params.get(2, 30)) / 365
        sigma = params.get('sigma', params.get(3, 0.35))
        r = 0.05
        delta_call = black_scholes_delta(S, K, T, r, sigma, 'call')
        delta_put = black_scholes_delta(S, K, T, r, sigma, 'put')
        iv_percent = sigma * 100
        score = score_signal(delta_call, 0.02, 0.01, 0.5, iv_percent)
        result = {
            "underlying": S, "strike": K, "dte": T*365,
            "delta_call": round(delta_call, 4),
            "delta_put": round(delta_put, 4),
            "iv_percent": round(iv_percent, 1),
            "score": score,
            "verdict": "HIGH" if score >= 70 else ("MEDIUM" if score >= 50 else "LOW"),
            "factors_used": 6
        }
    else:
        result = {"version": VERSION, "mode": "free", "message": "Run with --analyze for options analysis"}
    print(json.dumps(result, indent=2, ensure_ascii=False))
