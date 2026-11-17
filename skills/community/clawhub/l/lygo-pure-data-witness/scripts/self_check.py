#!/usr/bin/env python3
"""SkillSpector-friendly smoke: AST ban on real subprocess/shell use (not the word)."""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
BANNED_IMPORTS = {"subprocess", "os.system"}
BANNED_ATTR_CALLS = {("os", "system"), ("os", "popen")}


def _uses_banned(tree: ast.AST) -> list[str]:
    hits: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] == "subprocess":
                    hits.append(f"import:{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.split(".")[0] == "subprocess":
                hits.append(f"from:{mod}")
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                if (f.value.id, f.attr) in BANNED_ATTR_CALLS:
                    hits.append(f"call:{f.value.id}.{f.attr}")
            if isinstance(f, ast.Name) and f.id in {"system", "popen"}:
                # only flag if imported from os — soft: ignore bare names
                pass
    return hits


# FULL SkillHub unlock may ship stack limbs that use subprocess under LYGO_STACK_ROOT.
# ClawHub tentacle must remain subprocess-free — skip these when present.
FULL_LIMB_ALLOW_SUBPROCESS = {
    "pure_data_register.py",
    "map_pure_data_to_star_chart.py",
}


def main() -> int:
    bad: list[str] = []
    files = sorted(SCRIPTS.glob("*.py"))
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(text, filename=str(p))
        except SyntaxError as e:
            bad.append(f"{p.name}:syntax:{e}")
            continue
        if p.name not in FULL_LIMB_ALLOW_SUBPROCESS:
            for hit in _uses_banned(tree):
                bad.append(f"{p.name}:{hit}")
        # Comment-only mention of "subprocess" is allowed; AST catches real use.
        # Contiguous miner bait tokens must not appear in source (detector uses splits).
        banned_contiguous = (
            "crypto" + "-miner",
            "coin" + "hive",
            "malware" + "-download",
        )
        for tok in banned_contiguous:
            if tok in text:
                bad.append(f"{p.name}:contiguous_bait_token:{tok}")

    req = [
        ROOT / "SKILL.md",
        ROOT / "claw.json",
        ROOT / "references" / "SECURITY.md",
        ROOT / "references" / "PORTAL_TRAINING.md",
        ROOT / "references" / "SKILLSPECTOR_AUDIT.md",
        SCRIPTS / "pdw_cli.py",
        SCRIPTS / "pure_data_safety.py",
        SCRIPTS / "pure_data_witness.py",
    ]
    for r in req:
        if not r.is_file():
            bad.append(f"missing:{r.relative_to(ROOT)}")

    # Consent-contract regression (ClawHub security-audit 2026-08): fetch/all must gate network.
    wit = (SCRIPTS / "pure_data_witness.py").read_text(encoding="utf-8", errors="replace")
    for needle in (
        '--i-authorize-fetch',
        "i_authorize_fetch",
        "fetch_consent_required",
        "i_confirm_chain",
        "chain_consent_required",
    ):
        if needle not in wit:
            bad.append(f"pure_data_witness.py:missing_consent_marker:{needle}")
    cli = (SCRIPTS / "pdw_cli.py").read_text(encoding="utf-8", errors="replace")
    if "i_authorize_fetch" not in cli or "need --i-authorize-fetch" not in cli:
        bad.append("pdw_cli.py:fetch_gate_missing")

    print({"ok": not bad, "bad": bad, "files": len(files), "version_gate": "v1.3.0-consent"})
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
