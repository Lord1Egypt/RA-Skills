## Description:

PayClaw provides an MCP server that lets agents declare a UCP-compatible identity and request human-approved single-use virtual Visa cards for purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[payclawinc](https://clawhub.ai/user/payclawinc)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an AI agent to PayClaw for UCP identity declaration and human-approved payment flows at merchants. The skill is intended for agents that need to identify themselves before browsing, searching, or checking out.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is payment-related and can support agent-initiated purchase flows.

Mitigation: Use a restricted environment, require explicit human approval for purchases, and verify consent-key revocation or removal before operational use.

Risk: Installation runs the current unpinned @payclaw/mcp-server npm release, which can change after review.

Mitigation: Confirm npm package provenance and pin or otherwise control the reviewed package version before deployment.

## Reference(s):

- [PayClaw](https://payclaw.io)
- [PayClaw for Merchants](https://payclaw.io/merchants)
- [PayClaw Trust & Verification](https://payclaw.io/trust)
- [PayClaw API endpoint](https://api.payclaw.io)
- [npm: @payclaw/mcp-server](https://www.npmjs.com/package/@payclaw/mcp-server)
- [Universal Commerce Protocol](https://ucp.dev)
- [Protocol spec: ucp-agent-badge](https://github.com/payclaw/ucp-agent-badge)
- [GitHub: badge-server](https://github.com/payclaw/badge-server)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, API Calls]

**Output Format:** [Markdown with JSON configuration snippets, tool names, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+ and npx; configures the @payclaw/mcp-server package with PAYCLAW_API_URL.]

## Skill Version(s):

0.7.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
