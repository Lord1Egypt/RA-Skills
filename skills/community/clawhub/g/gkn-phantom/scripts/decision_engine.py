#!/usr/bin/env python3
"""Heuristic Decision Engine — deterministic rule-based decisions.

v2.2 REFACTOR: Replaces the v2.1 sigmoid/Bayesian probabilistic layer with
a deterministic, explainable heuristic scoring + rule fallback system.

Decision types (all deterministic, no randomness):
  1. probe_continuation  — heuristic: discovery_yield >= threshold AND budget > 0
  2. severity_upgrade     — rule-based: PII/cross_user/corroboration score ≥ threshold
  3. scope_expansion      — rule-based: chain_potential >= threshold AND not production
  4. finding_confidence   — heuristic: evidence completeness + reproducibility + signal

This module is marked as OPTIONAL PLUGIN (v2.2). The core pipeline works
without it; when enabled, it provides explainable decision traces for
auditability and CI integration.

Usage (CLI):
  python decision_engine.py --decision continue --findings findings.json --probes 50 --budget 100
  python decision_engine.py --decision upgrade --finding finding.json
  python decision_engine.py --decision expand --findings findings.json --candidate target.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json


# ---- Heuristic thresholds (all human-readable) -------------------------------
THRESHOLD_CONTINUE_YIELD = 0.05    # min discovery rate to continue probing
THRESHOLD_UPGRADE_SCORE = 2.5      # min composite score for severity upgrade
THRESHOLD_EXPAND_CHAIN = 0.5       # min chain potential to propose expansion

# ---- Severity order for upgrade decisions ------------------------------------
SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}

# ---- Heuristic weights for finding confidence (sum = 1.0) --------------------
CONFIDENCE_WEIGHTS = {
    "evidence_completeness": 0.35,  # how many required evidence fields are present
    "reproducibility": 0.35,         # how many replays matched
    "signal_strength": 0.20,         # how strong the detection signal is
    "corroboration": 0.10,           # multi-source agreement
}


@dataclass
class DecisionResult:
    """Deterministic decision output with full explainability trace."""
    decision: str
    score: float
    threshold: float
    reasoning: str
    factors: dict = field(default_factory=dict)
    rule_path: str = ""  # which rule chain was followed
    deterministic: bool = True


# =============================================================================
# 1. Probe Continuation — heuristic yield-based
# =============================================================================

def decide_probe_continuation(findings: list, probes_executed: int,
                              probe_budget: int) -> DecisionResult:
    """Should the agent continue probing?

    HEURISTIC RULES (evaluated in order, first match wins):
      Rule A: probes_executed >= budget → STOP (budget exhausted)
      Rule B: no findings at all AND probes > 20% of budget → STOP (low yield)
      Rule C: discovery_yield >= 0.05 → CONTINUE (still finding vulns)
      Rule D: budget_remaining > 50% AND probes < 20 → CONTINUE (early stage)
      Rule E: otherwise → STOP (diminishing returns)
    """
    n = max(1, probes_executed)
    B = max(1, probe_budget)
    budget_used_ratio = n / B
    budget_remaining_ratio = 1.0 - budget_used_ratio

    validated_count = sum(1 for f in findings if f.get("status") == "validated")
    discovery_yield = validated_count / n

    # Rule A: budget exhausted
    if probes_executed >= probe_budget:
        return DecisionResult(
            decision="stop", score=0.0, threshold=THRESHOLD_CONTINUE_YIELD,
            reasoning=f"Budget exhausted ({probes_executed}/{probe_budget} probes)",
            factors={"discovery_yield": round(discovery_yield, 4),
                     "budget_used": round(budget_used_ratio, 4),
                     "validated_count": validated_count},
            rule_path="A: budget_exhausted")

    # Rule B: low yield early
    if validated_count == 0 and budget_used_ratio > 0.20:
        return DecisionResult(
            decision="stop", score=discovery_yield, threshold=THRESHOLD_CONTINUE_YIELD,
            reasoning=f"No findings after {probes_executed} probes ({budget_used_ratio:.0%} budget); low yield",
            factors={"discovery_yield": round(discovery_yield, 4),
                     "budget_used": round(budget_used_ratio, 4),
                     "validated_count": 0},
            rule_path="B: low_yield_early")

    # Rule C: still finding vulns
    if discovery_yield >= THRESHOLD_CONTINUE_YIELD:
        return DecisionResult(
            decision="continue", score=discovery_yield, threshold=THRESHOLD_CONTINUE_YIELD,
            reasoning=f"Discovery yield {discovery_yield:.1%} >= {THRESHOLD_CONTINUE_YIELD:.1%}; {validated_count} findings so far",
            factors={"discovery_yield": round(discovery_yield, 4),
                     "budget_remaining": round(budget_remaining_ratio, 4),
                     "validated_count": validated_count,
                     "probes_executed": probes_executed},
            rule_path="C: yielding")

    # Rule D: early stage, lots of budget left
    if budget_remaining_ratio > 0.50 and probes_executed < 20:
        return DecisionResult(
            decision="continue", score=discovery_yield, threshold=THRESHOLD_CONTINUE_YIELD,
            reasoning=f"Early stage ({probes_executed} probes, {budget_remaining_ratio:.0%} budget remaining); continuing",
            factors={"discovery_yield": round(discovery_yield, 4),
                     "budget_remaining": round(budget_remaining_ratio, 4),
                     "probes_executed": probes_executed},
            rule_path="D: early_stage")

    # Rule E: diminishing returns
    return DecisionResult(
        decision="stop", score=discovery_yield, threshold=THRESHOLD_CONTINUE_YIELD,
        reasoning=f"Diminishing returns: yield {discovery_yield:.1%}, {probes_executed} probes, {budget_remaining_ratio:.0%} budget remaining",
        factors={"discovery_yield": round(discovery_yield, 4),
                 "budget_used": round(budget_used_ratio, 4),
                 "validated_count": validated_count,
                 "probes_executed": probes_executed},
        rule_path="E: diminishing_returns")


# =============================================================================
# 2. Severity Upgrade — rule-based scoring
# =============================================================================

def decide_severity_upgrade(finding: dict) -> DecisionResult:
    """Should a finding's severity be upgraded?

    HEURISTIC RULES (additive scoring, no sigmoid):
      +3.0  exposes PII (email/phone/SSN/password/secret/api_key/token in response)
      +2.5  cross-user impact (IDOR or stored XSS on high-severity finding)
      +2.0  corroboration >= 0.5 (multi-source agreement)
      +1.5  reproducibility >= 0.8 (high replay confidence)
      -----
      score >= 2.5 → UPGRADE one level (e.g., medium→high, high→critical)
      score < 2.5  → KEEP current severity

    This is deterministic: same finding always produces the same decision.
    """
    evidence = finding.get("evidence", {})
    response = (evidence.get("response", "") or "").lower()
    confidence_breakdown = finding.get("confidence_breakdown", {})

    # Factor 1: PII exposure (deterministic string check)
    pii_patterns = ["email", "phone", "ssn", "password", "secret", "api_key", "token"]
    exposes_pii = 1.0 if any(p in response for p in pii_patterns) else 0.0

    # Factor 2: cross-user impact
    vtype = finding.get("type", "")
    cross_user = 1.0 if vtype in ("idor", "xss") and finding.get("severity") == "high" else 0.0

    # Factor 3: corroboration
    corroboration = confidence_breakdown.get("corroboration", 0.0)

    # Factor 4: reproducibility
    reproducibility = finding.get("reproducibility_score",
                                  confidence_breakdown.get("reproducibility_score", 0.0))

    # Composite score (additive, not sigmoid)
    score = (3.0 * exposes_pii
             + 2.5 * cross_user
             + 2.0 * (1.0 if corroboration >= 0.5 else 0.0)
             + 1.5 * (1.0 if reproducibility >= 0.8 else 0.0))

    current_sev = finding.get("severity", "low")
    sev_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}

    # Determine upgrade target
    new_sev = current_sev
    for s, rank in sev_order.items():
        if rank == sev_order.get(current_sev, 0) + 1:
            new_sev = s
            break

    if score >= THRESHOLD_UPGRADE_SCORE and sev_order.get(current_sev, 0) < 3:
        return DecisionResult(
            decision="upgrade", score=round(score, 2), threshold=THRESHOLD_UPGRADE_SCORE,
            reasoning=(f"Upgrade score {score:.1f} >= {THRESHOLD_UPGRADE_SCORE} "
                       f"(PII={exposes_pii:.0f}, cross_user={cross_user:.0f}, "
                       f"corroboration={corroboration:.2f}, reproducibility={reproducibility:.2f}); "
                       f"upgrading {current_sev} → {new_sev}"),
            factors={"exposes_pii": exposes_pii, "cross_user": cross_user,
                     "corroboration": round(corroboration, 4),
                     "reproducibility": round(reproducibility, 4),
                     "current_severity": current_sev, "target_severity": new_sev},
            rule_path="upgrade: score >= threshold")
    else:
        return DecisionResult(
            decision="keep_severity", score=round(score, 2), threshold=THRESHOLD_UPGRADE_SCORE,
            reasoning=(f"Upgrade score {score:.1f} < {THRESHOLD_UPGRADE_SCORE} "
                       f"(PII={exposes_pii:.0f}, cross_user={cross_user:.0f}, "
                       f"corroboration={corroboration:.2f}, reproducibility={reproducibility:.2f}); "
                       f"keeping {current_sev}"),
            factors={"exposes_pii": exposes_pii, "cross_user": cross_user,
                     "corroboration": round(corroboration, 4),
                     "reproducibility": round(reproducibility, 4),
                     "current_severity": current_sev},
            rule_path="keep: score < threshold")


# =============================================================================
# 3. Scope Expansion — rule-based gating
# =============================================================================

def decide_scope_expansion(findings: list, candidate_target: dict,
                           current_scope: dict) -> DecisionResult:
    """Should the agent propose expanding scope to a new target?

    HEURISTIC RULES (gating, not probabilistic):
      Gate 1: candidate is production → BLOCK (never expand to production)
      Gate 2: candidate risk_score >= 80 → BLOCK (too dangerous)
      Gate 3: chain_potential < 0.5 → KEEP (not enough attack chain value)
      Gate 4: validated findings < 1 → KEEP (no findings to chain from)
      Gate 5: all gates passed → PROPOSE EXPANSION (still needs human approval)
    """
    validated = [f for f in findings if f.get("status") == "validated"]
    candidate_url = candidate_target.get("url", "") or candidate_target.get("target", "")
    candidate_path = candidate_url.lower()

    # Gate 1: production check
    env = candidate_target.get("environment", "staging")
    if env == "production":
        return DecisionResult(
            decision="keep_scope", score=0.0, threshold=THRESHOLD_EXPAND_CHAIN,
            reasoning="Candidate is production environment; scope expansion BLOCKED",
            factors={"environment": env, "chain_potential": 0.0},
            rule_path="Gate1: production_blocked")

    # Gate 2: risk score gate
    risk_score = candidate_target.get("risk_score", 50)
    if risk_score >= 80:
        return DecisionResult(
            decision="keep_scope", score=0.0, threshold=THRESHOLD_EXPAND_CHAIN,
            reasoning=f"Candidate risk score {risk_score} >= 80; too dangerous to expand",
            factors={"risk_score": risk_score, "environment": env},
            rule_path="Gate2: risk_too_high")

    # Gate 4: need at least one validated finding to chain from
    if len(validated) == 0:
        return DecisionResult(
            decision="keep_scope", score=0.0, threshold=THRESHOLD_EXPAND_CHAIN,
            reasoning="No validated findings to chain from; scope expansion not justified",
            factors={"validated_count": 0, "environment": env},
            rule_path="Gate4: no_findings")

    # Gate 3: chain potential assessment (deterministic heuristic)
    chain_potential = _assess_chain_potential(validated, candidate_path)

    if chain_potential < THRESHOLD_EXPAND_CHAIN:
        return DecisionResult(
            decision="keep_scope", score=chain_potential, threshold=THRESHOLD_EXPAND_CHAIN,
            reasoning=f"Chain potential {chain_potential:.2f} < {THRESHOLD_EXPAND_CHAIN}; expansion not justified",
            factors={"chain_potential": round(chain_potential, 4),
                     "risk_score": risk_score, "environment": env,
                     "validated_count": len(validated)},
            rule_path="Gate3: low_chain_potential")

    # Gate 5: all passed → propose expansion
    return DecisionResult(
        decision="expand", score=chain_potential, threshold=THRESHOLD_EXPAND_CHAIN,
        reasoning=(f"Chain potential {chain_potential:.2f} >= {THRESHOLD_EXPAND_CHAIN}, "
                   f"risk {risk_score}/100, env={env}; "
                   f"PROPOSING scope expansion (requires human approval)"),
        factors={"chain_potential": round(chain_potential, 4),
                 "risk_score": risk_score, "environment": env,
                 "validated_count": len(validated)},
        rule_path="Gate5: propose_expansion")


def _assess_chain_potential(validated_findings: list, candidate_path: str) -> float:
    """Deterministic chain potential assessment.

    Rules:
      +0.7  component_exposure finding exists → candidate can be exploited via exposed API
      +0.6  weak_credential finding exists → candidate may be accessible with creds
      +0.5  candidate is on same host as an existing finding → direct chain
      +0.3  any high-severity finding exists → general attack surface

    Capped at 1.0.
    """
    potential = 0.0
    from urllib.parse import urlparse

    for f in validated_findings:
        f_target = f.get("target", "").lower()

        # Component exposure → high chain value
        if f.get("type") == "component_exposure":
            potential = max(potential, 0.7)

        # Weak credential → authenticated access chain
        if f.get("type") == "weak_credential":
            potential = max(potential, 0.6)

        # Same host → direct chain
        try:
            f_host = urlparse(f_target).hostname or ""
            c_host = urlparse(candidate_path).hostname or ""
            if f_host and c_host and f_host == c_host:
                potential = max(potential, 0.5)
        except Exception:
            pass

        # High-severity finding → general attack surface
        if f.get("severity") in ("high", "critical"):
            potential = max(potential, 0.3)

    return min(1.0, potential)


# =============================================================================
# 4. Finding Confidence — heuristic scoring (replaces Bayesian posterior)
# =============================================================================

def heuristic_confidence(finding: dict) -> dict:
    """Compute deterministic heuristic confidence for a finding.

    Replaces the v2.1 Bayesian posterior with a transparent additive score:

      evidence_completeness (0.35): how many required evidence fields are present
      reproducibility (0.35):      fraction of replays that matched
      signal_strength (0.20):      per-type signal clarity baseline
      corroboration (0.10):        multi-source agreement

    This is 100% deterministic — same finding always yields the same score.
    """
    vtype = finding.get("type", "")
    evidence = finding.get("evidence", {})

    # ---- evidence_completeness (0.0-1.0) ----
    core_fields = ["request", "response", "timestamp", "tool"]
    present = sum(1 for f in core_fields if evidence.get(f))
    ev_score = present / len(core_fields)

    # ---- reproducibility (0.0-1.0) ----
    replay_results = finding.get("replay_results", [])
    if replay_results:
        matched = sum(1 for r in replay_results if r.get("signal_matched"))
        rep_score = matched / len(replay_results)
    elif finding.get("reproducible"):
        rep_score = 0.5  # single confirmation
    else:
        rep_score = 0.0

    # ---- signal_strength (0.0-1.0) ----
    # Per-type baseline signal clarity (same as confidence_scoring.py)
    SIGNAL_CLARITY = {
        "sqli": 0.90, "path_traversal": 0.92, "command_injection": 0.85,
        "ssti": 0.88, "component_exposure": 0.90, "weak_credential": 0.88,
        "info_leak": 0.80, "xss": 0.75, "open_redirect": 0.78, "idor": 0.80,
        "captcha_bypass": 0.75, "file_upload": 0.78, "logic_flaw": 0.65,
        "csrf": 0.70, "misconfig": 0.72, "ssrf": 0.65, "xxe": 0.68,
        "deserialization": 0.60, "rce": 0.70, "auth_bypass": 0.72,
        "priv_esc": 0.68, "data_exposure": 0.75,
    }
    sig_score = SIGNAL_CLARITY.get(vtype, 0.5)
    if finding.get("safe_poc"):
        sig_score = min(1.0, sig_score + 0.05)

    # ---- corroboration (0.0-1.0) ----
    corr_score = 0.0
    if len(replay_results) >= 2 and all(r.get("signal_matched") for r in replay_results):
        corr_score += 0.5
    adaptive = finding.get("adaptive_metadata", {})
    if adaptive.get("waf_detected"):
        corr_score += 0.3
    if adaptive.get("mutations_tried", 0) > 0:
        corr_score += 0.2
    corr_score = min(1.0, corr_score)

    # ---- weighted aggregate ----
    confidence = (
        CONFIDENCE_WEIGHTS["evidence_completeness"] * ev_score
        + CONFIDENCE_WEIGHTS["reproducibility"] * rep_score
        + CONFIDENCE_WEIGHTS["signal_strength"] * sig_score
        + CONFIDENCE_WEIGHTS["corroboration"] * corr_score
    )
    confidence = round(min(1.0, max(0.0, confidence)), 4)

    return {
        "vuln_type": vtype,
        "confidence": confidence,
        "meets_threshold": confidence >= 0.80,
        "threshold": 0.80,
        "method": "heuristic_v1",
        "breakdown": {
            "evidence_completeness": round(ev_score, 4),
            "reproducibility": round(rep_score, 4),
            "signal_strength": round(sig_score, 4),
            "corroboration": round(corr_score, 4),
        },
        "deterministic": True,
    }


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="Heuristic decision engine (v2.2 deterministic)")
    ap.add_argument("--decision", required=True,
                    choices=["continue", "upgrade", "expand", "confidence"],
                    help="Decision type")
    ap.add_argument("--findings", help="Findings JSON array (for continue/expand)")
    ap.add_argument("--finding", help="Single finding JSON (for upgrade/confidence)")
    ap.add_argument("--candidate", help="Candidate target JSON (for expand)")
    ap.add_argument("--scope", help="Current scope JSON (for expand)")
    ap.add_argument("--probes", type=int, default=0)
    ap.add_argument("--budget", type=int, default=100)
    args = ap.parse_args()

    if args.decision == "continue":
        findings = load_json(args.findings) if args.findings else []
        result = decide_probe_continuation(findings, args.probes, args.budget)
        print(dump_json({
            "decision": result.decision, "score": result.score,
            "threshold": result.threshold, "reasoning": result.reasoning,
            "factors": result.factors, "rule_path": result.rule_path,
        }))

    elif args.decision == "upgrade":
        finding = load_json(args.finding) if args.finding else {}
        result = decide_severity_upgrade(finding)
        print(dump_json({
            "decision": result.decision, "score": result.score,
            "threshold": result.threshold, "reasoning": result.reasoning,
            "factors": result.factors, "rule_path": result.rule_path,
        }))

    elif args.decision == "expand":
        findings = load_json(args.findings) if args.findings else []
        candidate = load_json(args.candidate) if args.candidate else {}
        scope = load_json(args.scope) if args.scope else {}
        result = decide_scope_expansion(findings, candidate, scope)
        print(dump_json({
            "decision": result.decision, "score": result.score,
            "threshold": result.threshold, "reasoning": result.reasoning,
            "factors": result.factors, "rule_path": result.rule_path,
        }))

    elif args.decision == "confidence":
        finding = load_json(args.finding) if args.finding else {}
        result = heuristic_confidence(finding)
        print(dump_json(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
