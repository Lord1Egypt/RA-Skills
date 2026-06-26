## Description: <br>
Parse and analyze application logs for patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send application log text to the NEXUS service for pattern analysis and troubleshooting support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided logs and payment proof are sent to the hosted NEXUS API. <br>
Mitigation: Install only if you trust NEXUS, and redact tokens, credentials, personal data, internal hostnames, and sensitive stack traces before sending logs. <br>
Risk: Requests can incur paid API costs. <br>
Mitigation: Use sandbox mode for testing and review request costs before enabling paid requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-log-analyzer) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON object containing a result string, with Markdown usage guidance and curl examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF for paid use; sandbox_test is documented for free testing.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
