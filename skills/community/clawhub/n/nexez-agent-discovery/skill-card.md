## Description:

Use when a user explicitly asks to discover, compare, shortlist, book, buy, or negotiate products or services through Nexez or the Nexez marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexez](https://clawhub.ai/user/nexez)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find, compare, shortlist, and initiate safe Nexez marketplace actions for products or services. It supports discovery, checkout, booking, and negotiation workflows while requiring approval before seller-facing or payment-related side effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unrestricted NEXEZ_BASE_URL override could redirect checkout, negotiation, or contact details to an unintended endpoint.

Mitigation: Before installing or using side-effecting flows, check that NEXEZ_BASE_URL is unset or points to the intended Nexez endpoint.

Risk: Checkout, negotiation, contact sharing, payment handoff, or booking actions can create external commitments or expose buyer information.

Mitigation: Use dry-run or validation tools when available and require explicit approval that names the business, offer, data being sent, destination, and exact action before proceeding.

Risk: Listings may omit price, refund, availability, credential, or service-area details that are important for a safe decision.

Mitigation: Disclose missing details, preserve hard user constraints, and pause or decline emergency, regulated, or high-risk flows when proof or safe handoff details are insufficient.

## Reference(s):

- [Nexez Agent Discovery Skill Page](https://clawhub.ai/nexez/skills/nexez-agent-discovery)
- [Nexez Homepage](https://nexez.ai)
- [Nexez Endpoint Contract](references/endpoint-contract.md)
- [Nexez Discovery Rubric](references/discovery-rubric.md)
- [Nexez Skill Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Concise Markdown recommendations with structured shortlist details, missing-information notes, and approval prompts before side effects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Nexez public endpoints or typed OpenClaw tools; validates checkout or negotiation with dry-run behavior when available.]

## Skill Version(s):

0.1.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
