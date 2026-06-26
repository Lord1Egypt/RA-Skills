## Description: <br>
Get a real email address for your AI agent. Create an inbox, send and receive email, with optional PGP encryption and DID verified identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karimibadr](https://clawhub.ai/user/karimibadr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to give an AI agent an email inbox, send and receive messages through the iClawd HTTP API, manage webhooks, and optionally use PGP encryption or DID identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provisions long-lived email credentials and the security evidence notes that it can instruct agents to expose those credentials through chat or full config sharing. <br>
Mitigation: Store API keys, config files, and PGP private keys locally with restrictive permissions or in a secret manager, and do not allow the agent to paste them into chat or external channels. <br>
Risk: An agent-controlled external email account can send messages, sign up for services, and contact recipients outside the local environment. <br>
Mitigation: Require explicit owner approval before external sends, service signups, or sharing content that may include personal information, credentials, or sensitive data. <br>
Risk: Webhook setup and inbox deletion can expose metadata externally or cause irreversible data loss. <br>
Mitigation: Require approval before webhook configuration or inbox deletion, verify webhook destinations, and prefer the reviewed ClawHub package over live remote instructions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/karimibadr/iclawd-email) <br>
- [iClawd Email website](https://iclawd.email) <br>
- [Skill and API documentation](https://iclawd.email/skill) <br>
- [MCP server endpoint](https://iclawd.email/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential handling guidance, JSON-RPC request examples, and local configuration instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
