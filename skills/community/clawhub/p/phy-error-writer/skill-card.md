## Description:

Rewrites unclear or unhelpful error messages into clear, actionable text for users, logs, and APIs, while auditing common error-message anti-patterns across languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, API designers, support engineers, and product teams use this skill to rewrite confusing error strings into audience-specific UI messages, API responses, log entries, and style guidance. It can also audit existing error messages for vague wording, leaked internals, missing context, and unclear recovery steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated log guidance may encourage inclusion of sensitive data such as credentials, tokens, cookies, personal data, payment data, request bodies, or broadly exposed stack traces.

Mitigation: Review generated log guidance before use, prefer allowlisted diagnostic fields, redact sensitive values, and keep stack traces in access-controlled diagnostic systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-error-writer)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Project homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown report with rewritten messages, audit tables, JSON API examples, log-line examples, and optional code constants.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces separate variants for end-user UI text, API response bodies, server logs, and project-specific error-message style guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
