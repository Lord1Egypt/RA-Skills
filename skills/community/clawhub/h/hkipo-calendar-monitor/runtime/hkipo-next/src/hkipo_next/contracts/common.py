"""Shared response metadata for hkipo_next contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


RULE_VERSION = "v0.4.0"
SCHEMA_VERSION = "1.2.0"


class ResponseMeta(BaseModel):
    """Top-level response metadata shared by every command."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    timestamp: datetime
    rule_version: str = RULE_VERSION
    schema_version: str = SCHEMA_VERSION
    degraded: bool = False
    data_status: Literal["complete", "partial", "error"] = "complete"
