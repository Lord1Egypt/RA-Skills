## Description:

Scan MCP configurations and agent skills with Open Agent Scan, explain security findings, and propose focused fixes. Use when evaluating an MCP server configuration or reviewing a skill before adoption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rahulbsw](https://clawhub.ai/user/rahulbsw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan MCP configurations and agent skills, interpret heuristic findings, and propose focused fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented `uvx open-agent-scan` command does not pin a package version, so the package resolved at install time may change.

Mitigation: Choose and review a specific release, then pin that version before running scans.

Risk: MCP discovery can start configured commands, download packages through runners, or contact remote MCP endpoints.

Mitigation: Inspect the selected configuration first, redact credentials, obtain consent for discovery actions, and use a disposable sandbox for untrusted servers.

## Reference(s):

- [Open Agent Scan project](https://github.com/rahulbsw/agent-scan)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command examples and scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted findings and focused remediation suggestions]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
