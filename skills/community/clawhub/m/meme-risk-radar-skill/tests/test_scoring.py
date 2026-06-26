from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from meme_risk_radar import calculate_score, normalize_token


def test_calculate_score_marks_high_risk_signals() -> None:
    token = {
        "holdersTop10Percent": "91",
        "holdersDevPercent": "12",
        "holdersSniperPercent": "17",
        "holdersInsiderPercent": "9",
        "bundlerHoldingPercent": "25",
        "liquidity": "3000",
    }
    audit = {
        "hasResult": True,
        "isSupported": True,
        "riskLevel": 4,
        "extraInfo": {"buyTax": "12", "sellTax": "12", "isVerified": False},
        "riskItems": [{"details": [{"title": "Honeypot risk", "isHit": True}]}],
    }
    meta = {"links": []}

    scored = calculate_score(token, audit, meta, "en")
    assert scored["score"] >= 75
    assert scored["risk_level"] == "Critical risk"
    assert scored["signals"]


def test_normalize_token_keeps_links_and_contract() -> None:
    token = {"symbol": "TEST", "name": "Test", "contractAddress": "0xabc", "liquidity": "10000"}
    audit = {"hasResult": False, "isSupported": False, "riskItems": []}
    meta = {"links": [{"label": "x", "link": "https://x.com/test"}]}

    normalized = normalize_token(token, audit, meta, "zh")
    assert normalized["contract_address"] == "0xabc"
    assert normalized["links"][0]["label"] == "x"
