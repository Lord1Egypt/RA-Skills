## Description:

Audits OpenClaw configuration files and produces a structured Markdown permissions report covering API credentials, channel access, gateway settings, tool execution rules, command permissions, device identity, and internal hooks with sensitive values masked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rushingai](https://clawhub.ai/user/rushingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to inspect what permissions and integrations an OpenClaw installation has configured. It helps summarize access posture while masking credentials, tokens, private keys, and full identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated permissions report can reveal enabled providers, gateway exposure, approval rules, operator scopes, and channel access patterns even when secrets are masked.

Mitigation: Treat the report as sensitive operational security material and share it only with reviewers who need to assess the OpenClaw installation.

Risk: The skill reads local OpenClaw configuration files that may contain credentials, private keys, tokens, user identifiers, and socket details.

Mitigation: Follow the skill's masking rules: never output full secrets, private keys, passwords, full user IDs, full device IDs, or expanded local file paths.

## Reference(s):

- [OpenClaw Permissions Audit on ClawHub](https://clawhub.ai/rushingai/skills/openclaw-permissions)
- [rushingai publisher profile](https://clawhub.ai/user/rushingai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with tables and grouped lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks sensitive values and reports missing, empty, or unreadable fields explicitly.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
