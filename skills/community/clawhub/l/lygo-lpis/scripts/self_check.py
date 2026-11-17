#!/usr/bin/env python3
"""LPIS skill self-check — P0 analyzer + ingest consent gate + security doc presence."""

from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
STACK = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(STACK))

from lygo_lpis.analyzer import PromptAnalyzer  # noqa: E402
from lygo_lpis.consent import require_ingest_authorization  # noqa: E402
from lygo_lpis.gatekeeper import P0Gatekeeper  # noqa: E402

REQUIRED_DOCS = (
    SKILL_DIR / "references" / "SECURITY.md",
    SKILL_DIR / "references" / "SKILLSPECTOR_AUDIT.md",
    SKILL_DIR / "references" / "AGENT_CONTRACT.md",
)


def check_security_docs() -> None:
    skill_md = SKILL_DIR / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    for phrase in (
        "Security notice",
        "When NOT to use",
        "--i-authorize",
        "ingest leaked",
    ):
        assert phrase in text, f"SKILL.md missing: {phrase}"
    for path in REQUIRED_DOCS:
        assert path.is_file(), f"missing {path.name}"
        body = path.read_text(encoding="utf-8")
        assert len(body) > 200, f"{path.name} too short"


def check_consent_gate() -> None:
    blocked = require_ingest_authorization(flag=False)
    assert blocked and blocked.get("error") == "ingest_not_authorized"
    assert require_ingest_authorization(flag=True) is None


def check_analyzer() -> None:
    g = P0Gatekeeper()
    assert g.validate_text("plan and verify")["verdict"] in ("AMPLIFY", "SOFTEN", "QUARANTINE")
    a = PromptAnalyzer().analyze("plan delegate verify safety")
    assert a["pattern_counts"]["planning"] >= 1


def main() -> int:
    check_security_docs()
    check_consent_gate()
    check_analyzer()
    print("OK lygo-lpis self_check v1.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())