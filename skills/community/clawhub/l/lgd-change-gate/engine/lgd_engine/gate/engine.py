"""GateEngine: aggregate domain-judge verdicts into one GateReport.

- Runs each registered DomainJudge against the same ctx.
- Honors L3-GATED: any critical reason → final verdict = reject.
- Honors L2-EVIDENCED: go verdict with no evidence across all judges → hold.
- Honors L1-RECORDED: caller (CLI/web) is expected to persist via LocalMemory;
  engine itself does not write (keeps it pure & testable).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from ..judges.base import DomainJudge, JudgeVerdict


@dataclass
class GateReport:
    verdict: str                          # go | hold | reject
    per_judge: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    reasons: List[Dict[str, str]] = field(default_factory=list)
    evidence: List[Dict[str, str]] = field(default_factory=list)
    law_enforcements: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "per_judge": self.per_judge,
            "reasons": self.reasons,
            "evidence": self.evidence,
            "law_enforcements": self.law_enforcements,
        }

    def pretty(self) -> str:
        """Human-readable gate report for CLI."""
        lines = []
        badge = {"go": "✅ GO", "hold": "🟡 HOLD", "reject": "🔴 REJECT"}[self.verdict]
        lines.append("=" * 60)
        lines.append(f"GATE VERDICT: {badge}")
        lines.append("=" * 60)
        if self.law_enforcements:
            lines.append("[LGD law enforcements]")
            for e in self.law_enforcements:
                lines.append(f"  - {e}")
            lines.append("")
        lines.append("[Per-judge verdicts]")
        for dom, v in self.per_judge.items():
            lines.append(f"  · {dom}: {v['verdict'].upper()}  "
                         f"({len(v['reasons'])} reasons, {len(v['evidence'])} evidence)")
        lines.append("")
        lines.append("[Reason chain]")
        for r in self.reasons:
            lines.append(f"  [{r['level'].upper():8}] {r['rule']}")
            lines.append(f"            {r['detail']}")
        lines.append("")
        lines.append("[Evidence cited]")
        if not self.evidence:
            lines.append("  (none)")
        for e in self.evidence:
            lines.append(f"  - ({e['kind']}) {e['ref']}")
        lines.append("=" * 60)
        return "\n".join(lines)


class GateEngine:
    """Aggregates N DomainJudge instances into one GateReport."""

    def __init__(self, judges: List[DomainJudge] | None = None) -> None:
        self.judges: List[DomainJudge] = list(judges or [])

    def register(self, judge: DomainJudge) -> None:
        self.judges.append(judge)

    # ------------------------------------------------------------------ run
    def evaluate(self, ctx: Dict[str, Any]) -> GateReport:
        per_judge: Dict[str, Dict[str, Any]] = {}
        all_reasons: List[Dict[str, str]] = []
        all_evidence: List[Dict[str, str]] = []
        law_hits: List[str] = []

        any_critical = False
        any_hold = False
        any_go = False

        for j in self.judges:
            dom = getattr(j, "domain", j.__class__.__name__)
            try:
                v = j.evaluate(ctx)
            except Exception as exc:
                # judge itself crashing is a critical failure
                v = {
                    "verdict": "reject",
                    "reasons": [{"rule": f"{dom}.exception",
                                 "level": "critical",
                                 "detail": f"judge raised: {exc!r}"}],
                    "evidence": [],
                }
            per_judge[dom] = v

            for r in v.get("reasons", []):
                all_reasons.append(r)
                if r["level"] == "critical":
                    any_critical = True
                elif r["level"] == "major":
                    any_hold = True
                # L2 downgrade is a hold signal regardless of how the judge tags
                # it; detect by rule name, not by level (LGD-EVAL-2026-009 H1).
                if r["rule"] == "L2-EVIDENCED":
                    law_hits.append("L2-EVIDENCED: go-without-evidence downgraded")

            for e in v.get("evidence", []):
                all_evidence.append(e)

            if v["verdict"] == "reject":
                any_critical = True
            elif v["verdict"] == "hold":
                any_hold = True
            elif v["verdict"] == "go":
                any_go = True

        # ---- L3-GATED: any critical → reject ----
        if any_critical:
            final = "reject"
            # dedup
            if "L3-GATED: critical veto forced reject" not in law_hits:
                law_hits.append("L3-GATED: at least one critical rule fired → forced reject")
        elif any_hold:
            final = "hold"
        elif any_go:
            # ---- L2-EVIDENCED at aggregate level ----
            if not all_evidence:
                final = "hold"
                law_hits.append("L2-EVIDENCED: aggregate go with zero evidence → hold")
            else:
                final = "go"
        else:
            final = "hold"  # no judges ran — safe default

        return GateReport(
            verdict=final,
            per_judge=per_judge,
            reasons=all_reasons,
            evidence=all_evidence,
            law_enforcements=law_hits,
        )
