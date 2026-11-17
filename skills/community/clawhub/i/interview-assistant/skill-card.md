## Description:

Structured interview assistant that generates STAR interview question sets from job descriptions and optional resume text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanwan2qq](https://clawhub.ai/user/wanwan2qq)

### License/Terms of Use:

MIT-0

## Use Case:

HR staff, recruiters, hiring managers, and interview preparation agents use this skill to turn a job description and optional candidate resume into structured STAR behavioral interview questions, matching analysis, and scoring guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper delegates execution to the first interview-assistant command found on PATH.

Mitigation: Install or link the interview-assistant binary from a trusted source and verify PATH resolution before use.

Risk: Resume inputs may contain unnecessary personal data or identifiers.

Mitigation: Redact contact details and other identifiers unless they are required for interview-question generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanwan2qq/skills/interview-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown, JSON, or plain text containing job and candidate analysis, STAR interview questions, scoring criteria, and summary guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an interview-assistant binary on PATH; accepts job-description text, optional resume text, question count, and output-format options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
