## Description: <br>
Convert data between formats (JSON, CSV, XML, YAML). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert JSON, CSV, XML, and YAML data through a paid hosted NEXUS API when they have a payment proof or sandbox credential. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends input data and payment proof to a hosted NEXUS conversion service, and the security scan notes unclear per-request controls. <br>
Mitigation: Use only for data you are allowed to send to the provider, configure the agent to ask before each paid remote request, and avoid secrets, regulated data, private datasets, and sensitive business records unless you trust the provider and its retention claims. <br>
Risk: Payment flows can create real charges or settlement activity across supported crypto payment protocols. <br>
Mitigation: Use sandbox credentials for testing and require explicit approval, budget limits, and payment review before x402, MPP, AP2, XRPL, Cardano, or Stellar payments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-data-transform) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, structured data] <br>
**Output Format:** [JSON object containing a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or a supported payment credential; sends the input payload to the hosted NEXUS service.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
