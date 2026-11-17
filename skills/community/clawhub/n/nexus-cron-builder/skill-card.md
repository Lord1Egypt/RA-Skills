## Description:

Generate and explain cron expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate and explain cron expressions through the NEXUS remote API. It is suited to agent workflows that can provide payment proof or use the sandbox test path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user input and payment or transaction material to a third-party host.

Mitigation: Use it only if you trust NEXUS, avoid secrets or internal infrastructure details, and prefer sandbox testing before paid use.

Risk: The security summary notes unclear per-request approval or spending controls for external requests, payments, signed transactions, or mandates.

Mitigation: Require separate confirmation for every external request, payment, signed transaction, or mandate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-cron-builder)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Cron Builder API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/cron-builder)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Fee Sponsorship](https://ai-service-hub-15.emergent.host/api/mpp/stellar/sponsor-info)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object with a result string from the remote service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and NEXUS_PAYMENT_PROOF; paid requests are $0.05 with sandbox testing available.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
