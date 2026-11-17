## Description:

Assists HR and hiring teams by combining a job description, resume, and optional interview notes to produce a candidate evaluation report with five scoring dimensions, a hiring recommendation, and export guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudmusiccio](https://clawhub.ai/user/cloudmusiccio)

### License/Terms of Use:

MIT-0

## Use Case:

HR employees and hiring teams use this skill to evaluate candidates against a job description using a resume and optional interview record. It produces a structured assessment for human review, not an automated final hiring decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process resumes and interview notes that contain sensitive candidate data and contact information.

Mitigation: Require explicit confirmation before parsing files, redact unnecessary personal data, and restrict access to generated PDF/PNG reports.

Risk: Broad keyword and file-name activation may process candidate files without clear consent.

Mitigation: Trigger only after an explicit interview-evaluation command and confirm which files will be used.

Risk: AI-generated hiring recommendations may be incomplete or biased if treated as final decisions.

Mitigation: Require human review of scores, rationale, and final hiring decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudmusiccio/skills/hr-interview-evaluator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown report text with optional PDF/PNG report files and radar chart image.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JD text, resume documents, and optional interview records; report content may contain personal candidate data.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
