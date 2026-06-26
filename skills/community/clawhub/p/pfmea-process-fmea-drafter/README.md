# PFMEA — Process Failure Mode and Effects Analysis Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Quality Engineering

## Purpose

Drafts a Process Failure Mode and Effects Analysis (PFMEA) aligned to the AIAG-VDA FMEA Handbook (2019, current 2026 edition) seven-step approach: planning and preparation, process structure analysis, function analysis, failure analysis, risk analysis, optimisation, and results documentation. The skill scores Severity, Occurrence, and Detection on the 1–10 scales and assigns the **Action Priority (AP)** rating — High / Medium / Low — that **replaces** the Risk Priority Number (RPN). The output is a DRAFT PFMEA worksheet plus an optimisation action plan and reanalysis-trigger list, structured for the cross-functional team's review before any control-plan update, PPAP package, customer Source-Inspection submission, or audit (IATF 16949 / AS9100 / 21 CFR 820 / customer-specific).

## When to Use

- Drafting a new PFMEA for a new product, new process, or process change before PPAP / FAI
- Updating a PFMEA after an OEM 8D corrective action, customer complaint, SCAR, audit finding, or recurring nonconformance
- Re-baselining a PFMEA on transfer from RPN-based templates to AIAG-VDA AP
- Preparing a PFMEA package for IATF 16949 / AS9100 / 21 CFR 820 surveillance or customer Source Inspection
- Pre-launch PSO / Run-at-Rate / Production Trial Run readiness review
- Triggering a focused reanalysis when one of the named triggers fires (design change, process change, supplier change, regulatory change, recurring field failure)

## What It Does

**Phase 1: Planning and Preparation**
1. Captures customer, programme, regulatory frame (IATF 16949 / AS9100 / 21 CFR 820 / MIL-STD-1629 / customer-specific format), prior PFMEA / DFMEA / control plan / process flow, cross-functional team roster (single named facilitator), scope IN / OUT, and PFMEA trigger
2. Confirms whether the customer mandates a specific PFMEA format (Ford FMEA-AP, GM, Stellantis, BMW, Daimler, VW Formel-Q, Volvo, JLR) and applies the customer's S / O / D tables when supplied

**Phase 2: Process Structure Analysis**
3. Decomposes the process into Process Item → Process Step → Process Work Element rows, classifying every work element by 4M / 6M category (Man, Machine, Material, Method, Measurement, Environment)

**Phase 3: Function Analysis**
4. Builds the three-tier function tree (Process-Item function, Process-Step function with the product characteristic it delivers, Process-Work-Element function with the process characteristic it controls)

**Phase 4: Failure Analysis**
5. Populates the failure chain row by row — Failure Effect (end customer / next process / plant), Failure Mode (at the process step), Failure Cause (at the process work element) — with each row tied to its function-tree node

**Phase 5: Risk Analysis**
6. Scores Severity (1–10 at the end customer, with safety / regulatory escalation), Occurrence (1–10 of the cause given current prevention control), and Detection (1–10 of the current detection control), identifying current prevention and current detection controls **separately**
7. Assigns the AIAG-VDA Action Priority (High / Medium / Low) per the AP look-up table — never an RPN, never a customer S × O × D threshold unless the customer mandates one

**Phase 6: Optimisation**
8. Drafts recommended preventive and detective actions for every High-AP row and (per management policy) every Medium-AP row, with a single named owner, target completion date, and effectiveness-verification method; re-scores S / O / D and AP after action verification

**Phase 7: Results Documentation**
9. Produces a DRAFT PFMEA worksheet, a Top-N High-AP action list, an optimisation action plan, a reanalysis-trigger list, and a cross-functional-team review-and-sign-off block

## Output

A DRAFT PFMEA package with:
- AIAG-VDA-format PFMEA worksheet (Structure / Function / Failure / Risk / Optimisation columns)
- Action Priority (AP) rating per row — never an RPN
- Top-N High-AP action list with single named owner and target date
- Optimisation action plan with effectiveness-verification method
- Reanalysis-trigger list (design change, process change, supplier change, tool change, gauge change, regulatory change, recurring field failure, customer concern, 8D linkage)
- Cross-functional-team review-and-sign-off block (Process Owner, Quality, Manufacturing / Industrial Engineering, Maintenance / Tooling, Supplier Quality where applicable, Safety / Regulatory where applicable)
- Open-questions / unresolved-information list

## Notes

This skill **drafts** the PFMEA to support — never replace — the cross-functional team's judgement and the responsible engineer's sign-off. The skill does not finalise a PFMEA, does not sign or submit PPAP, does not authorise production, does not opine on customer-specific Source-Inspection waivers, and does not commit to corrective action without explicit owner confirmation. When the customer mandates a specific format (Ford FMEA-AP, GM, Stellantis, BMW Group, Daimler / Mercedes-Benz, VW Formel-Q, Volvo Group, JLR), the skill applies the customer's S / O / D tables and column layout. The skill refuses to substitute RPN for AP when the AIAG-VDA Handbook applies, and refuses to silently drop the Action Priority field on customer-template requests — it surfaces the conflict for the engineer's resolution.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
