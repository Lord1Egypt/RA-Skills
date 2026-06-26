"""
mcp_connector/config.py
────────────────────────
Client-side connector configuration.

All values come from environment variables so the connector can be deployed
without touching source code.  The API key for the remote engine lives here —
NOT on the server (it's the credential the connector uses to authenticate).

Environment variables
─────────────────────
  QUOTE_ENGINE_URL      — base URL of api_engine, e.g. https://quote.example.com
  QUOTE_ENGINE_API_KEY  — X-API-Key credential for the engine
  ERP_EXCEL_PATH        — path to local ERP Excel file (ERP內容.xlsx)
  ERP_SQLITE_PATH       — alternative: path to local SQLite with erp_inventory table
  CONNECTOR_TIMEOUT     — HTTP timeout in seconds (default 15)
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConnectorConfig:
    # Remote engine
    engine_url: str = field(
        default_factory=lambda: os.environ.get("QUOTE_ENGINE_URL", "http://127.0.0.1:8001").rstrip("/")
    )
    engine_api_key: str = field(
        default_factory=lambda: os.environ.get("QUOTE_ENGINE_API_KEY", "")
    )
    timeout: int = field(
        default_factory=lambda: int(os.environ.get("CONNECTOR_TIMEOUT", "15"))
    )

    # Local ERP sources (Excel takes priority over SQLite)
    erp_excel_path: str = field(
        default_factory=lambda: os.environ.get(
            "ERP_EXCEL_PATH",
            str(Path.home() / "Desktop" / "ERP內容.xlsx"),
        )
    )
    erp_sqlite_path: str = field(
        default_factory=lambda: os.environ.get("ERP_SQLITE_PATH", "")
    )

    def validate(self) -> list[str]:
        """Return a list of configuration warnings (not errors — connector degrades gracefully)."""
        warnings: list[str] = []
        if not self.engine_url:
            warnings.append("QUOTE_ENGINE_URL is not set — remote quotes will fail.")
        if not self.engine_api_key:
            warnings.append("QUOTE_ENGINE_API_KEY is not set — remote quotes will be rejected with 403.")
        if not Path(self.erp_excel_path).exists() and not self.erp_sqlite_path:
            warnings.append(
                f"No local ERP source found at {self.erp_excel_path!r} "
                "and ERP_SQLITE_PATH is not set — local ERP data will be unavailable."
            )
        return warnings


# Module-level singleton — reloads from env on import
config = ConnectorConfig()
