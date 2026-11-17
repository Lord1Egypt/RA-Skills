## Description:

Guides agents through pay-per-call music, image, and video generation using USDC over x402 without an account or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[havenagent](https://clawhub.ai/user/havenagent)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to generate music, images, or short videos when the agent cannot create the media natively. It explains catalog discovery, wallet-funded requests, job tracking, and delivery through Haven's MCP server or an x402 v2 client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent with a funded local wallet can spend real USDC without approval for each call.

Mitigation: Keep mainnet spending disabled until the operator intentionally funds the wallet, and enforce low per-call and daily spend caps.

Risk: Installing the recommended MCP package with @latest may change executable behavior unexpectedly.

Mitigation: Pin and review the MCP package version before enabling spending.

Risk: Prompts and uploaded images are sent to Haven for processing.

Mitigation: Do not submit secrets, regulated data, or private media unless the provider is approved for that use.

Risk: Video outputs carry use restrictions accepted at purchase, including disclosure and redistribution obligations.

Mitigation: Review the current catalog terms before buying video; preserve AI disclosure and pass applicable restrictions to recipients.

## Reference(s):

- [Haven Media skill release](https://clawhub.ai/havenagent/skills/haven-media-x402)
- [Haven media catalog and current terms](https://api.havenagent.ai/x402/api/v1/catalog)
- [Haven MCP package](https://www.npmjs.com/package/@havenagent/mcp)
- [x402 protocol](https://x402.org)
- [Video use terms overview](artifact/references/use-terms.md)
- [Direct x402 HTTP flow](artifact/references/x402-http.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides requests for paid media files; generated media is delivered by Haven, not by this skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
