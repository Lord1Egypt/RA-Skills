## Description:

Helps OpenClaw owners install, verify, and manage InnerWarden protections for agent tool calls and MCP servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maiconburn](https://clawhub.ai/user/maiconburn)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw owners and developers use this skill to install and verify InnerWarden, understand what it protects, review commands for safety, and manage its configuration or removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because its installer pipes code downloaded from the internet directly into a shell.

Mitigation: Review the installer and independently verify what it downloads before running it; consider whether listed elevated commands are necessary.

Risk: The security scan is partial and does not resolve three local references.

Mitigation: Review those references before relying on the scan result.

## Reference(s):

- [InnerWarden skill documentation](https://github.com/InnerWarden/innerwarden-skill)
- [Pro installation guide](https://github.com/InnerWarden/innerwarden-skill/blob/master/docs/pro-on-a-server.md)
- [Managing InnerWarden Pro](https://github.com/InnerWarden/innerwarden-skill/blob/master/docs/managing-pro.md)
- [InnerWarden Pro pricing](https://innerwarden.com/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command examples and procedural instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands for installation and security-mode changes are presented for owner review.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
