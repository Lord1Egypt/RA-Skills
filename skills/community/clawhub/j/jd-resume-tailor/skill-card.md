## Description:

Generates job-specific tailored resumes from a base profile and job description, then produces print-optimized HTML suitable for PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[26048608982lp-ai](https://clawhub.ai/user/26048608982lp-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect resume profile details, compare them against a target job description, and generate a tailored bilingual resume for job applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive personal resume profile data in the workspace.

Mitigation: Review resume-profile.md for sensitive fields and delete or redact it when it is no longer needed.

Risk: The skill may fetch job descriptions from user-provided URLs.

Mitigation: Prefer pasted job descriptions or trusted local files when network fetching is not required.

Risk: Tailored resume content can overstate qualifications or introduce inaccurate claims.

Mitigation: Review generated resumes for correct contact details, dates, employer names, project facts, and achievement claims before sending.

## Reference(s):

- [HTML Resume Template Guide](references/html-template-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance plus self-contained HTML/CSS resume files and browser PDF export commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a persistent resume-profile.md and writes generated HTML/PDF resume artifacts under resumes/.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
