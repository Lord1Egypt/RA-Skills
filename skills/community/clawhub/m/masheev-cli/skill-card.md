## Description:

Operate a Masheev workspace from the terminal using the masheev CLI for authentication, inbox and contact tasks, JSON automation, customer replies, and MCP setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masheev](https://clawhub.ai/user/masheev)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and external teams use this skill to manage Masheev workspace tasks from a terminal, automate inbox and contact workflows, and configure Masheev MCP integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace access may grant write or customer-message permissions.

Mitigation: Start with read-only access, verify the selected workspace and granted scopes with whoami, and request only needed permissions.

Risk: A customer reply or MCP configuration change can affect people or local setup.

Mitigation: Prepare replies as drafts for human approval and inspect MCP configuration changes before applying them.

Risk: The separately downloaded CLI and any additionally installed skills were not audited here.

Mitigation: Review package versions and any additional skills before installation.

## Reference(s):

- [Masheev CLI documentation](https://docs.masheev.com/connect/cli)
- [Masheev CLI on ClawHub](https://clawhub.ai/masheev/skills/masheev-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown with shell commands, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and permissions vary by workspace; verify the installed prerelease CLI's help.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
