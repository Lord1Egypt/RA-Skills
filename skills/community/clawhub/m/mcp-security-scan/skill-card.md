## Description:

Scans MCP tool descriptions for command execution, file writing, network egress, and credential exposure signals, then provides risk ratings and least-privilege guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill before connecting a third-party MCP server to identify potentially risky tools and decide which permissions to limit or withhold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package requests WebFetch and Write while also claiming no network or filesystem access.

Mitigation: Review the requested permissions before installation; remove or justify unnecessary grants and align them with actual behavior.

Risk: Sensitive MCP configuration could be exposed under broader tool permissions.

Mitigation: Avoid supplying sensitive configurations unless those permissions are acceptable; redact secrets and apply least privilege.

Risk: A scan of tool metadata alone cannot establish how an MCP server behaves when connected.

Mitigation: Treat the report as a preliminary review and independently verify server behavior before granting access.

## Reference(s):

- [MCP Security Scan on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/mcp-security-scan)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-tool risk indicators, a high-risk tool count, and least-privilege advice; reviews supplied tool metadata rather than live server behavior.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; bundled SKILL.md declares 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
