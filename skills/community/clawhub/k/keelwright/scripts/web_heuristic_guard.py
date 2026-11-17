#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""web_heuristic_guard.py — lightweight injection fallback for keelwright.

WHY: `injection-guard` (DeBERTa ML) is the primary layer, but if its venv deps break
(e.g. a corrupted `regex` package -> circular import -> classifier unavailable), the ML
layer silently becomes a no-op. A safety engine must NEVER fall to no-op. This script is a
dependency-free heuristic backstop: it flags the most common indirect-prompt-injection and
agent-cloaking markers using plain string/regex matching. Stdlib only (no torch/transformers).

It is NOT a replacement for injection-guard — it is the floor that holds when the ceiling
collapses. When it fires, it logs to the attack registry like any other detection.

Rules (commercial-use white list sources, adapted in operator's own words; no verbatim copy):
- injection-guard internals: gweber/hermes-injection-guard (MIT)
- agent-defense layering: scastile/hermes-agent-defense (MIT)
- web-agent-security-gate: ClawHub / OpenClaw community, SPDX-License-Identifier: MIT-0

USAGE:
  python web_heuristic_guard.py --text "web page content here"
  # prints JSON {"flagged": bool, "markers": [...], "severity": "..."} and exits 1 if flagged
  # or, pipe via stdin:
  cat page.html | python web_heuristic_guard.py

Integrate in SKILL.md Web Guard: run this when verify_web_guard.py reports the ML layer
unavailable, OR always as a second opinion. On flag -> signal + log to attack_registry.py.
"""
import argparse
import json
import re
import sys

# Markers ordered by severity. Each is a compiled pattern (case-insensitive).
# CRITICAL: direct instruction-override attempts.
# CRITICAL: direct instruction-override attempts + code/exec injection.
CRITICAL = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(your\s+)?(prior\s+)?(system\s+)?(instructions|prompt)",
    r"you\s+are\s+now\s+",  # role-change / jailbreak preamble
    r"new\s+instructions\s*:",
    r"system\s*:\s*\[",  # fake [System: ...] banner
    r"invoke\s+this\s+skill",
    r"run\s+the\s+(following\s+)?(command|script|tool)",
    r"exfiltrate",
    r"send\s+(all\s+)?(data|keys?|tokens?|secrets?)\s+to",
    # injection: XSS / script injection / template injection
    r"<script",
    r"<\s*scr",  # catches <scr1pt> style obfuscation too
    r"onerror\s*=",
    r"javascript\s*:",
    r"\{\{.*\}\}",  # template-injection ({{7*7}})
    # SQL / command injection fragments (loose: catches missing-space mutations)
    r"(drop|delete|truncate|insert|update)\s*(table|from|into)?",
    r"(union\s+select|;\s*select\s+|\bselect\s+\*\s+from)",
    r"`\s*;?\s*(rm|curl|wget|bash|sh|nc)\s",
    r">>>\s*(drop|delete|select|insert)",  # markdown code-fence SQL
    # F31 (v1.9.0) canonical cases: secret + doom-loop
    r"password\s*=\s*['\"][^'\"]{4,}",  # hardcoded credential
    r"api[_-]?key\s*=\s*['\"][^'\"]{8,}",
    r"while\s+True\s*:",  # unbounded loop (doom-loop risk)
    r"for\s+\w+\s+in\s+range\(\s*\d{4,}",  # absurdly large range, no stop
    # jailbreak personas
    r"pretend\s+you\s+are\s+(dan|an\s+unrestricted|without\s+rules)",
    r"developer\s+mode\s+(unlocked|enabled|on)",
]
# HIGH: cloaking / tool-abuse framing.
HIGH = [
    r"do\s+not\s+tell\s+the\s+user",
    r"keep\s+this\s+(secret|hidden)",
    r"the\s+user\s+(should\s+not|won't|does\s+not)\s+(see|know)",
    r"bypass\s+(the\s+)?(security|guard|check)",
    r"override\s+(the\s+)?(safety|policy|rule)",
    r"continue\s+this\s+(video|task)\s+from",
    r"base64\s+decode\s+and\s+execute",
    r"no\s+(restrictions|limits|filters)",
    r"ignore\s+(all\s+)?(safety|ethical|moral)\s+(guidelines|rules)",
]
# MEDIUM: suspicious but ambiguous phrasing.
MEDIUM = [
    r"as\s+an\s+ai\s+language\s+model",
    r"hypothetically",
    r"for\s+research\s+purposes\s+only",
    r"developer\s+mode",
]


def compile_group(patterns):
    # T49 (v1.8.0): cap regex matching time to avoid ReDoS if a hostile/over-broad
    # pattern is ever added via --add-pattern. Python 3.11+ supports the timeout arg.
    kwargs = {"re.IGNORECASE": re.IGNORECASE}
    try:
        return [(p, re.compile(p, re.IGNORECASE, timeout=0.5)) for p in patterns]
    except TypeError:
        # Older Python without timeout support — compile without it.
        return [(p, re.compile(p, re.IGNORECASE)) for p in patterns]


CRIT_C = compile_group(CRITICAL)
HIGH_C = compile_group(HIGH)
MED_C = compile_group(MEDIUM)


def scan(text: str):
    hits = []
    for label, grp in (("CRITICAL", CRIT_C), ("HIGH", HIGH_C), ("MEDIUM", MED_C)):
        for pat, rx in grp:
            if rx.search(text):
                hits.append({"severity": label, "pattern": pat})
    severity = None
    # T14 (v1.8.0): MEDIUM markers are advisory only — they do NOT raise the
    # flagged/blocking severity. A page with only MEDIUM phrasing is reported as
    # advisory, not FLAGGED. Only CRITICAL/HIGH escalate.
    if any(h["severity"] == "CRITICAL" for h in hits):
        severity = "CRITICAL"
    elif any(h["severity"] == "HIGH" for h in hits):
        severity = "HIGH"
    advisory = [h["pattern"] for h in hits if h["severity"] == "MEDIUM"]
    flagged = severity is not None
    return hits, severity, advisory


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default=None)
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    args = ap.parse_args()

    if args.text is not None:
        text = args.text
    else:
        text = sys.stdin.read()

    hits, severity, advisory = scan(text)
    flagged = bool(hits) and severity is not None
    out = {"flagged": flagged, "severity": severity,
           "markers": [h["pattern"] for h in hits if h["severity"] != "MEDIUM"],
           "advisory": advisory}
    if args.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        if flagged:
            print(f"FLAGGED [{severity}]: {', '.join(out['markers'])}")
        elif advisory:
            print(f"ADVISORY (not flagged): {', '.join(advisory)}")
        else:
            print("clean")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
