# SPDX-License-Identifier: Apache-2.0
"""Env-var reference resolver for bundle.json.

Bundle.json holds env-var references like '$TOGETHER_API_KEY' instead of
raw key values (per feedback_v4_0_license_slot — bundle is safe to share /
git-commit BECAUSE it never carries secrets). This module resolves those
references against /data/keys.env at runtime.

The keys.env file format is the standard `KEY=VALUE\\n` shell-env shape:

    TOGETHER_API_KEY=tgp_v1_...
    OPENAI_API_KEY=sk-proj-...
    FINNHUB_KEY=...

It MUST be mode 0600 (owner-readable only). The resolver refuses to read
keys.env if its mode is more permissive — defense-in-depth against
accidental world-readable secrets.
"""
from __future__ import annotations

import os
import re
import stat
from pathlib import Path

import structlog

logger = structlog.get_logger("investorclaw_bridge.keys")


_REF_PATTERN = re.compile(r"^\$([A-Z][A-Z0-9_]+)$")
_ENV_LINE = re.compile(r"^\s*([A-Z][A-Z0-9_]+)\s*=\s*(.+?)\s*$")


class KeyResolverError(Exception):
    """Raised when a key reference cannot be resolved."""


class KeysFileTooPermissiveError(KeyResolverError):
    """Raised when keys.env file mode is more permissive than 0600."""


def load_keys_env(keys_env: Path) -> dict[str, str]:
    """Parse a keys.env file into a dict.

    Refuses to read if file mode is more permissive than 0600 (group/other
    have any permission). Returns empty dict if file doesn't exist (so the
    container can boot with no keys configured — degrades gracefully to
    yfinance / heuristic narrator).

    Skips comment lines (starting with #) and blank lines. Skips lines
    that don't match KEY=VALUE shape. Quotes around values stripped if
    matched.
    """
    if not keys_env.exists():
        logger.info("keys.load.missing", path=str(keys_env))
        return {}

    # Defense in depth: refuse to read overly-permissive keys files
    file_mode = stat.S_IMODE(keys_env.stat().st_mode)
    if file_mode & 0o077:  # any group/other perms set
        raise KeysFileTooPermissiveError(
            f"{keys_env} has mode {oct(file_mode)} — must be 0600 (owner-only). "
            f"Run: chmod 600 {keys_env}"
        )

    keys: dict[str, str] = {}
    for lineno, raw in enumerate(keys_env.read_text().splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _ENV_LINE.match(line)
        if not m:
            logger.warning(
                "keys.load.skip_unmatched_line", path=str(keys_env), lineno=lineno
            )
            continue
        key, value = m.group(1), m.group(2)
        # Strip matching quotes
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        keys[key] = value

    logger.info("keys.load.ok", path=str(keys_env), key_count=len(keys))
    return keys


def resolve_ref(
    ref: str,
    keys: dict[str, str],
    *,
    fallback_to_env: bool = True,
    raise_on_missing: bool = False,
) -> str | None:
    """Resolve a bundle.json env-var reference like '$TOGETHER_API_KEY'.

    Args:
        ref: the reference string. Must match `^\\$[A-Z][A-Z0-9_]+$`.
        keys: dict from load_keys_env (preferred source).
        fallback_to_env: if not in keys, also try os.environ.
        raise_on_missing: if True, raise KeyResolverError when ref cannot
            be resolved. If False, return None.

    Returns:
        Resolved value, or None if not found and raise_on_missing=False.
    """
    m = _REF_PATTERN.match(ref)
    if not m:
        raise KeyResolverError(
            f"Invalid env-var reference shape: {ref!r}. "
            f"Must match '^\\$[A-Z][A-Z0-9_]+$' (e.g., '$TOGETHER_API_KEY')."
        )
    var_name = m.group(1)

    if var_name in keys:
        return keys[var_name]
    if fallback_to_env and var_name in os.environ:
        return os.environ[var_name]

    if raise_on_missing:
        raise KeyResolverError(
            f"Cannot resolve {ref!r}: not in keys.env and not in os.environ."
        )
    return None


def is_ref(value: str) -> bool:
    """True if a string is an env-var reference shape (not a raw value)."""
    return bool(_REF_PATTERN.match(value))


def reverse_lookup_ref(
    raw_value: str, keys: dict[str, str]
) -> str | None:
    """For export: given a raw key value, find a matching reference name.

    Used when exporting bundle.json from the live state — config has
    raw values in memory, but bundle.json must store references. This
    walks the keys.env dict to find a name whose value matches.

    Returns the reference like '$TOGETHER_API_KEY', or None if no
    matching env entry exists (in which case the caller must surface
    a structured error: "this key is in your config but not in
    keys.env, so we can't export it without leaking the raw value").
    """
    for var_name, value in keys.items():
        if value == raw_value:
            return f"${var_name}"
    return None
