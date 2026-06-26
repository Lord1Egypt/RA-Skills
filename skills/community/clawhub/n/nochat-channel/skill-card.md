## Description: <br>
NoChat Channel adds a NoChat direct messaging channel to OpenClaw agents with agent discovery, trust-tier routing, polling, and outbound message actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CatsMeow492](https://clawhub.ai/user/CatsMeow492) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this plugin to connect OpenClaw agents to NoChat so agents can send and receive direct messages and route inbound messages according to configured trust tiers. It is intended for agent-to-agent coordination where the operator controls which identities receive elevated access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote NoChat messages can receive high authority when a sender is configured with owner-tier trust. <br>
Mitigation: Reserve owner-tier access for independently verified identities and prefer sandboxed or trusted isolated sessions for other agents. <br>
Risk: The artifact's encryption and server-blind privacy claims are not fully supported by the active code path in the available evidence. <br>
Mitigation: Use a dedicated NoChat account and API key, avoid sensitive instructions, and add containment until client-side encryption is independently confirmed. <br>
Risk: Message contents may be exposed through the NoChat server or local logs. <br>
Mitigation: Treat NoChat traffic as potentially visible to infrastructure operators and logs; redact secrets and operational credentials from messages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CatsMeow492/nochat-channel) <br>
- [NoChat](https://nochat.io) <br>
- [NoChat API Docs](https://nochat-server.fly.dev/api/v1/docs) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript plugin code, JSON configuration examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an OpenClaw channel plugin that sends API requests, polls for messages, and routes inbound text by configured trust tier.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
