#!/usr/bin/env python3
"""
LYGO CLI Bridge — unified entrypoint for common lattice intents.

Commands:
  lygo health              public lattice health (HTTPS GET allowlist)
  lygo map                 ecosystem map
  lygo analyze --text ...  ops/evasion signals (needs lygo-ops-detector nearby)
  lygo mint --pack ...     mint tutorial / local ledger (mint-walkthrough or draft hash)
  lygo radar               rebuild public deception radar feed (needs ops-detector)
  lygo next                roadmap status
  lygo version             version + signature

In-process imports only. No subprocess. No auto-publish.
Writes only with --i-consent where applicable.

Signature: Delta9Phi963-CLI-BRIDGE-v1.0.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SIG = "Delta9Phi963-CLI-BRIDGE-v1.0.0"
VERSION = "1.0.0"
UA = "LYGO-CLI-Bridge/1.0.0 (+https://clawhub.ai/deepseekoracle)"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SKILLS_ROOT = SKILL.parent

LATTICE_ENDPOINTS = [
    {
        "id": "immutable_anchors",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/network_builder/IMMUTABLE_ANCHORS.json",
        "label": "Link ledger",
    },
    {
        "id": "star_feed",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json",
        "label": "Star Chart feed",
    },
    {
        "id": "star_chart",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "label": "Haven Star Chart",
    },
    {
        "id": "clawhub",
        "url": "https://clawhub.ai/deepseekoracle",
        "label": "ClawHub publisher",
    },
    {
        "id": "deception_radar",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/deception-radar/",
        "label": "Deception Radar (public proof)",
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


def fetch_get(url: str, timeout: float = 12.0) -> dict[str, Any]:
    if not https_only(url):
        return {"ok": False, "error": "https_only"}
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(400_000)
            return {
                "ok": 200 <= resp.status < 400,
                "status": resp.status,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest() if body else None,
            }
    except Exception as e:
        return {"ok": False, "error": type(e).__name__, "detail": str(e)[:120]}


def _skill_candidates(slug: str, rel: str) -> list[Path]:
    stack = os.environ.get("LYGO_STACK_ROOT", "").strip()
    out = [
        SKILLS_ROOT / slug / rel,
        Path(r"I:\E Drive\.grok\skills") / slug / rel,
        Path.home() / ".grok" / "skills" / slug / rel,
    ]
    if stack:
        out.append(Path(stack) / "clawhub" / "mirrors" / slug / rel)
        out.append(Path(stack) / "docs" / "skills" / slug / rel)
    return out


def find_skill_file(slug: str, rel: str) -> Path | None:
    for p in _skill_candidates(slug, rel):
        if p.is_file():
            return p
    return None


def import_from(path: Path, module_name: str) -> Any:
    scripts = str(path.parent)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    # Avoid stale module if switching skills
    if module_name in sys.modules:
        del sys.modules[module_name]
    return __import__(module_name)


def cmd_version() -> dict[str, Any]:
    return {
        "ok": True,
        "kind": "version",
        "signature": SIG,
        "version": VERSION,
        "skill": "lygo-cli-bridge",
        "commands": ["health", "map", "analyze", "mint", "radar", "next", "version"],
        "plain_english": "Unified LYGO CLI bridge. Local-first; companions optional.",
    }


def cmd_map() -> dict[str, Any]:
    routes = [
        {
            "need": "Public lattice health",
            "cmd": "lygo health",
            "skill": "lygo-cli-bridge / lygo-kickstart-wizard / lygo-public-lattice-gate",
        },
        {
            "need": "Ops / evasion discourse signals",
            "cmd": 'lygo analyze --text "..."',
            "skill": "lygo-ops-detector",
        },
        {
            "need": "Mint → verify → anchor tutorial",
            "cmd": "lygo mint --pack pack.md",
            "skill": "lygo-mint-walkthrough (+ lygo-mint-verifier for production)",
        },
        {
            "need": "Public proof dashboard",
            "cmd": "lygo radar",
            "skill": "lygo-deception-radar",
        },
        {
            "need": "Full skill constellation",
            "cmd": "open Star Chart",
            "skill": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        },
        {
            "need": "Onboarding wizard",
            "cmd": "python kickstart_cli.py start",
            "skill": "lygo-kickstart-wizard",
        },
    ]
    return {
        "ok": True,
        "kind": "map",
        "signature": SIG,
        "version": VERSION,
        "title": "LYGO CLI — what to run",
        "routes": routes,
        "install": "npx clawhub@latest install deepseekoracle/lygo-cli-bridge",
        "star_chart": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
    }


def cmd_health() -> dict[str, Any]:
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
        level, plain = "healthy", f"Lattice looks healthy ({ok_n}/{len(LATTICE_ENDPOINTS)} surfaces)."
    elif score >= 40:
        level, plain = "partial", f"Partial public surface ({ok_n}/{len(LATTICE_ENDPOINTS)})."
    else:
        level, plain = "down", f"Public surfaces mostly unreachable ({ok_n}/{len(LATTICE_ENDPOINTS)})."
    return {
        "ok": ok_n > 0,
        "kind": "health",
        "signature": SIG,
        "version": VERSION,
        "score": score,
        "level": level,
        "plain_english": plain,
        "checks": checks,
        "generated_utc": utc_now(),
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
            "plain_english": 'Pass --text "..." or --text-file path',
            "example": 'python scripts/lygo_cli.py analyze --text "It\'s on you to prove it."',
        }

    det_path = find_skill_file("lygo-ops-detector", "scripts/lygo_ops_detector.py")
    if not det_path:
        return {
            "ok": False,
            "error": "ops_detector_missing",
            "plain_english": "Install lygo-ops-detector next to this skill or set LYGO_STACK_ROOT.",
            "install": "npx clawhub@latest install deepseekoracle/lygo-ops-detector",
        }

    det = import_from(det_path, "lygo_ops_detector")
    report = det.analyze(text=body, notes="cli-bridge")
    ops = float(getattr(report, "ops_score", 0) or 0)
    ev = float(getattr(report, "evasion_index", 0) or 0)
    if ev > 0.7:
        level = "strong_evasion_signals"
        plain = "Strong evasion-style discourse patterns. Signal only — not a person verdict."
    elif ops >= 0.65:
        level = "elevated_cluster"
        plain = "Operational bar (≥ 0.65) reached. Worth careful human review."
    elif ops >= 0.05:
        level = "weak_only"
        plain = "Weak/calibration-level signals only."
    else:
        level = "clear"
        plain = "No clear operational-deception pattern at published thresholds."

    return {
        "ok": True,
        "kind": "analyze",
        "signature": SIG,
        "version": VERSION,
        "detector": str(det_path),
        "result": {
            "level": level,
            "ops_score": ops,
            "evasion_index": ev,
            "verdict": str(getattr(report, "overall_verdict", "") or ""),
            "plain_english": plain,
        },
        "reminders": [
            "Not for doxing",
            "Private mail/logs need consent",
            "Scores are not sole evidence",
        ],
    }


def cmd_mint(pack: str = "", version: str = "v1", i_consent: bool = False) -> dict[str, Any]:
    """Prefer mint-walkthrough if installed; else draft SHA-256 of pack."""
    mw = find_skill_file("lygo-mint-walkthrough", "scripts/mint_walkthrough.py")
    if mw and pack:
        m = import_from(mw, "mint_walkthrough")
        out = m.step_mint(pack, version, "", i_consent)
        out["kind"] = "mint"
        out["via"] = "lygo-mint-walkthrough"
        out["signature"] = SIG
        out["version"] = VERSION
        return out

    if not pack:
        return {
            "ok": True,
            "kind": "mint_guide",
            "signature": SIG,
            "version": VERSION,
            "plain_english": (
                "Mint makes a pack checkable (same content → same hash). "
                "Install lygo-mint-walkthrough for the full tutorial, or pass --pack file.md."
            ),
            "steps": [
                "Create pack (no secrets)",
                "lygo mint --pack file.md --i-consent",
                "Copy anchor snippet (human posts only)",
                "Optional backfill after public post",
            ],
            "install_walkthrough": "npx clawhub@latest install deepseekoracle/lygo-mint-walkthrough",
            "install_production": "npx clawhub@latest install deepseekoracle/lygo-mint-verifier",
        }

    p = Path(pack)
    if not p.is_file():
        return {"ok": False, "error": "pack_not_found", "path": pack}
    raw = p.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    return {
        "ok": True,
        "kind": "mint_draft",
        "signature": SIG,
        "version": VERSION,
        "via": "cli-bridge-draft-hash",
        "path": str(p.resolve()),
        "bytes": len(raw),
        "sha256": digest,
        "plain_english": (
            f"Draft content hash for {p.name}: `{digest[:16]}…`. "
            "Install lygo-mint-walkthrough for canonicalize + ledger."
        ),
        "anchor_snippet_draft": (
            f"=== LYGO-MINT DRAFT ===\ntitle: {p.name}\nsha256: {digest}\n"
            f"tool: {SIG}\ncreated: {utc_now()}\n=== END ===\n"
        ),
    }


def cmd_radar(out_json: str = "", write_html: bool = False, i_consent: bool = False) -> dict[str, Any]:
    radar = find_skill_file("lygo-deception-radar", "scripts/build_radar_feed.py")
    if not radar:
        return {
            "ok": False,
            "error": "deception_radar_missing",
            "install": "npx clawhub@latest install deepseekoracle/lygo-deception-radar",
        }
    b = import_from(radar, "build_radar_feed")
    suite = None
    for cand in (
        SKILLS_ROOT / "lygo-ops-detector" / "tests" / "labeled_discourse_suite.json",
        Path(r"I:\E Drive\.grok\skills\lygo-ops-detector\tests\labeled_discourse_suite.json"),
        radar.parent.parent / "tests" / "public_samples.json",
    ):
        if cand.is_file():
            suite = cand
            break
    samples = b.load_suite(suite)
    if not samples:
        return {"ok": False, "error": "no_samples"}
    feed = b.build_feed(samples)
    if not feed.get("ok"):
        return feed

    result: dict[str, Any] = {
        "ok": True,
        "kind": "radar",
        "signature": SIG,
        "version": VERSION,
        "stats": feed.get("stats"),
        "ethics": feed.get("ethics"),
        "generated_utc": feed.get("generated_utc"),
        "via": "lygo-deception-radar",
    }

    if out_json:
        if not i_consent:
            result["written"] = False
            result["hint"] = "pass --i-consent with --out-json to write"
            return result
        outp = Path(out_json)
        if ".." in outp.parts:
            return {"ok": False, "error": "path_escape"}
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(feed, indent=2) + "\n", encoding="utf-8")
        result["written"] = True
        result["json"] = str(outp.resolve())
        if write_html:
            html_path = outp.parent / "index.html"
            b.write_html(feed, html_path)
            result["html"] = str(html_path.resolve())
    else:
        result["preview_signals"] = (feed.get("signals") or [])[:5]
        result["hint"] = "Add --out-json path --i-consent [--write-html] to deploy feed"
    return result


def cmd_next() -> dict[str, Any]:
    return {
        "ok": True,
        "kind": "roadmap",
        "signature": SIG,
        "version": VERSION,
        "items": [
            {"slug": "lygo-kickstart-wizard", "status": "shipped", "role": "UX bridge"},
            {"slug": "lygo-deception-radar", "status": "shipped", "role": "public proof"},
            {"slug": "lygo-mint-walkthrough", "status": "shipped", "role": "mint tutorial"},
            {"slug": "lygo-cli-bridge", "status": "this skill", "role": "unified CLI"},
        ],
        "plain_english": "Adoption stack complete: Kickstart → Radar → Walkthrough → CLI bridge.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lygo",
        description="LYGO CLI Bridge — health | map | analyze | mint | radar",
    )
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("version", help="Version + signature")
    sub.add_parser("map", help="Ecosystem map")
    sub.add_parser("health", help="Public lattice health (HTTPS GET)")
    sub.add_parser("next", help="Roadmap status")

    p = sub.add_parser("analyze", help="Ops/evasion analyze")
    p.add_argument("--text", default="")
    p.add_argument("--text-file", default="")

    p = sub.add_parser("mint", help="Mint guide or pack mint")
    p.add_argument("--pack", default="")
    p.add_argument("--version", default="v1", dest="pack_version")
    p.add_argument("--i-consent", action="store_true")

    p = sub.add_parser("radar", help="Build deception radar feed")
    p.add_argument("--out-json", default="")
    p.add_argument("--write-html", action="store_true")
    p.add_argument("--i-consent", action="store_true")

    args = ap.parse_args(argv)
    cmd = args.cmd or "version"

    if cmd == "version":
        out = cmd_version()
    elif cmd == "map":
        out = cmd_map()
    elif cmd == "health":
        out = cmd_health()
    elif cmd == "next":
        out = cmd_next()
    elif cmd == "analyze":
        out = cmd_analyze(text=args.text, text_file=args.text_file)
    elif cmd == "mint":
        out = cmd_mint(pack=args.pack, version=args.pack_version, i_consent=args.i_consent)
    elif cmd == "radar":
        out = cmd_radar(out_json=args.out_json, write_html=args.write_html, i_consent=args.i_consent)
    else:
        out = cmd_version()

    print(json.dumps(out, indent=2))
    if out.get("anchor_snippet"):
        print("\n" + out["anchor_snippet"])
    if out.get("anchor_snippet_draft"):
        print("\n" + out["anchor_snippet_draft"])
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
