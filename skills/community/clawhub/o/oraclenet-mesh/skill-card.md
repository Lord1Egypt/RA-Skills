## Description: <br>
OracleNet is a mesh capability router for autonomous agents that helps agents discover, route, verify, or pay for external capabilities through ToolOracle's machine-readable mesh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tooloracle](https://clawhub.ai/user/tooloracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use OracleNet when an autonomous agent needs to route natural-language capability requests to external services for blockchain intelligence, market and macro data, GPU pricing, research, sanctions screening, verification metadata, or optional regulated-evidence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may send sensitive intent text to ToolOracle during external routing. <br>
Mitigation: Redact secrets, private keys, access tokens, wallet seeds, regulated personal data, customer data, and confidential business context before calling ToolOracle endpoints. <br>
Risk: Some routed capabilities may require wallet-backed x402 payment. <br>
Mitigation: Require explicit user approval before any paid route or wallet-backed x402 call. <br>


## Reference(s): <br>
- [ToolOracle homepage](https://tooloracle.io) <br>
- [OracleNet ClawHub listing](https://clawhub.ai/tooloracle/oraclenet-mesh) <br>
- [Primary discovery card](https://tooloracle.io/.well-known/agent.json) <br>
- [Live mesh snapshot](https://tooloracle.io/.well-known/agent-pulse) <br>
- [Capabilities and rules](https://tooloracle.io/.well-known/deal-capabilities.json) <br>
- [Pricing](https://tooloracle.io/.well-known/pricing.json) <br>
- [Verification policy](https://tooloracle.io/.well-known/verification-policy.json) <br>
- [Do-not-contact policy](https://tooloracle.io/.well-known/do-not-contact.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and endpoint URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to external ToolOracle endpoints; route responses are interpreted by the calling agent.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
