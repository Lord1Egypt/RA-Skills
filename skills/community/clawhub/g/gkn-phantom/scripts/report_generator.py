#!/usr/bin/env python3
"""Report Generator for the GKN-Phantom Penetration Testing Skill.

Assembles the final FinalOutput from validated findings, attack paths, and the
execution log. Produces:
  - executive summary (human readable)
  - technical findings table (JSON)
  - risk score 0-100 (see safety_policy.md §6)
  - remediation steps per finding
  - reproduction steps per finding
  - CI-friendly SARIF-like JSON (sibling artifact)
  - full execution log

Usage:
  python report_generator.py --findings findings.json --assets assets.json \
      --paths paths.json --log execution_log.json [--blocked-l4]
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json, finding_fingerprint

SEVERITY_POINTS = {"critical": 25, "high": 15, "medium": 8, "low": 3}


def _risk_score(findings: list[dict], blocked_l4: bool) -> int:
    score = 0
    for f in findings:
        if f.get("status") == "validated":
            score += SEVERITY_POINTS.get(f.get("severity", "low"), 0)
    if blocked_l4:
        score += 5
    return min(100, score)


def _summary(findings: list[dict], risk: int, blocked_l4: bool) -> str:
    validated = [f for f in findings if f.get("status") == "validated"]
    fps = [f for f in findings if f.get("status") == "false_positive"]
    by_type: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for f in validated:
        by_type[f.get("type", "unknown")] = by_type.get(f.get("type", "unknown"), 0) + 1
        by_sev[f.get("severity", "low")] = by_sev.get(f.get("severity", "low"), 0) + 1

    lines = []
    lines.append(f"Risk score: {risk}/100.")
    if not validated:
        lines.append("No validated findings.")
    else:
        lines.append(f"{len(validated)} validated finding(s), {len(fps)} false positive(s).")
        if by_sev:
            lines.append("By severity: " + ", ".join(f"{k}={v}" for k, v in sorted(by_sev.items(), key=lambda x: -SEVERITY_POINTS.get(x[0], 0))))
        if by_type:
            lines.append("By type: " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
    if blocked_l4:
        lines.append("Note: L4 (destructive) actions were blocked in safe_mode; latent risk may be higher.")
    return " ".join(lines)


def _sarif(findings: list[dict]) -> dict:
    """Build SARIF 2.1.0 with rich per-finding metadata for CI integration.

    Adds:
      - partialFingerprints: a short stable hash of the finding for CI
        baseline dedup (SARIF standard).
      - properties.tier: low/medium/high/critical from vuln_detector.
      - properties.confidence, properties.reproducible, properties.safe_poc.
    """
    results = []
    level_map = {"critical": "error", "high": "error", "medium": "warning", "low": "note"}
    for f in findings:
        if f.get("status") != "validated":
            continue
        try:
            fp = f.get("fingerprint") or finding_fingerprint(f)
        except Exception:
            fp = "0" * 16
        results.append({
            "ruleId": f"{f.get('type', 'unknown')}-{f.get('id', '')}",
            "level": level_map.get(f.get("severity", "low"), "note"),
            "message": {"text": f"{f.get('type', '').upper()} at {f.get('target', '')}: {f.get('evidence', {}).get('response', '')[:120]}"},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": f.get("target", "")}
                }
            }],
            "partialFingerprints": {"gkn-phantom/v1": fp},
            "properties": {
                "tier": f.get("tier", f.get("severity", "low")),
                "severity": f.get("severity", "low"),
                "confidence": f.get("confidence", 0.0),
                "reproducible": bool(f.get("reproducible", False)),
                "safe_poc": bool(f.get("safe_poc", True)),
            },
        })
    return {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": "gkn-phantom", "version": "1.0.0", "informationUri": "https://github.com/gkn/phantom"}},
            "results": results,
        }],
    }


def _recommendations(findings: list[dict]) -> list[str]:
    recs: list[str] = []
    seen_types: set[str] = set()
    for f in findings:
        if f.get("status") != "validated":
            continue
        t = f.get("type", "unknown")
        if t in seen_types:
            continue
        seen_types.add(t)
        recs.append(f"[{t}] {f.get('remediation', 'Apply vendor/security best practices for this vulnerability class.')}")
    return recs


def build_report(findings: list[dict], assets: dict, paths: list[dict],
                 execution_log: list[dict], blocked_l4: bool = False) -> dict:
    risk = _risk_score(findings, blocked_l4)
    report_findings = [f for f in findings if f.get("status") == "validated" and f.get("safe_poc")]
    return {
        "summary": _summary(findings, risk, blocked_l4),
        "risk_score": risk,
        "assets": assets,
        "findings": report_findings,
        "attack_paths": paths,
        "recommendations": _recommendations(findings),
        "sarif": _sarif(findings),
        "execution_log": execution_log,
    }


def _load(p: str):
    return load_json(p)


def main() -> int:
    ap = argparse.ArgumentParser(description="Report generator")
    ap.add_argument("--findings", required=True)
    ap.add_argument("--assets", required=True)
    ap.add_argument("--paths", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--blocked-l4", action="store_true")
    args = ap.parse_args()

    findings = _load(args.findings)
    assets = _load(args.assets)
    paths = _load(args.paths)
    log = _load(args.log)
    report = build_report(findings, assets, paths, log, args.blocked_l4)
    print(dump_json(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
