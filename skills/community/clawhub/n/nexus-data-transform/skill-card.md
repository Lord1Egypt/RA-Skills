## Description:

Convert data between JSON, CSV, XML, and YAML through the NEXUS remote data-transform service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert structured data between common interchange formats. The skill is suited for workflows that can send input data and payment proof to NEXUS for remote processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input data and payment proof or payment credentials are sent to the NEXUS remote service.

Mitigation: Avoid sending secrets, credentials, regulated data, or private documents unless the user trusts the provider and its retention claims.

Risk: Paid payment flows can incur charges or settle with the wrong asset or network if used without review.

Mitigation: Confirm the payment requirement, currency, network, and amount before retrying the paid request; use the sandbox flow for testing when appropriate.

Risk: Remote AI processing can return transformed data that is malformed or semantically different from the input.

Mitigation: Validate the converted output against the expected schema or downstream parser before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-data-transform)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API requests and shell command examples; the service response is JSON containing a result string.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or a supported x402/MPP/AP2 payment credential for paid requests.]

## Skill Version(s):

2.1.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
