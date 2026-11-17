#!/usr/bin/env python3
"""Confidence Scoring System — evidence-based finding confidence.

Computes a multi-factor confidence score (0.0–1.0) for each finding based on:
  1. evidence_strength   — how complete and specific the evidence is
  2. reproducibility     — fraction of replays that matched the signal
  3. signal_clarity      — how unambiguous the detection signal is
  4. corroboration       — multiple independent signals or tools agree

The aggregate `confidence` is a weighted combination. A finding with
confidence >= 0.8 is promoted from `detected` to `validated`.

This replaces the simple "+0.3 on match" heuristic in finding_validator.py
with a transparent, tunable scoring model.

Usage (CLI):
  python confidence_scoring.py --finding finding.json
  cat finding.json | python confidence_scoring.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json

# ---- Scoring weights (sum = 1.0) -------------------------------------------
WEIGHTS = {
    "evidence_strength": 0.30,
    "reproducibility": 0.30,
    "signal_clarity": 0.25,
    "corroboration": 0.15,
}

# Confidence threshold for promotion: detected → validated
PROMOTION_THRESHOLD = 0.80

# ---- Signal clarity map: how unambiguous is each vuln type's signal? -------
# Types with deterministic, unique signals score higher.
SIGNAL_CLARITY_BASELINE = {
    # High clarity — unique, deterministic signals
    "sqli": 0.90,              # DB error signature is highly specific
    "path_traversal": 0.92,    # root:x:0:0: is unambiguous
    "command_injection": 0.85, # time delta is measurable
    "ssti": 0.88,              # 7*7=49 arithmetic is deterministic
    "component_exposure": 0.90,# /actuator/env JSON is specific
    "weak_credential": 0.88,   # login success with default cred is clear
    "info_leak": 0.80,         # 200 on .git/config is clear, but some false positives
    # Medium clarity — signal present but could be ambiguous
    "xss": 0.75,               # reflection could be in a safe context
    "open_redirect": 0.78,     # 3xx Location is clear, but meta-refresh less so
    "idor": 0.80,              # 200 vs 403 differential is clear
    "captcha_bypass": 0.75,    # bypass success is clear, but edge cases
    "file_upload": 0.78,       # file accessible is clear, executability less so
    "logic_flaw": 0.65,        # logic flaws are inherently ambiguous
    "csrf": 0.70,              # missing token is clear, but SameSite nuances
    "misconfig": 0.72,         # missing header is clear, but severity varies
    # Lower clarity — inference-based signals
    "ssrf": 0.65,              # OOB callback is clear, but timing-dependent
    "xxe": 0.68,               # OOB callback, but error-based less certain
    "deserialization": 0.60,   # stack trace present, but may be unrelated
    "rce": 0.70,               # second probe confirmation, but time-based uncertainty
    "auth_bypass": 0.72,       # accepted token is clear, but JWT edge cases
    "priv_esc": 0.68,          # 200 on admin endpoint is clear, but role nuances
    "data_exposure": 0.75,     # PII regex is clear, but threshold-based
}


@dataclass
class ConfidenceBreakdown:
    """Multi-factor confidence breakdown for a finding."""

    evidence_strength: float   # 0.0–1.0
    reproducibility_score: float  # 0.0–1.0
    signal_clarity: float      # 0.0–1.0
    corroboration: float       # 0.0–1.0
    confidence: float          # 0.0–1.0 (weighted aggregate)
    method: str = "weighted_v2"
    meets_threshold: bool = False


def score_evidence_strength(finding: dict) -> float:
    """Score how complete and specific the evidence is.

    Factors:
      - all 4 core evidence fields present (request/response/timestamp/tool)
      - status_code present (HTTP response confirmed)
      - response_time_ms present (timing evidence)
      - response body non-trivial (>100 chars suggests real content)
      - headers present (structured evidence)
    """
    evidence = finding.get("evidence", {})
    score = 0.0

    # Core fields (required by safety_policy.md §5)
    core_fields = ["request", "response", "timestamp", "tool"]
    present = sum(1 for f in core_fields if evidence.get(f))
    score += (present / len(core_fields)) * 0.5  # 50% weight

    # Extended fields
    if evidence.get("status_code") is not None:
        score += 0.15
    if evidence.get("response_time_ms") is not None:
        score += 0.10

    # Response body substance
    response = evidence.get("response", "") or ""
    if len(response) > 100:
        score += 0.15
    elif len(response) > 20:
        score += 0.08

    # Headers present
    if evidence.get("headers"):
        score += 0.10

    return min(1.0, score)


def score_reproducibility(finding: dict) -> float:
    """Score what fraction of replays matched the detection signal.

    If replay_results are present, compute match_rate = matched / total.
    If no replays yet (candidate finding), return 0.0 (not yet reproduced).
    If reproducible=True with no replay data, return 0.5 (single confirmation).
    """
    replay_results = finding.get("replay_results", [])
    replay_count = finding.get("replay_count", 0)

    if replay_results:
        matched = sum(1 for r in replay_results if r.get("signal_matched"))
        return matched / len(replay_results)

    if replay_count > 0:
        # replay_count set but no detail — assume all matched if reproducible
        if finding.get("reproducible"):
            return 1.0
        return 0.0

    # No replays yet
    if finding.get("reproducible"):
        return 0.5  # single confirmation, no multi-replay data
    return 0.0


def score_signal_clarity(finding: dict) -> float:
    """Score how unambiguous the detection signal is for this vuln type.

    Uses the SIGNAL_CLARITY_BASELINE map, adjusted by:
      - safe_poc=True → slight boost (confirmed safe detection method)
      - detection_signal present and descriptive → slight boost
    """
    vtype = finding.get("type", "")
    base = SIGNAL_CLARITY_BASELINE.get(vtype, 0.5)

    if finding.get("safe_poc"):
        base = min(1.0, base + 0.05)

    signal_desc = finding.get("detection_signal", "")
    if signal_desc and len(signal_desc) > 20:
        base = min(1.0, base + 0.03)

    return base


def score_corroboration(finding: dict) -> float:
    """Score whether multiple independent signals or tools agree.

    Factors:
      - multiple detection methods tried (from adaptive_metadata)
      - multiple replay attempts all matched
      - WAF was detected and bypassed (corroborates the vuln is real + defended)
      - finding is part of an attack path (corroborated by chain)
    """
    score = 0.0

    # Multiple replays all matched
    replay_results = finding.get("replay_results", [])
    if len(replay_results) >= 2 and all(r.get("signal_matched") for r in replay_results):
        score += 0.4

    # Adaptive metadata: alternative signals tried
    adaptive = finding.get("adaptive_metadata", {})
    if adaptive.get("mutations_tried", 0) > 0:
        score += 0.2
    if adaptive.get("waf_detected"):
        score += 0.2  # WAF presence corroborates vuln is real
    if adaptive.get("fallback_strategy"):
        score += 0.1

    # Part of attack path (corroborated by chain) — inferred if fingerprint exists
    if finding.get("fingerprint"):
        score += 0.1

    return min(1.0, score)


def compute_confidence(finding: dict) -> ConfidenceBreakdown:
    """Compute the multi-factor confidence score for a finding.

    Returns a ConfidenceBreakdown with all sub-scores and the aggregate.
    """
    es = score_evidence_strength(finding)
    rs = score_reproducibility(finding)
    sc = score_signal_clarity(finding)
    co = score_corroboration(finding)

    confidence = (
        WEIGHTS["evidence_strength"] * es
        + WEIGHTS["reproducibility"] * rs
        + WEIGHTS["signal_clarity"] * sc
        + WEIGHTS["corroboration"] * co
    )
    confidence = round(min(1.0, max(0.0, confidence)), 2)

    return ConfidenceBreakdown(
        evidence_strength=round(es, 2),
        reproducibility_score=round(rs, 2),
        signal_clarity=round(sc, 2),
        corroboration=round(co, 2),
        confidence=confidence,
        meets_threshold=confidence >= PROMOTION_THRESHOLD,
    )


def apply_confidence(finding: dict) -> dict:
    """Apply confidence scoring to a finding, returning an updated copy.

    Populates:
      - confidence (aggregate)
      - confidence_breakdown (sub-scores)
      - reproducibility_score
    Does NOT change finding.status — that is the validator's job. But sets
    a `meets_confidence_threshold` flag the validator can check.
    """
    out = json.loads(json.dumps(finding))  # deep copy
    breakdown = compute_confidence(out)
    out["confidence"] = breakdown.confidence
    out["confidence_breakdown"] = {
        "evidence_strength": breakdown.evidence_strength,
        "reproducibility_score": breakdown.reproducibility_score,
        "signal_clarity": breakdown.signal_clarity,
        "corroboration": breakdown.corroboration,
        "method": breakdown.method,
    }
    out["reproducibility_score"] = breakdown.reproducibility_score
    out["meets_confidence_threshold"] = breakdown.meets_threshold
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Confidence scoring system for findings")
    ap.add_argument("--finding", required=True, help="Finding JSON (path or '-')")
    args = ap.parse_args()

    finding = load_json(args.finding)
    scored = apply_confidence(finding)
    print(dump_json(scored))
    return 0


if __name__ == "__main__":
    sys.exit(main())
