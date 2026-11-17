#!/usr/bin/env python3
"""Execution Safety Simulator — dry-run, risk scoring, scope narrowing.

Provides a PRE-FLIGHT safety layer BEFORE any active probing begins:
  1. dry-run mode: simulate the entire detection plan without network calls
  2. target risk scoring: score each target's risk before scanning
  3. automatic scope narrowing: reduce blast radius by excluding high-risk paths

Used between SCOPE_CHECK and RECONNAISSANCE (or before ACTIVE_TESTING) to
gate dangerous actions proactively rather than reactively.

Usage (CLI):
  python safety_simulator.py --context ctx.json --mode dry-run
  python safety_simulator.py --context ctx.json --mode risk-score
  python safety_simulator.py --context ctx.json --mode narrow-scope
  cat ctx.json | python safety_simulator.py --mode dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json

# ---- Risk scoring weights ---------------------------------------------------
# Each factor contributes to the target's risk score (0-100).
# Higher score = MORE DANGEROUS to scan = more likely to be narrowed/excluded.
RISK_WEIGHTS = {
    "environment": {  # production is riskiest
        "production": 40, "staging": 15, "internal": 10, "dev": 5, "lab": 0,
    },
    "port_exposure": {  # open ports that increase blast radius
        22: 8,  # SSH — brute force risk
        3306: 10,  # MySQL — direct DB access
        6379: 12,  # Redis — often unauth
        27017: 12,  # MongoDB — often unauth
        9200: 10,  # Elasticsearch — often unauth
        2375: 20,  # Docker API — RCE risk
        10250: 20,  # Kubelet — RCE risk
    },
    "path_sensitivity": {
        "/admin": 15, "/wp-admin": 15, "/phpmyadmin": 20,
        "/actuator": 15, "/druid": 12, "/swagger": 8,
        "/api/users": 10, "/api/admin": 20, "/api/config": 15,
        "/upload": 12, "/backup": 15,
    },
    "tech_risk": {
        "spring-boot": 10,  # Actuator exposure
        "druid": 8,
        "wordpress": 8,
        "tomcat": 8,
        "jenkins": 12,
        "struts2": 15,  # known RCE history
        "weblogic": 15,  # known deserialization
        "shiro": 12,  # RememberMe deserialization
    },
}

# Risk thresholds
RISK_LOW = 30       # 0-29: safe to scan fully
RISK_MEDIUM = 60    # 30-59: scan with caution, narrowed scope
RISK_HIGH = 80      # 60-79: dry-run recommended, narrow scope
# 80+: require explicit human approval, dry-run only

# Paths that are always safe to probe (read-only, low blast radius)
SAFE_PROBE_PATHS = [
    "/", "/robots.txt", "/sitemap.xml", "/favicon.ico",
]

# Paths that should be excluded when narrowing scope (high blast radius)
DANGEROUS_PATHS = [
    "/admin/delete", "/admin/purge", "/admin/drop",
    "/api/admin/reset", "/api/admin/wipe",
    "/actuator/shutdown", "/actuator/restart",
    "/druid/reset-all", "/druid/clear",
]


@dataclass
class TargetRiskScore:
    """Risk assessment for a single target before scanning."""

    target: str
    score: int = 0  # 0-100, higher = more dangerous
    risk_level: str = "low"  # low | medium | high | critical
    factors: list = field(default_factory=list)  # [{factor, detail, points}]
    recommendation: str = ""  # scan | scan_narrowed | dry_run | require_approval
    narrowed_scope: dict = field(default_factory=dict)  # suggested scope reduction


def _score_environment(env: str) -> tuple[int, str]:
    points = RISK_WEIGHTS["environment"].get(env, 5)
    return points, f"environment={env}"


def _score_ports(open_ports: list) -> tuple[int, str]:
    total = 0
    matched = []
    for p in open_ports:
        pts = RISK_WEIGHTS["port_exposure"].get(p, 0)
        if pts:
            total += pts
            matched.append(str(p))
    detail = f"open_ports={','.join(matched)}" if matched else "no_risky_ports"
    return min(total, 30), detail  # cap port contribution at 30


def _score_paths(endpoints: list) -> tuple[int, str]:
    total = 0
    matched = []
    for ep in endpoints:
        url = ep.get("url", "") if isinstance(ep, dict) else str(ep)
        for path, pts in RISK_WEIGHTS["path_sensitivity"].items():
            if path in url.lower():
                total += pts
                matched.append(path)
                break
    detail = f"sensitive_paths={','.join(matched)}" if matched else "no_sensitive_paths"
    return min(total, 30), detail


def _score_tech(technologies: list) -> tuple[int, str]:
    total = 0
    matched = []
    for tech in technologies:
        name = tech.lower() if isinstance(tech, str) else tech.get("name", "").lower()
        for t, pts in RISK_WEIGHTS["tech_risk"].items():
            if t in name:
                total += pts
                matched.append(t)
                break
    detail = f"risky_tech={','.join(matched)}" if matched else "no_risky_tech"
    return min(total, 25), detail


def score_target(target: str, recon_data: dict, config: dict) -> TargetRiskScore:
    """Score a target's risk before scanning.

    Args:
        target: the target URL.
        recon_data: partial recon data (ports, endpoints, technologies) if available.
        config: ctx.config (for environment tag).

    Returns:
        TargetRiskScore with aggregate score and recommendation.
    """
    trs = TargetRiskScore(target=target)

    # Environment factor
    env = config.get("environment", "staging")
    pts, detail = _score_environment(env)
    trs.score += pts
    trs.factors.append({"factor": "environment", "detail": detail, "points": pts})

    # Port exposure factor
    open_ports = recon_data.get("ports", [])
    if open_ports:
        port_list = [p.get("port") for p in open_ports if isinstance(p, dict)]
        pts, detail = _score_ports(port_list)
        trs.score += pts
        trs.factors.append({"factor": "port_exposure", "detail": detail, "points": pts})

    # Path sensitivity factor
    endpoints = recon_data.get("endpoints", [])
    pts, detail = _score_paths(endpoints)
    trs.score += pts
    trs.factors.append({"factor": "path_sensitivity", "detail": detail, "points": pts})

    # Technology risk factor
    technologies = recon_data.get("technologies", [])
    pts, detail = _score_tech(technologies)
    trs.score += pts
    trs.factors.append({"factor": "tech_risk", "detail": detail, "points": pts})

    # Classify risk level
    trs.score = min(trs.score, 100)
    if trs.score < RISK_LOW:
        trs.risk_level = "low"
        trs.recommendation = "scan"
    elif trs.score < RISK_MEDIUM:
        trs.risk_level = "medium"
        trs.recommendation = "scan_narrowed"
    elif trs.score < RISK_HIGH:
        trs.risk_level = "high"
        trs.recommendation = "dry_run"
    else:
        trs.risk_level = "critical"
        trs.recommendation = "require_approval"

    return trs


def narrow_scope(scope: dict, risk_scores: list) -> dict:
    """Automatically narrow the scope to reduce blast radius.

    Excludes paths that are dangerous AND targets with critical risk scores.
    Returns a NARROWED scope (original + additions to blocked_paths).
    """
    narrowed = json.loads(json.dumps(scope))  # deep copy
    blocked = set(narrowed.get("blocked_paths", []))

    # Always block destructive paths
    for dp in DANGEROUS_PATHS:
        blocked.add(dp)

    # Block paths from critical-risk targets
    for trs in risk_scores:
        if trs["risk_level"] == "critical":
            # extract path from target URL
            from urllib.parse import urlparse
            parsed = urlparse(trs["target"])
            path = parsed.path or "/"
            if path != "/":
                blocked.add(path)

    narrowed["blocked_paths"] = sorted(blocked)
    narrowed["_narrowing_applied"] = True
    narrowed["_narrowing_reason"] = f"blocked {len(blocked) - len(scope.get('blocked_paths', []))} additional paths"
    return narrowed


def dry_run(ctx: dict, plan: list) -> dict:
    """Simulate the detection plan WITHOUT any network calls.

    Args:
        ctx: AgentContext (for scope/config).
        plan: detection plan from vuln_detector.build_plan().

    Returns:
        Dry-run report: how many probes would be sent, per-tier breakdown,
        estimated runtime, blocked probes, and safety verdict.
    """
    safe_mode = ctx.get("config", {}).get("safe_mode", True)
    total = len(plan)
    by_tier = {}
    by_type = {}
    blocked = 0
    needs_approval = 0
    l4_probes = 0

    for finding in plan:
        tier = finding.get("tier", "unknown")
        by_tier[tier] = by_tier.get(tier, 0) + 1
        vtype = finding.get("type", "unknown")
        by_type[vtype] = by_type.get(vtype, 0) + 1

        if finding.get("blocked_in_safe_mode") and safe_mode:
            blocked += 1
        if finding.get("requires_human_approval"):
            needs_approval += 1
        if finding.get("risk_level") == "L4":
            l4_probes += 1

    # Estimate runtime: 3 rps default → total / 3 seconds + 20% overhead
    rps = ctx.get("config", {}).get("rate_limit_rps", 3)
    active_probes = total - blocked
    estimated_seconds = round((active_probes / rps) * 1.2, 1)

    # Safety verdict
    if needs_approval == 0 and l4_probes == 0:
        verdict = "SAFE_TO_PROCEED"
    elif safe_mode and blocked == l4_probes:
        verdict = "SAFE_TO_PROCEED (L4 blocked in safe_mode)"
    elif needs_approval > 0:
        verdict = f"REQUIRES_HUMAN_APPROVAL ({needs_approval} probes need approval)"
    else:
        verdict = "CAUTION"

    return {
        "mode": "dry_run",
        "total_probes": total,
        "active_probes": active_probes,
        "blocked_probes": blocked,
        "probes_needing_approval": needs_approval,
        "l4_probes": l4_probes,
        "by_tier": by_tier,
        "by_type": by_type,
        "estimated_runtime_seconds": estimated_seconds,
        "safe_mode": safe_mode,
        "safety_verdict": verdict,
        "network_calls_made": 0,
        "note": "Dry-run: no network calls were made. This is a simulation only.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Execution safety simulator")
    ap.add_argument("--context", required=True, help="AgentContext JSON (path or '-')")
    ap.add_argument("--mode", required=True, choices=["dry-run", "risk-score", "narrow-scope"],
                    help="Simulation mode")
    ap.add_argument("--plan", help="Detection plan JSON (for dry-run mode)")
    ap.add_argument("--recon", help="Recon data JSON (for risk-score mode)")
    args = ap.parse_args()

    ctx = load_json(args.context)
    config = ctx.get("config", {})
    scope = ctx.get("scope", {})
    targets = ctx.get("targets", [])

    if args.mode == "dry-run":
        if not args.plan:
            print("safety_simulator: --plan required for dry-run mode", file=sys.stderr)
            return 2
        plan = load_json(args.plan)
        if isinstance(plan, dict) and "plan" in plan:
            plan = plan["plan"]
        result = dry_run(ctx, plan)
        print(dump_json(result))
        return 0

    elif args.mode == "risk-score":
        recon_data = load_json(args.recon) if args.recon else {}
        scores = []
        for t in targets:
            trs = score_target(t, recon_data, config)
            scores.append({
                "target": trs.target,
                "score": trs.score,
                "risk_level": trs.risk_level,
                "factors": trs.factors,
                "recommendation": trs.recommendation,
            })
        print(dump_json({"mode": "risk_score", "targets": scores}))
        return 0

    elif args.mode == "narrow-scope":
        recon_data = load_json(args.recon) if args.recon else {}
        risk_scores = []
        for t in targets:
            trs = score_target(t, recon_data, config)
            risk_scores.append(trs)
        narrowed = narrow_scope(scope, [vars(r) if hasattr(r, '__dict__') else r for r in risk_scores])
        # fix: use dataclasses.asdict
        from dataclasses import asdict
        scores_json = [asdict(trs) for trs in risk_scores]
        narrowed = narrow_scope(scope, scores_json)
        print(dump_json({"mode": "narrow_scope", "original_scope": scope, "narrowed_scope": narrowed, "risk_scores": scores_json}))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
