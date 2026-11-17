## Description:

Provides agents with pay-per-call web search, page extraction, link checks, and other web utilities using Nano (XNO).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhyabi2](https://clawhub.ai/user/dhyabi2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve web content, search results, and site metadata through a metered web service without an account or API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous use could send Nano to service-provided payment addresses without a local spending limit or user confirmation.

Mitigation: Enforce a per-call spending cap, approve each recipient, and require explicit confirmation for every payment.

Risk: Submitted URLs and search queries may be disclosed to the third-party web service.

Mitigation: Submit only URLs and queries that are safe to share with paypercall.dev.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dhyabi2/skills/paypercall-web-tools)
- [Service tool manifest](https://extract.paypercall.dev/.well-known/x402)
- [Service delivery-proof endpoint](https://extract.paypercall.dev/api/v1/delivery-proof)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON containing tool-specific web results or payment-required details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the live service; calls after the free allowance may require Nano payment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
