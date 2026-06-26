import os
import time
from typing import Any, Dict, List, Optional, Tuple
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

APP_NAME = "polymarket-movers"
SKILLPAY_API_KEY = "sk_8b36c2ca9e774eb0243752f907b086e78c8af866a4088d3e3475113ed446b71"
SKILLPAY_API_BASE = os.getenv("SKILLPAY_API_BASE", "https://api.skillpay.me")
SKILLPAY_WEB_BASE = os.getenv("SKILLPAY_WEB_BASE", "https://pay.skillpay.me")
PRICE_CURRENCY = "USDT"
PRICE_AMOUNT = "0.01"
POLYMARKET_MARKETS_URL = "https://clob.polymarket.com/markets"
@app.get("/invoke")
async def root_get():
    return {"service": "polymarket-movers", "status": "ready", "api_connected": API_KEY is not None}
class InvokeRequest(BaseModel):
    charge_id: Optional[str] = None

class MoversResponse(BaseModel):
    requires_payment: bool
    charge_id: Optional[str] = None
    payment_url: Optional[str] = None
    status: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
    allow_credentials=False,
)

def _get_float(d: Dict[str, Any], keys: List[str], default: float = 0.0) -> float:
    for k in keys:
        if k in d and d[k] is not None:
            try:
                return float(d[k])
            except Exception:
                continue
    return default

def _extract_title(m: Dict[str, Any]) -> str:
    for k in ["question", "title", "name", "slug"]:
        if m.get(k):
            return str(m[k])
    return str(m.get("id", ""))

def _extract_current_price(m: Dict[str, Any]) -> Optional[float]:
    v = _get_float(m, ["price", "current_price", "yesPrice", "lastPrice", "yes_price"])
    if v:
        return v
    prices = m.get("prices") or m.get("priceObj") or {}
    if isinstance(prices, dict):
        pv = _get_float(prices, ["yes", "YES", "price"])
        if pv:
            return pv
    outcomes = m.get("outcomes") or []
    if isinstance(outcomes, list) and outcomes:
        for o in outcomes:
            if isinstance(o, dict) and str(o.get("name", "")).lower() in ["yes", "y"]:
                ov = _get_float(o, ["price", "lastPrice", "yesPrice"])
                if ov:
                    return ov
        o0 = outcomes[0]
        if isinstance(o0, dict):
            ov = _get_float(o0, ["price", "lastPrice", "yesPrice"])
            if ov:
                return ov
    bids = m.get("bids") or {}
    asks = m.get("asks") or {}
    bb = _get_float(bids, ["best", "bestBid"])
    ba = _get_float(asks, ["best", "bestAsk"])
    if bb and ba:
        return (bb + ba) / 2.0
    if bb:
        return bb
    if ba:
        return ba
    return None

def _extract_prev_price_1h(m: Dict[str, Any]) -> Optional[float]:
    delta = _get_float(m, ["priceChange1h", "change1h", "delta1h"])
    if delta:
        curr = _extract_current_price(m)
        if curr is not None:
            return curr - delta
    prev = _get_float(m, ["price1hAgo", "prevPrice", "previous_price"])
    if prev:
        return prev
    return None

def fetch_markets() -> List[Dict[str, Any]]:
    try:
        r = requests.get(POLYMARKET_MARKETS_URL, timeout=20)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch markets")
        data = r.json()
        if isinstance(data, dict) and "markets" in data and isinstance(data["markets"], list):
            return data["markets"]
        if isinstance(data, list):
            return data
        raise HTTPException(status_code=502, detail="Unexpected markets payload")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Markets fetch error: {e}")

def pick_active_top10(markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    active: List[Dict[str, Any]] = []
    for m in markets:
        active_flag = False
        if isinstance(m, dict):
            if m.get("active") is True:
                active_flag = True
            if str(m.get("status", "")).lower() == "active":
                active_flag = True
            if m.get("closed") is False:
                active_flag = True
        if active_flag:
            active.append(m)
    if not active:
        for m in markets:
            if isinstance(m, dict) and not m.get("resolved", False):
                active.append(m)
    def vol_key(m: Dict[str, Any]) -> float:
        return _get_float(m, ["volume", "volume24hr", "volume24h", "totalVolume", "liquidity"], 0.0)
    active.sort(key=vol_key, reverse=True)
    return active[:10]

def compute_movers(markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    movers: List[Tuple[float, Dict[str, Any]]] = []
    for m in markets:
        curr = _extract_current_price(m)
        prev = _extract_prev_price_1h(m)
        if curr is None:
            continue
        if prev is None:
            try:
                prev = fetch_prev_price_from_api(m)
            except Exception:
                prev = None
        if prev is None:
            continue
        delta = curr - prev
        item = {
            "id": m.get("id"),
            "title": _extract_title(m),
            "current_price": round(curr, 6),
            "prev_price": round(prev, 6),
            "delta": round(delta, 6),
            "abs_delta": round(abs(delta), 6),
            "volume": _get_float(m, ["volume", "volume24hr", "volume24h", "totalVolume", "liquidity"], 0.0),
            "status": m.get("status") or ("active" if m.get("active") else None)
        }
        movers.append((abs(delta), item))
    movers.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in movers[:3]]

def fetch_prev_price_from_api(m: Dict[str, Any]) -> Optional[float]:
    mid = str(m.get("id", ""))
    if not mid:
        return None
    candidates = [
        f"https://clob.polymarket.com/markets/{mid}/candles?interval=1h&limit=2",
        f"https://clob.polymarket.com/markets/{mid}/prices?interval=1h&limit=2",
    ]
    for url in candidates:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                continue
            payload = r.json()
            arr = None
            if isinstance(payload, dict):
                for k in ["candles", "prices", "data"]:
                    if isinstance(payload.get(k), list):
                        arr = payload[k]
                        break
            if isinstance(payload, list):
                arr = payload
            if not arr or len(arr) < 2:
                continue
            p0 = arr[-2]
            if isinstance(p0, dict):
                v = _get_float(p0, ["close", "price", "yesPrice"])
                if v:
                    return v
            if isinstance(p0, list) and len(p0) >= 5:
                try:
                    return float(p0[4])
                except Exception:
                    continue
        except Exception:
            continue
    return None

def create_skillpay_charge(amount: str, currency: str) -> Tuple[str, str]:
    if not SKILLPAY_API_KEY:
        raise HTTPException(status_code=400, detail="Missing SKILLPAY_API_KEY")
    url = f"{SKILLPAY_API_BASE.rstrip('/')}/v1/charges"
    headers = {
        "Authorization": f"Bearer {SKILLPAY_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "amount": amount,
        "currency": currency,
        "title": "OpenClaw Skill Payment",
        "description": "Polymarket Movers x3",
    }
    r = requests.post(url, json=body, headers=headers, timeout=20)
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail="SkillPay create charge failed")
    data = r.json()
    cid = str(data.get("id") or data.get("charge_id") or "")
    purl = data.get("payment_url")
    if not purl and cid:
        purl = f"{SKILLPAY_WEB_BASE.rstrip('/')}/checkout/{cid}"
    if not cid or not purl:
        raise HTTPException(status_code=502, detail="Invalid SkillPay response")
    return cid, purl

def get_skillpay_status(charge_id: str) -> str:
    if not SKILLPAY_API_KEY:
        raise HTTPException(status_code=400, detail="Missing SKILLPAY_API_KEY")
    url = f"{SKILLPAY_API_BASE.rstrip('/')}/v1/charges/{charge_id}"
    headers = {"Authorization": f"Bearer {SKILLPAY_API_KEY}"}
    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="SkillPay status query failed")
    data = r.json()
    status = str(data.get("status") or data.get("state") or "").lower()
    return status

@app.post("/invoke", response_model=MoversResponse)
def invoke(req: InvokeRequest) -> MoversResponse:
    if not req.charge_id:
        cid, purl = create_skillpay_charge(PRICE_AMOUNT, PRICE_CURRENCY)
        return MoversResponse(requires_payment=True, charge_id=cid, payment_url=purl, status="pending")
    status = ""
    for _ in range(10):
        status = get_skillpay_status(req.charge_id)
        if status in ["paid", "succeeded", "success", "completed"]:
            break
        if status in ["failed", "canceled", "expired"]:
            return MoversResponse(requires_payment=True, charge_id=req.charge_id, payment_url=None, status=status)
        time.sleep(3)
    if status not in ["paid", "succeeded", "success", "completed"]:
        return MoversResponse(requires_payment=True, charge_id=req.charge_id, payment_url=None, status=status or "pending")
    markets = fetch_markets()
    top10 = pick_active_top10(markets)
    movers = compute_movers(top10)
    return MoversResponse(requires_payment=False, data=movers, status="ok")

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
