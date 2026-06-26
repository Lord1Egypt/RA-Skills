"""
HealthProbe API — FastAPI application.

Single endpoint: POST /v1/probe
Probes a URL and returns health status, latency, and status code.
"""

import time

import httpx
from fastapi import FastAPI

from .models import ProbeRequest, ProbeResponse

app = FastAPI(
    title="HealthProbe API",
    description="On-demand URL health probing for AI agents.",
    version="0.1.0",
)


@app.post("/v1/probe", response_model=ProbeResponse)
async def probe(request: ProbeRequest) -> ProbeResponse:
    """Probe a URL and return health status."""
    url = str(request.url)
    timeout_s = request.timeout_ms / 1000

    start = time.monotonic()
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.head(url, timeout=timeout_s, follow_redirects=True)
            latency_ms = int((time.monotonic() - start) * 1000)
            healthy = 200 <= resp.status_code < 300
            return ProbeResponse(
                url=url,
                healthy=healthy,
                status_code=resp.status_code,
                latency_ms=latency_ms,
            )
    except Exception as e:
        latency_ms = int((time.monotonic() - start) * 1000)
        return ProbeResponse(
            url=url,
            healthy=False,
            status_code=-1,
            latency_ms=latency_ms,
            error=str(e),
        )
