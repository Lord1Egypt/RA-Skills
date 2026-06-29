"""
venture_council_gate.py — Mandatory council review for all ORA ventures and campaigns.

Every campaign draft, venture brief, and content revision must pass through this
gate before reaching the operator's approval queue. This is structural, not opt-in.

PUBLIC API
----------
run_campaign_gate(brief, venture_key)     → GateResult
    Runs strategy + content + market + risk councils on a campaign brief.
    Returns go/hold/kill verdict + per-council notes + synthesis.

run_content_gate(copy_text, venture_key)  → GateResult
    Lighter content-only pass: content + ethics councils.
    Used on revision cycles so operator edits always get a sanity check.

run_venture_gate(venture_idea, venture_key) → GateResult
    Full multi-council pass for new venture proposals (Tier 3+).
    Runs all eight Business Mind Tree councils and returns go/hold/kill.

GateResult fields
-----------------
    ok:         bool
    verdict:    "go" | "hold" | "kill"
    confidence: float (0–1)
    councils:   list[dict]   each council's raw output
    synthesis:  str          combined recommendation paragraph
    flags:      list[str]    specific items needing operator attention
    cost_usd:   float        approximate council call cost
"""
from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Optional

_log = logging.getLogger("venture_council_gate")

# ── safe imports ─────────────────────────────────────────────────────────────

try:
    from business_mind_tree import (  # type: ignore
        strategy_council, content_council, risk_council, market_council,
        operations_council, ethics_council, forecasting_council, execution_council,
        multi_council,
    )
    _MIND_TREE_OK = True
except Exception as _e:
    _MIND_TREE_OK = False
    _log.warning(f"business_mind_tree unavailable: {_e}")

try:
    from council_chat import chat_with_council  # type: ignore
    _COUNCIL_CHAT_OK = True
except Exception as _e:
    _COUNCIL_CHAT_OK = False
    _log.warning(f"council_chat unavailable: {_e}")

# ── cost logging (R5) ────────────────────────────────────────────────────────

def _log_gate_cost(venture_key: str, gate_type: str, cost_usd: float) -> None:
    try:
        from pathlib import Path
        cost_log = Path(__file__).resolve().parent / "cost_log.json"
        try:
            existing = json.loads(cost_log.read_text()) if cost_log.exists() else []
        except Exception:
            existing = []
        existing.append({
            "ts":          time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "service":     "venture_council_gate",
            "gate_type":   gate_type,
            "venture_key": venture_key,
            "cost_usd":    round(cost_usd, 6),
            "model":       "multi-council",
        })
        cost_log.write_text(json.dumps(existing[-500:], indent=2))
    except Exception as exc:
        _log.warning(f"cost log failed (non-fatal): {exc}")


# ── result dataclass ─────────────────────────────────────────────────────────

@dataclass
class GateResult:
    ok:         bool
    verdict:    str          # "go" | "hold" | "kill"
    confidence: float        # 0.0–1.0
    councils:   list[dict]   = field(default_factory=list)
    synthesis:  str          = ""
    flags:      list[str]    = field(default_factory=list)
    cost_usd:   float        = 0.0
    gate_type:  str          = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok":         self.ok,
            "verdict":    self.verdict,
            "confidence": self.confidence,
            "councils":   self.councils,
            "synthesis":  self.synthesis,
            "flags":      self.flags,
            "cost_usd":   self.cost_usd,
            "gate_type":  self.gate_type,
        }


def _fallback_result(gate_type: str, reason: str) -> GateResult:
    """Return when councils are unavailable — defaults to 'hold' so nothing slips through."""
    _log.warning(f"Council gate falling back to hold: {reason}")
    return GateResult(
        ok=False,
        verdict="hold",
        confidence=0.0,
        synthesis=f"Council unavailable ({reason}). Operator review required before proceeding.",
        flags=["councils_unavailable"],
        gate_type=gate_type,
    )


# ── verdict extraction ────────────────────────────────────────────────────────

def _synthesis_to_text(synthesis: Any) -> str:
    """multi_council() returns "synthesis" as a dict (consensus_recommendation,
    all_findings, all_concerns, ...), not a string — render it to readable text
    so GateResult.synthesis (typed str) never ends up holding a raw dict."""
    if isinstance(synthesis, str):
        return synthesis
    if isinstance(synthesis, dict):
        parts = []
        consensus = synthesis.get("consensus_recommendation")
        if consensus:
            parts.append(f"Consensus: {consensus}")
        for f in (synthesis.get("all_findings") or [])[:5]:
            parts.append(f"- {f}")
        for c in (synthesis.get("all_concerns") or [])[:5]:
            parts.append(f"! {c}")
        return "\n".join(parts) if parts else "No synthesis available."
    return "No synthesis available."


def _extract_verdict(council_outputs: list[dict]) -> tuple[str, float, list[str]]:
    """Derive go/hold/kill from aggregated council outputs.

    Each council returns {"recommendation": "go"|"hold"|"kill", "confidence": 0–1, ...}.
    Majority rules; any kill from risk or ethics council overrides.
    """
    votes: dict[str, int] = {"go": 0, "hold": 0, "kill": 0}
    confidences: list[float] = []
    flags: list[str] = []
    hard_kill = False

    for c in council_outputs:
        if not isinstance(c, dict):
            continue
        rec = str(c.get("recommendation", "hold")).lower()
        # Normalize variations
        if rec in ("proceed", "approve", "launch", "yes"):
            rec = "go"
        elif rec in ("stop", "reject", "no", "do not", "don't"):
            rec = "kill"
        elif rec not in ("go", "hold", "kill"):
            rec = "hold"

        # Risk and ethics councils have veto power
        council_name = c.get("council", "")
        if council_name in ("risk", "ethics") and rec == "kill":
            hard_kill = True
            flags.append(f"VETO from {council_name} council")

        votes[rec] = votes.get(rec, 0) + 1
        conf = float(c.get("confidence", 0.7))
        confidences.append(min(max(conf, 0.0), 1.0))

        # Surface explicit flags/concerns from council
        concerns = c.get("risks_or_concerns") or c.get("concerns") or c.get("risks") or []
        if isinstance(concerns, list):
            for concern in concerns[:2]:
                if concern:
                    flags.append(f"[{council_name}] {str(concern)[:120]}")

    if hard_kill:
        verdict = "kill"
    elif votes["kill"] > votes["go"]:
        verdict = "kill"
    elif votes["go"] >= votes["hold"] and votes["go"] > votes["kill"]:
        verdict = "go"
    else:
        verdict = "hold"

    avg_conf = sum(confidences) / len(confidences) if confidences else 0.5
    return verdict, avg_conf, flags[:8]


# ── public gate functions ─────────────────────────────────────────────────────

def run_campaign_gate(
    brief:       Any,
    venture_key: str = "united_tax_pros",
) -> GateResult:
    """Run strategy + content + market + risk councils on a campaign brief.

    Called automatically on every new campaign draft and on every approval.
    Operator sees the synthesis in the approval queue before clicking Approve.
    """
    if not _MIND_TREE_OK:
        return _fallback_result("campaign", "business_mind_tree not imported")

    prompt = (
        f"Venture: {venture_key}\n\n"
        f"Campaign brief:\n{json.dumps(brief, indent=2)[:2000]}"
    )

    council_names = ["strategy", "content", "market", "risk"]
    result = multi_council(prompt, councils=council_names)

    council_outputs = []
    total_cost = 0.0
    synthesis_parts = []

    individual = result.get("results") or []
    for c in individual:
        council_outputs.append(c)
        total_cost += float(c.get("cost_usd", 0))
        # Pull recommendation text for synthesis
        rec_text = (c.get("recommendation_text") or c.get("reasoning") or "")[:300]
        if rec_text:
            synthesis_parts.append(f"[{c.get('council','?')}] {rec_text}")

    synthesis = _synthesis_to_text(result.get("synthesis")) or "\n".join(synthesis_parts) or "No synthesis available."
    verdict, confidence, flags = _extract_verdict(council_outputs)

    _log_gate_cost(venture_key, "campaign", total_cost)
    _log.info(f"campaign gate: venture={venture_key} verdict={verdict} conf={confidence:.2f}")

    return GateResult(
        ok=verdict in ("go", "hold"),
        verdict=verdict,
        confidence=confidence,
        councils=council_outputs,
        synthesis=synthesis,
        flags=flags,
        cost_usd=total_cost,
        gate_type="campaign",
    )


def run_content_gate(
    copy_text:   str,
    venture_key: str = "united_tax_pros",
) -> GateResult:
    """Content + ethics council check on copy/revisions.

    Lighter than run_campaign_gate — runs on every operator edit so that
    revisions don't accidentally introduce non-compliant claims (Rule R8)
    or off-brand voice.
    """
    if not _MIND_TREE_OK:
        return _fallback_result("content", "business_mind_tree not imported")

    prompt = (
        f"Venture: {venture_key}\n\n"
        f"Review this content for brand voice, accuracy, compliance "
        f"(no guaranteed outcomes, no IRS-approval claims, no specific dollar "
        f"promises per Rule R8), and ethical marketing:\n\n{copy_text[:2500]}"
    )

    council_names = ["content", "ethics"]
    result = multi_council(prompt, councils=council_names)

    council_outputs = result.get("results") or []
    total_cost = sum(float(c.get("cost_usd", 0)) for c in council_outputs)
    synthesis = _synthesis_to_text(result.get("synthesis"))

    verdict, confidence, flags = _extract_verdict(council_outputs)

    _log_gate_cost(venture_key, "content", total_cost)
    _log.info(f"content gate: venture={venture_key} verdict={verdict}")

    return GateResult(
        ok=verdict != "kill",
        verdict=verdict,
        confidence=confidence,
        councils=council_outputs,
        synthesis=synthesis,
        flags=flags,
        cost_usd=total_cost,
        gate_type="content",
    )


def run_venture_gate(
    venture_idea: str,
    venture_key:  str = "",
) -> GateResult:
    """Full eight-council Business Mind Tree pass for new venture proposals.

    Called when scaffolding a new venture (Tier 3+). Returns a go/hold/kill
    with full reasoning from every council seat. Operator sees this before
    any build work starts on the new venture.
    """
    if not _MIND_TREE_OK:
        return _fallback_result("venture", "business_mind_tree not imported")

    prompt = (
        f"New venture proposal for evaluation:\n\n{venture_idea}\n\n"
        f"Evaluate from your council seat: is this worth pursuing? "
        f"What are the critical success factors and fatal risks? "
        f"Return: recommendation (go/hold/kill), confidence (0–1), "
        f"key concerns list, and your reasoning."
    )

    all_councils = ["strategy", "content", "market", "risk",
                    "operations", "ethics", "forecasting", "execution"]
    result = multi_council(prompt, councils=all_councils)

    council_outputs = result.get("results") or []
    total_cost = sum(float(c.get("cost_usd", 0)) for c in council_outputs)
    synthesis = _synthesis_to_text(result.get("synthesis"))

    verdict, confidence, flags = _extract_verdict(council_outputs)

    _log_gate_cost(venture_key or "new_venture", "venture", total_cost)
    _log.info(f"venture gate: verdict={verdict} conf={confidence:.2f} venture={venture_key}")

    return GateResult(
        ok=verdict in ("go", "hold"),
        verdict=verdict,
        confidence=confidence,
        councils=council_outputs,
        synthesis=synthesis,
        flags=flags,
        cost_usd=total_cost,
        gate_type="venture",
    )


def gate_summary_for_approval(gate: GateResult) -> str:
    """Format a GateResult as a compact string for the approval queue edit log."""
    emoji = {"go": "✅", "hold": "⚠️", "kill": "🛑"}.get(gate.verdict, "?")
    lines = [
        f"{emoji} Council gate [{gate.gate_type}]: {gate.verdict.upper()} "
        f"(confidence {gate.confidence:.0%})",
    ]
    if gate.synthesis:
        lines.append(gate.synthesis[:400])
    if gate.flags:
        lines.append("Flags: " + "; ".join(gate.flags[:4]))
    return "\n".join(lines)
