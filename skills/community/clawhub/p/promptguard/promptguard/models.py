"""
Pydantic request/response models for PromptGuard API.

All models use extra="forbid" per CLAUDE.md compliance rules.
Risk score uses Decimal per security policy (no float for scored values).
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ScanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        ...,
        min_length=1,
        max_length=100_000,
        description="Text to scan for prompt injection patterns.",
    )


class ScanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_score: Decimal = Field(
        ...,
        ge=Decimal("0"),
        le=Decimal("1"),
        description="Injection risk score in [0.0, 1.0].",
    )
    patterns_detected: list[str] = Field(
        ...,
        description="List of detected injection pattern names.",
    )
    input_length: int = Field(
        ...,
        ge=0,
        description="Length of the scanned input text.",
    )
