"""
PromptGuard API — FastAPI application.

Single endpoint: POST /v1/scan
Accepts text, returns injection risk score and detected patterns.
"""

from decimal import ROUND_HALF_UP, Decimal

from fastapi import FastAPI

from .detectors import TOTAL_PATTERNS, scan
from .models import ScanRequest, ScanResponse

app = FastAPI(
    title="PromptGuard API",
    description="Prompt injection detection for AI agents.",
    version="0.1.0",
)


@app.post("/v1/scan", response_model=ScanResponse)
async def scan_text(request: ScanRequest) -> ScanResponse:
    """Scan text for prompt injection patterns."""
    detected = scan(request.text)
    num_matched = len(detected)

    if num_matched == 0:
        risk_score = Decimal("0")
    else:
        risk_score = (Decimal(num_matched) / Decimal(TOTAL_PATTERNS)).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )

    return ScanResponse(
        risk_score=risk_score,
        patterns_detected=detected,
        input_length=len(request.text),
    )
