## Description:

Creates and polishes Persian right-to-left resumes and CVs while preserving readable English names, technical terms, and contact details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ehsanghaffar](https://clawhub.ai/user/ehsanghaffar)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and resume writers use this skill to create or revise Persian CVs for job applications, including mixed Persian-English content and right-to-left layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume inputs and output files contain personal contact and employment information.

Mitigation: Use only the necessary candidate information and store generated files in an appropriately protected location.

Risk: Missing document-generation dependencies or Persian fonts can prevent generation or impair rendering.

Mitigation: Check python-docx, WeasyPrint, and suitable Persian fonts in the target environment; review the rendered PDF or DOCX before sharing.

## Reference(s):

- [Persian Resume on ClawHub](https://clawhub.ai/ehsanghaffar/skills/persian-resume)
- [Resume data schema](references/resume-data-schema.md)
- [Resume validation rules](references/validation-rules.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Persian resume or CV as PDF or DOCX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Right-to-left layout with readable English terms and contact details; classic and modern templates.]

## Skill Version(s):

0.1.2 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
