# Job Hazard Analysis (JHA / JSA) Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Occupational Safety — OSHA / MSHA / ANSI Z10

## Purpose

A Job Hazard Analysis drafting partner for EHS managers, safety professionals, foremen, supervisors, competent persons, and frontline workers. Turns a job description, work environment, equipment list, and worker input into a structured DRAFT JHA (also known as JSA or Activity Hazard Analysis) that walks the job step by step, identifies hazards by category, scores risk before and after controls, and proposes mitigations in strict **hierarchy-of-controls** order (Elimination → Substitution → Engineering → Warnings → Administrative → PPE) per OSHA Publication 3071 and ANSI/ASSP Z10.

## When to Use

- Drafting a new JHA for a routine, non-routine, emergency, or one-off job
- Reviewing or updating an existing JHA when a step, tool, material, or environmental factor has changed
- Pre-task / pre-shift hazard analysis for high-risk work (confined space, fall exposure, energized work, hot work, excavation, lifting / rigging, chemical handling, mobile equipment)
- Building the JHA package for OSHA VPP / SHARP, ANSI Z10 audits, MSHA Part 46 / 48 task training, USACE EM 385-1-1 AHAs, or contractor pre-qualification (ISNetworld / Avetta / Veriforce)
- Capturing worker input on hazards before authorizing the work

## What It Does

**Phase 1: Scope and authority**
1. Captures job title, work activity, location, duration, frequency, and crew size
2. Captures the regulatory frame (29 CFR 1910 General Industry, 29 CFR 1926 Construction, 30 CFR Parts 46 / 48 / 56 / 57 MSHA, EM 385-1-1, ANSI/ASSP Z10, site EHS program)
3. Captures the competent-person / supervisor / qualified-person of record and worker participants

**Phase 2: Job description**
4. Captures tools, equipment, materials (with SDS references), energy sources, environment, weather sensitivity, simultaneous operations (SIMOPs), and known PPE constraints
5. Breaks the job into ordered steps at the right granularity (typically 8–15 steps) using verb-object phrasing

**Phase 3: Hazard identification per step**
6. For every step, walks an explicit hazard-category checklist (struck-by / struck-against, caught-in / between, fall-same / fall-from / fall-into, electrical, thermal, chemical / inhalation / skin / eye, biological, ergonomic, noise / vibration, radiation, fire / explosion, pressure / stored energy, environmental, line-of-fire, dropped objects, vehicular)
7. Records the hazardous condition and the potential incident / injury / illness, and computes an inherent risk score (Severity 1–5 × Likelihood 1–5)

**Phase 4: Controls in hierarchy order**
8. For each hazard, proposes controls **in strict order** — Elimination → Substitution → Engineering → Warnings → Administrative → PPE — and never advances to a lower tier without explaining why higher tiers were rejected
9. Re-scores residual risk after the proposed controls
10. Flags any residual High or Extreme risk for stop-work consideration and management of change

**Phase 5: Permits, training, and emergency response**
11. Cross-references required permits (confined space, hot work, LOTO, line-break, excavation, fall protection, energized electrical work, dive, radiation)
12. Lists required training, qualifications, medical clearance, fit-test, and refresher dates per role
13. Captures emergency response (egress, muster, communication, rescue, first aid, eyewash / shower, spill response, fire suppression) and stop-work triggers

**Phase 6: Worker review and sign-off**
14. Produces a worker-acknowledgement block (signatures captured at the worksite, not by the agent) and an unsigned competent-person / supervisor / EHS-reviewer sign-off block
15. Runs a self-check against the OSHA JHA quality gates and lists unresolved items before delivering the DRAFT

## Output

A DRAFT JHA with:

- Header (job, location, dates, regulatory frame, revision, competent person)
- Tools / equipment / materials inventory with SDS references
- Required permits, training, and PPE
- Step-by-step table: **Step → Hazard category → Hazardous condition → Potential incident → Inherent risk → Controls (hierarchy-ordered) → Residual risk → Verification**
- Emergency response and stop-work-trigger block
- Worker-participation list and unsigned acknowledgement block
- Unsigned competent-person / supervisor / EHS sign-off block
- Self-check rubric output
- Unresolved-information list

## Safety

This skill drafts a hazard analysis, **not** an authorization to work. Every output is labeled **DRAFT — COMPETENT PERSON / SUPERVISOR / EHS MUST REVIEW**. The agent never approves work, never signs the JHA, never selects a respirator cartridge or PPE without referring to the SDS / employer respiratory-protection program, and never overrides site-specific procedures or AHJ requirements. SDS data and worker personal identifiers are summarized — never pasted verbatim into the JHA. The skill enforces the hierarchy of controls and refuses to recommend PPE as the sole control where engineering or administrative controls are feasible.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
