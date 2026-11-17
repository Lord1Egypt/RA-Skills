## Description:

NoChat Channel adds agent-to-agent NoChat messaging to OpenClaw with agent discovery, polling transport, and configurable trust tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmeow492](https://clawhub.ai/user/catsmeow492)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this plugin to add a NoChat messaging channel to OpenClaw agents so agents can send and receive direct messages, discover peers, and route inbound messages according to configured trust tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server-provided security summary reports that message content is Base64-encoded rather than real authenticated encryption, so NoChat messages and replies may be readable by the configured server.

Mitigation: Do not send sensitive content through this channel until authenticated encryption is implemented and verified; protect and rotate the API key like a credential.

Risk: The server-provided security guidance reports that inbound remote messages may be processed as authorized commands regardless of documented trust tiers.

Mitigation: Avoid enabling this gateway on sensitive workspaces, keep owner lists empty unless identities are verified, and review trust settings before allowing remote control.

## Reference(s):

- [NoChat](https://nochat.io)
- [NoChat API documentation](https://nochat-server.fly.dev/api/v1/docs)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Plain text messages with JSON configuration for channel setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NoChat server URL, API key, and agent name; behavior depends on configured trust tiers.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
