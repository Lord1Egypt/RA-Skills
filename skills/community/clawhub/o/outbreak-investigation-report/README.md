# Outbreak Investigation Report

**Domain:** Public Health · Field Epidemiology · Communicable Disease
**Platforms:** Claude · Codex

## Purpose

Turns case data, environmental observations, lab results, and team notes into a DRAFT outbreak-investigation report that follows the CDC Field Epi Manual 10-step framework — preparation, existence confirmation, diagnosis verification, case-definition construction, systematic case finding and line-listing, descriptive epidemiology (time / place / person + epi-curve interpretation), hypothesis generation, analytical-study design (cohort RR / case-control OR with 95% CI), control and prevention measures, and communication planning. The output is always a DRAFT for the supervising medical epidemiologist to review, edit, and release — never a public-release document, clinician HAN, or press release.

## When to Use

- A field epidemiologist or EIS officer must draft a foodborne / waterborne / vectorborne / vaccine-preventable / respiratory / healthcare-associated outbreak-investigation report
- A communicable-disease nurse must document a cluster investigation against a baseline
- A local / state / tribal / territorial health department must produce a methods-and-limitations-disciplined report from a partially completed investigation
- An environmental-health specialist must document control measures and authorizing authority for a foodborne or waterborne outbreak
- A hospital infection preventionist must draft an HAI-cluster report for the medical epidemiologist
- An international (IHR-relevant) investigator must draft a structured report for the IHR National Focal Point review

## What It Does

1. Collects role, jurisdiction and authority, investigation identifier, suspected agent class, first-report and earliest-onset dates, and source documents through one-question-at-a-time intake — and enforces a confidentiality reminder before any data is pasted
2. Walks all 10 CDC steps: preparation; outbreak-existence test against baseline with pseudo-outbreak rule-outs; diagnosis verification; four-element case definition with confirmed / probable / suspect ladder; case-finding plan and line-list specification (case IDs only, never personal identifiers); descriptive epidemiology with epi-curve shape interpretation and exposure-window arithmetic; testable hypotheses; analytical-study design matching measure to design (cohort → RR, case-control → OR, both with 95% CI); control measures with authorizing authority; and a communication plan that distinguishes internal / clinician / public / community-plain-language specifications
3. Drafts methods, limitations, lessons-learned, and action items (owner-role / due-date / status)
4. Runs a 15-item confidentiality and compliance self-check (identifier scan, small-cell N < 5 suppression, case-definition-before-counts, measure-matches-design, CI-and-p-value, HIPAA public-health-authority basis, IRB / human-subjects determination, authorizing-authority for every control measure, agent-not-medical-epi) and maintains an edit log
5. Outputs a complete DRAFT report with an executive summary, full 10-step structure, and a verbatim supervising-medical-epidemiologist-review banner

## Notes

This skill produces a **DRAFT outbreak-investigation report**, not a public-release document. It does not declare an outbreak over, does not authorize control measures, does not issue clinician HAN messages or press releases, and does not communicate with affected parties. The drafting agent is never the supervising medical epidemiologist, never the agency communications lead, and never the IHR National Focal Point. Personal identifiers must remain redacted in the working draft; the skill uses case IDs (C-###) throughout and enforces a small-cell suppression rule. For bioterrorism or select-agent suspicion, the skill flags an immediate referral to the FBI / federal SOC and stops drafting public-content specifications.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
