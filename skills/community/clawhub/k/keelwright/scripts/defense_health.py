#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""defense_health.py — full-layer web-defense health check for keelwright.

WHY: verify_web_guard.py only checks the ML layer (injection-guard / DeBERTa). A safety
engine must know the state of EVERY layer, not just one. This script checks all of them and
reports pass | fail | unverified per layer, plus a concrete fix recommendation on failure.

Layers checked:
  A. injection-guard (ML)   — via scripts/verify_web_guard.py in the agent's Python environment
  B. caught_attacks.jsonl   — the log file exists AND is writable (attacks must be recorded)
  C. security-guidance       — listed in config.yaml plugins.enabled (best-effort, if readable)
  D. agent-defense           — skill present (optional; unverified if not installed)

On any CRITICAL layer fail, exit non-zero so a dispatch decision can be gated — but the
AGENT's response (per keelwright SKILL.md) is WARN + RECOMMEND FIX NOW, NOT a hard block.
The heuristic fallback (web_heuristic_guard.py) stays on regardless.

Sources (commercial-use white list, adapted in operator's own words; no verbatim copy):
- injection-guard: gweber/hermes-injection-guard (MIT)
- agent-defense: scastile/hermes-agent-defense (MIT)
- web-agent-security-gate: ClawHub / OpenClaw community, MIT-0
- recovery: corrupted `regex` in the agent's Python environment is the usual fix (see FIX_REGEX below; self-contained)

USAGE:
  python defense_health.py            # human summary + JSON
  python defense_health.py --json     # JSON only
"""
import argparse
import json
import os
import subprocess
import sys

# Runtime-agnostic: the agent's Python interpreter IS the venv we need. We run
# verify_web_guard.py with the same interpreter that is running this script, so there is
# no hardcoded vendor path or home dir to guess (works on Hermes, OpenClaw, Cursor, Codex,
# Cline, Kilo, and any venv-based agent on Windows / Linux / macOS).
# Optional opt-in override for callers that know a specific agent Python:
#   KEELWRIGHT_AGENT_PYTHON=/path/to/python
import sys as _sys
VENV_CANDIDATES = [_sys.executable]
if os.environ.get("KEELWRIGHT_AGENT_PYTHON"):
    VENV_CANDIDATES.insert(0, os.environ["KEELWRIGHT_AGENT_PYTHON"])
HERE = os.path.dirname(os.path.abspath(__file__))
VERIFY = os.path.join(HERE, "verify_web_guard.py")
# Home dir for keelwright-managed artifacts (attack log, config). Override with KEELWRIGHT_HOME.
HERMES_HOME = os.environ.get("KEELWRIGHT_HOME", os.path.join(os.path.expanduser("~"), ".hermes"))
CAUGHT = os.path.join(HERMES_HOME, "injection-guard", "caught_attacks.jsonl")
CONFIG = os.path.join(HERMES_HOME, "config.yaml")
AGENT_DEFENSE = os.path.join(HERMES_HOME, "skills", "agent-defense", "SKILL.md")

# Fix recommendation: corrupted `regex` package in the agent's Python venv is the usual
# cause of the injection-guard ML layer silently becoming a no-op (circular import on `_regex`).
# Runtime-agnostic — works for Hermes, OpenClaw, or any agent that runs this skill in a venv.
FIX_REGEX = (
    "The ML layer (injection-guard / DeBERTa) is down. Most often the `regex` package in your "
    "agent's Python environment is corrupted (e.g. after a pip upgrade). Fix: in that environment "
    "run `python -m pip install --force-reinstall --no-deps regex`, then re-run "
    "`python scripts/verify_web_guard.py` (expect PASS: injection-guard is ACTIVE). "
    "If torch/transformers/sentencepiece are missing from the environment, install them — without "
    "them the ML layer is a silent no-op. The verify script prints the exact venv/python to use."
)


def find_venv_python():
    for c in VENV_CANDIDATES:
        if os.path.isfile(c):
            return c
    return None


def check_injection_guard():
    vpy = find_venv_python()
    if not vpy:
        return "unverified", "agent Python environment not found; run scripts/verify_web_guard.py manually"
    if not os.path.isfile(VERIFY):
        return "unverified", "verify_web_guard.py not beside this script"
    r = subprocess.run([vpy, VERIFY], capture_output=True, text=True)
    if r.returncode == 0:
        return "pass", "injection-guard ACTIVE (DeBERTa classifier loads + hook fires)"
    # not active — try to surface the reason
    reason = "see verify_web_guard.py output"
    for line in (r.stdout + r.stderr).splitlines():
        if "FAIL" in line or "unavailable" in line or "regex" in line.lower():
            reason = line.strip()
            break
    return "fail", f"injection-guard NOT active: {reason}"


def check_caught_log():
    d = os.path.dirname(CAUGHT)
    if not os.path.isdir(d):
        return "fail", f"injection-guard dir missing: {d} (attacks won't be recorded)"
    try:
        with open(CAUGHT, "a", encoding="utf-8") as f:
            pass
        return "pass", f"caught_attacks.jsonl writable: {CAUGHT}"
    except OSError as e:
        return "fail", f"caught_attacks.jsonl NOT writable: {e}"


def check_security_guidance():
    if not os.path.isfile(CONFIG):
        return "unverified", f"config.yaml not found at {CONFIG}"
    try:
        txt = open(CONFIG, encoding="utf-8").read()
    except OSError:
        return "unverified", "config.yaml not readable"
    # crude parse: plugins.enabled block should list security-guidance + injection-guard
    has_ig = "injection-guard" in txt
    has_sg = "security-guidance" in txt
    if has_ig and has_sg:
        return "pass", "config.yaml lists injection-guard + security-guidance in plugins.enabled"
    missing = [n for n, ok in (("injection-guard", has_ig), ("security-guidance", has_sg)) if not ok]
    return "fail", f"config.yaml missing from plugins.enabled: {', '.join(missing)}"


def check_agent_defense():
    if os.path.isfile(AGENT_DEFENSE):
        return "pass", "agent-defense skill present"
    return "unverified", "agent-defense not installed (optional layer; skip if unused)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    layers = {
        "injection_guard_ml": check_injection_guard(),
        "caught_attacks_log": check_caught_log(),
        "security_guidance_cfg": check_security_guidance(),
        "agent_defense": check_agent_defense(),
    }
    # critical = must be healthy for safe web trips
    critical = {"injection_guard_ml", "caught_attacks_log"}
    any_fail = any(v[0] == "fail" for v in layers.values())

    out = {k: {"status": v[0], "detail": v[1]} for k, v in layers.items()}
    out["critical_layer_failed"] = any(layers[k][0] == "fail" for k in critical)
    out["recommendation"] = FIX_REGEX if out["critical_layer_failed"] else "none"

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("Keelwright defense health:\n")
        for k, (st, det) in layers.items():
            tag = {"pass": "PASS", "fail": "FAIL", "unverified": "UNVERIFIED"}[st]
            print(f"  [{tag}] {k}: {det}")
        print()
        if out["critical_layer_failed"]:
            print("⚠️ Web defense NOT fully operational. Recommend fixing NOW:")
            print(f"     {FIX_REGEX}")
        else:
            print("✅ Web defense layers healthy (or optional layers unverified).")

    sys.exit(1 if out["critical_layer_failed"] else 0)


if __name__ == "__main__":
    main()
