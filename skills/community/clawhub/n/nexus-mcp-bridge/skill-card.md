## Description:

Bridge to MCP servers - IPFS, GitHub, filesystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send text queries through the NEXUS service to MCP-backed IPFS, GitHub, and filesystem bridge capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and payment proof data are sent to the third-party NEXUS service.

Mitigation: Send only data intended for NEXUS processing, avoid secrets and private repository contents, and use sandbox or tightly scoped payment credentials during testing.

Risk: Paid requests can incur charges or consume payment credentials.

Mitigation: Confirm payment requirements before retrying after HTTP 402 responses and prefer sandbox testing for initial validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-mcp-bridge)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [MCP Bridge API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/mcp-bridge)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON response or text returned by the NEXUS API, with markdown usage guidance and curl examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or an x402/MPP payment credential; sends the user's input to a third-party HTTPS API.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
