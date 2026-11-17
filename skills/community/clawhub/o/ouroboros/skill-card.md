## Description:

Ouroboros routes messages prefixed with `ooo` to the `ouroboros_channel_workflow` MCP tool and relays the tool response back to the channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q00](https://clawhub.ai/user/q00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to hand off `ooo`-prefixed requests to the Ouroboros MCP service for interviewing, seed generation, execution, and status tracking while the agent acts only as a relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external Ouroboros MCP service and an unpinned third-party MCP package.

Mitigation: Install only after reviewing and trusting the service and publisher, prefer a pinned package version, and run the MCP server in a constrained environment.

Risk: Messages and channel, guild, and user identifiers may be forwarded to the Ouroboros service.

Mitigation: Avoid sending sensitive content and limit the MCP server's access to unrelated repositories, credentials, and home-directory data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/q00/skills/ouroboros)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relays the Ouroboros MCP tool response without summarizing or reinterpreting it.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
