"""Postmarket-surveillance judge.

Domain: postmarket-surveillance

Takes a reported adverse-event / recall event and returns an action-level
verdict (reject=Class 1 style immediate field safety notice; hold=Class 2
field correction; go=Class 3 / record-and-continue).

Rules grounded in VERIFIED recall records:
  - P2-CASE-MAJ-01..04  (FDA Class 1 recalls: process/material/design)
  - B1-C02 Dexcom CGM App (Class 1 missed sensor-failed alert)
  - B1-C08 Baxter Spectrum IQ (Class 1 software design, infusion safety)
  - B1-C05 Blue Ortho Predict+ (Class 2, no marketing application)
  - B1-C07 Butterfly iQ Auto EF (Class 2, no marketing application, AI feature)
  - B1-C09 Change Healthcare Hemo (Class 2, software autosave defect)
  - B1-C12 Siemens NAEOTOM AI (Class 2, AI feature removed from deployed devices)
  - B1-C14 Hologic Genius (Class 2, user tampered validated config)
  - B1-C04 Philips Pinnacle3 (NMPA Class 3, SPR calculation error)
  - B1-C11 Elekta MOSAIQ (NMPA Class 3, image offset calc)

Input ctx schema:
{
  "recall_class":        "none" | "class1" | "class2" | "class3",
  "fda_cause_type":      "software_design" | "process_change_control" |
                         "nonconforming_material" | "device_design" |
                         "no_marketing_application" | "user_config_tampering" |
                         "under_investigation" | "other",
  "harm_severity":       "no_harm" | "temporary_reversible" |
                         "serious_injury" | "death",
  "distribution_scope":  "limited_local" | "us_national" | "global",
  "event_report_count":  int,
  "marketing_without_license": bool,
  "source_refs": [{"kind": str, "ref": str}],
}
"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Reason, Evidence


_CRITICAL = [
    {
        "rule": "PM-CRIT-01-class1-recall",
        "detail": "FDA/NMPA Class 1 recall: reasonable probability of serious "
                  "injury or death. Mandatory urgent field safety notice; "
                  "quarantine affected lots.",
        "when": lambda c: c.get("recall_class") == "class1",
    },
    {
        "rule": "PM-CRIT-02-unlicensed-on-market",
        "detail": "Product/feature on US/EU market without premarket clearance "
                  "or PMA (No Marketing Application). Immediate removal from "
                  "distribution; cannot operate until gate passes.",
        "when": lambda c: bool(c.get("marketing_without_license")),
    },
    {
        "rule": "PM-CRIT-03-death-or-serious-causal",
        "detail": "Death or serious injury reported and plausibly caused by "
                  "device software/design/material root cause — opens root-cause "
                  "CAPA and regulator notification.",
        "when": lambda c: (
            c.get("harm_severity") in {"serious_injury", "death"}
            and c.get("fda_cause_type") in {
                "software_design", "device_design", "nonconforming_material",
                "process_change_control",
            }
        ),
    },
]

_MAJOR = [
    {
        "rule": "PM-MAJ-01-class2-recall",
        "detail": "Class 2 / NMPA 二级 recall: temporary or medically reversible "
                  "health consequence. Field correction + enhanced monitoring + "
                  "CAPA within agreed timeline.",
        "when": lambda c: c.get("recall_class") == "class2",
    },
    {
        "rule": "PM-MAJ-02-user-config-deviation",
        "detail": "Deployed unit found operating outside its FDA-validated "
                  "configuration (user tampering). Re-seat to validated config "
                  "and audit access controls.",
        "when": lambda c: c.get("fda_cause_type") == "user_config_tampering",
    },
    {
        "rule": "PM-MAJ-03-high-report-volume",
        "detail": "Adverse-event report volume exceeds the watch threshold for "
                  "this device code — open trending review even if no recall yet.",
        "when": lambda c: int(c.get("event_report_count", 0) or 0) >= 25,
    },
]

_MINOR = [
    {
        "rule": "PM-MIN-01-class3-record",
        "detail": "Class 3 / NMPA 三级 recall: unlikely adverse health "
                  "consequence. Log, communicate, no product return.",
        "when": lambda c: c.get("recall_class") == "class3",
    },
]


class JudgePostmarket:
    domain = "postmarket-surveillance"

    def evaluate(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        reasons: List[Reason] = []
        evidence: List[Evidence] = []
        for e in ctx.get("source_refs", []) or []:
            evidence.append(Evidence(kind=e.get("kind", "unspecified"),
                                    ref=e.get("ref", "")))

        crit = False
        for rule in _CRITICAL:
            try:
                if rule["when"](ctx):
                    reasons.append(Reason(rule=rule["rule"], level="critical",
                                          detail=rule["detail"]))
                    crit = True
            except Exception:
                pass

        if crit:
            verdict = "reject"
        else:
            maj = False
            for rule in _MAJOR:
                try:
                    if rule["when"](ctx):
                        reasons.append(Reason(rule=rule["rule"], level="major",
                                              detail=rule["detail"]))
                        maj = True
                except Exception:
                    pass
            if maj:
                verdict = "hold"
            else:
                for rule in _MINOR:
                    try:
                        if rule["when"](ctx):
                            reasons.append(Reason(rule=rule["rule"], level="minor",
                                                  detail=rule["detail"]))
                    except Exception:
                        pass
                # default: if no recall at all, still require evidence per L2
                verdict = "go" if evidence else "hold"

        if verdict == "go" and not evidence:
            reasons.append(Reason(
                rule="L2-EVIDENCED", level="critical",
                detail="postmarket go with zero evidence refs — L2 law downgrades.",
            ))
            verdict = "hold"

        return {
            "verdict": verdict,
            "reasons": [{"rule": r.rule, "level": r.level, "detail": r.detail}
                        for r in reasons],
            "evidence": [{"kind": e.kind, "ref": e.ref} for e in evidence],
        }


__all__ = ["JudgePostmarket"]
