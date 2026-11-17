## Description:

PayClaw Badge lets MCP agents declare themselves as authorized actors and receive a UCP-compatible identity credential before interacting with merchants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[payclawinc](https://clawhub.ai/user/payclawinc)

### License/Terms of Use:

MIT

## Use Case:

External agent users and developers use this skill to configure an MCP server that requests PayClaw identity credentials, presents merchant-facing disclosure text, and reports badge presentation outcomes during shopping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default npx install path can execute a moving package target.

Mitigation: Use a pinned package version or a locally installed audited build before deployment.

Risk: The skill uses a PayClaw API key and may report merchant and badge outcome data.

Mitigation: Treat the API key and merchant/outcome data as sensitive, and review data sharing expectations before use.

Risk: Changing PAYCLAW_API_URL could redirect credential-bearing requests away from the official service.

Mitigation: Keep PAYCLAW_API_URL set only to the official HTTPS endpoint unless using an approved test environment.

Risk: Release metadata reports version 0.5.1, while server.json and runtime metadata still contain 0.4.0.

Mitigation: Confirm the deployed package and MCP server metadata match the intended release version.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/payclawinc/skills/payclaw-badge)
- [PayClaw Badge dashboard](https://payclaw.io/dashboard/badge)
- [PayClaw API endpoint](https://api.payclaw.io)
- [PayClaw trust and verification](https://payclaw.io/trust)
- [Merchant integration documentation](https://payclaw.io/merchants)
- [Universal Commerce Protocol](https://ucp.dev)
- [UCP identity extension specification](https://github.com/payclaw/ucp-agent-badge)
- [npm package: @payclaw/badge](https://www.npmjs.com/package/@payclaw/badge)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [MCP tool responses with human-readable disclosure text and structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+, npx, PAYCLAW_API_KEY, and an HTTPS PayClaw API URL for live use.]

## Skill Version(s):

0.5.1 (source: evidence.release.version and package.json; server.json and runtime metadata also contain 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
