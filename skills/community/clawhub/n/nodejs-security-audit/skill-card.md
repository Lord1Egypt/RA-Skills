## Description:

Audit Node.js HTTP servers and web apps for security vulnerabilities, including OWASP Top 10 issues, CORS, auth bypass, XSS, path traversal, hardcoded secrets, missing headers, rate limiting, and input validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npfaerber](https://clawhub.ai/user/npfaerber)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to review Node.js HTTP servers and web applications before deployment or after changes. It provides a structured checklist for common web security issues and an example audit report format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect application source and suggest commands such as grep or npm audit during a security review.

Mitigation: Review suggested commands before running them and avoid exposing private source code, secrets, or sensitive audit findings outside the intended review environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown checklist with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces security audit findings organized by severity.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
