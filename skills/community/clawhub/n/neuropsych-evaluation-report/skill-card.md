## Description:

Drafts comprehensive neuropsychological evaluation reports from intake data, behavioral observations, performance validity information, standardized test results, clinical interpretation, diagnostic formulation, and functional recommendations for licensed neuropsychologist review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Licensed neuropsychologists, post-doctoral fellows, and clinical neuropsychology trainees use this skill to turn evaluation history, observations, validity results, and test battery scores into a structured draft report. The draft is intended for licensed neuropsychologist review, correction, signature, and compliance checks before any clinical, educational, insurance, or patient-facing release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft report content may contain incorrect clinical interpretations, diagnostic language, codes, or recommendations.

Mitigation: Have a licensed neuropsychologist verify language factors, performance validity, diagnostic formulation, DSM-5-TR or ICD-11 codes, and recommendations before release.

Risk: Patient-identifying information could be exposed if users enter full names, dates of birth, MRNs, or other protected health information into an unapproved AI environment.

Mitigation: Use initials plus case number only, avoid DOBs and MRNs, and enter identifying patient data only in institutionally approved HIPAA-covered environments.

Risk: Missing or fabricated test scores could make the draft misleading.

Mitigation: Use only user-provided scores and leave explicit placeholders for missing scores until testing records are inserted and reviewed.

Risk: Invalid or atypical performance validity results could undermine subsequent cognitive interpretation.

Mitigation: Apply the validity warning when any PVT fails or is atypical, reference that limitation in summary and formulation sections, and require clinician review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/neuropsych-evaluation-report)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft report with labeled sections, tables, warnings, open items, and review block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft clinical documentation only; requires licensed neuropsychologist review and signature before release.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog, released 2026-05-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
