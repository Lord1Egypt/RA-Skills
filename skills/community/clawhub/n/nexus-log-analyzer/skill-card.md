## Description:

Parse and analyze application logs for patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to submit application logs or log-analysis queries to the NEXUS service and receive pattern analysis. It is suited for external agent workflows that can use HTTPS service calls with payment proof or supported HTTP payment protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted logs or queries are sent to an external paid NEXUS service.

Mitigation: Install only if that data transfer is acceptable for the intended logs and operating environment.

Risk: Logs may contain secrets, tokens, personal data, internal hostnames, or incident details.

Mitigation: Redact sensitive values before use.

Risk: Requests may incur per-request payment.

Mitigation: Use the sandbox or explicit payment controls where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-log-analyzer)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [NEXUS log analyzer endpoint](https://ai-service-hub-15.emergent.host/api/original-services/log-analyzer)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar payment information](https://ai-service-hub-15.emergent.host/api/mpp/stellar)
- [Stellar fee sponsorship](https://ai-service-hub-15.emergent.host/api/mpp/stellar/sponsor-info)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON response containing a string result from the service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HTTPS access to the NEXUS service and payment proof or supported payment credentials.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
