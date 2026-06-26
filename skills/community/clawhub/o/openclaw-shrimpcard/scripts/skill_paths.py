#!/usr/bin/env python3
import os
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = SKILL_ROOT / "schemas"

AGENT_EVIDENCE_SCHEMA_PATH = SCHEMA_DIR / "agent-evidence-schema.json"
SUBMISSION_SCHEMA_PATH = SCHEMA_DIR / "agent-self-intro-submission-schema.json"
SHARE_CARD_SCHEMA_PATH = SCHEMA_DIR / "share-card-schema.json"
CARD_TEMPLATE_PATH = SKILL_ROOT / "assets" / "card-template.html"


def is_fixture_path(path: Path) -> bool:
    try:
        resolved = path.resolve()
    except Exception:
        resolved = path
    return "examples" in resolved.parts


def require_live_input(path: Path, label: str):
    if is_fixture_path(path) and os.environ.get("SHRIMPCARD_ALLOW_FIXTURES") != "1":
        raise SystemExit(
            f"[FAIL] {label}: {path} is under examples/ and is fixture-only. "
            "Provide a real agent evidence/submission file or set SHRIMPCARD_ALLOW_FIXTURES=1 for smoke tests."
        )
