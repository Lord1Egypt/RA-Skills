## Description:

Perform a security audit of a Go codebase, targeting SSH servers, BBS systems, API services, and CLI tools for race conditions, goroutine leaks, missing error handling, command injection, and authentication bypasses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forgou37](https://clawhub.ai/user/forgou37)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to review Go repositories for concurrency, error handling, command execution, authentication, session, and resource-leak risks. It produces prioritized findings with file and line citations plus minimal suggested patches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad Go repository review requests when a non-security code review was intended.

Mitigation: Phrase requests clearly, for example by asking for either a Go security audit or a non-security code review.

Risk: Security findings and suggested fixes may be incomplete or incorrect without project-specific validation.

Mitigation: Review findings against the source code, run the project's tests and security checks, and apply suggested patches only after maintainer review.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, markdown, code, guidance]

**Output Format:** [Markdown finding list with Go code snippets and minimal diff-style fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are prioritized by severity from Critical through Low.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
