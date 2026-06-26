## Description: <br>
Guides agents through the OpenClaw message send workflow for sending text, media, and structured payloads to WhatsApp, Telegram, Discord, Slack, and other chat channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RaphaCastelloes](https://clawhub.ai/user/RaphaCastelloes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help an agent prepare OpenClaw commands for selecting a chat channel, finding a recipient or group, and sending text, media, buttons, cards, or other supported message payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages, media, and structured payloads may be sent to external chat services or unintended recipients. <br>
Mitigation: Verify the channel, account, recipient or group ID, and message contents before sending; use dry-run mode for complex payloads. <br>
Risk: Shared message content can expose secrets, credentials, personal data, or confidential files. <br>
Mitigation: Avoid sending sensitive data unless the user has intentionally approved sharing it through the selected chat service. <br>


## Reference(s): <br>
- [Canais Suportados pelo OpenClaw](references/channels.md) <br>
- [Exemplos de Payloads JSON para Mensagens](references/payloads.md) <br>
- [Adaptive Cards JSON Schema](http://adaptivecards.io/schemas/adaptive-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes channel-specific target formats and dry-run guidance for complex payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
