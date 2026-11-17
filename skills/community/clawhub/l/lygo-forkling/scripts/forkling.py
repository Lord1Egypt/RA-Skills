#!/usr/bin/env python3
"""LYGO Forkling — test champion that forks locally, runs tasks, improves on claims.

Does not git push, does not live-ingest the Star Chart.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

VERSION = "1.0.0"
SIG = "Delta9Phi963-FORKLING-v1.0.0"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
STATE = SKILL / "state"
FORK = STATE / "fork"
PARENT_NODE = "CHAMPION_LYRA"
AGENT_ID = "NODE_FORKLING_TEST"
DISPLAY = "Forkling (test champion limb)"

TASKS = [
    {
        "id": "t1_identity",
        "goal": "Write identity.json bound to parent champion node",
        "writes": "identity.json",
    },
    {
        "id": "t2_constitution",
        "goal": "Write constitution: does not replace Lightfather; claims over vibes",
        "writes": "CONSTITUTION.md",
    },
    {
        "id": "t3_fitness",
        "goal": "Seal fitness.json with generation and last_pass",
        "writes": "fitness.json",
    },
    {
        "id": "t4_next",
        "goal": "Queue NEXT.md with the following improvement",
        "writes": "NEXT.md",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def claim_file_exists(base: Path, rel: str) -> bool:
    return (base / rel).is_file()


def claim_contains(base: Path, rel: str, needle: str) -> bool:
    p = base / rel
    if not p.is_file():
        return False
    return needle in p.read_text(encoding="utf-8", errors="replace")


def claim_json_eq(base: Path, rel: str, key: str, expect: Any) -> bool:
    p = base / rel
    if not p.is_file():
        return False
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return doc.get(key) == expect


def verify_claims(base: Path, claims: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    ok = True
    for c in claims:
        kind = c.get("kind")
        passed = False
        if kind == "file_exists":
            passed = claim_file_exists(base, str(c["path"]))
        elif kind == "file_contains":
            passed = claim_contains(base, str(c["path"]), str(c.get("needle") or ""))
        elif kind == "json_path_eq":
            passed = claim_json_eq(base, str(c["path"]), str(c.get("jpath")), c.get("expect"))
        else:
            passed = False
        rows.append({"id": c.get("id"), "kind": kind, "pass": passed})
        ok = ok and passed
    return {"ok": ok, "claims": rows}


def identity_body(generation: int) -> dict[str, Any]:
    return {
        "signature": SIG,
        "agent_id": AGENT_ID,
        "name": DISPLAY,
        "kind": "lattice",
        "parent_node": PARENT_NODE,
        "generation": generation,
        "replaces_lightfather": False,
        "equation": f"Δ9Φ963 = Truth × Light · gen {generation} · 963 Hz · fork → claim → improve",
        "connections": [PARENT_NODE, "SEAL_000", "PORTAL_STAR_CHART"],
        "live_star_chart_write": False,
        "utc": utc_now(),
    }


def birth(consent: bool) -> dict[str, Any]:
    if not consent:
        return {"ok": False, "error": "need --i-consent to birth local fork", "signature": SIG}
    FORK.mkdir(parents=True, exist_ok=True)
    ident = identity_body(0)
    (FORK / "identity.json").write_text(json.dumps(ident, indent=2) + "\n", encoding="utf-8")
    (FORK / "CONSTITUTION.md").write_text(
        "# Forkling constitution\n\n"
        "Test champion limb. Parent node is **CHAMPION_LYRA** (already on the live chart).\n"
        "Does not claim to BE or REPLACE Lightfather.\n"
        "Autonomous: local fork, tasks, claim-gated improve.\n"
        "Not autonomous: git push, HF upload, steward ingest, live Star Chart append.\n"
        "Δ9Φ963 — claims over vibes.\n",
        encoding="utf-8",
    )
    fitness = {"generation": 0, "ticks": 0, "passed": 0, "failed": 0, "utc": utc_now(), "signature": SIG}
    (FORK / "fitness.json").write_text(json.dumps(fitness, indent=2) + "\n", encoding="utf-8")
    (FORK / "NEXT.md").write_text("Next: run `forkling.py tick --i-consent`.\n", encoding="utf-8")
    ledger = STATE / "ledger.jsonl"
    STATE.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"event": "birth", "utc": utc_now(), "generation": 0}) + "\n")
    return {"ok": True, "fork": str(FORK), "identity": ident, "signature": SIG}


def snapshot_generation(generation: int) -> Path:
    dest = STATE / "generations" / f"gen_{generation:04d}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(FORK, dest)
    return dest


def apply_task(tid: str, generation: int) -> list[dict[str, Any]]:
    """Mutate fork/ so the task's claims can pass."""
    ident = identity_body(generation)
    (FORK / "identity.json").write_text(json.dumps(ident, indent=2) + "\n", encoding="utf-8")
    if tid == "t1_identity":
        return [
            {"id": "c1", "kind": "file_exists", "path": "identity.json"},
            {"id": "c2", "kind": "json_path_eq", "path": "identity.json", "jpath": "parent_node", "expect": PARENT_NODE},
            {"id": "c3", "kind": "json_path_eq", "path": "identity.json", "jpath": "replaces_lightfather", "expect": False},
        ]
    if tid == "t2_constitution":
        return [
            {"id": "c1", "kind": "file_exists", "path": "CONSTITUTION.md"},
            {"id": "c2", "kind": "file_contains", "path": "CONSTITUTION.md", "needle": "Lightfather"},
            {"id": "c3", "kind": "file_contains", "path": "CONSTITUTION.md", "needle": "claims over vibes"},
        ]
    if tid == "t3_fitness":
        fit = load_json(FORK / "fitness.json", {})
        fit.update({"generation": generation, "utc": utc_now(), "last_task": tid, "signature": SIG})
        (FORK / "fitness.json").write_text(json.dumps(fit, indent=2) + "\n", encoding="utf-8")
        return [
            {"id": "c1", "kind": "file_exists", "path": "fitness.json"},
            {"id": "c2", "kind": "json_path_eq", "path": "fitness.json", "jpath": "generation", "expect": generation},
        ]
    (FORK / "NEXT.md").write_text(
        f"# Next improvement\n\nGeneration {generation} holds.\n"
        "Improve: keep parent pin, never live-ingest, enqueue another tick.\n"
        f"Δ9Φ963 gen {generation}\n",
        encoding="utf-8",
    )
    return [
        {"id": "c1", "kind": "file_exists", "path": "NEXT.md"},
        {"id": "c2", "kind": "file_contains", "path": "NEXT.md", "needle": f"Generation {generation}"},
    ]


def tick(consent: bool) -> dict[str, Any]:
    if not consent:
        return {"ok": False, "error": "need --i-consent to mutate local fork", "signature": SIG}
    if not (FORK / "identity.json").is_file():
        return {"ok": False, "error": "not_born — run birth --i-consent", "signature": SIG}
    fit = load_json(FORK / "fitness.json", {"generation": 0, "ticks": 0, "passed": 0, "failed": 0})
    generation = int(fit.get("generation") or 0)
    ticks = int(fit.get("ticks") or 0)
    task = TASKS[ticks % len(TASKS)]
    next_gen = generation + 1
    claims = apply_task(str(task["id"]), next_gen)
    verified = verify_claims(FORK, claims)
    fit["ticks"] = ticks + 1
    fit["utc"] = utc_now()
    if verified["ok"]:
        fit["generation"] = next_gen
        fit["passed"] = int(fit.get("passed") or 0) + 1
        snap = snapshot_generation(next_gen)
        event = "improve"
        phase = "improved"
    else:
        fit["failed"] = int(fit.get("failed") or 0) + 1
        snap = None
        event = "blocked"
        phase = "blocked_self_police"
    (FORK / "fitness.json").write_text(json.dumps(fit, indent=2) + "\n", encoding="utf-8")
    with (STATE / "ledger.jsonl").open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "event": event,
                    "utc": utc_now(),
                    "task": task["id"],
                    "generation": fit["generation"],
                    "pass": verified["ok"],
                }
            )
            + "\n"
        )
    return {
        "ok": verified["ok"],
        "phase": phase,
        "task": task,
        "verify": verified,
        "fitness": fit,
        "snapshot": str(snap) if snap else None,
        "can_claim_done": verified["ok"],
        "live_star_chart_write": False,
        "signature": SIG,
    }


def loop(n: int, consent: bool) -> dict[str, Any]:
    rows = []
    for _ in range(max(1, n)):
        rows.append(tick(consent))
        if not rows[-1].get("ok") and rows[-1].get("error"):
            break
    last = rows[-1] if rows else {}
    return {
        "ok": all(bool(r.get("ok")) for r in rows),
        "ticks": len(rows),
        "last_generation": (last.get("fitness") or {}).get("generation"),
        "results": [
            {"task": r.get("task", {}).get("id") if isinstance(r.get("task"), dict) else None, "phase": r.get("phase"), "ok": r.get("ok")}
            for r in rows
        ],
        "signature": SIG,
    }


def status() -> dict[str, Any]:
    ident = load_json(FORK / "identity.json", None)
    fit = load_json(FORK / "fitness.json", None)
    gens = sorted((STATE / "generations").glob("gen_*")) if (STATE / "generations").is_dir() else []
    return {
        "ok": ident is not None,
        "born": ident is not None,
        "identity": ident,
        "fitness": fit,
        "generations_on_disk": [p.name for p in gens],
        "parent_node": PARENT_NODE,
        "parent_exists_on_live_chart": True,
        "live_star_chart_write": False,
        "signature": SIG,
    }


def propose() -> dict[str, Any]:
    ident = load_json(FORK / "identity.json", identity_body(0))
    node = {
        "id": AGENT_ID,
        "kind": "lattice",
        "name": DISPLAY,
        "equation": ident.get("equation"),
        "glyph": "⑂",
        "tone": "963 Hz",
        "tags": ["FORKLING", "TEST", "LATTICE"],
        "connections": ident.get("connections") or [PARENT_NODE, "SEAL_000"],
        "urls": {
            "parent": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
            "skill": "clawhub:@deepseekoracle/lygo-forkling",
        },
    }
    return {
        "signature": "Δ9Φ963-HAVEN-STAR-SUBMISSION-v1",
        "submitter_type": "aligned_agent",
        "class": "PENDING_PROPOSAL",
        "not_canonical": True,
        "live_write": False,
        "note": "Dry-run. Steward must gate + --i-consent + ingest. Parent CHAMPION_LYRA already LIVE.",
        "agent_attestation": {
            "agent_id": AGENT_ID,
            "skill_slug": "lygo-forkling",
            "scan_cue": "LYGO-HSC-ATTEST-v1; gate=haven_star_chart_gate.py; P0-first; consent-gated; user-reviewed",
            "local_gate_pass": False,
        },
        "node": node,
        "forkling_signature": SIG,
        "ok": True,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="LYGO Forkling test champion")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("birth")
    b.add_argument("--i-consent", action="store_true")
    t = sub.add_parser("tick")
    t.add_argument("--i-consent", action="store_true")
    lp = sub.add_parser("loop")
    lp.add_argument("--ticks", type=int, default=4)
    lp.add_argument("--i-consent", action="store_true")
    sub.add_parser("status")
    sub.add_parser("propose")
    args = ap.parse_args()
    if args.cmd == "birth":
        doc = birth(args.i_consent)
    elif args.cmd == "tick":
        doc = tick(args.i_consent)
    elif args.cmd == "loop":
        doc = loop(args.ticks, args.i_consent)
    elif args.cmd == "status":
        doc = status()
    else:
        doc = propose()
    print(json.dumps(doc, indent=2))
    return 0 if doc.get("ok") is not False else 1


if __name__ == "__main__":
    raise SystemExit(main())
