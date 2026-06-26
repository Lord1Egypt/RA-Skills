# HAZOP Node Analysis Worksheet

**Platforms:** Claude · Openclaw · Codex
**Domain:** Process Safety

## Purpose

Walks a HAZOP (Hazard and Operability) team through one node of a process-hazard-analysis study aligned to **IEC 61882:2016** and the **CCPS Guidelines for Hazard Evaluation Procedures**. Captures the node's P&ID bounds, design intent, and operating envelope; applies the full guideword × parameter matrix (No / Less / More / Reverse / As Well As / Part Of / Other Than against Flow / Pressure / Temperature / Level / Composition / Phase / Reaction / Time / Sequence); records cause → consequence → existing-safeguard chains with prevention and mitigation barriers kept separate; assigns severity × likelihood on the facility risk matrix; flags any deviation whose residual risk warrants a follow-on LOPA / SIL study; and produces a DRAFT HAZOP worksheet, a recommendation register with single named owners, and a node-closure block for the HAZOP chair and process-safety responsible person's review.

## When to Use

- New unit, project, or major modification (OSHA PSM 1910.119(e) / EPA RMP / Seveso III pre-startup PHA)
- 5-year PHA revalidation cycle under OSHA PSM 1910.119(e)(6)
- Management of Change (MOC) trigger where the change rises to a PHA requirement
- Post-incident root-cause-driven re-study of a node
- Pre-startup HAZOP node walk-down ahead of a Pre-Startup Safety Review (PSSR)
- HAZOP refresh after a fired-heater / compressor / reactor / storage-tank retrofit
- HAZOP support for SIL determination and the LOPA hand-off

## What It Does

**Phase 1: Study Set-Up**
1. Captures facility, unit, P&ID set with revision dates, study scope IN / OUT, HAZOP chair / scribe / discipline-rep roster (process, operations, mechanical, instrumentation / controls, electrical, safety, environmental, maintenance), regulatory frame (OSHA PSM 1910.119 / EPA RMP 40 CFR 68 / Seveso III / MOC trigger / re-validation cycle), risk-matrix selection, and the LOPA-trigger criteria the facility uses

**Phase 2: Node Definition**
2. Defines one node at a time — node ID, P&ID reference, line / vessel / equipment bounds, normal and design operating envelope for flow / pressure / temperature / level / composition / phase, instrumentation, isolations, utility ties

**Phase 3: Design Intent**
3. States the node's design intent (function + target operating envelope) and cites the source-of-truth references (PFD, P&ID, datasheet, line list, cause-and-effect chart)

**Phase 4: Deviation Analysis**
4. Walks the full guideword × parameter matrix; for every credible deviation records cause, consequence (people, asset, environment, production, reputation — never collapsed into one), existing safeguards split into **prevention** and **mitigation** layers, and severity × likelihood on the facility risk matrix

**Phase 5: Recommendations and LOPA Referral**
5. Generates recommendations with action wording, single named owner, target date, recommendation type (design change / procedure / training / IPL / further study), and a LOPA-trigger flag when residual risk exceeds corporate tolerance

**Phase 6: Node Closure and Worksheet Assembly**
6. Produces a DRAFT HAZOP worksheet in the IEC 61882 column layout, a recommendation register, a deviations-not-credible log, a parking-lot list, and a chair / scribe / discipline review-and-sign-off block

## Output

A DRAFT HAZOP package with:
- HAZOP worksheet in the IEC 61882 column layout (Node, Parameter, Guideword, Deviation, Cause, Consequence, Existing Safeguards — Prevention, Existing Safeguards — Mitigation, Severity, Likelihood, Risk, Recommendation, Owner, Target Date, LOPA flag)
- Recommendation register with single named owners and target dates
- Deviations-not-credible log (records why the team eliminated a guideword × parameter combination)
- Parking-lot list (items raised but out of scope for the current node)
- Chair / scribe / discipline review-and-sign-off block
- Open-questions / unresolved-information list

## Notes

This skill **drafts** the HAZOP worksheet to support — never replace — the multidisciplinary HAZOP team's judgement, the HAZOP chair's sign-off, and the process-safety responsible person's adoption of recommendations. The skill does not finalise a PHA, does not sign the Pre-Startup Safety Review (PSSR), does not authorise start-up, does not perform LOPA / SIL determination (it only flags candidates for it), and does not perform Quantitative Risk Assessment (QRA). The skill keeps prevention and mitigation safeguards in separate columns, refuses to merge them, and refuses to lower severity to make a deviation "go away".

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
