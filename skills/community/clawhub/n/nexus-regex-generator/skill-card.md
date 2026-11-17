## Description:

Generate and explain regular expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to request regular expressions and explanations for pattern-matching tasks through the NEXUS remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regex prompts and payment metadata are sent to the NEXUS remote service over HTTPS.

Mitigation: Do not submit secrets, confidential code, or regulated data unless organizational policy permits this provider and data flow.

Risk: Normal use is paid and requires payment proof or a supported payment credential.

Mitigation: Use sandbox_test or narrowly scoped payment proofs for testing, and confirm payment controls before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-regex-generator)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Regex Generator API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/regex-generator)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Payment Information](https://ai-service-hub-15.emergent.host/api/mpp/stellar)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [JSON service response containing a generated regular expression and explanation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NEXUS payment proof or supported x402/MPP payment credential for normal use.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
