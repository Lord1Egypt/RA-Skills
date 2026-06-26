## Description: <br>
Helps users set up a Telegram channel so multiple OpenClaw bots can chat with each other and with friends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moon-frost](https://clawhub.ai/user/Moon-frost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to configure Telegram channels, bot privacy settings, administrator permissions, channel binding, and persistent channel rules for multi-bot conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bots in the configured channel may be able to read channel messages. <br>
Mitigation: Use a dedicated private channel, get participant consent, and avoid sharing sensitive messages. <br>
Risk: Broad administrator permissions can expose more channel control than the setup requires. <br>
Mitigation: Grant only the minimum Telegram administrator permissions needed for the bots to send and read messages. <br>
Risk: Forwarding channel messages to third-party ID-helper bots can expose message content or metadata. <br>
Mitigation: Avoid forwarding sensitive messages to ID-helper bots and verify channel IDs through trusted methods when possible. <br>
Risk: Persisted AGENTS.md channel rules can keep the behavior active after the user no longer wants it. <br>
Mitigation: Remove or update the AGENTS.md rules when multi-bot channel behavior is no longer intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with step-by-step setup instructions and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language user guidance for Telegram and OpenClaw setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
