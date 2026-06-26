"""Create request-scoped metadata for CLI runs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from hkipo_next.contracts.common import RULE_VERSION, SCHEMA_VERSION, ResponseMeta


@dataclass(frozen=True)
class RunContext:
    """Immutable request metadata propagated to responses."""

    run_id: str
    timestamp: datetime
    rule_version: str = RULE_VERSION
    schema_version: str = SCHEMA_VERSION

    @classmethod
    def create(cls) -> "RunContext":
        return cls(
            run_id=uuid4().hex,
            timestamp=datetime.now(timezone.utc),
        )

    def meta(self, *, degraded: bool, data_status: str) -> ResponseMeta:
        return ResponseMeta(
            run_id=self.run_id,
            timestamp=self.timestamp,
            rule_version=self.rule_version,
            schema_version=self.schema_version,
            degraded=degraded,
            data_status=data_status,
        )
