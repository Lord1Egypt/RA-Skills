# Interpretive Lab Comment Drafter

Drafts interpretive comments for complex laboratory panel results. Applies delta-check logic, critical-value notation, pattern recognition, and clinical-correlation language for pathologist or licensed-provider review before result release.

## Use Cases

- Clinical laboratory scientists (MLS/MT/CLS) drafting reflex or added-value comments on complex panels
- Pathologists reviewing AI-drafted comments for sign-out efficiency
- Lab directors building comment libraries for standing orders
- Residents and fellows in laboratory medicine learning interpretive comment patterns

## Scope

**Supported panels:**
- CBC with differential (leukocytosis differential, anemia morphology, thrombocytopenia patterns)
- Comprehensive metabolic panel (CMP) and basic metabolic panel (BMP)
- Hepatic function panel (hepatocellular vs. cholestatic patterns)
- Thyroid panel (TSH-reflex, free T4, T3 uptake)
- Lipid panel (Friedewald LDL, non-HDL, atherogenic risk language)
- Coagulation studies (PT/INR, aPTT, D-dimer, fibrinogen)
- Urinalysis with microscopy
- Glucose and HbA1c (diabetes monitoring context)

**Out of scope:**
- Molecular / genomic / cytogenetic report interpretation — requires subspecialty pathologist
- Final result sign-out or release — the skill drafts; a pathologist or licensed provider must review and release
- Drug level (therapeutic drug monitoring) dosing recommendations — pharmacist/physician only
- Insurance pre-authorization or coverage determinations

## Output

A DRAFT interpretive comment containing:
- Abnormal result summary with high/low flags
- Critical value notation with mandatory notification reminder
- Delta-check comparison with prior results (if provided)
- Pattern recognition narrative (e.g., "findings are consistent with iron-deficiency anemia")
- Clinical-correlation recommendation for the ordering provider
- Pathologist or MLS review block

**This comment is a DRAFT only.** A licensed pathologist or authorized provider must review and release the comment before it is appended to a result or delivered to a clinician.

## Safety and Boundaries

- Never include full patient names, medical record numbers, or dates of birth in agent conversation.
- Critical values must be communicated to the ordering provider per laboratory policy — this skill drafts the notation but does not perform the notification.
- Institutional reference ranges and critical-value thresholds always take precedence over generic ranges cited in this skill.
- Specimen quality (hemolysis, lipemia, icterus) and pre-analytic variables must be noted when provided; they may invalidate results.
- Do not interpret molecular, cytogenetic, or flow cytometry panels — refer to the appropriate subspecialty pathologist.

## Feedback & Contributions

Found a gap or want to improve this skill? Open an issue at [https://github.com/archlab-space/Open-Skill-Hub/issues](https://github.com/archlab-space/Open-Skill-Hub/issues).
