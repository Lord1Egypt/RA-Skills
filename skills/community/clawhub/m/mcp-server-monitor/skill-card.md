## Description:

This German-language skill helps agents diagnose official MCP connector status in Claude and prepare setup, OAuth scope, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to determine whether an official MCP connector exists, identify its connection state, and provide concrete next steps for Claude app, Claude Code, OAuth, and configuration troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested OAuth scopes or connector configuration could grant more access than the user needs.

Mitigation: Review scopes and connector settings before applying them, especially for write, billing, credential, or deletion permissions.

Risk: Users may expect the skill to install connectors or complete authentication automatically.

Mitigation: Keep connector setup and OAuth authorization in an interactive user-controlled session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kikikari/skills/mcp-server-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
