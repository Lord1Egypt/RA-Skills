## Description:

Connects an agent to ClickUp MCP to read, create, and update workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to search ClickUp workspaces, inspect tasks and members, and create or update tasks, comments, and chat messages through a connected ClickUp MCP account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic CLI installer and deployed connector were not verified.

Mitigation: Review and preinstall a verified CLI release before use, review the connector, and connect only the ClickUp scopes needed.

Risk: Task, comment, and chat actions can change ClickUp data.

Mitigation: Inspect the action schema and confirm the exact payload and effect before running write actions.

Risk: oo CLI commands may make broader changes to other agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 for oo commands to prevent skill synchronization.

## Reference(s):

- [ClickUp MCP documentation](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [CLI skill sync controls](https://raw.githubusercontent.com/oomol-lab/oo-cli/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payloads; JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may create or update ClickUp tasks, comments, and chat messages.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
