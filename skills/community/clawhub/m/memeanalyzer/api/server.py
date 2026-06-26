"""
Solana Meme Token Analyzer - Paid API Server
Charges per-request via x402 micropayment protocol (USDC on Base chain)
"""

import os
import sys
import json
import time
import requests
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# Add scripts dir to path so we can import the analyzer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from psdm import MemeAnalyzerPro

app = FastAPI(
    title="Solana Meme Token Analyzer API",
    description="Detect insider wallets and rug risk for any Solana token CA. Pay-per-request via x402.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# x402 Payment Middleware
# ============================================================
# Price per request in USDC (e.g. 0.02 = $0.02)
PRICE_PER_REQUEST = os.environ.get("PRICE_PER_REQUEST", "0.02")
# Your Base chain wallet address to receive payments
PAY_TO_ADDRESS = os.environ.get("PAY_TO_ADDRESS", "")
# x402 facilitator URL (default: public facilitator)
FACILITATOR_URL = os.environ.get("FACILITATOR_URL", "https://x402.org/facilitator")


def build_402_response():
    """Return HTTP 402 with x402 payment requirements"""
    if not PAY_TO_ADDRESS:
        return None  # x402 not configured, skip payment requirement

    payment_required = {
        "x402Version": 1,
        "accepts": [
            {
                "scheme": "exact",
                "network": "base",
                "maxAmountRequired": str(int(float(PRICE_PER_REQUEST) * 1_000_000)),  # USDC has 6 decimals
                "resource": "/analyze",
                "description": f"Solana meme token risk analysis - ${PRICE_PER_REQUEST} per request",
                "mimeType": "application/json",
                "payTo": PAY_TO_ADDRESS,
                "maxTimeoutSeconds": 60,
                "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
                "extra": {
                    "name": "Solana Meme Analyzer",
                    "version": "1.0.0"
                }
            }
        ],
        "error": "Payment required"
    }
    return payment_required


def verify_x402_payment(request: Request) -> bool:
    """Verify incoming x402 payment header"""
    if not PAY_TO_ADDRESS:
        return True  # Payment not configured, allow all requests

    payment_header = request.headers.get("X-PAYMENT")
    if not payment_header:
        return False

    try:
        verify_resp = requests.post(
            f"{FACILITATOR_URL}/verify",
            json={
                "payment": payment_header,
                "paymentRequirements": build_402_response()["accepts"][0]
            },
            timeout=10
        )
        if verify_resp.status_code == 200:
            result = verify_resp.json()
            return result.get("isValid", False)
    except Exception:
        pass
    return False


def settle_x402_payment(payment_header: str) -> dict:
    """Settle the payment with the facilitator"""
    try:
        settle_resp = requests.post(
            f"{FACILITATOR_URL}/settle",
            json={
                "payment": payment_header,
                "paymentRequirements": build_402_response()["accepts"][0]
            },
            timeout=10
        )
        if settle_resp.status_code == 200:
            return settle_resp.json()
    except Exception:
        pass
    return {}


# ============================================================
# API Routes
# ============================================================

@app.get("/")
def root():
    return {
        "name": "Solana Meme Token Analyzer API",
        "version": "1.0.0",
        "price_per_request": f"${PRICE_PER_REQUEST} USDC",
        "payment_protocol": "x402",
        "network": "Base",
        "endpoints": {
            "analyze": "GET /analyze?ca=<TOKEN_CA>",
            "health": "GET /health"
        }
    }


@app.get("/health")
def health():
    return {"status": "ok", "payment_configured": bool(PAY_TO_ADDRESS)}


@app.get("/analyze")
async def analyze(ca: str, request: Request):
    """
    Analyze a Solana token CA for rug risk.
    Requires x402 micropayment of ${PRICE_PER_REQUEST} USDC on Base chain.
    
    Parameters:
        ca: Solana token contract address
    
    Returns:
        token info, risk level, holder analysis, warnings
    """
    if not ca or len(ca) < 32:
        raise HTTPException(status_code=400, detail="Invalid token CA. Must be a valid Solana address.")

    # Check x402 payment
    if PAY_TO_ADDRESS:
        payment_header = request.headers.get("X-PAYMENT")

        if not payment_header:
            payment_required = build_402_response()
            return Response(
                content=json.dumps(payment_required),
                status_code=402,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Expose-Headers": "X-PAYMENT-RESPONSE"
                }
            )

        if not verify_x402_payment(request):
            raise HTTPException(status_code=402, detail="Invalid or expired payment")

    # Run the analysis
    try:
        analyzer = MemeAnalyzerPro(ca)

        # Fetch DexScreener data
        dex_info = analyzer.get_token_info_dex()
        if not dex_info:
            raise HTTPException(status_code=404, detail="Token not found on DexScreener. Check the CA or try again later.")

        symbol = dex_info['baseToken']['symbol']
        price = dex_info.get('priceUsd', '0')
        lp_address = dex_info.get('pairAddress')
        liquidity_usd = dex_info.get('liquidity', {}).get('usd', 0)

        # Fetch on-chain data
        total_supply = analyzer.get_token_supply()
        if not total_supply:
            raise HTTPException(status_code=503, detail="Could not fetch token supply. RPC unavailable.")

        holders = analyzer.get_largest_accounts()
        if not holders:
            raise HTTPException(
                status_code=503,
                detail="Could not fetch holder data. Set HELIUS_API_KEY for reliable results on popular tokens."
            )

        # Analyze holders
        suspicious_count = 0
        top10_share = 0
        result_holders = []

        for i, h in enumerate(holders):
            addr = h['address']
            amount = float(h['uiAmountString'])
            percent = (amount / total_supply) * 100
            tag = "normal"
            sol_balance = None

            if addr == lp_address:
                tag = "lp_pool"
            elif i < 12:
                sol_bal = analyzer.get_sol_balance(addr)
                sol_balance = sol_bal if sol_bal != -1 else None
                if i < 10:
                    top10_share += percent
                if sol_bal != -1:
                    if sol_bal < 0.05:
                        tag = "suspected_insider"
                        suspicious_count += 1
                    elif sol_bal > 500:
                        tag = "whale_or_exchange"
                    else:
                        tag = "normal"
            elif i < 10:
                top10_share += percent

            result_holders.append({
                "rank": i + 1,
                "address": addr,
                "percent": round(percent, 2),
                "tag": tag,
                "sol_balance": round(sol_balance, 4) if sol_balance is not None else None
            })
            time.sleep(0.05)

        # Calculate risk level
        risk_level = "LOW"
        warnings = []

        if suspicious_count > 0:
            warnings.append(f"{suspicious_count} suspected insider wallet(s) detected (large token holdings, near-zero SOL)")
            risk_level = "HIGH"

        if top10_share > 50:
            risk_level = "EXTREME"
            warnings.append(f"Extreme concentration: top 10 holders control {top10_share:.1f}% of supply")
        elif top10_share > 30:
            if risk_level == "LOW":
                risk_level = "MEDIUM"
            warnings.append(f"High concentration: top 10 holders control {top10_share:.1f}% of supply")

        result = {
            "token": {
                "ca": ca,
                "symbol": symbol,
                "price_usd": price,
                "liquidity_usd": liquidity_usd,
                "lp_address": lp_address
            },
            "risk": {
                "level": risk_level,
                "top10_concentration_pct": round(top10_share, 2),
                "suspected_insider_count": suspicious_count,
                "warnings": warnings
            },
            "holders": result_holders
        }

        # Settle payment after successful response
        if PAY_TO_ADDRESS:
            payment_header = request.headers.get("X-PAYMENT")
            if payment_header:
                settlement = settle_x402_payment(payment_header)
                return Response(
                    content=json.dumps(result),
                    status_code=200,
                    headers={
                        "Content-Type": "application/json",
                        "X-PAYMENT-RESPONSE": json.dumps(settlement)
                    }
                )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
