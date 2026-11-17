## Description:

NoChat Channel Plugin adds NoChat as an OpenClaw messaging channel for encrypted agent-to-agent direct messages with per-agent trust tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmeow492](https://clawhub.ai/user/catsmeow492)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this plugin to connect OpenClaw agents to NoChat so they can send and receive direct messages, configure per-agent trust tiers, and route inbound messages to agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote NoChat messages may steer an OpenClaw agent as authorized commands without the advertised trust controls being enforced in the reviewed runtime.

Mitigation: Install only after the publisher fixes the trust-enforcement gap; until then, treat NoChat messages as capable of controlling the agent and avoid granting owner access broadly.

Risk: The reviewed runtime does not provide enough assurance that the advertised encryption controls are enforced.

Mitigation: Use a trusted HTTPS NoChat server endpoint, protect and rotate the NoChat API key, and avoid relying on the encryption claim until the publisher resolves the gap.

Risk: Owner-tier access can route messages into a main session with full tool access.

Mitigation: Use a dedicated low-privilege OpenClaw profile and reserve owner-tier trust for identities that have been independently verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catsmeow492/skills/nochat-channel-plugin)
- [NoChat](https://nochat.io)
- [NoChat API docs](https://nochat-server.fly.dev/api/v1/docs)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Plugin source link from artifact docs](https://github.com/kindlyrobotics/nochat-channel-plugin)
- [NoChat server source link from artifact docs](https://github.com/kindlyrobotics/nochat)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples; runtime messages are text direct messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, network access, a NoChat server URL, and a NoChat API key.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
