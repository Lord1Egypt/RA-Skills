# Neuropsychological Evaluation Report Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Neuropsychology
**Skill:** `neuropsych-evaluation-report`

## Purpose

A clinical documentation assistant for licensed neuropsychologists (Ph.D., Psy.D.), post-doctoral fellows, and neuropsychology trainees. Converts intake data, behavioral observations, and standardized test battery results into a structured evaluation report aligned to APA and APPCN reporting standards — ready for licensed neuropsychologist review and signature before release.

## When to Use

- When drafting a comprehensive neuropsychological evaluation report after completing a full test battery
- When you need to organize and interpret standardized cognitive test results across domains
- When writing domain-by-domain clinical interpretations with functional impact language
- When you need a diagnostic formulation with DSM-5-TR / ICD-11 considerations
- When drafting functional recommendations (academic, occupational, driving, medical follow-up)
- When preparing a report for a supervising neuropsychologist's review and signature

## What It Does

**Phase 1: Intake and History**
1. Collects PII-safe patient identifier, referral question, evaluation setting, and testing dates
2. Documents background history across medical, psychiatric, developmental, social, occupational, and medication domains

**Phase 2: Behavioral Observations and Validity**
3. Documents behavioral observations during testing (appearance, cooperation, affect, motor)
4. Records performance validity test (PVT) results; gates all subsequent interpretation — applies VALIDITY WARNING if any PVT fails or is atypical

**Phase 3: Test Results**
5. Builds a standardized test battery results table with raw scores, standard scores, percentiles, and classification bands (Very Superior to Extremely Low/Impaired)

**Phase 4: Domain-by-Domain Interpretation**
6. Writes interpretive narratives for up to 10 cognitive domains: intellectual functioning, attention, processing speed, working memory, memory/learning, language, visuospatial, executive function, motor, and mood

**Phase 5: Summary, Formulation, and Recommendations**
7. Integrative clinical summary relating findings to the referral question
8. Diagnostic formulation with provisional DSM-5-TR/ICD-11 considerations labeled PRELIMINARY
9. Numbered recommendations covering medical referrals, cognitive rehab, accommodations, driving safety, and reassessment
10. DRAFT report assembly with Neuropsychologist Review Block

## Safety Boundaries

- Never uses full patient names, dates of birth, or MRNs — initials + case number only
- Never fabricates or estimates test scores — uses placeholders for all missing scores
- Performance validity testing gates all interpretation — VALIDITY WARNING is mandatory when PVTs fail
- Diagnostic labels are never stated as definitive; uses "consistent with" and "suggestive of" language throughout
- All DSM-5-TR / ICD-11 code suggestions are labeled PRELIMINARY for licensed neuropsychologist verification
- Includes a driving safety flag if the cognitive profile raises fitness-to-drive concerns
- All output is a DRAFT requiring licensed neuropsychologist (Ph.D./Psy.D.) review and signature before release
- Includes HIPAA reminder for AI tool usage in clinical environments

## Notes

This skill is intended for neuropsychological professionals working within a licensed clinical framework. It does not replace clinical judgment, doctoral-level neuropsychological training, or institutional compliance review. All interpretations, diagnostic formulations, and recommendations must be reviewed and verified by a licensed neuropsychologist before any clinical, educational, or insurance use.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
