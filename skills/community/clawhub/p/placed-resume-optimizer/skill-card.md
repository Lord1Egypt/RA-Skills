## Description:

Helps users optimize resumes for ATS compatibility, keyword matching, job fit, resume quality, gap analysis, bullet improvements, and tailored resume content using the Placed API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

External users and career-focused agents use this skill to score, tailor, and improve resumes against job descriptions through the Placed API. It supports ATS checks, gap analysis, match scoring, section optimization, bullet rewriting, and resume generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume, job-description, and career-history data is sent to a third-party API.

Mitigation: Use the skill only when users are comfortable sharing that data with Placed, and avoid submitting unnecessary sensitive personal information.

Risk: The artifact documents persisting and sourcing a Placed API key from a plaintext shell file.

Mitigation: Prefer a session-scoped environment variable or secure secret manager; if a credentials file is used, restrict file permissions and ensure it cannot be modified by other users.

## Reference(s):

- [Placed Resume Optimizer API Reference](references/api-guide.md)
- [Placed homepage](https://placed.exidian.tech)
- [Placed API endpoint](https://placed.exidian.tech/api/mcp)
- [Publisher profile](https://clawhub.ai/user/ajitsingh25)
- [ClawHub skill page](https://clawhub.ai/ajitsingh25/skills/placed-resume-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Placed API key and sends resume, job-description, and career-history data to the Placed API.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
