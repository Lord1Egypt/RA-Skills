## Description:

Creates structured medical CVs and resumes for medical professionals using provided education, experience, and CV type inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Medical professionals, academic medicine applicants, and supporting agents use this skill to draft US-style CV or resume sections from education and experience inputs. It is best suited for formatting and organization, with human review required for accuracy, credentials, citations, and local requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CV or resume content may be incomplete, inaccurate, or mismatched to institution-specific and locale-specific expectations.

Mitigation: Review all generated sections against the source materials, medical credentials, citation needs, and applicable local or institutional requirements before use.

Risk: The packaged implementation is basic and does not validate credentials, citations, or professional claims.

Mitigation: Use the skill for formatting and organization only; require a qualified human reviewer to confirm facts and professional suitability.

Risk: Broad workflow wording could lead an agent beyond CV and resume formatting tasks.

Mitigation: Keep use within documented medical CV/resume formatting scope and stop when required inputs or source evidence are missing.

## Reference(s):

- [Medical CV/Resume Builder References](references/guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/medical-cv-resume-builder)

## Skill Output:

**Output Type(s):** [markdown, json, guidance]

**Output Format:** [JSON containing generated CV markdown and section metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No additional Python packages are required; output should be reviewed for accuracy and locale fit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
