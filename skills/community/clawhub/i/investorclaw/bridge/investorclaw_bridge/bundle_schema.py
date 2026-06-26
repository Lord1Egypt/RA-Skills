# SPDX-License-Identifier: Apache-2.0
"""Pydantic schema for the InvestorClaw v4.0 bundle.json.

The bundle is the dashboard's config state + data file references in a JSON
file. Drag-drop into the dashboard to import / export to back up. Same
fields, same validation, two interfaces.

Critical security property: API keys are stored as env-var REFERENCES
("$TOGETHER_API_KEY"), never raw values. A bundle.json is safe to back up
to git, share with co-admin, etc., because it never contains secrets.

Schema version is part of the file. v4.0 is the first version; v4.1+ will
extend with backwards-compatible fields. Major version bump (v5.x) means
breaking schema change requires migration.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────


_ENV_REF_PATTERN = re.compile(r"^\$[A-Z][A-Z0-9_]+$")


def _validate_env_ref(v: str) -> str:
    """Validate that a string is an env-var reference, never a raw value.

    Acceptable: '$TOGETHER_API_KEY', '$IC_MCP_TOKEN'
    Rejected: 'tgp_v1_abc...', '<some-key>', '${TOGETHER_API_KEY}'

    Why strict: the bundle is meant to be safe to commit / share. Raw
    keys defeat that property. Catch the violation at parse time.
    """
    if not _ENV_REF_PATTERN.match(v):
        raise ValueError(
            f"Bundle.json must use env-var references (e.g., '$TOGETHER_API_KEY'), "
            f"not raw values. Got: {v[:24]!r} (truncated). "
            f"Fix: store the actual key in /data/keys.env (mode 0600) and reference it by name here."
        )
    return v


# ──────────────────────────────────────────────────────────────────────
# Sub-schemas
# ──────────────────────────────────────────────────────────────────────


class ProviderConfig(BaseModel):
    """Per-provider config. Provider name is the dict key in the parent."""

    model_config = ConfigDict(extra="forbid")

    api_key_ref: str | None = Field(
        default=None,
        description="Env-var reference like '$TOGETHER_API_KEY'. Never the raw key.",
    )
    base_url: str | None = Field(
        default=None,
        description="OpenAI-compatible base URL override. Useful for Together / OpenRouter / local llama-server.",
    )
    default_model: str | None = Field(
        default=None,
        description="Default model id at this provider (e.g., 'MiniMaxAI/MiniMax-M2.7' for Together).",
    )

    @field_validator("api_key_ref")
    @classmethod
    def validate_api_key_ref(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return _validate_env_ref(v)


class DataSourceConfig(BaseModel):
    """Per-data-source config (Finnhub, FRED, NewsAPI, etc.)."""

    model_config = ConfigDict(extra="forbid")

    api_key_ref: str | None = Field(default=None)

    @field_validator("api_key_ref")
    @classmethod
    def validate_api_key_ref(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return _validate_env_ref(v)


class PortfolioRef(BaseModel):
    """Reference to a portfolio file in /data/portfolios/.

    The file itself is shipped in a companion .tar.gz alongside bundle.json,
    or expected to already exist in the data volume on import.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Stable identifier, e.g., 'ubs_taxable'.")
    source_file: str = Field(description="Path relative to /data/portfolios/, e.g., 'ubs_07_04_2026.xls'.")
    broker: str = Field(description="Detected broker format, e.g., 'ubs', 'schwab', 'vanguard', 'generic'.")
    account_type: Literal["taxable", "ira", "roth", "401k", "crypto", "other"] = Field(
        description="Account taxation tier — affects performance / rebalance logic.",
    )
    label: str | None = Field(default=None, description="User-friendly label for the dashboard.")
    last_imported_at: datetime | None = None


class NarrativeConfig(BaseModel):
    """Narrative-tier configuration for the synthesis layer."""

    model_config = ConfigDict(extra="forbid")

    tier: Literal["heuristic", "local_llm", "cloud_llm", "auto", "off"] = "auto"
    depth: Literal["terse", "standard", "deep"] = "standard"
    provider_route: str | None = Field(
        default=None,
        description="Provider key from the providers map to route narrative calls through. None = use first available.",
    )


class McpConfig(BaseModel):
    """MCP server config."""

    model_config = ConfigDict(extra="forbid")

    bind: str = Field(default="127.0.0.1", description="Bind address. '127.0.0.1' for localhost-only, '0.0.0.0' for remote.")
    port: int = Field(default=8090, ge=1024, le=65535)
    auth_token_ref: str | None = Field(default=None)

    @field_validator("auth_token_ref")
    @classmethod
    def validate_token_ref(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return _validate_env_ref(v)


class MemoryConfig(BaseModel):
    """Memory (mnemos-lite) config."""

    model_config = ConfigDict(extra="forbid")

    retention_days: int = Field(default=365, ge=0, le=10000)
    embedding_model: str | None = Field(
        default="all-MiniLM-L6-v2",
        description="Embedding model identifier for semantic search. None disables semantic search.",
    )
    enabled_categories: list[str] = Field(
        default_factory=lambda: ["infrastructure", "solutions", "patterns", "decisions", "projects", "standards"],
    )


class BundleMetadata(BaseModel):
    """Metadata about the bundle itself."""

    model_config = ConfigDict(extra="forbid")

    exported_at: datetime
    from_host: str = Field(description="Hostname of the machine that exported this bundle.")
    investorclaw_version: str = Field(description="InvestorClaw version that exported.")
    schema_version: Literal["4.0"] = "4.0"


class MemoryRecord(BaseModel):
    """A single memory record in the bundle (mnemos memories portion)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    content: str
    category: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    metadata: dict[str, str | int | float | bool] | None = None


# ──────────────────────────────────────────────────────────────────────
# Top-level bundle schema
# ──────────────────────────────────────────────────────────────────────


class Bundle(BaseModel):
    """v4.0 bundle.json — the canonical export/import shape.

    Wire example::

        {
          "version": "4.0",
          "providers": {
            "together": {
              "api_key_ref": "$TOGETHER_API_KEY",
              "default_model": "MiniMaxAI/MiniMax-M2.7"
            }
          },
          "data_sources": {
            "finnhub": { "api_key_ref": "$FINNHUB_KEY" }
          },
          "portfolios": [
            { "id": "ubs_taxable", "source_file": "ubs_07_04_2026.xls",
              "broker": "ubs", "account_type": "taxable" }
          ],
          "narrative": { "tier": "auto", "depth": "standard" },
          "mcp": { "bind": "127.0.0.1", "port": 8090 },
          "memory": { "retention_days": 365 },
          "memories": [
            { "id": "mem_abc123", "content": "User flagged BABA as never-sell sentimental",
              "category": "preferences", "tags": ["portfolio", "user-rule"],
              "created_at": "2026-04-30T18:30:00Z" }
          ],
          "metadata": {
            "exported_at": "2026-05-01T08:15:00Z",
            "from_host": "studio.local",
            "investorclaw_version": "4.0.0a1"
          }
        }
    """

    model_config = ConfigDict(extra="forbid")

    version: Literal["4.0"] = "4.0"
    providers: dict[str, ProviderConfig] = Field(default_factory=dict)
    data_sources: dict[str, DataSourceConfig] = Field(default_factory=dict)
    portfolios: list[PortfolioRef] = Field(default_factory=list)
    narrative: NarrativeConfig = Field(default_factory=NarrativeConfig)
    mcp: McpConfig = Field(default_factory=McpConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    # `memories` is Optional in v4.0.0a1 beta because mnemos-rs companion
    # is deferred. Bundle imports without memories work; with-memories
    # bundles are accepted and the memories block is held until mnemos
    # connects (or skipped if mnemos is permanently absent). Per
    # GRAEAE 2026-05-01: handle the absence in code, not docs — pilot
    # imports failing on schema validation kill conversion rate.
    memories: list[MemoryRecord] | None = Field(
        default=None,
        description=(
            "Mnemos memory records. May be omitted entirely (v4.0.0a1 beta) "
            "OR an empty list (mnemos connected, no memories yet) OR populated. "
            "Handlers must accept all three states."
        ),
    )
    metadata: BundleMetadata


# ──────────────────────────────────────────────────────────────────────
# Round-trip helpers
# ──────────────────────────────────────────────────────────────────────


def parse_bundle(json_str: str) -> Bundle:
    """Parse + validate a bundle.json string. Raises on schema violations."""
    return Bundle.model_validate_json(json_str)


def serialize_bundle(bundle: Bundle, indent: int = 2) -> str:
    """Serialize a bundle to JSON. Stable key order for round-trip diff."""
    return bundle.model_dump_json(indent=indent, exclude_none=True)
