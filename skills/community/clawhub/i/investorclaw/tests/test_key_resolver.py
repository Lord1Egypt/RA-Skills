# SPDX-License-Identifier: Apache-2.0
"""Tests for key_resolver — env-var reference resolution + safety properties."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bridge"))

from investorclaw_bridge.key_resolver import (  # noqa: E402
    KeyResolverError,
    KeysFileTooPermissiveError,
    is_ref,
    load_keys_env,
    resolve_ref,
    reverse_lookup_ref,
)


# ─── load_keys_env ─────────────────────────────────────────────────────


def _write_keys_file(path: Path, content: str, mode: int = 0o600) -> Path:
    path.write_text(content)
    path.chmod(mode)
    return path


def test_load_keys_env_returns_empty_when_missing(tmp_path: Path) -> None:
    """Missing keys.env → empty dict (boots gracefully without keys)."""
    assert load_keys_env(tmp_path / "keys.env") == {}


def test_load_keys_env_parses_basic_format(tmp_path: Path) -> None:
    p = _write_keys_file(
        tmp_path / "keys.env",
        "TOGETHER_API_KEY=tgp_v1_abc\nOPENAI_API_KEY=sk-proj-xyz\n",
    )
    keys = load_keys_env(p)
    assert keys == {
        "TOGETHER_API_KEY": "tgp_v1_abc",
        "OPENAI_API_KEY": "sk-proj-xyz",
    }


def test_load_keys_env_skips_blank_lines_and_comments(tmp_path: Path) -> None:
    p = _write_keys_file(
        tmp_path / "keys.env",
        "# This is a comment\n\nFINNHUB_KEY=abc123\n# Another comment\nFRED_API_KEY=xyz789\n\n",
    )
    keys = load_keys_env(p)
    assert keys == {"FINNHUB_KEY": "abc123", "FRED_API_KEY": "xyz789"}


def test_load_keys_env_strips_quotes(tmp_path: Path) -> None:
    p = _write_keys_file(
        tmp_path / "keys.env",
        'TOGETHER_API_KEY="tgp_v1_quoted"\nFINNHUB_KEY=\'finnhub_quoted\'\n',
    )
    keys = load_keys_env(p)
    assert keys["TOGETHER_API_KEY"] == "tgp_v1_quoted"
    assert keys["FINNHUB_KEY"] == "finnhub_quoted"


def test_load_keys_env_REJECTS_overly_permissive_mode(tmp_path: Path) -> None:
    """keys.env mode > 0600 must be rejected (defense-in-depth security)."""
    p = _write_keys_file(
        tmp_path / "keys.env",
        "TOGETHER_API_KEY=tgp_v1_abc\n",
        mode=0o644,  # group + other readable — UNSAFE
    )
    with pytest.raises(KeysFileTooPermissiveError, match="must be 0600"):
        load_keys_env(p)


def test_load_keys_env_REJECTS_world_readable(tmp_path: Path) -> None:
    p = _write_keys_file(tmp_path / "keys.env", "X=1\n", mode=0o604)
    with pytest.raises(KeysFileTooPermissiveError):
        load_keys_env(p)


def test_load_keys_env_REJECTS_group_readable(tmp_path: Path) -> None:
    p = _write_keys_file(tmp_path / "keys.env", "X=1\n", mode=0o640)
    with pytest.raises(KeysFileTooPermissiveError):
        load_keys_env(p)


def test_load_keys_env_accepts_0400(tmp_path: Path) -> None:
    """Mode 0400 (read-only owner) is even more locked-down than 0600 — accept."""
    p = _write_keys_file(tmp_path / "keys.env", "MY_KEY=1\n", mode=0o400)
    assert load_keys_env(p) == {"MY_KEY": "1"}


def test_load_keys_env_REJECTS_world_writable(tmp_path: Path) -> None:
    p = _write_keys_file(tmp_path / "keys.env", "TOGETHER_API_KEY=x\n", mode=0o602)
    with pytest.raises(KeysFileTooPermissiveError):
        load_keys_env(p)


# ─── resolve_ref ────────────────────────────────────────────────────────


def test_resolve_ref_finds_in_keys() -> None:
    keys = {"TOGETHER_API_KEY": "tgp_v1_abc"}
    assert resolve_ref("$TOGETHER_API_KEY", keys) == "tgp_v1_abc"


def test_resolve_ref_falls_back_to_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FRED_API_KEY", "fred_from_env")
    assert resolve_ref("$FRED_API_KEY", {}) == "fred_from_env"


def test_resolve_ref_keys_takes_precedence_over_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FRED_API_KEY", "fred_from_env")
    keys = {"FRED_API_KEY": "fred_from_keys_file"}
    assert resolve_ref("$FRED_API_KEY", keys) == "fred_from_keys_file"


def test_resolve_ref_missing_returns_none_by_default() -> None:
    assert resolve_ref("$NONEXISTENT_KEY", {}, fallback_to_env=False) is None


def test_resolve_ref_missing_raises_when_requested() -> None:
    with pytest.raises(KeyResolverError, match="Cannot resolve"):
        resolve_ref(
            "$NONEXISTENT_KEY", {}, fallback_to_env=False, raise_on_missing=True
        )


def test_resolve_ref_invalid_shape_raises() -> None:
    """Raw values, lowercase, bash-style ${...} all rejected."""
    with pytest.raises(KeyResolverError, match="Invalid env-var reference shape"):
        resolve_ref("tgp_v1_raw_value", {})
    with pytest.raises(KeyResolverError):
        resolve_ref("${TOGETHER_API_KEY}", {})  # bash form
    with pytest.raises(KeyResolverError):
        resolve_ref("$lowercase_key", {})


# ─── is_ref / reverse_lookup_ref ────────────────────────────────────────


def test_is_ref() -> None:
    assert is_ref("$TOGETHER_API_KEY") is True
    assert is_ref("$FRED_API_KEY") is True
    assert is_ref("tgp_v1_abc") is False
    assert is_ref("${TOGETHER_API_KEY}") is False
    assert is_ref("$lowercase") is False
    assert is_ref("") is False


def test_reverse_lookup_ref_finds_match() -> None:
    """Export path: given a raw value, find the env-var name that holds it."""
    keys = {
        "TOGETHER_API_KEY": "tgp_v1_abc",
        "OPENAI_API_KEY": "sk-proj-xyz",
    }
    assert reverse_lookup_ref("tgp_v1_abc", keys) == "$TOGETHER_API_KEY"
    assert reverse_lookup_ref("sk-proj-xyz", keys) == "$OPENAI_API_KEY"


def test_reverse_lookup_ref_returns_none_when_no_match() -> None:
    """If the raw value isn't in keys.env, export must surface a structured error
    (caller's responsibility) rather than leak the raw value."""
    keys = {"TOGETHER_API_KEY": "tgp_v1_abc"}
    assert reverse_lookup_ref("some_other_value", keys) is None
