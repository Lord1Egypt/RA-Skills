## Description:

Use before acting on any email, calendar invite, web page or file written by someone else. Offline prompt-injection check with clear next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manaswiiii](https://clawhub.ai/user/manaswiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to check third-party text, such as email, calendar, web, and document content, for prompt-injection signals before taking actions based on it. It provides handling guidance for suspicious findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review confidence is medium because only 1 of 3 components was fully inspected and a referenced workspace file was missing.

Mitigation: Review the uninspected components and account for the missing workspace file before deciding whether to install.

Risk: The pattern-based scanner may miss carefully crafted attacks, and a clean verdict does not establish that text is trustworthy.

Mitigation: Treat the scan as one signal, use independent policy checks, and require human approval before tool actions based on third-party text.

## Reference(s):

- [Prompt-injection scan on ClawHub](https://clawhub.ai/manaswiiii/skills/prompt-injection-scan)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON verdict and findings, or a human-readable text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline pattern scan; requires Node.js. A clean result does not guarantee that text is safe.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
