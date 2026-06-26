"""
mindclaw.config — Persistent user configuration for MindClaw.

Config file: ~/.mindclaw/config.json

Priority chain for every setting:
    CLI flag  >  MINDCLAW_* env var  >  config file  >  hardcoded default

The config file is written by `mindclaw setup` (or the `setup_mindclaw` MCP
tool) and read automatically on every command, so users never have to pass
--db, --agent, or --workspace flags more than once.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config file location
# ---------------------------------------------------------------------------

_CONFIG_PATH = Path.home() / ".mindclaw" / "config.json"


@dataclass
class MindClawConfig:
    """
    Persistent MindClaw configuration.

    All fields are optional — unset fields fall back to hardcoded defaults.
    """

    # Path to the SQLite database file.
    # None → use MemoryStore default (~/.mindclaw/memory.db)
    db_path: Optional[str] = None

    # Default agent/namespace for memories.
    # "" → shared namespace (no isolation)
    agent_id: str = ""

    # Path to the OpenClaw workspace directory.
    # None → auto-detect (~/.openclaw/workspace)
    openclaw_workspace: Optional[str] = None

    # ---------------------------------------------------------------------------
    # Effective value helpers — apply env var overrides on top of saved values
    # ---------------------------------------------------------------------------

    def effective_db(self) -> Optional[str]:
        """CLI/env-resolved db_path.  None → MemoryStore picks its default."""
        return os.environ.get("MINDCLAW_DB") or self.db_path or None

    def effective_agent(self) -> str:
        """CLI/env-resolved agent_id."""
        return os.environ.get("MINDCLAW_AGENT", "") or self.agent_id

    def effective_workspace(self) -> Optional[str]:
        """CLI/env-resolved OpenClaw workspace path."""
        return (
            os.environ.get("MINDCLAW_OPENCLAW_WORKSPACE")
            or self.openclaw_workspace
            or None
        )


# ---------------------------------------------------------------------------
# Load / save
# ---------------------------------------------------------------------------

def load_config() -> MindClawConfig:
    """
    Load config from ~/.mindclaw/config.json.
    Returns a default (all-None) config if the file does not exist or is invalid.
    """
    if _CONFIG_PATH.exists():
        try:
            raw = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
            # Only pass fields that actually exist in the dataclass
            valid = {
                k: v for k, v in raw.items()
                if k in MindClawConfig.__dataclass_fields__
            }
            return MindClawConfig(**valid)
        except Exception:
            pass
    return MindClawConfig()


def save_config(cfg: MindClawConfig) -> str:
    """Write config to ~/.mindclaw/config.json.  Returns the path written."""
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_PATH.write_text(
        json.dumps(asdict(cfg), indent=2, default=str),
        encoding="utf-8",
    )
    return str(_CONFIG_PATH)


def config_path() -> Path:
    """Return the canonical config file path (may not exist yet)."""
    return _CONFIG_PATH
