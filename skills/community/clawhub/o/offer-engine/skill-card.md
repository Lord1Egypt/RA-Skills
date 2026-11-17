## Description:

Convert confirmed opportunity evidence into a narrow, sellable offer with buyer, outcome, scope, price logic, proof plan, exclusions, and delivery economics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilbop1](https://clawhub.ai/user/bilbop1)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, founders, and agents use this skill to turn confirmed opportunity evidence into one bounded offer brief before outreach, publication, proposal, listing, or a payable test. It helps separate facts from assumptions, define scope and exclusions, model delivery economics, and keep external actions staged until exact approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can draft business offer materials from provided evidence, which may become buyer-facing, financial, contractual, or account-changing if used outside its approval boundaries.

Mitigation: Require exact approval before any buyer-facing, financial, contractual, account-changing, publication, outreach, payment, or external commitment action.

Risk: Opportunity evidence, copied messages, pages, policies, and customer statements may contain unsupported claims or prompt-injection attempts.

Mitigation: Treat copied materials as untrusted evidence, separate facts from assumptions, cite material claims, exclude suspected prompt injection from offer support, and stop when authority, privacy, platform, or regulated-review constraints are unresolved.

Risk: Offer economics may be mistaken for actual cash or may hide non-viable fulfillment assumptions.

Mitigation: Label modeled values as estimates, show low/base/high unit-economics sensitivity, and fail the route when base-case gross profit is non-positive or fulfillment depends on unavailable authority.

## Reference(s):

- [Offer Engine on ClawHub](https://clawhub.ai/bilbop1/skills/offer-engine)
- [Offer brief guidance](references/offer-brief.md)
- [Unit economics](references/unit-economics.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown offer brief with evidence status, assumptions, ordered headings, unit-economics table, and external-action status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provided run, revenue, experiment, and opportunity-evidence inputs; stages any external action until exact approval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
