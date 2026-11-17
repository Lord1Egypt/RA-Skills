## Description:

Controls IATerm terminals through a local WebSocket API so an agent can list workspaces, displays, panels, and remote connections, send terminal input, and subscribe to terminal output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sutaixu](https://clawhub.ai/user/sutaixu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to local IATerm sessions for terminal discovery, controlled command input, and terminal-output monitoring, including remote SSH or serial sessions surfaced by IATerm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact control of IATerm terminal sessions, including remote SSH or serial sessions.

Mitigation: Install and use it only when agent terminal control is intended, and review target connection identifiers before sending input or subscribing to output.

Risk: Approval bypass options and persistent approval state can allow later commands to run without fresh user confirmation.

Mitigation: Avoid --auto-approve and persistent always-approve choices unless every caller and workflow is trusted; clear ~/.cache/iaterm-ws-client when approval state should be reset.

Risk: Interactive raw JSON mode may expose sensitive terminal operations without the same approval checks as normal commands.

Mitigation: Avoid interactive raw JSON mode for sensitive terminal operations until it enforces the same approval checks as normal commands.

## Reference(s):

- [IATerm WebSocket Agent on ClawHub](https://clawhub.ai/sutaixu/skills/iaterm-ws-client)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses from the WebSocket client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The client can stream terminal output during subscribe_output sessions.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
