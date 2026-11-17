## Description:

Guides developers through validating, publishing, and testing an external x402 service listing in the Nevermined Agent Services Catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevermined-io](https://clawhub.ai/user/nevermined-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and service operators use this skill to assess whether an external x402 endpoint is routable, publish its listing, and verify paid access through the Nevermined Router. It also explains curated listing claims and credit eligibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags external requests as an environment-use concern, and scan coverage is incomplete, including degraded tool-misuse analysis.

Mitigation: Review the connected services and requested actions before execution, and inspect any behavior that has not been reviewed.

Risk: The direct-wallet validation can send real USDC, and the workflow uses Nevermined API credentials and a wallet private key.

Mitigation: Prefer the sandbox while validating; use a throwaway wallet with a low payment cap, protect credentials as secrets, and confirm the endpoint, amount, and network before paying.

## Reference(s):

- [Nevermined Catalog overview](https://nevermined.ai/docs/products/catalog/overview)
- [Direct wallet payment guide](references/direct-wallet-pay.md)
- [Catalog listing and promotion guide](references/list-and-promote.md)
- [Claiming listings and credits](references/claim-and-credits.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with shell commands, HTTP requests, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phased workflow for validating and publishing x402 catalog listings.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
