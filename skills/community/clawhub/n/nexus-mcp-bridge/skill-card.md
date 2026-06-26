## Description: <br>
Bridge to MCP servers - IPFS, GitHub, filesystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send paid requests to the NEXUS MCP bridge for IPFS, GitHub, and filesystem-oriented MCP services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid remote calls and payment proofs may be forwarded by an agent. <br>
Mitigation: Use sandbox testing where appropriate, confirm payment intent before live calls, and do not expose wallet keys or reusable payment credentials. <br>
Risk: Broad MCP routing to GitHub, IPFS, or filesystem-style services could expose sensitive prompts, repository context, or local file contents. <br>
Mitigation: Review each request before forwarding and avoid sending secrets, private repository data, or local file contents unless explicitly approved. <br>
Risk: Inputs are processed by the remote NEXUS service. <br>
Mitigation: Install and use the skill only when the user trusts NEXUS with the data being sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-mcp-bridge) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [NEXUS MCP bridge endpoint](https://ai-service-hub-15.emergent.host/api/original-services/mcp-bridge) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls] <br>
**Output Format:** [JSON object with a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a payment proof or payment credential and sends the input to the remote NEXUS API over HTTPS.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
