## Description:

Access and manage ClickUp tasks, spaces, folders, and create new tasks using the ClickUp REST API v2 with a user-provided API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to a Pipeworx-hosted ClickUp MCP endpoint for listing and creating ClickUp workspace items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClickUp workspace data and user-provided credentials may pass through an unexplained third-party MCP gateway.

Mitigation: Verify the Pipeworx gateway operator and privacy posture before installation, use a dedicated least-privilege ClickUp API token, avoid highly sensitive workspaces, and revoke the token if the gateway behaves unexpectedly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-clickup)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with JSON configuration and tool-call results from the ClickUp MCP server]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided ClickUp API key through the configured MCP gateway.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
