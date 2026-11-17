## Description:

Connects a local OpenClaw agent to browser voice chat through the Hotbutter hosted relay, relaying transcribed speech to the local agent and returning spoken responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-stajer](https://clawhub.ai/user/michael-stajer)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to add a hosted browser voice interface to a local OpenClaw agent. It pairs a browser session with a local voice bridge that runs the OpenClaw CLI for each transcribed message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcribed speech and agent response text pass through the hosted relay.

Mitigation: Use the default relay only for conversations suitable for hosted transit, or configure a relay you control with --relay-url.

Risk: Relay-delivered messages can invoke the local OpenClaw agent without local confirmation.

Mitigation: Run the bridge with OpenClaw permissions limited to actions you are comfortable exposing to relay-delivered prompts.

Risk: Agent responses may include secrets, credentials, or private data that would be sent back through the relay.

Mitigation: Avoid agents and sessions that can reveal sensitive data, and review agent output behavior before using the voice bridge.

Risk: Installation depends on downloaded package contents and npm dependencies.

Mitigation: Verify the downloaded artifact, file hashes, and dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michael-stajer/skills/hotbutter)
- [Publisher profile](https://clawhub.ai/user/michael-stajer)
- [Hotbutter hosted relay](https://hotbutter.ai)
- [Hotbutter local alternative](https://github.com/hotbutter-ai/hotbutter-os)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with setup prompts, pairing URL, status logs, and relayed agent response text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local openclaw CLI and a WebSocket relay; the default relay is wss://hotbutter.ai.]

## Skill Version(s):

1.0.6 (source: server release evidence; package.json lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
