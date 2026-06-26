## Description: <br>
PayClaw lets an agent declare itself as an authorized actor at UCP-compliant merchants and request human-approved single-use virtual Visa cards without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[payclawinc](https://clawhub.ai/user/payclawinc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent declare PayClaw merchant identity and request human-approved single-use virtual cards for UCP-compatible purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent request payment capability through PayClaw, including single-use virtual cards. <br>
Mitigation: Confirm the merchant, item, amount, and purpose before approving any card issuance. <br>
Risk: A stored Consent Key may allow future PayClaw interactions through the configured agent environment. <br>
Mitigation: Review PayClaw controls for monitoring or revoking the stored Consent Key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/payclawinc/payclaw-io) <br>
- [PayClaw](https://payclaw.io) <br>
- [PayClaw merchant guide](https://payclaw.io/merchants) <br>
- [PayClaw trust and verification](https://payclaw.io/trust) <br>
- [UCP](https://ucp.dev) <br>
- [PayClaw MCP server package](https://www.npmjs.com/package/@payclaw/mcp-server) <br>
- [UCP agent badge protocol spec](https://github.com/payclaw/ucp-agent-badge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API Calls] <br>
**Output Format:** [Markdown instructions with JSON MCP configuration and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and Node.js 20+; purchase flows require human approval before card issuance.] <br>

## Skill Version(s): <br>
0.7.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
