"""510(k) change-classification judge.

Domain: 510k-change-classification

Rules distilled from P2 判例分级样本集 (10 VERIFIED FDA/NMPA cases, 2026-11-03).
Input ctx schema (all fields optional but recommended):
{
  "device_risk_class": "I" | "II" | "III",
  "regulatory_path":   "510k" | "pma" | "nmpa_import",
  "jurisdiction":      "FDA" | "NMPA"   # default "FDA"
  "change_type":       "label_correction" | "label_clarification" |
                      "label_expansion" | "function_config_change" |
                      "process_change_control" | "material_nonconforming" |
                      "design_defect" | "maintenance_execution" |
                      "supplier_substitution",
  "safety_impact":     "none" | "limited_reversible" | "severe_life_threatening",
  "evidence_sufficiency": "sufficient" | "needs_supplement" | "none",
  "recall_class":      "none" | "class1" | "class2" | "class3",
  "requires_submission": bool,     # needs new 510(k) / PMA supplement
  "predicate_unchanged": bool,     # intended use & predicate tech unchanged
  "equivalence_declared": bool,     # NMPA: supplier/material equivalence filed
  "device_description": str,        # free text, used for FTS/LIKE memory recall
  "source_refs": [{"kind": str, "ref": str}],  # external evidence
}

Jurisdiction notes (bound to public regulatory facts; see
framework/eco-regulatory-matrix.md):
  - FDA: 21 CFR 807.81(a) — "significant change in specifications/design/
    materials/energy source/performance" requires new 510(k). Conservative:
    material/process/design changes default to submission.
  - NMPA: 《医疗器械注册与备案管理办法》(NMPA 2021 年第 47 号公告) —
    changes affecting safety/effectiveness require 变更注册; administrative
    (登记事项) changes with equivalence evidence may be self-declared.
    Threshold is materially narrower than FDA 807.81 for supplier swaps.
"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import DomainJudge, JudgeVerdict, Reason, Evidence


# ----- rule tables, distilled from the 10 verified cases ------------------

# Critical veto rules (one vote → reject). Each fires independently.
_CRITICAL_RULES = [
    {
        "rule": "R-CRIT-01-class1-recall",
        "detail": "FDA/NMPA Class 1 recall: reasonable probability of serious "
                  "injury or death. Veto.",
        "when": lambda c: c.get("recall_class") == "class1",
    },
    {
        "rule": "R-CRIT-02-pma-process-uncontrolled",
        "detail": "PMA-listed device with uncontrolled process change — correct "
                  "path is PMA supplement with reliability validation. Veto.",
        "when": lambda c: (
            c.get("regulatory_path") == "pma"
            and c.get("change_type") == "process_change_control"
        ),
    },
    {
        "rule": "R-CRIT-03-severe-harm-rootcause",
        "detail": "Severe / life-threatening impact tied to material, design or "
                  "process root cause — gate failure has already produced (or can "
                  "produce) serious injury. Veto.",
        "when": lambda c: (
            c.get("safety_impact") == "severe_life_threatening"
            and c.get("change_type") in {
                "material_nonconforming", "design_defect", "process_change_control",
            }
        ),
    },
]

# Major rules (escalate → hold) when no critical fired.
_MAJOR_RULES = [
    {
        "rule": "R-MAJ-01-needs-submission",
        "detail": "Change requires a new 510(k) / Special 510(k) / Traditional "
                  "510(k) submission before transition — conditional hold pending "
                  "FDA clearance.",
        "when": lambda c: bool(c.get("requires_submission")),
    },
    {
        "rule": "R-MAJ-02-nmpa-class2-maintenance",
        "detail": "NMPA Class II recall tied to maintenance/process execution — "
                  "reversible but requires corrective action plan + enhanced "
                  "monitoring.",
        "when": lambda c: (
            c.get("recall_class") == "class2"
            and c.get("change_type") == "maintenance_execution"
        ),
    },
    {
        "rule": "R-MAJ-03-evidence-incomplete",
        "detail": "Evidence package incomplete — must supplement verification "
                  "data (e.g. freeze-thaw study, V&V report) before go.",
        "when": lambda c: c.get("evidence_sufficiency") == "needs_supplement",
    },
    {
        "rule": "R-MAJ-04-config-change-same-platform",
        "detail": "Functional configuration change on an existing tech platform "
                  "(feature add/remove) — hold pending 510(k) equivalence review.",
        "when": lambda c: (
            c.get("change_type") == "function_config_change"
            and c.get("predicate_unchanged", True)
        ),
    },
]

# Minor / green-path rules (log only; default go).
_MINOR_RULES = [
    {
        "rule": "R-MIN-01-label-only-no-harm",
        "detail": "Label / document correction only; no safety impact; no product "
                  "recall or Class 3 at most. Record-and-go.",
        "when": lambda c: (
            c.get("change_type") in {"label_correction", "label_clarification"}
            and c.get("safety_impact") == "none"
            and c.get("recall_class") in {"none", "class3"}
        ),
    },
]


class Judge510kChange:
    """DomainJudge adapter for 510(k) change-classification.

    Instantiate and pass into GateEngine, or call .evaluate(ctx) directly.
    """

    domain = "510k-change-classification"

    # Friendly public handle, used by CLI / web layer.
    def evaluate(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        reasons: List[Reason] = []
        evidence: List[Evidence] = []

        # External evidence refs passed in.
        for e in ctx.get("source_refs", []) or []:
            evidence.append(Evidence(kind=e.get("kind", "unspecified"),
                                     ref=e.get("ref", "")))

        # 1) critical vetoes
        crit_fired = []
        for rule in _CRITICAL_RULES:
            try:
                if rule["when"](ctx):
                    crit_fired.append(rule)
                    reasons.append(Reason(rule=rule["rule"], level="critical",
                                          detail=rule["detail"]))
            except Exception:
                # predicate errors are themselves a hold signal
                reasons.append(Reason(
                    rule=rule["rule"], level="major",
                    detail=f"rule predicate raised on ctx keys: {list(ctx.keys())}",
                ))

        verdict = "go"

        if crit_fired:
            verdict = "reject"
        else:
            # 2) major escalations
            maj_fired = []
            for rule in _MAJOR_RULES:
                try:
                    if rule["when"](ctx):
                        maj_fired.append(rule)
                        reasons.append(Reason(rule=rule["rule"], level="major",
                                              detail=rule["detail"]))
                except Exception as exc:  # pragma: no cover - defensive
                    reasons.append(Reason(rule=rule["rule"], level="minor",
                                          detail=f"predicate error: {exc}"))
            if maj_fired:
                verdict = "hold"
            else:
                # 3) minor / green
                for rule in _MINOR_RULES:
                    try:
                        if rule["when"](ctx):
                            reasons.append(Reason(rule=rule["rule"], level="minor",
                                                 detail=rule["detail"]))
                    except Exception:
                        pass
                # default stays go
                verdict = "go"

        # L2-EVIDENCED: if verdict says go but there is zero evidence, downgrade.
        # NOTE: this is a hold signal (major), NOT a critical veto — a missing
        # evidence package must never flip a verdict to reject (red-team fix
        # 2026-11-03: LGD-EVAL-2026-009 H1).
        if verdict == "go" and not evidence:
            reasons.append(Reason(
                rule="L2-EVIDENCED", level="major",
                detail="go verdict with zero evidence refs — LGD L2 law downgrades "
                       "to hold pending documented evidence.",
            ))
            verdict = "hold"

        # R-MAJ-05: supplier substitution without a filed equivalence declaration
        # is never self-declarable — hold pending equivalence evidence (FDA 807.81
        # and NMPA 登记事项 routes both require the declaration). Non-boolean
        # truthy values (e.g. the string "yes") count as no declaration.
        if (
            ctx.get("change_type") == "supplier_substitution"
            and ctx.get("equivalence_declared") is not True
        ):
            reasons.append(Reason(
                rule="R-MAJ-05-supplier-no-equivalence",
                level="major",
                detail="Supplier substitution without a filed equivalence "
                       "declaration — hold pending equivalence evidence "
                       "(both FDA 807.81 and NMPA 登记事项 routes require it).",
            ))
            verdict = "hold"

        # ---- jurisdiction-specific override (⑭) ----
        jur = (ctx.get("jurisdiction") or "FDA").strip().upper()
        if jur not in {"FDA", "NMPA"}:
            reasons.append(Reason(
                rule="R-JUR-UNKNOWN", level="major",
                detail=f"Unknown jurisdiction '{ctx.get('jurisdiction')}' — "
                       "conservative hold pending jurisdiction routing.",
            ))
            verdict = "hold"
        elif jur == "NMPA" and not any(r.level in ("critical", "major") for r in reasons):
            # NMPA 登记事项变更: equivalent supplier substitution with full
            # validation evidence may be self-declared (no 变更注册 needed),
            # whereas FDA 807.81 would still expect a 510(k).
            if (
                ctx.get("change_type") == "supplier_substitution"
                and ctx.get("evidence_sufficiency") == "sufficient"
                and ctx.get("equivalence_declared") is True
            ):
                reasons.append(Reason(
                    rule="R-JUR-NMPA-01-supplier-equivalence-self-declared",
                    level="minor",
                    detail="NMPA: supplier substitution with equivalent-material "
                           "declaration + validation evidence falls under 登记"
                           "事项变更 (self-declared); no 变更注册 required. "
                           "Downgraded from FDA hold to go.",
                ))
                verdict = "go"
        elif jur == "FDA" and verdict == "go":
            # FDA 807.81 conservative: material/supplier change even with
            # equivalence data still requires 510(k) submission.
            if ctx.get("change_type") == "supplier_substitution":
                reasons.append(Reason(
                    rule="R-JUR-FDA-01-80781-material-change",
                    level="major",
                    detail="FDA 21 CFR 807.81(a): change in materials/specs "
                           "is presumptively significant; new 510(k) required "
                           "even with equivalence data.",
                ))
                verdict = "hold"

        v = JudgeVerdict(verdict=verdict, reasons=reasons, evidence=evidence)
        return v.to_dict()


__all__ = ["Judge510kChange"]
