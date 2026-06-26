## Description: <br>
Get your banking going - Financial enablement and accounting platform for Bots, Agents, and OpenClaw with methods for agentic spending, purchases, consolidated accounts, and transaction guardrails across wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to connect an agent to CreditClaw payment rails, check wallet status and spending permissions, request top-ups, create payment links, and make purchases within owner-configured limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses JPMorgan-like branding while server evidence identifies the publisher as jononovo and the artifact describes CreditClaw services. <br>
Mitigation: Treat it as a third-party CreditClaw payment skill unless the publisher proves an official JPMorgan relationship. <br>
Risk: The skill can enable real agent spending through wallet, card, payment-link, and x402-related flows. <br>
Mitigation: Use a dedicated low-balance wallet, require human approval for purchases and top-ups, and set strict spending, category, and domain limits. <br>
Risk: CREDITCLAW_API_KEY functions like a payment credential for authenticated CreditClaw API requests. <br>
Mitigation: Store the key only in a secure secrets manager or environment variable and send it only to https://creditclaw.com/api/* endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jononovo/jpmorgan) <br>
- [CreditClaw Homepage](https://creditclaw.com) <br>
- [CreditClaw Skill Reference](https://creditclaw.com/skill.md) <br>
- [CreditClaw Heartbeat Reference](https://creditclaw.com/heartbeat.md) <br>
- [CreditClaw Skill Metadata](https://creditclaw.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CREDITCLAW_API_KEY for authenticated CreditClaw API requests.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata); artifact frontmatter reports 2.0.11 and skill.json reports 2.0.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
