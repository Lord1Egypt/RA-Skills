## Description:

Builds offline payment-routing diagnostics, route matrices, retry and failover policies, rollout guardrails, and merchant-friendly planning briefs for payment, checkout, finance, and cross-border ecommerce teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, payment operations teams, finance stakeholders, and checkout product teams use this skill to prepare offline payment-routing strategy briefs, compare PSP or acquirer options, plan retry and failover rules, and package rollout guardrails for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste raw card data, credentials, or unmasked payment records into planning prompts.

Mitigation: Use only masked, tokenized, or aggregated payment summaries and exclude credentials or sensitive payment records.

Risk: Routing recommendations could be adopted without adequate review and affect approval rates, costs, fraud exposure, or chargebacks.

Mitigation: Require finance, fraud, compliance, and named human production approval before applying any routing, retry, or failover policy.

Risk: Retry or failover plans can create duplicate-payment or inappropriate-retry exposure if applied broadly.

Mitigation: Limit retries to soft declines or recoverable technical failures, simulate policies on historical samples, and require idempotency-safe failover design.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/payment-route-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown planning brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline planning output; no live payment routing changes or payment data access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
