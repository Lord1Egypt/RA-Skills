## Description: <br>
Connects OpenClaw agents to iMessage, RCS, and SMS through Claw Messenger's managed relay server using API key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demegire](https://clawhub.ai/user/demegire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure OpenClaw agents for sending and receiving iMessage, RCS, and SMS messages without local Apple hardware or a phone. It is intended for messaging workflows that can tolerate a managed relay service and require careful handling of API keys, recipient policies, and billing exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive cm_live API key that authorizes messaging for the account. <br>
Mitigation: Keep .openclaw.json out of version control, restrict access to the key, and rotate it from the Claw Messenger dashboard if exposed. <br>
Risk: Messages and metadata pass through a third-party managed relay for delivery and billing. <br>
Mitigation: Review Claw Messenger privacy and billing terms before use, and avoid sending data that is not appropriate for that relay path. <br>
Risk: An agent with broad messaging access could send or respond to unintended recipients. <br>
Mitigation: Use pairing or allowlist DM policies for sensitive accounts and test with limited recipients before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/demegire/imessage-claw-messenger) <br>
- [Claw Messenger Homepage](https://clawmessenger.com) <br>
- [Claw Messenger Docs](https://clawmessenger.com/docs) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [npm package](https://www.npmjs.com/package/@emotion-machine/claw-messenger) <br>
- [Privacy Policy](https://clawmessenger.com/privacy) <br>
- [Pricing](https://clawmessenger.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, configuration fields, operational guidance, and agent-facing tool or command descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
