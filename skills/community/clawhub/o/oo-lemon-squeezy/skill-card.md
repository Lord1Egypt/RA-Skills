## Description:

Connects an agent to Lemon Squeezy to read and manage customer, store, product, order, subscription, variant, and webhook data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a Lemon Squeezy account can use this skill to retrieve account and commerce data, create or update customers and webhooks, and delete webhooks through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to execute an online CLI installer that was not audited in this review.

Mitigation: Review and approve installation separately, use a verified CLI release, and check whether installation adds other agent skills.

Risk: Connecting the account gives OOMOL access to Lemon Squeezy account and business data; the hosted connector was not audited here.

Mitigation: Review the requested connection and its access before connecting, and confirm the exact effect of account changes before running write or destructive actions.

## Reference(s):

- [Lemon Squeezy](https://www.lemonsqueezy.com)
- [Lemon Squeezy API getting started](https://docs.lemonsqueezy.com/guides/developer-guide/getting-started)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-lemon-squeezy)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [Structured JSON results with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can contain customer and business account data.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
