## Description:

CORS Audit probes live API endpoints with crafted Origin headers, scans source code for insecure CORS middleware patterns, and generates safer CORS configuration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit CORS behavior on authorized endpoints, identify risky header or middleware patterns, and draft corrected configuration for common web stacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can probe arbitrary URLs from the agent environment.

Mitigation: Use it only for endpoints you own or are authorized to test; avoid localhost, private network addresses, metadata services, and untrusted user-supplied URLs.

Risk: Generated Express preflight examples may be unsafe if applied without preserving a restricted CORS policy.

Mitigation: Review generated snippets before deployment and ensure preflight handling reuses the same explicit allowlist and credentials policy as normal requests.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-cors-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands and generated configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CORS probe findings, source scan findings, remediation notes, and stack-specific configuration examples.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
