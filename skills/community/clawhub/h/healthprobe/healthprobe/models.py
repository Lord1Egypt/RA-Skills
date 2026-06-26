"""
Pydantic models for HealthProbe API.
"""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProbeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: HttpUrl = Field(..., description="URL to probe.")
    timeout_ms: int = Field(default=5000, ge=100, le=30000, description="Timeout in milliseconds.")


class ProbeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str = Field(..., description="Probed URL.")
    healthy: bool = Field(..., description="True if status 2xx and responsive.")
    status_code: int = Field(..., description="HTTP status code, or -1 on connection error.")
    latency_ms: int = Field(..., ge=0, description="Response time in milliseconds.")
    error: str = Field(default="", description="Error message if probe failed.")
