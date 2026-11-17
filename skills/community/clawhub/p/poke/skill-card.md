## Description:

Send SMS/iMessage to the user via Poke and process inbound Poke events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect OpenClaw with Poke for user messaging, SMS-based alerts, inbound Poke event handling, and webhook-triggered workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Poke tunnel access may provide a long-lived route to the local OpenClaw MCP server.

Mitigation: Prefer a foreground, temporary tunnel unless persistent access is explicitly needed, and review the systemd service before enabling it.

Risk: The exposed MCP-side tools can enable access to active sessions, logs, and workspace files.

Mitigation: Require explicit approval or allowlists before exposing files, logs, active sessions, or session-targeting actions.

Risk: The documented SDK workaround patches installed Poke binaries and libraries in place.

Mitigation: Pin and verify package versions, and avoid patching installed binaries unless the change has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g9pedro/skills/poke)
- [Poke device login](https://poke.com/device)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup, routing, troubleshooting, and webhook guidance for Poke and OpenClaw integration.]

## Skill Version(s):

0.6.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
