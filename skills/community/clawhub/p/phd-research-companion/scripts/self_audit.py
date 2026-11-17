#!/usr/bin/env python3
"""
Self-audit: the gap between "mathematically proven" and "publishable".

Running the proof once is not the same as being able to defend it in review.
This script cross-reads the proof ledger, the priority records, the exact
certificates and the revision history, then prints the blockers that would stop
a submission today.

Every blocker is either resolved or listed. There is no optimistic default.

Usage:
    python self_audit.py -p ./my-project
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def _j(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def audit(project: Path) -> dict:
    blockers: list[str] = []
    warnings: list[str] = []
    facts: list[str] = []

    ledger = _j(project / "02-methodology-dev" / "claims.json")
    prio = _j(project / "02-methodology-dev" / "priority-records.json")
    rev = _j(project / "05-revision-rounds" / "revision-history.json")
    cert_dir = project / "07-audit-trail"

    # --- ledger
    if ledger is None:
        blockers.append("no proof ledger (02-methodology-dev/claims.json); "
                        "run: run.py ledger --init 02-methodology-dev")
    else:
        claims = ledger.get("claims", {})
        facts.append(f"{len(claims)} claim(s) in ledger")
        if not claims:
            blockers.append("proof ledger is empty")
        for cid, c in sorted(claims.items()):
            st = c.get("status")
            if st == "open":
                warnings.append(f"{cid} is still OPEN: it must be stated as open in the paper")
            if st == "proven" and not c.get("proof"):
                blockers.append(f"{cid} marked proven but has no proof artifact")
            if st == "conditional":
                warnings.append(f"{cid} is CONDITIONAL: the assumption must be explicit")
            for d in (c.get("depends_on") or []):
                if d not in claims:
                    blockers.append(f"{cid} depends on unknown claim {d}")
                elif claims[d].get("status") not in ("proven", "definition", "assumption") \
                        and st == "proven":
                    blockers.append(
                        f"{cid} marked proven while dependency {d} is "
                        f"{claims[d].get('status')}")

    # --- priority
    if prio is None:
        warnings.append("no priority records; any novelty claim is currently unsupported")
    else:
        recs = prio.get("records", {})
        unresolved = [k for k, v in recs.items() if v.get("verdict") == "unchecked"]
        facts.append(f"{len(recs)} priority record(s), {len(unresolved)} unresolved")
        for k in unresolved:
            blockers.append(f"priority record {k} unresolved - "
                            f"the claim must not be called novel")

    # --- certificates
    certs = sorted(cert_dir.glob("certificate-*.json")) if cert_dir.is_dir() else []
    facts.append(f"{len(certs)} certificate(s) in 07-audit-trail")
    if not certs:
        warnings.append("no exact-arithmetic certificate; numerical claims are unsupported")
    for c in certs:
        data = _j(c)
        if data and data.get("float_contamination"):
            blockers.append(f"{c.name}: float contamination "
                            f"{data['float_contamination']} - not machine-precision evidence")
        if data and data.get("verdict") != "CERTIFIED":
            warnings.append(f"{c.name}: verdict {data.get('verdict')}")

    # --- revisions
    if rev is None:
        blockers.append("no revision history")
    else:
        done = int(rev.get("rounds_completed", 0))
        facts.append(f"{done} revision round(s)")
        if done < 5:
            blockers.append(f"only {done} revision round(s); >= 5 expected before submission")

    return {"blockers": blockers, "warnings": warnings, "facts": facts,
            "publishable": not blockers}


def render(result: dict, project: Path) -> str:
    verdict = "PUBLISHABLE (no blockers)" if result["publishable"] else "NOT PUBLISHABLE"
    lines = ["# Self-audit: proven vs publishable", "",
             f"Project: {project.name}",
             f"Audit date: {datetime.now().isoformat(timespec='seconds')}",
             f"Verdict: {verdict}", "",
             "## Facts", ""]
    lines += [f"- {f}" for f in result["facts"]] or ["- none"]
    lines += ["", "## Blockers", ""]
    lines += [f"- {b}" for b in result["blockers"]] or ["- none"]
    lines += ["", "## Warnings (must be disclosed, do not block)", ""]
    lines += [f"- {w}" for w in result["warnings"]] or ["- none"]
    lines += ["", "---",
              "A clean audit is a necessary condition, not a sufficient one.",
              "Generated by phd-research-companion 2.4.0"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Proven vs publishable gap report")
    ap.add_argument("-p", "--project", default=".")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any blocker exists")
    args = ap.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"error: project dir not found: {project}", file=sys.stderr)
        return 2

    result = audit(project)
    out = project / f"self-audit-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    out.write_text(render(result, project), encoding="utf-8")

    print(f"Verdict: {'PUBLISHABLE' if result['publishable'] else 'NOT PUBLISHABLE'}")
    print(f"Blockers: {len(result['blockers'])}  Warnings: {len(result['warnings'])}")
    for b in result["blockers"]:
        print(f"  [BLOCKER] {b}")
    for w in result["warnings"]:
        print(f"  [warn]    {w}")
    print(f"Report: {out}")
    return 1 if (args.strict and not result["publishable"]) else 0


if __name__ == "__main__":
    sys.exit(main())
