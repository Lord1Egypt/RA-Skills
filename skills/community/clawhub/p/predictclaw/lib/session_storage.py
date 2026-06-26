from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any


_session_storage_lock = Lock()
_TERMINAL_SESSION_STATUSES = {"succeeded", "failed", "cancelled"}


@dataclass
class FundAndActionSessionRecord:
    session_id: str
    predict_account_address: str
    market_id: str
    position_id: str
    outcome: str
    order_hash: str | None
    session_scope: str
    funding_plan: dict[str, Any]
    funding_session: dict[str, Any]
    funding_next_step: dict[str, Any]
    created_at: str
    updated_at: str

    def binding_payload(self) -> dict[str, Any]:
        return {
            "sessionId": self.session_id,
            "marketId": self.market_id,
            "positionId": self.position_id,
            "outcome": self.outcome,
            "orderHash": self.order_hash,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "predict_account_address": self.predict_account_address,
            "market_id": self.market_id,
            "position_id": self.position_id,
            "outcome": self.outcome,
            "order_hash": self.order_hash,
            "session_scope": self.session_scope,
            "funding_plan": self.funding_plan,
            "funding_session": self.funding_session,
            "funding_next_step": self.funding_next_step,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "FundAndActionSessionRecord":
        return cls(
            session_id=str(payload.get("session_id", "")),
            predict_account_address=str(payload.get("predict_account_address", "")),
            market_id=str(payload.get("market_id", "")),
            position_id=str(payload.get("position_id", "")),
            outcome=str(payload.get("outcome", "")),
            order_hash=str(payload.get("order_hash"))
            if payload.get("order_hash") is not None
            else None,
            session_scope=str(payload.get("session_scope", "generic-balance-top-up")),
            funding_plan=dict(payload.get("funding_plan", {})),
            funding_session=dict(payload.get("funding_session", {})),
            funding_next_step=dict(payload.get("funding_next_step", {})),
            created_at=str(payload.get("created_at", "")),
            updated_at=str(payload.get("updated_at", "")),
        )


class SessionStorage:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.storage_dir / "fund_and_action_sessions.json"

    def list_sessions(self) -> list[FundAndActionSessionRecord]:
        return [
            FundAndActionSessionRecord.from_dict(item) for item in self._read_payload()
        ]

    def upsert(self, record: FundAndActionSessionRecord) -> None:
        with _session_storage_lock:
            rows = self.list_sessions()
            replaced = False
            for index, existing in enumerate(rows):
                if existing.session_id == record.session_id:
                    rows[index] = record
                    replaced = True
                    break
            if not replaced:
                rows.append(record)
            self._write_payload([row.to_dict() for row in rows])

    def get_active_session(
        self, *, predict_account_address: str | None = None
    ) -> FundAndActionSessionRecord | None:
        rows = []
        for record in self.list_sessions():
            session_status = str(record.funding_session.get("status", "")).lower()
            if session_status in _TERMINAL_SESSION_STATUSES:
                continue
            if (
                predict_account_address is not None
                and record.predict_account_address.lower()
                != predict_account_address.lower()
            ):
                continue
            rows.append(record)
        if not rows:
            return None
        rows.sort(key=lambda record: record.updated_at)
        return rows[-1]

    def _read_payload(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            payload = json.loads(self.path.read_text())
        except json.JSONDecodeError:
            return []
        if not isinstance(payload, list):
            return []
        return [item for item in payload if isinstance(item, dict)]

    def _write_payload(self, payload: list[dict[str, Any]]) -> None:
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(payload, indent=2))
        temp_path.replace(self.path)
