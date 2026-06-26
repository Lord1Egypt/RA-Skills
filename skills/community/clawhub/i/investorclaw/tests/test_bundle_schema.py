# SPDX-License-Identifier: Apache-2.0
"""Tests for the v4.0 bundle.json Pydantic schema.

The critical safety property: bundle.json refuses to validate raw API
keys. Every key field is an env-var reference like '$TOGETHER_API_KEY';
raw values are rejected at parse time. This is the security boundary
between "safe to git-commit" and "do not share."
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bridge"))

from investorclaw_bridge.bundle_schema import (  # noqa: E402
    Bundle,
    BundleMetadata,
    DataSourceConfig,
    McpConfig,
    MemoryConfig,
    MemoryRecord,
    NarrativeConfig,
    PortfolioRef,
    ProviderConfig,
    parse_bundle,
    serialize_bundle,
)


def _basic_metadata() -> BundleMetadata:
    return BundleMetadata(
        exported_at=datetime.now(timezone.utc),
        from_host="testhost.local",
        investorclaw_version="4.0.0a1",
    )


def test_minimal_bundle_validates() -> None:
    """A bundle with only required fields parses."""
    bundle = Bundle(metadata=_basic_metadata())
    assert bundle.version == "4.0"
    assert bundle.providers == {}
    assert bundle.portfolios == []


def test_provider_with_env_ref_parses() -> None:
    """Provider with a valid env-var reference accepts."""
    config = ProviderConfig(
        api_key_ref="$TOGETHER_API_KEY",
        default_model="MiniMaxAI/MiniMax-M2.7",
    )
    assert config.api_key_ref == "$TOGETHER_API_KEY"


def test_provider_with_raw_key_REJECTS() -> None:
    """Critical security property: raw API keys must be rejected.

    This is the single most important test in the bundle schema. If this
    ever silently passes, the bundle becomes unsafe to commit / share.
    """
    # Together raw key shape
    with pytest.raises(ValidationError, match="env-var references"):
        ProviderConfig(api_key_ref="tgp_v1_FAKE_TEST_VALUE_NEVER_DEPLOYED_PLACEHOLDER")

    # OpenAI raw key shape
    with pytest.raises(ValidationError, match="env-var references"):
        ProviderConfig(api_key_ref="sk-proj-abc123def456...")

    # Anthropic raw key shape
    with pytest.raises(ValidationError, match="env-var references"):
        ProviderConfig(api_key_ref="sk-ant-api03-xxx...")

    # Bash-style env-var with braces (technically valid bash but not our format)
    with pytest.raises(ValidationError, match="env-var references"):
        ProviderConfig(api_key_ref="${TOGETHER_API_KEY}")

    # Empty string
    with pytest.raises(ValidationError):
        ProviderConfig(api_key_ref="")


def test_data_source_raw_key_REJECTS() -> None:
    """Data source keys must also be env-var references."""
    with pytest.raises(ValidationError, match="env-var references"):
        DataSourceConfig(api_key_ref="raw_finnhub_key_here")


def test_mcp_token_raw_value_REJECTS() -> None:
    """MCP auth tokens must also be env-var references."""
    with pytest.raises(ValidationError, match="env-var references"):
        McpConfig(auth_token_ref="raw_token_here")


def test_provider_with_no_key_ref_parses() -> None:
    """Provider config with no api_key_ref is valid (e.g., for local providers)."""
    config = ProviderConfig(base_url="http://localhost:11434", default_model="gemma4:e4b")
    assert config.api_key_ref is None


def test_mcp_default_localhost() -> None:
    """MCP config defaults to localhost-only — secure default."""
    config = McpConfig()
    assert config.bind == "127.0.0.1"
    assert config.port == 8090


def test_mcp_remote_bind_allowed() -> None:
    """Remote bind (0.0.0.0) is explicit, not default."""
    config = McpConfig(bind="0.0.0.0", auth_token_ref="$IC_MCP_TOKEN")
    assert config.bind == "0.0.0.0"


def test_portfolio_account_type_validated() -> None:
    """Portfolio account_type must be from the enumerated list."""
    PortfolioRef(
        id="ubs_taxable",
        source_file="ubs.xls",
        broker="ubs",
        account_type="taxable",
    )

    with pytest.raises(ValidationError):
        PortfolioRef(
            id="x",
            source_file="x.xls",
            broker="ubs",
            account_type="bizarre_type_not_in_enum",  # type: ignore[arg-type]
        )


def test_full_bundle_round_trip() -> None:
    """Serialize → parse → equal."""
    bundle = Bundle(
        providers={
            "together": ProviderConfig(
                api_key_ref="$TOGETHER_API_KEY",
                default_model="MiniMaxAI/MiniMax-M2.7",
            ),
        },
        data_sources={"finnhub": DataSourceConfig(api_key_ref="$FINNHUB_KEY")},
        portfolios=[
            PortfolioRef(
                id="ubs_taxable",
                source_file="ubs_07_04_2026.xls",
                broker="ubs",
                account_type="taxable",
            ),
        ],
        narrative=NarrativeConfig(tier="auto", depth="standard", provider_route="together"),
        mcp=McpConfig(),
        memory=MemoryConfig(),
        memories=[
            MemoryRecord(
                id="mem_abc",
                content="User flagged BABA as never-sell sentimental position",
                category="preferences",
                tags=["portfolio", "user-rule"],
                created_at=datetime.now(timezone.utc),
            ),
        ],
        metadata=_basic_metadata(),
    )

    serialized = serialize_bundle(bundle)
    parsed = parse_bundle(serialized)

    # Equality at the level that matters
    assert parsed.version == bundle.version
    assert parsed.providers["together"].api_key_ref == "$TOGETHER_API_KEY"
    assert parsed.portfolios[0].id == "ubs_taxable"
    assert parsed.memories[0].id == "mem_abc"


def test_extra_fields_REJECTED() -> None:
    """Schema is strict. Unknown fields fail validation."""
    raw = """
    {
      "version": "4.0",
      "totally_made_up_field": "something",
      "metadata": {
        "exported_at": "2026-05-01T08:15:00Z",
        "from_host": "test",
        "investorclaw_version": "4.0.0a1"
      }
    }
    """
    with pytest.raises(ValidationError, match="extra"):
        parse_bundle(raw)


def test_old_version_rejected() -> None:
    """Bundles must be v4.0. Older versions need migration first."""
    raw = """
    {
      "version": "3.5",
      "metadata": {
        "exported_at": "2026-05-01T08:15:00Z",
        "from_host": "test",
        "investorclaw_version": "3.5.0"
      }
    }
    """
    with pytest.raises(ValidationError):
        parse_bundle(raw)
