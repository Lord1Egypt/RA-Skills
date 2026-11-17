#!/usr/bin/env python3
"""
LYGO Public Lattice Gate — on-ramp for foreign agents (ClawHub).

Subcommands:
  verify   HTTPS GET public lattice surfaces (default: zero disk writes)
  align    Readiness score from verify + optional local stack markers
  propose  Dry-run Star Chart presence proposal (JSON stdout; optional write)
  restore  Short restore card (links + digests only)

Security:
  - HTTPS GET only for network
  - No subprocess, no os.system, no shell
  - No auto git / HF / ClawHub / social publish
  - Live chart write NEVER performed here — pair lygo-haven-star-chart + human --i-consent

Signature: Delta9Phi963-PUBLIC-LATTICE-GATE-v1.0.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SIG = "Delta9Phi963-PUBLIC-LATTICE-GATE-v1.0.0"
UA = "LYGO-PublicLatticeGate/1.0.0 (+https://eternalhaven.ca; +https://clawhub.ai/deepseekoracle)"
VERSION = "1.0.0"

# Public surfaces — dual ledger + hubs + skill registry
ENDPOINTS: list[dict[str, str]] = [
    {
        "id": "immutable_anchors",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/network_builder/IMMUTABLE_ANCHORS.json",
        "role": "link_ledger",
        "verify": "http_required",
    },
    {
        "id": "immutable_anchors_raw",
        "url": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/network_builder/IMMUTABLE_ANCHORS.json",
        "role": "link_ledger_mirror",
        "verify": "http_soft",
    },
    {
        "id": "haven_star_feed",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json",
        "role": "star_ledger",
        "verify": "http_required",
    },
    {
        "id": "haven_star_chart",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "role": "world_map",
        "verify": "http_required",
    },
    {
        "id": "stack_pages",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/",
        "role": "stack_mirror",
        "verify": "http_required",
    },
    {
        "id": "lygo_claw_public_usb",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/LYGO_CLAW_USB_PUBLIC.md",
        "role": "usb_public_kit",
        "verify": "http_soft",
    },
    {
        "id": "chatagent_hub",
        "url": "https://chatagent.ca/app.html",
        "role": "summon_hub",
        "verify": "http_soft",
    },
    {
        "id": "asiancoastline_listen",
        "url": "https://asiancoastline.com/listen.html",
        "role": "music_primary",
        "verify": "http_soft",
    },
    {
        "id": "excavationpro_listen",
        "url": "https://deepseekoracle.github.io/Excavationpro/excavationpro-listen.html",
        "role": "music_backup",
        "verify": "http_soft",
    },
    {
        "id": "eternalhaven",
        "url": "https://eternalhaven.ca/",
        "role": "public_hub",
        "verify": "http_soft",
    },
    {
        "id": "bpmfinder",
        "url": "https://bpmfinder.ca/",
        "role": "tools_domain",
        "verify": "http_soft",
    },
    {
        "id": "clawhub_publisher",
        "url": "https://clawhub.ai/deepseekoracle",
        "role": "skill_registry",
        "verify": "http_soft",
    },
]

STACK_MARKERS = [
    "docs/network_builder/IMMUTABLE_ANCHORS.json",
    "docs/haven_star_chart/haven_star_chart_feed.json",
    "docs/public_verify_manifest.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def https_only(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False


def fetch(url: str, timeout: float = 20.0) -> dict[str, Any]:
    if not https_only(url):
        return {"ok": False, "status": 0, "error": "https_only", "bytes": 0, "sha256": None}
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            # Cap digest work on huge HTML (still record size)
            sample = body[: 2_000_000]
            return {
                "ok": 200 <= resp.status < 400,
                "status": resp.status,
                "error": None,
                "bytes": len(body),
                "sha256": hashlib.sha256(sample).hexdigest() if sample else None,
                "body_sample": sample if url.endswith(".json") and len(body) < 5_000_000 else None,
            }
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e), "bytes": 0, "sha256": None}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e), "bytes": 0, "sha256": None}


def stack_root() -> Path | None:
    env = (os.environ.get("LYGO_STACK_ROOT") or "").strip()
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    candidates.extend(
        [
            Path(r"D:\lygo-protocol-stack"),
            Path(r"I:\E Drive\lygo-protocol-stack"),
        ]
    )
    # walk up from skill
    here = Path(__file__).resolve()
    for p in here.parents:
        candidates.append(p)
    for c in candidates:
        try:
            if (c / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json").is_file():
                return c.resolve()
        except OSError:
            continue
    return None


def parse_json_body(raw: bytes | None) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except Exception:
        return None


def summarize_feed(data: Any) -> dict[str, Any] | None:
    if not isinstance(data, dict):
        return None
    entries = data.get("entries") or []
    counts: dict[str, int] = {}
    for e in entries:
        if isinstance(e, dict):
            st = str(e.get("status") or "unknown")
            counts[st] = counts.get(st, 0) + 1
    return {
        "entry_count": data.get("entry_count") or len(entries),
        "chain_valid": data.get("chain_valid"),
        "chain_root": data.get("chain_root"),
        "updated_utc": data.get("updated_utc"),
        "signature": data.get("signature"),
        "status_counts": counts,
    }


def summarize_anchors(data: Any) -> dict[str, Any] | None:
    if not isinstance(data, dict):
        return None
    groups = data.get("immutable_anchors") or {}
    cats = list(groups.keys()) if isinstance(groups, dict) else []
    return {
        "signature": data.get("signature"),
        "version": data.get("version"),
        "updated_utc": data.get("updated_utc"),
        "categories": cats,
        "category_count": len(cats),
    }


def run_verify(timeout: float = 20.0) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    required_fail = 0
    soft_fail = 0
    feed_summary = None
    anchors_summary = None

    for ep in ENDPOINTS:
        url = ep["url"]
        r = fetch(url, timeout=timeout)
        item = {
            "id": ep["id"],
            "role": ep["role"],
            "verify": ep["verify"],
            "url": url,
            "ok": r["ok"],
            "status": r["status"],
            "bytes": r["bytes"],
            "sha256": r["sha256"],
            "error": r["error"],
        }
        if r.get("body_sample") and ep["id"] in ("haven_star_feed", "immutable_anchors", "immutable_anchors_raw"):
            data = parse_json_body(r["body_sample"])
            if ep["id"] == "haven_star_feed":
                feed_summary = summarize_feed(data)
                item["feed"] = feed_summary
            elif ep["id"].startswith("immutable_anchors") and anchors_summary is None:
                anchors_summary = summarize_anchors(data)
                item["anchors"] = anchors_summary

        if not r["ok"]:
            if ep["verify"] == "http_required":
                required_fail += 1
            else:
                soft_fail += 1
        results.append(item)

    ok = required_fail == 0
    return {
        "signature": SIG,
        "version": VERSION,
        "command": "verify",
        "ok": ok,
        "updated_utc": utc_now(),
        "required_fail": required_fail,
        "soft_fail": soft_fail,
        "endpoints": results,
        "dual_ledgers": {
            "link": anchors_summary,
            "star_feed": feed_summary,
        },
        "policy": {
            "network": "https_get_only",
            "writes": "none_by_default",
            "publish": "never",
        },
    }


def local_stack_probe(root: Path | None) -> dict[str, Any]:
    if not root:
        return {"present": False, "root": None, "markers": {}}
    markers = {}
    for rel in STACK_MARKERS:
        p = root / rel
        markers[rel] = {
            "exists": p.is_file(),
            "bytes": p.stat().st_size if p.is_file() else 0,
        }
    return {
        "present": all(m["exists"] for m in markers.values()),
        "root": str(root),
        "markers": markers,
    }


def run_align(verify_report: dict[str, Any] | None = None) -> dict[str, Any]:
    v = verify_report or run_verify()
    root = stack_root()
    local = local_stack_probe(root)

    score = 0
    max_score = 100
    notes: list[str] = []

    # Public required endpoints (50 pts)
    total_req = sum(1 for e in ENDPOINTS if e["verify"] == "http_required")
    ok_req = total_req - int(v.get("required_fail") or 0)
    if total_req:
        score += int(50 * ok_req / total_req)
    if v.get("ok"):
        notes.append("public_required_ok")
    else:
        notes.append("public_required_fail")

    # Dual ledgers (25 pts)
    dual = v.get("dual_ledgers") or {}
    link = dual.get("link")
    feed = dual.get("star_feed")
    if link and link.get("category_count", 0) > 0:
        score += 10
        notes.append("link_ledger_ok")
    if feed and feed.get("chain_valid") is True:
        score += 15
        notes.append("star_chain_valid")
    elif feed and feed.get("entry_count"):
        score += 5
        notes.append("star_feed_present_chain_unknown")

    # Soft hubs (15 pts)
    soft_total = sum(1 for e in ENDPOINTS if e["verify"] == "http_soft")
    soft_ok = soft_total - int(v.get("soft_fail") or 0)
    if soft_total:
        score += int(15 * soft_ok / soft_total)

    # Local stack optional (10 pts)
    if local.get("present"):
        score += 10
        notes.append("local_stack_present")
    else:
        notes.append("local_stack_optional_missing")

    score = max(0, min(max_score, score))
    ready = score >= 70 and bool(v.get("ok"))

    return {
        "signature": SIG,
        "version": VERSION,
        "command": "align",
        "updated_utc": utc_now(),
        "score": score,
        "max_score": max_score,
        "ready_for_live_ops": ready,
        "ready_for_public_presence": bool(v.get("ok")),
        "notes": notes,
        "verify_ok": v.get("ok"),
        "local_stack": local,
        "dual_ledgers": dual,
        "next_steps": [
            "If ready_for_public_presence: run propose (dry-run) to draft a Star Chart card",
            "Live chart write requires lygo-haven-star-chart + human --i-consent (not this skill)",
            "USB offline agent: docs/lygo-claw-usb / LYGO_CLAW_USB_PUBLIC.md",
        ],
        "policy": "no auto publish; local stack optional",
    }


def sanitize_agent_id(raw: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_\-\.]", "-", (raw or "").strip())[:64]
    return s or "lygo-agent"


def run_propose(
    agent_id: str,
    display_name: str = "",
    skill_slug: str = "lygo-public-lattice-gate",
    note: str = "",
    i_consent: bool = False,
    write_path: Path | None = None,
) -> dict[str, Any]:
    """Dry-run proposal only. Even with --i-consent this skill does NOT live-submit."""
    aid = sanitize_agent_id(agent_id)
    name = (display_name or aid).strip()[:120]
    proposal = {
        "signature": "Delta9Phi963-PUBLIC-LATTICE-GATE-PROPOSAL-v1",
        "skill": "lygo-public-lattice-gate",
        "skill_version": VERSION,
        "mode": "dry_run" if not i_consent else "consent_acknowledged_still_dry_here",
        "created_utc": utc_now(),
        "agent_id": aid,
        "display_name": name,
        "skill_slug": skill_slug,
        "note": (note or "")[:500],
        "event_type": "agent_presence_propose",
        "status": "PROPOSAL",
        "public_anchors": {
            "star_chart": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
            "star_feed": "https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json",
            "link_ledger": "https://deepseekoracle.github.io/lygo-protocol-stack/network_builder/IMMUTABLE_ANCHORS.json",
            "clawhub": "https://clawhub.ai/deepseekoracle",
        },
        "live_write": {
            "performed": False,
            "reason": "This skill never writes the live Star Chart. Use lygo-haven-star-chart gate + submit with human --i-consent.",
            "pair_skill": "lygo-haven-star-chart",
        },
        "consent": {
            "i_consent_flag": bool(i_consent),
            "human_must_still_approve_live": True,
        },
    }

    out: dict[str, Any] = {
        "signature": SIG,
        "version": VERSION,
        "command": "propose",
        "ok": True,
        "proposal": proposal,
    }

    if write_path is not None:
        # Only write under cwd or explicit path — never remote publish
        write_path = Path(write_path)
        if ".." in write_path.parts:
            out["ok"] = False
            out["error"] = "path_escape"
            return out
        write_path.parent.mkdir(parents=True, exist_ok=True)
        write_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        out["written"] = str(write_path.resolve())

    if i_consent:
        out["warning"] = (
            "--i-consent acknowledged for readiness, but live chart submit is intentionally "
            "NOT implemented in this skill. Pair lygo-haven-star-chart."
        )
    return out


def run_restore(verify_report: dict[str, Any] | None = None, align_report: dict[str, Any] | None = None) -> dict[str, Any]:
    v = verify_report or run_verify()
    a = align_report or run_align(v)
    dual = v.get("dual_ledgers") or {}
    feed = dual.get("star_feed") or {}
    link = dual.get("link") or {}

    lines = [
        "LYGO PUBLIC LATTICE RESTORE CARD",
        f"gate: {SIG}",
        f"utc: {utc_now()}",
        f"score: {a.get('score')}/{a.get('max_score')} ready_public={a.get('ready_for_public_presence')}",
        "",
        "PUBLIC SURFACES",
        "  stack:     https://deepseekoracle.github.io/lygo-protocol-stack/",
        "  star chart:https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "  star feed: https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json",
        "  anchors:   https://deepseekoracle.github.io/lygo-protocol-stack/network_builder/IMMUTABLE_ANCHORS.json",
        "  clawhub:   https://clawhub.ai/deepseekoracle",
        "  usb kit:   https://deepseekoracle.github.io/lygo-protocol-stack/LYGO_CLAW_USB_PUBLIC.md",
        "  music:     https://asiancoastline.com/listen.html",
        "  summon:    https://chatagent.ca/app.html",
        "",
        "DIGESTS (from live GET)",
    ]
    if feed:
        lines.append(f"  star_entries: {feed.get('entry_count')} chain_valid={feed.get('chain_valid')}")
        if feed.get("chain_root"):
            lines.append(f"  chain_root: {str(feed.get('chain_root'))[:20]}...")
    if link:
        lines.append(f"  anchor_categories: {link.get('category_count')} sig={link.get('signature')}")
    for ep in v.get("endpoints") or []:
        if ep.get("id") in ("immutable_anchors", "haven_star_feed", "stack_pages"):
            lines.append(f"  {ep['id']}: status={ep.get('status')} sha={str(ep.get('sha256') or '')[:12]}...")

    lines.extend(
        [
            "",
            "AGENT NEXT",
            "  1) python scripts/gate_cli.py verify",
            "  2) python scripts/gate_cli.py align",
            "  3) python scripts/gate_cli.py propose --agent-id YOUR-ID",
            "  4) Live chart: install lygo-haven-star-chart + human --i-consent",
            "  5) Offline USB: LYGO CLAW PUBLIC USB kit (no secrets)",
            "",
            "NEVER auto-publish. Local authority. Public is mirror.",
            "Δ9Φ963",
        ]
    )
    card = "\n".join(lines)
    return {
        "signature": SIG,
        "version": VERSION,
        "command": "restore",
        "updated_utc": utc_now(),
        "card": card,
        "score": a.get("score"),
        "ready_for_public_presence": a.get("ready_for_public_presence"),
    }


def maybe_write_report(obj: dict[str, Any], path: Path | None) -> None:
    if not path:
        return
    path = Path(path)
    if ".." in path.parts:
        raise ValueError("path_escape")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lygo-public-lattice-gate",
        description="Public lattice join + verify gate (no auto-publish)",
    )
    ap.add_argument("--json", action="store_true", help="JSON only on stdout")
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument(
        "--write-report",
        default="",
        help="Optional local path to write report JSON (opt-in)",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("verify", help="HTTPS GET public lattice surfaces")
    sub.add_parser("align", help="Readiness score (verify + optional local stack)")
    p_prop = sub.add_parser("propose", help="Dry-run presence proposal (no live chart write)")
    p_prop.add_argument("--agent-id", required=True)
    p_prop.add_argument("--display-name", default="")
    p_prop.add_argument("--skill-slug", default="lygo-public-lattice-gate")
    p_prop.add_argument("--note", default="")
    p_prop.add_argument(
        "--i-consent",
        action="store_true",
        help="Acknowledge human consent intent (still dry-run in this skill)",
    )
    p_prop.add_argument(
        "--write",
        default="",
        help="Write proposal JSON to local path",
    )
    sub.add_parser("restore", help="Print short restore card")

    args = ap.parse_args(argv)
    report_path = Path(args.write_report) if args.write_report else None

    if args.cmd == "verify":
        out = run_verify(timeout=args.timeout)
    elif args.cmd == "align":
        out = run_align()
    elif args.cmd == "propose":
        out = run_propose(
            agent_id=args.agent_id,
            display_name=args.display_name,
            skill_slug=args.skill_slug,
            note=args.note,
            i_consent=bool(args.i_consent),
            write_path=Path(args.write) if args.write else None,
        )
    elif args.cmd == "restore":
        out = run_restore()
    else:
        ap.error("unknown command")
        return 2

    if report_path:
        try:
            maybe_write_report(out, report_path)
            out["report_written"] = str(report_path.resolve())
        except Exception as e:
            out["report_error"] = str(e)

    if args.cmd == "restore" and not args.json:
        print(out.get("card") or "")
        if report_path:
            print(f"\n# report -> {report_path}", file=sys.stderr)
        return 0 if out.get("ready_for_public_presence") or out.get("score", 0) >= 50 else 1

    print(json.dumps(out, indent=2, ensure_ascii=False))
    if args.cmd == "verify":
        return 0 if out.get("ok") else 1
    if args.cmd == "align":
        return 0 if out.get("ready_for_public_presence") else 1
    if args.cmd == "propose":
        return 0 if out.get("ok") else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
