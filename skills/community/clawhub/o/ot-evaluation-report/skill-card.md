## Description:

Drafts an initial Occupational Therapy evaluation report from clinician-provided data, aligned to the AOTA Occupational Therapy Practice Framework 4th edition and CMS / Medicare documentation standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Licensed Occupational Therapists, supervised OTAs, OT students, and rehabilitation documentation specialists use this skill to turn clinician-provided evaluation data into a structured draft OT evaluation report for review and sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft OT documentation could contain inaccurate facts, clinical reasoning, payer language, or final wording if user-provided inputs are incomplete or wrong.

Mitigation: Require licensed OT review, editing, dating, and signature before entry into any medical record, school record, or payer submission.

Risk: Patient information may be included while preparing an evaluation draft.

Mitigation: Use initials and placeholders in working drafts and handle any patient information according to clinical privacy policies.

Risk: Safety concerns such as fall risk, pressure injury, or cognitive decline could be under-addressed in a draft.

Mitigation: Flag safety concerns prominently in the unresolved-information list for clinician follow-up.

## Reference(s):

- [AOTA Occupational Therapy Practice Framework, 4th edition (OTPF-4)](artifact/README.md)
- [CMS Medicare Part B documentation requirements (42 CFR § 410.59, MLN 905364)](artifact/README.md)
- [IDEA Part B school-based OT evaluation requirements](artifact/README.md)
- [AOTA Occupational Profile Template (2017)](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown draft evaluation report with tables and unresolved-information list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is labeled as a draft for licensed OT review and sign-off.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
