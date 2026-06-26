# Medication Therapy Review

**Platforms:** Claude · Openclaw · Codex
**Domain:** Pharmacy

## Purpose

Conducts a pharmacist-led Comprehensive Medication Review (CMR) for a single patient and produces a structured DRAFT Medication Action Plan (MAP), Personal Medication List (PML), and prescriber communication letter. Covers reconciliation, drug-therapy problem (DTP) identification, Beers / STOPP-START screening, renal- and hepatic-dose review, drug-drug interaction triage, adherence diagnosis, and deprescribing taper plans.

**The output is always DRAFT.** A licensed pharmacist must verify every drug name, dose, indication, interaction call, and recommendation before any prescriber communication, dispense decision, or change to therapy.

## When to Use

- Annual Medicare Part D MTM Comprehensive Medication Review (CMR)
- Polypharmacy review for an older adult (typically 5+ chronic medications)
- Post-discharge medication reconciliation and follow-up review
- Pre-clinic visit deprescribing review for a frail or long-term-care patient
- Drug-therapy problem workup before a pharmacist-prescriber consult or collaborative practice agreement (CPA) visit
- Pharmacy-resident or APPE student structured CMR practice with preceptor review

## What It Does

**Phase 1: Intake and Reconciliation**
1. Collects patient demographics (age, sex, weight, pregnancy/lactation status when relevant), allergies, key conditions with indications
2. Collects a complete medication list — prescription, OTC, herbals, supplements, PRN, recently stopped — with dose, route, frequency, duration, and prescriber
3. Collects clinical context — labs (SCr, eGFR, A1c, INR, K, LFTs, TSH as relevant), vitals, recent hospitalizations, social history (alcohol, tobacco, falls, cognition), goals of care
4. Reconciles the list into a single table with indication mapping, flagging unindicated drugs and undiagnosed/untreated indications

**Phase 2: Clinical Analysis**
5. Screens every medication against age-appropriate criteria (Beers for adults ≥65 in the US; STOPP/START for an alternative European framework)
6. Identifies drug-therapy problems using the seven-DTP framework (indication, effectiveness, safety, adherence)
7. Runs a drug-drug, drug-disease, and drug-food/lab interaction pass with severity tiering
8. Performs renal-dose and hepatic-dose review for every medication where dosing depends on organ function
9. Diagnoses adherence root cause (cost, complexity, side effects, beliefs, access, cognition) before recommending interventions

**Phase 3: Plan and Communicate**
10. Produces a Medication Action Plan with patient-friendly language at ~6th-grade reading level
11. Drafts deprescribing taper plans for each candidate (taper schedule, monitoring, withdrawal-symptom plan, restart-trigger)
12. Drafts a prescriber communication letter using the SBAR structure with a single specific ask per recommendation
13. Produces a Personal Medication List the patient can carry
14. Lists unresolved-information items, open clinical questions, and items that exceed pharmacist scope and require prescriber input

## Output

A DRAFT CMR packet with: reconciled medication table, indication-mapping table, drug-therapy-problem list (severity-rated), Beers / STOPP-START flag table, drug-drug interaction table, renal/hepatic dose-adjustment table, deprescribing candidate table with taper plans, Personal Medication List, Medication Action Plan, prescriber SBAR letter, and an unresolved-information list — all clearly labeled DRAFT, for licensed-pharmacist review.

## Notes

This skill never determines a final therapy plan, never directly contacts a prescriber, and never instructs a patient to change therapy on its own authority. It identifies candidates, classifies their risk, and writes structured DRAFT communications. The pharmacist owns every clinical decision.

It defaults to the 2023 AGS Beers Criteria for US patients ≥65 and STOPP/START v3 when the user requests a European framework or the patient is outside the US. It uses Cockcroft-Gault for renal dosing unless the user specifies CKD-EPI or measured CrCl. It treats every PHI element as confidential — patient identifiers must not be quoted in examples, search queries, or any artifact outside the session.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
