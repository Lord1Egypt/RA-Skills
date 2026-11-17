## Description:

Audit HTTP security headers for any website, including HSTS, CSP, X-Frame-Options, information-leak headers, per-site grades, and optional JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and site operators use this skill to audit public websites for missing or weak HTTP security headers and receive grades, warnings, and fix recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unrestricted outbound requests from the runner to user-provided URLs.

Mitigation: Use it only on public websites you intend to audit, avoid internal or sensitive URLs, and run it in a network-restricted environment when possible.

Risk: The security scan verdict is suspicious pending stronger URL validation, redirect validation, response streaming, and pinned dependencies.

Mitigation: Review the skill before deployment and add those controls before using it in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/http-sec-audit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report or JSON array with per-URL findings, grades, warnings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make outbound HTTP requests to user-provided URLs and follows redirects during scanning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
