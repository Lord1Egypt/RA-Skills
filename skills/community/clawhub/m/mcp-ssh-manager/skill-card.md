## Description:

Helps agents manage remote SSH server workflows with MCP ssh-manager, including command execution, session reuse, file transfer, monitoring, tunneling, backup, troubleshooting, and workdir organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaxtomas](https://clawhub.ai/user/imaxtomas)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to guide SSH-based administration through MCP ssh-manager while preserving session context, command logs, status snapshots, and reusable workdir records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-proposed SSH commands can perform privileged or destructive server actions.

Mitigation: Review every command before execution, with extra scrutiny for sudo, uploads, syncs, restores, tunnels, and deletions.

Risk: A troubleshooting example uses broad PHP-FPM socket permissions.

Mitigation: Do not use the chmod 666 example; apply least-privilege ownership and socket mode settings instead.

Risk: Persisted workdir records may contain operational details or secrets.

Mitigation: Store outputs in private directories, redact sensitive values, and clean obsolete records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaxtomas/skills/mcp-ssh-manager)
- [Publisher profile](https://clawhub.ai/user/imaxtomas)
- [Original MCP Server](https://github.com/bvisible/mcp-ssh-manager)
- [Session Management Deep Dive](references/sessions.md)
- [Workdir Structure and Usage](references/workspace.md)
- [Comparing Historical Data](references/comparison.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and MCP tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ssh-manager MCP server; outputs may include operational notes, command logs, status summaries, and configuration guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
