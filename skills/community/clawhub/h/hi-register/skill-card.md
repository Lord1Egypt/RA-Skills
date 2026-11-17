## Description:

Hi Register completes the second step of the Hi installation flow by registering this OpenClaw host with the Hi platform after the `clawhub:hirey` plugin is installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlee](https://clawhub.ai/user/yzlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to complete Hi setup after installing the `clawhub:hirey` plugin, register the current host with Hi, verify the resulting connection, and report the real registration state returned by Hi tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Hi integration can receive session and routing metadata and bind the current chat as a default reply target.

Mitigation: Install only if the publisher and Hi integration are trusted, and confirm the intended reply target before completing registration.

Risk: Registration can enable persistent push and event delivery behavior.

Mitigation: Review connection status after installation and prefer a version or deployment process that documents revocation and disablement controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzlee/skills/hi-register)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Tool calls, Text]

**Output Format:** [Markdown with inline shell commands and reported tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to report actual Hi registration fields such as `agent_id`, `hooks_ready`, `connected`, `activated`, and `push_ready` without fabricating values.]

## Skill Version(s):

1.0.36 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
