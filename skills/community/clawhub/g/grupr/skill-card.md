## Description:

Add an OpenClaw agent to a Grupr conversation, stream new messages over WebSocket, generate responses through a local OpenClaw gateway, and post replies back as the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[babcobb287](https://clawhub.ai/user/babcobb287)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to connect an existing local OpenClaw agent to a Grupr group conversation so the agent can respond to human messages in real time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Grupr conversation participants can influence prompts sent to a local OpenClaw agent.

Mitigation: Use a dedicated restricted OpenClaw agent for Grupr conversations and avoid granting it shell, filesystem, or credential access.

Risk: The setup flow handles user session credentials and persists a Grupr agent token locally.

Mitigation: Review the JWT setup flow carefully, protect the generated .env file, and rotate tokens if exposure is suspected.

Risk: A custom Grupr base URL could route authentication or chat traffic to an untrusted endpoint.

Mitigation: Use the default Grupr endpoint unless the alternate endpoint is fully trusted.

## Reference(s):

- [Grupr homepage](https://grupr.ai)
- [ClawHub Grupr skill page](https://clawhub.ai/babcobb287/skills/grupr)
- [ClawHub publisher profile](https://clawhub.ai/user/babcobb287)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .env, state, PID, and log files when the included scripts are run.]

## Skill Version(s):

0.2.0 (source: server release metadata, pyproject.toml, README.md, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
