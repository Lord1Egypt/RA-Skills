## Description: <br>
WhatsApp bridge for OpenClaw that sends and receives messages, runs auto-reply agents, supports QR pairing, searches message history, and syncs contacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xs4m1337](https://clawhub.ai/user/0xs4m1337) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw agents to a local WhatsApp bridge for sending messages, handling QR pairing, replying to direct messages, searching history, and syncing contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge can read WhatsApp chats and contacts and send messages through the linked account. <br>
Mitigation: Link only an account approved for this use, protect the local data directory and logs, and know how to stop the service and unlink the WhatsApp device. <br>
Risk: The setup runs a persistent local auto-reply agent that can respond automatically. <br>
Mitigation: Start with auto-reply disabled or tightly allowlisted, review prompts and command behavior, and monitor worker logs before broader use. <br>
Risk: Installation depends on a remote shell installer referenced by the skill. <br>
Mitigation: Review the installer before running it and prefer a pinned or verified release. <br>
Risk: Configured webhooks can expose incoming message payloads to external services. <br>
Mitigation: Avoid untrusted webhook URLs and restrict webhook receivers to services approved for the message data handled by the bridge. <br>


## Reference(s): <br>
- [OpenClaw WhatsApp on ClawHub](https://clawhub.ai/0xs4m1337/openclaw-whatsapp) <br>
- [API reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, JSON, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service commands and configuration values for a persistent WhatsApp bridge.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
