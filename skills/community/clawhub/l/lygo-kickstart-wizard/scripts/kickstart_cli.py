#!/usr/bin/env python3
"""
LYGO Kickstart Wizard — UX bridge for the ClawHub lattice.

Plain-English onboarding that routes users to the right tools without
requiring them to read source code first.

Intents:
  start      interactive menu
  map        ecosystem map (what exists + when to use it)
  analyze    run local Ops Detector on text/file (if skill present)
  mint       guided mint-verify walkthrough + optional local hash receipt
  lattice    quick public lattice health check (HTTPS GET only)
  next       roadmap: radar, walkthrough skill, CLI bridge

Security:
  - No subprocess / shell
  - Network: opt-in lattice intent only (HTTPS GET allowlist)
  - Writes: opt-in --write only
  - No auto git / HF / ClawHub / social

Signature: Delta9Phi963-LYGO-KICKSTART-WIZARD-v1.0.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SIG = "Delta9Phi963-LYGO-KICKSTART-WIZARD-v1.0.0"
VERSION = "1.0.0"
UA = "LYGO-KickstartWizard/1.0.0 (+https://clawhub.ai/deepseekoracle; +https://eternalhaven.ca)"

# Fixed public health endpoints (same dual-ledger idea as public-lattice-gate)
LATTICE_ENDPOINTS = [
    {
        "id": "immutable_anchors",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/network_builder/IMMUTABLE_ANCHORS.json",
        "label": "Link ledger (immutable anchors)",
    },
    {
        "id": "star_feed",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json",
        "label": "Star Chart feed",
    },
    {
        "id": "star_chart",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "label": "Haven Star Chart (visual map)",
    },
    {
        "id": "clawhub",
        "url": "https://clawhub.ai/deepseekoracle",
        "label": "ClawHub publisher profile",
    },
]

ECOSYSTEM_MAP = [
    {
        "need": "Check if the public lattice is up",
        "skill": "lygo-public-lattice-gate / this wizard → lattice",
        "plain": "Health-check public mirrors. No install of the full stack required.",
    },
    {
        "need": "Analyze a statement or conversation for evasion / ops signals",
        "skill": "lygo-ops-detector (via this wizard → analyze)",
        "plain": "Local heuristics only. Not a person verdict. Consent before private mail/logs.",
    },
    {
        "need": "Turn a prompt pack into a verifiable hash + anchor snippet",
        "skill": "lygo-mint-verifier (this wizard → mint guides you)",
        "plain": "Create a receipt you can post anywhere. No secrets in the pack.",
    },
    {
        "need": "See the full skill constellation",
        "skill": "Haven Star Chart",
        "plain": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html — filter CLAWHUB / SKILL",
    },
    {
        "need": "Champion advice (truth, architecture, time…)",
        "skill": "lygo-champion-council / lygo-champion-*",
        "plain": "Advisory personas. They advise; you decide.",
    },
    {
        "need": "Full stack operator audits",
        "skill": "lygo-protocol-stack-operator",
        "plain": "For engineers with a local lygo-protocol-stack checkout.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def https_only(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False


def fetch_get(url: str, timeout: float = 15.0) -> dict[str, Any]:
    if not https_only(url):
        return {"ok": False, "error": "https_only"}
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(500_000)
            return {
                "ok": 200 <= resp.status < 400,
                "status": resp.status,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest() if body else None,
            }
    except Exception as e:
        return {"ok": False, "error": type(e).__name__, "detail": str(e)[:120]}


def find_ops_detector() -> Path | None:
    """Locate lygo_ops_detector.py near this skill or under LYGO_STACK_ROOT."""
    here = Path(__file__).resolve()
    candidates = [
        here.parents[2] / "lygo-ops-detector" / "scripts" / "lygo_ops_detector.py",
        here.parents[1] / "vendor" / "lygo_ops_detector.py",
    ]
    stack = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if stack:
        candidates.append(
            Path(stack) / "clawhub" / "mirrors" / "lygo-ops-detector" / "scripts" / "lygo_ops_detector.py"
        )
    # common install locations
    home = Path.home()
    candidates += [
        home / ".grok" / "skills" / "lygo-ops-detector" / "scripts" / "lygo_ops_detector.py",
        Path(r"I:\E Drive\.grok\skills\lygo-ops-detector\scripts\lygo_ops_detector.py"),
        Path(r"D:\lygo-protocol-stack\clawhub\mirrors\lygo-ops-detector\scripts\lygo_ops_detector.py"),
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def plain_ops_result(report: Any) -> dict[str, Any]:
    """Translate OpsReport into plain English."""
    ops = float(getattr(report, "ops_score", 0) or 0)
    ev = float(getattr(report, "evasion_index", 0) or 0)
    verdict = str(getattr(report, "overall_verdict", "") or "")
    if ev > 0.7:
        level = "strong_evasion_signals"
        plain = (
            "The text shows **strong evasion-style patterns** (deflection, burden-shifting, "
            "gaslighting language, etc.). This is a discourse signal — not a judgment about a person. "
            "Review the original claims with primary sources before acting."
        )
    elif ops >= 0.65:
        level = "elevated_cluster"
        plain = (
            "Several signal channels together score at the **operational bar (≥ 0.65)**. "
            "Worth a careful human read. Still not proof of identity or guilt."
        )
    elif ops >= 0.05:
        level = "weak_only"
        plain = (
            "Only **weak/calibration-level** signals. Fine for ranking short samples; "
            "not enough alone for any real-world accusation."
        )
    else:
        level = "clear"
        plain = "No clear operational-deception pattern at the published thresholds."

    return {
        "level": level,
        "ops_score": ops,
        "evasion_index": ev,
        "detector_verdict": verdict,
        "plain_english": plain,
        "reminders": [
            "Not for doxing or identity profiling.",
            "Private email/logs require consent.",
            "Never treat scores as sole evidence.",
            "Operational bar is ops_score ≥ 0.65 or high evasion.",
        ],
    }


def cmd_map() -> dict[str, Any]:
    return {
        "ok": True,
        "kind": "ecosystem_map",
        "signature": SIG,
        "version": VERSION,
        "title": "LYGO lattice — what to use when",
        "profile": "https://clawhub.ai/deepseekoracle",
        "star_chart": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "routes": ECOSYSTEM_MAP,
        "layers_plain": {
            "ethical_core": "Guardian / mint-verifier / lattice pulse — trust and health",
            "champions": "Specialized advisors (truth, architecture, time…) — advice only",
            "memory": "Lore + living memory library — grounding and continuity",
            "orchestration": "LPIS + agent lattice — prompts and aligned agents",
            "infrastructure": "Protocol stack operator — full engineer audits",
        },
        "gap_note": (
            "This Kickstart wizard is the UX bridge: plain English routing. "
            "Next: deception radar dashboard, mint walkthrough skill, unified CLI bridge."
        ),
    }


def cmd_lattice() -> dict[str, Any]:
    checks = []
    ok_n = 0
    for ep in LATTICE_ENDPOINTS:
        r = fetch_get(ep["url"])
        row = {"id": ep["id"], "label": ep["label"], "url": ep["url"], **r}
        checks.append(row)
        if r.get("ok"):
            ok_n += 1
    score = int(round(100 * ok_n / max(len(LATTICE_ENDPOINTS), 1)))
    if score >= 75:
        plain = (
            f"**Lattice looks healthy** ({ok_n}/{len(LATTICE_ENDPOINTS)} surfaces responded). "
            "Public mirrors are reachable. Local stack authority still wins if you have one."
        )
        level = "healthy"
    elif score >= 40:
        plain = (
            f"**Partial** public surface ({ok_n}/{len(LATTICE_ENDPOINTS)}). "
            "Some hubs may be slow or offline. Retry later; don't panic."
        )
        level = "partial"
    else:
        plain = (
            f"**Public surfaces mostly unreachable** ({ok_n}/{len(LATTICE_ENDPOINTS)}). "
            "Check your network. Your local clone (if any) is still the authority."
        )
        level = "down"
    return {
        "ok": ok_n > 0,
        "kind": "lattice_health",
        "signature": SIG,
        "version": VERSION,
        "score": score,
        "level": level,
        "plain_english": plain,
        "checks": checks,
        "next": [
            "Open Star Chart: https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
            "For deeper join flow: install lygo-public-lattice-gate",
        ],
    }


def cmd_analyze(text: str = "", text_file: str = "") -> dict[str, Any]:
    body = text
    if text_file:
        p = Path(text_file)
        if not p.is_file():
            return {"ok": False, "error": "file_not_found", "path": text_file}
        body = p.read_text(encoding="utf-8", errors="replace")
    if not (body or "").strip():
        return {
            "ok": False,
            "error": "need_text",
            "plain_english": "Paste text with --text \"...\" or --text-file path/to/snippet.txt",
            "example": 'python scripts/kickstart_cli.py analyze --text "It\'s on you to prove it."',
        }

    det_path = find_ops_detector()
    if not det_path:
        return {
            "ok": False,
            "error": "ops_detector_missing",
            "plain_english": (
                "Ops Detector is not installed next to this skill. "
                "Install: npx clawhub@latest install deepseekoracle/lygo-ops-detector "
                "or set LYGO_STACK_ROOT to your lygo-protocol-stack clone."
            ),
            "install": "npx clawhub@latest install deepseekoracle/lygo-ops-detector",
        }

    # In-process import (no subprocess)
    scripts_dir = str(det_path.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import lygo_ops_detector as det  # type: ignore  # noqa: E402

    report = det.analyze(text=body, notes="kickstart-wizard")
    plain = plain_ops_result(report)
    return {
        "ok": True,
        "kind": "analyze",
        "signature": SIG,
        "version": VERSION,
        "detector": str(det_path),
        "result": plain,
        "raw_scores": {
            "ops_score": plain["ops_score"],
            "evasion_index": plain["evasion_index"],
            "association_index": float(getattr(report, "association_index", 0) or 0),
        },
        "how_to_go_deeper": "python path/to/lygo-ops-detector/scripts/lygo_ops_detector.py --text \"...\" --json",
    }


def cmd_mint(pack: str = "", dry_hash: bool = True) -> dict[str, Any]:
    """Plain-English mint walkthrough + optional local SHA-256 of a pack file."""
    steps = [
        {
            "step": 1,
            "title": "Create a pack (no secrets)",
            "plain": "Write or export a Champion/alignment prompt pack as a .md or .txt file. Never put API keys or passwords in the pack.",
        },
        {
            "step": 2,
            "title": "Mint (canonicalize + hash)",
            "plain": "Run lygo-mint-verifier so the pack gets a deterministic SHA-256 and ledger receipt.",
            "command": "python scripts/mint_pack_local.py --pack your_pack.md --version 2026-08-06.v1",
            "skill": "lygo-mint-verifier",
        },
        {
            "step": 3,
            "title": "Make an Anchor Snippet",
            "plain": "Generate a short portable snippet you can paste on Moltbook/X/Discord as a public receipt.",
            "command": "python scripts/make_anchor_snippet.py --hash <64-hex> --title \"My pack\"",
        },
        {
            "step": 4,
            "title": "Optional backfill",
            "plain": "After you post, record the post URL/id so the ledger points at the public anchor.",
            "command": "python scripts/backfill_anchors.py --hash <64-hex> --channel moltbook --id <url-or-id>",
        },
        {
            "step": 5,
            "title": "Human only",
            "plain": "You (or a steward) choose whether to publish the snippet. Kickstart never auto-posts.",
        },
    ]

    out: dict[str, Any] = {
        "ok": True,
        "kind": "mint_guide",
        "signature": SIG,
        "version": VERSION,
        "title": "Mint → Verify → Anchor (plain English)",
        "install_mint": "npx clawhub@latest install deepseekoracle/lygo-mint-verifier",
        "steps": steps,
        "plain_english": (
            "Minting makes a pack **checkable**: same file → same hash. "
            "You can prove what was hashed without uploading secrets to a server."
        ),
    }

    if pack:
        p = Path(pack)
        if not p.is_file():
            out["ok"] = False
            out["error"] = "pack_not_found"
            out["path"] = pack
            return out
        raw = p.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        out["local_receipt"] = {
            "path": str(p.resolve()),
            "bytes": len(raw),
            "sha256": digest,
            "note": (
                "Simple content hash (kickstart). Full lygo-mint-verifier also canonicalizes "
                "and writes ledgers — install that skill for production receipts."
            ),
            "anchor_snippet_draft": (
                f"LYGO-MINT draft receipt\n"
                f"title: {p.name}\n"
                f"sha256: {digest}\n"
                f"bytes: {len(raw)}\n"
                f"tool: {SIG}\n"
                f"created: {utc_now()}\n"
            ),
        }
        out["plain_english"] += f" Local draft hash for {p.name}: `{digest[:16]}…`."
    return out


def cmd_next() -> dict[str, Any]:
    return {
        "ok": True,
        "kind": "roadmap",
        "signature": SIG,
        "version": VERSION,
        "title": "Build priorities after Kickstart",
        "items": [
            {
                "when": "now",
                "slug": "lygo-kickstart-wizard",
                "status": "this skill",
                "goal": "UX bridge: route users to mint / ops / lattice in plain English",
            },
            {
                "when": "1–2 weeks",
                "slug": "lygo-deception-radar",
                "status": "planned",
                "goal": "Public dashboard of anonymized Ops Detector signals on public samples only",
            },
            {
                "when": "1–2 weeks",
                "slug": "lygo-mint-walkthrough",
                "status": "planned (mint intent here is the seed)",
                "goal": "Interactive end-to-end mint-verify-anchor tutorial skill",
            },
            {
                "when": "1–2 months",
                "slug": "lygo-cli-bridge",
                "status": "planned",
                "goal": "Single CLI: lygo verify | mint | health | analyze",
            },
        ],
        "plain_english": (
            "Kickstart closes the onboarding gap. Radar proves value publicly. "
            "Walkthrough teaches mint end-to-end. CLI unifies power users."
        ),
    }


def interactive_menu() -> str:
    print(
        """
╔══════════════════════════════════════════════════════╗
║           LYGO Kickstart Wizard v1.0.0               ║
║     Plain English · Local-first · No auto-publish    ║
╚══════════════════════════════════════════════════════╝

What do you want to do?

  1) Map the ecosystem (what skill for which job)
  2) Check public lattice health
  3) Analyze text for ops/evasion signals
  4) Learn mint → verify → anchor (optional hash a file)
  5) See next build priorities (radar / walkthrough / CLI)

"""
    )
    choice = (input("Enter 1-5 [1]: ").strip() or "1")
    return {
        "1": "map",
        "2": "lattice",
        "3": "analyze",
        "4": "mint",
        "5": "next",
    }.get(choice, "map")


def maybe_write(obj: dict, path: str | None, consent: bool) -> dict:
    if not path:
        return {"written": False}
    if not consent:
        return {"written": False, "error": "need --i-consent with --write"}
    p = Path(path)
    if ".." in p.parts:
        return {"written": False, "error": "path_escape"}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return {"written": True, "path": str(p.resolve())}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LYGO Kickstart Wizard — plain-English lattice onboarding")
    ap.add_argument(
        "intent",
        nargs="?",
        default="start",
        choices=["start", "map", "analyze", "mint", "lattice", "next"],
        help="What to do (default: interactive start)",
    )
    ap.add_argument("--text", default="", help="Text for analyze intent")
    ap.add_argument("--text-file", default="", help="File for analyze intent")
    ap.add_argument("--pack", default="", help="Optional pack file for mint draft hash")
    ap.add_argument("--json", action="store_true", help="JSON only (default for non-start)")
    ap.add_argument("--write", default="", help="Opt-in write report path")
    ap.add_argument("--i-consent", action="store_true", help="Consent for --write")
    args = ap.parse_args(argv)

    intent = args.intent
    if intent == "start":
        if sys.stdin.isatty():
            intent = interactive_menu()
            if intent == "analyze" and not args.text and not args.text_file:
                args.text = input("Paste a short text sample to analyze:\n> ").strip()
            if intent == "mint" and not args.pack:
                pack = input("Optional path to a pack file to draft-hash (Enter to skip):\n> ").strip()
                args.pack = pack
        else:
            intent = "map"

    if intent == "map":
        out = cmd_map()
    elif intent == "lattice":
        out = cmd_lattice()
    elif intent == "analyze":
        out = cmd_analyze(text=args.text, text_file=args.text_file)
    elif intent == "mint":
        out = cmd_mint(pack=args.pack)
    else:
        out = cmd_next()

    out["intent"] = intent
    out["created_at"] = utc_now()
    if args.write:
        out["write"] = maybe_write(out, args.write, args.i_consent)

    # Human-friendly stdout unless --json forced; always JSON if not tty
    if args.json or not sys.stdout.isatty():
        print(json.dumps(out, indent=2))
    else:
        print(json.dumps(out, indent=2))
        if out.get("plain_english"):
            print("\n—— Plain English ——")
            print(out["plain_english"])
        if out.get("result", {}).get("plain_english"):
            print("\n—— Plain English ——")
            print(out["result"]["plain_english"])

    return 0 if out.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
