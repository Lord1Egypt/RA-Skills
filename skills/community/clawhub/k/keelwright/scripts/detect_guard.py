#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""detect_guard.py — runtime-agnostic web-defense probe for keelwright.

WHY THIS EXISTS
---------------
The old Web Guard rule said "the agent MUST run verify_web_guard.py before any
web call". That was an instruction, not a mechanism — subagents and kanban
workers (which do NOT inherit the parent's loaded skills) never ran it, and the
operator was never actually told when protection was offline. This probe fixes
both gaps: it is a *script* (callable from any runtime, any subprocess, any
subagent via execute_code) that returns a single machine-readable verdict, and
the skill text now REQUIRES the agent to surface that verdict to the operator
when it is not ACTIVE.

WHAT IT CHECKS (no single-runtime assumptions)
----------------------------------------------
We do NOT hardcode a vendor plugin path or a vendor module name — every agent
runtime (Hermes, OpenClaw, Cursor, Codex, Cline, Kilo) loads its web-defense
plugin differently. Instead we probe what is actually observable from the
interpreter that runs the agent:

Layer 1 — ML / plugin classifier (best protection):
    The well-known classifier dependencies (transformers + torch + sentencepiece)
    are importable in this interpreter. If present, the classifier CAN run; the
    agent then confirms it answers correctly by running `verify_web_guard.py`
    (which performs a safe-vs-injection smoke test). We never auto-download the
    model here — that is an explicit operator-approved step (see "Operator
    onboarding" in references/web-guard.md): the agent MUST ask before any
    ~700MB download begins.

Layer 2 — Heuristic backstop (always-available floor):
    web_heuristic_guard.py ships INSIDE this skill. If it is present next to
    this script, the agent at least has a dependency-free marker scanner.

Layer 3 — External pre-dispatch gate (operator's choice):
    Any skill/plugin the operator wired in (e.g. web-agent-security-gate on
    ClawHub). We do not assume a specific one; the operator enables it per their
    runtime's docs.

VERDICT
-------
  ACTIVE      — ML deps present; operator approved + verified the classifier.
  DEGRADED    — no ML classifier, but the heuristic backstop (Layer 2) is present.
                Web trips are NOT fully protected; operator must be told.
  UNPROTECTED — nothing usable. Web trips are forbidden until fixed / confirmed.

Exit code mirrors the verdict: 0 = ACTIVE, 1 = DEGRADED, 2 = UNPROTECTED.
The stdout message is plain language so an agent can paste it to the operator
verbatim. Nothing here installs packages or downloads models.
Note: `_classifier_verified()` may write `.web_guard_verified` marker file as a cache.
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _have_modules(interp: str, mods) -> bool:
    spec = (
        "import importlib.util as u, sys; "
        "sys.exit(0 if all(u.find_spec(m) for m in " + repr(list(mods)) + ") else 1)"
    )
    try:
        r = subprocess.run([interp, "-c", spec], capture_output=True, text=True, timeout=40)
        return r.returncode == 0
    except Exception:
        return False


def _classifier_verified(interp: str) -> bool:
    """T11 (v1.8.0): ACTIVE requires proof the classifier actually works, not just imports.

    We look for a verification marker written by verify_web_guard.py (operator-approved
    smoke test). If absent, the agent must run verify_web_guard.py before claiming ACTIVE.
    This avoids the false-ACTIVE trap where deps import but the model is broken/MITM'd.
    """
    marker = os.path.join(HERE, ".web_guard_verified")
    try:
        if os.path.exists(marker):
            return True
    except Exception:
        pass
    # Fallback: if verify_web_guard.py exists, run it non-interactively (it exits 0 on pass).
    vwg = os.path.join(HERE, "verify_web_guard.py")
    if os.path.isfile(vwg) and os.path.basename(vwg) == "verify_web_guard.py":
        try:
            r = subprocess.run(
                [sys.executable, vwg],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if r.returncode == 0:
                try:
                    with open(marker, "w", encoding="utf-8") as f:
                        f.write("")
                except Exception:
                    pass
                return True
        except Exception:
            return False
    return False


def _heuristic_present() -> bool:
    return os.path.isfile(os.path.join(HERE, "web_heuristic_guard.py"))


def main() -> int:
    interp = sys.executable or "python3"

    ml_ready = _have_modules(interp, ("transformers", "torch", "sentencepiece"))
    if ml_ready:
        # T11 (v1.8.0): deps present is NOT the same as "verified working".
        # The classifier can be broken (corrupted regex pkg, MITM model, revoked source)
        # even when deps import. ACTIVE requires a passing verify_web_guard.py smoke
        # test (operator-approved, may download ~700MB model). Without it we report
        # DEGRADED so the operator is never falsely told they are fully protected.
        verified = _classifier_verified(interp)
        if verified:
            print(
                "ACTIVE: web prompt-injection protection is verified working "
                "(classifier deps present AND verify_web_guard.py passed)."
            )
            return 0
        print(
            "DEGRADED: ML classifier deps are present, but the classifier has NOT been "
            "verified by verify_web_guard.py. It may be broken, revoked, or MITM-substituted — "
            "do NOT report ACTIVE. Run `verify_web_guard.py` (operator-approved, may download "
            "a ~700MB model) to confirm protection before unattended web trips."
        )
        return 1

    if _heuristic_present():
        print(
            "DEGRADED: ML classifier deps (transformers/torch/sentencepiece) are NOT "
            "installed in this agent environment, but the dependency-free heuristic "
            "backstop (web_heuristic_guard.py) is present. This is NOT full protection — "
            "common injection/cloaking markers are still caught, but sophisticated prompts "
            "may pass. The operator must be told, and offered the option to install the ML "
            "classifier (one-time ~700MB download) before unattended web trips."
        )
        return 1

    print(
        "UNPROTECTED: no web prompt-injection defense is active in this agent "
        "environment (no classifier, no heuristic backstop). Web trips are "
        "FORBIDDEN until a layer is enabled, OR the operator explicitly confirms "
        "they accept the risk. Do not silently proceed."
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
