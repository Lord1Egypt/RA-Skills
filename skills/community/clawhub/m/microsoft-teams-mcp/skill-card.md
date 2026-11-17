## Description:

Use fpx from a shell to read Microsoft Teams chats, channels, unread messages, inline images, and the Activity feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use shell commands and scripts to inspect Microsoft Teams conversations and activity when they need Teams data without running the Teams MCP server. The workflow requires a signed-in Teams browser tab to capture an access token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marked suspicious because its read-focused purpose is paired with instructions for state-changing Teams requests.

Mitigation: Keep shell use to the provided GET helpers; require explicit user approval for any write, with the exact conversation and content shown before execution.

Risk: If request destinations or arguments are controlled, the captured Teams authorization header could be sent to another destination.

Mitigation: Use only approved Teams chat-service and image hosts, and review request URLs and arguments before execution.

Risk: The security scan is partial because several local references could not be resolved.

Mitigation: Resolve and review the missing references, then complete security review before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/microsoft-teams-mcp)
- [Teams chat-service recipes](references/chatsvc-recipes.md)
- [Teams shell helpers](references/teams-env.sh)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Shell commands, JSON data, Text]

**Output Format:** [Shell commands with JSON or text response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads private Teams conversation and activity data; requires a signed-in Teams tab for token capture.]

## Skill Version(s):

0.13.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
