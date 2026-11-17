"""Shared stack resolution — skill + planter scripts."""

from __future__ import annotations

import os
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def resolve_stack_root(explicit: str | None = None) -> Path:
    if explicit:
        p = Path(explicit).resolve()
        _assert_stack(p)
        return p
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        p = Path(env).resolve()
        _assert_stack(p)
        return p
    for anc in SKILL_ROOT.parents:
        if (anc / "tools" / "build_kernel_eggs.py").is_file():
            _assert_stack(anc)
            return anc
    raise SystemExit("Set LYGO_STACK_ROOT to a lygo-protocol-stack clone")


def _assert_stack(p: Path) -> None:
    required = [
        p / "tools" / "build_kernel_eggs.py",
        p / "tools" / "verify_kernel_eggs.py",
        p / "tools" / "retrieve_kernel_egg.py",
        p / "protocol0_byte_entropy_filter" / "fixtures" / "p0_canonical.sha256",
    ]
    missing = [str(x.relative_to(p)) for x in required if not x.is_file()]
    if missing:
        raise SystemExit(f"Invalid stack root {p}; missing: {missing}")


def require_consent(flag: bool) -> None:
    """Require explicit plant/retrieve consent. Never infer from chat alone."""
    if flag:
        return
    if os.environ.get("LYGO_EGG_PLANT_CONSENT", "").lower() in ("yes", "1", "true"):
        return
    print("Consent required: --i-consent or LYGO_EGG_PLANT_CONSENT=yes", file=sys.stderr)
    print("Read references/CONSENT_AND_ETHICS.md and references/AGENT_CONTRACT.md", file=sys.stderr)
    raise SystemExit(2)